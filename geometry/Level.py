import csv
import enum
import sys

import pygame
from MenuButton import MenuButton

player_image: pygame.Surface = pygame.image.load("../resources/tileset/avatar.png")
player_image = pygame.transform.smoothscale(player_image, (32, 32))

block_image: pygame.Surface = pygame.image.load("../resources/tileset/block_32px.png")

spike_image: pygame.Surface = pygame.image.load("../resources/tileset/spike_32px.png")
spike_mask = pygame.mask.from_surface(spike_image)

orb_image: pygame.Surface = pygame.image.load("../resources/tileset/orb_32px.png")


class Level:
    def __init__(self, screen: pygame.Surface, level_name: str, draw_background_func) -> None:
        self.screen: pygame.Surface = screen
        self.draw_background_func = draw_background_func

        self.level_data_list: list[list[str]] = list(csv.reader(
            open("test.csv", encoding="utf-8"), delimiter=",", quotechar="\""))
        self.level_data_group: pygame.sprite.Group | None = None
        self.player: Player | None = None

        self.back_button: MenuButton = MenuButton(50, 50, 52, 68, "back_btn.png")

    def initElements(self) -> None:
        self.level_data_group = pygame.sprite.Group()
        x: int = 32
        y: int = 32

        for row in self.level_data_list:
            for element in row:
                match element:
                    case "0":
                        self.player = Player(player_image, (x, y), self.level_data_group)
                    case "2":
                        Block(block_image, (x, y), self.level_data_group)
                    case "3":
                        Spike(spike_image, (x, y), self.level_data_group)
                    case "4":
                        Orb(orb_image, (x, y), self.level_data_group)
                x += 32
            x = 0
            y += 32

    def draw(self) -> None:
        self.draw_background_func()
        self.level_data_group.draw(self.screen)

    def moveMap(self) -> None:
        for sprite in self.level_data_group:
            if sprite.object_type != GDObjectType.PLAYER:
                sprite.rect.x -= self.player.x_speed

    def run(self) -> bool:
        self.initElements()
        clock: pygame.time.Clock = pygame.time.Clock()
        running: bool = True

        while running:
            self.moveMap()
            self.draw()
            self.back_button.draw(self.screen)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
                self.player.is_jump = True
            self.player.update(self.level_data_group)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.back_button.isClicked(event):
                    return True
            mouse_tuple: tuple[int, int] = pygame.mouse.get_pos()
            if self.back_button.checkHover(mouse_tuple):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            if self.player.is_died:
                return False

            clock.tick(60)
            pygame.display.flip()

        return False


class GDObjectType(enum.IntEnum):
    PLAYER = 0
    BLOCK = 1
    SPIKE = 2
    ORB = 3


class GDObject(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, pos, object_type: GDObjectType, *groups) -> None:
        super().__init__(*groups)
        self.image: pygame.Surface = image
        self.rect = self.image.get_rect(topleft=pos)
        self.object_type = object_type


class Block(GDObject):
    def __init__(self, image: pygame.Surface, pos, *groups) -> None:
        super().__init__(image, pos, GDObjectType.BLOCK, *groups)


class Spike(GDObject):
    def __init__(self, image: pygame.Surface, pos, *groups) -> None:
        super().__init__(image, pos, GDObjectType.SPIKE, *groups)


class Orb(GDObject):
    def __init__(self, image: pygame.Surface, pos, *groups) -> None:
        super().__init__(image, pos, GDObjectType.ORB, *groups)


class Player(GDObject):
    def __init__(self, image: pygame.Surface, pos, *groups) -> None:
        super().__init__(image, pos, GDObjectType.PLAYER, *groups)
        self.on_ground: bool = True
        self.is_jump: bool = False
        self.x_speed: float = 5.5
        self.y_speed: float = 0
        self.jump_strength: float = 11

        self.is_died: bool = False

    def jump(self):
        self.y_speed = -self.jump_strength

    def update(self, sprites):
        if self.is_jump and self.on_ground:
            self.jump()

        if not self.on_ground:
            self.y_speed += 0.86

        self.on_ground = False
        steps = int(abs(self.y_speed) / 10) + 1
        y_increase: float = self.y_speed / steps
        for _ in range(steps):
            self.rect.top += y_increase  # Перемещаем на 1 шаг
            self.collide(sprites)
            if self.on_ground:
                break

    def collide(self, objects: pygame.sprite.Group):
        for obj in objects:
            if pygame.sprite.collide_rect(self, obj):
                match obj.object_type:
                    case GDObjectType.BLOCK:
                        # Проверяем пересечение по оси Y
                        if self.y_speed > 0:
                            # Добавляем небольшую погрешность для "мягкого" приземления
                            if self.rect.bottom - obj.rect.top <= 10:
                                self.rect.bottom = obj.rect.top
                                self.y_speed = 0
                                self.on_ground = True
                                self.is_jump = False
                            else:
                                self.is_died = True

                        elif self.y_speed < 0:
                            # Аналогично, добавляем погрешность при ударе головой
                            if obj.rect.bottom - self.rect.top <= 8:
                                self.rect.top = obj.rect.bottom
                            else:
                                self.is_died = True

                        else:
                            # Столкновение по горизонтали
                            self.is_died = True

                    case GDObjectType.SPIKE:
                        offset_x = self.rect.left - obj.rect.left
                        offset_y = self.rect.top - obj.rect.top
                        if spike_mask.overlap(pygame.mask.Mask(obj.rect.size, True), (offset_x, offset_y)):
                            self.is_died = True

                    case GDObjectType.ORB:
                        keys = pygame.key.get_pressed()
                        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]):
                            self.jump_strength = 15  # gives a little boost when hit orb
                            self.jump()
                            self.jump_strength = 11  # return jump_amount to normal
