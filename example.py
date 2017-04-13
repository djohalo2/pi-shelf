#!/usr/bin/env python

import signal
import time
import sys
import requests
import RPi.GPIO as GPIO

from pirc522 import RFID
from uuid import getnode as get_mac

trackingPin = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(trackingPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

run = True
rdr = RFID()
util = rdr.util()
util.debug = True

def authenticate_shelf():
    r = requests.post("https://ipmedt5.roddeltrein.nl/api/authenticate",
                      data = {'email':'s1095067@student.hsleiden.nl', 'password': 'secret'})
    r.headers['content-type']
    response = r.json()
    token = response['token']
    return token


def end_read(signal,frame):
    global run
    print("\nCtrl+C captured, ending read.")
    run = False
    rdr.cleanup()
    sys.exit()

signal.signal(signal.SIGINT, end_read)

def main():
    mac = get_mac()
    finalMac = "".join(c + ":" if i % 2 else c for i, c in enumerate(hex(mac)[2:].zfill(12)))[:-1]
    print(finalMac)

    token = authenticate_shelf()
    print(token)
    print("test")

    print("Starting")
    while run:
        print(GPIO.input(trackingPin))
        rdr.wait_for_tag()

        (error, data) = rdr.request()
        if not error:
            print("\nDetected: " + format(data, "02x"))

        (error, uid) = rdr.anticoll()
        if not error:
            print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))

            tagId = str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
            print(tagId)

            time.sleep(1)

if __name__ == "__main__":
    main()
