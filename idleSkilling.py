import keyboard
import mss
import cv2
import numpy
from time import time, sleep
import pyautogui
from utils.screen.Screen import Screen
from utils.Mouse import Mouse
import threading

print("Press 'f' to start fighting.")
print("Press 's' to take screenshot area.")
print("Press 2 to start training")
print("Once started press 'q' to quit.")

# Configuring the game2
monitorNumber = 2
mouse = Mouse(pyautogui,sleep)
screen = Screen(mss, cv2, numpy, mouse, sleep)
screen.setMonitorNumber(2)
screen.selectGameArea()

# Configuring threads
workerThread = threading.Thread(target=screen.trainAll)

# Main loop2
while True:
    if keyboard.is_pressed('q'):
        break
    if keyboard.is_pressed("1"):
        img = screen.takeGameScreenshot()
        screen.showImage(img)
    if keyboard.is_pressed("2"): # Start Training
        screen.trainAll()
    if keyboard.is_pressed("3"): # Start Fight
        screen.goToFight()


 
        

