"""Run orbit.py with other starting speeds and time steps, fast, headless.

The frame clock is switched off so each run takes a moment instead of
twenty seconds. The arithmetic is untouched.
"""

import math
import os

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
import pygame

src = open("orbit.py").read()
FRAMES = 1200
WIDTH = 800
HEIGHT = 600


class NoWaitClock:
    """A clock whose tick returns at once, so 1200 frames take a moment."""

    def tick(self, fps=0):
        return 0


def run(dx, dt):
    """Return closest, farthest, and off-screen frame count for one run."""
    patched = src.replace("ship = Ship(400, 120, 3.8, 0.0)", f"ship = Ship(400, 120, {dx}, 0.0)")
    patched = patched.replace("DT = 0.6", f"DT = {dt}")
    frames = {"n": 0}
    real_get = pygame.event.get

    def fake_get(*a, **k):
        frames["n"] += 1
        if frames["n"] > FRAMES:
            return [pygame.event.Event(pygame.QUIT)]
        return real_get(*a, **k)

    pygame.event.get = fake_get
    real_clock = pygame.time.Clock
    pygame.time.Clock = NoWaitClock
    ns = {"__name__": "__main__"}
    exec(compile(patched, "orbit.py", "exec"), ns)
    pygame.event.get = real_get
    pygame.time.Clock = real_clock
    trail = ns["ship"].trail
    ds = [math.hypot(400 - x, 300 - y) for (x, y) in trail]
    off = 0
    for x, y in trail:
        if x < 0 or x > WIDTH or y < 0 or y > HEIGHT:
            off = off + 1
    return min(ds), max(ds), off


print(f"{FRAMES} frames each. planet radius 26. window 800 by 600.")
print("  dx    DT    closest   farthest   frames off screen")
for dx, dt in [(2.0, 0.6), (2.8, 0.6), (3.8, 0.6), (6.0, 0.6), (6.5, 0.6), (7.6, 0.6), (3.8, 3.0), (3.8, 8.0)]:
    lo, hi, off = run(dx, dt)
    print(f"  {dx:<5} {dt:<5} {lo:>7.0f}   {hi:>8.0f}   {off:>5}")
