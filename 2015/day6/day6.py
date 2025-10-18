import re
import numpy as np
from enum import StrEnum

instruction_pattern = re.compile(
    r"^(turn off|turn on|toggle)\s(\d+,\d+)\sthrough\s(\d+,\d+)$"
)


class Instruction(StrEnum):
    TURN_ON = "turn on"
    TURN_OFF = "turn off"
    TOGGLE = "toggle"


class Lights:

    def __init__(self, width: int, height: int):
        self._state = np.zeros((width, height), dtype=bool)

    def change_lights(self, instruction: Instruction, start_coords, end_coords):
        start_x, start_y = start_coords
        end_x, end_y = end_coords

        match instruction:
            case Instruction.TURN_ON:
                self._state[start_x : (end_x + 1), start_y : (end_y + 1)] = True
            case Instruction.TURN_OFF:
                self._state[start_x : (end_x + 1), start_y : (end_y + 1)] = False
            case Instruction.TOGGLE:
                self._state[start_x : (end_x + 1), start_y : (end_y + 1)] = (
                    ~self._state[start_x : (end_x + 1), start_y : (end_y + 1)]
                )

    def __repr__(self):
        return str(self._state)


lights = Lights(1000, 1000)


with open("day6_input.txt", "r", encoding="utf-8") as f:
    instructions = [l.strip() for l in f.readlines()]
    for instruction in instructions:
        if pattern_match := instruction_pattern.fullmatch(instruction):
            command, start_coord, end_coord = pattern_match.groups()

            start_coord = [int(x) for x in start_coord.split(",")]
            end_coord = [int(x) for x in end_coord.split(",")]

            match command:
                case Instruction.TURN_ON:
                    lights.change_lights(Instruction.TURN_ON, start_coord, end_coord)
                case Instruction.TURN_OFF:
                    lights.change_lights(Instruction.TURN_OFF, start_coord, end_coord)
                case Instruction.TOGGLE:
                    lights.change_lights(Instruction.TOGGLE, start_coord, end_coord)


print(np.count_nonzero(lights._state))
