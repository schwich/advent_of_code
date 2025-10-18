def calculate_perimeter(side1, side2):
    return 2 * side1 + 2 * side2


def calculate_amount_of_ribbon_to_wrap(length, width, height):
    return min(
        (
            calculate_perimeter(length, width),
            calculate_perimeter(length, height),
            calculate_perimeter(width, height),
        )
    )


def calculate_amount_of_ribbon_for_bow(length, width, height):
    return length * width * height


def unpack_measurements(line):
    """Returns a 3-tuple of (length, width, height)"""
    # l, w, h = line.strip().split('x')
    return tuple(int(x) for x in line.strip().split("x"))


measurements = []
with open("puzzle2_input.txt", "r", encoding="utf-8") as f:
    for line in f:
        length, width, height = unpack_measurements(line)
        measurements.append(
            calculate_amount_of_ribbon_to_wrap(length, width, height)
            + calculate_amount_of_ribbon_for_bow(length, width, height)
        )

print(f"The total feet of ribbon the elves should order is {sum(measurements)}.")
