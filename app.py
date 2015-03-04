#
# start sound output system
#
import signal
from cement.core import foundation, exc
import numpy as np
from pydispatch import dispatcher

import sound
import mouse
import sattr
import monitor

import time

class AppClass:
  updateSound = False

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

    dispatcher.connect( self.handleChange, signal='Sattr::changed', sender=dispatcher.Any )

    self.monitor = monitor.ActivityMonitor(maxIdle=(3), activateDuration=(2), idleLimit=0.3)

    dispatcher.connect( self.handleIdleTooLong, signal='Monitor::idleTooLong', sender=dispatcher.Any )
    dispatcher.connect( self.handleActivationComplete, signal='Monitor::activationComplete', sender=dispatcher.Any )

    self.app.run()

  def update(self, dt=0):
    self.mouse.update()

    # tell the monitor how much time has elapsed and what the current gain level is,
    # it will trigger the 'Monitor::shakeItUp' signal if the gain has been too low for too long
    self.monitor.update(dt, self.gain.value)

    self.gain.set(self.mouse.x)
    self.frequency.set(self.mouse.y)

    # updateSound could be set to by the handleChange callback method
    if self.updateSound == True: 
      print ("Freq: %.1f, Peak: %.1f"  % (self.frequency.value, self.gain.value))
      self.sounder.change(frequency = self.frequency.value, gain = self.gain.value)
      self.updateSound = False

  def destroy(self):
    self.app.close()

  def handleChange(self, sender):
    self.updateSound = True    

  def handleIdleTooLong(self, sender):
    print('Starting shake-up')
    self.gain.setMin(self.monitor.idleLimit)

  def handleActivationComplete(self, sender):
    print('Shake-up done')
    self.gain.setMin(0.0)

theApp = AppClass()

try:

  frameTime = (1.0/25.0) # 25fps
  prevt = time.time()

  while( 1 ):
    t = time.time() # current time
    dt = t-prevt # elapsed time since laster 'frame'

    theApp.update(dt)

    prevt = t
    if dt < frameTime: # we don't need to go that fast, sleep a bit if time allows it
      time.sleep(frameTime - dt)


except exc.CaughtSignal as e:
    if e.signum == signal.SIGTERM:
        print("Caught signal SIGTERM...")
        # do something to handle signal here
    elif e.signum == signal.SIGINT:
        print("Caught signal SIGINT...")
        # do something to handle signal here
finally:
  theApp.destroy()


