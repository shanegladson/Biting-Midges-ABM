from mesa import Agent
from mesa.datacollection import DataCollector
import random

class Target(Agent):
	def __init__(self, unique_id, model, istrap):
		super().__init__(unique_id, model)
		self.istrap = istrap