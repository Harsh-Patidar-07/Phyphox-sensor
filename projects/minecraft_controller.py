import requests
import time
import math
import pydirectinput as pd
import keyboard

Cx = 0.05

jitter_coeff = 0.045   # radians / second

BASE = "http://192.168.29.57:8080"   # Replace

def mouseMovement(target_x, target_y, steps=5, delay=0.05):
    """
    Smoothly moves the mouse from current position to (target_x, target_y).

    :param target_x: X coordinate to move to
    :param target_y: Y coordinate to move to
    :param steps: Number of small steps (higher = smoother)
    :param delay: Delay between steps (lower = faster)
    """
    current_x, current_y = pd.position()

    step_x = (target_x - current_x) / steps
    step_y = (target_y - current_y) / steps

    for _ in range(steps):
        current_x += step_x
        current_y += step_y
        pd.moveTo(int(current_x), int(current_y))
        time.sleep(delay)

    # Ensure exact final position
    pd.moveTo(target_x, target_y)

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
        print("Waiting for sensor to come in !")

    else :
        if dx >= 0 :
            if dx >= jitter_coeff :
                dx = math.degrees(dx)
                dy = math.degrees(dy)
                Mx = (dx) / Cx
                My = (dy) / Cx

                # pd.moveRel(int(Mx) * -1, 0, duration = 0.1)   # only for Mx for now
                mouseMovement(int(Mx) * -1, 0)

                print(f"moved dx : {dx}, Mouse movement : {Mx}")
        if dx <= 0 :
            if dx <= (-1 * jitter_coeff) :
                dx = math.degrees(dx)
                dy = math.degrees(dy)
                Mx = (dx) / Cx
                My = (dy) / Cx

                # pd.moveRel(int(Mx) * -1, 0, duration = 0.2)   # only for Mx for now
                mouseMovement(int(Mx) * -1, 0)

                print(f"moved dx : {dx}, Mouse movement : {Mx}")

while True:
    movement_algorithm(get_latest("gyrZ"), get_latest("gyrX"))

    if keyboard.is_pressed("v") :
        break
