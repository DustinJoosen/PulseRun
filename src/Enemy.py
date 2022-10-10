from GameState import GameState
from Display import Display


class Enemy:
    SIZE = 40
    SPEED = 20

    def __init__(self):
        self.position_x = Display.WIDTH - self.SIZE
        self.position_y = Display.BATTLEBOX_VERTICAL_BORDER

        self.direction_x = 0
        self.direction_y = 0

        self.color = (200, 200, 255)

        GameState.ENEMY = self

    def update_position(self):
        # Move
        self.position_x += (self.direction_x / 100) * self.SPEED
        self.position_y += (self.direction_y / 100) * self.SPEED

        # Wall collisions
        if self.position_x <= 0:
            self.direction_x = 1
        elif self.position_x >= Display.WIDTH - self.SIZE:
            self.direction_x = -1

        if self.position_y <= Display.BATTLEBOX_VERTICAL_BORDER:
            self.direction_y = 1
        elif self.position_y >= Display.HEIGHT - self.SIZE:
            self.direction_y = -1

        # Player collisions
        player = GameState.PLAYER
        collision_x = False
        collision_y = False

        for x in range(int(self.position_x), int(self.position_x) + self.SIZE):
            if x in range(int(player.position_x), int(player.position_x) + player.SIZE):
                collision_x = True

        for y in range(int(self.position_y), int(self.position_y) + self.SIZE):
            if y in range(int(player.position_y), int(player.position_y) + player.SIZE):
                collision_y = True

        if collision_x and collision_y:
            self.direction_x = -self.direction_x
            self.direction_y = -self.direction_y
