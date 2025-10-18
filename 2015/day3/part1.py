from enum import StrEnum
from typing import NamedTuple


class Direction(StrEnum):
    NORTH = "^"
    EAST = ">"
    SOUTH = "v"
    WEST = "<"


class Position(NamedTuple):
    x: int
    y: int


def move_santa(current_position: Position, direction: Direction) -> Position:
    if direction == Direction.NORTH:
        return Position(current_position.x, current_position.y + 1)
    elif direction == Direction.EAST:
        return Position(current_position.x + 1, current_position.y)
    elif direction == Direction.SOUTH:
        return Position(current_position.x, current_position.y - 1)
    elif direction == Direction.WEST:
        return Position(current_position.x - 1, current_position.y)


current_position = Position(0, 0)

visited_houses = set()
visited_houses.add(current_position)

houses_with_multiple_visits = set()

with open("puzzle3_input.txt", "r", encoding="utf-8") as f:
    movelist = f.readline()

    for move in movelist:
        current_position = move_santa(current_position, move)
        if current_position in visited_houses:
            houses_with_multiple_visits.add(current_position)
        else:
            visited_houses.add(current_position)

    print(
        f"The number of houses that received at least one present is {len(visited_houses)}"
    )
