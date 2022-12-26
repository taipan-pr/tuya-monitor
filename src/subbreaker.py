from device import Device


class SubBreaker(Device):
    def _process(self, data):
        if 't' not in data:
            return

        print('Received Payload: %r' % data)

    def __init__(self, device_id, local_key, ip_address):
        Device.__init__(self, device_id, local_key, ip_address)
