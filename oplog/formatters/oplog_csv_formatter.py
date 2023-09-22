import logging
from oplog.exceptions import LogRecordMissingOperationException
from oplog.operation import Operation


class OplogCsvFormatter(logging.Formatter):
    def format(self, record) -> str:
        if hasattr(record, "oplog"):
            op: Operation = record.oplog
            csv_row = [
                f'"{op.start_time_utc_str}"',
                f'"{str(op.duration_ms)}"',
                f'"{op.name}"',
                f'"{op.correlation_id}"',
                f'"{op.result}"',
                f'"{str(op.exception_type)}"',
            ]
            return ','.join(csv_row)
        else:
            raise LogRecordMissingOperationException(
                "record does not have an oplog property"
            )
