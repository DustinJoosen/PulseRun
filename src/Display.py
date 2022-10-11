from GameState import GameState
from Enums import ScreenCodes
import pygame

pygame.init()


class Display:
    WIDTH = 500
    HEIGHT = 600

    BATTLEBOX_VERTICAL_BORDER = 50

    def __init__(self, screen):
        self.screen = screen

        self.font = pygame.font.Font("freesansbold.ttf", 15)

    def update(self):
        self.screen.fill((0, 0, 0))

        if GameState.SCREEN_CODE == ScreenCodes.MA:
            self.__draw_main_screen()
        elif GameState.SCREEN_CODE == ScreenCodes.SH:
            self.__draw_shop_screen()
        elif GameState.SCREEN_CODE == ScreenCodes.BA:
            self.__draw_battle_screen()
        else:
            print(f"Can't draw with screencode {GameState.SCREEN_CODE}")

        pygame.display.update()

    def __draw_main_screen(self):
        pass

    def __draw_shop_screen(self):
        pass

    def __draw_battle_screen(self):
        # Temp
        pygame.draw.rect(self.screen, (0, 255, 255), [0, 0, self.WIDTH, self.BATTLEBOX_VERTICAL_BORDER])
        pygame.draw.rect(self.screen, (255, 255, 0), [0, self.BATTLEBOX_VERTICAL_BORDER, self.WIDTH, self.HEIGHT - self.BATTLEBOX_VERTICAL_BORDER])

        pygame.draw.rect(self.screen, (0, 255, 0),
                         [GameState.PLAYER.position_x, GameState.PLAYER.position_y, GameState.PLAYER.SIZE , GameState.PLAYER.SIZE])

        pygame.draw.rect(self.screen, GameState.ENEMY.color,
                         [GameState.ENEMY.position_x, GameState.ENEMY.position_y, GameState.ENEMY.SIZE, GameState.ENEMY.SIZE])

        for projectile in GameState.ENEMY.projectiles:
            pygame.draw.rect(self.screen, (255, 255, 255), [projectile.position_x, projectile.position_y, projectile.SIZE, projectile.SIZE])

        for projectile in GameState.PLAYER.projectiles:
            pygame.draw.rect(self.screen, (255, 255, 255), [projectile.position_x, projectile.position_y, projectile.SIZE, projectile.SIZE])

        pygame.draw.rect(self.screen, (0, 0, 255),
                         [GameState.BATTERY.position_x, GameState.BATTERY.position_y, GameState.BATTERY.SIZE, GameState.BATTERY.SIZE])

        battery_text = self.font.render(f"{GameState.BATTERY.value}", True, (255, 255, 255))
        self.screen.blit(battery_text, (GameState.BATTERY.position_x + 10, GameState.BATTERY.position_y + 15))
