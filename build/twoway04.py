"""Session 4: the cipher console asks whether to encrypt or decrypt, then does it."""

import os
import subprocess

from build import (answer_key, code, downloads, labelled_code, laddered, masthead,
                   output, pager, reveal)
from console03 import _excerpt, _shot, _source
from stds import panel
from twoway_edits import (ANSWERS, DOCSTRING_4, QUESTION, STEP_EDITS, STEP_FILES,
                          STRETCH_FILE, build_texts)

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERIFIED = "verified output, verify_two_way.py"

QUESTION_PARTS = [
    ('if mode == "":', "The gate. The lines under it run only while nobody has "
     "answered yet, when <code>mode</code> is still the empty string.", "frame"),
    ("screen.fill(BOARD)", "Paint the whole window over, on top of the console "
     "drawn above. Drawing happens out of sight until "
     "<code>pygame.display.flip()</code>, so the console never shows.", "frame"),
    ('letters.draw_word(screen, "do you want to"', "The question, in two lines of "
     "the letters from <code>letters.py</code>.", "frame"),
    ("pygame.draw.rect(screen, TILE,", "A cream square with a big e on it, and the "
     "word encrypt under it. Cream is the color of the plain alphabet in the console.",
     "frame"),
    ("pygame.draw.rect(screen, CODED_TILE,", "A green square with a big d on it, and "
     "the word decrypt under it. Green is the color of the coded alphabet.", "frame"),
]

ANSWER_PARTS = [
    ("if event.type == pygame.KEYDOWN and event.key == pygame.K_e:", "The gate for E. "
     "It is True only when the event is a key press and the key is E.", "frame"),
    ('mode = "encrypt"', "Remember the answer. Now <code>mode</code> is not the empty "
     "string, so the question stops showing.", "frame"),
    ("coded = shift_by(MESSAGE, KEY)", "Code the message and the alphabet with "
     "<code>KEY</code>.", "frame"),
    ("frame = 0", "Put the two accumulators back to 0, so the coded letters start "
     "again from the first one.", "frame"),
    ("if event.type == pygame.KEYDOWN and event.key == pygame.K_d:", "The gate for D.",
     "frame"),
    ('mode = "decrypt"', "Remember the answer.", "frame"),
    ("coded = shift_by(MESSAGE, -KEY)", "Code the message and the alphabet with "
     "<code>-KEY</code>, the opposite of the key.", "frame"),
    ("frame = 0", "Start the letters again from the first one.", "frame"),
]


def _check_files():
    """Check the program files on disk are the ones the page's steps make."""
    for name, text in build_texts(_ROOT).items():
        assert _source(name) + "\n" == text, f"{name} is out of date: run build/twoway_edits.py --write"

    def grab(name):
        text = _source(name)
        start = text.find("def shift_by")
        return text[start:text.find("\n\n\n", start)]

    for name in ("undo_tour.py", STEP_FILES[3], STRETCH_FILE):
        assert grab(name) == grab("caesar_encode.py"), f"shift_by differs in {name}"


def _undo_lines():
    """Return undo_tour.py's printed lines, run here so the page quotes a real run."""
    run = subprocess.run(["python3", "undo_tour.py"], cwd=_ROOT, capture_output=True,
                         text=True, check=True)
    lines = run.stdout.rstrip("\n").split("\n")
    assert lines == ["gdzq", "dawn", "zab", "25", "hello"], lines
    return lines


def _prints_lines():
    """Return the print lines at the top of two_way_console.py, as the page shows them."""
    text = _source(STEP_FILES[3])
    return "\n".join(ln for ln in text.split("\n") if ln.startswith("print("))


def day04():
    """Session 4: encrypt or decrypt, in one window."""
    from days38 import exits

    _check_files()
    undo = _undo_lines()
    message3 = "attack at dawn"
    fits = max(n for n in range(1, 60) if 40 + (n - 1) * 16 + 12 <= 640)
    starter_prints = (
        f"plain: {message3}\ncoded: dwwdfn dw gdzq\ncoded row: defghijklmnopqrstuvwxyzabc"
    )
    prints4 = (
        "message: dwwdfn dw gdzq\nencrypted with key 3: gzzgiq gz jgct\n"
        "decrypted with key 3: attack at dawn"
    )

    b = masthead(
        "04",
        "Encrypt or decrypt, in one window",
        "Wednesday 7 October 2026",
        "In session 3 the console turned a message into code. Today it goes both ways. "
        "When the window opens, it asks whether you want to encrypt or decrypt, and you "
        "answer with a key on the keyboard.",
    )

    # Section 1: the opener
    b += (
        '<h2><span class="num">1</span>Opener: a negative key undoes a positive one'
        '<span class="mins">10 minutes</span></h2>'
        "<p>To <b>encrypt</b> a message is to turn plaintext into ciphertext. To "
        "<b>decrypt</b> it is to turn the ciphertext back into plaintext. In session 3, "
        "the last test line was <code>print(shift_by(\"gdzq\", -3))</code>, and it printed "
        "<code>dawn</code>. Moving every letter back 3 undid moving it forward 3.</p>"
        "<p>On paper, predict what each line of this program prints. "
        "<code>shift_by</code> is the same function you wrote in session 3. In the last "
        "line, the inner call runs first, and its result goes into the outer call.</p>"
    )
    b += code(
        _excerpt("undo_tour.py", 'print(shift_by("dawn", 3))', "-7))"),
        "undo_tour.py, under shift_by",
    )
    b += reveal(
        "Lines 1 and 2.",
        output("\n".join(undo[:2]), label="verified output, undo_tour.py")
        + "<p>Line 1 encrypts <code>dawn</code> with key 3. Line 2 decrypts the result "
        "with key -3 and gets <code>dawn</code> back.</p>",
    )
    b += reveal(
        "Line 3 moves <code>a</code> back 1, past the start of the alphabet. Which letter "
        "does it land on? Line 4 is the step inside <code>shift_by</code> that decides "
        "it.",
        output("\n".join(undo[2:4]), label="verified output, undo_tour.py")
        + "<p><code>a</code> is at position 0, and 0 - 1 = -1. <code>% 26</code> always "
        "gives a number from 0 to 25, even when the number before it is negative, so "
        "<code>-1 % 26</code> is 25. Position 25 is <code>z</code>. It is the same wrap "
        "as in session 3, run backwards: going forward past z comes around to a, and going "
        "back past a comes around to z.</p>",
    )
    b += reveal(
        "Line 5.",
        output(undo[4], label="verified output, undo_tour.py")
        + "<p>7 moves every letter forward and -7 moves it back the same distance. 7 and "
        "-7 are <b>opposites</b>: the same size, in opposite directions, so together "
        "they add to 0. A shift of 0 changes nothing, so <code>hello</code> comes back. "
        "That is the idea for the whole session: <b>decrypting is encrypting with the "
        "opposite key</b>.</p>",
    )

    # Section 2: the question screen
    b += (
        '<h2><span class="num">2</span>A question in the window'
        '<span class="mins">30 minutes</span></h2>'
        "<p>Today's program starts as the finished console from session 3. By the end, "
        "the window opens on a question, and E or D answers it.</p>"
    )
    b += _shot(
        "two_way_console_5.png",
        "The question screen: do you want to encrypt or decrypt, a cream square with E "
        "labeled encrypt, and a green square with D labeled decrypt.",
    )
    b += (
        "<h3>Get the files</h3>"
        "<p>You need two files in the same folder: the finished console from session 3, "
        "which saves as <code>two_way_console.py</code>, and <code>letters.py</code>.</p>"
    )
    b += downloads(("cipher_console.py", "two_way_console.py"), "letters.py")
    b += (
        '<div class="now"><p><b>Now open the files.</b> Do these four things before '
        "you type any code.</p>"
        '<ol class="tight">'
        "<li>Put both files in the same folder. If your browser saved the console as "
        "<code>cipher_console.py</code>, rename it to <code>two_way_console.py</code>.</li>"
        "<li>In VS Code, choose File, then Open Folder, and open that folder.</li>"
        "<li>Click <code>two_way_console.py</code> in the list on the left to open "
        "it.</li>"
        "<li>Run it without changing anything. The session 3 console opens, and the "
        "terminal shows these three lines:</li>"
        "</ol>"
    )
    b += output(starter_prints)
    b += (
        "<p>Before them, pygame prints two lines of its own, starting with "
        "<code>pygame 2</code>. If the program stops with <code>No module named "
        "'letters'</code>, the two files are not in the same folder. If it stops with "
        "<code>No module named 'pygame'</code>, type <code>pip install pygame</code> in "
        "the terminal and run it again.</p></div>"
    )

    b += "<h3>Step 1: ask the question</h3>"
    b += (
        "<p>The program needs a variable that remembers the answer. <code>mode</code> "
        "starts as the empty string, which means nobody has answered yet. Later it will "
        "be <code>\"encrypt\"</code> or <code>\"decrypt\"</code>. Just above "
        "<code>running = 1</code>, add:</p>"
    )
    b += code(STEP_EDITS[1][0][2], "two_way_console.py, step 1, above running = 1")
    b += (
        "<p>Then find the loop that draws the letters that are showing. Under it, four "
        "spaces in, the same as <code>screen.fill(BOARD)</code>, add these lines. "
        "There is a button under each part. Before you press it, say what you think "
        "that part does.</p>"
    )
    b += labelled_code(QUESTION.strip("\n"), QUESTION_PARTS,
                       "two_way_console.py, step 1, after the letters that are showing")
    b += (
        "<p>The console is still drawn on every frame, and then, while "
        "<code>mode</code> is empty, painted over. That way none of the console's lines "
        "have to move.</p>"
        "<p>Each big letter is drawn at size 12, so it is 3 × 12 = 36 pixels wide and "
        "5 × 12 = 60 pixels tall.</p>"
    )
    b += reveal(
        "The cream square starts at x = 150 and is 120 pixels wide. Why is the e drawn "
        "at x = 192?",
        "<p>The square has 120 - 36 = 84 pixels to spare across, 42 on each side. "
        "150 + 42 = 192. The same sum down: 120 - 60 = 60 to spare, 30 above, and "
        "140 + 30 = 170.</p>",
    )
    b += reveal(
        "Run it. What does the window show? Then click the window and press E. What "
        "happens?",
        _shot(
            "two_way_step1_60.png",
            "The question screen: do you want to encrypt or decrypt, with an E square "
            "and a D square.",
        )
        + "<p>Pressing E does nothing yet. Nothing in the program changes "
        "<code>mode</code>, so it stays empty and the question stays up:</p>"
        + output("E pressed on pass 30, mode is '' after pass 60", label=VERIFIED),
    )

    # Section 3: answering it
    b += (
        '<h2><span class="num">3</span>Answer with a key'
        '<span class="mins">40 minutes</span></h2>'
        "<h3>Key presses are events</h3>"
        "<p>Pressing a key makes an event, the same way clicking the close button does, "
        "and it arrives in the same <code>for event</code> loop. A key event has two "
        "things to check:</p>"
        '<ul class="tight">'
        "<li><code>event.type</code> is <code>pygame.KEYDOWN</code>, which means a key "
        "went down.</li>"
        "<li><code>event.key</code> says which key: <code>pygame.K_e</code> for E, "
        "<code>pygame.K_d</code> for D.</li>"
        "</ul>"
        "<p>The window only hears keys while it is the active window. If pressing a key "
        "does nothing, click the window once, then press the key.</p>"
    )
    b += "<h3>Step 2: answer the question</h3>"
    b += (
        "<p>In the <code>for event</code> loop, under <code>running = 0</code>, add these "
        "lines. The two <code>if</code> lines start eight spaces in, the same as "
        "<code>if event.type == pygame.QUIT:</code>. Before you press each button, say "
        "what you think that part does.</p>"
    )
    b += labelled_code(ANSWERS, ANSWER_PARTS, "two_way_console.py, step 2, under running = 0")
    b += reveal(
        "Compare the E block with the D block. Apart from the word in <code>mode</code>, "
        "what is the only difference?",
        "<p>The E block uses <code>KEY</code>. The D block uses <code>-KEY</code>. "
        "Everything else is the same. Decrypting is encrypting with the opposite key, "
        "the idea from the opener.</p>",
    )
    b += reveal(
        "Why does each gate check <code>event.type</code> before "
        "<code>event.key</code>?",
        "<p>Only a key event has <code>event.key</code>. Moving the mouse makes an event "
        "too. With the two sides swapped, the first mouse movement stops the "
        "program:</p>"
        + output(
            "AttributeError: 'pygame.event.Event' object has no attribute 'key'",
            label=VERIFIED,
        )
        + "<p>With <code>event.type == pygame.KEYDOWN</code> first, a mouse event makes "
        "the left side False, and <code>and</code> never reads its right side. It is the "
        "same reason as the box gate in session 3.</p>",
    )
    b += (
        "<p>Run it and press E. You get the session 3 console. Close the window, run it "
        "again, and this time press D.</p>"
    )
    b += reveal(
        "<code>MESSAGE</code> is still <code>attack at dawn</code>. What appears at the "
        "bottom when you press D?",
        output(
            "D pressed: mode is 'decrypt', coded is 'xqqxzh xq axtk'\n"
            "the green row after D: xyzabcdefghijklmnopqrstuvw",
            label=VERIFIED,
        )
        + "<p>Nonsense. Decrypting moves every letter back 3, and "
        "<code>attack at dawn</code> was never moved forward 3 in the first place. "
        "Decrypt only makes sense on a coded message.</p>"
        "<p>Look at the green row too. With <code>-KEY</code>, it is the alphabet moved "
        "back 3: under <code>a</code> sits <code>x</code>.</p>",
    )

    b += "<h3>Step 3: decrypt a real message</h3>"
    b += (
        "<p>Three changes at the top of the file. First, replace the docstring on the "
        "first line with this one:</p>"
    )
    b += code(DOCSTRING_4, "two_way_console.py, step 3, line 1")
    b += "<p>Then change <code>MESSAGE</code> to the coded message from session 3:</p>"
    b += code('MESSAGE = "dwwdfn dw gdzq"', "two_way_console.py, step 3")
    b += (
        "<p>Then replace the three <code>print</code> lines with these three, which "
        "print the message both ways:</p>"
    )
    b += code(_prints_lines(), "two_way_console.py, step 3, in place of the three prints")
    b += reveal(
        "Run it. Before you press anything, what do the three lines in the terminal "
        "say?",
        output(prints4)
        + "<p>The third line is the answer the window is about to show you.</p>",
    )
    b += reveal(
        "Now press D. The first letter of the message is <code>d</code>. Which tile gets "
        "the orange box on the top row, and which letter is on the green tile under it?",
        "<p>The box goes around <code>d</code> on the top row, and the green tile under "
        "it shows <code>a</code>, because the green row is the alphabet moved back 3. "
        "Here it is a few letters later, with <code>atta</code> done and the box on "
        "<code>f</code>, which decrypts to <code>c</code>:</p>"
        + _shot(
            "two_way_console_140.png",
            "Decrypting: dwwdfn dw gdzq at the top, the alphabet on cream tiles, the "
            "alphabet moved back 3 on green tiles, f and c boxed in orange, and atta at "
            "the bottom.",
        )
        + "<p>And at the end:</p>"
        + _shot(
            "two_way_console_600.png",
            "Decrypted: dwwdfn dw gdzq at the top and attack at dawn at the bottom.",
        ),
    )
    b += (
        "<h3>Swap messages with a partner</h3>"
        '<ol class="tight">'
        f"<li>Pick a message of lowercase letters and spaces, {fits} characters or "
        "fewer, and a key from 1 to 25. Put them in <code>MESSAGE</code> and "
        "<code>KEY</code>.</li>"
        "<li>Run it. The terminal line that starts <code>encrypted with key</code> is your "
        "coded message. Press E to watch it being made.</li>"
        "<li>Write the coded message and your key on paper, and swap papers with your "
        "partner.</li>"
        "<li>Put your partner's coded message in <code>MESSAGE</code> and their key in "
        "<code>KEY</code>. Run it and press D.</li>"
        "</ol>"
        "<p>Pressing E or D again starts the letters over in that direction.</p>"
    )

    b += exits(
        "Your window asks the question, and pressing E shows the session 3 console. "
        "Point at the line that makes the question go away once you answer.",
        "Floor, plus you decrypted your partner's message with D. Say why "
        "<code>-KEY</code> undoes <code>KEY</code>.",
        "Middle, plus pressing the space bar brings the question back. Work it out "
        "below.",
    )
    b += laddered(
        "Make the space bar bring the question back, so you can choose again.",
        [
            "<p>Which variable decides whether the question shows? What value does it "
            "have before anyone answers?</p>",
            "<p>The space bar is a key like E and D. Its name is "
            "<code>pygame.K_SPACE</code>.</p>",
            "<p>Add a third gate in the <code>for event</code> loop that puts "
            "<code>mode</code> back to the empty string.</p>",
        ],
        code(
            _excerpt(STRETCH_FILE, "if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:",
                     'mode = ""'),
            f"{STRETCH_FILE}, under the D block",
        )
        + "<p>After the space bar, <code>mode</code> is empty again, so the question is "
        "painted over the console on every frame:</p>"
        + output("D on pass 10, space on pass 200: mode is '' after pass 300",
                 label=VERIFIED),
        "space",
    )

    key = "<p>Each file below runs as it is.</p>"
    for n in (1, 2, 3):
        key += code(_source(STEP_FILES[n]), f"two_way_console.py after step {n}")
    b += answer_key(
        key,
        "two-way",
        "The whole of <code>two_way_console.py</code> after each step. Open it to check "
        "a program that will not run, or one that does something different.",
    )

    b += panel(
        ["6.NS.C.5", "7.NS.A.1.b", "MP7"],
        "<p>10 opener, 30 the question screen (files, then step 1), 40 the answers (key "
        "events, steps 2 and 3, and the partner swap), 10 exits. Do the steps in the "
        "box headed <b>Now open the files</b> together on the projector, and check that "
        "every student's run shows the session 3 console before anyone types. If the "
        "room is behind, the partner swap is what slips: the middle exit can be met by "
        "decrypting <code>dwwdfn dw gdzq</code>.</p>",
        "<p>Key presses go to whichever window is active. Students who run from VS Code "
        "and press E straight away are typing into VS Code. Tell them to click the "
        "window first.</p>"
        "<p>Indentation is the usual failure in step 2. The two <code>if</code> lines "
        "sit inside the <code>for event</code> loop, eight spaces in; the lines under "
        "them are twelve. In step 1 the gate is four spaces in and its lines are "
        "eight.</p>"
        "<p>Decrypting <code>attack at dawn</code> gives <code>xqqxzh xq axtk</code>. "
        "That is planned. Let students be puzzled for a moment before the reveal.</p>"
        "<p>Someone will ask why the console is drawn at all if it is painted over. "
        "Drawing happens out of sight until the flip, so painting over it costs nothing "
        "the student can see, and it saves moving every drawing line under a gate.</p>",
        retouch=(
            "Session 3's console, unchanged except for what this page adds, and its "
            "<code>shift_by</code>. The negative key from session 3's third test line, "
            "now explained. The order of the two sides of <code>and</code>, from "
            "session 3's box gate, now needed for key events."
        ),
        extras=(
            "<h3>Files</h3><p><code>undo_tour.py</code> for the opener, run by the build "
            "so the page quotes its real output. <code>cipher_console.py</code> from "
            "session 3, which downloads as <code>two_way_console.py</code>, and "
            "<code>letters.py</code>. The answer-key files "
            "<code>two_way_step1.py</code>, <code>two_way_step2.py</code>, and "
            "<code>two_way_console.py</code>, and <code>two_way_space.py</code>, the "
            "stretch answer. <code>build/twoway_edits.py</code> holds the typed lines; "
            "the build checks that session 3's console plus each step's lines, as the page "
            "shows them, gives each answer-key file exactly, and that "
            "<code>shift_by</code> in every file is identical to the one in "
            "<code>caesar_encode.py</code>. <code>verify_two_way.py</code> runs each "
            "program without a screen, sends key presses on chosen passes through the "
            "loop, and takes the screenshots. Verified on Python 3.12.3 and pygame "
            "2.6.1.</p>"
            "<h3>Lifted this week</h3><p>Key events: <code>pygame.KEYDOWN</code>, "
            "<code>event.key</code>, and key names such as <code>pygame.K_e</code>. A "
            "variable that remembers a choice. <code>%</code> with a negative number, and "
            "opposite keys.</p>"
            "<h3>Assumed knowledge</h3><p>Session 3's console and "
            "<code>shift_by</code>. Nothing from session 3's stretch is needed: key "
            "events are taught here from the start.</p>"
        ),
    )
    b += pager(
        ("wed03_counting.html", "Session 3: a cipher in a window"),
        ("wed05_hashing.html", "Session 5: seals and real hashes"),
    )
    return b
