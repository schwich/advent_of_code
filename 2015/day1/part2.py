with open("puzzle1_input.txt", "r", encoding="utf-8") as f:
    instructions = f.readline()

    current_floor = 0
    current_move_index = 0
    for move in instructions:
        current_move_index += 1

        if move == "(":
            current_floor += 1
        elif move == ")":
            current_floor -= 1

        if current_floor == -1:
            print(
                f"The position of the character that caused Santa to first enter the basement is {current_move_index}."
            )
            break
