"""Write every page, then validate."""

import os

from build import OUT, page, validate
from days12 import day01, day02
from days38 import day03, day04, day05, day06, day07, day08
from days913 import day09, day10, day11, day12, day13
from hub import hub

os.makedirs(OUT, exist_ok=True)

PAGES = [
    ("advanced_python_hub.html", "Advanced Python, Fall 2026, Robofun", hub),
    ("wed01_cold_read.html", "Session 1: cold read, then a style pass", day01),
    ("wed02_return_and_modules.html", "Session 2: functions that hand something back", day02),
    ("wed03_counting.html", "Session 3: counting, and what counting buys you", day03),
    ("wed04_messy_files.html", "Session 4: messy files", day04),
    ("wed05_transposition.html", "Session 5: ciphers that move letters", day05),
    ("wed06_hashing.html", "Session 6: your seal, and a real one", day06),
    ("wed07_what_it_costs.html", "Session 7: what a program costs", day07),
    ("wed08_heuristics.html", "Session 8: smarter than brute force", day08),
    ("wed09_monte_carlo.html", "Session 9: settling an argument by simulation", day09),
    ("wed10_benford.html", "Session 10: the first digit tells on you", day10),
    ("wed11_markov.html", "Session 11: machines that write", day11),
    ("wed12_classes.html", "Session 12: objects that remember", day12),
    ("wed13_orbits_demo.html", "Session 13: orbits, then the demo", day13),
]

written = []
for filename, title, fn in PAGES:
    written.append(page(filename, title, fn()))
    print(f"wrote {filename}")

print()
problems = validate(written)
if problems:
    print(f"{len(problems)} PROBLEM(S):")
    for p in problems:
        print("  " + p)
else:
    print("validation clean: tags balanced, reveals paired, links resolve, no dashes")

total = sum(os.path.getsize(p) for p in written)
print(f"\n{len(written)} pages, {total // 1024} KB total")
