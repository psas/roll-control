#!/usr/bin/env python
import lv2
import numpy
from scipy.signal import resample
import matplotlib.pyplot as plt

# define things
or_sample_rate = 100        # Hz
adis_sample_rate = 819.2    # Hz

# Read in from open rocket
columns = numpy.loadtxt('./openrocket/launch-12.csv', delimiter=',', unpack=True)

time        = columns[0]
altitude    = columns[1]*1000
velocity    = columns[4]

# resample data to ADIS timebase
nsamples = (len(time) * adis_sample_rate)/or_sample_rate
#print nsamples
#time     = resample(time, nsamples)
#altitude = resample(altitude, nsamples)
#velocity = resample(velocity, nsamples)


angular_accel = []
roll = [0]
angle = [0]
for i, t in enumerate(time):
    a = 0
    if t > 5 and t < 8:
        a = 1
    elif t > 12 and t < 15:
        a = -1
    else:
        a = 0
    x = altitude[i]
    v = velocity[i]
    aa = lv2.angular_accel(a, x, v, t)
    if i >= 1:
        r = roll[i-1] + aa/or_sample_rate
        roll.append(r)
        ang = angle[i-1] + r/or_sample_rate
        angle.append(ang)
    angular_accel.append(aa)

ax = plt.figure(figsize=(16,9))
plt.plot(time, angle, 'r-')
plt.xlabel('Time [s]')
plt.ylabel('Angle [o]')
ax.axes[0].set_xlim([0,30])
plt.title("Roll Angle")
#plt.legend()
plt.show()
