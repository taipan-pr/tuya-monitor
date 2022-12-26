from powerclamp import *
from rabbitmq import RabbitMq
import os
from dotenv import find_dotenv, load_dotenv


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
queue = RabbitMq(os.getenv("RABBITMQ_HOST"), os.getenv("RABBITMQ_EXCHANGE_NAME"), os.getenv("RABBITMQ_QUEUE_NAME"))
# Power Clamp
device = PowerClamp(os.getenv("TUYA_DEVICE_ID"), os.getenv("TUYA_LOCAL_KEY"), os.getenv("TUYA_DEVICE_IP"))
device.listen(queue.publish)

# from subbreaker import *
#
# # Miner Breaker
# device = SubBreaker('ebc9dede24278b55a2jksk', 'e2b7f60d7d691d3f', '88.87.4.198')
#
# # Blower Breaker
# device = SubBreaker('eb3e19ed3e86b1604c1tot', 'ecb7c936bd157677', '88.87.4.197')
