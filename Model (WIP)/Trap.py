from mesa import Agent
from mesa.datacollection import DataCollector
import random
import numpy as np
from Target import Target


class Trap(Target):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.midgestrapped = 0

    def trapmidge(self):
        self.midgestrapped += 1

    def feed(self, midge):
        self.trapmidge()
        midge.death()

    def step(self):
        # print("There are " + str(len(self.model.grid.get_neighbors(self.pos, radius=3, include_center=False))) + " neighbors of the trap at " + str(self.pos))
        print("On day " + str(self.model.day) + ", there were " + str(self.midgestrapped) + " midges trapped.")
