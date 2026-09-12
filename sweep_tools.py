"""Helpers that summarize a list of tower readings.

Every function here hands a value back. None of them print.
"""


def total_of(values):
    """Return the sum of every number in values."""
    running = 0
    for v in values:
        running = running + v
    return running


def average_of(values):
    """Return the mean of values."""
    return total_of(values) / len(values)


def count_over(values, limit):
    """Return how many values are strictly greater than limit."""
    hits = 0
    for v in values:
        if v > limit:
            hits = hits + 1
    return hits


def best_index(values):
    """Return the index of the first largest value in values."""
    best = values[0]
    where = 0
    for i in range(len(values)):
        if values[i] > best:
            best = values[i]
            where = i
    return where


def last_best_index(values):
    """Return the index of the last largest value in values."""
    best = values[0]
    where = 0
    for i in range(len(values)):
        if values[i] >= best:
            best = values[i]
            where = i
    return where
