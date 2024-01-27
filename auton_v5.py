#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
brain_inertial = Inertial()
intake_motor_a = Motor(Ports.PORT6, True)
intake_motor_b = Motor(Ports.PORT12, False)
intake = MotorGroup(intake_motor_a, intake_motor_b)
hopper_motor_a = Motor(Ports.PORT5, False)
hopper_motor_b = Motor(Ports.PORT11, True)
hopper = MotorGroup(hopper_motor_a, hopper_motor_b)
left_drive_smart = Motor(Ports.PORT1, 1.0, False)
right_drive_smart = Motor(Ports.PORT7, 1.0, True)

drivetrain = SmartDrive(left_drive_smart, right_drive_smart, brain_inertial, 200)



# Make random actually random
def setRandomSeedUsingAccel():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    urandom.seed(int(xaxis + yaxis + zaxis))
    
# Set random seed 
setRandomSeedUsingAccel()

vexcode_initial_drivetrain_calibration_completed = False
def calibrate_drivetrain():
    # Calibrate the Drivetrain Inertial
    global vexcode_initial_drivetrain_calibration_completed
    sleep(200, MSEC)
    brain.screen.print("Calibrating")
    brain.screen.next_row()
    brain.screen.print("Inertial")
    brain_inertial.calibrate()
    while brain_inertial.is_calibrating():
        sleep(25, MSEC)
    vexcode_initial_drivetrain_calibration_completed = True
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)

#endregion VEXcode Generated Robot Configuration
# Begin project code
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
        print(rot)
        # random wait that I think somehow helps
        wait(20, MSEC)
    left_drive_smart.stop()
    right_drive_smart.stop()

def shake(dur, amount=100):
    brain.timer.clear()
    while brain.timer.time(SECONDS) < dur:
        drivetrain.set_drive_velocity(100, PERCENT)
        drivetrain.drive_for(FORWARD, amount, MM)
        drivetrain.drive_for(REVERSE, amount, MM)
        wait(20, MSEC)

def move(dist):
    # reset gyro
    gyro_10.set_rotation(0, DEGREES)
    if dist < 0:
        forward(abs(dist))
    else:
        backward(dist)

def purple():
    hopper.spin_to_position(900, DEGREES)
    
def green():
    hopper.spin_to_position(1800, DEGREES)

VIB_T = 5
def vibrate_hopper():
    hopper.spin(FORWARD)
    wait(VIB_T, SECONDS)
    hopper.stop()
    hopper.set_position(1800, DEGREES)  


def hdown():
    hopper.spin_to_position(0, DEGREES)
    
def gyro_turn(direction, speed=100):
    drivetrain.set_rotation(0, DEGREES)
    for x in range(5):  # changed 6 to 5 because (5-5) is just a stop
        drivetrain.set_turn_velocity((speed/5)*(5-x), PERCENT)
        drivetrain.turn_to_rotation(direction, DEGREES)
        print(drivetrain.rotation())
        wait(20, MSEC)

def check():
    if intake.velocity(RPM) < 20:
        intake.set_velocity(-100, PERCENT)
        wait(1, SECONDS)
        intake.set_velocity(100, PERCENT)

def stop_if_stall():
    while True:
        if drivetrain.velocity(RPM) < 10:
            drivetrain.stop()
            break

# Code goes here
intake.set_max_torque(100, PERCENT)
intake.set_velocity(100, PERCENT)
hopper.set_max_torque(100, PERCENT)
hopper.set_velocity(100, PERCENT)
intake.spin(FORWARD)
drivetrain.set_stopping(BRAKE)
# 540 degrees per mm
# first part
move(1622)
# check thread
ws2 = Thread(check)
# continue code
gyro_turn(140)
move(1153)
shake(6)
purple()
gyro_turn(-170)
drivetrain.set_timeout(5, SECONDS)
left_drive_smart.set_velocity(90, PERCENT)
right_drive_smart.set_velocity(100, PERCENT)
left_drive_smart.spin_for(REVERSE, -700, DEGREES)
right_drive_smart.spin_for(REVERSE, -700, DEGREES)
green()
ws3 = Thread(vibrate_hopper)
shake(10, amount=10)
touchled_8.set_brightness(100)
touchled_8.set_color(Color.BLUE)
# start second section
move(3000)
