#imports
import os
import sys
import time
import serial
import datetime
import logging
import RPi.GPIO as GPIO
#add lib to sys path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib'))
#variables
import variables
#add lib to sys path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib'))
#functies
import functions
#check active
active = functions.checkActive()
time.sleep(3)
#mainloop
try:
    while active:
            line = functions.readString()
            lines = line.split(",")            
            functions.main(lines)
except (KeyboardInterrupt, SystemExit):
    GPIO.setup(variables.runled, GPIO.OUT)
    GPIO.output(variables.runled, GPIO.LOW)
    raise
except Exception as ex:
    functions.logging.info('close :' + str(ex))
    GPIO.setup(variables.runled, GPIO.OUT)
    GPIO.output(variables.runled, GPIO.LOW)