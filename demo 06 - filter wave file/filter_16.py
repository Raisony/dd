# filter_16.py
# 
# Implement the second-order recursive difference equation
# y(n) = x(n) - a1 y(n-1) - a2 y(n-2)
# 
# 16 bit/sample

from math import cos, pi 
import pyaudio
import struct

def clip16( x ):
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x
    return (x)

# Fs : Sampling frequency (samples/second)
Fs = 8000
# Also try other values of 'Fs'. What happens? Why?
# Fs = 16000
# Fs = 32000
# Fs = 5000

T = 1       # T : Duration of audio to play (seconds)
N = T*Fs    # N : Number of samples to play

# Difference equation coefficients
a1 = -1.9
a2 = 0.998

# Initialization
y1 = 0.0
y2 = 0.0
gain = 100000.0
# Also try other values of 'gain'. What is the effect?
# gain = 1000.0

# Create an audio object and open an audio stream for output
p = pyaudio.PyAudio()
stream = p.open(format      = pyaudio.paInt16,  
                channels    = 1, 
                rate        = Fs,
                input       = False, 
                output      = True)

# paInt16 is 16 bits/sample

# Run difference equation
for n in range(0, N):

    # Use impulse as input signal
    if n == 0:
        x0 = 1.0
    else:
        x0 = 0.0

    # Difference equation
    y0 = x0 - a1 * y1 - a2 * y2

    # Delays
    y2 = y1
    y1 = y0

    # Output
    a=gain * y0
    if a > 32767:
        a = 32767
    elif a < -32768:
        a = -32768
    else:
        pass

    output_value = a
    output_string = struct.pack('h', int(output_value))   # 'h' for 16 bits
    stream.write(output_string)

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
