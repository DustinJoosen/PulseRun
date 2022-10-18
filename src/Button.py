import pygame
from GameState import GameState

class Button:
    def __init__(self, width, height, onclick=None, position=(0, 0), color=(255, 255, 255), text="", image=None):
        self.width = width
        self.height = height

        self.onclick = onclick
        self.position = position
        self.color = color
        self.image = image
        self.text = text

    def draw(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.position)
        else:
            pygame.draw.rect(screen, self.color, [self.position[0], self.position[1], self.width, self.height])

    def is_hovering(self):
        mouse_pos = pygame.mouse.get_pos()

        x_col = mouse_pos[0] in range(self.position[0], self.position[0] + self.width)
        y_col = mouse_pos[1] in range(self.position[1], self.position[1] + self.height)

        return x_col and y_col

    def check_onclick(self):
        hovering = self.is_hovering()
        if not hovering:
            return False

        clicking = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicking = True
                print("Clicking")

        if clicking or self.onclick is not None:
            self.onclick()

        return clicking
