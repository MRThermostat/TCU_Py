import serial
import time
import json
import ast
import itertools

ARDUINO = 0
JSON = 0
CREATEJSON = 1
NETWORKSETUP = 0

if ARDUINO: #Enables the use of serial port
    ser = serial.Serial('COM10', 9600, timeout=0)

while NETWORKSETUP: #Pulls SSID and password from HTML page
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
    else:
        if(incoming != b''):
            print(incoming)
            
while 0: #Simply reads the serial
    test = ser.readline()
    if(test != b''):
        print(test)
    time.sleep(.1)

while 0: #Test to send stuff over serial
    var = input("Enter something: ")
    outgoing = var.encode('utf-8')
    time.sleep(.01)
    ser.write(outgoing)
    var = outgoing.decode()
    time.sleep(.01)
    print("Arduino:\n %s\n" % ser.readline())

if JSON: #Parses incoming JSON file from Android app
    #testing data
    info = json.loads('{\r\n\t"fan":"on",\r\n\t"system":"heat",\r\n\t"profileList":[\r\n\t\t{\r\n\t\t\t"active":0,\r\n\t\t\t"profileRulesList":[\r\n\t\t\t\t{\r\n\t\t\t\t\t"setting":70,\r\n\t\t\t\t\t"start_condition":1400,\r\n\t\t\t\t\t"end_condition":2300,\r\n\t\t\t\t\t"type":"Time",\r\n\t\t\t\t\t"Profile_Name":"Weekend"\r\n\t\t\t\t},\r\n\t\t\t\t{\r\n\t\t\t\t\t"setting":66,\r\n\t\t\t\t\t"start_condition":300,\r\n\t\t\t\t\t"end_condition":500,\r\n\t\t\t\t\t"type":"Time",\r\n\t\t\t\t\t"Profile_Name":"Weekend"\r\n\t\t\t\t}\r\n\t\t\t],\r\n\t\t\t"name":"Weekend"\r\n\t\t},\r\n\t\t{\r\n\t\t\t"active":1,\r\n\t\t\t"profileRulesList":[\r\n\t\t\t\t{\r\n\t\t\t\t\t"setting":66,\r\n\t\t\t\t\t"start_condition":100,\r\n\t\t\t\t\t"end_condition":700,\r\n\t\t\t\t\t"type":"Time",\r\n\t\t\t\t\t"Profile_Name":"Work Week"\r\n\t\t\t\t},\r\n\t\t\t\t{\r\n\t\t\t\t\t"setting":72,\r\n\t\t\t\t\t"start_condition":800,\r\n\t\t\t\t\t"end_condition":1400,\r\n\t\t\t\t\t"type":"Time",\r\n\t\t\t\t\t"Profile_Name":"Work Week"\r\n\t\t\t\t}\r\n\t\t\t],\r\n\t\t\t"name":"Work Week"\r\n\t\t},\r\n\t\t{\r\n\t\t\t"active":0,\r\n\t\t\t"profileRulesList":[\r\n\t\t\t\t{\r\n\t\t\t\t\t"setting":70,\r\n\t\t\t\t\t"start_condition":1400,\r\n\t\t\t\t\t"end_condition":2300,\r\n\t\t\t\t\t"type":"Time",\r\n\t\t\t\t\t"Profile_Name":"Vacation"\r\n\t\t\t\t},\r\n\t\t\t\t{\r\n\t\t\t\t\t"setting":66,\r\n\t\t\t\t\t"start_condition":300,\r\n\t\t\t\t\t"end_condition":500,\r\n\t\t\t\t\t"type":"Time",\r\n\t\t\t\t\t"Profile_Name":"Vacation"\r\n\t\t\t\t}\r\n\t\t\t],\r\n\t\t\t"name":"Vacation"\r\n\t\t}\r\n\t],\r\n\t"sensorList":[\r\n\t\t{\r\n\t\t\t"active":1,\r\n\t\t\t"name":"Porch",\r\n\t\t\t"temperature":55\r\n\t\t},\r\n\t\t{\r\n\t\t\t"active":1,\r\n\t\t\t"name":"Basement",\r\n\t\t\t"temperature":65\r\n\t\t},\r\n\t\t{\r\n\t\t\t"active":0,\r\n\t\t\t"name":"Porch",\r\n\t\t\t"temperature":80\r\n\t\t},\r\n\t\t{\r\n\t\t\t"active":1,\r\n\t\t\t"name":"Bedroom",\r\n\t\t\t"temperature":55\r\n\t\t},\r\n\t\t{\r\n\t\t\t"active":1,\r\n\t\t\t"name":"Foyer",\r\n\t\t\t"temperature":50\r\n\t\t},\r\n\t\t{\r\n\t\t\t"active":1,\r\n\t\t\t"name":"Kitchen",\r\n\t\t\t"temperature":50\r\n\t\t}\r\n\t]\r\n}')

    json_info = json.dumps(info)
    decoded_info = json.loads(json_info)

    print("\nFan Status: %s" % decoded_info["fan"])
    print("\nSystem Status: %s" % decoded_info["system"])

    profileList = ', '.join(map(str, decoded_info["profileList"]))
    sensorList = ', '.join(map(str, decoded_info["sensorList"]))

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
            print("\t\tProfile Name: %s" % conds["Profile_Name"])
            print("\t\tType: %s" % conds["type"])
        
    sensorInfoList = ast.literal_eval(sensorList)
    sensorCount = 0
    for sensors in sensorInfoList:
        sensorCount += 1
        print("\nSensor %d:" % sensorCount)
        print("\tName: %s" % sensors["name"])
        print("\tTemperature: %d" % sensors["temperature"])
        if sensors["active"]:
            print("\tActive: True")
        else:
            print("\tActive: False")

if CREATEJSON: #Creates JSON for Android app
    #testing data block
    settings,start_cond,end_cond,types,profile_name = 72,800,1400,"Time","Work Week" #Rule structure
    active,name = 0,"Weekend" #Profile structure
    active_s,name_s,temperature = 1,"Porch",55 #Sensor structure
    fan,system = "on","heat" #HVAC structure
    ruleCount = 2
    sensorCount = 6
    profileCount = 3
    #
    
    profileList = []
    sensorList = []
    for _ in itertools.repeat(None, profileCount):
        profileRuleList = []
        for _ in itertools.repeat(None, ruleCount):
            rule = {"setting":settings,"start_condition":start_cond,"end_condition":end_cond,"type":types,"Profile_Name":profile_name}
            profileRuleList.append(rule)
        profile = {"active":active,"profileRulesList":profileRuleList,"name":name}
        profileList.append(profile)
    for _ in itertools.repeat(None, sensorCount):
        sensor = {"active":active_s,"name":name_s,"temperature":temperature}
        sensorList.append(sensor)
    data = json.dumps({"fan":fan,"system":system,"profileList":profileList,"sensorList":sensorList}, separators=(',',':'))
    print(data)
