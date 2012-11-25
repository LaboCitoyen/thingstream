#!/usr/bin/python3

import serial

ser = Serial.Serial('/dev/ttyAMA0', 9600)

while True:
    print ser.read()
