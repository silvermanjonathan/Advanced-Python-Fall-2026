"""Session 6: who wins a round of rock paper scissors, decided with if lines."""

MOVES = ["rock", "paper", "scissors"]


def winner(move1, move2):
    """Return who wins when player 1 plays move1 and player 2 plays move2."""
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


# every pairing, one line each
for move1 in MOVES:
    for move2 in MOVES:
        print(f"{move1} against {move2}: {winner(move1, move2)}")
