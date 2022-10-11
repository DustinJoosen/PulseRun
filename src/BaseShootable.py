from GameState import GameState
from Enums import ProjectileOrigin


class BaseShootable:
    SIZE = 40

    def __init__(self, x=0, y=0):
        self.position_x = x
        self.position_y = y

        self.projectiles = []

    def get_mid_pos(self):
        mid_x = list(range(int(self.position_x), int(self.position_x) + self.SIZE))[int(self.SIZE / 2 - 1)]
        mid_y = list(range(int(self.position_y), int(self.position_y) + self.SIZE))[int(self.SIZE / 2 - 1)]

        return mid_x, mid_y

    def update_projectiles(self):
        for projectile in self.projectiles:
            projectile.update_position()

            # No need for invisible projectiles. just remove them
            if projectile.out_of_bounds():
                projectile.direction_x = 0
                projectile.direction_y = 0

                self.projectiles.remove(projectile)

            if projectile.has_collision():
                self.projectiles.remove(projectile)

                if projectile.source == ProjectileOrigin.Enemy:
                    GameState.PLAYER.LIVES -= 1
                    print(f"Player lost a life! Only {GameState.PLAYER.LIVES} lives left!")

                    if GameState.PLAYER.LIVES <= 0:
                        GameState.RUNNING = False