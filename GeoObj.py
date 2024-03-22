import numpy as np
from typing import Final, Sequence
from random import randint
from Tools import dot_coors, dvType, colorType, color_randomize, polylineType
import pygame
from pygame.gfxdraw import pixel, line, filled_circle
from math import cos, sin


clBlack: Final = (0, 0, 0)
clRed: Final = (255, 0, 0)
clGreen: Final = (0, 255, 0)
clBlue: Final = (0, 0, 255)
clWhite: Final = (255, 255, 255)


class _AbstractGeoObj:
    def __init__(self, color: colorType = clWhite):
        self.color = color
        self.hidden = False

    def pg_draw(self, screen: pygame.Surface):
        pass


class Dot(_AbstractGeoObj):
    def __init__(self, coors: dvType = np.array([0, 0]), color: colorType = clWhite):
        super().__init__(color)
        self._coors = self._new_coors(coors)

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


class Worm(_AbstractGeoObj):
    def __init__(self, head_coors: dvType = np.array([0, 0]), min_r: int = 1, max_r: int = 5,
                 length: int = 5, step: int | float = 5, color: colorType = clWhite):
        super().__init__(color)
        self.length = length
        self.cells: list[FatDot] = [FatDot(head_coors, randint(min_r, max_r), self.color)]
        self._create_worm(min_r, max_r, step)

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


class DotCloud(_AbstractGeoObj):
    def __init__(self, count: int, rect: list[list[int]], color: colorType = clWhite):
        super().__init__(color)
        self.count = count
        self.rect = rect
        self.__dots: list[Dot] = []
        self.__gen()

    def __gen(self):
        for _ in range(self.count):
            self.__dots.append(Dot(np.array((randint(self.rect[0][0], self.rect[1][0]),
                                             randint(self.rect[0][1], self.rect[1][1]))),
                                   color_randomize(self.color, 30)))

    def pg_draw(self, screen: pygame.Surface):
        for dot in self.__dots:
            dot.pg_draw(screen)


class Polyline(_AbstractGeoObj):
    def __init__(self, coors: polylineType, color: colorType):
        super().__init__(color)
        self._coors = Polyline.__generalized_mod(coors)

    def move_to(self, D):
        self.abstract_transformation(0, D, 1)

    def rotate_by_dot(self, alpha, d):
        self.abstract_transformation(0, [-d[0], -d[1], 1], 1)
        self.abstract_transformation(alpha, [0, 0], 1)
        self.abstract_transformation(0, d, 1)

    def rotate(self, alpha):
        c = self._center
        self.rotate_by_dot(alpha, c)

    def scale_by_dot(self, d, k):
        self.abstract_transformation(0, [-d[0], -d[1], 1], 1)
        self.abstract_transformation(0, [0, 0], k)
        self.abstract_transformation(0, d, 1)

    def scale(self, k):
        c = self._center
        self.scale_by_dot(c, k)

    def pg_draw(self, screen: pygame.Surface):
        height, width = screen.get_height(), screen.get_width()
        for (x1, y1, _), (x2, y2, _) in zip(self._coors[:-1], self._coors[1:]):
            line(screen, int(x1 + width // 2), int(height // 2 - y1),
                 int(x2 + width // 2), int(height // 2 - y2), self.color)

    @property
    def _center(self):
        return np.mean(self._coors, axis=0)[:2]

    def abstract_transformation(self, alpha: int | float = 0, d: dvType = (0, 0), k: int | float = 1):
        f = np.array([[k * cos(alpha), k*sin(alpha), 0],
                      [-k*sin(alpha), k * cos(alpha), 0],
                      [d[0], d[1], 1]]
                     )
        self._coors = self._coors.dot(f)

    @staticmethod
    def __generalized_mod(coors: polylineType):
        coors = np.array(coors, dtype=np.float64)
        ones_array = np.ones((coors.shape[0], 1), dtype=int)
        return np.hstack((coors, ones_array))


class Polygon(Polyline):
    def __init__(self, coors: polylineType, color: colorType):
        coors.append(coors[0])
        super().__init__(coors, color)

    @property
    def _center(self):
        return np.mean(self._coors[:-1], axis=0)[:2]


class Square(Polygon):
    def __init__(self, center: dvType, height: int | float, color: colorType):
        coors = Square.create_square_coors(center, height)
        super().__init__(coors, color)

    @staticmethod
    def create_square_coors(c, h):
        return [[c[0] - h//2, c[1] - h//2], [c[0] - h//2, c[1] + h//2],
                [c[0] + h//2, c[1] + h//2], [c[0] + h//2, c[1] - h//2]]
