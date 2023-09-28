import logging
from abc import abstractmethod, ABC

from oplog.exceptions import LogRecordMissingOperationException
from oplog.operation import Operation


class BaseOperationFormatter(logging.Formatter, ABC):
    def format(self, record) -> str:
        if hasattr(record, "oplog"):
            op: Operation = record.oplog
            return self.format_op(op=op)
        else:
            raise LogRecordMissingOperationException(
                "record does not have an oplog property"
            )

    @abstractmethod
    def format_op(self, op: Operation) -> str:  # pragma: no cover
        raise NotImplementedError("format_operation is required")
