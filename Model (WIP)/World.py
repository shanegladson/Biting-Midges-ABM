from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner
import random
import numpy as np
import Midge

class WorldModel(Model):
    def __init__(self, N, width=1000, height=1000, start=None):
        self.NumAgents = N
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, True)
        for i in range(self.NumAgents):
            a = Walker(i, self)
            self.schedule.add(a)
            
            if start == None:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                self.grid.place_agent(a, (x,y))
            else:
                self.grid.place_agent(a, start)
            
        self.datacollector = DataCollector(agent_reporters={"Position" : "pos"})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()