"""Canard Aerodynamics
"""
from math import sin, cos, radians, exp, degrees

# Define PSAS wing:
k_p = 2.45
k_v = 3.2
Cl_base = 3.2
fin_area = 1.13e-3  # m^2
fin_arm = 0.085     # m

# Define LV2.3 Mass properties
I_0 = 0.086         # m^2 kg
I_1 = 0.077         # m^2 kg

# Data storage
current_alpha = 0


def C_L(a, v):
    """Find C_L for a given speed and angle of attack

    :param float a: Angle of attack, alpha in degrees
    :param float v: velocity, v in m/s
    :returns float C_L (dimensionless):

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

    # lift
    l = 0.5*C_L(a, v)*rho*v*v*fin_area

    if(a < 0):
        return -l
    else:
        return l


def angular_accel(a, x, v, t):
    """Compute angular accelation for a single point

    :param a: Fin alpha (degrees)
    :param x: altitude (meters, MSL)
    :param v: air velocity (m/s)
    :param t: time since launch (seconds)
    :returns float angular acceleration in degrees/s^2:

    """

    # compute I
    if t <= 0:
        I = I_0
    elif t < 5.6:
        I = I_0 + (I_1-I_0)*t/5.6
    else:
        I = I_1

    aa = degrees((4*lift(a, v, x)*fin_arm)/I)

    if a < 0:
        return -aa
    return aa


def servo(alpha, t):
    """Outputs canard fin position when requested by the flight computer

    :param alpha: requested canard angle in degrees
    :param t:     current time in seconds
    :returns actual canard angle in degrees:

    """

    global current_alpha

    t_ms = int(round(t * 1000))  # convert time to ms

    # servo only responds every 3.3ms
    if (t_ms % 3) == 0:
        current_alpha = alpha

    # clamp the output to only 15deg
    if current_alpha > 15:
        current_alpha = 15

    return current_alpha
