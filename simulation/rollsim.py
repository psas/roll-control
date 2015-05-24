#!/usr/bin/env python
import lv2
import numpy
from scipy.signal import resample
import matplotlib.pyplot as plt
import random
from PIDcontroller import PIDController


# define things
or_sample_rate = 820.0      # Hz
adis_sample_rate = 819.2    # Hz

# Read in from open rocket
columns = numpy.loadtxt('./openrocket/launch-12.csv', delimiter=',', unpack=True)

time     = columns[0]
altitude = columns[1]*1000  # km to meters
velocity = columns[4]

# only care about launch to apogee
begin = 500
apogee = 25000
time = time[begin:apogee]
altitude = altitude[begin:apogee]
velocity = velocity[begin:apogee]

# Set up PID
pid = PIDController(p=10.0, i=0.01, d=0.1)
pid.setTarget(0.0)

# simulate roll
angular_accel = []
roll = [0]
angle = [0]
alpha = []
pids =[]
for i, t in enumerate(time):

    # current time step:
    x = altitude[i]
    v = velocity[i]
    r = roll[-1]
    correction = pid.step(r)
    a = lv2.estimate_alpha(correction, x, v, t)
    a = lv2.servo(a, t)
    aa = lv2.angular_accel(a, x, v, t)

    # step response:
    #if t > 7 and t < 7.1:
    #   aa += 100

    # random acceleration:
    aa_offset = 80                          # ang acc offset in degs/s^2
    aa_rand = random.gauss(aa_offset, 20)   # random ang acc on the rocket
    aa += aa_rand                           # add random torque to rocket

    # next time step:
    r += aa/or_sample_rate
    roll.append(r)
    ang = angle[-1] + r/or_sample_rate
    angle.append(ang)
    alpha.append(a)
    angular_accel.append(aa)
    pids.append(correction)

# chart
fig, (ax0, ax1, ax2, ax3) = plt.subplots(nrows=4, sharex=True)
ax0.plot(time, roll[1:], 'r-')
ax0.set_title('Roll Rate')
ax0.set_ylabel(r'Roll Rate [${}^0/s$]')
ax0.set_ylim([-400,400])

ax1.plot(time, angular_accel, 'r-')
ax1.set_title('Roll Accel')
ax1.set_ylabel(r'$\omega$ [${}^0/s/s$]')
ax1.set_ylim([-1000,1000])

ax2.plot(time, pids)
ax2.set_title('Correction')
ax2.set_ylabel(r'Correction')

ax3.plot(time, alpha)
ax3.set_title('Alpha')
ax3.set_ylabel(r'Alpha [${}^0$]')
ax3.set_xlabel(r'Time [$s$]')

plt.savefig('out.png', dpi=200)
plt.show()
