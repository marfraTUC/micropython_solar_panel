import utime
from machine import Timer
import util
from SolarPanelDisplay import SolarPanelDisplay
from SolarPlant import SolarPlant
#from SunriseConnector import SunriseConnector
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
        #self.sunriseConnector = SunriseConnector(config.LOCATION_LATITUDE, config.LOCATION_LONGITUDE)
        #self.display_timer = Timer(-1)
        #display_timer.init(period=180000, mode=Timer.PERIODIC, callback=self.updateSolarDisplay)
        #self.display_timer.init(period=30000, mode=Timer.PERIODIC, callback=self.updateSolarDisplay)
        self.isDaytime = True
        print("DisplayController: Init done")

    def write_to_display(self):
        self.solarPanelDisplay.write_to_display()

    def updateSolarDisplay(self, timer):
        '''
        This function updates the display with the current solar power production. But before it checks if its Daytime or Nighttime.
        Based on day or night it sets the update interval to night or day time update interval.
        '''
        print("updateSolarDisplay")
        gc.collect()

        ''' Get current time and sunrise and sunset time.'''
        now = utime.mktime(utime.localtime())
        sunrise = utime.mktime(util.parse_time_string(self.sunriseConnector.get_sunrise_sunset()['sunrise']))
        sunset = utime.mktime(util.parse_time_string(self.sunriseConnector.get_sunrise_sunset()['sunset']))

        ''' Get solar Plant Consumtion and Production.'''
        self.solarPlant.update()

        ''' update display'''
        if (now > sunrise) and (now < sunset):
            print("daytime")
            if (now - self.lastUpdate) > 120:
                self.lastUpdate = now
                self.write_to_display()
        else:
            print("nighttime")
            if (now - self.lastUpdate) > 1200:
                self.lastUpdate = now
                self.write_to_display()


if __name__ == '__main__':
    util.connect_to_wifi(config.WIFI_SSID, config.WIFI_PASSWORD)
    util.set_time()
    gc.collect()
    displayController = DisplayController()
    gc.collect()
    displayController.write_to_display()
    gc.collect()
#    display_timer = Timer(-1)
#    display_timer.init(period=180000, mode=Timer.PERIODIC, callback=displayController.updateSolarDisplay)

