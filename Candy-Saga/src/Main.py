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
manager = Manager('Candy-Saga\leveldata')
camera = Camera()
editor = Editor(manager.selectedLevel, input)
scrollx, scrolly = 0,0



while True:

    for event in pygame.event.get():
        input.update(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    camera.x += (input.EditorAction.right - input.EditorAction.left) * 10
    camera.y += (input.EditorAction.down - input.EditorAction.up) * 10
    camera.x = pygame.math.clamp(camera.x, manager.selectedLevel.borders['left'], manager.selectedLevel.borders['right'])
    camera.y = pygame.math.clamp(camera.y, manager.selectedLevel.borders['top'], manager.selectedLevel.borders['bottom'])
    scrollx += (camera.x - scrollx)/10
    scrolly += (camera.y - scrolly)/10


    manager.selectedLevel.update(scrollx, scrolly)
    editor.update(scrollx, scrolly)

    screen.fill((230,230,255))
    manager.selectedLevel.background.update(scrollx, scrolly)
    for tile in manager.selectedLevel.background.tiles:

        screen.blit(tile.img, (tile.x, tile.y))

    
    for tile in manager.selectedLevel.tiles:
        if type(tile.img) is pygame.Surface :
            screen.blit(tile.img, (tile.x - scrollx, tile.y - scrolly))

    
    pygame.display.flip()
    clock.tick(FPS)