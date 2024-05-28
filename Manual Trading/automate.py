import streamlit as st
import pyautogui
import time
def hover(x,y):
    pyautogui.moveTo(x, y)
    time.sleep(0.5)

def click(x,y):
    pyautogui.moveTo(x, y)
    pyautogui.click()
    time.sleep(0.5)
def buy(x):
    click((1125-790)/9*(x-0.5) + 790,460)

def drag_and_drop(start_x, start_y, end_x, end_y):

    pyautogui.moveTo(start_x, start_y)
    pyautogui.mouseDown(button='left')

    pyautogui.moveTo(end_x, end_y)
    pyautogui.mouseUp(button='left')

def execute(target):
    buy(target)
    pyautogui.scroll(-200, x=825, y=800)
    time.sleep(0.75)
    pyautogui.click(1050,600,clicks=19,interval = 0.01)
    pyautogui.click(1175,600,clicks=int((target)*2),interval = 0.01)

    drag_and_drop(725,950,1200,950)




st.title('Intraday Trading Dashboard')
selected_value = None

col1, col2 = st.columns(2)  # Create two columns for better arrangement

with col1:
    for value in range(1,11):
        if st.button(str(value/2)):
            selected_value = value/2
            execute(selected_value)
            print('Executing',selected_value)

with col2:
    for value in range(11,20):
        if st.button(str(value/2)):
            selected_value = value/2
            execute(selected_value)
            print('Executing',selected_value)
