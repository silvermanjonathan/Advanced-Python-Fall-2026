"""Run each program and confirm the lines quoted on its page really appear."""

import html
import os
import re
import subprocess

_HERE = os.path.dirname(os.path.abspath(__file__))
# Shipped layout: programs and pages both sit in the repo root, one level up.
# Dev layout: ./prog and ./site next to this file.
if os.path.isdir(os.path.join(_HERE, "prog")):
    PROG = os.path.join(_HERE, "prog")
    SITE = os.path.join(_HERE, "site")
else:
    PROG = SITE = os.path.dirname(_HERE)

# page -> (command, lines that must appear in the run)
CHECKS = {
    "wed01_cold_read.html#2": ("python3 gate_log.py", [
        "x 7", "y 5", "z 0", "q 3",
    ]),
    "wed12_classes.html#2": ("python3 sparks_parallel.py", [
        "spark 1: x=109 y=485 orange",
        "spark 2: x=100 y=494 red",
        "after removing from four lists but forgetting the fifth:",
    ]),
    "wed01_cold_read.html": ("python3 sweep_report.py", [
        "total 503", "average 50.3", "over 55: 6", "best 77 at index 5",
        "i=1 reading=58 slot=0", "i=9 reading=77 slot=8",
    ]),
    "wed02_return_and_modules.html": ("python3 sweep_report2.py", [
        "first best at 5", "last best at 9",
        "total_of([]) expected 0 got 0",
        "count_over([5, 5, 5], 5) expected 0 got 0",
        "last_best_index([9, 9]) expected 1 got 1",
    ]),
    "wed03_counting.html": ("python3 caesar_crack.py", [
        "five most common: [('h', 12), ('u', 5), ('g', 5), ('r', 5), ('w', 4)]",
        "distinct letters used: 14", "guessed shift 3",
        "plaintext: read the code and trace the code before you ever run the code",
    ]),
    "wed04_messy_files.html": ("python3 clean_readings.py", [
        "lines in the file: 13",
        "kept: [41, 58, 33, 58, 12, 77, 58, 60, 29, 77]",
        "kept 10, rejected 3", "total 503", "average 50.3",
    ]),
    "wed05_transposition.html": ("python3 transposition.py", [
        "rails 3  maettdetthnrhaetanetogaw", "round trip ok: True",
        "route    etnheantarhtmaettdetogaw",
    ]),
    "wed06_hashing.html": ("python3 avalanche.py", [
        "seal of 'ab' = 1", "seal of 'ba' = 1",
        "d502810c71aeb17e5ea1cbf930b46b87bb645a75df45f500230d061992aeb90a",
        "9076bc233a9100d5c0885c6a5f055ca13d856d28ee9cf74941719bb292f88da7",
        "dawn vs dusk: 130 of 256 bits differ",
        "dawn vs dawn+period: 124 of 256 bits differ",
    ]),
    "wed07_what_it_costs.html": ("python3 what_it_costs.py", [
        "linear: found at 999 after 1000 looks",
        "binary: found at 999 after 10 looks",
        "linear: returned -1 after 1000 looks",
        "binary: returned -1 after 10 looks",
    ]),
    "wed08_heuristics.html": ("python3 smarter_than_brute.py", [
        "brute force        4703917 tries",
        "random guessing    200000 tries (capped at 200000)",
        "run 3: 50 tries", "average 165.8 tries",
        "average 17.0 generations of 40 codes each",
    ]),
    "wed09_monte_carlo.html": ("python3 monty_hall.py", [
        "one hundred games, switching:", "67 wins out of 100",
        "100000    33318        0.3332       66682          0.6668",
        "1/3 = 0.3333", "2/3 = 0.6667",
    ]),
    "wed10_benford.html": ("python3 benford.py", [
        "largest gap from Benford: 0.004",
        "largest gap from Benford: 0.201",
        "1     182     0.303             0.301",
        "9      27     0.045             0.046",
        "1      60     0.100             0.301",
    ]),
    "wed11_markov.html": ("python3 markov.py", [
        "corpus words: 340", "distinct pairs: 250",
        "['counts', 'does', 'is', 'knows', 'picks', 'reads', 'was']",
    ]),
    "wed12_classes.html": (
        "SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python3 verify_plume.py", [
            "frames run: 241",
            "particles: 120, still airborne: 0, landed: 120",
            "highest point reached: y=64.2 (ground is y=560)",
            "trail lengths: shortest 92, longest 183",
        ]),
    "wed13_orbits_demo.html": (
        "SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python3 verify_orbit.py", [
            "frames: 1201, trail points: 1202",
            "closest approach 60.1 px, farthest 180.0 px",
            "final speed 5.94 px per step",
            "frame  100:   63.9 px",
        ]),
    "wed13_orbits_demo.html#band": (
        "SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python3 verify_orbit_band.py", [
            "2.0   0.6        15        190       0",
            "2.8   0.6        29        180       0",
            "6.0   0.6       180        298       0",
            "6.5   0.6       180        490     523",
            "7.6   0.6       180       2132    1077",
            "3.8   3.0        62        180       0",
            "3.8   8.0        66       4139     607",
        ]),
}

BROKEN_MONTY = [
    "55 wins out of 100",
    "100000    33318        0.3332       55402          0.5540",
]

fails = []
for pagename, (cmd, lines) in CHECKS.items():
    run = subprocess.run(
        cmd, shell=True, cwd=PROG, capture_output=True, text=True, timeout=600
    )
    real = run.stdout
    with open(os.path.join(SITE, pagename.split("#")[0])) as f:
        doc = f.read()
    blocks = re.findall(r"<pre><code>(.*?)</code></pre>", doc, re.S)
    page_text = "\n".join(html.unescape(b) for b in blocks)

    for line in lines:
        if line not in real:
            fails.append(f"{pagename}: NOT IN REAL RUN: {line!r}")
        if line not in page_text:
            fails.append(f"{pagename}: on page but claim missing from page: {line!r}")

# The broken Monty figures must come from the broken variant, not the shipped file.
src = open(os.path.join(PROG, "monty_hall.py")).read()
broken_src = src.replace(
    """    if switch:
        target = pick
        for door in range(3):
            if door != pick:
                if door != opened:
                    target = door
        pick = target""",
    """    if switch:
        for door in range(3):
            if door != pick:
                if door != opened:
                    pick = door""",
)
assert broken_src != src, "could not build the broken variant"
with open(os.path.join(PROG, "_broken_monty.py"), "w") as f:
    f.write(broken_src)
run = subprocess.run(
    "python3 _broken_monty.py", shell=True, cwd=PROG,
    capture_output=True, text=True, timeout=600,
)
for line in BROKEN_MONTY:
    if line not in run.stdout:
        fails.append(f"broken monty variant does not produce: {line!r}")
os.remove(os.path.join(PROG, "_broken_monty.py"))

print(f"checked {len(CHECKS)} pages against live runs")
if fails:
    print(f"\n{len(fails)} FAILURE(S):")
    for f_ in fails:
        print("  " + f_)
else:
    print("every quoted output line reproduced from a real run")
