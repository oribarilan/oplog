from oplog.core.exceptions import OperationPropertyAlreadyExistsException
from oplog.core.operated import Operated
from oplog.core.operation import Operation

from oplog.tests.logged_test_case import OpLogTestCase


class OperatedTestClass:
    @Operated()
    def operated_method(self):
        pass
    
    @Operated("test_op")
    def operated_named_method(self):
        pass
    
    @staticmethod
    @Operated("test_op2")
    def operated_named_static_method():
        pass

class TestOperated(OpLogTestCase):
    # TODO the correct testing would be to mock Operation and to make sure the constructor is called with the correct arguments
    
    def test_operated_vanilla_underlyingOperationCreated(self):
        otc = OperatedTestClass()
        otc.operated_method()
        
        self.assertEqual(len(self.ops), 1)

        op = self.ops[0]
        self.assertEqual(op.name, "OperatedTestClass.operated_method")

    def test_operated_namedOp_underlyingOperationCreated(self):
        otc = OperatedTestClass()
        otc.operated_named_method()
        
        self.assertEqual(len(self.ops), 1)

        op = self.ops[0]
        self.assertEqual(op.name, "test_op")
    
    def test_operated_namedOpWithStaticMethod_underlyingOperationCreated(self):
        otc = OperatedTestClass()
        otc.operated_named_static_method()
        
        self.assertEqual(len(self.ops), 1)

        op = self.ops[0]
        self.assertEqual(op.name, "test_op2")
