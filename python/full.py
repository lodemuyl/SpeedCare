#imports
import serial
import pynmea2
import datetime
import logging

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
