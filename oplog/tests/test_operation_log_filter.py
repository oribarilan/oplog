import logging
from unittest.mock import Mock
from oplog import OperationLogFilter
from oplog.tests.logged_test_case import OpLogTestCase


class OperationExceptionTest(Exception):
    pass


class TestOperationLogFilter(OpLogTestCase):
    def test_filter_recordIsVanillaLogRecord_false(self):
        mock_record = Mock(spec=logging.LogRecord)
        filter = OperationLogFilter()
        self.assertFalse(filter.filter(record=mock_record))
        
    def test_filter_recordHasOplogAttribute_true(self):
        mock_record = Mock(spec=logging.LogRecord)
        mock_record.oplog = Mock()
        filter = OperationLogFilter()
        self.assertTrue(filter.filter(record=mock_record))
        