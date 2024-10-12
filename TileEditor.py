import pygame
import os
import json

WORLD_WIDTH = 100
WORLD_HEIGHT = 100
TILE_SIZE = 25

class Level:
    def __init__(self) -> None:
        self.tiles = []
    

class Manager:
    def __init__(self, filePath) -> None:
        self.levels = self.ReadLevels(filePath)
        self.selectedLevel = self.levels[0]
        pass
    def ReadLevels(self, filePath):
        
        files = [file for file in os.listdir(filePath)]
        levels = []
        for file_name in files:
            level = Level()
            with open(os.path.join(filePath,file_name), 'r') as file:
                file = json.load(file)
                index = 0
                for x in range(WORLD_WIDTH):
                    for y in range(WORLD_HEIGHT):
                        tile = Tile((x,y), file[index])
                        level.tiles.append(tile)
                        index += 1
            levels.append(level)
        return levels
    def update(self):
        self.selectedLevel.update()

        

            


class Tile:
    TYPES = {
        0 : 'empty',
        1 : 'grass'
    }

    

    def __init__(self, pos, type) -> None:
        self.x = pos[0]
        self.y = pos[1]
        self.type = self.TYPES[type]
        
        pass


'''
check out branch 
make changes
add commit push
pull request
'''

data = []
'''
for x in range(WORLD_WIDTH):
    for y in range(WORLD_HEIGHT):
        data.append(0)

with open('Level Data\Level1', 'w') as file:
    json.dump(data, file)'''
