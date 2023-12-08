# IMPORTS
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from pygame import mixer
import numpy as np

import sys
from termcolor import colored, cprint
# Termcolor guide: https://pypi.org/project/termcolor/

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# INITIALIZATIONS 
default_mixer_volume = 0.70

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASSES

class audio_object:
	""" the base audio object class """
	
	def __init__(self, param_1, param_2, param_3, sound_library):				
		self.initialize() # reset the audio object (socket)

		# set all the sound parameters for the object (value for volume, amplitude of pitch change, etc)
		# Each parameter ranges on an INTEGER value from 0 to 4 value --> 0 is lowest, 4 is highest
		self.param_1 = param_1 	# Speed of audio loop (BPM)		 --> (100 BPM   //  140 BPM  //  180 BPM)
		self.param_2 = param_2 	# Number of beeps per loop (BPL) --> (1 BPL	 //  2 BPM	 //  4 BPL) 
		self.param_3 = param_3 	# Amplitude of Pitch Bend  		 --> (downward  //  neutral  //  upward)

		# Get the mp3 path based on parameter inputs
		param_1_str = str(self.param_1)
		param_2_str = str(self.param_2)
		param_3_str = str(self.param_3)

		self.confidence_level = 0.5 

		# Setup the elements to create the sound librabry global path	
		self.sound_library = sound_library # "lib3" = library 3
		
		audio_library_path = "audio/sonif_" + sound_library + "/looped/"
		# audio_library_path = "/home/liamroy/Documents/PHD/repos/RL_audio/audio/sonif_" + sound_library + "/looped/"
		audio_extension = ".mp3"

		# Define the sound librabry global path
		self.mp3_path = audio_library_path + param_1_str + "_" + param_2_str + "_" + param_3_str + audio_extension
		# print(f"returned mp3_path from Get_mp3_Path is: {self.mp3_path}")

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def initialize(self, load_file=None):
		""" Initialize the counter n to either 0 or 1 - dependant. """
		
		# n = the number of times this socket has been tried
		if load_file:
			self.n = 1  # The algirthm follows the Q-table if we initialize with a known action-value dataset
						# Setting each to 1 at the beginning means we will not receive "inf" for each uncertainty, 
						# and only have to try actions with initliazed high value
		else:
			self.n = 0	  

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def probe(self, all_states, mixer_volume=default_mixer_volume):
		""" play the mp3 file then return a reward based on the answer provided by the user. """
		
		#Instantiate mixer
		mixer.init()

		#Load audio file
		mixer.music.load(self.mp3_path)

		#Set preferred volume
		mixer.music.set_volume(mixer_volume)

		#Play the music
		mixer.music.play()

		state_probe_complete = False
		confid_probe_complete = False

		# Probe user on what state they think the robot is in, and how confident they are on scale 0-10
		while True:
			if state_probe_complete == False:
				while True:
					try:
						print("------------------------------------------------------------------------")
						print("------------------------------------------------------------------------\n")
						print("Robot sound is playing....\n")
						cprint(f"What state is the robot in: \n", "black", "on_green", attrs=["bold"])
						print(f"[S]: {all_states[0]} \n[A]: {all_states[1]} \n[P]: {all_states[2]} \n[N]: {all_states[3]} \n\n")
						print("To replay the sound: leave the input empty and hit 'enter'...")
						cprint(f"Select a state by entering its first letter [S - A - P - N]: ", "black", "on_green", attrs=["bold"])
						probed_state_str = str(input())
						print()

					except ValueError:
						mixer.music.rewind() # Restart the sound if user enters an invalid entry so they can re-listen
						mixer.music.play()

						cprint(f"\nPlease enter the first letter of the state...\n", "black", "on_red", attrs=["bold"])
						continue

					if probed_state_str == "S" or probed_state_str == "s":
						probed_state_index = 0
						print(f'You entered: {probed_state_str}')
						cprint(f"{all_states[probed_state_index]}\n", "black", "on_yellow", attrs=["bold"])
						state_probe_complete = True
						break
						
					elif probed_state_str == "A" or probed_state_str == "a":
						probed_state_index = 1
						print(f'You entered: {probed_state_str}')
						cprint(f"{all_states[probed_state_index]}\n", "black", "on_yellow", attrs=["bold"])
						state_probe_complete = True
						break
						
					elif probed_state_str == "P" or probed_state_str == "p":
						probed_state_index = 2
						print(f'You entered: {probed_state_str}')
						cprint(f"{all_states[probed_state_index]}\n", "black", "on_yellow", attrs=["bold"])
						state_probe_complete = True
						break
						
					elif probed_state_str == "N" or probed_state_str == "n":
						probed_state_index = 3
						print(f'You entered: {probed_state_str}')
						cprint(f"{all_states[probed_state_index]}\n", "black", "on_yellow", attrs=["bold"])
						state_probe_complete = True
						probed_confidence_int = 0
						confid_probe_complete = True
						break
					else:
						mixer.music.rewind()	# Restart the sound if user enters an invalid entry so they can re-listen
						mixer.music.play()
						cprint(f"\nPlease enter the first letter of the state...\n", "black", "on_red", attrs=["bold"])

						
			if confid_probe_complete == False:
				while True:
					try:
						print("To replay the sound: Leave the input empty and hit 'enter'...")
						cprint(f"Score your confidence in this response from [0 to 10]\n or \nType 'back' to change your response: ", "black", "on_green", attrs=["bold"])
						probed_confidence = input()
						probed_confidence_int = int(probed_confidence)
						
					except ValueError:
						if probed_confidence == "back":
							state_probe_complete = False
							confid_probe_complete = False
							break
						
						else:
							mixer.music.rewind() # Restart the sound if user enters an invalid entry so they can re-listen
							mixer.music.play()
							cprint(f"\nPlease enter a valid integer in the range 0 to 10 or type 'back' to go back...\n", "black", "on_red", attrs=["bold"])
							continue

					if probed_confidence_int >= 0 and probed_confidence_int <= 10:
						print(f'\nYou entered: {probed_confidence_int}\n')
						confid_probe_complete = True
						break

					else:
						mixer.music.rewind() # Restart the sound if user enters an invalid entry so they can re-listen
						mixer.music.play()
						cprint(f"\nPlease enter a valid integer in the range 0 to 10 or type 'back' to go back...\n", "black", "on_red", attrs=["bold"])

			if state_probe_complete == True and confid_probe_complete == True:
				break				
						
		# User has now responded --> stop the sound playing
		mixer.music.stop()

		return probed_state_index, probed_confidence_int


	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


	def play_sound(self, mixer_volume=default_mixer_volume):
		""" play the sound based on arguments. """	 
	
		print(f"\nPlaying MP3 Path: {self.mp3_path}\n")
	
 		#Instantiate mixer
		mixer.init()

		#Load audio file
		mixer.music.load(self.mp3_path)

		#Set preferred volume
		mixer.music.set_volume(mixer_volume)

		#Play the music
		mixer.music.play()

		cprint(f"Robot sound playing for:\nParam 1: {self.param_1} \nParam 2: {self.param_2} \nParam 3: {self.param_3}\n", "black", "on_green", attrs=["bold"])

	
	
  	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


	  
	
	def update(self):
		""" update the number of times this action has been selected. """	 
	
		self.n += 1

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	

	def uncertainty(self, time_step): 
		""" calculate the uncertainty based on the timestep and number of times this action has been selected. """
		
		if self.n == 0: return float('inf')	  # No longer need this but its a good failsafe 				 
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



