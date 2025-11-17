import requests
import time
import math
import pydirectinput as pd
import keyboard

Cx = 0.05

jitter_coeff = 0.045   # radians / second

BASE = "http://192.168.29.57:8080"   # Replace

def get_latest(buffer_name):
    url = f"{BASE}/get?{buffer_name}"
    r = requests.get(url).json()

    try:
        # Extract value from:
        # {"buffer": { "gyrX": { "buffer": [value] } } }
        return r["buffer"][buffer_name]["buffer"][0]
    except:
        return None

# gx = get_latest("gyrX")
# gy = get_latest("gyrY")
# gz = get_latest("gyrZ")

def movement_algorithm(dx, dy) :
    if dx == None and dy == None :
        time.sleep(1)

    else :
        if dx >= 0 :
            if dx >= jitter_coeff :
                dx = math.degrees(dx)
                dy = math.degrees(dy)
                Mx = (dx) / Cx
                My = (dy) / Cx

                pd.moveRel(int(Mx) * -1, int(My) * -1, duration = 0.2)   # only for Mx for now
                
                print(f"moved dx : {dx}, Mouse movement : {Mx}")
        if dx <= 0 :
            if dx <= (-1 * jitter_coeff) :
                dx = math.degrees(dx)
                dy = math.degrees(dy)
                Mx = (dx) / Cx
                My = (dy) / Cx

                pd.moveRel(int(Mx) * -1, int(My) * -1, duration = 0.2)   # only for Mx for now
                
                print(f"moved dx : {dx}, Mouse movement : {Mx}")

while True:
    movement_algorithm(get_latest("gyrZ"), get_latest("gyrX"))

    if keyboard.is_pressed("v") :
        break
