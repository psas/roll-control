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
import scipy.integrate as integrate #for integration
import PIDcontroller as controller #PID controller
import random #for random numbers
import os.path #for saving information
import math #for doing math stuff

#for storing data
track_thetadotdot = []
track_thetadot = []
track_lift = []
track_alpha = []
track_target = []

index=0 #index for while loop

withPID=input('Use PID controller to control roll? (1 for Yes, 0 for no): ')
if(withPID==1):
    getMode=input('Select test mode: (1 for manual 0 for random): ') #test mode
    alpha=input('Enter initial canard angle: ') #initial canard angle
    #alpha=math.radians(alpha) #convert to radians
    #manually enter values for PID controller
    if(getMode==1):
        setPoint = input('Target roll rate: ') #set target roll rate
        setKp = input('Proportional gain for PID controller: ') #set Kp 
        setKi = input('Integral gain for PID controller: ') #set Ki
        #randomly generate values for PID controller based on given intervals
    else:
        print 'Enter the following inputs as two element arrays'
        print 'And make sure that the first element is less than the second'
        print 'Ex: [0,1]'
        getSetPointInterval=input('Set Point Interval: ')
        getKpInterval=input('Kp Interval: ')
        getKiInterval=input('Ki Interval: ')
        setPoint=random.uniform(getSetPointInterval[0],getSetPointInterval[1])
        setKp=random.uniform(getKpInterval[0],getKpInterval[1])
        setKi=random.uniform(getKiInterval[0],getKiInterval[1])
    #set up PID controller
    p=controller.PID(setKp,setKi,0)
    p.setPoint(setPoint)
else:
    alpha=input('Enter canard angle in degrees: ') #get canard angle
    #alpha=math.radians(alpha) #convert to radians

#load flight data from csv
data=np.genfromtxt('flight_data00.csv',dtype=float,delimiter=',',names="t,altitude,velocity,acc,rr,I")
t=data['t'] #time
tos=len(t) #time of simulation
altitude=data['altitude'] #altitude
v=data['velocity'] #velocity
acc=data['acc'] #acceleration
rr=data['rr'] #roll rate
I=data['I'] #Rotational moment of inertia
g=9.81 #gravitational constant
L=finforce.lift(alpha,v[index],altitude[index]) #initialize lift force of the canards
thetadotdot=0 #initial angular acceleration

#start simulation
while(index<tos):   
    track_alpha.append(alpha) #store alpha
    track_lift.append(L) #store lift force of canards
    track_thetadotdot.append(thetadotdot) #store angular acceleration
    
    #prevent integration error    
    if(index==0):
        track_thetadot.append(0) #first value should be 0 anyway
        thetadot=0
    #otherwise we integrate thetadotdot to get roll rate
    else:
        thetadot=integrate.simps(track_thetadotdot[:index],t[:index]) #roll rate update
        track_thetadot.append(thetadot) #store roll rate
        
    #if PID controller is enabled
    if(withPID==1 and acc[index]>0):
        #keep output of PID between 15 & -15 degrees
        if(p.update(thetadot)<math.radians(15) and p.update(thetadot)>math.radians(-15)):
            alpha=p.update(thetadot) #PID controller update
            #alpha=math.radians(alpha) #convert to radians
    
    L=finforce.lift(alpha,v[index],altitude[index]) #lift force update
    
    if(index+1<tos-1):
        #total angular acceleration
        thetadotdot=float((4*L*.082)/I[index]) + (rr[index+1]-rr[index]) #angular acceleration update
    else:
        thetadotdot=0
    print 'Time = {:f} seconds'.format(t[index]) #show the time
    print 'Velocity is {:f} m/s '.format(v[index]) #show the velocity
    print 'Acceleration is {:f} m/s^2'.format(acc[index]) #show the acceleration
    print 'Altitude is {:f} m'.format(altitude[index]) #show the altitude
    print 'Canard angle(s) {:f} radians'.format(alpha) #show canard angles
    print 'Lift force {:f} N'.format(L) #show the lift force
    print 'Total Angular acc {:f} rad/s^2'.format(thetadotdot) #show the angular acc
    print 'Total Angular vel {:f} rad/s'.format(thetadot) #show roll rate
    
    index=index+1 #increment index

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
#canard angle over time
plt.subplot(236)
plt.title('Alpha vs Time')
plt.xlim(-1,t[tos-1])
plt.ylabel('Alpha (radians)')
plt.xlabel('Time (s)')
plt.plot(t,track_alpha)
plt.show() #show figure

if(withPID==1):
    #allow user to keep PID controller settings
    keepit=input('Save PID controller settings? (1 for Yes, 0 for No): ')

    #user wants to keep
    if(keepit==1 and withPID==1):
        filename=raw_input('Enter filename: ') #get filename
        #check to see if file exists    
        if(os.path.isfile(filename)):
            f = open(filename,"a") #append since file exists
            f.write('setPoint={:f}, setKp={:f}, setKi={:f}\n'.format(setPoint,setKp,setKi))
            f.close()
        else:
            f = open(filename, "w") #write if file doesn't exitst
            f.write('setPoint={:f}, setKp={:f}, setKi={:f}\n'.format(setPoint,setKp,setKi))
            f.close()
        print 'Saved to',os.path.abspath(filename)
    #user doesn't want to keep
    else:
        print 'Settings not saved'
    