import pygame
from GameState import GameState
from Display import Display
from Enums import ScreenCodes
from Player import Player
from Enemy import Enemy
from Battery import Battery
from Button import Button
from SetInterval import SetInterval
from time import sleep
import win32gui

pygame.init()

screen = pygame.display.set_mode((Display.WIDTH, Display.HEIGHT))
caption = pygame.display.set_caption("Pulse Run")

clock = pygame.time.Clock()

display = Display(screen)

frame_num = None
pause = None

windows = []


# This is initialized in a function, so that it can easily be reset.
def initialize_battle():
    global frame_num
    global pause

    frame_num = 1
    pause = False

    # Bring the window to the front
    for window in display.windows:
        if window[1] == "Pulse Run":
            win32gui.ShowWindow(window[0], 5)
            win32gui.SetForegroundWindow(window[0])

    Player()
    Battery()
    Enemy()

    display.frame_num = frame_num

    for i in range(3, 0, -1):
        display.draw_battle_screen()
        display.draw_number(i)

        sleep(1)

    GameState.ENEMY.start_thread()


win32gui.EnumWindows(display.window_enumeration_handler, display.windows)

# Allow the GameState to reset the battle
GameState.INIT_BATTLE = initialize_battle

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

        if event.type == pygame.MOUSEBUTTONDOWN:
            Button.MOUSE_DOWN = True
            print("button mouse down set to true")
        else:
            Button.MOUSE_DOWN = False
            print("button mouse down is set to false")

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
            # GameState.set_screen(ScreenCodes.SH)
            if (new_highscore := GameState.PLAYER.score) > GameState.TOP_SCORE:
                GameState.TOP_SCORE = new_highscore
                print("New Top score!!! " + str(new_highscore))

            GameState.set_save_file()

            GameState.ENEMY.thread.cancel()
            print(f"Batteries: {int(GameState.PLAYER.batteries)}\nScore: {GameState.PLAYER.score}")

            GameState.SCREEN_CODE = ScreenCodes.BA
            GameState.select_player()
            continue

        GameState.ENEMY.update_position()
        GameState.PLAYER.update_projectiles()

        button = display.buttons["bs"]["pause"]
        if button.check_onclick():
            pause = not pause
            print("toggled pause button. now " + str(pause))

        frame_num += 1

    display.update(frame_num)

# The enemy thread continues going after screen-death, so if there is an active thread, cancel it.
if GameState.ENEMY:
    GameState.ENEMY.thread.cancel()
