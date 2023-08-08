from contextlib import AbstractContextManager
import contextvars
import datetime
import inspect
import json
import logging
import multiprocessing
import threading
import time
import traceback
from typing import Any, Dict, Optional
import uuid
from oplog.core.constants import Constants

from oplog.core.exceptions import OperationPropertyAlreadyExistsException


active_operation_stack = contextvars.ContextVar("active_operation_stack", default=[])


class Operation(AbstractContextManager):
    # TODO Add support for global props
    # TODO add user support to extend inheritable props
    _global_props: Optional[Dict[str, str]] = None

    def __init__(self, name: str, suppress: bool = False) -> None:
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

        self.parent_op: Optional[Operation] = None
        self.child_ops: Optional[Operation] = []

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

        # safety measure
        if logger is None:
            return logging.getLogger()
        return logger

    def __enter__(self) -> "Operation":
        self._start_time_utc = datetime.datetime.utcnow()
        # time format example: 2023-06-22 06:27:53.922633
        self.start_time_utc = self._start_time_utc.strftime("%Y-%m-%d %H:%M:%S.%f")
        self._perf_start = time.perf_counter_ns()

        # Check if there's an active operation and assign parent-child relationship
        if active_operation_stack.get() and active_operation_stack.get()[-1]:
            self.parent_op = active_operation_stack.get()[-1]
            self.parent_op.child_ops.append(self)
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

        # this will either suprress (if configured) or no, in case an error was thrown in context
        return self.suppress

    def _is_too_big(self) -> bool:
        serialized_msg = self.serialize()
        # encode to utf-8 to get the size in bytes
        encoded_message = serialized_msg.encode("utf-8")
        message_kb = len(encoded_message) / 1024
        max_size_kb = 2
        return message_kb >= max_size_kb

    def serialize(self):
        props = self._get_property_bag()
        return json.dumps(props)

    def __hash__(self):
        return hash(self.op_id)

    def __eq__(self, other):
        if isinstance(other, Operation):
            return other.id == self.id
        return False

    def _get_main_props(self) -> Dict[str, Any]:
        main_props = dict()
        main_props[Constants.BASE_PROPS.NAME] = self.name
        main_props[Constants.BASE_PROPS.RESULT] = self.result
        main_props[Constants.BASE_PROPS.DURATION_MS] = self.duration_ms
        main_props[Constants.BASE_PROPS.EXCEPTION_TYPE] = self.exception_type
        main_props[Constants.BASE_PROPS.EXCEPTION_MSG] = self.exception_msg

        # TODO add support for global props
        # main_props['version'] = self.encoder.encode(self._version)
        return main_props

    def _get_property_bag(self):
        props = self._get_main_props()
        props["custom_props"] = self.custom_props
        props["meta_props"] = self.meta_props
        return props

    def add(self, prop_name: str, value: Any) -> None:
        if isinstance(value, Dict):
            raise TypeError(
                f"type {type(value)} is not supported for `{self.add.__name__}`. "
                f"Consider using `{self.add_multi.__name__}` or `{self.add_bag.__name__}`."
            )

        self._encode_and_add_custom_prop(property_name=prop_name, value=value)

    def add_bag(self, bag_prop_name: str, bag: Dict[str, Any]) -> None:
        # Adds a dictionary as a property
        encoded_bag = dict()
        for prop_name in bag:
            encoded_prop_name = prop_name
            encoded_bag[encoded_prop_name] = bag[encoded_prop_name]

        self._add_custom_prop(property_name=bag_prop_name, encoded_value=encoded_bag)

    def _encode_and_add_custom_prop(self, property_name: str, value: Any) -> None:
        encoded_value = value
        self._add_custom_prop(property_name=property_name, encoded_value=encoded_value)

    def _add_custom_prop(self, property_name: str, encoded_value: Any) -> None:
        if property_name in self.custom_props:
            raise OperationPropertyAlreadyExistsException(
                op_name=self.name, prop_name=property_name
            )
        self.custom_props[property_name] = encoded_value

    def pretty_print(self) -> str:
        pretty_string = f"{self.end_time_utc} [{self.meta_props[Constants.BASE_PROPS.LEVEL]}] - [{self.name}] {self.result}. Custom props: {self.custom_props}"
        if self.result != "Success":
            pretty_string += f" Exception type: {self.exception_type}, Exception msg: {self.exception_msg}."
        return pretty_string
