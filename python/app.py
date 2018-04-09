#imports
import os
import sys
import serial
import datetime
import logging
import RPi.GPIO as GPIO
#add lib to sys path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib'))
#variables
import variables
#functies
import functions
#check active
active = functions.checkActive()

#mainloop
try:
    while active:
            line = functions.readString()
            lines = line.split(",")
            if functions.checksum(line):
                functions.main(lines)
except Exception as ex:
    functions.log('close' + str(ex))
    GPIO.setup(variables.runled, GPIO.OUT)
    GPIO.output(variables.runled, GPIO.LOW)
