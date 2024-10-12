import pygame
import sys
from pygame.locals import *
from main import Object

pygame.init()

# Set up display
display_w = 350
display_h = 600
window = pygame.display.set_mode((display_w, display_h), HWSURFACE | DOUBLEBUF | RESIZABLE)
pygame.display.set_caption("Candy Saga")

# Set up the clock for frame rate control
clock = pygame.time.Clock()

class Hero(Object):
    def __init__(self, hp, name, power, x, y, width, height, speed, sprite_sheet_path, num_frames):
        super().__init__(hp, name, power, x, y, width, height, speed, sprite_sheet_path, num_frames)


# Create a hero object with the sprite sheet for running
hero = Hero(100, 'HeroName', 50, 100, 100, 374.2, 571, 5, 'run.png', 5)

# Main game loop
while True:
    window.fill((0, 0, 0))  # Clear the screen with black

    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Call the movement and draw functions
    hero.movement()
    hero.draw(window)

    # Control the frame rate
    clock.tick(60)  # 60 FPS

    # Update the display
    pygame.display.update()