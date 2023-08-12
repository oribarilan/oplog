import logging


class OperationLogFilter(logging.Filter):
    def filter(self, record):
        return hasattr(record, "oplog")
