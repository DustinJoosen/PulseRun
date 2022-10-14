from GameState import GameState
from Display import Display
from Projectile import Projectile
from BaseShootable import BaseShootable
from SetInterval import SetInterval
from Enums import ProjectileOrigin


class Enemy(BaseShootable):
    SPEED = 80
    PROJECTILE_INTERVAL = 1
    ORIGIN_TYPE = ProjectileOrigin.Enemy

    def __init__(self):
        super().__init__((Display.WIDTH - self.SIZE), Display.BATTLEBOX_VERTICAL_BORDER)

        self.direction_x = 0
        self.direction_y = 0

        self.color = (50, 50, 255)

        GameState.ENEMY = self

        self.thread = SetInterval(self.shoot_projectile, self.PROJECTILE_INTERVAL)

        self.damage_ticks = 0
        self.is_stunned = False

    def update_position(self):
        # If stunned, don't update anything
        if self.is_stunned:
            self.color = (255, 100, 100)

            if self.damage_ticks < 86:
                self.damage_ticks += 1
            else:
                self.is_stunned = False
                self.damage_ticks = 0
                self.color = (50, 50, 255)

            return

        # Move
        self.position_x += (self.direction_x / 100) * self.SPEED
        self.position_y += (self.direction_y / 100) * self.SPEED

        self.update_projectiles()

        # Wall collisions
        if self.position_x <= 0:
            self.direction_x = 1
        elif self.position_x >= Display.WIDTH - self.SIZE:
            self.direction_x = -1

        if self.position_y <= Display.BATTLEBOX_VERTICAL_BORDER:
            self.direction_y = 1
        elif self.position_y >= Display.HEIGHT - self.SIZE:
            self.direction_y = -1

    def shoot_projectile(self):
        if self.is_stunned:
            return

        mid_x, mid_y = self.get_mid_pos()
        projectile = Projectile(ProjectileOrigin.Enemy, mid_x, mid_y)

        player_pos = [GameState.PLAYER.position_x, GameState.PLAYER.position_y]
        enemy_pos = [self.position_x, self.position_y]

        distance_x = player_pos[0] - enemy_pos[0]
        distance_y = player_pos[1] - enemy_pos[1]

        projectile.direction_x = distance_x / 100
        projectile.direction_y = distance_y / 100

        self.projectiles.append(projectile)
