import pyaudio
import wave
import numpy
import struct
import sys
import pyLiquidTile
import time

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

	t = pyLiquidTile.LiquidTileNxN(0,width=3,height=3, loopback=True)
	t.clear()

	CHUNK = 16
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 48000
	RECORD_SECONDS = 100
	WAVE_OUTPUT_FILENAME = "output.wav"
	DEV_INDEX = 2

	audio_in = LiquidAudioIn(format=FORMAT, chunk_size=CHUNK, rate=RATE, dev_index=DEV_INDEX)
	audio_in.start()

	count = 0
	count2 = 0
	max_avg = 1
	maxes_prev = [0 for i in range(8)]
	fft_filtered = [0 for i in range(CHUNK/2)]
	r = 2*0xff/3
	g = 0xff/3
	b = 0x0
	while 1:
		try:
			count += 1
			count2 += 1

			audio_in.read()
			audio_in.to_array()
			fft = abs(numpy.fft.fft(audio_in.data))
			fft_normalized = [i/(len(fft)/2) for i in fft]
			#maxes_prev.append(max(fft))
			#maxes_prev.pop(0)
			#max_avg = .1*(sum(maxes_prev)/len(maxes_prev)) + .9*max_avg
			if count == 256:
			#	t.setCell(1,0,(int(g*fft_filtered[1]),int(b*fft_filtered[1]/max_avg),int(r*fft[1]/max_avg)))
			#	t.setCell(1,2,(int(r*fft_filtered[2]),int(g*fft_filtered[2]/max_avg),int(b*fft[2]/max_avg)))
				for i in range(CHUNK/2):
					fft_filtered[i] = .9*fft_normalized[i] + .1*fft_filtered[i]
					if (fft_filtered[i] > 1):
						fft_filtered[i] = 1
				t.setRow(0,(int(r/2*fft_filtered[2]),int(g/2*fft_filtered[2]),int(b/2*fft_filtered[2])))
				t.setRow(1,(int(r/3*fft_filtered[0]),int(g/3*fft_filtered[0]),int(b/3*fft_filtered[0])))
				t.setRow(2,(int(r*fft_filtered[4]),int(g*fft_filtered[4]),int(b*fft_filtered[4])))
				t.addToColumn(0,(int(r/2*fft_filtered[2]),int(g/2*fft_filtered[2]),int(b/2*fft_filtered[2])))
				t.addToColumn(1,(int(r/3*fft_filtered[0]),int(g/3*fft_filtered[0]),int(b/3*fft_filtered[0])))
				t.addToColumn(2,(int(r*fft_filtered[4]),int(g*fft_filtered[4]),int(b*fft_filtered[4])))
				t.pushFrame()            
				t.update()
				count = 0
			if count2 == 512:
				r = (r + 2) & 0xff
				g = (g + 2) & 0xff
				b = (b + 2) & 0xff
				count2 = 0
		except KeyboardInterrupt:
			print("Exiting!")
			t.close()
			audio_in.stop()
			audio_in.close()
			sys.exit(0)
		except:
			count += 1
#			print "",
		#print("WARNING: Packet Dropped")
