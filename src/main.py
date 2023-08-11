from powerclamp import PowerClamp
from process import Process
import os
from dotenv import find_dotenv, load_dotenv
from influxdbclient import InfluxDbClient

print(f"Process start")

# load environment variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# create an instance of influx db with the configuration values
influxdb = InfluxDbClient(os.getenv("INFLUXDB_URL"),
                          os.getenv("INFLUXDB_TOKEN"),
                          os.getenv("INFLUXDB_ORG"),
                          os.getenv("INFLUXDB_BUCKET"))

# create an instance of power clamp device with configuration values
device = PowerClamp(os.getenv("TUYA_DEVICE_ID"), os.getenv("TUYA_LOCAL_KEY"), os.getenv("TUYA_DEVICE_IP"))

# value for delaying each request
delay_secs = float(os.getenv("DELAY_SECS"))

process = Process(device, influxdb, delay_secs)
process.process()
