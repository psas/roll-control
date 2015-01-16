# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 09:25:44 2015
Another attempt at simulating rocket roll without SimPy
@author: William Harrington (github.com/wrh2)
"""
import matplotlib #for plotting stuff
import matplotlib.pylab as plt
import math #for our friend pi
#for storing data
track_altitude = []
track_velocity = []
track_time = []
track_thetadotdot = []
track_temp = []
track_airdensity = []
track_lift = []

#gather user defined parameters for simulation
tos=input('Time of simulation: ') #time of simulation
dt=input('Time step: ') #time step
acc=input('Acceleration: ') #acceleration of rocket
alpha=input('Canard(s) angle: ') #angle of attack for canards
alpha = alpha * (float(math.pi)/180) #1 degree * pi/180 gives us radians
t=0 #start time at 0
vPrev=0 #start velocity at 0
v=vPrev
g=9.81 #gravitational constant
M=0 #mach number

#stuff for simulating the roll of the rocket
F=4 #number of canards
A=11.64*(10**-2) #surface area of one canard in meters
r=82*(10**-3) #canard distance from the Z axis
I=.08594 #moment of inertia about the Z axis
S=A*alpha #Planform area of the canard
peakv=340 #peak velocity m/s
Molarmass=.0289644 #molar mass of dry air
R=8.31447 #ideal universal gas constant J/(mol*K)
po = 101.325#*(10**3) #sea level standard atmospheric pressure (Pa)

#Constants for coefficient of lift
Kp=2.45     #this is the kp
Kv=3.21
#This is the coefficient of lift in subsonic speeds
Cl = (Kp*(math.cos(alpha)**2)*math.sin(alpha))+(Kv*math.cos(alpha)*(math.sin(alpha)**2))

#for calculating air density as a function of altitude
lapserate=.0065 #K/m
Tempo=288.15 #Temperature at launch site in Kelvins
Temp=Tempo #for holding temp
initial_altitude = 0 #probably not right at sea level but we can fix this later
prev_altitude = initial_altitude #keep track of previous altitude
altitude=prev_altitude
thetadotdot=0
#air density as a function of altitude
p=po*(1-(float(lapserate*altitude)/float(Tempo)))**(float(g*Molarmass)/float(R*lapserate))
        
#lift force of the canard
L=.5*Cl*p*(v**2)*S

#do the following while time is less than the time of simulation
while(t<tos):
    track_velocity.append(round(v,3)) #store velocity
    track_time.append(round(t,3)) #store time
    track_altitude.append(round(altitude,3)) #store altitude
    track_thetadotdot.append(round(thetadotdot,3)) #store thetadotdot
    track_temp.append(round(Temp,3)) #store temp
    track_airdensity.append(round(p,3)) #store air density
    track_lift.append(round(L,3)) #store canard lift force
    
    t=t+dt #time update
    vPrev=v #keep track of previous velocity
    prev_altitude=altitude #keep track of previous altitude
    v=vPrev+acc*dt #velocity update
    M=v/332.529 #mach number update
    altitude=prev_altitude+v*dt #altitude update
    Temp=Tempo-lapserate*altitude #temp update
    p=po*(1-(float(lapserate*altitude)/float(Tempo)))**(float(g*Molarmass)/float(R*lapserate))
    L=.5*Cl*p*(v**2)*S #lift force update
    thetadotdot=float(F*L*r)/float(I) #angular acceleration update
    print 'Time = {:3.2f} minutes'.format(t) #show the time
    print 'Velocity is {:3.2f} m/s '.format(v) #show the velocity
    print 'Mach {:3.2f}'.format(M) #show the mach number
    print 'Altitude is {:3.2f} m'.format(altitude) #show the altitude
    print 'Temp is {:3.2f} K'.format(Temp) #show the temp
    print 'Air density {:3.2f} kg/m^3'.format(p) #show the air density
    print 'Lift force {:3.2f} N'.format(L) #show the lift force
    print 'Angular acc {:3.2f} rad/s^2'.format(thetadotdot) #show the angular acc
    
#plot the results
matplotlib.rcParams.update({'figure.autolayout':True})
plt.figure(1)
#ang acc vs time
plt.subplot(331)
plt.title('Angular Acceleration vs. Time')
plt.ylabel('Angular Acceleration (rad/s^2)')
plt.xlabel('Time (s)')
plt.plot(track_time,track_thetadotdot)
#altitude vs time
plt.subplot(332)
plt.title('Altitude vs. Time')
plt.ylabel('Altitude (m)')
plt.xlabel('Time (s)')
plt.plot(track_time,track_altitude)
#velocity vs time
plt.subplot(333)
plt.title('Velocity vs. Time')
plt.ylabel('Velocity (m/s)')
plt.xlabel('Time (s)')
plt.plot(track_time,track_velocity)
plt.subplot(334)
#temp vs time
plt.title('Temp vs. Time')
plt.ylabel('Temp (K)')
plt.xlabel('Time (s)')
plt.plot(track_time,track_temp)
#canard lift vs time
plt.subplot(335)
plt.title('Canard Lift vs Time')
plt.ylabel('Lift force (N?)')
plt.xlabel('Time (s)')
plt.plot(track_time,track_airdensity)
#air density vs altitude
plt.subplot(336)
plt.title('Air density vs Altitude')
plt.ylabel('Air density (kg/m^3)')
plt.xlabel('Altitude (m)')
plt.plot(track_altitude,track_airdensity)
plt.show() #show figure
    
