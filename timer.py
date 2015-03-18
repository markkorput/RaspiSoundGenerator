import time
from pydispatch import dispatcher

class Timer:
  def __init__(self, duration=None, verbose=False):
    self.verbose = verbose
    self.duration = duration
    self.startTime = None # not started yet
    self.currentTime = None
    self.running = False

  def log(self, msg):
    if self.verbose:
      print(msg)

  def start(self):
    self.startTime = time.time()
    self.currentTime = self.startTime
    self.running = True
    dispatcher.send(signal='Timer::started', sender=self)

  def update(self, dt):
    if not self.running:
      return # nothing to do here

    self.currentTime += dt

    if self.duration and self.time() >= self.duration:
      dispatcher.send(signal='Timer::finished', sender=self)
      self.stop()

  def time(self):
    return self.currentTime - self.startTime

  def stop(self):
    self.running = False
    dispatcher.send(signal='Timer::stopped', sender=self)


