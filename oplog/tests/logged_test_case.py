import logging
from typing import List
import unittest

from oplog.core.operation import Operation


class ListLoggingHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.logs = []

    def emit(self, record):
        self.logs.append(record)


class LoggedTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        self.handler = ListLoggingHandler()
        self.handler.logs = []

        logger.addHandler(self.handler)

    def tearDown(self):
        super().tearDown()


class OpLogTestCase(LoggedTestCase):
    @property
    def ops(self) -> List[Operation]:
        return [log.oplog for log in self.handler.logs]
