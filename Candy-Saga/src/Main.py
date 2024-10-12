import pygame 
import sys
from TileEditor import*

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
manager = Manager('Level Data')


while True:

    screen.fill((0,0,0))

    
    for tile in manager.selectedLevel.tiles:
        screen.blit(tile.img, (tile.x, tile.y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()
    clock.tick(FPS)