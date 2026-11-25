"""Extra page: ten problems from Codewars. Writes extra_codewars.html.

Each problem is a kata on codewars.com, picked because it can be solved with what
sessions 1 to 7 taught. The kata titles, ranks and links in PROBLEMS were read from
codewars.com on 25 November 2026. The task wording, the function names, the test
lines and the answers are this course's own.

Nothing here is typed from expectation. For every problem the build runs the answer
with its test lines as FILE_NAME and shows what the run printed as the target output.
Each test line also has an expected value worked out a second way (the "want" list);
the build stops if the run and the second way disagree. crosscheck.py runs them all
again through verify().

The hints are there to help a student think, not to show the method. Each problem
has three hints, from the most general to the most specific, and each one shows the
function with blanks, cut from the answer that was run:

    hint 1   the idea, then the plan as comments with a blank for every line of code
    hint 2   how the idea is used, then the control words the function has (for,
             if, elif, else, return); the rest of each line is blank
    hint 3   a case to work by hand, then everything except the ⟦marked⟧ parts:
             every condition and every worked-out value is still blank

Each hint's caption is built from that problem's own function, so it cannot name a
word the function does not use. The build also stops if a hint sentence or a plan
comment says loop, pass or gate about a function with no for or no if.

Why the hints are built this way (read 25 November 2026):
  - General first, specific last: tutors order hint levels from the principle that
    applies down to the bottom-out hint (Koedinger and Aleven 2007).
  - Control words shown, conditions and values blank: Faded Parsons Problems never
    blank top-level control flow and blank conditionals, constants and expressions
    (Weinman, Fox and Hearst 2021).
  - The plan as comments: subgoal labels, short phrases that say what a group of
    lines is for (Margulieux, Morrison and Decker).
  - A case to work by hand before the last blanks: finishing a part-written program
    can turn into filling a template without understanding it (van Merrienboer
    1990), and students often click through to the last hint (Aleven et al. 2006).
"""

import ast
import html
import os
import re
import subprocess
import sys
import tempfile

from build import code, masthead, output

OUT_NAME = "extra_codewars.html"
TITLE = "Ten problems from Codewars"
FILE_NAME = "Jonathan_codewars.py"


def c(text):
    return text[1:] if text.startswith("\n") else text


# title, rank, url   the kata on codewars.com
# uses               what it needs, and the session that taught it
# task               paragraphs: what the function takes and what it returns
# name               the function's name; tests are the lines under the function
# want               one Python expression per test line, worked out a second way
# hints              three sentences, general to specific: the idea, how it is used
#                    here, and a case to work by hand. Each opens inside the one
#                    before.
# answer             the function. A comment line is a step of the plan and shows in
#                    every hint. ⟦text⟧ marks a part to think about: a condition or
#                    the value a line works out. Those parts stay blank in every
#                    hint and show only in the answer.
# after              text under the answer
# further            optional Go further line
PROBLEMS = [
{"title": "Even or Odd", "rank": "8 kyu",
 "url": "https://www.codewars.com/kata/53da3dbb4a5168369a0000fe",
 "uses": "`%` (session 6) and `return` (session 2)",
 "task": [
     "Write a function `even_or_odd(number)`. It takes a whole number. It returns the "
     "string `\"Even\"` when the number is even and the string `\"Odd\"` when it is odd.",
 ],
 "tests": c('''
print(even_or_odd(4))
print(even_or_odd(7))
print(even_or_odd(0))
print(even_or_odd(-3))
'''),
 "want": ['"Even"', '"Odd"', '"Even"', '"Odd"'],
 "hints": [
     "An even number divides by 2 with nothing left over. `%` gives what is left over.",
     "A gate compares what is left over with a number. One answer is returned under "
     "the gate and the other under `else`.",
     "Work 7 by hand first: what is left over when 7 is divided by 2? What is left "
     "over for 4? The condition has to say yes for 4 and no for 7.",
 ],
 "answer": c('''
def even_or_odd(number):
    # decide: is the number even?
    if ⟦number % 2 == 0⟧:
        return "Even"
    else:
        return "Odd"
'''),
 "after": [
     "`-3 % 2` is 1, so the function works for numbers below zero as well. Session 4 "
     "used `%` with a negative number the same way.",
 ],
 "facts": ["-3 % 2 == 1"]},

{"title": "Is n divisible by x and y?", "rank": "8 kyu",
 "url": "https://www.codewars.com/kata/5545f109004975ea66000086",
 "uses": "`%` (session 6) and `and` to join two comparisons (session 2)",
 "task": [
     "Write a function `is_divisible(n, x, y)`. It returns `True` when `n` divides by "
     "`x` with nothing left over and also divides by `y` with nothing left over. "
     "Otherwise it returns `False`.",
 ],
 "tests": c('''
print(is_divisible(12, 3, 4))
print(is_divisible(12, 3, 5))
print(is_divisible(100, 5, 10))
'''),
 "want": ["True", "False", "True"],
 "hints": [
     "One number divides by another with nothing left over when the remainder is 0. "
     "`%` gives the remainder.",
     "A function can return the value of a comparison, so no gate is needed. One "
     "word joins two comparisons so that both have to be True.",
     "Work the second test line by hand, `is_divisible(12, 3, 5)`: does 12 divide by"
     " 3? Does 12 divide by 5? Write one comparison for each question.",
 ],
 "answer": c('''
def is_divisible(n, x, y):
    # both comparisons have to be True
    return ⟦n % x == 0⟧ and ⟦n % y == 0⟧
'''),
 "after": [
     "12 divides by 3 and by 4, so the first line prints `True`. 12 does not divide by "
     "5, so `and` gives `False` on the second line.",
 ],
 "facts": ["12 % 3 == 0 and 12 % 4 == 0", "12 % 5 != 0"]},

{"title": "Sum of positive", "rank": "8 kyu",
 "url": "https://www.codewars.com/kata/5715eaedb436cf5606000381",
 "uses": "an accumulator with a gate (session 1)",
 "task": [
     "Write a function `sum_of_positive(numbers)`. It takes a list of numbers. It "
     "returns the total of the numbers that are more than 0. Numbers below 0 are left "
     "out of the total.",
     "For a list with no numbers above 0, it returns 0.",
 ],
 "tests": c('''
print(sum_of_positive([1, -4, 7, 12]))
print(sum_of_positive([-1, -2, -3]))
print(sum_of_positive([]))
'''),
 "want": ["1 + 7 + 12", "0", "0"],
 "hints": [
     "This needs an accumulator, as in session 1: a variable that starts at 0 and "
     "grows inside a loop.",
     "Inside the loop, a gate decides whether `n` is added to `total`.",
     "Work the first test line by hand, `[1, -4, 7, 12]`: write the value of `total`"
     " after each pass of the loop. Then fill in the blanks so the code does what "
     "you did.",
 ],
 "answer": c('''
def sum_of_positive(numbers):
    # start the total
    total = ⟦0⟧
    # look at each number, and add it only when it is more than 0
    for n in numbers:
        if ⟦n > 0⟧:
            total = ⟦total + n⟧
    # give the total back
    return total
'''),
 "after": [
     "For the empty list the loop makes no passes, so `total` is still 0 when it is "
     "returned.",
 ]},

{"title": "Find the smallest integer in the array", "rank": "8 kyu",
 "url": "https://www.codewars.com/kata/55a2d7ebe362935a210000b2",
 "uses": "a best-so-far variable (session 1)",
 "task": [
     "Write a function `smallest(numbers)`. It takes a list of whole numbers with at "
     "least one number in it. It returns the smallest number in the list.",
     "Codewars calls a list an array. Integer is the name for a whole number.",
 ],
 "tests": c('''
print(smallest([34, 15, 88, 2]))
print(smallest([34, -345, -1, 100]))
print(smallest([7]))
'''),
 "want": ["min([34, 15, 88, 2])", "min([34, -345, -1, 100])", "7"],
 "hints": [
     "Session 1 kept a best-so-far variable. Here it holds the smallest number seen "
     "so far.",
     "The variable cannot start at 0, because 0 might not be in the list. Start it "
     "at a number that is in the list. Inside the loop, a gate decides whether `n` "
     "replaces it.",
     "Work the first test line by hand, `[34, 15, 88, 2]`: write the value of `best`"
     " after each pass of the loop. Then fill in the blanks so the code does what "
     "you did.",
 ],
 "answer": c('''
def smallest(numbers):
    # start with a number from the list as the smallest so far
    best = ⟦numbers[0]⟧
    # look at each number, and keep it when it is smaller
    for n in numbers:
        if ⟦n < best⟧:
            best = ⟦n⟧
    # give the smallest back
    return best
'''),
 "after": [
     "Starting `best` at 0 would be a bug: for the list `[34, 15, 88, 2]` the function "
     "would return 0, and 0 is not in the list.",
 ]},

{"title": "Reversed Strings", "rank": "8 kyu",
 "url": "https://www.codewars.com/kata/5168bb5dfe9a00b126000018",
 "uses": "a string accumulator and `+` to join strings (session 3)",
 "task": [
     "Write a function `reverse(text)`. It takes a string and returns the same letters "
     "in the opposite order.",
 ],
 "tests": c('''
print(reverse("world"))
print(reverse("stressed"))
print(reverse("a"))
'''),
 "want": ['"".join(reversed("world"))', '"".join(reversed("stressed"))', '"a"'],
 "hints": [
     "This needs a string accumulator, as in session 3: start with the empty string "
     "and join one letter to it on each pass of the loop.",
     "`+` can join the new letter at either end of `out`. One end keeps the letters "
     "in order. The other end turns them around.",
     "Work `reverse(\"abc\")` by hand: write `out` after each pass of the loop. "
     "Which end of `out` does each new letter go on?",
 ],
 "answer": c('''
def reverse(text):
    # start with no letters
    out = ⟦""⟧
    # take each letter, and join it to the letters so far
    for ch in text:
        out = ⟦ch + out⟧
    # give the new string back
    return out
'''),
 "after": [
     "Each new letter goes in front of the letters already in `out`, so the last "
     "letter of `text` ends up first.",
 ]},

{"title": "Vowel Count", "rank": "7 kyu",
 "url": "https://www.codewars.com/kata/54ff3102c1bad923760001f3",
 "uses": "a counter with a gate (session 1) and `in` with a list (session 6)",
 "task": [
     "Write a function `count_vowels(text)`. It takes a string of small letters and "
     "spaces. It returns how many of its letters are vowels. The vowels are a, e, i, o "
     "and u.",
 ],
 "tests": c('''
print(count_vowels("abracadabra"))
print(count_vowels("sky"))
print(count_vowels("read the code"))
'''),
 "want": ['sum("abracadabra".count(v) for v in "aeiou")',
          'sum("sky".count(v) for v in "aeiou")',
          'sum("read the code".count(v) for v in "aeiou")'],
 "hints": [
     "Put the five vowels in a list at the top of the file. Then this needs a "
     "counter: a variable that starts at 0 and goes up by 1 inside a loop.",
     "Inside the loop, a gate asks whether the character is one of the vowels. "
     "Session 6 asked whether a move was in a list.",
     "Work the second test line by hand, `\"sky\"`: how many times does the gate say"
     " yes? Then do the same for the first three letters of `\"abracadabra\"`.",
 ],
 "answer": c('''
VOWELS = ["a", "e", "i", "o", "u"]


def count_vowels(text):
    # start the count
    count = ⟦0⟧
    # look at each character, and count it only when it is a vowel
    for ch in text:
        if ⟦ch in VOWELS⟧:
            count = ⟦count + 1⟧
    # give the count back
    return count
'''),
 "after": [
     "`count = count + 1` adds 1 for each vowel. Adding `ch` would be a bug, because "
     "`ch` is a letter and `count` is a number.",
 ]},

{"title": "Disemvowel Trolls", "rank": "7 kyu",
 "url": "https://www.codewars.com/kata/52fba66badcd10859f00097e",
 "uses": "a string accumulator (session 3) and `not in` with a list (session 6)",
 "task": [
     "Write a function `remove_vowels(text)`. It takes a string and returns the string "
     "with every small a, e, i, o and u taken out. Every other character stays, spaces "
     "included.",
 ],
 "tests": c('''
print(remove_vowels("your code is so slow"))
print(remove_vowels("trace it first"))
print(remove_vowels("rhythm"))
'''),
 "want": ['"".join(ch for ch in "your code is so slow" if ch not in "aeiou")',
          '"".join(ch for ch in "trace it first" if ch not in "aeiou")',
          '"rhythm"'],
 "hints": [
     "This is problem 6 with one change. In place of counting the vowels, build a "
     "new string from the characters that are not vowels.",
     "Start with the empty string. Inside the loop, a gate decides whether the "
     "character is joined to the end of `out`.",
     "Work the word `\"trace\"` by hand: write `out` after each pass of the loop. On"
     " which passes does `out` stay the same?",
 ],
 "answer": c('''
VOWELS = ["a", "e", "i", "o", "u"]


def remove_vowels(text):
    # start with no characters
    out = ⟦""⟧
    # look at each character, and keep it only when it is not a vowel
    for ch in text:
        if ⟦ch not in VOWELS⟧:
            out = ⟦out + ch⟧
    # give the new string back
    return out
'''),
 "after": [
     "A space is not in `VOWELS`, so every space is added to `out` and the words stay "
     "apart.",
 ],
 "further": "Make the function take out capital vowels as well, so that "
            "`remove_vowels(\"I AM LOUD\")` returns `\" M LD\"`.",
 "facts": ['"".join(ch for ch in "I AM LOUD" if ch not in "aeiouAEIOU") == " M LD"']},

{"title": "Rock Paper Scissors!", "rank": "8 kyu",
 "url": "https://www.codewars.com/kata/5672a98bdbdd995fad00000f",
 "uses": "a dictionary lookup and a flat `if`, `elif`, `else` (session 6)",
 "task": [
     "Write a function `rps(move1, move2)`. Each move is `\"rock\"`, `\"paper\"` or "
     "`\"scissors\"`. Rock beats scissors, scissors beats paper, and paper beats rock.",
     "The function returns `\"Player 1 won!\"` when `move1` beats `move2`, "
     "`\"Player 2 won!\"` when `move2` beats `move1`, and `\"Draw!\"` when the two moves "
     "are the same.",
 ],
 "tests": c('''
print(rps("rock", "scissors"))
print(rps("scissors", "rock"))
print(rps("paper", "paper"))
print(rps("paper", "rock"))
'''),
 "want": ['"Player 1 won!"', '"Player 2 won!"', '"Draw!"', '"Player 1 won!"'],
 "hints": [
     "Session 6 kept the rules in a dictionary: each key beats its value. `BEATS = "
     "{\"rock\": \"scissors\", \"paper\": \"rock\", \"scissors\": \"paper\"}`.",
     "Check for a draw first. Then look up `move1` in the dictionary: that gives the"
     " move it beats.",
     "Work the second test line by hand, `rps(\"scissors\", \"rock\")`: what does "
     "the dictionary give for `\"scissors\"`? Is that the same as `move2`? Who won?",
 ],
 "answer": c('''
# the rules: each key beats its value
BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}


def rps(move1, move2):
    # the same move twice: nobody wins
    if ⟦move1 == move2⟧:
        return "Draw!"
    # does move1 beat move2?
    elif ⟦BEATS[move1] == move2⟧:
        return ⟦"Player 1 won!"⟧
    # the only case left
    else:
        return ⟦"Player 2 won!"⟧
'''),
 "after": [
     "The function has three gates in one flat chain. Without the dictionary it would "
     "need a gate for each of the nine pairs of moves.",
 ],
 "facts": ["3 * 3 == 9"]},

{"title": "Count characters in your string", "rank": "6 kyu",
 "url": "https://www.codewars.com/kata/52efefcbcdf57161d4000091",
 "uses": "building a dictionary one key at a time, with `.get` (session 3)",
 "task": [
     "Write a function `count_characters(text)`. It returns a dictionary. Each key is a "
     "character of `text`, and its value is how many times that character is in `text`.",
     "For the empty string it returns an empty dictionary.",
 ],
 "tests": c('''
print(count_characters("aba"))
print(count_characters("banana"))
print(count_characters(""))
'''),
 "want": ['{"a": 2, "b": 1}', '{"b": 1, "a": 3, "n": 2}', "{}"],
 "hints": [
     "The counts go in a dictionary: each character is a key, and its count is the "
     "value. Start with an empty dictionary.",
     "Adding 1 to a count that is not in the dictionary yet gives a `KeyError`. "
     "Session 3 used a dictionary method that gives a value you choose for a missing"
     " key, with no error.",
     "Work the first test line by hand, `\"aba\"`: write the dictionary after each "
     "pass of the loop. What is different about the third pass, when a comes up "
     "again?",
 ],
 "answer": c('''
def count_characters(text):
    # start with no counts
    counts = ⟦{}⟧
    # look at each character, and add 1 to its count
    for ch in text:
        counts[ch] = ⟦counts.get(ch, 0) + 1⟧
    # give the dictionary back
    return counts
'''),
 "after": [
     "The first time a character is seen, `counts.get(ch, 0)` gives 0, so the "
     "character is stored with the value 1. Every time after that, `.get` gives the "
     "value stored so far and the line adds 1 to it.",
 ]},

{"title": "Rot13", "rank": "5 kyu",
 "url": "https://www.codewars.com/kata/530e15517bc88ac656000716",
 "uses": "`ord`, `chr` and `% 26` from the Caesar cipher (session 3)",
 "task": [
     "Rot13 is a Caesar cipher with the key 13: each letter is replaced by the letter "
     "13 places after it in the alphabet, going back to a after z.",
     "Write a function `rot13(text)`. It takes a string of small letters and spaces. "
     "It returns the string with every letter moved 13 places. Spaces stay as they are.",
 ],
 "tests": c('''
print(rot13("hello"))
print(rot13("attack at dawn"))
print(rot13(rot13("attack at dawn")))
'''),
 "want": ['__import__("codecs").encode("hello", "rot13")',
          '__import__("codecs").encode("attack at dawn", "rot13")',
          '"attack at dawn"'],
 "hints": [
     "This is `shift_by` from session 3 with the amount always 13.",
     "A letter takes three steps: change it to its position in the alphabet, move "
     "the position, and change the position back to a letter. `ord` and `chr` do the"
     " changing, and `%` goes back to the start after z.",
     "Work the letter h by hand. `ord(\"h\")` is 104 and `ord(\"a\")` is 97. What is"
     " the position of h? Where does it move to? Which letter is that?",
 ],
 "answer": c('''
def rot13(text):
    # start with no characters
    out = ""
    # look at each character
    for ch in text:
        # a space stays a space
        if ⟦ch == " "⟧:
            out = out + " "
        else:
            # change the letter to its position, counting a as 0
            spot = ⟦ord(ch) - ord("a")⟧
            # move 13 places, going back to the start after z
            spot = ⟦(spot + 13) % 26⟧
            # change the position back to a letter
            out = out + ⟦chr(spot + ord("a"))⟧
    # give the new string back
    return out
'''),
 "after": [
     "The third test line uses `rot13` twice and gets the first message back. Moving "
     "13 places and then 13 more is 26 places, and the alphabet has 26 letters, so "
     "every letter ends where it started.",
 ],
 "further": "Make capital letters move 13 places as well and stay capital, so that "
            "`rot13(\"Hello\")` returns `\"Uryyb\"`.",
 "facts": ["13 + 13 == 26", 'ord("h") == 104', 'ord("a") == 97',
           'chr((104 - 97 + 13) % 26 + 97) == "u"',
           '__import__("codecs").encode("Hello", "rot13") == "Uryyb"']},
]


# ------------------------------------------------------------------ running

def run(source):
    """Run one program as FILE_NAME and return (stdout, stderr)."""
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, FILE_NAME), "w") as f:
            f.write(source)
        env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
        env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
        r = subprocess.run([sys.executable, FILE_NAME], cwd=d, env=env,
                           capture_output=True, text=True, timeout=5)
    return r.stdout.rstrip("\n"), r.stderr.strip()


def check_rules(label, source):
    """The course's code rules: flat gates, no break, every def before the work."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Break, ast.Continue, ast.Try, ast.Lambda, ast.Global,
                             ast.ListComp, ast.DictComp, ast.GeneratorExp, ast.While)):
            raise AssertionError(f"{label}: uses {type(node).__name__}")
        if isinstance(node, ast.If) and any(
            isinstance(n, ast.If) for s in node.body for n in ast.walk(s)
        ):
            raise AssertionError(f"{label}: a gate inside a gate")
    seen_work = False
    for stmt in tree.body:
        if isinstance(stmt, ast.FunctionDef):
            assert not seen_work, f"{label}: a def comes after a line that does work"
        elif not isinstance(stmt, ast.Assign):
            seen_work = True


MARK = re.compile(r"⟦(.+?)⟧")
BLANK = "____"
LEVELS = 3  # hints per problem
CONTROL = ("for", "if", "elif", "else", "return")


def answer_of(p):
    """The answer as it is run: the marked text with the marks taken off."""
    return MARK.sub(lambda m: m.group(1), p["answer"])


def function_lines(p):
    """The lines of the answer from the def line on."""
    lines = answer_of(p).rstrip("\n").split("\n")
    start = next(i for i, ln in enumerate(lines) if ln.startswith("def "))
    return lines[start:]


def control_words(p):
    """The control words this function has, in the order of CONTROL."""
    firsts = {ln.strip().rstrip(":").split(" ")[0] for ln in function_lines(p)}
    return [w for w in CONTROL if w in firsts]


def _shape(line, level):
    """One line of the answer as hint 1 or hint 2 shows it."""
    body = line.strip()
    pad = line[: len(line) - len(line.lstrip(" "))]
    # the def line, plan comments, blank lines and lists kept above the def all show
    if not body or body.startswith(("def ", "#")) or not pad:
        return line
    if level == 2:
        if body == "else:":
            return line
        for word in ("for", "if", "elif"):
            if body.startswith(word + " "):
                return f"{pad}{word} {BLANK}:"
        if body.startswith("return "):
            return f"{pad}return {BLANK}"
    return pad + BLANK


def blanked(p, level):
    """The function as hint level shows it."""
    if level == LEVELS:
        return MARK.sub(BLANK, p["answer"]).rstrip("\n")
    return "\n".join(_shape(ln, level) for ln in answer_of(p).rstrip("\n").split("\n"))


def count_blanks(p, level):
    return blanked(p, level).count(BLANK)


def _words(words):
    coded = [f"<code>{w}</code>" for w in words]
    if len(coded) == 1:
        return "word " + coded[0] + " is"
    return "words " + ", ".join(coded[:-1]) + " and " + coded[-1] + " are"


def caption(p, level):
    """What this hint's code shows, said from this problem's own function."""
    n = count_blanks(p, level)
    if level == 1:
        lines = "The one line of code is a blank." if n == 1 else \
            "Every line of code under the <code>def</code> line is a blank."
        return f"Here is the plan, written as comments. {lines}"
    if level == 2:
        return (f"Here the {_words(control_words(p))} filled in. Everything else "
                "on a line of code is a blank.")
    left = "one blank" if n == 1 else f"{n} blanks"
    return (f"Here the function is filled in except for {left}. Work out "
            + ("that part" if n == 1 else "those parts") + " yourself.")


def hidden(p, level):
    """How many characters of the answer a hint leaves out."""
    shown = blanked(p, level).replace(BLANK, "")
    return len(re.sub(r"\s", "", answer_of(p))) - len(re.sub(r"\s", "", shown))


def check_blanks(label, p):
    assert len(p["hints"]) == LEVELS, f"{label}: needs {LEVELS} written hints"
    assert BLANK not in answer_of(p) and "⟦" not in answer_of(p), f"{label}: a mark did not parse"
    marks = MARK.findall(p["answer"])
    assert marks, f"{label}: no part of the answer is marked to stay blank"
    assert any(ln.strip().startswith("#") for ln in function_lines(p)), \
        f"{label}: the function has no plan comment"
    # the last hint fills back to the answer that is run
    text = blanked(p, LEVELS)
    for piece in marks:
        text = text.replace(BLANK, piece, 1)
    assert text == answer_of(p).rstrip("\n"), f"{label}: hint {LEVELS} does not fill back to the answer"
    # no marked part shows in any hint (a piece of one or two characters, such as n
    # or 0, is skipped: it also turns up inside names; hint 3's fill-back covers those)
    for k in range(1, LEVELS + 1):
        for piece in marks:
            assert len(piece) < 3 or piece not in blanked(p, k), \
                f"{label}: hint {k} shows {piece!r}"
    # each hint hides less than the one before, and the last still hides something
    sizes = [hidden(p, k) for k in range(1, LEVELS + 1)]
    assert sizes == sorted(set(sizes), reverse=True) and sizes[-1] > 0, \
        f"{label}: hints must hide less each time, got {sizes}"
    # what the words say has to be true of this function
    has = control_words(p)
    said = p["hints"] + [ln for ln in function_lines(p) if ln.strip().startswith("#")]
    for text in said:
        low = re.sub(r"`[^`]*`", " ", text).lower()
        if re.search(r"\b(loop|pass|passes)\b", low):
            assert "for" in has, f"{label}: says loop or pass, but the function has no for: {text!r}"
        if re.search(r"\bgate\b", low) and "no gate" not in low:
            assert "if" in has, f"{label}: says gate, but the function has no if: {text!r}"
        for word in re.findall(r"`(for|if|elif|else|return)`", text):
            assert word in has, f"{label}: names `{word}`, which the function does not use: {text!r}"
    for k in range(1, LEVELS + 1):
        for word in re.findall(r"<code>(for|if|elif|else|return)</code>", caption(p, k)):
            assert word in has, f"{label}: hint {k} caption names {word}"
        # the caption's count of blanks is the count in the code under it
        assert count_blanks(p, k) > 0, f"{label}: hint {k} has no blank"
    # hint 2 shows every control word the function has
    two = blanked(p, 2)
    for word in has:
        assert re.search(rf"^\s+{word}\b", two, re.M), f"{label}: hint 2 does not show {word}"


def program(p):
    return answer_of(p).rstrip("\n") + "\n\n" + p["tests"]


def run_problem(n, p):
    """Run the answer with its test lines, check every printed line, return the output."""
    label = f"problem {n} ({p['title']})"
    check_blanks(label, p)
    check_rules(label, program(p))
    out, err = run(program(p))
    assert not err, f"{label}: the answer stops with an error:\n{err}"
    lines = out.split("\n")
    tests = p["tests"].strip().split("\n")
    assert len(lines) == len(tests) == len(p["want"]), f"{label}: tests, wants and output differ in number"
    for test, got, want in zip(tests, lines, p["want"]):
        expected = str(eval(want, {}))
        assert got == expected, f"{label}: {test} printed {got!r}, the second way gives {expected!r}"
    for fact in p.get("facts", []):
        assert eval(fact, {}) is True, f"{label}: fact is not True: {fact}"
    return out


def verify():
    """Run every answer again and return how many ran. Used by crosscheck.py."""
    for n, p in enumerate(PROBLEMS, 1):
        run_problem(n, p)
    return len(PROBLEMS)


# ------------------------------------------------------------------ the page

def fmt(text):
    """Escape, then `code` -> <code>, **term** -> <b>."""
    t = html.escape(text, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return t


def hint_ladder(p, answer, slug):
    """Hints that open one inside the other, with the answer inside the last hint.

    Each hint shows the function with blanks, fewer in each hint than the one before.
    """
    hints = p["hints"]
    aid = f"cw-{slug}-answer"
    inner = (
        f'<button class="rev" data-target="{aid}" data-show="Show the answer" '
        f'data-hide="Hide the answer" aria-expanded="false" aria-controls="{aid}">'
        "Show the answer</button>\n"
        f'<div class="ans" id="{aid}">{answer}</div>\n'
    )
    for k in range(len(hints), 0, -1):
        hid = f"cw-{slug}-{k}"
        inner = (
            f'<button class="rev" data-target="{hid}" data-show="Hint {k}" '
            f'data-hide="Hide hint {k}" aria-expanded="false" aria-controls="{hid}">'
            f"Hint {k}</button>\n"
            f'<div class="ans" id="{hid}"><p>{fmt(hints[k - 1])}</p>'
            f"{blank_block(p, k)}{inner}</div>\n"
        )
    return ('<div class="predict ladder"><b>Stuck?</b> Open one hint. Fill in what you '
            "can and run your file. Open the next hint only if you are still stuck. "
            f"Every hint shows the function with blanks, written <code>{BLANK}</code>, "
            f"for you to work out. The answer is inside the last hint.\n{inner}</div>\n")


def blank_block(p, level):
    """The function as this hint shows it, under a line that says what is filled in."""
    return f"<p>{caption(p, level)}</p>" + code(blanked(p, level))


def problem_html(n, p):
    out = run_problem(n, p)
    answer = (
        code(program(p), FILE_NAME) + output(out)
        + "".join(f"<p>{fmt(t)}</p>" for t in p["after"])
    )
    b = (
        f"<h2>{n}. {html.escape(p['title'])}</h2>\n"
        f'<p>From Codewars: <a href="{p["url"]}">{html.escape(p["title"])}</a>, '
        f'{p["rank"]}. Uses {fmt(p["uses"])}.</p>\n'
        + "".join(f"<p>{fmt(t)}</p>" for t in p["task"])
        + "<p>Put these test lines under your function. A function that works prints "
        "the target output.</p>\n"
        + code(p["tests"])
        + output(out, label="target output")
        + hint_ladder(p, answer, str(n))
    )
    if p.get("further"):
        b += f"<p><b>Go further.</b> {fmt(p['further'])}</p>\n"
    return b


def teacher_panel():
    rows = "".join(
        f'<tr><td>{n}</td><td>{html.escape(p["title"])}</td><td>{p["rank"]}</td>'
        f'<td>{fmt(p["uses"])}</td></tr>'
        for n, p in enumerate(PROBLEMS, 1)
    )
    return (
        '<section class="panel"><h2>Teacher panel</h2>'
        "<h3>How to use it</h3><ul>"
        "<li>For a student who finishes a build early, or for the whole room as "
        "practice. Nothing later in the course depends on this page.</li>"
        "<li>The problems run from the shortest to the longest. Problems 1 to 5 need "
        "sessions 1 to 3 and <code>%</code>. Problems 6 to 10 need sessions 3 and 6.</li>"
        "<li>Students work in VS Code. Nobody needs a Codewars account. The link on "
        "each problem goes to the kata it came from.</li>"
        "<li>The target output is shown openly, so a student can check their own "
        "function.</li>"
        "<li>Each problem has three hints, from the most general to the most "
        "specific, and every hint shows the function with blanks. Hint 1 gives the "
        "idea, then the plan as comments with a blank for every line of code. Hint 2 "
        "says how the idea is used, then fills in the control words the function "
        "has, such as <code>if</code> and <code>return</code>. Hint 3 gives a case to "
        "work by hand, then fills in the names.</li>"
        "<li>No hint shows a condition or the value a line works out. Those stay "
        "blank until the answer, so the student still has to do the thinking. The "
        "answer is inside the third hint.</li>"
        "<li>Ask for a try between hints: fill in what you can, run the file, and "
        "open the next hint only if still stuck.</li>"
        "</ul>"
        "<h3>What each problem uses</h3>"
        '<div style="overflow-x:auto"><table style="min-width:600px; table-layout:auto">'
        "<thead><tr><th>#</th><th>Kata</th><th>Rank</th><th>Uses</th></tr></thead>"
        f"<tbody>{rows}</tbody></table></div>"
        "<p>On Codewars, kyu is the rank of a kata: 8 kyu is the most basic and the "
        "numbers go down as the kata get harder.</p>"
        "<h3>Why the hints are built this way</h3><ul>"
        "<li>General first, specific last. Tutoring systems order their hint levels "
        "from the principle that applies down to a last hint that gives the step "
        '(<a href="https://pslcdatashop.web.cmu.edu/KDDCup/FAQ/Koedinger-Aleven-EPR-07.pdf">'
        "Koedinger and Aleven, 2007</a>).</li>"
        "<li>Control words shown, conditions and values blank. Faded Parsons Problems "
        "never blank the top-level control words and do blank conditions, constants "
        'and expressions (<a href="https://acelab.berkeley.edu/wp-content/papercite-data/pdf/parsons-chi2021.pdf">'
        "Weinman, Fox and Hearst, 2021</a>).</li>"
        "<li>The plan as comments. Subgoal labels are short phrases that say what a "
        "group of lines is for, and worked examples that carry them helped new "
        'programmers (<a href="https://www.raspberrypi.org/app/uploads/2020/07/Using-subgoal-labels-to-reduce-cognitive-load-in-introductory-programming.pdf">'
        "Margulieux, Morrison and Decker</a>).</li>"
        "<li>A case to work by hand before the last blanks. Students who finished "
        "part-written programs built programs better than students who wrote from "
        "nothing, but the study did not show they understood the patterns they used "
        '(<a href="https://research.utwente.nl/en/publications/strategies-for-programming-instruction-in-high-school-program-com/">'
        "van Merri&euml;nboer, 1990</a>). Students also often click through to the last "
        'hint (<a href="https://learnlab.org/research/wiki/index.php/Help_abuse">'
        "Aleven and others, 2006</a>), which is why each hint asks for a try before the "
        "next.</li></ul>"
        "<h3>Where the wording comes from</h3>"
        "<p>The kata titles, ranks and links were read from codewars.com on 25 November "
        "2026. The task wording, function names, test lines and answers on this page are "
        "this course's own, written to use only what sessions 1 to 7 taught. A kata's "
        "own tests on Codewars can ask for a different function name or more cases, so "
        "an answer from this page may need changes before it passes there.</p>"
        "</section>\n"
    )


def extra_codewars():
    """Extra page: ten Codewars kata that fit what sessions 1 to 7 taught."""
    b = masthead(
        None,
        TITLE,
        "Any time after session 6",
        "Ten short problems, each one a function to write. Every problem can be solved "
        "with what you have learned in sessions 1 to 7.",
        time=None,
        length="10 problems",
        eyebrow="Advanced Python &middot; Fall 2026 &middot; Extra",
    )
    b += (
        "<p>Codewars is a website of coding problems. It calls each problem a "
        "<b>kata</b>. These ten were picked from it.</p>"
        "<ol><li>Read the problem. Write the function in VS Code, in a file named with "
        "your first name, like <code>Jonathan_even_or_odd.py</code>.</li>"
        "<li>Put the test lines under your function and run the file.</li>"
        "<li>Compare what your file prints with the target output. If a line is "
        "different, read your function one line at a time before you change it.</li></ol>"
    )
    for n, p in enumerate(PROBLEMS, 1):
        b += problem_html(n, p)
    b += teacher_panel()
    b += '<nav class="pager"><a href="advanced_python_hub.html">Course hub</a></nav>\n'
    return b
