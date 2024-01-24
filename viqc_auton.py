#config: {leftmotor:4, rightmotor(rev):9, brain_inertial:10, intake:[6(rev),12], hopper:[5, 11(rev)]}

MOMENTUM = 25
ADJUSTMENT = 2;

def move(dist, speed=80, kp=2):
  leftmotor.set_position(0, DEGREES)
  rightmotor.set_position(0, DEGREES)
  brain_inertial.set_rotation(0, DEGREES)
  # speed *= -1
  if dist < 0:
      while leftmotor.position(DEGREES) > dist:
          error = (brain_inertial.rotation(DEGREES)) * kp
          print(leftmotor.position(DEGREES))
          leftmotor.set_velocity(speed*-1 - (error+ADJUSTMENT))
          rightmotor.set_velocity(speed*-1 + (error))
          leftmotor.spin(FORWARD)
          rightmotor.spin(FORWARD)
          if (abs(brain_inertial.rotation()) < 20):
              brain_inertial.set_rotation(0, DEGREES)
  else:
      while leftmotor.position(DEGREES) < dist:
          print(leftmotor.position(DEGREES))
          error = (brain_inertial.rotation()) * kp
          leftmotor.set_velocity(speed + (error+ADJUSTMENT))
          rightmotor.set_velocity(speed - (error))
          leftmotor.spin(FORWARD)
          rightmotor.spin(FORWARD)
          if (abs(brain_inertial.rotation()) < 20):
              brain_inertial.set_rotation(0, DEGREES)
  rightmotor.stop()
  leftmotor.stop()

def gyro_turn(direction, momentum=MOMENTUM, speed=80):
   gyro_10.calibrate(GyroCalibrationType.NORMAL)
   gyro_10.set_rotation(0, DEGREES)
   if direction > gyro_10.rotation():
      while direction - momentum > -1*gyro_10.rotation():
          print(gyro_10.rotation())
          leftmotor.set_velocity(speed, PERCENT)
          rightmotor.set_velocity(speed, PERCENT)
          leftmotor.spin(REVERSE)
          rightmotor.spin(FORWARD)
          wait(20, MSEC)
      leftmotor.stop()
      rightmotor.stop()
   else:
      while direction + momentum < -1*gyro_10.rotation():
          leftmotor.set_velocity(speed, PERCENT)
          rightmotor.set_velocity(speed, PERCENT)
          leftmotor.spin(FORWARD)
          rightmotor.spin(REVERSE)
          wait(20, MSEC)
      leftmotor.stop()
      rightmotor.stop()
intake.set_max_torque(100, PERCENT)
hopper.set_max_torque(100, PERCENT)
intake.set_velocity(100, PERCENT)
hopper.set_velocity(100, PERCENT)
intake.spin(FORWARD)

def run_path():
  move(601)
# move(601)
# gyro_turn(91)
# move(296)
# gyro_turn(-153)
# move(331)

# move(331)
# gyro_turn(-27)
# move(593)
# gyro_turn(-27)
# move(331)
# gyro_turn(-63)
# move(445)
# gyro_turn(135)
# move(421)
# gyro_turn(-135)
# move(445)
# gyro_turn(-168)
# move(756)
# gyro_turn(25)
# move(741)
# gyro_turn(53)
# move(593)
# gyro_turn(180)
# move(296)
# gyro_turn(-90)
# move(889)

# move(296)
# gyro_turn(180)
# move(1186)
# gyro_turn(-90)
# move(741)
# gyro_turn(-153)
# move(663)
# gyro_turn(10)
# move(741)
# gyro_turn(8)
# move(629)
# gyro_turn(-19)
# move(343)
# gyro_turn(-116)
# move(593)

run_path()
