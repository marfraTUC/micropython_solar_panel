from collections import namedtuple
import ustruct
import usocket as socket
import config


Measurement = namedtuple('Measurement', ['value', 'trend'])
tolerance_max = 1.1
tolerance_min = 0.9

class SolarPlant:

    def __init__(self, historySize):
        self._energyProduced = Measurement(0,0)
        self._energyConsumed = Measurement(0,0)
        self._energyStored = Measurement(0,0)
        self._energyExported = Measurement(0,0)
        self._historySize = historySize
        self._energyHistory = [0,0,0]
        self.update()

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

    def update(self):
        print("Updating Solar Plant start ...")
        # Request payload
        payload = b'\xf7\x03\x89\x1c\x00}z\xe7'

        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(15)

        try:
            send_request(sock, payload)
            data = receive_data(sock)
            data = data[5:-2]
            energy_exported = read_int16(data, 80)
            energyProduced = read_int16(data, 76)
            house_consumption = energyProduced - energy_exported

        except OSError as e:
            print('Error:', e)

        self.addHistory(energyProduced)
        self._energyProduced = check_tendenz(energyProduced, self._energyProduced.value)
        self._energyConsumed = check_tendenz(house_consumption, self._energyConsumed.value)
        self._energyExported = check_tendenz(energy_exported, self._energyExported.value)
        print("...Updating Solar Plant done")


def check_tendenz(new_value, old_value):
    if new_value > old_value * tolerance_max:
        return Measurement(new_value, 1)
    elif new_value < old_value * tolerance_min:
        return Measurement(new_value, -1)
    else:
        return Measurement(new_value, 0)

def read_int16(data, offset):
    return ustruct.unpack(">h", data[offset:offset+2])[0]

def send_request(sock, payload):
    sock.sendto(payload, (config.INVERTER_IP, config.INVERTER_PORT))

# Receive data from the inverter
def receive_data(sock):
    data, addr = sock.recvfrom(1024)
    return data
    
            

      
