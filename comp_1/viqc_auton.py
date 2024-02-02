#config: {leftmotor:4, rightmotor(rev):9, brain_inertial:10, intake:[6(rev),12], hopper:[5, 11(rev)]}

#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
brain_inertial = Inertial()
leftmotor = Motor(Ports.PORT4, False)
rightmotor = Motor(Ports.PORT9, True)
gyro_10 = Gyro(Ports.PORT10)



# Make random actually random
def setRandomSeedUsingAccel():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    urandom.seed(int(xaxis + yaxis + zaxis))
    
# Set random seed 
setRandomSeedUsingAccel()

#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
# 
# 	Project:      VEXcode Project
# 	Author:       VEX
# 	Created:
# 	Description:  VEXcode IQ Python Project
# 
# ------------------------------------------

# Library imports
from vex import *
MOMENTUM = 10
kp = 1
fixer = 20

# Begin project code
def move(dist, momentum=MOMENTUM):
    if dist > 0:
        leftmotor.set_velocity(100, RPM)
        rightmotor.set_velocity(100, RPM)
        leftmotor.set_position(0, DEGREES)
        rightmotor.set_position(0, DEGREES)
        leftmotor.spin(FORWARD)
        rightmotor.spin(FORWARD)
        wait(0.2, SECONDS)  # changed
        while (leftmotor.position(DEGREES) + rightmotor.position(DEGREES))/2 - momentum < dist:
            diff = (leftmotor.velocity(RPM) - rightmotor.velocity(RPM))*kp
            if diff > 0:
                leftmotor.set_velocity(leftmotor.velocity(RPM) - abs(diff) + fixer, RPM)
            else:
                rightmotor.set_velocity(rightmotor.velocity(RPM) - abs(diff) + fixer, RPM)
            leftmotor.spin(FORWARD)
            rightmotor.spin(FORWARD)
        leftmotor.stop()
        rightmotor.stop()
    else:
        # dist is negative
        leftmotor.set_velocity(-80, RPM)
        rightmotor.set_velocity(-80, RPM)
        leftmotor.set_position(0, DEGREES)
        rightmotor.set_position(0, DEGREES)
        leftmotor.spin(FORWARD)
        rightmotor.spin(FORWARD)
        wait(0.2, SECONDS)
        t = -80
        while (leftmotor.position(DEGREES) + rightmotor.position(DEGREES))/2 + momentum > dist:
            off_l = t - leftmotor.velocity(RPM)
            off_r = t - rightmotor.velocity(RPM)
            leftmotor.set_velocity(t+off_l)
            rightmotor.set_velocity(t+off_l)
            leftmotor.spin(FORWARD)
            rightmotor.spin(FORWARD)
        leftmotor.stop()
        rightmotor.stop()

def gyro_turn(direction, momentum=MOMENTUM, speed=80):
   gyro_10.calibrate(GyroCalibrationType.NORMAL)
   gyro_10.set_rotation(0, DEGREES)
   if direction > gyro_10.rotation():
      while direction - momentum > -1*gyro_10.rotation():
          print(gyro_10.rotation())
          leftmotor.set_velocity(speed, PERCENT)
          rightmotor.set_velocity(speed, PERCENT)
          leftmotor.spin(REVERSE)
          rightmotor.spin(FORWARD)
          wait(20, MSEC)
      leftmotor.stop()
      rightmotor.stop()
   else:
      while direction + momentum < -1*gyro_10.rotation():
          leftmotor.set_velocity(speed, PERCENT)
          rightmotor.set_velocity(speed, PERCENT)
          leftmotor.spin(FORWARD)
          rightmotor.spin(REVERSE)
          wait(20, MSEC)
      leftmotor.stop()
      rightmotor.stop()

intake.set_max_torque(100, PERCENT)
hopper.set_max_torque(100, PERCENT)
intake.set_velocity(100, PERCENT)
hopper.set_velocity(100, PERCENT)
intake.spin(FORWARD)

def run_path():
  move(601)
# move(601)
# gyro_turn(91)
# move(296)
# gyro_turn(-153)
# move(331)

# move(331)
# gyro_turn(-27)
# move(593)
# gyro_turn(-27)
# move(331)
# gyro_turn(-63)
# move(445)
# gyro_turn(135)
# move(421)
# gyro_turn(-135)
# move(445)
# gyro_turn(-168)
# move(756)
# gyro_turn(25)
# move(741)
# gyro_turn(53)
# move(593)
# gyro_turn(180)
# move(296)
# gyro_turn(-90)
# move(889)

# move(296)
# gyro_turn(180)
# move(1186)
# gyro_turn(-90)
# move(741)
# gyro_turn(-153)
# move(663)
# gyro_turn(10)
# move(741)
# gyro_turn(8)
# move(629)
# gyro_turn(-19)
# move(343)
# gyro_turn(-116)
# move(593)

run_path()
