#!/user/bin/env python

import RPi.GPIO as GPIO, time
from cement.core import foundation, exc

class Strobe:
    def __init__(self, outPin=17, frequency=10, timeOn=0.01, verbose=False):
        self.verbose = verbose
        self.outPin = outPin # pin to which the light is connected
        self.timeOn = timeOn # the duration the light will be ON every blink
        self.setFrequency(frequency) # set frequency (also updates self.timeOff and self.timeOn if necessary)
        self.isOn = False # we're starting in OFF state
        self._timeToSwitch = self.timeOff # countdown until switch-ON
        GPIO.setup(outPin, GPIO.OUT)
        GPIO.output(outPin, GPIO.LOW)

    def setFrequency(self, frequency=10):
        self.freq = frequency # remember the frequency value (not really used)
        cycleTime = 1.0 / self.freq # time between two blinks
        if self.timeOn >= cycleTime: # time On can't be as long as (or longer than) the time between two blinks, otherwise, there is no time left to be OFF
          self.timeOn = cycleTime / 2 # default time On to 50% of the time between two blinks (todo: test what work best)
        self.timeOff = cycleTime - self.timeOn # time off is the remained of the time between two blinks
        if self.verbose:
          print "ON-time: %.2f, OFF-time: %0.2f" % (self.timeOn, self.timeOff)

    def update(self, dt=0):
        self._timeToSwitch -= dt # progress timer
        if self._timeToSwitch <= 0.0: # countdown ended; switch on/off
            if self.isOn: # is on; turn off
                self.isOn = False
                GPIO.output(self.outPin, GPIO.LOW)
                self._timeToSwitch += self.timeOff # set timer for turning ON
                if self.verbose:
                    print '(%d hz)  OFF' % self.freq
            else: # if off; turn on
                self.isOn = True
                GPIO.output(self.outPin, GPIO.HIGH)
                self._timeToSwitch += self.timeOn # set timer for turning OFF
                if self.verbose:
                    print '(%d hz) ON' % self.freq


if __name__ == "__main__":
    try:
      GPIO.setmode(GPIO.BCM)
      GPIO.setwarnings(False)

      strobe = Strobe(outPin=17, frequency=10, verbose=True)

      frameTime = (1.0/25.0) # 25fps
      prevt = time.time()

      while( 1 ):
        t = time.time() # current time
        dt = t-prevt # elapsed time since laster 'frame'

        # theApp.update(dt)
        strobe.update(dt)

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
      #theApp.destroy()
      print('Cleaning up...')
      GPIO.cleanup()
