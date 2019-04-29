#SIM800Modem.py

import RPi.GPIO as GPIO
import time

VERBOSE = True
P_POWER = 7 # Power pin

def debug(text):
    if VERBOSE:
        print "Debug:---", text


print "POWER BOARD", GPIO.BOARD
print "POWER LOW", GPIO.OUT
print "POWER HIGH", GPIO.HIGH

def togglePower():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(P_POWER, GPIO.OUT)
    GPIO.output(P_POWER, GPIO.LOW)
    time.sleep(1)
    GPIO.output(P_POWER, GPIO.HIGH)
    GPIO.setup(P_POWER, GPIO.IN)  # set a port/pin as an input  
    time.sleep(3)
    

def getGPS(ser):
    print ser.write('AT+CGNSPWR=1\n')
    time.sleep(5)
    data = ""

    gps_data = ser.write('AT+CGNSINF\n')
    return gps_data


def connectGSM(ser, apn):
    # Login to APN, no userid/password needed
    cmd = 'AT+CSTT="' + apn + '"\r'
    CSTT = ser.write(cmd)
    time.sleep(3)
    # Bringing up network
    cmd = "AT+CIICR\r"
    debug("Cmd: " + cmd)
    CIICR = ser.write(cmd)
    time.sleep(5)
    # Getting IP address
    cmd = "AT+CIFSR\r"
    debug("Cmd: " + cmd)
    CIFSR = ser.write(cmd)
    time.sleep(3)
    # Returning all messages from modem
    # reply = ser.read(ser.inWaiting())
    # debug("connectGSM() retured:\n" + reply)
    return CSTT + CIICR + CIICR

def connectTCP(ser, host, port):
    cmd = 'AT+CIPSTART="TCP","' + host + '","' + str(port) + '"\r'
    response = ser.write(cmd)
    time.sleep(1)
    return response


MAX_TRIES = 5
def sendHTTPRequest(ser, host, request, data, tries=0):
    if True:
        ser.write('AT+SAPBR=3,1,"Contype","GPRS"\n')
        time.sleep(1)
        ser.write('AT+SAPBR =1,1 \n')
        time.sleep(1)
        ser.write('AT+SAPBR=2,1 \n')
        time.sleep(1)
        ser.write('AT+HTTPINIT \n')
        time.sleep(1)
        ser.write('AT+HTTPPARA="CID",1 \n')
        time.sleep(1)
        ser.write('AT+HTTPPARA="URL","http://{}{}"\n'.format(host, request))
        time.sleep(1)
        ser.write('AT+HTTPPARA="CONTENT","application/json" \n')
        time.sleep(1)
        import json
        data = json.dumps(data)
        len_data = len(data)
        print len_data, data
        ser.write('AT+HTTPDATA=300,5000 \n'.format(len_data))
        time.sleep(2)
        data = ser.write(data)
        time.sleep(5)
        data += ser.write('AT+HTTPACTION=1 \n')


def closeTCP(ser, showResponse = False):
    ser.write("AT+CIPCLOSE=1\r")
    time.sleep(2)

def getIPStatus(ser):
    cmd = "AT+CIPSTATUS\n"
    ser.write(cmd)
    time.sleep(1)
    reply = ser.read(ser.inWaiting())
    return reply
