#!/user/bin/env python

import RPi.GPIO as GPIO, time

timeout = 10000
total = 0
DEBUG = 1
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def CapRead(inPin,outPin):
    total = 0
    
    # set Send Pin Register low
    GPIO.setup(outPin, GPIO.OUT)
    GPIO.output(outPin, GPIO.LOW)
    
    # set receivePin Register low to make sure pullups are off 
    GPIO.setup(inPin, GPIO.OUT)
    GPIO.output(inPin, GPIO.LOW)
    GPIO.setup(inPin, GPIO.IN)
    
    # set send Pin High
    GPIO.output(outPin, GPIO.HIGH)
    
    # while receive pin is LOW AND total is positive value
    while( GPIO.input(inPin) == GPIO.LOW and total < timeout ):
        total+=1
    
    if ( total > timeout ):
        return -2 # total variable over timeout
        
     # set receive pin HIGH briefly to charge up fully - because the while loop above will exit when pin is ~ 2.5V 
    GPIO.setup( inPin, GPIO.OUT )
    GPIO.output( inPin, GPIO.HIGH )
    GPIO.setup( inPin, GPIO.IN )
    
    # set send Pin LOW
    GPIO.output( outPin, GPIO.LOW ) 

    # while receive pin is HIGH  AND total is less than timeout
    while (GPIO.input(inPin)==GPIO.HIGH and total < timeout) :
        total+=1
    
    if ( total >= timeout ):
        return -2
    else:
        return total


if __name__ == "__main__":
    # loop
    while True:
        total = 0
        for j in range(0,10):
            total += CapRead(17,18);

        str = ""
        for j in range(0, int(total / 10.0)):
            str += "#"
        print str + " - total: %d" % (total)
  
    # clean before you leave
    GPIO.cleanup()
