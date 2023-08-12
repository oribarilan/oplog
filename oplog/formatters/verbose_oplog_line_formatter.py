import logging
from oplog.core.operation import Operation


class LogRecordMissingOperationException(Exception):
    pass


class VerboseOplogLineFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        if hasattr(record, "oplog"):
            op: Operation = record.oplog
            msg = f"{op.start_time_utc} ({op.duration_ms}ms): [{op.name} / {op.result}]"
            if op.exception_type:
                msg += f" {op.exception_type}: {op.exception_msg}"
            
            if len(op.custom_props) > 0:
                msg += f" {op.custom_props}"
            
            if len(op.global_props) > 0:
                msg += f" {op.global_props}"
            
            return msg
        else:
            raise LogRecordMissingOperationException(
                "record does not have an oplog property"
            )
