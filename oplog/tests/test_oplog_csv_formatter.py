import csv
import logging
from unittest.mock import Mock

from oplog import Operation
from oplog.formatters import OplogCsvFormatter
from oplog.tests.logged_test_case import OpLogTestCase


class TestOplogCsvFormatter(OpLogTestCase):
    def test_format_operationNameContainsSeparator_internalSeparatorIsEscaped(self):
        # arrange
        separator = ","
        expected_num_columns = (
            self._get_num_columns_for_csv_formatted_operation("operation_name"))

        # act
        actual_num_columns = (
            self._get_num_columns_for_csv_formatted_operation(f"operation{separator}name"))

        # assert
        self.assertEquals(expected_num_columns, actual_num_columns)

    @staticmethod
    def _get_num_columns_for_csv_formatted_operation(operation_name: str) -> int:
        mock_record = Mock(spec=logging.LogRecord)
        mock_record.oplog = Operation(name=operation_name)
        formatter = OplogCsvFormatter()
        csv_str = formatter.format(record=mock_record)
        csv_reader = csv.reader(csv_str.splitlines(), delimiter=',')
        first_row = next(csv_reader)
        num_columns = len(first_row)
        return num_columns
