"""Session 6 stretch: rock paper scissors lizard Spock, decided two ways."""

MOVES = ["rock", "paper", "scissors", "spock", "lizard"]

# each move beats the two moves in its list
BEATS = {
    "rock": ["scissors", "lizard"],
    "paper": ["rock", "spock"],
    "scissors": ["paper", "lizard"],
    "spock": ["scissors", "rock"],
    "lizard": ["spock", "paper"],
}


def winner_dict(move1, move2):
    """Return who wins, decided with the BEATS dictionary."""
    if move1 == move2:
        return "tie"
    elif move2 in BEATS[move1]:
        return "player 1"
    else:
        return "player 2"


def winner_clock(move1, move2):
    """Return who wins, decided by counting steps around the circle."""
    spot1 = MOVES.index(move1)
    spot2 = MOVES.index(move2)

    steps = (spot1 - spot2) % 5

    if steps == 0:
        return "tie"
    elif steps % 2 == 1:
        return "player 1"
    else:
        return "player 2"


agree = 0

for move1 in MOVES:
    for move2 in MOVES:
        if winner_dict(move1, move2) == winner_clock(move1, move2):
            agree = agree + 1

print(f"the two versions agree on {agree} of the 25 pairings")
