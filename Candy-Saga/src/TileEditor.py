import pygame
import os
import json
import math
from Input import InputHandler

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WORLD_WIDTH = 100
WORLD_HEIGHT = 50
TILE_SIZE = 25
TILEAMOUNT_X = math.ceil(SCREEN_WIDTH/TILE_SIZE) + 1
TILEAMOUNT_Y = math.ceil(SCREEN_HEIGHT/TILE_SIZE) + 1


class Level:
    def __init__(self, manager, file):
        self.data = {}
        self.tiles = []
        self.borders = {}
        self.width = None
        self.height = None
        self.manager = manager
        self.file = file
        self.settings = None
        self.background = None
        

    def assignData(self):
        for index in self.data:
            # Assign the correct image based on the tile type
            self.data[index].img = self.manager.tile_images[self.data[index].type]

    def assignTiles(self):
        index = 0
        for x in range(TILEAMOUNT_X):
            for y in range(TILEAMOUNT_Y):
                tile = Tile()
                tile.id = index
                tile.x = self.data[index].x
                tile.y = self.data[index].y
                tile.coll = self.data[index].coll
                tile.img = self.data[index].img
                tile.rect = self.data[index].rect
                self.tiles.append(tile)
                index += 1

            index += WORLD_HEIGHT - TILEAMOUNT_Y

    def assignBorders(self, width, height):
        self.borders['left'] = 0
        self.borders['bottom'] = height * TILE_SIZE - TILEAMOUNT_Y * TILE_SIZE
        self.borders['top'] = 0
        self.borders['right'] = width * TILE_SIZE - TILEAMOUNT_X * TILE_SIZE
    
    def assignBackground(self):
        self.background = Background(self.settings['background'])

    def getTile(self, x, y):
        tile_x = math.floor((x) / TILE_SIZE)
        tile_y = math.floor((y) / TILE_SIZE)
        return pygame.math.clamp((tile_y ) + (tile_x * WORLD_HEIGHT), 0, WORLD_WIDTH * WORLD_HEIGHT - 1)

    def update(self, scrollx, scrolly):
        tile : Tile
        for tile in self.tiles:
            x = tile.x - scrollx
            y = tile.y - scrolly
            loopCapX = math.ceil(SCREEN_WIDTH/ TILE_SIZE) * TILE_SIZE
            loopCapY = math.ceil(SCREEN_HEIGHT/ TILE_SIZE) * TILE_SIZE 
            offset = TILE_SIZE

            if (x > loopCapX):
                tile.id -= TILEAMOUNT_X * WORLD_HEIGHT
            if (x < -offset):
                tile.id += TILEAMOUNT_X * WORLD_HEIGHT
            if (y < -offset):
                tile.id += TILEAMOUNT_Y
            if (y > loopCapY): 
                tile.id -= TILEAMOUNT_Y
            tile.x = self.data[tile.id].x
            tile.y = self.data[tile.id].y
            tile.coll = self.data[tile.id].coll
            tile.img = self.data[tile.id].img
            tile.type = self.data[tile.id].type
            tile.rect.topleft = (tile.x, tile.y)

    def saveData(self):
        file = {}
        file['settings'] = self.settings 

        with open(self.file, 'w') as f:
            index = 0
            for data in self.data:
                file[str(index)] = {}
                file[str(index)]['type'] = self.data[index].type
                file[str(index)]['x'] = self.data[index].x
                file[str(index)]['y'] = self.data[index].y
                file[str(index)]['coll'] = self.data[index].coll
                index += 1
            json.dump(file, f)




class Manager:
    def __init__(self, filePath) -> None:

        self.tile_images = self.ReadTileSheet()
        self.levels, self.background = self.ReadLevels(filePath)
        self.selectedLevel: Level
        self.selectedLevel = self.levels[0]
    
    def ReadLevels(self, filePath):
        # Read all files in the level data directory
        files = [file for file in os.listdir(filePath) if file.endswith('.json')]
        levels = []
        for file_name in files:
            file = os.path.join(filePath, file_name)
            level = Level(self, file)
            with open(file, 'r') as file:
                data = json.load(file)
                width, height = data.get('settings').get('width'), data.get('settings').get('height')
                level.settings = data.get('settings')
                background = Background(data.get('settings').get('background'))

                numOfTiles = width * height
                
                for index in range(numOfTiles):
                    tile_data = data.get(str(index))
                    type = tile_data.get('type')
                    x = tile_data.get('x')
                    y = tile_data.get('y')
                    coll = tile_data.get('coll')
                    # Create Data object for each tile
                    level.data[index] = Data(type, x, y, coll)

            # Assign tile images
            level.assignData()
            level.assignTiles()
            level.assignBackground()
            level.assignBorders(width, height)
            levels.append(level)
        return levels, background
    
    def ReadTileSheet(self):
        tileSheet = pygame.image.load('Candy-Saga/assets/Terrain (16x16).png').convert_alpha()
        # Extracting specific tile images from the sheet
        dirt_img = tileSheet.subsurface(16 * 7, 16, 16, 16)
        grass_img = tileSheet.subsurface(16 * 7, 0, 16, 16)
        # Scaling them to the defined TILE_SIZE
        dirt_img = pygame.transform.scale(dirt_img, (TILE_SIZE, TILE_SIZE))
        grass_img = pygame.transform.scale(grass_img, (TILE_SIZE, TILE_SIZE))
        
        # Store them in the dictionary
        images = {
            'grass': grass_img,
            'dirt': dirt_img,
            'empty': None
        }

        return images

    def update(self):
        self.selectedLevel.update()
        
    


class Editor:
    def __init__(self, level : Level, input : InputHandler) -> None:
        self.input = input
        self.level = level
        self.x = 0
        self.y = 0
        self.selected_tile = None
        self.paint_area = 3
        self.type = 'dirt'
        self.img = None
        
    
    def update(self, scrollx, scrolly):
        self.paintTiles(scrollx, scrolly)
        if self.input.EditorAction.save:
            self.level.saveData()
            print("Work")
        
    def paintTiles(self, scrollx, scrolly):
        self.img = self.level.manager.tile_images[self.type]
        pos = (self.input.EditorAction.mouse + pygame.Vector2(scrollx, scrolly))
        for dx in range(-self.paint_area, self.paint_area + 1):
            for dy in range(-self.paint_area, self.paint_area + 1):
                id_offset = dx * WORLD_HEIGHT + dy
                data = self.level.data.get(int(self.level.getTile(*pos) + id_offset))
                self.selected_tile = data
                if self.selected_tile:
                    if self.input.EditorAction.paint or self.input.EditorAction.pressed:
                        data.type = self.type
                        data.img = self.img

                    if self.input.EditorAction.erase:
                        data.type = 'empty'
                        data.coll = False
                        data.img = self.level.manager.tile_images['empty']

        if self.input.EditorAction.autoTile:
            self.autoTile()


    def autoTile(self):

        for index in range(len(self.level.data)):
            if self.level.data[index].type == 'dirt':
                try:
                    if self.level.data.get(index - 1).type == 'empty':
                        self.level.data[index].type = 'grass'
                        self.level.data[index].img = self.level.manager.tile_images['grass']
                except:
                    pass

            

    
class Data:
    def __init__(self, type, x, y, coll) -> None:
        self.type = type
        self.x = x
        self.y = y
        self.coll = coll
        self.img = None
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
    
        
    

class Tile:
    def __init__(self) -> None:
        self.type = None
        self.x = None
        self.y = None
        self.coll = False
        self.img = None
        self.rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
        self.id = None


class Background:
    TILE_SIZE = 100

    class Tile:
        def __init__(self, x, y) -> None:
            self.x = x 
            self.y = y
            self.init_x = x
            self.init_y = y
            self.img = None

    def __init__(self, file, parallax= 0.6) -> None:
        self.tile_img = pygame.image.load(file)
        self.tile_img = pygame.transform.scale(self.tile_img, (self.TILE_SIZE, self.TILE_SIZE))
        self.tiles = self.generateTiles()
        self.parallax = parallax  # Factor for parallax effect
    
    def update(self, scrollx, scrolly):
        for tile in self.tiles:
            # Apply parallax effect to scroll
            tile.x = tile.init_x - scrollx * self.parallax
            tile.y = tile.init_y - scrolly * self.parallax

            # Wrap horizontally
            if tile.x < -self.TILE_SIZE:
                tile.x += (math.ceil(SCREEN_WIDTH / self.TILE_SIZE) + 1) * self.TILE_SIZE
            elif tile.x > SCREEN_WIDTH:
                tile.x -= (math.ceil(SCREEN_WIDTH / self.TILE_SIZE) + 1) * self.TILE_SIZE

            # Wrap vertically
            if tile.y < -self.TILE_SIZE:
                tile.y += (math.ceil(SCREEN_HEIGHT / self.TILE_SIZE) + 1) * self.TILE_SIZE
            elif tile.y > SCREEN_HEIGHT:
                tile.y -= (math.ceil(SCREEN_HEIGHT / self.TILE_SIZE) + 1) * self.TILE_SIZE

    def generateTiles(self):
        tile_amount_x = math.ceil(SCREEN_WIDTH / self.TILE_SIZE) + 3
        tile_amount_y = math.ceil(SCREEN_HEIGHT / self.TILE_SIZE) + 1
        tiles = []

        for x in range(tile_amount_x):
            for y in range(tile_amount_y):
                tile = self.Tile(x * self.TILE_SIZE, y * self.TILE_SIZE)
                tile.img = self.tile_img
                tiles.append(tile)
        return tiles


data = {
    'settings': {
        'width': 100,
        'height': 50,
        'background' : 'Candy-Saga/assets/Purple.png'
    }
}

index = 0
'''
for x in range(WORLD_WIDTH):
    for y in range(WORLD_HEIGHT):
        # Initialize a new dictionary for each index
        data[str(index)] = {}
        
        # Assign type, x, and y values
        data[str(index)]['type'] = 'empty'
        data[str(index)]['x'] = x * TILE_SIZE
        data[str(index)]['y'] = y * TILE_SIZE
        data[str(index)]['coll'] = True

        index += 1

# Ensure the directory exists
os.makedirs('Candy-Saga\leveldata', exist_ok=True)

# Write the data to a JSON file
with open(os.path.join('Candy-Saga/leveldata', 'Level1.json'), 'w') as file:
    json.dump(data, file, indent=4)  # Write with indentation for readability
'''