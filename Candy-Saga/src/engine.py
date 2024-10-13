import pygame
import sys
from pygame.locals import *

# Initialize pygame
pygame.init()

# Set up display
display_w = 350
display_h = 600
window = pygame.display.set_mode((display_w, display_h), HWSURFACE | DOUBLEBUF | RESIZABLE)
pygame.display.set_caption("Candy Saga")

# Set up the clock for frame rate control
clock = pygame.time.Clock()

# Define your Object and Hero classes
class Object:
    def __init__(self, hp, name, power, x, y, width, height, speed, sprite_sheet_path, num_frames):
        self.hp = hp
        self.name = name
        self.power = power
        self.x = x
        self.y = y
        self.width = width  # Adjusted for each frame's width
        self.height = height  # Adjusted for the frame's height
        self.speed = speed

        # Load the sprite sheet
        try:
            self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        except pygame.error as e:
            print(f"Error loading sprite sheet: {e}")
            sys.exit()

        # Animation variables
        self.num_frames = num_frames
        self.current_frame = 0
        self.animation_speed = 5  # Controls the speed of the animation
        self.frame_count = 0

        # Extract frames from the sprite sheet
        self.frames = []
        for i in range(self.num_frames):
            frame = self.sprite_sheet.subsurface(pygame.Rect(i * self.width, 0, self.width, self.height))
            self.frames.append(frame)

    def draw(self, window):
        # Draw the current frame of animation
        window.blit(self.frames[self.current_frame], (self.x, self.y))

    def update_animation(self):
        self.frame_count += 1
        if self.frame_count >= self.animation_speed:
            self.frame_count = 0
            self.current_frame = (self.current_frame + 1) % self.num_frames

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.update_animation()  # Update animation when moving
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.update_animation()
        if keys[pygame.K_UP]:
            self.y -= self.speed
            self.update_animation()
        if keys[pygame.K_DOWN]:
            self.y += self.speed
            self.update_animation()

