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

    def get_op(self, name: str) -> Operation:
        for op in self.ops:
            if op.name == name:
                return op
        raise LookupError(f"Operation with name {name} not found")

    def tearDown(self):
        Operation.factory_reset()
        return super().tearDown()

    
class LoggedAsyncTestCase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        self.handler = ListLoggingHandler()
        self.handler.logs = []

        logger.addHandler(self.handler)
    
    async def asyncTearDown(self):
        await super().asyncTearDown()


class OpLogAsyncTestCase(LoggedAsyncTestCase):
    @property
    def ops(self) -> List[Operation]:
        return [log.oplog for log in self.handler.logs]

    def get_op(self, name: str) -> Operation:
        for op in self.ops:
            if op.name == name:
                return op
        raise LookupError(f"Operation with name {name} not found")

    async def asyncTearDown(self):
        Operation.factory_reset()
        return super().tearDown()