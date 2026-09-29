"""Cipher console with replay: press R to build the coded message again."""

import pygame

import letters

MESSAGE = "attack at dawn"
KEY = 3
ALPHABET = "abcdefghijklmnopqrstuvwxyz"

BOARD = (15, 19, 24)
TILE = (242, 233, 211)
TILE_INK = (27, 31, 38)
CODED_TILE = (31, 46, 39)
CODED_INK = (123, 228, 149)
PLAIN_INK = (150, 143, 128)
GLOW = (201, 139, 31)


def shift_by(text, amount):
    """Return text with every letter rotated forward by amount."""
    out = ""
    for ch in text:
        if ch == " ":
            out = out + " "
        else:
            spot = ord(ch) - ord("a")
            spot = (spot + amount) % 26
            out = out + chr(spot + ord("a"))
    return out


coded = shift_by(MESSAGE, KEY)
coded_row = shift_by(ALPHABET, KEY)
print(f"plain: {MESSAGE}")
print(f"coded: {coded}")
print(f"coded row: {coded_row}")

pygame.init()
screen = pygame.display.set_mode((640, 400))
clock = pygame.time.Clock()

frame = 0
shown = 0
running = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            frame = 0
            shown = 0

    screen.fill(BOARD)

    for i in range(26):
        x = 20 + i * 23
        pygame.draw.rect(screen, TILE, (x, 130, 20, 26))
        letters.draw_letter(screen, ALPHABET[i], x + 7, 138, 2, TILE_INK)
        pygame.draw.rect(screen, CODED_TILE, (x, 190, 20, 26))
        letters.draw_letter(screen, coded_row[i], x + 7, 198, 2, CODED_INK)

    if shown < len(MESSAGE) and MESSAGE[shown] != " ":
        spot = ord(MESSAGE[shown]) - ord("a")
        x = 20 + spot * 23
        pygame.draw.rect(screen, GLOW, (x - 3, 127, 26, 32), 3)
        pygame.draw.rect(screen, GLOW, (x - 3, 187, 26, 32), 3)

    letters.draw_word(screen, MESSAGE, 40, 50, 4, PLAIN_INK)
    for i in range(shown):
        letters.draw_letter(screen, coded[i], 40 + i * 16, 280, 4, CODED_INK)

    frame = frame + 1
    if frame % 30 == 0 and shown < len(MESSAGE):
        shown = shown + 1

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
