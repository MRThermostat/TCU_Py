import serial
import time
ser = serial.Serial('COM10', 9600, timeout=0)

while 1:
    var = input("Enter something: ")
    outgoing = var.encode('utf-8')
    time.sleep(.01)
    ser.write(outgoing)
    var = outgoing.decode()
    time.sleep(.01)
    print("Arduino:\n %s\n" % ser.readline())
