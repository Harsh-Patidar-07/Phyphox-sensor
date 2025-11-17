import requests
import time
import math

BASE_URL = "" 

Xaxis = "gyrX"
Yaxis = "gyrY"
Zaxis = "gyrZ"

def get_latest(buffer_name) :
    url_final = f"{url}/get?{buffer_name}"
    r = requests.get(url_final).json()

    try :
        # Extract value from : 
        # {"buffer": { "gyrX": { "buffer": [value] } }
        return r["buffer"][buffer_name]["buffer"][0]
    except :
        return None
