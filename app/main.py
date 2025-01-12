from flask import Flask, request, jsonify, render_template
import requests
import uuid
import os
import logging

app = Flask(__name__)

headers = {
        "Govee-API-Key" :  "",
        "Content-Type" : "application/json"
    }

def get_devices():
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

def device_power_onoff(self, id, device_addr, instance, state=0):
    url = "https://openapi.api.govee.com/router/api/v1/device/control"
    content = {
        "requestId": str(uuid.uuid4()),
        "payload": {
            "sku": id,
            "device": device_addr,
            "capability": {
                "type": "devices.capabilities.on_off",
                "instance": instance,
                "value": state
            }
        }
    }
    response = requests.post(url=url, headers=self.header, json=content)
    return response.status_code, response.json()

    
# will remove in the future
@app.route("/devices", methods = ["GET"])
def display_device_details():
    url = "https://openapi.api.govee.com/router/api/v1/user/devices"
    response = requests.get(url=url, headers = headers).json()
    return render_template("devices_temp.html", devices = response)


# Understand how this shitty flask works or switch to astapi
# work on routing (when i submit it works but i have to hit the back button to return home)
# @app.route("/device/on_off", methods=["POST"])
# def device_power_onoff():
#     # Retrieve form data
#     form_data = request.form

#     # Convert form data to JSON-like dictionary
#     data = {
#         "deviceaddr": form_data.get("deviceaddr"),
#         "deviceId": form_data.get("deviceId"),
#         "instance": form_data.get("instance"),
#         "state": int(form_data.get("state")),  # Convert to int
#     } 

#     govee = Govee()
#     status_code, response = govee.device_power_onoff(
#         id=data["deviceId"],
#         device_addr=data["deviceaddr"],  # Assuming deviceId is used here
#         instance=data["instance"],
#         state=data["state"]
#     )
#     return jsonify(response), status_code




@app.route("/device/<device_id>", methods = ["GET"])
def device_details(device_id):
    try:
        _, devices_detailed_data = get_devices()
        #device_capabilities = None
        for device_detailed_data in devices_detailed_data:
            if device_id == device_detailed_data["sku"]:
                 device_data = {
                    "Device addr": device_detailed_data["device"],
                    "Device ID":   device_detailed_data["sku"],
                    "Device Name": device_detailed_data["deviceName"]
                }
            device_capabilities = device_detailed_data.get("capabilities", [])
            break 
        return render_template("devices.html", device_capabilities = device_capabilities, device_data = device_data)
    except Exception as e:
        logging.error("Error fetching details for device %s: %s", device_id, e)
        return "An error occurred while fetching device details.", 500
    
    
@app.route("/", methods=["GET", "POST"])
def index(): 
    try:
        devices, _ = get_devices()
        return render_template("index.html", devices = devices)
    except Exception as e:
        logging.error("Error displaying device details: %s", e)
        return "An error occurred while fetching devices.", 500



if __name__ == "__main__":
    app.run(debug = True,host="0.0.0.0", port=5000)
