import utime
import util
from SolarPanelDisplay import SolarPanelDisplay
from SolarPlant import SolarPlant
from SunriseConnector import SunriseConnector
import config
import gc

class DisplayController:
    '''
    This class is the main class of the application. It is responsible for the main loop and the update interval of the display.
    '''
    def __init__(self):
        print("DisplayController: Init")
        self.solarPlant = SolarPlant(config.HISTORY_SIZE)
        self.solarPanelDisplay = SolarPanelDisplay(self.solarPlant, config.MIRROR_DISPLAY, config.ROTATE_DISPLAY)
        self.lastUpdate = utime.mktime(utime.localtime())
        self.sunrise = 0
        self.sunset = 0
        self.isDaytime = True
        print("DisplayController: Init done")

    def write_to_display(self):
        self.solarPanelDisplay.write_to_display()

    def updateSolarDisplay(self):
        '''
        This function updates the display with the current solar power production. But before it checks if its Daytime or Nighttime.
        Based on day or night it sets the update interval to night or day time update interval.
        '''
        print("updateSolarDisplay")

        ''' Get current time and sunrise and sunset time.'''
        now = utime.mktime(utime.localtime())

        ''' update display'''
        if (now > self.sunrise) and (now < self.sunset):
            print("daytime")
            if (now - self.lastUpdate) > config.DAYTIME_UPDATE_INTERVAL:
                self.lastUpdate = now
                self.write_to_display()
            else:
                print("Next update in " + str(120 - (now - self.lastUpdate)) + " seconds.")

        else:
            print("nighttime")
            if (now - self.lastUpdate) > config.NIGHTTIME_UPDATE_INTERVAL:
                self.lastUpdate = now
                self.write_to_display()

    def update_sunset(self):
        sunriseConnector = SunriseConnector(config.LOCATION_LATITUDE, config.LOCATION_LONGITUDE)
        self.sunrise = utime.mktime(util.parse_time_string(sunriseConnector.get_sunrise_sunset()['sunrise']))
        self.sunset = utime.mktime(util.parse_time_string(sunriseConnector.get_sunrise_sunset()['sunset']))

    def start_runner(self):
        while True:
            try:
                gc.collect()
                displayController.update_sunset()
                gc.collect()
                ''' Get solar Plant Consumtion and Production.'''
                self.solarPlant.update()
                displayController.updateSolarDisplay()
                gc.collect()
            except Exception as e:
                print("Exception: " + str(e))
            utime.sleep(config.DATA_UPDATE_INTERVAL)


if __name__ == '__main__':
    gc.collect()
    util.connect_to_wifi(config.WIFI_SSID, config.WIFI_PASSWORD)
    util.set_time()
    displayController = DisplayController()
    gc.collect()
    displayController.write_to_display()
    gc.collect()
    displayController.start_runner()

