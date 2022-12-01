import serialComms as sc
import threading as t
import time
from datetime import datetime

class TestRuns:
    f = open('config.json')
    Controller = sc.SerialGateway("")
    Controller.LoadConfig()
    Controller.Prepare()
    Controller.Init()
    Controller.stringToFind = "dispensed volume = "
    _ = t.Thread(target=Controller.AReadFromBufferInLine).start()
    
    def TestDispensedVolumeAccuracy(self, rate, volume, cycles):
        controller = self.Controller
        controller.testDataFileName = datetime.now().strftime("%d-%m-%Y") + "_rate-" + str(rate) + "_volume-" + str(volume) + "_cycles-" + str(cycles) + ".csv"
        controller.SendCommand(controller.Commands.SetRate(1, rate))
        controller.SendCommand(controller.Commands.SetRate(2, rate))
        runTime = ((60 * volume) / rate) + 3
        i = 1
        print("Running 'Dispensed Volume Accuracy' test with parameters:")
        print("Transfer rate: " + str(rate) + "\nPump volume:   " + str(volume))
        print("Pump run time: " + str(runTime) + "\nCycles:        " + str(cycles))
        print("TEST RUN TIME: " + str(cycles * (runTime + 2)) + "\n")
        time.sleep(3)
        while i < cycles:
            print("Cycle:  " + str(i))
            controller.SendCommand(controller.Commands.SetVolume(1, volume))
            controller.SendCommand(controller.Commands.SetVolume(2, volume))
            controller.SendCommand(controller.Commands.StartPump(1))
            controller.SendCommand(controller.Commands.StartPump(2))
            time.sleep(runTime)
            controller.SendCommand(controller.Commands.GetDispensedVolume(1))
            controller.SendCommand(controller.Commands.GetDispensedVolume(2))
            i += 1
            volume *= -1
            time.sleep(2)
        time.sleep(1)
        print("Finishing test run...\n")
        
    def TestDispensedVolumeFrequency(self):
        controller = self.Controller
        controller.testDataFileName = datetime.now().strftime("%d-%m-%Y") + "_vol-freq.txt"
        controller.SendCommand(controller.Commands.SetRate(1, 90))
        controller.SendCommand(controller.Commands.SetVolume(1, -30))
        cycles = 80
        i = 1
        time.sleep(1)
        controller.SendCommand(controller.Commands.StartPump(1))
        time.sleep(1)
        while i < cycles:
            controller.SendCommand(controller.Commands.GetDispensedVolume(1))
            time.sleep(0.05)
            i += 1
        time.sleep(1)
        print("Finishing test run...\n")



# --- MAIN ---

test = TestRuns()

test.TestDispensedVolumeFrequency()

# test.TestDispensedVolumeAccuracy(20, 1, 5)
# test.TestDispensedVolumeAccuracy(5, 1, 500)
# test.TestDispensedVolumeAccuracy(20, 2, 500)
# test.TestDispensedVolumeAccuracy(50, 5, 500)
# test.TestDispensedVolumeAccuracy(60, 20, 500)
# test.TestDispensedVolumeAccuracy(10, 10, 500)
# test.TestDispensedVolumeAccuracy(10, 30, 500)
# test.TestDispensedVolumeAccuracy(1, 25, 500)
print("\nFINISHING TESTS...\n")
time.sleep(5)
test.Controller.ToggleShouldRunProcess()
