"""Session 3: a loop inside a loop, before step 3 of the console."""

for row in range(2):
    for col in range(3):
        print(f"row {row} col {col}")

for row in range(3):
    line = ""
    for col in range(4):
        line = line + "#"
    print(line)
