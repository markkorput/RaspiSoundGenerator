#
# start sound output system
#
import signal
from cement.core import foundation, exc
import numpy as np

import sound
import mouse
import sattr

class AppClass:
  def __init__(self):
    self.setup()

  def setup(self):
    self.app = foundation.CementApp('RaspiSoundGenerator')
    self.app.setup()

    self.gain = sattr.Sattr(value=0.1, min=0.0, max=1.0)
    self.frequency = sattr.Sattr(value=300.0, min=1.0, max=2000.0)

    self.sounder = sound.SineSound(frequency=self.frequency.value, gain=self.gain.value)
    self.sounder.start()

    self.mouse = mouse.MouseFileReader()
    self.mouse.xSensitivity = 0.001
    self.mouse.ySensitivity = 1.3
    self.mouse.x = self.gain.value
    self.mouse.y = self.frequency.value

    self.app.run()

  def update(self):
    self.mouse.update()

    if(self.mouse.x != self.gain.value) or (self.mouse.y != self.frequency.value):
      self.gain.set(self.mouse.x)
      self.frequency.set(self.mouse.y)
      print ("Freq: %.1f, Peak: %.1f"  % (self.frequency.value, self.gain.value))
      self.sounder.change(frequency = self.frequency.value, gain = self.gain.value)

  def destroy(self):
    self.app.close()


theApp = AppClass()

try:
  while( 1 ):
    theApp.update()

except exc.CaughtSignal as e:
    if e.signum == signal.SIGTERM:
        print("Caught signal SIGTERM...")
        # do something to handle signal here
    elif e.signum == signal.SIGINT:
        print("Caught signal SIGINT...")
        # do something to handle signal here
finally:
  theApp.destroy()

