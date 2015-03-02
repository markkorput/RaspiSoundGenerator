import numpy as np
import pygame as pg
import time

frequency, samplerate, duration = 1000, 44100, 20000
nchannels = 1 # change to 2 for stereo

def mkSine(freq=1000, peak=0.5, samplerate=44100, nchannels=1):
	sinusoid = (2**15 - 1) * np.sin(2.0 * np.pi * freq * np.arange(0, 20000) / float(samplerate)) * peak
	samples = np.array(sinusoid, dtype=np.int16)
	if(nchannels > 1):
		samples = np.tile(samples, (nchannels, 1)).T
	return pg.sndarray.make_sound(samples)


# pg.mixer.pre_init(channels=nchannels, frequency=frequency)
pg.mixer.pre_init(samplerate, -16, nchannels)
pg.init()

#sinusoid = (2**15 - 1) * np.sin(2.0 * np.pi * frequency * \
#                   np.arange(0, duration) / float(samplerate))
#samples = np.array(sinusoid, dtype=np.int16)
#if nchannels > 1: #copy mono signal to two channels
#       samples = np.tile(samples, (nchannels, 1)).T
#sound = pg.sndarray.make_sound(samples)
sound = mkSine(frequency, 0.2, samplerate)
sound.play(-1)

time.sleep(duration/float(samplerate)*10)
