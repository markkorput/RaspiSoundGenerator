#!/usr/bin/env python
#
# Raspberry Pi Rotary Encoder Class
# $Id: rotary_class.py,v 1.2 2014/01/14 07:30:07 bob Exp $
#
# Author : Bob Rathbone
# Site : http://www.bobrathbone.com
#
# This class uses standard rotary encoder with push switch
#
#
import RPi.GPIO as GPIO

class RotaryEncoder:
  CLOCKWISE=1
  ANTICLOCKWISE=2
  BUTTONDOWN=3
  BUTTONUP=4
  rotary_a = 0
  rotary_b = 0
  rotary_c = 0
  last_state = 0
  direction = 0

  # Initialise rotary encoder object
  def __init__(self,pinA=14,pinB=15,button=None,callback=None,verbose=False):
    self.pinA = pinA
    self.pinB = pinB
    self.button = button
    self.callback = callback
    self.verbose = verbose
    GPIO.setmode(GPIO.BCM)
    # The following lines enable the internal pull-up resistors
    # on version 2 (latest) boards
    GPIO.setwarnings(False)
    GPIO.setup(self.pinA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(self.pinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    if self.button != None:
      GPIO.setup(self.button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # For version 1 (old) boards comment out the above four lines
    # and un-comment the following 3 lines
    #GPIO.setup(self.pinA, GPIO.IN)
    #GPIO.setup(self.pinB, GPIO.IN)
    #if self.button != None:
    #  GPIO.setup(self.button, GPIO.IN)
    # Add event detection to the GPIO inputs
    GPIO.add_event_detect(self.pinA, GPIO.FALLING, callback=self.switch_event)
    GPIO.add_event_detect(self.pinB, GPIO.FALLING, callback=self.switch_event)
    if self.button != None:
      GPIO.add_event_detect(self.button, GPIO.BOTH, callback=self.button_event, bouncetime=200)
    return

  # Call back routine called by switch events
  def switch_event(self,switch):
    if GPIO.input(self.pinA):
      self.rotary_a = 1
    else:
      self.rotary_a = 0

    if GPIO.input(self.pinB):
      self.rotary_b = 1
    else:
      self.rotary_b = 0

    self.rotary_c = self.rotary_a ^ self.rotary_b
    new_state = self.rotary_a * 4 + self.rotary_b * 2 + self.rotary_c * 1
    delta = (new_state - self.last_state) % 4
    self.last_state = new_state
    event = 0
    
    if delta == 1:
      if self.direction == self.CLOCKWISE:
        if self.verbose:
          print "Clockwise"
        event = self.direction
      else:
        self.direction = self.CLOCKWISE
    elif delta == 3:
      if self.direction == self.ANTICLOCKWISE:
        if self.verbose:
          print "Anticlockwise"
        event = self.direction
      else:
        self.direction = self.ANTICLOCKWISE
    
    if event > 0 and self.callback != None:
      self.callback(event)

    return

    # Push button event
    def button_event(self,button):
      if GPIO.input(button):
        event = self.BUTTONUP
      else:
        event = self.BUTTONDOWN
    
    if self.callback != None:
      self.callback(event)
    return

    # Get a switch state
    def getSwitchState(self, switch):
      return GPIO.input(switch)

# End of RotaryEncoder class

#
#
#


#!/usr/bin/env python
#
# Raspberry Pi Rotary Test Encoder Class
#
# Author : Bob Rathbone
# Site : http://www.bobrathbone.com
#
# This class uses a standard rotary encoder with push switch
#
import sys
import time
# from rotary_class import RotaryEncoder

# Define GPIO inputs
PIN_A = 15 # Pin 8
PIN_B = 14 # Pin 10
# BUTTON = 4 # Pin 7

# This is the event callback routine to handle events
def print_event(event):
  print "global printer"
  if event == RotaryEncoder.CLOCKWISE:
    print "[%.2f] Clockwise" % time.clock()
  elif event == RotaryEncoder.ANTICLOCKWISE:
    print "[%.2f] Anticlockwise" % time.clock()
  # elif event == RotaryEncoder.BUTTONDOWN:
  #   print "Button down"
  # elif event == RotaryEncoder.BUTTONUP:
  #   print "Button up"

  return

def main():
  # Define the switch
  rswitch = RotaryEncoder(PIN_A,PIN_B,None,None,True) # verbose == True
  while True:
    time.sleep(0.05)

if __name__ == "__main__":
  main()

