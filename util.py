import utime
import ntptime
import network
from machine import Pin, RTC


def flash_pins(numer_of_flashes, time_between_flashes):
    led = Pin(2, Pin.OUT)
    enabled = False
    for i in range(numer_of_flashes*2):
        if enabled:
            led.off()
        else:
            led.on()
        utime.sleep_ms(time_between_flashes)
        enabled = not enabled
    led.on()

# Convert the input time string to a time tuple
def parse_time_string(time_string):
    year, month, day, hour, minute, second = time_string[:-6].replace('T', '-').replace(':','-').split('-')
    return (int(year), int(month), int(day), int(hour), int(minute), int(second), 0, 0)

# Compare two time tuples
def compare_times(time1, time2):
    time1_seconds = utime.mktime(time1)
    time2_seconds = utime.mktime(time2)

    if time1_seconds < time2_seconds:
        return -1
    elif time1_seconds > time2_seconds:
        return 1
    else:
        return 0

def connect_to_wifi(ssid, password):
    wifi = network.WLAN(network.STA_IF)
    if not wifi.isconnected():
        print('connecting to network...')
        wifi.active(True)
        wifi.connect(ssid, password)
        retries = 0
        while not wifi.isconnected():
            pass
    print('network config:', wifi.ifconfig())
    flash_pins(2, 100)


def set_time():
    rtc = RTC()
    ntptime.settime()  # set the rtc datetime from the remote server
    rtc.datetime()  # get date and time
    print(rtc.datetime()) # print the date and time)
    flash_pins(3, 100)

