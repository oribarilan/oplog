import csv

from oplog import Operation
from oplog.formatters import CsvOperationFormatter
from oplog.tests.logged_test_case import OpLogTestCase


class TestCsvOperationFormatter(OpLogTestCase):
    def test_formatOp_operationNameContainsSeparator_internalSeparatorIsEscaped(self):
        # arrange
        separator = ","
        expected_num_columns = (
            self._get_num_columns_for_csv_formatted_operation("operation_name"))

        # act
        actual_num_columns = (
            self._get_num_columns_for_csv_formatted_operation(f"operation{separator}name"))

        # assert
        self.assertEqual(expected_num_columns, actual_num_columns)

    @staticmethod
    def _get_num_columns_for_csv_formatted_operation(operation_name: str) -> int:
        op = Operation(name=operation_name)
        formatter = CsvOperationFormatter()
        csv_str = formatter.format_op(op=op)
        csv_reader = csv.reader(csv_str.splitlines(), delimiter=',')
        first_row = next(csv_reader)
        num_columns = len(first_row)
        return num_columns
