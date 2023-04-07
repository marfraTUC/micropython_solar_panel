import framebuf
from machine import SPI, Pin

import epaper1in54
import solar_icons
from SolarPlant import SolarPlant, Measurement

black = 0
white = 1
x = 0
y = 0
spi = SPI(1)
cs = Pin(15)
dc = Pin(4)
rst = Pin(2)
busy = Pin(5)

number_switcher = {
    0: solar_icons.zero,
    1: solar_icons.one,
    2: solar_icons.two,
    3: solar_icons.three,
    4: solar_icons.four,
    5: solar_icons.five,
    6: solar_icons.six,
    7: solar_icons.seven,
    8: solar_icons.eight,
    9: solar_icons.nine
}

trend_switcher = {
    -1: solar_icons.down,
    0: solar_icons.draw,
    1: solar_icons.up,
    }

class SolarPanelDisplay:
    '''This class is responsible for displaying the solar panel data on the e-paper display.'''
    def __init__(self, energy_plant):
        '''
        Initializes the display and takes the energy plant as a parameter. From which the data is read.
        :param energy_plant:
        '''
        self.display = epaper1in54.EPD(spi, cs, dc, rst, busy)
        self.display.init()
        self.solarPlant = energy_plant

    def write_to_display(self):
        '''
        Writes the data to the display.
        :return:
        '''
        self.buf = bytearray(self.display.width * self.display.height // 8)
        self.fb = framebuf.FrameBuffer(self.buf, self.display.width, self.display.height, framebuf.MONO_HLSB)
        self.fb.fill(white)

        write_power_production(self.solarPlant, self.fb)
        write_power_production_chart(self.solarPlant, self.fb, self.display.width)
        write_power_consumption(self.solarPlant, self.fb)
        write_power_exported(self.solarPlant, self.fb)
        mirror_framebuffer_horizontal(self.fb, self.display.width, self.display.height)

        self.display.set_frame_memory(self.buf, 0, 0, self.display.width, self.display.height)
        self.display.display_frame()


def write_power_production(solar_plant : SolarPlant, fb : framebuf.FrameBuffer):
    write_measurment(fb, 65, 10, solar_plant.energyProduced())
    icon = solar_icons.solar_panel
    icon_frame = framebuf.FrameBuffer(icon.icon, icon.width, icon.height, framebuf.MONO_HLSB)
    fb.blit(icon_frame, 10, 4)
    fb.rect(1, 1, 199, 49, black)




def write_power_production_chart(solar_plant : SolarPlant, fb : framebuf.FrameBuffer, width, height = 100):
    '''
    Writes the power production chart to the framebuffer.
    :param solar_plant:
    :param fb:
    :return:
    '''

    # Calculate the maximum and minimum value in the energy history
    max_value = max(solar_plant.energyHistory())
    min_value = min(solar_plant.energyHistory())

    # Calculate a scaling factor that scales the values to fit in the chart's height
    scaling_factor = height / (max_value - min_value)

    steps = len(solar_plant.energyHistory()) / width
    for x in range(0, width):
        # Scale the value using the scaling factor
        scaled_value = int((solar_plant.energyHistory()[int(x * steps)] - min_value) * scaling_factor)

        # Draw the chart
        fb.vline(x, height - scaled_value, scaled_value, black)


    #steps = len(solar_plant.energyHistory()) / width
    #for x in range(0, width):
    #    fb.vline(x, 100 - solar_plant.energyHistory()[int(x*steps)], solar_plant.energyHistory()[int(x*steps)], black)

    #for value in solar_plant.energyHistory():
    #    fb.vline(x, height - value, value, black)
    #    x = x + 1


def write_power_consumption(solar_plant : SolarPlant, fb : framebuf.FrameBuffer):
    '''
    Writes the power consumption meassuremnt to the framebuffer.
    :param solar_plant:
    :param fb:
    :return:
    '''
    write_measurment(fb, 65, 110, solar_plant.energyConsumed())
    icon = solar_icons.house
    icon_frame = framebuf.FrameBuffer(icon.icon, icon.width, icon.height, framebuf.MONO_HLSB)
    fb.blit(icon_frame, 7, 104)
    fb.rect(1, 101, 199, 49, black)


def write_power_exported(solar_plant : SolarPlant, fb : framebuf.FrameBuffer):
    '''
    Writes the power exported meassuremnt to the framebuffer.
    :param solar_plant:
    :param fb:
    :return:
    '''
    write_measurment(fb, 65, 160, solar_plant.energyExported())
    icon = solar_icons.grid
    icon_frame = framebuf.FrameBuffer(icon.icon, icon.width, icon.height, framebuf.MONO_HLSB)
    fb.blit(icon_frame, 13, 154)
    fb.rect(1, 151, 199, 49, black)

def write_measurment(fb : framebuf.FrameBuffer, x, y, number : Measurement):
    '''
    Writes a measurement to the framebuffer. Measurement is a class with a value and a trend.
    Trend is a number between -1 and 1. -1 is down, 0 is draw and 1 is up.
    :param fb:
    :param x:
    :param y:
    :param number:
    :return:
    '''
    icon = trend_switcher.get(number.trend)
    icon_frame = framebuf.FrameBuffer(icon.icon, icon.width, icon.height, framebuf.MONO_HLSB)
    fb.blit(icon_frame, x, int(y+icon.height/2)+5)
    x = x + icon.width +5
    for char in str(number.value):
        icon = number_switcher.get(int(char))
        icon_frame = framebuf.FrameBuffer(icon.icon, icon.width, icon.height, framebuf.MONO_HLSB)
        fb.blit(icon_frame, x, y)
        x = x + icon.width
    icon = solar_icons.watt
    icon_frame = framebuf.FrameBuffer(icon.icon, icon.width, icon.height, framebuf.MONO_HLSB)
    fb.blit(icon_frame, x, y)


def mirror_framebuffer_horizontal(fb, width, height):
    '''Mirrors the framebuffer horizontally.'''
    width = width
    height = height
    for y in range(height):
        for x in range(width // 2):
            pixel1 = fb.pixel(x, y)
            pixel2 = fb.pixel(width - x - 1, y)
            fb.pixel(x, y, pixel2)
            fb.pixel(width - x - 1, y, pixel1)

