import hashlib


def test_if_at_least_five_leading_zeros(hash_digest: str):
    return hash_digest[0:5] == "00000"


input_text_base = "iwrupvqb"
num = 0
while True:
    md5_hash = hashlib.md5(f"{input_text_base}{num}".encode()).hexdigest()
    if test_if_at_least_five_leading_zeros(md5_hash):
        print(num)
        break

    num += 1
