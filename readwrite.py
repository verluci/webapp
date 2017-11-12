import serial as s
import MySQLdb as dbs
import time
import struct
import json
import serial.tools.list_ports

class ReadWrite:
    def __init__(self):
        self.ser = s.Serial('COM5', baudrate=19200) #verbind met de arduino op port 5, zet de baudrate naar 19200
        with open("settings.json", "r") as jsonFile: #opent json en leest settings er uit
            self.settings = json.load(jsonFile)

    def run(self):
        while True:
            with open("settings.json", "r") as jsonFile:
                tempSettings = json.load(jsonFile)
            if(self.ser.inWaiting() >= 1):
                self.read()
                print(self.ser.inWaiting(), " wachtende")
            if(self.settings!=tempSettings):
                self.settings = tempSettings
                self.write()
            time.sleep(2)
        
    def write(self):
        self.x = 0
        if(self.settings["settings"]["manual"] == True):
            self.y = self.settings["settings"]["pos"]
            self.y = self.y+100
            self.x = 1
        temp = self.settings["settings"]["temp"]+30
        s = struct.Struct('B')
        packed_data = s.pack(temp)
        self.ser.write(packed_data)
        s = struct.Struct('B')
        packed_data = s.pack(self.settings["settings"]["licht"])
        self.ser.write(packed_data)
        s = struct.Struct('B')
        packed_data = s.pack(self.y)
        self.ser.write(packed_data)
        if(self.x == 1):
            self.y = self.y-100
        print("ran")
    
    def read(self):
        self.readOut = self.ser.read(3)
        latestL = struct.unpack('B', self.readOut[0:1])[0] #leest de lichtintensiteit uit
        latestT = struct.unpack('B', self.readOut[2:3])[0] #leest de temperatuur uit
        latestP = struct.unpack('b', self.readOut[1:2])[0] #leest de positie van het scherm uit
        db = dbs.connect(host="localhost", user="root", db="project21")
        c = db.cursor()
        print(latestP)
        c.execute("""INSERT INTO data (temperatuur, licht, positie) VALUES (%s, %s, %s)""",
                  (latestT, latestL, latestP))
        db.commit()
        db.close()
