from mesa import Agent
from mesa.datacollection import DataCollector
import random
import numpy as np
import Target
import Trap

class Midge(Agent):
    dps = 0.7 # Daily probability of survival. Applied every day of midge's life (Maybe model with sine wave?)
    avgeggbatch = 100 # Average number of eggs laid per oviposition
    gtrclength = 14 # Number of days in the gonotrophpic cycle
    senserange = 1 # Range at which midges can detect CO2 emitting from source (deer or trap) in grid tiles
    fov = 2*np.pi # Field of View which the midge chooses from to move
    step_length = 5 # Distance traveled per step

    def __init__(self, unique_id, model, x, y):
        super().__init__(unique_id, model)
        self.fed = False # True if the midge has taken a bloodmeal recently, False otherwise
        self.timesincefed = 0 # Time in days since the midge has fed, will only increase if the midge has fed at all, resets to 0 after another bloodmeal
        self.previous_angle = 0
        self.dead = False # Toggles when midge has either died or entered trap
    def step(self):

        if not self.fed:
            # Get list of agents in nearby "sensitivity" radius
            neighbors = self.model.grid.get_neighbors(self.pos, radius=Midge.senserange)
            
            # Iterate through neighbors and filter for Target agent
            # TODO: Implement decision-making process for each animal
            if len(neighbors) > 1:
	            for n in neighbors:
	                if issubclass(type(n), Target.Target):
	                    # Navigate to bloodmeal source
	                    self.biasedwalk(n.pos)
	                    self.feed(n)
            else:
	            self.randomwalk()

        # If days since last bloodmeal >= gonotrophic cycle, begin oviposition
        elif self.timesincefed >= Midge.gtrclength:
            self.layeggs()
            self.fed = False

        # Random walk if not searching for food, increment days since fed
        else:
            self.timesincefed += 1
            self.randomwalk()


        # Daily probability of survival calculation (uniform distribution), calculated at end of step function only if midge is still alive
        if not self.dead and random.random() > self.dps:
            print("Killing midge " + str(self.unique_id) + " by dps")
            self.death()
            return

    # Random walk function, chooses randomly from available cells in Moore neighborhood
    def randomwalk(self):
        new_position = (0,0)
        angle = 0
        while self.model.grid.out_of_bounds(new_position):
            new_position, angle = self.new_position()
            self.model.grid.move_agent(self, new_position)

        self.previous_angle = angle

    def new_position(self):
        angle = self.previous_angle + random.uniform(-self.fov/2, self.fov/2)
        new_position = (self.pos[0]+self.step_length*np.cos(angle), self.pos[1]+self.step_length*np.sin(angle))
        return new_position, angle
 
    # TODO: implement biased walk method when attracted to CO2 source (emission point)
    def biasedwalk(self, pos):
        self.model.grid.move_agent(self, pos)

    # TODO: Implement bloodfeeding of other animals/trap
    def feed(self, prey):
        if not prey.istrap:
            self.fed = True
            self.timesincefed = 0
            return
        elif type(prey) == Trap.Trap:
            print("Midge " + str(self.unique_id) + " found trap")
            prey.trapmidge()
            print("trapmidge incremented")
            self.death()
            print("Midge killed")

    # TODO: Implement egg-laying process
    def layeggs(self):
        # Adds avgeggbatch number of eggs to the model (TODO: implement larval stage and distribution of batch sizes)
        for i in range(Midge.avgeggbatch):
            # Each offspring has same starting location as egg-laying location
            a = Midge(random.random(), self.model, self.pos[0], self.pos[1])
            self.model.schedule.add(a)
            self.model.grid.place_agent(a, self.pos)

    def death(self):
        print("In death function")
        # Add midges to list which will kill them all at the end of the day
        self.model.kill_midges.append(self)
        print("Appended midge " + str(self.unique_id) + " to kill list")
        self.dead = True