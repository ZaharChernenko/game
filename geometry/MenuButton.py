import pygame


class MenuButton:
    def __init__(self, x: int, y: int, width: int, height: int, icon_name: str) -> None:
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height

        self.icon: pygame.Surface = pygame.image.load(fr"../resources/icons/{icon_name}")
        # сначала иконка при наведении
        self.icon_hovered: pygame.Surface = pygame.transform.scale(self.icon, (self.width + 10, self.height + 10))
        self.icon = pygame.transform.scale(self.icon, (self.width, self.height))
        self.rect: pygame.Rect = self.icon.get_rect(topleft=(x, y))

        self.is_hovered: bool = False

    def draw(self, screen: pygame.Surface) -> None:
        current_icon: pygame.Surface = self.icon if not self.is_hovered else self.icon_hovered
        x: int = self.x - 5 if self.is_hovered else self.x
        y: int = self.y - 5 if self.is_hovered else self.y
        screen.blit(current_icon, (x, y))  # отрисовываем кнопку
        self.rect = self.icon.get_rect(topleft=(x, y))

    def checkHover(self, mouse_pos) -> bool:
        """проверяет, находится ли точка, координаты которой были
        переданы в качестве аргумента, в пределах прямоугольника"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered

    def isClicked(self, event) -> bool:
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered
