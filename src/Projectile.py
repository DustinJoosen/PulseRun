from Display import Display
from Enums import ProjectileOrigin
from GameState import GameState


class Projectile:
    SIZE = 10
    SPEED = 80

    def __init__(self, source, pos_x=0, pos_y=0):
        self.position_x = pos_x
        self.position_y = pos_y

        self.direction_x = 1
        self.direction_y = 0

        self.source = source

    def update_position(self):
        # Move
        self.position_x += (self.direction_x / 100) * self.SPEED
        self.position_y += (self.direction_y / 100) * self.SPEED

    def out_of_bounds(self):
        size = self.SIZE

        if self.position_x < 0 - size or self.position_x > Display.WIDTH:
            return True

        if self.position_y < Display.BATTLEBOX_VERTICAL_BORDER - size or self.position_y > Display.HEIGHT + size:
            return True

        return False

    def has_collision(self):
        player = GameState.PLAYER
        enemy = GameState.ENEMY

        for entity in [player, enemy]:
            if self.source == entity.ORIGIN_TYPE:
                continue

            x_col = False
            y_col = False

            for x in range(int(entity.position_x), int(entity.position_x) + entity.SIZE):
                if x in range(int(self.position_x), int(self.position_x) + self.SIZE):
                    x_col = True

            for y in range(int(entity.position_y), int(entity.position_y) + entity.SIZE):
                if y in range(int(self.position_y), int(self.position_y) + self.SIZE):
                    y_col = True

            if x_col and y_col:
                return True

        return False
