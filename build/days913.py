"""Sessions 9 to 13."""

from build import code, masthead, output, pager, reveal
from days38 import exits
from stds import panel

CAPSTONE = (
    '<section class="panel" style="border-top-color:#8A5A00;background:#F7F2E6">'
    "<h2>Capstone thread</h2>"
    "<p>The capstone is a thread from here to 16 December, not a session. Before any "
    "code is written, one page on paper is required, and it is the same page for "
    "everyone:</p>"
    '<ul class="tight">'
    "<li>A sketch of the screen, drawn by hand, with the edges marked.</li>"
    "<li>What the player can do. Every key, every click.</li>"
    "<li>What is on screen that is not the player, and what happens when they touch.</li>"
    "<li>How score or state is kept, and where it is displayed.</li>"
    "<li>How it ends. Both ways: winning and losing.</li>"
    "<li>Then pseudocode, in English, before any Python.</li>"
    "</ul>"
    "<p>Sketches are due at the start of session 11, two weeks from today. No sketch means no build, which is "
    "not a punishment: it is the same rule every working programmer has learned the hard "
    "way.</p>"
    "<p>What you build on is fixed, so the sketch has something to stand on. In sessions "
    "12 and 13 you get two working programs with moving objects and gravity: a plume of "
    "particles, and a ship going round a planet. Your capstone is what you add to one of "
    "them, and the sketch page describes that addition. A fuel budget and a target orbit. "
    "A second planet. A vent that fires when a key is pressed and scores every particle "
    "that clears a line. Anything that gives the player something to do and a way to win "
    "or lose.</p>"
    "<h3>How it is judged</h3>"
    '<ul class="tight">'
    "<li>It runs, and the window closes only when you close it.</li>"
    "<li>At least one thing on screen answers a key or a click, and you can point at the "
    "line that does it.</li>"
    "<li>It can end, at least one way, and the ending prints to the terminal.</li>"
    "<li>Your sixty second demo names one bug you fixed and how you found it.</li>"
    "</ul>"
    "<p>Four items. Each is yes or no. Four yes is a finished capstone.</p>"
    "<h3>Where the time is</h3>"
    "<p>Session 10: bring questions about the sketch, and see your first window. Session "
    "11: sketch handed in at the start, and five minutes at the end where you say which "
    "program you are extending and what the first addition is. Session 12: the plume "
    "arrives, and the stretch exit is the first capstone addition. Session 13: the "
    "orbit arrives, the stretch exit is a fuel budget and a target, and the last 45 "
    "minutes are rehearsal and demo. There is no separate build session, so the "
    "addition has to be small enough to finish inside two stretch exits.</p>"
    "</section>\n"
)


def day09():
    """Session 9: Monte Carlo and Monty Hall."""
    b = masthead(
        "09",
        "Settling an argument by simulation",
        "Wednesday 18 November 2026",
        "There is a probability question that fooled a great many mathematicians in "
        "1990. You are not going to argue about it. You are going to run it a hundred "
        "thousand times and read the answer off the screen.",
    )
    b += (
        '<div class="flag"><b>No class on 11 November.</b> Veterans Day. Session 8 was '
        "two weeks ago, so the opener does more work than usual today.</div>"
    )
    b += '<h2><span class="num">1</span>Opener<span class="mins">10 minutes</span></h2>'
    b += (
        "<p>Two weeks back, hill climbing opened a seven digit lock in about 170 tries "
        "where brute force needed 4.7 million. On paper, two things: what information "
        "did <code>score</code> give the climber, and why did we insist on five runs "
        "rather than one?</p>"
    )
    b += reveal(
        "Both answers before you click.",
        "<p>The score said how many positions were right, which turns one bit per guess "
        "into seven. And five runs because a method that starts from a random place has "
        "a spread, not a single running time. Ours ran from 50 to 238.</p>"
        "<p>Hold on to the word spread. Today it is the entire lesson.</p>",
    )

    b += '<h2><span class="num">2</span>The problem<span class="mins">15 minutes</span></h2>'
    b += (
        "<p>Three doors. One prize. You pick a door. The host, who knows where the prize "
        "is, opens a different door that does not have the prize behind it. You may keep "
        "your door or switch to the remaining one.</p>"
        "<p>Vote as a room, out loud, before any code. Write the vote count on the "
        "board. You will come back to it.</p>"
    )
    b += (
        '<div class="predict"><b>State a model first.</b> Write down the probability you '
        "think staying wins, and the probability switching wins. Two numbers between 0 "
        "and 1. They should add to 1. Everyone commits in writing before the program "
        "runs.</div>"
    )

    b += '<h2><span class="num">3</span>One game, in code<span class="mins">20 minutes</span></h2>'
    b += code(
        '''def one_game(switch):
    """Play one game. Return 1 for a win, 0 for a loss."""
    prize = random.randrange(3)
    pick = random.randrange(3)

    opened = -1
    for door in range(3):
        if door != prize:
            if door != pick:
                opened = door

    if switch:
        for door in range(3):
            if door != pick:
                if door != opened:
                    pick = door

    if pick == prize:
        return 1
    return 0''',
        "monty_hall.py, first draft",
    )
    b += reveal(
        "Why does the host's loop need both gates, and what happens when your first "
        "pick is already the prize?",
        "<p>The host may not open the prize door and may not open your door, so both "
        "gates are doing real work. When your pick is the prize, two doors qualify and "
        "the loop keeps the later one. That is fine, because a real host could open "
        "either.</p>"
        "<p>Read the switch block too. It looks reasonable. Hold your opinion of it "
        "until section 5.</p>",
    )

    b += '<h2><span class="num">4</span>Run it until it settles<span class="mins">20 minutes</span></h2>'
    b += reveal(
        "A hundred games, switching. How many wins?",
        output("one hundred games, switching:\n  55 wins out of 100")
        + "<p>55 out of 100. If switching really wins two thirds of the time you would "
        "expect about 67, so either the model is wrong or a hundred games is too few. "
        "Run more. Same seed both ways, so both columns play identical games.</p>"
        + output(
            """does it settle down?
  trials    stay wins    stay rate    switch wins    switch rate
  10        4            0.4000       5              0.5000
  100       33           0.3300       55             0.5500
  1000      327          0.3270       526            0.5260
  10000     3378         0.3378       5537           0.5537
  100000    33318        0.3332       55402          0.5540""",
            "output from the broken version",
        )
        + "<p>Read the last row. Staying settles on 0.3332, which is one third. "
        "Switching settles on 0.5540, which is not two thirds and not one half. It is "
        "not anything. A number that converges cleanly onto nothing recognisable is the "
        "signature of a bug, not of a surprising truth.</p>",
    )
    b += (
        '<div class="bug"><b>This is the session\'s bug hunt.</b> The program above is '
        "the broken one. It has no traceback, it never crashes, and it produces a stable "
        "wrong answer with five digits of apparent precision. Your model says switching "
        "wins two thirds of the time, or 0.6667. The program says 0.5540. One of them is "
        "wrong and you have to find out which.</div>"
    )

    b += '<h2><span class="num">5</span>Find it<span class="mins">15 minutes</span></h2>'
    b += (
        "<p>The broken switch block is four lines and looks reasonable:</p>"
    )
    b += code(
        """    if switch:
        for door in range(3):
            if door != pick:
                if door != opened:
                    pick = door"""
    )
    b += reveal(
        "Trace it by hand with prize 0, pick 1, opened 2. Follow <code>pick</code> "
        "through all three passes of the loop.",
        "<p>Pass door=0: 0 is not 1 and 0 is not 2, so <code>pick</code> becomes 0. "
        "Correct so far. Pass door=1: the test is now <code>1 != pick</code>, and "
        "<code>pick</code> is 0, so it passes, and 1 is not 2, so <code>pick</code> "
        "becomes 1 again. Pass door=2: blocked by <code>opened</code>. Final "
        "<code>pick</code> is 1, the door you started on. It never switched.</p>"
        "<p>The loop writes to the variable it is testing. Fix it by working out the "
        "target first and assigning once, after the loop.</p>"
        + code(
            """    if switch:
        target = pick
        for door in range(3):
            if door != pick:
                if door != opened:
                    target = door
        pick = target"""
        )
        + output(
            """one hundred games, switching:
  67 wins out of 100

  trials    stay wins    stay rate    switch wins    switch rate
  10        4            0.4000       6              0.6000
  100       33           0.3300       67             0.6700
  1000      327          0.3270       673            0.6730
  10000     3378         0.3378       6622           0.6622
  100000    33318        0.3332       66682          0.6668

the model says stay 1/3 and switch 2/3:
  1/3 = 0.3333
  2/3 = 0.6667""",
            "verified output, fixed version",
        )
        + "<p>0.3332 and 0.6668, against 0.3333 and 0.6667. Now the two columns add to "
        "exactly 100000, because with the same seed every game that staying lost, "
        "switching won.</p>"
        "<p>Look at the 10-trial row: 0.4 and 0.6. Ten games tells you nothing. The "
        "answer only appears as the trials pile up, and the model and the measurement "
        "only agree in the last row.</p>",
    )
    b += CAPSTONE
    b += exits(
        "You committed a written model, ran a hundred games, and can explain why the "
        "host is not allowed to open your door or the prize door.",
        "Floor, plus the convergence table out to 10000 trials, plus you found the "
        "switch bug by tracing rather than by being told.",
        "Middle, plus run it with four doors and then five, work out the switching "
        "probability for each, and state the general rule. Then explain why it converges "
        "to two thirds with three doors but the advantage shrinks as doors are added.",
    )
    b += panel(
        ["7.SP.C.6", "7.SP.C.7", "7.SP.C.5"],
        "<p>10 opener, 15 the problem and the vote, 20 reading the code, 20 running and "
        "the table, 15 the bug hunt, 10 capstone brief. That is 90 with no slack. If "
        "section 3 runs long, take the minutes from section 4 by running the table on "
        "the projector once rather than on every machine. The written model has to "
        "happen before any code runs or the session loses its spine, and the capstone "
        "brief has to be read aloud, because the sketch is due in two weeks and next week "
        "is the light attendance day.</p>",
        "<p>Some of the room will refuse the two thirds answer even after the "
        "simulation. That is the correct historical reaction and you should say so. Do "
        "not argue them into it. Have them run 100000 trials themselves.</p>"
        "<p>The bug is the most valuable thing here and it is tempting to skip it for "
        "time. Do not. A silent bug that produces a stable, plausible, wrong number is "
        "exactly what they will hit in their capstones, and 0.5540 is a much better "
        "teacher than any traceback.</p>"
        "<p>Standard <span class=\"std\">7.SP.C.7</span> asks students to explain "
        "sources of discrepancy when a model and the observed frequencies disagree. "
        "This session is that standard almost word for word, with the discrepancy "
        "supplied by a real bug.</p>",
        retouch=(
            "Session 8's five-runs-not-one discipline and the idea of a spread. Also "
            "session 8's fixed seed, which becomes load-bearing here: the same seed is "
            "what makes the stay and switch columns comparable."
        ),
        extras=(
            "<h3>Files</h3><p><code>monty_hall.py</code>, seeded with 1963. Both the "
            "broken and fixed figures on this page were produced by running it, and are "
            "reproducible with that seed.</p>"
            "<h3>Lifted this week</h3><p><code>random.seed</code> for reproducibility, "
            "<code>random.randrange</code>, booleans as function arguments.</p>"
        ),
    )
    b += pager(
        ("wed08_heuristics.html", "Session 8: smarter than brute force"),
        ("wed10_benford.html", "Session 10: the first digit"),
    )
    return b


def day10():
    """Session 10: Benford's law on real data."""
    b = masthead(
        "10",
        "The first digit tells on you",
        "Wednesday 25 November 2026",
        "Numbers that grow on their own start with 1 about thirty percent of the time "
        "and with 9 about five percent. Numbers people invent do not. Today you read two "
        "files and work out which one was made up.",
    )
    b += (
        '<div class="flag"><b>Day before Thanksgiving.</b> Attendance is usually light. '
        "This session is self-contained on purpose: nothing later in the term depends on "
        "it, so anyone away can pick it up from this page alone. Capstone sketches are "
        "due next week, not today, so nobody away loses a deadline. If you are here and "
        "have a question about the sketch, ask it after the histogram: this is the first "
        "window you have seen, and the sketch describes a window.</div>"
    )
    b += '<h2><span class="num">1</span>Opener<span class="mins">10 minutes</span></h2>'
    b += (
        "<p>Write down a list of ten amounts of money, as if you were filling in an "
        "expenses form and inventing the numbers. Anything from 100 to 9999. Do it "
        "quickly and do not think about it.</p>"
        "<p>Now circle the first digit of each one. As a room, tally how many 1s, how "
        "many 2s, and so on up to 9. Put the tally on the board and leave it there.</p>"
    )

    b += '<h2><span class="num">2</span>Two files<span class="mins">20 minutes</span></h2>'
    b += (
        "<p>Both files hold 600 amounts in a column called <code>amount</code>. One was "
        "built from Fibonacci numbers and powers of two, which are quantities that grow "
        "by multiplying. The other is 600 numbers picked at random between 100 and 9999, "
        "which is what invented figures look like.</p>"
        "<p>Read each file, pull the first digit off each amount, and tally.</p>"
    )
    b += code(
        '''import csv
import math
from collections import Counter


def leading_digit(text):
    """Return the first digit character in text as an integer."""
    for ch in text:
        if ch in "123456789":
            return int(ch)
    return 0


def tally_file(filename):
    """Return a Counter of leading digits in the amount column."""
    counts = Counter()
    with open(filename, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            counts[leading_digit(row["amount"])] += 1
    return counts


def benford_expected(digit):
    """Return the share of numbers Benford's law predicts start with digit."""
    return math.log10(1 + 1 / digit)''',
        "benford.py",
    )
    b += (
        "<p>One function in there is probably new. <code>math.log10</code> asks: what power do I raise 10 to, to get this number? <code>log10(100)</code> is 2, because "
        "10 squared is 100. <code>log10(2)</code> is about 0.301, because 10 to the "
        "0.301 is 2. You do not need more than that today, and the calculator does "
        "the work.</p>"
        "<p>Why a logarithm turns up in a rule about first digits is a fair question "
        "and the honest short answer is that quantities which grow by multiplying "
        "spend equal stretches of time in each power of ten, and the gap from 1 to 2 "
        "is a longer stretch than the gap from 9 to 10.</p>"
    )
    b += reveal(
        "<code>benford_expected(1)</code> and <code>benford_expected(9)</code>. Work "
        "both out on a calculator before you click.",
        "<p>log of 2, which is 0.301, and log of one and a ninth, which is 0.046. So 1 "
        "should lead about thirty percent of the time and 9 about five percent: roughly "
        "six times as often.</p>"
        "<p>Check that the nine shares add to 1. They do, exactly, because the logs "
        "telescope: each term is log of (d+1) minus log of d, and the whole sum "
        "collapses to log 10 minus log 1.</p>",
    )

    b += '<h2><span class="num">3</span>Which one was invented<span class="mins">30 minutes</span></h2>'
    b += reveal(
        "Predict the largest gap from Benford for each file. Two numbers.",
        output(
            """honest_ledger.csv
  digit   count    actual   benford predicts
      1     182     0.303             0.301
      2     106     0.177             0.176
      3      75     0.125             0.125
      4      56     0.093             0.097
      5      49     0.082             0.079
      6      39     0.065             0.067
      7      34     0.057             0.058
      8      32     0.053             0.051
      9      27     0.045             0.046
  largest gap from Benford: 0.004

cooked_ledger.csv
  digit   count    actual   benford predicts
      1      60     0.100             0.301
      2      67     0.112             0.176
      3      54     0.090             0.125
      4      73     0.122             0.097
      5      74     0.123             0.079
      6      82     0.137             0.067
      7      71     0.118             0.058
      8      52     0.087             0.051
      9      67     0.112             0.046
  largest gap from Benford: 0.201"""
        )
        + "<p>0.004 against 0.201. The grown numbers track Benford to within half a "
        "percentage point on every digit. The invented numbers sit near 0.11 everywhere, "
        "because a random pick between 100 and 9999 treats every leading digit alike.</p>"
        "<p>Go back to the tally on the board from the opener. Compare it to the second "
        "table. It usually looks a lot like the cooked file, which is the point: you "
        "invent numbers the same way the generator does.</p>",
    )

    b += '<h2><span class="num">4</span>Draw it<span class="mins">25 minutes</span></h2>'
    b += (
        "<p>A table of nine numbers is hard to judge by eye. A histogram is not. Draw "
        "nine bars with <code>pygame.draw.rect</code>, one per digit, height "
        "proportional to the count, and draw the Benford expectation as a line across "
        "the top of where each bar should reach.</p>"
    )
    b += (
        "<p>This is the first window in the course, so the whole program is here, and "
        "the shape of its loop is the shape every window in this course will have. Read "
        "the loop before the drawing.</p>"
    )
    b += code(
        '''import pygame

FILENAME = "honest_ledger.csv"

WIDTH = 800
HEIGHT = 600
BLACK = (14, 36, 48)
TEAL = (14, 107, 98)
AMBER = (232, 150, 60)

counts = tally_file(FILENAME)
total = sum(counts.values())
print(f"{FILENAME}: {total} amounts tallied, window open, close it to finish")

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
    screen.fill(BLACK)
    for d in range(1, 10):
        share = counts[d] / total
        height = int(share * 900)
        x = 60 + (d - 1) * 80
        pygame.draw.rect(screen, TEAL, (x, 520 - height, 54, height))
        expected = int(benford_expected(d) * 900)
        pygame.draw.line(screen, AMBER, (x, 520 - expected), (x + 54, 520 - expected), 3)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()''',
        "benford_histogram.py, after the same three functions as benford.py",
    )
    b += reveal(
        "The loop runs sixty times a second and draws the same nine bars every time. "
        "What happens if you take the <code>for event</code> loop out?",
        "<p>The window stops answering. Nothing reads the close button, so the program "
        "never learns you clicked it, and you have to kill it from the terminal. That "
        "loop is not decoration. It is how the window listens.</p>"
        "<p>Four things in this loop will be in every window you write this term: "
        "<code>while running:</code>, the <code>event.get()</code> loop with its QUIT "
        "check, <code>display.flip()</code>, and <code>clock.tick(60)</code>. A window "
        "never closes itself. You close it.</p>",
    )
    b += (
        "<p>One more rule starts here and holds for the rest of the course: words go in "
        "the terminal, visuals go in the window. Never draw text into the window. Change "
        "<code>FILENAME</code>, run again, and put the two windows side by side. The "
        "honest one has its bars touching the amber lines. The cooked one does not.</p>"
    )
    b += exits(
        "You tallied the room's invented numbers and ran the program on both files, and "
        "can say which file was made up and how you know.",
        "Floor, plus you computed the Benford shares yourself and checked they sum to 1, "
        "plus a working histogram of one file.",
        "Middle, plus both histograms with the expectation line drawn, plus tally the "
        "room's own invented numbers from the opener into a third CSV and test it. Then "
        "answer honestly: does one class's worth of numbers give you enough to conclude "
        "anything?",
    )
    b += panel(
        ["6.SP.B.4", "7.SP.A.1", "MP4"],
        "<p>10 opener, 20 the two files, 30 the comparison, 25 the histogram, 5 exits. "
        "With light attendance, run the histogram as a whole-room build on the projector "
        "rather than individually. Have <code>benford_histogram.py</code> on the "
        "machines: the point of the section is reading the loop, not typing it.</p>",
        "<p>Be careful with the fraud framing. Benford is a reason to look harder, not "
        "proof of anything, and a great many honest datasets fail it: anything with a "
        "fixed range, anything assigned rather than grown, anything in a narrow band. "
        "Ask them for a list of honest data that would fail, and expect good answers "
        "like shoe sizes and house numbers.</p>"
        "<p>The stretch question about the class's own numbers is the real statistics "
        "lesson. Thirty invented numbers from ten students is a small and unrepresentative "
        "sample, and <span class=\"std\">7.SP.A.1</span> is exactly about that.</p>"
        "<p>Watch for students reading <code>counts[leading_digit(...)] += 1</code> and "
        "asking why it does not raise <code>KeyError</code> the way session 3's plain "
        "dictionary did. Good question. A Counter supplies the zero.</p>",
        retouch=(
            "Session 3's Counter and the KeyError rule, and session 4's file reading "
            "with a dirty column. Also session 9's habit of writing the model down "
            "before measuring anything."
        ),
        extras=(
            "<h3>Files</h3><p><code>make_data.py</code> builds "
            "<code>honest_ledger.csv</code> and <code>cooked_ledger.csv</code>, seeded "
            "with 20261125. <code>benford.py</code> prints the tables and "
            "<code>benford_histogram.py</code> draws one file, chosen by the "
            "<code>FILENAME</code> line at the top. Put all four on the machines "
            "beforehand. All figures verified on Python 3.12.3; the histogram was run "
            "headless on both CSVs with pygame 2.6.1.</p>"
            "<h3>Honesty note for the room</h3><p>The cooked file was generated by "
            "<code>random.randint(100, 9999)</code>, not taken from a real fraud case. "
            "Say so. It stands in for invented figures, and the comparison is real even "
            "though the crime is not.</p>"
        ),
    )
    b += pager(
        ("wed09_monte_carlo.html", "Session 9: settling it by simulation"),
        ("wed11_markov.html", "Session 11: machines that write"),
    )
    return b


def day11():
    """Session 11: Markov chains and the LLM conversation."""
    b = masthead(
        "11",
        "Machines that write, and what they are actually doing",
        "Wednesday 2 December 2026",
        "You are going to build the thing that makes a chatbot feel like magic, out of a "
        "list, a loop, and a dictionary. It takes about forty lines. Once you have built "
        "it, it will not feel like magic any more, and that is the point of the session.",
    )
    b += '<h2><span class="num">1</span>Opener<span class="mins">10 minutes</span></h2>'
    b += (
        "<p>Last week the first digit told you which ledger was invented. On paper: what "
        "share of grown numbers start with 1, and why does a random pick between 100 and "
        "9999 not match it?</p>"
    )
    b += reveal(
        "Both answers first.",
        "<p>About 0.301. And a uniform pick gives every leading digit roughly the same "
        "share, near 0.11, because nothing in the process favours small leading digits "
        "the way repeated multiplying does.</p>",
    )

    b += '<h2><span class="num">2</span>The table<span class="mins">30 minutes</span></h2>'
    b += (
        "<p>Read a text file. Walk through it a word at a time. For every pair of "
        "consecutive words, record which word came next. That record is the whole "
        "model.</p>"
    )
    b += code(
        '''def build_model(words):
    """Return a table mapping each word pair to the words that followed it."""
    model = defaultdict(list)
    for i in range(len(words) - 2):
        pair = (words[i], words[i + 1])
        model[pair].append(words[i + 2])
    return model''',
        "markov.py",
    )
    b += reveal(
        "The corpus is a short passage about how these models work. In it, the pair "
        "<code>(\"the\", \"machine\")</code> appears eleven times. What do you expect the "
        "table to hold for that key?",
        output(
            """corpus words: 340
distinct pairs: 250

what followed ('the', 'machine'):
  ['counts', 'does', 'is', 'knows', 'picks', 'reads', 'was']"""
        )
        + "<p>Seven different words, each one recorded because it actually followed "
        "those two words somewhere in the text. The list on the page is the set, with "
        "repeats removed. The table itself holds all eleven: <code>does</code>, "
        "<code>is</code>, <code>knows</code>, and <code>was</code> twice each, and "
        "the other three once. Nothing in that list is a guess and nothing in it is "
        "understood. It is a record of what happened.</p>"
        "<p>340 words produced 250 distinct pairs. Most pairs occur once, which is why "
        "a small corpus generates text that quotes itself in long stretches.</p>",
    )
    b += (
        "<p><code>defaultdict(list)</code> hands you an empty list for a key you have "
        "not seen, so <code>.append</code> works the first time. Compare that to session "
        "3, where a plain dictionary raised <code>KeyError</code> and you had to check "
        "first.</p>"
    )

    b += '<h2><span class="num">3</span>Let it write<span class="mins">25 minutes</span></h2>'
    b += code(
        '''def generate(model, seed_pair, length):
    """Return a sentence of the given length, starting from seed_pair."""
    first, second = seed_pair
    out = [first, second]
    for step in range(length):
        options = model[(first, second)]
        if len(options) == 0:
            return " ".join(out)
        nxt = random.choice(options)
        out.append(nxt)
        first, second = second, nxt
    return " ".join(out)'''
    )
    b += reveal(
        "Starting from <code>(\"the\", \"machine\")</code>, twenty two words. Will the "
        "output be grammatical? Will it make sense? Those are two separate questions.",
        output(
            """1. the machine reads a great deal of text. the machine is often followed by the word machine, and that the word not. you are

2. the machine knows which word followed which other word. then the machine reads a great deal of text. the machine does not know what

3. the machine picks a word, looks at what followed that word before, and picks one of those. it does this again, and again, until

4. the machine is broken. neither reader is right, because the machine knows which word followed which other word. then the machine was doing the"""
        )
        + "<p>Mostly grammatical, because every three word window came from real text. "
        "Sentence 3 reads almost perfectly. Sentence 1 falls apart at "
        "<code>the word not. you are</code>, because the chain walked into a pair that "
        "only occurred once and had nowhere sensible to go.</p>"
        "<p>Now the question worth the whole session: which of those four sentences did "
        "the program understand? None. It looked up two words and picked from a list. "
        "That is the entire mechanism.</p>",
    )

    b += '<h2><span class="num">4</span>The honest conversation<span class="mins">20 minutes</span></h2>'
    b += (
        "<p>The programs that write text for people are built on a much bigger version "
        "of what you just wrote. The differences are real and worth naming plainly:</p>"
        '<ul class="tight">'
        "<li>They look back over hundreds or thousands of words, not two.</li>"
        "<li>They do not store a list per pair. They learn a function that scores every "
        "possible next word, so they can respond to word sequences they never saw.</li>"
        "<li>They are trained on an enormous amount of text, then adjusted further using "
        "human feedback about which answers are wanted.</li>"
        "</ul>"
        "<p>What does not change is the shape: look at what came before, produce a "
        "distribution over what might come next, pick from it. When one of those systems "
        "produces something confident and wrong, this is why. Nothing in the mechanism "
        "checks the world. It checks what usually follows.</p>"
        '<div class="predict"><b>Your model is a probability model.</b> Seven options '
        "for <code>(\"the\", \"machine\")</code> does not mean one in seven each. The "
        "table holds eleven entries, so <code>does</code> gets two chances in eleven "
        "and <code>reads</code> gets one. Session 9 had you write a model down and then "
        "test it against what actually happened. Do the same here: pick a pair, predict "
        "the share for each option, generate 200 continuations, and count.</div>"
    )
    b += exits(
        "The table builds and you can read off what followed a pair you choose.",
        "Floor, plus generation running on the supplied corpus, plus you can explain what "
        "<code>defaultdict</code> saves you compared with session 3.",
        "Middle, plus swap in your own corpus, at least 2000 words, and compare the "
        "output quality. Then change the pair to a single word and to three words, and "
        "report what happens at each: one word wanders badly, three words quotes the "
        "source almost verbatim. Explain why.",
    )
    b += panel(
        ["7.SP.C.7", "7.SP.C.6", "MP4"],
        "<p>10 opener, 30 building the table, 25 generation, 20 the conversation, 5 "
        "exits and the capstone checkpoint. The conversation in section 4 is the reason "
        "this session is in the course. Protect the time for it.</p>"
        "<h3>Capstone checkpoint</h3><p>Sketches are collected at the start of today, "
        "not last week: the light attendance day and the first window both come before "
        "the deadline on purpose. Read each one for the four checks before section 2. "
        "In the last five minutes, each student says in one sentence which program they "
        "are extending, the plume or the orbit, and what the first addition is. Write "
        "the answers down. A student with no answer gets one assigned: a key that "
        "fires the vent.</p>",
        "<p>Students will want a bigger corpus immediately, and they are right that it "
        "helps. Have a 2000 word text file ready. Write it yourself or use something "
        "clearly out of copyright, and do not let them paste in a book they do not have "
        "the right to use.</p>"
        "<p>The three word window is the best stretch result: it produces text that is "
        "almost exactly the original, which shows memorisation and generalisation "
        "trading off. That conversation transfers directly to the real systems.</p>"
        "<p>One code note. <code>model[(first, second)]</code> on a "
        "<code>defaultdict</code> silently inserts an empty list for a missing key, so "
        "generating quietly grows the model. Harmless here, worth pointing at, and a "
        "good stretch fix using <code>.get</code> instead.</p>",
        retouch=(
            "Session 3's dictionary and KeyError, now solved a second way with "
            "<code>defaultdict</code>. Session 9's discipline of stating a probability "
            "model and then measuring against it."
        ),
        extras=(
            "<h3>Files</h3><p><code>markov.py</code> and <code>corpus.txt</code>, "
            "seeded with 20261202. The four sentences above came from running it and are "
            "reproducible with that seed. The corpus was written for this lesson, so "
            "there is no copyright question.</p>"
            "<h3>Lifted this week</h3><p><code>collections.defaultdict</code>, tuples as "
            "dictionary keys, <code>.split()</code>, <code>\" \".join()</code>, "
            "multiple assignment.</p>"
        ),
    )
    b += pager(
        ("wed10_benford.html", "Session 10: the first digit"),
        ("wed12_classes.html", "Session 12: objects that remember"),
    )
    return b


def day12():
    """Session 12: classes and particles."""
    b = masthead(
        "12",
        "Objects that remember their own history",
        "Wednesday 9 December 2026",
        "Tracking four moving sparks takes five lists kept in step by hand, and the "
        "lists are held together by nothing but your attention. Today each spark is one "
        "object that carries its own position, its own speed, and its own trail.",
    )
    b += '<h2><span class="num">1</span>Opener<span class="mins">10 minutes</span></h2>'
    b += (
        "<p>Session 3 showed two lists kept in step to count letters. Here are five, "
        "tracking four sparks that are being pulled downward one frame at a time.</p>"
    )
    b += code(
        """xs = [100, 100, 100, 100]
ys = [500, 500, 500, 500]
dxs = [2, -1, 3, 0]
dys = [-6, -5, -7, -4]
colors = ["gold", "orange", "red", "gold"]""",
        "sparks_parallel.py",
    )
    b += (
        "<p>Spark 1 lands, so it has to come out of every list. Someone removes it from "
        "four of them and misses the fifth.</p>"
    )
    b += code(
        """xs.pop(1)
ys.pop(1)
dxs.pop(1)
dys.pop(1)
# colors.pop(1) is missing on purpose"""
    )
    b += reveal(
        "Before the removal, spark 2 was red. What colour is it afterwards, and what "
        "else is now wrong?",
        output(
            """frame 2
  spark 0: x=106 y=488 dy=-3 gold
  spark 1: x=97 y=491 dy=-2 orange
  spark 2: x=109 y=485 dy=-4 red
  spark 3: x=100 y=494 dy=-1 gold

now remove spark 1, which has landed
after removing from four lists but forgetting the fifth:
  spark 0: x=106 y=488 gold
  spark 1: x=109 y=485 orange
  spark 2: x=100 y=494 red"""
        )
        + "<p>The spark that was at x=109 was red and is now orange. Every colour after "
        "the removal point is off by one, and the program does not complain, because "
        "nothing in it knows those five lists were ever related.</p>"
        "<p>There is a second problem that is worse. You cannot hand one spark to a "
        "function. You have to hand over five lists and an index, and hope the caller "
        "keeps them together.</p>",
    )

    b += '<h2><span class="num">2</span>One spark, one object<span class="mins">30 minutes</span></h2>'
    b += (
        "<p>One line in the class below needs explaining first. A spark is launched "
        "with a speed and an angle, but the program has to move it in two separate "
        "directions each frame: some amount across, and some amount up. Splitting one "
        "speed-and-angle into those two amounts is what <code>cos</code> and "
        "<code>sin</code> do.</p>"
        "<p>Speed 10 at 60 degrees gives 5.0 across and 8.66 up. You can check those "
        "two numbers are right without knowing any trigonometry: 5.0 squared plus "
        "8.66 squared is 100, and the speed squared is also 100. The across-amount "
        "and the up-amount always fit the original speed exactly.</p>"
        "<p><code>math.radians</code> is a unit change, nothing more. Python's "
        "<code>cos</code> and <code>sin</code> want radians and you are thinking in "
        "degrees, so you convert. Treat all three as tools you are handed today.</p>"
    )
    b += code(
        '''class Particle:
    """One thrown speck that keeps a trail of where it has been."""

    def __init__(self, x, y, speed, angle):
        self.x = x
        self.y = y
        self.dx = speed * math.cos(math.radians(angle))
        self.dy = -speed * math.sin(math.radians(angle))
        self.trail = [(x, y)]
        self.alive = 1

    def step(self):
        """Move one frame forward and record the new position."""
        self.dy = self.dy + GRAVITY
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.trail.append((self.x, self.y))
        if self.y > HEIGHT - 40:
            self.alive = 0''',
        "plume.py",
    )
    b += reveal(
        "Why is there a minus sign on <code>self.dy</code> in <code>__init__</code> but "
        "a plus on <code>GRAVITY</code> in <code>step</code>?",
        "<p>Because the screen's y axis points down. <code>dy</code> is how much "
        "<code>y</code> changes each frame, so a positive <code>dy</code> moves the "
        "particle down the screen and a negative <code>dy</code> moves it up. An angle "
        "of 90 degrees means straight up, which on screen means y decreasing, so the "
        "initial dy has to be negative. Gravity pulls down the screen, which is y "
        "increasing, so it adds.</p>"
        "<p>This is the coordinate system from session 5's grid, with one axis flipped "
        "relative to the one you use in maths class. Say that out loud every time it "
        "comes up, because it never stops causing bugs.</p>",
    )
    b += (
        "<p><code>self</code> is the particular spark this call is about. "
        "<code>self.x</code> is that spark's own x, not shared with any other. That one "
        "idea replaces all five lists and the comment.</p>"
    )

    b += '<h2><span class="num">3</span>A list of objects<span class="mins">25 minutes</span></h2>'
    b += code(
        """running = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
    screen.fill(BLACK)
    pygame.draw.rect(screen, (90, 108, 116), (0, HEIGHT - 40, WIDTH, 40))
    for p in particles:
        if p.alive == 1:
            p.step()
        p.draw(screen)
    pygame.display.flip()
    clock.tick(60)"""
    )
    b += reveal(
        "120 particles launched from the vent at speeds 6 to 11 and angles 60 to 120 "
        "degrees. After 240 frames, how many are still in the air, and how high did the "
        "highest one get?",
        output(
            """frames run: 241
particles: 120, still airborne: 0, landed: 120
highest point reached: y=64.2 (ground is y=560)
trail lengths: shortest 92, longest 183""",
            "verified from a headless run",
        )
        + "<p>All 120 have landed within four seconds. The highest reached y=64.2, which "
        "is near the top of an 800 by 600 window, about 500 pixels above the vent.</p>"
        "<p>The trail lengths are the useful number: 92 frames for the shortest flight "
        "and 183 for the longest, which is exactly what a spread of launch speeds and "
        "angles should produce. Every one of those trails lives inside its own object, "
        "and no list is keeping them in step.</p>",
    )
    b += (
        "<p>The loop has the same shape as the histogram in session 10: "
        "<code>while running:</code>, the QUIT listener, <code>clock.tick(60)</code>, "
        "and a window that never closes itself. Objects changed what is in the loop, not "
        "the loop.</p>"
    )
    b += exits(
        "You can say what went wrong in the opener, and a <code>Particle</code> class "
        "exists with <code>__init__</code> and <code>step</code>, and one particle "
        "moves and falls on screen.",
        "Floor, plus a list of 120 particles all stepping in one loop, plus trails "
        "drawn, plus you can explain the minus sign on the initial dy.",
        "Middle, plus colour each particle by its current vertical speed so the rising "
        "ones differ from the falling ones. Then add the shock canopy: make the trail "
        "brighter near the top of the arc, where dy passes through zero.",
    )
    b += panel(
        ["6.NS.C.8", "5.G.A.1", "6.EE.A.2"],
        "<p>10 opener, 30 the class, 25 the list of objects, 20 colour and exits. "
        "Typing a class from scratch takes longer than you expect. Have the file on the "
        "machines and read it before extending it.</p>"
        "<h3>Capstone checkpoint</h3><p>Students extending the plume start their "
        "addition in the stretch exit today. Check each one against the first rubric "
        "line before they leave: it runs, and the window closes only when they close "
        "it. Students extending the orbit do the stretch exit as written and start "
        "next week.</p>",
        "<p>The predictable error is forgetting <code>self</code> on an attribute inside "
        "a method, which gives <code>NameError</code> rather than anything helpful. "
        "Second is writing <code>def step(self)</code> and then calling "
        "<code>step(p)</code> instead of <code>p.step()</code>.</p>"
        "<p>Keep <code>pygame.font</code> out of it. Words in the terminal, visuals in "
        "the window, the rule set in session 10. If they want a readout, print it.</p>"
        "<p>If the room needs a gentler first class, write a two-attribute one on the "
        "board first: a <code>Pet</code> with a name and a hunger level, one method "
        "that feeds it. Five minutes, then come back to the particle.</p>",
        retouch=(
            "The parallel list problem from session 3, now solved properly. Also "
            "session 5's row and column coordinates, reappearing as screen coordinates "
            "with the y axis flipped."
        ),
        extras=(
            "<h3>Files</h3><p><code>sparks_parallel.py</code> for the opener, then "
            "<code>plume.py</code>, seeded with 20261209. Verified "
            "headless with <code>SDL_VIDEODRIVER=dummy</code> over 240 frames on pygame "
            "2.6.1. Confirm pygame is installed on the classroom machines before this "
            "session.</p>"
            "<h3>Lifted this week</h3><p><code>class</code>, <code>__init__</code>, "
            "<code>self</code>, methods, a list of objects, "
            "<code>pygame.draw.lines</code>.</p>"
        ),
    )
    b += pager(
        ("wed11_markov.html", "Session 11: machines that write"),
        ("wed13_orbits_demo.html", "Session 13: orbits, then the demo"),
    )
    return b


def day13():
    """Session 13: orbits and the parent demo."""
    b = masthead(
        "13",
        "Orbits, then the demo",
        "Wednesday 16 December 2026",
        "Gravity is one line of arithmetic applied over and over. A ship that only ever "
        "falls toward a planet, and never stops falling, is in orbit. Then the room fills "
        "with parents and you show them what you built.",
    )
    b += '<h2><span class="num">1</span>Opener<span class="mins">10 minutes</span></h2>'
    b += (
        "<p>Last week gravity was <code>self.dy = self.dy + GRAVITY</code>, always "
        "straight down. Today it points at a planet that can be anywhere. On paper: if "
        "the planet is at (400, 300) and the ship is at (400, 120), which way does "
        "gravity point, and how do you compute the distance?</p>"
    )
    b += reveal(
        "Both, before you click.",
        "<p>Straight down the screen, because the ship is directly above the planet, "
        "and the distance is 180.</p>"
        "<p>The general rule, in case you have not met it: if two points are "
        "<code>a</code> apart across and <code>b</code> apart up, the straight-line "
        "distance between them is the square root of <code>a</code> squared plus "
        "<code>b</code> squared. That is the Pythagorean theorem, and it is the only "
        "piece of geometry this session needs. Here the across gap is 0, so it "
        "collapses to 300 minus 120.</p>"
        "<p>With gaps of 100 across and 80 up it does not collapse: the distance is "
        "the square root of 10000 plus 6400, which is about 128.</p>"
        "<p>When the ship is off to one side, both differences matter and you need the "
        "full calculation.</p>",
    )

    b += '<h2><span class="num">2</span>Falling sideways<span class="mins">30 minutes</span></h2>'
    b += code(
        '''    def distance(self):
        """Return the distance from this ship to the planet centre."""
        gap_x = PLANET_X - self.x
        gap_y = PLANET_Y - self.y
        return math.sqrt(gap_x * gap_x + gap_y * gap_y)

    def step(self):
        """Apply one time slice of gravity, then move."""
        gap_x = PLANET_X - self.x
        gap_y = PLANET_Y - self.y
        r = self.distance()
        pull = PULL / (r * r)
        self.dx = self.dx + pull * (gap_x / r) * DT
        self.dy = self.dy + pull * (gap_y / r) * DT
        self.x = self.x + self.dx * DT
        self.y = self.y + self.dy * DT
        self.trail.append((self.x, self.y))''',
        "orbit.py",
    )
    b += (
        "<p>Three things are happening. <code>PULL / (r * r)</code> makes gravity weaker "
        "further out. <code>gap_x / r</code> and <code>gap_y / r</code> split that pull "
        "into its across and down parts, in proportion to how much of the gap lies along "
        "each axis. And <code>DT</code> is how big a slice of time each frame stands "
        "for.</p>"
    )
    b += reveal(
        "The ship starts at (400, 120) with <code>dx = 3.8</code> and "
        "<code>dy = 0</code>, so it is moving sideways at 180 pixels out. Does it fall "
        "into the planet, fly away, or go round?",
        output(
            """frames: 1201, trail points: 1202
closest approach 60.1 px, farthest 180.0 px
start distance 180.0 px, end distance 131.5 px
final speed 5.94 px per step
distance at a few frames:
  frame    0:  180.0 px
  frame   50:  141.2 px
  frame  100:   63.9 px
  frame  200:  178.5 px
  frame  400:  174.6 px
  frame  800:  159.3 px
  frame 1200:  133.2 px""",
            "verified from a headless run",
        )
        + "<p>Round. The distance falls from 180 to about 60, climbs back to 178, and "
        "keeps cycling for all 1200 frames, which is twenty seconds at sixty frames a "
        "second. The planet's radius is 26, so a closest approach of 60 clears it.</p>"
        "<p>The ship is falling the whole time. It never stops falling. It keeps missing, "
        "because it also has sideways speed, and the two together make a closed "
        "path.</p>",
    )
    b += (
        "<p>Change <code>dx</code> to 2.0 and the ship falls through the planet. Change "
        "it to 6.5 and it leaves the window. There is a band of starting speeds that "
        "stay on screen and clear the planet. Find both edges of the band by trying "
        "values, and write both numbers down before you look.</p>"
    )
    b += reveal(
        "Both edges, to one decimal place. Then a harder one: at what <code>dx</code> "
        "does the ship stop coming back at all?",
        output(
            """1200 frames each. planet radius 26. window 800 by 600.
  dx    DT    closest   farthest   frames off screen
  2.0   0.6        15        190       0
  2.8   0.6        29        180       0
  3.8   0.6        60        180       0
  6.0   0.6       180        298       0
  6.5   0.6       180        490     523
  7.6   0.6       180       2132    1077
  3.8   3.0        62        180       0
  3.8   8.0        66       4139     607""",
            "verified from headless runs of orbit.py with those values",
        )
        + "<p>About 2.8 to 6.0. Below 2.8 the closest approach drops inside the planet's "
        "radius of 26, and above 6.0 the far end of the loop goes off the top of the "
        "window. At 6.5 it goes off screen and comes back, on a much longer loop. At "
        "7.6 it does not come back: the farthest distance is still climbing when the "
        "run ends. That is the escape speed for this planet at this height, and the "
        "band from crash to escape is 2.8 to 7.6, which is wider than most people "
        "guess.</p>",
    )
    b += (
        '<div class="predict"><b>DT is a lie you are choosing.</b> Real gravity acts '
        "continuously, and this program applies it in jumps of 0.6. Set <code>DT</code> "
        "to 3.0 and the arithmetic is unchanged but the loop stops closing on itself: "
        "each pass lands a little to one side of the last, and the trail becomes a set of "
        "overlapping loops. The two rows at the bottom of the table show it. At 3.0 the ship "
        "still holds between 62 and 180, and it takes a DT of about 8 before a single "
        "jump is big enough to fling it off screen. That is worth seeing once.</div>"
    )

    b += '<h2><span class="num">3</span>The demo<span class="mins">45 minutes</span></h2>'
    b += (
        "<p>Parents arrive. Each student gets sixty seconds, and the shape is fixed:</p>"
        '<ul class="tight">'
        "<li><b>Run it.</b> Start the program. Say nothing while it loads.</li>"
        "<li><b>Point at it.</b> Name one thing on screen and say what line of your code "
        "makes it happen.</li>"
        "<li><b>Tell them.</b> One sentence on the hardest bug you fixed and how you "
        "found it.</li>"
        "</ul>"
        "<p>The third part is the one that matters, and it is the one to rehearse. "
        "Anybody can run a program. Explaining how you found a bug is the evidence that "
        "you wrote it.</p>"
        "<p>Rehearse in pairs first, twice through, with a timer. Sixty seconds is "
        "shorter than it sounds.</p>"
    )
    b += exits(
        "Your orbit program runs and the ship goes round at least once without crashing "
        "or escaping, and you can point at the line that makes gravity weaker further "
        "out.",
        "Floor, plus you found the band of starting speeds that produce an orbit and "
        "recorded both edges, plus a rehearsed sixty second demo.",
        "Middle, plus add a fuel budget: each key press spends fuel and changes dx or dy, "
        "and the readout prints to the terminal. Then set a target orbit and see whether "
        "you can reach it before the fuel runs out.",
    )
    b += panel(
        ["8.G.B.7", "7.RP.A.2", "8.F.B.4"],
        "<p>10 opener, 30 the orbit, 45 rehearsal and demo, 5 close. On demo day the "
        "timings slip, so have the orbit file working on the machines beforehand and "
        "treat section 2 as optional if parents arrive early. The band reveal is the "
        "first thing to cut from section 2: the table is on the page for anyone who "
        "wants it.</p>",
        "<p>Do not let the demo become a slideshow about what they meant to build. Run, "
        "point, tell. Sixty seconds each. Hold the timer yourself.</p>"
        "<p>A ship that spirals out or flies off is almost always a bug, not "
        "<code>DT</code>. The step order in <code>step</code> updates speed first and "
        "position second, and that order holds an orbit steady even at a DT of 6. Two "
        "bugs produce the fly-off: moving the position lines above the speed lines, "
        "and the double division by <code>r</code> below. Check those before anything "
        "else.</p>"
        "<p>Watch for students who normalise by dividing by <code>r</code> twice, or who "
        "forget it entirely. Forgetting it gives a pull that grows with distance and a "
        "ship that flies off immediately, which at least fails loudly.</p>",
        retouch=(
            "Session 12's class and its <code>step</code> method, with gravity changed "
            "from a constant to something that depends on position. Also session 12's "
            "flipped y axis, which still applies."
        ),
        extras=(
            "<h3>Files</h3><p><code>orbit.py</code>. Verified headless over 1200 frames "
            "on pygame 2.6.1. The orbit is stable for at least twenty seconds of "
            "runtime. <code>verify_orbit_band.py</code> produced the table of other "
            "starting speeds and time steps by running <code>orbit.py</code> with those "
            "values, with the frame clock switched off.</p>"
            "<h3>Capstone checkpoint</h3><p>Before parents arrive, walk the room with "
            "the four rubric lines from session 9. Any student with two or fewer yes "
            "answers demos the session 12 or 13 program as shipped and names the bug "
            "they fixed in their own addition, however far it got. Nobody demos a "
            "sketch.</p>"
            "<h3>Lifted this week</h3><p><code>math.sqrt</code> for distance, vector "
            "components by proportion, a time step.</p>"
            "<h3>After the demo</h3><p>Collect the Cartridge Ledger cards. Thirteen "
            "stamps is a full card and worth something to a twelve year old. Ask each "
            "student which session they would keep if they could only keep one, and "
            "write the answers down: that is your best data for next term.</p>"
        ),
    )
    b += pager(("wed12_classes.html", "Session 12: objects that remember"), None)
    return b
