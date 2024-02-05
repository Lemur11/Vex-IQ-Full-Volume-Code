from vex import *

# Constants
kp = 1.5
# if we multiply the degrees we wanna turn by this num, we get the amount we want our motors to spin
# 2.3 is fine
tcov = 2.3
mommentum =  1
# State thread
def state():
    while True:
        print(brain_inertial.rotation(), left_drive_smart.velocity(PERCENT), right_drive_smart.velocity(PERCENT))


s = Thread(state)

def move(amnt, speed):
    # speed decides if its forward or backward
    brain_inertial.set_rotation(0, DEGREES)
    left_drive_smart.set_position(0, DEGREES)
    right_drive_smart.set_position(0, DEGREES)
    left_drive_smart.spin(FORWARD)
    right_drive_smart.spin(FORWARD)
    while (right_drive_smart.position(DEGREES) + left_drive_smart.position(DEGREES))/2 < amnt:
        error = brain_inertial.rotation(DEGREES) * kp
        if speed > 0:
            left_correct = speed - max(0, error)
            right_correct = speed - abs(min(0, error))
        elif speed < 0:
            left_correct = speed + abs(min(0, error))
            right_correct = speed + max(0, error)
        left_drive_smart.set_velocity(left_correct)
        right_drive_smart.set_velocity(right_correct)
        wait(0.5, SECONDS)
    left_drive_smart.stop()
    right_drive_smart.stop()

def turnr(degs):
    degs-= mommentum
    degs *= tcov
    while (abs(left_drive_smart.position(DEGREES))+abs(right_drive_smart.position(DEGREES)))/2 < degs:
        left_drive_smart.spin(FORWARD)
        right_drive_smart.spin(REVERSE)
    left_drive_smart.stop()
    right_drive_smart.stop()
    wait(0.5, SECONDS)

def turnl(degs):
    degs -= mommentum
    degs *= tcov
    while (abs(left_drive_smart.position(DEGREES))+abs(right_drive_smart.position(DEGREES)))/2 < degs:
        left_drive_smart.spin(REVERSE)
        right_drive_smart.spin(FORWARD)
    left_drive_smart.stop()
    right_drive_smart.stop()
    wait(0.5, SECONDS)
