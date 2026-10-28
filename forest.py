"""Session 5: a class for a tree, and a forest of seven trees made from it."""

import pygame

pygame.init()

WIDTH = 640
HEIGHT = 400
GROUND = 340
SKY = (214, 234, 244)
GRASS = (96, 150, 72)
BARK = (110, 74, 44)
LEAVES = (40, 112, 56)


class Tree:
    """A tree that keeps its own place, height, and leaves, and draws itself."""

    def __init__(self, x, height):
        self.x = x
        self.height = height
        self.leaf_size = 0

    def grow(self, amount):
        """Make this tree amount pixels taller."""
        self.height = self.height + amount

    def add_leaves(self):
        """Give this tree a round clump of leaves."""
        self.leaf_size = 30

    def draw(self, screen):
        """Draw this tree's trunk, then its leaves if it has any."""
        top = GROUND - self.height
        pygame.draw.rect(screen, BARK, (self.x - 5, top, 10, self.height))

        if self.leaf_size > 0:
            pygame.draw.circle(screen, LEAVES, (self.x, top), self.leaf_size)


# make seven trees, 80 pixels apart, each one 20 taller than the one before
forest = []
for i in range(7):
    forest.append(Tree(80 + i * 80, 40 + i * 20))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
        if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
            for tree in forest:
                tree.grow(20)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
            for tree in forest:
                tree.add_leaves()

    screen.fill(SKY)
    pygame.draw.rect(screen, GRASS, (0, GROUND, WIDTH, HEIGHT - GROUND))
    for tree in forest:
        tree.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
