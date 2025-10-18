from typing import NamedTuple


class PairInfo(NamedTuple):
    character: str
    start: int
    end: int


def test_condition1(s) -> bool:
    """It contains a pair of any two letters that appears at least twice in the string without overlapping,
    like xyxy (xy) or aabcdefgaa (aa),
    but not like aaa (aa, but it overlaps)."""
    letter_pairs: list[PairInfo] = []
    two_pairs: list[PairInfo] = []
    # collect all letter pairs
    for i in range(0, len(s) - 1):
        letter_pairs.append(PairInfo(s[i] + s[i + 1], i, i + 1))

    # collect all matching letter pairs that don't overlap
    for i, pair in enumerate(letter_pairs):
        for other_pair in letter_pairs[(i + 1) :]:
            if pair.character == other_pair.character and pair.end != other_pair.start:
                two_pairs.append((pair, other_pair))

    # if there is at least one matching letter pair that doesn't overlap, the condition is True
    return len(two_pairs) >= 1


def test_condition2(s) -> bool:
    """It contains at least one letter which repeats with exactly one letter between them, like xyx, abcdefeghi (efe), or even aaa."""
    for i, letter in enumerate(s):
        if letter in s[i + 1 :] and s[i + 2] == letter:
            return True
    return False


num_nice_strings = 0
with open("puzzle5_input.txt", "r", encoding="utf-8") as f:
    for string_to_test in f:
        if test_condition1(string_to_test) and test_condition2(string_to_test):
            num_nice_strings += 1
    print(f"The number of nice strings is {num_nice_strings}.")
