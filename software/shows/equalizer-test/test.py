import pyaudio
import wave
import numpy
import struct
import sys
#import liquidtile

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 48000
RECORD_SECONDS = 100
WAVE_OUTPUT_FILENAME = "output.wav"
DEV_INDEX = 2
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
		input_device_index=DEV_INDEX,
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
	print chr(27) + "[2J"
	for i in range(0,CHUNK/4, 8):
		print ''.join(["|" for i in range(0,int(fft[i]))])
    except KeyboardInterrupt:
	print "Exiting"
	sys.exit(0)
    except:
	print "dropped packet"

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

