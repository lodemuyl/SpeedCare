import os
import sys
#toevoegen van deze pip3 lib aan python syspath zodat speedcare.service deze lib kan terugvinden.
sys.path.append('/home/pi/.local/lib/python3.5/site-packages')
import serial
from firebase_admin import credentials
from firebase_admin import db
import datetime
import time
#abspath
abspath = os.path.dirname(os.path.realpath(__file__))

#verschil tussen onze tijdszone en utc
lokaal = 1
#seriele interface voor ontvangen van gps data
si = "/dev/serial0"
#productnummer van de module
pk = '76846847687s'
#signaalsterkte
signaal = ['slecht','normaal', 'uitstekend']
#connectie naar gps module
ser = serial.Serial(si, 9600, timeout=0.5)
#knotsconvertfactor
factor = 1.85200
#firebase
cred = credentials.Certificate(os.path.join(abspath, 'key.json'))
uid = ''
#rmc&gga
lat = 0
lon = 0
snelheid = 0
sattelieten = 0
kwaliteit = ""
hoogte = 0
gewijzigdeparameters = 0
#leds
powerled = 27
runled = 17
errorled = 22
#autoritid
timenow = datetime.datetime.now()
autoritid = timenow.time()
#counter
counter = 0
#networktimeout
networktimeoutcounter = 0
#loginterval
loginterval = 3
#maxspeedpath
scriptdir = os.path.dirname(__file__)
rel_path = "maximumsnelheden.json"
maxspeedpath = os.path.join(scriptdir, rel_path)
#maxspeedapi
appid = 'bngQkvofptY6BhYwJqkR'
appcode = 'PiLtHYGTE1jPKNQuDp7xxw'
#gogolegeocodeapi
key = 'AIzaSyCjDB7jB1CqPueuUcUPXj1LBxMmob3iF1M'



