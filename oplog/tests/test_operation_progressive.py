from unittest.mock import patch
from tqdm.auto import tqdm

from oplog.operation import Operation

from oplog.tests.logged_test_case import OpLogTestCase


class OperationExceptionTest(Exception):
    pass


class TestOperation(OpLogTestCase):
    def test_operation_progressive_progressiveExitCalled(self):
        # arrange & act
        with patch.object(
                Operation,
                Operation._progressive_exit.__name__,
                return_value=None) as mock_progressive_exit:
            with Operation(name="test_op").progressive():
                pass

            # assert
            mock_progressive_exit.assert_called_once()

    def test_operation_progressive_tqdmClosed(self):
        # arrange & act
        with patch.object(
                tqdm,
                tqdm.close.__name__,
                return_value=None) as tqdm_close_mock:
            with Operation(name="test_op").progressive():
                pass

            # assert
            tqdm_close_mock.assert_called_once()

    def test_operation_progressive_progress(self):
        # arrange & act
        with patch.object(
                tqdm,
                tqdm.close.__name__,
                return_value=None) as tqdm_close_mock:
            with Operation(name="test_op").progressive() as op:
                op.progress()

            # assert
            tqdm_close_mock.assert_called_once()
