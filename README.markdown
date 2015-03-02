# Canard Roll Control

Math, data, and algorithms for our canard roll control setup.

## Setup:

![overview](http://psas.github.io/roll-control/diagrams/PIDs.svg)

We have a modular flight computer stack. There is an ethernet bridge between sensors and actuators. The FC in the middle is running a state estimator (kalman filter) and a nested PID loop as in the above diagram.


## Canard Aerodynamics

Gathering up the theory from past roll teams for a theoretical model of the aerodynamics on delta wings:

**[notebooks/fin-force.ipynb](http://nbviewer.ipython.org/github/psas/roll-control/blob/master/notebooks/fin-force.ipynb)**

**[notebooks/accel-fin-alpha.ipynb](http://nbviewer.ipython.org/github/psas/roll-control/blob/master/notebooks/accel-fin-alpha.ipynb)**

Tring to use Launch 11 as a wind tunnel test:

**[notebooks/l11-wind-tunnel.ipynb](http://nbviewer.ipython.org/github/psas/roll-control/blob/master/notebooks/l11-wind-tunnel.ipynb)**

