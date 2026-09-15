"""Sessions 1 and 2."""

import os

from build import code, masthead, output, pager, reveal
from stds import panel


def day01():
    """Session 1: cold read and style pass."""
    b = masthead(
        "01",
        "Cold read, then a style pass",
        "Wednesday 16 September 2026",
        "You will read a working program you have never seen, predict what it prints, "
        "and only then run it. After that you will rename everything in it so the next "
        "reader does not have to work as hard as you just did.",
    )

    b += (
        '<div class="toolbar"><a class="btn" href="wed01_worksheet.html">Open the '
        'worksheet</a><a class="btn quiet" href="wed01_doors_trace.html">Watch the door '
        "trace fill in</a></div>"
    )
    b += '<h2><span class="num">1</span>Opener<span class="mins">10 minutes</span></h2>'
    b += (
        "<p>No code yet. On paper, write down what each of these does. One line each. "
        "These four lines are what this course assumes you already know.</p>"
        '<ul class="tight">'
        "<li><code>for i in range(10):</code></li>"
        "<li><code>total = total + r</code></li>"
        "<li><code>if r &gt; best:</code></li>"
        "<li><code>slot = (slot + 5) % 9</code></li>"
        "</ul>"
        "<p>If any of the four is unfamiliar, say so now rather than in November. "
        "Nothing later in the course assumes more than these plus lists.</p>"
        "<p>Keep the paper. You check your answers against a real program in four "
        "minutes.</p>"
    )

    b += '<h2><span class="num">2</span>The cold read<span class="mins">25 minutes</span></h2>'
    b += (
        "<p>Here is the whole program. Read it top to bottom before you touch a "
        "keyboard. Do not run it. Do not type it. Read it. There is a "
        '<a href="wed01_worksheet.html">printed worksheet</a> for this session with a '
        "trace table for each loop, one row per pass, so you have somewhere to write "
        "the values down as they change.</p>"
    )
    b += code(
        """readings = [41, 58, 33, 58, 12, 77, 58, 60, 29, 77]
limit = 55

t = 0
c = 0
b = 0
bi = 0

for i in range(10):
    r = readings[i]

    t = t + r

    if r > limit:
        c = c + 1

    if r > b:
        b = r
        bi = i

avg = t / 10

print(f"total {t}")
print(f"average {avg}")
print(f"over {limit}: {c}")
print(f"best {b} at index {bi}")""",
        "sweep_report.py, first half",
    )
    b += reveal(
        "Four numbers come out. Write all four on your paper before you click. The "
        "fourth one is the one people get wrong.",
        output("total 503\naverage 50.3\nover 55: 6\nbest 77 at index 5")
        + "<p>The list holds 77 twice, at index 5 and at index 9. The program reports "
        "index 5. The reason is the single character <code>&gt;</code> in "
        "<code>if r &gt; b</code>. When the second 77 arrives, 77 is not greater than "
        "77, so the gate stays shut and <code>bi</code> keeps the value it already "
        "had.</p>"
        "<p>Change that one character to <code>&gt;=</code> and the answer becomes "
        "index 9. Neither version is wrong. They answer different questions. The code "
        "has to say which question you meant.</p>",
    )

    b += "<h3>The second half</h3>"
    b += (
        "<p>Same file, next four lines. One operator here may be new. "
        "<code>%</code> gives the remainder after dividing: <code>41 % 9</code> is 5, "
        "because 41 is four nines with 5 left over. It never returns 9 or more.</p>"
    )
    b += code(
        """slot = 0
for i in range(10):
    slot = (slot + readings[i]) % 9
    print(f"i={i} reading={readings[i]} slot={slot}")""",
        "sweep_report.py, second half",
    )
    b += reveal(
        "Trace this by hand. What is <code>slot</code> after i=0, after i=1, and after "
        "i=2?",
        output(
            """i=0 reading=41 slot=5
i=1 reading=58 slot=0
i=2 reading=33 slot=6
i=3 reading=58 slot=1
i=4 reading=12 slot=4
i=5 reading=77 slot=0
i=6 reading=58 slot=4
i=7 reading=60 slot=1
i=8 reading=29 slot=3
i=9 reading=77 slot=8"""
        )
        + "<p>41 wraps to 5 because 41 is 36 plus 5. Then 5 plus 58 is 63, and 63 is "
        "exactly seven nines, so slot lands on 0. Two different readings can land on "
        "the same slot, and two identical readings can land on different slots, because "
        "what wraps is the running total and not the reading. Look at i=1 and i=3: both "
        "readings are 58, and the slots are 0 and 1.</p>",
    )

    b += '<h2><span class="num">3</span>Run it<span class="mins">10 minutes</span></h2>'
    b += (
        "<p>Now type it, or open the copy on the machine, and run it. Compare the real "
        "output against your paper. Mark every line you got wrong. Do not erase the marks. For each wrong line, find the pass in your trace where the value went off.</p>"
        '<div class="predict"><b>Read it, trace it, then run it.</b> Running shows you what the program printed. Tracing shows you why. That is the order for every program in this course.</div>'
    )

    b += '<h2><span class="num">4</span>The style pass<span class="mins">30 minutes</span></h2>'
    b += (
        "<p>The program works and it is hard to read. <code>t</code>, <code>c</code>, <code>b</code>, and <code>bi</code> made the cold read slower: every time you met one, you had to scroll back up to find out what it was.</p>"
        "<p>Rename every variable so the name says what the value is. Then add a "
        "docstring at the top of the file. A docstring is a new word today. It is one sentence, inside triple quotes, on line 1 of the file, "
        "saying what the program is for. Python ignores it. The next reader does not. "
        "Here is one for this program. Copy it onto line 1, or put your own sentence "
        "between the quotes.</p>"
    )
    b += code('''"""Summarize a run of tower readings and report where the strongest one sat."""''', "line 1 of sweep_report.py")
    b += reveal(
        "Rename all seven short names on paper before you look. Yours does not have to match mine. It has to say what the value is.",
        code(
            '''"""Summarize a run of tower readings and report where the strongest one sat."""

readings = [41, 58, 33, 58, 12, 77, 58, 60, 29, 77]
limit = 55

total = 0
over_limit = 0
best = 0
best_index = 0

for i in range(10):
    reading = readings[i]

    total = total + reading

    if reading > limit:
        over_limit = over_limit + 1

    if reading > best:
        best = reading
        best_index = i

average = total / 10

print(f"total {total}")
print(f"average {average}")
print(f"over {limit}: {over_limit}")
print(f"best {best} at index {best_index}")'''
        )
        + "<p>One name here can still mislead. <code>best_index</code> holds the index of the first largest value, and nothing in the name says first. <code>first_best_index</code> says it. A name that leaves something out sends the next reader the wrong way.</p>",
    )
    b += (
        "<h3>A second one, harder</h3>"
        "<p>Same job on a different program. This one counts doors along a corridor, "
        "where 1 means open and 0 means shut.</p>"
        + code(
            """door = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0]

x = 0
y = 0
z = 0
q = 0

for i in range(12):
    d = door[i]

    if d == 1:
        x = x + 1
        z = z + 1

    if d == 0:
        y = y + 1
        z = 0

    if z > q:
        q = z

print(f"x {x}")
print(f"y {y}")
print(f"z {z}")
print(f"q {q}")""",
            "gate_log.py",
        )
        + '<div class="toolbar"><a class="btn quiet" href="wed01_doors_trace.html">Watch '
        "this trace fill in, one gate at a time</a></div>"
        + reveal(
            "Trace all four variables, then give each one a clear name. All four count something about the doors. One of the four is much harder to name than the others.",
            output("x 7\ny 5\nz 0\nq 3")
            + "<p><code>x</code> is <code>open_count</code>, 7. <code>y</code> is "
            "<code>shut_count</code>, 5. <code>q</code> is "
            "<code>longest_open_run</code>, 3.</p>"
            "<p><code>z</code> is the hard one. It prints 0, so it looks like a counter "
            "that never worked. It is actually <code>current_open_run</code>, and it "
            "reads 0 only because the last door in the list is shut. Name it "
            "<code>open_run_so_far</code> and the 0 stops looking like a bug.</p>"
            "<p><code>z</code> was right, and its name made it look wrong. A clear name has to make a right value look right.</p>",
        )
        + "<p>Delete any comment that says what the line already says. A comment should say why the line is there. The line already says what it does.</p>"
    )

    b += panel(
        ["MP1", "MP6", "MP3"],
        "<p>10 opener, 25 cold read, 10 run and compare, 30 style pass, and the last 15 "
        "go to <code>gate_log.py</code> and packing up. The session stops after the "
        "doors: there is no separate exits section, because the style pass is the exit. "
        "The cold read is the diagnostic and it is the part to protect. If it runs long, "
        "the doors are what gets cut, and they become the take-home.</p>",
        "<p>This session is a placement test in ordinary clothes. Watch for anyone who "
        "cannot trace an accumulator at all. That tells you the room has beginners in "
        "it regardless of what the enrollment says. Three or more students stuck on "
        "<code>total = total + reading</code> means you should slow sessions 2 and 3 "
        "and push the module split back a week.</p>"
        "<p>Expect most of the room to say index 9. That error is the point of the "
        "session. Do not soften it, and do not let anyone settle it by running the "
        "program. Make them find the character.</p>"
        "<h3>If the diagnostic fails</h3>"
        "<p>If three or more students cannot trace <code>total = total + reading</code> "
        "by the end of section 2, this is the slower plan for the next two weeks, "
        "decided now rather than on the day.</p>"
        "<p>Session 2: replace the opener with the wrap loop from this session, traced "
        "again by hand with a new list of five readings. Build only "
        "<code>total_of</code>, <code>count_over</code>, and <code>best_index</code>, "
        "and drop <code>average_of</code> and <code>last_best_index</code>.</p>"
        "<p>Session 3: keep the hand encode and the dictionary. Run the crack as a "
        "projected trace you do together rather than a build, and cut the sets "
        "section. Students who could not trace an accumulator in session 1 still "
        "reach that session's floor: they encode by hand and read the top letter off "
        "the output. From session 4 the pace returns to the pages as written.</p>",
        extras=(
            "<h3>Files</h3><p><code>wed01_doors_trace.html</code>, an animated trace of <code>gate_log.py</code> for the projector: step or play, and the worksheet table fills in one gate at a time. <code>wed01_worksheet.html</code>, printed one per student, double-sided: a trace table for each loop, one row per pass, and the rename tables. Print it from the browser; the page is laid out for letter paper and the style pass starts on a fresh sheet. <code>sweep_report.py</code> and <code>gate_log.py</code>. Every output on this page "
            "came from running that file on Python 3.12.3. Re-run it on the classroom "
            "machines before Wednesday.</p>"
            "<h3>Constraints</h3><p>This session uses only the prerequisite vocabulary "
            "listed on the hub, so the diagnostic measures tracing rather than new "
            "syntax. The list opens from session 2. See the "
            '<a href="advanced_python_hub.html">hub</a>.</p>'
        ),
    )
    b += pager(
        None, ("wed02_return_and_modules.html", "Session 2: functions that return a value")
    )
    return b


READINGS = [41, 58, 33, 58, 12, 77, 58, 60, 29, 77]
LIMIT = 55


_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)


def _shipped(name, start):
    """Return the tail of a shipped program from the line that begins with start."""
    text = open(os.path.join(_ROOT, name)).read()
    return text[text.find(start):].rstrip("\n")


funcs_text = _shipped("sweep_tools_more.py", "def smallest_of")
prints_text = _shipped("sweep_report3.py", 'print(f"smallest')


def day02_extras():
    """Return (name, description, answer) for the section 5 functions, computed."""
    r = READINGS
    over = [v for v in r if v > LIMIT]
    return [
        ("smallest_of(values)", "The smallest reading.", min(r)),
        ("largest_of(values)", "The largest reading.", max(r)),
        ("spread_of(values)",
         "The largest minus the smallest. Write it by calling the two above.",
         max(r) - min(r)),
        ("count_under(values, limit)",
         "How many readings are strictly less than the limit. Use 55.",
         sum(1 for v in r if v < LIMIT)),
        ("count_between(values, low, high)",
         "How many readings are from low to high, both ends included. Use 30 and 60.",
         sum(1 for v in r if 30 <= v <= 60)),
        ("total_over(values, limit)",
         "The total of the readings that are strictly over the limit. Use 55.",
         sum(over)),
        ("first_over_index(values, limit)",
         "The index of the first reading strictly over the limit. Use 55.",
         next(i for i, v in enumerate(r) if v > LIMIT)),
    ]


def day02():
    """Session 2: return values and your own module."""
    b = masthead(
        "02",
        "Functions that return a value",
        "Wednesday 23 September 2026",
        "A function can show you a number or it can give you a number, and those are "
        "different things. Today yours start handing values back, which is what lets "
        "you test a function, build one out of another, and split a program across two "
        "files.",
    )

    b += '<h2><span class="num">1</span>Opener<span class="mins">10 minutes</span></h2>'
    b += (
        "<p>Three questions about last week. Talk them through with the person next to "
        "you, then we take answers from the room.</p>"
        '<ul class="tight">'
        "<li>Why did we trace the program on paper before running it? What did the "
        "trace table show you that running the program would not have?</li>"
        "<li>We renamed <code>t</code>, <code>c</code>, <code>b</code>, and "
        "<code>bi</code>. What does a good variable name do for the next person who "
        "reads the file?</li>"
        "<li>One character, <code>&gt;</code> against <code>&gt;=</code>, changed the "
        "answer. What does that tell you about reading code?</li>"
        "</ul>"
    )
    b += reveal(
        "Talk through all three before you click. The wording does not matter. Check "
        "whether you had the idea.",
        "<p><b>Tracing.</b> Running shows you what the program printed. Tracing shows "
        "you why, one pass at a time. The trace table showed the pass where the second "
        "77 arrived and the gate stayed shut. The printed output does not show that.</p>"
        "<p><b>Names.</b> A good name says what the value is, so the next reader does "
        "not have to scroll back up to work it out. The next reader is usually you, a "
        "week later.</p>"
        "<p><b>One character.</b> A single character can change which question the "
        "program answers, so you have to read every character. That is why the rule "
        "is read it, trace it, then run it.</p>",
    )

    b += (
        '<h2><span class="num">2</span>Print is not return'
        '<span class="mins">20 minutes</span></h2>'
    )
    b += "<p>Two functions that look like they do the same job.</p>"
    b += code(
        """def show_total(values):
    running = 0
    for v in values:
        running = running + v
    print(running)


def total_of(values):
    running = 0
    for v in values:
        running = running + v
    return running"""
    )
    b += reveal(
        "What does <code>doubled = show_total([1, 2, 3]) * 2</code> do? And what does "
        "<code>doubled = total_of([1, 2, 3]) * 2</code> do?",
        "<p><b>The first one</b>, with <code>show_total</code>, prints 6 and then "
        "crashes on the multiplication.</p>"
        + output(
            """6
Traceback (most recent call last):
  File "demo.py", line 1, in <module>
    doubled = show_total([1, 2, 3]) * 2
              ~~~~~~~~~~~~~~~~~~~~~~^~~
TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'""",
            "what Python says",
        )
        + "<p>A function with no <code>return</code> returns <code>None</code>, and "
        "<code>None</code> times 2 is an error.</p>"
        "<p><b>The second one</b>, with <code>total_of</code>, prints nothing. "
        "<code>total_of([1, 2, 3])</code> returns 6, 6 times 2 is 12, and 12 is "
        "stored in <code>doubled</code>. Nothing appears on the screen because nothing "
        "in that line prints.</p>"
        "<p>A printing function shows you a number on the screen and then it is gone. "
        "A returning function gives the number back to the line that called it, so "
        "that line can store it in a variable, do arithmetic with it, or pass it to "
        "another function.</p>",
    )
    b += (
        '<div class="predict"><b>Same word as in math class.</b> In math, a function '
        "is a machine: you put a number in and exactly one number comes out. "
        "<code>total_of</code> works that way. Put a list in, one number comes out. "
        "<code>show_total</code> puts a number on the screen, but nothing comes out of "
        "it for the rest of the program to use. From now on, when this course says "
        "function, it means the kind something comes out of.</div>"
    )

    b += '<h2><span class="num">3</span>Build the module<span class="mins">25 minutes</span></h2>'
    b += (
        "<p>Make a new file. It holds functions and nothing else. No printing, no "
        "readings list, no loop at the bottom. A file like that is a module.</p>"
    )
    b += code(
        '''"""Helpers that summarize a list of tower readings.

Every function here returns a value. None of them print.
"""


def total_of(values):
    """Return the sum of every number in values."""
    running = 0
    for v in values:
        running = running + v
    return running


def average_of(values):
    """Return the mean of values."""
    return total_of(values) / len(values)


def count_over(values, limit):
    """Return how many values are strictly greater than limit."""
    hits = 0
    for v in values:
        if v > limit:
            hits = hits + 1
    return hits


def best_index(values):
    """Return the index of the first largest value in values."""
    best = values[0]
    where = 0
    for i in range(len(values)):
        if values[i] > best:
            best = values[i]
            where = i
    return where


def last_best_index(values):
    """Return the index of the last largest value in values."""
    best = values[0]
    where = 0
    for i in range(len(values)):
        if values[i] >= best:
            best = values[i]
            where = i
    return where''',
        "sweep_tools.py",
    )
    b += (
        "<p>Look at <code>average_of</code>. It does not add anything up. It calls "
        "<code>total_of</code> and divides. A function that only prints could not be "
        "used this way, because it has nothing to give another function.</p>"
        "<p><code>best_index</code> and <code>last_best_index</code> differ by exactly "
        "the character you found last week. Now both questions have a name, and the "
        "name says which one you are asking.</p>"
    )

    b += '<h2><span class="num">4</span>Import your own file<span class="mins">15 minutes</span></h2>'
    b += (
        "<p>Second file, same folder. <code>import sweep_tools</code> sends Python "
        "looking for a file called <code>sweep_tools.py</code> and gives you everything "
        "inside it.</p>"
    )
    b += code(
        '''"""Summarize tower readings using our own sweep_tools module."""

import sweep_tools

readings = [41, 58, 33, 58, 12, 77, 58, 60, 29, 77]
limit = 55

print(f"total {sweep_tools.total_of(readings)}")
print(f"average {sweep_tools.average_of(readings)}")
print(f"over {limit}: {sweep_tools.count_over(readings, limit)}")
print(f"first best at {sweep_tools.best_index(readings)}")
print(f"last best at {sweep_tools.last_best_index(readings)}")''',
        "sweep_report2.py",
    )
    b += reveal(
        "Same readings as last week. Will the first three numbers match last week's "
        "output exactly?",
        output(
            """total 503
average 50.3
over 55: 6
first best at 5
last best at 9"""
        )
        + "<p>Identical, because the arithmetic did not change. Only the shape of the "
        "program changed. And now both answers to the index question sit next to each "
        "other with names on them.</p>",
    )

    b += '<h2><span class="num">5</span>Add to the module<span class="mins">20 minutes</span></h2>'
    b += (
        "<p>Your module has five functions. Add more. Pick from the list below, or "
        "invent your own, and write each one in <code>sweep_tools.py</code>. Every one "
        "takes the readings list in and returns one value. None of them print.</p>"
        "<p>Then open <code>sweep_report2.py</code> and add one <code>print</code> line "
        "for each new function, in the same style as the five already there. The "
        "answer column is what your print line should show for the readings list, so "
        "you can check your function without asking anyone.</p>"
        "<table><tr><th>Function</th><th>What it returns</th><th>Answer on the readings</th></tr>"
        + "".join(
            f"<tr><td><code>{name}</code></td><td>{what}</td><td><code>{answer}</code></td></tr>"
            for name, what, answer in day02_extras()
        )
        + "</table>"
        "<p>Two rules from earlier today still apply. A function that prints instead of "
        "returning cannot be used in a print line, so it fails the moment you try. And "
        "if a new function can be written by calling ones you already have, call them: "
        "<code>spread_of</code> should not contain a loop.</p>"
    )
    b += reveal(
        "Write <code>smallest_of</code> and its print line on paper before you look. "
        "Where does the running value start, and why does 0 not work?",
        code(
            '''def smallest_of(values):
    """Return the smallest number in values."""
    smallest = values[0]
    for v in values:
        if v < smallest:
            smallest = v
    return smallest''',
            "sweep_tools.py, added at the bottom",
        )
        + code(
            '''print(f"smallest {sweep_tools.smallest_of(readings)}")''',
            "sweep_report2.py, added at the bottom",
        )
        + "<p>The running value starts at the first reading, not at 0. Start it at 0 "
        "and nothing is ever smaller than 0, so the function returns 0 for every list "
        "that has no negatives in it. That is the same kind of mistake as the "
        "<code>&gt;</code> against <code>&gt;=</code> question from session 1: the "
        "starting value decides the answer.</p>"
        "<p>The print line is the same shape as the five above it: a label, then the "
        "module name, a dot, the function name, and the readings list in the "
        "brackets.</p>",
    )
    b += reveal(
        "All seven, written out. Look only after yours run, or when you are stuck on "
        "one and have already tried it on paper.",
        code(funcs_text, "sweep_tools_more.py, the seven functions")
        + code(prints_text, "sweep_report3.py, the seven print lines")
        + output(
            """smallest 12
largest 77
spread 65
under 55: 4
between 30 and 60: 6
total over 55: 388
first over 55 at index 1"""
        )
        + "<p>Two things to notice. <code>spread_of</code> is one line, because the "
        "two functions it needs already exist. And <code>count_between</code> uses "
        "one gate inside another: a reading has to pass <code>v &gt;= low</code> "
        "before it is even asked about <code>v &lt;= high</code>.</p>",
        show="Show all seven answers",
        hide="Hide the answers",
    )

    b += panel(
        ["8.F.A.1", "MP7", "6.EE.B.6"],
        "<p>10 opener, 20 print against return, 25 building the module, 15 the import, "
        "20 adding to the module. No slack. The module build runs long. If you are "
        "short, ship three functions instead of five in section 3 and let section 5 "
        "make up the difference: a student who adds <code>smallest_of</code> and "
        "<code>largest_of</code> has written five functions either way. Section 5 is "
        "where the room spreads out: two new functions is the floor, "
        "<code>count_between</code> with two limits is the middle, and a function of "
        "their own invention with a print line to match is the stretch.</p>",
        "<p>The common failure is a function with both a <code>print</code> and a "
        "<code>return</code> in it. It works, and it teaches nothing. Make them delete "
        "the print. Rule for the term: a module never prints.</p>"
        "<p>Second common failure is running <code>sweep_tools.py</code> directly, "
        "seeing no output, and deciding it is broken. It is not broken. It has nothing "
        "to say. Name that moment out loud before it happens.</p>"
        "<p>When <code>count_over</code> is written, ask the room what "
        "<code>count_over([5, 5, 5], 5)</code> returns. Anyone who says 3 has forgotten "
        "last week's strict <code>&gt;</code>, and that question is the retrieval this "
        "session is built to force.</p>",
        retouch=(
            "Session 1's three habits, asked for in the opener as ideas rather than "
            "numbers: trace before you run, name the value, and read every character. "
            "Then the strict <code>&gt;</code> gate from session 1, now given two names: "
            "<code>best_index</code> keeps <code>&gt;</code> and "
            "<code>last_best_index</code> uses <code>&gt;=</code>, so last week's "
            "argument becomes this week's pair of functions."
        ),
        extras=(
            "<h3>Files</h3><p><code>sweep_tools.py</code> and "
            "<code>sweep_report2.py</code>. All output verified on Python 3.12.3.</p>"
            "<h3>Lifted this week</h3><p><code>return</code>, <code>len()</code>, and "
            "<code>import</code> of your own module. Full list on the "
            '<a href="advanced_python_hub.html">hub</a>.</p>'
        ),
    )
    b += pager(
        ("wed01_cold_read.html", "Session 1: cold read"),
        ("wed03_counting.html", "Session 3: counting and cracking"),
    )
    return b
