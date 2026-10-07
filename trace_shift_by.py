"""Session 3: shift_by traced one pass at a time, then the real shift_by's answer."""


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


text = "hi zoe"
amount = 3
out = ""
step = 0
for ch in text:
    step = step + 1
    if ch == " ":
        out = out + " "
        print(f"pass {step}: ch is ' ', the gate says yes, out is '{out}'")
    else:
        first = ord(ch) - ord("a")
        spot = (first + amount) % 26
        out = out + chr(spot + ord("a"))
        print(f"pass {step}: ch is '{ch}', spot {first} then {spot}, adds '{out[-1]}', out is '{out}'")

print(f"shift_by returns '{shift_by(text, amount)}'")
