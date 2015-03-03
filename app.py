#
# start sound output system
#
import signal
from cement.core import foundation, exc
import numpy as np
import pygame as pg
import time
import struct

import sound

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

    global sounder
    sounder.change(frequency = currentFreq, gain = currentPeak)


app = foundation.CementApp('RaspiSoundGenerator')

try:
	app.setup()
	app.run()

	freqSensitivity = 1.3
	maxFreq = 2000.0
	minFreq = 1.0
	currentFreq = 500.0

	peakSensitivity = 0.001
	maxPeak = 1.0
	minPeak = 0.0
	currentPeak = 0.1

	sounder = sound.SineSound()
	sounder.start()
	
	# initialize mouse reader
	file = open( "/dev/input/mice", "rb" );

	while( 1 ):
	  getMouseEvent();

	file.close();
except exc.CaughtSignal as e:
    if e.signum == signal.SIGTERM:
        print("Caught signal SIGTERM...")
        # do something to handle signal here
    elif e.signum == signal.SIGINT:
        print("Caught signal SIGINT...")
        # do something to handle signal here
finally:
	app.close()


