readings = [41, 58, 33, 58, 12, 77, 58, 60, 29, 77]
limit = 55

t = 0
c = 0
b = 0
bi = 0

for i in range(10):
    r = readings[i]

    t = t + r

    if r > limit:
        c = c + 1

    if r > b:
        b = r
        bi = i

avg = t / 10

print(f"total {t}")
print(f"average {avg}")
print(f"over {limit}: {c}")
print(f"best {b} at index {bi}")

slot = 0
for i in range(10):
    slot = (slot + readings[i]) % 9
    print(f"i={i} reading={readings[i]} slot={slot}")
