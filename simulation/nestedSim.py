import lv2  # launch vehicle stuff
from scipy.integrate import simps  # cause we need to do some calculus bruh


def simulate(time, altitude, velocity, timestep, PID, PID2, callback):
    """Function simulates lv2 flight

    :param time: time in seconds
    :param altitude: altitude in meters
    :param velocity: velocity in meters/second
    :param timestep: change in time (seconds)
    :param PID: PID loop for controlling roll angle
    :param PID2: PID loop for controlling roll rate
    :param callback:
    """

    roll_accel = []
    roll_rate = [0]
    roll_angle = [0]
    fin_angle = []
    pids = []
    pids2 = []

    for i, t in enumerate(time):

        # roll angle PID loop
        correction0 = PID.step(roll_angle[-1])
        pids.append(correction0)

        # set correction to roll rate
        # PID loop target
        PID2.setTarget(correction0)

        # roll rate PID loop
        correction1 = PID2.step(roll_rate[-1])
        pids2.append(correction1)

        # estimate fin position
        a = lv2.estimate_alpha(correction1, altitude[i], velocity[i], t)

        # run through physical servo model
        a = lv2.servo(a, t)


        # integrate motion and record
        aa = lv2.angular_accel(a, altitude[i], velocity[i], t)

        # adjust actual angular aceleration by caller
        aa = callback(i, t, aa)

        roll_accel.append(aa)
        roll_angle.append(simps(roll_rate, time[:i+1]))
        roll_rate.append(simps(roll_accel, time[:i+1]))
        fin_angle.append(a)
        pids.append(correction0)
        pids2.append(correction1)

    return roll_accel, roll_rate, roll_angle, fin_angle, pids, pids2
