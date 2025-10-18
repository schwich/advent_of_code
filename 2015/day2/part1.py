def smallest_side_surface_area(length, width, height):
    return min((length * width, length * height, width * height))


def calculate_surface_area_of_box(length, width, height):
    return (2 * length * width) + (2 * length * height) + (2 * width * height)


def unpack_measurements(line):
    """Returns a 3-tuple of (length, width, height)"""
    return tuple(int(x) for x in line.strip().split("x"))


measurements = []
with open("puzzle2_input.txt", "r", encoding="utf-8") as f:
    for line in f:
        length, width, height = unpack_measurements(line)
        measurements.append(
            calculate_surface_area_of_box(length, width, height)
            + smallest_side_surface_area(length, width, height)
        )
print(
    f"The total square feet of wrapping paper the elves should order is {sum(measurements)}."
)
