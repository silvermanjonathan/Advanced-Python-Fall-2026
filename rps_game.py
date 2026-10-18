"""Session 6: five rounds of rock paper scissors against the computer."""

import random

MOVES = ["rock", "paper", "scissors"]

# each key beats its value: rock beats scissors
BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}

# what to tell you, for each answer winner can return
SAY = {"tie": "it is a tie", "player 1": "you win", "player 2": "the computer wins"}


def winner(move1, move2):
    """Return who wins when player 1 plays move1 and player 2 plays move2."""
    if move1 == move2:
        return "tie"
    elif BEATS[move1] == move2:
        return "player 1"
    else:
        return "player 2"


wins = 0
losses = 0
ties = 0

for turn in range(5):
    my_move = input("rock, paper, or scissors? ")

    while my_move not in MOVES:
        my_move = input("type rock, paper, or scissors: ")

    computer_move = random.choice(MOVES)
    result = winner(my_move, computer_move)
    print(f"the computer played {computer_move}, so {SAY[result]}")

    if result == "player 1":
        wins = wins + 1
    elif result == "player 2":
        losses = losses + 1
    else:
        ties = ties + 1

print(f"you won {wins}, lost {losses}, and tied {ties}")
