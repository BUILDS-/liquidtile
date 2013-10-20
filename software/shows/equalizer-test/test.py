import pyaudio
import wave
import numpy
import struct
import sys
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 100
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
		input_device_index=0,
                frames_per_buffer=CHUNK)

print("* recording")

# http://stackoverflow.com/questions/4160175/detect-tap-with-pyaudio-from-live-mic
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #Blocking
    try:
        data = stream.read(CHUNK)
	count = len(data)/2
	format = "%dh"%(count)
	shorts = struct.unpack( format, data )
	# normalize shorts
	SHORT_NORMALIZE = (1.0/32768.0)
	shorts = [i*SHORT_NORMALIZE for i in shorts]
	fft = abs(numpy.fft.fft(shorts))
	for i in range(0,CHUNK/2, 16):
		print ''.join(["|" for i in range(0,int(fft[i]))])
	print chr(27) + "[2J"
    except:
	print "dropped packet"

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

