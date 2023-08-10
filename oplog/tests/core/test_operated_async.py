import asyncio

from oplog.core.operated import Operated

from oplog.tests.logged_test_case import OpLogAsyncTestCase


class OperatedTestClass:
    @Operated("test_op_async")
    async def operated_async_method(self) -> str:
        await asyncio.sleep(0.1)
        return "success"

class TestOperatedAsync(OpLogAsyncTestCase):
    async def test_operated_asyncMethod_underlyingOperationCreated(self):
        otc = OperatedTestClass()
        
        success = await otc.operated_async_method()
        
        self.assertEqual(success, "success")
        self.assertEqual(len(self.ops), 1)
        op = self.ops[0]
        self.assertEqual(op.name, "test_op_async")