import csv
import enum
import sys

import pygame


class Level:
    def __init__(self, screen: pygame.Surface, level_name: str, draw_background_func) -> None:
        self.screen: pygame.Surface = screen
        print(type(draw_background_func))
        self.draw_background_func = draw_background_func
        self.block_image: pygame.Surface = pygame.image.load("../resources/tileset/block_32px.png")

        self.level_data_list: list[list[str]] = list(csv.reader(
            open("test..csv", encoding="utf-8"), delimiter=",", quotechar="\""))
        self.level_data_group: pygame.sprite.Group = pygame.sprite.Group()
        self.initElements()

    def initElements(self) -> None:
        x: int = 32
        y: int = 32

        for row in self.level_data_list:
            for element in row:
                if element == "2":
                    Block(self.block_image, (x, y), self.level_data_group)
                x += 32
            x = 0
            y += 32

    def draw(self) -> None:
        self.draw_background_func()
        self.level_data_group.draw(self.screen)

    def run(self) -> None:
        running: bool = True

        while running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()


class GDObjectType(enum.IntEnum):
    BLOCK = 1
    SPIKE = 2


class GDObject(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, pos, object_type: GDObjectType, *groups) -> None:
        super().__init__(*groups)
        self.image: pygame.Surface = image
        self.rect = self.image.get_rect(topleft=pos)
        self.object_type = object_type


class Block(GDObject):
    def __init__(self, image: pygame.Surface, pos, *groups) -> None:
        super().__init__(image, pos, GDObjectType.BLOCK, *groups)
