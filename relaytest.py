print(" Control + C to exit Program")

import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)    # the pin numbers refer to the board connector not the chip
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT)     # sets the pin input/output setting to OUT
GPIO.output(4, GPIO.HIGH)   # sets the pin output to high

try:
  while 1 >=0:
    GPIO.output(4, GPIO.LOW)   # turns the first relay switch ON
    time.sleep(.5)             # pauses system for 1/2 second
    GPIO.output(4, GPIO.HIGH)  # turns the first relay switch OFF
    time.sleep(.5)

except KeyboardInterrupt:     # Stops program when "Control + C" is entered
  GPIO.cleanup()               # Turns OFF all relay switches
