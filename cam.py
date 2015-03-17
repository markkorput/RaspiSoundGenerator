import pygame
import pygame.camera
from pygame.locals import *

class CamViewer:
  def __init__(self, devicePath='/dev/video0', camSize=(480,360), displaySize=(640, 480), verbose=False):
    self.devPath = devicePath
    self.camSize = camSize
    self.displaySize = displaySize
    self.verbose = verbose

    if self.verbose:
      print 'Initialising display...'
    # create a display surface. standard pygame stuff
    self.display = pygame.display.set_mode(self.displaySize, 0)

    if self.verbose:
      print 'Initialising camera: %s (%d, %d)' % (self.devPath, self.camSize[0], self.camSize[1])
    self.cam = pygame.camera.Camera(self.devPath, self.camSize)

    if self.verbose:
      print("Starting cam...")
    self.cam.start()

    # if self.verbose:
    #   print("Creating surface...")
    # # create a surface to capture to. for performance purposes
    # # bit depth is the same as that of the display surface.
    # self.snapshot = pygame.surface.Surface(self.size, 0, self.display)

  def destroy(self):
    if self.verbose:
      print("stopping cam...")
    self.cam.stop()

    #if self.verbose:
    #  print("quitting display...")
    #self.display.quit()

  # def get_and_flip(self):
  #   # if you don't want to tie the framerate to the camera, you can check 
  #   # if the camera has an image ready.  note that while this works
  #   # on most cameras, some will never return true.
  #   if self.cam.query_image():
  #       self.snapshot = self.cam.get_image(self.snapshot)

  #   # blit it to the display surface.  simple!
  #   self.display.blit(self.snapshot, (0,0))
  #   pygame.display.flip()

  def update(self):
    imagen = self.cam.get_image()
    imagen = pygame.transform.scale(imagen, self.displaySize)
    self.display.blit(imagen, (0,0))
    pygame.display.update()

# end of class CamViewer

from app_class import AppClass
class CamAppClass(AppClass):
  def setup(self):
    AppClass.setup(self)

    pygame.init()
    pygame.camera.init()
    camlist = pygame.camera.list_cameras()
    if self.verbose:
      print 'found %d cameras: \n - %s' % (len(camlist), "\n - ".join(str(x) for x in camlist))

    self.viewer = None
    if camlist and len(camlist) > 0:
      self.viewer = CamViewer(devicePath=camlist[0], camSize=(480, 360), verbose=True)

  def start(self):
    if self.viewer == None:
      if self.verbose:
        print('No camera found, aborting...')
      self.destroy()
      return

    AppClass.start(self)

  def destroy(self):
    if self.viewer:
      self.viewer.destroy()

    AppClass.destroy(self)

  def update(self, dt=0.0):
    #self.viewer.get_and_flip()
    self.viewer.update()


# end of class CamAppClass

if __name__ == "__main__":
  app = CamAppClass(verbose=True)
  app.start()
