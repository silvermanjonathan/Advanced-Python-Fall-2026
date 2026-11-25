"""Review for Advanced Python Fall 2026. Writes advanced_python_review.html.

A short review in two parts. Each part is a 10 minute opener for the start of a
class session, so the review never takes a whole session. The questions are weighted
by the assessment result in WEIGHTS below: the topics with the most wrong answers get
the most questions, and dictionaries, the weakest topic, come back in part 2.

Every program here is run with real Python when the page is built, as FILE_NAME, and
the output boxes are what the run printed. In an explanation, [[text]] marks a quoted
output line (or an error's name): the build stops unless that text is a real line of
a run on that question. Each question can also list facts, small Python expressions
that back a number the prose states, and the build stops if one is False.
crosscheck.py runs every program again through verify().

Edit the questions here, never in the .html.
"""

import ast
import html
import os
import re
import subprocess
import sys
import tempfile

from build import code, masthead, output, reveal

OUT_NAME = "advanced_python_review.html"
TITLE = "Review for Advanced Python Fall 2026"
FILE_NAME = "Jonathan_review.py"

# Installed as sitecustomize so the typed answer appears after the input() prompt,
# the way a terminal shows it. Piped input does not echo on its own.
ECHO_INPUT = '''
import builtins
import sys as _sys
def _echo_input(prompt=""):
    answer = _sys.stdin.readline().rstrip("\\n")
    print(str(prompt) + answer)
    return answer
builtins.input = _echo_input
'''


def c(text):
    return text[1:] if text.startswith("\n") else text


# ------------------------------------------------------------------ the result
# The assessment result this review was built from, one row per quiz round:
# (round id, title, right, asked, sure but wrong, what the wrong answers were about).
WEIGHTS = [
    ("dicts", "Dictionaries", 1, 4, 3,
     "changing and adding a pair, a key that does not match, what `in` checks"),
    ("remainders", "Remainders", 2, 4, 2,
     "what `%` gives, and using it to go round a list again"),
    ("functions", "Functions", 3, 5, 2,
     "`print` or `return`, and the order of the values in a call"),
    ("strings", "Strings", 3, 5, 1,
     "index numbers and slices, and storing what `strip` or `replace` makes"),
    ("types", "Input and types", 3, 5, 2,
     "`input` gives text, so `+` joins"),
    ("gates", "Comparisons and if", 3, 4, 1,
     "the first condition that is True wins"),
    ("loops", "for loops and range", 3, 4, 1,
     "adding up a total in a loop"),
    ("names", "Printing and names", 3, 4, 1,
     "capital and small letters make different names"),
    ("andor", "and, or, and while", 4, 5, 1,
     "the order of the lines in a `while` loop"),
    ("lists", "Lists", 4, 5, 1,
     "an index number past the end of a list"),
    ("errors", "Reading errors", 5, 6, 1,
     "calling a function above its `def`"),
]

# ------------------------------------------------------------------ the questions
# topic    shown above the question
# patches  the round ids in WEIGHTS this question works on
# ask      the prediction question
# code     the program; stdin is what is typed when it asks
# explain  paragraphs shown with the real output
# then     optional second program: lead (text before it), code, after (text under it)
# facts    Python expressions that must be True
# allow    code rules this program breaks on purpose

PARTS = [
{"id": "part1", "name": "Part 1", "focus": "Dictionaries, remainders and strings",
 "questions": [

 {"topic": "Dictionaries", "patches": ["dicts"],
  "ask": "A dictionary holds pairs: a **key** and the **value** stored under it. "
         "What two lines does this program print?",
  "code": c('''
prices = {"pen": 2, "cup": 5}
prices["cup"] = 6
prices["hat"] = 9
print(prices["cup"])
print(len(prices))
'''),
  "explain": [
      "Line 2 uses the key `\"cup\"`, which is already in the dictionary, so the value "
      "stored under it changes from 5 to 6. Line 4 prints [[6]].",
      "Line 3 uses the key `\"hat\"`, which is not in the dictionary yet, so Python adds "
      "a new pair. `len` counts the pairs. There were 2 and line 3 added one more, so "
      "line 5 prints [[3]].",
      "**`prices[key] = value` changes the value when the key is already there, and "
      "adds a new pair when it is not.**",
  ]},

 {"topic": "Dictionaries", "patches": ["dicts", "names"],
  "ask": "Does this program stop with an error? If it does, say the error's name.",
  "code": c('''
prices = {"pen": 2, "cup": 5}
print(prices["Cup"])
'''),
  "explain": [
      "The dictionary has the key `\"cup\"` with a small c. Line 2 asks for `\"Cup\"` "
      "with a capital C. Python treats capital and small letters as different, so "
      "there is no such key and the program stops with a [[KeyError]].",
      "The last line of the error message shows the key Python could not find: "
      "[[KeyError: 'Cup']]",
      "**A key has to match exactly, capital letters included.** Variable names work "
      "the same way: `score` and `Score` are two different names.",
  ]},

 {"topic": "Dictionaries", "patches": ["dicts"],
  "ask": "`in` asks a yes or no question about a dictionary. What two lines does this "
         "program print?",
  "code": c('''
prices = {"pen": 2, "cup": 5}
print(2 in prices)
print("pen" in prices)
'''),
  "explain": [
      "With a dictionary, `in` looks at the keys only. The keys are `\"pen\"` and "
      "`\"cup\"`. The number 2 is a value, not a key, so line 2 prints [[False]].",
      "`\"pen\"` is a key, so line 3 prints [[True]].",
      "**`in` checks the keys of a dictionary, not the values.**",
  ]},

 {"topic": "Remainders", "patches": ["remainders"],
  "ask": "`%` gives the **remainder**: what is left over after dividing. What three "
         "lines does this program print?",
  "code": c('''
print(14 % 4)
print(12 % 4)
print(3 % 7)
'''),
  "explain": [
      "Three 4s fit into 14 and make 12, with 2 left over, so line 1 prints [[2]].",
      "Three 4s fit into 12 with nothing left over, so line 2 prints [[0]].",
      "No 7 fits into 3, so all of the 3 is left over and line 3 prints [[3]].",
      "**When the first number is smaller than the second, the remainder is the first "
      "number.**",
  ],
  "facts": ["3 * 4 == 12", "14 - 12 == 2"]},

 {"topic": "Remainders and lists", "patches": ["remainders", "lists"],
  "ask": "The list has two names, at index 0 and index 1. The loop makes five passes. "
         "What does the program print?",
  "code": c('''
team = ["Ada", "Mo"]
for turn in range(5):
    print(team[turn % 2])
'''),
  "explain": [
      "`turn` counts 0, 1, 2, 3, 4. `turn % 2` changes those numbers into 0, 1, 0, 1, 0. "
      "The index number never goes past 1, so the two names take turns.",
  ],
  "then": {
      "lead": "Without `% 2`, the third pass asks for `team[2]`:",
      "code": c('''
team = ["Ada", "Mo"]
for turn in range(5):
    print(team[turn])
'''),
      "after": [
          "The error's name is [[IndexError]]. A list with 2 items has index 0 and "
          "index 1, and no index 2.",
          "**The last index number of a list is one less than its length.**",
      ]},
  "facts": ["[turn % 2 for turn in range(5)] == [0, 1, 0, 1, 0]",
            "list(range(5)) == [0, 1, 2, 3, 4]"]},

 {"topic": "Strings", "patches": ["strings", "loops"],
  "ask": "Each letter of a string has an index number, starting at 0. What two lines "
         "does this program print?",
  "code": c('''
word = "planet"
print(word[0])
print(word[2:5])
'''),
  "explain": [
      "Index 0 is the first letter, so line 2 prints [[p]].",
      "`word[2:5]` is a **slice**. It starts at index 2 and stops before index 5. That "
      "is index 2, 3 and 4: the letters a, n and e. Line 3 prints [[ane]]. The letter "
      "at index 5, t, is left out.",
      "**A slice includes its first index number and stops before its second.** "
      "`range(2, 5)` counts the same way: 2, 3, 4.",
  ],
  "facts": ["'planet'[5] == 't'", "list(range(2, 5)) == [2, 3, 4]",
            "['planet'[i] for i in (2, 3, 4)] == ['a', 'n', 'e']"]},

 {"topic": "Strings", "patches": ["strings"],
  "ask": "Line 2 replaces a letter. What does line 3 print?",
  "code": c('''
word = "cool"
word.replace("c", "p")
print(word)
'''),
  "explain": [
      "`replace` makes a new string, `\"pool\"`, and leaves `word` as it was. Line 2 "
      "does not store the new string under any name, so it is lost. Line 3 prints "
      "[[cool]].",
  ],
  "then": {
      "lead": "To keep the new string, store it under the name:",
      "code": c('''
word = "cool"
word = word.replace("c", "p")
print(word)
'''),
      "after": [
          "Now line 3 prints [[pool]].",
          "**`replace` and `strip` make a new string. Store it, or it is lost.**",
      ]},
  "facts": ["'cool'.replace('c', 'p') == 'pool'"]},
 ]},

{"id": "part2", "name": "Part 2", "focus": "Dictionaries again, functions, input, if and loops",
 "questions": [

 {"topic": "Dictionaries", "patches": ["dicts"],
  "ask": "`tally` starts as an empty dictionary. The loop looks at one vote on each "
         "pass. What two lines does the program print?",
  "code": c('''
votes = ["cat", "dog", "cat", "cat"]
tally = {}
for v in votes:
    if v in tally:
        tally[v] = tally[v] + 1
    else:
        tally[v] = 1
print(tally["cat"])
print(len(tally))
'''),
  "explain": [
      "On the first pass `\"cat\"` is not a key yet, so line 7 adds it with the value 1. "
      "On the second pass line 7 adds `\"dog\"` the same way. On the third and fourth "
      "passes `\"cat\"` is already a key, so line 5 adds 1 to its value: 2, then 3. "
      "Line 8 prints [[3]].",
      "The dictionary ends with two keys, `\"cat\"` and `\"dog\"`, so line 9 prints "
      "[[2]]. Four votes went in, but each key is stored once and `len` counts the keys.",
  ],
  "facts": ["['cat', 'dog', 'cat', 'cat'].count('cat') == 3",
            "len(set(['cat', 'dog', 'cat', 'cat'])) == 2"]},

 {"topic": "Functions", "patches": ["functions"],
  "ask": "The function prints, but it has no `return` line. What two lines does the "
         "program print?",
  "code": c('''
def add_one(n):
    print(n + 1)

result = add_one(4)
print(result)
'''),
  "explain": [
      "Line 4 calls the function, and line 2 prints [[5]].",
      "The function has no `return` line, so the call gives the value `None`. That is "
      "what line 4 stores in `result`, and line 5 prints [[None]].",
  ],
  "then": {
      "lead": "With `return` in place of `print`, the call gives the value 5 to line 4:",
      "code": c('''
def add_one(n):
    return n + 1

result = add_one(4)
print(result)
'''),
      "after": [
          "**`print` shows a value on the screen. `return` gives a value to the line "
          "that called the function, so that line can store it or use it.**",
      ]}},

 {"topic": "Functions", "patches": ["functions"],
  "ask": "Look at the order of the two values in the call on line 4. What does the "
         "program print?",
  "code": c('''
def ticket(name, seat):
    return f"{name} sits in {seat}"

print(ticket(12, "Mo"))
'''),
  "explain": [
      "Python matches the values in the call to the parameters by position. The first "
      "value, 12, goes to `name`. The second value, `\"Mo\"`, goes to `seat`. The "
      "program prints [[12 sits in Mo]].",
      "Python gives no error message here, because every line is allowed. The mistake "
      "shows only in the output.",
      "**The first value in a call goes to the first parameter, the second value to the "
      "second parameter.**",
  ]},

 {"topic": "Functions", "patches": ["functions", "errors"],
  "ask": "Does this program stop with an error? If it does, say the error's name.",
  "code": c('''
print(square(3))

def square(n):
    return n * n
'''),
  "allow": ["def after work"],
  "explain": [
      "Python runs a file from the top. Line 1 calls `square` before Python has reached "
      "the `def` on line 3, so the name `square` has no value yet. The program stops "
      "with a [[NameError]].",
      "**Every `def` goes at the top of the file, before any line that does work.**",
  ]},

 {"topic": "Input and types", "patches": ["types"],
  "ask": "The person types 4 and presses Enter. What does line 2 print?",
  "stdin": "4",
  "code": c('''
laps = input("Laps: ")
print(laps + laps)
'''),
  "explain": [
      "`input` gives text, even when the person types digits. `laps` holds the text "
      "`\"4\"`. With two pieces of text, `+` joins them end to end, so line 2 prints "
      "[[44]].",
  ],
  "then": {
      "lead": "To add, change the type to a whole number with `int`:",
      "stdin": "4",
      "code": c('''
laps = input("Laps: ")
laps = int(laps)
print(laps + laps)
'''),
      "after": [
          "Now `+` adds two numbers, and line 3 prints [[8]].",
          "**`input` gives text. Change the type with `int` before doing arithmetic.**",
      ]}},

 {"topic": "Comparisons and if", "patches": ["gates"],
  "ask": "35 is more than 20 and more than 30. What does the program print?",
  "code": c('''
temp = 35
if temp > 20:
    print("warm")
elif temp > 30:
    print("hot")
else:
    print("cold")
'''),
  "explain": [
      "Python checks the conditions from the top and runs the lines under the first one "
      "that is True. `temp > 20` is True, so line 3 prints [[warm]]. Python then skips "
      "the `elif` and the `else` without checking them.",
  ],
  "then": {
      "lead": "To print hot for 35, put the `temp > 30` check first:",
      "code": c('''
temp = 35
if temp > 30:
    print("hot")
elif temp > 20:
    print("warm")
else:
    print("cold")
'''),
      "after": [
          "Now the first condition that is True is `temp > 30`, and line 3 prints [[hot]].",
          "**In an `if`, `elif`, `else` chain, only the first condition that is True "
          "runs its lines.**",
      ]}},

 {"topic": "Loops and totals", "patches": ["loops", "andor"],
  "ask": "Say the value of `total` after each pass of the loop. Then say what line 6 "
         "prints.",
  "code": c('''
count = 1
total = 0
while count <= 4:
    total = total + count
    count = count + 1
print(total)
'''),
  "explain": [
      "**The value of `total` after each pass.** `total` starts at 0, and line 4 adds "
      "`count` to it on each pass: 1, then 3, then 6, then 10.",
      "**What line 6 prints.** Line 5 makes `count` one bigger on each pass. When "
      "`count` reaches 5, `count <= 4` is False and the loop stops. Line 6 prints [[10]].",
      "Without line 5, `count` would stay at 1, the condition would stay True, and the "
      "loop would never stop.",
  ],
  "facts": ["[sum(range(1, k + 1)) for k in (1, 2, 3, 4)] == [1, 3, 6, 10]"]},
 ]},
]


# ------------------------------------------------------------------ running

def run(source, stdin=None):
    """Run one program as FILE_NAME and return what a terminal would show."""
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, FILE_NAME), "w") as f:
            f.write(source if source.endswith("\n") else source + "\n")
        with open(os.path.join(d, "sitecustomize.py"), "w") as f:
            f.write(ECHO_INPUT)
        env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
        env.update(PYTHONPATH=d, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
        r = subprocess.run(
            [sys.executable, FILE_NAME], cwd=d, env=env, capture_output=True, text=True,
            input=(stdin + "\n") if stdin is not None else "", timeout=5,
        )
        err = r.stderr.replace(os.path.realpath(d) + os.sep, "").replace(d + os.sep, "")
    err = "\n".join(ln.rstrip() for ln in err.rstrip().splitlines())
    return "\n".join(part for part in (r.stdout.rstrip("\n"), err) if part)


def error_name(term):
    last = term.splitlines()[-1] if term else ""
    m = re.match(r"^([A-Za-z]+Error)\b", last)
    return m.group(1) if m else None


# ------------------------------------------------------------------ checks

def check_program(label, source, allow=()):
    """The code rules: flat gates, a loop that stops, every def at the top."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Break, ast.Continue, ast.Try, ast.Lambda, ast.Global)):
            raise AssertionError(f"{label}: uses {type(node).__name__}")
        if isinstance(node, ast.While) and isinstance(node.test, ast.Constant):
            raise AssertionError(f"{label}: while with a constant condition")
        if isinstance(node, ast.If) and any(
            isinstance(n, ast.If) for s in node.body for n in ast.walk(s)
        ):
            raise AssertionError(f"{label}: a gate inside a gate; join with and")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and \
                node.func.id == "print" and len(node.args) > 1:
            raise AssertionError(f"{label}: print with several values; use an f-string")
    seen_work = False
    for stmt in tree.body:
        if isinstance(stmt, ast.FunctionDef):
            if seen_work and "def after work" not in allow:
                raise AssertionError(f"{label}: a def comes after a line that does work")
        else:
            seen_work = True


def said(texts):
    return [m for t in texts for m in re.findall(r"\[\[(.+?)\]\]", t)]


def fmt(text):
    """Escape, then `code` and [[output line]] -> <code>, **term** -> <b>."""
    t = html.escape(text, quote=False)
    t = re.sub(r"\[\[(.+?)\]\]", r"<code>\1</code>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return t


def run_question(label, q):
    """Run a question's programs, check every claim, return (first run, second run)."""
    allow = q.get("allow", ())
    check_program(label, q["code"], allow)
    term = run(q["code"], q.get("stdin"))
    real = set(term.splitlines())
    names = {error_name(term)}
    texts = [q["ask"]] + q["explain"]
    term2 = None
    then = q.get("then")
    if then:
        check_program(label + " (second program)", then["code"], allow)
        term2 = run(then["code"], then.get("stdin"))
        real |= set(term2.splitlines())
        names.add(error_name(term2))
        texts += [then["lead"]] + then["after"]
    quotes = said(texts)
    assert quotes, f"{label}: the explanation quotes no output line"
    for quote in quotes:
        assert quote in real or quote in names, \
            f"{label}: [[{quote}]] is not a line of the real output:\n{term}"
    for fact in q.get("facts", []):
        assert eval(fact, {}) is True, f"{label}: fact is not True: {fact}"
    return term, term2


def verify():
    """Run every program again and return how many ran. Used by crosscheck.py."""
    n = 0
    for part in PARTS:
        for k, q in enumerate(part["questions"], 1):
            _, second = run_question(f"{part['id']} question {k}", q)
            n += 2 if second is not None else 1
    return n


# ------------------------------------------------------------------ the page

def question_html(part, n, q):
    term, term2 = run_question(f"{part['id']} question {n}", q)
    answer = output(term) + "".join(f"<p>{fmt(t)}</p>" for t in q["explain"])
    then = q.get("then")
    if then:
        answer += (
            f"<p>{fmt(then['lead'])}</p>" + code(then["code"]) + output(term2)
            + "".join(f"<p>{fmt(t)}</p>" for t in then["after"])
        )
    return (
        f"<h3>Question {n}: {html.escape(q['topic'])}</h3>\n"
        + code(q["code"])
        + reveal(fmt(q["ask"]), answer, show="Say your answer first, then check here")
    )


def teacher_panel():
    where = {w[0]: [] for w in WEIGHTS}
    for part in PARTS:
        for n, q in enumerate(part["questions"], 1):
            for rid in q["patches"]:
                where[rid].append(f"{part['name']} Q{n}")
    assert all(where.values()), "a topic in WEIGHTS has no review question"
    rows = "".join(
        f"<tr><td>{html.escape(title)}</td><td>{right} of {asked}</td><td>{sw}</td>"
        f"<td>{fmt(about)}</td><td>{', '.join(where[rid])}</td></tr>"
        for rid, title, right, asked, sw, about in WEIGHTS
    )
    wrong = sum(w[3] - w[2] for w in WEIGHTS)
    asked = sum(w[3] for w in WEIGHTS)
    n1, n2 = (len(p["questions"]) for p in PARTS)
    return (
        '<section class="panel"><h2>Teacher panel</h2>'
        "<h3>How to run it</h3><ul>"
        "<li>Use one part as the opener of each of two class sessions. Each part is "
        f"planned for 10 minutes: {n1} questions in part 1 and {n2} in part 2.</li>"
        "<li>For each question, students read the program and say their prediction to a "
        "neighbour. Then press the button. Nothing a program prints shows before the "
        "press.</li>"
        "<li>The questions in each part run from the weakest topic down. If time runs "
        "out, stop where you are. Part 1 questions 1 to 5 and part 2 questions 1 to 4 "
        "are the ones to finish.</li>"
        '<li>Adding <code>#part2</code> to the address opens the page at part 2.</li>'
        "</ul>"
        "<h3>Why these questions</h3>"
        f"<p>The review was built from an assessment result with {wrong} wrong answers "
        f"out of {asked}. Most of the wrong answers were given with Sure pressed, which "
        "points to a wrong idea about Python, not a guess. So every question here asks "
        "for a prediction first and then shows the real output. The programs are new, "
        "so a remembered answer from the assessment does not help.</p>"
        '<div style="overflow-x:auto"><table style="min-width:640px; table-layout:auto"><thead><tr><th>Topic</th><th>Right</th>'
        "<th>Sure but wrong</th><th>The wrong answers were about</th>"
        f"<th>Reviewed in</th></tr></thead><tbody>{rows}</tbody></table></div>"
        "<p>Dictionaries had the lowest score, so they get three questions in part 1 "
        "and come back as the first question of part 2.</p>"
        "</section>\n"
    )


def review():
    """The review page: two parts, each a 10 minute opener."""
    total = sum(len(p["questions"]) for p in PARTS)
    b = masthead(
        None,
        TITLE,
        "The first 10 minutes of two class sessions",
        "Read each program and say what it will print. Then check.",
        time=None,
        length=f"2 parts, {total} questions",
        eyebrow="Advanced Python &middot; Fall 2026 &middot; Review",
    )
    b += (
        "<ol><li>Read the program. Go one line at a time, top to bottom.</li>"
        "<li>Say what it will print to the person next to you.</li>"
        "<li>Press the button to see what Python really printed, and why.</li></ol>"
    )
    for i, part in enumerate(PARTS, 1):
        b += (
            f'<h2><span class="num">{i}</span>{part["name"]}: '
            f'{html.escape(part["focus"])}<span class="mins">10 minutes</span></h2>'
            f'<p id="{part["id"]}">{len(part["questions"])} questions. No new syntax.</p>'
        )
        for n, q in enumerate(part["questions"], 1):
            b += question_html(part, n, q)
    b += teacher_panel()
    b += '<nav class="pager"><a href="advanced_python_hub.html">Course hub</a></nav>\n'
    return b
