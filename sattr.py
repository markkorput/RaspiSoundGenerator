from pydispatch import dispatcher

class Sattr:
  """Super-attribute"""
  max = None
  min = None

  def __init__(self, value='', min=None, max=None):
    self.value = value
    self.min = min
    self.max = max

  def set(self, value):
    if self.max != None and value > self.max:
      value = self.max

    if self.min != None and value < self.min:
      value = self.min

    old_value = self.value
    self.value = value

    if old_value != value:
      dispatcher.send( signal='Sattr::changed', sender=self )

  def setMin(self, minVal):
    self.min = minVal
    self.set(self.value)

  def setMax(self, maxVal):
    self.max = maxVal
    self.set(self.value)
