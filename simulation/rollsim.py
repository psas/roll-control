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
pid = PIDController(p=50, i=0.009, d=0)
pid.setTarget(0.0)

# simulate roll
angular_accel = []
roll = [0]
angle = [0]
alpha = []
pids =[]
rand_stuff = []

for i, t in enumerate(time):

    # current time step:
    x = altitude[i]
    v = velocity[i]
    r = roll[-1]

    #correction = pid.step(angle[-1])
    correction = pid.step(r)
    a = lv2.estimate_alpha(correction, x, v, t)
    a = lv2.servo(a, t)
    aa = lv2.angular_accel(a, x, v, t)

    # step response:
    #if t > 7 and t < 7.1:
    #   aa += 100

    # random acceleration:
    #aa_offset = 80                          # ang acc offset in degs/s^2
    aa_offset = v/2.0
    aa_rand = random.gauss(aa_offset, 20)   # random ang acc on the rocket
    rand_stuff.append(aa_rand)
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
fig, (ax0, ax1, ax2, ax3, ax4) = plt.subplots(nrows=5, sharex=True, figsize=(16,9))
ax0.plot(time, angle[1:], 'g-')
ax0.set_title('Rocket Angle')
ax0.set_ylabel(r'Angle [${}^0$]')

ax1.plot(time, roll[1:], 'r-')
ax1.set_title('Roll Rate')
ax1.set_ylabel(r'Roll Rate [${}^0/s$]')
ax1.set_ylim([-5,10])

ax2.plot(time, angular_accel, 'r-')
ax2.set_title('Roll Accel')
ax2.set_ylabel(r'$\omega$ [${}^0/s/s$]')
ax2.set_ylim([-100,100])

ax3.plot(time, pids)
ax3.set_title('Correction')
ax3.set_ylabel(r'Correction')

ax4.plot(time, alpha)
ax4.set_title('Alpha')
ax4.set_ylabel(r'Alpha [${}^0$]')
ax4.set_xlabel(r'Time [$s$]')

plt.savefig('out.png', dpi=200)
plt.show()
