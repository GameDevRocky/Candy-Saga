from abc import ABC, abstractmethod

class Candy(ABC):
    def __init__(self, worth, speed, size, color):
        self.worth = worth  # Damage to the villain
        self.speed = speed  # Movement speed
        self.size = size    # Size of the candy
        self.color = color  # Color for rendering

    @abstractmethod
    def shoot(self):
        pass

    def get_worth(self):
        return self.worth


class ChocolateCandy(Candy):
    def __init__(self):
        super().__init__(worth=10, speed=5, size=5, color=(150, 75, 0))

    def shoot(self):
        print("Shooting a chocolate candy!")


class GummyCandy(Candy):
    def __init__(self):
        super().__init__(worth=15, speed=4, size=6, color=(255, 0, 0))

    def shoot(self):
        print("Shooting a gummy candy!")
