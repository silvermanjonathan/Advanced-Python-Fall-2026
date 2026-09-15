"""Sessions 1 and 2."""

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
        "These four lines are the floor for this course.</p>"
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
        "output against your paper. Mark every line you got wrong. Those marks are the "
        "only useful information in this session, so do not tidy them away.</p>"
        '<div class="predict"><b>Rule for the term.</b> Read it, trace it, then run it. '
        "Running first tells you what happened. Tracing first tells you why it "
        "happened. You need the second one.</div>"
    )

    b += '<h2><span class="num">4</span>The style pass<span class="mins">30 minutes</span></h2>'
    b += (
        "<p>The program works and it is hard to read. Those are separate facts. "
        "<code>t</code>, <code>c</code>, <code>b</code>, and <code>bi</code> cost you "
        "time during the cold read, and you can measure that cost: it is however long "
        "you spent scrolling back up to find out what <code>bi</code> meant.</p>"
        "<p>Rename every variable so the name says what the value is. Then add a "
        "docstring at the top of the file. A docstring is a new word today, so here is "
        "the whole idea: one sentence, inside triple quotes, on line 1 of the file, "
        "saying what the program is for. Python ignores it. The next reader does not. "
        "Here is one for this program. Copy it onto line 1, or put your own sentence "
        "between the quotes.</p>"
    )
    b += code('''"""Summarize a run of tower readings and report where the strongest one sat."""''', "line 1 of sweep_report.py")
    b += reveal(
        "Rename all seven short names on paper before you look. Yours does not have to "
        "match mine. It has to be honest.",
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
        + "<p>One name here is still a small lie. <code>best_index</code> holds the "
        "first largest index, not the best one, and nothing in the name tells you that. "
        "<code>first_best_index</code> is the honest name. Naming is not decoration. It "
        "is where the bug hides.</p>",
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
            "Trace all four values, then give each one an honest name. One of the four "
            "is much harder to name than the others.",
            output("x 7\ny 5\nz 0\nq 3")
            + "<p><code>x</code> is <code>open_count</code>, 7. <code>y</code> is "
            "<code>shut_count</code>, 5. <code>q</code> is "
            "<code>longest_open_run</code>, 3.</p>"
            "<p><code>z</code> is the hard one. It prints 0, so it looks like a counter "
            "that never worked. It is actually <code>current_open_run</code>, and it "
            "reads 0 only because the last door in the list is shut. Name it "
            "<code>open_run_so_far</code> and the 0 stops looking like a bug.</p>"
            "<p>A name that makes a correct value look wrong costs you just as much as "
            "a name that makes a wrong value look right.</p>",
        )
        + "<p>Delete any comment that says what the line already says. A comment earns "
        "its place by saying why, not what.</p>"
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
        "and drop <code>average_of</code> and <code>last_best_index</code>. Keep "
        "section 5, because the five checks are the second trace of the strict gate "
        "and the retrieval the course depends on. The floor exit does not change.</p>"
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
        None, ("wed02_return_and_modules.html", "Session 2: functions that hand things back")
    )
    return b


def day02():
    """Session 2: return values and your own module."""
    b = masthead(
        "02",
        "Functions that hand something back",
        "Wednesday 23 September 2026",
        "A function can show you a number or it can give you a number, and those are "
        "different things. Today yours start handing values back, which is what lets "
        "you test a function, build one out of another, and split a program across two "
        "files.",
    )

    b += '<h2><span class="num">1</span>Opener<span class="mins">10 minutes</span></h2>'
    b += (
        "<p>Last week you renamed <code>sweep_report.py</code> and found the character "
        "that picks index 5 over index 9. On paper, from memory: what were the four "
        "numbers it printed, and which one depended on that character?</p>"
    )
    b += reveal(
        "Write the four numbers before you click.",
        output("total 503\naverage 50.3\nover 55: 6\nbest 77 at index 5")
        + "<p>The fourth one. Same list, same readings, all term.</p>",
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
        "<p>The first one prints 6, then crashes.</p>"
        + output(
            """6
Traceback (most recent call last):
  File "demo.py", line 1, in <module>
    doubled = show_total([1, 2, 3]) * 2
              ~~~~~~~~~~~~~~~~~~~~~~^~~
TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'""",
            "what Python says",
        )
        + "<p>A function with no <code>return</code> hands back <code>None</code>, and "
        "<code>None</code> times 2 is not a thing. The second one puts 12 in "
        "<code>doubled</code> and prints nothing at all.</p>"
        "<p>A printing function shows you a number. A returning function gives you a "
        "number. Only the second kind can be used in arithmetic, and only the second "
        "kind can be tested.</p>",
    )
    b += (
        '<div class="predict"><b>This is the grade 8 definition of a function.</b> '
        "A rule that assigns to each input exactly one output. <code>total_of</code> "
        "takes a list in and hands one number out. <code>show_total</code> assigns "
        "nothing to anything, so it is not a function in the mathematical sense at all, "
        "whatever the <code>def</code> keyword says.</div>"
    )

    b += '<h2><span class="num">3</span>Build the module<span class="mins">25 minutes</span></h2>'
    b += (
        "<p>Make a new file. It holds functions and nothing else. No printing, no "
        "readings list, no loop at the bottom. A file like that is a module.</p>"
    )
    b += code(
        '''"""Helpers that summarize a list of tower readings.

Every function here hands a value back. None of them print.
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
        "looking for a file called <code>sweep_tools.py</code> and hands you everything "
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

    b += (
        '<h2><span class="num">5</span>Test it, do not trust it'
        '<span class="mins">15 minutes</span></h2>'
    )
    b += (
        "<p>A returning function can be checked against an answer you worked out "
        "yourself. Add these lines. Predict every one before running.</p>"
    )
    b += code(
        '''print("--- checks ---")
print(f"total_of([1, 2, 3]) expected 6 got {sweep_tools.total_of([1, 2, 3])}")
print(f"total_of([]) expected 0 got {sweep_tools.total_of([])}")
print(f"count_over([5, 5, 5], 5) expected 0 got {sweep_tools.count_over([5, 5, 5], 5)}")
print(f"best_index([9, 9]) expected 0 got {sweep_tools.best_index([9, 9])}")
print(f"last_best_index([9, 9]) expected 1 got {sweep_tools.last_best_index([9, 9])}")'''
    )
    b += reveal(
        "Two of these five are traps. Which two, and why? Write your five expected "
        "values first.",
        output(
            """--- checks ---
total_of([1, 2, 3]) expected 6 got 6
total_of([]) expected 0 got 0
count_over([5, 5, 5], 5) expected 0 got 0
best_index([9, 9]) expected 0 got 0
last_best_index([9, 9]) expected 1 got 1"""
        )
        + "<p>All five pass. The traps are the empty list, where <code>total_of</code> "
        "sensibly hands back 0, and <code>count_over([5, 5, 5], 5)</code>, where nothing "
        "counts because 5 is not strictly greater than 5. Most students predict 3 for "
        "that one.</p>"
        "<p>Now call <code>sweep_tools.average_of([])</code> on purpose.</p>"
        + output(
            """  File "sweep_tools.py", line 17, in average_of
    return total_of(values) / len(values)
           ~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~
ZeroDivisionError: division by zero""",
            "verified traceback",
        )
        + "<p>Read the file name in that traceback. Your machine will show the full "
        "path; the point is the file name. The error is reported inside "
        "<code>sweep_tools.py</code>, not in the file you ran. A traceback crosses file "
        "boundaries and tells you which file broke. That is new this week, and it is "
        "most of the reason splitting a program into files is worth the trouble.</p>",
    )

    b += '<h2><span class="num">6</span>Where to stop<span class="mins">5 minutes</span></h2>'
    b += (
        '<div class="exits">'
        '<div class="exit"><span class="lab">FLOOR</span><p><code>sweep_tools.py</code> '
        "holds <code>total_of</code> and <code>count_over</code>, both returning, and "
        "<code>sweep_report2.py</code> imports them and prints the right two "
        "numbers.</p></div>"
        '<div class="exit"><span class="lab">MIDDLE</span><p>All five functions written '
        "and imported, output matching session 1, and the five checks passing with your "
        "predictions written down first.</p></div>"
        '<div class="exit"><span class="lab">STRETCH</span><p>Middle, plus add '
        "<code>spread_of(values)</code>, returning the largest value minus the "
        "smallest, written so it calls other functions in your module rather than "
        "looping again. Then break <code>average_of([])</code> on purpose and write "
        "down which file the traceback names.</p></div>"
        "</div>"
    )

    b += panel(
        ["8.F.A.1", "MP7", "6.EE.B.6"],
        "<p>10 opener, 20 print against return, 25 building the module, 15 the import, "
        "15 the checks, 5 exits. The module build runs long. If you are short, ship "
        "three functions instead of five and keep the checks.</p>",
        "<p>The common failure is a function with both a <code>print</code> and a "
        "<code>return</code> in it. It works, and it teaches nothing. Make them delete "
        "the print. Rule for the term: a module never prints.</p>"
        "<p>Second common failure is running <code>sweep_tools.py</code> directly, "
        "seeing no output, and deciding it is broken. It is not broken. It has nothing "
        "to say. Name that moment out loud before it happens.</p>"
        "<p>Watch for anyone who predicted 3 on <code>count_over([5, 5, 5], 5)</code>. "
        "That is last week's strict inequality in a new costume, one week later, which "
        "is exactly the retrieval this session is built to force.</p>",
        retouch=(
            "The strict <code>&gt;</code> gate from session 1, now given two names. "
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
