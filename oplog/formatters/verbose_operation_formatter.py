from oplog.operation_step import OperationStep

from oplog.formatters.base_operation_formatter import BaseOperationFormatter
from oplog.operation import Operation


class VerboseOperationFormatter(BaseOperationFormatter):
    def format_op(self, op: Operation) -> str:
        duration = f" ({op.duration_ms}ms)" if op.step == OperationStep.END else ""
        result = op.result if op.result else "started"
        msg = (f"{op.start_time_utc_str}{duration}: "
               f"[{op.name} / {result}]")
        if op.exception_type:
            msg += f" {op.exception_type}: {op.exception_msg}"

        if len(op.custom_props) > 0:
            msg += f" {op.custom_props}"

        if len(op.global_props) > 0:
            msg += f" {op.global_props}"

        return msg
