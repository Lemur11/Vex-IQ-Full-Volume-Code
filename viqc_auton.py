def forward_distance_degrees_at_speed__25_speed(forward_distance_degrees_at_speed__25_speed__distance, forward_distance_degrees_at_speed__25_speed__speed):
    rightmotor.set_position(0, DEGREES)
    leftmotor.set_position(0, DEGREES)
    brain_inertial.set_rotation(0, DEGREES)
    while (leftmotor.position(DEGREES) + rightmotor.position(DEGREES)) / 2 < forward_distance_degrees_at_speed__25_speed__distance:
        leftmotor.set_velocity((forward_distance_degrees_at_speed__25_speed__speed - brain_inertial.rotation()), PERCENT)
        rightmotor.set_velocity((forward_distance_degrees_at_speed__25_speed__speed + brain_inertial.rotation()), PERCENT)
        leftmotor.spin(FORWARD)
        rightmotor.spin(FORWARD)
        wait(20, MSEC)
    leftmotor.stop()
    rightmotor.stop()

def gyro_turn_heading_velocity_momentum(gyro_turn_heading_velocity_momentum__heading, gyro_turn_heading_velocity_momentum__velocity, gyro_turn_heading_velocity_momentum__momentum):
    gyro_10.set_rotation(0, DEGREES)
    if gyro_turn_heading_velocity_momentum__heading > gyro_10.rotation():
        while gyro_turn_heading_velocity_momentum__heading - gyro_turn_heading_velocity_momentum__momentum > gyro_10.rotation():
            leftmotor.set_velocity(gyro_turn_heading_velocity_momentum__velocity, PERCENT)
            rightmotor.set_velocity(gyro_turn_heading_velocity_momentum__velocity, PERCENT)
            leftmotor.spin(REVERSE)
            rightmotor.spin(FORWARD)
            wait(20, MSEC)
    else:
        while gyro_turn_heading_velocity_momentum__heading - gyro_turn_heading_velocity_momentum__momentum < gyro_10.rotation():
            leftmotor.set_velocity(gyro_turn_heading_velocity_momentum__velocity, PERCENT)
            rightmotor.set_velocity(gyro_turn_heading_velocity_momentum__velocity, PERCENT)
            leftmotor.spin(FORWARD)
            rightmotor.spin(REVERSE)
            wait(20, MSEC)
    leftmotor.stop()
    rightmotor.stop()

def backwards_distance_degrees_at_speed__25_speed(backwards_distance_degrees_at_speed__25_speed__distance, backwards_distance_degrees_at_speed__25_speed__speed):
    rightmotor.set_position(0, DEGREES)
    leftmotor.set_position(0, DEGREES)
    brain_inertial.set_rotation(0, DEGREES)
    while backwards_distance_degrees_at_speed__25_speed__distance < (leftmotor.position(DEGREES) + rightmotor.position(DEGREES)) / 2:
        rightmotor.set_velocity((backwards_distance_degrees_at_speed__25_speed__speed - brain_inertial.rotation()), PERCENT)
        leftmotor.set_velocity((backwards_distance_degrees_at_speed__25_speed__speed + brain_inertial.rotation()), PERCENT)
        leftmotor.spin(REVERSE)
        rightmotor.spin(REVERSE)
        wait(20, MSEC)
    leftmotor.stop()
    rightmotor.stop()

def when_started1():
    intake.set_max_torque(100, PERCENT)
    hopper.set_max_torque(100, PERCENT)
    intake.set_velocity(100, PERCENT)
    hopper.set_velocity(100, PERCENT)
    intake.spin(FORWARD)
    gyro_10.calibrate(GyroCalibrationType.NORMAL)
    gyro_turn_heading_velocity_momentum(90, 50, 5)

when_started1()
