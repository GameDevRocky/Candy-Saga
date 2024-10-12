import pygame

class Bullet:
    def __init__(self, x, y, width, height, speed, damage):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.damage = damage  # Damage that this bullet can inflict
        self.is_active = True  # To track if the bullet is still in play

    def update(self):
        self.x += self.speed  # Move the bullet to the right

        # Deactivate the bullet if it goes off-screen (adjust for right-side)
        if self.x > 350:  # Assuming your window width is 350
            self.is_active = False

    def draw(self, window):
        if self.is_active:
            pygame.draw.rect(window, (255, 255, 0), (self.x, self.y, self.width, self.height))  # Yellow bullet
