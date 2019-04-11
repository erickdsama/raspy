# SIMClient.py

import serial
import time, sys
from SIM800 import *
from service import Loc
import RPi.GPIO as GPIO

APN = "CMNET"
#HOST = "5.149.19.125"
HOST = "location-rwas-api.herokuapp.com"
PORT = "80"
#SERIAL_PORT = "/dev/ttyS"  # Raspberry Pi 2
SERIAL_PORT = "/dev/ttyS0"    # Raspberry Pi 3
P_BUTTON = 7 # adapt to your wiring

#def setup():
#    GPIO.setmode(GPIO.BOARD)
#    GPIO.setup(P_BUTTON, GPIO.IN, GPIO.PUD_UP)
#
#setup()
#print "Resetting modem..."
#resetModem()
from SerialX import SerialX

MAX_TRYES = 5
def read_location(ser, tryes=0):
    gps_data = getGPS(ser)
    gps_data = gps_data.replace("+CGNSINF:", "").strip()
    data = {}
    fields = gps_data.split(",")
    if len(fields) >=6:
        for key, value in  Loc.__dict__.iteritems():
            if "__" not in key:
                try:
                    data[key] = fields[value]
                except IndexError:
                    data[key] =  None

    if data.get("latitude", "").strip() != "" and  data.get("longitude", "").strip() != "":
        new_data = {"lng": data.get("longitude"), "lat": data.get("latitude"), "id_code": "Ax34b9"}
        return new_data
    if tryes < MAX_TRYES:
        return read_location(ser, tryes+1)
    return None

while True:
    try:
        ser = SerialX(SERIAL_PORT, baudrate=115200, timeout=5)
        connectGSM(ser, APN)
        reply = connectTCP(ser, HOST, PORT)
        new_data = {}
        data = read_location(ser)
        if not data:
            raise Exception("Coordenadas incompletas")

        sendHTTPRequest(ser, HOST, "/location", new_data)
        ser.close()
        time.sleep(30)
    except Exception as e:
        print e
        ser.close()
        time.sleep(5)
        continue 
 #   closeTCP(ser)
#
 #   print "closing "
  #  import datetime 
   # t = datetime.datetime.now()
    #startTime = time.time()
    #isRunning = True
    #while time.time() - startTime < 60:
    #    time.sleep(0.1)

    #ser.write("AT+CIPSEND=" + str(k) +"\r") # fixed length sending
    #time.sleep(4) # wait for prompt
    #ser.write(k)
    #time.sleep(4)
