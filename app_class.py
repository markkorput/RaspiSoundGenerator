import signal
from cement.core import foundation, exc
import time
import RPi.GPIO as GPIO
import pygame

class AppClass:

  def __init__(self, verbose=False):
    self.verbose = verbose
    self.setup()

  def setup(self):
    self.app = foundation.CementApp('Test')
    self.app.setup()

    # config GPIOs (used by rotary input)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    if self.verbose:
      print('Setup done')

    self.app.run()

  def update(self, dt=0):
    return

  def destroy(self):  
    self.app.close()
    if self.verbose:
      print 'Cleaning up GPIO...'
    GPIO.cleanup()

  def start(self, framerate=None):
    try:
      frameTime = 0
      if framerate != None:
        frameTime = (1.0 / framerate)

      prevt = time.time()

      going = True
      while going:
        t = time.time() # current time
        dt = t-prevt # elapsed time since last 'frame'

        self.update(dt)

        prevt = t

        events = pygame.event.get()
        for e in events:
          if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            going = False

        if framerate != None:
          time.sleep(frameTime - dt)

    except exc.CaughtSignal as e:
      if e.signum == signal.SIGTERM:
        print("Caught signal SIGTERM...")
        # do something to handle signal here
      elif e.signum == signal.SIGINT:
        print("Caught signal SIGINT...")
        # do something to handle signal here
    finally:
      self.destroy()

if __name__ == "__main__":
  app = AppClass(verbose=True)
  app.start()


