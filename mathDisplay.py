import matplotlib.pyplot as plt
from GeoObj import *


cls_mpl = {clBlack: 'black',
           clRed: 'red',
           clGreen: 'green',
           clBlue: 'blue',
           clWhite: 'white'}


class GraphDisplay:
    def __init__(self, screen: plt.Figure, size_rect: tuple[int, int] | list[int, int],
                 back_color: tuple[int, int, int] | tuple[int, int, int, int] = clWhite):
        """
        :param screen: экран (холст) в matplotlib.
        :param back_color: цвет фона: кортеж из 3 или 4 значений (RGB / RGBA, где A - прозрачность).
        """
        self.__objects: list[Dot | FatDot, ...] = []
        self.screen = screen
        self.axs = self.screen.add_subplot()
        self.back_color = back_color
        self.weight, self.height = size_rect[0], size_rect[1]

    def create_point(self, dot: np.ndarray | list | tuple = np.array([0, 0]),
                     color: tuple[int, int, int] | tuple[int, int, int, int] = clBlack):
        pg_dot = Dot(dot, color)
        self.__objects.append(pg_dot)
        return pg_dot

    def create_fat_point(self, dot: np.ndarray | list | tuple = np.array([0, 0]), r: int = 1,
                     color: tuple[int, int, int] | tuple[int, int, int, int] = clBlack):
        pg_fat_dot = FatDot(dot, r, color)
        self.__objects.append(pg_fat_dot)
        return pg_fat_dot
    #!Определения новых объектов на поверхности помещать здесь!

    def show(self):
        plt.clf()
        self.__main_plot()
        self.__show_objects()
        plt.gcf().canvas.flush_events()
        plt.draw()

    def __main_plot(self):
        plt.scatter(-self.weight/2, -self.height/2, color='white')
        plt.scatter(self.weight/2, self.height/2, color='white')

    def __show_objects(self):
        for obj in self.__objects:
            if not obj.hidden:
                self.__paint(obj)

    def __paint(self, obj: Dot | FatDot):
        if type(obj) is Dot:
            self.__paint_point(obj.coors, obj.color)
        if type(obj) is FatDot:
            self.__paint_fat_point(obj.coors, obj.r, obj.color)

    def __paint_point(self, coors: np.ndarray | list[int | float, int | float] | tuple[int | float, int | float],
                      color: tuple[int, int, int] | tuple[int, int, int, int]):
        plt.scatter(coors[0], coors[1], color=cls_mpl[color])

    def __paint_fat_point(self, coors: np.ndarray | list[int | float, int | float] | tuple[int | float, int | float],
                          r: int, color: tuple[int, int, int] | tuple[int, int, int, int]):
        plt.gca().add_artist(plt.Circle((coors[0], coors[1]), radius=r, color=cls_mpl[color]))
