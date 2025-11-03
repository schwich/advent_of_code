from typing import override
import unittest


def count_num_chars_str(strings):
    num_char_str_code: int
    lengths = [len(line.strip()) for line in strings]
    num_char_str_code = sum(lengths)
    return num_char_str_code


def count_num_chars_in_memory(strings: list[str]):
    num_chars_in_memory: int
    line_chars = []
    for line in strings:
        line = line.strip()
        i = 0
        end = len(line)
        chars: list[str] = []
        while True:
            if i >= end:
                break

            if line[i] == "\\":
                if line[i + 1] == "x":
                    chars.append(f"{line[i]}{line[i + 1]}{line[i + 2]}{line[i + 3]}")
                    i += 4
                    continue
                elif line[i + 1] == '"':
                    chars.append(f"{line[i]}{line[i + 1]}")
                    i += 2
                    continue
                elif line[i + 1] == "\\":
                    chars.append(f"{line[i]}{line[i + 1]}")
                    i += 2
                    continue
            else:
                chars.append(line[i])
                i += 1

        chars = list(filter(lambda c: c != '"', chars))
        line_chars.append(chars)
    num_chars_in_memory = sum([len(l) for l in line_chars])
    return num_chars_in_memory


def print_str_codes(s: str) -> None:
    print("\n")
    print("-" * 30)
    for c in s:
        print(f"{c} => {ord(c)}")


def encode_str(s: str) -> str:
    s = s.strip()
    encoded_str = ""
    i = 0
    stop = len(s)

    while True:
        if i >= stop:
            break

        # " => 34
        # \ => 92
        if s[i] == '"':
            encoded_str += r"\""
        elif ord(s[i]) == 92:
            encoded_str += f"{chr(92)}{chr(92)}"
        else:
            encoded_str += s[i]

        i += 1

    return encoded_str


def count_num_encoded_char(strings: list[str]):
    # add 2 to count surrounding quotes
    encoded_str_lengths = [len(encode_str(s)) + 2 for s in strings]
    return sum(encoded_str_lengths)


class TestCharacterCounter(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

        self.test_file: list[str]
        self.puzzle_file: list[str]

    @override
    def setUp(self) -> None:
        f = open("day8_test.txt", "r", encoding="utf-8")
        self.test_file = []
        for l in f.readlines():
            self.test_file.append(l.strip())
        f.close()
        f = open("day8_input.txt", "r", encoding="utf-8")
        self.puzzle_file = []
        for l in f.readlines():
            self.puzzle_file.append(l.strip())
        f.close()

    def test_count_num_str(self):
        self.assertEqual(count_num_chars_str(self.test_file), 23)

    def test_count_num_chars_in_memory(self):
        self.assertEqual(count_num_chars_in_memory(self.test_file), 11)

    def test_puzzle_part1(self):
        self.assertEqual(
            count_num_chars_str(self.puzzle_file)
            - count_num_chars_in_memory(self.puzzle_file),
            1333,
        )

    def test_encode_str(self):
        # "" => "\"\""
        self.assertEqual(encode_str(self.test_file[0]), r"\"\"")
        self.assertEqual(count_num_encoded_char([self.test_file[0]]), 6)

        # "abc" => "\"abc\""
        self.assertEqual(encode_str(self.test_file[1]), r"\"abc\"")
        self.assertEqual(count_num_encoded_char([self.test_file[1]]), 9)

        # "aaa\"aaa" => "\"aaa\\\"aaa\""
        self.assertEqual(encode_str(self.test_file[2]), r"\"aaa\\\"aaa\"")
        self.assertEqual(count_num_encoded_char([self.test_file[2]]), 16)

        self.assertEqual(encode_str(self.test_file[3]), r"\"\\x27\"")
        self.assertEqual(count_num_encoded_char([self.test_file[3]]), 11)

    def test_count_num_encoded_str(self):
        self.assertEqual(count_num_encoded_char(self.test_file), 42)

    def test_puzzle_part2(self):
        self.assertEqual(
            count_num_encoded_char(self.puzzle_file)
            - count_num_chars_str(self.puzzle_file),
            2046,
        )


if __name__ == "__main__":
    _ = unittest.main()
