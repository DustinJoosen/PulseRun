from GameState import GameState
from Display import Display
from random import randint


class Battery:
    SIZE = 40

    def __init__(self):
        self.position_x = randint(0, Display.WIDTH - self.SIZE)
        self.position_y = randint(Display.BATTLEBOX_VERTICAL_BORDER, Display.HEIGHT - self.SIZE)

        self.prev_values = [1]
        self.value = 1

        GameState.BATTERY = self

    def regenerate(self):
        # Add a new sequence to the fibonacci sequence
        new_val = self.prev_values[-1] + self.value
        self.prev_values.append(self.value)
        self.value = new_val

        self.position_x = randint(0, Display.WIDTH - self.SIZE)
        self.position_y = randint(Display.BATTLEBOX_VERTICAL_BORDER, Display.HEIGHT - self.SIZE)
