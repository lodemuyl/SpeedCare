#imports
import os
import sys
import serial
#import pynmea2
import datetime
import logging
import RPi.GPIO as GPIO
#abs path

abspath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(abspath)
#libpath = os.path.join(abspath, 'lib')

#variables
from lib import variables
#functies
from lib import functions
#check active
active = functions.checkActive()

#mainloop
try:
    while active:
            line = functions.readString()
            lines = line.split(",")
            if functions.checksum(line):
                functions.main(lines)
except:
    print('afsluiten')
    functions.log('close')
    GPIO.setup(variables.runled, GPIO.OUT)
    GPIO.output(variables.runled, GPIO.LOW)
