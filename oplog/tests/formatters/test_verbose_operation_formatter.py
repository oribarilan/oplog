from oplog import Operation
from oplog.formatters import VerboseOperationFormatter
from oplog.tests.logged_test_case import OpLogTestCase


class VerboseOplogLineFormatterTestException(Exception):
    pass


class TestVerboseOperationFormatter(OpLogTestCase):
    def test_formatOp_operationWithCustomProperties(self):
        # arrange
        op_name = "test_operation"
        custom_prop_name = "some_custom_prop"
        custom_prop_value = "some_custom_value"
        with Operation(name=op_name) as op:
            op.add(custom_prop_name, custom_prop_value)
        formatter = VerboseOperationFormatter()

        # act
        log_line = formatter.format_op(op=op)

        # assert
        self.assertIn(custom_prop_name, log_line)
        self.assertIn(custom_prop_value, log_line)

    def test_formatOp_operationWithGlobalProperties(self):
        # arrange
        op_name = "test_operation"
        global_prop_name = "some_global_prop"
        global_prop_value = "some_global_value"
        with Operation(name=op_name) as op:
            op.add_global(global_prop_name, global_prop_value)
        formatter = VerboseOperationFormatter()

        # act
        log_line = formatter.format_op(op=op)

        # assert
        self.assertIn(global_prop_name, log_line)
        self.assertIn(global_prop_value, log_line)

    def test_formatOp_operationFailure(self):
        # arrange
        op_name = "test_operation"
        error_msg = "some error message"
        with Operation(name=op_name, suppress=True) as op:
            raise VerboseOplogLineFormatterTestException(error_msg)
        formatter = VerboseOperationFormatter()

        # act
        log_line = formatter.format_op(op=op)

        # assert
        self.assertIn(VerboseOplogLineFormatterTestException.__name__, log_line)
        self.assertIn(error_msg, log_line)
