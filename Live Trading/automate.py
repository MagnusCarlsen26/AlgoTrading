import pyautogui
import time

def hover(x,y):
    pyautogui.moveTo(x, y)
    time.sleep(0.5)

def click(x,y):
    pyautogui.moveTo(x, y)
    pyautogui.click()
    
startOfSlider = 265
endOfSlider = 690
heightOfSlider = 790

for i in range(1,20):
    target = i/2
    click((endOfSlider-startOfSlider)/9*(target-0.5) + startOfSlider,800)