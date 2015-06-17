# -*- coding: utf-8 -*-
"""
    Created on Tue Jun 16 20:29:53 2015

    @author: Will Harrington
    @organization: Portland State Aerospace Society
    
    Messing around with more state space stuff
    Generally just trying to examine how the 
    state space equations work
"""
from PIDcontroller import PIDController
import matplotlib.pyplot as plt
import numpy


Izz = 0.08594  # moment of inertia about the z-axis
Kd = .002      # damping coefficient
lf = .085      # distance from canard to z-axis

# ok now we set up some sampling stuff
duration = 1  # duration of signal
sample_rate = 820  # sampling rate
nSamples = duration * sample_rate  # number of samples

# make a linear space
k = numpy.linspace(1, nSamples, nSamples)

# create time vector
t = k-.5/sample_rate

# state space representation x'(t)=Ax+Bu, y(t)=Cx+D
A = numpy.matrix([[0, 1], [0, -Kd/Izz]])
B = numpy.matrix([[0], [1/Izz]])
C = numpy.matrix([1,0])
D = 0

# set up PID to control the angle
pid = PIDController(p=1, i=.01, d=.1)
pid.setTarget(0.0)

# set up PID to control the roll
pid2 = PIDController(p=1, i=.02, d=.1)
pid2.setTarget(0.0)

# some arrays to store the state equation and output equation
x_dot = []  # state equation
y = []  # output equation

# some random initial state
initial_state = numpy.random.randn(2,1)

# initialize
state = initial_state
u = 0

# iterate through the duration (1 second in this case)
for i in t:
    x_dot.append(A*state + B*u)  # state equation update
    y.append(C*state)  # output equation update
    
    # lets make some random spikes and see what happens    
    if i > 200 and i < 205:
        state += numpy.random.randn(2,1)
    if i > 400 and i < 405:
        state += numpy.random.randn(2,1)

    # correction for roll angle
    theta_correction = pid.step(y[-1].item(0))
    
    # correction for roll rate
    thetadot_correction = pid2.step(x_dot[-1].item(0))
    
    # update the state vector by 
    # stepping the pids to correct it to what we want
    state += numpy.matrix([[theta_correction], [thetadot_correction]])

# arrays to store stuff
angles = []
angles_dot = []
angles_dotdot = []

# iterate through x_dot and y
# pull out the angles, angular velocities, and angular accelerations
for j in y:
    angles.append(j.item(0))
for l in x_dot:
    angles_dot.append(l.item(0))
for m in x_dot:
    angles_dotdot.append(m.item(1))

# now plot it all
fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, sharex=True, figsize=(16,9))
ax0.plot(t/sample_rate, angles)
ax0.set_ylabel('Angle [$rad$]')
ax0.set_xlabel('Time [$s$]')
ax1.plot(t/sample_rate, angles_dot)
ax1.set_ylabel('Angular velocity [$rad/s$]')
ax1.set_xlabel('Time [$s$]')
ax2.plot(t/sample_rate, angles_dotdot)
ax2.set_ylabel('Angular Acceleration [$rad/s^2$]')
ax2.set_xlabel('Time [$s$]')