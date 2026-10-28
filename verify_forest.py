"""Check every output quoted in the forest section of the session 5 page.

forest.py runs without a screen. Key presses are sent as pygame events on chosen passes
through the loop, the same as pressing the key. Screenshots go to the folder named in
SHOTS, if set. The page's code for the trace rounds is the strings in SNIPPETS below;
the page generator reads them from this file, so the code on the page and the code run
here cannot drift apart. Rounds run with the Tree class from forest.py in front of them.
"""

import os
import subprocess
import sys

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame

SHOTS = os.environ.get("SHOTS", "")

SNIPPETS = {
    "round1": '''forest = [Tree(100, 40), Tree(300, 40), Tree(500, 40)]

for tree in forest:
    tree.grow(50)

forest[0].grow(80)

for tree in forest:
    print(tree.x, tree.height)''',
    "round2": '''first = Tree(100, 40)
forest = [first, first, first]

for tree in forest:
    tree.grow(50)

print(first.height)''',
}

# the class from forest.py, without the forest and the window below it
CLASS = open("forest.py").read().split("# make seven trees")[0]


def key(k):
    """Return a key press event for key k."""
    return pygame.event.Event(pygame.KEYDOWN, key=k)


def run(frames, shot_at=(), events_at=None, source=None):
    """Run forest.py for frames passes. Return its variables when the window closes."""
    count = {"n": 0}
    real_get = pygame.event.get
    real_flip = pygame.display.flip
    events_at = events_at or {}

    def fake_get(*a, **k):
        count["n"] += 1
        events = list(real_get(*a, **k))
        if count["n"] in events_at:
            events.append(events_at[count["n"]])
        if count["n"] >= frames:
            events.append(pygame.event.Event(pygame.QUIT))
        return events

    def fake_flip(*a, **k):
        real_flip(*a, **k)
        if SHOTS and count["n"] in shot_at:
            name = f"forest_{count['n']}.png"
            pygame.image.save(pygame.display.get_surface(), os.path.join(SHOTS, name))

    pygame.event.get = fake_get
    pygame.display.flip = fake_flip
    ns = {"__name__": "__main__"}
    try:
        exec(compile(source or open("forest.py").read(), "forest.py", "exec"), ns)
    finally:
        pygame.event.get = real_get
        pygame.display.flip = real_flip
    return ns


print("--- forest.py, no key pressed ---")
ns = run(5, shot_at=(5,))
print(f"heights {[t.height for t in ns['forest']]}")
print(f"leaf sizes {[t.leaf_size for t in ns['forest']]}")

print("--- forest.py, G on passes 10, 20, 30, then L on pass 40 ---")
presses = {10: key(pygame.K_g), 20: key(pygame.K_g), 30: key(pygame.K_g),
           40: key(pygame.K_l)}
ns = run(60, shot_at=(60,), events_at=presses)
trees = ns["forest"]
print(f"heights {[t.height for t in trees]}")
print(f"leaf sizes {[t.leaf_size for t in trees]}")
tall = trees[-1]
top = ns["GROUND"] - tall.height
print(f"tallest tree: x {tall.x}, height {tall.height}, top of trunk at y {top}")

# draw one more frame from the trees as they ended, and read two pixels from it
screen = pygame.display.set_mode((ns["WIDTH"], ns["HEIGHT"]))
screen.fill(ns["SKY"])
for t in trees:
    t.draw(screen)
leaf = tuple(screen.get_at((tall.x, top)))[:3] == ns["LEAVES"]
bark = tuple(screen.get_at((tall.x, top + 40)))[:3] == ns["BARK"]
print(f"leaf green at the top of the tallest trunk: {leaf}, bark 40 pixels below: {bark}")
pygame.quit()

print("--- forest.py with range(8) in place of range(7) ---")
src = open("forest.py").read()
assert src.count("range(7)") == 1, "forest.py has changed; update the eighth tree check"
ns = run(3, source=src.replace("range(7)", "range(8)"))
print(f"x positions {[t.x for t in ns['forest']]}, window width {ns['WIDTH']}")
pygame.quit()


def run_snippet(source):
    """Run source in a fresh Python and return its output and its last error line."""
    env = dict(os.environ)
    done = subprocess.run(
        [sys.executable, "-c", source], capture_output=True, text=True, timeout=30,
        env=env,
    )
    errors = done.stderr.strip().splitlines()
    last = errors[-1] if errors else "no error"
    return done.stdout, last


for name in ["round1", "round2"]:
    out, err = run_snippet(CLASS + SNIPPETS[name])
    print(f"{name}:")
    print(out, end="")
    print(f"  error: {err}")
