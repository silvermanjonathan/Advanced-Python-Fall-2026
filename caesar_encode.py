"""Session 3: the Caesar cipher as a function, checked on the hand-worked examples."""


def shift_by(text, amount):
    """Return text with every letter rotated forward by amount."""
    out = ""
    for ch in text:
        if ch == " ":
            out = out + " "
        else:
            spot = ord(ch) - ord("a")
            spot = (spot + amount) % 26
            out = out + chr(spot + ord("a"))
    return out


print(shift_by("dawn", 3))
print(shift_by("zebra", 3))
print(shift_by("gdzq", -3))
