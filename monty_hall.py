"""Settle the Monty Hall argument by running it, not by arguing."""

import random


def one_game(switch):
    """Play one game. Return 1 for a win, 0 for a loss."""
    prize = random.randrange(3)
    pick = random.randrange(3)

    opened = -1
    for door in range(3):
        if door != prize:
            if door != pick:
                opened = door
    # If pick == prize, two doors qualify and the loop keeps the later one.
    # That is fine: the host may open either.

    if switch:
        target = pick
        for door in range(3):
            if door != pick:
                if door != opened:
                    target = door
        pick = target

    if pick == prize:
        return 1
    return 0


def run_trials(switch, trials):
    """Return the number of wins over the given number of games."""
    wins = 0
    for t in range(trials):
        wins = wins + one_game(switch)
    return wins


random.seed(1963)

print("one hundred games, switching:")
wins = 0
for t in range(100):
    wins = wins + one_game(True)
print(f"  {wins} wins out of 100")

print()
print("does it settle down?")
print("  trials    stay wins    stay rate    switch wins    switch rate")
for trials in [10, 100, 1000, 10000, 100000]:
    random.seed(1963)
    stay = run_trials(False, trials)
    random.seed(1963)
    switch = run_trials(True, trials)
    print(
        f"  {trials:<9} {stay:<12} {stay / trials:<12.4f} "
        f"{switch:<14} {switch / trials:.4f}"
    )

print()
print("the model says stay 1/3 and switch 2/3:")
print(f"  1/3 = {1 / 3:.4f}")
print(f"  2/3 = {2 / 3:.4f}")
