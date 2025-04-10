import sys

import numpy as np
import pygame
import pygame_gui
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

from Figure import Cube, Triangle


def draw_all_screen_info_txt(offset):
    text_offset = offset[:2:]
    num = offset[2]
    drawText(text_offset[0], text_offset[1], ("figure " + str(num) + ' coordinates: ' + str(a[num - 1].coordinates)))
    text_offset[1] -= 14
    if need_points_inf:
        for i in a[num - 1].points:
            text_offset[1] -= 14
            drawText(text_offset[0], text_offset[1], (str(i.coordinates)))
    num += 1
    output = [text_offset[0], text_offset[1], num]
    return output


# Функция для отображения текста
def drawText(x, y, text):
    font = pygame.font.SysFont('arial', 14)
    textSurface = font.render(text, True, (255, 255, 66, 255), (0, 66, 0, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


def project_polygon(vertices, axis):
    """Проецируем вершины на ось и возвращаем минимум и максимум."""
    dots = np.dot(vertices, axis)
    return np.min(dots), np.max(dots)


def is_separating_axis(axis, vertices1, vertices2):
    """Проверяет, является ли данная ось разделяющей для двух наборов вершин."""
    min1, max1 = project_polygon(vertices1, axis)
    min2, max2 = project_polygon(vertices2, axis)
    return max1 < min2 or max2 < min1  # Изменено на '<' для строгого сравнения


def generate_axes(vertices):
    """Генерируем оси, используя разности векторов между вершинами."""
    axes = []
    num_vertices = len(vertices)
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            axis = vertices[j] - vertices[i]
            norm = np.linalg.norm(axis)
            if norm >= 1e-8:  # Учитываем только ненулевые векторы
                axes.append(axis / norm)
    return axes


def check_collision(vertices1, vertices2):
    """Проверяет столкновение между двумя четырёхмерными фигурами."""
    vertices1 = vertices1.get_coordinates_of_points()
    vertices2 = vertices2.get_coordinates_of_points()

    # Генерируем оси для обеих фигур
    axes1 = generate_axes(vertices1)
    axes2 = generate_axes(vertices2)

    # Проверяем все оси из первой фигуры
    for axis in axes1:
        if is_separating_axis(axis, vertices1, vertices2):
            return False  # Найдена разделяющая ось

    # Проверяем все оси из второй фигуры
    for axis in axes2:
        if is_separating_axis(axis, vertices1, vertices2):
            return False  # Найдена разделяющая ось

    return True  # Нет разделяющих осей, фигуры сталкиваются


def main(desc):
    global a
    global need_points_inf
    need_points_inf = False
    a = []
    tt = 1
    for i in desc:
        if i[0] == 'Тессеракт':
            a.append(Cube(i[1], int(i[2]), tt, i[3]))
            tt *= -1
        elif i[0] == 'Апекс':
            a.append(Triangle(i[1], int(i[2]), tt, i[3]))
            tt *= -1

    rotation = 0
    pl = 0

    # Установка шрифта и размера

    roting = True
    pygame.init()
    display = (1280, 720)
    sc = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(100, (display[0] / display[1]), 0.1, 100.0)
    glTranslatef(0.0, 0.0, -5)
    pygame.mouse.set_visible(False)
    displayCenter = [720, 360]
    mouseMove = [0, 0]
    pygame.mouse.set_pos(displayCenter)
    manager = pygame_gui.UIManager((1280, 720))

    while True:
        keypress = pygame.key.get_pressed()  # Move using WASD
        manager.update(pygame.time.Clock().tick(60) / 1000.0)
        if keypress[pygame.K_w]:
            glTranslatef(0, 0, 0.1)
        if keypress[pygame.K_s]:
            glTranslatef(0, 0, -0.1)
        if keypress[pygame.K_d]:
            glTranslatef(-0.1, 0, 0)
        if keypress[pygame.K_a]:
            glTranslatef(0.1, 0, 0)
        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:

                    rotation = -0.1
                    pl = 0
                elif event.key == pygame.K_RIGHT:
                    rotation = 0.1
                    pl = 0
                elif event.key == pygame.K_UP:
                    rotation = -0.1
                    pl = 1
                elif event.key == pygame.K_DOWN:
                    rotation = 0.1
                    pl = 1
                elif event.key == pygame.K_TAB:
                    print('fu')
                    for i in a:
                        i.true_false_figurine()
                elif event.key == pygame.K_r:
                    if roting:
                        roting = False
                    else:
                        roting = True




            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    rotation = 0

            if event.type == pygame.MOUSEMOTION and roting:
                mouseMove = [event.pos[i] - displayCenter[i] for i in range(2)]
                pygame.mouse.set_pos(displayCenter)

        if roting:
            mouseMove = pygame.mouse.get_rel()
            glRotatef(mouseMove[0] * 0.1, 0.0, 1.0, 0.0)
            glRotatef(mouseMove[1] * 0.1, 1.0, 0.0, 0.0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        offset_for_text_and_num = [0, 706, 1]
        for i in a:
            i.update_cycle(rotation, pl)
            i.draw()
            offset_for_text_and_num = draw_all_screen_info_txt(offset_for_text_and_num)

        pygame.display.flip()
        # pygame.time.wait(15)
        if len(a) >=2:
            for i in range(len(a)):
                for j in range(i+1
                        ,len(a)):
                    if (check_collision(a[i], a[j])):
                        for k in a:
                            k.moving = False


#

if len(sys.argv) >= 3:
    input1 = sys.argv[1]
    input2 = sys.argv[2]
