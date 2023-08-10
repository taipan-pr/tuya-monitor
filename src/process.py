import datetime


class Process:
    def __init__(self, power_clamp, influxdb, delay_secs):
        self.power_clamp = power_clamp
        self.influxdb = influxdb
        self.delay_secs = delay_secs

    def process(self):
        data = self.power_clamp.power_clamp_data()
        date_time = datetime.datetime.utcnow()

        # define all the known (expected) elements in the response
        device_dps = ['101', '102', '103', '104', '106',
                      '111', '112', '113', '114', '116',
                      '121', '122', '123', '124', '126',
                      '131', '132', '133', '135', '136']

        for key, value in data['dps'].items():
            # process data and value
            self.send_data(date_time, key, value)

            # remove item from the expected elements
            if key in device_dps:
                device_dps.remove(key)

        # since the status with 0 value will not be in the response
        # loop through the expected elements and send 0.0
        for key in device_dps:
            self.send_data(date_time, key, 0.0)

        print()

    def send_data(self, date_time, key, value):
        dp_type = self.power_clamp.get_dp_type(key)
        if dp_type is None:
            return

        if value < 0.0:
            value = 0.0

        obj = {
            'name': 'PowerClamp',
            't': date_time,
            'type': dp_type['type'],
            'dp': key,
            'value': value / dp_type['divider']
        }
        print(f"{obj['type']} {obj['value']}")
        self.influxdb.write(obj, date_time)

        if key == '103' or key == '113' or key == '123':
            kwh = 0.0
            if value > 0.0:
                kwh = (value * ((self.delay_secs / 60) / 60))

            obj = {
                'name': 'PowerClamp',
                't': date_time,
                'type': dp_type['type'] + "Wh",
                'dp': key,
                'value': kwh
            }

            print(f"{obj['type']} {obj['value']}")
            self.influxdb.write(obj, date_time)
