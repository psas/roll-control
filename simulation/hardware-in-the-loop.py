#!/usr/bin/env python
from psas_packet import io, messages
import socket
import errno
import lv2
from contextlib import closing
import time
import numpy
import Queue

ADIS = messages.MESSAGES['ADIS']

q = Queue.Queue()

servolisten = lv2.Servo(q)

# Read in from open rocket
columns = numpy.loadtxt('./openrocket/launch-12.csv', delimiter=',', unpack=True)
or_sample_rate = 820.0
ortime   = columns[0]
altitude = columns[1]*1000  # km to meters
accel    = columns[3]
velocity = columns[4]

def arm():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
        sock.bind(('', 35666))
        sock.connect(('127.0.0.1', 36000))
        sock.settimeout(0.01)
        try:
            sock.send("DI_SLOCK")
            sock.send("#YOLO")
        except socket.error as e:
            if e.errno == errno.ECONNREFUSED:
                print('connection refused, continuing')
            else:
                raise


def sim():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
        sock.bind(('', 35020))
        sock.connect(('127.0.0.1', 36000))
        sock.settimeout(0.01)
        net = io.Network(sock)

        finangle = 0
        roll = [0]
        for i, t in enumerate(ortime):
            if not q.empty():
                # finangle = lv2.servo(q.get(), t)
                finangle = q.get()
                print t, finangle, r

            x = altitude[i]
            v = velocity[i]
            r = roll[-1]
            aa = lv2.angular_accel(finangle, x, v, t)


            if t > 2.5 and t < 2.7:
                aa = 100


            r += aa/or_sample_rate
            roll.append(r)

            if r > 399:
                r = 399
            if r < -399:
                r = -399

            # Data to pack
            data = {
                'VCC': 5.0,
                'Gyro_X': r/360.0,
                'Gyro_Y': 0,
                'Gyro_Z': 1,
                'Acc_X': accel[i],
                'Acc_Y': 0,
                'Acc_Z': 0,
                'Magn_X': 53e-6,
                'Magn_Y': 0,
                'Magn_Z': 0,
                'Temp': 20,
                'Aux_ADC': 0,
            }

            net.send_data(ADIS, i, data)

            if i == 5:
                arm()

            time.sleep(0.001)

try:
    servolisten.start()
    sim()
except KeyboardInterrupt, SystemExit:
    servolisten.stop()
