import inspect
import logging
from unittest.mock import patch
from parameterized import parameterized
from oplog.core.exceptions import OperationPropertyAlreadyExistsException
from oplog.core.operation import Operation

from oplog.tests.logged_test_case import OpLogTestCase


class OperationExceptionTest(Exception):
    pass


class TestOperation(OpLogTestCase):
    def test_operation_loggerLogCalled(self):
        with patch.object(
            logging.Logger,
            logging.Logger.log.__name__,
            return_value=None) as mock_log:
            with Operation(name="test_op") as op:
                pass

        mock_log.assert_called_once_with(
            level=logging.getLevelName(op.log_level),
            msg="operation logged",
            extra={"oplog": op},
        )
        
    def test_operation_loggerIsOfTheCaller(self):
        expected_logger = logging.getLogger(inspect.getmodule(TestOperation).__name__)
        
        with Operation(name="test_op") as op:
                pass
        
        actual_logger = op._logger
        self.assertEqual(expected_logger, actual_logger)

    def test_operation_contextManagerLogged(self):
        with Operation(name="test_op"):
            pass

        assert len(self.ops) == 1

    @parameterized.expand(
        [
            ("Null Type", None),
            ("Bool Type", True),
            ("Int Type", 1),
            ("Float Type", 1.5),
            ("String type", "1"),
        ]
    )
    def test_add_customPropAdded(self, name, value):
        prop_name = "test_custom_prop"
        prop_value = value

        with Operation(name="test_op") as op:
            op.add(prop_name=prop_name, value=prop_value)

        self.assertEqual(len(self.ops), 1)

        op = self.get_op("test_op")
        self.assertIn(prop_name, op.custom_props)
        self.assertEqual(op.custom_props[prop_name], prop_value)

    def test_addGlobal_customPropAdded(self):
        prop_name = "test_global_prop"
        prop_value = 1
        Operation.add_global(prop_name=prop_name, value=prop_value)

        with Operation(name="test_op") as op:
            op.add(prop_name=prop_name, value=prop_value)

        self.assertEqual(len(self.ops), 1)

        op = self.get_op("test_op")
        self.assertIn(prop_name, op.global_props)
        self.assertEqual(op.global_props[prop_name], prop_value)

    def test_operation_add_valueIsDict_customPropsAdded(self):
        prop_name_1 = "test_custom_prop_1"
        prop_name_2 = "test_custom_prop_2"
        prop_value_1 = 1
        prop_value_2 = 2
        prop_bag = {
            prop_name_1: prop_value_1,
            prop_name_2: prop_value_2,
        }

        with Operation(name="test_op") as op:
            op.add_multi(bag=prop_bag)

        self.assertEqual(len(self.ops), 1)

        op = self.get_op("test_op")
        self.assertIn(prop_name_1, op.custom_props)
        self.assertEqual(op.custom_props[prop_name_1], prop_value_1)
        self.assertIn(prop_name_2, op.custom_props)
        self.assertEqual(op.custom_props[prop_name_2], prop_value_2)

    def test_operation_addMulti_customPropsAdded(self):
        prop_name_1 = "test_custom_prop_1"
        prop_name_2 = "test_custom_prop_2"
        prop_value_1 = 1
        prop_value_2 = 2
        prop_bag = {
            prop_name_1: prop_value_1,
            prop_name_2: prop_value_2,
        }
        prop_bag_name = "test_bag"

        with Operation(name="test_op") as op:
            op.add(prop_name=prop_bag_name, value=prop_bag)

        self.assertEqual(len(self.ops), 1)

        op = self.get_op("test_op")
        self.assertIn(prop_bag_name, op.custom_props)
        self.assertEqual(op.custom_props[prop_bag_name], prop_bag)

    def test_operation_exceptionThrownWitoutHandling_failedOperationLoggedExceptionReraised(self):  # noqa: E501
        with self.assertRaises(OperationExceptionTest):
            with Operation(name="test_op") as op:
                raise OperationExceptionTest("test exception")

        self.assertEqual(len(self.ops), 1)

        op = self.get_op("test_op")
        self.assertEqual(op.exception_type, "OperationExceptionTest")
        self.assertEqual(op.exception_msg, "test exception")
    
    def test_operation_exceptionThrownWitoutSuppression_failedOperationLoggedExceptionReraised(self):  # noqa: E501
        with self.assertRaises(OperationExceptionTest):
            with Operation(name="test_op", suppress=False) as op:
                raise OperationExceptionTest("test exception")

        self.assertEqual(len(self.ops), 1)

        op = self.get_op("test_op")
        self.assertEqual(op.exception_type, "OperationExceptionTest")
        self.assertEqual(op.exception_msg, "test exception")

    def test_operation_exceptionThrownWithSuppression_failedOperationLoggedFlowContinues(self):  # noqa: E501
        try:
            with Operation(name="test_op", suppress=True) as op:
                # obvious if to help IDE with "unreachable code"
                if (1 == 1):
                    raise OperationExceptionTest("test exception")
        except OperationExceptionTest:
            # for making this code intentional and explicit
            self.fail("exception should have been suppressed")

        self.assertEqual(len(self.ops), 1)

        op = self.get_op("test_op")
        self.assertEqual(op.exception_type, "OperationExceptionTest")
        self.assertEqual(op.exception_msg, "test exception")
        
    def test_operation_failureWithSuppression_exceptionLogged(self):
        with Operation(name="test_op", suppress=True) as op:
            raise OperationExceptionTest("test exception")

        self.assertEqual(len(self.ops), 1)

        op = self.get_op("test_op")
        self.assertEqual(op.exception_type, "OperationExceptionTest")
        self.assertEqual(op.exception_msg, "test exception")

    def test_operation_add_propertyExists_exceptionRaised(self):
        prop_name = "test_custom_prop"

        with self.assertRaises(OperationPropertyAlreadyExistsException):
            with Operation(name="test_op") as op:
                op.add(prop_name=prop_name, value=1)
                op.add(prop_name=prop_name, value=2)

    def test_operation_parentOperation_parentAndChildrenSet(self):
        with Operation(name="parent_op"):
            with Operation(name="child_op1"):
                pass

            with Operation(name="child_op2"):
                pass

        self.assertEqual(len(self.ops), 3)

        child_op1 = self.get_op("child_op1")
        child_op2 = self.get_op("child_op2")
        parent_op = self.get_op("parent_op")

        self.assertEqual(child_op1.parent_op, parent_op)
        self.assertEqual(child_op2.parent_op, parent_op)

        self.assertIn(child_op1, parent_op.child_ops)
        self.assertIn(child_op2, parent_op.child_ops)

    def test_operation_correlationId_correlationIdSet(self):
        with Operation(name="parent_op"):
            with Operation(name="child_op1"):
                pass

            with Operation(name="child_op2"):
                pass

        self.assertEqual(len(self.ops), 3)

        child_op1 = self.get_op("child_op1")
        child_op2 = self.get_op("child_op2")
        parent_op = self.get_op("parent_op")

        self.assertEqual(child_op1.correlation_id, parent_op.correlation_id)
        self.assertEqual(child_op2.correlation_id, parent_op.correlation_id)
