import numpy as np
from typing import Final
from random import randint
from Tools import dot_coors, dvType, colorType
import pygame
from pygame.gfxdraw import pixel, line, filled_circle


clBlack: Final = (0, 0, 0)
clRed: Final = (255, 0, 0)
clGreen: Final = (0, 255, 0)
clBlue: Final = (0, 0, 255)
clWhite: Final = (255, 255, 255)


class Dot:
    def __init__(self, coors: dvType = np.array([0, 0]), color: colorType = clWhite):
        self._coors = self._new_coors(coors)
        self.color = color
        self.hidden = False

    def move(self, d: dvType = np.array([0, 0])):
        d = self._new_coors(d)
        self._coors += d

    def move_to(self, d: dvType = np.array([0, 0])):
        self._coors = self._new_coors(d)

    def pg_draw(self, screen: pygame.Surface):
        height, width = screen.get_height(), screen.get_width()
        pixel(screen, int(self._coors[0] + width // 2), int(height // 2 - self._coors[1]), self.color)

    @property
    def coors(self):
        return self._coors

    @coors.setter
    def coors(self, coors: dvType = np.array([0, 0])):
        self._coors = self._new_coors(coors)

    @staticmethod
    def _new_coors(coors: dvType = np.array([0, 0])) -> np.ndarray:
        return dot_coors(coors)


class FatDot(Dot):
    def __init__(self, coors: dvType = np.array([0, 0]), r: int | float = 1, color: colorType = clWhite):
        super().__init__(coors, color)
        self.r = r

    def pg_draw(self, screen: pygame.Surface):
        height, width = screen.get_height(), screen.get_width()
        filled_circle(screen, int(self._coors[0] + width // 2), int(height // 2 - self._coors[1]), self.r, self.color)


class Worm:
    def __init__(self, head_coors: dvType = np.array([0, 0]), min_r: int = 1, max_r: int = 5,
                 length: int = 5, step: int | float = 5, color: colorType = clWhite):
        self.color = color
        self.length = length
        self.cells: list[FatDot, ...] = [FatDot(head_coors, randint(min_r, max_r), self.color)]
        self._create_worm(min_r, max_r, step)
        self.hidden = False

    def _create_worm(self, min_r, max_r, step):
        head = self.cells[0].coors
        st = np.array([0, -step])
        for i in range(1, self.length):
            self.cells.append(FatDot(head - i * st, randint(min_r, max_r), self.color))

    def move(self, d: dvType = np.array([0, 0])):
        for i in range(self.length - 1, 0, -1):
            self.cells[i].move_to(self.cells[i-1].coors)
        self.cells[0].move(d)

    def pg_draw(self, screen: pygame.Surface):
        for cell in self.cells:
            cell.pg_draw(screen)
