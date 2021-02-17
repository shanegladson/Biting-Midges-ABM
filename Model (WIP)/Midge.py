from mesa import Model, Agent
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner
import random
import numpy as np

class Walker(Agent):
    dps = 0.7 # Daily probability of survival. Applied every day of midge's life
    fed = False # True if the midge has taken a bloodmeal recently, False otherwise
    timesincefed = 0 # Time in days since the midge has fed, will only increase if the midge has fed at all, resets to 0 after another bloodmeal
    avgeggbatch = 100 # Average number of eggs laid per oviposition
    gtrclength = 14 # Number of days in the gonotrophpic cycle
    senserange = 5 # Range at which midges can detect CO2 emitting from source (deer or trap)


    def __init__(self, unique_id, model, x, y):
        super().__init__(unique_id, model)
        self.x, self.y = x, y

    def step(self):
        if True:
            # In future add toggle between random walk (searching) and biased walk (locked on to CO2 emitter)
            self.randomwalk()
            self.x, self.y = self.pos
        # TODO: Implement bloodfeeding/oviposition

        # Daily probability of survival calculation (uniform distribution), calculated at end of step function
        if random.random() > self.dps:
            self.death()
    
    # Random walk function, chooses randomly from available cells in Moore neighborhood
    def randomwalk(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
 
    # TODO: implement biased walk method when attracted to CO2 source (emission point)
    def biasedwalk(self, pos):
        return

    def death(self):
        self.model.grid._remove_agent(self.pos, self)
        self.model.schedule.remove(self)