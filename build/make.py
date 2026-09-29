"""Write every page, then validate."""

import os

from build import OUT, page, validate
from days12 import day01, day02
from ws01 import WS_CSS, worksheet01, worksheet01_key
from trace01 import TRACE_CSS, trace01
from days38 import day03, day04, day05, day06, day07
from days913 import day08, day09, day10, day11, day12, day13
from hub import hub

os.makedirs(OUT, exist_ok=True)

PAGES = [
    ("advanced_python_hub.html", "Advanced Python, Fall 2026, Robofun", hub),
    ("wed01_cold_read.html", "Session 1: cold read, then a style pass", day01),
    ("wed01_worksheet.html", "Session 1 worksheet: trace it before you run it", worksheet01),
    ("wed01_worksheet_key.html", "Session 1 worksheet: teacher's answer key", worksheet01_key),
    ("wed01_doors_trace.html", "Session 1: watch the door trace fill in", trace01),
    ("wed02_return_and_modules.html", "Session 2: functions that return a value", day02),
    ("wed03_counting.html", "Session 3: counting, and what counting lets you do", day03),
    ("wed04_transposition.html", "Session 4: ciphers that move letters", day04),
    ("wed05_hashing.html", "Session 5: your seal, and a real one", day05),
    ("wed06_what_it_costs.html", "Session 6: what a program costs", day06),
    ("wed07_heuristics.html", "Session 7: smarter than brute force", day07),
    ("wed08_monte_carlo.html", "Session 8: settling an argument by simulation", day08),
    ("wed09_benford.html", "Session 9: the first digit tells on you", day09),
    ("wed10_markov.html", "Session 10: machines that write", day10),
    ("wed11_classes.html", "Session 11: objects that remember", day11),
    ("wed12_orbits.html", "Session 12: orbits", day12),
    ("wed13_demo_day.html", "Session 13: to be written, then the demo", day13),
]

written = []
for filename, title, fn in PAGES:
    extra = {"wed01_worksheet.html": WS_CSS, "wed01_worksheet_key.html": WS_CSS, "wed01_doors_trace.html": TRACE_CSS}.get(filename, "")
    written.append(page(filename, title, fn(), head_extra=extra))
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
