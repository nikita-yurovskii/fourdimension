
from Vector import Vector
from abc import ABC, abstractmethod
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import math
import numpy as np
from Point import Point
import itertools

class Figure:
    def __init__(self, points, coordinates, scale, mover, color):
        self.color = color
        self.scale = scale
        self.coordinates = coordinates
        self.points = points
        for i in self.points:
            for j in range(len(i.coordinates)):
                i.coordinates[j] += self.coordinates[j]
                i.coordinates[j] *= scale
        self.dxd=[0.5,0.5,0,1]
        self.edgez = []
        self.moving = False
        self.mover = mover
        self.surfaces = None
        self.coordinates = self.center_of_4d_shape()
    def update_cycle(self,rotation,pl):
        self.move_fucking_figurine()
        self.rotate_figure(rotation,pl)

    def calc_surfaces(self):
            print(self.edgez)
            faces = []

            # Тессеракт имеет 8 кубических ячеек, каждая из которых состоит из 6 квадратных граней.
            # Всего 24 грани. Рассмотрим их по координатным направлениям.

            # Фиксируем каждую из 4 координат и изменяем оставшиеся
            for fixed_coordinate in range(4):
                vertices = []
                # Генерируем все возможные комбинации из 4 бит (0 и 1)
                for i in range(16):  # 2^4 = 16
                    # Преобразуем число в двоичную строку с 4 битами
                    vertex = [(i >> j) & 1 for j in range(4)]
                    vertices.append(vertex)
                return vertices

            return faces
    def proecite(self):
        for i in (self.points):
            if self.dxd[3] != 0:
                i.trim_cord = [i.coordinates[0]-i.coordinates[3]*self.dxd[0]/self.dxd[3],i.coordinates[1]-i.coordinates[3]*self.dxd[1]/self.dxd[3], i.coordinates[2]-i.coordinates[3]*self.dxd[2]/self.dxd[3] ]
            else:
                i.trim_cord = [i.coordinates[0], i.coordinates[1], i.coordinates[2]]
    def draw(self):

        glBegin(GL_QUADS)
        # for surface in self.calc_surfaces():
        #     x = 0
        #     for vertex in surface:
        #         x += 1
        #         glColor3fv((1,1,1))
        #
        glEnd()
        self.proecite()

        glColor3f(int(self.color[0])/255,int(self.color[1])/255,int(self.color[2])/255)
        #glColor3f(1, 0, 0)
        glBegin(GL_LINES)
        for edge in self.edgez:
            for vertex in edge:
                glVertex3fv(self.points[vertex].trim_cord)
        glEnd()

    def rotate_figure(self, angle, plosk):
        # Шаг 1: Вычислить центр фигуры
        center = np.mean([point.coordinates for point in self.points], axis=0)

        # Шаг 2: Сместить фигуры к началу координат
        for i in self.points:
            i.coordinates = np.array(i.coordinates) - center

        # Шаг 3: Применить матрицу поворота
        if plosk == 0:
            mat_povorota = np.array([[1, 0, 0, 0],
                                     [0, 1, 0, 0],
                                     [0, 0, math.cos(angle), -math.sin(angle)],
                                     [0, 0, math.sin(angle), math.cos(angle)]])
        elif plosk == 1:
            mat_povorota = np.array([[math.cos(angle), 0, 0, -math.sin(angle)],
                                     [0, 1, 0, 0],
                                     [0, 0, 1, 0],
                                     [math.sin(angle), 0, 0, math.cos(angle)]])

        for i in self.points:
            mat_tochki = np.array([i.coordinates[0],
                                   i.coordinates[1],
                                   i.coordinates[2],
                                   i.coordinates[3]])
            mat_itog = mat_povorota.dot(mat_tochki)
            i.coordinates = [mat_itog[0], mat_itog[1], mat_itog[2], mat_itog[3]]

        # Шаг 4: Сместить фигуры обратно
        for i in self.points:
            i.coordinates += center

    def true_false_figurine(self):
        if self.moving:
            self.moving = False
        else:
            self.moving = True

    def center_of_4d_shape(self):
        n = len(self.points)
        if n == 0:
            raise ValueError("Список вершин не должен быть пустым")

        sum_x = sum(vertex.coordinates[0] for vertex in self.points)
        sum_y = sum(vertex.coordinates[1] for vertex in self.points)
        sum_z = sum(vertex.coordinates[2] for vertex in self.points)
        sum_w = sum(vertex.coordinates[3] for vertex in self.points)

        center_x = sum_x / n
        center_y = sum_y / n
        center_z = sum_z / n
        center_w = sum_w / n

        return (center_x, center_y, center_z, center_w)
    def move_fucking_figurine(self):
        if self.moving:
            for i in self.points:
                i.coordinates[0]+=(0.1*self.mover)
            self.coordinates = np.mean([point.coordinates for point in self.points], axis=0)


    def find_side(self, point):
        pass



    def get_coordinates_of_points(self):
        a = []
        for i in self.points:
            a.append(i.coordinates)
        return a

class Cube(Figure):
    def __init__(self,coordinates,scale,mover, color):
        vertices = []
        # Генерируем все возможные комбинации координат (0 или 1) для 4-мерного пространства
        for i in range(16):  # 2^4 = 16
            # Формируем координаты в 4D
            vertex = [(i >> j) & 1 for j in range(4)]
            vertices.append(vertex)

        super().__init__(list(Point(vertices[i][0],vertices[i][1],vertices[i][2],vertices[i][3] ) for i in range(len(vertices))),coordinates, scale,mover, color)

        edges = []
        num_vertices = len(vertices)

        # Проверяем каждую вершину
        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                # Проверяем, отличаются ли вершины в ровно одной координате
                if sum(a != b for a, b in zip(vertices[i], vertices[j])) == 1:
                    edges.append((i, j))  # Добавляем связь между вершинами


        self.edgez = edges






class Triangle(Figure):
    def __init__(self, coordinates, scale, mover, color):
        vertices = []
        base_vertices = [
            (1, 0, 0, 0),  # Вершина 1
            (0, 1, 0, 0),  # Вершина 2
            (0, 0, 1, 0),  # Вершина 3

        ]
        height = 1  # Высота пирамиды (координата w)
        # Вершина (апекс) пирамиды
        apex = (0, 0, 0, height)

        # Список всех вершин (апекс + базовые вершины)
        vertices = base_vertices + [apex]
        # Генерация ребер
        # Генерация ребер
        edges = []

        # Добавляем ребра между базовыми вершинами по индексам
        for i, j in itertools.combinations(range(len(base_vertices)), 2):
            edges.append((i, j))

        # Добавляем ребра от апекса к каждой из базовых вершин по индексам
        apex_index = len(base_vertices)
        for i in range(len(base_vertices)):
            edges.append((apex_index, i))



        super().__init__(
            list(Point(vertices[i][0], vertices[i][1], vertices[i][2], vertices[i][3]) for i in range(len(vertices))),
            coordinates, scale, mover, color)
        self.edgez = edges
