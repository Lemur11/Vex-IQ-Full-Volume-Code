# Library imports
from vex import *

# Constants
kp = 1.5


# State thread
def state():
    while True:
        print(brain_inertial.rotation(), left_drive_smart.velocity(PERCENT), right_drive_smart.velocity(PERCENT))


s = Thread(state)


def move(amnt, speed):
    brain_inertial.set_rotation(0, DEGREES)
    left_drive_smart.set_position(0, DEGREES)
    right_drive_smart.set_position(0, DEGREES)
    left_drive_smart.spin(FORWARD)
    right_drive_smart.spin(FORWARD)
    while (right_drive_smart.position(DEGREES) + left_drive_smart.position(DEGREES)) / 2 < amnt:
        error = brain_inertial.rotation(DEGREES) * kp
        left_correct = speed - max(0, error)
        right_correct = speed - abs(min(0, error))
        left_drive_smart.set_velocity(left_correct)
        right_drive_smart.set_velocity(right_correct)
        wait(0.5, SECONDS)
    left_drive_smart.stop()
    right_drive_smart.stop()

def trun(degs):
    drivetrain.set_heading(0, DEGREES)
    drivetrain.set_turn_velocity(100, PERCENT)
    left_drive_smart.set_velocity(100, PERCENT)
    right_drive_smart.set_velocity(100, PERCENT)
    degrs = degs * (2+(2/9))
    left_drive_smart.spin_for(FORWARD, degrs, DEGREES, wait=False)
    right_drive_smart.spin_for(FORWARD, -1*degrs, DEGREES)
    if degs < 0:
        drivetrain.turn_to_heading(360-degs, DEGREES)
    else:
        drivetrain.turn_to_heading(degs, DEGREES)
