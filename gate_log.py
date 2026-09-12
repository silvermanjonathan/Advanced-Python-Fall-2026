door = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0]

x = 0
y = 0
z = 0
q = 0

for i in range(12):
    d = door[i]
    if d == 1:
        x = x + 1
        z = z + 1
    if d == 0:
        y = y + 1
        z = 0
    if z > q:
        q = z

print(f"x {x}")
print(f"y {y}")
print(f"z {z}")
print(f"q {q}")
