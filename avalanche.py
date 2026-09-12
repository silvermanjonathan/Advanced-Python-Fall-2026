"""Compare a homemade letter-sum seal against a real hash."""

import hashlib


def letter_sum_seal(text):
    """Return our summer seal: add up the letter positions, wrap at 97."""
    running = 0
    for ch in text:
        running = running + ord(ch)
    return running % 97


def sha(text):
    """Return the sha256 hex digest of text."""
    return hashlib.sha256(text.encode()).hexdigest()


def bits_of(hexdigest):
    """Return hexdigest as a string of 0s and 1s."""
    number = int(hexdigest, 16)
    return format(number, "0256b")


def bits_differing(a, b):
    """Return how many bit positions differ between two hex digests."""
    left = bits_of(a)
    right = bits_of(b)
    count = 0
    for i in range(256):
        if left[i] != right[i]:
            count = count + 1
    return count


first = "attack at dawn"
second = "attack at dusk"
third = "attack at dawn."

print(f"seal of {first!r} = {letter_sum_seal(first)}")
print(f"seal of {second!r} = {letter_sum_seal(second)}")
print()
print("collision hunt on the homemade seal:")
print(f"  seal of 'ab' = {letter_sum_seal('ab')}")
print(f"  seal of 'ba' = {letter_sum_seal('ba')}")
print(f"  same seal, different message: {letter_sum_seal('ab') == letter_sum_seal('ba')}")
print()
print(f"sha256 {first!r}")
print(f"  {sha(first)}")
print(f"sha256 {second!r}")
print(f"  {sha(second)}")
print(f"sha256 {third!r}")
print(f"  {sha(third)}")
print()
print(f"dawn vs dusk: {bits_differing(sha(first), sha(second))} of 256 bits differ")
print(f"dawn vs dawn+period: {bits_differing(sha(first), sha(third))} of 256 bits differ")
