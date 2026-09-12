"""Break a Caesar cipher by letter frequency instead of by guessing."""

from collections import Counter

ENGLISH_ORDER = "etaoinshrdlcumwfgypbvkjxqz"

ciphertext = "uhdg wkh frgh dqg wudfh wkh frgh ehiruh brx hyhu uxq wkh frgh"


def shift_by(text, amount):
    """Return text with every letter rotated forward by amount."""
    out = ""
    for ch in text:
        if ch == " ":
            out = out + " "
        else:
            spot = ord(ch) - ord("a")
            spot = (spot + amount) % 26
            out = out + chr(spot + ord("a"))
    return out


def letter_counts(text):
    """Return a Counter of the letters in text, ignoring spaces."""
    letters = ""
    for ch in text:
        if ch != " ":
            letters = letters + ch
    return Counter(letters)


def guess_shift(text):
    """Return the shift that maps the most common letter onto 'e'."""
    counts = letter_counts(text)
    top_letter = counts.most_common(1)[0][0]
    return (ord(top_letter) - ord("e")) % 26


counts = letter_counts(ciphertext)
print("five most common:", counts.most_common(5))
print("distinct letters used:", len(set(ciphertext.replace(" ", ""))))

k = guess_shift(ciphertext)
print(f"guessed shift {k}")
print("plaintext:", shift_by(ciphertext, -k))

print("--- every shift, for comparison ---")
for amount in range(26):
    candidate = shift_by(ciphertext, -amount)
    print(f"{amount:2d} {candidate[:34]}")
