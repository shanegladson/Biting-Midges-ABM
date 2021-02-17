from mesa import Model, Agent
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner
import random
import numpy as np

class Walker(Agent):
    age = 0 # Age in days
    fed = False # True if the midge has taken a bloodmeal recently, False otherwise
    timesincefed = 0 # Time in days since the midge has fed, will only increase if the midge has fed at all, resets to 0 after another bloodmeal
    avgeggbatch = 100 # Average number of eggs laid per oviposition
    gtrclength = 14 # Number of days in the gonotrophpic cycle
    senserange = 5 # Range at which midges can detect CO2 emitting from source (deer or trap)

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
    def step(self):
        self.move()
    
    def randomwalk(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def biasedwalk(self):
        return