import random #for random values


#for roll rate
def setupRollRatePID(Kd,Ki,Kp,setPoint):
    #set up PID controller
    p=PIDController(Kp,Ki,Kd)
    p.setTarget(setPoint)
    return p

class PIDController:
    def __init__(self,p,i,d):
        self.kP=p
        self.kI=i
        self.kD=d
        self.target=0

        self.lastError=0
        self.integrator=0

    def setTarget(self,newTarget):
        self.target=newTarget
        self.integrator=0

    def step(self,currentValue):
        """
        Calculates the error and derives a desired output value.
        """
        # determine the error by simply looking at the difference between
        # current value and target value.
        error=currentValue-self.target

        # Build the output by summing the contributions of the
        # proportional, integral, and derivative models.
        output= (self.kP * error
                 + self.kI * self.integrator
                 + self.kD * (error - self.lastError)
                 )

        # Remember the error for the derivative model
        self.lastError=error
        # Add the error to the integral model
        self.integrator+=error

        return output
