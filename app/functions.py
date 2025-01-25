import requests
import uuid

# def device_power_onoff(self, id, device_addr, instance, capability, state=0):
#     url = "https://openapi.api.govee.com/router/api/v1/device/control"
#     content = {
#         "requestId": str(uuid.uuid4()),
#         "payload": {
#             "sku": id,
#             "device": device_addr,
#             "capability": {
#                 "type": capability,
#                 "instance": instance,
#                 "value": state
#             }
#         }
#     }
#     response = requests.post(url=url, headers=self.header, json=content)
#     return response.status_code, response.json()


def device_toggle(id, device_addr, instance, capability, headers, state=0):
    print("aaa", instance)
    print("bbb ", capability)
    url = "https://openapi.api.govee.com/router/api/v1/device/control"
    content = {
        "requestId": str(uuid.uuid4()),
        "payload": {
            "sku": id,
            "device": device_addr,
            "capability": {
                "type": capability,
                "instance": instance,
                "value": int(state)
            }
        }
    }
    response = requests.post(url=url, headers = headers, json=content)
    return response


def get_devices(headers):
    url = "https://openapi.api.govee.com/router/api/v1/user/devices"
    response = requests.get(url=url, headers = headers).json()
    #logging.print("lol::::::::",response)
    devices_details = response.get("data",[])
    
    devices = []
    for device in devices_details:
        device_address = device.get("device","")
        device_id = device.get("sku","")
        device_name = device.get("deviceName", "")
        device_data = {
            "Device addr": device_address,
            "Device ID":   device_id,
            "Device Name": device_name
        }
        devices.append(device_data)
    return devices, devices_details