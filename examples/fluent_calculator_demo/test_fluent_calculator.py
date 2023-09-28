import pytest

from examples.fluent_calculator_demo.main import FluentCalculator


@pytest.fixture
def calculator():
    return FluentCalculator()


def test_add(calculator):
    # act
    result = calculator.add(5).add(3).add(2).calc()
    # assert
    assert result == 10
