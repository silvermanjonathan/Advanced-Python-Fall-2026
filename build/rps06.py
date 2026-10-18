"""Session 6: rock, paper, scissors, decided three ways."""

import ast
import math
import os
import subprocess

from build import answer_key, code, downloads, labelled_code, laddered, masthead, output, pager, reveal
from stds import panel

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ERROR = "last line of the error"


def _source(name):
    """Return the text of a program in the repo root."""
    with open(os.path.join(_ROOT, name)) as f:
        return f.read()


def _part(name, start, end=None):
    """Return the lines of a program from the one beginning start, up to end."""
    text = _source(name)
    i = text.index(start)
    j = text.index(end, i) if end else len(text)
    return text[i:j].strip("\n")


def _run(name):
    """Run a program in the repo root and return its printed lines."""
    done = subprocess.run(["python3", name], cwd=_ROOT, capture_output=True, text=True,
                          check=True, timeout=60)
    return done.stdout.rstrip("\n").split("\n")


def _snippets():
    """Return the SNIPPETS dictionary from verify_rps.py, the code that was run."""
    tree = ast.parse(_source("verify_rps.py"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "SNIPPETS":
            return ast.literal_eval(node.value)
    raise ValueError("verify_rps.py has no SNIPPETS")


def _verified():
    """Run verify_rps.py and return each check's printed lines and last error line."""
    lines = _run("verify_rps.py")
    found = {}
    label = None
    for line in lines:
        if label is None:
            label = line.rstrip(":")
            found[label] = ([], "")
        elif line.startswith("  error: "):
            found[label] = (found[label][0], line[len("  error: "):])
            label = None
        else:
            found[label][0].append(line)
    return found


def _printed(found, label, error=None):
    """Return the printed lines of one check, after checking its error line."""
    lines, err = found[label]
    assert err == (error or "no error"), f"{label}: {err}"
    return "\n".join(lines)


def _table(lines):
    """Return the opener's table of who wins, built from what rps_if.py printed."""
    moves = ["rock", "paper", "scissors"]
    who = {}
    for line in lines:
        pairing, result = line.split(": ")
        move1, move2 = pairing.split(" against ")
        who[(move1, move2)] = result
    assert len(who) == 9
    rows = (
        "<table><tr><th>player 1 down, player 2 across</th>"
        + "".join(f"<th>{m}</th>" for m in moves)
        + "</tr>"
    )
    for move1 in moves:
        rows += f"<tr><th>{move1}</th>"
        rows += "".join(f"<td>{who[(move1, move2)]}</td>" for move2 in moves)
        rows += "</tr>"
    return rows + "</table>"


def _circle_svg():
    """Return the three moves around a circle, with an arrow from each to the next."""
    moves = ["rock", "paper", "scissors"]
    cx, cy, r, node = 230, 140, 92, 40
    spots = []
    for k in range(3):
        angle = math.radians(-90 + 120 * k)
        spots.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    parts = [
        '<defs><marker id="rps-head" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="#0A3A3E"/></marker></defs>'
    ]
    beats = ["paper beats rock", "scissors beats paper", "rock beats scissors"]
    for k in range(3):
        (x1, y1), (x2, y2) = spots[k], spots[(k + 1) % 3]
        dx, dy = x2 - x1, y2 - y1
        length = math.hypot(dx, dy)
        ux, uy = dx / length, dy / length
        sx, sy = x1 + ux * (node + 4), y1 + uy * (node + 4)
        ex, ey = x2 - ux * (node + 6), y2 - uy * (node + 6)
        parts.append(
            f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
            'stroke="#0A3A3E" stroke-width="3" marker-end="url(#rps-head)"/>'
        )
        # the label sits outside the circle, beside the middle of its arrow
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ox, oy = mx - cx, my - cy
        olen = math.hypot(ox, oy)
        # the bottom label has to clear the two circles beside it, so it goes further out
        out = 64 if abs(ox) < 1 else 34
        lx, ly = mx + ox / olen * out, my + oy / olen * out
        anchor = "middle" if abs(ox) < 1 else ("start" if ox > 0 else "end")
        parts.append(
            f'<text x="{lx:.1f}" y="{ly + 5:.1f}" text-anchor="{anchor}" font-size="16" '
            f'fill="#17181B">{beats[k]}</text>'
        )
    for k, (x, y) in enumerate(spots):
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{node}" fill="#FFFDF7" '
            'stroke="#0E4D52" stroke-width="3"/>'
        )
        parts.append(
            f'<text x="{x:.1f}" y="{y - 2:.1f}" text-anchor="middle" font-size="17" '
            f'font-weight="700" fill="#0A3A3E">{moves[k]}</text>'
        )
        parts.append(
            f'<text x="{x:.1f}" y="{y + 18:.1f}" text-anchor="middle" font-size="14" '
            f'fill="#4A4D53">position {k}</text>'
        )
    return (
        '<svg viewBox="0 0 460 290" width="460" style="max-width:100%; height:auto; '
        'display:block; margin:10px 0 16px" role="img" aria-label="Rock at position 0, '
        "paper at position 1, and scissors at position 2, around a circle. Arrows go "
        "one step forward: rock to paper, labelled paper beats rock; paper to scissors, "
        "labelled scissors beats paper; scissors back around to rock, labelled rock beats "
        'scissors.">' + "".join(parts) + "</svg>"
    )


GAME_PARTS = [
    ("wins = 0", "Three counters, each starting at 0: rounds you win, rounds you lose, "
     "and ties. These lines run once.", "once"),
    ("for turn in range(5):", "Five rounds. Every line indented under this one runs "
     "once in each round. First, show the question and store what you type in "
     "<code>my_move</code>.", "frame"),
    ("while my_move not in MOVES:", "While what you typed is not one of the three "
     "moves, ask again and store the new answer. The loop stops when the answer is one "
     "of the moves, so <code>winner</code> never gets a typo.", "frame"),
    ("computer_move = random.choice(MOVES)", "The computer picks a move at random. "
     "<code>winner</code> works out who won, with you as player 1, and the printed line "
     "uses <code>SAY</code> to put the result in words.", "frame"),
    ('if result == "player 1":', "Add 1 to the counter that matches the result.",
     "frame"),
    ('print(f"you won', "After the fifth round, print the three counters. This line is "
     "not indented, so it runs once, after the loop.", "after"),
]


def day06():
    """Session 6: rock, paper, scissors, three ways."""
    from days38 import exits

    s = _snippets()
    v = _verified()
    if_lines = _run("rps_if.py")
    dict_lines = _run("rps_dict.py")
    clock_lines = _run("rps_clock.py")
    three = _run("rps_three_ways.py")
    spock = _run("rps_spock.py")
    assert if_lines == dict_lines, "the if and dictionary versions disagree"
    assert three == ["the three versions agree on 9 of the 9 pairings"], three
    assert spock == ["the two versions agree on 25 of the 25 pairings"], spock

    # the worked trace in section 5, done with the program's own arithmetic
    moves = ["rock", "paper", "scissors"]
    results = ["tie", "player 1", "player 2"]
    spot1, spot2 = moves.index("rock"), moves.index("scissors")
    steps = (spot1 - spot2) % 3
    assert results[steps] == "player 1"
    assert f"rock against scissors: ({spot1} - {spot2}) % 3 = {steps}" in clock_lines

    game = _printed(v, "one game, seed 2")
    assert game.count("type rock, paper, or scissors:") == 1

    b = masthead(
        "06",
        "Rock, paper, scissors, three ways",
        "Wednesday 4 November 2026",
        "A program that plays rock paper scissors has to work out who won each round. "
        "Today you write that function three ways: with if lines, with a dictionary, "
        "and by counting steps around a circle. You play five rounds against the "
        "computer, and you check that all three versions give the same answer for every "
        "pairing.",
    )

    # Section 1: opener
    b += (
        '<h2><span class="num">1</span>Opener: nine pairings'
        '<span class="mins">10 minutes</span></h2>'
        "<p>Talk this one over with your neighbor first.</p>"
    )
    b += reveal(
        "In session 5, <code>report</code> worked out one line about a pet. Did "
        "<code>report</code> print the line, or return it? Then say what the caller can "
        "do with a returned line that it could not do with a printed one.",
        "<p><b>Return.</b> <code>report</code> returned the line, and "
        "<code>print(rocky.report())</code> printed it.</p>"
        "<p><b>What the caller can do.</b> A returned value goes to the line that called "
        "the function. That line can print it, store it in a variable, or compare it with "
        "something else. A printed line only goes to the terminal, and the program cannot "
        "use it again. Today's function, <code>winner</code>, returns who won, so the "
        "game in section 4 can store the answer and count it.</p>",
    )
    b += (
        "<p>The rules: rock beats scissors, scissors beats paper, and paper beats rock. "
        "If both players pick the same move, it is a tie.</p>"
        "<p>Player 1 picks one of the three moves, and player 2 picks one of the three "
        "moves. Each combination of the two picks is called a <b>pairing</b>. On paper, "
        "draw a table with player 1's move down the left side and player 2's move across "
        "the top. In each square, write who wins: player 1, player 2, or tie.</p>"
    )
    b += reveal(
        "How many squares does your table have? In how many does player 1 win, in how "
        "many does player 2 win, and how many are ties?",
        _table(if_lines)
        + "<p><b>Squares.</b> 9: 3 rows times 3 columns.</p>"
        "<p><b>Who wins.</b> Player 1 wins in 3 squares, player 2 wins in 3, and 3 are "
        "ties.</p>"
        "<p>Look along any one row. Whatever player 1 picks, one of player 2's picks "
        "loses to it, one is a tie, and one beats it. So if the computer picks at random, "
        "with each move as likely as the others, you win about 1 round in every 3, "
        "whatever you pick.</p>"
        "<p>Keep your table. You will check three programs against it today.</p>",
    )

    # Section 2: if lines
    b += (
        '<h2><span class="num">2</span>Decide it with if lines'
        '<span class="mins">15 minutes</span></h2>'
        '<div class="now"><p><b>Do this now.</b> Make a new file called '
        "<code>rps.py</code>. Type the list and the function below, then the three "
        "<code>print</code> lines under them. Answer the question under them before you "
        "run it.</p></div>"
    )
    b += code(_part("rps_if.py", "MOVES =", "# every pairing"), "rps.py")
    b += code(s["tests"], "rps.py, at the bottom")
    b += (
        "<p><code>MOVES</code> is a list of the three moves. A name in capitals holds a "
        "value the program never changes while it runs.</p>"
        "<p><code>winner</code> has two parameters: <code>move1</code> is player 1's move "
        "and <code>move2</code> is player 2's move. It returns one of three strings: "
        "<code>\"tie\"</code>, <code>\"player 1\"</code>, or "
        "<code>\"player 2\"</code>.</p>"
        "<p>The first gate checks for a tie. The next three gates are the three ways "
        "player 1 can win. Each one joins two comparisons with <code>and</code>, from "
        "session 2, so it is True only when both comparisons are True. If none of the "
        "four gates is True, the <code>else</code> line returns "
        "<code>\"player 2\"</code>.</p>"
    )
    tests = _printed(v, "if version, three tests")
    assert tests == "player 1\nplayer 2\ntie", tests
    b += reveal(
        "What do the three <code>print</code> lines print? Say which gate decides each "
        "one.",
        output(tests)
        + "<p><b>Line 1</b>, rock against scissors: the second gate is True, so player "
        "1.</p>"
        "<p><b>Line 2</b>, rock against paper: none of the four gates is True, so "
        "<code>else</code> returns player 2.</p>"
        "<p><b>Line 3</b>, paper against paper: the first gate is True, so it is a "
        "tie.</p>",
    )

    b += "<h3>Check every pairing</h3>"
    b += (
        "<p>Three tests try only three of the nine pairings. Replace the three "
        "<code>print</code> lines with this loop:</p>"
    )
    b += code(_part("rps_if.py", "# every pairing"), "rps.py, in place of the three print lines")
    b += (
        "<p>This is a loop inside a loop, as in session 3. The outer loop gives "
        "<code>move1</code> each of the three moves in turn. For each one, the inner loop "
        "gives <code>move2</code> all three moves.</p>"
    )
    b += reveal(
        "How many lines does it print? Check each line against the square for the same "
        "pairing in your table.",
        output("\n".join(if_lines), label="verified output, rps.py")
        + "<p>9 lines: 3 passes of the outer loop, and 3 passes of the inner loop on "
        "each of them. Each line should match a square of your table. If one does not, "
        "either the table or a gate is wrong. Find out which.</p>",
    )

    b += "<h3>A typo</h3>"
    b += "<p>Players make typos. Add this line at the bottom of <code>rps.py</code>, under the loop:</p>"
    b += code(s["typo"], "rps.py, at the bottom")
    typo_if = _printed(v, "if version, typo in move1")
    assert typo_if == "player 2", typo_if
    b += reveal(
        "The player meant rock and typed <code>rokc</code>, which is not one of the three "
        "moves. What does this line print, and which line of <code>winner</code> returns "
        "it?",
        output(typo_if)
        + "<p>It prints <code>player 2</code>, from the <code>else</code> line. "
        "<code>\"rokc\"</code> is not equal to <code>\"scissors\"</code>, so the first "
        "gate is False. Each player 1 gate needs <code>move1</code> to be "
        "<code>\"rock\"</code>, <code>\"scissors\"</code>, or <code>\"paper\"</code>, and "
        "<code>\"rokc\"</code> is none of them, so those three gates are False too. "
        "<code>else</code> runs whenever every gate above it is False, typo or not.</p>"
        "<p>Rock beats scissors, so the right answer is player 1. The program gives a "
        "wrong answer and shows no error.</p>",
    )

    # Section 3: a dictionary
    b += (
        '<h2><span class="num">3</span>The rules in a dictionary'
        '<span class="mins">15 minutes</span></h2>'
        "<p>In session 3, a dictionary stored values under keys, and "
        "<code>code_names[\"ben\"]</code> looked up the value stored under the key "
        "<code>\"ben\"</code>. The rules of rock paper scissors fit in a dictionary: each "
        "move is a key, and its value is the move it beats.</p>"
        "<p>A comparison such as <code>BEATS[\"scissors\"] == \"paper\"</code> gives True "
        "or False, and <code>print</code> shows which.</p>"
    )
    b += code(s["lookup"])
    lookup = _printed(v, "lookup")
    assert lookup == "rock\nTrue\nFalse", lookup
    b += reveal(
        "What do the three <code>print</code> lines print? For the second and third, say "
        "True or False, and why.",
        output(lookup)
        + "<p><b>Line 1</b> prints <code>rock</code>, the value stored under the key "
        "<code>\"paper\"</code>: paper beats rock.</p>"
        "<p><b>Line 2</b> prints <code>True</code>. <code>BEATS[\"scissors\"]</code> is "
        "<code>\"paper\"</code>, because scissors beats paper, and "
        "<code>\"paper\" == \"paper\"</code> is True.</p>"
        "<p><b>Line 3</b> prints <code>False</code>. <code>BEATS[\"rock\"]</code> is "
        "<code>\"scissors\"</code>, and <code>\"scissors\" == \"paper\"</code> is False. "
        "Rock does not beat paper.</p>",
    )
    b += (
        '<div class="now"><p><b>Do this now.</b> In <code>rps.py</code>, add '
        "<code>BEATS</code> and its comment under <code>MOVES</code>. Then change "
        "<code>winner</code> to the one below. Leave the loop and the typo line at the "
        "bottom as they are.</p></div>"
    )
    b += code(_part("rps_dict.py", "# each key beats", "\n\n\ndef winner"), "rps.py, under MOVES")
    b += code(_part("rps_dict.py", "def winner", "# every pairing"), "rps.py, the new winner")
    b += (
        "<p><code>BEATS[move1] == move2</code> asks one question: is <code>move2</code> "
        "the move that <code>move1</code> beats? If it is, player 1 wins. The three "
        "player 1 gates from section 2 are now one gate, and the rules are in the "
        "dictionary instead of in the gates.</p>"
    )
    typo_dict = _printed(v, "dictionary version, typo in move1", "KeyError: 'rokc'")
    assert typo_dict == ""
    b += reveal(
        "Before you run it: will the loop print the same nine lines as in section 2? Say "
        "yes or no, and why. Then say what the typo line will do now.",
        "<p><b>The nine lines.</b> Yes, the same nine:</p>"
        + output("\n".join(dict_lines), label="verified output, rps.py")
        + "<p>The inside of the function is different, but for each pairing it returns "
        "the same answer.</p>"
        "<p><b>The typo line.</b> After the nine lines, the program stops with an "
        "error:</p>"
        + output("KeyError: 'rokc'", ERROR)
        + "<p><code>\"rokc\"</code> is not a key in <code>BEATS</code>, so "
        "<code>BEATS[move1]</code> stops the program with a <code>KeyError</code>, as in "
        "session 3. The error names the typo, which is easier to spot than a wrong "
        "answer.</p>",
    )
    b += "<p>Now move the typo to player 2's move. Change the typo line to this:</p>"
    b += code(s["typo2"], "rps.py, at the bottom")
    typo2 = _printed(v, "dictionary version, typo in move2")
    assert typo2 == "player 2", typo2
    b += reveal(
        "Does it stop with an error, or print an answer? If it prints an answer, is the "
        "answer right?",
        output(typo2)
        + "<p>It prints an answer, and the answer is wrong. <code>BEATS[\"rock\"]</code> "
        "is <code>\"scissors\"</code>, so the lookup works. Then "
        "<code>\"scissors\" == \"sissors\"</code> is False, so the <code>else</code> "
        "line returns player 2. The player meant scissors, and rock beats scissors, so "
        "the right answer is player 1.</p>"
        "<p>Only <code>move1</code> is looked up in the dictionary, so only a typo in "
        "<code>move1</code> stops the program. Section 4 stops typos before they reach "
        "<code>winner</code>.</p>",
    )
    b += (
        "<p>If you fell behind, this is <code>rps.py</code> at the end of this section, "
        "without the typo line:</p>"
    )
    b += downloads(("rps_dict.py", "rps.py"))

    # Section 4: the game
    b += (
        '<h2><span class="num">4</span>Play the computer'
        '<span class="mins">15 minutes</span></h2>'
        "<p>The game needs three new things: a way to read what the player types, a way "
        "for the computer to pick at random, and a way to check that what was typed is "
        "one of the moves.</p>"
        "<h3>input</h3>"
        "<p><code>input(\"rock, paper, or scissors? \")</code> shows the words in the "
        "brackets in the terminal, then waits. When you type something and press Enter, "
        "<code>input</code> returns what you typed, as a string. Store it in a variable, "
        "or it is lost.</p>"
        "<h3>random.choice</h3>"
        "<p><code>import random</code> at the top of a file gives you Python's "
        "<code>random</code> module. <code>random.choice(MOVES)</code> returns one item "
        "of the list, picked at random.</p>"
    )
    b += code(s["choice"])
    choice = _printed(v, "choice, seed 6")
    assert len(set(choice.split("\n"))) == 3, choice
    b += reveal(
        "Before you run it: what do you know for sure about each of the three lines? Can "
        "the same move come up twice?",
        "<p><b>For sure.</b> Each line is one of the three moves: rock, paper, or "
        "scissors. Which one, nobody can know before it runs.</p>"
        "<p><b>Twice.</b> Yes. Each call picks again from all three moves, so the same "
        "move can come up twice, or even three times. One run printed:</p>"
        + output(choice, label="verified output, one run")
        + "<p>Run it again and the lines change.</p>",
    )
    b += (
        "<h3>in and not in</h3>"
        "<p><code>in</code> checks whether an item is in a list. It gives True or "
        "False, like a comparison.</p>"
    )
    b += code(s["in"])
    inn = _printed(v, "in")
    assert inn == "True\nFalse\nTrue", inn
    b += reveal(
        "What do the three lines print: True or False?",
        output(inn)
        + "<p><b>Line 1</b> is True, because <code>\"paper\"</code> is one of the items "
        "in <code>MOVES</code>.</p>"
        "<p><b>Line 2</b> is False, because <code>\"papper\"</code> is not.</p>"
        "<p><b>Line 3</b> is True. <code>not in</code> is the opposite of "
        "<code>in</code>.</p>",
    )
    b += (
        "<h3>The game</h3>"
        '<div class="now"><p><b>Do this now.</b> Make a new file called '
        "<code>rps_game.py</code>. Type <code>import random</code> at the top. Copy "
        "<code>MOVES</code>, <code>BEATS</code>, and <code>winner</code> into it from "
        "<code>rps.py</code>, and add <code>SAY</code> under <code>BEATS</code>, so the "
        "top of the file looks like this:</p></div>"
    )
    b += code(_part("rps_game.py", "import random", "\n\n\nwins = 0"), "rps_game.py, the top")
    b += (
        "<p><code>SAY</code> is a dictionary too. Its keys are the three strings "
        "<code>winner</code> can return, and each value is what to tell the player, so "
        "<code>SAY[\"player 1\"]</code> is <code>\"you win\"</code>. You are player "
        "1.</p>"
        "<p>Then type the game under <code>winner</code>. There is a button under each "
        "part. Before you press it, say what you think that part does.</p>"
    )
    b += labelled_code(_part("rps_game.py", "wins = 0"), GAME_PARTS, "rps_game.py, under winner")
    b += downloads("rps_game.py")
    b += reveal(
        "In one game the player typed six answers: <code>rock</code>, "
        "<code>papper</code>, <code>paper</code>, <code>scissors</code>, "
        "<code>rock</code>, <code>paper</code>. The game has five rounds. Which round got "
        "two answers, and which line of the program asked the second time?",
        "<p><b>Round.</b> Round 2. <code>papper</code> is not in <code>MOVES</code>, so "
        "the <code>while</code> loop ran, and <code>paper</code> was accepted.</p>"
        "<p><b>Line.</b> <code>my_move = input(\"type rock, paper, or scissors: \")</code>, "
        "the line inside the <code>while</code> loop.</p>"
        "<p>Here is the whole game:</p>"
        + output(game, label="verified output, one game")
        + "<p>The computer's moves are random, so your games will be different. Check "
        "the last line against the five rounds above it.</p>",
    )
    b += "<p>Play a game. Then play another, and make a typo on purpose.</p>"

    # Section 5: the circle
    b += (
        '<h2><span class="num">5</span>Count steps around a circle'
        '<span class="mins">25 minutes</span></h2>'
        "<p>The third version uses numbers. In <code>MOVES</code>, rock is at position "
        "0, paper at 1, and scissors at 2. Put the three moves around a circle in that "
        "order. After scissors, the circle comes back around to rock.</p>"
    )
    b += _circle_svg()
    b += (
        "<p>Follow an arrow one step forward. The move you land on beats the move you "
        "left: paper beats rock, scissors beats paper, and rock beats scissors.</p>"
        "<h3>From a move to its position</h3>"
    )
    b += code(s["index"])
    index = _printed(v, "index")
    assert index == "scissors\n1", index
    b += reveal(
        "What do the two lines print?",
        output(index)
        + "<p><b>Line 1.</b> <code>MOVES[2]</code> goes from a position to an item: the "
        "item at position 2 is <code>scissors</code>.</p>"
        "<p><b>Line 2.</b> <code>.index</code> goes the other way, from an item to its "
        "position: <code>\"paper\"</code> is at position 1. <code>.index</code> is a "
        "method, a function that belongs to every list, the way <code>feed</code> "
        "belongs to every pet in session 5.</p>",
    )
    b += (
        "<h3>Wrapping with % 3</h3>"
        "<p>In session 4, <code>-1 % 26</code> was 25: going back 1 from <code>a</code>, "
        "past the start of the alphabet, comes around to <code>z</code>. "
        "<code>% 3</code> does the same on a circle of three positions.</p>"
    )
    b += code(s["wrap"])
    wrap = _printed(v, "wrap")
    assert wrap == "2\n1", wrap
    b += reveal(
        "What do the two lines print?",
        output(wrap)
        + "<p><code>% 3</code> always gives 0, 1, or 2, even when the number before it is "
        "negative. Going back 1 from position 0 comes around to position 2. Going back 2 "
        "from position 0 comes around to position 1.</p>",
    )
    b += (
        "<h3>Steps for every pairing</h3>"
        '<div class="now"><p><b>Do this now.</b> Make a new file called '
        "<code>rps_clock.py</code> and type this:</p></div>"
    )
    b += code(_source("rps_clock.py"), "rps_clock.py")
    b += (
        "<p><code>spot1</code> is the position of player 1's move and <code>spot2</code> "
        "is the position of player 2's move. They are numbers this time, so the loops "
        "use <code>range(3)</code>. <code>MOVES[spot1]</code> turns a position back into "
        "a move for the printed line.</p>"
    )
    b += reveal(
        "Before you run it, work out the number at the end of each of the nine lines. "
        "The first one is <code>(0 - 0) % 3 = 0</code>.",
        output("\n".join(clock_lines), label="verified output, rps_clock.py"),
    )
    ones = [ln.split(":")[0] for ln in clock_lines if ln.endswith("= 1")]
    assert ones == ["rock against scissors", "paper against rock", "scissors against paper"], ones
    b += reveal(
        "Put each line beside the same pairing in your table from the opener. When the "
        "number is 0, who wins? When it is 1? When it is 2?",
        "<p><b>0</b>: a tie. Both players picked the same move.</p>"
        f"<p><b>1</b>: player 1 wins. {ones[0].capitalize()}, {ones[1]}, and {ones[2]} "
        "all give 1.</p>"
        "<p><b>2</b>: player 2 wins.</p>"
        "<p>Here is why. <code>(spot1 - spot2) % 3</code> is the number of steps forward "
        "around the circle from player 2's move to player 1's move. 1 step forward means "
        "player 1's move comes just after player 2's, so it beats it. 2 steps forward "
        "lands in the same place as 1 step back, so player 1's move comes just before "
        "player 2's, and player 2's move beats it.</p>",
    )
    b += (
        "<h3>winner, by counting steps</h3>"
        '<div class="now"><p><b>Do this now.</b> Download <code>rps_three_ways.py</code> '
        "and open it. It holds all three versions of <code>winner</code>, renamed "
        "<code>winner_if</code>, <code>winner_dict</code>, and <code>winner_clock</code>, "
        "and a check at the bottom that runs them against each other.</p></div>"
    )
    b += downloads("rps_three_ways.py")
    b += (
        "<p><code>winner_clock</code> is the new one. The number of steps says who won, "
        "so a list turns it into the answer: position 0 holds <code>\"tie\"</code>, "
        "position 1 holds <code>\"player 1\"</code>, and position 2 holds "
        "<code>\"player 2\"</code>.</p>"
    )
    b += code(
        _part("rps_three_ways.py", "# what each number of steps", "\n\n\ndef winner_if")
        + "\n\n\n"
        + _part("rps_three_ways.py", "def winner_clock", "agree = 0"),
        "rps_three_ways.py, the third version",
    )
    b += reveal(
        "Trace <code>winner_clock(\"rock\", \"scissors\")</code>. Write the value of "
        "<code>spot1</code>, <code>spot2</code>, and <code>steps</code>, then the return "
        "value.",
        f"<p><code>spot1</code> is {spot1}, the position of rock. <code>spot2</code> is "
        f"{spot2}, the position of scissors.</p>"
        f"<p><code>steps</code> is <code>({spot1} - {spot2}) % 3</code>. "
        f"{spot1} - {spot2} = {spot1 - spot2}, and <code>{spot1 - spot2} % 3</code> is "
        f"{steps}, the same wrap as above.</p>"
        f"<p>The function returns <code>RESULTS[{steps}]</code>, which is "
        f"<code>\"{results[steps]}\"</code>. Rock beats scissors.</p>",
    )
    one_line = _printed(v, "one-line version in rps_three_ways.py")
    assert one_line == three[0], one_line
    b += "<p>Some programmers write the whole function on one line:</p>"
    b += code(s["one_line"])
    b += (
        "<p>It does the same arithmetic in the same order and returns the same answers. "
        "The four-line version gives each step a name, so you can print "
        "<code>spot1</code>, <code>spot2</code>, or <code>steps</code> to check it.</p>"
    )
    bad1 = "ValueError: 'rokc' is not in list"
    bad2 = "ValueError: 'sissors' is not in list"
    agree_line = three[0]
    assert _printed(v, "clock version, typo in move1", bad1) == agree_line
    assert _printed(v, "clock version, typo in move2", bad2) == agree_line
    b += (
        "<p>The two typos again. Add the first of these lines under the check at the "
        "bottom of <code>rps_three_ways.py</code>. After you answer the question below, "
        "run it, then replace it with the second line and run it again.</p>"
    )
    b += code(s["clock_typos"], "rps_three_ways.py, at the bottom, one line at a time")
    b += reveal(
        "For each line: does it print an answer, or stop with an error?",
        "<p><b>The first line</b> stops with an error, after the check has printed its "
        "line:</p>"
        + output(bad1, ERROR)
        + "<p><b>The second line</b> stops with an error too:</p>"
        + output(bad2, ERROR)
        + "<p><code>.index</code> stops the program with a <code>ValueError</code> when "
        "the item is not in the list. Both moves are looked up with <code>.index</code>, "
        "so this version catches a typo in either move.</p>",
    )
    b += (
        "<h3>Do all three agree?</h3>"
        "<p>Take the typo line out again. This is the check at the bottom of "
        "<code>rps_three_ways.py</code>. It runs all three versions on every pairing:</p>"
    )
    b += code(_part("rps_three_ways.py", "agree = 0"), "rps_three_ways.py, the check")
    b += reveal(
        "What does it print?",
        output(three[0], label="verified output, rps_three_ways.py")
        + "<p>The gate joins two comparisons with <code>and</code>: the first answer "
        "equals the second, and the second equals the third. When both are True, all "
        "three answers are the same, and <code>agree</code> goes up by 1.</p>",
    )
    wrong = _printed(v, "paper beats scissors by mistake")
    assert wrong == "the three versions agree on 7 of the 9 pairings", wrong
    b += reveal(
        "Suppose <code>BEATS</code> had <code>\"paper\": \"scissors\"</code> by mistake, "
        "in place of <code>\"paper\": \"rock\"</code>. How many of the 9 pairings would "
        "the three versions agree on? Say which pairings go wrong.",
        output(wrong)
        + "<p><b>How many.</b> 7.</p>"
        "<p><b>Which pairings.</b> <code>winner_dict</code> only looks up "
        "<code>BEATS[\"paper\"]</code> when player 1 plays paper. Paper against paper "
        "is a tie, which the first gate returns before any lookup. That leaves paper "
        "against scissors, which now says player 1, and paper against rock, which now "
        "says player 2. Both are wrong, and the other 7 pairings still agree.</p>"
        "<p>The three tests from section 2 would not have caught this mistake: rock "
        "against scissors, rock against paper, and paper against paper all still give "
        "the right answer. Checking all nine pairings does catch it.</p>",
    )
    b += (
        "<p>Any of the three versions can go in <code>rps_game.py</code>. They take the "
        "same two moves and return the same answer, so the game plays the same way. The "
        "third version needs <code>RESULTS</code> copied in with it.</p>"
    )

    # exits, then the stretch
    b += exits(
        "<code>rps.py</code> runs with the dictionary version of <code>winner</code>, and "
        "its nine lines match your table from the opener. You can say what the if "
        "version and the dictionary version each do with "
        "<code>winner(\"rokc\", \"scissors\")</code>.",
        "Floor, plus you played a game of <code>rps_game.py</code> with a typo in it, "
        "and <code>rps_three_ways.py</code> prints 9 of the 9. Trace "
        "<code>winner_clock(\"scissors\", \"rock\")</code> out loud: <code>spot1</code>, "
        "<code>spot2</code>, <code>steps</code>, and the return value.",
        "Middle, plus rock paper scissors lizard Spock. Write its <code>BEATS</code> and "
        "a <code>winner_dict</code> that uses it, then find the rule for steps with "
        "<code>% 5</code>. Work it out below.",
    )

    spock_beats = ast.literal_eval(
        _part("rps_spock.py", "BEATS = {", "\n\n\ndef winner_dict").split("=", 1)[1].strip()
    )
    names = {"spock": "Spock"}
    rules = "".join(
        f"<li>{names.get(m, m).capitalize()} beats {names.get(a, a)} and "
        f"{names.get(c, c)}.</li>"
        for m, (a, c) in spock_beats.items()
    )
    b += (
        "<h3>Stretch: rock paper scissors lizard Spock</h3>"
        "<p>This game has five moves. Each move beats two others:</p>"
        f'<ul class="tight">{rules}</ul>'
        "<p>Make a new file called <code>rps_spock.py</code> for it.</p>"
    )
    b += laddered(
        "Write <code>MOVES</code> and <code>BEATS</code> for five moves, and a function "
        "called <code>winner_dict</code> that uses <code>BEATS</code>. The file gets a "
        "second version later, so this one is not called <code>winner</code>. Each value "
        "in <code>BEATS</code> is now a list of two moves.",
        [
            "<p>Each key still holds what it beats, now as a list: "
            "<code>\"rock\": [\"scissors\", \"lizard\"]</code>.</p>",
            "<p>The gate in <code>winner_dict</code> now asks whether <code>move2</code> is one "
            "of the items in the list <code>BEATS[move1]</code>. Section 4 used "
            "<code>in</code> to ask whether an item is in a list.</p>",
        ],
        code(_part("rps_spock.py", "MOVES =", "def winner_clock"), "rps_spock.py"),
        "spock-dict",
    )
    steps_table = _printed(v, "lizard Spock steps")
    wins = sorted({int(ln.split("steps ")[1].split(",")[0])
                   for ln in steps_table.split("\n") if ln.endswith("player 1")})
    losses = sorted({int(ln.split("steps ")[1].split(",")[0])
                     for ln in steps_table.split("\n") if ln.endswith("player 2")})
    assert wins == [1, 3] and losses == [2, 4], (wins, losses)
    swapped = _printed(v, "lizard Spock with spock and lizard swapped")
    assert swapped.endswith("of the 25 pairings") and "25 of the 25" not in swapped
    b += laddered(
        "Keep the moves in this order: rock, paper, scissors, spock, lizard. With "
        "<code>% 5</code> in place of <code>% 3</code>, steps is "
        "<code>(spot1 - spot2) % 5</code>, a number from 0 to 4. Which numbers of steps "
        "mean player 1 wins? Write a <code>winner_clock</code> that uses the rule.",
        [
            "<p>Let <code>winner_dict</code> say who wins, and print the steps beside it, "
            "for every pairing that is not a tie. <code>!=</code> means not equal, so the "
            "gate skips the five pairings where both moves are the same. Put this under "
            "<code>winner_dict</code>:</p>"
            + code(s["steps_table"], "rps_spock.py, under winner_dict"),
            "<p>Here is what it prints. Look at the steps on the lines that end in "
            "player 1, then on the lines that end in player 2.</p>"
            + output(steps_table, label="verified output"),
            f"<p>Player 1 wins when steps is {wins[0]} or {wins[1]}, and player 2 wins "
            f"when it is {losses[0]} or {losses[1]}. {wins[0]} and {wins[1]} are odd. A "
            "whole number is odd when <code>% 2</code> gives 1.</p>",
        ],
        f"<p>Player 1 wins when steps is {wins[0]} or {wins[1]}, the odd numbers. "
        "Here is <code>winner_clock</code> with that rule:</p>"
        + code(_part("rps_spock.py", "def winner_clock", "agree = 0"), "rps_spock.py")
        + "<p>The check at the bottom of <code>rps_spock.py</code> runs both versions on "
        "all 25 pairings:</p>"
        + output(spock[0], label="verified output, rps_spock.py")
        + "<p>The order of <code>MOVES</code> matters. With <code>spock</code> and "
        "<code>lizard</code> swapped, the same check prints:</p>"
        + output(swapped)
        + "<p>The odd rule only works when the moves go around the circle in an order "
        "where each move beats the moves 1 and 3 steps before it.</p>",
        "spock-clock",
    )

    key = "<p>Each file below runs as it is.</p>"
    key += code(_source("rps_if.py"), "rps.py after section 2, without the typo line (rps_if.py)")
    key += code(_source("rps_dict.py"), "rps.py after section 3, without the typo line (rps_dict.py)")
    key += code(_source("rps_game.py"), "rps_game.py")
    key += code(_source("rps_three_ways.py"), "rps_three_ways.py")
    key += code(_source("rps_spock.py"), "rps_spock.py, the stretch")
    b += answer_key(
        key,
        "rps",
        "The whole of each program. Open it to check a program that will not run, or one "
        "that prints something different.",
    )

    b += panel(
        ["7.SP.C.8", "MP7", "MP8"],
        "<p>10 opener, 15 if lines, 15 the dictionary, 15 the game, 25 the circle, 10 "
        "exits. The opener's table is used again in sections 2, 3, and 5, so check that "
        "every student has one, with player 1 down the left side, before section 2. If "
        "the room is behind, the one-line version and the typo question in section 5 "
        "can go, and the nine numbers from <code>rps_clock.py</code> can be worked out "
        "together on the board: the middle exit needs the trace and the check, not "
        "those.</p>",
        "<p>The <code>else</code> line in section 2. Students read it as \"player 2 "
        "won\". It means \"none of the gates above was True\", which is why a typo lands "
        "there. Ask the room which line returns for <code>rokc</code> before anyone opens "
        "the answer.</p>"
        "<p><code>BEATS[move1] == move2</code> reads backwards to some students. Say it "
        "the same way every time: is <code>move2</code> the move that <code>move1</code> "
        "beats?</p>"
        "<p><code>input</code> reads what is typed in the terminal. If a student's game "
        "waits and typing does nothing, the typing is going into the editor: click in "
        "the terminal panel first. If the program runs in VS Code's Output tab, which "
        "cannot take typing, run it in the terminal instead.</p>"
        "<p>A capital letter counts as a typo: <code>\"Rock\" in MOVES</code> is False, "
        "so the game asks again. Expect \"it keeps asking me\".</p>"
        "<p>Use the rock against scissors trace in section 5 as a hinge. The step that "
        "matters is <code>-2 % 3</code>. A student who writes -2 has not carried session "
        "4's wrap over to this circle. Run the two-line wrap program again on the "
        "projector before going on.</p>"
        "<p>Name the habit in the three-way check: test every pairing, not three of them. "
        "The mistake in <code>BEATS</code> passes all three of section 2's tests and "
        "fails the check.</p>",
        retouch=(
            "Session 4's <code>%</code> with a negative number, now on a circle of three: "
            "<code>-2 % 3</code> is 1. Session 3's dictionaries and <code>KeyError</code>, "
            "now holding the rules of a game, and session 3's loop inside a loop, to "
            "reach every pairing. Session 5's <code>report</code>, which returned its line "
            "for the caller to use: <code>winner</code> returns its answer, and the game "
            "stores it, compares it, and counts it."
        ),
        extras=(
            "<h3>Files</h3><p><code>rps_if.py</code> and <code>rps_dict.py</code> are "
            "<code>rps.py</code> after sections 2 and 3; the second has a download button "
            "that saves it as <code>rps.py</code>. Then <code>rps_game.py</code>, "
            "<code>rps_clock.py</code>, <code>rps_three_ways.py</code>, and "
            "<code>rps_spock.py</code>, the stretch answer. <code>verify_rps.py</code> is "
            "for you. It runs every short piece of code on the page after the function "
            "it needs and prints the last line of each error; checks the one-line "
            "version, the mistake in <code>BEATS</code>, and the swapped lizard Spock "
            "order; and plays one game with six typed answers and the computer's moves "
            "fixed by a seed. A second seed fixes the one run of "
            "<code>random.choice</code> in section 4. The build runs these files and "
            "quotes what they print, so every output and error on the page came from a "
            "run on Python 3.12.3.</p>"
            "<h3>Lifted this week</h3><p><code>input</code>, <code>import random</code> "
            "and <code>random.choice</code>, <code>in</code> and <code>not in</code> with "
            "a list, <code>.index</code> on a list, <code>ValueError</code>, and the word "
            "pairing.</p>"
        ),
    )
    b += pager(
        ("wed05_objects.html", "Session 5: making your own objects"),
        ("wed07_heuristics.html", "Session 7: smarter than brute force"),
    )
    return b
