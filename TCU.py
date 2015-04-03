import serial
import time
ser = serial.Serial('COM10', 9600, timeout=0)

while 1:
    time.sleep(1)
    incoming = ser.readline()
    start = incoming.find(b'ssid=')
    end = incoming.find(b'&')
    outgoing = incoming[start+5:end+1] #'&' is SSID terminal character
    print("SSID: %s" % outgoing)
    start = incoming.find(b'pw=', end+1)
    end = incoming.find(b'HTTP/1.1', start+3)
    append = incoming[start+3:end-1]
    outgoing = append + b'$' #'$' is Password terminal character
    print("Password: %s\n" % outgoing)



while 0:
    var = input("Enter something: ")
    outgoing = var.encode('utf-8')
    time.sleep(.01)
    ser.write(outgoing)
    var = outgoing.decode()
    time.sleep(.01)
    print("Arduino:\n %s\n" % ser.readline())
