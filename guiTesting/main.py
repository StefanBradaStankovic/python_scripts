import pyautogui as gui
import elements as elem
import time

screenWidth, screenHeight = gui.size()
test = elem.Test()
test.PumpConnectDisconnect(10)

