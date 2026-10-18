"""The edits that turn session 3's finished console into session 4's two-way console.

Kept apart from the page generator so a script can build and check the program files
without importing the whole site.
"""

DOCSTRING_3 = '"""Cipher console: the coded message builds up one letter every half second."""'
DOCSTRING_4 = '"""Two-way cipher console: press E to encrypt the message, or D to decrypt it."""'
LAST_LETTER_LINE = "        letters.draw_letter(screen, coded[i], 40 + i * 16, 280, 4, CODED_INK)"

QUESTION = '''
    if mode == "":
        screen.fill(BOARD)
        letters.draw_word(screen, "do you want to", 238, 40, 3, PLAIN_INK)
        letters.draw_word(screen, "encrypt or decrypt", 178, 70, 4, TILE)
        pygame.draw.rect(screen, TILE, (150, 140, 120, 120))
        letters.draw_letter(screen, "e", 192, 170, 12, TILE_INK)
        letters.draw_word(screen, "encrypt", 170, 285, 3, PLAIN_INK)
        pygame.draw.rect(screen, CODED_TILE, (370, 140, 120, 120))
        letters.draw_letter(screen, "d", 412, 170, 12, CODED_INK)
        letters.draw_word(screen, "decrypt", 390, 285, 3, PLAIN_INK)'''

ANSWERS = '''        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            mode = "encrypt"
            coded = shift_by(MESSAGE, KEY)
            coded_row = shift_by(ALPHABET, KEY)
            frame = 0
            shown = 0
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            mode = "decrypt"
            coded = shift_by(MESSAGE, -KEY)
            coded_row = shift_by(ALPHABET, -KEY)
            frame = 0
            shown = 0'''

SPACE = '''        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            mode = ""'''

STEP_EDITS = {
    1: [("before", "running = 1", 'mode = ""'),
        ("after", LAST_LETTER_LINE, QUESTION)],
    2: [("after", "            running = 0", ANSWERS)],
    3: [("replace", DOCSTRING_3, DOCSTRING_4),
        ("replace", 'MESSAGE = "attack at dawn"', 'MESSAGE = "dwwdfn dw gdzq"'),
        ("replace", 'print(f"plain: {MESSAGE}")', 'print(f"message: {MESSAGE}")'),
        ("replace", 'print(f"coded: {coded}")', 'print(f"encrypted with key {KEY}: {coded}")'),
        ("replace", 'print(f"coded row: {coded_row}")',
         'print(f"decrypted with key {KEY}: {shift_by(MESSAGE, -KEY)}")')],
}

STEP_FILES = {
    0: "cipher_console.py",
    1: "two_way_step1.py",
    2: "two_way_step2.py",
    3: "two_way_console.py",
}

STRETCH_FILE = "two_way_space.py"


def apply_step(text, edits):
    """Return text with one step's edits made, each at its landmark line."""
    lines = text.split("\n")
    for kind, landmark, new in edits:
        where = [k for k, ln in enumerate(lines) if ln == landmark]
        assert len(where) == 1, f"landmark found {len(where)} times: {landmark!r}"
        k = where[0]
        block = new.split("\n")
        if kind == "after":
            lines[k + 1:k + 1] = block
        elif kind == "before":
            lines[k:k] = block
        else:
            lines[k:k + 1] = block
    return "\n".join(lines)


def stretch_text(final):
    """Return the stretch answer: the final program plus the space key handler."""
    text = final.replace(DOCSTRING_4, '"""Two-way cipher console: E encrypts, D decrypts, '
                         'space asks again."""')
    anchor = "            mode = \"decrypt\"\n"
    start = text.index(anchor)
    end = text.index("            shown = 0\n", start) + len("            shown = 0\n")
    return text[:end] + SPACE + "\n" + text[end:]


def build_texts(root):
    """Return {file name: text} for every step file and the stretch answer."""
    import os
    text = open(os.path.join(root, STEP_FILES[0])).read().rstrip("\n")
    out = {}
    for n in (1, 2, 3):
        text = apply_step(text, STEP_EDITS[n])
        out[STEP_FILES[n]] = text + "\n"
    out[STRETCH_FILE] = stretch_text(out[STEP_FILES[3]])
    return out


if __name__ == "__main__":
    import os
    import sys
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for name, text in build_texts(root).items():
        if "--write" in sys.argv:
            open(os.path.join(root, name), "w").write(text)
            print("wrote", name)
        else:
            assert open(os.path.join(root, name)).read() == text, f"{name} is out of date"
            print("matches", name)
