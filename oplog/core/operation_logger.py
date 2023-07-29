import logging
from oplog.core.operation import Operation


class OperationLogFilter(logging.Filter):
    def filter(self, record):
        return hasattr(record, "oplog")
