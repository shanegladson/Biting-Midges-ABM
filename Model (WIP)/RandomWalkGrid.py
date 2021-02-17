from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

origin = [0,0]

def avg_displacement(model):
    x = [a.pos[0] for a in model.schedule.agents]
    y = [a.pos[1] for a in model.schedule.agents]

    disp = (sum(x)/len(x), sum(y)/len(y))
    return disp

class Walker(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
    def step(self):
        self.move()
    
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        
class WorldModel(Model):
    def __init__(self, N, width=10, height=10, start=None):
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
            
        self.datacollector = DataCollector(model_reporters={"Displacement" : avg_displacement},
                                               agent_reporters={"Position" : "pos"})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()


sim = WorldModel(10,10,10)
sim.step()