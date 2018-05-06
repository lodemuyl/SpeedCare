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
logging.basicConfig(filename=abslogname,level=logging.DEBUG, format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')
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
    try:
        firebase_admin.initialize_app(variables.cred, {
        'databaseURL' : 'https://speedcare-lode.firebaseio.com/',
        'httpTimeout' : False
        })
        variables.init = True
    except (KeyboardInterrupt, SystemExit):
        GPIO.setup(variables.runled, GPIO.OUT)
        GPIO.output(variables.runled, GPIO.LOW)
        sys.exit(1)
    except Exception as active:
        logging.info('message : initprobleem' + str(active))
        GPIO.setup(variables.errorled, GPIO.OUT)
        GPIO.output(variables.errorled, GPIO.HIGH)
        return False
#checkactive
def checkActive():
    network = checknetwork()
    if network:
        try:
            if(variables.init == False):            
                #firebase credentials
                initfirebase()
                checkproductkey = db.reference('Relations').get()        
            if checkproductkey and checkproductkey[variables.pk]:
                variables.uid = checkproductkey[variables.pk].get('user')
                print('start')
                logging.info('start')
                GPIO.setup(variables.errorled, GPIO.OUT)
                GPIO.output(variables.errorled, GPIO.LOW)
                GPIO.setup(variables.runled, GPIO.OUT)
                GPIO.output(variables.runled,GPIO.HIGH)                
                return True
        except (KeyboardInterrupt, SystemExit):
            GPIO.setup(variables.runled, GPIO.OUT)
            GPIO.output(variables.runled, GPIO.LOW)
            sys.exit(1)
        except Exception as active:
            print('jouw pk is nog niet geactiveerd of bestaat niet')
            logging.info('jouw pk is nog niet geactiveerd of bestaat niet' + str(active))            
            GPIO.setup(variables.errorled, GPIO.OUT)
            GPIO.output(variables.errorled, GPIO.HIGH)
            return False
    else:        
        logging.info('network down')
        GPIO.setup(variables.errorled, GPIO.OUT)
        GPIO.output(variables.errorled, GPIO.HIGH)
        return False
    
#check internet connection      
def checknetwork():
    try:        
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        if variables.counter == 0:
            logging.info('Network up')
        return True
    except (KeyboardInterrupt, SystemExit):
        GPIO.setup(variables.runled, GPIO.OUT)
        GPIO.output(variables.runled, GPIO.LOW)
        sys.exit(1)
    except Exception as exnetwork:
        logging.info('Network down' + str(exnetwork))
        return False
  
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
    except (KeyboardInterrupt, SystemExit):
        GPIO.setup(variables.runled, GPIO.OUT)
        GPIO.output(variables.runled, GPIO.LOW)
        sys.exit(1)
    except Exception as Exspeed:
        logging.info('message : speedlimerror' + str(Exspeed))
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
            logging.info('message : fout bij het ophalen violationlocation')
            return False
    except (KeyboardInterrupt, SystemExit):
        GPIO.setup(variables.runled, GPIO.OUT)
        GPIO.output(variables.runled, GPIO.LOW)
        sys.exit(1)
    except Exception as ex:
       logging.info('message : ' + str(ex))
       print('message : fout bij het ophalen violationlocation')
       return False
        
#wegschrijven naar firebase
def write():    
    try:
        #logging om de 3 seconden
        if variables.counter % variables.loginterval == 0:
            #current time
            connectioncheck = checknetwork()            
            if connectioncheck:
                if variables.gps:
                    variables.networktimeoutcounter = 0                
                    speedlim = getSpeedLimit(variables.lat,variables.lon)                
                    now = datetime.datetime.now()
                    year = now.year
                    month = now.month
                    day = now.day
                    currdate = str(day) +'/'+ str(month) +'/'+str(year)
                    currtime = str(now.time())
                    #refs
                    writeref = variables.uid + '/' + str(year) + '/' + str(month) + '/' + str(day) + '/' + str(variables.autoritid)[:8] + '/' + currtime[:8]
                    writerefovertredingen = variables.uid + '/' + 'overtredingen' + '/' + str(year) + '/' + str(month) + '/' + str(day) + '/' + str(variables.autoritid)[:8] + '/' + currtime[:8]
                    writeaantalritten = variables.uid + '/' + 'aantalritten' + '/' + str(year) + '/' + str(month)
                    writeaantalovertredingen = variables.uid + '/' + 'aantal overtredingen' + '/' + str(year) + '/' + str(month)
                    #data die moet worden weggeschreven bijd e gewone logs
                    writedata = {
                        "lat" : variables.lat,
                        "lon" : variables.lon,
                        "snelheid" : variables.snelheid,
                        "maxsnelheid" : str(speedlim),
                        "signaal" : variables.kwaliteit,
                        "sattelieten" : variables.sattelieten,
                        }
                    #overtredingen wegschrijven
                    if variables.snelheid > speedlim:
                        violation = getViolationLocation(variables.lat, variables.lon)
                        violation["werkelijkesnelheid"] = variables.snelheid
                        violation["maximumsnelheid"] = speedlim
                        violation["tesnel"] = variables.snelheid - speedlim
                        violation["lat"] = variables.lat
                        violation["lng"] = variables.lon
                        connectieovertredingen = db.reference(writerefovertredingen)
                        connectieaantalovertredingen = db.reference(writeaantalovertredingen)
                        def updateovertredingen(current):
                            return current + 1 if current else 1
                        connectieaantalovertredingen.transaction(updateovertredingen)
                        if violation:
                            writedata["overtreding"] = True
                            connectieovertredingen.push(violation)
                        else:
                            writedata["overtreding"] = True
                            connectieovertredingen.push("Kon locatie niet ophalen.")
                    #increment van aantalritten en aantal overtredingen bij 1e tick
                    if variables.counter == 0:                    
                        connectieaantalritten = db.reference(writeaantalritten)                
                        def updateritten(current):
                            return current + 1 if current else 1                        
                        connectieaantalritten.transaction(updateritten)
                    #gewone logs wegschrijven
                    write = db.reference(writeref)
                    write.push(writedata)
                else:
                    pass
            elif not connectioncheck:
                print('!!!' + str(variables.networktimeoutcounter) + 'seconden timeout')
                logging.info('message : networkdown since' + str(variables.networktimeoutcounter) + ' seconds')
                if variables.networktimeoutcounter == variables.timeouttime:
                    print('networktimeout expired')
                    raise Exception('networktimeout expired')
                variables.networktimeoutcounter += variables.loginterval
        variables.counter += 1
    except (KeyboardInterrupt, SystemExit):
        GPIO.setup(variables.runled, GPIO.OUT)
        GPIO.output(variables.runled, GPIO.LOW)
        sys.exit(1)
    except Exception as exwrite:
        logging.info('message : ' + str(exwrite))
        print('timeout van ' + str(variables.networktimeoutcounter))
        GPIO.setup(variables.errorled, GPIO.OUT)
        GPIO.output(variables.errorled, GPIO.HIGH)
        GPIO.setup(variables.runled, GPIO.OUT)
        GPIO.output(variables.runled, GPIO.LOW)
        sys.exit(1)

#ophalen van alle data afkomstig uit de ultimate gps module
def readString():
    try:
        while 1:
            while variables.ser.read().decode("utf-8") != '$':
                pass
            line = variables.ser.readline().decode("utf-8")
            return line
    except Exception as ex:
        logging.info('message : ' + str(ex))
        print('message : no gps stream')
        GPIO.setup(variables.errorled, GPIO.OUT)
        GPIO.output(variables.errorled, GPIO.HIGH)
        GPIO.setup(variables.runled, GPIO.OUT)
        GPIO.output(variables.runled, GPIO.LOW)
        sys.exit(1)
#lat en long
def getLatLng(latString,lngString):
    degr = 1.0/60.0
    latstr = latString[:2]
    lngstr = lngString[:3]
    lat = latstr.lstrip('0') + "." + "%.7s" % str((float(latstr)*degr)).lstrip("0.")
    lng = lngstr.lstrip('0') + "." + "%.7s" % str((float(lngstr)*degr)).lstrip("0.")
    return lat,lng
    
#rmc
def printRMC(lines):
    try:
        if not (str(lines[0]) == "" or str(lines[1]) == "" or str(lines[3]) == "" or str(lines[5]) == ""):
            variables.gewijzigdeparameters = float(variables.gewijzigdeparameters) + 3            
            latlng = getLatLng(lines[3],lines[5])
            variables.lat = float(latlng[0])
            variables.lon = float(latlng[1])
            variables.snelheid = speed(float(lines[7]))
            print("")
            print("")
            print("Lat,Long                       :", variables.lat, lines[4], ", ", variables.lon, lines[6], sep='')
            print("Snelheid                       :", variables.snelheid)
            variables.gps = True
            return
        else:
            logging.info('message : no rmc lines')            
            pass
    except Exception as ex:
        logging.info('message : ' + str(ex))
        print('message : ex rmc lines')
        GPIO.setup(variables.errorled, GPIO.OUT)
        GPIO.output(variables.errorled, GPIO.HIGH)
        GPIO.setup(variables.runled, GPIO.OUT)
        GPIO.output(variables.runled, GPIO.LOW)
        sys.exit(1)
    
#knots to kmph
def speed(knots):
    kmph = float(knots)*variables.factor
    return kmph

#gga
def printGGA(lines):
    try:
        if not (str(lines[6]) == "" or str(lines[7]) == "" or str(lines[9]) == ""):
            variables.gewijzigdeparameters = float(variables.gewijzigdeparameters) + 3
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
        else:
            logging.info('message : no gga lines')
            pass
    except Exception as ex:
        logging.info('message : ' + str(ex))
        print('message : gga exeption')
        GPIO.setup(variables.errorled, GPIO.OUT)
        GPIO.output(variables.errorled, GPIO.HIGH)
        GPIO.setup(variables.runled, GPIO.OUT)
        GPIO.output(variables.runled, GPIO.LOW)
        sys.exit(1)


