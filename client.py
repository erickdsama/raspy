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

#if not isReady(ser):
#    print "Modem not ready."
#    sys.exit(0)
    
#print "Connecting to GSM net..."

#print "Connecting to TCP server..."
#print reply
#if "CONNECT" not in reply or "OK" not in reply :
#    print "Connection failed"
#    #sys.exit(0)

#
def read_last_location(last_line):
    if last_line:
        fields = last_line.split(",")
        if len(fields) < 6:
            return None
        data = {}
        for key, value in  Loc.__dict__.iteritems():
            if "__" not in key:
                try:
                    data[key] = fields[value]
                except IndexError:
                    data[key] =  None
        return data
    return None

while True:
    try:
        ser = SerialX(SERIAL_PORT, baudrate=115200, timeout=5)
        connectGSM(ser, APN)
        reply = connectTCP(ser, HOST, PORT)
        gps_data = getGPS(ser)
        gps_data = gps_data.replace("+CGNSINF:", "").strip()
        new_data = {}
        data = read_last_location(gps_data)
        if not data:
            raise Exception("Coordenadas incompletas")

        if data.get('longitude') == "" and data.get('latitude') == "":
            raise Exception("Noo hay coordenadas")
        new_data["lng"] = data.get("longitude")
        new_data["lat"] = data.get("latitude")
        new_data["id_code"] = "Ax34b9"
        sendHTTPRequest(ser, HOST, "/location", new_data)
        #closeTCP(ser)
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
