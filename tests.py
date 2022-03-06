import keyboard

def callback(event):
    print(event.name)

keyboard.on_release(callback=callback)
keyboard.wait()