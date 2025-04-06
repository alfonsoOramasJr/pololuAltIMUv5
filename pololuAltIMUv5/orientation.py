import numpy as np
from ahrs.filters import Madgwick

import lps25h, lsm6ds33, lis3mdl

class Orientation:
    def __init__(self):
        self.madgwick_filter = Madgwick()
        self.pressure_interface = lps25h.LPS25H()
        self.magnetometer_interface = lis3mdl.LIS3MDL()
        self.gyroscope_and_acceleromter_interface = lsm6ds33.LSM6DS33()
        self.euler_angles = None
    
    def get_three_degrees_of_freedom_as_numpy_array(self, array_data):
        return np.array([array_data])

    def get_accelerometer_values_as_numpy_array(self):
        return self.get_three_degrees_of_freedom_as_numpy_array(list(self.gyroscope_and_acceleromter_interface.read_accelerometer()))

    def get_gyroscope_values_as_numpy_array(self):
        return self.get_three_degrees_of_freedom_as_numpy_array(list(self.gyroscope_and_acceleromter_interface.read_gyroscope()))

    def get_magnetometer_values_as_numpy_array(self):
        return self.get_three_degrees_of_freedom_as_numpy_array(list(self.magnetometer_interface.read_magnetic_field()))

    def get_roll_pitch_and_yaw(self):
        euler_angles = self.madgwick_filter.updateMARG(
                                            self.get_accelerometer_values_as_numpy_array(),
                                            self.get_gyroscope_values_as_numpy_array(),
                                            self.get_magnetometer_values_as_numpy_array())
        roll, pitch, yaw = euler_angles[0]
        return roll, pitch, yaw
    
    def get_roll_pitch_and_yaw_in_degrees(self):
        roll, pitch, yaw = self.get_roll_pitch_and_yaw()
        roll_degree = np.degrees(roll)
        pitch_degree = np.degrees(pitch)
        yaw_degree = np.degrees(yaw)
        print(f"Roll: {roll_degree:.2f}°, Pitch: {pitch_degree:.2f}°, Yaw: {yaw_degree:.2f}°")
        return roll_degree, pitch_degree, yaw_degree