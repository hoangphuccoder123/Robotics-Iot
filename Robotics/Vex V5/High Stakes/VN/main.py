#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration
# Import thư viện VEX
from vex import *
import urandom

# Khởi tạo Brain
brain = Brain()

# Cấu hình động cơ Mecanum Drive
front_left_motor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
back_left_motor = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)
front_right_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
back_right_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)

# Cấu hình máy hút
may_hut = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)

# Cấu hình máy kéo (2 motor: PORT6 & PORT8)
may_keo_motor1 = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
may_keo_motor2 = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
may_keo = MotorGroup(may_keo_motor1, may_keo_motor2)  # Nhóm motor kéo

# Cấu hình tay gắp (2 motor: PORT7 & PORT9)
tay_arm_motor1 = Motor(Ports.PORT7, GearSetting.RATIO_18_1, False)
tay_arm_motor2 = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)
tay_arm = MotorGroup(tay_arm_motor1, tay_arm_motor2)  # Nhóm motor tay gắp

# Cấu hình bộ điều khiển (controller)
controller_1 = Controller(PRIMARY)

# Cấu hình servo (clamp)
clamp = DigitalOut(brain.three_wire_port.g)
climp = DigitalOut(brain.three_wire_port.b)

# Hàm khởi tạo số ngẫu nhiên
 
# Khởi tạo giá trị random
initializeRandomSeed()

# Biến để kiểm soát trạng thái robot
remote_control_code_enabled = True

# 🚀 **Hàm điều khiển Mecanum Drive**
def mecanum_drive():
    global remote_control_code_enabled

    while True:
        if remote_control_code_enabled:
            # Lấy giá trị từ joystick
            forward = controller_1.axis3.position()  # Tiến/Lùi
            strafe = controller_1.axis4.position()   # Di chuyển ngang
            turn = controller_1.axis1.position()     # Xoay

            # Công thức điều khiển bánh Mecanum
            front_left_speed = forward + strafe + turn
            front_right_speed = forward - strafe - turn
            back_left_speed = forward - strafe + turn
            back_right_speed = forward + strafe - turn

            # Gửi tốc độ đến động cơ
            front_left_motor.set_velocity(front_left_speed, PERCENT)
            back_left_motor.set_velocity(back_left_speed, PERCENT)
            front_right_motor.set_velocity(front_right_speed, PERCENT)
            back_right_motor.set_velocity(back_right_speed, PERCENT)

            # Quay động cơ
            front_left_motor.spin(FORWARD)
            back_left_motor.spin(FORWARD)
            front_right_motor.spin(FORWARD)
            back_right_motor.spin(FORWARD)

        # Chờ trước khi lặp lại
        wait(20, MSEC)

# 🚀 **Hàm xử lý các nút trên bộ điều khiển**
def controller_buttons():
    global remote_control_code_enabled
    while True:
        if remote_control_code_enabled:
            # Điều khiển máy hút (may_hut) bằng nút L1/L2
            if controller_1.buttonL1.pressing():
                may_hut.set_velocity(100, PERCENT)
                may_hut.spin(FORWARD)
            elif controller_1.buttonL2.pressing():
                may_hut.set_velocity(100, PERCENT)
                may_hut.spin(REVERSE)
            else:
                may_hut.stop()

            # Điều khiển máy kéo (may_keo - MotorGroup) bằng nút R1/R2
            if controller_1.buttonR1.pressing():
                may_keo_motor1.set_max_torque(100,PERCENT)
                may_keo_motor2.set_max_torque(-100,PERCENT)
                may_keo_motor1.set_velocity(250,PERCENT)
                may_keo_motor2.set_velocity(-250,PERCENT)
                may_keo.spin(FORWARD)
            elif controller_1.buttonR2.pressing():
                
                may_keo.spin(REVERSE)
            else:
                may_keo.stop()

            # Điều khiển tay gắp (tay_arm - MotorGroup) bằng nút X/B
            if controller_1.buttonX.pressing():
                tay_arm.set_velocity(100, PERCENT)
                tay_arm.spin(FORWARD)
            elif controller_1.buttonB.pressing():
                tay_arm.set_velocity(100, PERCENT)
                tay_arm.spin(REVERSE)
            else:
                tay_arm.stop()

            # Điều khiển kẹp (clamp) bằng nút Y/A
            if controller_1.buttonY.pressing():
                clamp.set(True)
            elif controller_1.buttonA.pressing():
                clamp.set(False)

            # Điều khiển kẹp phụ (climp) bằng nút Up/Down
            if controller_1.buttonUp.pressing():
                climp.set(True)
            elif controller_1.buttonDown.pressing():
                climp.set(False)

        # Chờ trước khi tiếp tục
        wait(20, MSEC)

# 🚀 **Khởi động các thread điều khiển**
mecanum_drive_thread = Thread(mecanum_drive)
controller_buttons_thread = Thread(controller_buttons)
