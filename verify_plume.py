import os, random, math
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
import pygame

src = open("plume.py").read()
frames = {"n": 0}
real_get = pygame.event.get
def fake_get(*a, **k):
    frames["n"] += 1
    if frames["n"] > 240:
        return [pygame.event.Event(pygame.QUIT)]
    return real_get(*a, **k)
pygame.event.get = fake_get

# Screenshots go to the folder named in SHOTS, if set. The session 11 page shows them.
SHOTS = os.environ.get("SHOTS", "")
real_flip = pygame.display.flip
def fake_flip(*a, **k):
    real_flip(*a, **k)
    if SHOTS and frames["n"] in (40, 70, 240):
        name = f"plume_{frames['n']}.png"
        pygame.image.save(pygame.display.get_surface(), os.path.join(SHOTS, name))
pygame.display.flip = fake_flip

ns = {"__name__": "__main__"}
exec(compile(src, "plume.py", "exec"), ns)
ps = ns["particles"]
alive = sum(1 for p in ps if p.alive == 1)
peaks = [min(pt[1] for pt in p.trail) for p in ps]
lens = [len(p.trail) for p in ps]
print(f"frames run: {frames['n']}")
print(f"particles: {len(ps)}, still airborne: {alive}, landed: {len(ps)-alive}")
print(f"highest point reached: y={min(peaks):.1f} (ground is y=560)")
print(f"trail lengths: shortest {min(lens)}, longest {max(lens)}")
