"""Session 6: three versions of winner, checked against each other."""

MOVES = ["rock", "paper", "scissors"]

# each key beats its value: rock beats scissors
BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}

# what each number of steps means
RESULTS = ["tie", "player 1", "player 2"]


def winner_if(move1, move2):
    """Return who wins, decided with if lines."""
    if move1 == move2:
        return "tie"
    elif move1 == "rock" and move2 == "scissors":
        return "player 1"
    elif move1 == "scissors" and move2 == "paper":
        return "player 1"
    elif move1 == "paper" and move2 == "rock":
        return "player 1"
    else:
        return "player 2"


def winner_dict(move1, move2):
    """Return who wins, decided with the BEATS dictionary."""
    if move1 == move2:
        return "tie"
    elif BEATS[move1] == move2:
        return "player 1"
    else:
        return "player 2"


def winner_clock(move1, move2):
    """Return who wins, decided by counting steps around the circle of moves."""
    spot1 = MOVES.index(move1)
    spot2 = MOVES.index(move2)

    steps = (spot1 - spot2) % 3
    return RESULTS[steps]


agree = 0

for move1 in MOVES:
    for move2 in MOVES:
        first = winner_if(move1, move2)
        second = winner_dict(move1, move2)
        third = winner_clock(move1, move2)

        if first == second and second == third:
            agree = agree + 1

print(f"the three versions agree on {agree} of the 9 pairings")
