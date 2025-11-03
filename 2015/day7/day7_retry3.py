import re
import pprint

from enum import StrEnum, auto, Enum
from typing import Any
from abc import abstractmethod, ABC

import numpy as np

# wire_id => source
WIRES = {}

# <wire_id or signal> -> <wire_id>
apply_pattern = re.compile(r"^([a-z][a-z]?|\d+)\s->\s([a-z][a-z]?|\d+)$")

# NOT <wire> -> <wire>
not_pattern = re.compile(r"^NOT\s([a-z][a-z]?)\s->\s([a-z][a-z]?)$")

# <wire_id or signal> <AND|OR|LSHIFT|RSHIFT> <wire_id or signal> -> <wire_id>
binary_pattern = re.compile(
    r"^([a-z][a-z]?|\d+)\s(?:AND|OR|LSHIFT|RSHIFT)\s([a-z][a-z]?|\d+)\s->\s([a-z][a-z]?)$"
)


class Wire:
    source: Wire | Gate | np.uint16

    def __init__(self, source) -> None:
        self.source = source

    def get_output(self) -> np.uint16:
        match source:
            case Wire() as wire:
                return wire.get_output()
            case Gate() as gate:
                return gate.get_output()
            case _:
                return self.source  # pyright: ignore[reportReturnType]

    def __repr__(self) -> str:
        return f"Wire({source=}, source_type={type(source)})"


class Gate(ABC):
    @abstractmethod
    def get_output(self) -> np.uint16:
        pass


class NotGate(Gate):
    source: Wire

    def __init__(self, source) -> None:
        super().__init__()
        self.source = source

    def get_output(self) -> np.uint16:
        return ~source.get_output()  # pyright: ignore[reportAttributeAccessIssue]


class BinaryGate(Gate):
    input_1: Wire
    input_2: Wire

    def __init__(self, input_1, input_2):
        self.input_1 = input_1
        self.input_2 = input_2


class AndGate(BinaryGate):
    def __init__(self, input_1, input_2) -> None:
        super.__init__(input_1, input_2)

    def get_output(self) -> np.uint16:
        return self.input_1.get_output() & self.input_2.get_output()


class OrGate(BinaryGate):
    def __init__(self, input_1, input_2) -> None:
        super.__init__(input_1, input_2)

    def get_output(self) -> np.uint16:
        return self.input_1.get_output() | self.input_2.get_output()


class LShiftGate(BinaryGate):
    def __init__(self, input_1, input_2) -> None:
        super.__init__(input_1, input_2)

    def get_output(self) -> np.uint16:
        return self.input_1.get_output() << self.input_2.get_output()


class RShiftGate(BinaryGate):
    def __init__(self, input_1, input_2) -> None:
        super.__init__(input_1, input_2)

    def get_output(self) -> np.uint16:
        return self.input_1.get_output() >> self.input_2.get_output()


class InstructionType(StrEnum):
    NOT = "NOT"
    AND = "AND"
    OR = "OR"
    LSHIFT = "LSHIFT"
    RSHIFT = "RSHIFT"
    APPLY = auto()


def determine_instruction_type(instruction) -> InstructionType:
    if "AND" in instruction:
        return InstructionType.AND
    elif "OR" in instruction:
        return InstructionType.OR
    elif "LSHIFT" in instruction:
        return InstructionType.LSHIFT
    elif "RSHIFT" in instruction:
        return InstructionType.RSHIFT
    elif "NOT" in instruction:
        return InstructionType.NOT
    else:
        return InstructionType.APPLY


with open("day7_input.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for instruction in lines:
        instruction = instruction.strip()
        instruction_type = determine_instruction_type(instruction)

        match instruction_type:
            case InstructionType.APPLY:
                if m := apply_pattern.fullmatch(instruction):
                    print(instruction)
                    source, wire = m.groups()
                    WIRES[Wire(wire)] = Wire(source)
                    # # is source a value or another wire?
                    # if source.isdigit():
                    #     signal = np.uint16(source)
                    #     WIRES[wire] = signal
                    # else:
                    #     WIRES[wire] = source
            case InstructionType.NOT:
                if m := not_pattern.fullmatch(instruction):
                    source, output = m.groups()
            case InstructionType.AND:
                pass
            case InstructionType.OR:
                pass
            case InstructionType.LSHIFT:
                pass
            case InstructionType.RSHIFT:
                pass


pprint.pprint(WIRES)
