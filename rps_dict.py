"""Session 6: who wins a round of rock paper scissors, decided with a dictionary."""

MOVES = ["rock", "paper", "scissors"]

# each key beats its value: rock beats scissors
BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}


def winner(move1, move2):
    """Return who wins when player 1 plays move1 and player 2 plays move2."""
    if move1 == move2:
        return "tie"
    elif BEATS[move1] == move2:
        return "player 1"
    else:
        return "player 2"


# every pairing, one line each
for move1 in MOVES:
    for move2 in MOVES:
        print(f"{move1} against {move2}: {winner(move1, move2)}")
