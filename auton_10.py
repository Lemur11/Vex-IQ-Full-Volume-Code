#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
brain_inertial = Inertial()
left_drive_smart = Motor(Ports.PORT4, 1.5, True)
right_drive_smart = Motor(Ports.PORT11, 1.5, False)

drivetrain = SmartDrive(left_drive_smart, right_drive_smart, brain_inertial, 200)
hopper_motor_a = Motor(Ports.PORT5, False)
hopper_motor_b = Motor(Ports.PORT9, True)
hopper = MotorGroup(hopper_motor_a, hopper_motor_b)
intake_motor_a = Motor(Ports.PORT6, True)
intake_motor_b = Motor(Ports.PORT12, False)
intake = MotorGroup(intake_motor_a, intake_motor_b)
touchled_1 = Touchled(Ports.PORT1)



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

calibrate_drivetrain()
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
CORRECT = 20
CC = 10

# Begin project code
drivetrain.set_stopping(HOLD)
def state():
    while True:
        print(left_drive_smart.velocity(PERCENT) - right_drive_smart.velocity(PERCENT), brain_inertial.rotation(DEGREES))
        wait(20, MSEC)

def drive_(amnt, speed):
    brain_inertial.set_rotation(0, DEGREES)
    left_drive_smart.set_position(0, DEGREES)
    right_drive_smart.set_position(0, DEGREES)
    if speed > 0:
        left_drive_smart.spin(FORWARD)
        right_drive_smart.spin(FORWARD)
        while (right_drive_smart.position(DEGREES) + left_drive_smart.position(DEGREES))/2 < amnt:
            rot = brain_inertial.rotation()
            if rot > 0:
                left_drive_smart.set_velocity(speed - CORRECT - CC)
                right_drive_smart.set_velocity(speed)
            elif rot < 0:
                left_drive_smart.set_velocity(speed)
                right_drive_smart.set_velocity(speed - CORRECT + CC)
            wait(20, MSEC)
        left_drive_smart.stop()
        right_drive_smart.stop()
    elif speed < 0:
        left_drive_smart.spin(FORWARD)
        right_drive_smart.spin(FORWARD)
        while abs(right_drive_smart.position(DEGREES) + left_drive_smart.position(DEGREES))/2 < amnt:
            rot = brain_inertial.rotation()
            if rot < 0:
                left_drive_smart.set_velocity(speed - CORRECT*-1 + CC)
                right_drive_smart.set_velocity(speed)
            elif rot > 0:
                left_drive_smart.set_velocity(speed)
                right_drive_smart.set_velocity(speed - CORRECT*-1)
            wait(20, MSEC)
        left_drive_smart.stop()
        right_drive_smart.stop()
def turn_(degrees, speed):
    drivetrain.set_heading(0, DEGREES)
    drivetrain.set_turn_velocity(speed, PERCENT)
    for i in range(2):
        drivetrain.turn_to_heading(degrees)

def lower_hopper():
    hopper.spin_to_position(0, DEGREES)


s = Thread(state)

touchled_1.set_color(Color.BLUE)
while not touchled_1.pressing():
    wait(20, MSEC)
# setup
intake.set_max_torque(100, PERCENT)
hopper.set_max_torque(100, PERCENT)
intake.set_velocity(100, PERCENT)
hopper.set_velocity(100, PERCENT)
intake.spin(FORWARD)

# # 4 cubes in far goal
# drive_(2300, 100)
# turn_(120, 80)
# drive_(300, -100)
# wait(2, SECONDS)
# hopper.spin_for(FORWARD, 1800, DEGREES)
# hopper.set_position(900, DEGREES)
# l = Thread(lower_hopper)

# # put cluster in near goal
# touchled_1.set_color(Color.BLUE)
# while not touchled_1.pressing():
#     wait(20, MSEC)
# drivetrain.set_heading(0, DEGREES)
# drive_(200, 100)
# drivetrain.set_timeout(2, SECONDS)
# drivetrain.turn_to_heading(360 - 35, DEGREES)
# drivetrain.set_timeout(100, SECONDS)
# drive_(800, 100)
# wait(1, SECONDS)
# drivetrain.set_timeout(5, SECONDS)
# turn_(35, 80)
# drivetrain.set_timeout(5, SECONDS) 
# drive_(500, -100)
# wait(3, SECONDS)
# hopper.spin_for(FORWARD, 1800, DEGREES)
# hopper.set_position(900, DEGREES)
# wait(5, SECONDS)
# l = Thread(lower_hopper)

# # hit red 1
# touchled_1.set_color(Color.BLUE)
# while not touchled_1.pressing():
#     wait(20, MSEC)
# drive_(700, 100)

# # hit red 2
# touchled_1.set_color(Color.BLUE)
# while not touchled_1.pressing():
#     wait(20, MSEC)
# drive_(2200, 100)

# put right cubes in right goal
touchled_1.set_color(Color.BLUE)
while not touchled_1.pressing():
    wait(20, MSEC)
drive_(1300, 100)
turn_(-30, 80)
drive_(1400, -100)
hopper.spin_for(FORWARD, 1800, DEGREES)
hopper.set_position(900, DEGREES)
# partial park
wait(3, SECONDS)
drive_(2000, 100)
