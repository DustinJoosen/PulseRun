import pygame
from GameState import GameState
from Display import Display
from Enums import ScreenCodes
from Player import Player
from Enemy import Enemy
from Battery import Battery
from SetInterval import SetInterval

pygame.init()

screen = pygame.display.set_mode((Display.WIDTH, Display.HEIGHT))
caption = pygame.display.set_caption("Pulse Run")

clock = pygame.time.Clock()

display = Display(screen)

player = Player()
enemy = Enemy()

battery = Battery()

frame_num = 0

pause = False

GameState.init()

while GameState.RUNNING:
    clock.tick(64)

    # If you press 'q' or the exit button, stop the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            GameState.RUNNING = False
            continue

        if event.type == pygame.KEYDOWN:
            if not pause and event.key == pygame.K_SPACE and GameState.PLAYER.batteries >= 4:
                GameState.PLAYER.shoot_projectiles()
                GameState.PLAYER.batteries -= 4
            elif event.key == pygame.K_p:
                pause = not pause

    if GameState.SCREEN_CODE == ScreenCodes.MA:
        pass

    if GameState.SCREEN_CODE == ScreenCodes.SH:
        pass

    if GameState.SCREEN_CODE == ScreenCodes.BA:
        if pause:
            continue

        GameState.PLAYER.score += 7

        # Input handling
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            GameState.PLAYER.update_position("left")
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            GameState.PLAYER.update_position("right")
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            GameState.PLAYER.update_position("up")
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            GameState.PLAYER.update_position("down")

        if GameState.PLAYER.battery_collision():
            GameState.PLAYER.batteries += GameState.BATTERY.value
            GameState.BATTERY.regenerate()

        # If gameover, goto shop
        if GameState.PLAYER.lives <= 0:
            GameState.SCREEN_CODE = ScreenCodes.SH
            GameState.set_save_file()
            continue

        GameState.ENEMY.update_position()
        GameState.PLAYER.update_projectiles()

        button = display.buttons["bs"]["pause"]
        if button.is_hovering():
            print("hovering pause")

        frame_num += 1

    display.update(frame_num)

GameState.ENEMY.thread.cancel()
print(f"Batteries: {int(GameState.PLAYER.batteries)}\nScore: {GameState.PLAYER.score}")
