import pygame

digit2difficulty_icon: dict[int, str] = {1: "easiest.png"}


class LevelButton:
    def __init__(self, level_name: str, difficulty: int, n_coins: int, percentage: int):
        self.level_name = level_name
        self.percentage = int(percentage)
        self.is_hovered: bool = False
        font: pygame.font.Font = pygame.font.SysFont("pusab", 36)
        self.level_text: pygame.Surface = font.render(level_name, True, (255, 255, 255))
        self.normal_mode_text: pygame.Surface = font.render("Normal Mode", True, (255, 255, 255))

        font = pygame.font.SysFont("pusab", 24)
        self.normal_mode_percentage_text: pygame.Surface = font.render(f"{self.percentage}%", True, (255, 255, 255))

        self.main_width: int = 700
        self.main_height: int = 500
        self.x: int = 250
        self.y: int = 150
        self.main_surface: pygame.Surface = pygame.Surface((self.main_width, self.main_height), pygame.SRCALPHA)

        self.radius: int = 20
        self.color: tuple[int, int, int, int] = (50, 50, 50, 192)
        self.upper_rect_height: int = 200
        self.upper_rect: pygame.Rect = pygame.Rect(0, 0, self.main_width, self.upper_rect_height)
        self.lower_rect_height: int = 100
        self.lower_rect: pygame.Rect = pygame.Rect(0, 225, self.main_width, self.lower_rect_height)

        self.progress_rect_width: int = 6 * percentage
        self.progress_rect_height: int = 20
        self.progress_rect: pygame.Rect = pygame.Rect(20, 285, self.progress_rect_width, self.progress_rect_height)

        # это для правильного захвата мышки
        self.upper_button_rect: pygame.Rect = pygame.Rect(self.x, self.y, self.main_width, self.upper_rect_height)
        # difficulty init
        self.difficulty_width: int = 70
        self.difficulty_height: int = 70
        self.difficulty_icon: pygame.Surface = pygame.image.load(
            fr"../resources/icons/{digit2difficulty_icon[difficulty]}")
        self.difficulty_icon = pygame.transform.scale(
            self.difficulty_icon, (self.difficulty_width, self.difficulty_height))

        # coins init
        self.coins: tuple = tuple(pygame.transform.scale(pygame.image.load(
            r"../resources/icons/coin.png"), (50, 50)) for _ in range(3))
        self.coin_color = (50, 50, 50)

        for i in range(3 - n_coins):
            self.coins[i].fill(self.coin_color, special_flags=pygame.BLEND_MULT)

    def draw(self, screen):
        # upper_rect
        pygame.draw.rect(self.main_surface, self.color, self.upper_rect, border_radius=self.radius)
        pygame.draw.rect(self.main_surface, self.color, self.lower_rect, border_radius=self.radius)
        pygame.draw.rect(self.main_surface, (0, 255, 0), self.progress_rect, border_radius=self.radius)

        self.main_surface.blit(self.difficulty_icon, (50, (self.upper_rect_height - self.difficulty_height) // 2))
        start = 525
        for i in range(3):
            self.main_surface.blit(self.coins[i], (start, 125))
            start += 50

        # upper_rect text
        self.main_surface.blit(self.level_text, ((self.main_width - self.level_text.get_width()) // 2,
                               (self.upper_rect_height - self.level_text.get_height()) // 2))

        self.main_surface.blit(self.normal_mode_text, ((self.main_width - self.normal_mode_text.get_width()
                                                        ) // 2, (self.main_height - self.level_text.get_height()) // 2))

        self.main_surface.blit(self.normal_mode_percentage_text, (self.main_width - 10 - self.normal_mode_percentage_text.get_width(),
                                                                  285))
        screen.blit(self.main_surface, (self.x, self.y))

    def checkHover(self, mouse_pos) -> bool:
        self.is_hovered = self.upper_button_rect.collidepoint(mouse_pos)
        return self.is_hovered

    def isClicked(self, event) -> bool:
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered

    def getLevelName(self) -> str:
        return self.level_name

    def getPercentage(self) -> int:
        return self.percentage
