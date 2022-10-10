import pygame
from GameState import GameState
from Display import Display
from ScreenCodes import ScreenCodes
from Player import Player
from Enemy import Enemy

pygame.init()
GameState.init()

screen = pygame.display.set_mode((Display.WIDTH, Display.HEIGHT))
caption = pygame.display.set_caption("Pulse Run")

display = Display(screen)

player = Player()
enemy = Enemy()

while GameState.RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            GameState.RUNNING = False
            continue

    if GameState.SCREEN_CODE == ScreenCodes.BA:
        keys = pygame.key.get_pressed()

        GameState.PLAYER.update_position(keys)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            GameState.PLAYER.update_position("left")
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            GameState.PLAYER.update_position("right")
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            GameState.PLAYER.update_position("up")
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            GameState.PLAYER.update_position("down")

    enemy.update_position()
    display.update()
