#include <PS2X_lib.h>
#include <Adafruit_PWMServoDriver.h>
#include <Wire.h>

/******************************************************************
 * Cài đặt chân cho thư viện :
 * - Trên mạch Motorshield của VIA Makerbot BANHMI, có header 6 chân
 *   được thiết kế để cắm tay cầm PS2.
 * Sơ đồ chân header và sơ đồ GPIO tương ứng:
 *   MOSI | MISO | GND | 3.3V | CS | CLK
 *    12     13    GND   3.3V   15   14
 ******************************************************************/

#define PS2_DAT 12 // MISO
#define PS2_CMD 13 // MOSI
#define PS2_SEL 15 // SS
#define PS2_CLK 14 // SLK

#define SERVO_1_CHANNEL 2
#define SERVO_2_CHANNEL 3
#define SERVO_3_CHANNEL 4
#define SERVO_4_CHANNEL 5
#define SERVO_5_CHANNEL 6
#define SERVO_6_CHANNEL 7

#define MOTOR_1_CHANNEL_A 8
#define MOTOR_1_CHANNEL_B 9
#define MOTOR_2_CHANNEL_A 10
#define MOTOR_2_CHANNEL_B 11
#define MOTOR_3_CHANNEL_A 12
#define MOTOR_3_CHANNEL_B 13
#define MOTOR_4_CHANNEL_A 14
#define MOTOR_4_CHANNEL_B 15

/******************************************************************
 * Lựa chọn chế độ cho tay cầm PS2 :
 *   - pressures = đọc giá trị analog từ các nút bấm
 *   - rumble    = bật/tắt chế độ rung
 ******************************************************************/
#define pressures false
#define rumble true
int pulse_thuan = 480;
int pulse_stop_thuan = 400;
int pulse_nguoc = 240;
int pulse_stop_nguoc = 300;
int pulse_stop = 330 ; 
int pulse = 150;
int servo_min_1 = 120, servo_max_1 = 350;
unsigned char thabong = 0 , thanongsan=0;
unsigned char dangdichuyen = 0;
PS2X ps2x; // khởi tạo class PS2x
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();// khởi tạo class Servo

//--------------- Khai báo hàm --------------

void kep_nong_san(){
  if (ps2x.Button(PSB_CIRCLE)) {
    Serial.println("Servo số 2 quay thuận (CIRCLE)");
    pwm.setPWM(SERVO_2_CHANNEL, 0, pulse_thuan);
  }
  else if (ps2x.Button(PSB_SQUARE)) {
    Serial.println("Servo số 2 quay ngược (SQUARE)");
    pwm.setPWM(SERVO_2_CHANNEL, 0, pulse_nguoc);
  }
  else {
    pwm.setPWM(SERVO_2_CHANNEL, 0, pulse_stop);
  }
}
//----------------------
void giu_tha_bong() {
  if (ps2x.ButtonPressed(PSB_R1) && thabong==0) {
    thabong = 1;
    Serial.println("Servo quay về 0 độ (R1)");
    for (pulse = servo_max_1; pulse > servo_min_1; pulse--){
      pwm.setPWM(SERVO_1_CHANNEL, 0, pulse);}
  }
  else if (ps2x.ButtonPressed(PSB_R2) && thabong==1) {
    thabong = 0;
    Serial.println("Servo quay về 180 độ (R2)");
    for (pulse = servo_min_1; pulse < servo_max_1; pulse++){
      pwm.setPWM(SERVO_1_CHANNEL, 0, pulse);}
  }
}
//----------------------
void testPS2(){
  if (ps2x.Button(PSB_START))
    Serial.println("Start is being held");
  if (ps2x.Button(PSB_SELECT))
    Serial.println("Select is being held");

  if (ps2x.Button(PSB_PAD_UP))
  {
    Serial.print("Up held this hard: ");
    Serial.println(ps2x.Analog(PSAB_PAD_UP), DEC);
  }
  if (ps2x.Button(PSB_PAD_RIGHT))
  {
    Serial.print("Right held this hard: ");
    Serial.println(ps2x.Analog(PSAB_PAD_RIGHT), DEC);
  }
  if (ps2x.Button(PSB_PAD_LEFT))
  {
    Serial.print("LEFT held this hard: ");
    Serial.println(ps2x.Analog(PSAB_PAD_LEFT), DEC);
  }
  if (ps2x.Button(PSB_PAD_DOWN))
  {
    Serial.print("DOWN held this hard: ");
    Serial.println(ps2x.Analog(PSAB_PAD_DOWN), DEC);
  }

  if (ps2x.NewButtonState())
  {
    if (ps2x.Button(PSB_L3))
      Serial.println("L3 pressed");
    if (ps2x.Button(PSB_R3))
      Serial.println("R3 pressed");
    if (ps2x.Button(PSB_L2))
      Serial.println("L2 pressed");
    if (ps2x.Button(PSB_R2))
      Serial.println("R2 pressed");
    if (ps2x.Button(PSB_TRIANGLE))
      Serial.println("△ pressed");
  }
  if (ps2x.ButtonPressed(PSB_CIRCLE))
    Serial.println("○ just pressed");
  if (ps2x.NewButtonState(PSB_CROSS))
    Serial.println("× just changed");
  if (ps2x.ButtonReleased(PSB_SQUARE))
    Serial.println("□ just released");

  if (ps2x.Button(PSB_L1) || ps2x.Button(PSB_R1))
  {
    Serial.print("Stick Values:");
    Serial.print(ps2x.Analog(PSS_LY));
    Serial.print(",");
    Serial.print(ps2x.Analog(PSS_LX));
    Serial.print(",");
    Serial.print(ps2x.Analog(PSS_RY));
    Serial.print(",");
    Serial.println(ps2x.Analog(PSS_RX));
  }
}
//----------------------
void dichuyen(){
  int JSL = ps2x.Analog(PSS_LY);
  int JSR = ps2x.Analog(PSS_RX);
  unsigned char ratio = 12;

  if (JSL >= 0 && JSL <= 124 && JSR > 125 && JSR < 130) {
    Serial.println("JSL: ");
    Serial.println(JSL);
    dangdichuyen = 1;
    pwm.setPin(MOTOR_1_CHANNEL_A, ratio * (124-JSL));
    pwm.setPin(MOTOR_1_CHANNEL_B, 0);
    pwm.setPin(MOTOR_2_CHANNEL_A, ratio * (124-JSL));
    pwm.setPin(MOTOR_2_CHANNEL_B, 0);
  } 
  else if (JSL >= 130 && JSL <= 255 && JSR > 125 && JSR < 130) {
    Serial.println("JSL: ");
    Serial.println(JSL);
    dangdichuyen = 1;
    pwm.setPin(MOTOR_1_CHANNEL_A, 0);
    pwm.setPin(MOTOR_1_CHANNEL_B, ratio * (JSL-130));
    pwm.setPin(MOTOR_2_CHANNEL_A, 0);
    pwm.setPin(MOTOR_2_CHANNEL_B, ratio * (JSL-130));
  } 

  if (JSR >= 130 && JSR <= 255 && JSL > 125 && JSL < 130) {
    Serial.println("JSR: ");
    Serial.println(JSR);
    dangdichuyen = 1;
    pwm.setPin(MOTOR_1_CHANNEL_A, 7 * (JSR-130));
    pwm.setPin(MOTOR_1_CHANNEL_B, 0);
    pwm.setPin(MOTOR_2_CHANNEL_A, 0);
    pwm.setPin(MOTOR_2_CHANNEL_B, 7 * (JSR-130));
  } 
  else if (JSR >= 0 && JSR <= 124 && JSL > 125 && JSL < 130) {
    Serial.println("JSR: ");
    Serial.println(JSR);
    dangdichuyen = 1;
    pwm.setPin(MOTOR_1_CHANNEL_A, 0);
    pwm.setPin(MOTOR_1_CHANNEL_B, 7 * (124-JSR));
    pwm.setPin(MOTOR_2_CHANNEL_A, 7 * (124-JSR));
    pwm.setPin(MOTOR_2_CHANNEL_B, 0);
  } 
  if (JSL > 124 && JSL < 130 && JSR > 124 && JSR < 130){
    dangdichuyen = 0;
    pwm.setPin(MOTOR_1_CHANNEL_A, 0);
    pwm.setPin(MOTOR_1_CHANNEL_B, 0);
    pwm.setPin(MOTOR_2_CHANNEL_A, 0);
    pwm.setPin(MOTOR_2_CHANNEL_B, 0);
  }
}
//----------------------
void linear() {
  const int MOTOR_3_SPEED = 4096;
  if (ps2x.Button(PSB_L1) && dangdichuyen == 0) {
    pwm.setPin(MOTOR_3_CHANNEL_A, MOTOR_3_SPEED);
    pwm.setPin(MOTOR_3_CHANNEL_B, 0);
    Serial.println("Linear motors 3 extending");
  }
  else if (ps2x.Button(PSB_L2) && dangdichuyen == 0) {
    pwm.setPin(MOTOR_3_CHANNEL_A, 0);
    pwm.setPin(MOTOR_3_CHANNEL_B, MOTOR_3_SPEED);
    Serial.println("Linear motors 3 retracting");
  }
  else {
    pwm.setPin(MOTOR_3_CHANNEL_A, 0);
    pwm.setPin(MOTOR_3_CHANNEL_B, 0);
  }
}
void hang() {
  const int MOTOR_4_SPEED = 4096;
  if (ps2x.Button(PSB_CIRCLE) && dangdichuyen == 0) {
    pwm.setPin(MOTOR_4_CHANNEL_A, 0 );
    pwm.setPin(MOTOR_4_CHANNEL_B, MOTOR_4_SPEED);
    Serial.println("Linear motors 4 extending");
  }
  else {
    pwm.setPin(MOTOR_4_CHANNEL_A, 0);
    pwm.setPin(MOTOR_4_CHANNEL_B, 0);
  }
}

//----------------------
void setup()
{
  Serial.begin(115200);
  Serial.print("Ket noi voi tay cam PS2:");
  pwm.begin();
  pwm.setPWMFreq(50); 
  pwm.setPin(MOTOR_1_CHANNEL_A, 0);
  pwm.setPin(MOTOR_1_CHANNEL_B, 0);
  pwm.setPin(MOTOR_2_CHANNEL_A, 0);
  pwm.setPin(MOTOR_2_CHANNEL_B, 0);
  pwm.setPin(MOTOR_3_CHANNEL_A, 0);
  pwm.setPin(MOTOR_3_CHANNEL_B, 0);
  pwm.setPin(MOTOR_4_CHANNEL_A, 0);
  pwm.setPin(MOTOR_4_CHANNEL_B, 0);

  int error = -1;
  for (int i = 0; i < 5; i++)
  {
    delay(1000);
    error = ps2x.config_gamepad(PS2_CLK, PS2_CMD, PS2_SEL, PS2_DAT, pressures, rumble);
    Serial.print(".");
  }

  switch (error)
  {
  case 0:
    Serial.println(" Ket noi tay cam PS2 thanh cong");
    break;
  case 1:
    Serial.println(" LOI: Khong tim thay tay cam, hay kiem tra day ket noi vơi tay cam ");
    break;
  case 2:
    Serial.println(" LOI: khong gui duoc lenh");
    break;
  case 3:
    Serial.println(" LOI: Khong vao duoc Pressures mode ");
    break;
  }
}
void hang() {
  const int MOTOR_4_SPEED = 4096;
  if (ps2x.Button(PSB_TRIANGLE) && dangdichuyen == 0) {
    pwm.setPin(MOTOR_4_CHANNEL_A, 0 );
    pwm.setPin(MOTOR_4_CHANNEL_B, MOTOR_4_SPEED);
    Serial.println("Linear motors 4 extending");
  }
  else {
    pwm.setPin(MOTOR_4_CHANNEL_A, 0);
    pwm.setPin(MOTOR_4_CHANNEL_B, 0);
  }
}
void loop() {
  ps2x.read_gamepad(false, false);
  dichuyen();
  linear();
  giu_tha_bong();
  kep_nong_san();
  hang();
  delay(20);
}  
