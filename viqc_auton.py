from vex import *

def forward(distance, speed=100):
    rightmotor.set_position(0, DEGREES)
    leftmotor.set_position(0, DEGREES)
    brain_inertial.set_rotation(0, DEGREES)
    while (leftmotor.position(DEGREES) + rightmotor.position(DEGREES)) / 2 < distance:
        leftmotor.set_velocity((speed - brain_inertial.rotation()), PERCENT)
        rightmotor.set_velocity((speed + brain_inertial.rotation()), PERCENT)
        leftmotor.spin(FORWARD)
        rightmotor.spin(FORWARD)
        wait(20, MSEC)
    leftmotor.stop()
    rightmotor.stop()

def gyro_turn(heading, momentum, velocity=100):
    gyro_10.set_rotation(0, DEGREES)
    if heading > gyro_10.rotation():
        while heading - momentum > gyro_10.rotation():
            leftmotor.set_velocity(velocity, PERCENT)
            rightmotor.set_velocity(velocity, PERCENT)
            leftmotor.spin(REVERSE)
            rightmotor.spin(FORWARD)
            wait(20, MSEC)
    else:
        while heading - momentum < gyro_10.rotation():
            leftmotor.set_velocity(velocity, PERCENT)
            rightmotor.set_velocity(velocity, PERCENT)
            leftmotor.spin(FORWARD)
            rightmotor.spin(REVERSE)
            wait(20, MSEC)
    leftmotor.stop()
    rightmotor.stop()

def backward(distance, speed=100):
    rightmotor.set_position(0, DEGREES)
    leftmotor.set_position(0, DEGREES)
    brain_inertial.set_rotation(0, DEGREES)
    while (leftmotor.position(DEGREES) + rightmotor.position(DEGREES)) / 2 > distance:
        leftmotor.set_velocity((speed - brain_inertial.rotation()), PERCENT)
        rightmotor.set_velocity((speed + brain_inertial.rotation()), PERCENT)
        leftmotor.spin(REVERSE)
        rightmotor.spin(REVERSE)
        wait(20, MSEC)
    leftmotor.stop()
    rightmotor.stop()



def when_started():
    # setup
    intake.set_max_torque(100, PERCENT)
    hopper.set_max_torque(100, PERCENT)
    intake.set_velocity(100, PERCENT)
    hopper.set_velocity(100, PERCENT)
    intake.spin(FORWARD)
    gyro_10.calibrate(GyroCalibrationType.NORMAL)

    # movement

when_started()
