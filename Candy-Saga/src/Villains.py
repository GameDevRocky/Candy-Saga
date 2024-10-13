from main import Object

class Villains(Object):
    def __init__(self, hp, name, power, x, y, width, height, speed, sprite_sheet_path, num_frames):
        super().__init__(hp, name, power, x, y, width, height, speed, sprite_sheet_path, num_frames)

