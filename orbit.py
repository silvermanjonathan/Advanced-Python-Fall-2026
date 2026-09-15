"""Gravity as acceleration toward a body, stepped a slice of time at a time."""

import math

import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600
PLANET_X = 400
PLANET_Y = 300
PULL = 5200.0
DT = 0.6
BLACK = (14, 36, 48)
PAPER = (241, 243, 242)
TEAL = (14, 107, 98)


class Ship:
    """A craft that only ever falls toward the planet."""

    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.trail = [(x, y)]

    def distance(self):
        """Return the distance from this ship to the planet centre."""
        gap_x = PLANET_X - self.x
        gap_y = PLANET_Y - self.y
        return math.sqrt(gap_x * gap_x + gap_y * gap_y)

    def step(self):
        """Apply one time slice of gravity, then move."""
        gap_x = PLANET_X - self.x
        gap_y = PLANET_Y - self.y
        r = self.distance()
        pull = PULL / (r * r)

        self.dx = self.dx + pull * (gap_x / r) * DT
        self.dy = self.dy + pull * (gap_y / r) * DT

        self.x = self.x + self.dx * DT
        self.y = self.y + self.dy * DT

        self.trail.append((self.x, self.y))

    def speed(self):
        """Return how fast this ship is travelling."""
        return math.sqrt(self.dx * self.dx + self.dy * self.dy)

    def draw(self, screen):
        """Draw the flight path and the ship."""
        if len(self.trail) > 1:
            pygame.draw.lines(screen, TEAL, False, self.trail[-900:], 1)
        pygame.draw.circle(screen, PAPER, (int(self.x), int(self.y)), 3)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
ship = Ship(400, 120, 3.8, 0.0)

running = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0

    screen.fill(BLACK)
    pygame.draw.circle(screen, (198, 142, 60), (PLANET_X, PLANET_Y), 26)
    ship.step()
    ship.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
