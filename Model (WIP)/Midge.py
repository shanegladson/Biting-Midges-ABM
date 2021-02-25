from mesa import Agent
from mesa.datacollection import DataCollector
import random
import numpy as np
import Target
import Trap
import Deer
import Egg


class Midge(Agent):
    dps = 0.75  # Daily probability of survival. Applied every day of midge's life (Maybe model with sine wave?)
    avgeggbatch = 100  # Average number of eggs laid per oviposition
    gtrclength = 14  # Number of days in the gonotrophpic cycle
    senserange = 5  # Range at which midges can detect CO2 emitting from source (deer or trap) in grid tiles
    fov = 2 * np.pi  # Field of View which the midge chooses from to move
    step_length = 2  # Distance traveled per step

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.fed = False  # True if the midge has taken a bloodmeal recently, False otherwise
        self.timesincefed = 0  # Time in days since the midge has fed, will only increase if the midge has fed at all, resets to 0 after another bloodmeal
        self.previous_angle = 0
        self.dead = False  # Toggles when midge has either died or entered trap
        self.hasbtv = False

    def step(self):
        # Get list of targets in nearby "sensitivity" radius
        # TODO: Optimize by preloading a list of targets, and then will just select from a certain radius instead of 20K midges searching each step
        nearbytargets = [i for i in self.model.targets if self.model.grid.get_distance(self.pos, i.pos) <= Midge.senserange]

        if not self.fed and len(nearbytargets) != 0:

            # Iterate through neighbors and filter for Target agent
            # TODO: Implement decision-making process for each animal
            n = random.choice(nearbytargets)
            # Navigate to bloodmeal source
            self.biasedwalk(n.pos)
            if n.pos == self.pos:
                self.feed(n)

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
            # print("Killing midge " + str(self.unique_id) + " by DPS")
            self.death()
            return

    # Random walk function, chooses randomly from available cells
    def randomwalk(self):
        new_position, angle = self.randomposition()

        while self.model.grid.out_of_bounds(new_position):
            new_position, angle = self.randomposition()

        self.model.grid.move_agent(self, new_position)

        self.previous_angle = angle

    # New position function to use correlated random walk, can adjust fov in the future
    def randomposition(self):
        angle = self.previous_angle + random.uniform(-self.fov / 2, self.fov / 2)
        new_position = (self.pos[0] + self.step_length * np.cos(angle), self.pos[1] + self.step_length * np.sin(angle))
        return new_position, angle

    # Navigates to the position given, if not within range then as close as possible
    def biasedwalk(self, pos):
        if self.model.grid.get_distance(self.pos, pos) <= Midge.step_length:
            self.model.grid.move_agent(self, pos)

        else:
            # Get direction of desired position as a tuple
            heading = self.model.grid.get_heading(self.pos, pos)

            # Compute the angle at which to fly
            dx, dy = heading
            angle = np.arctan2(dy, dx)

            # Calculate new position based on angle and step length
            new_position = (self.pos[0] + self.step_length * np.cos(angle), self.pos[1] + self.step_length * np.sin(angle))

            # Move midge to new position
            self.model.grid.move_agent(self, new_position)

    # TODO: Expand on bloodfeeding of other animals

    def feed(self, prey):
        # Activates the feed function for the prey agent, passes itself as the argument
        prey.feed(self)
        return

    # Function that lays eggs, which will then incubate and develop into adults in the same location
    def layeggs(self):
        # Adds normal distribution with avgeggbatch mean number of eggs to the model (TODO: implement larval stage and distribution of batch sizes)
        # TODO: Optimize by doing total survival calc in one go
        batchsize = abs(int(0.5*random.normalvariate(Midge.avgeggbatch, 10)))
        for i in range(batchsize):
            # Each offspring has same starting location as egg-laying location
            a = Egg.Egg(self.model.idcounter, self.model)
            self.model.schedule.add(a)
            self.model.grid.place_agent(a, self.pos)

            self.model.idcounter += 1

    # Death function that removes the midge from the grid as well as deletes it from the scheduler
    def death(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)
        self.dead = True
