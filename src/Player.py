from GameState import GameState
from Display import Display
from Projectile import Projectile
from BaseShootable import BaseShootable
from Enums import ProjectileOrigin


class Player(BaseShootable):
    ORIGIN_TYPE = ProjectileOrigin.Player
    LIVES = 100

    def __init__(self):
        super().__init__(0, Display.BATTLEBOX_VERTICAL_BORDER)

        self.batteries = 1

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

    def shoot_projectiles(self):
        mid_x, mid_y = self.get_mid_pos()

        for x in [-1, 1]:
            for y in [-1, 1]:
                projectile = Projectile(ProjectileOrigin.Player, mid_x, mid_y, speed=250)

                projectile.direction_x = x
                projectile.direction_y = y

                self.projectiles.append(projectile)

    def battery_collision(self):
        battery = GameState.BATTERY

        x_col = False
        y_col = False

        for x in range(battery.position_x, battery.position_x + battery.SIZE):
            if x in range(int(self.position_x), int(self.position_x) + self.SIZE):
                x_col = True

        for y in range(battery.position_y, battery.position_y + battery.SIZE):
            if y in range(int(self.position_y), int(self.position_y) + self.SIZE):
                y_col = True

        return x_col and y_col
