import struct

file = open( "/dev/input/mice", "rb" );

mouseSensitivity = 0.5
value = 0.0

def getMouseEvent():
  buf = file.read(3);
  button = ord( buf[0] );
  bLeft = button & 0x1;
  bMiddle = ( button & 0x4 ) > 0;
  bRight = ( button & 0x2 ) > 0;
  x,y = struct.unpack( "bb", buf[1:] );
  # print ("L:%d, M: %d, R: %d, x: %d, y: %d\n" % (bLeft,bMiddle,bRight, x, y) );
  if( y!=0 ):
    global value, mouseSensitivity
    value += y * mouseSensitivity
    print ("Value: %d (%d)" % (value, y))
  # return stuffs

while( 1 ):
  getMouseEvent();

file.close();

