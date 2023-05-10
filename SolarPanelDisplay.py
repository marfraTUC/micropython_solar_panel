import framebuf
import utime
import epaper1in54
import gc
import solar_icons
from machine import SPI, Pin
from micropython import const
from SolarPlant import SolarPlant, Measurement

black = const(0)
white = const(1)
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
    """This class is responsible for displaying the solar panel data on the e-paper display."""

    def __init__(self, energy_plant: SolarPlant, mirrow_horizontal=True, rotated=False):
        """
        Initializes the display and takes the energy plant as a parameter. From which the data is read.
        :param energy_plant:
        """
        print("SolarPanelDisplay: Init")
        self.display = epaper1in54.EPD(spi, cs, dc, rst, busy)
        self.display.init()
        self.solarPlant = energy_plant
        self.mirrow_horizontal = mirrow_horizontal
        self.rotated = rotated
        print("SolarPanelDisplay: Init done")

    def write_to_display(self):
        """im
        Writes the data to the display.
        :return:
        """
        print("SolarPanelDisplay: Update Display")
        gc.collect()
        buf = bytearray(self.display.width * self.display.height // 8)
        fb = framebuf.FrameBuffer(buf, self.display.width, self.display.height, framebuf.MONO_HLSB)
        fb.fill(white)

        write_section(fb, self.solarPlant.energyProduced(), solar_icons.solar_panel, 1, 49)
        gc.collect()
        write_power_production_chart(fb, self.solarPlant.energyHistory(),200,50)
        gc.collect()
        write_section(fb, self.solarPlant.energyConsumed(), solar_icons.house, 101, 149)
        gc.collect()
        write_section(fb, self.solarPlant.energyExported(), solar_icons.grid, 151, 199)
        gc.collect()
        ## Write current time
        current_time = utime.time()
        hours = current_time // 3600 % 24
        minutes = (current_time // 60) % 60
        gc.collect()
        fb.text("{:02d}:{:02d}".format(hours, minutes), 156, 192, black)

        if self.mirrow_horizontal:
            mirror_framebuffer_horizontal(fb, self.display.width, self.display.height)
        # Commented because it used to much memory
        #rotated = 0
        #while (rotated < self.rotated):
        #    self.rotate_framebuffer()
        #    rotated += 90
        self.display.set_frame_memory(buf, 0, 0, self.display.width, self.display.height)
        self.display.display_frame()


def write_section(fb, measurment, icon, start=1, end=49):
    """
    Writes the power production meassuremnt to the framebuffer.
    :param start: The start position (y) of the chart
    :return:
    """
    print("SolarPanelDisplay: Write power production")
    write_measurment(fb, 65, start+10, measurment)
    icon_frame = framebuf.FrameBuffer(icon.icon, icon.width, icon.height, framebuf.MONO_HLSB)
    fb.blit(icon_frame, 10, 4+start)
    fb.rect(1, start, 199, end, black)

def write_power_production_chart(fb, history, width = 200, height=50, start=51):
    """
    Writes the power production chart to the framebuffer.
    :param start: The start position (y) of the chart
    :param height: The height of the chart
    :return:
    """
    print("SolarPanelDisplay: Write power production chart")
    # Calculate the maximum and minimum value in the energy history
    max_value = max(history)
    min_value = min(history)

    # Calculate a scaling factor that scales the values to fit in the chart's height
    try:
        scaling_factor = height / (max_value - min_value)
    except ZeroDivisionError:
        scaling_factor = 0
    steps = len(history) / width
    for x_value in range(0, width):
        # Scale the value using the scaling factor
        scaled_value = int((history[int(x_value * steps)] - min_value) * scaling_factor)

        # Draw the chart
        fb.vline(x_value, start + height - scaled_value, scaled_value, black)


def mirror_framebuffer_horizontal(fb, width = 200, height = 200):
    """Mirrors the framebuffer horizontally."""
    print("SolarPanelDisplay: Mirror Display")
    width = width
    height = height
    print("width: " + str(width))
    print("height: " + str(height))
    for y_value in range(height):
        for x_value in range(width // 2):
            pixel1 = fb.pixel(x_value, y_value)
            pixel2 = fb.pixel(width - x_value - 1, y_value)
            fb.pixel(x_value, y_value, pixel2)
            fb.pixel(width - x_value - 1, y_value, pixel1)

# Commented out because it is used to much memory
#def rotate_framebuffer(self):
#    """Rotates the framebuffer 90 degrees."""
#    print("SolarPanelDisplay: Rotate Display")
#    width = self.display.width
#    height = self.display.height
#    for y_vlaue in range(height):
#        for x_value in range(width // 2):
#            pixel1 = self.fb.pixel(x_value, y_vlaue)
#            pixel2 = self.fb.pixel(width - x_value - 1, y_vlaue)
#            self.fb.pixel(x_value, y_vlaue, pixel2)
#           self.fb.pixel(width - x_value - 1, y_vlaue, pixel1)


def write_measurment(fb: framebuf.FrameBuffer, x_value, y_value, number: Measurement):
    """
    Writes a measurement to the framebuffer. Measurement is a class with a value and a trend.
    Trend is a number between -1 and 1. -1 is down, 0 is draw and 1 is up.
    :param fb: framebuffer
    :param x_value: x position
    :param y_value: y position
    :param number: measurement
    :return:
    """
    print("SolarPanelDisplay: Write measurment")
    icon = trend_switcher.get(number.trend)
    icon_frame = framebuf.FrameBuffer(icon.icon, icon.width, icon.height, framebuf.MONO_HLSB)
    fb.blit(icon_frame, x_value, int(y_value + icon.height / 2) + 5)
    x_value = x_value + icon.width + 5
    for char in str(number.value):
        try:
            icon = number_switcher.get(int(char))
            icon_frame = framebuf.FrameBuffer(icon.icon, icon.width, icon.height, framebuf.MONO_HLSB)
            fb.blit(icon_frame, x_value, y_value)
        except ValueError:
            icon = solar_icons.minus
            icon_frame = framebuf.FrameBuffer(icon.icon, icon.width, icon.height, framebuf.MONO_HLSB)
            fb.blit(icon_frame, x_value, y_value+15)

        x_value = x_value + icon.width
    icon = solar_icons.watt
    icon_frame = framebuf.FrameBuffer(icon.icon, icon.width, icon.height, framebuf.MONO_HLSB)
    fb.blit(icon_frame, x_value, y_value)
