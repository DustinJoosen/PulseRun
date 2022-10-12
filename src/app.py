import pygame
from GameState import GameState
from Display import Display
from Enums import ScreenCodes
from Player import Player
from Enemy import Enemy
from Battery import Battery
from SetInterval import SetInterval

pygame.init()
GameState.init()

screen = pygame.display.set_mode((Display.WIDTH, Display.HEIGHT))
caption = pygame.display.set_caption("Pulse Run")

clock = pygame.time.Clock()

display = Display(screen)

player = Player()
enemy = Enemy()

battery = Battery()

while GameState.RUNNING:
    clock.tick(64)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            GameState.RUNNING = False
            continue

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                GameState.PLAYER.shoot_projectiles()
            if event.key == pygame.K_RETURN:
                battery.regenerate()

    if GameState.SCREEN_CODE == ScreenCodes.BA:
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
            GameState.BATTERY.regenerate()

        GameState.ENEMY.update_position()
        GameState.PLAYER.update_projectiles()

    display.update()

GameState.ENEMY.thread.cancel()
