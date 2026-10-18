"""Session 4 opener: a negative key undoes a positive one."""


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
print(shift_by("gdzq", -3))
print(shift_by("abc", -1))
print((0 - 1) % 26)
print(shift_by(shift_by("hello", 7), -7))
