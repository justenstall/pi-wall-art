import alsaaudio
import time
import io
import numpy as np
import librosa
import soundfile as sf

def visualizer():
	device = "hw:1,0"

	# Open the device in nonblocking capture mode in mono, with a sampling rate of 44100 Hz 
	# and 16 bit little endian samples
	# The period size controls the internal number of frames per period.
	# The significance of this parameter is documented in the ALSA api.
	# For our purposes, it is suficcient to know that reads from the device
	# will return this many frames. Each frame being 2 bytes long.
	# This means that the reads below will return either 320 bytes of data
	# or 0 bytes of data. The latter is possible because we are in nonblocking
	# mode.
	inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, 
		channels=1, rate=44100, format=alsaaudio.PCM_FORMAT_S16_LE, 
		periodsize=160, device=device)
	
	f = io.BytesIO()

	# librosa.stream(f)
	

	while True:
		# Read data from device
		l, data = inp.read()

		if l:
			f.write(data)
			sfdata, samplerate = sf.read(data)
			print(f"Valid? {librosa.util.valid_audio(data.T)}")
			time.sleep(.001)

# def sample_to_bars(samples):
# 	freq_bins = abs(np.array_split(np.fft(samples, self.count * 2), 2)[0]) / self.count
# 	new_positions = np.clip(np.log10(freq_bins * 9 + 1), 0, 1)

import pyaudio
p = pyaudio.PyAudio()
for ii in range(p.get_device_count()):
   print(f"{ii}:{p.get_device_info_by_index(ii).get('name')}")

# visualizer()