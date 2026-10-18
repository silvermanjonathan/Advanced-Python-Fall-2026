"""Check every output and error message quoted on the session 5 page.

The page's code blocks for the trace rounds, the quick check, the gate, and the broken
pets are the strings in SNIPPETS below; the page generator reads them from this file,
so the code on the page and the code run here cannot drift apart. Rounds run with the
Pet class from pets.py in front of them. Broken pets run in a separate Python, and the
last line of the error is printed, which is the line a student sees in the terminal.
"""

import subprocess
import sys

SNIPPETS = {
    "empty": '''class Pet:
    pass''',
    "first": '''class Pet:
    def __init__(self, name):
        self.name = name


rocky = Pet("Rocky")
print(rocky.name)''',
    "stats": '''class Pet:
    def __init__(self, name):
        self.name = name
        self.hunger = 5
        self.happiness = 5


rocky = Pet("Rocky")
print(rocky.name, rocky.hunger, rocky.happiness)''',
    "report": '''rocky = Pet("Rocky")
rocky.report()
print(rocky.report())''',
    "round1": '''a = Pet("Mochi")
b = Pet("Pixel")

a.feed()
a.feed()
a.feed()
b.play()
b.play()

print(a.report())
print(b.report())''',
    "round2": '''a = Pet("Mochi")

for i in range(7):
    a.feed()
    a.play()

print(a.report())''',
    "round3": '''a = Pet("Mochi")
b = a

b.feed()
b.feed()

print(a.report())
print(b.report())''',
    "check": '''rocky = Pet("Rocky")
luna = Pet("Luna")

rocky.feed()
rocky.feed()

print(luna.hunger)''',
    "gate": '''    def feed(self):
        """Make this pet 1 less hungry, but never below 0."""
        if self.hunger > 0:
            self.hunger = self.hunger - 1''',
    "broken1": '''class Pet:
    def __init__(self, name):
        self.name = name
        self.hunger = 5

    def feed():
        self.hunger = self.hunger - 1


rocky = Pet("Rocky")
rocky.feed()''',
    "broken2": '''class Pet:
    def __init__(self, name):
        self.name = name
        self.hunger = 5

    def feed(self):
        hunger = hunger - 1


rocky = Pet("Rocky")
rocky.feed()''',
    "broken3": '''rocky = Pet("Rocky")
Pet.feed()''',
    "broken4": '''rocky = Pet
print(rocky.name)''',
    "broken5": '''rocky = Pet("Rocky")
rocky.feed(rocky)''',
    "broken6": '''class Pet:
    def _init_(self, name):
        self.name = name
        self.hunger = 5


rocky = Pet("Rocky")''',
}

# the class from pets.py, without the two pets it makes at the bottom
CLASS = open("pets.py").read().split("# make two pets")[0]

# broken pets 3 to 5 use the working class; the others bring their own
NEEDS_CLASS = ["broken3", "broken4", "broken5"]


def run(source):
    """Run source in a fresh Python and return its output and its last error line."""
    done = subprocess.run(
        [sys.executable, "-c", source], capture_output=True, text=True, timeout=30
    )
    errors = done.stderr.strip().splitlines()
    last = errors[-1] if errors else "no error"
    return done.stdout, last


for name in ["empty", "first", "stats"]:
    out, err = run(SNIPPETS[name])
    print(f"{name}: output {out!r}, error: {err}")

for name in ["report", "round1", "round2", "round3", "check"]:
    out, err = run(CLASS + SNIPPETS[name])
    print(f"{name}:")
    print(out, end="")
    print(f"  error: {err}")

# round 2 again, with the gated feed swapped in for the plain one
plain = '''    def feed(self):
        """Make this pet 1 less hungry."""
        self.hunger = self.hunger - 1'''
assert plain in CLASS, "pets.py feed has changed; update the gate check"
out, err = run(CLASS.replace(plain, SNIPPETS["gate"]) + SNIPPETS["round2"])
print("round2 with the gate:")
print(out, end="")
print(f"  error: {err}")

for k in range(1, 7):
    name = f"broken{k}"
    source = SNIPPETS[name]
    if name in NEEDS_CLASS:
        source = CLASS + source
    out, err = run(source)
    print(f"{name}: {err}")
