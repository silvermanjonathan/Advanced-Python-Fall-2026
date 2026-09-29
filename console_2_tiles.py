"""Cipher console, step 2: a row of 26 tiles, one for each letter."""

import pygame

BOARD = (15, 19, 24)
TILE = (242, 233, 211)

pygame.init()
screen = pygame.display.set_mode((640, 400))
clock = pygame.time.Clock()
print(f"first tile starts at x = {20 + 0 * 23}")
print(f"last tile starts at x = {20 + 25 * 23}")

running = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0

    screen.fill(BOARD)

    for i in range(26):
        x = 20 + i * 23
        pygame.draw.rect(screen, TILE, (x, 130, 20, 26))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
