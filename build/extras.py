"""Extras: pages that sit outside the thirteen sessions."""

from build import code, laddered, masthead, output, pager, reveal
from days38 import cipher_strip, exits
from stds import panel


def extra_crack():
    """Extra page: break a Caesar cipher by counting letters."""
    b = masthead(
        None,
        "Break a Caesar cipher by counting letters",
        "Any time after session 3",
        "Learn Counter, a dictionary made for counting. Then count the letters of a "
        "message somebody encoded with a key you do not have, turn the most common one "
        "into a key, and decode it, without trying every key.",
        time=None,
        length="About 35 minutes",
        eyebrow="Advanced Python &middot; Robofun &middot; Extra",
    )
    b += (
        "<p>This page uses two things from session 3: dictionaries, from section 2, "
        "and <code>shift_by</code>, the function you wrote in section 3.</p>"
        '<div class="toolbar"><a class="btn quiet" href="wed03_counting.html">Back to '
        "session 3</a></div>"
    )

    b += '<h2><span class="num">1</span>Counter<span class="mins">10 minutes</span></h2>'
    b += (
        "<p>In session 3 you counted with a plain dictionary. You had to set a key to 0 "
        "before you could add 1 to it, or Python stopped with <code>KeyError</code>. "
        "Here is that example again, with a label on its print line.</p>"
    )
    b += code(
        """counts = {}
counts["b"] = 0
counts["b"] = counts["b"] + 1
print(f"made without Counter: {counts}")"""
    )
    b += output("made without Counter: {'b': 1}")
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
        "<p>About 35 minutes, any time after session 3: 10 Counter, 25 breaking the "
        "cipher. It needs dictionaries from session 3's section 2 and "
        "<code>shift_by</code> from its section 3. Use it "
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
            "<h3>Lifted on this page</h3><p><code>collections.Counter</code>: "
            "<code>most_common</code>, <code>total</code>, <code>update</code>, and "
            "comparing two Counters.</p>"
        ),
    )
    b += pager(
        ("wed03_counting.html", "Session 3: counting and a cipher"),
        ("wed04_transposition.html", "Session 4: moving letters"),
    )
    return b
