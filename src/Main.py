import pygame 
import sys
from TileEditor import*
from Input import InputHandler
from Camera import Camera
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
input = InputHandler()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
manager = Manager('Level Data')
camera = Camera()
scrollx, scrolly = 0,0



while True:

    camera.x += (input.EditorAction.right - input.EditorAction.left) * 10
    camera.y += (input.EditorAction.down - input.EditorAction.up) * 10
    camera.x = pygame.math.clamp(camera.x, manager.selectedLevel.borders['left'], manager.selectedLevel.borders['right'])
    camera.y = pygame.math.clamp(camera.y, manager.selectedLevel.borders['top'], manager.selectedLevel.borders['bottom'])
    scrollx += (camera.x - scrollx)/10
    scrolly += (camera.y - scrolly)/10

    manager.selectedLevel.update(scrollx, scrolly)

    for event in pygame.event.get():
        input.update(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0,0,0))

    
    for tile in manager.selectedLevel.tiles:
        if tile.img is not None:
            screen.blit(tile.img, (tile.x - scrollx, tile.y - scrolly))

    
    pygame.display.flip()
    clock.tick(FPS)