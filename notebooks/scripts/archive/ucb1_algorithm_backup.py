# IMPORTS
import numpy as np
import random
import time

import sys
from termcolor import colored, cprint
# Termcolor guide: https://pypi.org/project/termcolor/

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# INITIALIZATIONS 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASSES

class robot_state:
	""" the base state object class """
	
	def __init__(self, state_idx, description, param_disc, load_file, user_ID_str):				

		self.state_idx = state_idx
		self.description = description

		if load_file: # Load an existing Q-table
			self.action_value_lookup = np.load("user_data/user_" + user_ID_str + "/arrays/" + load_file + "_st" + str(self.state_idx) + ".npy")
			# print("\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			# print(f"Initialized Q-table file: {'user_data/user_' + user_ID_str + '/arrays/' + load_file + '_st' + str(self.state_idx) + '.npy'}\n")
			
		else: # Initialize all Q-Values to max reward (optimism in the face of uncertainty)
			self.action_value_lookup = np.ones((param_disc, param_disc, param_disc)) * 10.0 # Arbitrary initialization
			# print("\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			# print(f"Initialized action value Q-table as flat 10.0\n")


	def action_selection(self, uncertainty_array, printer=None):
		''' selects an action based on Q-values and uncertainty. '''
		
		action_value_with_uncertainty = self.action_value_lookup + uncertainty_array
		
		if printer:
			print("\naction value:\n", self.action_value_lookup)
			print("\nuncertainty:\n", uncertainty_array)
			print("\naction value with uncertainty\n", action_value_with_uncertainty)
			print()

		max_action_index = np.unravel_index(randargmax(action_value_with_uncertainty + uncertainty_array), self.action_value_lookup.shape)
		
		param_1_idx = max_action_index[0]
		param_2_idx = max_action_index[1]
		param_3_idx = max_action_index[2]

		return param_1_idx, param_2_idx, param_3_idx


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# STAND-ALONE FUNCTIONS

def randargmax(b,**kw):
	""" a random tie-breaking argmax """
	return np.argmax(np.random.random(b.shape) * (b==b.max()), **kw)



def ucb1_algor(num_of_states, state_descriptions, param_disc, sound_obj_array, current_user_ID_str, sect_str, load_file=None, 
			   budget=50, delta_Q_thresh=2.0, conv_thresh=3, printer=True, mixer_volume=0.70):
	""" runs the UCB1 algorithm for budget or until convergence. """ 

	# budget		 = Max number of total iterations 
	# delta_Q_thresh = Change in Q value of a given state action-value 
	# conv_thresh	= How many times a state is guessed correctly in a row before that state converges
	# printer		= Either set to True or None (prints hidden statements for debug)
	
	# Initializations:
	time_step = 0
	save_file = current_user_ID_str + sect_str	# Filename to save Q-table on exit
	
	
	# Create the uncertainty array based on size of sound object array
	uncertainty_array = np.zeros_like(sound_obj_array)
	# print(f"\nuncertainty_array at init: \n{uncertainty_array}")
	
	
	# Create the N-values array based on size of sound object array (this array is only for debugging purposes)
	N_array = np.zeros_like(sound_obj_array)
	# print(f"\N_array at init: \n{N_array}")


	# Initialize convergece param markers to None
	prev_st0_param_1_idx, prev_st0_param_2_idx, prev_st0_param_3_idx = None, None, None
	prev_st1_param_1_idx, prev_st1_param_2_idx, prev_st1_param_3_idx = None, None, None
	prev_st2_param_1_idx, prev_st2_param_2_idx, prev_st2_param_3_idx = None, None, None


	# Set initial convergence markers to zero
	in_a_row_st0 = 0
	in_a_row_st1 = 0
	in_a_row_st2 = 0


	# Re-Initialize states array. Each state is initialized with a Q-table based on load_file
	states_array = np.ndarray(num_of_states, dtype=object)
	for state_idx in range(num_of_states):
		states_array[state_idx] = robot_state(state_idx=state_idx, description=state_descriptions[state_idx], param_disc=param_disc, 
												   load_file=load_file, user_ID_str=current_user_ID_str)


	# Creates the initial set of {0, 1, 2) which the for loop will sample from to choose a state index
	state_idx_set = set()
	for state_idx in range(num_of_states):
		state_idx_set.add(state_idx)

		
	# Initialize the n-values for each sounnd object to 1 (using 1 instead of 0 so the algirthm follows a Q-table if we initialize with a known action-value dataset using load_file)
	for param_1_range in range(param_disc):
		for param_2_range in range(param_disc):
			for param_3_range in range(param_disc):
				sound_obj_array[param_1_range, param_2_range, param_3_range].initialize(load_file)
				
		  
	# Run a for loop which plays a sound, gets a response, then updates. Itterations is the budget
	for i in range(0, budget):

		
		if printer:
			cprint("\n\n\n--------------------------------------------------------------", "light_yellow", attrs=["bold"])
			cprint("--------------------------------------------------------------\n", "light_yellow", attrs=["bold"])
			cprint(f"STARTING NEW LOOP", "black", "on_yellow", attrs=["bold"])
			cprint("--------------------------------------------------------------", "light_yellow", attrs=["bold"])
			cprint("--------------------------------------------------------------\n\n\n", "light_yellow", attrs=["bold"])
		
		
		# Incriment our timestep
		time_step += 1
		time_step_str = f"{time_step:02}"
		
		
		# Calculate uncertainty signal (U_t) for each actiion based on number of times explored (N) and time_step
		for param_1_range in range(param_disc):
			for param_2_range in range(param_disc):
				for param_3_range in range(param_disc):
					uncertainty_array[param_1_range, param_2_range, param_3_range] = sound_obj_array[param_1_range, param_2_range, param_3_range].uncertainty(time_step)
					N_array[param_1_range, param_2_range, param_3_range] = sound_obj_array[param_1_range, param_2_range, param_3_range].n
		
		
		# Randomly select a state as our "true state" from the states which we have not yet converged
		current_state_index = random.choice(tuple(state_idx_set)) 		
		
		if printer:
			print("\n(Hidden loop layer):")
			print(f"Time Step: {time_step_str}")
			print("state_idx_set:", state_idx_set)
			print("current_state_index:", current_state_index)
			print(f"\nN_array in loop at time {time_step}: \n{N_array}")

		# Select new action based on our algorithm - if first timestep, use 1,1,1
		if time_step == 1 and load_file == None:
			param_1_idx = 1 
			param_2_idx = 1
			param_3_idx = 1
		else:
			param_1_idx, param_2_idx, param_3_idx = states_array[current_state_index].action_selection(uncertainty_array, printer)

		if printer:

			print(f"\nNew Param INDICES (not direct values): \nP1: {param_1_idx} (Beats per Minute - BPM) \nP2: {param_2_idx} (Beeps per Loop - BPL) \nP3: {param_3_idx} (Amplitude of Pitch Change)\n")

		   
		# Play the desired mp3 file & probe user for perceived state & confidence in their response
		probed_state_index, probed_confidence = sound_obj_array[param_1_idx, param_2_idx, param_3_idx].probe(state_descriptions)


		# Update N for selected audio obj (action)
		sound_obj_array[param_1_idx, param_2_idx, param_3_idx].update()
		
		
		# For each state, calculate the respective reward signal (R)
		for state_idx in range(num_of_states):

			
			# If the user enters [3] "Unsure", reward signal is zero
			if probed_state_index == len(state_descriptions) - 1:
				reward_signal = 0.0

			# Otherwise we calculate reward based on: correct * confidence
			else:
				if probed_state_index == state_idx:
					correct_multiplier = 1.0
				elif probed_state_index != state_idx:
					correct_multiplier = -1.0

				# This is the reward signal R
				reward_signal = correct_multiplier * probed_confidence

				
			# Calculate new Q_t = {[(1 - 1/n) * Q_t-1] + [(1/n) * R]} + U_t   ~  UCB1 algorithm update equation
			# Takes the mean of previously observed reward and new reward
			Q_value = ((1 - 1.0/sound_obj_array[param_1_idx, param_2_idx, param_3_idx].n) * states_array[state_idx].action_value_lookup[param_1_idx, param_2_idx, param_3_idx] 
					   + (1.0/sound_obj_array[param_1_idx, param_2_idx, param_3_idx].n) * reward_signal)


			# Calculate delta_Q which we will use as a convergence marker 
			delta_Q = abs(Q_value - states_array[state_idx].action_value_lookup[param_1_idx, param_2_idx, param_3_idx])


			# Update value in lookup table for state S with new Q_t 
			# Added an np.clip so that the mix/max Q-Value in the table cant exceed -10 to +10
			states_array[state_idx].action_value_lookup[param_1_idx, param_2_idx, param_3_idx] = np.clip(Q_value, -10, 10)


			# A few print statements for terminal
			if printer:
				print("\n\n----------------------------------------------------------------\n")
				print(f"(Hidden state {state_idx} layer):")
				print(f"Reward_signal (R):\t {reward_signal}")
				print(f"N value for state {state_idx} is {sound_obj_array[param_1_idx, param_2_idx, param_3_idx].n}")
				print(f"Delta_Q for state {state_idx} is: {delta_Q}")
				print(f"New action value (Q):\t {Q_value}")
				print(f"Q-table after update for state {state_idx}:\n")
				print(states_array[state_idx].action_value_lookup)
				print()

			# Save the action-value array for that state at that timestep	
			np.save("user_data/user_" + current_user_ID_str + "/arrays/" + save_file + "_step" + time_step_str + "_st" + str(state_idx) + ".npy", states_array[state_idx].action_value_lookup)


			
		# Now check to see if there is convergence for each state..

		#If probing state 0, did they get it correct?
		if current_state_index == 0:
			if probed_state_index == current_state_index and prev_st0_param_1_idx == param_1_idx and prev_st0_param_2_idx == param_2_idx and prev_st0_param_3_idx == param_3_idx:
				in_a_row_st0 += 1
				if printer:
					print(f"in_a_row_st0 +1, total {in_a_row_st0} becase correct and same")
			elif probed_state_index == current_state_index and delta_Q <= delta_Q_thresh: 
				in_a_row_st1 += 1
				if printer:
					print(f"in_a_row_st0 +1, total {in_a_row_st0} becase correct and under delta Q thresh")
			else:
				in_a_row_st0 = 0
				if printer:
					print(f"in_a_row_st0 back to zero")

			prev_st0_param_1_idx, prev_st0_param_2_idx, prev_st0_param_3_idx = param_1_idx, param_2_idx, param_3_idx


		#If probing state 1, did they get it correct?
		if current_state_index == 1:
			if probed_state_index == current_state_index and prev_st1_param_1_idx == param_1_idx and prev_st1_param_2_idx == param_2_idx and prev_st1_param_3_idx == param_3_idx:
				in_a_row_st1 += 1
				if printer:
					print(f"in_a_row_st1 +1, total {in_a_row_st1} becase correct and same")
			elif probed_state_index == current_state_index and delta_Q <= delta_Q_thresh: 
				in_a_row_st1 += 1
				if printer:
					print(f"in_a_row_st1 +1, total {in_a_row_st1} becase correct and under delta Q thresh")
			else:
				in_a_row_st1 = 0
				if printer:
					print(f"in_a_row_st1 back to zero")

			prev_st1_param_1_idx, prev_st1_param_2_idx, prev_st1_param_3_idx = param_1_idx, param_2_idx, param_3_idx


		#If probing state 2, did they get it correct?
		if current_state_index == 2:
			if probed_state_index == current_state_index and prev_st2_param_1_idx == param_1_idx and prev_st2_param_2_idx == param_2_idx and prev_st2_param_3_idx == param_3_idx:
				in_a_row_st2 += 1
				if printer:
					print(f"in_a_row_st2 +1, total {in_a_row_st2} becase correct and same")
			elif probed_state_index == current_state_index and delta_Q <= delta_Q_thresh: 
				in_a_row_st1 += 1
				if printer:
					print(f"in_a_row_st2 +1, total {in_a_row_st2} becase correct and under delta Q thresh")			
			else:
				in_a_row_st2 = 0
				if printer:
					print(f"in_a_row_st2 back to zero")

			prev_st2_param_1_idx, prev_st2_param_2_idx, prev_st2_param_3_idx = param_1_idx, param_2_idx, param_3_idx

			
		# Check to see if we've hit the convergence threshold on any of our states. If so, remove that state index from unconverged state index set
		if in_a_row_st0 >= conv_thresh:
			state_idx_set.discard(0)
			if printer:
				cprint(f"State 0 Converged", "black", "on_yellow", attrs=["bold"])

		if in_a_row_st1 >= conv_thresh:
			state_idx_set.discard(1)
			if printer:
				cprint(f"State 1 Converged", "black", "on_yellow", attrs=["bold"])

		if in_a_row_st2 >= conv_thresh:
			state_idx_set.discard(2)
			if printer:
				cprint(f"State 2 Converged", "black", "on_yellow", attrs=["bold"])

				
		# If we've hit the convergence threshold on all our states --> end the algorithm early
		if in_a_row_st0 >= conv_thresh and in_a_row_st1 >= conv_thresh and in_a_row_st2 >= conv_thresh:
			if printer:
				print("running 'break' on converge\n")
			break

			
	if printer:
		print("in_a_row_st0", in_a_row_st0)
		print("in_a_row_st1", in_a_row_st1)
		print("in_a_row_st2", in_a_row_st2)
		print("final time_step:", time_step)

		
	# Coloured print statement to direct user to next cell
	cprint("\n\n\n------------------------------------------------------------------------", "light_yellow", attrs=["bold"])
	cprint("------------------------------------------------------------------------\n", "light_yellow", attrs=["bold"])
	cprint(f"Great job! The system terminated successfully at itter: {time_step}.", "black", "on_yellow", attrs=["bold"])
	cprint(f"Click on the next cell below and hit 'shift + enter' to continue\n", "black", "on_yellow", attrs=["bold"])
	cprint("------------------------------------------------------------------------", "light_yellow", attrs=["bold"])
	cprint("------------------------------------------------------------------------\n\n\n", "light_yellow", attrs=["bold"])
	
	
	# Return the timestep string - use this for loading the last known Q-table for each state
	return time_step_str