import re
import pprint

from enum import StrEnum, auto, Enum
from abc import ABC, abstractmethod

import numpy as np

# <wire_id or signal> -> <wire_id>
apply_pattern = re.compile(r"^([a-z][a-z]?|\d+)\s->\s([a-z][a-z]?|\d+)$")

# NOT <wire> -> <wire>
not_pattern = re.compile(r"^NOT\s([a-z][a-z]?)\s->\s([a-z][a-z]?)$")

# <wire_id or signal> <AND|OR|LSHIFT|RSHIFT> <wire_id or signal> -> <wire_id>
binary_pattern = re.compile(
    r"^([a-z][a-z]?|\d+)\s(?:AND|OR|LSHIFT|RSHIFT)\s([a-z][a-z]?|\d+)\s->\s([a-z][a-z]?)$"
)

# wire_id => <another wire_id> | Gate | Value
WIRES = {}

# wire_id => Wire
SIGNALS = {}


class Gate(ABC):
    output: np.uint16 | SignalType

    @abstractmethod
    def get_output(self) -> np.uint16:
        pass


class NotGate(Gate):
    def __init__(self, source):
        self.source = source

    def get_output(self):
        return ~(get_signal(self.source))

    def __repr__(self) -> str:
        return f"NotGate(source={self.source})"


class AndGate(Gate):
    def __init__(self, input1, input2):
        self.input1 = input1
        self.input2 = input2

    def get_output(self):
        return get_signal(self.input1) & get_signal(self.input2)

    def __repr__(self) -> str:
        return f"AndGate(input1={self.input1}, input2={self.input2})"


class OrGate(Gate):
    def __init__(self, input1, input2):
        self.input1 = input1
        self.input2 = input2

    def get_output(self):
        return get_signal(self.input1) | get_signal(self.input2)

    def __repr__(self) -> str:
        return f"OrGate(input1={self.input1}, input2={self.input2})"


class LShiftGate(Gate):
    def __init__(self, input1, input2):
        self.input1 = input1
        self.input2 = input2

    def get_output(self):
        # print(f"{self=} get_output()")
        # print("getting sig1")
        sig1 = get_signal(self.input1)
        # print("getting sig2")
        sig2 = get_signal(self.input2)
        # print(f"{self=}\t{sig1=}, {sig2=}")
        return sig1 << sig2
        # return get_signal(self.input1) << get_signal(self.input2)

    def __repr__(self) -> str:
        return f"LShiftGate(input1={self.input1}, input2={self.input2})"


class RShiftGate(Gate):
    def __init__(self, input1, input2):
        self.input1 = input1
        self.input2 = input2

    def get_output(self):
        return get_signal(self.input1) >> get_signal(self.input2)

    def __repr__(self) -> str:
        return f"RShiftGate(input1={self.input1}, input2={self.input2})"


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


# def get_signal(wire_id) -> np.uint16:
#     if type(wire_id) is np.uint16:
#         print(f"VALUE {wire_id=}")
#         return wire_id

#     wire_signal = WIRES[wire_id]

#     print(f"get_signal() with {wire_id=}\t{wire_signal=}")
#     if type(wire_signal) is np.uint16:
#         return wire_signal
#     elif type(wire_signal) is str:
#         if wire_signal.isdigit():
#             print(f"ERROR {wire_signal=} isdigit")
#             return np.uint16(wire_signal)
#         else:
#             print(f"source is wire: {wire_signal}")
#             # return get_signal(WIRES[wire])
#             return get_signal(wire_signal)
#     elif isinstance(wire_signal, Gate):
#         print(f"GATE {wire_signal=}")
#         return wire_signal.get_output()
#     else:
#         print("FUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")
#         print(f"{wire_id=} {wire_signal=}")
#         return np.uint16(0)


def get_signal(wire_id) -> np.uint16:
    # print(f"get_signal({wire_id=})")
    if type(wire_id) is np.uint16:
        return wire_id
    if wire_id in SIGNALS:
        return SIGNALS[wire_id]
    else:
        # wire_id's source is either another Wire or a Gate or a Value
        wire_source = WIRES[wire_id]
        match wire_source:
            case str():
                # either a Value or another Wire
                if wire_id.isdigit():
                    signal_value = np.uint16(wire_id)
                    SIGNALS[wire_id] = signal_value
                    return signal_value
                else:
                    signal_output = get_signal(WIRES[wire_id])
                    SIGNALS[wire_id] = signal_output
                    return signal_output
            case Gate():
                signal_output = wire_source.get_output()
                SIGNALS[wire_id] = signal_output
                return signal_output
            case _:
                print("FUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")
                return np.uint16(0)


def process_instruction(instruction):
    instruction_type = determine_instruction_type(instruction)

    match instruction_type:
        case InstructionType.APPLY:
            if m := apply_pattern.fullmatch(instruction):
                # print(instruction)
                source, output = m.groups()
                # print(f"{source=}, {output=}")
                if source.isdigit():
                    source = np.uint16(source)
                    SIGNALS[output] = source
                else:
                    WIRES[output] = source
                    # SIGNALS[output] = Wire(output, source)
        case InstructionType.NOT:
            if m := not_pattern.fullmatch(instruction):
                # print(instruction)
                source, output = m.groups()
                # print(f"{source=}, {output=}")
                gate = NotGate(source)
                WIRES[output] = gate
                # SIGNALS[output] = Wire(output, gate)
        case InstructionType.AND:
            if m := binary_pattern.fullmatch(instruction):
                input1, input2, output = m.groups()
                if input1.isdigit():
                    input1 = np.uint16(input1)
                elif input2.isdigit():
                    input2 = np.uint16(input2)
                gate = AndGate(input1, input2)
                WIRES[output] = gate
        case InstructionType.OR:
            if m := binary_pattern.fullmatch(instruction):
                input1, input2, output = m.groups()
                if input1.isdigit():
                    input1 = np.uint16(input1)
                elif input2.isdigit():
                    input2 = np.uint16(input2)
                gate = OrGate(input1, input2)
                WIRES[output] = gate
        case InstructionType.LSHIFT:
            if m := binary_pattern.fullmatch(instruction):
                input1, input2, output = m.groups()
                if input1.isdigit():
                    input1 = np.uint16(input1)
                elif input2.isdigit():
                    input2 = np.uint16(input2)
                gate = LShiftGate(input1, input2)
                WIRES[output] = gate
        case InstructionType.RSHIFT:
            if m := binary_pattern.fullmatch(instruction):
                input1, input2, output = m.groups()
                if input1.isdigit():
                    input1 = np.uint16(input1)
                elif input2.isdigit():
                    input2 = np.uint16(input2)
                gate = RShiftGate(input1, input2)
                WIRES[output] = gate


class SignalType(StrEnum):
    WIRE = auto()
    GATE = auto()
    VALUE = auto()
    UNKNOWN = auto()


# class Wire:
#     id: str
#     signal: Wire | Gate | np.uint16 | None
#     signal_type: SignalType

#     def __init__(self, id, signal) -> None:
#         self.id = id
#         self.signal_type = Wire.determine_signal_type(signal)
#         self.signal = None
#         print(f"match {self.signal_type=}")
#         match self.signal_type:
#             case SignalType.WIRE:
#                 print(f"{signal=}")
#                 self.signal = Wire(signal, SignalType.UNKNOWN)
#                 pass
#             case SignalType.GATE:
#                 pass
#             case SignalType.VALUE:
#                 self.signal = np.uint16(signal)
#             case SignalType.UNKNOWN:
#                 self.signal = None

#     def __repr__(self) -> str:
#         return f'Wire(id="{self.id}", signal={self.signal})'

#     @staticmethod
#     def determine_signal_type(sig) -> SignalType:
#         match sig:
#             case str():
#                 if sig.isdigit():
#                     return SignalType.VALUE
#                 else:
#                     return SignalType.WIRE
#             case Gate():
#                 return SignalType.GATE
#             case _:
#                 return SignalType.UNKNOWN


class Wire:
    id: str
    source: Wire | Gate | np.uint16 | None

    def __init__(self, id, source) -> None:
        self.id = id

        if type(source) is str:
            if source.isdigit():
                self.source = np.uint16(source)
            else:
                self.source = Wire(source, None)
        else:
            self.source = source

    def __repr__(self) -> str:
        return f"Wire(id={self.id}, source={self.source})"


def process():
    pass


test_instructions = """\
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
""".splitlines()
print("\n\n")
# for instruction in test_instructions:
#     instruction = instruction.strip()
#     process_instruction(instruction)
with open("day7_input.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for instruction in lines:
        instruction = instruction.strip()
        process_instruction(instruction)

print("=" * 80)
# # WIRES["js"] = np.uint16(5)
# # WIRES["lx"] = AndGate("js", np.uint16(1))
# # WIRES["jx"] = np.uint16(5)
# # WIRES["lx"] = RShiftGate("jx", np.uint16(1))
print("WIRES")
pprint.pprint(WIRES)
# print("-" * 40)
# print(f"d: {get_signal('d')}")
# print(f"e: {get_signal('e')}")
# print("-" * 40)
# int(f"f: {get_signal('f')}")
# print(f"g: {get_signal('g')}")
# print("-" * 40)
# print(f"h: {get_signal('h')}")
# print(f"i: {get_signal('i')}")
# print(f"x: {get_signal('x')}")
# print(f"y: {get_signal('y')}")

print("\n")
print("SIGNALS")
# SIGNALS["w"] = np.uint(54)
SIGNALS["b"] = np.uint(46065)
pprint.pprint(SIGNALS)
# print(get_signal("a"))
wire_a_answer = get_signal("a")
print(f"{wire_a_answer=}")
# pprint.pprint(SIGNALS)
