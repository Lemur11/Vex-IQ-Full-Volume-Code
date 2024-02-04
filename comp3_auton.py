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


move(10000, 100)
