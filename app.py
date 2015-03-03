#
# start sound output system
#
import signal
from cement.core import foundation, exc
import numpy as np
import pygame as pg
import time
import struct


def mkSine(freq=1000, peak=0.1, samplerate=44100, nchannels=1):
  wavelen = 0.0
  if( freq != 0.0 ):
    wavelen = 1.0/freq
  wavesize = wavelen * samplerate

  sinusoid = (2**15 - 1) * np.sin(2.0 * np.pi * freq * np.arange(0, wavesize) / float(samplerate)) * peak
  samples = np.array(sinusoid, dtype=np.int16)
  if(nchannels > 1):
    samples = np.tile(samples, (nchannels, 1)).T
  return pg.sndarray.make_sound(samples)


def getMouseEvent():
  buf = file.read(3);
  button = ord( buf[0] );
  bLeft = button & 0x1;
  bMiddle = ( button & 0x4 ) > 0;
  bRight = ( button & 0x2 ) > 0;
  x,y = struct.unpack( "bb", buf[1:] );
  # print ("L:%d, M: %d, R: %d, x: %d, y: %d\n" % (bLeft,bMiddle,bRight, x, y) );

  global currentFreq, freqSensitivity, minFreq, maxFrew
  global currentPeak, peakSensitivity, minPeak, maxPeak

  newFreq = currentFreq
  if( y!=0 ):
    newFreq = np.clip(currentFreq + y * freqSensitivity, minFreq, maxFreq)

  newPeak = currentPeak
  if( x!=0 ):
    newPeak = np.clip(currentPeak + x * peakSensitivity, minPeak, maxPeak)

  if(newPeak != currentPeak) or (newFreq != currentFreq):
    currentFreq = newFreq
    currentPeak = newPeak
    print ("Freq: %.1f, Peak: %.1f"  % (currentFreq, currentPeak))
    global sound, samplerate, nchannels
    newSound = mkSine(currentFreq, currentPeak, samplerate, nchannels)
    pg.mixer.stop()
    sound = newSound
    sound.play(-1)


app = foundation.CementApp('RaspiSoundGenerator')

try:
	app.setup()
	app.run()

	frequency, samplerate, duration = 1000, 44100, 20000
	nchannels = 1 # change to 2 for stereo

	freqSensitivity = 1.3
	maxFreq = 2000.0
	minFreq = 1.0
	currentFreq = 500.0

	peakSensitivity = 0.001
	maxPeak = 1.0
	minPeak = 0.0
	currentPeak = 0.1

	pg.mixer.pre_init(samplerate, -16, nchannels)
	pg.init()
	sound = mkSine(currentFreq, currentPeak, samplerate, nchannels)
	sound.play(-1)
	
	# initialize mouse reader
	file = open( "/dev/input/mice", "rb" );

	while( 1 ):
	  getMouseEvent();

	file.close();
except exc.CaughtSignal as e:
    # do something with e.signum or e.frame (passed from signal library)

    if e.signum == signal.SIGTERM:
        print("Caught signal SIGTERM...")
        # do something to handle signal here
    elif e.signum == signal.SIGINT:
        print("Caught signal SIGINT...")
        # do something to handle signal here
finally:
	app.close()

