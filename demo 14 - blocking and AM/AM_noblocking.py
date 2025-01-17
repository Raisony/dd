# AM_noblocking.py
# Play a wave file with amplitude modulation. 
# Assumes wave file is mono.
# This implementation reads and plays one frame (sample) at a time (no blocking)
"""
Read a signal from a wave file, do amplitude modulation, play to output
Original: pyrecplay_modulation.py by Gerald Schuller, Octtober 2013
Modified to read a wave file - Ivan Selesnick, September 2015
"""

# f0 = 0      # Normal audio
f0 = 400    # 'Duck' audio

import pyaudio
import struct
import wave
import math

# Open wave file (mono)
input_wavefile = 'author.wav'
# input_wavefile = 'sin01_mono.wav'
# input_wavefile = 'sin01_stereo.wav'

wf          = wave.open( input_wavefile, 'rb')
RATE        = wf.getframerate()
WIDTH       = wf.getsampwidth()
LEN         = wf.getnframes() 
CHANNELS    = wf.getnchannels() 

print('The sampling rate is {0:d} samples per second'.format(RATE))
print('Each sample is {0:d} bytes'.format(WIDTH))
print('The signal is {0:d} samples long'.format(LEN))
print('The signal has {0:d} channel(s)'.format(CHANNELS))

# Open audio stream
p = pyaudio.PyAudio()
stream = p.open(
    format      = p.get_format_from_width(WIDTH),
    channels    = CHANNELS,
    rate        = RATE,
    input       = False,
    output      = True)

print('* Playing...')
print(RATE)
# Loop through wave file 
for n in range(0, LEN):
    # Get sample from wave file
    binary_data = wf.readframes(1)
    # Convert binary data to tuple of numbers
    input_tuple = struct.unpack('h', binary_data)
        # (h: two bytes per sample (WIDTH = 2))
    # Use first value (of two if stereo)
    input_value = input_tuple[0]
    # Amplitude modulation  (f0 Hz cosine)
    output_value = input_value * math.cos(2.0*math.pi*f0*n/RATE)
    # Convert value to binary data
    binary_data = struct.pack('h', int(output_value))
    # Write binary data to audio output stream
    stream.write(binary_data)
print('* Finished *')
stream.stop_stream()
stream.close()
p.terminate()
# Close wavefile
wf.close()
