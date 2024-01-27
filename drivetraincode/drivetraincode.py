from vex import *
momentum = 5
def forward(dist):
    gyro_10.set_rotation(0, DEGREES)
    left_drive_smart.spin(FORWARD)
    right_drive_smart.spin(FORWARD)
    left_drive_smart.set_position(0, DEGREES)
    right_drive_smart.set_position(0, DEGREES)
    left_drive_smart.set_velocity(100, PERCENT)
    right_drive_smart.set_velocity(100, PERCENT)
    # u sure u dont wanna reset gyro? It was dot there so i just did it for u.
    while True:
        if (right_drive_smart.position(DEGREES) + left_drive_smart.position(DEGREES))/2 - momentum >= dist:
            break
        rot = gyro_10.rotation()
        print(rot)
        left_drive_smart.set_velocity( 100 - max(0, rot) )
        right_drive_smart.set_velocity( 100 - abs(min(0, rot)) )
        wait(20, MSEC)
    right_drive_smart.stop()
    left_drive_smart.stop()

# motors always spin forward]
def backward(dist):
    gyro_10.set_rotation(0, DEGREES)
    left_drive_smart.spin(FORWARD)
    right_drive_smart.spin(FORWARD)
    left_drive_smart.set_position(0, DEGREES)
    right_drive_smart.set_position(0, DEGREES)
    left_drive_smart.set_velocity(-100, PERCENT)
    right_drive_smart.set_velocity(-100, PERCENT)
    while True:
        if abs(right_drive_smart.position(DEGREES) + left_drive_smart.position(DEGREES))/2 - momentum >= dist:
            break
        rot = gyro_10.rotation()
        left_drive_smart.set_velocity( -100 + abs(min(0, rot)) , PERCENT)
        right_drive_smart.set_velocity( -100 + max(0, rot), PERCENT)
        wait(20, MSEC)
    left_drive_smart.stop()
    right_drive_smart.stop()


def move(dist):
    if dist < 0:
        backward(abs(dist))
    else:
        forward(dist)

def purple():
    hopper.spin_to_position(900, DEGREES)
def green():
    hopper.spin_to_position(1800, DEGREES)
def hdown():
    hopper.spin_to_position(0, DEGREES)
def gyro_turn(direction, speed=50):
    x = 0
    for x in range(6):
        drivetrain.set_turn_velocity((speed/20)*x, PERCENT)
        drivetrain.turn_to_heading(direction, DEGREES)
# Code goes here
