#Canard lift force and coefficient of lift
#Originally programmed by Nathan Bergey
#Modified by William Harrington for testing with rocketroll2.py

from math import sin, cos, radians, exp

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

    l = 0.5*C_L(a, v)*rho*v*v*fin_area
    
    return l