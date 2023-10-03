import time
import unittest
from unittest.mock import patch, call

from oplog.spinner import Spinner


class TestSpinner(unittest.TestCase):
    @patch('sys.stderr')  # Mock stderr
    def test_spinner(self, mock_stderr):
        cycle = ["a", "b", "c", "d"]
        spinner = Spinner(desc="desc", cycle=cycle, interval=100)
        spinner.start()
        time.sleep(0.5)

        for frame in cycle:
            self.assertTrue(call(f'|── desc:     {frame}') in mock_stderr.write.call_args_list)

        spinner.terminate()


if __name__ == '__main__':
    unittest.main()
