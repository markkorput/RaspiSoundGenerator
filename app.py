#
# start sound output system
#
import signal
from cement.core import foundation, exc
import numpy as np
from pydispatch import dispatcher

import sound
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
    self.frequency = sattr.Sattr(value=self.config.defaultFreq, min=self.config.freqMin, max=self.config.freqMax) #min=1.0, max=2000.0)
    self.log('freq initial: %.1f' % self.frequency.value)
    self.position = sattr.Sattr(value = 0.0) #value=math.asin(self.frequency.value))

    self.sounder = sound.SineSound(frequency=self.frequency.value, gain=self.gain.value)
    self.sounder.start()

    # #self.fileSounder = sound.FileSound(path='audio/sweep01.wav', gain=0.3)
    # self.fileSounders = []
    # for startSound in self.config.startSounds:
    #   self.fileSounders.append(sound.FileSound(path=startSound, gain=0.3, verbose=True))
    # # self.mixSound = sound.FileSound(path=self.config.mixingAudio, gain=1.0, verbose=True)

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
    self.gain.setMax(self.config.activeMaxGain) #self.monitor.idleLimit+0.1)
    self.freqAffectorTimer = Timer()
    self.freqAffectorTimer.start()
    self.touchDelay = Timer(duration=0.1)
    self.touchDelay.start()

    dispatcher.connect( self.onPosChange, signal='Sattr::changed', sender=self.position )
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
    #self.touchDelay.update(dt)
    #if self.touchDelay.running == False:
    #  self.touches.update(dt)
    #  self.touchDelay.start()
    self.touches.update(dt)

    self.gain.update(dt)
    self.activityTimer.update(dt) 
    self.forcedIdleTimer.update(dt)
    # tell the monitor how much time has elapsed and what the current gain level is,
    # it will trigger the 'Monitor::shakeItUp' signal if the gain has been too low for too long
    # note that we're using a sound file for the mixing now, so our gain level
    # (which is only used for the wave-forms) will be zero, but we still want the monitor to know we're
    # making sound, so we'll simply use the specified idLimit instead
    monitorValue = self.gain.value
    if self.status.value == 'mixing':
      monitorValue = self.monitor.idleLimit + 0.1

    self.monitor.update(dt, monitorValue)
    self.freqAffectorTimer.update(dt)

  def destroy(self):
    self.app.close()
    GPIO.cleanup()

  def onPosChange(self, sender):
    self.log("Freq pos: %.1f" % sender.value)

    if self.config.posAffectFreq:
      min = self.config.freqMin
      max = self.config.freqMax
      delta = max-min
      # position is a frequency affector; its value traverse a sine wave
      # which is used to calculate new frequency values, based on the configure
      # minimum and maximum frequencies
      self.frequency.set(min + delta * (math.sin(sender.value) * 0.5 + 0.5))

    if self.config.posAffectGain and self.status.value == 'interactive':
      min = self.gain.min
      max = self.gain.max
      delta = max-min
      # position is a frequency affector; its value traverse a sine wave
      # which is used to calculate new frequency values, based on the configure
      # minimum and maximum frequencies
      self.log('affecting gain: %d,%d,%d' % (min, max, delta))
      self.gain.set(min + delta * (math.sin(sender.value) * 0.5 + 0.5))

  def onFreqChange(self, sender):
    # if self.touchDelay.running == True:
    #   return
    # self.touchDelay.start()

    affectorValue = math.sin(self.freqAffectorTimer.time() * self.config.affectorSpeed) * self.config.affectorAmp
    freq = self.frequency.value + affectorValue
    self.log("Freq: %.1f, Gain: %.1f"  % (freq, self.gain.value))
    self.sounder.change(frequency = freq)
    self.log(random.choice(self.sounder.ascii))

  def onGainChange(self, sender):
    self.log("Freq: %.1f, Gain: %.1f"  % (self.frequency.value, self.gain.value))
    self.sounder.setGain(self.gain.value)

  def handleIdleTooLong(self, sender):
    if self.status.value == 'idle':
      self.status.set('mixing')
      # self.mixSound.play()
      #self.gain.animateTo(0.0) # turn wave of during mixing, we're using an audio file instead
      self.gain.animateTo(self.config.activateGain, self.config.activateDuration*0.75)
      # self.gain.setMin(self.monitor.idleLimit)
      # self.gain.animateTo(self.config.activateGain)

  def handleActivationComplete(self, sender):
    if self.status.value == 'mixing':
      self.log('mixing done')
      self.status.set('idle')
      self.gain.animateTo(0.0)

  def onRotary(self, event):
    if event == RotaryEncoder.CLOCKWISE:
      self.position.set(self.position.value + self.config.rotaryPosStep)
      self.frequency.set(self.frequency.value + self.config.rotaryFreqStep)
      self.gain.set(self.gain.value + self.config.rotaryGainStep)
    elif event == RotaryEncoder.ANTICLOCKWISE:
      self.position.set(self.position.value - self.config.rotaryPosStep)
      self.frequency.set(self.frequency.value - self.config.rotaryFreqStep)
      self.gain.set(self.gain.value - self.config.rotaryGainStep)

  def onTouchCountChange(self, sender):
    if self.status.value == 'forcedIdle':
      return # ignore touches during forced idle

    if sender.value == 0:
      self.log("lost capacitive control")
      # touch count just turned zero, we just lost our last touch (delay already taken into account)
      # self.gain.setMax(0.0)
      if self.status.value == 'interactive':
        self.log('zero gain')
        self.gain.setMin(0.0)
        self.gain.animateTo(0.0)
        # for fileSounder in self.fileSounders:
        #   fileSounder.stop()
        self.status.set('idle')

      return

    # we just got a first touch, don't do anything unless we're idle
    # (don't interrupt the mixing procedure... or should be?)
    if sender.prev == 0: 
      self.log('first touch')
      self.status.set('interactive')
      self.gain.setMin(self.config.activeMinGain)
      self.gain.setMax(self.config.activeMaxGain)

      # # self.fileSounder.play()
      # if len(self.fileSounders) > 0:
      #   self.log('playing sweep')
      #   # random.choice(self.fileSounders).play()
      
      self.log('setting initial gain')
      # self.gain.setMin(self.config.initialActiveGainMin)
      self.gain.animateTo(self.config.initialActiveGainMin)
      self.position.set(value=0.0, dispatch=False)
      #self.frequency.set(self.config.touchFreqs[sender.value])
      #return

    #self.log('proportional gain')
    #self.gain.animateTo(sender.value * 1.0 / len(self.touches.capReaders))
    val = 0
    for i in range(0,len(self.touches.capReaders)):
      if self.touches.capReaders[i].isTouching.value:
        val += (1 << i)
    self.log('touch val: %d' % val)
    self.frequency.set(self.config.touchFreqs[val]) #sender.value])



  def onStatusChange(self, sender):
    self.log('STATUS: %s' % sender.value)
    if sender.value == 'interactive':
      self.activityTimer.start()
      self.log('starting timer (%s to %s)' % (sender.prev, sender.value))
    else:
      self.activityTimer.stop()

    if sender.value == 'idle':
      self.frequency.set(self.config.defaultFreq)

    # if sender.value != 'mixing':
    #   self.mixSound.stop()

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


