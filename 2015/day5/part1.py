bad_substrings = ["ab", "cd", "pq", "xy"]

vowels = list("aeiou")


def contains_at_least_3_vowels(string_to_test) -> bool:
    vowel_count = 0
    for character in string_to_test:
        if character in vowels:
            vowel_count += 1
            if vowel_count >= 3:
                return True
    return False


def contains_at_least_one_pair_of_letters(string_to_test) -> bool:
    for i in range(len(string_to_test) - 1):
        if string_to_test[i] == string_to_test[i + 1]:
            return True
    return False


def contains_bad_substring(string_to_test) -> bool:
    for bad_sub in bad_substrings:
        if bad_sub in string_to_test:
            return True
    return False


num_nice_strings = 0
with open("puzzle5_input.txt", "r", encoding="utf-8") as f:
    for string_to_test in f:
        if (
            (not contains_bad_substring(string_to_test))
            and contains_at_least_3_vowels(string_to_test)
            and contains_at_least_one_pair_of_letters(string_to_test)
        ):
            num_nice_strings += 1
    print(f"The number of nice strings is {num_nice_strings}.")
