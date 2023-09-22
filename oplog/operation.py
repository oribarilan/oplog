import contextvars
import datetime
import inspect
import logging
import multiprocessing
import threading
import time
import traceback
import uuid
from contextlib import AbstractContextManager
from typing import Any, Dict, Iterable, Optional, Type, List, Final

from tqdm.auto import tqdm

from oplog.exceptions import (
    GlobalOperationPropertyAlreadyExistsException,
    OperationPropertyAlreadyExistsException
)

active_operation_stack = contextvars.ContextVar("active_operation_stack", default=[])


class Operation(AbstractContextManager):
    PROGRESS_INDENT: Final[str] = '--'
    global_props: Optional[Dict[str, Any]] = {}

    def __init__(self, name: str, suppress: bool = False) -> None:
        # Check if there's an active operation and assign parent-child relationship
        self.parent_op: Optional[Operation] = None
        self.child_ops: List[Operation] = []
        if active_operation_stack.get() and active_operation_stack.get()[-1]:
            self.parent_op = active_operation_stack.get()[-1]
            self.parent_op.child_ops.append(self)

        self.name = name
        self.suppress = suppress
        self.custom_props: Dict[str, Any] = dict()

        self.start_time_utc: Optional[datetime.datetime] = None
        self.end_time_utc: Optional[datetime.datetime] = None
        self.duration_ms: Optional[int] = None
        self.id = str(uuid.uuid4())
        self.result: Optional[str] = None
        self.exception_type: Optional[str] = None
        self.exception_msg: Optional[str] = None

        self._logger = self._get_caller_logger()
        self.logger_name = self._logger.name

        current_proc = multiprocessing.current_process()
        self.process_name = current_proc.name
        self.process_id = current_proc.pid
        self.thread_name = threading.current_thread().name
        self.thread_id = threading.get_ident()

        # inheritable props
        self.correlation_id: Optional[str] = None

        self._perf_start: Optional[float] = None

        # extension - progress
        self._progress: Optional[tqdm] = None

    @classmethod
    def factory_reset(cls) -> None:
        cls.global_props = {}

    @classmethod
    def _get_caller_logger(cls) -> logging.Logger:
        logger = None
        stack = inspect.stack()
        if len(stack) >= 3:
            # the caller is the 3rd frame in the stack
            caller_frame = stack[2]
            if len(caller_frame) >= 1:
                # the caller module is the 1st element in the caller frame
                caller_module = inspect.getmodule(caller_frame[0])
                if caller_module is not None:
                    logger = logging.getLogger(caller_module.__name__)
        return logger

    def __enter__(self) -> "Operation":
        self._start_time_utc = datetime.datetime.utcnow()
        # time format example: 2023-06-22 06:27:53.922633
        self.start_time_utc = self._start_time_utc.strftime("%Y-%m-%d %H:%M:%S.%f")
        self._perf_start = time.perf_counter_ns()

        self.set_inheritable_props()

        # Push the current operation onto the stack
        active_operation_stack.set(active_operation_stack.get([]) + [self])

        return self

    def set_inheritable_props(self) -> None:
        if self.parent_op is not None:
            self.correlation_id = self.parent_op.correlation_id
        else:
            self.correlation_id = str(uuid.uuid4())

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.end_time_utc = datetime.datetime.utcnow()
        perf_end = time.perf_counter_ns()
        self.duration_ms = round((perf_end - self._perf_start) / 1_000_000)

        # Pop the current operation off the stack
        current_stack = active_operation_stack.get([])
        if current_stack:
            current_stack.pop()
            active_operation_stack.set(current_stack)

        is_success = exc_type is None
        if is_success:
            result = "Success"
            tb = ""
        else:
            result = "Failure"
            self.exception_type = exc_type.__name__
            self.exception_msg = str(exc_value)
            tb = traceback.extract_tb(exc_tb, limit=10).format()

        self.result = result
        self.traceback = tb
        level = logging.INFO if is_success else logging.ERROR
        self.log_level = logging.getLevelName(level)

        self._logger.log(level=level, msg="operation logged", extra={"oplog": self})

        self._progressive_exit()

        # this will either suppress (if configured) or no,
        # in case an error was thrown in context
        return self.suppress

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Operation):
            return other.id == self.id
        return False

    def add(self, prop_name: str, value: Any) -> None:
        self._add_custom_prop(property_name=prop_name, value=value)

    @classmethod
    def add_global(cls, prop_name: str, value: Any) -> None:
        cls._validate_type(value=value, expected_types=(str, int, float, bool))
        cls._add_global_prop(property_name=prop_name, value=value)

    @staticmethod
    def _validate_type(value: Any, expected_types: Iterable[Type]):
        if not any(isinstance(value, t) for t in expected_types):
            expected_types_str = " or ".join(str(t) for t in expected_types)
            raise TypeError(f"Expected {expected_types_str}, but got {type(value)}")

    def add_multi(self, bag: Dict[str, Any]) -> None:
        for prop_name in bag:
            self.add(prop_name=prop_name, value=bag[prop_name])

    def _add_custom_prop(self, property_name: str, value: Any) -> None:
        if property_name in self.custom_props:
            raise OperationPropertyAlreadyExistsException(
                op_name=self.name, prop_name=property_name
            )
        self.custom_props[property_name] = value

    @classmethod
    def _add_global_prop(cls, property_name: str, value: Any) -> None:
        if property_name in cls.global_props:
            raise GlobalOperationPropertyAlreadyExistsException(prop_name=property_name)
        cls.global_props[property_name] = value

    def progressive(self, total: Optional[int] = None):
        """
        Makes the operation progressive, meaning it will display a progress bar.
        Note that the progress bar may not be displayed correctly in some IDEs
        (but will work in the terminal, notebooks, etc.).

        :param total: the maximum number of steps expected for the operation to complete
        :return: the operation itself (fluent syntax)
        """
        pop: Operation = self.parent_op  # to eliminate private attribute access warning
        pbar_desc = self.name
        is_child_of_progressive = pop._progress if pop else None
        if is_child_of_progressive:
            indent = len(active_operation_stack.get()) * self.PROGRESS_INDENT
            pbar_desc = f'{indent} {pbar_desc}'
        self._progress = tqdm(
            total=total,
            desc=pbar_desc,
            leave=not is_child_of_progressive
        )
        return self

    def progress(self, n: Optional[int] = 1):
        if self._progress is not None:
            self._progress.update(n)

    def _progressive_exit(self):
        if self._progress is not None:
            if self.result != "Success":
                self._progress.update(self._progress.total - self._progress.n)
            self._progress.close()

    def __repr__(self):
        return f"<Operation name={self.name}>"
