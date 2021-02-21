from mesa import Agent
from mesa.datacollection import DataCollector
import random
import numpy as np
from Target import Target

class Trap(Target):
	def __init__(self, unique_id, model):
		super().__init__(unique_id, model, True)
		self.midgestrapped = 0

	def trapmidge(self):
		self.midgestrapped += 1

	def step(self):
		self.model.grid.place_agent(self, self.pos)
		print("On day " + str(self.model.day) + ", there were " + str(self.midgestrapped) + " midges trapped")
		pass