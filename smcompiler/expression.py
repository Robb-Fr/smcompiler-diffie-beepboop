"""
Tools for building arithmetic expressions to execute with SMC.

Example expression:
>>> alice_secret = Secret()
>>> bob_secret = Secret()
>>> expr = alice_secret * bob_secret * Scalar(2)

MODIFY THIS FILE.
"""

import base64
import random
from typing import Optional, Tuple


ID_BYTES = 4


def gen_id() -> bytes:
    id_bytes = bytearray(random.getrandbits(8) for _ in range(ID_BYTES))
    return base64.b64encode(id_bytes)


class Expression:
    """
    Base class for an arithmetic expression.
    """

    def __init__(self, id: Optional[bytes] = None):
        # If ID is not given, then generate one.
        if id is None:
            id = gen_id()
        self.id = id

    def __add__(self, other):
        return AddOp(self, other)

    def __sub__(self, other):
        return SubOp(self, other)

    def __mul__(self, other):
        return MultOp(self, other)

    def __hash__(self):
        return hash(self.id)

    # Feel free to add as many methods as you like.


class Scalar(Expression):
    """Term representing a scalar finite field value."""

    def __init__(self, value: int, id: Optional[bytes] = None):
        self.value = value
        super().__init__(id)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.value)})"

    # def __hash__(self): ### seems to already be implemented by super class
    #     return hash(self.id)

    # Feel free to add as many methods as you like.


class Secret(Expression):
    """Term representing a secret finite field value (variable)."""

    def __init__(self, value: Optional[int] = None, id: Optional[bytes] = None):
        self.value = value
        super().__init__(id)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.value if self.value is not None else ''})"
        )

    # Feel free to add as many methods as you like.


# Feel free to add as many classes as you like.


class Op(Expression):
    def __init__(self, a: Expression, b: Expression):
        if not (isinstance(a, Expression) and isinstance(b, Expression)):
            raise ValueError("Can only construct operation between expressions")
        super().__init__()
        self.a = a
        self.b = b

    def get_operands(self) -> Tuple[Expression, Expression]:
        return self.a, self.b

    def scalar_operand(self) -> int:
        """Returns 0 if none of the operands is a scalar, 1 if the left one only is, 2 if the right one only is and 3 if both are. Could be written:
        if isinstance(self.a, Scalar) and not isinstance(self.b, Scalar):
            return 1
        elif not isinstance(self.a, Scalar) and isinstance(self.b, Scalar):
            return 2
        elif isinstance(self.a, Scalar) and isinstance(self.b, Scalar):
            return 3
        else:
            return 0
        """
        return int(isinstance(self.a, Scalar)) + (int(isinstance(self.b, Scalar)) << 1)


class AddOp(Op):
    def __repr__(self) -> str:
        return f"({repr(self.a)} + {self.b})"


class MultOp(Op):
    def __repr__(self) -> str:
        return f"{repr(self.a)} * {self.b}"


class SubOp(Op):
    def __repr__(self) -> str:
        return f"({repr(self.a)} - {self.b})"
