# IMPORTS
import numpy as np
import audio_control
import ucb1_algorithm as ucb1
import time
import argparse

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ARGUMENTS 

argParser = argparse.ArgumentParser()

# Enter any valid integer value
argParser.add_argument("-b", "--budg", required=False, help="select the budget value (dtype=int)")

# Enter a valid parameter discritization integer (must match sound library size)
argParser.add_argument("-d", "--disc", required=False, help="select discritization size (dtype=int)")

# Enter true if you would like to see hidden print log, including Q-tables
argParser.add_argument("-p", "--prnt", required=False, help="show hidden print log (dtype=bool)")

# To load and save, simply enter in the base filename such as "lastsave" or "set_A", system takes care of rest
argParser.add_argument("-s", "--save", required=False, help="filename to save Q-table on exit (dtype=str)") 
argParser.add_argument("-l", "--load", required=False, help="load Q-table from filename (dtype=str)") 		


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PARSER 

args = argParser.parse_args()

# number of total iterations 
if args.budg:
	budget = int(args.budg)
else:
	budget = 50			

if args.disc:
	param_disc = int(args.disc)
else:
	param_disc = 3 

# whether or not to include print statements for hidden values
printer = args.prnt

# filename to save Q-table on exit
if args.save:
	save_file = args.save
else:
	save_file = "lastsave"	

# filename to save Q-table on exit
if args.load:
	load_file = args.load
else:
	load_file = None # "last_array.npy"





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# INITIALIZATIONS 

state_descriptions = ["Progressing \t- robot is working and doesn't need help", "Successful \t- robot has completed it's task", "Stuck      \t- robot needs your help", "None of the above"]
num_of_states = len(state_descriptions) - 1 # Adding a minus 1 since the last state in "state_descriptions" is "none of the above"


# Create an array of size (N x N x N) where N = number of discretized regions
# number of discretized regions for each param --> i.e. if equals 3 then (0, 1, 2)
# ** must align with the discretization for selected sound library
sound_obj_array = np.ndarray((ucb1.param_disc, ucb1.param_disc, ucb1.param_disc),dtype=np.object)


for param_1_range in range(ucb1.param_disc):
	for param_2_range in range(ucb1.param_disc):
		for param_3_range in range(ucb1.param_disc):
			sound_obj_array[param_1_range, param_2_range, param_3_range] = audio_control.audio_object(param_1_range, param_2_range, param_3_range, budget)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN

if __name__ == "__main__":

	# Initialize time_step to zero
	time_step = 0

	# Initialize to center of mapping
	param_1_idx = 1 
	param_2_idx = 1
	param_3_idx = 1

	states_array = np.ndarray(num_of_states, dtype=np.object)

	for state_idx in range(num_of_states):
		states_array[state_idx] = ucb1.robot_state(state_idx, state_descriptions[state_idx], param_disc, load_file)

	for i in range(0, budget):

		current_state_index = np.random.randint(0, 3) 		# Current actual state of the robot - change this to fluctuate during study

		if time_step == 0:
			param_1_idx = 1 
			param_2_idx = 1
			param_3_idx = 1
		else:
		# Select new params
			param_1_idx, param_2_idx, param_3_idx = states_array[current_state_index].action_selection()

		time_step += 1
		
		print("\n----------------------------------------------------------------")
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		print("----------------------------------------------------------------\n")

		if printer:
			print("(Hidden):")
			print(f"Current actual state of robot: {current_state_index}\n")
			print(f"New Param INDICES (not direct values): \nP1: {param_1_idx} (Beats per Minute - BPM) \nP2: {param_2_idx} (Beeps per Loop - BPL) \nP3: {param_3_idx} (Amplitude of Pitch Change)\n")


		# Play the desired mp3 file, probe user based on sound, then update the Q-Value look-up table...
		
		# Probe user for perceived state & confidence in their response
		probed_state_index, probed_confidence = sound_obj_array[param_1_idx, param_2_idx, param_3_idx].probe(state_descriptions)

		# Update N for audio obj
		sound_obj_array[param_1_idx, param_2_idx, param_3_idx].update()
		
		# Calculate uncertainty signal (U_t) based on N and time_step
		uncertainty_signal = sound_obj_array[param_1_idx, param_2_idx, param_3_idx].uncertainty(time_step)

		# For each state, calculate the respective reward signal (R)
		for state_idx in range(num_of_states):
			
			if probed_state_index == len(state_descriptions) - 1:
				reward_signal = 0.0

			else:
				if probed_state_index == state_idx:
					correct_multiplier = 1.0
				elif probed_state_index != state_idx:
					correct_multiplier = -1.0

				# This is the reward signal R
				reward_signal = correct_multiplier * probed_confidence

			# Calculate new Q_t = {[(1 - 1/n) * Q_t-1] + [(1/n) * R]} + U_t   ~  UCB1 algorithm update equation
			# Takes the mean of previously observed reward and new reward, adding on an uncertainty term
			Q_value = ((1 - 1.0/sound_obj_array[param_1_idx, param_2_idx, param_3_idx].n) * states_array[state_idx].action_value_lookup[param_1_idx, param_2_idx, param_3_idx] + (1.0/sound_obj_array[param_1_idx, param_2_idx, param_3_idx].n) * reward_signal) + uncertainty_signal

			# Update value in lookup table for state S with new Q_t
			# Added an np.clip so that the mix/max Q-Value in the table cant exceed -10 to +10
			states_array[state_idx].action_value_lookup[param_1_idx, param_2_idx, param_3_idx] = np.clip(Q_value, -10, 10)

			if printer:
				print("\n\n----------------------------------------------------------------\n")
				print("(Hidden):")
				print(f"Uncertainty_signal (U):\t {uncertainty_signal}")
				print(f"Reward_signal (R):\t {reward_signal}")
				print(f"New action value (Q):\t {Q_value}")
				print(f"Q-table after update for state {state_idx}:\n")
				print(states_array[state_idx].action_value_lookup)
	 
			np.save("arrays/" + save_file + "_st" + str(state_idx) + ".npy", states_array[state_idx].action_value_lookup)

			time.sleep(1) # Put here to make UI a bit nicer 

			

			# x = np.arange(10)
			# print("x", x)

			# b = np.load(load_file)
			# print("b", b)




