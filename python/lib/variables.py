import serial
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime
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
cred = credentials.Certificate('./lib/key.json')
uid = ''
#rmc&gga
lat = 0
lon = 0
snelheid = 0
tijd = 0
kwaliteit = ""
hoogte = 0

