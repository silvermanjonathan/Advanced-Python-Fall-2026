"""Extras: pages that sit outside the thirteen sessions."""

import os

from build import code, downloads, labelled_code, laddered, masthead, output, pager, reveal
from days38 import cipher_strip, exits
from stds import panel


def extra_crack():
    """Extra page: break a Caesar cipher by counting letters."""
    b = masthead(
        None,
        "Break a Caesar cipher by counting letters",
        "Any time after session 3",
        "Learn dictionaries and Counter, a dictionary made for counting. Then count the "
        "letters of a message somebody encoded with a key you do not have, turn the most "
        "common one into a key, and decode it, without trying every key.",
        time=None,
        length="About 40 minutes",
        eyebrow="Advanced Python &middot; Robofun &middot; Extra",
    )
    b += (
        "<p>This page uses <code>shift_by</code>, the function you wrote in section 2 of "
        "session 3.</p>"
        '<div class="toolbar"><a class="btn quiet" href="wed03_counting.html">Back to '
        "session 3</a></div>"
    )

    b += (
        '<h2><span class="num">1</span>Dictionaries and Counter'
        '<span class="mins">15 minutes</span></h2>'
    )
    b += (
        "<p>To break a cipher by counting, you need a count for every letter. A "
        "<b>dictionary</b> keeps them. It stores each value under a name called a "
        "<b>key</b>: here the letter is the key and its count is the value. That is a "
        "different key from the cipher's key in section 2. You met a dictionary "
        "in session 3, <code>SHAPES</code> in <code>letters.py</code>, where each key "
        "was a letter and each value was its picture.</p>"
        "<p><code>{}</code> is an empty dictionary. <code>counts[\"b\"] = 0</code> "
        "stores 0 under the key <code>\"b\"</code>. The print line has a label so you "
        "can compare it with a Counter below.</p>"
    )
    b += code(
        """counts = {}
counts["b"] = 0
counts["b"] = counts["b"] + 1
print(f"made without Counter: {counts}")"""
    )
    b += reveal(
        "What prints? And what happens if you run <code>counts[\"z\"] + 1</code> "
        "without setting <code>counts[\"z\"]</code> first?",
        output("made without Counter: {'b': 1}")
        + "<p>The first one prints the dictionary: the key <code>'b'</code> with the "
        "value 1.</p>"
        "<p>The second one raises <code>KeyError: 'z'</code>. A dictionary does not start "
        "a missing key at zero for you. A Counter does, which is why it exists.</p>",
    )
    b += (
        "<p><code>collections</code> is a module that comes with Python, the same way "
        "<code>sweep_tools</code> was your own module in session 2. The line "
        "<code>from collections import Counter</code> takes one thing out of it, "
        "<code>Counter</code>, so you can write <code>Counter</code> instead of "
        "<code>collections.Counter</code>. That import line goes at the top of any file "
        "that uses a Counter.</p>"
        "<p>A <b>Counter</b> is a dictionary made for counting. Give it a string and it "
        "counts every character. Here is what else it can do.</p>"
    )
    b += code(
        """from collections import Counter

counts = Counter("banana")
print(f"made with Counter: {counts}")
print(counts["a"])
print(counts["z"])
print(counts.most_common(2))
print(counts.total())

counts.update("bandana")
print(f"made with Counter: {counts}")

first = Counter("listen")
second = Counter("silent")
print(first == second)""",
        "counter_tour.py",
    )
    b += reveal(
        "Two to predict before you run it. What does <code>counts[\"z\"]</code> print, "
        "when there is no z in banana? And what does the last line print?",
        output(
            """made with Counter: Counter({'a': 3, 'n': 2, 'b': 1})
3
0
[('a', 3), ('n', 2)]
6
made with Counter: Counter({'a': 6, 'n': 4, 'b': 2, 'd': 1})
True"""
        )
        + "<p>One line at a time:</p>"
        '<ul class="tight">'
        "<li><code>counts[\"a\"]</code> reads one count, the same way as a dictionary: "
        "3.</li>"
        "<li><code>counts[\"z\"]</code> is 0. A plain dictionary would stop with "
        "<code>KeyError</code>. A Counter gives 0 for anything it has not seen.</li>"
        "<li><code>most_common(2)</code> returns the top two, biggest first, as pairs "
        "of letter and count. Section 2 uses this to find the top letter.</li>"
        "<li><code>total()</code> adds up every count: banana has 6 letters.</li>"
        "<li><code>update(\"bandana\")</code> counts more letters into the same "
        "Counter, so a goes from 3 to 6.</li>"
        "<li><code>first == second</code> is <code>True</code> when two Counters have "
        "the same counts. listen and silent use the same letters the same number of "
        "times, so they are anagrams: two words made from the same letters.</li>"
        "</ul>",
    )

    b += (
        '<h2><span class="num">2</span>Break one'
        '<span class="mins">25 minutes</span></h2>'
    )
    b += (
        "<p>Here is a message somebody encoded with a key you do not have. You could "
        "try all 26 keys, and for a Caesar cipher that is fast enough. There is a "
        "faster way: count the letters.</p>"
        "<p>In ordinary English, <code>e</code> is the most common letter. So the most "
        "common letter in the ciphertext is probably what <code>e</code> turned into. "
        "Breaking the cipher takes three steps: count the letters, turn the top letter "
        "into a key, and decode. Do them one at a time.</p>"
    )
    b += code(
        '''ciphertext = "uhdg wkh frgh dqg wudfh wkh frgh ehiruh brx hyhu uxq wkh frgh"''',
        "the message",
    )

    b += "<h3>Step 1: count the letters</h3>"
    b += (
        "<p>This is the <code>Counter</code> from section 1, with the spaces taken out "
        "first. The file starts with <code>from collections import Counter</code>, the "
        "same import line as in section 1. <code>counts.most_common(5)</code> returns "
        "the five most common letters with how many times each appears, biggest "
        "first.</p>"
    )
    b += code(
        '''from collections import Counter


def letter_counts(text):
    """Return a Counter of the letters in text, ignoring spaces."""
    letters = ""
    for ch in text:
        if ch != " ":
            letters = letters + ch
    return Counter(letters)


counts = letter_counts(ciphertext)
print("five most common:", counts.most_common(5))''',
        "caesar_crack.py, step 1",
    )
    b += reveal(
        "Look at the message before you run anything. Which letter do you see most "
        "often?",
        output("five most common: [('h', 12), ('u', 5), ('g', 5), ('r', 5), ('w', 4)]")
        + "<p><code>h</code> appears 12 times. The next letters appear 5 times each. "
        "So <code>h</code> is the top letter, and it is probably what <code>e</code> "
        "turned into.</p>",
    )

    b += "<h3>Step 2: turn the top letter into a key</h3>"
    b += (
        "<p>If <code>e</code> turned into <code>h</code>, the key is how many places "
        "<code>e</code> moved. Use the strip: click <code>e</code> in the top row, then "
        "press <b>+1</b> until the bottom row under <code>e</code> shows "
        "<code>h</code>.</p>"
    )
    b += cipher_strip("strip2")
    b += laddered(
        "What is the key?",
        [
            "<p>Count along the alphabet from <code>e</code> to <code>h</code>.</p>",
            "<p><code>e</code>, <code>f</code>, <code>g</code>, <code>h</code>. How many "
            "moves is that?</p>",
            "<p>In code, it is the distance between the two letters' numbers: "
            "<code>ord(\"h\") - ord(\"e\")</code>, which is 104 minus 101.</p>",
        ],
        "<p>The key is 3.</p>"
        + code(
            '''def guess_shift(text):
    """Return the shift that maps the most common letter onto 'e'."""
    counts = letter_counts(text)
    top_letter = counts.most_common(1)[0][0]
    return (ord(top_letter) - ord("e")) % 26''',
            "caesar_crack.py, step 2",
        )
        + "<p><code>counts.most_common(1)[0][0]</code> is the top letter: the first "
        "pair in the list, and the letter in that pair. The <code>% 26</code> is for "
        "a top letter that comes before <code>e</code> in the alphabet. If the top "
        "letter were <code>b</code>, 98 minus 101 is -3, and <code>% 26</code> turns "
        "it into 23: <code>e</code> moved 23 places and wrapped round to "
        "<code>b</code>.</p>",
        "crack-key",
    )

    b += "<h3>Step 3: decode</h3>"
    b += (
        "<p>You have the key, and you have <code>shift_by</code> from session 3. "
        "Moving every letter back by the key undoes the cipher, so decode with a "
        "negative key.</p>"
    )
    b += code(
        '''k = guess_shift(ciphertext)
print(f"guessed shift {k}")
print("plaintext:", shift_by(ciphertext, -k))''',
        "caesar_crack.py, step 3",
    )
    b += reveal(
        "The first word of the message is <code>uhdg</code>. Move each letter back 3 "
        "by hand. What is the first word of the plaintext?",
        output("guessed shift 3\nplaintext: read the code and trace the code before you ever run the code")
        + "<p><code>u</code> goes back to <code>r</code>, <code>h</code> to "
        "<code>e</code>, <code>d</code> to <code>a</code>, <code>g</code> to "
        "<code>d</code>: <code>read</code>. The program does the same for every "
        "letter.</p>",
    )

    b += "<h3>The whole program</h3>"
    b += (
        "<p>Here are the three steps in one file, with <code>shift_by</code> at the "
        "top. It is the same function you wrote in session 3.</p>"
    )
    b += code(
        '''"""Break a Caesar cipher by letter frequency instead of by guessing."""

from collections import Counter

ciphertext = "uhdg wkh frgh dqg wudfh wkh frgh ehiruh brx hyhu uxq wkh frgh"


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


def letter_counts(text):
    """Return a Counter of the letters in text, ignoring spaces."""
    letters = ""
    for ch in text:
        if ch != " ":
            letters = letters + ch
    return Counter(letters)


def guess_shift(text):
    """Return the shift that maps the most common letter onto 'e'."""
    counts = letter_counts(text)
    top_letter = counts.most_common(1)[0][0]
    return (ord(top_letter) - ord("e")) % 26


counts = letter_counts(ciphertext)
print("five most common:", counts.most_common(5))

k = guess_shift(ciphertext)
print(f"guessed shift {k}")
print("plaintext:", shift_by(ciphertext, -k))''',
        "caesar_crack.py",
    )
    b += reveal(
        "Run it. Do its lines match what you worked out in steps 1, 2, and 3?",
        output(
            """five most common: [('h', 12), ('u', 5), ('g', 5), ('r', 5), ('w', 4)]
guessed shift 3
plaintext: read the code and trace the code before you ever run the code"""
        )
        + "<p>They match.</p>"
        "<p>Two limits. The text has to be long enough for <code>e</code> to actually "
        "win, and the text has to be ordinary English. Try it on a short message and "
        "watch it fail.</p>",
    )
    b += (
        '<div class="predict"><b>Frequency counts are ratios.</b> 12 of 49 letters is '
        "about 0.24. In ordinary English <code>e</code> runs near 0.12. Your sample is "
        "small, so your share is off.</div>"
    )
    b += exits(
        "You ran <code>counter_tour.py</code> and can say what a Counter gives for a "
        "letter it has not seen, and you ran <code>letter_counts</code> on the "
        "ciphertext and read the top letter off the output.",
        "Floor, plus the full crack running and printing the plaintext.",
        "Middle, plus break it on purpose: find a message short enough that the most "
        "common letter is not <code>e</code>, then write a <code>guess_shift</code> "
        "that scores all 26 shifts against English letter frequencies and picks the "
        "best total instead of trusting one letter.",
    )
    b += panel(
        ["6.SP.B.5.a", "6.RP.A.3", "MP7"],
        "<p>About 40 minutes, any time after session 3: 15 dictionaries and Counter, 25 "
        "breaking the cipher. It needs <code>shift_by</code> from session 3's section 2. "
        "Use it "
        "as a take-home, for a student who finishes early, or as a whole session if the "
        "room has time.</p>",
        "<p>Students read <code>counts[\"z\"]</code> giving 0 as a bug. It is the point "
        "of a Counter: a plain dictionary stops with <code>KeyError</code> for a key it "
        "has not seen, and a Counter gives 0.</p>"
        "<p>Some students will want to brute force all 26 shifts because it is easier "
        "to write. Let them, then ask what they would do with a Vigenere key of length "
        "7. Brute force stops being available and counting does not.</p>"
        "<p>Session 4's opener asks what happens to letter counts when letters are only "
        "moved. Students who did this page will see straight away that counting no "
        "longer helps.</p>",
        retouch=(
            "The returning functions from session 2: <code>guess_shift</code> is only "
            "possible because <code>letter_counts</code> returns a Counter."
        ),
        extras=(
            "<h3>Files</h3><p><code>counter_tour.py</code> for section 1 and "
            "<code>caesar_crack.py</code> for section 2. Output verified on Python "
            "3.12.3. The build checks that its <code>shift_by</code> is identical to the "
            "one in <code>caesar_encode.py</code>. The plaintext restates this course's "
            "own rule from session 1, which is deliberate.</p>"
            "<h3>Lifted on this page</h3><p>Dictionaries, keys and "
            "<code>KeyError</code>, and <code>collections.Counter</code>: "
            "<code>most_common</code>, <code>total</code>, <code>update</code>, and "
            "comparing two Counters.</p>"
        ),
    )
    b += pager(
        ("wed03_counting.html", "Session 3: a cipher in a window"),
        ("wed04_transposition.html", "Session 4: moving letters"),
    )
    return b


_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _read(name):
    """Return a file from the repo root, without its last newline."""
    return open(os.path.join(_ROOT, name)).read().rstrip("\n")


def _function(name, source):
    """Return one function from source, from its def line to the blank lines after it."""
    start = source.index(f"def {name}")
    end = source.find("\n\n\n", start)
    return source[start:end if end > 0 else len(source)].rstrip("\n")


def _grid_svg(rows):
    """Return a letter's 5 by 3 grid with row and column numbers, and its strings beside."""
    cell, gap, left, top = 40, 4, 64, 30
    parts = []
    for c in range(3):
        parts.append(
            f'<text x="{left + c * (cell + gap) + cell / 2}" y="{top - 9}" '
            'text-anchor="middle" font-size="14" fill="#4A4D53">col ' + str(c) + "</text>"
        )
    for r, text in enumerate(rows):
        yy = top + r * (cell + gap)
        parts.append(
            f'<text x="{left - 10}" y="{yy + 25}" text-anchor="end" font-size="14" '
            f'fill="#4A4D53">row {r}</text>'
        )
        for c, mark in enumerate(text):
            fill = "#0E4D52" if mark == "#" else "#FFFDF7"
            parts.append(
                f'<rect x="{left + c * (cell + gap)}" y="{yy}" width="{cell}" '
                f'height="{cell}" fill="{fill}" stroke="#D3CBB8"/>'
            )
        parts.append(
            f'<text x="{left + 3 * (cell + gap) + 18}" y="{yy + 25}" font-size="15" '
            f'font-family="monospace" fill="#17181B">shape[{r}] is "{text}"</text>'
        )
    height = top + 5 * (cell + gap) + 4
    return (
        f'<svg viewBox="0 0 420 {height}" width="420" style="max-width:100%; '
        'height:auto; display:block; margin:10px 0 16px" role="img" aria-label="The '
        "letter a on a grid of 5 rows and 3 columns, rows numbered 0 to 4 from the top, "
        'columns 0 to 2 from the left, with each row\'s string beside it.">'
        + "".join(parts) + "</svg>"
    )


LETTER_PARTS = [
    ("def draw_letter", "The function and its docstring. It is given the window, the "
     "letter, where the letter's top left corner goes, how big each square is, and the "
     "color.", ""),
    ("shape = SHAPES[letter]", "Look up the letter's five strings in the dictionary. "
     "This runs once each time the function is called.", "once"),
    ("for row in range(5):", "Outer loop: <code>row</code> is 0, 1, 2, 3, 4, top to "
     "bottom. It runs 5 times.", "frame"),
    ("for col in range(3):", "Inner loop: <code>col</code> is 0, 1, 2, left to right. It "
     "runs 3 times for every row, so 15 times in all.", "frame"),
    ('if shape[row][col] == "#":', "The gate: draw only where the mark is "
     "<code>#</code>. It is checked 15 times.", "frame"),
    ("pygame.draw.rect", "One square, <code>size</code> pixels wide and tall, with its "
     "top left corner at <code>(x + col * size, y + row * size)</code>.", "frame"),
]


def extra_letters():
    """Extra page: how letters.py stores a letter and draws it from squares."""
    src = _read("letters.py")
    tour = _read("letters_tour.py")
    tour_out = (
        "['.#.', '#.#', '###', '#.#', '#.#']\n###\n#"
    )
    a_rows = [".#.", "#.#", "###", "#.#", "#.#"]
    assert '    "a": [".#.", "#.#", "###", "#.#", "#.#"],' in src
    x, y, size = 100, 50, 10
    squares = [(r, c) for r in range(5) for c in range(3) if a_rows[r][c] == "#"]
    trace = "\n".join(
        f"row {r} col {c}: square at ({x + c * size}, {y + r * size})" for r, c in squares
    ) + f"\nsquares drawn: {len(squares)}"
    starts = "\n".join(f"letter {i} starts at x = {40 + i * 4 * 4}" for i in range(3))

    b = masthead(
        None,
        "How letters.py draws a letter",
        "Any time after session 3",
        "In session 3, letters.py drew every letter in the cipher console. Here is how "
        "it works, line by line: a dictionary of pictures, two loops, and one gate.",
        time=None,
        length="About 30 minutes",
        eyebrow="Advanced Python &middot; Robofun &middot; Extra",
    )
    b += (
        "<p>Put these two files in one folder. <code>letters_tour.py</code> is a short "
        "program that prints what <code>letters.py</code> does, step by step.</p>"
    )
    b += downloads("letters.py", "letters_tour.py")
    b += (
        "<p>When pygame loads, it prints two lines of its own, starting with "
        "<code>pygame 2</code>. They are left out of the outputs on this page.</p>"
        '<div class="toolbar"><a class="btn quiet" href="wed03_counting.html">Back to '
        "session 3</a></div>"
    )

    b += (
        '<h2><span class="num">1</span>A letter is five strings'
        '<span class="mins">10 minutes</span></h2>'
        "<p><code>letters.py</code> starts with a dictionary called <code>SHAPES</code>. "
        "Here are its first two entries. After them come 25 more, one for each other "
        "letter and one for the space, then a closing <code>}</code>.</p>"
    )
    first = src[src.index("SHAPES = {"):]
    first = "\n".join(first.split("\n")[:3])
    b += code(first, "letters.py, the start of SHAPES")
    b += (
        "<p>Each key is a letter. Each value is a <b>list</b> of five strings, one "
        "string for each row of the picture, top to bottom. Each string has three "
        "characters, one for each column, left to right. <code>#</code> is a filled "
        "square and <code>.</code> is an empty one.</p>"
        "<p>Rows and columns are numbered from 0, the same as list indexes. Here is "
        "<code>a</code> on its grid:</p>"
    )
    b += _grid_svg(a_rows)
    b += (
        "<h3>Two indexes</h3>"
        "<p><code>shape = letters.SHAPES[\"a\"]</code> gives you the list of five "
        "strings. <code>shape[2]</code> picks one string from the list: row 2. A second "
        "index picks one character from that string, so <code>shape[2][1]</code> is "
        "row 2, column 1.</p>"
        "<p>So <code>shape[row][col]</code> is the mark at that row and column. The "
        "first index is the row. The second is the column.</p>"
    )
    b += code(tour[tour.index("shape = "):tour.index("\n\nx = ")], "letters_tour.py, first part")
    b += reveal(
        "What do the three print lines show? For the last one, find row 0 on the grid "
        "first, then column 1.",
        output(tour_out)
        + "<p>The first line is the whole list. The second is row 2, <code>###</code>. "
        "The third is row 0, column 1: the middle of <code>.#.</code>, which is "
        "<code>#</code>.</p>",
    )

    b += (
        '<h2><span class="num">2</span>draw_letter: two loops and a gate'
        '<span class="mins">15 minutes</span></h2>'
        "<p>Here is <code>draw_letter</code>, with each part labelled.</p>"
    )
    b += labelled_code(_function("draw_letter", src), LETTER_PARTS, "letters.py")
    b += (
        "<p>One loop is inside the other. The inner loop runs all the way through for "
        "every pass of the outer loop, so the order is row 0, columns 0, 1, 2; then row "
        "1, columns 0, 1, 2; and so on down to row 4. That is 5 × 3 = 15 checks, one for "
        "each square of the grid.</p>"
        "<p>Each step right adds <code>size</code> to x. Each step down adds "
        "<code>size</code> to y, because in pygame y counts down from the top. So the "
        "square for row 2, column 1 starts 1 square right and 2 squares down from the "
        "letter's corner.</p>"
    )
    b += reveal(
        f"Say <code>x</code> is {x}, <code>y</code> is {y} and <code>size</code> is "
        f"{size}. Where is the top left corner of the square for row 2, column 1? And "
        "how many squares does <code>draw_letter</code> draw for <code>a</code>?",
        f"<p>Row 2, column 1: x is {x} + 1 × {size} = {x + size}, and y is {y} + 2 × "
        f"{size} = {y + 2 * size}. The corner is at ({x + size}, {y + 2 * size}).</p>"
        f"<p>Count the <code>#</code> marks: 1 + 2 + 3 + 2 + 2 = {len(squares)}. The "
        "gate lets one square through for each one.</p>",
    )
    b += (
        "<p>The rest of <code>letters_tour.py</code> runs the same two loops and the "
        "same gate as <code>draw_letter</code>, with the same numbers. Instead of "
        "drawing each square, it prints where the square goes.</p>"
    )
    b += code(tour[tour.index("x = 100"):tour.index("\n\nfor i in range(3)")],
              "letters_tour.py, second part")
    b += output(trace)
    b += (
        "<p>Ten squares, in order: row by row, and left to right in each row.</p>"
    )

    b += (
        '<h2><span class="num">3</span>draw_word: one letter after another'
        '<span class="mins">5 minutes</span></h2>'
    )
    b += code(_function("draw_word", src), "letters.py")
    b += (
        "<p><code>word[i]</code> is letter <code>i</code> of the word, and "
        "<code>draw_word</code> calls <code>draw_letter</code> once for each one. Every "
        "letter gets the same <code>y</code>. Only x changes.</p>"
        "<p>A letter is 3 squares wide, and one empty square goes between letters, so "
        "each letter starts 4 squares to the right of the one before. That is "
        "<code>i * 4 * size</code> pixels from the first letter.</p>"
    )
    b += code(tour[tour.index("for i in range(3)"):], "letters_tour.py, last part")
    b += reveal(
        "The cipher console draws <code>MESSAGE</code> with "
        "<code>letters.draw_word(screen, MESSAGE, 40, 50, 4, PLAIN_INK)</code>. Where do "
        "the first three letters start?",
        output(starts)
        + "<p>With <code>size</code> 4, letters are 4 × 4 = 16 pixels apart: 40, 56, 72. "
        "That is why step 4 of the console draws the coded letters at "
        "<code>40 + i * 16</code>: the same spacing as <code>draw_word</code>.</p>",
    )

    b += exits(
        "You can say what <code>SHAPES[\"a\"][2]</code> is and why, and which index of "
        "<code>shape[row][col]</code> picks the row.",
        "Floor, plus on paper, trace <code>draw_letter</code> for <code>t</code> at "
        "<code>x</code> 0, <code>y</code> 0, <code>size</code> 10: list every square it "
        "draws, in order. Then change <code>\"a\"</code> to <code>\"t\"</code> in "
        "<code>letters_tour.py</code> and check your list.",
        "Middle, plus design a picture for <code>!</code>, add it to <code>SHAPES</code> "
        "in your copy of <code>letters.py</code>, and draw the word <code>hi!</code> in "
        "a window with <code>letters.draw_word</code>.",
    )
    b += panel(
        ["5.G.A.1", "MP7"],
        "<p>About 30 minutes, any time after session 3: 10 the dictionary and its two "
        "indexes, 15 <code>draw_letter</code>, 5 <code>draw_word</code>. It suits "
        "students who finished the console and asked how the letters work.</p>",
        "<p>The double index is the hard part. Students read <code>shape[2][1]</code> as "
        "one number, or swap the row and the column. Have them point at the grid: the "
        "first index goes down to a row, the second goes across to a column.</p>"
        "<p>Nested loops are new. The trace output is the answer to \"in what order?\": "
        "it lists the squares row by row. If a student expects column by column, ask "
        "which loop is on the outside.</p>"
        "<p>y points down here too, so row 4 has the biggest y.</p>",
        retouch=(
            "Session 3's console: <code>letters.py</code>, <code>SHAPES</code>, and "
            "draw positions in pixels. The <code>count</code> in "
            "<code>letters_tour.py</code> is an accumulator from session 3's opener."
        ),
        extras=(
            "<h3>Files</h3><p><code>letters.py</code> and <code>letters_tour.py</code>. "
            "<code>verify_letters.py</code> calls the real <code>draw_letter</code> and "
            "<code>draw_word</code> without a screen, records every square and letter "
            "position they ask pygame for, and prints them in the tour's words. The "
            "output check confirms both programs print the same lines, so the tour "
            "tells the truth about <code>letters.py</code>. Verified on Python 3.12.3 and "
            "pygame 2.6.1.</p>"
            "<h3>Lifted on this page</h3><p>A list of strings as a grid, two indexes "
            "(<code>shape[row][col]</code>), and one loop inside another.</p>"
        ),
    )
    b += pager(
        ("extra_crack_caesar.html", "Extra: break a Caesar cipher"),
        ("wed04_transposition.html", "Session 4: moving letters"),
    )
    return b
