import datetime
import os
import tinytuya
from powerclamp import PowerClamp


class Process:
    def __init__(self, influxdb, delay_secs):
        self.influxdb = influxdb
        self.delay_secs = delay_secs

    def start(self):
        while True:
            try:
                device = PowerClamp(os.getenv("TUYA_DEVICE_ID"),
                                    os.getenv("TUYA_LOCAL_KEY"),
                                    os.getenv("TUYA_DEVICE_IP"))
                device.device.set_socketPersistent(True)
                print(" > Send Request for Status < ")
                payload = device.device.generate_payload(tinytuya.DP_QUERY)
                device.device.send(payload)

                self.process(device)
            except TypeError:
                print("exception")

    def process(self, device):
        print(" > Begin Monitor Loop <")
        while True:
            # See if any data is available
            data = device.device.receive()
            if 'dps' not in data:
                continue

            for key, value in data['dps'].items():
                # process data and value
                dt = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0)
                if 't' in data:
                    dt = datetime.datetime.fromtimestamp(data['t'], tz=datetime.timezone.utc)
                self.send_data(dt, key, value, device)

            payload = device.device.generate_payload(tinytuya.HEART_BEAT)
            device.device.send(payload)

    def send_data(self, date_time, key, value, device):
        dp_type = device.get_dp_type(key)
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
