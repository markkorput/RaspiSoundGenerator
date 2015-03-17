# sudo apt-get install python-picamera
# or the python3 package: sudo apt-get install python3-picamera
import picamera
# import pygame
# import pygame.camera
# from pygame.locals import *
import time

class CamViewer:
  def __init__(self, log=None):
    self.log = log
    self.camera = None

  def destroy(self):
    self.stop()

  def start(self):
    if self.camera == None:
      if self.log:
        self.log.info('Initializing pi camera...')
      self.camera = picamera.PiCamera()
      # # picam settings
      # self.camera.sharpness = 0
      # self.camera.contrast = 0
      # self.camera.brightness = 50
      # self.camera.saturation = 0
      # self.camera.ISO = 0
      # self.camera.video_stabilization = False
      # self.camera.exposure_compensation = 0
      # self.camera.exposure_mode = 'auto'
      # self.camera.meter_mode = 'average'
      # self.camera.awb_mode = 'auto'
      # self.camera.image_effect = 'none'
      # self.camera.color_effects = None
      # self.camera.rotation = 0
      # self.camera.hflip = False
      self.camera.vflip = True
      # self.camera.crop = (0.0, 0.0, 1.0, 1.0)
      if self.log:
        self.log.debug('camera initialize done.')

    if self.log:
      self.log.info("Starting camera preview...")
    self.camera.start_preview()
    return

    # if self.log:
    #   self.log.error("No camera initialized, can't start preview")

  def stop(self):
    if self.camera:
      if self.log:
        self.log.info("Stopping camera preview...")
      self.camera.stop_preview()
      return

    if self.log:
      self.log.warn("No camera initialized, nothing to stop.")

  # def update(self):
  #   imagen = self.cam.get_image()
  #   imagen = pygame.transform.scale(imagen, self.displaySize)
  #   self.display.blit(imagen, (0,0))
  #   pygame.display.update()

# end of class CamViewer

from app_class import AppClass
class PiCamAppClass(AppClass):
  def setup(self):
    AppClass.setup(self)
    self.viewer = CamViewer(log=self.app.log)

  def start(self):
    if self.viewer == None:
      self.app.log.warn('No camera found, aborting...')
      self.destroy()
      return

    # self.app.log.info('Starting app...')
    # AppClass.start(self, handleEvents=False)
    # self.app.log.info('Starting viewer...')
    self.viewer.start()
    while True:
      time.sleep(1)

  def destroy(self):
    if self.viewer:
      self.viewer.stop()

    AppClass.destroy(self)

  # def update(self, dt=0.0):
  #   self.viewer.update()
  #   return

# end of class PiCamAppClass

if __name__ == "__main__":
  app = PiCamAppClass(verbose=True, initializeGPIO=False)
  app.start()
