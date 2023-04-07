from collections import namedtuple

import util

Measurement = namedtuple('Measurement', ['value', 'trend'])


class SolarPlant:

    def __init__(self, historySize):
        self._energyProduced = Measurement(8534,1)
        self._energyConsumed = Measurement(1530,1)
        self._energyStored = Measurement(0,0)
        self._energyExported = Measurement(self._energyProduced.value - self._energyConsumed.value, 1)
        self._historySize = historySize
        self._energyHistory = util.random_int_list(200, self._historySize)
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
