"""Pictures of the letters a to z and the space, each drawn from small squares."""

import pygame

# Each letter is 5 rows of 3 squares, top row first. "#" is a filled square.
# "." is an empty one.
SHAPES = {
    "a": [".#.", "#.#", "###", "#.#", "#.#"],
    "b": ["##.", "#.#", "##.", "#.#", "##."],
    "c": [".##", "#..", "#..", "#..", ".##"],
    "d": ["##.", "#.#", "#.#", "#.#", "##."],
    "e": ["###", "#..", "##.", "#..", "###"],
    "f": ["###", "#..", "##.", "#..", "#.."],
    "g": [".##", "#..", "#.#", "#.#", ".##"],
    "h": ["#.#", "#.#", "###", "#.#", "#.#"],
    "i": ["###", ".#.", ".#.", ".#.", "###"],
    "j": ["..#", "..#", "..#", "#.#", ".#."],
    "k": ["#.#", "##.", "#..", "##.", "#.#"],
    "l": ["#..", "#..", "#..", "#..", "###"],
    "m": ["#.#", "###", "###", "#.#", "#.#"],
    "n": ["##.", "#.#", "#.#", "#.#", "#.#"],
    "o": [".#.", "#.#", "#.#", "#.#", ".#."],
    "p": ["##.", "#.#", "##.", "#..", "#.."],
    "q": [".#.", "#.#", "#.#", "##.", ".##"],
    "r": ["##.", "#.#", "##.", "#.#", "#.#"],
    "s": [".##", "#..", ".#.", "..#", "##."],
    "t": ["###", ".#.", ".#.", ".#.", ".#."],
    "u": ["#.#", "#.#", "#.#", "#.#", "###"],
    "v": ["#.#", "#.#", "#.#", "#.#", ".#."],
    "w": ["#.#", "#.#", "###", "###", "#.#"],
    "x": ["#.#", "#.#", ".#.", "#.#", "#.#"],
    "y": ["#.#", "#.#", ".#.", ".#.", ".#."],
    "z": ["###", "..#", ".#.", "#..", "###"],
    " ": ["...", "...", "...", "...", "..."],
}


def draw_letter(screen, letter, x, y, size, color):
    """Draw one letter with its top left corner at (x, y), from squares size pixels wide."""
    shape = SHAPES[letter]
    for row in range(5):
        for col in range(3):
            if shape[row][col] == "#":
                pygame.draw.rect(screen, color, (x + col * size, y + row * size, size, size))


def draw_word(screen, word, x, y, size, color):
    """Draw a word one letter at a time, starting at (x, y)."""
    for i in range(len(word)):
        draw_letter(screen, word[i], x + i * 4 * size, y, size, color)
