from mesa import Model
from mesa.space import Grid
from mesa.time import BaseScheduler
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner
import random
import numpy as np
from Midge import Midge
from Trap import Trap

class WorldModel(Model):
    def __init__(self, NumMidges, width=100, height=100):
        # Starting number of midges
        self.NumMidges = NumMidges

        # Time (days) since simulation has begun
        self.day = 0

        # Activates the step function for midges sequentially (no order needed)
        self.schedule = BaseScheduler(self)

        # Create a grid model with potential for multiple agents on one cell
        self.grid = Grid(width, height, True)

        # Adds midges to random location in grid and to queue in scheduler
        for i in range(self.NumMidges):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            a = Midge(random.random(), self, x, y)
            self.schedule.add(a)
            
            self.grid.place_agent(a, (x,y))


        self.trap = Trap(random.random(), self)
        self.schedule.add(self.trap)
        self.grid.place_agent(self.trap, (1,1))

        # # TODO: Implement datacollector that can collect data from different agent types (gonna be a pain in my ass)
        #self.datacollector = DataCollector(agent_reporters={"x" : "x", "y" : "y"})

        self.kill_midges = []

    def step(self):
        self.kill_midges = []

        self.schedule.step()
        #self.datacollector.collect(self)

        for m in self.kill_midges:
            self.grid._remove_agent(m.pos, m)
            self.schedule.remove(m)