from vex import *
momentum = 5
def forward(dist):
    # start motors
    left_drive_smart.spin(FORWARD)
    right_drive_smart.spin(FORWARD)
    # set reset motor encoders
    left_drive_smart.set_position(0, DEGREES)
    right_drive_smart.set_position(0, DEGREES)
    # set velocity to max
    left_drive_smart.set_velocity(100, PERCENT)
    right_drive_smart.set_velocity(100, PERCENT)
    # drive loop
    while True:
        if (right_drive_smart.position(DEGREES) + left_drive_smart.position(DEGREES))/2 - momentum >= dist:  # check if dist reached
            break
        # decrease one motor if drifting
        rot = gyro_10.rotation()
        left_drive_smart.set_velocity( 100 - max(0, rot) )
        right_drive_smart.set_velocity( 100 - abs(min(0, rot)) )
        # random wait that I think somehow helps
        wait(20, MSEC)
    right_drive_smart.stop()
    left_drive_smart.stop()

# motors always spin forward
def backward(dist):
    # start motors
    left_drive_smart.spin(FORWARD)
    right_drive_smart.spin(FORWARD)
    # set reset motor encoders
    left_drive_smart.set_position(0, DEGREES)
    right_drive_smart.set_position(0, DEGREES)
    # set velocity to max
    left_drive_smart.set_velocity(-100, PERCENT)
    right_drive_smart.set_velocity(-100, PERCENT)
    # drive loop
    while True:
        if abs(right_drive_smart.position(DEGREES) + left_drive_smart.position(DEGREES))/2 - momentum >= dist:
            break
        # decrease one motor if drifting
        rot = gyro_10.rotation()
        left_drive_smart.set_velocity( -100 + abs(min(0, rot)) , PERCENT)
        right_drive_smart.set_velocity( -100 + max(0, rot), PERCENT)
        # random wait that I think somehow helps
        wait(20, MSEC)
    left_drive_smart.stop()
    right_drive_smart.stop()


def move(dist):
    # reset gyro
    gyro_10.set_rotation(0, DEGREES)
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
    for x in range(5):  # changed 6 to 5 because (5-5) is just a stop
        drivetrain.set_turn_velocity((speed/20)*(5-x), PERCENT)
        drivetrain.turn_to_heading(direction, DEGREES)
# Code goes here
