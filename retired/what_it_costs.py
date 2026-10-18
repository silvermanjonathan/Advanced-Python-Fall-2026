"""Measure what a program costs instead of guessing."""

from itertools import product
from time import perf_counter

CODE = "4703916"


def linear_find(values, target):
    """Return the index of target, and how many values we looked at."""
    looks = 0
    for i in range(len(values)):
        looks = looks + 1
        if values[i] == target:
            return i, looks
    return -1, looks


def binary_find(values, target):
    """Return the index of target in a sorted list, and how many looks."""
    low = 0
    high = len(values) - 1
    looks = 0
    while low <= high:
        mid = (low + high) // 2
        looks = looks + 1

        if values[mid] == target:
            return mid, looks

        if values[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1, looks


def sweep(digits):
    """Try every code of the given length. Return the winner and the tries."""
    tries = 0
    winner = ""
    target = CODE[:digits]

    for guess in product("0123456789", repeat=digits):
        tries = tries + 1
        attempt = "".join(guess)
        if attempt == target:
            winner = attempt
    return winner, tries


shelf = list(range(0, 2000, 2))

print("searching a sorted list of", len(shelf), "even numbers for 1998")
spot, looks = linear_find(shelf, 1998)
print(f"  linear: found at {spot} after {looks} looks")
spot, looks = binary_find(shelf, 1998)
print(f"  binary: found at {spot} after {looks} looks")

print()
print("searching for 1999, which is not there")
spot, looks = linear_find(shelf, 1999)
print(f"  linear: returned {spot} after {looks} looks")
spot, looks = binary_find(shelf, 1999)
print(f"  binary: returned {spot} after {looks} looks")

print()
print("brute force, every code of n digits")
print("  n   codes      tries    seconds")
for n in range(1, 8):
    start = perf_counter()
    found, tries = sweep(n)
    elapsed = perf_counter() - start
    print(f"  {n}   {10 ** n:<10} {tries:<8} {elapsed:.4f}")
