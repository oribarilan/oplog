import logging
from oplog.core.operation import Operation

from oplog.formatters.verbose_oplog_line_formatter import \
    LogRecordMissingOperationException


class OplogCsvFormatter(logging.Formatter):
    def format(self, record):
        if hasattr(record, "oplog"):
            op: Operation = record.oplog
            csv_row = [
                op.start_time_utc,
                str(op.duration_ms),
                op.name,
                op.correlation_id,
                op.result,
                str(op.exception_type)
            ]
            return ','.join(csv_row)
        else:
            raise LogRecordMissingOperationException(
                "record does not have an oplog property"
            )