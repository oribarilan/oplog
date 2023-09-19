import logging
from unittest.mock import Mock

from oplog import Operation
from oplog.formatters import VerboseOplogLineFormatter
from oplog.tests.logged_test_case import OpLogTestCase


class VerboseOplogLineFormatterTestException(Exception):
    pass


class TestVerboseOplogLineFormatter(OpLogTestCase):
    def test_format_operationWithCustomProperties(self):
        # arrange
        op_name = "test_operation"
        custom_prop_name = "some_custom_prop"
        custom_prop_value = "some_custom_value"
        mock_record = Mock(spec=logging.LogRecord)
        with Operation(name=op_name) as op:
            op.add(custom_prop_name, custom_prop_value)
        mock_record.oplog = op
        formatter = VerboseOplogLineFormatter()

        # act
        log_line = formatter.format(record=mock_record)

        # assert
        self.assertIn(custom_prop_name, log_line)
        self.assertIn(custom_prop_value, log_line)

    def test_format_operationWithGlobalProperties(self):
        # arrange
        op_name = "test_operation"
        global_prop_name = "some_global_prop"
        global_prop_value = "some_global_value"
        mock_record = Mock(spec=logging.LogRecord)
        with Operation(name=op_name) as op:
            op.add(global_prop_name, global_prop_value)
        mock_record.oplog = op
        formatter = VerboseOplogLineFormatter()

        # act
        log_line = formatter.format(record=mock_record)

        # assert
        self.assertIn(global_prop_name, log_line)
        self.assertIn(global_prop_value, log_line)

    def test_format_operationFailure(self):
        # arrange
        op_name = "test_operation"
        error_msg = "some error message"
        mock_record = Mock(spec=logging.LogRecord)
        with Operation(name=op_name, suppress=True) as op:
            raise VerboseOplogLineFormatterTestException(error_msg)
        mock_record.oplog = op
        formatter = VerboseOplogLineFormatter()

        # act
        log_line = formatter.format(record=mock_record)

        # assert
        self.assertIn(VerboseOplogLineFormatterTestException.__name__, log_line)
        self.assertIn(error_msg, log_line)

