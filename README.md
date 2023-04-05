# Solar Panel Display

This repository contains the code for a solar panel display. 
It is a simple display that shows the current power output of a solar panel. 
The project is based on a ESP8266 and a 1.54" e-Paper display from waveshare.

## What works
- Displaying data on the screen
- Updating the screen
- Fetching data from a API to change display update intervalls based on day/night
- Connecting to a WiFi network

## What doesn't work
- Connecting to a the inverter to fetch data from it


## Installation
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
```
- upload all files to the ESP8266
