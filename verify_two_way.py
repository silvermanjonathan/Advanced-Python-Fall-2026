"""Run the two-way console programs without a screen and report what they did.

Key presses are sent as pygame events on chosen passes through the loop, the same as
pressing the key. Screenshots go to the folder named in SHOTS, if set.
"""

import os

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame

SHOTS = os.environ.get("SHOTS", "")


def key(k):
    """Return a key press event for key k."""
    return pygame.event.Event(pygame.KEYDOWN, key=k)


def run(filename, frames, shot_at=(), events_at=None, source=None):
    """Run one program for frames passes. Return its variables when the window closes."""
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
            name = f"{filename[:-3]}_{count['n']}.png"
            pygame.image.save(pygame.display.get_surface(), os.path.join(SHOTS, name))

    pygame.event.get = fake_get
    pygame.display.flip = fake_flip
    ns = {"__name__": "__main__"}
    try:
        exec(compile(source or open(filename).read(), filename, "exec"), ns)
    finally:
        pygame.event.get = real_get
        pygame.display.flip = real_flip
    ns["frames run"] = count["n"]
    return ns


print("--- two_way_step1.py ---")
ns = run("two_way_step1.py", 60, shot_at=(60,), events_at={30: key(pygame.K_e)})
print(f"E pressed on pass 30, mode is {ns['mode']!r} after pass 60")

print("--- two_way_step2.py, still with the message attack at dawn ---")
ns = run("two_way_step2.py", 20, events_at={10: key(pygame.K_e)})
print(f"E pressed: mode is {ns['mode']!r}, coded is {ns['coded']!r}")
ns = run("two_way_step2.py", 20, events_at={10: key(pygame.K_d)})
print(f"D pressed: mode is {ns['mode']!r}, coded is {ns['coded']!r}")
print(f"the green row after D: {ns['coded_row']}")

print("--- two_way_console.py ---")
ns = run("two_way_console.py", 5, shot_at=(5,))
print(f"before any key: mode is {ns['mode']!r}")
ns = run("two_way_console.py", 600, shot_at=(140, 600), events_at={10: key(pygame.K_d)})
print(f"D pressed on pass 10: coded is {ns['coded']!r}")
for n in (428, 429):
    ns = run("two_way_console.py", n, events_at={10: key(pygame.K_d)})
    print(f"D pressed on pass 10, after pass {n} shown is {ns['shown']}")
ns = run("two_way_console.py", 600, events_at={10: key(pygame.K_d), 300: key(pygame.K_e)})
print(f"D on pass 10, then E on pass 300: mode is {ns['mode']!r}, coded is {ns['coded']!r}")

print("--- the two sides of and swapped, then the mouse moves ---")
src = open("two_way_console.py").read().replace(
    "event.type == pygame.KEYDOWN and event.key == pygame.K_e",
    "event.key == pygame.K_e and event.type == pygame.KEYDOWN",
)
assert "event.key == pygame.K_e and" in src
move = pygame.event.Event(pygame.MOUSEMOTION, pos=(100, 100), rel=(1, 1), buttons=(0, 0, 0))
try:
    run("two_way_console.py", 10, events_at={5: move}, source=src)
except AttributeError as err:
    print(f"AttributeError: {err}")

print("--- two_way_space.py ---")
ns = run("two_way_space.py", 300, events_at={10: key(pygame.K_d), 200: key(pygame.K_SPACE)})
print(f"D on pass 10, space on pass 200: mode is {ns['mode']!r} after pass 300")
