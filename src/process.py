import datetime
import os
import time

import tinytuya

from powerclamp import PowerClamp
from influxdbclient import InfluxDbClient


class Process:
    def process(self):
        # value for delaying each request
        delay_secs = float(os.getenv("DELAY_SECS"))

        # create an instance of power clamp device with configuration values
        device = PowerClamp(os.getenv("TUYA_DEVICE_ID"),
                            os.getenv("TUYA_LOCAL_KEY"),
                            os.getenv("TUYA_DEVICE_IP"))

        # create an instance of power clamp device with configuration values
        miner_power = tinytuya.OutletDevice(os.getenv("MINER_DEVICE_ID"),
                                            os.getenv("MINER_DEVICE_IP"),
                                            os.getenv("MINER_LOCAL_KEY"))
        miner_power.set_version(3.4)
        xx = miner_power.status()
        yy = miner_power.detect_available_dps()

        # create an instance of influx db with the configuration values
        influxdb = InfluxDbClient(os.getenv("INFLUXDB_URL"),
                                  os.getenv("INFLUXDB_TOKEN"),
                                  os.getenv("INFLUXDB_ORG"),
                                  os.getenv("INFLUXDB_BUCKET"))

        print(" > Begin Monitor Loop <")
        try:
            while True:
                # See if any data is available
                data = device.device.status()
                if 'dps' not in data:
                    print(f'dps not present - {data}')
                    continue

                dt = datetime.datetime.utcnow()
                # for key, value in data['dps'].items():
                #     # process data and value
                #     self.send_power_clamp_data(influxdb, dt, key, value, device)

                time.sleep(delay_secs)

        except:
            device.device.close()
            miner_power.device.close()
            raise TypeError("exception")

    @staticmethod
    def send_power_clamp_data(influxdb, date_time, key, value, device):
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

        # print(f"{obj['t']} - {obj['type']} {obj['value']}")
        influxdb.write(obj, date_time)
