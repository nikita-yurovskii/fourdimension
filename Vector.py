from Point import Point
import numpy as np
import OpenGL.GL
import OpenGL.GLUT
import OpenGL.GLU

class Vector:
    def __init__(self, point1: Point, point2: Point):
        self.start = point1
        self.end = point2
        self.coordinates = self.end - self.start


    def rotate(self,fi):
        a_coords = self.start.get_coordinates()
        b_coords = self.end.get_coordinates()

        self.start.change_coordinates()
