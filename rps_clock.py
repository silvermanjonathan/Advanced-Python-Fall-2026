"""Session 6: the number of steps from move2 to move1, for every pairing."""

MOVES = ["rock", "paper", "scissors"]

for spot1 in range(3):
    for spot2 in range(3):
        steps = (spot1 - spot2) % 3

        pairing = f"{MOVES[spot1]} against {MOVES[spot2]}"
        print(f"{pairing}: ({spot1} - {spot2}) % 3 = {steps}")
