import numpy as np
from math import sqrt
from typing import Union, Tuple, List, Final
from random import randint


colorType: Final = tuple[int, int, int] | tuple[int, int, int, int]
dvType: Final = np.ndarray[int | np.float64, int | np.float64] | list[int | float, int | float] | \
                 tuple[int | float, int | float]
rectType: Final = list[[int, int], [int, int]] | np.ndarray[[int, int], [int, int]]
NumberPair = Tuple[Union[int, float], Union[int, float]]
polylineType: Final = Union[List[NumberPair], Tuple[NumberPair, ...], np.ndarray]
#polylineType: Final = list[[int | float, int | float], ...] | tuple[[int | float, int | float], ...] | \
                      #np.ndarray[[int | np.float64, int | np.float64], ...]


def dot_coors(coors: dvType = np.array([0, 0])) -> np.ndarray[np.float64, np.float64]:
    return coors if type(coors) is np.ndarray[np.float64, np.float64] else np.array(coors, dtype=np.float64)


def normalization(vec: dvType = np.array((1, 1)), length: int | float = 1):
    return length * dot_coors(vec) / sqrt(vec[0]**2 + vec[1]**2)


def dot_not_in_rect(dot: dvType, vec: dvType, rect: rectType) -> bool | int:
    for i in range(2):
        if (dot[i] + vec[i] < rect[0][i]) or (dot[i] + vec[i] > rect[1][i]):
            return i + 1
    return False


def reflect_vec(dot: dvType, vec: dvType, rect: rectType) -> np.ndarray[np.float64, np.float64]:
    dir_ = dot_not_in_rect(dot, vec, rect)
    if dir_ == 1:
        if not dot_not_in_rect(dot, [-vec[0], vec[1]], rect):
            return np.array([-vec[0], vec[1]], dtype=np.float64)
    elif dir_ == 2:
        if not dot_not_in_rect(dot, [vec[0], -vec[1]], rect):
            return np.array([vec[0], -vec[1]], dtype=np.float64)
    return -dot_coors(vec)


def rect_to_polyline(rect: rectType) -> np.ndarray[[np.float64, np.float64], ...]:
    redef = [rect[0], [rect[0][0], rect[1][1]], rect[1], [rect[1][0], rect[0][1]], rect[0]]
    return np.array(redef, dtype=np.float64)


def color_randomize(color: colorType, neighborhood: int | float = 1) -> colorType:
    _red = randint(max(0, color[0] - neighborhood), min(255, color[0] + neighborhood))
    _green = randint(max(0, color[1] - neighborhood), min(255, color[1] + neighborhood))
    _blue = randint(max(0, color[2] - neighborhood), min(255, color[2] + neighborhood))
    if len(color) == 4:
        return _red, _green, _blue, color[3]
    return _red, _green, _blue
