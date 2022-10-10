from GameState import GameState
from Display import Display


class Player:
    SIZE = 40

    def __init__(self):
        self.position_x = 0
        self.position_y = Display.BATTLEBOX_VERTICAL_BORDER

        # self.direction_x = 0
        # self.direction_y = 0

        GameState.PLAYER = self

    def update_position(self, direction):
        movement = (GameState.PLAYER.SIZE / 100) * GameState.PLAYER_SPEED

        if direction == "left" and self.position_x > 0:
            self.position_x -= movement
        if direction == "right" and self.position_x < Display.WIDTH - self.SIZE:
            self.position_x += movement
        if direction == "up" and self.position_y > Display.BATTLEBOX_VERTICAL_BORDER:
            self.position_y -= movement
        if direction == "down" and self.position_y < Display.HEIGHT - self.SIZE:
            self.position_y += movement

