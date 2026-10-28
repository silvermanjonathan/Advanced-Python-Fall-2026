"""Sessions 3 to 7. Sessions 4 and 6 live in their own modules."""

import ast
import os

from build import answer_key, labelled_code, laddered, code, downloads, masthead, output, pager, reveal
from stds import panel
from console03 import _shot, console_section
from twoway04 import day04  # noqa: F401  (session 4 lives in its own module)
from rps06 import day06  # noqa: F401  (session 6 lives in its own module)


def exits(floor, middle, stretch):
    """Return the three differentiated exits."""
    return (
        '<div class="exits">'
        f'<div class="exit"><span class="lab">FLOOR</span><p>{floor}</p></div>'
        f'<div class="exit"><span class="lab">MIDDLE</span><p>{middle}</p></div>'
        f'<div class="exit"><span class="lab">STRETCH</span><p>{stretch}</p></div>'
        "</div>"
    )


_STRIP_TEMPLATE = (
    '<div class="strip" id="strip">'
    '<div class="strip-controls">'
    '<button type="button" id="strip-down" aria-label="Key down by 1">&minus;1</button>'
    '<span class="strip-key">Key <b id="strip-keyval">0</b></span>'
    '<button type="button" id="strip-up" aria-label="Key up by 1">+1</button>'
    '<button type="button" id="strip-reset" class="quiet">Key 0</button>'
    '<label class="strip-word">Try a word <input id="strip-input" type="text" '
    'maxlength="20" autocomplete="off" spellcheck="false"></label>'
    "</div>"
    '<div class="strip-rows" id="strip-rows"></div>'
    '<p class="strip-say" id="strip-say" aria-live="polite">Click a letter in the top '
    "row.</p>"
    "</div>"
    """<script>
(function(){
  var A = 'abcdefghijklmnopqrstuvwxyz';
  var key = 0, picked = [];
  var rows = document.getElementById('strip-rows');
  var say = document.getElementById('strip-say');
  var keyval = document.getElementById('strip-keyval');
  var input = document.getElementById('strip-input');
  function cell(text, cls){ var d = document.createElement('span'); d.className = cls; d.textContent = text; return d; }
  function draw(){
    rows.textContent = '';
    var top = document.createElement('div'); top.className = 'strip-row top';
    var bot = document.createElement('div'); bot.className = 'strip-row bottom';
    top.appendChild(cell('plain', 'strip-label'));
    bot.appendChild(cell('cipher', 'strip-label'));
    for (var i = 0; i < 26; i++) {
      var on = picked.indexOf(i) >= 0 ? ' on' : '';
      var t = cell(A[i], 'strip-cell' + on);
      t.setAttribute('role', 'button'); t.setAttribute('tabindex', '0');
      t.setAttribute('aria-label', A[i]);
      (function(n){
        t.addEventListener('click', function(){ pick([n]); input.value = ''; });
        t.addEventListener('keydown', function(e){ if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick([n]); input.value = ''; } });
      })(i);
      top.appendChild(t);
      bot.appendChild(cell(A[(i + key) % 26], 'strip-cell' + on));
    }
    rows.appendChild(top); rows.appendChild(bot);
    keyval.textContent = key;
  }
  function pick(list){
    picked = list; draw();
    if (list.length === 0) { say.textContent = 'Click a letter in the top row.'; return; }
    if (list.length === 1) {
      var n = list[0], out = (n + key) % 26;
      var wrap = n + key >= 26 ? ' It ran off the end at z and came back round to a.' : '';
      say.textContent = A[n] + ' moves ' + key + ' places and becomes ' + A[out] + '.' + wrap;
      return;
    }
    var word = '', enc = '';
    list.forEach(function(n){ word += A[n]; enc += A[(n + key) % 26]; });
    say.textContent = word + ' with key ' + key + ' becomes ' + enc + '.';
  }
  function setKey(k){
    key = ((k % 26) + 26) % 26;
    if (input.value) { fromInput(); } else { pick(picked.length === 1 ? picked : []); }
  }
  function fromInput(){
    var list = [];
    input.value.toLowerCase().split('').forEach(function(ch){ var n = A.indexOf(ch); if (n >= 0) list.push(n); });
    pick(list);
  }
  document.getElementById('strip-up').addEventListener('click', function(){ setKey(key + 1); });
  document.getElementById('strip-down').addEventListener('click', function(){ setKey(key - 1); });
  document.getElementById('strip-reset').addEventListener('click', function(){ setKey(0); });
  input.addEventListener('input', fromInput);
  draw();
})();
</script>
"""
)


def cipher_strip(prefix):
    """Return one copy of the alphabet strip, with its element ids prefixed."""
    return (
        _STRIP_TEMPLATE.replace('id="strip', f'id="{prefix}')
        .replace("getElementById('strip", f"getElementById('{prefix}")
    )


CIPHER_STRIP = (
    "<p>Here is the alphabet twice. The top row is the plaintext letter. The bottom "
    "row is the letter it becomes. Press <b>+1</b> to slide the bottom row one place "
    "to the left, which adds 1 to the key. Then click a letter in the top row to see "
    "what it becomes.</p>"
    + cipher_strip("strip")
)


def _shift_by_source():
    """Return shift_by from caesar_encode.py, checked equal to caesar_crack.py's."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def grab(name):
        text = open(os.path.join(root, name)).read()
        start = text.find("def shift_by")
        end = text.find("\n\n\n", start)
        return text[start:end].rstrip("\n")

    mine = grab("caesar_encode.py")
    assert mine == grab("caesar_crack.py"), "shift_by differs between the two files"
    return mine


def _hide_letters_source():
    """Return hide_letters.py from its def to its print line."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    text = open(os.path.join(root, "hide_letters.py")).read()
    return text[text.index("def hide_letters"):].rstrip("\n")


def _accumulator_parts():
    """Return the three loops from accumulators.py, split at the blank lines."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    text = open(os.path.join(root, "accumulators.py")).read()
    blocks = [blk.strip("\n") for blk in text.split("\n\n")]
    assert len(blocks) == 4, "accumulators.py should be a docstring and three loops"
    return blocks[1:]


SHIFT_BY_PARTS = [
    ("def shift_by", "The function. It is given the text and the key, here called "
     "<code>amount</code>.", ""),
    ('out = ""', "Part 1 of the accumulator: start with the empty string. This runs "
     "once.", "once"),
    ("for ch in text:", "The loop. <code>ch</code> is each character of "
     "<code>text</code> in turn, spaces included.", "frame"),
    ('if ch == " ":', "The gate. A space stays a space: add it to <code>out</code> "
     "unchanged.", "frame"),
    ("else:", "Any other character is a letter. These three lines are the four steps "
     "from the <code>z</code> walk-through: find its position, add the key and wrap, "
     "turn the position back into a letter, and add it to <code>out</code>.", "frame"),
    ("return out", "Part 3: after the loop, return the finished text. This runs once.",
     "after"),
]


def _trace_lines():
    """Return trace_shift_by.py's output lines, run here so the page quotes a real run.

    Also check that its shift_by is the one in caesar_encode.py.
    """
    import subprocess
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    text = open(os.path.join(root, "trace_shift_by.py")).read()
    start = text.index("def shift_by")
    assert text[start:text.index("\n\n\n", start)] == _shift_by_source(), \
        "shift_by in trace_shift_by.py differs from caesar_encode.py"
    run = subprocess.run(["python3", "trace_shift_by.py"], cwd=root,
                         capture_output=True, text=True, check=True)
    return run.stdout.strip().split("\n")


def day03():
    """Session 3: accumulators, a Caesar cipher, and the cipher console."""
    b = masthead(
        "03",
        "A cipher in a window",
        "Wednesday 30 September 2026",
        "First the accumulator pattern again, because today's code is full of it. Then "
        "you will learn what a Caesar cipher is, write one, and put it in a pygame "
        "window.",
    )
    parts = _accumulator_parts()
    console, console_stretch, console_key = console_section()
    b += (
        '<h2><span class="num">1</span>Opener: the accumulator pattern'
        '<span class="mins">15 minutes</span></h2>'
    )
    b += (
        "<p>In session 1, <code>t = t + r</code> in <code>sweep_report.py</code> added "
        "each reading to a running total. In session 2, <code>hits = hits + 1</code> in "
        "<code>count_over</code> added 1 each time the gate said yes. A variable that is "
        "updated like this on every pass of a loop is called an <b>accumulator</b>. "
        "Sections 2 and 3 today each have one, so here is the pattern again.</p>"
        "<p>An accumulator has three parts:</p>"
        '<ol class="tight">'
        "<li><b>Before the loop</b>, the variable gets its starting value.</li>"
        "<li><b>Inside the loop</b>, the variable is updated. The new value is worked "
        "out from the old value: <code>total = total + s</code> reads "
        "<code>total</code>, adds <code>s</code>, and stores the result back in "
        "<code>total</code>.</li>"
        "<li><b>After the loop</b>, the program uses the final value. It prints it or "
        "returns it.</li>"
        "</ol>"
    )
    b += code(parts[0], "accumulators.py, part 1")
    b += (
        "<p><code>total = 0</code> is part 1. <code>total = total + s</code> is part 2. "
        "<code>print(f\"total {total}\")</code> is part 3.</p>"
    )
    b += reveal(
        "Trace it. What is <code>total</code> after the first pass, after the second "
        "pass, and after the third pass? What prints?",
        "<p>After the first pass, <code>total</code> is 0 + 4 = 4. After the second "
        "pass, it is 4 + 7 = 11. After the third pass, it is 11 + 2 = 13.</p>"
        + output("total 13"),
    )

    b += "<h3>An accumulator can hold a string</h3>"
    b += (
        "<p><code>+</code> between two strings joins them into one string: "
        "<code>\"ab\" + \"c\"</code> is <code>\"abc\"</code>.</p>"
        "<p><code>\"\"</code> is the <b>empty string</b>, a string with no characters "
        "in it. It is the starting value for a string accumulator, the same way 0 is "
        "the starting value for a running total.</p>"
    )
    b += code(parts[1], "accumulators.py, part 2")
    b += reveal(
        "What prints?",
        output("out ccaabb")
        + "<p>Each pass joins the letter on twice. After <code>c</code>, "
        "<code>out</code> is <code>cc</code>. After <code>a</code>, it is "
        "<code>ccaa</code>. After <code>b</code>, it is <code>ccaabb</code>.</p>",
    )
    b += code(parts[2], "accumulators.py, part 3")
    b += reveal(
        "This loop has <code>ch + backwards</code> where part 2 had "
        "<code>out + ch</code>, so each new letter goes on the front. What prints?",
        output("backwards bac")
        + "<p>After <code>c</code>, <code>backwards</code> is <code>c</code>. After "
        "<code>a</code>, it is <code>ac</code>. After <code>b</code>, it is "
        "<code>bac</code>. With <code>+</code> on strings the order matters: the "
        "string on the left comes first.</p>",
    )
    b += (
        "<p>In section 2 you will build a coded message this way, one letter at a "
        "time, starting from <code>out = \"\"</code>.</p>"
    )

    b += "<h3>Now write one</h3>"
    b += (
        "<p>Last week you wrote a module of functions that return values. On paper: "
        "write a function <code>hide_letters(text)</code> that returns <code>text</code> "
        "with every letter changed to <code>*</code> and every space kept. "
        "<code>hide_letters(\"meet at dawn\")</code> should return "
        "<code>\"**** ** ****\"</code>.</p>"
        "<p>It is a string accumulator, like part 2 above, with a gate inside the loop: "
        "if the character is a space, add a space; otherwise, add a star.</p>"
    )
    b += reveal(
        "Write yours first.",
        code(_hide_letters_source(), "hide_letters.py")
        + output("**** ** ****")
        + "<p><code>out = \"\"</code> is part 1. The two <code>out = out + ...</code> "
        "lines are part 2. On each pass exactly one of them runs, so one character is "
        "added: a space if <code>ch</code> is a space, and a star if it is not. "
        "<code>return out</code> is part 3.</p>"
        "<p>Keep this shape in mind. In section 2 you will write <code>shift_by</code>, "
        "and it has the same shape. The difference is what it adds in place of the star: "
        "the coded letter.</p>",
    )

    b += (
        '<h2><span class="num">2</span>What a Caesar cipher is'
        '<span class="mins">40 minutes</span></h2>'
    )
    b += (
        "<p>A Caesar cipher is a way to scramble a message. Pick a number, move every letter forward in the alphabet by that "
        "number, and wrap around from z back to a.</p>"
        "<p>Three words come with it, and session 4 uses them again. The number "
        "is the <b>key</b>. The readable message is the <b>plaintext</b>. The scrambled "
        "message is the <b>ciphertext</b>.</p>"
        "<p>Do one by hand before any code. Key 3, plaintext <code>dawn</code>. Write "
        "the alphabet along the top of your page if it helps.</p>"
    )
    b += CIPHER_STRIP
    b += reveal(
        "Encode <code>dawn</code> with key 3. Then encode <code>zebra</code> with the same key. Watch what happens to the z.",
        "<p><code>dawn</code> becomes <code>gdzq</code>. d goes to g, a goes to d, w "
        "goes to z, n goes to q.</p>"
        "<p><code>zebra</code> becomes <code>cheud</code>. Three past z runs off the end of the alphabet and comes back round to c. "
        "Without that wrap, x, y, and z would have no letter to become.</p>"
        "<p>To decode, move backwards by the same key. A Caesar cipher undoes itself "
        "with a negative key, which is why one function can do both jobs.</p>",
    )
    b += "<h3>Letters into numbers</h3>"
    b += (
        "<p>Python will not add 3 to a letter. Two functions change a letter into a number and back. "
        "<code>ord</code> turns a character into the number the machine stores it as, "
        "and <code>chr</code> turns a number back into a character.</p>"
    )
    b += code(
        """print(ord("a"))   # 97
print(ord("d"))   # 100
print(ord("z"))   # 122
print(chr(103))   # g"""
    )
    b += (
        "<p>The numbers themselves do not matter. What matters is that they run in "
        "order, so <code>ord(ch) - ord(\"a\")</code> gives you a position from 0 to 25. "
        "Add the key to the position, wrap it with <code>% 26</code>, then add "
        "<code>ord(\"a\")</code> back on to return to a letter.</p>"
    )
    b += laddered(
        "Walk <code>z</code> with key 3 through all four steps and write the number at "
        "each one.",
        [
            "<p>Start with <code>ord(\"z\")</code>. The code block above prints it. "
            "Then take away <code>ord(\"a\")</code>, which is 97. That gives the "
            "position of z in the alphabet, counting a as 0.</p>",
            "<p>Add the key to the position. The alphabet has positions 0 to 25, so any "
            "answer bigger than 25 has run off the end. <code>% 26</code> keeps the "
            "remainder after dividing by 26, which brings it back to the start.</p>",
            "<p>The third step is <code>(25 + 3) % 26</code>. 28 divided by 26 is 1, with "
            "2 left over. For the last step, add 97 back on and use <code>chr</code>: "
            "<code>chr(2 + 97)</code> is <code>chr(99)</code>. If a is 97, which letter "
            "is 99?</p>",
        ],
        "<pre><code>ord(\"z\")            122\n"
        "122 - ord(\"a\")       25     the position of z\n"
        "(25 + 3) % 26         2     wraps past the end\n"
        "chr(2 + ord(\"a\"))   'c'    back to a letter</code></pre>"
        "<p>This is the <code>%</code> wrap from session 1. There it kept a number under 9. Here it keeps a letter inside the alphabet.</p>",
        "z-steps",
    )
    b += "<h3>Write it as a function</h3>"
    b += (
        "<p>You just did four steps by hand for one letter. Now put them in a function "
        "called <code>shift_by(text, amount)</code> that does the four steps for every "
        "letter in <code>text</code> and returns the new message. Leave spaces as "
        "spaces. Then add these three lines under it and run the file.</p>"
    )
    b += code(
        '''print(shift_by("dawn", 3))
print(shift_by("zebra", 3))
print(shift_by("gdzq", -3))''',
        "caesar_encode.py, under your function",
    )
    b += laddered(
        "Before you run it: what should each of the three lines print? You worked out "
        "the first two by hand at the start of this section.",
        [
            "<p>Start with an empty string, <code>out = \"\"</code>. Loop over every "
            "character in <code>text</code> with <code>for ch in text:</code>. After the "
            "loop, <code>return out</code>.</p>",
            "<p>Inside the loop, one gate. If <code>ch</code> is a space, add a space to "
            "<code>out</code>. Otherwise, do the four steps from the <code>z</code> "
            "walk-through with <code>ch</code> and <code>amount</code>, and add the new "
            "letter to <code>out</code>.</p>",
            code('''def shift_by(text, amount):
    out = ""
    for ch in text:
        if ch == " ":
            out = out + " "
        else:
            spot = ord(ch) - ord("a")
            spot = (spot + amount) % 26
            out = out + ____
    return out'''),
        ],
        code(_shift_by_source(), "caesar_encode.py")
        + output("gdzq\ncheud\ndawn")
        + "<p>The first two match the hand answers. The third decodes: a key of -3 moves "
        "every letter back by 3, so <code>g</code> goes back to <code>d</code> and "
        "<code>d</code> goes back to <code>a</code>. A letter near the start of the "
        "alphabet, like <code>b</code>, would go back past <code>a</code>, and "
        "<code>% 26</code> wraps it round to <code>y</code>. One function does both "
        "jobs.</p>",
        "shift-by",
    )

    b += "<h3>Trace shift_by, one pass at a time</h3>"
    b += (
        "<p>Before you put <code>shift_by</code> in a window, follow one call through "
        "it, line by line. Here it is split into parts, with a button under each part. "
        "Before you press a button, say what you think that part does.</p>"
    )
    b += labelled_code(_shift_by_source(), SHIFT_BY_PARTS, "caesar_encode.py")
    trace = _trace_lines()
    b += reveal(
        "Call <code>shift_by(\"hi zoe\", 3)</code>. How many times does the loop run? "
        "How many of those times does the gate say yes?",
        "<p>The loop runs 6 times, once for each character of <code>\"hi zoe\"</code>. "
        "The space counts as a character.</p>"
        "<p>The gate says yes once, on pass 3, for the space. On the other 5 passes it "
        "says no, and the three letter lines run.</p>",
    )
    b += reveal(
        "Pass 1: <code>ch</code> is <code>\"h\"</code>. Work out <code>spot</code> after "
        "each of the two <code>spot</code> lines, the letter that is added, and "
        "<code>out</code> at the end of the pass.",
        "<p><code>ord(\"h\")</code> is 104, and 104 - 97 = 7, so <code>spot</code> is 7: "
        "h is at position 7, counting a as 0.</p>"
        "<p><code>(7 + 3) % 26</code> is 10, so <code>spot</code> becomes 10.</p>"
        "<p><code>chr(10 + 97)</code> is <code>chr(107)</code>, which is "
        "<code>\"k\"</code>. <code>out</code> was <code>\"\"</code>, so now it is "
        "<code>\"k\"</code>.</p>"
        + output(trace[0], label="verified output, trace_shift_by.py"),
    )
    b += reveal(
        "Pass 3: <code>ch</code> is a space. Which line runs, and what is "
        "<code>out</code> at the end of the pass?",
        "<p>The gate says yes, so <code>out = out + \" \"</code> runs and the three letter "
        "lines are skipped. <code>out</code> was <code>\"kl\"</code> after passes 1 and 2, "
        "so now it is <code>\"kl \"</code>, with a space on the end.</p>"
        + output(trace[2], label="verified output, trace_shift_by.py"),
    )
    b += reveal(
        "Pass 4: <code>ch</code> is <code>\"z\"</code>. Which letter is added?",
        "<p>The same four steps as the <code>z</code> walk-through above: position 25, "
        "then <code>(25 + 3) % 26</code> is 2, and position 2 is <code>\"c\"</code>. "
        "<code>out</code> is now <code>\"kl c\"</code>.</p>"
        + output(trace[3], label="verified output, trace_shift_by.py"),
    )
    b += reveal(
        "Finish the last two passes. What does <code>shift_by(\"hi zoe\", 3)</code> "
        "return?",
        "<p>Pass 5 adds <code>r</code> for <code>o</code>, and pass 6 adds <code>h</code> "
        "for <code>e</code>. After the loop, the function returns "
        "<code>\"kl crh\"</code>.</p>"
        "<p>Here is every pass, then what the real <code>shift_by</code> returns:</p>"
        + output("\n".join(trace), label="verified output, trace_shift_by.py"),
    )

    b += console
    b += exits(
        "You encoded <code>dawn</code> and <code>zebra</code> by hand with key 3, you "
        "can say what plaintext, ciphertext, and key mean, and your window from step 1 "
        "of the console opens and closes. You can point to the line that keeps it open "
        "and the line that lets it close.",
        "Floor, plus <code>shift_by</code> written and encoding correctly including the "
        "wrap past z, plus all four console steps typed and running, with your own "
        "<code>MESSAGE</code> and <code>KEY</code> and the coded letters appearing twice "
        "as fast. Say which number you changed and why.",
        "Middle, plus pressing R starts the coded message again from nothing. Work it "
        "out below.",
    )
    b += console_stretch
    b += (
        "<p><b>Extra.</b> You can also break a Caesar cipher without the key, by "
        "counting its letters. The Extras page teaches <code>Counter</code>, a "
        "dictionary made for counting, and uses it to do that. It is for any time after "
        "today.</p>"
        '<div class="toolbar"><a class="btn quiet" href="extra_crack_caesar.html">Break '
        "a Caesar cipher by counting letters</a></div>"
    )
    b += answer_key(
        console_key,
        "console",
        "For section 3: the whole of <code>cipher_console.py</code> after each step. "
        "Open it to check a program that will not run, or one that does something "
        "different.",
    )
    b += panel(
        ["6.RP.A.3", "MP7"],
        "<p>15 opener with the accumulator review, 40 the cipher by hand, "
        "<code>shift_by</code> written, and the trace of one call, 30 the cipher "
        "console, 5 exits. The console's 30 minutes include two five-minute lessons just "
        "before step 3. One is on dictionaries, because <code>SHAPES</code> is one: "
        "making a dictionary, looking up a key, a list as a value, "
        "<code>KeyError</code>, and <code>.get</code> with a value to return when the "
        "key is missing. The other is on a loop inside a loop, because "
        "<code>draw_letter</code> uses one to go over a letter's grid. If time runs "
        "short, step 4 is what slips: the floor exit needs only step 1. "
        "Building a dictionary up one key at a time, and <code>Counter</code>, are on "
        "the Extras page, with breaking the cipher, because that is where they are "
        "used. Assume no student has seen a cipher or a pygame "
        "window before. Do not cut section 2 to make room for the console. A console for a cipher the "
        "students did not build teaches nothing about the cipher.</p>"
        "<p>Students do not open the starter until section 3: it holds a finished "
        "<code>shift_by</code>, the answer to section 2. At the start of section 3, do "
        "the steps in the box headed <b>Now open the files</b> together on the projector, and check that every "
        "student's run prints the three lines before anyone types. "
        "Students download two files, the starter and <code>letters.py</code>, and "
        "type the pygame code into the starter one step at a time. The starter already "
        "holds the lines that teach nothing new: the message, most of the colors, "
        "<code>shift_by</code>, and the prints. Step 1 has students type "
        "<code>import pygame</code> and <code>BOARD</code> as well as the window code, "
        "in the three places the starter marks, so every line the window needs is on "
        "the page. If the room is behind, type step 1 "
        "together on the projector, line by line, and let students do steps 2 to 4 on "
        "their own. The answer key at the bottom of the page has the whole file after "
        "each step, behind one button, for a student whose program will not run.</p>",
        "<p>The hand encode is the part to insist on. Students who go straight to "
        "<code>ord</code> without doing <code>dawn</code> on paper will not spot the "
        "wrap, and the wrap is the only hard part of the cipher.</p>"
        "<p>Expect <code>ord</code> and <code>chr</code> to feel arbitrary. The fix is "
        "to say the actual numbers do not matter, only that they run in order. Nobody "
        "needs to memorize 97.</p>"
        "<p><code>KeyError</code> is new this week. It turns up in step 3 of the "
        "console, when a capital letter has no entry in <code>SHAPES</code>. Students "
        "read it as a crash rather than as information. Point at the last line: it names "
        "the key that was missing.</p>"
        "<p>In the window, y points down. Students who have graphed points in math "
        "will expect <code>y = 130</code> near the bottom. Point at the diagram in step "
        "2 before they run it.</p>"
        "<p><code>and</code> skips its right side when the left side is False, and the "
        "console needs that twice: in step 4, where <code>MESSAGE[shown]</code> would "
        "raise <code>IndexError</code> without it, and in the stretch, where "
        "<code>event.key</code> raises <code>AttributeError</code> on the first mouse "
        "movement if it is checked first. Students who get the stretch working by luck "
        "of ordering should be asked to swap the two sides and run it.</p>",
        retouch=(
            "The <code>%</code> wrap traced by hand in session 1, now on a 26 hour clock. "
            "The returning functions from session 2: <code>shift_by</code> returns the "
            "coded text, so the console calls it on the alphabet as well as on the "
            "message. The accumulators from sessions 1 and 2, reviewed in the opener and "
            "used again in the console as <code>frame</code> and <code>shown</code>."
        ),
        extras=(
            "<h3>Files</h3><p><code>accumulators.py</code> for the opener, shown in "
            "three parts, and <code>hide_letters.py</code>, the answer to its last task. <code>caesar_encode.py</code> for section 2, the answer to the "
            "<code>shift_by</code> step, and <code>trace_shift_by.py</code>, which prints the "
            "trace of <code>shift_by(\"hi zoe\", 3)</code> one pass at a time; the build "
            "runs it and checks its <code>shift_by</code> is the same as the one in "
            "<code>caesar_encode.py</code>. For section 3: <code>dict_tour.py</code>, the "
            "dictionary lesson before step 3, which students type in three pieces and "
            "which shows a <code>KeyError</code> on purpose, then replaces that line with "
            "<code>.get</code>; the file holds the final version, and the output check "
            "runs the <code>KeyError</code> version too. The build checks its "
            "<code>pictures</code> entries match <code>letters.py</code>. "
            "<code>grid_tour.py</code>, the loop-inside-a-loop lesson, typed in two "
            "pieces. "
            "<code>letters.py</code> (a "
            "module, never prints) and <code>cipher_console_starter.py</code>, which "
            "downloads as <code>cipher_console.py</code>; then the answer-key files "
            "<code>cipher_console_step1.py</code> to <code>cipher_console_step3.py</code> "
            "and <code>cipher_console.py</code>, and <code>cipher_console_replay.py</code>, "
            "the stretch answer. The build checks that the starter plus each step's typed "
            "lines, as the page shows them, gives the next answer-key file exactly, and "
            "that <code>shift_by</code> in the console files is identical to the one in "
            "<code>caesar_encode.py</code>. "
            "<code>verify_console.py</code> runs every console program without a screen "
            "for a fixed number of frames, then sends the close event. Every output on "
            "this page and every screenshot came from a run, on Python 3.12.3 and pygame "
            "2.6.1. Confirm pygame is installed on the classroom machines before this "
            "session.</p>"
            "<h3>Lifted this week</h3><p>The word accumulator, the empty string, "
            "<code>+</code> to join strings, "
            "<code>ord</code> and <code>chr</code>, "
            "indexing a string, dictionaries (curly brackets, looking up a key, a list as "
            "a value), <code>KeyError</code>, <code>.get</code> with a default, a loop inside a loop (outer and inner "
            "loop), tuples, and a pygame window: the event loop, frames, "
            "<code>pygame.draw.rect</code>.</p>"
            "<h3>Assumed knowledge</h3><p>None beyond the hub prerequisites plus the "
            "<code>%</code> wrap from session 1. Section 2 teaches what a cipher is, "
            "including the words plaintext, ciphertext, and key, and assumes students "
            "have never used one. Section 3 assumes no pygame.</p>"
        ),
    )
    b += pager(
        ("wed02_return_and_modules.html", "Session 2: functions that return a value"),
        ("wed04_two_way.html", "Session 4: encrypt or decrypt"),
    )
    return b


def _root_file(name):
    """Return the text of a program in the repo root."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return open(os.path.join(root, name)).read()


def _pets_part(start, end):
    """Return the lines of pets.py from the one beginning start, up to end."""
    text = _root_file("pets.py")
    i = text.index(start)
    return text[i:text.index(end, i)].rstrip("\n")


def _pet_snippets():
    """Return the SNIPPETS dictionary from verify_pets.py, the code that was run."""
    tree = ast.parse(_root_file("verify_pets.py"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "SNIPPETS":
            return ast.literal_eval(node.value)
    raise ValueError("verify_pets.py has no SNIPPETS")


def _forest_part(start, end=None):
    """Return the lines of forest.py from the one beginning start, up to end."""
    text = _root_file("forest.py")
    i = text.index(start)
    if end is None:
        return text[i:].rstrip("\n")
    return text[i:text.index(end, i)].rstrip("\n")


def _forest_snippets():
    """Return the SNIPPETS dictionary from verify_forest.py, the code that was run."""
    tree = ast.parse(_root_file("verify_forest.py"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "SNIPPETS":
            return ast.literal_eval(node.value)
    raise ValueError("verify_forest.py has no SNIPPETS")


def _forest_section():
    """Return session 5's section 4: a Tree class, seven trees in a list, one window."""
    f = _forest_snippets()
    b = '<h2><span class="num">4</span>A forest of trees<span class="mins">20 minutes</span></h2>'
    b += (
        "<p>A pet keeps numbers and reports them in the terminal. A tree can keep "
        "numbers too, and draw itself in a pygame window from those numbers. The "
        "program in this section makes seven trees from one <code>Tree</code> class, "
        "keeps them in one list, and draws every tree in the list.</p>"
        '<div class="now"><p><b>Do this now.</b> Download <code>forest.py</code> with the '
        "button below, but do not run it yet. Read it one piece at a time and answer "
        "each question before you open its answer. You run it at tree piece 4.</p></div>"
    )
    b += downloads("forest.py")

    b += "<h3>Tree piece 1: setting up a new tree</h3>"
    b += code(_forest_part("class Tree:", "    def grow(self, amount):"))
    b += (
        "<p><code>x</code> is how many pixels from the left edge of the window the tree "
        "stands. <code>height</code> is how tall its trunk is, in pixels.</p>"
    )
    b += reveal(
        "<code>Tree(80, 40)</code> makes one tree. What are its three attributes, and "
        "what value does each one hold?",
        "<p><code>x</code> is 80 and <code>height</code> is 40. The two values in the "
        "brackets go into the parameters in order: 80 into <code>x</code>, 40 into "
        "<code>height</code>. <code>__init__</code> stores each one on the tree with "
        "<code>self.</code> in front.</p>"
        "<p><code>leaf_size</code> is 0. No value in the brackets sets it. "
        "<code>__init__</code> sets it to 0 for every new tree, the way it set "
        "<code>hunger</code> to 5 for every new pet.</p>"
        "<p>Piece 3 in section 1 said that to let pets start with different hunger, you "
        "would add a parameter to <code>__init__</code>. <code>Tree</code> does that with "
        "<code>height</code>, so each tree can start at its own height.</p>",
    )

    b += "<h3>Tree piece 2: things a tree can do</h3>"
    b += code(_forest_part("    def grow(self, amount):", "    def draw(self, screen):"))
    b += reveal(
        "<code>grow</code> has two parameters, <code>self</code> and "
        "<code>amount</code>. The call <code>tree.grow(20)</code> has one value in its "
        "brackets. Where does the value of each parameter come from?",
        "<p>The first parameter, <code>self</code>, gets its value from the dot. The "
        "tree before the dot becomes <code>self</code>, the same as in "
        "<code>rocky.feed()</code>.</p>"
        "<p>The second parameter, <code>amount</code>, gets its value from the brackets: "
        "20. So <code>tree.grow(20)</code> adds 20 to that tree's height and to no "
        "other tree's.</p>"
        "<p><code>add_leaves</code> has only <code>self</code>, so it is called with "
        "empty brackets: <code>tree.add_leaves()</code>. It sets "
        "<code>leaf_size</code> to 30.</p>",
    )

    b += "<h3>Tree piece 3: a tree draws itself</h3>"
    b += code(_forest_part("    def draw(self, screen):", "\n\n# make seven trees"))
    b += (
        "<p><code>draw</code> puts the tree in the window. Its parameter "
        "<code>screen</code> is the window to draw on. <code>GROUND</code>, "
        "<code>BARK</code>, and <code>LEAVES</code> are set at the top of "
        "<code>forest.py</code>: <code>BARK</code> and <code>LEAVES</code> are the two "
        "colours, and <code>GROUND</code> is 340, the y where the grass starts. In a pygame window y counts down from the top, as in "
        "session 3's cipher console, so y = 340 is 340 pixels below the top edge. The "
        "window is 640 wide and 400 tall.</p>"
        "<p><code>pygame.draw.rect</code> is the one from session 3: the window, a "
        "colour, then the rectangle's left edge, top edge, width, and height. "
        "<code>pygame.draw.circle</code> is new. It takes the window, a colour, the "
        "centre of the circle as an (x, y) pair, and the <b>radius</b>: the distance "
        "from the centre to the edge, in pixels.</p>"
    )
    b += reveal(
        "A tree has height 100. What is <code>top</code> for that tree? Then: why does "
        "the code take the height away from <code>GROUND</code> instead of adding it?",
        "<p>The first part: <code>top</code> is 340 take away 100, which is 240.</p>"
        "<p>The second part: y counts down from the top of the window, so a point higher "
        "up has a smaller y. The trunk goes up from the grass, so its top edge needs a y "
        "smaller than 340. Adding would give 440, which is below the bottom of the "
        "400 pixel window.</p>"
        "<p>The rectangle starts at <code>top</code> and is <code>self.height</code> "
        "pixels tall, so its bottom edge is at 340, on the grass. Its left edge is at "
        "<code>self.x - 5</code> and it is 10 wide, so the trunk is centred on "
        "<code>x</code>.</p>"
        "<p>The circle's centre is the top of the trunk, so the leaves sit on the trunk. "
        "It is drawn after the trunk, so it covers the top of the trunk. The "
        "<code>if</code> gate means a tree with <code>leaf_size</code> 0 gets no "
        "circle.</p>",
    )

    b += "<h3>Tree piece 4: a forest in a window</h3>"
    b += (
        "<p>This is the bottom of <code>forest.py</code>. <code>forest</code> starts as "
        "an empty list. The <code>for</code> loop makes seven trees and adds each one to "
        "the list with <code>append</code>. The window loop is the one from session 4, "
        "with two keys: G and L. Each key runs a <code>for</code> loop over the list, so "
        "one key press changes every tree.</p>"
    )
    b += code(_forest_part("# make seven trees"))
    b += reveal(
        "Work out two things before you run it. First: what are the seven starting "
        "heights, from left to right? Second: you press G three times, then L. How tall "
        "is the tallest tree then, and what y is the top of its trunk? Now run "
        "<code>forest.py</code>, look, then press G three times and L.",
        "<p>The first part: <code>i</code> goes from 0 to 6, and each height is "
        "<code>40 + i * 20</code>.</p>"
        + output("heights [40, 60, 80, 100, 120, 140, 160]", "verified from a headless run")
        + _shot("forest_5.png", "Seven brown trunks on green grass under a pale blue sky. "
                "The trunks get taller from left to right.")
        + "<p>The second part: each G adds 20 to every tree, so three presses add 60. "
        "The tallest tree goes from 160 to 220, and the top of its trunk is at 340 take "
        "away 220, which is 120. L sets every tree's <code>leaf_size</code> to 30.</p>"
        + output(
            """heights [100, 120, 140, 160, 180, 200, 220]
leaf sizes [30, 30, 30, 30, 30, 30, 30]
tallest tree: x 560, height 220, top of trunk at y 120""",
            "verified from a headless run",
        )
        + _shot("forest_60.png", "The same seven trees, each 60 pixels taller, each with "
                "a round dark green clump of leaves on top.")
        + "<p>Every tree grew by the same amount and kept its own height, so the trees "
        "still go up in steps of 20. Each frame, the loop fills the sky, draws the grass, "
        "then calls <code>draw</code> on each tree in the list. A tree is drawn again "
        "every frame from its own attributes, so a change to its height shows on the "
        "next frame.</p>",
    )
    b += reveal(
        "You want an eighth tree. What is the smallest change to <code>forest.py</code> "
        "that makes eight trees? Where would the eighth tree stand?",
        "<p>Change <code>range(7)</code> to <code>range(8)</code>. The eighth tree has "
        "<code>i</code> = 7, so its x is 80 add 7 times 80, which is 640.</p>"
        + output(
            "x positions [80, 160, 240, 320, 400, 480, 560, 640], window width 640",
            "verified from a headless run",
        )
        + "<p>The window is 640 wide, so the eighth tree stands on the right edge, and "
        "the right half of its trunk and leaves is cut off. To fit eight trees, make the "
        "gap between them smaller or the window wider.</p>",
    )

    b += "<h3>Forest round 1</h3>"
    b += (
        "<p>Each forest round goes under the <code>Tree</code> class in "
        "<code>forest.py</code>, in place of everything from "
        "<code># make seven trees</code> down. It prints, and opens no window. Write your "
        "prediction on paper before you open the answer.</p>"
    )
    b += code(f["round1"])
    b += reveal(
        "What three lines are printed? Which tree is tallest?",
        output(
            """100 170
300 90
500 90"""
        )
        + "<p>The tree at x 100 is tallest. The first loop grows every tree by 50: "
        "40 to 90. Then <code>forest[0].grow(80)</code> grows only the tree at index 0, "
        "the first tree in the list: 90 to 170.</p>"
        "<p><code>forest[0]</code> is one tree from the list, so the dot sends that tree "
        "in as <code>self</code>, and no other tree changes. Each tree keeps its own "
        "height, the way Rocky and Luna each kept their own hunger.</p>",
    )
    b += "<h3>Forest round 2</h3>"
    b += code(f["round2"])
    b += reveal(
        "How many trees does this code make? What is printed?",
        output("190")
        + "<p>One tree. Only <code>Tree(...)</code> makes a tree, and it appears once. "
        "The list holds that one tree three times, so the loop grows the same tree "
        "three times: 40, 90, 140, 190.</p>"
        "<p>This is round 3 from section 2 again. There, <code>b = a</code> gave one pet "
        "a second name. Here, one tree is in the list three times. To count the trees, "
        "count the calls to <code>Tree(...)</code>.</p>",
    )
    return b


def _broken(n, s, error, mistake, fix):
    """Return one broken pet: the code, then the error and the fix behind a button."""
    return (
        f"<h3>Broken pet {n}</h3>"
        + code(s[f"broken{n}"])
        + reveal(
            "What does the last line of the error say? What is the mistake, and what is "
            "the fix?",
            # an error line can be longer than the code column, so it wraps
            output(error, "last line of the error").replace("<pre>", '<pre class="wrap">', 1)
            + f"<p><b>The mistake.</b> {mistake}</p><p><b>The fix.</b> {fix}</p>",
        )
    )


def day05():
    """Session 5: classes, objects, and virtual pets."""
    s = _pet_snippets()
    b = masthead(
        "05",
        "Making your own objects",
        "Wednesday 28 October 2026",
        "Strings, lists, and dictionaries are objects that someone else designed. Today "
        "you write a class, the code that describes a new kind of object, and make "
        "virtual pets from it. Each pet keeps its own hunger and its own happiness. Then "
        "a Tree class draws a whole forest in a pygame window.",
    )

    b += '<h2><span class="num">1</span>Build a pet, one piece at a time<span class="mins">30 minutes</span></h2>'
    b += (
        '<div class="now"><p><b>Do this now.</b> Make a new file called '
        "<code>pets.py</code>. Type each piece as you reach it and run the file after "
        "each one. Answer each question before you open its answer.</p></div>"
    )
    b += "<h3>Piece 1: an empty class</h3>"
    b += code(s["empty"])
    b += (
        "<p><code>class Pet:</code> starts a class called <code>Pet</code>. A class is "
        "code that describes a new kind of object: what each one stores and what each "
        "one can do. Class names "
        "start with a capital letter, so you can tell a class from a variable. "
        "<code>pass</code> means nothing here yet. Python needs at least one line inside "
        "a class, and <code>pass</code> is a line that does nothing.</p>"
    )
    b += reveal(
        "You run this file. What appears in the terminal?",
        "<p>Nothing. The file describes what a pet is, but no line makes a pet, and no "
        "line prints. Writing a class does not make an object.</p>",
    )

    b += "<h3>Piece 2: setting up a new pet</h3>"
    b += code(s["first"])
    b += reveal(
        "What does it print? Then say what the difference is between <code>Pet</code> "
        "and <code>rocky</code>.",
        output("Rocky")
        + "<p><code>Pet</code> is the class. <code>rocky</code> is one pet made from it. "
        "A thing made from a class is called an <b>object</b> or an <b>instance</b> of "
        "that class. The two words mean the same thing.</p>"
        "<p><code>Pet(\"Rocky\")</code>, with brackets, makes a new pet. Python makes "
        "an empty object, then straight away runs <code>__init__</code> on it, with "
        "<code>self</code> set to the new object and <code>name</code> set to "
        "<code>\"Rocky\"</code>. <code>__init__</code> is short for initialise, which "
        "means set up. It has two underscores on each side.</p>"
        "<p><code>self.name = name</code> stores the name on this pet. "
        "<code>name</code> is a parameter, and like every parameter it is gone when "
        "<code>__init__</code> finishes. <code>self.name</code> belongs to the pet and "
        "stays. <code>rocky.name</code> reads it back: rocky's name.</p>",
    )

    b += "<h3>Piece 3: numbers every pet starts with</h3>"
    b += code(s["stats"])
    b += reveal(
        "<code>Pet(\"Rocky\")</code> only passes a name. What does it print, and where "
        "do the other two numbers come from?",
        output("Rocky 5 5")
        + "<p>Every new pet starts with hunger 5 and happiness 5, because "
        "<code>__init__</code> sets them to 5 for every pet it sets up. A value stored "
        "on an object like this is called an <b>attribute</b>. A pet has three: "
        "<code>name</code>, <code>hunger</code>, and <code>happiness</code>. Only the "
        "name comes from the line that makes the pet. To let pets start with different "
        "hunger, you would add a <code>hunger</code> parameter to <code>__init__</code> "
        "and pass a number in.</p>",
    )

    b += "<h3>Piece 4: things a pet can do</h3>"
    b += (
        "<p>A function written inside a class is called a <b>method</b>. Add these two "
        "below <code>__init__</code>, indented 4 spaces, the same as "
        "<code>__init__</code>, so they are inside the class.</p>"
    )
    b += code(_pets_part("    def feed(self):", "    def report(self):"))
    b += reveal(
        "<code>self</code> appears in two kinds of places in <code>feed</code>. Find "
        "both and say what each one does. Then: <code>rocky.feed()</code> has nothing "
        "in its brackets, but <code>feed</code> has one parameter. Where does the "
        "value of that parameter come from?",
        "<p>The first place is <code>def feed(self):</code>, the parameter list. The "
        "first parameter of every method is <code>self</code>. It holds the pet the "
        "method is working on.</p>"
        "<p>The second place is <code>self.hunger = self.hunger - 1</code>, in the "
        "body. <code>self.hunger</code> means this pet's hunger. The line reads this "
        "pet's hunger, takes 1 off, and stores the answer back on the same pet.</p>"
        "<p>The value comes from the dot. When you write <code>rocky.feed()</code>, "
        "Python runs <code>feed</code> with <code>self</code> set to "
        "<code>rocky</code>. The object before the dot becomes <code>self</code>. "
        "<code>luna.feed()</code> runs the same lines with <code>self</code> set to "
        "<code>luna</code>.</p>",
    )

    b += "<h3>Piece 5: a method that returns</h3>"
    b += (
        "<p>Session 2's rule holds inside a class too: a function that works out a value "
        "returns it, and the caller prints it. <code>report</code> builds one line "
        "about the pet and returns it. Add it below <code>play</code>.</p>"
    )
    b += code(_pets_part("    def report(self):", "\n\n# make two pets"))
    b += "<p>Then, below the class, make a pet and call <code>report</code> two ways:</p>"
    b += code(s["report"])
    b += reveal(
        "Two calls to <code>report</code>, one inside <code>print</code> and one not. "
        "What appears in the terminal?",
        output("Rocky: hunger 5, happiness 5")
        + "<p>One line, not two. <code>rocky.report()</code> on a line by itself "
        "returns the line and nothing prints it, so it is thrown away. "
        "<code>print(rocky.report())</code> prints whatever <code>report</code> "
        "returned. This is session 2's print is not return, inside a class.</p>",
    )

    b += "<h3>Piece 6: two pets at once</h3>"
    b += (
        "<p>Here is the whole of <code>pets.py</code>. The part at the bottom makes "
        "two pets and treats them differently.</p>"
    )
    b += code(_root_file("pets.py"), "pets.py")
    b += downloads("pets.py")
    b += reveal(
        "Write both lines on paper before you open the answer. Then say why "
        "Luna's hunger is not 3.",
        output(
            """Rocky: hunger 3, happiness 5
Luna: hunger 5, happiness 6"""
        )
        + "<p>Rocky was fed twice, so Rocky's hunger went 5, 4, 3. Luna was never fed, "
        "so Luna's hunger is still 5. Luna played once, so Luna's happiness is 6, and "
        "Rocky's is still 5.</p>"
        "<p>Each pet has its own copy of every attribute. <code>rocky.feed()</code> "
        "changes <code>rocky.hunger</code> and nothing else.</p>",
    )

    b += '<h2><span class="num">2</span>Trace, then predict<span class="mins">15 minutes</span></h2>'
    b += (
        "<p>Each round goes under the class in <code>pets.py</code>, in place of the "
        "lines that make Rocky and Luna. Write your prediction on paper before you "
        "open the answer, then run it to check.</p>"
    )
    b += "<h3>Round 1</h3>"
    b += code(s["round1"])
    b += reveal(
        "What two lines are printed?",
        output(
            """Mochi: hunger 2, happiness 5
Pixel: hunger 5, happiness 7"""
        )
        + "<p>Mochi was fed three times: hunger 5, 4, 3, 2. Mochi never played, so "
        "happiness stays 5. Pixel was never fed, so hunger stays 5. Pixel played "
        "twice: happiness 5, 6, 7.</p>",
    )
    b += "<h3>Round 2</h3>"
    b += code(s["round2"])
    b += reveal(
        "What is printed? Then: does the answer make sense for a pet?",
        output("Mochi: hunger -2, happiness 12")
        + "<p>Each pass through the loop feeds Mochi once and plays once. Seven passes: "
        "hunger is 5 take away 7, which is -2, and happiness is 5 add 7, which is "
        "12.</p>"
        "<p>The program does what the code says, but the pet makes no sense. A hunger "
        "of -2 means nothing, and nothing in the class stops it. Section 5 shows how to "
        "fix that.</p>",
    )
    b += "<h3>Round 3</h3>"
    b += code(s["round3"])
    b += reveal(
        "How many pets does this code make? What two lines are printed?",
        output(
            """Mochi: hunger 3, happiness 5
Mochi: hunger 3, happiness 5"""
        )
        + "<p>One pet. Only <code>Pet(...)</code> makes a pet, and it appears once. "
        "<code>b = a</code> does not copy Mochi. It gives the same pet a second name, "
        "so feeding <code>b</code> feeds <code>a</code>. To count the pets in a "
        "program, count the calls to <code>Pet(...)</code>.</p>",
    )
    b += "<h3>Quick check</h3>"
    b += code(s["check"])
    b += reveal(
        "What does the last line print? Pick one and say why."
        '<ul class="tight"><li><b>A.</b> 3</li><li><b>B.</b> 5</li>'
        "<li><b>C.</b> 4</li><li><b>D.</b> an error, because luna has not been "
        "fed</li></ul>",
        output("5")
        + "<p>B. Luna was made with hunger 5 and was never fed. Feeding "
        "<code>rocky</code> changes rocky's hunger only. Luna's hunger exists from the "
        "moment <code>Pet(\"Luna\")</code> runs <code>__init__</code>, so there is no "
        "error.</p>",
    )

    b += '<h2><span class="num">3</span>Six broken pets<span class="mins">10 minutes</span></h2>'
    b += (
        "<p>Each program has exactly one mistake. With a partner, for each one: "
        "predict what the terminal says, find the mistake, and fix it. Ninety seconds "
        "each. Broken pets 3, 4, and 5 use the working <code>Pet</code> class from "
        "section 1, so they only show the lines below it.</p>"
    )
    b += _broken(
        1, s,
        "TypeError: Pet.feed() takes 0 positional arguments but 1 was given",
        "<code>def feed():</code> has no <code>self</code>. <code>rocky.feed()</code> "
        "always sends rocky in as the first value, and this <code>feed</code> has no "
        "parameter to put it in. The error says so: 0 parameters, but 1 value was "
        "given.",
        "<code>def feed(self):</code>",
    )
    b += _broken(
        2, s,
        "UnboundLocalError: cannot access local variable 'hunger' where it is not "
        "associated with a value",
        "<code>hunger = hunger - 1</code> has no <code>self.</code> in front. Without "
        "it, <code>hunger</code> is an ordinary variable inside <code>feed</code>. It "
        "has never been given a value, so Python cannot read it to take 1 off. The "
        "pet's hunger is <code>self.hunger</code>.",
        "<code>self.hunger = self.hunger - 1</code>",
    )
    b += _broken(
        3, s,
        "TypeError: Pet.feed() missing 1 required positional argument: 'self'",
        "<code>Pet.feed()</code> calls the method on the class, not on a pet, so "
        "there is no pet to put in <code>self</code>. The error names the empty "
        "parameter.",
        "<code>rocky.feed()</code>",
    )
    b += _broken(
        4, s,
        "AttributeError: type object 'Pet' has no attribute 'name'",
        "<code>rocky = Pet</code> has no brackets, so no pet is made. "
        "<code>rocky</code> becomes a second name for the class itself, which the "
        "error calls a type object. The class has no <code>name</code>. Each pet gets "
        "its own name in <code>__init__</code>, and no pet was made.",
        "<code>rocky = Pet(\"Rocky\")</code>",
    )
    b += _broken(
        5, s,
        "TypeError: Pet.feed() takes 1 positional argument but 2 were given",
        "<code>rocky.feed(rocky)</code> sends rocky twice: once through the dot, which "
        "fills <code>self</code>, and once in the brackets. <code>feed</code> has 1 "
        "parameter and was given 2 values.",
        "<code>rocky.feed()</code>",
    )
    b += _broken(
        6, s,
        "TypeError: Pet() takes no arguments",
        "<code>_init_</code> has one underscore on each side, so Python does not treat "
        "it as the setup method. The class has no <code>__init__</code>, so "
        "<code>Pet(\"Rocky\")</code> has nowhere to send the name. Some fonts draw two "
        "underscores as one long line, so count them.",
        "<code>def __init__(self, name):</code>, with two underscores on each side.",
    )

    b += _forest_section()

    b += '<h2><span class="num">5</span>Build your own<span class="mins">15 minutes</span></h2>'
    b += (
        "<p>Pick one: a creature of your own, or a forest of your own. Each has its own "
        "brief below.</p>"
        "<h3>A creature</h3>"
        "<p>A dragon, a robot, a houseplant, a moody cat, a boss from a game. Pick "
        "something and write a class for it in a new file.</p>"
        "<h3>The creature brief</h3>"
        '<ul class="tight">'
        "<li>An <code>__init__</code> that takes at least the creature's name as a "
        "parameter.</li>"
        "<li>At least 3 attributes that are numbers: health, energy, fuel, water, "
        "whatever fits your creature.</li>"
        "<li>At least 2 methods, and each one changes at least one attribute.</li>"
        "<li>A <code>report</code> method that returns one line about the creature, "
        "printed by the caller.</li>"
        "<li>At least 2 creatures with different names, treated differently, that end "
        "with different reports. That is your proof that each one keeps its own "
        "attributes.</li>"
        "<li>Your own class, not <code>Pet</code> with the names changed.</li>"
        "</ul>"
        "<h3>A forest</h3>"
        "<p>Save a copy of <code>forest.py</code> under a new name and change the "
        "<code>Tree</code> class. The window loop can stay as it is.</p>"
        "<h3>The forest brief</h3>"
        '<ul class="tight">'
        "<li>At least one new attribute that each tree keeps for itself, set in "
        "<code>__init__</code>: its own leaf colour, its own trunk width, a number of "
        "fruit.</li>"
        "<li>At least one new method, with at least one parameter after "
        "<code>self</code>, the way <code>grow</code> has <code>amount</code>. It "
        "changes at least one attribute.</li>"
        "<li><code>draw</code> uses your new attribute, so you can see it in the "
        "window.</li>"
        "<li>At least 5 trees in the list, made with a <code>for</code> loop.</li>"
        "<li>At least one key that changes every tree, with a <code>for</code> loop over "
        "the list.</li>"
        "</ul>"
        "<h3>Check before you call it done</h3>"
        '<ul class="tight">'
        "<li>The class name starts with a capital letter.</li>"
        "<li><code>__init__</code> has two underscores on each side.</li>"
        "<li>Every method is indented inside the class.</li>"
        "<li>Every method has <code>self</code> as its first parameter.</li>"
        "<li>Every attribute inside a method has <code>self.</code> in front of it.</li>"
        "<li>Every call has the object before the dot and nothing in the brackets for "
        "<code>self</code>: <code>drake.fly()</code>, not <code>drake.fly(drake)</code> "
        "and not <code>Dragon.fly()</code>.</li>"
        "<li>You made as many creatures as your program has calls to the class.</li>"
        "<li>In a forest, every <code>pygame.draw</code> line for a tree is inside "
        "<code>draw</code>, and the window loop calls <code>draw</code> on every tree in "
        "the list.</li>"
        "</ul>"
        "<h3>Stuck for an idea?</h3>"
        "<p>A dragon with health, fire, and age. A robot with battery, heat, and "
        "version. A houseplant with water, light, and leaves. A wizard with mana, "
        "spells, and wisdom.</p>"
        "<p>For a forest: an autumn forest, where each tree has its own leaf colour and "
        "a key turns every tree orange. A fruit forest, where "
        "<code>add_fruit(count)</code> adds to each tree's number of fruit and "
        "<code>draw</code> puts small red circles near the top. A forest of thin trees "
        "and thick trees, where each tree has its own trunk width.</p>"
        "<h3>Keep a number in range</h3>"
        "<p>Round 2 in section 2 gave Mochi a hunger of -2. One <code>if</code> gate in "
        "<code>feed</code>, like the gates in session 1, fixes it: only take 1 off when "
        "hunger is above 0. In a forest, the same kind of gate in <code>grow</code> can "
        "stop a tree before its leaves go past the top of the window.</p>"
    )
    b += reveal(
        "Before you open this, write the condition the gate should check.",
        code(s["gate"])
        + "<p>Put this <code>feed</code> in place of the old one and run round 2 from "
        "section 2 again:</p>"
        + output("Mochi: hunger 0, happiness 12")
        + "<p>Hunger stops at 0. Happiness still reaches 12, because <code>play</code> "
        "has no gate yet. Writing that one is yours.</p>",
    )
    b += exits(
        "<code>pets.py</code> runs and prints the two lines from piece 6, and you can "
        "say what <code>self</code> is when <code>rocky.feed()</code> runs.",
        "Floor, plus your own class that meets every line of one brief in section 5: "
        "the creature brief, with two creatures that end with different reports, or the "
        "forest brief, with at least 5 trees that change when you press a key.",
        "Middle, plus every number in your class stays between 0 and 10: a gate in "
        "every method that changes one, as in Keep a number in range in section 5. Then "
        "add a method "
        "called <code>tick</code> that moves time on by one hour (you decide what "
        "changes), call it 10 times in a <code>for</code> loop, and print the report "
        "after each call. For a forest instead: a gate in <code>grow</code> stops every "
        "tree before its leaves go past the top of the window, and a second key grows "
        "only <code>forest[0]</code>, as in forest round 1.",
    )
    b += panel(
        ["6.EE.B.6", "MP7", "MP6"],
        "<p>30 building the pet, 15 the rounds and the quick check, 10 broken pets, 20 "
        "the forest, 15 build your own and exits. There is no opener: the session starts "
        "with piece 1. "
        "Section 1's 30 minutes includes typing. A "
        "student who falls behind downloads <code>pets.py</code> from the button under "
        "piece 6 and reads it instead of typing it. Nobody types the forest: students "
        "download <code>forest.py</code> at the start of section 4 and read it.</p>"
        "<p>If the room reaches section 4 late, run <code>forest.py</code> on the "
        "projector, press G three times and then L, and do tree piece 4 and forest "
        "round 1 together. The eighth tree and forest round 2 can be skipped.</p>",
        "<p>Use the quick check at the end of section 2 as a hinge. Count hands for each "
        "letter before anyone opens the answer. <b>A</b> (3) means the student thinks "
        "all pets share one hunger. <b>C</b> (4) can mean the student shared the "
        "two feeds out between the two pets. <b>D</b> means the student thinks an "
        "attribute exists only after a method has changed it, so <code>__init__</code> "
        "is not yet real to them. If more than a few pick A or D, run piece 6 again "
        "on the projector before broken pets.</p>"
        "<p>Slow down on round 3. <code>b = a</code> gives the "
        "same pet a second name; it does not make a second pet. Have the room count "
        "the calls to <code>Pet(</code> before anyone opens the answer.</p>"
        "<p>Broken pets 1 to 5 are the mistakes to expect while students write their "
        "own class in section 5: <code>self</code> missing from the parameter list, "
        "<code>self.</code> missing in the body, calling on the class instead of the "
        "pet, missing brackets, and sending the pet twice. Broken pet 6 is hard to see "
        "on a projector, where two underscores can look like one line. Point at them "
        "and count them out loud.</p>"
        "<p>Say <code>self</code> the same way every time: it is the object before the "
        "dot. Broken pets 1, 3, and 5 all come down to that one sentence.</p>"
        "<p>In tree piece 3, expect some students to add the height to "
        "<code>GROUND</code>. Ask which way y counts in the window before anyone opens "
        "the answer. Forest round 2 is round 3 in a new form: have the room count the "
        "calls to <code>Tree(</code> before anyone opens the answer.</p>",
        retouch=(
            "Session 2's print is not return, now inside a class: <code>report</code> "
            "returns a line and the caller prints it. Session 1's <code>if</code> gate, "
            "used in Keep a number in range to hold hunger at 0. Session 3's window, "
            "where y counts down from the top, sets the top of each trunk. Session 4's "
            "key events, now G and L."
        ),
        extras=(
            "<h3>Files</h3><p><code>pets.py</code> for sections 1 and 2, with a "
            "download button under piece 6. <code>verify_pets.py</code> is for you. It runs every piece, "
            "every round, the quick check, the gate, and all six broken pets, and "
            "prints the last line of each error. The page's code for those comes from "
            "that file, and every output and error on the page came from running it "
            "on Python 3.12.3. The six error lines read the same on Python 3.11 and "
            "3.13. Older versions word some of them differently.</p>"
            "<p><code>forest.py</code> for section 4, with a download button at the start "
            "of the section. <code>verify_forest.py</code> is for you. It runs "
            "<code>forest.py</code> without a screen, presses G three times and then L, "
            "runs the eighth tree change and both forest rounds, and saves the two "
            "screenshots on this page. The page's code for the forest rounds comes from "
            "that file. Verified headless on pygame 2.6.1.</p>"
            "<h3>Lifted this week</h3><p><code>class</code>, <code>__init__</code>, "
            "<code>self</code>, attributes, methods, objects, <code>pass</code>, a list "
            "of objects, <code>pygame.draw.circle</code>.</p>"
        ),
    )
    b += pager(
        ("wed04_two_way.html", "Session 4: encrypt or decrypt"),
        ("wed06_rock_paper_scissors.html", "Session 6: rock, paper, scissors, three ways"),
    )
    return b


def day07():
    """Session 7: hill climbing and a small genetic algorithm."""
    b = masthead(
        "07",
        "Smarter than brute force",
        "Wednesday 18 November 2026",
        "A lock with seven digits has ten million codes, and trying every code in turn "
        "is called brute force. Today you open that lock in about 170 tries, using "
        "nothing but a score, a random change, and a rule about when to keep it.",
    )
    b += (
        '<div class="flag"><b>No class on 11 November.</b> Veterans Day, so session 6 '
        "was two weeks ago.</div>"
    )
    b += '<h2><span class="num">1</span>Opener<span class="mins">10 minutes</span></h2>'
    lock = "4703916"
    codes = 10 ** len(lock)
    tries = int(lock) + 1
    b += "<p>Talk this one over with your neighbor first.</p>"
    b += reveal(
        "In session 6, <code>rps_three_ways.py</code> checked three versions of "
        "<code>winner</code> on all nine pairings. Why check all nine, when three tests "
        "had already printed the right answers?",
        "<p>Three tests only try three pairings, and a mistake can sit in a pairing the "
        "tests never tried. In session 6, a mistake planted in <code>BEATS</code> would "
        "have passed all three tests, and checking every pairing caught it.</p>"
        "<p>Today's first program does the same to a lock: it tries every code.</p>",
    )
    b += (
        f"<p>A lock has {len(lock)} digits, and each digit is 0 to 9. A program tries "
        "every code in order: 0000000, then 0000001, then 0000002, and so on. Trying "
        "every possibility in turn like this is called <b>brute force</b>. The lock's "
        f"code is <code>{lock}</code>.</p>"
    )
    b += reveal(
        f"How many codes does the lock have? How many tries does the program need to "
        f"reach {lock}?",
        f"<p><b>Codes.</b> 10 choices for each of {len(lock)} digits: "
        + " × ".join(["10"] * len(lock))
        + f" = {codes}, ten million.</p>"
        f"<p><b>Tries.</b> {tries}. Read as a number, {lock} has {int(lock)} codes before "
        f"it, from 0000000 to {int(lock) - 1}, and the right code is one more try.</p>",
    )

    b += '<h2><span class="num">2</span>A score changes everything<span class="mins">25 minutes</span></h2>'
    b += (
        "<p>Brute force learns one thing per guess: right or wrong. Suppose "
        "instead the lock tells you how many positions are correct. That one change makes the problem much easier.</p>"
    )
    b += code(
        '''def score(guess):
    """Return how many positions in guess match the secret."""
    hits = 0
    for i in range(len(SECRET)):
        if guess[i] == SECRET[i]:
            hits = hits + 1
    return hits


def hill_climb():
    """Keep any single-digit change that does not make the score worse."""
    current = ""
    for i in range(len(SECRET)):
        current = current + random.choice(DIGITS)

    best = score(current)
    tries = 1
    while best < len(SECRET):
        spot = random.randrange(len(SECRET))
        new_digit = random.choice(DIGITS)
        candidate = current[:spot] + new_digit + current[spot + 1:]

        tries = tries + 1
        if score(candidate) >= best:
            current = candidate
            best = score(candidate)
    return tries''',
        "smarter_than_brute.py",
    )
    example, spot, digit = "1234567", 2, "9"
    b += (
        "<p>Two pieces of <code>hill_climb</code> are new. "
        "<code>random.randrange(len(SECRET))</code> returns a random whole number from 0 "
        "up to, but not including, <code>len(SECRET)</code>, so it picks a position in "
        "the code.</p>"
        "<p><code>current[:spot]</code> is a <b>slice</b>: the characters of "
        "<code>current</code> before position <code>spot</code>. "
        "<code>current[spot + 1:]</code> is the characters after position "
        "<code>spot</code>. Joined with <code>new_digit</code> between them, they make a "
        "copy of <code>current</code> with the digit at <code>spot</code> replaced. If "
        f"<code>current</code> is <code>\"{example}\"</code> and <code>spot</code> is "
        f"{spot}, then <code>current[:{spot}]</code> is "
        f"<code>\"{example[:spot]}\"</code> and <code>current[{spot + 1}:]</code> is "
        f"<code>\"{example[spot + 1:]}\"</code>, so with a new digit of {digit} the "
        f"candidate is <code>\"{example[:spot] + digit + example[spot + 1:]}\"</code>.</p>"
    )
    b += reveal(
        "Brute force needs about 4.7 million tries on this lock. Guess how many hill "
        "climbing needs. Write a number.",
        output(
            """secret is 7 digits, so there are 10000000 codes

brute force        4703917 tries
random guessing    200000 tries (capped at 200000)

hill climbing, five runs:
  run 1: 193 tries
  run 2: 183 tries
  run 3: 50 tries
  run 4: 238 tries
  run 5: 165 tries
  average 165.8 tries"""
        )
        + "<p>About 170. That is roughly twenty eight thousand times less work than "
        "brute force's 4703917 tries. Note the middle line too: random guessing of whole codes failed inside "
        "200000 tries, so random guessing on its own does not help. The score is what helps.</p>"
        "<p>The five runs differ a lot, from 50 to 238. A method with a random start does not have one running time. It has a range. One run tells you almost nothing about the range; five runs start to.</p>",
    )
    b += (
        "<p>Why <code>&gt;=</code> rather than <code>&gt;</code> in the keep rule? "
        "Because a change that leaves the score alone still moves you sideways, and "
        "sideways moves are how you get out of a position where every single-digit change makes the score worse. It is the same <code>&gt;</code> against <code>&gt;=</code> question as session 1.</p>"
    )

    b += '<h2><span class="num">3</span>Breeding codes<span class="mins">30 minutes</span></h2>'
    b += (
        "<p>A genetic algorithm keeps a population instead of one candidate. Sort by "
        "score, keep the best few, and build the rest by cutting two parents together "
        "and occasionally changing one digit at random.</p>"
    )
    b += code(
        """        population.sort(key=score, reverse=True)
        if score(population[0]) == len(SECRET):
            return generation, population[0]

        parents = population[:keep]
        population = list(parents)

        while len(population) < pop_size:
            mum = random.choice(parents)
            dad = random.choice(parents)
            cut = random.randrange(1, len(SECRET))
            child = mum[:cut] + dad[cut:]

            if random.random() < 0.3:
                spot = random.randrange(len(SECRET))
                child = child[:spot] + random.choice(DIGITS) + child[spot + 1:]

            population.append(child)"""
    )
    b += (
        "<p>Slices work on lists too. <code>population[:keep]</code> is the first "
        "<code>keep</code> codes in the list, the best ones after the sort. A slice with "
        "the number before the colon starts there: <code>dad[cut:]</code> is the "
        "characters of <code>dad</code> from position <code>cut</code> to the end. So "
        "<code>mum[:cut] + dad[cut:]</code> is the front of one parent joined to the "
        "back of the other.</p>"
        "<p><code>return generation, population[0]</code> returns two values at once: "
        "how many generations it took, and the code it found. The line that calls the "
        "function stores them in two variables, <code>g, winner = genetic(40, 8)</code>, "
        "in the order they were returned.</p>"
    )
    b += reveal(
        "Population of 40, keeping the best 8. It finishes in about 17 generations. Is "
        "that better or worse than hill climbing's 170 tries? Careful.",
        output(
            """genetic algorithm, five runs:
  run 1: 24 generations, found 4703916
  run 2: 8 generations, found 4703916
  run 3: 4 generations, found 4703916
  run 4: 11 generations, found 4703916
  run 5: 38 generations, found 4703916
  average 17.0 generations of 40 codes each"""
        )
        + "<p>Worse. Seventeen generations of "
        "forty codes is about 680 scored guesses. Hill climbing used 170. The genetic "
        "algorithm looks faster only if you count generations instead of work.</p>"
        "<p>Compare like with like. A generation is not a try. On a lock this simple the population is wasted effort. The fancier method lost.</p>",
    )
    b += exits(
        "You ran hill climbing and can explain what <code>score</code> gives you that a "
        "yes-or-no answer does not.",
        "Floor, plus five runs recorded with their spread, plus you can say why the keep "
        "rule uses <code>&gt;=</code>.",
        "Middle, plus count scored guesses rather than generations for the genetic "
        "algorithm and settle which method actually wins. Then find a lock where the "
        "population does help: make the score reward only exact whole-code matches and "
        "watch hill climbing fall apart.",
    )
    b += panel(
        ["8.F.B.5", "MP1", "MP8"],
        "<p>10 opener, 25 hill climbing, 30 the genetic algorithm, 25 the comparison "
        "argument and exits. The comparison is the real content, so do not let it get "
        "squeezed.</p>",
        "<p>Students will report their best run as the result. Insist on five runs and a "
        "range. A method with a random start has a spread, and reporting the best of "
        "five is how people fool themselves.</p>"
        "<p>The seed is fixed at 4703 in the file so your numbers match this page. Take "
        "the seed out once and let them see the numbers move, then put it back. That "
        "sets up session 8 and session 9, where a fixed seed is what makes the run repeatable.</p>"
        "<p>Expect resistance to the conclusion that the genetic algorithm lost. Good. "
        "Make them do the multiplication on the board.</p>",
        retouch=(
            "Session 6's check of every pairing. Brute force is the same idea on a lock, "
            "trying every code, and the opener counts how many tries that is before the "
            "alternative appears. <code>random.choice</code> from session 6's game."
        ),
        extras=(
            "<h3>Files</h3><p><code>smarter_than_brute.py</code>, seeded with 4703. All "
            "five-run figures verified on Python 3.12.3 and reproducible with that "
            "seed.</p>"
            "<h3>Lifted this week</h3><p><code>random.randrange</code>, "
            "<code>random.random</code>, <code>list.sort</code> with a "
            "<code>key</code>, string slicing to replace one character.</p>"
        ),
    )
    b += pager(
        ("wed06_rock_paper_scissors.html", "Session 6: rock, paper, scissors, three ways"),
        ("wed08_monte_carlo.html", "Session 8: settling it by simulation"),
    )
    return b
