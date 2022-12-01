import pyautogui as gui
import time

screenWidth, screenHeight = gui.size()

class Button:
    __posX = -1
    __posY = -1
    
    def __init__(self, elemPos):
        if (elemPos[0] >= 0 and elemPos[0] <= screenWidth
            ) and (elemPos[1] >= 0 and elemPos[1] <= screenHeight):
            self.__posX = elemPos[0]
            self.__posY = elemPos[1]
        else:
            raise Exception("Button position is set outside of the screen boundaries.")
        
    def ReturnPosition(self):
        if self.__posX >= 0 and self.__posY >= 0:
            return [self.__posX, self.__posY]
        
    def ButtonClick(self):
        gui.click(self.__posX, self.__posY)
        
        
        
class ElementLocator:   
    def FindLocation(self):
        while True:
            currentMouseX, currentMouseY = gui.position()
            print(currentMouseX, currentMouseY)
            time.sleep(1)
            
    def ReturnElementPosition(self, elementName):
        if elementName in self.ELEMENTS_DICTIONARY:
            return self.ELEMENTS_DICTIONARY[elementName]
    
    def ReturnAllElementKeys(self):
        return self.ELEMENTS_DICTIONARY.keys()
            
    ELEMENTS_DICTIONARY = {
        "AppShortcutFocus":       [60,1065],
        "ChartButton0":           [1510, 200],
        "ChartButton1":           [1510, 370],
        "ChartButton2":           [1510, 550],
        "ChartButton3":           [1510, 730],
        "AllSensorsControl":      [125, 830],
        "SettingsOpen":           [150, 370],
        "SettingsPumpConnect":    [610, 625],
        "SettingsPumpDisconnect": [750, 625]
    }
    
class Test:
    search = ElementLocator()
    buttonConnect = Button(search.ReturnElementPosition("SettingsPumpConnect"))
    buttonDisconnect = Button(search.ReturnElementPosition("SettingsPumpDisconnect"))
    buttonAppFocus = Button(search.ReturnElementPosition("AppShortcutFocus"))
    buttonSettingsOpen = Button(search.ReturnElementPosition("SettingsOpen"))
        
    def PumpConnectDisconnect(self, counter):
        time.sleep(1)
        self.buttonAppFocus.ButtonClick()
        time.sleep(2)
        self.buttonSettingsOpen.ButtonClick()
        time.sleep(0.5)

        while counter > 0:
            self.buttonConnect.ButtonClick()
            time.sleep(0.5)
            self.buttonDisconnect.ButtonClick()
            time.sleep(0.5)
            counter -= 1