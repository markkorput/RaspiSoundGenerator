#
# start sound output system
#
import signal
from cement.core import foundation, exc
import numpy as np

import sound
import mouse

app = foundation.CementApp('RaspiSoundGenerator')

try:
  app.setup()
  app.run()

  maxFreq = 2000.0
  minFreq = 1.0
  currentFreq = 500.0

  maxPeak = 1.0
  minPeak = 0.0
  currentPeak = 0.1

  sounder = sound.SineSound()
  sounder.start()
  
  mouse = mouse.MouseFileReader()
  mouse.xSensitivity = 0.001
  mouse.ySensitivity = 1.3
  mouse.x = currentPeak
  mouse.y = currentFreq

  while( 1 ):
    mouse.update()

    newFreq = np.clip(mouse.y, minFreq, maxFreq)
    newPeak = np.clip(mouse.x, minPeak, maxPeak)

    if(newPeak != currentPeak) or (newFreq != currentFreq):
      currentFreq = newFreq
      currentPeak = newPeak
      print ("Freq: %.1f, Peak: %.1f"  % (currentFreq, currentPeak))
      sounder.change(frequency = currentFreq, gain = currentPeak)

except exc.CaughtSignal as e:
    if e.signum == signal.SIGTERM:
        print("Caught signal SIGTERM...")
        # do something to handle signal here
    elif e.signum == signal.SIGINT:
        print("Caught signal SIGINT...")
        # do something to handle signal here
finally:
  app.close()
