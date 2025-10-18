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


class Entity:
    name: str
    current_position: Position

    def __init__(self, name: str, current_position: Position):
        self.name = name
        self.current_position = current_position

    def move(self, direction: Direction):
        if direction == Direction.NORTH:
            self.current_position = Position(
                self.current_position.x, self.current_position.y + 1
            )
        elif direction == Direction.EAST:
            self.current_position = Position(
                self.current_position.x + 1, self.current_position.y
            )
        elif direction == Direction.SOUTH:
            self.current_position = Position(
                self.current_position.x, self.current_position.y - 1
            )
        elif direction == Direction.WEST:
            self.current_position = Position(
                self.current_position.x - 1, self.current_position.y
            )


visited_houses = set()
visited_houses.add(Position(0, 0))

with open("puzzle3_input.txt", "r", encoding="utf-8") as f:
    santa = Entity("Santa", Position(0, 0))
    robot = Entity("Robo-Santa", Position(0, 0))

    movelist = iter(list(f.readline()))
    # iterate pairwise
    for santa_move, robot_move in zip(movelist, movelist):
        santa.move(santa_move)
        robot.move(robot_move)

        visited_houses.add(santa.current_position)
        visited_houses.add(robot.current_position)

    print(
        f"The number of houses that received at least one present is {len(visited_houses)}."
    )
