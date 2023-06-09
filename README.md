# Solar Panel Display

## Introduction
This repository contains the code for a solar panel monitoring display. 
It is a simple display that shows the current power output of your solar panela. 
The project is based on a ESP8266 and a 1.54" e-Paper display from waveshare.

<img src="https://github.com/marfraTUC/micropython_solar_panel/blob/main/Accompanying%20Files%20/display.jpeg?raw=true" alt="display" width="200"/>

### What works
- Displaying data on the screen
- Updating the screen
- Fetching data from a API to change display update intervalls based on day/night
- Connecting to a WiFi network
- Connecting to a the inverter to fetch data from it

### What doesn't work yet
- Rotating the Screen
- Automatic updates in intervalls

### Hardware
* Waveshare ESP8266
* Waveshare 1.54" e-Paper Display

<img src="https://github.com/marfraTUC/micropython_solar_panel/blob/main/Accompanying%20Files%20/hardware.jpeg?raw=true" alt="hardware" width="200"/>


### Software
* MicroPython 1.9.4


## Getting Started
- check out repo
- create a config.py file with the following content in root:
```python
WIFI_SSID="your ssid"
WIFI_PASSWORD="your password"
WIFI_COUNTRY="YOUT_CONTRY_CODE"
DAYTIME_UPDATE_INTERVAL=180000 # 3 min
NIGHTTIME_UPDATE_INTERVAL=1800000 # 30 min
HISTORY_SIZE=200
LOCATION_LATITUDE=YOUR_LATITUDE
LOCATION_LONGITUDE=YOUR_LONGITUTE
SUNRISE_API="https://api.sunrise-sunset.org/json?lat="
SUNRISE_UPDATE_INTERVAL=43200000 # 12 hours
MIRROR_DISPLAY=True
ROTATE_DISPLAY=const(90)
```
- adjust the config.py to your needs
- upload all files ```*.py``` files to the ESP8266
