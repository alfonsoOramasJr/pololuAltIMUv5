## PRESSURE AND TEMPERATURE SENSOR

from i2c_interface import I2CInterface
import struct

class LPS25H:
    def __init__(self, i2c_bus=1, i2c_address=0x5D):
        self.i2c = I2CInterface(i2c_bus, i2c_address)
        self.WHO_AM_I_REG_ADDR = 0x0F
        self.CTRL_REG1_ADDR = 0x20
        self.CTRL_REG2_ADDR = 0x21
        self.RES_CONF_ADDR = 0x10
        self.FIFO_CTRL_ADDR = 0x2E
        self.CTRL_REG2_ADDR = 0x21
        self.PRESS_OUT_XL = 0x28
        self.PRESS_OUT_L = 0x29
        self.PRESS_OUT_H = 0x2A
        self.TEMP_OUT_L = 0x2B
        self.TEMP_OUT_H = 0x2C
        
        self.sea_level_pressure_pascals = 101325
        self.lapse_rate = 0.0065
        self.universal_gas_constant = 8.3144598
        self.gravitational_acceleration_in_meters_per_second_squared = 9.80665
        self.molar_mass_of_air = 0.0289644

        self.set_power_mode(True)

    def check_sensor(self):
        return self.i2c.read_byte_data(self.WHO_AM_I_REG_ADDR) == 0xBD

    def set_power_mode(self, power_on):
        mode = 0x90 if power_on else 0x00
        self.i2c.write_byte_data(self.CTRL_REG1_ADDR, mode)

    def read_pressure(self):
        data = [self.i2c.read_byte_data(reg) for reg in [self.PRESS_OUT_XL, self.PRESS_OUT_L, self.PRESS_OUT_H]]
        pressure_raw = data[2] << 16 | data[1] << 8 | data[0]
        if pressure_raw & 0x800000:
            pressure_raw -= 0x1000000
        return (pressure_raw / 4096.0) * 100

    def read_temperature_in_kelvin(self):
        l, h = self.i2c.read_byte_data(self.TEMP_OUT_L), self.i2c.read_byte_data(self.TEMP_OUT_H)
        temp_raw = struct.unpack('<h', bytes([l, h]))[0]
        return (42.5 + temp_raw / 480.0) + 273.15

    def get_altitude_in_meters(self):
        temperature_over_lapse_rate = self.read_temperature_in_kelvin() / self.lapse_rate
        pressure_refered_to_sea_level = self.read_pressure() / self.sea_level_pressure_pascals
        gas_constant_per_lapse_rate = self.universal_gas_constant * self.lapse_rate
        gravity_per_molar_mass = self.gravitational_acceleration_in_meters_per_second_squared * self.molar_mass_of_air

        return temperature_over_lapse_rate * (1 - (pressure_refered_to_sea_level) ** ((gas_constant_per_lapse_rate)/(gravity_per_molar_mass)))