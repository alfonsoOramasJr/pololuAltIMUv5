## GYROSCOPE AND ACCELEROMETER SENSOR
from i2c_interface import I2CInterface
import struct

class LSM6DS33:
    def __init__(self, i2c_bus=1, i2c_address=0x6B):
        self.i2c = I2CInterface(i2c_bus, i2c_address)
        self.CTRL1_XL = 0x10  # Accelerometer control register
        self.CTRL2_G = 0x11  # Gyroscope control register
        self.OUTX_L_G = 0x22  # Gyroscope output registers
        self.OUTX_L_XL = 0x28  # Accelerometer output registers
        self.GYROSCOPE_SENSITIVITY = 8.75 / 1000
        self.initialize()

    def initialize(self):
        # Initialize accelerometer to 208 Hz, 2g, and 400 Hz filter
        self.i2c.write_byte_data(self.CTRL1_XL, 0x60)
        # Initialize gyroscope to 208 Hz, 250 dps
        self.i2c.write_byte_data(self.CTRL2_G, 0x60)

    def read_raw_gyroscope(self):
        gravity_x_axis_low, gravity_x_axis_high, gravity_y_axis_low, gravity_y_axis_high, gravity_z_axis_low, gravity_z_axis_high = self.i2c.read_i2c_block_data(self.OUTX_L_G, 6)
        gravity_x_axis = struct.unpack('<h', bytes([gravity_x_axis_low, gravity_x_axis_high]))[0]
        gravity_y_axis = struct.unpack('<h', bytes([gravity_y_axis_low, gravity_y_axis_high]))[0]
        gravity_z_axis = struct.unpack('<h', bytes([gravity_z_axis_low, gravity_z_axis_high]))[0]
        return gravity_x_axis, gravity_y_axis, gravity_z_axis
    
    def read_gyroscope(self):
        """
        Converts the raw gyroscope data into degrees per second using the
        full scale range (default value of +- 245 degrees), and the sensitivity
        value associated with it in the datasheet for the LSM6DS33.

        The formula is as follows,
            Gyroscope = (raw gyroscope data) * (sensitivity value / 1000[milli])
        """
        
        gravity_x_axis, gravity_y_axis, gravity_z_axis = self.read_raw_gyroscope()
        gravity_x_axis *= self.GYROSCOPE_SENSITIVITY
        gravity_y_axis *= self.GYROSCOPE_SENSITIVITY
        gravity_z_axis *= self.GYROSCOPE_SENSITIVITY

        return gravity_x_axis, gravity_y_axis, gravity_z_axis

    def read_raw_accelerometer(self):
        ax_l, ax_h, ay_l, ay_h, az_l, az_h = self.i2c.read_i2c_block_data(self.OUTX_L_XL, 6)
        ax = struct.unpack('<h', bytes([ax_l, ax_h]))[0]
        ay = struct.unpack('<h', bytes([ay_l, ay_h]))[0]
        az = struct.unpack('<h', bytes([az_l, az_h]))[0]
        return ax, ay, az

    def isolate_gravity(self, accelerometer_reading, CONSTANT_SMOOTHING, current_gravity):
        self.current_gravity = CONSTANT_SMOOTHING * current_gravity + (1 - CONSTANT_SMOOTHING) * accelerometer_reading
        return self.current_gravity

    def get_linear_acceleration(accelerometer_reading, isolated_gravity):
        return accelerometer_reading - isolated_gravity