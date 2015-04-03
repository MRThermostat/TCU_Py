import serial
import time
ser = serial.Serial('COM10', 9600, timeout=0)

while 1:
    incoming = ser.readline()
    temp = -1
    temp = incoming.find(b'GET /?')
    time.sleep(0.01)
    if(temp != -1):
        start = incoming.find(b'ssid=', temp)
        end = incoming.find(b'&')
        outgoing = incoming[start+5:end+1] #'&' is SSID terminal character
        print("SSID: %s" % outgoing)
        start = end + 4
        end = incoming.find(b'HTTP/1.1', start)
        append = incoming[start:end-1]
        outgoing = append + b'$' #'$' is Password terminal character
        print("Password: %s\n" % outgoing)
#    else:
#        if(incoming != b''):
#            print(incoming)

while 0:
    test = ser.readline()
    if(test != b''):
        print(test)
    time.sleep(.1)

while 0:
    var = input("Enter something: ")
    outgoing = var.encode('utf-8')
    time.sleep(.01)
    ser.write(outgoing)
    var = outgoing.decode()
    time.sleep(.01)
    print("Arduino:\n %s\n" % ser.readline())
