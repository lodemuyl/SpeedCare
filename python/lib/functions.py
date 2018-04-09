from lib import variables
import datetime
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import socket
import os
import logging
import RPi.GPIO as GPIO
import urllib.request
import urllib.parse
import json
import sys

GPIO.setmode(GPIO.BCM)
logdir = os.path.dirname(__file__)
logname = "speedcarelog.log"
abslogname = os.path.join(logdir, logname)
logging.basicConfig(filename=abslogname,level=logging.DEBUG)
GPIO.setwarnings(False)

#main function
def main(lines):
    if lines[0] == "GPRMC":
        printRMC(lines)
        pass
    elif lines[0] == "GPGGA":
        printGGA(lines)
        if variables.gewijzigdeparameters >= 6:
            write()            
        pass     
#init firebase
def initfirebase():
    firebase_admin.initialize_app(variables.cred, {
    'databaseURL' : 'https://speedcare-lode.firebaseio.com/',
    'httpTimeout' : 1
    })
#checkactive
def checkActive():
    network = True
    #network = checknetwork()
    if network:
        #firebase credentials
        initfirebase()
        checkproductkey = db.reference('Relations').get()
        try:
            if checkproductkey and checkproductkey[variables.pk]:
                variables.uid = checkproductkey[variables.pk].get('user')
                print('start')
                log('start')
                GPIO.setup(variables.errorled, GPIO.OUT)
                GPIO.output(variables.errorled, GPIO.LOW)
                GPIO.setup(variables.runled, GPIO.OUT)
                GPIO.output(variables.runled,GPIO.HIGH)
                return True
        except Exception as exactive:
            print('jouw pk is nog niet geactiveerd of bestaat niet')
            log('message : ' + str(exactive))
            log('pk not active')
            GPIO.setup(variables.errorled, GPIO.OUT)
            GPIO.output(variables.errorled, GPIO.HIGH)
            return False
    else:
        GPIO.setup(variables.errorled, GPIO.OUT)
        GPIO.output(variables.errorled, GPIO.HIGH)
        return False
    
#check internet connection      
def checknetwork():
    try:
        #socket.setdefaulttimeout(3)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        #print('network')
        log('Network up')
        return True
    except Exception as exnetwork:
        #print('Geen netwerk')
        #log('message : ' + str(exnetwork))
        log('Network down' + str(exnetwork))
        #GPIO.setup(variables.errorled, GPIO.OUT)
        #GPIO.output(variables.errorled, GPIO.HIGH)
        return False
#logging
def log(message):
    now = datetime.datetime.now()
    logging.info(str(now) + ': ' + message)

#ophalen maximumsnelheden
def getSpeedLimit(lat, lon):
    try:
        url = 'http://reverse.geocoder.cit.api.here.com/6.2/reversegeocode.json?locationattributes=linkInfo&prox='+str(lat)+'%2C'+str(lon)+'%2C61&mode=retrieveAddresses&maxresults=1&&app_id='+str(variables.appid)+'&app_code='+str(variables.appcode)
        f = urllib.request.urlopen(url)
        g = f.read().decode('utf-8')
        fulljson = json.loads(g)
        category = fulljson["Response"]["View"][0]["Result"][0]['Location']['LinkInfo']['SpeedCategory']    
        gg = json.loads(open(variables.maxspeedpath).read())
        if category == 'SC2' or category == 'SC3' or category == 'SC4' or category == 'SC5' or category == 'SC6' or category == 'SC7' or category == 'SC8':
            return gg[category]        
        else:
            return gg['SC2']
    except Exception as Exspeed:
        return False
    
#ophalen maximumsnelheden
def getViolationLocation(lat, lng):
    try:
        url = 'https://maps.googleapis.com/maps/api/geocode/json?key='+str(variables.key)+'&latlng='+str(lat)+','+str(lng)
        f = urllib.request.urlopen(url)
        g = f.read().decode('utf-8')
        fulljson = json.loads(g)
        if fulljson["status"] == "OK":
            adres = fulljson['results'][0]['formatted_address']
            ac = fulljson['results'][0]['address_components']
            nummer = ac[0]['long_name']
            straatnaam = ac[1]['long_name']
            gemeente = ac[2]['long_name']
            provincie = ac[3]['long_name']
            land = ac[5]['long_name']
            postcode = ac[6]['long_name']
            obj = {
                "straat" : straatnaam,
                "nummer" : nummer,
                "postcode" : postcode,
                "gemeente" : gemeente,
                "provincie" : provincie,
                "land" : land
                }
            return obj
        else:
            log('message : fout bij het ophalen violationlocation')
            return False
    except Exception as ex:
       log('message : ' + str(ex))
       print('message : fout bij het ophalen violationlocation')
       return False
        
#wegschrijven naar firebase
def write():
    try:
        #logging om de 3 seconden
        if variables.counter % variables.loginterval == 0:
            #current time
            speedlim = getSpeedLimit(variables.lat,variables.lon)
            if speedlim:
                variables.networktimeoutcounter = 0
                now = datetime.datetime.now()
                year = now.year
                month = now.month
                day = now.day
                currdate = str(day) +'/'+ str(month) +'/'+str(year)
                currtime = str(now.time())
                writeref = variables.uid + '/' + str(year) + '/' + str(month) + '/' + str(day) + '/' + str(variables.autoritid)[:8] + '/' + currtime[:8]
                writedata = {
                    "lat" : variables.lat,
                    "lon" : variables.lon,
                    "snelheid" : variables.snelheid,
                    "maxsnelheid" : str(speedlim),
                    "signaal" : variables.kwaliteit,
                    "sattelieten": variables.sattelieten,
                    }
                if variables.snelheid > speedlim:
                    violation = getViolationLocation(variables.lat, variables.lon)
                    if violation:
                        writedata["overtreding"] = violation
                    else:
                        writedata["overtreding"] = "kon locatie van overtreding niet ophalen"
                write = db.reference(writeref)
                write.push(writedata)
            elif not speedlim:
                if checknetwork():
                    log('message : speedlimitation error')
                    print('speedlimitation error')
                    GPIO.output(variables.errorled, GPIO.OUT)
                    GPIO.output(variables.errorled, GPIO.HIGH)
                    sys.exit(1)
                elif not checknetwork():
                    print('!!!' + str(variables.networktimeoutcounter) + 'seconden timeout')
                    log('message : networkdown since' + str(variables.networktimeoutcounter) + ' seconds')
                    if variables.networktimeoutcounter == 15:
                        print('networktimeout expired')
                        raise Exception('networktimeout expired')
                    variables.networktimeoutcounter += variables.loginterval
        variables.counter += 1
    except Exception as exwrite:
        log('message : ' + str(exwrite))
        print('timeout van ' + str(variables.networktimeoutcounter))
        GPIO.setup(variables.errorled, GPIO.OUT)
        GPIO.output(variables.errorled, GPIO.HIGH)
        GPIO.setup(variables.runled, GPIO.OUT)
        GPIO.output(variables.runled, GPIO.LOW)
        sys.exit(1)

#ophalen van alle data afkomstig uit de ultimate gps module
def readString():
	while 1:
		while variables.ser.read().decode("utf-8") != '$': 
        		pass 
		line = variables.ser.readline().decode("utf-8") 
		return line
	    
#converteren van dateformat utc tijd
#def getTime(string,format,returnFormat):
#	new = time.strftime(returnFormat, time.strptime(string, format))
#	return new

#lat en long
def getLatLng(latString,lngString):
	lat = latString[:2].lstrip('0') + "." + "%.7s" % str(float(latString[2:])*1.0/60.0).lstrip("0.")
	lng = lngString[:3].lstrip('0') + "." + "%.7s" % str(float(lngString[3:])*1.0/60.0).lstrip("0.")
	return lat,lng
    
#rmc
def printRMC(lines):
    if lines:
        variables.gewijzigdeparameters += 3
        latlng = getLatLng(lines[3],lines[5])
        variables.lat = latlng[0]
        variables.lon = latlng[1]
        variables.snelheid = speed(lines[7])
        print("")
        print("")
        print("Lat,Long                       :", variables.lat, lines[4], ", ", variables.lon, lines[6], sep='')
        print("Snelheid                       :", variables.snelheid)
        return
    
#knots to kmph
def speed(knots):
    kmph = float(knots)*variables.factor
    return kmph

#gga
def printGGA(lines):
    if lines:
        variables.gewijzigdeparameters += 3
        #variables.tijd = getTime(lines[1], "%H%M%S.%f", "%H:%M:%S")
        variables.kwaliteit = variables.signaal[int(lines[6])]
        variables.hoogte = lines[9]
        variables.sattelieten = lines[7]
        print("Kwaliteit signaal              :", variables.kwaliteit)
        print("Hoogte                         :", variables.hoogte, lines[10],sep="")
        print("Aantal sattelieten             :", variables.sattelieten)
        print("")
        print("")
        return

#checksum 
def checksum(line):
	checkString = line.partition("*")
	checksum = 0
	for c in checkString[0]:
		checksum ^= ord(c)

	try: 
		inputChecksum = int(checkString[2].rstrip(), 16);
	except:
		print("Error in string")
		log('error in string')
		GPIO.setup(variables.errorled, GPIO.OUT)
		GPIO.output(variables.errorled, GPIO.HIGH)
		return False
	
	if checksum == inputChecksum:
		return True
	else:
		print("=====================================================================================")
		print("===================================error!============================================")
		print("=====================================================================================")
		print(hex(checksum), "!=", hex(inputChecksum))
		log('Checksum error')
		GPIO.setup(variables.errorled, GPIO.OUT)
		GPIO.output(variables.errorled, GPIO.HIGH)
		return False