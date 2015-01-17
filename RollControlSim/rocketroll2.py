# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 09:25:44 2015
Another attempt at simulating rocket roll without SimPy
@author: William Harrington (github.com/wrh2)
"""
import numpy as np #for getting data from csv
import finforce #for calculations for coefficient of lift & lift
import matplotlib #for plotting stuff
import matplotlib.pylab as plt
import math #for our friend pi
import scipy.integrate as integrate

#for storing data
track_thetadotdot = []
track_thetadot = []
track_lift = []

index=0 #index for while loop

#load flight data from csv
data=np.genfromtxt('flight_data.csv',dtype=float,delimiter=',',names="t,altitude,velocity,acc")
t=data['t'] #time
tos=len(t) #time of simulation
altitude=data['altitude'] #altitude
v=data['velocity'] #velocity
acc=data['acc'] #acceleration
alpha=1 #angle of canards
alpha = math.radians(alpha) #convert to radians
g=9.81 #gravitational constant
Cl = finforce.C_L(acc[index],v[index]) #initialize coefficient of lift
L=finforce.lift(acc[index],v[index],altitude[index]) #initialize lift force of the canards
thetadotdot=0 #initial angular acceleration
while(index<tos):
    track_lift.append(round(L,3)) #store lift force of canards
    track_thetadotdot.append(round(thetadotdot,3)) #store angular acceleration
    if(index==0):
        track_thetadot.append(0)
    else:
        track_thetadot.append(round(integrate.simps(track_thetadotdot[:index],t[:index]),3))
    Cl = finforce.C_L(acc[index],v[index]) #coefficient of lift update
    L=finforce.lift(acc[index],v[index],altitude[index]) #lift force update
    thetadotdot=float(4*L*.082)/float(.08594) #angular acceleration update
    print 'Time = {:3.2f} seconds'.format(t[index]) #show the time
    print 'Velocity is {:3.2f} m/s '.format(v[index]) #show the velocity
    print 'Altitude is {:3.2f} m'.format(altitude[index]) #show the altitude
    print 'Lift force {:3.2f} N'.format(L) #show the lift force
    print 'Angular acc {:3.2f} rad/s^2'.format(thetadotdot) #show the angular acc
    index=index+1

#plot the results
matplotlib.rcParams.update({'figure.autolayout':True})
plt.figure(1)
#ang acc vs time
plt.subplot(231)
plt.title('Angular Acceleration vs. Time')
plt.ylabel('Angular Acceleration (rad/s^2)')
plt.xlabel('Time (s)')
plt.plot(t,track_thetadotdot)
#altitude vs time
plt.subplot(232)
plt.title('Altitude vs. Time')
plt.ylabel('Altitude (m)')
plt.xlabel('Time (s)')
plt.plot(t,altitude)
#velocity vs time
plt.subplot(233)
plt.title('Velocity vs. Time')
plt.ylabel('Velocity (m/s)')
plt.xlabel('Time (s)')
plt.plot(t,v)
#canard lift vs time
plt.subplot(234)
plt.title('Canard Lift vs Time')
plt.ylabel('Lift force (N)')
plt.xlabel('Time (s)')
plt.plot(t,track_lift)
#roll rate vs time
plt.subplot(235)
plt.title('Roll rate vs Time')
plt.ylabel('Roll rate (rad/s)')
plt.xlabel('Time (s)')
plt.plot(t,track_thetadot)
plt.show() #show figure