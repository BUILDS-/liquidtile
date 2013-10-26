import pyaudio
import wave
import numpy
import struct
import sys
import pyLiquidTile
import time
import random as rand

class LiquidAudioIn(object):		
	def __init__(self, 
		         rate=44100, 
		         dev_index=0, 
		         format=pyaudio.paInt16,
		         chunk_size=1024, 
		         channels=1):
		"""
		Initialize variables which describe the audio stream and
		install the callback function (callback_fn)
		"""
		# Note that self.__varname member variables are protected
		self.__format = format
		self.__channels = channels
		self.__chunk = chunk_size
		self.__rate = rate
		self.__dev_index = dev_index

		self.audio = pyaudio.PyAudio()
		self.stream  = self.audio.open(format=self.__format,
						     		   channels=self.__channels,
						     		   frames_per_buffer=self.__chunk,
						     		   input=True,
						     		   input_device_index=self.__dev_index,
						     		   rate=self.__rate)
		self.raw_data = None
		self.data = []

	def start(self):
		"""
		Starts the audio stream.
		"""
		self.stream.start_stream()

	def stop(self):
		"""
		Stop the audio stream.
		"""
		self.stream.stop_stream()
	def is_active(self):
		"""
		Returns the active state of the stream
		"""
		self.stream.is_active()

	def close(self):
		"""
		Terminate the pyaudio object
		"""
		self.stream.close()
		self.audio.terminate()


	def read(self):
		self.raw_data = self.stream.read(self.__chunk)

	def to_array(self, fmt=None, normalize=True):
		# http://stackoverflow.com/questions/4160175/detect-tap-with-pyaudio-from-live-mic
		count = len(self.raw_data)/2
		norm = 1
		if not fmt:
			if self.__format == pyaudio.paInt16:
				fmt = "%dh"%(count)
				norm = (2**16)/2
		self.data = struct.unpack( fmt, self.raw_data )
		if norm:
			self.data = [i/norm for i in self.data]


if __name__ == "__main__":
	t = pyLiquidTile.LiquidTileNxN('/dev/ttyUSB0',width=3,height=3, loopback=False)
	t.clear()
	mappings = [0, 1,2,3,4,5,6,7,8]
	CHUNK = 4096
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 48000

	DEV_INDEX = 2

	audio_in = LiquidAudioIn(format=FORMAT, chunk_size=CHUNK, rate=RATE, dev_index=DEV_INDEX)	
#	print audio_in.audio.get_device_info_by_index(DEV_INDEX)
	audio_in.start()

	color_shift_counter = 0
	average_value = 1
	time_average = 1
	r = 2*0xff/3
	g = 0xff/3
	b = 0x0
	rdir = 1
	gdir = -1
	bdir = 1
	while True:
		try:
			color_shift_counter += 1

			audio_in.read()
			audio_in.to_array()
#			print audio_in.data
			# Compute the real FFT (assuming real input)... Length will be (CHUNK/2) + 1
			# Take the absolute value to get the amplitude spectrum
			amp_spectrum = numpy.abs(numpy.fft.rfft(audio_in.data)[16:int(CHUNK/32)])**2
			# Lets just throw out some of the higher frequency information (anything above 2.756kHz lets say)...
			# NOTE! We should filter, but it is moslty a waste of time right now [FIXME]
			# MATH (N = CHUNK)
			# 	fs = 44.1kHz => N/
			#	fs/2 = 22.05kHz => N/2
			#       2.756kHz = fs / h => N * (1/16)
#			amp_spectrum = amp_spectrum[16:int(CHUNK/(32))]

			# Compute the normalized spectrum, will be between 0 and 1
#			amp_spectrum_norm = [i/len(audio_in.data) for i in amp_spectrum] 

			# Compute an average value of the spectrum at this sample and also
			# compute the time average. Don't change too fast! We want average to adjust slowly
			# and not get rid of dynamic content.
#			average_value = sum(amp_spectrum)/len(amp_spectrum)		
#			time_average = .99*time_average + .01*average_value

#			average_value = max(amp_spectrum)
#			time_average = .99*time_average + .01*average_value
#			# Set the average value to about 40% brightness
#			amp_spectrum = [1*A/time_average for A in amp_spectrum]
#			print amp_spectrum

#			for i in range(len(amp_spectrum)):
#				if amp_spectrum[i] > 1:
#					amp_spectrum[i] = 1
	
			ranges = numpy.linspace(0, len(amp_spectrum)-1,10)
			ranges = [int(i) for i in ranges]
	
#			print ranges
			display = [sum(amp_spectrum[ranges[i]:ranges[i+1]])/(ranges[i+1] - ranges[i]) for i in range(len(ranges)-1)]
			average_value = max(display)
			time_average = .98*time_average + .02*average_value
#			print time_average
			display = [.7*A/time_average if .7*A <= time_average else 1 for A in display]
#			for i in display:
#				print "".join(["|" for j in range(i/2)])
			for i in range(9):
				pix = mappings[i]	
				t.setCell(pix%3, pix/3, (r*display[i], g*display[i],b*display[i]))
#			t.setRow(1, (r*display[0]/2, g*display[0]/2, int(b*display[0]/2)))
#			t.setRow(0, (r*display[2]/2, g*display[2]/2, int(b*display[2]/2)))
#			t.setRow(2, (r*display[4]/2, g*display[4]/2, int(b*display[4]/2)))
#			t.addToColumn(1, (r*display[1]/2, g*display[1]/2, b*display[1]/2))
#			t.addToColumn(0, (r*display[5]/2, g*display[5]/2, b*display[5]/2))
#			t.addToColumn(2, (r*display[3]/2, g*display[3]/2, b*display[3]/2))
			
			
			t.pushFrame()            
			t.update()
			if max(display) > .95:
				if rand.randint(0,1):
#				sys.stderr.write('shuffle\n')
#				sys.stderr.write(str(mappings))
					rand.shuffle(mappings)

			if color_shift_counter == 1:
				if (r == 0xff):
					rdir = -1
				elif (r == 0):
					rdir = 1 

				if (g == 0xff):
					gdir = -1
				elif g == 0:
					gdir = 1 

				if (b == 0xff):
					bdir = -1 
				elif b == 0:
					bdir = 1
				
				r = (r + rdir) & 0xff
				g = (g + gdir) & 0xff
				b = (b + bdir) & 0xff
				color_shift_counter = 0

		except KeyboardInterrupt:
			sys.stderr.write("Exiting!\n")
			audio_in.stop()
			audio_in.close()
			sys.exit(0)
		except IOError:
			sys.stderr.write("WARNING: Packet Dropped\n")
