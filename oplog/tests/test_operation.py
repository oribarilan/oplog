from parameterized import parameterized
from oplog.operation import Operation

from oplog.tests.logged_test_case import LoggedTestCase, OpLogTestCase

class OperationExceptionTest(BaseException):
    pass


class TestOperation(OpLogTestCase):
    def test_operation_contextManagerLogged(self):
        with Operation(name='test_op') as op:
            pass
        
        assert len(self.ops) == 1
    
    @parameterized.expand([
        ("Null Type", None),
        ("Bool Type", True),
        ("Int Type", 1),
        ("Float Type", 1.5),
        ("String type", "1"),
    ])
    def test_operation_add_customPropAdded(self, name, value):
        prop_name = 'test_custom_prop'
        prop_value = value
        
        with Operation(name='test_op') as op:
            op.add(prop_name=prop_name, value=prop_value)
        
        self.assertEqual(len(self.ops), 1)
        
        op = self.ops[0]
        self.assertIn(prop_name, op.custom_props)
        self.assertEqual(op.custom_props[prop_name], prop_value)

    def test_operation_addDict_customPropsAdded(self):
        prop_name_1 = 'test_custom_prop_1'
        prop_name_2 = 'test_custom_prop_2'
        prop_value_1 = 1
        prop_value_2 = 2
        prop_bag = {
            prop_name_1: prop_value_1,
            prop_name_2: prop_value_2,
        }
        prop_bag_name = 'test_bag'
        
        with Operation(name='test_op') as op:
            op.add_bag(bag_prop_name=prop_bag_name, bag=prop_bag)
        
        self.assertEqual(len(self.ops), 1)
        
        op = self.ops[0]
        self.assertIn(prop_bag_name, op.custom_props)
        self.assertEqual(op.custom_props[prop_bag_name], prop_bag)