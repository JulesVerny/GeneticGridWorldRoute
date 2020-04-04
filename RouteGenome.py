#  An Entity Class for the GA Gridworld Genome
#  Route + Fitness
import numpy as np 
# =========================================================================

class Genome:
	def __init__(self,ThePath,TheFitness):
		self.Path = ThePath
		self.Fitness = TheFitness

