"""Session 3, section 4: the Caesar cipher in a pygame window."""

import base64
import os

from build import code, downloads, labelled_code, laddered, output, reveal

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SHOTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shots")

STEPS = [
    ("console_1_window.py", "an empty window that stays open until you close it"),
    ("console_2_tiles.py", "a row of 26 tiles, one for each letter"),
    ("console_3_board.py", "the alphabet, the coded alphabet under it, and the message"),
    ("cipher_console.py", "the coded message appears one letter at a time"),
]


def _source(name):
    """Return the text of a program in the repo root, without its last newline."""
    return open(os.path.join(_ROOT, name)).read().rstrip("\n")


def _excerpt(name, first, last):
    """Return the lines of a program from the line starting with first to the one with last."""
    lines = _source(name).split("\n")
    start = next(i for i, ln in enumerate(lines) if ln.strip().startswith(first))
    end = next(i for i in range(start, len(lines)) if last in lines[i])
    return "\n".join(lines[start:end + 1])


def _shift_by_matches():
    """Check that the console's shift_by is the one from caesar_encode.py, unchanged."""
    def grab(name):
        text = _source(name)
        start = text.find("def shift_by")
        return text[start:text.find("\n\n\n", start)]

    for name in ("console_3_board.py", "cipher_console.py", "cipher_console_replay.py"):
        assert grab(name) == grab("caesar_encode.py"), f"shift_by differs in {name}"


def _shot(name, alt):
    """Return a screenshot from build/shots as an inline image."""
    data = base64.b64encode(open(os.path.join(_SHOTS, name), "rb").read()).decode()
    return (
        f'<img src="data:image/png;base64,{data}" alt="{alt}" width="640" height="400" '
        'style="display:block; max-width:100%; height:auto; border:2px solid var(--rule); '
        'border-radius:6px; margin:10px 0 16px">'
    )


def _grid_svg():
    """Return the diagram of pygame coordinates: x across, y down, (0, 0) top left."""
    return (
        '<svg viewBox="0 0 450 270" width="450" style="max-width:100%; height:auto; '
        'display:block; margin:10px 0 16px" role="img" aria-label="A window 640 wide '
        'and 400 tall. The top left corner is (0, 0). x grows to the right. y grows '
        'downward. A tile sits at (20, 130).">'
        '<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        'markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#0E4D52"/>'
        "</marker></defs>"
        '<rect x="90" y="40" width="320" height="200" fill="#10141A" stroke="#0E4D52" '
        'stroke-width="2"/>'
        '<circle cx="90" cy="40" r="4" fill="#9C2B22"/>'
        '<text x="84" y="30" text-anchor="end" font-size="14" fill="#17181B">(0, 0)</text>'
        '<line x1="100" y1="22" x2="280" y2="22" stroke="#0E4D52" stroke-width="2" '
        'marker-end="url(#arr)"/>'
        '<text x="288" y="27" font-size="14" fill="#17181B">x grows to the right</text>'
        '<line x1="50" y1="50" x2="50" y2="200" stroke="#0E4D52" stroke-width="2" '
        'marker-end="url(#arr)"/>'
        '<text x="46" y="222" text-anchor="middle" font-size="14" fill="#17181B">y grows</text>'
        '<text x="46" y="238" text-anchor="middle" font-size="14" fill="#17181B">downward</text>'
        '<rect x="100" y="105" width="10" height="13" fill="#F2E9D3"/>'
        '<circle cx="100" cy="105" r="3" fill="#9C2B22"/>'
        '<text x="118" y="100" font-size="14" fill="#F2E9D3">(20, 130)</text>'
        '<circle cx="410" cy="240" r="4" fill="#9C2B22"/>'
        '<text x="410" y="260" text-anchor="middle" font-size="14" fill="#17181B">'
        "(640, 400)</text>"
        "</svg>"
    )


def _letter_svg(rows):
    """Return a picture of one letter from its five strings, with each string beside its row."""
    cell = 18
    parts = []
    for r, text in enumerate(rows):
        for c, mark in enumerate(text):
            fill = "#0E4D52" if mark == "#" else "#FFFDF7"
            parts.append(
                f'<rect x="{c * (cell + 2)}" y="{r * (cell + 2)}" width="{cell}" '
                f'height="{cell}" fill="{fill}" stroke="#D3CBB8"/>'
            )
        parts.append(
            f'<text x="{3 * (cell + 2) + 16}" y="{r * (cell + 2) + 14}" font-size="15" '
            f'font-family="monospace" fill="#17181B">"{text}"</text>'
        )
    height = 5 * (cell + 2)
    return (
        f'<svg viewBox="0 0 160 {height}" width="160" style="display:block; '
        'margin:10px 0 16px" role="img" aria-label="The letter a drawn from 15 squares, '
        f'with its five strings beside the rows.">{"".join(parts)}</svg>'
    )


ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def _shift(text, amount):
    """Run shift_by from caesar_encode.py's source, so the page quotes the real function."""
    src = _source("caesar_encode.py")
    body = src[src.find("def shift_by"):src.find("\n\n\n", src.find("def shift_by"))]
    ns = {}
    exec(body, ns)
    return ns["shift_by"](text, amount)


WINDOW_PARTS = [
    ('"""Cipher console, step 1', "The docstring: one sentence saying what the "
     "program is for.", ""),
    ("import pygame", "Bring in pygame, the same way <code>import sweep_tools</code> "
     "brought in your own module in session 2.", ""),
    ("BOARD =", "A color for the background.", ""),
    ("pygame.init()", "Set up. This runs once.", "once"),
    ("while running:", "The loop. Every line indented under it runs again on every "
     "frame, up to 60 times a second.", "frame"),
    ("for event in", "1. Read the events.", "frame"),
    ("screen.fill", "2. Draw.", "frame"),
    ("pygame.display.flip", "3. Show the drawing, then wait.", "frame"),
    ("pygame.quit", "After the loop. This runs once, when the loop stops.", "after"),
]

CONSOLE_PARTS = [
    ('"""Cipher console', "The docstring: one sentence saying what the program is "
     "for.", ""),
    ("import pygame", "Bring in pygame and <code>letters.py</code>.", ""),
    ("MESSAGE =", "The two lines you change, and the alphabet.", ""),
    ("BOARD =", "Colors, each one (red, green, blue).", ""),
    ("def shift_by", "<code>shift_by</code>, your function from section 3.", ""),
    ("coded = shift_by", "Code the message and the alphabet, and print them in the "
     "terminal. This runs once.", "once"),
    ("pygame.init()", "Set up the window, the clock, and the two accumulators. This "
     "runs once.", "once"),
    ("while running:", "The loop. Every line indented under it runs again on every "
     "frame, up to 60 times a second.", "frame"),
    ("for event in", "1. Read the events.", "frame"),
    ("screen.fill", "2. Draw the background and the two rows of tiles.", "frame"),
    ("if shown < len", "3. Box the letter being coded.", "frame"),
    ("letters.draw_word", "4. Draw the message, and the coded letters that are "
     "showing.", "frame"),
    ("frame = frame + 1", "5. Count the frame. On every 30th frame, one more coded "
     "letter shows.", "frame"),
    ("pygame.display.flip", "6. Show the drawing, then wait.", "frame"),
    ("pygame.quit", "After the loop. This runs once, when the loop stops.", "after"),
]


def console_section():
    """Return session 3's section 4, the cipher console, and its stretch exit."""
    _shift_by_matches()
    a_rows = [".#.", "#.#", "###", "#.#", "#.#"]
    assert f'"a": [{", ".join(chr(34) + r + chr(34) for r in a_rows)}],' in _source("letters.py")
    board = _source("console_3_board.py")
    assert 'MESSAGE = "attack at dawn"' in board and "KEY = 3" in board
    message = "attack at dawn"
    fits = max(n for n in range(1, 60) if 40 + (n - 1) * 16 + 12 <= 640)
    key10 = _shift(ALPHABET, 10)

    b = (
        '<h2><span class="num">4</span>The cipher console in pygame'
        '<span class="mins">25 minutes</span></h2>'
        "<p>Now put your cipher in a window. The alphabet sits on top, the coded "
        "alphabet sits under it, and the coded message appears one letter at a "
        "time.</p>"
        "<h3>Get the files</h3>"
    )
    b += (
        "<p>You will build the console in four programs. Each one adds one thing to the "
        "one before, so you can run it after every step and see what changed.</p>"
        '<ol class="tight">'
        + "".join(f"<li><code>{name}</code>: {what}.</li>" for name, what in STEPS)
        + "</ol>"
        "<p>Download all four, and <code>letters.py</code> with them, into one folder. "
        "<code>letters.py</code> is a module that draws letters. Steps 3 and 4 import "
        "it.</p>"
    )
    b += downloads(*[name for name, _ in STEPS], "letters.py")
    b += (
        "<p>The programs use pygame. If one stops with <code>ModuleNotFoundError: No "
        "module named 'pygame'</code>, type <code>pip install pygame</code> in the "
        "terminal and run it again.</p>"
        "<p>Here is the finished console after 130 frames, a little over two seconds. "
        "The orange boxes are around the letter being coded now: <code>c</code> on the "
        "top row becomes <code>f</code> on the row under it.</p>"
    )
    b += _shot(
        "cipher_console_130.png",
        "The console: the message attack at dawn at the top, the alphabet on cream "
        "tiles, the coded alphabet on green tiles, c and f boxed in orange, and dwwd "
        "at the bottom.",
    )

    b += "<h3>Step 1: a window</h3>"
    b += (
        "<p>Here is the first program, split into its parts. The label on each part "
        "says what the part does and when it runs: once, or again on every frame.</p>"
    )
    b += labelled_code(_source("console_1_window.py"), WINDOW_PARTS, "console_1_window.py")
    b += (
        "<p>Run it. A dark window opens and the terminal prints one line. The window "
        "stays open until you click its close button.</p>"
    )
    b += output("window open, close it to finish")
    b += "<h4>Before the loop</h4>"
    b += (
        '<ul class="tight">'
        "<li><code>pygame.init()</code> starts pygame. It comes before anything else "
        "from pygame.</li>"
        "<li><code>pygame.display.set_mode((640, 400))</code> opens a window 640 pixels "
        "wide and 400 pixels tall. A <b>pixel</b> is one dot of the screen. The window "
        "is stored in <code>screen</code>, and everything you draw goes onto "
        "<code>screen</code>.</li>"
        "<li><code>clock = pygame.time.Clock()</code> makes a clock. The loop uses it to "
        "control its speed.</li>"
        "<li><code>running</code> controls the loop. <code>while running:</code> keeps "
        "going while <code>running</code> is 1 and stops when it is 0. It starts at "
        "1.</li>"
        "</ul>"
        "<p><code>(640, 400)</code> is a <b>tuple</b>: values in round brackets, "
        "separated by commas, kept together as one value. That is why the line has two "
        "pairs of brackets. The outer pair are the brackets of the call to "
        "<code>set_mode</code>, the same as in <code>print(...)</code>. The inner pair "
        "make the tuple. pygame uses tuples for sizes, colors, and rectangles.</p>"
        "<p><code>BOARD = (15, 19, 24)</code> is a color. A color is a tuple of three "
        "numbers: how much red, how much green, and how much blue, each from 0 to 255. "
        "<code>(0, 0, 0)</code> is black and <code>(255, 255, 255)</code> is white. "
        "<code>(15, 19, 24)</code> has a little of each, so it is nearly black.</p>"
    )
    b += "<h4>The loop</h4>"
    b += (
        "<p>Each pass through the <code>while</code> loop draws one picture. One picture "
        "is called a <b>frame</b>. Each pass does three things, in this order:</p>"
        '<ol class="tight">'
        "<li><b>Read the events.</b> An <b>event</b> is something that happened since "
        "the last frame, such as a key press or a click. <code>pygame.event.get()</code> "
        "gives a list of them, and the <code>for</code> loop looks at each one. "
        "<code>pygame.QUIT</code> is the event for the window's close button.</li>"
        "<li><b>Draw.</b> <code>screen.fill(BOARD)</code> paints the whole window one "
        "color. Drawing happens out of sight.</li>"
        "<li><b>Show.</b> <code>pygame.display.flip()</code> puts the finished drawing on "
        "the screen. <code>clock.tick(60)</code> waits long enough that the loop runs no "
        "more than 60 times a second.</li>"
        "</ol>"
        "<p>After the loop, <code>pygame.quit()</code> closes the window.</p>"
    )
    b += reveal(
        "You click the window's close button. Which lines run, in order, from that click "
        "until <code>pygame.quit()</code>?",
        '<ol class="tight">'
        "<li><code>pygame.event.get()</code> gives an event whose type is "
        "<code>pygame.QUIT</code>.</li>"
        "<li>The gate <code>if event.type == pygame.QUIT:</code> says yes, so "
        "<code>running = 0</code> runs.</li>"
        "<li>The rest of that pass still runs: <code>screen.fill(BOARD)</code>, "
        "<code>pygame.display.flip()</code>, <code>clock.tick(60)</code>.</li>"
        "<li>Back at <code>while running:</code>, <code>running</code> is 0, so the loop "
        "stops.</li>"
        "<li><code>pygame.quit()</code> runs and the window closes.</li>"
        "</ol>"
        "<p>Nothing else in the program sets <code>running</code> to 0. The window "
        "never closes itself. You close it.</p>",
    )
    b += reveal(
        "At 60 frames a second, how many frames does the loop draw in 2 seconds?",
        "<p>60 × 2 = 120 frames.</p>",
    )

    b += "<h3>Step 2: rectangles</h3>"
    b += (
        "<p>Every point in the window has two numbers, x and y. x counts pixels across "
        "from the left edge. y counts pixels down from the top edge. The top left corner "
        "is <code>(0, 0)</code>. In math class y goes up. In pygame y goes down.</p>"
    )
    b += _grid_svg()
    b += (
        "<p><code>pygame.draw.rect(screen, TILE, (x, 130, 20, 26))</code> draws a "
        "filled rectangle on <code>screen</code> in the color <code>TILE</code>. The "
        "tuple is (x, y, width, height). The top left corner of the rectangle is at "
        "<code>(x, 130)</code>, and the rectangle is 20 pixels wide and 26 pixels "
        "tall.</p>"
    )
    b += code(_source("console_2_tiles.py"), "console_2_tiles.py")
    b += (
        "<p>Inside the <code>while</code> loop, the <code>for</code> loop draws 26 "
        "tiles, one for each letter. Tile <code>i</code> starts at "
        "<code>x = 20 + i * 23</code>: 20 pixels in from the left edge, then 23 more for "
        "each tile before it. A tile is 20 pixels wide, so there is a gap of 3 pixels "
        "between tiles.</p>"
    )
    b += reveal(
        "Where does the first tile start? Where does the last tile start? Does the last "
        "tile fit inside the 640 pixel window?",
        "<p>The first tile is <code>i = 0</code>: 20 + 0 × 23 = 20.</p>"
        "<p>The last tile is <code>i = 25</code>: 20 + 25 × 23 = 595.</p>"
        "<p>The last tile is 20 pixels wide, so its right edge is at 595 + 20 = 615. "
        "That is inside 640, so it fits.</p>"
        + output("first tile starts at x = 20\nlast tile starts at x = 595")
        + _shot("console_2_tiles_5.png", "A dark window with a row of 26 cream tiles."),
    )

    b += "<h3>Step 3: letters</h3>"
    b += (
        "<p>This course does not use pygame to write words, so each letter is drawn "
        "from small squares. <code>letters.py</code> holds a dictionary called "
        "<code>SHAPES</code> with one entry for each letter and one for the space. Here "
        "is the entry for <code>a</code>:</p>"
    )
    b += code('"a": [".#.", "#.#", "###", "#.#", "#.#"],', "letters.py, one entry of SHAPES")
    b += (
        "<p>Each string is one row, top to bottom. <code>#</code> is a filled square and "
        "<code>.</code> is an empty one.</p>"
    )
    b += _letter_svg(a_rows)
    b += (
        "<p>You do not need to read the rest of <code>letters.py</code>. You need its "
        "two functions. <code>import letters</code> works the same way "
        "<code>import sweep_tools</code> did in session 2.</p>"
        '<ul class="tight">'
        "<li><code>letters.draw_letter(screen, letter, x, y, size, color)</code> draws "
        "one letter with its top left corner at <code>(x, y)</code>. "
        "<code>size</code> is how many pixels wide each square is, so a letter is "
        "3 × <code>size</code> wide and 5 × <code>size</code> tall.</li>"
        "<li><code>letters.draw_word(screen, word, x, y, size, color)</code> draws a "
        "whole word, with one square of space between letters.</li>"
        "</ul>"
    )
    b += (
        "<p>Here is step 3. Compared with step 2, it adds:</p>"
        '<ul class="tight">'
        "<li><code>import letters</code>;</li>"
        "<li><code>MESSAGE</code>, <code>KEY</code>, <code>ALPHABET</code>, and four "
        "more colors;</li>"
        "<li><code>shift_by</code>, and the five lines under it that code the message "
        "and the alphabet and print them;</li>"
        "<li>in the tile loop, a letter on each tile and a second row of tiles;</li>"
        "<li>two lines that draw <code>MESSAGE</code> and <code>coded</code>.</li>"
        "</ul>"
    )
    b += code(board, "console_3_board.py")
    b += (
        "<p><code>shift_by</code> is the function you wrote in section 3, "
        "copied in unchanged.</p>"
        "<p><code>coded_row = shift_by(ALPHABET, KEY)</code> codes the whole alphabet in "
        "one call.</p>"
        "<p>In the tile loop, <code>ALPHABET[i]</code> is the letter at index "
        "<code>i</code> of the string <code>ALPHABET</code>. A string has indexes the "
        "same way a list does, so <code>ALPHABET[0]</code> is <code>a</code>. "
        "<code>coded_row[i]</code> is what that letter becomes, so the loop draws it on "
        "the tile directly under it.</p>"
        "<p><code>x + 7</code> and <code>138</code> put each letter in the middle of its "
        "tile. At size 2 a letter is 6 pixels wide and 10 tall. The tile is 20 wide, "
        "which leaves 7 pixels on each side, and 26 tall, which leaves 8 above and 8 "
        "below: 130 + 8 = 138.</p>"
    )
    b += reveal(
        "With <code>KEY = 3</code>, which letter is on the tile under <code>x</code>? "
        "Which letter is on the tile under <code>z</code>?",
        "<p>Under <code>x</code>: x is at position 23, counting <code>a</code> as 0. "
        "23 + 3 = 26, and 26 % 26 = 0, so "
        "the letter is <code>a</code>.</p>"
        "<p>Under <code>z</code>: z is at position 25. 25 + 3 = 28, and 28 % 26 = 2, so "
        "the letter is <code>c</code>.</p>"
        + output(
            f"plain: {message}\ncoded: dwwdfn dw gdzq\n"
            "coded row: defghijklmnopqrstuvwxyzabc"
        )
        + _shot(
            "console_3_board_5.png",
            "The board: attack at dawn at the top, the alphabet on cream tiles, the "
            "coded alphabet on green tiles, and dwwdfn dw gdzq at the bottom.",
        ),
    )
    b += (
        f"<p>Change <code>KEY</code> to 10 and run it again. The bottom row now starts "
        f"with <code>{key10[0]}</code> and ends with <code>{key10[-1]}</code>.</p>"
        f"<p><b>MESSAGE rules.</b> Keep <code>MESSAGE</code> to {fits} characters or "
        "fewer, or the end runs off the right edge. Use lowercase letters and spaces "
        "only. <code>SHAPES</code> has no entry for a capital letter or a period, so "
        "<code>MESSAGE = \"Attack at dawn\"</code> stops with the same error a plain "
        "dictionary gave you in section 2 for a missing key:</p>"
    )
    b += output("KeyError: 'A'")

    b += "<h3>Step 4: make it move</h3>"
    b += (
        "<p><code>cipher_console.py</code> starts from <code>console_3_board.py</code>. "
        "It adds one color, <code>GLOW</code>, for the boxes, and changes the program "
        "in three places. Here they are, one at a time.</p>"
        "<h4>Two accumulators</h4>"
        "<p>Before the loop:</p>"
    )
    b += code(_excerpt("cipher_console.py", "frame = 0", "shown = 0"), "cipher_console.py")
    b += (
        "<p><code>frame</code> counts the frames drawn so far. <code>shown</code> counts "
        "how many coded letters are showing. Both start at 0, like the accumulators in "
        "the opener.</p>"
        "<p>At the end of the loop body, just before <code>flip</code>:</p>"
    )
    b += code(
        _excerpt("cipher_console.py", "frame = frame + 1", "shown = shown + 1"),
        "cipher_console.py",
    )
    b += (
        "<p>Every frame adds 1 to <code>frame</code>. <code>frame % 30</code> is 0 on "
        "frames 30, 60, 90, and so on, so on every 30th frame one more coded letter "
        "shows. At 60 frames a second, that is one letter every half second. "
        "<code>shown &lt; len(MESSAGE)</code> stops <code>shown</code> once every letter "
        "is showing.</p>"
        "<h4>Draw the letters that are showing</h4>"
    )
    b += code(
        _excerpt("cipher_console.py", "for i in range(shown):", "letters.draw_letter(screen, coded[i]"),
        "cipher_console.py",
    )
    b += (
        "<p>These two lines take the place of the line that drew all of "
        "<code>coded</code> in step 3. They draw the first <code>shown</code> letters "
        "of <code>coded</code>. A "
        "letter at size 4 is 12 pixels wide, and the letters are 16 pixels apart, so "
        "there are 4 pixels between them.</p>"
        "<h4>Box the letter being coded</h4>"
    )
    b += code(
        _excerpt("cipher_console.py", "if shown < len(MESSAGE) and MESSAGE", "(x - 3, 187"),
        "cipher_console.py",
    )
    b += (
        "<p><code>MESSAGE[shown]</code> is the next letter to be coded. "
        "<code>spot</code> is its position in the alphabet, worked out the same way as in "
        "<code>shift_by</code>. The two rectangles go around its tile and around the tile "
        "under it.</p>"
        "<p>Each box is 3 pixels bigger than its tile on every side. The top tile starts "
        "at <code>(x, 130)</code> and is 20 by 26, so the box starts at "
        "<code>(x - 3, 127)</code> and is 26 by 32. The last number, 3, tells pygame to "
        "draw the outline only, 3 pixels thick, instead of a filled rectangle.</p>"
        "<p>A space has no tile, so the gate skips spaces.</p>"
        "<p>When <code>shown</code> reaches the end of the message, "
        "<code>shown &lt; len(MESSAGE)</code> is False, and Python does not check the "
        "right side of <code>and</code> at all. That matters, because there is no letter "
        "at that index. With the two sides swapped, the program stops as soon as the "
        "last coded letter shows:</p>"
    )
    b += output("IndexError: string index out of range", label="verified output, verify_console.py")
    b += reveal(
        f"<code>\"{message}\"</code> has {len(message)} characters, counting the two "
        "spaces. How many seconds until the whole coded message is showing?",
        f"<p>One letter every 30 frames, so {len(message)} × 30 = {len(message) * 30} "
        f"frames. At 60 frames a second, {len(message) * 30} ÷ 60 = "
        f"{len(message) * 30 // 60} seconds.</p>"
        "<p>Running the program for exactly 419 frames, and then for exactly 420, shows "
        "<code>shown</code> reaching 14 on frame 420:</p>"
        + output(
            "after 419 frames, shown is 13\n"
            "after 420 frames, shown is 14",
            label="verified output, verify_console.py",
        )
        + _shot(
            "cipher_console_700.png",
            "The finished console: dwwdfn dw gdzq complete at the bottom and no boxes.",
        ),
    )

    b += "<h4>The whole program</h4>"
    b += (
        "<p>Here is <code>cipher_console.py</code> from top to bottom, with the same "
        "kind of labels as step 1. Compare it with step 1: the loop still reads the "
        "events first and shows the drawing last. Everything in between, the parts "
        "labelled 2 to 5, is drawing and counting.</p>"
    )
    b += labelled_code(_source("cipher_console.py"), CONSOLE_PARTS, "cipher_console.py")

    stretch = laddered(
        "Make the R key start the coded message again from nothing.",
        [
            "<p>A key press is an event, like the close button. It arrives in the same "
            "<code>for event</code> loop.</p>",
            "<p><code>event.type == pygame.KEYDOWN</code> is True when the event is a key "
            "being pressed. <code>event.key == pygame.K_r</code> is True when that key is "
            "R. You need both, so join them with <code>and</code>, with the "
            "<code>event.type</code> check first.</p>",
            "<p>Starting again means putting the two accumulators back to their starting "
            "values.</p>",
        ],
        code(
            _excerpt("cipher_console_replay.py", "for event in pygame.event.get():", "shown = 0"),
            "cipher_console_replay.py",
        )
        + "<p>After R, <code>frame</code> counts up from 0 again. 100 frames later it "
        "has passed 30, 60, and 90, so <code>shown</code> is 3:</p>"
        + output(
            "R pressed on frame 600, shown is 3 after frame 700",
            label="verified output, verify_console.py",
        )
        + "<p>The order of the two checks matters, for the same reason as the box gate "
        "in step 4. Only a key event has <code>event.key</code>. Moving the mouse makes "
        "an event too, and with the two sides swapped, the first mouse movement stops "
        "the program:</p>"
        + output(
            "AttributeError: 'pygame.event.Event' object has no attribute 'key'",
            label="verified output, verify_console.py",
        )
        + "<p>With <code>event.type == pygame.KEYDOWN</code> first, a mouse event makes "
        "the left side False, and Python never reads <code>event.key</code>.</p>",
        "replay",
    )
    return b, stretch
