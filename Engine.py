from math import sin, cos, pi, sqrt
import numpy as np
from Tools import dot_coors, normalization, dvType, polylineType


#Генератор перемещений для движения по окружности:
class CirclePath:
    def __init__(self, r: int = 100, step: int = 5, start_angle: float = pi, clockwise: bool = True,
                 center: dvType = np.array((0, 0))):
        """Генератор круговой траектории.
        :param r: радиус траектории;
        :param step: длина вектора перемещения за один шаг при перемещении по траектории;
        :param start_angle: начальный угол, от которого начинается перемещение;
        :param clockwise: True: по часовой стрелке; False: против часовой стрелки;
        :param center: предполагаемый центр окружности (необязательный параметр, нужен только для метода starter)."""
        self.center = dot_coors(center)
        self.r, self.step, self.start_angle, self.clockwise = r, step, start_angle, clockwise

    def starter(self) -> np.ndarray[np.float64, np.float64]:
        return self.center + self.r * np.array([cos(self.start_angle), sin(self.start_angle)])

    def step_on(self):
        angle = self.start_angle
        start_dot = self.r * np.array([cos(angle), sin(angle)])
        angle_step = (-1 if self.clockwise else 1) * self.step / self.r
        while True:
            now_dot = self.r * np.array([cos(angle + angle_step), sin(angle + angle_step)])
            yield now_dot - start_dot
            angle = self._redef_angle(angle, angle_step)
            start_dot = now_dot

    @staticmethod
    def _redef_angle(angle, angle_step):
        angle += angle_step
        if angle < -pi:
            angle += 2 * pi
        elif angle > 2 * pi:
            angle -= 2 * pi
        return angle


#Генератор неравеномерных перемещений для движения по окружности:
class CircleUnevenPath(CirclePath):
    def __init__(self, r: int = 100, max_step: int = 15, start_angle: float = pi, clockwise: bool = True,
                 center: dvType = np.array((0, 0))):
        """Генератор круговой траектории.
        :param r: радиус траектории;
        :param max_step: максимальная длина вектора перемещения за один шаг при движении по траектории;
        :param start_angle: начальный угол, от которого начинается перемещение;
        :param clockwise: True: по часовой стрелке; False: против часовой стрелки;
        :param center: предполагаемый центр окружности (необязательный параметр, нужен только для метода starter)."""
        super().__init__(r, max_step, start_angle, clockwise, center)

    def step_on(self):
        angle, uneven_step_angle, uneven_current = self.start_angle, pi/15, 0
        start_dot = self.r * np.array([cos(angle), sin(angle)])
        while True:
            angle_step = abs(cos(uneven_current)) * (-1 if self.clockwise else 1) * self.step / self.r
            now_dot = self.r * np.array([cos(angle + angle_step), sin(angle + angle_step)])
            yield now_dot - start_dot
            angle = self._redef_angle(angle, angle_step)
            uneven_current = self._redef_angle(uneven_current, uneven_step_angle)
            start_dot = now_dot


#Генератор перемещений для движения по траектории "квадрат":
class SquarePath:
    def __init__(self, length: int = 100, count_step: int = 20, clockwise: bool = True,
                 center: dvType = np.array((0, 0))):
        """Генератор траектории "по квадрату" (начало перемещения - нижний левый угол).
        :param length: длина стороны квадрата;
        :param count_step: количество шагов, требуемое для обхода траектории (желательно, чтобы было кратно 4);
        :param clockwise: True: по часовой стрелке; False: против часовой стрелки;
        :param center: предполагаемый центр квадрата (необязательный параметр, нужен только для метода starter)."""
        self.center = dot_coors(center)
        self.count_step = count_step if count_step > 4 else 4
        self.length, self.clockwise = length, clockwise

    def starter(self) -> np.ndarray[np.float64, np.float64]:
        return self.center - self.length / 2 * np.array([1, 1])

    def step_on(self):
        counts_on_side = [self.count_step // 4 for _ in range(3)]
        counts_on_side.append(self.count_step - 3 * (self.count_step // 4))
        length_on_side = [self.length / count for count in counts_on_side]
        if self.clockwise:
            steps = [np.array((0, 1)), np.array((1, 0)), np.array((0, -1)), np.array((-1, 0))]
        else:
            steps = [np.array((1, 0)), np.array((0, 1)), np.array((-1, 0)), np.array((0, -1))]
        index = 0
        while True:
            for _ in range(counts_on_side[index]):
                yield steps[index] * length_on_side[index]
            index += 1
            index %= 4


#Генератор перемещений по заданной ломанной линии:
class PolylinearPath:
    def __init__(self, length: int = 100, count_step: int = 10, clockwise: bool = True,
                 steps: polylineType = (((1, 0), (-1, 0)), ),
                 rect_length: int = 100, center: dvType = np.array((0, 0))):
        """Генератор траектории перемещения по заданной ломанной линии.
        :param length: длина звена ломаной;
        :param count_step: количество шагов, требуемое для прохода звена ломаной;
        :param clockwise: True: условно "прямой" обход; False: "обратный" обход;
        :param steps: перечень последовательных направлений перемещения;
        :param rect_length: предполагаемая длина квадрата, внутри которого перемещается объект
        (необязательный параметр, нужен только для метода starter)
        :param center: предполагаемый центр такого квадрата (необязательный, нужен для starter)."""
        self.length, self.count_step, self.clockwise, self.rect_length = \
            length / count_step, count_step, clockwise, rect_length
        self.dirs, self.inv_dirs = self.directions(steps), self.invert_direction(steps)
        self.center = dot_coors(center)

    def starter(self) -> np.ndarray[np.float64, np.float64]:
        """Предполагаемое начало траетории - нижний-левый угол \"описанного\" квадрата"""
        return self.center - self.rect_length / 2 * np.array([1, 1])

    def step_on(self):
        steps = self.dirs if self.clockwise else self.inv_dirs
        count = steps.shape[0]
        index = 0
        while True:
            for _ in range(self.count_step):
                yield steps[index] * self.length
            index += 1
            index %= count

    @staticmethod
    def directions(steps: polylineType):
        return np.array([normalization(step) for step in steps], dtype=np.float64)

    @staticmethod
    def invert_direction(steps: polylineType):
        return np.flipud(np.array([-normalization(step) for step in steps], dtype=np.float64))


#Генератор перемещений по заданному отрезку:
class LinearPath(PolylinearPath):
    def __init__(self, length: int = 100, count_step: int = 10, vec: dvType = (1, 1),
                 center: dvType = np.array((0, 0))):
        """Генератор траектории перемещения по заданному отрезку.
        :param length: длина отрезка;
        :param count_step: количество шагов, требуемое для прохода по отрезку в одном направлении;
        :param vec: начальное направление перемещения объекта;
        :param center: предполагаемый центр такого квадрата (необязательный, нужен для starter)."""
        super().__init__(length, count_step, True, (vec, (-vec[0], -vec[1])), center=center)

    def starter(self) -> np.ndarray[np.float64, np.float64]:
        return self.center - self.length * self.count_step / 2 * self.dirs[0]


#Генератор перемещений для движения по дуге:
class ArcPath:
    def __init__(self, r: int = 100, start_angle: int | float = 0, end_angle: int | float = pi, step: int = 5,
                 center: dvType = np.array((0, 0))):
        """Генератор дуговой траектории.
        :param r: радиус траектории;
        :param start_angle: начальный угол, от которого начинается перемещение;
        :param end_angle: конечный угол, на котором движение заканчивается;
        :param step: количество шагов при перемещении по дуге;
        :param center: предполагаемый центр окружности (необязательный параметр, нужен только для метода starter)."""
        self.center = dot_coors(center)
        self.r, self.step, self.start_angle, self.end_angle = r, step, start_angle, end_angle

    def starter(self) -> np.ndarray[np.float64, np.float64]:
        return self.center + self.r * np.array([cos(self.start_angle), sin(self.start_angle)])

    def step_on(self):
        while True:
            angle = self.start_angle
            start_dot = self.r * np.array([cos(angle), sin(angle)])
            angle_step = (self.end_angle - self.start_angle) / self.step
            for _ in range(self.step):
                now_dot = self.r * np.array([cos(angle + angle_step), sin(angle + angle_step)])
                yield now_dot - start_dot
                start_dot = now_dot
                angle += angle_step
            angle = self.end_angle
            start_dot = self.r * np.array([cos(angle), sin(angle)])
            angle_step = (self.start_angle - self.end_angle) / self.step
            for _ in range(self.step):
                now_dot = self.r * np.array([cos(angle + angle_step), sin(angle + angle_step)])
                yield now_dot - start_dot
                start_dot = now_dot
                angle += angle_step


if __name__ == '__main__':
    print(PolylinearPath.invert_direction([[1, 0]]))
