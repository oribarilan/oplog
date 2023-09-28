import logging
from unittest.mock import Mock, patch

from oplog import Operation
from oplog.exceptions import LogRecordMissingOperationException
from oplog.formatters import BaseOperationFormatter
from oplog.tests.logged_test_case import OpLogTestCase


class MyTestOperationFormatter(BaseOperationFormatter):
    def format_op(self, op: Operation) -> str:
        return op.name


class TestBaseOperationFormatter(OpLogTestCase):
    def test_format_logRecordIsNotOplog_errorRaised(self):
        # arrange
        mock_record = Mock(spec=logging.LogRecord)
        formatter = MyTestOperationFormatter()

        # act
        with self.assertRaises(LogRecordMissingOperationException):
            formatter.format(record=mock_record)

    def test_format_callsFormatOp(self):
        # arrange
        formatter = MyTestOperationFormatter()
        op_name = "test_operation"
        mock_record = Mock(spec=logging.LogRecord)
        with patch.object(
                MyTestOperationFormatter,
                MyTestOperationFormatter.format_op.__name__,
                return_value=None) as format_op_mock:
            with Operation(name=op_name) as op:
                mock_record.oplog = op

            # act
            formatter.format(record=mock_record)

            # assert
            format_op_mock.assert_called_once_with(op=mock_record.oplog)

