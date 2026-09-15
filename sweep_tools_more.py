"""Answer key for session 2, section 5: seven more functions for the module.

Every function here returns a value. None of them print.
"""


def smallest_of(values):
    """Return the smallest number in values."""
    smallest = values[0]
    for v in values:
        if v < smallest:
            smallest = v
    return smallest


def largest_of(values):
    """Return the largest number in values."""
    largest = values[0]
    for v in values:
        if v > largest:
            largest = v
    return largest


def spread_of(values):
    """Return the largest minus the smallest, using the two functions above."""
    return largest_of(values) - smallest_of(values)


def count_under(values, limit):
    """Return how many values are strictly less than limit."""
    hits = 0
    for v in values:
        if v < limit:
            hits = hits + 1
    return hits


def count_between(values, low, high):
    """Return how many values are from low to high, both ends included."""
    hits = 0
    for v in values:
        if v >= low:
            if v <= high:
                hits = hits + 1
    return hits


def total_over(values, limit):
    """Return the total of the values that are strictly greater than limit."""
    running = 0
    for v in values:
        if v > limit:
            running = running + v
    return running


def first_over_index(values, limit):
    """Return the index of the first value strictly greater than limit, or -1."""
    for i in range(len(values)):
        if values[i] > limit:
            return i
    return -1
