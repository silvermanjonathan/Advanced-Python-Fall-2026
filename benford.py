"""Tally leading digits and compare them to Benford's law."""

import csv
import math
from collections import Counter


def leading_digit(text):
    """Return the first digit character in text as an integer."""
    for ch in text:
        if ch in "123456789":
            return int(ch)
    return 0


def tally_file(filename):
    """Return a Counter of leading digits in the amount column."""
    counts = Counter()
    with open(filename, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            counts[leading_digit(row["amount"])] += 1
    return counts


def benford_expected(digit):
    """Return the share of numbers Benford's law predicts start with digit."""
    return math.log10(1 + 1 / digit)


for filename in ["honest_ledger.csv", "cooked_ledger.csv"]:
    counts = tally_file(filename)
    total = sum(counts.values())
    print(filename)
    print("  digit   count    actual   benford predicts")
    for d in range(1, 10):
        actual = counts[d] / total
        print(f"  {d:>5}   {counts[d]:>5}   {actual:>7.3f}   {benford_expected(d):>15.3f}")
    worst = 0
    for d in range(1, 10):
        gap = abs(counts[d] / total - benford_expected(d))
        if gap > worst:
            worst = gap
    print(f"  largest gap from Benford: {worst:.3f}")
    print()
