from mesa import Agent
from mesa.datacollection import DataCollector
import random


class Target(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    # Feed function that requires a midge and is dependent on the type of agent that the midge will feed on
    def feed(self, midge):
        return
