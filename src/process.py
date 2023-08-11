import datetime
import tinytuya


class Process:
    def __init__(self, power_clamp, influxdb, delay_secs):
        self.power_clamp = power_clamp
        self.influxdb = influxdb
        self.delay_secs = delay_secs

    def process(self):
        self.power_clamp.device.set_socketPersistent(True)
        print(" > Send Request for Status < ")
        payload = self.power_clamp.device.generate_payload(tinytuya.DP_QUERY)
        self.power_clamp.device.send(payload)

        print(" > Begin Monitor Loop <")
        while True:
            try:
                # See if any data is available
                data = self.power_clamp.device.receive()
                if 'dps' not in data:
                    continue

                for key, value in data['dps'].items():
                    # process data and value
                    dt = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0)
                    if 't' in data:
                        dt = datetime.datetime.fromtimestamp(data['t'], tz=datetime.timezone.utc)
                    self.send_data(dt, key, value)
            except TypeError:
                print("exception")

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
        print(f"{obj['t']} - {obj['type']} {obj['value']}")
        self.influxdb.write(obj, date_time)
