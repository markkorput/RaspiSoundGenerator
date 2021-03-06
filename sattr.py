from pydispatch import dispatcher
import time

class Sattr:
  """Super-attribute"""
  max = None
  min = None

  def __init__(self, value='', min=None, max=None):
    self.value = value
    self.min = min
    self.max = max
    self.prev = None
    # animate
    self.fromVal = None
    self.toVal = None
    self.startTime = None
    self.duration = None

  def set(self, value, dispatch=True):
    if self.max != None and value > self.max:
      value = self.max

    if self.min != None and value < self.min:
      value = self.min

    self.prev = self.value
    self.value = value

    if self.prev != value and dispatch:
      dispatcher.send( signal='Sattr::changed', sender=self )

  def setMin(self, minVal):
    self.min = minVal
    if self.max < self.min:
      self.setMax(minVal)
    self.set(self.value)

  def setMax(self, maxVal):
    self.max = maxVal
    if self.min > self.max:
      self.setMin(maxVal)
    self.set(self.value)

  def animateTo(self, toVal, duration=0.3):
    self.toVal = toVal
    self.fromVal = self.value
    self.duration = duration
    self.timer = 0.0

  def update(self, dt):
    if self.toVal == None:
      return

    self.timer += dt
    if self.timer >= self.duration:
      self.set(self.toVal)
      self.toVal = None # done
      return

    dv = self.toVal - self.fromVal
    self.set(self.fromVal + dv * self.timer / self.duration)

import time

class DelaySattr(Sattr):

  def __init__(self, value=False, delay=1.0):
    self.value = value
    self.delay=delay
    self.timeToChange=-1.0
    self.changeValue=None

  def set(self, value=True, immediate=False, customDelay=None):
    if immediate == True:
      Sattr.set(self, value)
      self.changeValue = None # cancel any pending changes
      return

    if customDelay == None:
      self.timeToChange = self.delay
    else:
      self.timeToChange = customDelay

    self.changeValue = value

  def update(self, dt):
    if self.changeValue == None:
      return

    self.timeToChange -= dt
    if self.timeToChange <= 0:
      self.set(value=self.changeValue, immediate=True) # this reset changeValue


if __name__ == "__main__":

  def onChange(sender):
    print 'Value changed to: %.1f' % sender.value

  def onTouchChange(sender):
    if(sender.value == True):
      print 'Touching'
    else:
      print 'Not touching'

  print 'Starting test'
  attr = Sattr(value = 0.0) #value=math.asin(self.frequency.value))
  dispatcher.connect( onChange, signal='Sattr::changed', sender=attr )
  attr.set(301)

  tAttr = DelaySattr(value=False, delay=0.5)
  dispatcher.connect( onTouchChange, signal='Sattr::changed', sender=tAttr )

  tAttr.set(True, True)

  firstt = time.time()
  prevt = time.time()
 
  tAttr.set(False)
  while prevt - firstt < 2.0:
    t = time.time() # current time
    dt = t-prevt # elapsed time since last 'frame'
    tAttr.update(dt)
    prevt = t
  print 'Test ended'