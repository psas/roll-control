import random #for random values


#for roll rate
def setupRollRatePID(Kd,Ki,Kp,setPoint):
    '''
    getMode=input('Select test mode: (1 for manual 0 for random): ') #test mode
    #manually enter values for PID controller
    if(getMode==1):
        setPoint = input('Target angular velocity: ') #set target roll rate
        setKp = input('Proportional gain for PID controller: ') #set Kp 
        setKi = input('Integral gain for PID controller: ') #set Ki
        setKd = input('Derivative gain for PID controller: ') #set Kd
    #randomly generate values for PID controller based on given intervals
    else:
        print 'Enter the following inputs as two element arrays'
        print 'And make sure that the first element is less than the second'
        print 'Ex: [0,1]'
        getSetPointInterval=input('Set Point Interval: ')
        getKpInterval=input('Kp Interval: ')
        getKiInterval=input('Ki Interval: ')
        getKdInterval=input('Kd Interval: ')
        setPoint=random.uniform(getSetPointInterval[0],getSetPointInterval[1])
        setKp=random.uniform(getKpInterval[0],getKpInterval[1])
        setKi=random.uniform(getKiInterval[0],getKiInterval[1])
        setKd=random.uniform(getKdInterval[0],getKdInterval[1])
    '''
    #set up PID controller
    p=PIDController(Kp,Ki,Kd)
    p.setTarget(setPoint)
    return p
    
#for angular position
def setupThetaPID(Kd,Ki,Kp,setPoint):
    '''
    getMode=input('Select test mode: (1 for manual 0 for random): ') #test mode
    #alpha=input('Enter initial canard angle: ') #initial canard angle

    #manually enter values for PID controller
    if(getMode==1):
        setPoint = input('Target theta: ') #set target roll rate
        setKp = input('Proportional gain for PID controller: ') #set Kp 
        setKi = input('Integral gain for PID controller: ') #set Ki
        setKd = input('Derivative gain for PID controller: ') #set Kd
    #randomly generate values for PID controller based on given intervals
    else:
        print 'Enter the following inputs as two element arrays'
        print 'And make sure that the first element is less than the second'
        print 'Ex: [0,1]'
        getSetPointInterval=input('Set Point Interval: ')
        getKpInterval=input('Kp Interval: ')
        getKiInterval=input('Ki Interval: ')
        getKdInterval=input('Kd Interval: ')
        setPoint=random.uniform(getSetPointInterval[0],getSetPointInterval[1])
        setKp=random.uniform(getKpInterval[0],getKpInterval[1])
        setKi=random.uniform(getKiInterval[0],getKiInterval[1])
        setKd=random.uniform(getKdInterval[0],getKdInterval[1])
    '''
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


'''
This is another implementation of the PID controller, slightly different then the one above and it was the one being used originally

#for roll rate
def setupRollRatePID():
    getMode=input('Select test mode: (1 for manual 0 for random): ') #test mode
    
    #manually enter values for PID controller
    if(getMode==1):
        setPoint = input('Target roll rate: ') #set target roll rate
        setKp = input('Proportional gain for PID controller: ') #set Kp 
        setKi = input('Integral gain for PID controller: ') #set Ki
        setKd = input('Derivative gain for PID controller: ') #set Kd
    #randomly generate values for PID controller based on given intervals
    else:
        print 'Enter the following inputs as two element arrays'
        print 'And make sure that the first element is less than the second'
        print 'Ex: [0,1]'
        getSetPointInterval=input('Set Point Interval: ')
        getKpInterval=input('Kp Interval: ')
        getKiInterval=input('Ki Interval: ')
        getKdInterval=input('Kd Interval: ')
        setPoint=random.uniform(getSetPointInterval[0],getSetPointInterval[1])
        setKp=random.uniform(getKpInterval[0],getKpInterval[1])
        setKi=random.uniform(getKiInterval[0],getKiInterval[1])
        setKd=random.uniform(getKdInterval[0],getKdInterval[1])
    #set up PID controller
    p=PID(setKp,setKi,setKd)
    p.setPoint(setPoint)
    return p
    
#for angular position
def setupThetaPID():
    getMode=input('Select test mode: (1 for manual 0 for random): ') #test mode
    
    #manually enter values for PID controller
    if(getMode==1):
        setPoint = input('Target theta: ') #set target roll rate
        setKp = input('Proportional gain for PID controller: ') #set Kp 
        setKi = input('Integral gain for PID controller: ') #set Ki
        setKd = input('Derivative gain for PID controller: ') #set Kd
    #randomly generate values for PID controller based on given intervals
    else:
        print 'Enter the following inputs as two element arrays'
        print 'And make sure that the first element is less than the second'
        print 'Ex: [0,1]'
        getSetPointInterval=input('Set Point Interval: ')
        getKpInterval=input('Kp Interval: ')
        getKiInterval=input('Ki Interval: ')
        getKdInterval=input('Kd Interval: ')
        setPoint=random.uniform(getSetPointInterval[0],getSetPointInterval[1])
        setKp=random.uniform(getKpInterval[0],getKpInterval[1])
        setKi=random.uniform(getKiInterval[0],getKiInterval[1])
        setKd=random.uniform(getKdInterval[0],getKdInterval[1])
    #set up PID controller
    p=PID(setKp,setKi,setKd)
    p.setPoint(setPoint)
    return p

#old PID controller implementation
class PID:
	"""
	Discrete PID control
	"""

	def __init__(self, P=2.0, I=0.0, D=1.0, Derivator=0, Integrator=0, Integrator_max=500, Integrator_min=-500):

		self.Kp=P
		self.Ki=I
		self.Kd=D
		self.Derivator=Derivator
		self.Integrator=Integrator
		self.Integrator_max=Integrator_max
		self.Integrator_min=Integrator_min

		self.set_point=0.0
		self.error=0.0

	def update(self,current_value):
		"""
		Calculate PID output value for given reference input and feedback
		"""

		self.error = self.set_point - current_value

		self.P_value = self.Kp * self.error
		self.D_value = self.Kd * ( self.error - self.Derivator)
		self.Derivator = self.error

		self.Integrator = self.Integrator + self.error

		if self.Integrator > self.Integrator_max:
			self.Integrator = self.Integrator_max
		elif self.Integrator < self.Integrator_min:
			self.Integrator = self.Integrator_min

		self.I_value = self.Integrator * self.Ki

		PID = self.P_value + self.I_value + self.D_value

		return PID

	def setPoint(self,set_point):
		"""
		Initilize the setpoint of PID
		"""
		self.set_point = set_point
		self.Integrator=0
		self.Derivator=0

	def setIntegrator(self, Integrator):
		self.Integrator = Integrator

	def setDerivator(self, Derivator):
		self.Derivator = Derivator

	def setKp(self,P):
		self.Kp=P

	def setKi(self,I):
		self.Ki=I

	def setKd(self,D):
		self.Kd=D

	def getPoint(self):
		return self.set_point

	def getError(self):
		return self.error

	def getIntegrator(self):
		return self.Integrator

	def getDerivator(self):
		return self.Derivator
'''
