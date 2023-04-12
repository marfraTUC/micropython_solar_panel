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
    """This class is responsible for displaying the solar panel data on the e-paper display."""

    def __init__(self, energy_plant: SolarPlant, mirrow_horizontal=True, rotated=False):
        """
        Initializes the display and takes the energy plant as a parameter. From which the data is read.
        :param energy_plant:
        """
        self.display = epaper1in54.EPD(spi, cs, dc, rst, busy)
        self.display.init()
        self.solarPlant = energy_plant
        self.mirrow_horizontal = mirrow_horizontal
        self.rotated = rotated
        self.buf = bytearray(self.display.width * self.display.height // 8)
        self.fb = framebuf.FrameBuffer(self.buf, self.display.width, self.display.height, framebuf.MONO_HLSB)

    def write_to_display(self):
        """im
        Writes the data to the display.
        :return:
        """
        print("SolarPanelDisplay: Update Display")
        self.fb.fill(white)

        self.write_power_production()
        self.write_power_production_chart()
        self.write_power_consumption()
        self.write_power_exported()

        if self.mirrow_horizontal:
            self.mirror_framebuffer_horizontal()
        rotated = 0
        #while (rotated < self.rotated):
        #    self.rotate_framebuffer()
        #    rotated += 90

        self.display.set_frame_memory(self.buf, 0, 0, self.display.width, self.display.height)
        self.display.display_frame()

    def write_power_production(self, start=1):
        """
        Writes the power production meassuremnt to the framebuffer.
        :param start: The start position (y) of the chart
        :return:
        """
        write_measurment(self.fb, 65, 10, self.solarPlant.energyProduced())
        icon = solar_icons.solar_panel
        icon_frame = framebuf.FrameBuffer(icon.icon, icon.width, icon.height, framebuf.MONO_HLSB)
        self.fb.blit(icon_frame, 10, 4)
        self.fb.rect(1, start, 199, 49, black)

    def write_power_production_chart(self, start=51, height=50):
        """
        Writes the power production chart to the framebuffer.
        :param start: The start position (y) of the chart
        :param height: The height of the chart
        :return:
        """

        # Calculate the maximum and minimum value in the energy history
        max_value = max(self.solarPlant.energyHistory())
        min_value = min(self.solarPlant.energyHistory())

        # Calculate a scaling factor that scales the values to fit in the chart's height
        scaling_factor = height / (max_value - min_value)
        steps = len(self.solarPlant.energyHistory()) / self.display.width
        for x_value in range(0, self.display.width):
            # Scale the value using the scaling factor
            scaled_value = int((self.solarPlant.energyHistory()[int(x_value * steps)] - min_value) * scaling_factor)

            # Draw the chart
            self.fb.vline(x_value, start + height - scaled_value, scaled_value, black)

    def write_power_consumption(self, start=101):
        """
        Writes the power consumption meassuremnt to the framebuffer.
        :param start: The start position (y) of the chart
        :return:
        """
        write_measurment(self.fb, 65, 110, self.solarPlant.energyConsumed())
        icon = solar_icons.house
        icon_frame = framebuf.FrameBuffer(icon.icon, icon.width, icon.height, framebuf.MONO_HLSB)
        self.fb.blit(icon_frame, 7, 104)
        self.fb.rect(1, start, 199, 49, black)

    def write_power_exported(self, start=151):
        """
        Writes the power exported meassuremnt to the framebuffer.
        :param start: The start position (y) of the chart
        :return:
        """
        write_measurment(self.fb, 65, 160, self.solarPlant.energyExported())
        icon = solar_icons.grid
        icon_frame = framebuf.FrameBuffer(icon.icon, icon.width, icon.height, framebuf.MONO_HLSB)
        self.fb.blit(icon_frame, 13, 154)
        self.fb.rect(1, start, 199, 49, black)

    def mirror_framebuffer_horizontal(self):
        """Mirrors the framebuffer horizontally."""
        print("Mirror Display")
        width = self.display.width
        height = self.display.height
        for y_value in range(height):
            for x_value in range(width // 2):
                pixel1 = self.fb.pixel(x_value, y_value)
                pixel2 = self.fb.pixel(width - x_value - 1, y_value)
                self.fb.pixel(x_value, y_value, pixel2)
                self.fb.pixel(width - x_value - 1, y_value, pixel1)

    def rotate_framebuffer(self):
        """Rotates the framebuffer 90 degrees."""
        print("Rotate Display")
        width = self.display.width
        height = self.display.height
        for y_vlaue in range(height):
            for x_value in range(width // 2):
                pixel1 = self.fb.pixel(x_value, y_vlaue)
                pixel2 = self.fb.pixel(width - x_value - 1, y_vlaue)
                self.fb.pixel(x_value, y_vlaue, pixel2)
                self.fb.pixel(width - x_value - 1, y_vlaue, pixel1)


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
    icon = trend_switcher.get(number.trend)
    icon_frame = framebuf.FrameBuffer(icon.icon, icon.width, icon.height, framebuf.MONO_HLSB)
    fb.blit(icon_frame, x_value, int(y_value + icon.height / 2) + 5)
    x_value = x_value + icon.width + 5
    for char in str(number.value):
        icon = number_switcher.get(int(char))
        icon_frame = framebuf.FrameBuffer(icon.icon, icon.width, icon.height, framebuf.MONO_HLSB)
        fb.blit(icon_frame, x_value, y_value)
        x_value = x_value + icon.width
    icon = solar_icons.watt
    icon_frame = framebuf.FrameBuffer(icon.icon, icon.width, icon.height, framebuf.MONO_HLSB)
    fb.blit(icon_frame, x_value, y_value)
