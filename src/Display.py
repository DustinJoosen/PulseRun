from GameState import GameState
from Enums import ScreenCodes
from Button import Button
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
            "spike": pygame.image.load("lib/sprites/spike.png"),
            "orig_enemy": pygame.image.load("lib/sprites/enemy.png"),
            "enemy": {
                "original": pygame.image.load("lib/sprites/enemy.png"),
                "active": pygame.image.load("lib/sprites/enemy.png"),
                "rect": None
            }
        }

        self.buttons = {
            "bs": {
                "pause": Button(20, 20, position=[445, 15]),
                "stop": Button(20, 20, position=[470, 15])
            }
        }

        self.sprites["enemy"]["rect"] = self.sprites["enemy"]["active"].get_rect()

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

        self.buttons["bs"]["pause"].draw(self.screen)
        self.buttons["bs"]["stop"].draw(self.screen)
        # Score bar close

        # Enemy open---

        enemy = GameState.ENEMY
        rotation = self.frame_num - int(self.frame_num / 360) * 360

        self.sprites["enemy"]["active"] = pygame.transform.rotate(self.sprites["enemy"]["original"], rotation)
        x, y = (enemy.position_x + enemy.SIZE / 2, enemy.position_y + enemy.SIZE / 2)
        self.sprites["enemy"]["rect"] = self.sprites["enemy"]["active"].get_rect()
        self.sprites["enemy"]["rect"].center = (x, y)

        self.sprites["enemy"]["active"].fill(enemy.color, special_flags=pygame.BLEND_ADD)

        self.screen.blit(self.sprites["enemy"]["active"], self.sprites["enemy"]["rect"])

        # Enemy close---

        pygame.draw.rect(self.screen, (0, 255, 0),
                         [GameState.PLAYER.position_x, GameState.PLAYER.position_y, GameState.PLAYER.SIZE , GameState.PLAYER.SIZE])

        sprite = self.sprites["spike"]
        for projectile in GameState.ENEMY.projectiles:
            self.screen.blit(sprite, (projectile.position_x, projectile.position_y))

        sprite = self.sprites["pulse"]
        for projectile in GameState.PLAYER.projectiles:
            self.screen.blit(sprite, (projectile.position_x, projectile.position_y))
