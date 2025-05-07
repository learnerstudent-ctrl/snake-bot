import RPi.GPIO as GPIO
import time

# Define GPIO pin connected to the IR sensor output
IR_SENSOR_PIN = 17  # Change this to the GPIO pin you are using

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_SENSOR_PIN, GPIO.IN)

try:
    while True:
        if GPIO.input(IR_SENSOR_PIN) == 0:  # Obstacle detected (LOW)
            print("Obstacle detected!")
        else:
            print("No obstacle")
        time.sleep(0.5)  # Small delay to avoid rapid readings

except KeyboardInterrupt:
    print("Exiting Program")
    GPIO.cleanup()  # Reset GPIO settings