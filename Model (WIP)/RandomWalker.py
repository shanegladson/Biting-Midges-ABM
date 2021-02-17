from mesa import Model, Agent
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner
import random
import numpy as np

class Walker(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
    def step(self):
        self.move()
    
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)