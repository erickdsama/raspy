# SIMClient.py

import serial
import time, sys
from SIM800 import *
from service import Loc
import RPi.GPIO as GPIO

APN = "CMNET" 
HOST = "location-rwas-api.herokuapp.com" # Web service
PORT = "80" # Puerto 
SERIAL_PORT = "/dev/ttyS0"    # Raspberry Pi Zero
P_BUTTON = 7 # GPIO para encender Waveshareg

from SerialX import SerialX

MAX_TRIES = 5 # numero maximo de intentos 
def read_location(ser, tries=0):
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
    # revisar que las coordenadas sean en el formato correcto 
    if data.get("latitude", "").strip() != "" and  data.get("longitude", "").strip() != "":
        new_data = {"lng": data.get("longitude"), "lat": data.get("latitude"), "id_code": "Ax34b9"}
        return new_data
    if tries < MAX_TRIES:
        time.sleep(2)
        return read_location(ser, tries+1)
    return None


ser = None
togglePower()
time.sleep(5)

while True:
    try:
        ser = SerialX(SERIAL_PORT, baudrate=115200, timeout=5)
        connectGSM(ser, APN)  # conectar a la red GSM
        reply = connectTCP(ser, HOST, PORT)  # conectar al servidor
        new_data = read_location(ser) # intentar leer  las coordenadas
        if not new_data:
            raise Exception("Coordenadas incompletas")

        sendHTTPRequest(ser, HOST, "/location", new_data) # enviar las coordenadas al servicio web
        ser.close()
        time.sleep(300) # intervalo entre lectura de coordenadas
    except Exception as e:
        print e
        if ser:
            ser.close()
        time.sleep(5)
        continue 
