## MAGNETOMETER SENSOR
from .i2c_interface import I2CInterface

class LIS3MDL:
    """
    The base address is 0x1E, if the SA0 is connected to the VDD_IO, the
    address becomes 0x1F.
    """

    def __init__(self, i2c_bus=1, i2c_address=0x1E):
        self.i2c = I2CInterface(i2c_bus, i2c_address)
        self.WHO_AM_I = 0x0F
        self.CTRL_REG1 = 0x20
        self.CTRL_REG2 = 0x21
        self.CTRL_REG3 = 0x22
        self.CTRL_REG4 = 0x23
        self.OUT_X_L = 0x28
        self.OUT_X_H = 0x29
        self.OUT_Y_L = 0x2A
        self.OUT_Y_H = 0x2B
        self.OUT_Z_L = 0x2C
        self.OUT_Z_H = 0x2D

        self.MAGNETOMETER_SENSITIVITY = 0.14

        self.initialize()
    
    def initialize(self):
        self.i2c.write_byte_data(self.CTRL_REG1, 0x70)  # 80 Hz, high performance
        self.i2c.write_byte_data(self.CTRL_REG2, 0x00)  # ±4 gauss
        self.i2c.write_byte_data(self.CTRL_REG3, 0x00)  # Continuous-conversion mode
        self.i2c.write_byte_data(self.CTRL_REG4, 0x0C)  # Z-axis ultra high performance

    def read_raw_magnetic_field(self):
        east_component = self.read_axis(self.OUT_X_L, self.OUT_X_H)
        north_component = self.read_axis(self.OUT_Y_L, self.OUT_Y_H)
        up_component = self.read_axis(self.OUT_Z_L, self.OUT_Z_H)
        return east_component, north_component, up_component
    
    def read_magnetic_field(self):
        east_magnetic_field, north_magnetic_field, up_magnetic_field = self.read_raw_magnetic_field()
        east_magnetic_field *= self.MAGNETOMETER_SENSITIVITY
        north_magnetic_field *= self.MAGNETOMETER_SENSITIVITY
        up_magnetic_field *= self.MAGNETOMETER_SENSITIVITY

        return east_magnetic_field, north_magnetic_field, up_magnetic_field

    def read_axis(self, low_addr, high_addr):
        low_byte = self.i2c.read_byte_data(low_addr)
        high_byte = self.i2c.read_byte_data(high_addr)
        value = (high_byte << 8) | low_byte
        if value > 32767:
            value -= 65536
        return value