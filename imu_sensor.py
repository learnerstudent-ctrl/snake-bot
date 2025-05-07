#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu
from smbus2 import SMBus
import time
import math

# MPU6050 I2C address
MPU6050_ADDR = 0x68

# MPU6050 Registers
PWR_MGMT_1   = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H  = 0x43

# Initialize I2C bus
bus = SMBus(3)

# Wake up the MPU6050
bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

# Function to read raw data from the sensor
def read_raw_data(addr):
    high = bus.read_byte_data(MPU6050_ADDR, addr)
    low = bus.read_byte_data(MPU6050_ADDR, addr + 1)
    value = (high << 8) | low
    if value > 32767:
        value -= 65536
    return value

# Function to publish IMU data
def imu_publisher():
    # Initialize the ROS node
    rospy.init_node('imu_publisher', anonymous=True)
   
    # Create a publisher for IMU data
    imu_pub = rospy.Publisher('imu_data', Imu, queue_size=10)
   
    # Set loop rate (10 Hz)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        # Read accelerometer and gyroscope data
        acc_x = read_raw_data(ACCEL_XOUT_H) / 16384.0
        acc_y = read_raw_data(ACCEL_XOUT_H + 2) / 16384.0
        acc_z = read_raw_data(ACCEL_XOUT_H + 4) / 16384.0

        gyro_x = read_raw_data(GYRO_XOUT_H) / 131.0
        gyro_y = read_raw_data(GYRO_XOUT_H + 2) / 131.0
        gyro_z = read_raw_data(GYRO_XOUT_H + 4) / 131.0

        # Create and populate an Imu message
        imu_msg = Imu()
       
        # Set accelerometer values
        imu_msg.linear_acceleration.x = acc_x
        imu_msg.linear_acceleration.y = acc_y
        imu_msg.linear_acceleration.z = acc_z
       
        # Set gyroscope values
        imu_msg.angular_velocity.x = gyro_x
        imu_msg.angular_velocity.y = gyro_y
        imu_msg.angular_velocity.z = gyro_z
       
        # Set the orientation as NaN (since we're not calculating orientation here)
        imu_msg.orientation.x = math.nan
        imu_msg.orientation.y = math.nan
        imu_msg.orientation.z = math.nan
        imu_msg.orientation.w = math.nan

        # Publish the IMU data
        imu_pub.publish(imu_msg)

        # Log the data
        rospy.loginfo(f"Accel: X={acc_x:.2f}, Y={acc_y:.2f}, Z={acc_z:.2f} | "
                      f"Gyro: X={gyro_x:.2f}, Y={gyro_y:.2f}, Z={gyro_z:.2f}")

        # Sleep to maintain the loop rate
        rate.sleep()

if __name__ == '__main__':
    try:
        imu_publisher()
    except rospy.ROSInterruptException:
        pass
    finally:
        bus.close()
