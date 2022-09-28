from typing import Dict

import socketio

# Key -> Device id
# Value -> Socket id
hardware_devices: Dict[str, str] = {}


class HardwareNameSpace(socketio.AsyncNamespace):
    def on_connect(self, sid, environ):
        print(f"Hardware {sid} connected to namespace: {self.namespace}")

    def on_disconnect(self, sid, *args, **kwargs):
        print(f"Hardware {sid} disconnected from namespace: {self.namespace}")
        print("Before pop: ", hardware_devices)
        for k, v in hardware_devices.items():
            if v == sid:
                hardware_devices.pop(k)
                break
        print("After pop: ", hardware_devices)

    async def on_register_device(self, sid, data):
        device_id = data["device_id"]
        hardware_devices[device_id] = sid
        print("Register device id")
