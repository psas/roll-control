import lv2
from scipy.integrate import simps

def simulate(time, altitude, velocity, timestep, PID, callback):

    roll_accel = []
    roll_rate = [0]
    roll_angle = [0]
    fin_angle = []
    pids =[]

    for i, t in enumerate(time):

        # get correction from PID loop
        correction = PID.step(roll_rate[-1])

        # estimate fin position
        a = lv2.estimate_alpha(correction, altitude[i], velocity[i], t)

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
        pids.append(correction)

    return roll_accel, roll_rate, roll_angle, fin_angle, pids
