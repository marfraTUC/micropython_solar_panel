from machine import Timer

import utime
import util
from SolarPanelDisplay import SolarPanelDisplay
from SolarPlant import SolarPlant
from SunriseConnector import SunriseConnector
import config

class DisplayController:
    '''
    This class is the main class of the application. It is responsible for the main loop and the update interval of the display.
    '''
    def __init__(self):
        self.solarPlant = SolarPlant(config.HISTORY_SIZE)
        self.solarPanelDisplay = SolarPanelDisplay(self.solarPlant, config.MIRROR_DISPLAY, config.ROTATE_DISPLAY)
        self.sunriseConnector = SunriseConnector(config.LOCATION_LATITUDE, config.LOCATION_LONGITUDE)
        self.display_timer = Timer(-2)
        # display_timer.init(period=180000, mode=Timer.PERIODIC, callback=self.updateSolarDisplay)
        # self.display_timer.init(period=1800, mode=Timer.PERIODIC, callback=self.updateSolarDisplay)
        self.isDaytime = True

    def write_to_display(self):
        self.solarPanelDisplay.write_to_display()

    def updateSolarDisplay(self, timer):
        '''
        This function updates the display with the current solar power production. But before it checks if its Daytime or Nighttime.
        Based on day or night it sets the update interval to night or day time update interval.
        '''
        print("updateSolarDisplay")
        now = utime.mktime(utime.localtime())
        sunrise = utime.mktime(util.parse_time_string(self.sunriseConnector.get_sunrise_sunset()['sunrise']))
        sunset = utime.mktime(util.parse_time_string(self.sunriseConnector.get_sunrise_sunset()['sunset']))
        if (now > sunrise) and (now < sunset):
            # its Daytime. If its isDaytime is still on Nighttime, switch to Daytime
            print("daytime")
            if (not self.isDaytime):
                self.isDaytime = True
                self.display_timer.deinit()
                self.display_timer.init(period=config.DAYTIME_UPDATE_INTERVAL, mode=Timer.PERIODIC, callback=self.updateSolarDisplay)
        else:
            # Its Nighttime. If its isDaytime is still on Daytime, switch to Nighttime
            print("nighttime")
            if (self.isDaytime):
                self.isDaytime = False
                self.display_timer.deinit()
                self.display_timer.init(period=config.NIGHTTIME_UPDATE_INTERVAL, mode=Timer.PERIODIC, callback=self.updateSolarDisplay)
        self.write_to_display()


if __name__ == '__main__':
    util.connect_to_wifi(config.WIFI_SSID, config.WIFI_PASSWORD)
    util.set_time()
    displayController = DisplayController()
    displayController.write_to_display()