"""Session 3 opener: a string accumulator with a gate inside the loop."""


def hide_letters(text):
    """Return text with every letter changed to * and every space kept."""
    out = ""
    for ch in text:
        if ch == " ":
            out = out + " "
        else:
            out = out + "*"
    return out


print(hide_letters("meet at dawn"))
