from oplog.formatters.base_operation_formatter import BaseOperationFormatter
from oplog.operation import Operation


class CsvOperationFormatter(BaseOperationFormatter):
    def format_op(self, op: Operation) -> str:
        csv_row = [
            f'"{op.start_time_utc_str}"',
            f'"{str(op.duration_ms)}"',
            f'"{op.name}"',
            f'"{op.correlation_id}"',
            f'"{op.result}"',
            f'"{str(op.exception_type)}"',
        ]
        return ','.join(csv_row)
