#!/user/bin/env python

import RPi.GPIO as GPIO, time
from sattr import Sattr, DelaySattr
from pydispatch import dispatcher

class CapReader:
  def __init__(self, inPin=17, outPin=18, timeout=10000, treshold=100, cycles=10):
    self.inPin = inPin
    self.outPin = outPin
    self.timeout = timeout
    self.cycles = cycles
    self.treshold = treshold
    self.isTouching = Sattr(value=False) #DelaySattr(value=False, delay=0.1)
    self.totalValue = 0

  def read(self):
    return self._CapRead(self.inPin, self.outPin, self.timeout)

  def update(self, dt=0.0):
    # self.isTouching.update(dt)

    self.totalValue = 0
    for j in range(0, self.cycles):
      self.totalValue += self._CapRead(self.inPin, self.outPin, self.timeout) # self.read()
      if self.totalValue >= self.treshold:
        self.isTouching.set(True) #(value=True, immediate=True)
        return True

    self.isTouching.set(False) #(value=False, immediate=False) # delayed
    return False

  def _CapRead(self, inPin=17,outPin=18, timeout=10000):
    total = 0
    
    # set Send Pin Register low
    GPIO.setup(outPin, GPIO.OUT)
    GPIO.output(outPin, GPIO.LOW)
    
    # set receivePin Register low to make sure pullups are off 
    GPIO.setup(inPin, GPIO.OUT)
    GPIO.output(inPin, GPIO.LOW)
    GPIO.setup(inPin, GPIO.IN)
    
    # set send Pin High
    GPIO.output(outPin, GPIO.HIGH)
    
    # while receive pin is LOW AND total is positive value
    while( GPIO.input(inPin) == GPIO.LOW and total < timeout ):
        total+=1
    
    if ( total > timeout ):
        return -2 # total variable over timeout
        
     # set receive pin HIGH briefly to charge up fully - because the while loop above will exit when pin is ~ 2.5V 
    GPIO.setup( inPin, GPIO.OUT )
    GPIO.output( inPin, GPIO.HIGH )
    GPIO.setup( inPin, GPIO.IN )
    
    # set send Pin LOW
    GPIO.output( outPin, GPIO.LOW ) 

    # while receive pin is HIGH  AND total is less than timeout
    while (GPIO.input(inPin)==GPIO.HIGH and total < timeout) :
        total+=1
    
    if ( total >= timeout ):
        return -2
    else:
        return total

class CapReaderGroup:
  def __init__(self, inPins=[], outPins=[], timeout=10000, treshold=100, cycles=10, noTouchDelay=1.0, verbose=False):
    self.verbose=verbose
    self.capReaders = []
    self.touchCount = DelaySattr(value=0, delay=noTouchDelay) # default delay of 1.0 second

    for i in range(0,len(inPins)):
      reader = CapReader(inPin=inPins[i], outPin=outPins[i], timeout=timeout, treshold=treshold, cycles=cycles)
      self.capReaders.append(reader)
      dispatcher.connect( self._onTouchChange, signal='Sattr::changed', sender=reader.isTouching )

    self.log('Created %d touch sensor readers' % len(self.capReaders))

  def log(self, msg):
    if self.verbose:
      print(msg)
      
  def update(self, dt):
    self.touchCount.update(dt)

    for reader in self.capReaders:
      reader.update(dt)
    # count = len(self.capReaders)
    # for idx,reader in enumerate(self.capReaders):
    #   reader.update(dt)
    #   # prev = reader.isTouching.value
    #   # if reader.isTouching.value and not reader.isTouching.prev:
    #   #   self.log("Touch on pin %d (%d/%d, %d touches total)" % (reader.inPin, idx+1, count, self.touchCount.value))

  def _onTouchChange(self, sender):
    count = 0

    for reader in self.capReaders:
      if reader.isTouching.value:
        count += 1

    if count == 0:
      self.touchCount.set(0) # delayed
    else:
      self.touchCount.set(value=count, immediate=True)

    # self.log('Touch count: %d/%d' % (self.touchCount.value, len(self.capReaders)))
      

if __name__ == "__main__":
    total = 0
    DEBUG = 1
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    reader = CapReader(inPin=17, outPin=18)


    # loop
    while True:
        # total = 0
        # for j in range(0,10):
        #     total += CapRead(inPin=17,outPin=18);
        touching = reader.update()

        str = "N - "
        if touching:
            str = "Y - "

        for j in range(0, int(reader.totalValue / 10.0)):
            str += "#"
        print str + " - total: %d" % (reader.totalValue)
  
    # clean before you leave
    GPIO.cleanup()
