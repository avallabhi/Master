import os
import time
from pynput.keyboard import KeyCode,Controller


os.system("open -a Messages")

time.sleep(3)

keyboard = Controller()

keyboard.type("Hi how are you")
time.sleep(3)
keyboard.press(KeyCode.enter)


