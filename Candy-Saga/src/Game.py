import pygame
from candy import ChocolateCandy, GummyCandy
from Villains import Villains

class Game:
    def __init__(self, villain):
        self.villain = Villains
        self.candies = []

    def shoot_candy(self, candy):
        candy.shoot()
        self.candies.append(candy)

    def update(self):
        for candy in self.candies:
            # Move candy (simplified)
            candy.speed += 1
            if self.check_collision(candy):
                self.handle_collision(candy)

    def check_collision(self, candy):
        # Simplified collision detection for now
        return candy.speed > 10  # Dummy condition

    def handle_collision(self, candy):
        damage = candy.get_worth()
        is_defeated = self.villain.take_damage(damage)
        if is_defeated:
            self.explode_candy()

    def explode_candy(self):
        print("Candy explosion! Main character can collect the candies.")

def game_loop():
    villain = Villains(100)  # 100 HP
    game = Game(villain)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    candy = ChocolateCandy()
                    game.shoot_candy(candy)

        game.update()
        pygame.display.update()

game_loop()
