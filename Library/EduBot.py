"""
Open Robotics library for educational use. This library gives access to a handful of chassis designs
with the aimed intension to be for cheaper robotics use without the need of expert programming.

Code written by:

Dexter R Shepherd, AI student at the University of Sussex
    https://www.linkedin.com/in/dexter-shepherd-1a4a991b8/
    https://shepai.github.io/

Debugged by:

Joshua Kybett, Computer Science Masters student at the University of Sussex

This code is open source, therefore free to distribute or modify. We only ask to credit original source.

"""
#import standard needed libraries
from machine import Pin
import machine
import utime
#import servo libraries
try:
    pass
except:
    print("Servo libraries are not in the directory. These will need to be installed before using servo chassis")
    #output more values
print("Loaded OpenEduBot Education library")

ValidGPIO=[i for i in range(28)] #valid pins
class WheelBot:
    """
    Requires:
    2 DC motors
    Motor driver
    Raspberry Pi Pico
    Two separate battery packs
        4xAA
        3XAA
    Ultrasound range sensor
    Breadboard (for ease)
    """
    def __init__(self,trigPin=26,echoPin=22,in1=18,in2=19,in3=20,in4=21):
        """
        Creates a wheel chassis bot for two DC motors using a motor driver and ultrasound sensor
        with given pins that the chassis can use connected to the Pico. Al must be GPIO pins
        @param trigPin is the pin that connects to the ultrasound sensor trigger pin
        @param echoPin is the pin that connects to the ultrasound sensor echo pin
        @param in1 connects to the motor driver in1 (motor1)
        @param in2 connects to the motor driver in2 (motor1)
        @param in3 connects to the motor driver in3 (motor2)
        @param in4 connects to the motor driver in4 (motor2)
        """
        assert in1 in ValidGPIO and in2 in ValidGPIO and in3 in ValidGPIO and in4 in ValidGPIO,"Invalid pin specified. Only use pins within "+str(ValidGPIO)
        if type(trigPin)==type([]) and type(echoPin)==type([]): #if multiple pins for multiple sensors are present
            assert len(trigPin)==len(echoPin),"Echo Pin and Trigger Pin list of pins are not equal. Place in format [trig1,trig2] and [echo1,echo2]"
            self.trigger = []
            self.echo = []
            for i in range(len(trigPin)): #loop through and check the pins + append them
                self.trigger.append(Pin(trigPin[i], Pin.OUT))
                assert trigPin.count(trigPin[i])==1 and echoPin.count(echoPin[i])==1 and trigPin[i] not in echoPin and echoPin[i] not in trigPin, "You cannot have the same pin called multiple times"
                self.echo.append(Pin(echoPin[i], Pin.IN))
        elif trigPin!=None and echoPin!=None: #use as default pins
            assert trigPin in ValidGPIO and echoPin in ValidGPIO, "Invalid pin specified. Only use pins within "+str(ValidGPIO)
            self.trigger = [Pin(trigPin, Pin.OUT)]
            self.echo = [Pin(echoPin, Pin.IN)]
        self.IN1 = Pin(in1, Pin.OUT)
        self.IN2 = Pin(in2, Pin.OUT)
        self.IN3 = Pin(in3, Pin.OUT)
        self.IN4 = Pin(in4, Pin.OUT)

    def distance(self):
       """
       Get the distance from the ultrasound sensor wired to the trigger and echo pins
       if multiple sensors are entered then return array of distances
       """
       val=[]
       for i in range(len(self.trigger)): #go through all sensors
           trig=self.trigger[i] #get each pin value
           echo=self.echo[i]
           trig.low()
           utime.sleep_us(2)
           trig.high()
           utime.sleep_us(5)
           trig.low()
           while echo.value() == 0:
               signaloff = utime.ticks_us()
           while echo.value() == 1:
               signalon = utime.ticks_us()
           timepassed = signalon - signaloff
           distance = (timepassed * 0.0343) / 2
           val.append(distance)
       return val if len(val)>1 else val[0] #return list for multiple sensors and single value for one
    def forward(self):
        """
        Move the robot forward by rotating both motors the same direction. This relies on the robot motors being wired the same way
        """
        self.motor1()
        self.motor2()
    def backward(self):
        """
        Move the robot backward by rotating both motors the same direction. This relies on the robot motors being wired the same way
        """
        self.motor1(fir=False)
        self.motor2(fir=False)
    def left(self,delay=1):
        """
        Move the robot forward by rotating both motors the same direction. This relies on the robot motors being wired the same way
        @param delay is how long the robot will turn left for
        """
        self.stop()
        self.motor1(fir=False)
        self.motor2()
        utime.sleep(delay)
        #self.stop()
    def right(self,delay=1):
        """
        Move the robot forward by rotating both motors the same direction. This relies on the robot motors being wired the same way
        @param delay is how long the robot will turn right for
        """
        self.stop()
        self.motor1()
        self.motor2(fir=False)
        utime.sleep(delay)
        #self.stop()
    def motor1(self,fir=True):
        """
        Rotate the motor based on the direction
        @param fir decides which way it should rotate
        """
        if fir:
            self.IN1.value(1)  #spin forward
            self.IN2.value(0)
        else:
            self.IN1.value(0)  #spin forward
            self.IN2.value(1)
    def motor2(self,fir=True):
        """
        Rotate the motor based on the direction
        @param fir decides which way it should rotate
        """
        if fir:
            self.IN3.value(1)  #spin forward
            self.IN4.value(0)
        else:
            self.IN3.value(0)  #spin forward
            self.IN4.value(1)
    def stop(self):
        """
        Stop the robot by setting all signals to 0
        """
        self.IN1.value(0)
        self.IN2.value(0)
        self.IN3.value(0)
        self.IN4.value(0)


class lineFollower(WheelBot):
    def __init__(self, sensePinL=1,sensePinR=1,in1=18,in2=19,in3=20,in4=21):
        super().__init__(trigPin=None,echoPin=None,in1=18,in2=19,in3=20,in4=21)

class ServoBot:
    pass

class wheelBot_2:
    """
    Requires:
    2 DC motors
    Pico Robotics board
    Raspberry Pi Pico
    Battery packs
        4xAA
    Light sensitivity sensors (optional)
    
    The I2C communication part of the code was taken from the KitronikPicoRobotics library
    which was used within our own library function to make the control easier for all ages
    """

    #Class variables - these should be the same for all instances of the class.
    # If you wanted to write some code that stepped through
    # the servos or motors then this is the Base and size to do that
    SRV_REG_BASE = 0x08
    MOT_REG_BASE = 0x28
    REG_OFFSET = 4
    def __init__(self, I2CAddress=108,sda=8,scl=9):
        self.CHIP_ADDRESS = 108
        sda=machine.Pin(sda)
        scl=machine.Pin(scl)
        self.i2c=machine.I2C(0,sda=sda, scl=scl, freq=100000)
        self.initPCA()
    #to perform a software reset on the PCA chip.
    #Separate from the init function so we can reset at any point if required - useful for development...
    def swReset(self):
        self.i2c.writeto(0,"\x06")

    #setup the PCA chip for 50Hz and zero out registers.
    def initPCA(self):
        self.swReset() #make sure we are in a known position
        #setup the prescale to have 20mS pulse repetition - this is dictated by the servos.
        self.i2c.writeto_mem(108,0xfe,"\x78")
        #block write outputs to off
        self.i2c.writeto_mem(108,0xfa,"\x00")
        self.i2c.writeto_mem(108,0xfb,"\x00")
        self.i2c.writeto_mem(108,0xfc,"\x00")
        self.i2c.writeto_mem(108,0xfd,"\x00")
        #come out of sleep
        self.i2c.writeto_mem(108,0x00,"\x01")    

    def setPrescaleReg(self):
        i2c.writeto_mem(108,0xfe,"\x78")
    #Driving the motor is simpler than the servo - just convert 0-100% to 0-4095 and push it to the correct registers.
    #each motor has 4 writes - low and high bytes for a pair of registers. 
    def motorOn(self,motor, direction, speed):
        #cap speed to 0-100%
        if (speed<0):
            speed = 0
        elif (speed>100):
            speed=100
            
        motorReg = self.MOT_REG_BASE + (2 * (motor - 1) * self.REG_OFFSET)
        PWMVal = int(speed * 40.95)
        lowByte = PWMVal & 0xFF
        highByte = (PWMVal>>8) & 0xFF #motors can use all 0-4096
        #print (motor, direction, "LB ",lowByte," HB ",highByte)
        if direction == "f":
            self.i2c.writeto_mem(self.CHIP_ADDRESS, motorReg,bytes([lowByte]))
            self.i2c.writeto_mem(self.CHIP_ADDRESS, motorReg+1,bytes([highByte]))
            self.i2c.writeto_mem(self.CHIP_ADDRESS, motorReg+4,bytes([0]))
            self.i2c.writeto_mem(self.CHIP_ADDRESS, motorReg+5,bytes([0]))
        elif direction == "r":
            self.i2c.writeto_mem(self.CHIP_ADDRESS, motorReg+4,bytes([lowByte]))
            self.i2c.writeto_mem(self.CHIP_ADDRESS, motorReg+5,bytes([highByte]))
            self.i2c.writeto_mem(self.CHIP_ADDRESS, motorReg,bytes([0]))
            self.i2c.writeto_mem(self.CHIP_ADDRESS, motorReg+1,bytes([0]))
        else:
            self.i2c.writeto_mem(self.CHIP_ADDRESS, motorReg+4,bytes([0]))
            self.i2c.writeto_mem(self.CHIP_ADDRESS, motorReg+5,bytes([0]))
            self.i2c.writeto_mem(self.CHIP_ADDRESS, motorReg,bytes([0]))
            self.i2c.writeto_mem(self.CHIP_ADDRESS, motorReg+1,bytes([0]))
            raise Exception("INVALID DIRECTION")
    #To turn off set the speed to 0...
    def motorOff(self,motor):
        self.motorOn(motor,"f",0)
    def forward(self,speed):
        """
        Move the robot forward by rotating both motors the same direction. This relies on the robot motors being wired the same way
        @param speed is the speed that the robot will move at
        """
        self.motorOn(4, "f", speed)
        self.motorOn(3, "f", speed)
    def backward(self,speed):
        """
        Move the robot backward by rotating both motors the same direction. This relies on the robot motors being wired the same way
        """
        self.motorOn(4, "r", speed)
        self.motorOn(3, "r", speed)
    def left(self,speed=30,delay=1):
        """
        Move the robot forward by rotating both motors the same direction. This relies on the robot motors being wired the same way
        @param speed is how quickly it rotates
        @param delay is how long the robot will turn left for
        """
        self.motorOff(4)
        self.motorOff(3)
        self.motorOn(4, "f", speed)
        self.motorOn(3, "r", speed)
        utime.sleep(delay)
        #self.stop()
    def right(self,speed=30,delay=1):
        """
        Move the robot forward by rotating both motors the same direction. This relies on the robot motors being wired the same way
        @param speed is how quickly it rotates
        @param delay is how long the robot will turn right for
        """
        self.motorOff(4)
        self.motorOff(3)
        self.motorOn(4, "r", speed)
        self.motorOn(3, "f", speed)
        utime.sleep(delay)
        #self.stop()
    
    def stop(self):
        """
        Stop the robot by setting all signals to 0
        """
        self.motorOff(4)
        self.motorOff(3)

class servoBot:
    def __init__(self,chanA,chanB,I2CAddress=108,sda=8,scl=9):
        self.CHIP_ADDRESS = 108
        sda=machine.Pin(sda)
        scl=machine.Pin(scl)
        self.i2c=machine.I2C(0,sda=sda, scl=scl, freq=100000)
        self.initPCA()
    #Class variables - these should be the same for all instances of the class.
    # If you wanted to write some code that stepped through
    # the servos or motors then this is the Base and size to do that
    SRV_REG_BASE = 0x08
    MOT_REG_BASE = 0x28
    REG_OFFSET = 4

    #to perform a software reset on the PCA chip.
    #Separate from the init function so we can reset at any point if required - useful for development...
    def swReset(self):
        self.i2c.writeto(0,"\x06")

    #setup the PCA chip for 50Hz and zero out registers.
    def initPCA(self):
        self.swReset() #make sure we are in a known position
        #setup the prescale to have 20mS pulse repetition - this is dictated by the servos.
        self.i2c.writeto_mem(108,0xfe,"\x78")
        #block write outputs to off
        self.i2c.writeto_mem(108,0xfa,"\x00")
        self.i2c.writeto_mem(108,0xfb,"\x00")
        self.i2c.writeto_mem(108,0xfc,"\x00")
        self.i2c.writeto_mem(108,0xfd,"\x00")
        #come out of sleep
        self.i2c.writeto_mem(108,0x00,"\x01")

    def setPrescaleReg(self):
        i2c.writeto_mem(108,0xfe,"\x78")


    def servoWrite(self,servo, degrees):
        #check the degrees is a reasonable number. we expect 0-180, so cap at those values.
        if(degrees>180):
            degrees = 180
        elif (degrees<0):
            degrees = 0
        #check the servo number
        if((servo<1) or (servo>8)):
            raise Exception("INVALID SERVO NUMBER") #harsh, but at least you'll know
        calcServo = self.SRV_REG_BASE + ((servo - 1) * self.REG_OFFSET)
        PWMVal = int((degrees*2.2755)+102) # see comment above for maths
        lowByte = PWMVal & 0xFF
        highByte = (PWMVal>>8)&0x01 #cap high byte at 1 - shoud never be more than 2.5mS.
        self.i2c.writeto_mem(self.CHIP_ADDRESS, calcServo,bytes([lowByte]))
        self.i2c.writeto_mem(self.CHIP_ADDRESS, calcServo+1,bytes([highByte]))

