# villain.py
from object import Object
import pygame

class Villain(Object):
    def __init__(self, hp, name, power, x, y, width, height, speed, sprite_sheet_path=None, num_frames=0):
        super().__init__(hp, name, power, x, y, width, height, speed, sprite_sheet_path, num_frames)

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            print(f"{self.name} defeated!")
            return True  # Indicate that the villain was defeated
        return False  # Indicate that the villain is still alive

    def draw(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, self.width, self.height))  # Red for villains
