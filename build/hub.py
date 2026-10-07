"""The course hub, which serves as the site homepage."""

from build import esc
from stds import MAPNOTE, STD

SESSIONS = [
    ("01", "16 Sep", "wed01_cold_read.html", "Cold read, then a style pass",
     "Trace 60 lines of an unfamiliar working program, then rename everything in it. Session 1 also shows where the room is."),
    ("02", "23 Sep", "wed02_return_and_modules.html", "Functions that return a value",
     "return, composition, and splitting a program into your own importable module."),
    ("03", "30 Sep", "wed03_counting.html", "Counting, and a cipher in a window",
     "Accumulators and dictionaries, then collections.Counter, then write a Caesar cipher "
     "and put it in a pygame window."),
    ("04", "7 Oct", "wed04_transposition.html", "Ciphers that move letters",
     "Rail fence, then a route cipher on a list-of-lists grid with a signed key."),
    ("05", "14 Oct", "wed05_hashing.html", "Your seal, and a real one",
     "Build a letter-sum seal, find a collision in it, then hashlib.sha256 and the "
     "avalanche property, measured in bits."),
    ("06", "21 Oct", "wed06_what_it_costs.html", "What a program costs",
     "Linear against binary search, brute force with itertools.product, and a "
     "runtime-against-digits table you time yourself."),
    ("07", "28 Oct", "wed07_heuristics.html", "Smarter than brute force",
     "Fitness, mutation, selection. Hill climbing, then a small genetic algorithm, then a fair comparison of the two."),
    ("08", "4 Nov", "wed08_monte_carlo.html", "Settling an argument by simulation",
     "Monty Hall: trials, tally, convergence, and a silent bug that produces a stable "
     "wrong answer. Capstone brief issued."),
    ("09", "18 Nov", "wed09_benford.html", "The first digit tells on you",
     "Benford's law on two CSV files, one grown and one invented, with a histogram drawn "
     "in pygame."),
    ("10", "25 Nov", "wed10_markov.html", "Machines that write",
     "A word-pair model trained on a text file, then what the big language models do differently, and what they do the same."),
    ("11", "2 Dec", "wed11_classes.html", "Objects that remember their own history",
     "class, __init__, self, methods, and a list of objects stepped in one loop. A "
     "particle plume with gravity and trails. Capstone sketches due."),
    ("12", "9 Dec", "wed12_orbits.html", "Orbits",
     "Gravity as acceleration toward a body, and time steps."),
    ("13", "16 Dec", "wed13_demo_day.html", "To be written, then the demo",
     "The first half is not written yet. The second half is the sixty second parent "
     "demo."),
]

LIFTED = [
    ("Session 2", "<code>return</code> values, <code>len()</code>, <code>import</code> "
     "of your own module, <code>and</code> to join two comparisons"),
    ("Session 3", "the word accumulator, the empty string, <code>+</code> to join strings, dictionaries, <code>collections.Counter</code>, "
     "<code>ord</code> and <code>chr</code>, indexing a string, tuples, and a pygame "
     "window: the event loop, frames, <code>pygame.draw.rect</code>"),
    ("Session 4", "list of lists as a grid, slicing, <code>range</code> with a negative "
     "step, <code>abs</code>, <code>.join()</code>"),
    ("Session 5", "<code>hashlib</code>, <code>.encode()</code>, "
     "<code>int(text, 16)</code>, <code>format</code> with a bit spec"),
    ("Session 6", "<code>itertools.product</code>, <code>time.perf_counter</code>, "
     "<code>//</code>, compound <code>while</code> conditions"),
    ("Session 7", "<code>random.randrange</code>, <code>random.random</code>, "
     "<code>sort</code> with a <code>key</code>"),
    ("Session 8", "<code>random.seed</code> for reproducibility"),
    ("Session 9", "reading a file with <code>with open(...) as f:</code>, "
     "<code>try</code> and <code>except</code> with a named error, "
     "<code>csv.DictReader</code>, <code>math.log10</code>, "
     "<code>pygame.draw.line</code>, and a histogram drawn from data"),
    ("Session 10", "<code>collections.defaultdict</code>, tuples as dictionary keys, "
     "<code>.split()</code>, multiple assignment"),
    ("Session 11", "<code>class</code>, <code>__init__</code>, <code>self</code>, "
     "methods, a list of objects, <code>pygame.draw.lines</code>"),
    ("Session 12", "<code>math.sqrt</code> for distance, vector components, a time step"),
]

HELD = [
    ("Nested gates", "Flat <code>if</code> / <code>elif</code> / <code>else</code> "
     "only, all term. Two flat gates in a row beat one nested pair, and session 4's "
     "rail fence shows why."),
    ("<code>break</code>", "Lifted, but only in session 6 and after, and only where the "
     "loop exit is itself the topic. Before that, every <code>while</code> names its "
     "exit condition."),
    ("Bare <code>except:</code>", "Never. Catch one named error. A bare except hides "
     "bugs you have not met."),
    ("<code>pygame.font</code>", "Not used. Words go in the terminal, visuals go in the "
     "window. The session 3 cipher console draws its letters from squares, because "
     "there the letters are the picture."),
    ("Self-closing windows", "A pygame window never closes itself. "
     "<code>while running:</code>, an <code>event.get()</code> loop, a QUIT listener, "
     "and <code>clock.tick(60)</code>. The same loop in every window."),
    ("A module that prints", "Never. A module holds functions. The program that imports "
     "it does the printing."),
    ("turtle", "Not available in our VS Code setup, so every graphic on this course is "
     "pygame."),
]


def hub():
    """Return the hub page body."""
    b = (
        '<header class="top"><div class="wrap">'
        '<p class="eyebrow">Robofun &middot; Fall 2026 &middot; 110 West End Avenue</p>'
        "<h1>Advanced Python</h1>"
        '<p class="sub">A course about the machine underneath. You will read code '
        "before you run it, measure what a program costs instead of guessing, and build three things that look hard from the outside: a cipher you can watch in a window, a simulation that settles an argument, a program that writes sentences.</p>"
        '<div class="dates"><span class="pill"><b>Wednesdays</b> 16 Sep to 16 Dec 2026, '
        '13 sessions</span><span class="pill"><b>Time</b> 4:00 to 5:30</span>'
        '<span class="pill"><b>Grades</b> 5 to 8</span>'
        '<span class="pill"><b>Demo day</b> 16 December</span></div>'
        "</div></header>\n"
    )

    b += "<h2>The thirteen sessions</h2>"
    b += '<div class="grid">'
    for n, d, href, title, sub in SESSIONS:
        b += (
            f'<div class="row"><span class="n">{esc(n)}</span>'
            f'<span class="d">{esc(d)}</span>'
            f'<span class="t"><a href="{href}">{esc(title)}</a>'
            f'<span class="s">{esc(sub)}</span></span></div>'
        )
        if n == "08":
            b += (
                '<div class="row off"><span class="n">&middot;</span>'
                '<span class="d">11 Nov</span>'
                '<span class="t">No class, Veterans Day'
                '<span class="s">Fourteen Wednesdays fall in the term. This is the one '
                "that comes out, which is what makes it a thirteen session course. "
                "Session 9 comes straight after the two week gap.</span>"
                "</span></div>"
            )
    b += "</div>"
    b += (
        '<div class="flag"><b>Two dates to confirm against Robofun\'s closure list '
        "before this syllabus goes to parents.</b> 30 September falls in the "
        "intermediate days of Sukkot, which some Upper West Side programs skip. "
        "25 November, session 10, is the day before Thanksgiving, and attendance is "
        "usually light. Nothing later in the term depends on session 10, so anyone away "
        "can pick it up from its page.</div>"
    )
    b += (
        "<h2>Extras</h2>"
        "<p>Pages outside the thirteen sessions, for any time after the session they "
        "build on.</p>"
        '<div class="grid"><div class="row extra"><span class="n">+</span>'
        '<span class="d">after session 3</span>'
        '<span class="t"><a href="extra_crack_caesar.html">Break a Caesar cipher by '
        "counting letters</a>"
        '<span class="s">Count the letters of a coded message, turn the most common one '
        "into a key, and decode it without trying every key. Uses "
        "<code>shift_by</code> and <code>Counter</code> from session 3. About 25 "
        "minutes.</span></span></div></div>"
    )

    b += "<h2>What this course is for</h2>"
    b += (
        "<p>A model can write code for you. What it cannot do is tell you whether the code is right, what it "
        "will cost to run, or why it produced the number it produced. Those are the "
        "skills this course is about.</p>"
        "<p>So the order is always the same. Read it, trace it, then run it. Every page "
        "asks you to predict the output before you see it, because a prediction you got "
        "wrong teaches you something and a program you watched run does not.</p>"
        "<p>Three sessions are built around a wrong answer. In session 7 the fancier method loses. In session 11 five lists fall out of step. In session 8 a program settles on 0.5540 when the true value is 0.6667, with no error message anywhere, and finding out why is the point of that session.</p>"
    )

    b += "<h2>What this course assumes</h2>"
    b += (
        "<p>This course assumes the list below and teaches everything else in class. It does not assume you took any particular class before "
        "this one. Where a session needs an idea from an earlier session, that session "
        "says which one and re-derives it.</p>"
        "<p>You should already be able to read and write these. You do not need to be "
        "fast at them.</p>"
        '<ul class="tight">'
        "<li>Variables, and reassigning one.</li>"
        "<li><code>print</code>, and an f-string like <code>f\"total {n}\"</code>.</li>"
        "<li><code>if</code>, <code>elif</code>, <code>else</code>, and comparisons.</li>"
        "<li><code>for i in range(n):</code>, and a counter or a running total inside "
        "a loop.</li>"
        "<li>A list, and reading one item out of it with <code>values[i]</code>.</li>"
        "<li><code>def</code> with parameters, even if your functions have only ever "
        "printed.</li>"
        "</ul>"
        "<p>Everything else is taught during the term and is listed below. "
        "<code>return</code> values, dictionaries, files, and classes are all treated "
        "as new.</p>"
        "<p>No mathematics beyond grade 5 arithmetic is assumed either. Four things the "
        "course needs are taught in the session that first uses them, and none of them "
        "is assumed on the way in:</p>"
        "<table><tr><th>Introduced in</th><th>What, and how far it goes</th></tr>"
        "<tr><td>Session 3</td><td>Ciphers, taught from the start: what a Caesar cipher does, "
        "and the words plaintext, ciphertext, and key. Students encode by hand before "
        "any code.</td></tr>"
        "<tr><td>Session 9</td><td>Logarithms, only as far as \"what power of ten "
        "gives this number\". The calculator does the arithmetic.</td></tr>"
        "<tr><td>Session 11</td><td>Splitting a speed and an angle into an across "
        "amount and an up amount. Presented as a tool, with a squares check students "
        "can verify themselves.</td></tr>"
        "<tr><td>Session 12</td><td>The Pythagorean theorem, stated plainly as the "
        "distance rule.</td></tr>"
        "</table>"
        '<div class="flag"><b>If session 1 goes badly for a third of the room, the '
        "course is mispaced, not the room.</b> Advanced enrollment at an after-school "
        "program is usually chosen by a parent rather than verified against a skill "
        "check, and the grade band here is 5 to 8. Session 1 is built as a diagnostic "
        "for exactly this reason: it uses only the list above, so what it measures is "
        "tracing. Slow sessions 2 and 3 if the tracing is not there.</div>"
    )

    b += "<h2>Code rules</h2>"
    b += (
        "<p>Version 1, dated 12 September 2026. If you are holding a page that "
        "contradicts this list, this list wins.</p>"
    )
    b += "<h3>Opened this term, session by session</h3>"
    b += "<table><tr><th>From</th><th>Now allowed</th></tr>"
    for when, what in LIFTED:
        b += f"<tr><td>{esc(when)}</td><td>{what}</td></tr>"
    b += "</table>"
    b += (
        "<p>Session 1 uses nothing beyond the prerequisites above, on purpose, so the "
        "cold read measures tracing rather than new syntax.</p>"
    )
    b += "<h3>Still closed, or closed on purpose</h3>"
    b += "<table><tr><th>Rule</th><th>Why</th></tr>"
    for rule, why in HELD:
        b += f"<tr><td>{rule}</td><td>{why}</td></tr>"
    b += "</table>"

    b += "<h2>The Cartridge Ledger</h2>"
    b += (
        "<p>One printed card for the whole term, not one per session. Thirteen rows, one "
        "per Wednesday, each with room for the date, the thing you built, and one line in "
        "your own handwriting on what you would tell someone else about it.</p>"
        "<p>There are seven days between sessions and nothing survives on the machines, "
        "so the card is the only thing that carries from week to week. Bring it every "
        "time. It gets stamped at the door.</p>"
        "<p>Thirteen stamps is a full card. Bring the full card to the demo on "
        "16 December.</p>"
    )

    b += "<h2>Capstone</h2>"
    b += (
        "<p>The capstone runs from session 8 to the demo, not as a session of its own. "
        "The brief goes out on 4 November and the sketch is due on 2 December. There "
        "is no separate build session: the capstone is an addition to one of the two "
        "programs the course gives you in sessions 11 and 12, the particle plume or the "
        "orbit, and it is built inside those two sessions' stretch exits and shown at "
        "the demo on 16 December.</p>"
        "<p>Before any code: one page on paper with a hand drawn screen, every player "
        "action, everything on screen that is not the player, how score is kept, both "
        "ways the program can end, and then pseudocode in English. No sketch means no "
        "build. Session 8's page carries the four yes-or-no checks it is judged by.</p>"
    )

    b += "<h2>Standards</h2>"
    b += (
        "<p>All 27 codes below were retrieved from the CASE Network through the Learning "
        "Commons Knowledge Graph on 12 September 2026, and each statement is quoted in "
        "full apart from the two deviations named under the table. Each session maps to "
        "at most three.</p>"
    )
    b += "<table><tr><th>Code</th><th>Statement</th></tr>"
    for c in sorted(STD, key=lambda k: (k.startswith("MP"), k)):
        b += f'<tr><td class="std">{esc(c)}</td><td>{esc(STD[c])}</td></tr>'
    b += "</table>"
    b += MAPNOTE
    b += (
        '<div class="flag"><b>On New York and CSTA.</b> The Learning Commons graph '
        "carries Common Core and state-adopted frameworks. It returned nothing for New "
        "York's Computer Science and Digital Fluency codes, and it rejects CSTA as a "
        "jurisdiction outright. So the anchor here is the Common Core mathematics "
        "framework, which is the national option. No CSTA or New York code appears "
        "anywhere on this site, because none could be verified. Paste the codes you want "
        "and they can be added with the usual verification flags.</div>"
    )

    b += "<h2>Open decisions</h2>"
    b += (
        "<p>These are built one way and can be built the other. Each one is a real "
        "choice, not an oversight.</p>"
        "<table><tr><th>Decision</th><th>Built as</th><th>If you change it</th></tr>"
        "<tr><td>Are classes lifted?</td><td>Yes, from session 11</td>"
        "<td>Sessions 11 and 12 restructure around functions plus parallel lists, and "
        "the plume and the orbit both go. Those two sessions would need replacing.</td>"
        "</tr>"
        "<tr><td>Environment</td><td>VS Code throughout, pygame for all graphics</td>"
        "<td>Sessions 3, 9, 11, and 12 need pygame on the machines. Sessions 1, 2, 4 to "
        "8, and 10 are terminal only and run anywhere.</td></tr>"
        "<tr><td>Theme</td><td>None.</td>"
        "<td>Sessions 3, 4, and 5 are all about ciphers and could share one theme. Sessions 6 to 12 would not.</td></tr>"
        "<tr><td>Data files</td><td>Three needed on disk</td>"
        "<td><code>honest_ledger.csv</code>, "
        "<code>cooked_ledger.csv</code>, <code>corpus.txt</code>. All three are generated "
        "by scripts in the repo, so nothing needs fetching over the network. Each has a "
        "download button on the page of the session that uses it.</td></tr>"
        "<tr><td>Capstone sketch deadline</td><td>Session 11, 2 December</td>"
        "<td>It comes after session 9, the histogram window, because the sketch "
        "describes a window, and after session 10, the light attendance day before "
        "Thanksgiving. The build lives in the session 11 and 12 stretch exits.</td></tr>"
        "</table>"
    )

    b += "<h2>Programs in this repo</h2>"
    b += (
        "<p>Every output printed on these pages came from running these files on Python "
        "3.12.3, with pygame 2.6.1 for the sessions that open a window, verified headless. "
        "Timings in session 6 are machine specific and will not match your classroom "
        "machines. Re-run before Wednesday.</p>"
        "<table><tr><th>File</th><th>Session</th></tr>"
        "<tr><td><code>sweep_report.py</code>, <code>gate_log.py</code></td>"
        "<td>1</td></tr>"
        "<tr><td><code>sweep_tools.py</code>, <code>sweep_report2.py</code>, "
        "<code>print_the_return.py</code>, <code>sweep_tools_more.py</code>, "
        "<code>sweep_report3.py</code>, <code>first_over_enumerate.py</code></td>"
        "<td>2</td></tr>"
        "<tr><td><code>accumulators.py</code>, <code>counter_tour.py</code>, "
        "<code>caesar_encode.py</code>, <code>letters.py</code>, "
        "<code>cipher_console_starter.py</code>, <code>cipher_console_step1.py</code>, "
        "<code>cipher_console_step2.py</code>, <code>cipher_console_step3.py</code>, "
        "<code>cipher_console.py</code>, "
        "<code>cipher_console_replay.py</code>, <code>verify_console.py</code></td>"
        "<td>3</td></tr>"
        "<tr><td><code>caesar_crack.py</code></td><td>Extra, after 3</td></tr>"
        "<tr><td><code>transposition.py</code></td><td>4</td></tr>"
        "<tr><td><code>avalanche.py</code></td><td>5</td></tr>"
        "<tr><td><code>what_it_costs.py</code></td><td>6</td></tr>"
        "<tr><td><code>smarter_than_brute.py</code></td><td>7</td></tr>"
        "<tr><td><code>monty_hall.py</code></td><td>8</td></tr>"
        "<tr><td><code>make_data.py</code>, <code>read_ledger.py</code>, <code>safe_count.py</code>, "
        "<code>benford.py</code>, <code>benford_histogram.py</code></td><td>9</td></tr>"
        "<tr><td><code>markov.py</code>, <code>corpus.txt</code></td><td>10</td></tr>"
        "<tr><td><code>sparks_parallel.py</code>, <code>plume.py</code>, "
        "<code>verify_plume.py</code></td><td>11</td></tr>"
        "<tr><td><code>orbit.py</code>, <code>verify_orbit.py</code>, "
        "<code>verify_orbit_band.py</code></td><td>12</td></tr>"
        "</table>"
    )

    b += (
        '<nav class="pager"><span class="none">&nbsp;</span>'
        '<a href="wed01_cold_read.html">Start with session 1 &rarr;</a></nav>\n'
    )
    return b
