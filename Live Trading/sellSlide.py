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
    
startOfSlider = 265
endOfSlider = 690
heightOfSlider = 790

sio = socketio.Client()

@sio.on('sell')
def handle_trade(data):
    x_coordinate = (endOfSlider - startOfSlider) / 9 * (price - 0.5) + startOfSlider
    click(x_coordinate, 800)
    sio.emit('confirmSell', f'Sold for {price}')


if __name__ == '__main__':
    try:
        sio.connect('http://localhost:8080')
        sio.wait()
    except socketio.exceptions.ConnectionError as e:
        print("Connection error:", e)
