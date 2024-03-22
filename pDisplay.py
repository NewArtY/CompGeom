import pygame
from pygame.gfxdraw import pixel, line, filled_circle
from GeoObj import *
from Tools import dvType, polylineType, colorType


class Display:
    def __init__(self, screen: pygame.Surface, back_color: colorType = clBlack):
        """
        :param screen: экран (холст) в pygame.
        :param back_color: цвет фона: кортеж из 3 или 4 значений (RGB / RGBA, где A - прозрачность).
        """
        self.__objects: list[Dot | FatDot | Worm | DotCloud | Polyline | Polygon] = []
        self.screen = screen
        self.back_color = back_color

    def create_point(self, dot: dvType = np.array([0, 0]), color: colorType = clWhite):
        pg_dot = Dot(dot, color)
        self.__objects.append(pg_dot)
        return pg_dot

    def create_fat_point(self, dot: dvType = np.array([0, 0]), r: int = 1, color: colorType = clWhite):
        pg_fat_dot = FatDot(dot, r, color)
        self.__objects.append(pg_fat_dot)
        return pg_fat_dot

    def create_worm(self, head_coors: polylineType = np.array([[0, 0]]), min_r: int = 1, max_r: int = 5,
                    length: int = 5, step: int | float = 5, color: colorType = clWhite):
        pg_worm = Worm(head_coors, min_r, max_r, length, step, color)
        self.__objects.append(pg_worm)
        return pg_worm

    def create_cloud_dot(self, count: int, rect: list[list[int]], color: colorType = clWhite):
        pg_cloud_dot = DotCloud(count, rect, color)
        self.__objects.append(pg_cloud_dot)
        return pg_cloud_dot

    def create_polyline(self, coors: polylineType, color: colorType):
        pg_polyline = Polyline(coors, color)
        self.__objects.append(pg_polyline)
        return pg_polyline

    def create_polygon(self, coors: polylineType, color: colorType):
        pg_polygon = Polygon(coors, color)
        self.__objects.append(pg_polygon)
        return pg_polygon
    #!Определения новых объектов на поверхности помещать здесь!

    def show(self):
        self.screen.fill(self.back_color)
        self.__show_objects()

    def __show_objects(self):
        for obj in self.__objects:
            if not obj.hidden:
                obj.pg_draw(self.screen)
