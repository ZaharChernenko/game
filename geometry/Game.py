import sys
from random import randint, randrange

import pygame
from Header import Header
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
        pygame.init()
        pygame.display.set_caption("Geometry Dash")

        self.screen: pygame.Surface = pygame.display.set_mode(screen_size)
        self.width: int = screen_size[0]
        self.height: int = screen_size[1]

        # Инициализация заднего фона
        self.background_image: pygame.Surface | None = None
        self.background_rect: pygame.Rect | None = None
        self.background_color: tuple[int, int, int] | None = None
        self._backgroundInit()
        # конец инициализации фона

        self.header: Header = Header(self.width // 2 - 743 // 2, 210)

        self.play_button: MenuButton = MenuButton(
            self.width // 2 - 50, self.height // 2 - 25, 100, 100, "play_btn.png")

        running: bool = True
        while running:
            # Дублирование фона по горизонтали и вертикали
            for x in range(0, self.screen.get_width(), self.background_image.get_width()):
                for y in range(0, self.screen.get_height(), self.background_image.get_height()):
                    self.screen.blit(self.background_image, (x, y))

            # self.screen.fill((0, 0, 0))  очистка экрана
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            mouse_tuple: tuple[int, int] = pygame.mouse.get_pos()
            self.play_button.checkHover(mouse_tuple)
            self.play_button.draw(self.screen)
            self.header.draw(self.screen)
            pygame.display.flip()  # обновить весь экран

        pygame.quit()
        sys.exit()

    def _backgroundInit(self):
        # Случайный задний фон
        self.background_image = pygame.image.load(fr"../resources/background/game_bg_{randrange(1, 6)}.png").convert()
        self.background_rect = self.background_image.get_rect()
        # Задаем случайный цвет для фона
        self.background_color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.background_image.fill(self.background_color, special_flags=pygame.BLEND_MULT)
