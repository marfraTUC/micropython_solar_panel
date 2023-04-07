import json
import urequests
import config


class SunriseConnector:
    '''
    This class connects to the sunrise-sunset.org API and gets the sunrise and sunset time for the given location.
    It updates these values every 12 hours.
    '''
    def __init__(self, latitude, longitude):
        '''
        Constructor to initialize the class with the given latitude and longitude.
        The URL for the API is defined in the config file.
        :param latitude:
        :param longitude:
        '''
        self.latitude = latitude
        self.longitude = longitude
        self.url = config.SUNRISE_API + str(latitude) + '&lng=' + str(
            longitude) + '&formatted=0'

        self.update_information()

        #sunrise_timer = Timer(-3)
        #sunrise_timer.init(period=config.SUNRISE_UPDATE_INTERVAL, mode=Timer.PERIODIC, callback=self.update_information)

    def update_information(self, timer=None):
        '''
        This function updates the sunrise and sunset time for the given location.
        :param timer:
        :return:
        '''
        response = urequests.get(self.url)
        data = json.loads(response.text)
        sunrise = data['results']['sunrise']
        sunset = data['results']['sunset']
        self.sun_info = {'sunrise': sunrise, 'sunset': sunset}


    def get_sunrise_sunset(self):
        '''
        This function returns the sunrise and sunset time.
        :return:
        '''
        return self.sun_info
