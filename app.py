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
import random
from timer import Timer

class AppClass:

  def __init__(self, verbose=False):
    self.verbose = verbose
    self.setup()

  def setup(self):
    self.app = foundation.CementApp('RaspiSoundGenerator')
    self.app.setup()

    self.config = StrpConfig()
    
    self.status = sattr.Sattr(value='loading')

    self.gain = sattr.Sattr(value=0.0, min=0.0, max=1.0)
    self.frequency = sattr.Sattr(value=120.0, min=self.config.freqMin, max=self.config.freqMax) #min=1.0, max=2000.0)
    self.log('freq initial: %.1f' % self.frequency.value)
    self.frequencyPos = sattr.Sattr(value = 0.0) #value=math.asin(self.frequency.value))

    self.sounder = sound.SineSound(frequency=self.frequency.value, gain=self.gain.value)
    self.sounder.start()

    #self.fileSounder = sound.FileSound(path='audio/sweep01.wav', gain=0.3)
    self.fileSounders = []
    for startSound in self.config.startSounds:
      self.fileSounders.append(sound.FileSound(path=startSound, gain=0.3, verbose=True))

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

    self.monitor = monitor.ActivityMonitor(maxIdle=self.config.maxIdle, activateDuration=self.config.activateDuration, idleLimit=self.config.idleLimit)
    self.touches = CapReaderGroup(inPins=self.config.touchInPins, outPins=self.config.touchOutPins, noTouchDelay=self.config.noTouchDelay, verbose=True)
    self.activityTimer = Timer(duration=self.config.maxInteraction, verbose=True)
    self.forcedIdleTimer = Timer(duration=self.config.minIdle, verbose=True)
    self.gain.setMax(1.0) #self.monitor.idleLimit+0.1)

    dispatcher.connect( self.onFreqPosChange, signal='Sattr::changed', sender=self.frequencyPos )
    dispatcher.connect( self.onFreqChange, signal='Sattr::changed', sender=self.frequency )
    dispatcher.connect( self.onGainChange, signal='Sattr::changed', sender=self.gain )
    dispatcher.connect( self.handleIdleTooLong, signal='Monitor::idleTooLong', sender=dispatcher.Any )
    dispatcher.connect( self.handleActivationComplete, signal='Monitor::activationComplete', sender=dispatcher.Any )
    dispatcher.connect( self.onTouchCountChange, signal='Sattr::changed', sender=self.touches.touchCount)
    dispatcher.connect( self.onStatusChange, signal='Sattr::changed', sender=self.status )
    dispatcher.connect( self.onMaxActivity, signal='Timer::finished', sender=self.activityTimer )
    dispatcher.connect( self.onForcedIdleDone, signal='Timer::finished', sender=self.forcedIdleTimer )

    self.app.run()
    self.status.set('idle')

  def update(self, dt=0.0):
    self.touches.update(dt)
    self.gain.update(dt)
    self.activityTimer.update(dt) 
    self.forcedIdleTimer.update(dt)
    # tell the monitor how much time has elapsed and what the current gain level is,
    # it will trigger the 'Monitor::shakeItUp' signal if the gain has been too low for too long
    self.monitor.update(dt, self.gain.value)

  def destroy(self):
    self.app.close()
    GPIO.cleanup()

  def onFreqPosChange(self, sender):
    self.log("Freq pos: %.1f" % sender.value)
    min = self.config.freqMin
    max = self.config.freqMax
    delta = max-min
    # frequencyPos is a frequency affector; its value traverse a sine wave
    # which is used to calculate new frequency values, based on the configure
    # minimum and maximum frequencies
    self.frequency.set(min + delta * (math.sin(sender.value) * 0.5 + 0.5))

  def onFreqChange(self, sender):
    self.log("Freq: %.1f, Gain: %.1f"  % (self.frequency.value, self.gain.value))
    self.sounder.change(frequency = self.frequency.value)

  def onGainChange(self, sender):
    self.log("Freq: %.1f, Gain: %.1f"  % (self.frequency.value, self.gain.value))
    self.sounder.setGain(self.gain.value)

  def handleIdleTooLong(self, sender):
    if self.status.value == 'idle':
      self.status.set('mixing')
      # self.gain.setMin(self.monitor.idleLimit)
      self.gain.animateTo(self.monitor.idleLimit)

  def handleActivationComplete(self, sender):
    if self.status.value == 'mixing':
      self.log('mixing done')
      self.status.set('idle')
      self.gain.animateTo(0.0)

  def onRotary(self, event):
    if event == RotaryEncoder.CLOCKWISE:
      self.frequencyPos.set(self.frequencyPos.value + self.config.rotaryFreqPosStep)
      self.frequency.set(self.frequency.value + self.config.rotaryFreqStep)
      self.gain.set(self.gain.value + self.config.rotaryGainStep)
    elif event == RotaryEncoder.ANTICLOCKWISE:
      self.frequencyPos.set(self.frequencyPos.value - self.config.rotaryFreqPosStep)
      self.frequency.set(self.frequency.value - self.config.rotaryFreqStep)
      self.gain.set(self.gain.value - self.config.rotaryGainStep)

  def onTouchCountChange(self, sender):
    if self.status.value == 'forcedIdle':
      return # ignore touches during forced idle

    if sender.value == 0:
      self.log("Lost capacitive control")
      # touch count just turned zero, we just lost our last touch (delay already taken into account)
      # self.gain.setMax(0.0)
      if self.status.value == 'interactive':
        self.log('zero gain')
        self.gain.animateTo(0.0)
        for fileSounder in self.fileSounders:
          fileSounder.stop()
        self.status.set('idle')

      return

    # we just got a first touch, don't do anything unless we're idle
    # (don't interrupt the mixing procedure... or should be?)
    if sender.prev == 0: 
      self.log('first touch')

      # self.fileSounder.play()
      if len(self.fileSounders) > 0:
        self.log('playing sweep')
        random.choice(self.fileSounders).play()
        self.status.set('interactive')
        #  self.sounder.playOnce('audio/weedflute_mac.wav')

      self.log('setting initial gain')
      # self.gain.setMin(self.config.initialActiveGainMin)
      self.gain.animateTo(self.config.initialActiveGainMin)
      return

    self.log('proportional gain')
    self.gain.animateTo(sender.value * 1.0 / len(self.touches.capReaders))

  def onStatusChange(self, sender):
    self.log('STATUS: %s' % sender.value)
    if sender.value == 'interactive':
      self.activityTimer.start()
      self.log('starting timer (%s to %s)' % (sender.prev, sender.value))
    else:
      self.activityTimer.stop()

  def onMaxActivity(self, sender):
    self.log('zeroing gain')
    self.gain.animateTo(0.0)
    self.status.set('forcedIdle')
    self.forcedIdleTimer.start()

  def onForcedIdleDone(self, sender):
    self.status.set('idle')

  def log(self, msg):
    if self.verbose:
      print(msg)

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


