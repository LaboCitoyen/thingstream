#!/usr/bin/python

"""
Allows linking an Open Energy Monitor RasPi shield to thingstream.
"""

import serial
import ts_client

ser = serial.Serial('/dev/ttyAMA0', 9600)

tsd_pow = ts_client.ThingStream(USERNAME, API_KEY, STREAM_ID)

while True:
    line = ser.readline()
    sline = line.strip().split()
    tx_struct = []
    print sline
    for idx in range(1, len(sline), 2):
        el_val = (int(sline[idx+1]) << 8) + int(sline[idx])
        tx_struct.append(el_val)

    real_power = tx_struct[0]
    rms_voltage = tx_struct[-1]
    print real_power, rms_voltage
    tsd_pow.push_data(real_power)


