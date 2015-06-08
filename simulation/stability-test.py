"""
    Prototype code for doing monte carlo testing
    on the stability of our nested PID loop
    
    Programmed by William Harrington
    Portland State Aerospace Society
"""

from __future__ import division  # import newer division rules
from nestedSim import simulate as sim  # get the nested pid loop simulation
from PIDcontroller import PIDController  # get the PID controller stuff in here
import numpy  # for number stuff
import random  # for random stuff
import os.path  # for saving info to file
from datetime import datetime  # for time stamping our file

# Read in from open rocket
columns = numpy.loadtxt('./openrocket/launch-12.csv', delimiter=',', unpack=True)

time     = columns[0]
altitude = columns[1]*1000  # km to meters
velocity = columns[4]

# only care about launch to apogee
begin = 500
apogee = 25000
time = time[begin:apogee]
altitude = altitude[begin:apogee]
velocity = velocity[begin:apogee]

# create a range of values
prop_values = numpy.arange(0, 2, 1)
integrate_values = numpy.arange(0, .002, .001)
deriv_values = numpy.arange(0, .02, .01)

# some arrays to store stuff in
simulations = []
pid_values = []

# dictionary for storing results of each sim
results = {}

# my dopey callback function
def randomness(i, t, aa):
    return aa + random.gauss(80,20)
        
k=0  # counter variable

# a range of P, I, D values
for p in prop_values:
    for i in integrate_values:
        for d in deriv_values:

            # initialize dictionary
            results[k] = {
                'pid': '',
                'pid2': '',
                'stability': []
            }

            # PID controller for roll angle
            pid0 = PIDController(p, i, d)

            # PID controller for roll rate
            pid1 = PIDController(10, 0, 0)

            # store PID controllers for later reference
            results[k]['pid'] = pid0
            results[k]['pid2'] = pid1

            # simulate it
            simulation = sim(time=time, altitude=altitude, velocity=velocity, timestep=None, PID=pid0, PID2=pid1, callback=randomness)

            # save info
            simulations.append(simulation)

            # increment counter
            k += 1

# now lets go through the simulations
for i in range(len(simulations)):

    # set initial stability value
    stability = 0

    # store length of roll rate from simulation    
    length = len(simulations[i][1])

    for t in range(length):

        # extract roll rate for some time t
        rr = simulations[i][1][t]

        # check to see if it falls in this range
        if rr > -.5 and rr < .5:

            # it does so lets count that as being stable
            stability += 1

    # store the result in our dictionary
    results[i]['stability'] = stability/length

# lets make a file to save some of this info
filename = 'results.txt'

# check to see if that file already exists
if os.path.isfile(filename):

    # it does so lets open and append
    f = open(filename, "a")
    f.write('\n%s\n' % str(datetime.now()))
    
# doesn't exist so lets create it
else:
    f = open(filename, "w")
    f.write('\n%s\n' % str(datetime.now()))

# now lets go through the results and find simulations with
# some range of 'acceptable' stability
for j in results:

    # lets say 70% stability is an acceptable percentage
    # just for example...(its probably not in real life)
    if results[j]['stability'] > .7:

        # stability and PID values
        # converted to a string
        stab = str(results[j]['stability'])
        Kp = str(results[j]['pid'].kP)
        Ki = str(results[j]['pid'].kI)
        Kd = str(results[j]['pid'].kD)
        Kp2 = str(results[j]['pid2'].kP)
        Ki2 = str(results[j]['pid2'].kI)
        Kd2 = str(results[j]['pid2'].kD)
        
        
        f.write('Stability: %s\n' % stab)
        f.write('Roll Angle P:%s I:%s D:%s\n' % (Kp, Ki, Kd))
        f.write('Roll Rate P:%s I:%s D:%s\n' % (Kp2, Ki2, Kd2))

# we are done now..close the file
f.close()