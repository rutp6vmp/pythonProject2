#!/usr/bin/python

# -*- coding: utf-8 -*-


import serial

# import modbus_tk

import modbus_tk.defines as cst

import modbus_tk.modbus_rtu as modbus_rtu

import modbus_tk.modbus_tcp as modbus_tcp

from struct import *

import json

import requests

import time

import sqlite3

import sys


import requests

def save_sensor_data(url, data):
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print('Data saved successfully!')
    else:
        print('Error:', response.status_code, response.text)


def poll_th(mb_id=1, port='/dev/ttyUSB0', timeout=1000, br=9600, databit=8, parity='N', stopbit=1):
    print('-%d- poll_adtek_sun' % (mb_id))

    data = {'time': time.strftime("%Y-%m-%d %H:%M:%S"), 'T': 0, 'H': 0}

    mb_port = serial.Serial(port=port, baudrate=br, bytesize=databit, parity=parity, stopbits=stopbit)

    master = modbus_rtu.RtuMaster(mb_port)

    master.set_timeout(timeout / 1000.0)

    try:

        addr = 1

        rr = master.execute(mb_id, cst.ANALOG_INPUTS, addr, 2)

        print('rr: ', rr)

        data['T'] = rr[0] / 10.0

        data['H'] = rr[1] / 10.0

        url = 'https://iotadmin.onrender.com/save-sensor-data/'

        data = {
            "time": "string",
            "T": 81,
            "H": 99
        }

        save_sensor_data(url, data)

    except Exception as e:

        print("poll Error: " + str(e))

    master._do_close()

    return data


def main():
    data = poll_th()
    print(data)


if __name__ == '__main__':
    main()
