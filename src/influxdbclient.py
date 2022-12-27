import datetime

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxDbClient:
    def __init__(self, url, token, org, bucket):
        self.client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        self.bucket = bucket
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.org = org

    def write(self, data):
        dt = datetime.datetime.fromtimestamp(data['t'])
        local_time = dt.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=7)))
        p = influxdb_client \
            .Point(data['name']) \
            .field(data['type'], data['value']) \
            .time(local_time)
        self.write_api.write(bucket=self.bucket, org=self.org, record=p)
