# Phyphox Sensor Integration with Python

This project provides a simple and reliable way to access smartphone sensor data through the Phyphox app and use it inside Python scripts. It is useful for physics experiments, robotics prototypes, motion tracking, and real-time sensor logging without needing extra hardware.

## Overview

Phyphox exposes mobile sensor data over a local network. This project shows how to request those values from a running Phyphox experiment and process them in Python using basic HTTP requests.

Supported sensors depend on your phone, but commonly include:

- Accelerometer
- Gyroscope
- Magnetometer
- Pressure sensor
- Light sensor
- Additional sensors supported by Phyphox

## How It Works

1. Install the Phyphox app on your phone.
2. Open any experiment that supports remote access.
3. Enable the "Remote Access" option in the experiment.
4. Note the IP address and port shown inside the app.
5. Update the `URL` URL in your Python script accordingly.
6. Use the script in this repository to pull sensor data via HTTP.

Your Python code sends GET requests, Phyphox responds with JSON, and you extract the values you need.

## Requirements

- Python 3
- `requests` library
- Smartphone with Phyphox installed
- Both devices connected to the same Wi-Fi network
