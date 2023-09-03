import logging

from oplog.operation_log_filter import OperationLogFilter


class OperationHandler(logging.Handler):
    def __init__(self, handler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = handler
        self.addFilter(OperationLogFilter())

    def emit(self, record):
        self.handler.emit(record)