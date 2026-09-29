"""Run the cipher console programs without a screen and report what they did.

Each program runs for a fixed number of frames, then gets a QUIT event, the same
as clicking the close button. Screenshots go to the folder named in SHOTS, if set.
"""

import os

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame

SHOTS = os.environ.get("SHOTS", "")


def run(filename, frames, shot_at=(), events_at=None, source=None):
    """Run one program for frames frames. Return its variables when the window closes."""
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


print("--- console_1_window.py ---")
ns = run("console_1_window.py", 120, shot_at=(120,))
print(f"passes through the while loop: {ns['frames run']}")

print("--- console_2_tiles.py ---")
run("console_2_tiles.py", 5, shot_at=(5,))

print("--- console_3_board.py ---")
run("console_3_board.py", 5, shot_at=(5,))

print("--- cipher_console.py ---")
ns = run("cipher_console.py", 700, shot_at=(130, 700))
print(f"letters in the message, counting spaces: {len(ns['MESSAGE'])}")
for n in (419, 420):
    ns = run("cipher_console.py", n)
    print(f"after {ns['frame']} frames, shown is {ns['shown']}")

print("--- cipher_console_replay.py ---")
press_r = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r)
ns = run("cipher_console_replay.py", 700, events_at={600: press_r})
print(f"R pressed on frame 600, shown is {ns['shown']} after frame 700")

print("--- the two sides of and swapped, then the mouse moves ---")
src = open("cipher_console_replay.py").read().replace(
    "event.type == pygame.KEYDOWN and event.key == pygame.K_r",
    "event.key == pygame.K_r and event.type == pygame.KEYDOWN",
)
assert "event.key == pygame.K_r and" in src
move = pygame.event.Event(pygame.MOUSEMOTION, pos=(100, 100), rel=(1, 1), buttons=(0, 0, 0))
try:
    run("cipher_console_replay.py", 10, events_at={5: move}, source=src)
except AttributeError as err:
    print(f"AttributeError: {err}")

print("--- the two sides of the box gate swapped ---")
src = open("cipher_console.py").read().replace(
    'if shown < len(MESSAGE) and MESSAGE[shown] != " ":',
    'if MESSAGE[shown] != " " and shown < len(MESSAGE):',
)
assert 'if MESSAGE[shown] != " " and' in src
try:
    run("cipher_console.py", 500, source=src)
except IndexError as err:
    print(f"IndexError: {err}")

print("--- a capital letter in MESSAGE ---")
src = open("cipher_console.py").read().replace('MESSAGE = "attack at dawn"', 'MESSAGE = "Attack at dawn"')
try:
    run("cipher_console.py", 5, source=src)
except KeyError as err:
    print(f"KeyError: {err}")
