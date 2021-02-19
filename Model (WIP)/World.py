from mesa import Model
from mesa.space import MultiGrid
from mesa.time import BaseScheduler
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner
import random
import numpy as np
from Midge import Midge

class WorldModel(Model):
    def __init__(self, NumMidges, width=100, height=100):
        # Starting number of midges
        self.NumMidges = NumMidges

        # Time (days) since simulation has begun
        self.day = 0

        # Activates the step function for midges sequentially (no order needed)
        self.schedule = BaseScheduler(self)

        # Create a grid model with potential for multiple agents on one cell
        self.grid = MultiGrid(width, height, True)

        # Adds midges to random location in grid and scheduler
        for i in range(self.NumMidges):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            a = Midge(i, self, x, y)
            self.schedule.add(a)
            
            self.grid.place_agent(a, (x,y))

        # Collects position data for each midge every day
        self.datacollector = DataCollector(agent_reporters={"x" : "x", "y" : "y"})

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)