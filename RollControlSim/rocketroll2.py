# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 09:25:44 2015
Another attempt at simulating rocket roll without SimPy

TODO: 
    1) Need to add event latency in. (i.e. we need to simulate the delay between the flight computer and when the actual correction is applied to the rocket)
    2) Need to translate thetadot_correction into canard angle
@author: William Harrington (github.com/wrh2)
"""
import numpy as np #for getting data from csv
import finforce #for calculations for coefficient of lift & lift
import matplotlib #for plotting stuff
import matplotlib.pylab as plt
import scipy.integrate as integrate #for integration
import PIDcontroller as controller #PID controller
import os.path #for saving information
import math #for doing math stuff
#import random

#for storing data
track_thetadotdot = []
track_thetadot = []
track_lift = []
track_alpha = []
track_unknown = []
track_theta = []
ctrl_sig2 = []
ctrl_sig3 = []
angular_freq = []

index=0 #index for while loop

withPID=input('Use PID controller to control roll & theta? (1 for Yes, 0 for no): ')
if(withPID==1):
    alpha=input('Enter initial canard angle (deg): ') #initial canard angle
    delay=input('Enter delay: ') #set value for delay
    angle=[] #array for canard angle values
    for i in range(delay):
        angle.append(alpha) #initialize array with value for initial canard angle
    p_rr=controller.setupRollRatePID() #Set up roll rate PID
    p_theta=controller.setupThetaPID() #Set up Theta PID
else:
    alpha=input('Enter initial canard angle (deg): ') #get canard angle


#load flight data from csv
data=np.genfromtxt('flight_data00.csv',dtype=float,delimiter=',',names="t,altitude,velocity,acc,rr,I")
t=data['t'] #time
tos=len(t) #time of simulation
altitude=data['altitude'] #altitude
v=data['velocity'] #velocity
acc=data['acc'] #acceleration
I=data['I'] #Rotational moment of inertia
L=finforce.lift(alpha,v[index],altitude[index]) #initialize lift force of the canards
theta=0
thetadot=0
thetadotdot=0 #initial angular acceleration
unknown = 0 #unknown

#control signals
thetadot_correction=0
theta_correction=0

#start simulation
while(index<tos):
    track_lift.append(L) #store lift force of canards
    track_theta.append(theta) #store angular position
    track_thetadot.append(thetadot) #store angular velocity
    track_thetadotdot.append(thetadotdot) #store angular acceleration
    track_unknown.append(unknown) #store unknown
    ctrl_sig2.append(thetadot_correction) #store control signal(s)
    ctrl_sig3.append(theta_correction)
    angular_freq.append(thetadot/.082) #store angular frequency (not sure why I have this in here)
            
    #if PID controller is enabled
    if(withPID==1):
        track_alpha.append(angle[index]) #store canard angle
        #PID controller updates
        theta_correction=p_theta.step(theta) #correction for angular position
        p_rr.setTarget=theta_correction #change set target for thetadot PID
        thetadot_correction=p_rr.step(thetadot) #correction for angular velocity
        alpha=finforce.estimate_alpha(altitude[index], v[index], thetadot_correction, t[index]) #translate correction to fin angle
        angle.append(alpha) #add alpha to angle array
        L=finforce.lift(angle[index],v[index],altitude[index]) #lift force update
    else:
        track_alpha.append(alpha) #store canard angle
        L=finforce.lift(alpha,v[index],altitude[index]) #lift force update
    
    #sqaure waves
    if(index>87 and index<127):
       alpha = 1
       unknown = -1
    elif(index>127 and index<167):
        alpha = -1
        unknown = 1
    else:
        alpha = 0
        unknown = 0
    
    #unknown = t[index]*math.sin(t[index]*math.pi/10) #insert some angular acceleration

    
    #prevent integration error    
    if(index>0):
        thetadotdot=float((4*L*.082)/finforce.getMOI(t[index])) + unknown #total angular acceleration update
        thetadot=integrate.simps(track_thetadotdot[:index],t[:index]) #angular velocity update
        theta=integrate.simps(track_thetadot[:index],t[:index]) #angular position update
    
    print 'Time = {:f} seconds'.format(t[index]) #show the time
    print 'Velocity is {:f} m/s '.format(v[index]) #show the velocity
    print 'Acceleration is {:f} m/s^2'.format(acc[index]) #show the acceleration
    print 'Altitude is {:f} m'.format(altitude[index]) #show the altitude
    print 'Canard angle(s) {:f} degrees'.format(alpha) #show canard angles
    print 'Lift force {:f} N'.format(L) #show the lift force
    print 'Total Angular acc {:f} rad/s^2'.format(thetadotdot) #show the angular acc
    print 'Total Angular vel {:f} rad/s'.format(thetadot) #show roll rate
    
    index=index+1 #increment index

#plot the results
matplotlib.rcParams.update({'figure.autolayout':True})
plt.figure(1)
#ang acc vs time
plt.subplot(441)
plt.title('Angular Acceleration vs. Time')
plt.ylabel('Angular Acceleration (rad/s^2)')
plt.xlabel('Time (s)')
plt.plot(t,track_thetadotdot)
#altitude vs time
plt.subplot(442)
plt.title('Altitude vs. Time')
plt.ylabel('Altitude (m)')
plt.xlabel('Time (s)')
plt.plot(t,altitude)
#velocity vs time
plt.subplot(443)
plt.title('Velocity vs. Time')
plt.ylabel('Velocity (m/s)')
plt.xlabel('Time (s)')
plt.plot(t,v)
#canard lift vs time
plt.subplot(444)
plt.title('Canard Lift vs Time')
plt.ylabel('Lift force (N)')
plt.xlabel('Time (s)')
plt.plot(t,track_lift)
#roll rate vs time
plt.subplot(445)
plt.title('Roll rate vs Time')
plt.ylabel('Roll rate (rad/s)')
plt.xlabel('Time (s)')
plt.plot(t,track_thetadot)
#canard angle over time
plt.subplot(446)
plt.title('Alpha vs Time')
plt.xlim(-1,t[tos-1])
plt.ylabel('Alpha (degrees)')
plt.xlabel('Time (s)')
plt.plot(t,track_alpha)
#unknown vs. time
plt.subplot(447)
plt.title('Unknown vs Time')
plt.xlim(-1,t[tos-1])
plt.ylabel('Unknown')
plt.xlabel('Time (s)')
plt.plot(t,track_unknown)
#angular position vs time
plt.subplot(448)
plt.title('Theta vs Time')
plt.xlim(-1,t[tos-1])
plt.ylabel('Theta (radians)')
plt.xlabel('Time (s)')
plt.plot(t,track_theta)
#angular velocity correction vs time
plt.subplot(449)
plt.title('Thetadot correction vs Time')
plt.ylabel('Thetadot (rad/s)')
plt.xlabel('Time (s)')
plt.plot(t,ctrl_sig2)
#angular position correction vs time
plt.subplot(4,4,10)
plt.title('Theta correction vs Time')
plt.ylabel('Theta (radians)')
plt.xlabel('Time (s)')
plt.plot(t,ctrl_sig3)
#angular frequency vs time
plt.subplot(4,4,11)
plt.title('Angular freq vs Time')
plt.ylabel('Theta (radians)')
plt.xlabel('Time (s)')
plt.plot(t,angular_freq)
plt.show() #show figure


#option to saveSettings()
def saveSettings():
    #allow user to keep PID controller settings
    keepit=input('Save PID controller settings? (1 for Yes, 0 for No): ')

    #user wants to keep
    if(keepit==1):
        filename=raw_input('Enter filename: ') #get filename
        #check to see if file exists    
        if(os.path.isfile(filename)):
            f = open(filename,"a") #append since file exists
            f.write('Roll Rate PID setting:\n')
            f.write('Target={:f}, setKp={:f}, setKi={:f}, setKd={:f}\n'.format(p_rr.setPoint,p_rr.setKp,p_rr.setKi,p_rr.setKd))
            f.write('Theta PID setting:\n')
            f.write('Target={:f}, setKp={:f}, setKi={:f}, setKd={:f}\n'.format(p_theta.setPoint,p_theta.setKp,p_theta.setKi,p_theta.setKd))
            f.close()
        else:
            f = open(filename, "w") #write if file doesn't exitst
            f.write('Roll Rate PID setting:\n')
            f.write('Target={:f}, setKp={:f}, setKi={:f}, setKd={:f}\n'.format(p_rr.setPoint,p_rr.setKp,p_rr.setKi,p_rr.setKd))
            f.write('Theta PID setting:\n')
            f.write('Target={:f}, setKp={:f}, setKi={:f}, setKd={:f}\n'.format(p_theta.setPoint,p_theta.setKp,p_theta.setKi,p_theta.setKd))
            f.close()
        print 'Saved to',os.path.abspath(filename)
    #user doesn't want to keep
    else:
        print 'Settings not saved'