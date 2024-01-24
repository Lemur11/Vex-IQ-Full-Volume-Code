#config: {leftmotor:4, rightmotor(rev):9, gyro10:10, intake:[6(rev),12], hopper:[5, 11(rev)]}

from vex import *
MOMENTUM = 0

def move(dist, speed=80, kp=2):
    leftmotor.set_position(0, DEGREES)
    rightmotor.set_position(0, DEGREES)
    gyro10.set_heading(0, DEGREES)
    # add starting velocity?
    rightmotor.spin(FORWARD)
    leftmotor.spin(FORWARD)
    if dist > 0:
        while leftmotor.position(DEGREES) < abs(dist):
            error = (gyro10.rotation(DEGREES)) * kp
            leftmotor.set_velocity(speed - error)
            rightmotor.set_velocity(speed + error)
    else:
        speed *= -1
        while leftmotor.position(DEGREES) > abs(dist):
            error = (gyro10.rotation()) * kp
            leftmotor.set_velocity(speed + error)
            rightmotor.set_velocity(speed - error)
    rightmotor.stop()
    leftmotor.stop()

def gyro_turn(direction, momentum=MOMENTUM, speed=80):
     gyro10.set_rotation(0, DEGREES)
     if direction > gyro10.rotation():
        while direction - momentum > gyro10.rotation():
            leftmotor.set_velocity(speed, PERCENT)
            rightmotor.set_velocity(speed, PERCENT)
            leftmotor.spin(REVERSE)
            rightmotor.spin(FORWARD)
            wait(20, MSEC)
     else:
        while direction - momentum < gyro10.rotation():
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
    # path code goes here
    move(300)
    move(-300)
    gyro_turn(90)
    gyro_turn(-90)

run_path()

