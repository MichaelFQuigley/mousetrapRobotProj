import thread
import serial
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class BTPeripheral:

    def __init__(self, btDeviceName, readTimeout = 0.01):
        self.btDeviceName = btDeviceName 
        self.serPort      = None
        self.readTimeout  = readTimeout

    #returns false on failure
    def connect(self):
        baudRate = 9600
        try:
            self.serPort = serial.Serial(self.btDeviceName, baudRate, timeout=self.readTimeout)
        except:
            return False
        return True

    def send(self, text): 
        self.serPort.write(str(text))

    def close(self):
        self.serPort.close()

    def startListeningForRead(self, callback):
        thread.start_new_thread(self.readWorker, (callback,))

    #callback takes format callback(string)
    def readWorker(self, callback):
        while True:
            inStr = self.read()
            if len(inStr) > 0:
                callback(inStr)

    def read(self):
        resultStr = ""
        ch        = self.serPort.read()
        while len(ch) > 0:
            resultStr += ch
            ch = self.serPort.read()
        return resultStr




#exampleUsage

def prinnnt(x):
    print bcolors.OKGREEN + x + bcolors.ENDC

peripheral = BTPeripheral('/dev/cu.HC-06-DevB')

if peripheral.connect():
    peripheral.startListeningForRead(prinnnt)
    try:
        while True:
            peripheral.send(str(raw_input("Input to send:\n")) + '\n')
    finally:
        peripheral.close()
else:
    print "Could not connect"
