import requests
import time
import math

BASE_URL = "" 

gyro_Xaxis = "gyrX"
gyro_Yaxis = "gyrY"
gyro_Zaxis = "gyrZ"

class Gyroscope() :
    def get_latest(buffer_name) :
        url_final = f"{BASE_URL}/get?{buffer_name}"
        r = requests.get(url_final).json()

        try :
            # Extract value from : 
            # {"buffer": { "gyrX": { "buffer": [value] } }
            return r["buffer"][buffer_name]["buffer"][0]
        except :
            return None
        
class Accelerometer() :
    def get_latest(buffer_name) :
        url_final = f"{BASE_URL}/get?{buffer_name}" 
        r = requests.get(url_final).json

        try :
            return r["buffer"][buffer_name]["buffer"][0]
        except :
            return None