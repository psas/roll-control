# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 09:25:44 2015
Another attempt at simulating rocket roll without SimPy
@author: William Harrington (github.com/wrh2)
"""
import finforce
import matplotlib #for plotting stuff
import matplotlib.pylab as plt
import math #for our friend pi
#for storing data
track_altitude = []
track_velocity = []
track_time = []
track_thetadotdot = []
track_lift = []

#gather user defined parameters for simulation
tos=input('Time of simulation: ') #time of simulation
dt=input('Time step: ') #time step
acc=input('Acceleration: ') #acceleration of rocket
alpha=input('Canard(s) angle: ') #angle of attack for canards
alpha = math.radians(alpha) #convert to radians
t=0 #start time at 0
vPrev=0 #start velocity at 0
v=vPrev 
g=9.81 #gravitational constant
Cl = finforce.C_L(acc,v) #coefficient of lift
initial_altitude = 0 #probably not right at sea level but we can fix this later
prev_altitude = initial_altitude #keep track of previous altitude
altitude=prev_altitude
thetadotdot=0
      
#lift force of the canards
L=finforce.lift(acc,v,altitude)

#do the following while time is less than the time of simulation
while(t<tos):
    track_time.append(round(t,3)) #store time
    track_velocity.append(round(v,3)) #store velocity
    track_altitude.append(round(altitude,3)) #store altitude
    track_lift.append(round(L,3)) #store canard lift force
    track_thetadotdot.append(round(thetadotdot,3)) #store thetadotdot
    
    t=t+dt #time update
    vPrev=v #keep track of previous velocity
    prev_altitude=altitude #keep track of previous altitude
    v=vPrev+acc*dt #velocity update
    altitude=prev_altitude+v*dt #altitude update
    Cl = finforce.C_L(acc,v) #coefficient of lift update
    L=finforce.lift(acc,v,altitude) #lift force update
    thetadotdot=float(4*L*.082)/float(.08594) #angular acceleration update
    print 'Time = {:3.2f} seconds'.format(t) #show the time
    print 'Velocity is {:3.2f} m/s '.format(v) #show the velocity
    print 'Altitude is {:3.2f} m'.format(altitude) #show the altitude
    print 'Lift force {:3.2f} N'.format(L) #show the lift force
    print 'Angular acc {:3.2f} rad/s^2'.format(thetadotdot) #show the angular acc
    
#plot the results
matplotlib.rcParams.update({'figure.autolayout':True})
plt.figure(1)
#ang acc vs time
plt.subplot(221)
plt.title('Angular Acceleration vs. Time')
plt.ylabel('Angular Acceleration (rad/s^2)')
plt.xlabel('Time (s)')
plt.plot(track_time,track_thetadotdot)
#altitude vs time
plt.subplot(222)
plt.title('Altitude vs. Time')
plt.ylabel('Altitude (m)')
plt.xlabel('Time (s)')
plt.plot(track_time,track_altitude)
#velocity vs time
plt.subplot(223)
plt.title('Velocity vs. Time')
plt.ylabel('Velocity (m/s)')
plt.xlabel('Time (s)')
plt.plot(track_time,track_velocity)
#canard lift vs time
plt.subplot(224)
plt.title('Canard Lift vs Time')
plt.ylabel('Lift force (N)')
plt.xlabel('Time (s)')
plt.plot(track_time,track_lift)
plt.show() #show figure