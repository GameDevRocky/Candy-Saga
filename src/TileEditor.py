import pygame
import os
import json
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WORLD_WIDTH = 100
WORLD_HEIGHT = 100
TILE_SIZE = 25
TILEAMOUNT_X = math.ceil(SCREEN_WIDTH/TILE_SIZE) + 1
TILEAMOUNT_Y = math.ceil(SCREEN_HEIGHT/TILE_SIZE) + 1

class Level:
    def __init__(self, manager) -> None:
        self.data = {}
        self.tiles = []
        self.borders = {}
        self.manager = manager

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


        


        


class Manager:
    def __init__(self, filePath) -> None:
        self.tile_images = self.ReadTileSheet()
        self.levels = self.ReadLevels(filePath)
        self.selectedLevel: Level
        self.selectedLevel = self.levels[0]
    
    def ReadLevels(self, filePath):
        # Read all files in the level data directory
        files = [file for file in os.listdir(filePath) if file.endswith('.json')]
        levels = []
        for file_name in files:
            level = Level(self)
            with open(os.path.join(filePath, file_name), 'r') as file:
                data = json.load(file)
                width, height = data.get('settings').get('width'), data.get('settings').get('height')
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
            level.assignBorders(width, height)
            levels.append(level)
        return levels
    
    def ReadTileSheet(self):
        tileSheet = pygame.image.load('Images/Terrain (16x16).png').convert_alpha()
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
    def update(self):

        pass



# Sample JSON Data Creation
data = {
    'settings': {
        'width': 100,
        'height': 100
    }
}

index = 0

for x in range(WORLD_WIDTH):
    for y in range(WORLD_HEIGHT):
        # Initialize a new dictionary for each index
        data[str(index)] = {}
        
        # Assign type, x, and y values
        data[str(index)]['type'] = 'grass'
        data[str(index)]['x'] = x * TILE_SIZE
        data[str(index)]['y'] = y * TILE_SIZE
        data[str(index)]['coll'] = True

        index += 1

# Ensure the directory exists
os.makedirs('Level Data', exist_ok=True)

# Write the data to a JSON file
with open(os.path.join('Level Data', 'Level1.json'), 'w') as file:
    json.dump(data, file, indent=4)  # Write with indentation for readability
