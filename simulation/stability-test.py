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
prop_values = numpy.arange(0, 30.25, .25)
integrate_values = numpy.arange(2, 15, 1)
deriv_values = numpy.arange(0, 1, 1)

# some arrays to store stuff in
simulations = []
pid_values = []

# dictionary for storing results of each sim
results = {}

# my dopey callback function
def randomness(i, t, aa):
    return aa + random.gauss(80,20)
        
k = 0  # counter variable

total = len(prop_values)
total *= len(integrate_values)
total *= len(deriv_values)

print 'About to perform %d simulation(s)...' % total

# a range of P, I, D values
for p in range(len(prop_values)):
    for i in range(len(integrate_values)):
        for d in range(len(deriv_values)):

            # initialize dictionary
            results[k] = {
                'pid': '',
                'pid2': '',
                'stability': []
            }

            # PID controller for roll angle
            pid0 = PIDController(prop_values[p], integrate_values[i], deriv_values[d])

            # PID controller for roll rate
            pid1 = PIDController(0, 0, 0)

            # store PID controllers for later reference
            results[k]['pid'] = pid0
            results[k]['pid2'] = pid1

            # simulate it
            simulation = sim(time=time, altitude=altitude, velocity=velocity, timestep=None, PID=pid0, PID2=pid1, callback=randomness)[1]

            # save info
            simulations.append(simulation)

            # increment counter
            k += 1
            
            # show user how much longer
            percentage_comp = k/total
            percentage_comp *= 100
            print 'Simulation %d completed. Overall completion %.2f%%' % (k, percentage_comp)


# alright now lets look at which simulations were stable
print 'Beginning stability analysis....'
print 'About to analyze %d simulations' % len(simulations)

# grab the total number of iterations we are about to do
total = len(simulations)*len(simulations[0])

# another counter variable
l = 0

# now lets go through the simulations
for i in range(len(simulations)):

    # set initial stability value
    stability = 0

    # store length of roll rate from simulation    
    length = len(simulations[i])

    for t in range(length):

        # extract roll rate for some time t
        rr = simulations[i][t]

        # check to see if it falls in this range
        if rr > -.5 and rr < .5:

            # it does so lets count that as being stable
            stability += 1

        # update counter
        l += 1
        
        # keep track of analysis completion percentage
        #perc_comp = ((t+1)*(i+1))/total
        perc_comp = l/total
        perc_comp *= 100
        
        #only show the percent complete every so often
        if (t % 2000) == 0:
            print 'Overall analysis compeletion %.3f%%' % perc_comp

    # store the result in our dictionary
    results[i]['stability'] = stability/length

    # keep track of analysis completion
    print 'Analysis complete on simulation %d' % i


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

# counter variable
good_res = 0

# now lets go through the results and find simulations with
# some range of 'acceptable' stability
for j in results:

    # lets say 70% stability is an acceptable percentage
    # just for example...(its probably not in real life)
    if results[j]['stability'] > .8:

        # count good results
        good_res += 1

        # stability and PID values
        # converted to a string
        stab = str(results[j]['stability'])
        Kp = str(results[j]['pid'].kP)
        Ki = str(results[j]['pid'].kI)
        Kd = str(results[j]['pid'].kD)
        Kp2 = str(results[j]['pid2'].kP)
        Ki2 = str(results[j]['pid2'].kI)
        Kd2 = str(results[j]['pid2'].kD)
        
        # write everything in a neat format to the file        
        f.write('Stability: %s\n' % stab)
        f.write('Roll Angle P:%s I:%s D:%s\n' % (Kp, Ki, Kd))
        f.write('Roll Rate P:%s I:%s D:%s\n' % (Kp2, Ki2, Kd2))

# Completion message
print '%d good results saved' % good_res

# we are done now..close the file
f.close()
