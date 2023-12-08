# IMPORTS
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from pygame import mixer
import numpy as np

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# INITIALIZATIONS 
default_mixer_volume = 0.75
sound_library = "lib3"

audio_library_path = "/home/liamroy/Documents/PHD/repos/RL_audio/audio/sonif_" + sound_library + "/looped/"
audio_extension = ".mp3"


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASSES

class audio_object:
	""" the base audio object class """
	
	def __init__(self, param_1, param_2, param_3, budget):                
		self.initialize() # reset the audio object (socket)

		# set all the sound parameters for the object (value for volume, amplitude of pitch change, etc)
		# Each parameter ranges on an INTEGER value from 0 to 4 value --> 0 is lowest, 4 is highest
		self.param_1 = param_1 	# Speed of audio loop (BPM)		 --> (120 BPM   //  150 BPM  //  180 BPM)
		self.param_2 = param_2 	# Number of beeps per loop (BPL) --> (1 BPL     //  2 BPM    //  4 BPL) 
		self.param_3 = param_3 	# Amplitude of Pitch Bend  		 --> (downward  //  neutral  //  upward)

		# Get the mp3 path based on parameter inputs
		param_1_str = str(self.param_1)
		param_2_str = str(self.param_2)
		param_3_str = str(self.param_3)

		self.confidence_level = 0.5 # * np.sqrt(np.log(budget)) ~ set arbitrarily for now - tune later (between 0.2 & 2)
									# could maybe create self.time_step & slowly increment down

		self.mp3_path = audio_library_path + sound_library + "_" + param_1_str + "_" + param_2_str + "_" + param_3_str + audio_extension
		# print(f"returned mp3_path from Get_mp3_Path is: {self.mp3_path}")

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def initialize(self):
		""" Initialize both counter n and estimated reward Q. """
		self.n = 0   # the number of times this socket has been tried

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def probe(self, all_states, mixer_volume=default_mixer_volume):
		""" play the mp3 file then return a reward based on the answer provided by the user. """
		
		#Instantiate mixer
		mixer.init()

		#Load audio file
		mixer.music.load(self.mp3_path)
		print("robot sound is playing....")

		#Set preferred volume
		mixer.music.set_volume(mixer_volume)

		#Play the music
		mixer.music.play()


		# Probe user on what state they think the robot is in, and how confident they are on scale 0-10
		while True:
			try:
				print()
				probed_state_index = int(input(f"What state is the robot in: \n[0]: {all_states[0]} \n[1]: {all_states[1]} \n[2]: {all_states[2]} \n[3]: {all_states[3]} \n\nHit 'enter' to replay the sound...\nSelect a state between [0 to 3]:\n"))
				print()

			except ValueError:
				mixer.music.rewind() # Restart the sound if user enters an invalid entry so they can re-listen
				mixer.music.play()
				print()
				print(f"Please enter the numerical index of the state shown below.")
				print()
				continue

			if probed_state_index == 0:
				print(f'You entered: {probed_state_index} --> state: {all_states[probed_state_index]}\n')
				break

			elif probed_state_index == 1:
				print(f'You entered: {probed_state_index} --> state: {all_states[probed_state_index]}\n')
				break
			
			elif probed_state_index == 2:
				print(f'You entered: {probed_state_index} --> state: {all_states[probed_state_index]}\n')
				break

			elif probed_state_index == 3:
				print(f'You entered: {probed_state_index} --> state: {all_states[probed_state_index]}\n')
				break

			elif probed_state_index == 4:
				print(f'Replaying sound...\n')
				print()

			else:
				print()
				print(f"Please enter the numerical index of the state shown below.")
				print()


		while True:
			try:
				probed_confidence = int(input("Hit 'enter' to replay the sound... \nScore your confidence in this response from [0 to 10]: "))
			except ValueError:
				print()
				print("Please enter a valid integer 0 to 10")
				print()
				mixer.music.rewind() # Restart the sound if user enters an invalid entry so they can re-listen
				mixer.music.play()

				continue
			if probed_confidence >= 0 and probed_confidence <= 10:
				print(f'You entered: {probed_confidence}\n')
				break

			else:
				print()
				print('The integer must be in the range 0 to 10')
				print()

		# User has now responded --> stop the sound playing
		mixer.music.stop()

		return probed_state_index, probed_confidence


	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


	def update(self):
		""" update this Q-Value for this sound after it has returned reward value 'R' """     
	
		# increment the number of times this socket has been tried
		self.n += 1

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	

	def uncertainty(self, time_step): 
		""" calculate the uncertainty in the estimate of this audio object's mean """
		if self.n == 0: return float('inf')                         
		return self.confidence_level * (np.sqrt(np.log(time_step) / self.n))   


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# STAND-ALONE FUNCTIONS


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CODE ARCHIVE:


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# RESOURCES:

# PyGame Installation:		https://www.pygame.org/wiki/GettingStarted 
# PyGame Documentation:		https://www.pygame.org/docs/ref/music.html  
# Play Sound w/ PyGame:		https://www.educative.io/answers/how-to-play-an-audio-file-in-pygame



