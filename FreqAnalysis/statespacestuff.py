# -*- coding: utf-8 -*-
"""
    Created on Thu Jun 11 21:37:49 2015

    @author: Will Harrington
    @organization: Portland State Aerospace Society

    Going to state space route now
    Trying to get some good frequency domain analysis
"""
import matplotlib.pyplot as plt
import control
import numpy
from scipy import signal

Izz = 0.08594  # moment of inertia about the z-axis
Kd = .002      # damping coefficient
lf = .085      # distance from canard to z-axis

# state space representation x'(t)=Ax+Bu, y(t)=Cx+D
A = numpy.matrix([[0, 1], [0, -Kd/Izz]])
B = numpy.matrix([[0], [lf/Izz]])
C = numpy.matrix([1,0])
D = 0

# convert it to a transfer function
# using control library
transfer_func = control.ss2tf(A, B, C, D)

# note: we can do the same thing with
# scipy but its not as pretty for output
# ex: transfer_func = signal.ss2tf(A, B, C, D) is same thing

print transfer_func

# give me a bode plot of it
# using the control library
# this yields results that differ from scipy
# why?
#mag, phase, omega = control.bode(transfer_func)


# now lets make a linear time invariant representation
# with scipy
s1 = signal.lti(A, B, C, D)

# ...and now give me some of that bode
# this will give us a look at the frequency
# response of our system
w, mag, phase = signal.bode(s1)

# display all the nice pictures
fig, (ax0, ax1) = plt.subplots(nrows=2, sharex=True, figsize=(16,9))
ax0.semilogx(w, mag)    # Bode mag plot
ax0.set_title('Bode Mag Plot')
ax0.set_ylabel(r'Magnitude [$dB$]')
ax0.set_xlabel(r'Freq [$Hz$]')
ax1.semilogx(w, phase)  # Bode phase plot
ax1.set_title('Bode Phase Plot')
ax1.set_ylabel(r'Phase [${}^0$]')
ax1.set_xlabel(r'Freq [$Hz$]')
plt.savefig('bode.png', dpi=200)
plt.show()


