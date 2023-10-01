import datetime
import inspect
import logging
import multiprocessing
import threading
import time
import traceback
import uuid
from contextlib import AbstractContextManager
from contextvars import ContextVar
from typing import Any, Dict, Iterable, Optional, Type, List, Union, Callable

from oplog.exceptions import (
    GlobalOperationPropertyAlreadyExistsException,
    OperationPropertyAlreadyExistsException, OperationIsAlreadyDisplayingException
)
from oplog.operation_progress import OperationProgress
from oplog.operation_step import OperationStep
from oplog.spinner import Spinner

active_operation_stack: ContextVar[List['Operation']] = (
    ContextVar("active_operation_stack", default=[])
)


class Operation(AbstractContextManager):
    global_props: Dict[str, Any] = {}
    _serializer: Optional[Callable[['Operation'], str]] = None

    @classmethod
    def config(cls, serializer: Callable[['Operation'], str]) -> None:
        """
        Configure global behavior of all operations.

        :param serializer: A function that receives an operation
        and returns a string, to be formatted where relevant.
        :return:
        """
        # Any attributes that are set here should be cleaned in `factory_reset`
        cls._serializer = serializer

    def __init__(self,
                 name: str,
                 suppress: bool = False,
                 on_start: bool = False) -> None:
        """
        Initialize a new operation, to be used as a context manager,
        and create a context-rich operation log, to be handled by
         `oplog.handlers.OperationLogHandler`.
        :param name: The name of the operation.
        :param suppress: if True, the context manager will suppress
        any exception thrown in the context. Otherwise, the exception
        will be raised. Default is False. Operation metadata will be set properly
        regardless of this flag (e.g., failed operation).
        :param on_start: if True, the operation will be logged on start
        (as well as on exit).
        """
        # Check if there's an active operation and assign parent-child relationship
        self.parent_op: Optional[Operation] = None
        self.child_ops: List[Operation] = []
        if active_operation_stack.get() and active_operation_stack.get()[-1]:
            self.parent_op = active_operation_stack.get()[-1]
            self.parent_op.child_ops.append(self)

        self.name = name
        self.suppress = suppress
        self._on_start = on_start
        self.custom_props: Dict[str, Any] = dict()

        self.start_time_utc: Optional[datetime.datetime] = None
        self.end_time_utc: Optional[datetime.datetime] = None
        self.start_time_utc_str: Optional[str] = None
        self.end_time_utc_str: Optional[str] = None
        self.duration_ms: Optional[int] = None
        self.duration_ns: Optional[int] = None
        self.id = str(uuid.uuid4())
        self.step: Optional[OperationStep] = None
        self.is_successful: Optional[bool] = None
        self.result: Optional[str] = None
        self.exception_type: Optional[str] = None
        self.exception_msg: Optional[str] = None

        self._logger = self._get_caller_logger()
        self.logger_name = self._logger.name
        self.log_level: Optional[str] = None

        current_proc = multiprocessing.current_process()
        self.process_name = current_proc.name
        self.process_id = current_proc.pid
        self.thread_name = threading.current_thread().name
        self.thread_id = threading.get_ident()

        # inheritable props
        self.correlation_id: Optional[str] = None

        self._perf_start: Optional[float] = None

        # extension - progress
        self._progress: Optional[OperationProgress] = None
        self._spinner: Optional[Spinner] = None

    def is_displaying(self) -> bool:
        has_pbar = self._progress is not None and self._progress.is_displaying()
        has_spinner = self._spinner is not None
        return has_pbar or has_spinner

    @staticmethod
    def get_num_displaying_ancestors() -> int:
        displaying_ancestors = [op._progress for op in active_operation_stack.get()
                                if op.is_displaying()]
        return len(displaying_ancestors)

    @classmethod
    def factory_reset(cls) -> None:
        cls.global_props = {}
        cls._serializer = None

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

        if logger is None:
            logger = logging.getLogger()
        return logger

    def __str__(self):
        if self._serializer:
            return self.__class__._serializer(self)

        msg = (f"{self.start_time_utc_str} ({self.duration_ms}ms): "
               f"[{self.name} / {self.result}]")
        return msg

    def __enter__(self) -> "Operation":
        if self._spinner is not None:
            if self.parent_op is not None and self.parent_op._spinner is not None:
                self.parent_op._spinner.pause()
            self._spinner.start()

        self.start_time_utc = datetime.datetime.utcnow()
        # time format example: 2023-06-22 06:27:53.922633
        self.start_time_utc_str = self.start_time_utc.strftime("%Y-%m-%d %H:%M:%S.%f")
        self._perf_start = time.perf_counter_ns()

        self.step = OperationStep.START

        self.set_inheritable_props()

        # Push the current operation onto the stack
        active_operation_stack.set(active_operation_stack.get([]) + [self])

        if self._on_start:
            self._logger.log(
                level=logging.INFO,
                msg=str(self),
                extra={"oplog": self}
            )

        return self

    def set_inheritable_props(self) -> None:
        if self.parent_op is not None:
            self.correlation_id = self.parent_op.correlation_id
        else:
            self.correlation_id = str(uuid.uuid4())

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.end_time_utc = datetime.datetime.utcnow()
        self.end_time_utc_str = self.end_time_utc.strftime("%Y-%m-%d %H:%M:%S.%f")

        perf_end = time.perf_counter_ns()
        self.duration_ms = round((perf_end - self._perf_start) / 1_000_000)
        self.duration_ns = round(perf_end - self._perf_start)

        self.step = OperationStep.END

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

        self.is_successful = is_success
        self.result = result
        self.traceback = tb
        level = logging.INFO if is_success else logging.ERROR
        self.log_level = logging.getLevelName(level)

        self._logger.log(
            level=level,
            msg=str(self),
            extra={"oplog": self}
        )

        if self._spinner is not None:
            self._spinner.terminate()
            if self.parent_op is not None and self.parent_op._spinner is not None:
                self.parent_op._spinner.resume()

        if self._progress is not None:
            self._progress.exit(is_successful=self.is_successful)

        # this will either suppress (if configured) or no,
        # in case an error was thrown in context
        return self.suppress

    def __hash__(self):  # pragma: no cover
        return hash(self.id)

    def __eq__(self, other):  # pragma: no cover
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

    def __repr__(self):  # pragma: no cover
        return f"<Operation name={self.name}>"

    def progressable(self,
                     iterations: Optional[Union[int, float]] = None,
                     with_pbar: bool = True) -> 'Operation':
        """
        Context manager extension that makes the operation progress-able.
        This adds progress properties to the operation,
        and also (optionally) displays a progress bar.
        Progress is reported using the `.progress()` method.
        :param iterations: Optional. estimated number of iterations, if known
        :param with_pbar: if True, a progress bar will be displayed.
        :return:
        """
        if self.is_displaying():
            raise OperationIsAlreadyDisplayingException(op=self)

        self._progress = OperationProgress(
            iterations=iterations,
            pbar_descriptor=self.name if with_pbar else None,
            nest_level=self.get_num_displaying_ancestors(),
        )
        return self

    def get_progress(self) -> Optional[OperationProgress]:
        return self._progress

    def progress(self, n: Union[int, float] = 1):
        if self._progress is not None:
            self._progress.progress(n)
        else:
            raise AttributeError("Operation is not progressable")

    def spinnable(self, disable: bool = False, cycle: Optional[List[str]] = None):
        """
        A context manager that displays a spinner while the operation is running.
        :param disable: if True, the spinner will not be displayed.
        :param cycle: a list of strings, each representing a spinner frame.
        """
        if self.is_displaying():
            raise OperationIsAlreadyDisplayingException(op=self)

        cursor_offset = self.compute_cursor_offset()

        self._spinner = Spinner(desc=self.name,
                                cycle=cycle,
                                disable=disable,
                                total_nest_level=self.get_num_displaying_ancestors(),
                                cursor_offset=cursor_offset)
        return self

    def compute_cursor_offset(self) -> int:
        # tqdm assumes that the cursor is at the first line
        # spinner assumes that the cursor is at last line
        cursor_offset = 0
        if self.parent_op and self.parent_op.is_displaying():
            if self.parent_op._spinner is not None:
                # parent is spinner, move one down
                cursor_offset = 1
            elif self.parent_op._progress is not None and self.parent_op._progress.is_displaying():
                # parent is tqdm, move # of displaying ancestors down
                cursor_offset = len([op._progress for op in active_operation_stack.get() if op.is_displaying()])

        return cursor_offset
