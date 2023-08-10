import tinytuya


class PowerClamp:
    def __init__(self, device_id, local_key, ip_address):
        self.device_id = device_id
        self.local_key = local_key
        self.ip_address = ip_address
        self.device = tinytuya.OutletDevice(device_id, ip_address, local_key)
        self.device.set_version(3.3)
        self.is_lost_status = False
        self.data = None

    @staticmethod
    def get_dp_type(dp_key):
        match dp_key:
            case '101':
                return {'type': 'VoltageA', 'divider': 10}
            case '102':
                return {'type': 'CurrentA', 'divider': 1000}
            case '103':
                return {'type': 'ActivePowerA', 'divider': 1}
            case '104':
                return {'type': 'PowerFactorA', 'divider': 100}
            case '106':
                return {'type': 'EnergyConsumedA', 'divider': 100}
            case '111':
                return {'type': 'VoltageB', 'divider': 10}
            case '112':
                return {'type': 'CurrentB', 'divider': 1000}
            case '113':
                return {'type': 'ActivePowerB', 'divider': 1}
            case '114':
                return {'type': 'PowerFactorB', 'divider': 100}
            case '116':
                return {'type': 'EnergyConsumedB', 'divider': 100}
            case '121':
                return {'type': 'VoltageC', 'divider': 10}
            case '122':
                return {'type': 'CurrentC', 'divider': 1000}
            case '123':
                return {'type': 'ActivePowerC', 'divider': 1}
            case '124':
                return {'type': 'PowerFactorC', 'divider': 100}
            case '126':
                return {'type': 'EnergyConsumedC', 'divider': 100}
            case '131':
                return {'type': 'TotalEnergyConsumed', 'divider': 100}
            case '132':
                return {'type': 'TotalCurrent', 'divider': 1000}
            case '133':
                return {'type': 'TotalActivePower', 'divider': 1}
            case '135':
                return {'type': 'Frequency', 'divider': 1}
            case '136':
                return {'type': 'Temperature', 'divider': 10}
            case _:
                return None

    def power_clamp_data(self):
        data = self.device.status()
        if (data is None or
                'dps' not in data or
                # check if there's active power in the data if none of them exists returns
                ('103' not in data['dps'] and '113' not in data['dps'] and '123' not in data['dps'])):

            if self.data is None:
                return None

            return self.data

        self.data = data
        return data
