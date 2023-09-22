from unittest.mock import patch
from tqdm.auto import tqdm

from oplog.operation import Operation
from oplog.operation_progress import OperationProgress, ProgressNotAvailableException

from oplog.tests.logged_test_case import OpLogTestCase


class OperationExceptionTest(Exception):
    pass


class TestOperationProgress(OpLogTestCase):
    def test_progressable_exitCalled(self):
        # arrange & act
        with patch.object(
                OperationProgress,
                OperationProgress.exit.__name__,
                return_value=None) as mock_progressive_exit:
            with Operation(name="test_op").progressable():
                pass

            # assert
            mock_progressive_exit.assert_called_once()

    def test_progressable_tqdmClosed(self):
        # arrange & act
        with patch.object(
                tqdm,
                tqdm.close.__name__,
                return_value=None) as tqdm_close_mock:
            with Operation(name="test_op").progressable():
                pass

            # assert
            tqdm_close_mock.assert_called_once()

    def test_progress_withIterations_completionRateUpdated(self):
        # arrange & act
        with Operation(name="test_op").progressable(iterations=10) as op:
            op.progress()

            # assert
            self.assertEqual(op.get_progress().completion_ratio, 0.1)

    def test_progress_withIterations_completionRateUpdatedTwice(self):
        # arrange & act
        with Operation(name="test_op").progressable(iterations=10) as op:
            op.progress()
            op.progress()

            # assert
            self.assertEqual(op.get_progress().completion_ratio, 0.2)

    def test_progress_withIterations_completionRateUpdatedExplicitly(self):
        # arrange & act
        with Operation(name="test_op").progressable(iterations=10) as op:
            op.progress(n=5)

            # assert
            self.assertEqual(op.get_progress().completion_ratio, 0.5)

    def test_progress_withIterations_completionRateUpdatedOnExit(self):
        # arrange & act
        with Operation(name="test_op").progressable(iterations=10) as op:
            op.progress(n=5)

        # assert
        self.assertEqual(op.get_progress().completion_ratio, 1.0)

    def test_progress_withIterationsExceptionThrown_completionRateCaptured(self):
        # arrange & act
        with Operation(name="test_op", suppress=True).progressable(iterations=10) as op:
            op.progress(n=2)
            raise Exception()

        # assert
        self.assertEqual(op.get_progress().completion_ratio, 0.2)

    def test_progress_withoutIterationsExceptionThrown_completionRateUnknown(self):
        # arrange & act
        with Operation(name="test_op", suppress=True).progressable() as op:
            op.progress(n=2)
            raise Exception()

        # assert
        self.assertEqual(op.get_progress().completion_ratio, None)

    def test_progress_noIterationsNoPbar_progressThrowsException(self):
        # arrange & act
        with self.assertRaises(ProgressNotAvailableException):
            with Operation(name="test_op").progressable(with_pbar=False) as op:
                op.progress()
