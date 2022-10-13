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

        self.frame_num = 0

        self.images = {
            "background_bs": pygame.image.load("lib/images/background_bs.png")
        }

        self.sprites = {
            "battery": pygame.image.load("lib/sprites/battery.png"),
            "pulse": pygame.image.load("lib/sprites/pulse.png"),
            "spike": pygame.image.load("lib/sprites/spike.png")
        }

    def update(self, frame_num):
        self.screen.fill((40, 40, 40))
        self.frame_num = frame_num

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
        text = self.font.render("Main screen", True, (255, 255, 255))
        self.screen.blit(text, (0, 0))

    def __draw_shop_screen(self):
        text = self.font.render("Shop screen", True, (255, 255, 255))
        self.screen.blit(text, (0, 0))

    def __draw_battle_screen(self):
        self.screen.blit(self.images["background_bs"], (0, self.BATTLEBOX_VERTICAL_BORDER))
        self.screen.blit(self.sprites["battery"], (GameState.BATTERY.position_x, GameState.BATTERY.position_y))

        pygame.draw.rect(self.screen, (40, 40, 40), [0, 0, self.WIDTH, self.BATTLEBOX_VERTICAL_BORDER])

        points_text = self.font.render(f"{int(GameState.PLAYER.batteries)} batteries", True, (255, 255, 255))
        self.screen.blit(points_text, (300, 25))

        pygame.draw.rect(self.screen, GameState.ENEMY.color,
                         [GameState.ENEMY.position_x, GameState.ENEMY.position_y, GameState.ENEMY.SIZE, GameState.ENEMY.SIZE])

        pygame.draw.rect(self.screen, (0, 255, 0),
                         [GameState.PLAYER.position_x, GameState.PLAYER.position_y, GameState.PLAYER.SIZE , GameState.PLAYER.SIZE])

        lives_text = self.font.render(f"{GameState.PLAYER.LIVES}", True, (255, 255, 255))
        self.screen.blit(lives_text, (GameState.PLAYER.position_x + 10, GameState.PLAYER.position_y + 15))

        sprite = self.sprites["spike"]
        for projectile in GameState.ENEMY.projectiles:
            self.screen.blit(sprite, (projectile.position_x, projectile.position_y))

        sprite = self.sprites["pulse"]
        for projectile in GameState.PLAYER.projectiles:
            self.screen.blit(sprite, (projectile.position_x, projectile.position_y))
