# To play .wav file: 
# >> aplay sine_wave.wav


import wave
import numpy as np

# Set the parameters for the wave file
num_channels = 1
sample_width = 2
sample_rate = 44100
num_samples = 44100

# Create a sine wave with a frequency of 440 Hz
frequency = 440
sine_wave = np.array([np.sin(2*np.pi*frequency*x/sample_rate) for x in range(num_samples)])

# Scale the sine wave to fit within the 16-bit range
sine_wave *= 32767 / np.max(np.abs(sine_wave))
sine_wave = sine_wave.astype(np.int16)

# Create a wave file and write the sine wave to it
with wave.open('sine_wave.wav', 'w') as wave_file:
    wave_file.setparams((num_channels, sample_width, sample_rate, num_samples, "NONE", "not compressed"))
    wave_file.writeframes(sine_wave.tostring())
