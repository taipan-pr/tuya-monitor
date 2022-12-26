import json

from device import Device
from datetime import datetime


class PowerClamp(Device):
    def __init__(self, device_id, local_key, ip_address):
        Device.__init__(self, device_id, local_key, ip_address)

    @staticmethod
    def __get_dp_type(dp_key):
        match dp_key:
            case '101': return 'VoltageA'
            case '102': return 'CurrentA'
            case '103': return 'ActivePowerA'
            case '104': return 'PowerFactorA'
            case '106': return 'EnergyConsumedA'
            case '111': return 'VoltageB'
            case '112': return 'CurrentB'
            case '113': return 'ActivePowerB'
            case '114': return 'PowerFactorB'
            case '116': return 'EnergyConsumedB'
            case '121': return 'VoltageC'
            case '122': return 'CurrentC'
            case '123': return 'ActivePowerC'
            case '124': return 'PowerFactorC'
            case '126': return 'EnergyConsumedC'
            case '131': return 'TotalEnergyConsumed'
            case '132': return 'TotalCurrent'
            case '133': return 'TotalActivePower'
            case '135': return 'Frequency'
            case '136': return 'Temperature'
            case _: return None

    def _process(self, data, func=None):
        try:
            # See if any data is available
            data = self.device.receive()

            if 't' not in data or data['dps'] is None:
                return

            for key, value in data['dps'].items():
                obj = {
                    't': data['t'],
                    'type': self.__get_dp_type(key),
                    'dp': key,
                    'value': value
                }
                print(obj)

                if func is not None:
                    func(obj)

        except:
            print('Exception payload: %r' % data)
