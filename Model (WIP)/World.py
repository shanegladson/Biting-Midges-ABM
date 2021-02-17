from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner
import random
import numpy as np
from Midge import Walker

class WorldModel(Model):
    def __init__(self, N, width=100, height=100):
        self.NumAgents = N
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, True)
        for i in range(self.NumAgents):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            a = Walker(i, self, x, y)
            self.schedule.add(a)
            
            self.grid.place_agent(a, (x,y))

        self.datacollector = DataCollector(agent_reporters={"x" : "x", "y" : "y"})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()