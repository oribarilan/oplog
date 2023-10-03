import pytest
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the path to the repository root directory (one level up)
repository_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

# Add the repository root directory to the Python path
sys.path.append(repository_root)


from examples.fluent_calculator_demo.calc import FluentCalculator  # noqa: E402


@pytest.fixture
def calculator():
    return FluentCalculator()


def test_add(calculator):
    # act
    result = calculator.add(5).add(3).add(2).calc()
    # assert
    assert result == 10
