from adafruit_servokit import ServoKit
import time
import math

# Initialize PCA9685 with 16 channels
kit = ServoKit(channels=16)

# Define servo channels
servo_vertical_1 = 0  # First vertical servo
servo_horizontal_1 = 1  # First horizontal servo
servo_vertical_2 = 2  # Second vertical servo
servo_horizontal_2 = 3  # Second horizontal servo

# Motion Parameters
amplitude = 45  # Maximum servo movement in degrees
offset = 90     # Neutral position
speed = 2       # Speed of oscillation
shift = math.pi / 2  # 90-degree phase difference

while True:
    print("Moving 4 Servos with 90-degree phase shift...")
    for i in range(360):  # Full cycle movement
        rads = math.radians(i)  # Convert degrees to radians

        # Vertical servos follow a sine wave motion
        kit.servo[servo_vertical_1].angle = offset + amplitude * math.sin(speed * rads)
        kit.servo[servo_vertical_2].angle = offset + amplitude * math.sin(speed * rads + shift)

        # Horizontal servos follow the same sine wave but with a 90-degree phase shift
        kit.servo[servo_horizontal_1].angle = offset + amplitude * math.sin(speed * rads + shift)
        kit.servo[servo_horizontal_2].angle = offset + amplitude * math.sin(speed * rads + 2 * shift)

        time.sleep(0.01)  # Small delay for smooth motion