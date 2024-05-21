import pyautogui
import time
import socketio 
from flask_socketio import emit

def hover(x,y):
    pyautogui.moveTo(x, y)
    time.sleep(0.5)

def click(x,y):
    pyautogui.moveTo(x, y)
    pyautogui.click()

def drag_and_drop(start_x, start_y, end_x, end_y):

    pyautogui.moveTo(start_x, start_y)
    pyautogui.mouseDown(button='left')

    pyautogui.moveTo(end_x, end_y)
    pyautogui.mouseUp(button='left')

sliderx = 265
sliderxx = 690
slidery = 1000

pricex = 330
pricexx = 610
pricey = 535

sio = socketio.Client()

import random
@sio.on('buy')
def sell(price):
    price = random.randint(1,9)
    click((pricexx-pricex)/9*(price-0.5) + pricex,pricey) # Set Price
    click(332,635) # Quantity = 1
    print('Bought',price)
    # drag_and_drop(sliderx,slidery,sliderxx,slidery) # Buy SLide    
    # Reload /arena
    # Reload /portfolio
    sio.emit('confirmBuy',1)


if __name__ == '__main__':
    sio.connect('http://localhost:8080')
    sio.wait()
