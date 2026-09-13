"""Draw the leading-digit tally of one CSV file as nine bars in a window.

The three helper functions are the same ones as in benford.py. This file
draws; that file prints. Words in the terminal, visuals in the window.
"""

import csv
import math
from collections import Counter

import pygame

FILENAME = "honest_ledger.csv"

WIDTH = 800
HEIGHT = 600
BLACK = (14, 36, 48)
TEAL = (14, 107, 98)
AMBER = (232, 150, 60)


def leading_digit(text):
    """Return the first digit character in text as an integer."""
    for ch in text:
        if ch in "123456789":
            return int(ch)
    return 0


def tally_file(filename):
    """Return a Counter of leading digits in the amount column."""
    counts = Counter()
    with open(filename, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            counts[leading_digit(row["amount"])] += 1
    return counts


def benford_expected(digit):
    """Return the share of numbers Benford's law predicts start with digit."""
    return math.log10(1 + 1 / digit)


counts = tally_file(FILENAME)
total = sum(counts.values())
print(f"{FILENAME}: {total} amounts tallied, window open, close it to finish")

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
    screen.fill(BLACK)
    for d in range(1, 10):
        share = counts[d] / total
        height = int(share * 900)
        x = 60 + (d - 1) * 80
        pygame.draw.rect(screen, TEAL, (x, 520 - height, 54, height))
        expected = int(benford_expected(d) * 900)
        pygame.draw.line(screen, AMBER, (x, 520 - expected), (x + 54, 520 - expected), 3)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
