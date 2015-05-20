#!/usr/bin/env python
import lv2
import numpy
from scipy.signal import resample
import matplotlib.pyplot as plt
import random
from PIDcontroller import PIDController


# define things
or_sample_rate = 100        # Hz
adis_sample_rate = 819.2    # Hz

# Read in from open rocket
columns = numpy.loadtxt('./openrocket/launch-12.csv', delimiter=',', unpack=True)

time     = columns[0]
altitude = columns[1]*1000  # km to meters
velocity = columns[4]

# resample data to ADIS timebase
nsamples = (len(time) * adis_sample_rate)/or_sample_rate
#time     = resample(time, nsamples)
#altitude = resample(altitude, nsamples)
#velocity = resample(velocity, nsamples)

pid = PIDController(10, 1, 0)
pid.setTarget(0.0)


angular_accel = []
roll = [0]
angle = [0]
for i, t in enumerate(time):
    correction = pid.step(roll[-1])
    print correction
    # TODO: Reverse look up for alpha (canard angle)
    a = 0                    # canard angle in degrees
    a = lv2.servo(a, t)      # request servo update canard angle
    x = altitude[i]
    v = velocity[i]
    aa = lv2.angular_accel(a, x, v, t)

    aa_offset = 50                          # ang acc offset in degs/s^2
    aa_rand = random.gauss(aa_offset, 50)   # random ang acc on the rocket

    aa += aa_rand                           # add random torque to rocket
    if i >= 1:
        r = roll[i-1] + aa/or_sample_rate
        roll.append(r)
        ang = angle[i-1] + r/or_sample_rate
        angle.append(ang)
    angular_accel.append(aa)


ax = plt.figure(figsize=(16, 9))
plt.plot(time, angle, 'r-')
plt.xlabel('Time [s]')
plt.ylabel('Angle [o]')
ax.axes[0].set_xlim([0, 30])
plt.title("Roll Angle")
plt.show()
