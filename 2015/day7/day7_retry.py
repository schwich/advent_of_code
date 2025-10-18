import re
import numpy as np

from typing import Any
from enum import auto, Enum, StrEnum

# <wire_id or signal> -> <wire_id or signal>
connect_pattern = re.compile(r"^([a-z][a-z]?|\d+)\s->\s([a-z][a-z]?|\d+)$")

# NOT <wire_id or signal> -> <wire_id or signal>
not_pattern = re.compile(r"^NOT\s([a-z][a-z]?)\s->\s([a-z][a-z]?)$")

# <wire_id or signal> <AND|OR|LSHIFT|RSHIFT> <wire_id or signal> -> <wire_id>
binary_pattern = re.compile(
    r"^([a-z][a-z]?|\d+)\s(?:AND|OR|LSHIFT|RSHIFT)\s([a-z][a-z]?|\d+)\s->\s([a-z][a-z]?)$"
)

# type WireId = str
# type Signal = WireId | np.uint16 | Gate


# class Wire:
#     source: Signal
#     destinations: list[Signal]

#     def signal_out(self):
#         if isinstance(self.source, np.uint16):


# class Gate:
#     output: np.uint16 | None


# class InstructionType(Enum):
#     NOT = "NOT"
#     AND = "AND"
#     OR = "OR"
#     LSHIFT = "LSHIFT"
#     RSHIFT = "RSHIFT"
#     CONNECT = auto()


# class BinaryGate(Gate):
#     input1: Any
#     input2: Any
#     output: Any


# class NotGate(Gate):
#     type = InstructionType.NOT


# class ConnectGate(Gate):
#     type = InstructionType.CONNECT
#     input1: Any
#     output: Any


# class TokenType(Enum):
#     WIRE_ID = auto()
#     SIGNAL = auto()
#     GATE = auto()


# class Token:
#     type: TokenType
#     value: Any

#     def __init__(self) -> None:
#         pass
