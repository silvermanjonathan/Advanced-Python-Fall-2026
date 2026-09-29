"""Session 2, section 5: first_over_index written a second way, with enumerate."""


def first_over_index(values, limit):
    """Return the index of the first value strictly greater than limit, or -1."""
    for i, v in enumerate(values):
        if v > limit:
            return i
    return -1


readings = [41, 58, 33, 58, 12, 77, 58, 60, 29, 77]

print(f"first over 55 at index {first_over_index(readings, 55)}")
print(f"first over 100 at index {first_over_index(readings, 100)}")

for i, v in enumerate(["a", "b", "c"]):
    print(i, v)
