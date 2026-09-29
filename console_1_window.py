"""Cipher console, step 1: a window that stays open until you close it."""

import pygame

BOARD = (15, 19, 24)

pygame.init()
screen = pygame.display.set_mode((640, 400))
clock = pygame.time.Clock()
print("window open, close it to finish")

running = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0

    screen.fill(BOARD)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
