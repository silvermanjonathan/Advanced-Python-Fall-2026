"""Check that letters.draw_letter and letters.draw_word really do what letters_tour.py prints.

Runs without a screen. It records every rectangle draw_letter asks pygame for, and
every letter position draw_word asks for, and prints them in letters_tour.py's words.
"""

import os

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame

import letters

pygame.init()
screen = pygame.display.set_mode((640, 400))

rects = []
real_rect = pygame.draw.rect
pygame.draw.rect = lambda surface, color, r, *more: rects.append(tuple(r))
letters.draw_letter(screen, "a", 100, 50, 10, (255, 255, 255))
pygame.draw.rect = real_rect
for (rx, ry, w, h) in rects:
    print(f"row {(ry - 50) // 10} col {(rx - 100) // 10}: square at ({rx}, {ry})")
print(f"squares drawn: {len(rects)}")

starts = []
real_letter = letters.draw_letter
letters.draw_letter = lambda surface, letter, lx, ly, size, color: starts.append(lx)
letters.draw_word(screen, "att", 40, 50, 4, (255, 255, 255))
letters.draw_letter = real_letter
for i, lx in enumerate(starts):
    print(f"letter {i} starts at x = {lx}")
pygame.quit()
