import serial
import serial.tools.list_ports
from timeit import default_timer as timer
from time import sleep
import matplotlib.pyplot as plt
from numpy import std
import csv

# self defined function for this script
#-----------------------------------------------
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

# set up serial port communication
#-----------------------------------------------
def get_ports(): 
    ports = serial.tools.list_ports.comports()
    return ports

def findArduino(portsFound): 

    commPort = 'None'
    numConnection = len(portsFound)

    for i in range(0,numConnection): 
        port = foundPorts[i]
        strPort = str(port)
        
        if 'usbmodem' in strPort: #it is understood that 'usbmodem1101' can be used to identify the port of interest
            splitPort = strPort.split(' ')
            commPort = splitPort[0]
    return commPort

foundPorts = get_ports()
connectPort = findArduino(foundPorts)

if connectPort != 'None': 
    ser = serial.Serial(connectPort,baudrate=115200,timeout=1)
    print('Connected to ' + connectPort)

else:
    print('Connection Issue!')


if ser.is_open == True:
    ser.close()
    print("Port was already open, closing.")
    
ser.open()
print("Opening port connection")

# collect data
#-----------------------------------------------
# ask for input: current opsition of knife
position = input('What is the current position of knife in unit (mm)?\n')
if isfloat(position):
    position = float(position) / 1000


y = []
N = 200 # number of samples points per scan
waitTime = 2 # wait time in between scans
n = 3 # number of scans
testrun1 = ser.readline()
testrun2 = ser.readline()
testrun3 = ser.readline() # for unknown reasons, first three readlin() calls take long time
for j in range(0,n-1):
    for i in range(0,N):
        line = ser.readline()  
        if line: 
            string = line.decode()
            num = int(string)
            y.append(num/1024*5 )
    sleep(waitTime)

print("finish data collection")
ser.close()
print("serial port closed")

# process data and write into csv
#-----------------------------------------------
voltage = sum(y) / (N*n)
stdev = std(y)
row = [position, voltage,stdev]
# please input dataFile position here!!!
dataFile = '/Users/JohnnyLin/Desktop/Dzmitry_Lab /UROPS/cavity/BeamWidthOfFiberBeam/measurement1.csv'
with open(dataFile,'a') as f: 
    writer = csv.writer(f)
    writer.writerow(row)

print('all done')