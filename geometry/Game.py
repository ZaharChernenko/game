import sqlite3
import sys
from random import randint, randrange

import pygame
from Header import Header
from Level import Level
from LevelButton import LevelButton
from MenuButton import MenuButton


def singleton(_class):
    instances = {}

    def getinstance(*args, **kwargs):
        if _class not in instances:
            instances[_class] = _class(*args, **kwargs)
        return instances[_class]
    return getinstance


@singleton
class Game:
    def __init__(self, screen_size: tuple[int, int] = (1200, 800)) -> None:
        self.client: sqlite3.Connection | None = None
        self.databaseInit()

        pygame.init()
        pygame.display.set_caption("Geometry Dash")

        self.screen: pygame.Surface = pygame.display.set_mode(screen_size)
        self.width: int = screen_size[0]
        self.height: int = screen_size[1]

        # Инициализация заднего фона
        self.background_image: pygame.Surface | None = None
        self.background_rect: pygame.Rect | None = None
        self.background_color: tuple[int, int, int] | None = None
        self.backgroundInit()
        # конец инициализации фона

        self.header: Header = Header(self.width // 2 - 743 // 2, 210)

        self.play_button: MenuButton = MenuButton(
            self.width // 2 - 50, self.height // 2 - 25, 100, 100, "play_btn.png")

        self.back_button: MenuButton = MenuButton(50, 50, 52, 68, "back_btn.png")

        self.enterScreen()

        pygame.quit()
        sys.exit()

    def backgroundInit(self):
        # Случайный задний фон
        self.background_image = pygame.image.load(fr"../resources/background/game_bg_{randrange(1, 6)}.png").convert()
        self.background_rect = self.background_image.get_rect()
        # Задаем случайный цвет для фона
        self.background_color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.background_image.fill(self.background_color, special_flags=pygame.BLEND_MULT)

    def drawBackground(self):
        # Дублирование фона по горизонтали и вертикали
        for x in range(0, self.screen.get_width(), self.background_image.get_width()):
            for y in range(0, self.screen.get_height(), self.background_image.get_height()):
                self.screen.blit(self.background_image, (x, y))

    def enterScreen(self):
        running: bool = True
        while running:
            self.drawBackground()
            # self.screen.fill((0, 0, 0))  очистка экрана
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                running = not self.play_button.isClicked(event)

            mouse_tuple: tuple[int, int] = pygame.mouse.get_pos()
            if self.play_button.checkHover(mouse_tuple):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            self.play_button.draw(self.screen)
            self.header.draw(self.screen)
            pygame.display.flip()  # обновить весь экран

        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.mainScreen()

    def databaseInit(self):
        self.client = sqlite3.connect("user/levels.db")

        cursor = self.client.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS levels (
            name TEXT PRIMARY KEY,
            difficulty INTEGER NOT NULL,
            coins INTEGER CHECK (coins BETWEEN 0 AND 3),
            completion_rate REAL CHECK (completion_rate BETWEEN 0 AND 100))""")

        self.client.commit()

    def getLevelData(self):
        cursor = self.client.cursor()
        cursor.execute("SELECT * FROM levels")
        return cursor.fetchall()

    def mainScreen(self):
        running: bool = True
        level_start: bool = False
        level_buttons: tuple[LevelButton, ...] = tuple(LevelButton(*level) for level in self.getLevelData())

        while running:
            self.drawBackground()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if self.back_button.isClicked(event):
                    running = False
                    break

                for level_button in level_buttons:
                    if level_button.isClicked(event):
                        running = False
                        level_start = True
                        level_name: str = level_button.getLevelName()
                        break

            mouse_tuple: tuple[int, int] = pygame.mouse.get_pos()
            for level_button in level_buttons:
                level_button.checkHover(mouse_tuple)
                level_button.draw(self.screen)

            if any(level_button.checkHover(mouse_tuple) for level_button in level_buttons) or self.back_button.checkHover(mouse_tuple):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            self.back_button.draw(self.screen)

            pygame.display.flip()

        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if not level_start:
            self.enterScreen()
        else:
            self.levelScreen(level_name)

    def levelScreen(self, level_name: str):
        level = Level(self.screen, level_name, self.drawBackground)
        is_exit: bool = level.run()
        while not is_exit:
            is_exit = level.run()
        self.mainScreen()
