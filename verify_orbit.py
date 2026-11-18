import os, math
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
import pygame
src = open("orbit.py").read()
frames = {"n": 0}
real_get = pygame.event.get
def fake_get(*a, **k):
    frames["n"] += 1
    if frames["n"] > 1200:
        return [pygame.event.Event(pygame.QUIT)]
    return real_get(*a, **k)
pygame.event.get = fake_get

# Screenshots go to the folder named in SHOTS, if set. The session 12 page shows them.
SHOTS = os.environ.get("SHOTS", "")
real_flip = pygame.display.flip
def fake_flip(*a, **k):
    real_flip(*a, **k)
    if SHOTS and frames["n"] in (60, 1200):
        name = f"orbit_{frames['n']}.png"
        pygame.image.save(pygame.display.get_surface(), os.path.join(SHOTS, name))
pygame.display.flip = fake_flip

ns = {"__name__": "__main__"}
exec(compile(src, "orbit.py", "exec"), ns)
s = ns["ship"]
ds = [math.hypot(400-x, 300-y) for (x,y) in s.trail]
print(f"frames: {frames['n']}, trail points: {len(s.trail)}")
print(f"closest approach {min(ds):.1f} px, farthest {max(ds):.1f} px")
print(f"start distance {ds[0]:.1f} px, end distance {ds[-1]:.1f} px")
print(f"final speed {s.speed():.2f} px per step")
print("distance at a few frames:")
for f in [0, 50, 100, 200, 400, 800, 1200]:
    if f < len(ds):
        print(f"  frame {f:>4}: {ds[f]:>6.1f} px")
