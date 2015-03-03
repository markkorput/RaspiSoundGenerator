#
# start sound output system
#
import signal
from cement.core import foundation, exc
import numpy as np

import sound
import mouse
import sattr

app = foundation.CementApp('RaspiSoundGenerator')

try:
  app.setup()
  app.run()

  gain = sattr.Sattr(value=0.1, min=0.0, max=1.0)
  frequency = sattr.Sattr(value=300.0, min=1.0, max=2000.0)

  sounder = sound.SineSound(frequency=frequency.value, gain=gain.value)
  sounder.start()

  mouse = mouse.MouseFileReader()
  mouse.xSensitivity = 0.001
  mouse.ySensitivity = 1.3
  mouse.x = gain.value
  mouse.y = frequency.value

  while( 1 ):
    mouse.update()

    newFreq = mouse.x
    newPeak = mouse.y

    if(mouse.x != gain.value) or (mouse.y != frequency.value):
      gain.set(mouse.x)
      frequency.set(mouse.y)
      print ("Freq: %.1f, Peak: %.1f"  % (frequency.value, gain.value))
      sounder.change(frequency = frequency.value, gain = gain.value)

except exc.CaughtSignal as e:
    if e.signum == signal.SIGTERM:
        print("Caught signal SIGTERM...")
        # do something to handle signal here
    elif e.signum == signal.SIGINT:
        print("Caught signal SIGINT...")
        # do something to handle signal here
finally:
  app.close()
