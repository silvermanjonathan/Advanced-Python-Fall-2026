"""Three ways to open the same lock. Only one of them scales."""

import random
from itertools import product

SECRET = "4703916"
DIGITS = "0123456789"


def score(guess):
    """Return how many positions in guess match the secret."""
    hits = 0
    for i in range(len(SECRET)):
        if guess[i] == SECRET[i]:
            hits = hits + 1
    return hits


def brute_force():
    """Try every code. Return the tries used."""
    tries = 0
    for combo in product(DIGITS, repeat=len(SECRET)):
        tries = tries + 1
        if score("".join(combo)) == len(SECRET):
            return tries
    return tries


def random_guessing(cap):
    """Guess whole codes at random. Return the tries used, or the cap."""
    tries = 0
    while tries < cap:
        tries = tries + 1
        guess = ""
        for i in range(len(SECRET)):
            guess = guess + random.choice(DIGITS)
        if score(guess) == len(SECRET):
            return tries
    return cap


def hill_climb():
    """Keep any single-digit change that does not make the score worse."""
    current = ""
    for i in range(len(SECRET)):
        current = current + random.choice(DIGITS)
    best = score(current)
    tries = 1
    while best < len(SECRET):
        spot = random.randrange(len(SECRET))
        new_digit = random.choice(DIGITS)
        candidate = current[:spot] + new_digit + current[spot + 1:]
        tries = tries + 1
        if score(candidate) >= best:
            current = candidate
            best = score(candidate)
    return tries


def genetic(pop_size, keep):
    """Breed a population of codes toward the secret. Return generations."""
    population = []
    for i in range(pop_size):
        code = ""
        for j in range(len(SECRET)):
            code = code + random.choice(DIGITS)
        population.append(code)

    generation = 0
    while True:
        generation = generation + 1
        population.sort(key=score, reverse=True)
        if score(population[0]) == len(SECRET):
            return generation, population[0]
        parents = population[:keep]
        population = list(parents)
        while len(population) < pop_size:
            mum = random.choice(parents)
            dad = random.choice(parents)
            cut = random.randrange(1, len(SECRET))
            child = mum[:cut] + dad[cut:]
            if random.random() < 0.3:
                spot = random.randrange(len(SECRET))
                child = child[:spot] + random.choice(DIGITS) + child[spot + 1:]
            population.append(child)


random.seed(4703)

print(f"secret is {len(SECRET)} digits, so there are {10 ** len(SECRET)} codes")
print()
print(f"brute force        {brute_force()} tries")
print(f"random guessing    {random_guessing(200000)} tries (capped at 200000)")
print()
print("hill climbing, five runs:")
total = 0
for run in range(5):
    t = hill_climb()
    total = total + t
    print(f"  run {run + 1}: {t} tries")
print(f"  average {total / 5} tries")
print()
print("genetic algorithm, five runs:")
total = 0
for run in range(5):
    g, winner = genetic(40, 8)
    total = total + g
    print(f"  run {run + 1}: {g} generations, found {winner}")
print(f"  average {total / 5} generations of 40 codes each")
