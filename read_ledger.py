"""Session 9: open a CSV file and look at its first three rows."""

import csv

with open("honest_ledger.csv", newline="") as f:
    reader = csv.DictReader(f)
    count = 0
    for row in reader:
        if count < 3:
            print(row)
        count = count + 1

print(f"rows read: {count}")
