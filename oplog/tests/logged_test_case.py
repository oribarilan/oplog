import logging
from typing import List
import unittest

from oplog.core.operation import Operation


class ListLoggingHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.logs = []

    def emit(self, record):
        log_entry = self.format(record)
        self.logs.append(log_entry)
        print(log_entry)


class LoggedTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        self.handler = ListLoggingHandler()

        formatter = logging.Formatter("%(message)s")
        self.handler.setFormatter(formatter)
        self.handler.logs = []

        logger.addHandler(self.handler)

    def tearDown(self):
        super().tearDown()


class OpLogTestCase(LoggedTestCase):
    @property
    def ops(self) -> List[Operation]:
        return [Operation.deserialize(log) for log in self.handler.logs]
