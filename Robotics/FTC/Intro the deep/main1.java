// Put initialization blocks here.
speed = 0.5;
MOTOR_SETTINGS();
servomoi1.scaleRange(0.5, 0.7);
waitForStart();
if (opModeIsActive()) {
  // Put run blocks here.
  while (opModeIsActive()) {
    MECANUM_DRIVE();
    Arm2();
    KHOP_NOI();
    Holding_elements();
    specimens_holding();
    specimens_holding2();
    truc_quay_tay_gap();
    sppeciemns_holding_3();
    Viper3();
  }
}
}

/**
* Describe this function...
*/
private void truc_quay_tay_gap() {
if (gamepad2.dpad_right) {
  servomoi2.setPower(0.5);
} else if (gamepad2.dpad_left) {
  servomoi2.setPower(-0.5);
} else {
  servomoi2.setPower(gamepad2.touchpad_finger_2_y);
}
telemetry.addData("Servo Power", servomoi2.getPower());
telemetry.update();
}

/**
* Describe this function...
*/
private void MECANUM_DRIVE() {
float forwardBack;
float strafe;
float turn;
double leftFrontPower;
double rightFrontPower;
double leftBackPower;
double rightBackPower;

// Determining movement based on gamepad inputs
Speed_changing();
forwardBack = -gamepad1.left_stick_y;
strafe = gamepad1.right_stick_x;
turn = -gamepad1.right_stick_y;
leftFrontPower = (forwardBack + strafe + turn) * speed;
rightFrontPower = ((forwardBack - strafe) - turn) * speed;
leftBackPower = ((forwardBack - strafe) + turn) * speed;
rightBackPower = ((forwardBack + strafe) - turn) * speed;
// Setting Motor Power
leftFront.setPower(leftFrontPower);
rightFront.setPower(rightFrontPower);
leftBack.setPower(leftBackPower);
rightBack.setPower(rightBackPower);
}

/**
* Describe this function...
*/
private void sppeciemns_holding_3() {
if (opModeIsActive()) {
  servomoi1.setPosition(gamepad2.right_trigger);
  servomoi1.setDirection(Servo.Direction.REVERSE);
}
}

/**
* Describe this function...
*/
private void KHOP_NOI() {
if (opModeIsActive()) {
  if (gamepad1.dpad_right) {
    servo3.setPower(0.5);
  } else if (gamepad1.dpad_left) {
    servo3.setPower(-0.5);
  } else {
    servo3.setPower(gamepad1.touchpad_finger_2_y);
  }
  telemetry.addData("Servo Power", servo3.getPower());
  telemetry.update();
}
}

/**
* Describe this function...
*/
private void specimens_holding() {
if (opModeIsActive()) {
  servo0.setPosition(gamepad1.right_trigger);
  servo0.setDirection(Servo.Direction.FORWARD);
}
}

/**
* Describe this function...
*/
private void specimens_holding2() {
if (opModeIsActive()) {
  servo2.setPosition(gamepad1.right_trigger);
  servo2.setDirection(Servo.Direction.REVERSE);
}
}

/**
* Describe this function...
*/
private void Viper3() {
if (opModeIsActive()) {
  if (gamepad2.left_bumper) {
    Viper.setZeroPowerBehavior(DcMotor.ZeroPowerBehavior.BRAKE);
Viper.setDirection(DcMotor.Direction.REVERSE);
    Viper2.setZeroPowerBehavior(DcMotor.ZeroPowerBehavior.BRAKE);
    Viper2.setDirection(DcMotor.Direction.FORWARD);
    Viper2.setPower(1);
    Viper.setPower(1);
  } else {
    if (gamepad2.right_bumper) {
      Viper.setZeroPowerBehavior(DcMotor.ZeroPowerBehavior.BRAKE);
      Viper.setDirection(DcMotor.Direction.FORWARD);
      Viper.setPower(1);
      Viper2.setZeroPowerBehavior(DcMotor.ZeroPowerBehavior.BRAKE);
      Viper2.setDirection(DcMotor.Direction.REVERSE);
      Viper2.setPower(1);
    } else {
      Viper.setPower(0);
      Viper.setPower(0);
      Viper2.setPower(0);
      Viper2.setPower(0);
    }
  }
} else {
  Viper2.setPower(0);
  Viper2.setPower(0);
  Viper.setPower(0);
  Viper.setPower(0);
}
}

/**
* Describe this function...
*/
private void Arm2() {
if (opModeIsActive()) {
  if (gamepad1.right_bumper) {
    Arm.setZeroPowerBehavior(DcMotor.ZeroPowerBehavior.BRAKE);
    Arm.setDirection(DcMotor.Direction.FORWARD);
    Arm.setPower(0.8);
  } else {
    if (gamepad1.left_bumper) {
      Arm.setZeroPowerBehavior(DcMotor.ZeroPowerBehavior.BRAKE);
      Arm.setDirection(DcMotor.Direction.REVERSE);
      Arm.setPower(0.8);
    } else {
      Arm.setPower(0);
      Arm.setPower(0);
    }
  }
} else {
  Arm.setPower(0);
  Arm.setPower(0);
}
}

/**
* Describe this function...
*/
private void Holding_elements() {
if (opModeIsActive()) {
  if (gamepad1.b) {
    servo1.setPower(0.5);
  } else if (gamepad1.x) {
    servo1.setPower(-0.5);
  } else {
    servo1.setPower(gamepad1.touchpad_finger_2_y);
  }
  telemetry.addData("Servo Power", servo1.getPower());
  telemetry.update();
}
}
}