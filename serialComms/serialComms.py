import json, serial, time
from datetime import datetime
    
class SerialCommands:
    __HELP = "help"
    __PUMP_START = " start 0"
    __SET_VOLUME = " set volume "
    __SET_RATE = " set rate "
    __GET_DISPENSED_VOLUME = " dispensed volume"
    __GET_PUMP_STATUS = " pump status"
    
    def __init__(self):
        pass
    
    def Help(self):
        return self.__HELP
    
    def StartPump(self, pumpNumber):
        return str(pumpNumber) + self.__PUMP_START
    
    def SetRate(self, pumpNumber, value):
        return str(pumpNumber) + self.__SET_RATE + str(value)

    def SetVolume(self, pumpNumber, value):
        return str(pumpNumber) + self.__SET_VOLUME + str(value)
    
    def GetDispensedVolume(self, pumpNumber):
        return str(pumpNumber) + self.__GET_DISPENSED_VOLUME
    
    def GetPumpStatus(self, pumpNumber):
        return str(pumpNumber) + self.__GET_PUMP_STATUS

class SerialGateway:
    __port = ""
    __baudrate = ""
    __ser = serial.Serial()
    __shouldRunProcess = True
    testDataFileName = "test_data.txt"
    stringToFind = ""
    Commands = SerialCommands()
    
    def __init__(self, config):
        if(config != ""):
            self.__port = config["port"]
            self.__baudrate = config["baudrate"]
        else:
            pass
    
    @property
    def Port(self):
        return self.__port
    @property
    def Baudrate(self):
        return self.__baudrate
    @property
    def ShouldRunProcess(self):
        return self.__shouldRunProcess
    
    @Port.setter
    def Port(self, port):
        if(port[0:3] == "COM" and port[3:].isnumeric()):
            self.__port = port
        else:
            raise ValueError("Invalid com port - please comply to the criteria: 'COM<int>' !")
    @Baudrate.setter
    def Baudrate(self, baudrate):
        if(baudrate.isnumeric()):
            self.__baudrate = baudrate
        else:
            raise ValueError("Invalid baudrate - please comply to the criteria: '<int>' !")
    
    def LoadConfig(self):
        __f = open("config.json", "r")
        data = json.load(__f)
        self.Port = data["port"]
        self.Baudrate = data["baudrate"]
        __f.close()
           
    def Prepare(self):
        print("Preparing port: " + self.__port + " with baudrate: " + self.__baudrate)
        self.__ser = serial.Serial(port = self.__port, baudrate = self.__baudrate, timeout=0.1)
        self.__ser.close()
        
    def Init(self):
        self.__ser.close()
        self.__ser.setDTR(False)
        if not self.__ser.is_open:
            print("Opening serial port!")
            self.__ser.open()
            
    def SendCommand(self, command):
        time.sleep(0.2)
        print(command)
        self.__ser.write(command.encode('utf_8'))
        self.__ser.write(b"\r")
        # self.SReadFromBuffer()
        pass
               
    def ToggleShouldRunProcess(self):
        if(self.__shouldRunProcess):
            self.__shouldRunProcess = False
        else:
            self.__shouldRunProcess = True
    
    def SReadFromBufferAndListen(self):
        time.sleep(0.1)
        while self.__ser.in_waiting:
            linein = self.__ser.readline().strip().decode( "utf-8" )
            print(linein)
            if linein.find(self.stringToFind) != -1:
                self.__WriteToFile(self.__ExtractValue(linein))
        
    def AReadFromBufferIntoCSV(self):
        time.sleep(0.1)
        valueModifyer = 1
        valueSeparator = ", "
        while self.__shouldRunProcess:
            while self.__ser.in_waiting:
                linein = self.__ser.readline().strip().decode( "utf-8" )
                print(linein)
                if linein.find(self.stringToFind) != -1:
                    self.__WriteToFile(str(float(self.__ExtractValue(linein)) * valueModifyer) + valueSeparator)
                    if valueSeparator == ", ":
                        valueSeparator = "\n"
                    else:
                        valueSeparator = ", "
                        valueModifyer = valueModifyer * -1
        
    def AReadFromBufferInLine(self):
        time.sleep(0.1)
        while self.__shouldRunProcess:
            while self.__ser.in_waiting:
                linein = self.__ser.readline().strip().decode( "utf-8" )
                print(linein)
                if linein.find(self.stringToFind) != -1:
                    self.__WriteToFile(str(datetime.now()) + " - " + str(self.__ExtractValue(linein)) + "\n")
                    
    
    def __ExtractValue(self, string):
        listOfstrings = string.split(" = ")
        return listOfstrings[-1]

    def __WriteToFile(self, value):
        __f = open(self.testDataFileName, "a")
        __f.write(value)
        __f.close()