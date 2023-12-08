# IMPORTS
import numpy as np

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# INITIALIZATIONS 

param_disc = 3 # number of discretized regions for each param --> i.e. if equals 5 then (0, 1, 2, 3, 4)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASSES

class robot_state:
	""" the base state object class """
	
	def __init__(self, state_idx, description, param_disc, load_file):                

		self.state_idx = state_idx
		self.description = description

		if load_file: # Load an existing Q-table
			self.action_value_lookup = np.load("arrays/" + load_file + "_st" + str(self.state_idx) + ".npy")
		
		else: # Initialize all Q-Values to max reward (optimism in the face of uncertainty)
			self.action_value_lookup = np.ones((param_disc, param_disc, param_disc)) * 10.0 # Arbitrary initialization


	def action_selection(self):
		max_action_index = np.unravel_index(randargmax(self.action_value_lookup), self.action_value_lookup.shape)
		param_1_idx = max_action_index[0]
		param_2_idx = max_action_index[1]
		param_3_idx = max_action_index[2]

		return param_1_idx, param_2_idx, param_3_idx


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# STAND-ALONE FUNCTIONS

def randargmax(b,**kw):
	""" a random tie-breaking argmax"""
	return np.argmax(np.random.random(b.shape) * (b==b.max()), **kw)