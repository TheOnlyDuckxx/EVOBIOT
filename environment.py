import pygame
from math import sin, cos
from noise import pnoise2
from random import random

class Cellule:
    def __init__(self, x, y, cell_type=None, seed=0):
        self.x = x
        self.y = y
        self.seed = seed
        self.altitude = self.get_altitude()
        self.cell_type = cell_type or self.generate_type()
        self.active = True

    def get_altitude(self):
        scale = 60
        x = self.x / scale
        y = self.y / scale
        return pnoise2(x, y, octaves=5,base=self.seed)


    def generate_type(self):
        a = self.altitude
        if a < -0.2:
            return "eau"
        elif a < 0.05:
            return self.generate_in_plaine()
        elif a < 0.2:
            return self.generate_in_sparse_forest()
        else:
            return self.generate_in_dense_forest()

    def generate_in_plaine(self):
        r = random()
        if r < 0.05:
            return "nourriture"
        elif r < 0.05:
            return "arbre"
        else:
            return "sol"

    def generate_in_sparse_forest(self):
        r = random()
        if r < 0.2:
            return "arbre"
        elif r < 0.05:
            return "nourriture"
        else:
            return "sol"

    def generate_in_dense_forest(self):
        r = random()
        if r < 0.4:
            return "arbre"
        elif r < 0.05:
            return "nourriture"
        else:
            return "sol"

    def get_color(self):
        colors = {
            "sol": (218, 247, 193),
            "eau": (180, 220, 255),
            "arbre": (112, 168, 110),
            "nourriture": (255, 229, 135)
        }
        return colors.get(self.cell_type, (0, 0, 0))

    def render(self, screen, cell_size):
        rect = (self.x * cell_size, self.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, self.get_color(), rect)
