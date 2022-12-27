from powerclamp import *
import os
from dotenv import find_dotenv, load_dotenv
from influxdbclient import InfluxDbClient

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
influxdb = InfluxDbClient(os.getenv("INFLUXDB_URL"), os.getenv("INFLUXDB_TOKEN"), os.getenv("INFLUXDB_ORG"), os.getenv("INFLUXDB_BUCKET"))
# Power Clamp
device = PowerClamp(os.getenv("TUYA_DEVICE_ID"), os.getenv("TUYA_LOCAL_KEY"), os.getenv("TUYA_DEVICE_IP"))
device.listen(influxdb.write)

# from subbreaker import *
#
# # Miner Breaker
# device = SubBreaker('ebc9dede24278b55a2jksk', 'e2b7f60d7d691d3f', '88.87.4.198')
#
# # Blower Breaker
# device = SubBreaker('eb3e19ed3e86b1604c1tot', 'ecb7c936bd157677', '88.87.4.197')
