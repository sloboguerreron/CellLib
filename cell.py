from random import random
import numpy as np
import math

class Cell:
    def __init__(self, idx, V0, num_steps):
        self.idx = idx
        self.V0 = V0
        self.total_steps = num_steps
        self.num_steps = 0

        self.V = []
        self.F = []
        self.rv = np.random.rand()
        self.sons = []

    def change(self, Vn):
        self.F.append(0)
        self.V.append(Vn)
        self.rv = np.random.rand()


    def division(self, Vn):
        self.F.append(0)
        self.V.append(Vn/2)
        self.rv = np.random.rand()


    def add_growth(self, Vn, Fn):
        self.F.append(Fn)
        self.V.append(Vn)

    def get_size(self, time):
        return self.V[time]

    def __str__(self):
        return "Cell: {\n   idx: "+str(self.idx)+"\n    V0: "+str(self.V0)+"\n}"
