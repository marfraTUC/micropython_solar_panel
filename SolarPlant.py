from machine import Timer
from collections import namedtuple

Measurement = namedtuple('Measurement', ['value', 'trend'])


class SolarPlant:

    def __init__(self, historySize):
        self._energyProduced = Measurement(8534,1)
        self._energyConsumed = Measurement(1530,1)
        self._energyStored = Measurement(0,0)
        self._energyExported = Measurement(self._energyProduced.value - self._energyConsumed.value, 1)
        self._historySize = historySize
        self._energyHistory = [35, 48, 2, 46, 37, 26, 24, 38, 3, 30, 22, 1, 34, 25, 46, 47, 13, 17, 28, 23, 50, 20, 25,
                               6, 8, 9,
                               39, 4, 36, 45, 27, 37, 25, 16, 33, 10, 16, 25, 5, 17, 47, 28, 39, 50, 25, 13, 47, 28, 2,
                               45, 35,
                               12, 49, 26, 30, 7, 14, 9, 46, 23, 38, 41, 50, 23, 13, 20, 29, 44, 22, 13, 16, 28, 11, 11,
                               23, 45,
                               49, 18, 22, 33, 29, 38, 35, 14, 34, 15, 15, 25, 48, 9, 3, 18, 19, 8, 16, 15, 18, 44, 35,
                               19, 43,
                               45, 4, 4, 45, 24, 22, 27, 48, 10, 25, 9, 13, 5, 1, 10, 39, 50, 48, 36, 21, 44, 3, 46, 41,
                               5, 31,
                               47, 17, 31, 33, 43, 25, 50, 1, 25, 5, 15, 11, 45, 12, 16, 22, 9, 48, 34, 30, 10, 34, 38,
                               27, 33,
                               29, 10, 23, 12, 11, 49, 21, 35, 8, 2, 23, 12, 20, 43, 36, 16, 7, 41, 3, 4, 6, 14, 26, 38,
                               20, 39,
                               14, 14, 10, 35, 13, 30, 23, 12, 20, 49, 25, 12, 7, 20, 4, 12, 6, 15, 3, 9, 14, 36, 5, 14,
                               43, 17,
                               30]
        #solar_plant_timer = Timer(-1)
        #solar_plant_timer.init(period=30000, mode=Timer.PERIODIC, callback=self.update)

    def energyProduced(self):
        return self._energyProduced

    def energyConsumed(self):
        return self._energyConsumed

    def energyStored(self):
        return self._energyStored

    def energyExported(self):
        return self._energyExported

    def energyHistory(self):
        return self._energyHistory

    def addHistory(self, energy):
        while len(self._energyHistory) >= self._historySize:
            self._energyHistory.pop(0)
        self._energyHistory.append(energy)

    def update(self, timer):
        print("Updating Solar Plant")
