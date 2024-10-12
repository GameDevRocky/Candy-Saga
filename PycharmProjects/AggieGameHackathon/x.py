import pygame
import sys
from pygame.locals import *

pygame.init()
display_w = 800
display_h = 600

window = pygame.display.set_mode((display_w, display_h), HWSURFACE | DOUBLEBUF | RESIZABLE)
pygame.display.set_icon(pygame.image.load("game_icon.png"))
pygame.display.set_caption("Work in progress")
clock = pygame.time.Clock()
background = pygame.image.load("background.png")


class Player(object):
    """The controllable player in game"""

    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load("sprite_sheet.png")
        self.speed = speed

    def draw(self):
        self.sprite = (self.image.subsurface(pygame.Rect(0, 100, 50, 50)))
        window.blit(self.sprite, (self.x, self.y))

    def movement(self):
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_LEFT]:
            self.x -= self.speed
        if self.keys[pygame.K_RIGHT]:
            self.x += self.speed
        if self.keys[pygame.K_UP]:
            self.y -= self.speed
        if self.keys[pygame.K_DOWN]:
            self.y += self.speed


player = Player(400, 300, 50, 50, 5)

running = True
while running:
    window.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), RESIZABLE)

    player.draw()
    player.movement()

    clock.tick(60)
    pygame.display.flip()