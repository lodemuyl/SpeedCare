from lib import variables
import datetime
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import socket
import logging

logging.basicConfig(filename='logfile.log',level=logging.DEBUG)

#utc naar lokale tijd
#def lokaletijd(utctijd):
    #huidiguur = datetime.datetime(100,1,1,utctijd.hour,utctijd.minute,utctijd.second) 
    #nieuwuur = huidiguur + datetime.timedelta(hours=variables.lokaal)
    #return nieuwuur.time()

#checkactive
def checkActive():
    network = checknetwork()
    if network:
        #firebase credentials
        firebase_admin.initialize_app(variables.cred, {
            'databaseURL' : 'https://speedcare-lode.firebaseio.com/'
        })
        checkproductkey = db.reference('Relations').get()
        try:
            if checkproductkey and checkproductkey[variables.pk]:
                variables.uid = checkproductkey[variables.pk].get('user')
                print('start')
                log('start')
                return True
        except Exception as inst:
            print('jouw pk is nog niet geactiveerd activeer hem nu op blablabla')
            log('pk not active')
            return False
    else:
        return False
    
#main function
def main(lines):
    if lines[0] == "GPRMC":
        printRMC(lines)
        pass
    elif lines[0] == "GPGGA":
        printGGA(lines)
        write()
        pass
    
#check internet connection
def checknetwork():
    try:
        socket.setdefaulttimeout(3)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        print('network')
        log('Network up')
        return True
    except Exception as ex:
        print('geen netwerk')
        log('Network down')
        return False

#logging
def log(message):
    now = datetime.datetime.now()
    logging.info(str(now) + ': ' + message)

#wegschrijven naar firebase
def write():
    #current time
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    currdate = str(day) +'/'+ str(month) +'/'+str(year)
    currtime = str(now.time())
    writeref = variables.uid + '/' + str(year) + '/' + str(month) + '/' + str(day) + '/' + currtime[:8]
    writedata = {
        "lat" : variables.lat,
        "lon" : variables.lon,
        "snelheid" : variables.snelheid,
        "signaal" : variables.kwaliteit,
        "hoogte" : variables.hoogte,
        "utc" : variables.tijd
        }
    write = db.reference(writeref)
    #print(write)
    write.push(writedata)

#ophalen van alle data afkomstig uit de ultimate gps module
def readString():
	while 1:
		while variables.ser.read().decode("utf-8") != '$': 
        		pass 
		line = variables.ser.readline().decode("utf-8") 
		return line
	    
#converteren van dateformat utc tijd
def getTime(string,format,returnFormat):
	new = time.strftime(returnFormat, time.strptime(string, format))
	return new

#lat en long
def getLatLng(latString,lngString):
	lat = latString[:2].lstrip('0') + "." + "%.7s" % str(float(latString[2:])*1.0/60.0).lstrip("0.")
	lng = lngString[:3].lstrip('0') + "." + "%.7s" % str(float(lngString[3:])*1.0/60.0).lstrip("0.")
	return lat,lng
    
#rmc
def printRMC(lines):
    latlng = getLatLng(lines[3],lines[5])
    variables.lat = latlng[0]
    variables.lon = latlng[1]
    variables.snelheid = speed(lines[7])	    
    print("Lat,Long                       :", variables.lat, lines[4], ", ", variables.lon, lines[6], sep='')
    print("Snelheid                       :", variables.snelheid)	
    return
    
#knots to kmph
def speed(knots):
    kmph = float(knots)*variables.factor
    return kmph

#gga
def printGGA(lines):
    #print("tijd                           :", getTime(lines[1], "%H%M%S.%f", "%H:%M:%S"), "UTC")
    variables.tijd = getTime(lines[1], "%H%M%S.%f", "%H:%M:%S")
    variables.kwaliteit = variables.signaal[int(lines[6])]
    variables.hoogte = lines[9]
    print("tijd                           :", variables.tijd , "UTC")
    print("Kwaliteit signaal              :", variables.kwaliteit)
    print("Hoogte                         :", variables.hoogte, lines[10],sep="")
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
		return False
	
	if checksum == inputChecksum:
		return True
	else:
		print("=====================================================================================")
		print("===================================error!============================================")
		print("=====================================================================================")
		print(hex(checksum), "!=", hex(inputChecksum))
		log('Checksum error')
		return False