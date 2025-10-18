with open("puzzle1_input.txt", "r", encoding="utf-8") as f:
    instructions = f.readline()

    current_floor = 0
    for move in instructions:
        if move == "(":
            current_floor += 1
        elif move == ")":
            current_floor -= 1

    print(f"Santa ends up on floor {current_floor}.")
