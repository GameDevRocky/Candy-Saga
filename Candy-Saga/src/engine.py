
from pygame.locals import *
import pygame
import sys
from hero import Hero
from villain import Villain

# Initialize pygame
pygame.init()

# Set up display
display_w = 350
display_h = 600
window = pygame.display.set_mode((display_w, display_h), HWSURFACE | DOUBLEBUF | RESIZABLE)
pygame.display.set_caption("Candy Saga")

# Set up the clock for frame rate control
clock = pygame.time.Clock()

# Create the hero with a valid num_frames
hero = Hero(100, 'Candy Cane Crusader', 50, 100, 100, 50, 100, 5, num_frames=1)

# Create villains with valid num_frames
villains = [
    Villain(90, 'Licorice Lurker', 25, 150, 200, 50, 50, 3, num_frames=1)
]


# Main game loop

while True:
    window.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle movement and draw hero
    hero.movement()

    # Check for shooting input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:  # Press space to shoot
        hero.shoot()

    hero.update_bullets()  # Update bullets
    hero.draw(window)

    # Handle villains
    for villain in villains:
        villain.draw(window)

        # Check for bullet collisions with villains
        for bullet in hero.bullets:
            if (bullet.is_active and
                    bullet.x < villain.x + villain.width and bullet.x + bullet.width > villain.x and
                    bullet.y < villain.y + villain.height and bullet.y + bullet.height > villain.y):

                if villain.take_damage(bullet.damage):  # Deal damage with bullet's damage
                    # Collect candy (assuming defeating a villain gives 10 candy)
                    hero.collect_candy(10)
                bullet.is_active = False  # Deactivate bullet after hit

    pygame.display.update()
    clock.tick(60)
