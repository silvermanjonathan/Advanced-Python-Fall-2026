"""Check every output and error message quoted on the session 6 page.

The short pieces of code on the page are the strings in SNIPPETS below; the page
generator reads them from this file, so the code on the page and the code run here
cannot drift apart. Each piece runs in a fresh Python after the winner function it
needs, and the last line of any error is printed, which is the line a student sees in
the terminal. The game is played once with typed answers and a fixed seed, so the
computer's moves are the same every time this file runs.
"""

import subprocess
import sys

SNIPPETS = {
    "tests": '''print(winner("rock", "scissors"))
print(winner("rock", "paper"))
print(winner("paper", "paper"))''',
    "typo": '''print(winner("rokc", "scissors"))''',
    "typo2": '''print(winner("rock", "sissors"))''',
    "clock_typos": '''print(winner_clock("rokc", "scissors"))
print(winner_clock("rock", "sissors"))''',
    "lookup": '''BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}

print(BEATS["paper"])
print(BEATS["scissors"] == "paper")
print(BEATS["rock"] == "paper")''',
    "index": '''MOVES = ["rock", "paper", "scissors"]

print(MOVES[2])
print(MOVES.index("paper"))''',
    "wrap": '''print(-1 % 3)
print(-2 % 3)''',
    "one_line": '''def winner(move1, move2):
    """Return who wins when player 1 plays move1 and player 2 plays move2."""
    return RESULTS[(MOVES.index(move1) - MOVES.index(move2)) % 3]''',
    "in": '''MOVES = ["rock", "paper", "scissors"]

print("paper" in MOVES)
print("papper" in MOVES)
print("papper" not in MOVES)''',
    "choice": '''import random

MOVES = ["rock", "paper", "scissors"]

print(random.choice(MOVES))
print(random.choice(MOVES))
print(random.choice(MOVES))''',
    "steps_table": '''for move1 in MOVES:
    for move2 in MOVES:
        if move1 != move2:
            steps = (MOVES.index(move1) - MOVES.index(move2)) % 5
            result = winner_dict(move1, move2)

            print(f"{move1} against {move2}: steps {steps}, {result}")''',
}

# the typed answers for the game, and the seed that fixes the computer's moves
ANSWERS = ["rock", "papper", "paper", "scissors", "rock", "paper"]
SEED = 2


def part(name, start, end):
    """Return the lines of a program file from the one beginning start, up to end."""
    text = open(name).read()
    i = text.index(start)
    return text[i:text.index(end, i)]


IF_WINNER = part("rps_if.py", "MOVES =", "# every pairing")
DICT_WINNER = part("rps_dict.py", "MOVES =", "# every pairing")
SPOCK_DICT = part("rps_spock.py", "MOVES =", "def winner_clock")


def run(source):
    """Run source in a fresh Python and return its output and its last error line."""
    done = subprocess.run(
        [sys.executable, "-c", source], capture_output=True, text=True, timeout=30
    )
    errors = done.stderr.strip().splitlines()
    last = errors[-1] if errors else "no error"
    return done.stdout, last


def show(label, source):
    """Run source and print what it printed, then its last error line."""
    out, err = run(source)
    print(f"{label}:")
    print(out, end="")
    print(f"  error: {err}")


show("if version, three tests", IF_WINNER + SNIPPETS["tests"])
show("if version, typo in move1", IF_WINNER + SNIPPETS["typo"])
show("dictionary version, typo in move1", DICT_WINNER + SNIPPETS["typo"])
show("dictionary version, typo in move2", DICT_WINNER + SNIPPETS["typo2"])
CLOCK_FILE = open("rps_three_ways.py").read()
first, second = SNIPPETS["clock_typos"].split("\n")
show("clock version, typo in move1", CLOCK_FILE + first)
show("clock version, typo in move2", CLOCK_FILE + second)
show("lookup", SNIPPETS["lookup"])
show("index", SNIPPETS["index"])
show("wrap", SNIPPETS["wrap"])
show("in", SNIPPETS["in"])

# random.choice gives three moves; the seed only fixes them for this check
show("choice, seed 6", "import random\nrandom.seed(6)\n" + SNIPPETS["choice"].replace("import random\n", ""))

# the one-line winner, in place of the four-line one, must give the same nine answers
three = open("rps_three_ways.py").read()
four_lines = part("rps_three_ways.py", "def winner_clock", "agree = 0")
one_line = SNIPPETS["one_line"].replace("def winner(", "def winner_clock(") + "\n\n\n"
assert four_lines in three
show("one-line version in rps_three_ways.py", three.replace(four_lines, one_line))

# a wrong rule in the dictionary: the check should catch it
wrong = three.replace('"paper": "rock"', '"paper": "scissors"', 1)
assert wrong != three
show("paper beats scissors by mistake", wrong)

# the stretch: which numbers of steps go with a win, for all 20 pairings that are not ties
show("lizard Spock steps", SPOCK_DICT + SNIPPETS["steps_table"])

# the order of the five moves matters: with spock and lizard swapped, the rule breaks
spock = open("rps_spock.py").read()
swapped = spock.replace('"spock", "lizard"]', '"lizard", "spock"]', 1)
assert swapped != spock
show("lizard Spock with spock and lizard swapped", swapped)

# a capital letter is not one of the three moves, so the game asks again
show("capital letter", 'MOVES = ["rock", "paper", "scissors"]\nprint("Rock" in MOVES)')

# one game, with the answers typed in and printed the way the terminal shows them
game = f'''import builtins
import random

answers = iter({ANSWERS!r})


def typed(prompt):
    answer = next(answers)
    print(prompt + answer)
    return answer


builtins.input = typed
random.seed({SEED})
exec(open("rps_game.py").read())
'''
show(f"one game, seed {SEED}", game)
