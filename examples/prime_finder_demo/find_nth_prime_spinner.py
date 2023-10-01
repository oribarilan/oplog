import os
import sys
import time

import click

current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the path to the repository root directory (one level up)
repository_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

# Add the repository root directory to the Python path
sys.path.append(repository_root)

from oplog import Operated, Operation, OperationHandler  # noqa: E402
from oplog.formatters import CsvOperationFormatter  # noqa: E402


@click.command()
@click.argument('n', default=10, type=int)
def find_nth_prime(n: int) -> None:
    with Operation(name='op1').spinner():
        time.sleep(2)
        with Operation(name="op2").spinner(nesting_level=1):
            time.sleep(2)
            with Operation(name="op3").spinner(nesting_level=2):
                time.sleep(2)
            time.sleep(3)
        time.sleep(3)

if __name__ == '__main__':
    find_nth_prime()
