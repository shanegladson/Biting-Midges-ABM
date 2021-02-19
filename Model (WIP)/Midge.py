from mesa import Agent
from mesa.datacollection import DataCollector
import random
import numpy as np

class Midge(Agent):
    dps = 0.7 # Daily probability of survival. Applied every day of midge's life
    avgeggbatch = 100 # Average number of eggs laid per oviposition
    gtrclength = 14 # Number of days in the gonotrophpic cycle
    senserange = 5 # Range at which midges can detect CO2 emitting from source (deer or trap) in grid tiles


    def __init__(self, unique_id, model, x, y):
        super().__init__(unique_id, model)
        self.fed = False # True if the midge has taken a bloodmeal recently, False otherwise
        self.timesincefed = 0 # Time in days since the midge has fed, will only increase if the midge has fed at all, resets to 0 after another bloodmeal
    
    def step(self):
        self.x, self.y = self.pos

        if not self.fed:
            # Get list of agents in nearby "sensitivity" radius
            neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=True, radius=Midge.senserange)
            
            # Iterate through neighbors and filter out all other midges
            # TODO: Implement decision-making process for each animal
            for n in neighbors:
                if type(self) != type(n):
                    # Navigate to bloodmeal source
                    self.biasedwalk(n.pos)
                    self.feed(n)
                    # Could be problem if trap deletes midge before these variables can be changed, watch out for potential bug
                    self.fed = True
                    self.timesincefed = 0
        
        # If days since last bloodmeal > gonotrophic cycle, begin oviposition
        elif self.timesincefed >= Midge.gtrclength:
            self.layeggs()
            self.fed = False

        # Random walk if not searching for food, increment days since fed
        else:
            self.timesincefed += 1
            self.randomwalk()


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
        self.model.grid.move_agent(self, pos)

    # TODO: Implement bloodfeeding of other animals/trap
    def feed(self, prey):
        if not prey.istrap:
            return
        else:
            prey.midgestrapped += 1
            self.death()

    # TODO: Implement egg-laying process
    def layeggs(self):
        return

    def death(self):
        self.model.grid._remove_agent(self.pos, self)
        self.model.schedule.remove(self)