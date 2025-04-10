
import OpenGL.GL
import OpenGL.GLUT
import OpenGL.GLU
from functools import singledispatchmethod

class Point:
    def __init__(self,x,y,z,v):
        self.coordinates = [x,y,z,v]
        self.trim_cord = []
    # @singledispatchmethod
    def __add__(a, b):
        new_cord = [0, 0, 0]
        for i in range(len(a.coordinates)):
            new_cord[i] = a.coordinates[i] + b.coordinates[i]
        return new_cord


    def __sub__(self, other):
        new_cord = [0, 0, 0,0]
        for i in range(len(self.coordinates)):
            new_cord[i] = self.coordinates[i] - other.coordinates[i]
        return new_cord

    # @__add__.register
    # def _(a,b: Vector):
    #     new_cord = [0,0,0]
    #     for i in range(len(a.coordinates)):
    #         new_cord[i] = a.coordinates[i] + b.coordinates[i]
    #     return new_cord

    def __neg__(a):
        a.coordinates = [-a.coordinates[0], -a.coordinates[1], -a.coordinates[2], -a.coordinates[3]]
    def get_coordinates(self):
        return self.coordinates


    def change_coordinates(self,new_coordinates):
        self.coordinates = new_coordinates


    def draw_Point(self):
        pass