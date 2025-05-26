#region VEXcode Generated Robot Configuration
from vex import *
import random
import time

# Brain should be defined by default
brain = Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)
left_motor_a = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)    
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain = DriveTrain(
    left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)
highintake = Motor(Ports.PORT19, GearSetting.RATIO_18_1, False)
hand_arm = Motor(Ports.PORT18, GearSetting.RATIO_18_1, False)
intake_ring = Motor(Ports.PORT16, GearSetting.RATIO_18_1, False)
climp = DigitalOut(brain.three_wire_port.a)
break_ring = DigitalOut(brain.three_wire_port.b)
# wait for rotation sensor to fully initialize
wait(30, MSEC)

# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    seed_value = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    random.seed(int(seed_value))
      
# Set random seed 
initializeRandomSeed()

def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration

# Initialize global status variables
highintake_status = True
hand_arm_status = True
intake_ring_status = True
climp_status = True
drivetrain_l_needs_to_be_stopped_controller_1 = False
drivetrain_r_needs_to_be_stopped_controller_1 = False
break_ring_status = True
controller_1_left_shoulder_control_motors_stopped = True
controller_1_right_shoulder_control_motors_stopped = True

remote_control_code_enabled = True

def opcontrol():
    global drivetrain_l_needs_to_be_stopped_controller_1, drivetrain_r_needs_to_be_stopped_controller_1
    global highintake_status, hand_arm_status, intake_ring_status, climp_status, break_ring_status
    global controller_1_left_shoulder_control_motors_stopped, controller_1_right_shoulder_control_motors_stopped
    
    # Loop inside driver control - managed by competition framework
    while True:
        if remote_control_code_enabled:
            drivetrain_left_side_speed = controller_1.axis3.position() + controller_1.axis1.position()
            drivetrain_right_side_speed = controller_1.axis3.position() - controller_1.axis1.position()
            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
                if drivetrain_l_needs_to_be_stopped_controller_1:
                    left_drive_smart.stop()
                    drivetrain_l_needs_to_be_stopped_controller_1 = False
            else:
                drivetrain_l_needs_to_be_stopped_controller_1 = True
            if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
                if drivetrain_r_needs_to_be_stopped_controller_1:
                    right_drive_smart.stop()
                    drivetrain_r_needs_to_be_stopped_controller_1 = False
            else:
                drivetrain_r_needs_to_be_stopped_controller_1 = True
            if drivetrain_l_needs_to_be_stopped_controller_1:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            if drivetrain_r_needs_to_be_stopped_controller_1:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
                
            # Hand arm position control
            if controller_1.buttonB.pressing():
                hand_arm.spin_to_position(20, DEGREES, 50, PERCENT)
                
            # Intake control
            if controller_1.buttonL1.pressing():
                intake_ring.set_velocity(100, PERCENT)
                highintake.set_velocity(100, PERCENT)
                highintake.set_max_torque(250, PERCENT)
                intake_ring.spin(REVERSE)
                highintake.spin(FORWARD)
                controller_1_left_shoulder_control_motors_stopped = False
            elif controller_1.buttonL2.pressing():
                intake_ring.set_velocity(100, PERCENT)
                highintake.set_velocity(100, PERCENT)
                highintake.set_max_torque(250, PERCENT)
                intake_ring.spin(FORWARD)
                highintake.spin(REVERSE)
                controller_1_left_shoulder_control_motors_stopped = False
            elif not controller_1_left_shoulder_control_motors_stopped:
                highintake.stop()
                intake_ring.stop()
                controller_1_left_shoulder_control_motors_stopped = True
                
            # Hand arm manual control
            if controller_1.buttonR1.pressing():
                hand_arm.set_max_torque(250, PERCENT)
                hand_arm.set_velocity(100, PERCENT)
                hand_arm.spin(FORWARD)
                controller_1_right_shoulder_control_motors_stopped = False
            elif controller_1.buttonR2.pressing():
                hand_arm.set_max_torque(250, PERCENT)
                hand_arm.set_velocity(100, PERCENT)
                hand_arm.spin(REVERSE)
                controller_1_right_shoulder_control_motors_stopped = False
            elif not controller_1_right_shoulder_control_motors_stopped:
                hand_arm.stop()
                controller_1_right_shoulder_control_motors_stopped = True
                
            # Climp control
            if controller_1.buttonLeft.pressing():
                climp.set(True)
            elif controller_1.buttonRight.pressing():  # Changed from B to Down to avoid conflict
                climp.set(False)
                
            # Break ring control
            if controller_1.buttonUp.pressing():
                break_ring.set(True)
            elif controller_1.buttonDown.pressing():
                break_ring.set(False)
                
            # Hand arm precise movements
            # Hand arm precise movements
            if controller_1.buttonY.pressing():
                hand_arm.set_velocity(10, PERCENT)  # Set velocity to 10%
                hand_arm.spin_to_position(-35, DEGREES, wait=False)  # Move to 35 degrees
                controller_1_right_shoulder_control_motors_stopped = False
            elif controller_1.buttonA.pressing():
                hand_arm.set_velocity(10, PERCENT)  # Set velocity to 10%
                hand_arm.spin_to_position(35, DEGREES, wait=False)  # Move to 35 degrees
                controller_1_right_shoulder_control_motors_stopped = False
                
        wait(20, MSEC)

def open_climp():
    global climp_status
    climp.set(True)
    climp_status = True
def close_climp():
    global climp_status
    climp.set(False)
    climp_status = False

def auto_high_intake(open_time=1.5, close_time=1.5):
    highintake.set_velocity(100, PERCENT)
    highintake.set_max_torque(250, PERCENT)
    highintake.spin(FORWARD)
    wait(open_time, SECONDS)
    highintake.stop()
    wait(close_time, SECONDS)
def intake_ring_auto(open_time=1.5, close_time=1.5):
    intake_ring.set_velocity(100, PERCENT)
    intake_ring.set_max_torque(250, PERCENT)
    intake_ring.spin(FORWARD)
    wait(open_time, SECONDS)
    intake_ring.stop()
    wait(close_time, SECONDS)
def close_hand(open_time=1.0, close_time=1.0):
    hand_arm.set_max_torque(60, PERCENT)
    hand_arm.set_velocity(60, PERCENT)
    hand_arm.spin(FORWARD)
    wait(open_time, SECONDS)
    hand_arm.stop()
    wait(close_time, SECONDS)

def open_hand(open_time=1.0, close_time=1.0):
    hand_arm.set_max_torque(60, PERCENT)
    hand_arm.set_velocity(60, PERCENT)
    hand_arm.spin(REVERSE)
    wait(open_time, SECONDS)
    hand_arm.stop()
    wait(close_time, SECONDS)
def auto_break_ring(open_time=1.0, close_time=1.0):
    break_ring.set(True)
    wait(open_time, SECONDS)
    break_ring.set(False)
    wait(close_time, SECONDS)
def dont_break_ring(open_time=1.0, close_time=1.0):
    break_ring.set(False)
    wait(open_time, SECONDS)
    break_ring.set(True)
    wait(close_time, SECONDS)
def comboo1(open_time=3.0, close_time=3.0):
    # Create threads to run both intake functions simultaneously
    def run_intake_ring():
        intake_ring.set_velocity(100, PERCENT)
        intake_ring.set_max_torque(250, PERCENT)
        intake_ring.spin(REVERSE)
        wait(open_time, SECONDS)
        intake_ring.stop()
    def run_high_intake():
        highintake.set_velocity(100, PERCENT)
        highintake.set_max_torque(250, PERCENT)
        highintake.spin(FORWARD)
        wait(open_time, SECONDS)
        highintake.stop()
    
    # Start both operations in parallel
    intake_ring_thread = Thread(run_intake_ring)
    high_intake_thread = Thread(run_high_intake)
    
    # Wait for both operations to complete
    wait(open_time, SECONDS)
    
    # Wait for the close_time
    wait(close_time, SECONDS)
# ...existing code...
def drivetrain_auto():
    dont_break_ring()
    open_hand()
    close_hand()
    open_climp()
def go_auto():
    auton_task_2 = Thread(drivetrain_auto)
    while (competition.is_autonomous() and competition.is_enabled()):
        wait(10, MSEC)
    auton_task_2.stop()
def go_driver():
    driver_control_task = Thread(opcontrol)
    while (competition.is_driver_control() and competition.is_enabled()):
        wait(10, MSEC)
    driver_control_task.stop()

competition = Competition(go_driver, go_auto)
# rc_auto_loop_thread_controller_1 = Thread(opcontrol)

 