"""Build the two CSV files session 10 reads.

honest_ledger.csv holds Fibonacci numbers and powers of two. Both of those
follow Benford's law as a matter of arithmetic, so this file stands in for
figures that grew on their own.

cooked_ledger.csv holds numbers picked uniformly at random between 100 and
9999. That is what invented figures look like: every leading digit roughly
as common as every other.
"""

import csv
import random

random.seed(20261125)

rows = []
a, b = 1, 1
for i in range(300):
    rows.append(("fibonacci", a))
    a, b = b, a + b

power = 1
for i in range(300):
    rows.append(("power_of_two", power))
    power = power * 2

with open("honest_ledger.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["source", "amount"])
    for row in rows:
        writer.writerow(row)

cooked = []
for i in range(600):
    cooked.append(("invented", random.randint(100, 9999)))

with open("cooked_ledger.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["source", "amount"])
    for row in cooked:
        writer.writerow(row)

print(f"honest_ledger.csv: {len(rows)} rows")
print(f"cooked_ledger.csv: {len(cooked)} rows")
