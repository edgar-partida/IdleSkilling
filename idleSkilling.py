import keyboard
import mss
import cv2
import numpy
from time import time, sleep
import pyautogui
import util as util
from utils.screen.Screen import Screen
from utils.Mouse import Mouse



monitorNumber = 2

print("Press 'f' to start fighting.")
print("Press 's' to take screenshot area.")
print("Press 2 to start training")
print("Once started press 'q' to quit.")

# Configuring the game
mouse = Mouse(pyautogui)
screen = Screen(mss, cv2, numpy, mouse)
screen.setMonitorNumber(2)
screen.selectGameArea()

# Main loop
while True:
    if keyboard.is_pressed('q'):
        break
    if keyboard.is_pressed("1"):
        img = screen.takeGameScreenshot()
        screen.showImage(img)
    if keyboard.is_pressed("2"): # Start Training2
        screen.goToTraining()
    if keyboard.is_pressed("3"): # Start Fight
        screen.goToFight()


    

2
 
        

