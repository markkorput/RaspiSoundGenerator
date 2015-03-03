import numpy as np
import struct

class MouseFileReader:
  xSensitivity = 1.0
  ySensitivity = 1.0
  x = 0.0
  y = 0.0
  bLeft = False
  bMiddle = False
  bRight = False

  def __init__(self):
    self.file = None
    self.setup()

  def __del__(self):
    if self.file != None:
      self.file.close()
      self.file = None

  def setup(self, path="/dev/input/mice"):
    self._path = path
    self.file = open( self._path, "rb" );

  def update(self):
    buf = self.file.read(3);
    button = ord( buf[0] );
    self.bLeft = button & 0x1;
    self.bMiddle = ( button & 0x4 ) > 0;
    self.bRight = ( button & 0x2 ) > 0;
    dx,dy = struct.unpack( "bb", buf[1:] );
    self.x = self.x + dx * self.xSensitivity
    self.y = self.y + dy * self.ySensitivity

