from random import randint

import pygame


class Header:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.icon: pygame.Surface = pygame.image.load(r"../resources/icons/header.png")
        self.icon = pygame.transform.scale(self.icon, (743, 70))
        self.rect: pygame.Rect = self.icon.get_rect(topleft=(x, y))

        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.icon.fill(self.color, special_flags=pygame.BLEND_MULT)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.icon, (self.x, self.y))
