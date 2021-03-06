SPEEDCARE
==================================

	speedcare/
	├── docs/
	├── vue/
	├── python/
	│	├── lib/
	│	├── app.py
	│	└── logfile.log
	└── README.md


## Info

- Contributor: **Lode Muylaert**
- Opleidingsonderdeel: **Bachelorproef**
- Academiejaar: **2017-2018**
- Opleiding: **Bachelor in de grafische en digitale media**
- Afstudeerrichting: **Multimediaproductie**
- Keuzeoptie: **New Media Development**
- Opleidingsinstelling: **Arteveldehogeschool**


## Hardware

- Raspberry Pi 3
- Ultimate GPS breakout adafruit V3
- external 3v GPS module
- Interface cable SMA to U.FL
- Small powerbank
- Jumpcables
- Leds
- Button
- Resistors

## Technische Tekening

![Speedcare](https://github.com/lodemuyl/SpeedCare/blob/master/docs/schema.png)

## Deploy

### Clone

```
$ git clone https://github.com/lodemuyl/SpeedCare.git speedcare
```

### Install required python packages

```
$ sudo apt-get update
```
```
$ pip3 install firebase_admin 
```
```
$ pip3 install logging
```

### Speedcare webapp

[https://speedcare.herokuapp.com/](https://speedcare.herokuapp.com/)


## Execute

Speedcare start automatisch bij het opstarten van de pi.

```
$ cd speedcare/python
```

```
$ python3 app.py
```
