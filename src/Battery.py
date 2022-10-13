from GameState import GameState
from Display import Display
from random import randint


class Battery:
    SIZE = 40

    def __init__(self):
        self.position_x = randint(0, Display.WIDTH - self.SIZE)
        self.position_y = randint(Display.BATTLEBOX_VERTICAL_BORDER, Display.HEIGHT - self.SIZE)

        self.value = 1

        GameState.BATTERY = self

    def regenerate(self):
        self.value *= 1.1

        self.position_x = randint(0, Display.WIDTH - self.SIZE)
        self.position_y = randint(Display.BATTLEBOX_VERTICAL_BORDER, Display.HEIGHT - self.SIZE)
