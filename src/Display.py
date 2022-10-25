from GameState import GameState
from Enums import ScreenCodes
from Button import Button
import pygame
import win32gui

pygame.init()


class Display:
    WIDTH = 500
    HEIGHT = 600

    BATTLEBOX_VERTICAL_BORDER = 50

    def __init__(self, screen):
        self.screen = screen

        self.font = pygame.font.Font("lib/font/FreeSansBold.ttf", 15)
        self.font_arka = pygame.font.Font("lib/font/ARKANOID.TTF", 35)
        self.font_big = pygame.font.Font("lib/font/FreeSansBold.ttf", 125)

        self.frame_num = 0

        self.windows = []

        self.images = {
            "background_bs": pygame.image.load("lib/images/background_bs.png"),
            "hearth": pygame.image.load("lib/images/hearth.png"),
            "battery_icon": pygame.image.load("lib/images/battery-icon.png"),
            "button_template": pygame.image.load("lib/images/ms_button_template.png"),
            "exit_button": pygame.image.load("lib/images/exit_icon.png"),
            "logo": pygame.image.load("lib/images/logo.png")
        }

        self.sprites = {
            "battery": pygame.image.load("lib/sprites/battery.png"),
            "pulse": pygame.image.load("lib/sprites/pulse.png"),
            "spike": pygame.image.load("lib/sprites/spike.png"),
            "player": pygame.image.load("lib/sprites/player.png"),
            "enemy": {
                "original": pygame.image.load("lib/sprites/enemy.png"),
                "active": pygame.image.load("lib/sprites/enemy.png"),
                "rect": None
            }
        }

        self.buttons = {
            "ms": {
                "continue": Button(300, 60, position=[100, 250], image=self.images["button_template"],
                                   onclick=GameState.select_player),
                "new_game": Button(300, 60, position=[100, 350], image=self.images["button_template"],
                                   onclick=GameState.create_player),
                "exit": Button(40, 40, position=[440, 540], image=self.images["exit_button"], onclick=GameState.exit)
            },
            "bs": {
                "pause": Button(20, 20, position=[445, 15]),
                "stop": Button(20, 20, position=[470, 15], onclick=lambda: GameState.set_screen(ScreenCodes.MA))
            }
        }

        self.sprites["enemy"]["rect"] = self.sprites["enemy"]["active"].get_rect()

    def window_enumeration_handler(self, hwnd, windows):
        self.windows.append((hwnd, win32gui.GetWindowText(hwnd)))

    def update(self, frame_num):
        self.screen.fill((40, 40, 40))
        self.frame_num = frame_num

        if GameState.SCREEN_CODE == ScreenCodes.MA:
            self.draw_main_screen()
        elif GameState.SCREEN_CODE == ScreenCodes.SH:
            self.draw_shop_screen()
        elif GameState.SCREEN_CODE == ScreenCodes.BA:
            self.draw_battle_screen()
        else:
            print(f"Can't draw with screencode {GameState.SCREEN_CODE}")

        pygame.display.update()

    def draw_main_screen(self):
        self.screen.blit(self.images["logo"], (40, 100))

        # Draw all buttons
        for button in self.buttons["ms"]:
            self.buttons["ms"][button].draw(self.screen)
            self.buttons["ms"][button].check_onclick()

        text_continue = self.font_arka.render("Continue", True, (255, 255, 255))
        text_new_game = self.font_arka.render("New Game", True, (255, 255, 255))

        button_continue = self.buttons["ms"]["continue"]
        button_new_game = self.buttons["ms"]["new_game"]

        self.screen.blit(text_continue, (button_continue.position[0] + 55, button_continue.position[1] + 15))
        self.screen.blit(text_new_game, (button_new_game.position[0] + 55, button_new_game.position[1] + 15))

    def draw_shop_screen(self):
        # temp
        text = self.font.render("Game Over!", True, (255, 255, 255))
        self.screen.blit(text, (200, 200))

    def draw_battle_screen(self):
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

        # Player open---

        sprite = self.sprites["player"]
        player = GameState.PLAYER

        rotation = 0
        if player.direction == "left":
            rotation = 90
        elif player.direction == "right":
            rotation = 270
        elif player.direction == "down":
            rotation = 180

        sprite = pygame.transform.rotate(sprite, rotation)
        self.screen.blit(sprite, (player.position_x, player.position_y))

        # Player close---

        sprite = self.sprites["spike"]
        for projectile in GameState.ENEMY.projectiles:
            self.screen.blit(sprite, (projectile.position_x, projectile.position_y))

        sprite = self.sprites["pulse"]
        for projectile in GameState.PLAYER.projectiles:
            self.screen.blit(sprite, (projectile.position_x, projectile.position_y))

    def draw_number(self, number):
        text = self.font_big.render(f"{int(number)}", True, (255, 160, 75))
        self.screen.blit(text, (240, 200))
        pygame.display.update()
