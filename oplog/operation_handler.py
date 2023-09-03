import logging
from typing import Optional

from oplog import OperationLogFilter


class OperationHandler(logging.Handler):
    def __init__(self, 
                 handler: logging.Handler, 
                 formatter: Optional[logging.Formatter] = None, 
                 *args, 
                 **kwargs):
        """A logging handler that only handles operation logs.

        Args:
            handler (logging.Handler): _description_
            formatter (Optional[logging.Formatter], optional): _description_.
                If None, the handler's formatter will be used.
        """
        super().__init__(*args, **kwargs)
        self.handler = handler
        self.addFilter(OperationLogFilter())
        if formatter:
            self.handler.setFormatter(formatter)

    def emit(self, record):
        self.handler.emit(record)