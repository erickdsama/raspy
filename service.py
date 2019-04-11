import sys
import time
import subprocess
import threading


class Loc:
    GNSSrunstatus = 0
    Fixstatus = 1
    UTCDatetime = 2
    latitude = 3
    longitude = 4
    altitude = 5
    speedOTG = 6
    course = 7
    fixmode = 8
    Reseved1 = 9
    HDOP =10
    PDOP = 11
    VDOP = 12
    Reserved2 = 13
    GNSSatellitesinview = 14
    GNSSatellitesused = 15
    GLONASSatellitesused = 16
    Reserved3 = 17
    cn0max = 18
    HPA = 19
    VPA = 20

def service_gps():
    while True:
        subprocess.call("/home/pi/Waveshare-GPS/gps.sh  loc", shell=True)
        time.sleep(30)

def read_last_location():
    f = open('./file.txt', 'r')
    lines = f.readlines()
    if lines:
        last_line =  lines[-1:][0]
        fields = last_line.split(" ")
        if len(fields) < 20:
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
#service = threading.Thread(target=service_gps)
#service.run()

#print read_last_location()


if __name__ == "__main__":
    args = sys.argv
    if len > 1:
        func = args[1]
        if func == "service":
            service = threading.Thread(target=service_gps)
            service.start()
        elif func == "read":
            import requests
            data = read_last_location()
            new_data = {}
            new_data["lng"] = data.get("longitude")
            new_data["lat"] = data.get("latitude")
            if new_data["lng"] and new_data["lat"]:
                new_data["id_code"] = "Ax34b9"
                requests.post("http://192.168.1.20:5000/location", json=new_data)