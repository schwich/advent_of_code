from enum import StrEnum, auto, Enum
from dataclasses import dataclass
import re
import numpy as np


class Instruction(StrEnum):
    NOT = "NOT"
    AND = "AND"
    OR = "OR"
    LSHIFT = "LSHIFT"
    RSHIFT = "RSHIFT"
    APPLY = auto()
    UNKNOWN = auto()


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

BINARY_OPERATIONS = [
    Instruction.AND,
    Instruction.OR,
    Instruction.LSHIFT,
    Instruction.RSHIFT,
]


def is_binary_operation(instruction: str) -> bool:
    return (
        "AND" in instruction
        or "OR" in instruction
        or "LSHIFT" in instruction
        or "RSHIFT" in instruction
    )


def is_unary_operation(instruction: str) -> bool:
    return "NOT" in instruction


def determine_instruction_type(instr) -> Instruction:
    instruction_type: Instruction = Instruction.UNKNOWN
    if is_binary_operation(instr):
        if "AND" in instr:
            instruction_type = Instruction.AND
        elif "OR" in instr:
            instruction_type = Instruction.OR
        elif "LSHIFT" in instr:
            instruction_type = Instruction.LSHIFT
        elif "RSHIFT" in instr:
            instruction_type = Instruction.RSHIFT
    elif is_unary_operation(instr):
        instruction_type = Instruction.NOT
    else:
        instruction_type = Instruction.APPLY

    return instruction_type


# <wire_id or signal> -> <wire_id or signal>
apply_pattern = re.compile(r"^([a-z][a-z]?|\d+)\s->\s([a-z][a-z]?|\d+)$")

# NOT <wire_id or signal> -> <wire_id or signal>
not_pattern = re.compile(r"^NOT\s([a-z][a-z]?)\s->\s([a-z][a-z]?)$")

# <wire_id or signal> <AND|OR|LSHIFT|RSHIFT> <wire_id or signal> -> <wire_id>
binary_pattern = re.compile(
    r"^([a-z][a-z]?|\d+)\s(?:AND|OR|LSHIFT|RSHIFT)\s([a-z][a-z]?|\d+)\s->\s([a-z][a-z]?)$"
)


class TokenType(Enum):
    WIRE_ID = auto()
    SIGNAL = auto()


class Token:
    type: TokenType
    value: str | int

    def __init__(self, tok: str) -> None:
        self.type = Token.determine_wire_or_signal(tok)
        if type == TokenType.SIGNAL:
            self.value = int(tok)
        else:
            self.value = tok

    def __repr__(self) -> str:
        return f"Token(type={self.type}, value={self.value})"

    @staticmethod
    def determine_wire_or_signal(x: str) -> TokenType:
        try:
            int(x)
            return TokenType.SIGNAL
        except ValueError:
            return TokenType.WIRE_ID


WIRES = {}


def prepare_inputs_and_output(match_obj: re.Match) -> tuple[int, int, str]:
    input_tok_1, input_tok_2, output_tok = [Token(t) for t in match_obj.groups()]
    print(type(input_tok_1.value))

    if input_tok_1.type == TokenType.WIRE_ID:
        input1: int = WIRES[input_tok_1.value]
    else:
        input1: int = int(input_tok_1.value)
    if input_tok_2.type == TokenType.WIRE_ID:
        input2: int = WIRES[input_tok_2.value]
    else:
        input2: int = int(input_tok_2.value)

    return (input1, input2, str(output_tok.value))


def parse_instruction(instr: str):
    instruct_type = determine_instruction_type(instr)

    match instruct_type:
        case Instruction.APPLY:
            if m := apply_pattern.fullmatch(instr):
                wire_or_signal_1, wire_or_signal_2 = m.groups()
                token1 = Token(wire_or_signal_1)
                token2 = Token(wire_or_signal_2)

                if token1.type == TokenType.WIRE_ID:
                    WIRES[token2.value] = WIRES[token1.value]
                elif token1.type == TokenType.SIGNAL:
                    WIRES[token2.value] = token1.value

        case Instruction.NOT:
            if m := not_pattern.fullmatch(instr):
                input_tok, output = [Token(t) for t in m.groups()]
                print(input_tok, output)
                if input_tok.type == TokenType.WIRE_ID:
                    signal = WIRES[input_tok.value]
                else:
                    signal = input_tok.value

                WIRES[output.value] = ~np.uint16(signal)
        case Instruction.AND:
            if m := binary_pattern.fullmatch(instr):
                input1, input2, output = prepare_inputs_and_output(m)
                WIRES[output] = int(input1) & int(input2)
        case Instruction.OR:
            if m := binary_pattern.fullmatch(instr):
                input1, input2, output = prepare_inputs_and_output(m)
                WIRES[output] = int(input1) | int(input2)
        case Instruction.LSHIFT:
            if m := binary_pattern.fullmatch(instr):
                input1, input2, output = prepare_inputs_and_output(m)
                WIRES[output] = int(input1) << int(input2)
        case Instruction.RSHIFT:
            if m := binary_pattern.fullmatch(instr):
                input1, input2, output = prepare_inputs_and_output(m)
                print(type(input1), type(input2), type(output))
                WIRES[output] = int(input1) >> int(input2)
        case _:
            print("WHAT THE FUCK")


# for instr in test_instructions:
#     print(instr)
#     parse_instruction(instr)

a_instrs = []
with open("day7_input.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for instr in lines:
        instruction = instr.strip()
        instruction_type = determine_instruction_type(instruction)
        diag_str = f"instr: {instruction}\t type: {instruction_type}"

        if instruction_type in BINARY_OPERATIONS:
            if m := binary_pattern.fullmatch(instruction):
                input1, input2, output = m.groups()
                if "a" in m.groups():
                    print(instruction)
                    a_instrs.append(instruction)
                diag_str += f"\t({input1},{input2}) -> {output}"
        elif instruction_type == Instruction.APPLY:
            if m := apply_pattern.fullmatch(instruction):
                input_, output = m.groups()
                if "a" in m.groups():
                    print(instruction)
                    a_instrs.append(instruction)
                diag_str += f"\t{input_} -> {output}"

        # print(diag_str)
        # input1, input2, output = m.groups()


# print(a_instrs)
