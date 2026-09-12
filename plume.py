"""A plume of particles, each one an object that remembers its own path."""

import math
import random

import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600
GRAVITY = 0.12
BLACK = (14, 36, 48)
WHITE = (241, 243, 242)


class Particle:
    """One thrown speck that keeps a trail of where it has been."""

    def __init__(self, x, y, speed, angle):
        self.x = x
        self.y = y
        self.dx = speed * math.cos(math.radians(angle))
        self.dy = -speed * math.sin(math.radians(angle))
        self.trail = [(x, y)]
        self.alive = 1

    def step(self):
        """Move one frame forward and record the new position."""
        self.dy = self.dy + GRAVITY
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.trail.append((self.x, self.y))
        if self.y > HEIGHT - 40:
            self.alive = 0

    def color(self):
        """Return a color that depends on how fast this particle rose."""
        if self.dy < -2:
            return (255, 236, 170)
        if self.dy < 2:
            return (232, 150, 60)
        return (150, 74, 48)

    def draw(self, screen):
        """Draw this particle's trail and its head."""
        if len(self.trail) > 1:
            pygame.draw.lines(screen, self.color(), False, self.trail, 1)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 2)


def make_plume(count):
    """Return a list of particles launched from the vent."""
    out = []
    for i in range(count):
        speed = random.uniform(6, 11)
        angle = random.uniform(60, 120)
        out.append(Particle(WIDTH // 2, HEIGHT - 40, speed, angle))
    return out


random.seed(20261209)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
particles = make_plume(120)

running = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
    screen.fill(BLACK)
    pygame.draw.rect(screen, (90, 108, 116), (0, HEIGHT - 40, WIDTH, 40))
    for p in particles:
        if p.alive == 1:
            p.step()
        p.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
