from Engine import *
from mathDisplay import *
from pDisplay import *
import Tools as tl


#pygame: Задача про две управляемые точки
def pg_plot():
    """pygame: задача про две управляемые точки.\nУправление осуществляется стрелками с клавиатуры."""
    pygame.init()
    screen = pygame.display.set_mode([1600, 1200])
    pygame.display.set_caption('Управляемая точка')
    clock = pygame.time.Clock()
    display = Display(screen)
    dot = display.create_point([0, 0], clRed)
    fat_dot = display.create_fat_point([10, 10], 5, clGreen)
    move, f_move, d = [0, 0], np.array((0, 0)), 2
    done = False
    while not done:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    move = [0, -10]
                    f_move += np.array([0, -d])
                if event.key == pygame.K_UP:
                    move = [0, 10]
                    f_move += np.array([0, d])
                if event.key == pygame.K_LEFT:
                    move = [-10, 0]
                    f_move += np.array([-d, 0])
                if event.key == pygame.K_RIGHT:
                    move = [10, 0]
                    f_move += np.array([d, 0])
            if event.type == pygame.KEYUP:
                if event.key in {pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT}:
                    move = [0, 0]
        dot.move(move)
        fat_dot.move(f_move)
        display.show()
        pygame.display.flip()
    pygame.quit()


#pygame: Задача про точку, перемещающуюся по круговой траектории
def pg_path_dot():
    """pygame: задача про точку, которая движется по окружности."""
    pygame.init()
    screen = pygame.display.set_mode([1600, 1200])
    pygame.display.set_caption('Орбита')
    clock = pygame.time.Clock()
    display = Display(screen)
    path1, path2 = CirclePath(100, 5), CirclePath(300, 18, 0, False)
    steps_on_path1, steps_on_path2 = path1.step_on(), path2.step_on()
    fat_dot1 = display.create_fat_point(path1.starter(), 15, clWhite)
    fat_dot2 = display.create_fat_point(path2.starter(), 8, clBlue)
    display.create_fat_point([0, 0], 25, clRed)
    done = False
    while not done:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        fat_dot1.move(next(steps_on_path1))
        fat_dot2.move(next(steps_on_path2))
        display.show()
        pygame.display.flip()
    pygame.quit()

#pygame: Задача про точку, перемещающуюся по квадратной траектории
def pg_path_square():
    """pygame: задача про точку, которая движется по траектории "квадрат"."""
    pygame.init()
    screen = pygame.display.set_mode([1600, 1200])
    pygame.display.set_caption('Квадрат')
    clock = pygame.time.Clock()
    display = Display(screen)
    display.create_fat_point((0, 0), 10, clWhite)
    length = 200
    sp = SquarePath(length, 100)
    #Круговые траектории (необязательные в рамках задачи):
    left_bottom = sp.starter()
    left_top = [left_bottom[0], -left_bottom[1]]
    right_top = [-left_bottom[0], -left_bottom[1]]
    right_bottom = [-left_bottom[0], left_bottom[1]]
    paths = (CirclePath(12, 4, 0, True, left_bottom), CirclePath(12, 4, pi / 2, True, left_top),
             CirclePath(12, 4, pi, True, right_top), CirclePath(12, 4, 3 * pi / 2, True, right_bottom))
    steps_on_paths = [path.step_on() for path in paths]
    orbs = [display.create_fat_point(path.starter(), 3, clGreen) for path in paths]
    #Точка, идущая по траектории "квадрат":
    sq_dot = display.create_fat_point(sp.starter(), 8, clRed)
    sp_path = sp.step_on()
    done = False
    while not done:
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        sq_dot.move(next(sp_path))
        for orb, steps in zip(orbs, steps_on_paths):
            orb.move(next(steps))
        display.show()
        pygame.display.flip()
    pygame.quit()

#pygame: Задача про перемещение червя
def pg_worms():
    """pygame: задача про червя, который движется по окружности."""
    pygame.init()
    screen = pygame.display.set_mode([1600, 1200])
    pygame.display.set_caption('Червь')
    clock = pygame.time.Clock()
    display = Display(screen)
    path = CircleUnevenPath(300, 25, 0, False)
    steps_on_path = path.step_on()
    worm = display.create_worm(path.starter(), 4, 6, 8, 15, clWhite)
    display.create_fat_point([0, 0], 25, clRed)
    done = False
    while not done:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        worm.move(next(steps_on_path))
        display.show()
        pygame.display.flip()
    pygame.quit()

#matplotlib: Задача про точку, перемещающуюся по квадратной траектории
def mpl_path_square():
    """matplotlib: задача про точку, которая движется по траектории "квадрат"."""
    import time

    def close(_):
        done.append(1)

    size_rect = (1000, 800)
    my_dpi = 100
    plt.ion()
    fig = plt.figure("Квадрат", figsize=(size_rect[0]/my_dpi, size_rect[1]/my_dpi), dpi=my_dpi)
    display = GraphDisplay(fig, size_rect)
    length = 200
    sp = SquarePath(length, 100)
    sq_dot = display.create_fat_point(sp.starter(), 15, clRed)
    sp_path = sp.step_on()
    display.create_point((0, 0))
    done = []
    while not done:
        display.show()
        sq_dot.move(next(sp_path))
        fig.canvas.mpl_connect('close_event', close)
        time.sleep(0.01)
    plt.close(fig)
    plt.close()


#matplotlib: Задача про точку, перемещающуюся по отрезку
def mpl_path_line():
    """matplotlib: задача про точку, которая движется по траектории "отрезок"."""
    import time

    def close(_):
        done.append(1)

    size_rect = (1000, 800)
    my_dpi = 100
    plt.ion()
    fig = plt.figure("По отрезку", figsize=(size_rect[0]/my_dpi, size_rect[1]/my_dpi), dpi=my_dpi)
    display = GraphDisplay(fig, size_rect)
    length = 200
    sp = LinearPath(length, 25, [1, 1])
    display.create_point((0, 0))
    sq_dot = display.create_fat_point(sp.starter(), 15, clRed)
    sp_path = sp.step_on()
    done = []
    while not done:
        display.show()
        sq_dot.move(next(sp_path))
        fig.canvas.mpl_connect('close_event', close)
        time.sleep(0.01)
    plt.close(fig)
    plt.close()

#matplotlib: Задача про точку, перемещающуюся по дуге
def mpl_path_arc():
    """matplotlib: задача про точку, которая движется по траектории "дуга"."""
    import time

    def close(_):
        done.append(1)

    size_rect = (1000, 800)
    my_dpi = 100
    plt.ion()
    fig = plt.figure("Дуга", figsize=(size_rect[0]/my_dpi, size_rect[1]/my_dpi), dpi=my_dpi)
    display = GraphDisplay(fig, size_rect)
    length_r = 200
    sp = ArcPath(length_r, pi, 0, 30)
    display.create_point((0, 0))
    sq_dot = display.create_fat_point(sp.starter(), 15, clRed)
    sp_path = sp.step_on()
    done = []
    while not done:
        display.show()
        sq_dot.move(next(sp_path))
        fig.canvas.mpl_connect('close_event', close)
        time.sleep(0.01)
    plt.close(fig)
    plt.close()

#pygame: Задача про точку, перемещающуюся по дуге
def pg_path_arc():
    """pygame: задача про точку, которая движется по траектории "дуга"."""
    pygame.init()
    screen = pygame.display.set_mode([1600, 1200])
    pygame.display.set_caption('Квадрат')
    clock = pygame.time.Clock()
    display = Display(screen)
    length_r = 200
    sp = ArcPath(length_r, pi, 0, 33)
    display.create_point((0, 0))
    sq_dot = display.create_fat_point(sp.starter(), 15, clRed)
    sp_path = sp.step_on()
    done = False
    while not done:
        clock.tick(22)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        sq_dot.move(next(sp_path))
        display.show()
        pygame.display.flip()
    pygame.quit()

#pygame: Задача про точку, перемещающуюся по траектории "буква н"
def pg_path_letterH():
    """pygame: задача про точку, которая движется по траектории "буква н"."""
    pygame.init()
    screen = pygame.display.set_mode([1600, 1200])
    pygame.display.set_caption('Буква Н')
    clock = pygame.time.Clock()
    display = Display(screen, back_color=clWhite)
    display.create_fat_point((0, 0), 10, clBlack)
    length = 250
    letterN_path = [[0, 1], [0, 1], [0, 1], [1, 0], [0, -1], [1, 0], [0, 1], [1, 0],
                    [0, -1], [0, -1], [0, -1], [-1, 0], [0, 1], [-1, 0], [0, -1], [-1, 0]]
    sp = PolylinearPath(length, length // 10, True, letterN_path, 3*length)
    # Обрамление траектории точками (необязательная часть):
    place = sp.starter()
    count_step = 10
    length_step = length / count_step
    for vec in letterN_path:
        st = dot_coors(vec)
        for _ in range(count_step):
            place += length_step * st
            display.create_fat_point(place, 10, clBlack)
    # Создание перемещающейся точки (цвет - красный, прозрачный с A=120):
    sq_dot = display.create_fat_point(sp.starter(), 20, (255, 0, 0, 120))
    sp_path = sp.step_on()
    done = False
    while not done:
        clock.tick(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        sq_dot.move(next(sp_path))
        display.show()
        pygame.display.flip()
    pygame.quit()


#pygame: Задача про точку, отражающуюся от стенок прямоугольника
def pg_reflect():
    """pygame: точка находится внутри прямоугольника и отражается от его стенок."""
    pygame.init()
    screen = pygame.display.set_mode([1600, 1200])
    pygame.display.set_caption('Внутри прямоугольника')
    clock = pygame.time.Clock()
    display = Display(screen)
    runer = display.create_fat_point([0, 0], 10, clRed)
    run_dir = [4, 4]
    rect = [[-400, -300], [400, 300]]
    # Обрамление рамок прямоугольника точками:
    width, height = rect[1][0] - rect[0][0], rect[1][1] - rect[0][1]
    dirs = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    length_step = 25
    width_step, height_step = width // length_step, height // length_step
    place = dot_coors(rect[0])
    for dir_ in dirs:
        d = dot_coors(dir_)
        way = width_step if d[0] else height_step
        for _ in range(way):
            place += d*length_step
            display.create_fat_point(place, 10)
    done = False
    while not done:
        clock.tick(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        display.show()
        if tl.dot_not_in_rect(runer.coors, run_dir, rect):
            run_dir = tl.reflect_vec(runer.coors, run_dir, rect)
        runer.move(run_dir)
        pygame.display.flip()
    pygame.quit()
