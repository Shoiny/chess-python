# Example test file to show how pytest works.
# Run all tests from the project folder with:  python -m pytest
#
# pytest finds files named test_*.py and runs every function named test_*.
# Each test uses "assert": if the condition is False, the test fails (red).


def double(n):
    return n * 2


def test_double_positive_number():
    assert double(3) == 6


def test_double_zero():
    assert double(0) == 0


def test_double_negative_number():
    assert double(-4) == -8


# Real tests usually import the code they check from the project, e.g.:
#   from functions import get_pos_on_board
