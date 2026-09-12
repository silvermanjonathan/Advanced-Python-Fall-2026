"""Two ciphers that move letters instead of replacing them."""

MESSAGE = "meetatthenorthgateatdawn"


def rail_encode(text, rails):
    """Return text written down a zig-zag of rails, then read across."""
    rows = []
    for r in range(rails):
        rows.append("")
    r = 0
    step = 1
    for ch in text:
        rows[r] = rows[r] + ch
        if r == 0:
            step = 1
        if r == rails - 1:
            step = -1
        r = r + step
    joined = ""
    for row in rows:
        joined = joined + row
    return joined


def rail_decode(text, rails):
    """Return the original message from a rail fence ciphertext."""
    pattern = []
    r = 0
    step = 1
    for ch in text:
        pattern.append(r)
        if r == 0:
            step = 1
        if r == rails - 1:
            step = -1
        r = r + step
    out = [""] * len(text)
    spot = 0
    for target in range(rails):
        for i in range(len(text)):
            if pattern[i] == target:
                out[i] = text[spot]
                spot = spot + 1
    joined = ""
    for ch in out:
        joined = joined + ch
    return joined


def to_grid(text, width):
    """Return text packed into rows of the given width."""
    grid = []
    row = []
    for ch in text:
        row.append(ch)
        if len(row) == width:
            grid.append(row)
            row = []
    if len(row) > 0:
        while len(row) < width:
            row.append("x")
        grid.append(row)
    return grid


def route_encode(text, key):
    """Return text read out column by column in the order key gives.

    A negative number in key means read that column bottom to top.
    """
    grid = to_grid(text, len(key))
    out = ""
    for signed in key:
        col = abs(signed) - 1
        rows = range(len(grid))
        if signed < 0:
            rows = range(len(grid) - 1, -1, -1)
        for r in rows:
            out = out + grid[r][col]
    return out


fence = rail_encode(MESSAGE, 3)
print("message ", MESSAGE)
print("rails 3 ", fence)
print("back    ", rail_decode(fence, 3))
print("round trip ok:", rail_decode(fence, 3) == MESSAGE)

print()
grid = to_grid(MESSAGE, 4)
for row in grid:
    print("  " + " ".join(row))

key = [2, -4, 1, 3]
print("key     ", key)
print("route   ", route_encode(MESSAGE, key))
