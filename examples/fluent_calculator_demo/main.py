# Get the parent directory of the current file (project_demo folder)
import logging
import os
from pathlib import Path
import sys
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the path to the repository root directory (one level up)
repository_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

# Add the repository root directory to the Python path
sys.path.append(repository_root)

from oplog import Operated, Operation, OperationHandler # noqa: E402
from oplog.formatters import OplogCsvFormatter # noqa: E402


csv_op_handler = OperationHandler(
    handler=logging.FileHandler(filename=Path("oplogs.csv")), # <-- any logging handler
    formatter=OplogCsvFormatter(), # <-- use your own custom formatter, or built-in ones
)
logging.basicConfig(level=logging.INFO, handlers=[csv_op_handler])

class FluentCalculator:
    @Operated()
    def __init__(self):
        self.value = 0

    @Operated()
    def add(self, num):
        time.sleep(1)
        self.value += num
        return self

    @Operated()
    def subtract(self, num):
        time.sleep(1)
        self.value -= num
        return self

    @Operated()
    def divide(self, num):
        time.sleep(1)
        self.value /= num
        return self
    
    @Operated()
    def get_result(self):
        time.sleep(1)
        return self.value

with Operation("first_calc"):
    result1 = FluentCalculator().add(5).subtract(3).get_result()
    
with Operation("second_calc", suppress=True):
    result2 = FluentCalculator().add(5).divide(0).get_result()

