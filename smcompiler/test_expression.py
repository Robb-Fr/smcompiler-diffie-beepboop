"""
Unit tests for expressions.
Testing expressions is not obligatory.

MODIFY THIS FILE.
"""

from expression import Secret, Scalar


# Example test, you can adapt it to your needs.
def test_expr_construction():
    a = Secret(1)
    b = Secret(2)
    c = Secret(3)
    expr = (a + b) * c * Scalar(4) + Scalar(3)
    assert repr(expr) == "((Secret(1) + Secret(2)) * Secret(3) * Scalar(4) + Scalar(3))"
    expr_2 = (a + Scalar(3)) * b * c
    assert repr(expr_2) == "(Secret(1) + Scalar(3)) * Secret(2) * Scalar(3)"


def test_expr_equality():
    a = Secret(1)
    b = Secret()
    expr = (a + b) * Scalar(10) + Scalar(3)
    expr_2 = (a + b) * Scalar(10) + Scalar(3)
    assert expr != expr_2
