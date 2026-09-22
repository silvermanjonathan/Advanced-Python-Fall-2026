"""Sessions 3 to 8."""

import os

from build import laddered, code, masthead, output, pager, reveal
from stds import panel


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


def day03():
    """Session 3: dicts, sets, counting, and cracking a Caesar."""
    b = masthead(
        "03",
        "Counting, and what counting lets you do",
        "Wednesday 30 September 2026",
        "A dictionary keeps each letter together with its count, so you do not need "
        "two separate lists. Then you will learn what a Caesar cipher is, write one, and "
        "break one by counting letters instead of trying every key.",
    )
    b += '<h2><span class="num">1</span>Opener<span class="mins">10 minutes</span></h2>'
    b += (
        "<p>Last week you wrote a module of functions that return values. On paper: write a function "
        "<code>count_of(values, wanted)</code> that returns how many times "
        "<code>wanted</code> appears in <code>values</code>. Four lines plus the "
        "<code>def</code>.</p>"
    )
    b += reveal(
        "Write yours first.",
        code(
            """def count_of(values, wanted):
    \"\"\"Return how many times wanted appears in values.\"\"\"
    hits = 0
    for v in values:
        if v == wanted:
            hits = hits + 1
    return hits"""
        )
        + "<p>Now imagine calling that 26 times, once per letter. It works, and it reads the whole text 26 times. Section 2 fixes that.</p>",
    )

    b += '<h2><span class="num">2</span>The parallel list problem<span class="mins">15 minutes</span></h2>'
    b += (
        "<p>Here is the version without a dictionary. One list holds the letters. A "
        "second list holds their counts, in the same order. <code>counts[0]</code> is "
        "the count for <code>a</code>, <code>counts[1]</code> is the count for "
        "<code>b</code>, and so on. The count for a letter is at the same index as "
        "the letter.</p>"
    )
    b += code(
        """letters = ["a", "b", "c"]
counts = [0, 0, 0]

# add 1 to the count for "b":
# find the index of "b" in letters, then add 1 at that index in counts
for i in range(3):
    if letters[i] == "b":
        counts[i] = counts[i] + 1"""
    )
    b += (
        "<p>The <code>counts</code> list has no letters in it, only numbers. To add 1 "
        "to the count for <code>b</code>, the program first has to find out which index "
        "<code>b</code> is at, so it loops through <code>letters</code> until it finds "
        "it. Here <code>b</code> is at index 1, so the 1 is added to "
        "<code>counts[1]</code>. With 26 letters, every single count starts with a "
        "search through up to 26 items.</p>"
    )
    b += (
        "<p>A dictionary removes the search. The letter is the key. The count is the "
        "value. No index, no second list, no keeping anything in step.</p>"
    )
    b += code(
        """counts = {}
counts["b"] = 0
counts["b"] = counts["b"] + 1
print(counts)"""
    )
    b += reveal(
        "What prints? And what happens if you run <code>counts[\"z\"] + 1</code> "
        "without setting <code>counts[\"z\"]</code> first?",
        output("{'b': 1}")
        + "<p>The second one raises <code>KeyError: 'z'</code>. A dictionary does not start a missing key at zero for you. <code>collections.Counter</code> does, which is why it exists.</p>",
    )

    b += "<h3>Counter</h3>"
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
print(counts)
print(counts["a"])
print(counts["z"])
print(counts.most_common(2))
print(counts.total())

counts.update("bandana")
print(counts)

first = Counter("listen")
second = Counter("silent")
print(first == second)""",
        "counter_tour.py",
    )
    b += reveal(
        "Two to predict before you run it. What does <code>counts[\"z\"]</code> print, "
        "when there is no z in banana? And what does the last line print?",
        output(
            """Counter({'a': 3, 'n': 2, 'b': 1})
3
0
[('a', 3), ('n', 2)]
6
Counter({'a': 6, 'n': 4, 'b': 2, 'd': 1})
True"""
        )
        + "<p>One line at a time:</p>"
        '<ul class="tight">'
        "<li><code>counts[\"a\"]</code> reads one count, the same way as a dictionary: "
        "3.</li>"
        "<li><code>counts[\"z\"]</code> is 0. A plain dictionary would stop with "
        "<code>KeyError</code>. A Counter gives 0 for anything it has not seen.</li>"
        "<li><code>most_common(2)</code> returns the top two, biggest first, as pairs "
        "of letter and count. Section 4 uses this to find the top letter.</li>"
        "<li><code>total()</code> adds up every count: banana has 6 letters.</li>"
        "<li><code>update(\"bandana\")</code> counts more letters into the same "
        "Counter, so a goes from 3 to 6.</li>"
        "<li><code>first == second</code> is <code>True</code> when two Counters have "
        "the same counts. listen and silent use the same letters the same number of "
        "times, so they are anagrams: two words made from the same letters.</li>"
        "</ul>",
    )

    b += (
        '<h2><span class="num">3</span>What a Caesar cipher is'
        '<span class="mins">30 minutes</span></h2>'
    )
    b += (
        "<p>A Caesar cipher is a way to scramble a message. Pick a number, move every letter forward in the alphabet by that "
        "number, and wrap around from z back to a.</p>"
        "<p>Three words come with it and get used for the next four sessions. The number "
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

    b += (
        '<h2><span class="num">4</span>Now break one'
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
        "<p>This is the <code>Counter</code> from section 2, with the spaces taken out "
        "first. The file starts with <code>from collections import Counter</code>, the "
        "same import line as in section 2. <code>counts.most_common(5)</code> returns "
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
        "<p>You have the key, and you have <code>shift_by</code> from section 3. "
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
        "top. It is the same function you wrote in section 3.</p>"
    )
    b += code(
        '''"""Break a Caesar cipher by letter frequency instead of by guessing."""

from collections import Counter

ENGLISH_ORDER = "etaoinshrdlcumwfgypbvkjxqz"

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
print("distinct letters used:", len(set(ciphertext.replace(" ", ""))))

k = guess_shift(ciphertext)
print(f"guessed shift {k}")
print("plaintext:", shift_by(ciphertext, -k))''',
        "caesar_crack.py",
    )
    b += reveal(
        "Run it. Do its lines match what you worked out in steps 1, 2, and 3?",
        output(
            """five most common: [('h', 12), ('u', 5), ('g', 5), ('r', 5), ('w', 4)]
distinct letters used: 14
guessed shift 3
plaintext: read the code and trace the code before you ever run the code"""
        )
        + "<p>They match. The one new line, <code>distinct letters used</code>, is "
        "explained under Sets, below.</p>"
        "<p>Two limits. The text has to be long enough for <code>e</code> to actually "
        "win, and the text has to be ordinary English. Try it on a short message and "
        "watch it fail.</p>",
    )
    b += (
        '<div class="predict"><b>Frequency counts are ratios.</b> 12 of 49 letters is '
        "about 0.24. In ordinary English <code>e</code> runs near 0.12. Your sample is "
        "small, so your share is off. Any small sample has this problem. Session 9 is about it.</div>"
    )
    b += (
        "<h3>Sets, in one line</h3>"
        "<p><code>set(text)</code> throws away duplicates and order, and keeps only "
        "which things appeared. That is what <code>distinct letters used: 14</code> came "
        "from. A set answers which, a Counter answers how many.</p>"
        "<p>That line also uses <code>.replace</code>. "
        "<code>ciphertext.replace(\" \", \"\")</code> replaces every space with "
        "nothing, so the spaces are gone before the set is made. Without it, the space "
        "would be counted as one more character, and the line would say 15 instead of "
        "14. <code>.replace</code> does not change <code>ciphertext</code> itself. It "
        "returns a new string, and the new string is what goes into "
        "<code>set</code>.</p>"
    )
    b += exits(
        "You encoded <code>dawn</code> and <code>zebra</code> by hand with key 3, you "
        "can say what plaintext, ciphertext, and key mean, and you ran "
        "<code>letter_counts</code> on the ciphertext and read the top letter off the "
        "output.",
        "Floor, plus <code>shift_by</code> written and encoding correctly including the "
        "wrap past z, plus the full crack running.",
        "Middle, plus break it on purpose: find a message short enough that the most "
        "common letter is not <code>e</code>, then write a <code>guess_shift</code> "
        "that scores all 26 shifts against English letter frequencies and picks the "
        "best total instead of trusting one letter.",
    )
    b += panel(
        ["6.SP.B.5.a", "6.RP.A.3", "MP7"],
        "<p>10 opener, 15 parallel lists and Counter, 30 the cipher by hand and "
        "<code>shift_by</code> written, 25 the crack in three steps, 10 sets and exits. Assume no student "
        "has seen a cipher before. Do not cut section 3 to save the crack. Cracking a "
        "cipher the students did not build teaches nothing about the cipher. Cut the sets "
        "subsection first if pressed.</p>",
        "<p>The hand encode is the part to insist on. Students who go straight to "
        "<code>ord</code> without doing <code>dawn</code> on paper will not spot the "
        "wrap, and the wrap is the only hard part of the cipher.</p>"
        "<p>Expect <code>ord</code> and <code>chr</code> to feel arbitrary. The fix is "
        "to say the actual numbers do not matter, only that they run in order. Nobody "
        "needs to memorise 97.</p>"
        "<p><code>KeyError</code> is the new traceback this week and students read it as "
        "a crash rather than as information. Say the sentence out loud: a dictionary "
        "does not start a missing key at zero for you.</p>"
        "<p>Some students will want to brute force all 26 shifts because it is easier "
        "to write. Let them, then ask what they would do with a Vigenere key of length "
        "7. Brute force stops being available and counting does not.</p>",
        retouch=(
            "The <code>%</code> wrap traced by hand in session 1, now on a 26 hour clock. "
            "Also the returning functions from session 2: "
            "<code>guess_shift</code> is only possible because <code>letter_counts</code> "
            "hands a Counter back."
        ),
        extras=(
            "<h3>Files</h3><p><code>caesar_encode.py</code> for section 3, the answer to the <code>shift_by</code> step; the build checks that its <code>shift_by</code> is identical to the one in <code>caesar_crack.py</code>. <code>caesar_crack.py</code>. Output verified on Python "
            "3.12.3. The plaintext restates this course's own rule from session 1, which "
            "is deliberate.</p>"
            "<h3>Lifted this week</h3><p>Dictionaries, sets, "
            "<code>collections.Counter</code>, <code>.replace()</code>, "
            "<code>ord</code> and <code>chr</code>.</p>"
            "<h3>Assumed knowledge</h3><p>None beyond the hub prerequisites plus the "
            "<code>%</code> wrap from session 1. Section 3 teaches what a cipher is, "
            "including the words plaintext, ciphertext, and key, and assumes students "
            "have never used one.</p>"
        ),
    )
    b += pager(
        ("wed02_return_and_modules.html", "Session 2: functions that return a value"),
        ("wed04_messy_files.html", "Session 4: messy files"),
    )
    return b


def day04():
    """Session 4: files and messy text."""
    b = masthead(
        "04",
        "Messy files, and saying what you threw away",
        "Wednesday 7 October 2026",
        "Real data arrives dirty. Today you read a file off the disk, decide line by "
        "line what is usable, keep a record of what you rejected and why, and write "
        "your results back out to a second file.",
    )
    b += '<h2><span class="num">1</span>Opener<span class="mins">10 minutes</span></h2>'
    b += (
        "<p>From memory, no looking: what does <code>Counter(\"banana\")</code> return? Write it exactly, brackets and all.</p>"
    )
    b += reveal(
        "Write it first.",
        output("Counter({'a': 3, 'n': 2, 'b': 1})")
        + "<p>Ordered by count, highest first. That ordering is a Counter feature, not "
        "a dictionary feature.</p>",
    )

    b += '<h2><span class="num">2</span>The file, and the boundary<span class="mins">20 minutes</span></h2>'
    b += (
        "<p>A program that reads a file depends on something it did not make. Call that a <b>boundary</b>: the place where the program meets the outside. Boundaries are where programs break. Two things can go wrong before you even see "
        "a number: the file might not exist, and a line might not be a number.</p>"
        "<p><code>try</code> and <code>except</code> let you say what to do instead of "
        "crashing.</p>"
    )
    b += code(
        """def read_lines(filename):
    \"\"\"Return every line in the file, or an empty list if it is missing.\"\"\"
    try:
        handle = open(filename, "r")
    except FileNotFoundError:
        print(f"no file called {filename}, so there is nothing to read")
        return []
    lines = handle.readlines()
    handle.close()
    return lines"""
    )
    b += reveal(
        "Why is <code>handle.readlines()</code> outside the <code>try</code> block "
        "rather than inside it?",
        "<p>Because the only error being handled is the file not existing. Once "
        "<code>open</code> succeeds, a failure in <code>readlines</code> is a different problem and should not be hidden by an <code>except</code> written for a different error.</p>"
        "<p>Catch one named thing. Never write a bare <code>except:</code>. It hides "
        "bugs you have not met yet.</p>",
    )

    b += '<h2><span class="num">3</span>Clean it<span class="mins">35 minutes</span></h2>'
    b += (
        "<p>The input file holds thirteen lines. Some have spaces around them, one has "
        "a comma stuck on, one is blank, one spells a number as a word, and one is "
        "negative. Here it is as it sits on disk.</p>"
    )
    b += code(
        """41
58
  33
58
twelve
12

77,
58
-9
60
29
77 ""","readings_raw.txt",
    )
    b += code(
        '''def clean(lines):
    """Return the numbers we could read, plus the lines we could not."""
    good = []
    rejected = []
    for raw in lines:
        text = raw.strip()
        text = text.replace(",", "")

        if text == "":
            rejected.append((raw, "blank"))
        else:
            try:
                value = int(text)
            except ValueError:
                rejected.append((raw, "not a number"))
            else:
                if value < 0:
                    rejected.append((raw, "negative"))
                else:
                    good.append(value)
    return good, rejected''',
        "clean_readings.py, the important part",
    )
    b += reveal(
        "Thirteen lines go in. How many numbers come out, and what is their total? You "
        "have seen this total before.",
        output(
            """lines in the file: 13
kept: [41, 58, 33, 58, 12, 77, 58, 60, 29, 77]
kept 10, rejected 3
rejected lines and why:
  'twelve\\n' -> not a number
  '\\n' -> blank
  '-9\\n' -> negative

readings_report.txt now says:
kept 10 readings
rejected 3 lines
total 503
average 50.3"""
        )
        + "<p>503 and 50.3. That is session 1's list, exactly. The dirty file held the "
        "same ten readings you have been working with since the first day, buried in "
        "three lines of rubbish.</p>"
        "<p>Notice <code>else</code> attached to <code>try</code>. It runs only when no "
        "exception happened, which keeps the negative check out of the block that is "
        "watching for <code>ValueError</code>.</p>",
    )
    b += (
        '<div class="predict"><b>The rejected list is the important part.</b> A program that '
        "silently drops three lines and reports an average is worse than one that "
        "crashes, because you will believe it. Say what you threw away and why, every "
        "time.</div>"
    )

    b += '<h2><span class="num">4</span>Write it back out<span class="mins">15 minutes</span></h2>'
    b += (
        "<p>Reading was <code>open(filename, \"r\")</code>. Writing is the same call "
        "with <code>\"w\"</code>, and then <code>handle.write</code> instead of "
        "<code>handle.readlines</code>. One line at a time, and you put the "
        "<code>\\n</code> on yourself.</p>"
    )
    b += code(
        '''def write_report(filename, good, rejected):
    """Write a short report next to the data."""
    handle = open(filename, "w")

    handle.write(f"kept {len(good)} readings\\n")
    handle.write(f"rejected {len(rejected)} lines\\n")
    total = 0

    for v in good:
        total = total + v

    handle.write(f"total {total}\\n")
    handle.write(f"average {total / len(good)}\\n")
    handle.close()''',
        "clean_readings.py, the report",
    )
    b += reveal(
        "Suppose every line in the file was rubbish, so <code>good</code> is empty. "
        "Which line of <code>write_report</code> breaks, and what does Python say?",
        "<p>The average line. <code>total / len(good)</code> divides by zero and Python "
        "stops with <code>ZeroDivisionError: division by zero</code>, the same error <code>average_of([])</code> would give in your session 2 module. The report file is left half "
        "written, with the first three lines in it and no average.</p>"
        "<p>That is a boundary too. A file with nothing usable in it is a real case, "
        "and a report that says <code>kept 0 readings</code> tells the reader more than a crash does. Guard the average with an <code>if</code> before you divide.</p>",
    )
    b += exits(
        "Your program opens the file, survives a missing file without crashing, and "
        "prints how many lines it read.",
        "Floor, plus the full clean with a rejected list carrying reasons, plus a "
        "written report file, plus total 503 confirmed against session 1.",
        "Middle, plus decide and defend a fourth rejection rule of your own, such as a "
        "reading above 200. Then write the rejected lines to their own file so someone "
        "could fix them by hand and re-run.",
    )
    b += panel(
        ["6.SP.B.5.a", "6.SP.B.5.c", "MP6"],
        "<p>10 opener, 20 the boundary, 35 cleaning, 15 report writing, 10 exits. "
        "Typing the dirty file by hand wastes time, so put "
        "<code>readings_raw.txt</code> on the machines beforehand.</p>",
        "<p>Two failures to expect. First, <code>int(\"  33\")</code> actually works in "
        "Python, so some students will conclude <code>.strip()</code> is pointless. It "
        "is not: <code>int(\"77,\")</code> fails, which is why the comma is in the file. "
        "Second, students will write a bare <code>except:</code> because it is shorter. "
        "Do not allow it.</p>"
        "<p>The reveal that this is session 1's data lands well if you do not "
        "telegraph it. Let them compute 503 and notice.</p>",
        retouch=(
            "Session 1's reading list and its total of 503, arriving this time as a file "
            "that has to be cleaned before the arithmetic works. Session 2's functions return the results."
        ),
        extras=(
            "<h3>Files</h3><p><code>clean_readings.py</code> writes and then reads "
            "<code>readings_raw.txt</code>, and writes "
            "<code>readings_report.txt</code>. Verified on Python 3.12.3.</p>"
            "<h3>Lifted this week</h3><p>File reading and writing, "
            "<code>try</code> and <code>except</code> with a named error, "
            "<code>try/else</code>, <code>.strip()</code>, <code>.append()</code>, "
            "returning two values at once.</p>"
        ),
    )
    b += pager(
        ("wed03_counting.html", "Session 3: counting and cracking"),
        ("wed05_transposition.html", "Session 5: moving letters"),
    )
    return b


def day05():
    """Session 5: transposition ciphers."""
    b = masthead(
        "05",
        "Ciphers that move letters instead of replacing them",
        "Wednesday 14 October 2026",
        "Session 3's Caesar cipher replaced each letter with a different one. These two "
        "keep every letter and change only where it sits, which means the letter counts "
        "stay identical and last session's frequency attack is useless against them.",
    )
    b += '<h2><span class="num">1</span>Opener<span class="mins">10 minutes</span></h2>'
    b += (
        "<p>In session 3 you built a Caesar cipher, then broke one by counting letters "
        "and never trying a key. Question on paper: if I rearrange the letters of a "
        "message without replacing any of them, what happens to the letter counts, and "
        "what happens to that attack?</p>"
    )
    b += reveal(
        "Answer before you click.",
        "<p>The counts do not change at all. Not one of them. Your frequency attack finds nothing, because it never looked at where the letters sit.</p>"
        "<p>This is why real systems use both kinds. Substitution hides which letters. "
        "Transposition hides where they are.</p>",
    )

    b += '<h2><span class="num">2</span>Rail fence<span class="mins">30 minutes</span></h2>'
    b += (
        "<p>Write the message down a zig-zag across three rails, then read each rail "
        "straight across. The message is "
        "<code>meetatthenorthgateatdawn</code>.</p>"
    )
    b += code(
        """def rail_encode(text, rails):
    \"\"\"Return text written down a zig-zag of rails, then read across.\"\"\"
    rows = []
    for r in range(rails):
        rows.append("")

    r = 0
    step = 1
    for ch in text:
        rows[r] = rows[r] + ch

        if r == 0:
            step = 1
        if r == rails - 1:
            step = -1

        r = r + step

    joined = ""
    for row in rows:
        joined = joined + row
    return joined""",
        "transposition.py",
    )
    b += reveal(
        "The two gates set <code>step</code> before <code>r</code> changes. Trace the "
        "first seven letters and write down which rail each one lands on.",
        "<p>Rails go 0, 1, 2, 1, 0, 1, 2. The turn happens at the top rail and the bottom rail. The two gates are one after the other, not one inside the other, so both get checked every pass.</p>"
        + output(
            """message  meetatthenorthgateatdawn
rails 3  maettdetthnrhaetanetogaw
back     meetatthenorthgateatdawn
round trip ok: True"""
        )
        + "<p>Count the letters in both. Twenty four each, same letters, different "
        "order. Decoding is harder than encoding here: you have to rebuild the zig-zag "
        "pattern first, then fill it in, because you need to know how many letters "
        "landed on each rail before you can cut the ciphertext up.</p>"
        "<p><code>rail_decode</code> is yours to write. Plan it on paper first: build "
        "the list of rail numbers the same way <code>rail_encode</code> did, then put the ciphertext letters into those positions one rail at a time. The file on the "
        "machines has a finished one to compare against when yours round-trips.</p>",
    )

    b += '<h2><span class="num">3</span>The route cipher<span class="mins">30 minutes</span></h2>'
    b += (
        "<p>Pack the message into a grid, then read the columns out in an order the key "
        "gives you. A negative number in the key means read that column bottom to "
        "top.</p>"
    )
    b += code(
        """def to_grid(text, width):
    \"\"\"Return text packed into rows of the given width.\"\"\"
    grid = []
    row = []
    for ch in text:
        row.append(ch)
        if len(row) == width:
            grid.append(row)
            row = []

    if len(row) > 0:
        while len(row) < width:
            row.append("x")
        grid.append(row)
    return grid


def route_encode(text, key):
    \"\"\"Return text read out column by column in the order key gives.

    A negative number in key means read that column bottom to top.
    \"\"\"
    grid = to_grid(text, len(key))
    out = ""
    for signed in key:
        col = abs(signed) - 1
        rows = range(len(grid))
        if signed < 0:
            rows = range(len(grid) - 1, -1, -1)

        for r in rows:
            out = out + grid[r][col]
    return out"""
    )
    b += reveal(
        "The grid is four columns wide and the key is <code>[2, -4, 1, 3]</code>. Read "
        "the first column of output by hand off the grid below.",
        output(
            """  m e e t
  a t t h
  e n o r
  t h g a
  t e a t
  d a w n
key      [2, -4, 1, 3]
route    etnheantarhtmaettdetogaw"""
        )
        + "<p>Key entry 2 means column 2 top to bottom, which is "
        "<code>etnhea</code>. Then -4 means column 4 bottom to top, "
        "<code>ntarht</code> reversed off the grid. A grid position is a pair of numbers, row and column. The key says which column to read and which way, so every pair ends up at one place in the output.</p>",
    )
    b += exits(
        "Rail fence encoding works on your own message and you can point at the two "
        "gates that make the zig-zag turn.",
        "Floor, plus <code>rail_decode</code> round-tripping true, plus the grid built "
        "and one column read out by hand.",
        "Middle, plus full route encoding with a signed key, then write "
        "<code>route_decode</code>. It is harder than it looks, because you "
        "have to work out the column heights before you can cut the string.",
    )
    b += panel(
        ["5.G.A.1", "8.F.A.1", "MP7"],
        "<p>10 opener, 30 rail fence, 30 route cipher, 20 exits. The decode functions "
        "are where time goes. If the room is struggling, ship encoding only and make "
        "decoding the take-home.</p>",
        "<p>The padding question comes up and is worth stopping for. A twenty four "
        "letter message fills a four wide grid exactly. Ask what happens with twenty "
        "five letters, and let them find that you must pad and that the padding is then "
        "visible to anyone reading the ciphertext.</p>"
        "<p><code>range(len(grid) - 1, -1, -1)</code> reads as gibberish at first. Walk "
        "it once out loud: start at the last row, stop before -1, step backwards.</p>",
        retouch=(
            "Session 3's frequency attack, revisited to show what it cannot do. The "
            "opener makes students state that letter counts survive transposition, "
            "which is what this session is about."
        ),
        extras=(
            "<h3>Files</h3><p><code>transposition.py</code>. Round trip verified true "
            "on Python 3.12.3.</p>"
            "<h3>Lifted this week</h3><p>List of lists as a grid, "
            "<code>range</code> with a negative step, <code>abs</code>, "
            "<code>\" \".join()</code>, slicing.</p>"
        ),
    )
    b += pager(
        ("wed04_messy_files.html", "Session 4: messy files"),
        ("wed06_hashing.html", "Session 6: seals and real hashes"),
    )
    return b


def day06():
    """Session 6: hashing and integrity."""
    b = masthead(
        "06",
        "A homemade seal, and a real one",
        "Wednesday 21 October 2026",
        "A seal is a short number computed from a message, so a reader can tell whether "
        "the message changed on the way. You will build one, break it in about five "
        "minutes, and then use a function that does not break.",
    )
    b += '<h2><span class="num">1</span>Opener<span class="mins">10 minutes</span></h2>'
    b += (
        "<p>In session 3 you turned letters into numbers with <code>ord</code>. Here is "
        "the simplest seal you can build out of that: add up the letter positions and "
        "wrap the total at 97.</p>"
    )
    b += code(
        '''def letter_sum_seal(text):
    """Return a seal: add up the letter positions, wrap at 97."""
    running = 0
    for ch in text:
        running = running + ord(ch)
    return running % 97''',
        "avalanche.py",
    )
    b += (
        "<p>Send the message and the seal. The reader recomputes the seal and compares. "
        "If the two disagree, the message changed.</p>"
        "<p>Now break it. On paper: what is the seal of <code>ab</code>, and what is the "
        "seal of <code>ba</code>?</p>"
    )
    b += reveal(
        "Both, before you click.",
        output(
            """seal of 'ab' = 1
seal of 'ba' = 1
same seal, different message: True"""
        )
        + "<p>Identical. Addition does not care what order it gets its numbers in, so "
        "every rearrangement of a message carries the same seal. A seal that cannot "
        "tell <code>ab</code> from <code>ba</code> cannot tell <code>attack at "
        "dawn</code> from any anagram of it, so an attacker can shuffle your message "
        "and leave the seal untouched.</p>"
        "<p>Two different messages with the same seal is called a collision. Real hash "
        "functions are built specifically to make collisions hard to find.</p>",
    )

    b += '<h2><span class="num">2</span>sha256<span class="mins">25 minutes</span></h2>'
    b += code(
        '''import hashlib


def sha(text):
    """Return the sha256 hex digest of text."""
    return hashlib.sha256(text.encode()).hexdigest()''',
        "avalanche.py",
    )
    b += reveal(
        "<code>attack at dawn</code> and <code>attack at dusk</code> differ by two "
        "letters. How much of the output do you expect to change?",
        output(
            """sha256 'attack at dawn'
  d502810c71aeb17e5ea1cbf930b46b87bb645a75df45f500230d061992aeb90a
sha256 'attack at dusk'
  9076bc233a9100d5c0885c6a5f055ca13d856d28ee9cf74941719bb292f88da7
sha256 'attack at dawn.'
  9156781e12f9522c7e8c5aef869a43a495be33b3f42c8c8fe9206dd7e2458b39"""
        )
        + "<p>All of it. Adding a single full stop to the end of "
        "<code>dawn</code> also changes everything.</p>",
    )

    b += '<h2><span class="num">3</span>Measure the avalanche<span class="mins">30 minutes</span></h2>'
    b += (
        "<p>Do not take my word for it. Count. A sha256 digest is 256 bits, so "
        "convert both digests to bits and count how many positions differ.</p>"
    )
    b += code(
        '''def bits_of(hexdigest):
    """Return hexdigest as a string of 0s and 1s."""
    number = int(hexdigest, 16)
    return format(number, "0256b")


def bits_differing(a, b):
    """Return how many bit positions differ between two hex digests."""
    left = bits_of(a)
    right = bits_of(b)

    count = 0
    for i in range(256):
        if left[i] != right[i]:
            count = count + 1
    return count'''
    )
    b += reveal(
        "Out of 256 bits, how many do you predict differ? Write a number, not a word.",
        output(
            """dawn vs dusk: 130 of 256 bits differ
dawn vs dawn+period: 124 of 256 bits differ"""
        )
        + "<p>Around 128 both times, which is half. That is the design goal: each "
        "output bit should flip with probability about one half whenever the input "
        "changes at all, no matter how small the change. 130 and 124 are both close to 128. Two tries is a small sample, so neither lands on it exactly.</p>"
        "<p>Two things follow. You cannot push the output in a chosen direction by making small changes to the input, because every small change changes about half the bits. And you cannot work backwards from a digest to the input, because nothing in the digest tells you which input produced it.</p>",
    )
    b += (
        '<div class="predict"><b>One limit.</b> A hash proves a file was not '
        "changed. It does not hide anything and it does not prove who sent it. If "
        "someone can replace both the file and its posted hash, you learn nothing.</div>"
    )
    b += exits(
        "You built the seal, found a collision in it by hand, and can explain why "
        "addition causes it.",
        "Floor, plus sha256 running on your own strings, plus you can state the "
        "avalanche property in your own words.",
        "Middle, plus count the differing bits yourself and run it on five pairs of "
        "near-identical strings. Record the five counts and their average. Then try to "
        "find any sha256 collision by hand and write down why you stopped.",
    )
    b += panel(
        ["7.SP.C.8", "MP2", "MP6"],
        "<p>10 opener, 25 sha256, 30 measuring the avalanche, 25 the limits and exits. "
        "<code>format(number, \"0256b\")</code> is the line that needs unpacking.</p>",
        "<p>Do not skip building the seal. A collision found in something you wrote "
        "ten minutes ago lands differently from a collision in something handed to "
        "you.</p>"
        "<p>Students conclude a hash is encryption. It is not, and the difference is "
        "worth ten minutes: encryption is meant to be reversed by the right person, and "
        "a hash is meant to be reversed by nobody. Ask them how they would decrypt a "
        "digest back to the message and let them work out that the digest is the same "
        "length whatever goes in, so most of the message cannot be in there.</p>"
        "<p>The bit-counting loop is the part most likely to defeat the floor group. "
        "Have the digest comparison ready as a fallback: line the two hex strings up on "
        "the projector and count matching characters instead.</p>",
        retouch=(
            "Session 3's <code>ord</code> arithmetic, used here to build a seal from "
            "scratch in the first ten minutes so students own it before it breaks."
        ),
        extras=(
            "<h3>Files</h3><p><code>avalanche.py</code>. Digests and bit counts on this "
            "page verified on Python 3.12.3. The digests are reproducible, so students "
            "should get the identical hex strings.</p>"
            "<h3>Lifted this week</h3><p><code>hashlib</code>, <code>.encode()</code>, "
            "<code>int(text, 16)</code>, <code>format</code> with a bit spec.</p>"
        ),
    )
    b += pager(
        ("wed05_transposition.html", "Session 5: moving letters"),
        ("wed07_what_it_costs.html", "Session 7: what a program costs"),
    )
    return b


def day07():
    """Session 7: the cost of a program."""
    b = masthead(
        "07",
        "What a program costs",
        "Wednesday 28 October 2026",
        "Two programs can both be correct and one can be unusable. Today you measure "
        "the difference, first by counting the work and then by timing it, and you build "
        "a table that tells you when brute force stops being an option.",
    )
    b += '<h2><span class="num">1</span>Opener<span class="mins">10 minutes</span></h2>'
    b += (
        "<p>A sorted list holds the 1000 even numbers from 0 to 1998. You are looking "
        "for 1998. On paper: how many values does a start-to-finish scan look at? Then, "
        "if you are allowed to jump to the middle and throw half away each time, how "
        "many?</p>"
    )
    b += reveal(
        "Both numbers before you click.",
        output(
            """searching a sorted list of 1000 even numbers for 1998
  linear: found at 999 after 1000 looks
  binary: found at 999 after 10 looks

searching for 1999, which is not there
  linear: returned -1 after 1000 looks
  binary: returned -1 after 10 looks"""
        )
        + "<p>1000 against 10. Halving 1000 ten times gets you below 1. That is where "
        "the 10 comes from, and it is why doubling the list only adds one look.</p>"
        "<p>Look at the missing-value case. Both searches do their worst "
        "work when the answer is not there, and the scan has no way to stop early.</p>"
        "<p>Here are the two searches that produced those numbers. Both return two "
        "values: where the target was, and how many values they looked at.</p>"
        + code(
            '''def linear_find(values, target):
    """Return the index of target, and how many values we looked at."""
    looks = 0
    for i in range(len(values)):
        looks = looks + 1
        if values[i] == target:
            return i, looks
    return -1, looks


def binary_find(values, target):
    """Return the index of target in a sorted list, and how many looks."""
    low = 0
    high = len(values) - 1
    looks = 0
    while low <= high:
        mid = (low + high) // 2
        looks = looks + 1

        if values[mid] == target:
            return mid, looks

        if values[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1, looks''',
            "what_it_costs.py, the two searches",
        )
        + "<p><code>//</code> divides and throws the remainder away, so <code>mid</code> "
        "is always a whole index. The <code>while</code> keeps going only while the "
        "two ends have not crossed, the first loop in this course whose stopping condition has two parts.</p>",
    )

    b += '<h2><span class="num">2</span>Every code, timed<span class="mins">35 minutes</span></h2>'
    b += (
        "<p><code>itertools.product</code> generates every combination for you. This "
        "sweeps every code of n digits and times it.</p>"
    )
    b += code(
        '''from itertools import product
from time import perf_counter

CODE = "4703916"


def sweep(digits):
    """Try every code of the given length. Return the winner and the tries."""
    tries = 0
    winner = ""
    target = CODE[:digits]

    for guess in product("0123456789", repeat=digits):
        tries = tries + 1
        attempt = "".join(guess)
        if attempt == target:
            winner = attempt
    return winner, tries


for n in range(1, 8):
    start = perf_counter()
    found, tries = sweep(n)
    elapsed = perf_counter() - start
    print(f"  {n}   {10 ** n:<10} {tries:<8} {elapsed:.4f}")''',
        "what_it_costs.py",
    )
    b += reveal(
        "Seven digits takes about 1.2 seconds on my machine. Before you look: how long "
        "for eight digits, and for ten?",
        output(
            """brute force, every code of n digits
  n   codes      tries    seconds
  1   10         10       0.0000
  2   100        100      0.0000
  3   1000       1000     0.0001
  4   10000      10000    0.0010
  5   100000     100000   0.0108
  6   1000000    1000000  0.1092
  7   10000000   10000000 1.1845"""
        )
        + "<p>Each row multiplies the one above it by ten. So eight digits is about 12 "
        "seconds, nine is about two minutes, ten is about twenty minutes, and twelve is "
        "about a day and a half. Nothing about the program changed. You added digits.</p>"
        "<p>Ten to the seventh is ten million, and the seconds column follows it. Every extra digit multiplies the time by ten.</p>",
    )
    b += (
        '<div class="predict"><b>These timings are from one machine.</b> Yours will '
        "differ, maybe by a factor of three. What will not differ is the shape: every "
        "extra digit costs ten times the last one. Run it and write your own numbers in "
        "the table.</div>"
    )
    b += (
        "<h3>Plot it</h3>"
        "<p>Put digits on the horizontal axis and seconds on the vertical. Sketch it by "
        "hand. Then sketch a second graph with the same data and seconds on a scale "
        "where each step up is ten times the last. On the first graph the small rows are flat against the bottom and only the last one shows. On the second, every row is readable.</p>"
    )
    b += exits(
        "You ran both searches and can say why binary needs 10 looks where the scan "
        "needs 1000.",
        "Floor, plus the runtime table built on your own machine out to six digits, plus "
        "a hand sketch of digits against seconds.",
        "Middle, plus extend to eight digits and check your prediction against the "
        "clock. Then work out how many digits you would need before the sweep takes "
        "longer than this class, and defend the arithmetic.",
    )
    b += panel(
        ["8.EE.A.1", "8.F.B.5", "MP8"],
        "<p>10 opener, 35 the sweep and the table, 20 plotting, 25 exits and "
        "discussion. Warn them off nine digits on a classroom machine: that is roughly "
        "two minutes with nothing on screen, and someone will assume it has hung.</p>",
        "<p>The prediction that matters is eight digits. Students who say 2 seconds have "
        "not understood the table; students who say 12 have. Make them commit out loud "
        "before running.</p>"
        "<p><code>perf_counter</code> measurements bounce around on a shared machine. "
        "Run each row three times and take the middle. Say so, because otherwise a noisy row looks like a discovery.</p>",
        retouch=(
            "Trying every key, from session 3, now timed. Students who wanted to try all "
            "26 Caesar shifts in session 3 see how long the same idea takes when there "
            "are ten million codes."
        ),
        extras=(
            "<h3>Files</h3><p><code>what_it_costs.py</code>. Timings above measured on "
            "Python 3.12.3 in this container and will not match the classroom "
            "machines.</p>"
            "<h3>Lifted this week</h3><p><code>itertools.product</code>, "
            "<code>time.perf_counter</code>, <code>//</code>, <code>while</code> with a "
            "compound condition, returning two values.</p>"
        ),
    )
    b += pager(
        ("wed06_hashing.html", "Session 6: seals and real hashes"),
        ("wed08_heuristics.html", "Session 8: smarter than brute force"),
    )
    return b


def day08():
    """Session 8: hill climbing and a small genetic algorithm."""
    b = masthead(
        "08",
        "Smarter than brute force",
        "Wednesday 4 November 2026",
        "Last week brute force ran out of road at ten digits. Today you open a seven "
        "digit lock in about 170 tries instead of ten million, using nothing but a "
        "score, a random change, and a rule about when to keep it.",
    )
    b += '<h2><span class="num">1</span>Opener<span class="mins">10 minutes</span></h2>'
    b += (
        "<p>From last week: every extra digit made the sweep ten times slower. Seven digits took about a second. About how long would ten digits take, and why?</p>"
    )
    b += reveal(
        "Both, on paper.",
        "<p>About twenty minutes, because three more digits is three more multiplications by ten: a second, ten seconds, a hundred seconds, a thousand seconds. Today's target is the same seven digit lock, <code>4703916</code>.</p>",
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
        + "<p>About 170. That is roughly twenty eight thousand times less work than the "
        "sweep. Note the middle line too: random guessing of whole codes failed inside "
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
        "sets up session 9 and session 10, where a fixed seed is what makes the run repeatable.</p>"
        "<p>Expect resistance to the conclusion that the genetic algorithm lost. Good. "
        "Make them do the multiplication on the board.</p>",
        retouch=(
            "Session 7's runtime table, which priced brute force at ten million tries "
            "for this exact lock. The opener re-derives that number before the "
            "alternative appears."
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
        ("wed07_what_it_costs.html", "Session 7: what a program costs"),
        ("wed09_monte_carlo.html", "Session 9: settling it by simulation"),
    )
    return b
