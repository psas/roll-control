#Canard lift force and coefficient of lift
#Originally programmed by Nathan Bergey
#Modified by William Harrington for testing with rocketroll2.py

from math import sin, cos, radians, exp, sqrt, degrees

# Define PSAS wing:
k_p = 2.45
k_v = 3.2
Cl_base = 3.2
fin_area = 1.13e-3

#coefficient of lift
def C_L(a, v):
    """Find C_L for a given speed and angle of attack
    
    :param float a: Angle of attack, alpha in degrees
    :param float v: velocity, v in m/s
    """
    
    # math is in radians
    a = radians(a)
    
    # Subsonic case
    def _subsonic():
        sina = sin(a)
        cosa = cos(a)
        cl = k_p*sina*cosa*cosa
        cl += k_v*cosa*sina*sina
        return cl
    
    # Supersonic case
    def _supersonic():
        cl = a*Cl_base
        return cl

    if v <= 265:
        return _subsonic()
    elif v < 330:
        # Intepolate between super and subsonic
        y0 = _subsonic()
        y1 = _supersonic()
        x0 = 265
        x1 = 330
        cl = y0 + (y1-y0)*(v - x0)/(x1-x0)
        return cl
    else:
        return _supersonic()

#Polynomial Approximation for Coefficient of Lift
def C_L_aprox(a, v):

    # Subsonic case
    def _subsonic():
        af = 0.0006
        bf = 0.045
        cl = af*a**2 + bf*a
        return cl
    
    # Supersonic case
    def _supersonic():
        cl = a*Cl_base
        return cl

    if v <= 265:
        return _subsonic()
    elif v < 330:
        # Intepolate between super and subsonic
        y0 = _subsonic()
        y1 = _supersonic()
        x0 = 265
        x1 = 330
        cl = y0 + (y1-y0)*(v - x0)/(x1-x0)
        return cl
    else:
        return _supersonic()


#lift force of canard
def lift(a, v, alt):
    """Compute the lift of one fin at an angle of
    attack, velocity, and altitdue
    
    :param float a: Angle of attack in degrees
    :param float v: velocity in m/s
    :param float alt: altitude MSL in meters
    :returns float lift in Newtons:
    
    """
    
    # get density of atmosphere with quick exponential model
    rho = 1.2250 * exp((-9.80665 * 0.0289644 * alt)/(8.31432*288.15))

    #l = 0.5*C_L(a, v)*rho*v*v*fin_area
    l = 0.5*C_L(a, v)*rho*v*v*fin_area*sin(a)
    
    if(a<0):
        return -l
    else:
        return l

#computes MOI as time progresses
def getMOI(t):
    # LV2.3 Constants
    I_0 = 0.086
    I_1 = 0.077    
    
    # compute I
    if t <= 0:
        I = I_0
    elif t < 5.6:
        I = I_0 + (I_1-I_0)*t/5.6
    else:
        I = I_1
    return I

def estimate_alpha(x, v, aa, t):
    """Return an estimated fin angle of attack for to
    achieve the required angular acceleration.
    
    :param x: Altitude (meters, MSL)
    :param v: Air velocity (m/s)
    :param aa: Angular acceleration to compute alpha for (degrees/s/s)
    :param t: Time (seconds since launch)
    :returns fin angle:
    
    """
    # LV2.3 Constants
    fin_area = 1.13e-3
    fin_arm = 0.085
    af = 0.0006
    bf = 0.045
    cl_super = 3.2
    
    
    # compute rho
    rho = 1.2250 * exp((-9.80665 * 0.0289644 * x)/(8.31432*288.15))
    
    #get MOI
    I = getMOI(t)
    
    def _subsonic():
        alpha = sqrt(abs(2*aa*I*af)/(rho*v*v*fin_area*fin_arm) + bf*bf) - bf
        alpha = alpha / (2*af)
        return alpha / 10**3
        #if degrees(alpha)>15:
        #    return 15
        #elif degrees(alpha)<-15:
        #    return -15
        #else:
        #    return degrees(alpha)
    
    def _supersonic():
        alpha = (aa*I)/(2*rho*v*v*fin_area*fin_arm*cl_super)
        return alpha / 10**3
        #if degrees(alpha)>15:
        #    return 15
        #if degrees(alpha)<-15:
        #    return -15
        #else:
        #    return degrees(alpha)
    
    
    if v <= 265:
        return _subsonic()
    elif v < 330:
        # Intepolate between super and subsonic
        y0 = _subsonic()
        y1 = _supersonic()
        x0 = 265
        x1 = 330
        cl = y0 + (y1-y0)*(v - x0)/(x1-x0)
        return cl
    else:
        return _supersonic()