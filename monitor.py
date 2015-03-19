from pydispatch import dispatcher

class ActivityEpisode:
  def __init__(self, time=0.0, avg=0.0, min=0.0, max=0.0):
    self.time = time
    self.avg = avg
    self.min = min
    self.max = max

  def update(self, dt=0.0, value=0.0):
    dValue = value - self.avg
    newTime = self.time + dt
    dFactor = dt / newTime
    newAvg = self.avg + dValue * dFactor
    self.time = newTime
    self.avg = newAvg


class ActivityMonitor:
  def __init__(self, maxIdle=3, activateDuration=2, idleLimit=1, verbose=False):
    self.verbose = verbose
    self.maxIdle = maxIdle
    self.activateDuration = activateDuration
    self.idleLimit = idleLimit
    self._prevValue = 0.0

    self.episodes = [ActivityEpisode()]

  def update(self, dt=0, currentValue=0):
    # if we just went from active to idle, start new timer episode
    if currentValue < self.idleLimit and self._prevValue >= self.idleLimit:
      # if the just ended active period wasn't long enough, let's pretend it didn't happen
      if len(self.episodes) >= 2 and self.episodes[-1].time < self.activateDuration:
        self.episodes.pop(-1)
      else:
        self.episodes.append(ActivityEpisode())
        self.cleanEpisodes()      

    # if we just went from idle to active, start new timer episode
    if currentValue >= self.idleLimit and self._prevValue < self.idleLimit:
      self.episodes.append(ActivityEpisode())
      self.cleanEpisodes()

    ep = self.episodes[-1]
    ep.update(dt, currentValue)

    # idle too long? dipatch a signal!
    if currentValue < self.idleLimit and ep.time > self.maxIdle:
      dispatcher.send( signal='Monitor::idleTooLong', sender=self )

    if currentValue >= self.idleLimit and ep.time > self.activateDuration:
      dispatcher.send( signal='Monitor::activationComplete', sender=self )

    self._prevValue = currentValue

  def cleanEpisodes(self):
    if len(self.episodes) > 110:
      while len(self.episodes > 90):
        self.episodes.pop(0)

  def log(self, msg):
    if self.verbose:
      print(msg)
