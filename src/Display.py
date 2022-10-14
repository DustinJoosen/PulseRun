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
            "background_bs": pygame.image.load("lib/images/background_bs.png"),
            "hearth": pygame.image.load("lib/images/hearth.png"),
            "battery_icon": pygame.image.load("lib/images/battery-icon.png")
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
        # temp
        text = self.font.render("Main screen", True, (255, 255, 255))
        self.screen.blit(text, (0, 0))

    def __draw_shop_screen(self):
        # temp
        text = self.font.render("Game Over!", True, (255, 255, 255))
        self.screen.blit(text, (200, 200))

    def __draw_battle_screen(self):
        self.screen.blit(self.images["background_bs"], (0, self.BATTLEBOX_VERTICAL_BORDER))
        self.screen.blit(self.sprites["battery"], (GameState.BATTERY.position_x, GameState.BATTERY.position_y))

        pygame.draw.rect(self.screen, (40, 40, 40), [0, 0, self.WIDTH, self.BATTLEBOX_VERTICAL_BORDER])

        # Score bar open
        hearths = GameState.PLAYER.lives
        if hearths >= 6:
            hearths = 6

        for i in range(hearths):
            self.screen.blit(self.images["hearth"], (10 + (i * 25), 15))

        score_text = self.font.render(f"Score: {GameState.PLAYER.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (175, 18))

        self.screen.blit(self.images["battery_icon"], (300, 10))

        batteries_text = self.font.render(f"{int(GameState.PLAYER.batteries)} batteries", True, (255, 255, 255))
        self.screen.blit(batteries_text, (325, 18))

        # Score bar close

        # Enemy open---
        enemy = GameState.ENEMY
        pygame.draw.rect(self.screen, enemy.color,
                         [enemy.position_x, enemy.position_y, enemy.SIZE, GameState.ENEMY.SIZE])

        pygame.draw.rect(self.screen, (255, 255, 255),
                         [enemy.position_x + 4, enemy.position_y + 4, enemy.SIZE - 8, GameState.ENEMY.SIZE - 8])
        # Enemy close---

        pygame.draw.rect(self.screen, (0, 255, 0),
                         [GameState.PLAYER.position_x, GameState.PLAYER.position_y, GameState.PLAYER.SIZE , GameState.PLAYER.SIZE])

        sprite = self.sprites["spike"]
        for projectile in GameState.ENEMY.projectiles:
            self.screen.blit(sprite, (projectile.position_x, projectile.position_y))

        sprite = self.sprites["pulse"]
        for projectile in GameState.PLAYER.projectiles:
            self.screen.blit(sprite, (projectile.position_x, projectile.position_y))
