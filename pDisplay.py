import pygame
from pygame.gfxdraw import pixel, line, filled_circle
from GeoObj import *
from Tools import dvType, polylineType, colorType


class Display:
    def __init__(self, screen: pygame.Surface, type_screen: int = 2, back_color: colorType = clBlack):
        """
        :param screen: экран (холст) в pygame.
        :param type_screen: определение положения центра экрана, возможные значения:
        type==1 - нижний левый угол;
        type==2 - центр полотна;
        type==3 - середина левой границы;
        type==4 - привязка к current_center;
        всё остальное - по умолчанию для pygame (верхний левый угол, ось Oy инвертирована).
        :param back_color: цвет фона: кортеж из 3 или 4 значений (RGB / RGBA, где A - прозрачность).
        """
        self.__objects: list[Dot | FatDot | Worm, ...] = []
        self.screen = screen
        self.type_screen = type_screen
        self._current_center = (0, 0)
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
    #!Определения новых объектов на поверхности помещать здесь!

    def set_type_screen(self, type_screen: int = 2):
        self.type_screen = type_screen

    def set_center(self, center: dvType):
        self._current_center = (center[0], center[1])

    def set_center_dyn(self, center: dvType):
        self._current_center = center #динамическая привязка к центру

    def __change_coors(self, coors: dvType):
        height = self.screen.get_height()
        if self.type_screen == 1:
            return [coors[0], height - coors[1]]
        width = self.screen.get_width()
        if self.type_screen == 2:
            return [coors[0] + width // 2, height // 2 - coors[1]]
        if self.type_screen == 3:
            return [coors[0], height // 2 - coors[1]]
        if self.type_screen == 4:
            x, y = self._current_center
            return [coors[0] - x + width // 2, -coors[1] + y + height // 2]
        return [coors[0], coors[1]]

    def show(self):
        self.screen.fill(self.back_color)
        self.__show_objects()

    def __show_objects(self):
        for obj in self.__objects:
            if not obj.hidden:
                #obj.pg_draw(self.screen)
                self.__paint(obj)

    def __paint(self, obj: Dot | FatDot | Worm):
        if type(obj) is Dot:
            self.__paint_point(obj.coors, obj.color)
        if type(obj) is FatDot:
            self.__paint_fat_point(obj.coors, obj.r, obj.color)
        if type(obj) is Worm:
            self.__paint_worm(obj)

    def __paint_point(self, coors: dvType, color: colorType):
        coors = self.__change_coors(coors)
        pixel(self.screen, int(coors[0]), int(coors[1]), color)

    def __paint_fat_point(self, coors: dvType, r: int, color: colorType):
        coors = self.__change_coors(coors)
        filled_circle(self.screen, int(coors[0]), int(coors[1]), r, color)

    def __paint_worm(self, obj: Worm):
        for cell in obj.cells:
            coors = self.__change_coors(cell.coors)
            filled_circle(self.screen, int(coors[0]), int(coors[1]), cell.r, cell.color)
