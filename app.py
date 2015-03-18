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
from rotary import RotaryEncoder
from config import StrpConfig
import time
import RPi.GPIO as GPIO
from touch import CapReader, CapReaderGroup
import math

class AppClass:
  updateSound = False

  def __init__(self, verbose=False):
    self.verbose = verbose
    self.setup()

  def setup(self):
    self.app = foundation.CementApp('RaspiSoundGenerator')
    self.app.setup()

    self.config = StrpConfig()
    
    self.gain = sattr.Sattr(value=0.1, min=0.0, max=1.0)
    self.frequency = sattr.Sattr(value=120.0, min=self.config.freqMin, max=self.config.freqMax) #min=1.0, max=2000.0)
    print 'freq initial: %.1f' % self.frequency.value
    self.frequencyPos = sattr.Sattr(value = 0.0) #value=math.asin(self.frequency.value))

    self.sounder = sound.SineSound(frequency=self.frequency.value, gain=self.gain.value)
    self.sounder.start()

    self.fileSounder = sound.FileSound(path='audio/sweep01.wav', gain=0.3)

    self.mouse = mouse.MouseFileReader()
    # self.mouse.xSensitivity = 0.001
    # self.mouse.ySensitivity = 1.3
    # self.mouse.x = self.gain.value
    # self.mouse.y = self.frequency.value

    # config GPIOs (used by rotary input)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    self.rotary = None
    if self.config and self.config.rotaryA and self.config.rotaryB:
      self.rotary = RotaryEncoder(pinA=self.config.rotaryA, pinB=self.config.rotaryB, button=None, callback=self.onRotary, verbose=True)

    dispatcher.connect( self.onFreqPosChange, signal='Sattr::changed', sender=self.frequencyPos )    
    dispatcher.connect( self.onFreqChange, signal='Sattr::changed', sender=self.frequency )
    dispatcher.connect( self.onGainChange, signal='Sattr::changed', sender=self.gain )

    self.monitor = monitor.ActivityMonitor(maxIdle=(3), activateDuration=(2), idleLimit=0.3)

    dispatcher.connect( self.handleIdleTooLong, signal='Monitor::idleTooLong', sender=dispatcher.Any )
    dispatcher.connect( self.handleActivationComplete, signal='Monitor::activationComplete', sender=dispatcher.Any )

    self.touches = CapReaderGroup(inPins=self.config.touchInPins, outPins=self.config.touchOutPins, verbose=True)

    self.gain.setMax(self.monitor.idleLimit+0.1)
    self.app.run()
    self.bRightFirst = True

  def update(self, dt=0):
    self.touches.update(dt)

    # tell the monitor how much time has elapsed and what the current gain level is,
    # it will trigger the 'Monitor::shakeItUp' signal if the gain has been too low for too long
    self.monitor.update(dt, self.gain.value)

    # # mouse buttons plays sound
    # if(self.mouse.bRight):
    #   self.fileSounder.play()
    #   #print('bRight')
    #   #if(self.bRightFirst == True):
    #   #  print('right first')
    #   #  self.sounder.playOnce('audio/weedflute_mac.wav')
    # else:
    #   self.bRightFirst = True

    #self.gain.set(self.mouse.x)
    #self.frequency.set(self.mouse.y)

    # updateSound could be set to by the handleChange callback method
    # if self.updateSound == True: 
    #  print ("Freq: %.1f, Peak: %.1f"  % (self.frequency.value, self.gain.value))
    #  self.sounder.change(frequency = self.frequency.value)
    #  self.updateSound = False

  def destroy(self):
    self.app.close()
    GPIO.cleanup()

  def onFreqPosChange(self, sender):
    print ("Freq pos: %.1f" % sender.value)
    min = self.config.freqMin
    max = self.config.freqMax
    delta = max-min
    # frequencyPos is a frequency affector; its value traverse a sine wave
    # which is used to calculate new frequency values, based on the configure
    # minimum and maximum frequencies
    self.frequency.set(min + delta * (math.sin(sender.value) * 0.5 + 0.5))

  def onFreqChange(self, sender):
    # self.updateSound = True    
    print ("Freq: %.1f, Gain: %.1f"  % (self.frequency.value, self.gain.value))
    self.sounder.change(frequency = self.frequency.value)

  def onGainChange(self, sender):
    print ("Freq: %.1f, Gain: %.1f"  % (self.frequency.value, self.gain.value))
    self.sounder.setGain(self.gain.value)

  def handleIdleTooLong(self, sender):
    return
    print('Starting shake-up')
    self.gain.setMin(self.monitor.idleLimit)

  def handleActivationComplete(self, sender):
    return
    print('Shake-up done')
    self.gain.setMin(0.0)

  def onRotary(self, event):
    if event == RotaryEncoder.CLOCKWISE:
      self.frequencyPos.set(self.frequencyPos.value + self.config.rotaryFreqPosStep)
      self.frequency.set(self.frequency.value + self.config.rotaryFreqStep)
      self.gain.set(self.gain.value + self.config.rotaryGainStep)
    elif event == RotaryEncoder.ANTICLOCKWISE:
      self.frequencyPos.set(self.frequencyPos.value - self.config.rotaryFreqPosStep)
      self.frequency.set(self.frequency.value - self.config.rotaryFreqStep)
      self.gain.set(self.gain.value - self.config.rotaryGainStep)

# end of class AppClass

theApp = AppClass(verbose=True)

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


