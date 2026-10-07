"""Extra: how letters.py stores a letter, and where draw_letter puts its squares."""

import letters

shape = letters.SHAPES["a"]
print(shape)
print(shape[2])
print(shape[0][1])

x = 100
y = 50
size = 10
count = 0
for row in range(5):
    for col in range(3):
        if shape[row][col] == "#":
            print(f"row {row} col {col}: square at ({x + col * size}, {y + row * size})")
            count = count + 1
print(f"squares drawn: {count}")

for i in range(3):
    print(f"letter {i} starts at x = {40 + i * 4 * 4}")
