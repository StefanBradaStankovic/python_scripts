import pyautogui as gui
import time

startButtonsListInList = [[1510, 200], [1510, 370], [1510, 550], [1510, 730]]
startButtonsTupleInList = [(1510, 200), (1510, 370), (1510, 550), (1510, 730)]

""" def findLocation():
    while True:
        currentMouseX, currentMouseY = gui.position()
        print(currentMouseX, currentMouseY)
        time.sleep(1) """
        

def buttonClick(timeout, buttonPos):
    if timeout !=0:
        time.sleep(timeout)
    
    gui.click(buttonPos[0], buttonPos[1])