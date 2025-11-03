from typing import override
import unittest
import re
import pprint as pp

pattern = re.compile(r"^(\w+)\sto\s(\w+)\s=\s(\d+)$")


def construct_places_set(place_distances: list[str]) -> set[str]:
    places: set[str] = set()
    for line in place_distances:
        if m := pattern.fullmatch(line):
            from_place, to_place, _ = m.groups()
            places.add(from_place)
            places.add(to_place)

    return places


def construct_graph(place_distances: list[str]) -> dict[str, dict[str, int]]:
    place_graph: dict[str, dict[str, int]] = {}
    for line in place_distances:
        if m := pattern.fullmatch(line):
            from_place, to_place, distance = m.groups()
            from_place = str(from_place)
            to_place = str(to_place)
            distance = int(distance)

            if from_place not in place_graph:
                place_graph[from_place] = {}

            place_graph[from_place].update({to_place: distance})

    return place_graph


def read_places_file(filepath: str) -> list[str]:
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]


class TestShortestDistance(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.place_distances: list[str]

    @override
    def setUp(self) -> None:
        with open("day9_test_input.txt", "r", encoding="utf-8") as f:
            self.place_distances = [line.strip() for line in f.readlines()]


# def compute_cycle(places: set[str], place_graph: dict[str, dict[str, int]], accumulated_distance: int):
#     if not places:
#         return 0
#     else:
#         accumulated_distance += place_graph


def get_distance(
    places_graph: dict[str, dict[str, int]], from_place: str, to_place: str
) -> int | None:
    return places_graph[from_place][to_place]


def compute_tour_distance(
    places_graph: dict[str, dict[str, int]],
    start: str,
    places_left: set[str],
    places_visisted: list[str],
    accumulated_distance: int = 0,
) -> tuple[list[str], int]:
    print(
        f"compute_tour_distance() {start=}, {places_left=}, {places_visisted=}, {accumulated_distance=}"
    )

    if not places_left:
        return (places_visisted, accumulated_distance)

    next_place = places_left.pop()

    if start not in places_graph or next_place not in places_graph[start]:
        return (places_visisted, -1)

    accumulated_distance += places_graph[start][next_place]
    places_visisted.append(next_place)

    return compute_tour_distance(
        places_graph,
        start=next_place,
        places_left=places_left,
        places_visisted=places_visisted,
        accumulated_distance=accumulated_distance,
    )


if __name__ == "__main__":
    # print(construct_graph(read_places_file("day9_input.txt")))
    # _ = unittest.main()

    # place_info = read_places_file("day9_input.txt")
    place_info = read_places_file("day9_test_input.txt")
    places = construct_places_set(place_info)
    places_list = list(places)
    pp.pprint(places)

    places_graph = construct_graph(place_info)
    pp.pprint(places_graph)

    tours: list[tuple[list[str], int]] = []
    for start in places_list:
        all_places = places.copy()
        left_to_visit = all_places - set([start])
        print(f"{start=}")
        print(f"{left_to_visit=}")
        tours.append(
            compute_tour_distance(places_graph, start, left_to_visit, [start], 0)
        )

    pp.pprint(tours)
