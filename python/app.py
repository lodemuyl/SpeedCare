#imports
import serial
import pynmea2
import datetime
from ISStreamer.Streamer import Streamer
#variables
from lib import variables
#functies
from lib import functions 

serialStream = serial.Serial(variables.si, 9600, timeout=0.5)
#try:
#	while True:
#		sentence = serialStream.readline()
#		if b'GGA' in sentence:
#			data = pynmea2.parse(sentence.decode("utf-8"))
#			streamer.log("Locatie", "{lat},{lon}".format(lat=data.latitude,lon=data.longitude))
#			streamer.log("Hoogte ({unit})".format(unit=data.altitude_units), data.altitude)
#		if b'RMC' in sentence:
#			data = pynmea2.parse(sentence.decode("utf-8"))
#			tijd = functions.lokaletijd(data.timestamp)
#			streamer.log("Tijd", "{datum},{time}".format(datum=data.datetime.strftime('%d/%m/%Y'), time=tijd))			
#except KeyboardInterrupt:
#	streamer.close()

#main while true loop
try:
    while True:
            sentence = serialStream.readline()
            if b'GGA' in sentence:
                data = pynmea2.parse(sentence.decode("utf-8"))
                tijd = functions.lokaletijd(data.timestamp)
                #print ("{time}: {lat},{lon}".format(time=tijd,lat=data.latitude,lon=data.longitude))
            if b'RMC' in sentence:
                data = pynmea2.parse(sentence.decode("utf-8"))
                #print ("datum is {tijd}".format(tijd = data.datetime.strftime('%d/%m/%Y')))
                print(data[7])
except KeyboardInterrupt:
	streamer.close()
