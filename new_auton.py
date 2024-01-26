# Library imports
from vex import *
momentum = 5

# Begin project code
def forward(dist):
    gyro_10.set_rotation(0, DEGREES)
    leftmotor.spin(FORWARD)
    rightmotor.spin(FORWARD)
    leftmotor.set_position(0, DEGREES)
    rightmotor.set_position(0, DEGREES)
    leftmotor.set_velocity(100, PERCENT)
    rightmotor.set_velocity(100, PERCENT)
    # u sure u dont wanna reset gyro? It was dot there so i just did it for u.
    while True:
        if (rightmotor.position(DEGREES) + leftmotor.position(DEGREES))/2 - momentum >= dist:
            break
        rot = gyro_10.rotation()
        print(rot)
        leftmotor.set_velocity( 100 - max(0, rot) )
        rightmotor.set_velocity( 100 - abs(min(0, rot)) )
        wait(20, MSEC)
    rightmotor.stop()
    leftmotor.stop()

# motors always spin forward]
def backward(dist):
    gyro_10.set_rotation(0, DEGREES)
    leftmotor.spin(FORWARD)
    rightmotor.spin(FORWARD)
    leftmotor.set_position(0, DEGREES)
    rightmotor.set_position(0, DEGREES)
    leftmotor.set_velocity(-100, PERCENT)
    rightmotor.set_velocity(-100, PERCENT)
    while True:
        if abs(rightmotor.position(DEGREES) + leftmotor.position(DEGREES))/2 - momentum >= dist:
            break
        rot = gyro_10.rotation()
        leftmotor.set_velocity( -100 + abs(min(0, rot)) , PERCENT)
        rightmotor.set_velocity( -100 + max(0, rot), PERCENT)
        wait(20, MSEC)
    leftmotor.stop()
    rightmotor.stop()


def move(dist):
    if dist < 0:
        backward(abs(dist))
    else:
        forward(dist)

def turn_right(to_turn):
    gyro_10.set_rotation(0, DEGREES)
    turn_momentum = 35
    leftmotor.spin(FORWARD)
    rightmotor.spin(FORWARD)
    leftmotor.set_velocity(100, PERCENT)
    rightmotor.set_velocity(-100, PERCENT)
    while True:
        if gyro_10.rotation() > to_turn - turn_momentum:
            break
    leftmotor.stop()
    rightmotor.stop()

def turn_left(to_turn):
    gyro_10.set_rotation(0, DEGREES)
    turn_momentum = 35
    leftmotor.spin(FORWARD)
    rightmotor.spin(FORWARD)
    leftmotor.set_velocity(-100, PERCENT)
    rightmotor.set_velocity(100, PERCENT)
    while True:
        if abs(gyro_10.rotation()) > to_turn - turn_momentum:
            break
    leftmotor.stop()
    rightmotor.stop()

def gyro_turn(to_turn):
    if to_turn < 0:
        turn_left(abs(to_turn))
    else:
        turn_right(to_turn)
