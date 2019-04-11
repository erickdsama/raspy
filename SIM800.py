#SIM800Modem.py

import RPi.GPIO as GPIO
import time

VERBOSE = True
P_POWER = 7 # Power pin
P_RESET = 12 # Reset pin

def debug(text):
    if VERBOSE:
        print "Debug:---", text

def resetModem():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(P_RESET, GPIO.OUT)
    GPIO.output(P_RESET, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(P_RESET, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(P_RESET, GPIO.LOW)
    time.sleep(3)

def togglePower():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(P_POWER, GPIO.OUT)
    GPIO.output(P_POWER, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(P_POWER, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(P_POWER, GPIO.LOW)

def isReady(ser):
    # Resetting to defaults
    cmd = 'AT\r'
    debug("Cmd: " + cmd)
    print ser.write(cmd)
    time.sleep(2)
    reply = ser.read(ser.inWaiting())
    time.sleep(8) # Wait until connected to net
    return ("OK" in reply)




def getGPS(ser):
    print "GPS"
    print ser.write('AT+CGNSPWR=1\n')
    time.sleep(5)
    print ser.readline()
    data = ""

    ser.flushInput()
    ser.flushOutput()
    out=''
    prev='101001011'
    ser.write('AT+CGNSINF\n')
    print "Aqi", ser.readline()
    while True:
        out += str(ser.read(1))
        if "\n" in out:
            print out
            return out
        prev = out

    #if ser.inWaiting:
   #     data += ser.read(ser.inWaiting())
   #     time.sleep(1)
   # print "dataaaa", data

def connectGSM(ser, apn):
    # Login to APN, no userid/password needed
    cmd = 'AT+CSTT="' + apn + '"\r'
    debug("Cmd: " + cmd)
    ser.write(cmd)
    time.sleep(3)

    reply = ser.read(ser.inWaiting())
    print reply
    # Bringing up network
    cmd = "AT+CIICR\r"
    debug("Cmd: " + cmd)
    ser.write(cmd)
    time.sleep(5)

    # Getting IP address
    cmd = "AT+CIFSR\r"
    debug("Cmd: " + cmd)
    ser.write(cmd)
    time.sleep(3)

    # Returning all messages from modem
    reply = ser.read(ser.inWaiting())
    debug("connectGSM() retured:\n" + reply)
    return reply

def connectTCP(ser, host, port):
    cmd = 'AT+CIPSTART="TCP","' + host + '","' + str(port) + '"\r'
    ser.write(cmd)
    time.sleep(1)
    response = ""
    while ser.inWaiting() > 0:
        response += ser.read(ser.inWaiting())
        time.sleep(1)
        print "response", ser.inWaiting()
    debug("connctTCP() retured:\n" + response)
    return response

def sendHTTPRequest(ser, host, request, data):
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
    ser.write(data)
    time.sleep(5)
    ser.write('AT+HTTPACTION=1 \n')
    data = ""
    while ser.inWaiting() > 0:
        data += ser.read(ser.inWaiting())
        time.sleep(1)
    print data
    #request = "POST /location HTTP/1.1\r\n" \
    #"Host: " + host + "\r\n" \
    #"Content-Type: application/json\r\n" \
    #"Content-Length: 16\r\n\r\n" \
    #"{\"datos\":\"data\"}"
    #print request, len(request)
    #ser.write(request + chr(26))  # data<^Z>
    #time.sleep(2)

def closeTCP(ser, showResponse = False):
    ser.write("AT+CIPCLOSE=1\r")
    reply = ser.read(ser.inWaiting())
    debug("closeTCP() retured:\n" + reply)
    if showResponse:
        print "Server reponse:\n" + reply[(reply.index("SEND OK") + 9):]
    time.sleep(2)

def getIPStatus(ser):
    cmd = "AT+CIPSTATUS\n"
    ser.write(cmd)
    time.sleep(1)
    reply = ser.read(ser.inWaiting())
    return reply
