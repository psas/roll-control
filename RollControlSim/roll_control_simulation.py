# -*- coding: utf-8 -*-
"""
A really bad roll control simulation with SimPy
programmed by William Harrington
"""
import simpy #for simulation environment
import matplotlib
import matplotlib.pyplot as plt #for plotting stuff
import math

alpha=input('Enter canard angle (-15 < x < 15): ') #get canard angle from user
tau=input('Enter time step: ') #time step
tos=input('Enter time of simulation: ') #get time of simulation from user
#angle of attack (canard)
alpha = alpha * math.pi/180 #1 degree * pi/180 gives us radians
peakv=340 #peak velocity m/s
Molarmass=.0289644 #molar mass of dry air
R=8.31447 #ideal universal gas constant J/(mol*K)
po = 101.325#*(10**3) #sea level standard atmospheric pressure (Pa)

track_altitude = []
track_velocity = []
track_time = []
track_thetadotdot = []
track_temp = []
track_airdensity = []
track_lift = []
#define process
#in this example lets do a velocity update
def rocket_roll(env,tick,alpha):
    vo = 0 #initial velocity
    vPrev = vo #set velocity to initial velocity, used for keeping track of previous velocity
    v = vPrev #set velocity
    acc = 5.25 #150 m/s^2 acceleration
    g=9.81 #gravity
    dt = tick #time step

    #stuff for simulating the roll of the rocket
    F=4 #number of canards
    A=11.64*(10**-2) #surface area of one canard in meters
    r=82*(10**-3) #canard distance from the Z axis
    I=.08594 #moment of inertia about the Z axis
    
    S=A*alpha #Planform area of the canard
        
    #Constants for coefficient of lift
    Kp=2.45
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
    #altitude=prev_altitude+v*dt #altitude update
    #Temp=Tempo-lapserate*altitude #temp at altitude

    #air density as a function of altitude
    p=po*(1-((lapserate*altitude)/(Tempo)))**((g*Molarmass)/(R*lapserate))
        
    #lift force of the canard
    L=.5*Cl*p*(v**2)*S
        
    #This is the coefficent of lift in supersonic speeds
    #M=v/332.529 #mach number (velocity/velocity of sound)
    #Beta = math.sqrt(M**2-1) #constant for coefficient of lift
    #m = Beta * math.cot(math.pi/3) #constant for coefficient of lift
    #Cl2 = 2*math.pi*(m/Beta*1.079)
    
    #angular acceleration of the rocket
    #thetadotdot=(F*L*r)/I
    thetadotdot=0
    #env will be the simulation environment
    #tick will represent the time at which something occurs
    while True:
        vPrev=v #keep track of previous velocity
        prev_altitude=altitude #keep track of previous altitude
        track_velocity.append(v) #store velocity
        track_time.append(round(env.now,3)) #store time
        track_altitude.append(round(altitude,3)) #store altitude
        track_thetadotdot.append(round(thetadotdot,3)) #store thetadotdot
        track_temp.append(round(Temp,3)) #store temp
        track_airdensity.append(round(p,3)) #store air density
        track_lift.append(round(L,3)) #store canard lift force
        print 'Time = {:3.2f} minutes'.format(env.now) #show the time
        if(env.now == 0.01):
            print 'Rocket launch occured'
            v=vPrev+acc*dt
            M=v/332.529 #mach number update
            altitude=prev_altitude+v*dt #altitude update
            Temp=Tempo-lapserate*altitude #temp update
            p=po*((1-((lapserate*altitude)/(Tempo)))**((g*Molarmass)/(R*lapserate))) #air density update
            L=.5*Cl*p*(v**2)*S #lift force update
            thetadotdot=(F*L*r)/I #angular acceleration update
            print 'Velocity is {:3.2f} m/s'.format(v)
            print 'Mach {:3.2f}'.format(M)
            print 'Altitude is {:3.2f} m'.format(altitude)
            print 'Temp is {:3.2f} K'.format(Temp)
            print 'Air density {:3.2f} kg/m^3'.format(p)
            print 'Lift force {:3.2f} N'.format(L)
            print 'Angular acc {:3.2f} rad/s^2'.format(thetadotdot)
        elif(env.now > 0.01):
            v=vPrev+acc*dt
            M=v/332.529 #mach number update
            altitude=prev_altitude+v*dt #altitude update
            Temp=Tempo-lapserate*altitude #temp update
            p=po*((1-((lapserate*altitude)/(Tempo)))**((g*Molarmass)/(R*lapserate))) #air density update

            #velocity is over supersonic speed            
            if(v==(peakv-5)):
                Beta = math.sqrt(M**2-1) #constant for coefficient of lift
                m = Beta * math.cot(math.pi/3) #constant for coefficient of lift
                Cl = 2*math.pi*(m/Beta*1.079) #coeff of lift at supersonic speeds            
                L=.5*Cl*p*(v**2)*S #lift force update
                thetadotdot=(F*L*r)/I #angular acceleration update
            else:
                L=.5*Cl*p*(v**2)*S #lift force update
                thetadotdot=(F*L*r)/I #angular acceleration update
            print 'Velocity is {:3.2f} m/s'.format(v)
            print 'Mach {:3.2f}'.format(M)
            print 'Altitude is {:3.2f} m'.format(altitude)
            print 'Temp is {:3.2f} K'.format(Temp)
            print 'Air density {:3.2f} kg/m^3'.format(p)
            print 'Lift force {:3.2f} N'.format(L)
            print 'Angular acc {:3.2f} rad/s^2'.format(thetadotdot)
        else:
            print 'Rocket awaiting launch'
        yield env.timeout(tick) #yield the event that occurs at tick
        
#now lets run it
env = simpy.Environment() #create the simulation environment
env.process(rocket_roll(env,tau,alpha)) #add the clock process, set timestep
env.run(until=tos) #run simulation for a fixed period of time

#plot the results
matplotlib.rcParams.update({'figure.autolayout':True})
plt.figure(1)
plt.subplot(331)
plt.title('Angular Acceleration vs. Time')
plt.ylabel('Angular Acceleration (rad/s^2)')
plt.xlabel('Time (s)')
plt.plot(track_time,track_thetadotdot)
plt.subplot(332)
plt.title('Altitude vs. Time')
plt.ylabel('Altitude (m)')
plt.xlabel('Time (s)')
plt.plot(track_time,track_altitude)
plt.subplot(333)
plt.title('Velocity vs. Time')
plt.ylabel('Velocity (m/s)')
plt.xlabel('Time (s)')
plt.plot(track_time,track_velocity)
plt.subplot(334)
plt.title('Temp vs. Time')
plt.ylabel('Temp (K)')
plt.xlabel('Time (s)')
plt.plot(track_time,track_temp)
plt.subplot(335)
plt.title('Canard Lift vs Time')
plt.ylabel('Lift force (N?)')
plt.xlabel('Time (s)')
plt.plot(track_time,track_airdensity)
plt.subplot(336)
plt.title('Air density vs Altitude')
plt.ylabel('Air density (kg/m^3)')
plt.xlabel('Altitude (m)')
plt.plot(track_altitude,track_airdensity)
plt.show()