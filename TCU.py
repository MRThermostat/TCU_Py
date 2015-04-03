import serial
import time
ser = serial.Serial('COM10', 9600, timeout=0)

while 1:
    var = input("Enter something: ")
    outgoing = var.encode('utf-8')
    print("Encoded to %s\n" % outgoing)
    ser.write(outgoing)
    var = outgoing.decode()
    print("Decoded to %s\n" % var)
    print("Arduino:\n %s\n" % ser.readline())
    time.sleep(1)
