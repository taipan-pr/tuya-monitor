from abc import abstractmethod

import tinytuya


class Device:
    def __init__(self, device_id, local_key, ip_address):
        self.device_id = device_id
        self.local_key = local_key
        self.ip_address = ip_address
        self.device = tinytuya.OutletDevice(device_id, ip_address, local_key)
        self.device.set_version(3.3)
        self.device.set_socketPersistent(True)

    @abstractmethod
    def _process(self, data, func=None):
        pass

    def listen(self, func=None):
        while True:
            try:
                # See if any data is available
                data = self.device.receive()
                if data is None:
                    continue

                self._process(data, func)

            except:
                self.device.close()
                return
