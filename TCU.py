import serial
import time
import json
import ast

ARDUINO = 0

if ARDUINO:
    ser = serial.Serial('COM10', 9600, timeout=0)

while 0:
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

#Trying to parse json
info = json.loads('{\r\n\t"fan":"on",\r\n\t"system":"heat",\r\n\t"profileList":[\r\n\t\t{\r\n\t\t\t"active":0,\r\n\t\t\t"profileRulesList":[\r\n\t\t\t\t{\r\n\t\t\t\t\t"setting":70,\r\n\t\t\t\t\t"start_condition":1400,\r\n\t\t\t\t\t"end_condition":2300,\r\n\t\t\t\t\t"type":"Time",\r\n\t\t\t\t\t"Profile_Name":"Weekend"\r\n\t\t\t\t},\r\n\t\t\t\t{\r\n\t\t\t\t\t"setting":66,\r\n\t\t\t\t\t"start_condition":300,\r\n\t\t\t\t\t"end_condition":500,\r\n\t\t\t\t\t"type":"Time",\r\n\t\t\t\t\t"Profile_Name":"Weekend"\r\n\t\t\t\t}\r\n\t\t\t],\r\n\t\t\t"name":"Weekend"\r\n\t\t},\r\n\t\t{\r\n\t\t\t"active":1,\r\n\t\t\t"profileRulesList":[\r\n\t\t\t\t{\r\n\t\t\t\t\t"setting":66,\r\n\t\t\t\t\t"start_condition":100,\r\n\t\t\t\t\t"end_condition":700,\r\n\t\t\t\t\t"type":"Time",\r\n\t\t\t\t\t"Profile_Name":"Work Week"\r\n\t\t\t\t},\r\n\t\t\t\t{\r\n\t\t\t\t\t"setting":72,\r\n\t\t\t\t\t"start_condition":800,\r\n\t\t\t\t\t"end_condition":1400,\r\n\t\t\t\t\t"type":"Time",\r\n\t\t\t\t\t"Profile_Name":"Work Week"\r\n\t\t\t\t}\r\n\t\t\t],\r\n\t\t\t"name":"Work Week"\r\n\t\t},\r\n\t\t{\r\n\t\t\t"active":0,\r\n\t\t\t"profileRulesList":[\r\n\t\t\t],\r\n\t\t\t"name":"Vacation"\r\n\t\t}\r\n\t],\r\n\t"sensorList":[\r\n\t\t{\r\n\t\t\t"active":1,\r\n\t\t\t"name":"Porch",\r\n\t\t\t"temperature":55\r\n\t\t},\r\n\t\t{\r\n\t\t\t"active":1,\r\n\t\t\t"name":"Basement",\r\n\t\t\t"temperature":65\r\n\t\t},\r\n\t\t{\r\n\t\t\t"active":0,\r\n\t\t\t"name":"Porch",\r\n\t\t\t"temperature":80\r\n\t\t},\r\n\t\t{\r\n\t\t\t"active":1,\r\n\t\t\t"name":"Bedroom",\r\n\t\t\t"temperature":55\r\n\t\t},\r\n\t\t{\r\n\t\t\t"active":1,\r\n\t\t\t"name":"Foyer",\r\n\t\t\t"temperature":50\r\n\t\t},\r\n\t\t{\r\n\t\t\t"active":1,\r\n\t\t\t"name":"Kitchen",\r\n\t\t\t"temperature":50\r\n\t\t}\r\n\t]\r\n}')
json_info = json.dumps(info)
decoded_info = json.loads(json_info)

profileList = ', '.join(map(str, decoded_info["profileList"]))
profileRulesList = ast.literal_eval(profileList)
profileCount = 0
for rules in profileRulesList:
    profileCount += 1
    print("\nProfile \"%s\":" % rules["name"])
    json_info = json.dumps(rules)
    decoded_info = json.loads(json_info)
    profileRule = ', '.join(map(str, decoded_info["profileRulesList"]))
    profileRuleVals = ast.literal_eval(profileRule)
    ruleCount = 0
    for values in profileRuleVals:
        ruleCount += 1
        print("\tRule %d:" % ruleCount)
        json_info = json.dumps(values)
        decoded_info = json.loads(json_info)
        conds = decoded_info
        print("\t\tStart Conditions: %d" % conds["start_condition"])
        print("\t\tEnd Conditions: %d" % conds["end_condition"])
        print("\t\tSettings: %d" % conds["start_condition"])
        print("\t\tProfile Name: %d" % conds["start_condition"])
        print("\t\tType: %d" % conds["start_condition"])
    
sensorList = ', '.join(map(str, decoded_info["sensorList"]))    
