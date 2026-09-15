"""Track four sparks with parallel lists. This is the version we are replacing."""

xs = [100, 100, 100, 100]
ys = [500, 500, 500, 500]
dxs = [2, -1, 3, 0]
dys = [-6, -5, -7, -4]
colors = ["gold", "orange", "red", "gold"]

GRAVITY = 1

for frame in range(3):
    for i in range(4):
        dys[i] = dys[i] + GRAVITY
        xs[i] = xs[i] + dxs[i]
        ys[i] = ys[i] + dys[i]

    print(f"frame {frame}")
    for i in range(4):
        print(f"  spark {i}: x={xs[i]} y={ys[i]} dy={dys[i]} {colors[i]}")

print()
print("now remove spark 1, which has landed")
xs.pop(1)
ys.pop(1)
dxs.pop(1)
dys.pop(1)
# colors.pop(1) is missing on purpose

print("after removing from four lists but forgetting the fifth:")
for i in range(3):
    print(f"  spark {i}: x={xs[i]} y={ys[i]} {colors[i]}")
