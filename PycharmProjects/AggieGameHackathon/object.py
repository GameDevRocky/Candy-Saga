import pygame
import sys

class Object:
    def __init__(self, hp, name, power, x, y, width, height, speed, sprite_sheet_path=None, num_frames=0):
        self.hp = hp
        self.name = name
        self.power = power
        self.x = x
        self.y = y
        self.width = width  # Adjusted for each frame's width
        self.height = height  # Adjusted for the frame's height
        self.speed = speed

        # Load the sprite sheet only if a path is provided
        if sprite_sheet_path:
            try:
                self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
            except pygame.error as e:
                print(f"Error loading sprite sheet: {e}")
                sys.exit()
        else:
            self.sprite_sheet = None  # Set to None if no sprite sheet is provided

        # Animation variables
        self.num_frames = num_frames
        self.current_frame = 0
        self.animation_speed = 5  # Controls the speed of the animation
        self.frame_count = 0

        # Extract frames from the sprite sheet if it exists
        self.frames = []
        if self.sprite_sheet:
            for i in range(self.num_frames):
                frame = self.sprite_sheet.subsurface(pygame.Rect(i * self.width, 0, self.width, self.height))
                self.frames.append(frame)

    def draw(self, window):
        # Draw the current frame of animation if sprite sheet is available
        if self.frames:
            window.blit(self.frames[self.current_frame], (self.x, self.y))
        else:
            # Draw a rectangle if no sprite sheet is available
            pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, self.width, self.height))

    def update_animation(self):
        if self.num_frames > 0:  # Only update if there are frames to animate
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