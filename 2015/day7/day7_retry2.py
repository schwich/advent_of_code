import numpy as np
import re

from enum import StrEnum, auto, Enum

WIRES = {}

test_instructions = """\
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
lx -> a
lw OR lv -> lx
lc LSHIFT 1 -> lw
1 AND lu -> lv
""".splitlines()

wire_id_pattern = re.compile(r"^[a-z][a-z]?$")

signal_literal_pattern = re.compile(r"^\d+$")

# <wire_id or signal> -> <wire_id or signal>
apply_pattern = re.compile(r"^([a-z][a-z]?|\d+)\s->\s([a-z][a-z]?|\d+)$")

# NOT <wire_id or signal> -> <wire_id or signal>
not_pattern = re.compile(r"^NOT\s([a-z][a-z]?)\s->\s([a-z][a-z]?)$")

# <wire_id or signal> <AND|OR|LSHIFT|RSHIFT> <wire_id or signal> -> <wire_id>
binary_pattern = re.compile(
    r"^([a-z][a-z]?|\d+)\s(AND|OR|LSHIFT|RSHIFT)\s([a-z][a-z]?|\d+)\s->\s([a-z][a-z]?)$"
)


class Instruction(StrEnum):
    NOT = "NOT"
    AND = "AND"
    OR = "OR"
    LSHIFT = "LSHIFT"
    RSHIFT = "RSHIFT"
    APPLY = auto()


def determine_instruction_type(instr) -> Instruction:
    if "AND" in instr:
        return Instruction.AND
    elif "OR" in instr:
        return Instruction.OR
    elif "LSHIFT" in instr:
        return Instruction.LSHIFT
    elif "RSHIFT" in instr:
        return Instruction.RSHIFT
    elif "NOT" in instr:
        return Instruction.NOT
    else:
        return Instruction.APPLY
    
def is_signal(val):
    return type(val) == np.uint16


for instr in test_instructions:
    instruction = instr.strip()
    # print(instruction)

    if m := binary_pattern.fullmatch(instruction):
        in1, gate, in2, out = m.groups()
        print(f"{gate}: ({in1},{in2}) => {out}")

    elif m := not_pattern.fullmatch(instruction):
        in1, out = m.groups()
        print(f"NOT: {in1} => {out}")

        if is_wire(in1)

    elif m := apply_pattern.fullmatch(instruction):
        in1, out = m.groups()
        print(f"APPLY: {in1} => {out}")

        WIRES[out] = in1

    print("-" * 40)

print("=" * 80)
print(WIRES)
