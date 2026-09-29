"""Session 9: count the rows in a CSV file, without crashing if it is missing."""

import csv


def count_rows(filename):
    """Return how many rows the CSV file has, or 0 if there is no such file."""
    try:
        with open(filename, newline="") as f:
            count = 0
            for row in csv.DictReader(f):
                count = count + 1
    except FileNotFoundError:
        print(f"no file called {filename}, so there is nothing to count")
        return 0
    return count


print(count_rows("honest_ledger.csv"))
print(count_rows("honest_ledger.cvs"))
print("the program is still running")
