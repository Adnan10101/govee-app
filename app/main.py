from flask import Flask, request, jsonify, render_template, redirect, url_for
import requests
import uuid
import os
import logging
import environment as env

from functions import (
    get_devices,
    device_toggle
)

app = Flask(__name__)

headers = {
        "Govee-API-Key" : env.GOVEE_API,
        "Content-Type" : "application/json"
    }

    
# will remove in the future
@app.route("/devices", methods = ["GET"])
def display_device_details():
    url = "https://openapi.api.govee.com/router/api/v1/user/devices"
    response = requests.get(url=url, headers = headers).json()
    return render_template("devices_temp.html", devices = response)

@app.route("/device/control", methods=["POST"])
def control_device():
    try:
        capability_instance = request.form.get("instance")
        capability_type = request.form.get("type")
        sku = request.form.get("sku")
        device_addr = request.form.get("device")
        
        action = request.form.get("submit")
        
        if action == "toggle_on_off":
            user_input = request.form.get(capability_instance)
            response = device_toggle(sku, device_addr, capability_instance, capability_type, headers, user_input)
        # elif action == "toggle_power_on_off":
        #     user_input = request.form.get(capability_instance)
        #     response = device_toggle(sku, device_addr, capability_instance, capability_type, headers, user_input)
        
        if response.ok:
            return redirect(url_for("device_details",device_id = sku))
        else:
            return f"Error: {response.text}", 400
    except Exception as e:
        logging.error("Error controlling device: %s", e)
        return "An error occurred while processing the request.", 500


@app.route("/device/<device_id>", methods = ["GET"])
def device_details(device_id):
    try:
        _, devices_detailed_data = get_devices(headers)
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
        devices, _ = get_devices(headers)
        return render_template("index.html", devices = devices)
    except Exception as e:
        logging.error("Error displaying device details: %s", e)
        return "An error occurred while fetching devices.", 500



if __name__ == "__main__":
    app.run(debug = True,host="0.0.0.0", port=5000)
