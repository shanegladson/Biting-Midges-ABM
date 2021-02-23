from mesa import Agent
import Midge
import random
import types


class Egg(Agent):
    growthtime = 14
    survivalprob = 0.60

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.age = 0

    def step(self) -> None:
        if self.age >= Egg.growthtime:
            if random.random() >= Egg.survivalprob:
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
            else:
                a = Midge.Midge(self.model.idcounter, self.model)
                self.model.schedule.add(a)
                self.model.grid.place_agent(a, self.pos)

                self.model.idcounter += 1
        else:
            self.age += 1
