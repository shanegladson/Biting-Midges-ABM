from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import BaseScheduler
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner
import random
import numpy as np
import Midge
import Trap
import Deer
import Egg
import BiomeCell
import csv
import itertools


class WorldModel(Model):
    def __init__(self, NumMidges, NumTraps, NumDeer, width=100, height=100, mapfile=None):
        # Starting number of midges
        self.NumMidges = NumMidges
        self.NumTraps = NumTraps
        self.NumDeer = NumDeer
        self.idcounter = 0
        self.mapfile = mapfile

        self.midges = []
        self.traps = []
        self.deer = []

        # Time (days) since simulation has begun
        self.day = 0

        # Activates the step function for midges sequentially (no order needed)
        self.schedule = BaseScheduler(self)

        # Create a grid model with potential for multiple agents on one cell
        self.grid = ContinuousSpace(width, height, torus=False)

        # Adds midges to random location in grid and to queue in scheduler
        for i in range(self.NumMidges):
            x = self.random.random() * self.grid.width
            y = self.random.random() * self.grid.height
            a = Midge.Midge(self.idcounter, self)
            self.schedule.add(a)

            self.grid.place_agent(a, (x, y))

            self.idcounter += 1

        # Adds some eggs to the simulation as well, just to even out the population variability
        for i in range(250):
            x = self.random.random() * (self.grid.width)
            y = self.random.random() * (self.grid.height)
            a = Egg.Egg(self.idcounter, self)
            self.schedule.add(a)

            self.grid.place_agent(a, (x, y))

            self.idcounter += 1

        # Adds traps to random locations in the grid and to queue in scheduler
        for i in range(self.NumTraps):
            x = self.random.random() * (self.grid.width)
            y = self.random.random() * (self.grid.height)
            a = Trap.Trap(self.idcounter, self)
            self.schedule.add(a)

            self.grid.place_agent(a, (x, y))

            self.idcounter += 1

        # Adds deer to random locations in the grid and to queue in scheduler
        for i in range(self.NumDeer):
            x = self.random.random() * (self.grid.width)
            y = self.random.random() * (self.grid.height)
            a = Deer.Deer(self.idcounter, self)
            self.schedule.add(a)

            self.grid.place_agent(a, (x, y))

            self.idcounter += 1

        self.traps = [i for i in self.schedule.agents if type(i) == Trap.Trap]
        self.deer = [i for i in self.schedule.agents if type(i) == Deer.Deer]
        self.targets = combinelists(self.traps, self.deer)
        self.deerbites = 0

        # TODO: Implement datacollector that can collect data from different agent types (gonna be a pain in my ass)
        self.datacollector = DataCollector(model_reporters={"MidgePop" : "NumMidges",
                                                            "TotalDeerBites" : "deerbites"})


    def step(self):

        self.datacollector.collect(self)

        # World step function. Steps each agent as well as increments the day clock
        self.schedule.step()

        self.day += 1

        self.midges = [i for i in self.schedule.agents if type(i) == Midge.Midge]
        self.NumMidges = len(self.midges)
        self.deerbites = sum([d.numbites for d in self.deer])

        # print("On day " + str(self.day) + " there are " + str(self.NumMidges) + " midges left.")


def MidgePop(midges):
    return len(midges)

def combinelists(list1, list2):
    l = []
    l.extend(list1)
    l.extend(list2)
    return l