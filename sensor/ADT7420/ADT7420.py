########################################################################################################################
# sudo systemctl enable pigpiod
# sudo systemctl start pigpiod
# sudo pigpiod
# sudo systemctl disable pigpiod
# sudo systemctl stop pigpiod
#
# i2cdetect -y 1
# i2cget -y 1 0x49 0 b
########################################################################################################################

########################################################################################################################
# Datasheet: ADT7420 ±0.25°C Accurate, 16-Bit Digital I2C Temperature Sensor
########################################################################################################################

# ----------------------------------------------------------------------------------------------------------------------
# Table 6. ADT7420 Registers
# ----------------------------------------------------------------------------------------------------------------------
# Register  | Description                               | Power-On
# Address   |                                           | Default
# ----------|-------------------------------------------|---------------------------------------------------------------
# 0x00      | Temperature value most significant byte   | 0x00
# 0x01      | Temperature value least significant byte  | 0x00
# 0x02      | Status                                    | 0x00
# 0x03      | Configuration                             | 0x00
# 0x04      | T_HIGH setpoint most significant byte     | 0x20 (64 deg C)
# 0x05      | T_HIGH setpoint least significant byte    | 0x00 (64 deg C)
# 0x06      | T_LOW setpoint most significant byte      | 0x05 (10 deg C)
# 0x07      | T_LOW setpoint least significant byte     | 0x00 (10 deg C)
# 0x08      | T_CRIT setpoint most significant byte     | 0x49 (147 deg C)
# 0x09      | T_CRIT setpoint least significant byte    | 0x80 (147 deg C)
# 0x0A      | T_HYST setpoint                           | 0x00 (5 deg C)
# 0x0B      | ID                                        | 0xCB
# 0x0C      | Reserved                                  | 0xXX
# 0x0D      | Reserved                                  | 0xXX
# 0x0E      | Reserved                                  | 0xXX
# 0x0F      | Software reset                            | 0xXX
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Table 7. Address Pointer Register
# ----------------------------------------------------------------------------------------------------------------------
# P7    | P6    | P5    | P4    | P3    | P2    | P1    | P0
# ------|-------|-------|-------|-------|-------|-------|---------------------------------------------------------------
# ADD7  | ADD6  | ADD5  | ADD4  | ADD3  | ADD2  | ADD1  | ADD0
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Table 8. Temperature Value MSB Register (Register Address 0x00)
# ----------------------------------------------------------------------------------------------------------------------
# Bit       | Default   | Type      |   Name    | Description
#           | Value     |           |           |
# ----------|-----------|-----------|-----------|-----------------------------------------------------------------------
# [14:8]    | 0000000   | R         | Temp      | Temperature value in twos complement format
# ----------|-----------|-----------|-----------|-----------------------------------------------------------------------
# 15        | 0         | R         | Sign      | Sign bit, indicates if the temperature value is negative or positive
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Table 9. Temperature Value LSB Register (Register Address 0x01)
# ----------------------------------------------------------------------------------------------------------------------
# Bit       | Default   | Type      |   Name    | Description
#           | Value     |           |           |
# ----------|-----------|-----------|-----------|-----------------------------------------------------------------------
# 0         | 0         | R         | T_LOW     | flag/LSB0 Flags a T_LOW event if the configuration register, Register
#           |           |           |           | Address 0x03[7] = 0 (13-bit resolution). When the temperature value
#           |           |           |           | is below T_LOW, this bit it set to 1. Contains the Least Significant
#           |           |           |           | Bit 0 of the 15-bit temperature value if the configuration register,
#           |           |           |           | Register Address 0x03[7] = 1 (16-bit resolution).
# ----------|-----------|-----------|-----------|-----------------------------------------------------------------------
# 1         | 0         | R         | T_HIGH    | flag/LSB1 Flags a T_HIGH event if the configuration register, Register
#           |           |           |           | Address 0x03[7] = 0 (13-bit resolution). When the temperature value
#           |           |           |           | is above T_HIGH, this bit it set to 1. Contains the Least Significant
#           |           |           |           | Bit 1 of the 15-bit temperature value if the configuration register,
#           |           |           |           | Register Address 0x03[7] = 1 (16-bit resolution).
# ----------|-----------|-----------|-----------|-----------------------------------------------------------------------
# 2         | 0         | R         | T_CRIT    | flag/LSB2 Flags a T_CRIT event if the configuration register, Register
#           |           |           |           | Address 0x03[7] = 0 (13-bit resolution). When the temperature value
#           |           |           |           | exceeds T_CRIT, this bit it set to 1. Contains the Least Significant
#           |           |           |           | Bit 2 of the 15-bit temperature value if the configuration register,
#           |           |           |           | Register Address 0x03[7] = 1 (16-bit resolution).
# ----------|-----------|-----------|-----------|-----------------------------------------------------------------------
# [7:3]     | 00000     | R         | Temp      | Temperature value in twos complement format.
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Table 10. Status Register (Register Address 0x02)
# ----------------------------------------------------------------------------------------------------------------------
# Bit       | Default   | Type      |   Name    | Description
#           | Value     |           |           |
# ----------|-----------|-----------|-----------|-----------------------------------------------------------------------
# [3:0]     | 0000      | R         | Unused    | Reads back 0.
# ----------|-----------|-----------|-----------|-----------------------------------------------------------------------
# 4         | 0         | R         | T_LOW     | This bit is set to 1 when the temperature goes below the T_LOW
#           |           |           |           | temperature limit. The bit clears to 0 when the status register is
#           |           |           |           | read and/or when the temperature measured goes back above the limit
#           |           |           |           | set in the setpoint T_LOW + T_HYST registers.
# ----------|-----------|-----------|-----------|-----------------------------------------------------------------------
# 5         | 0         | R         | T_HIGH    | This bit is set to 1 when the temperature goes above the T_HIGH
#           |           |           |           | temperature limit. The bit clears to 0 when the status register is
#           |           |           |           | read and/or when the temperature measured goes back below the limit
#           |           |           |           | set in the setpoint T_HIGH − T_HYST registers.
# ----------|-----------|-----------|-----------|-----------------------------------------------------------------------
# 6         | 0         | R         | T_CRIT    | This bit is set to 1 when the temperature goes above the T_CRIT
#           |           |           |           | temperature limit. This bit clears to 0 when the status register is
#           |           |           |           | read and/or when the temperature measured goes back below the limit
#           |           |           |           | set in the setpoint T_CRIT − T_HYST registers.
# ----------|-----------|-----------|-----------|-----------------------------------------------------------------------
# 7         | 1         | R         | ^RDY      | This bit goes low when the temperature conversion result is written
#           |           |           |           | into the temperature value register. It is reset to 1 when the
#           |           |           |           | temperature value register is read. In one-shot and 1 SPS modes,
#           |           |           |           | this bit is reset after a write to the operation mode bits.
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Table 11. Configuration Register (Register Address 0x03)
# ----------------------------------------------------------------------------------------------------------------------
# Bit       | Default   |  Type     | Name          | Description
#           | Value     |           |               |
# ----------|-----------|-----------|---------------|-------------------------------------------------------------------
# [1:0]     | 00        | R/^w      | Fault         | These two bits set the number of undertemperature/overtemperature
#           |           |           | queue         | faults that can occur before setting the INT and CT pins. This
#           |           |           |               | helps to avoid false triggering due to temperature noise.
#           |           |           |               |   00 = 1 fault (default).
#           |           |           |               |   01 = 2 faults.
#           |           |           |               |   10 = 3 faults.
#           |           |           |               |   11 = 4 faults.
# ----------|-----------|-----------|---------------|-------------------------------------------------------------------
# 2         | 0         | R/^w      | CT pin        | This bit selects the output polarity of the CT pin.
#           |           |           | polarity      |   0 = active low.
#           |           |           |               |   1 = active high.
# ----------|-----------|-----------|---------------|-------------------------------------------------------------------
# 3         | 0         | R/^w      | INT pin       | This bit selects the output polarity of the INT pin.
#           |           |           | polarity      |   0 = active low.
#           |           |           |               |   1 = active high.
# ----------|-----------|-----------|---------------|-------------------------------------------------------------------
# 4         | 0         | R/^w      | INT/CT        | This bit selects between comparator mode and interrupt mode.
#           |           |           | mode          |   0 = interrupt mode
#           |           |           |               |   1 = comparator mode
# ----------|-----------|-----------|---------------|-------------------------------------------------------------------
# [6:5]     | 00        | R/^w      | Operation     | These two bits set the operational mode for the ADT7420.
#           |           |           | mode          |   00 = continuous conversion (default). When one conversion is
#           |           |           |               |       finished, the ADT7420 starts another.
#           |           |           |               |   01 = one shot. Conversion time is typically 240 ms.
#           |           |           |               |   10 = 1 SPS mode. Conversion time is typically 60 ms. This
#           |           |           |               |       operational mode reduces the average current consumption.
#           |           |           |               |   11 = shutdown. All circuitry except interface circuitry is
#           |           |           |               |       powered down.
# ----------|-----------|-----------|---------------|-------------------------------------------------------------------
# 7         |0          | R/^w      | Resolution    | This bit sets up the resolution of the ADC when converting.
#           |           |           |               |   0 = 13-bit resolution. Sign bit + 12 bits gives a temperature
#           |           |           |               |       resolution of 0.0625°C.
#           |           |           |               |   1 = 16-bit resolution. Sign bit + 15 bits gives a temperature
#           |           |           |               |       resolution of 0.0078°C.
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Table 12. T_HIGH Setpoint MSB Register (Register Address 0x04)
# ----------------------------------------------------------------------------------------------------------------------
# Bit       | Default   |  Type     | Name          | Description
#           | Value     |           |               |
# ----------|-----------|-----------|---------------|-------------------------------------------------------------------
# [15:8]    | 0x20      | R/^W      | T_HIGH MSB    | MSBs of the overtemperature limit, stored in twos complement
#           |           |           |               | format.
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Table 13. T_HIGH Setpoint LSB Register (Register Address 0x05)
# ----------------------------------------------------------------------------------------------------------------------
# Bit       | Default   |  Type     | Name          | Description
#           | Value     |           |               |
# ----------|-----------|-----------|---------------|-------------------------------------------------------------------
# [7:0]     | 0x00      | R/^W      | T_HIGH LSB    | LSBs of the overtemperature limit, stored in twos complement
#           |           |           |               | format.
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Table 14. T_LOW Setpoint MSB Register (Register Address 0x06)
# ----------------------------------------------------------------------------------------------------------------------
# Bit       | Default   |  Type     | Name          | Description
#           | Value     |           |               |
# ----------|-----------|-----------|---------------|-------------------------------------------------------------------
# [15:8]    | 0x05      | R/^W      | T_LOW MSB     | MSBs of the undertemperature limit, stored in twos complement
#           |           |           |               | format.
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Table 15. T_LOW Setpoint LSB Register (Register Address 0x07)
# ----------------------------------------------------------------------------------------------------------------------
# Bit       | Default   |  Type     | Name          | Description
#           | Value     |           |               |
# ----------|-----------|-----------|---------------|-------------------------------------------------------------------
# [7:0]     | 0x00      | R/^W      | T_LOW LSB     | LSBs of the undertemperature limit, stored in twos complement
#           |           |           |               | format.
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Table 16. T_CRIT Setpoint MSB Register (Register Address 0x08)
# ----------------------------------------------------------------------------------------------------------------------
# Bit       | Default   |  Type     | Name          | Description
#           | Value     |           |               |
# ----------|-----------|-----------|---------------|-------------------------------------------------------------------
# [15:8]    | 0x49      | R/^W      | T_CRIT MSB    | MSBs of the critical overtemperature limit, stored in twos
#           |           |           |               | complement format.
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Table 17. T_CRIT Setpoint LSB Register (Register Address 0x09)
# ----------------------------------------------------------------------------------------------------------------------
# Bit       | Default   |  Type     | Name          | Description
#           | Value     |           |               |
# ----------|-----------|-----------|---------------|-------------------------------------------------------------------
# [7:0]     | 0x80      | R/^W      | T_CRIT LSB    | LSBs of the critical overtemperature limit, stored in twos
#           |           |           |               | complement format.
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Table 18. T_HYST Setpoint Register (Register Address 0x0A)
# ----------------------------------------------------------------------------------------------------------------------
# Bit       | Default   |  Type     | Name          | Description
#           | Value     |           |               |
# ----------|-----------|-----------|---------------|-------------------------------------------------------------------
# [3:0]     | 0101      | R/^W      | T_HYST        | Hysteresis value, from 0°C to 15°C. Stored in straight binary
#           |           |           |               | format. The default setting is 5°C.
# ----------|-----------|-----------|---------------|-------------------------------------------------------------------
# [7:4]     | 0000      | R/^W      | N/A           | Not used.
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Table 19. ID Register (Register Address 0x0B)
# ----------------------------------------------------------------------------------------------------------------------
# Bit       | Default   |  Type     | Name          | Description
#           | Value     |           |               |
# ----------|-----------|-----------|---------------|-------------------------------------------------------------------
# [2:0]     | 011       | R         | Revision ID   | Contains the silicon revision identification number
# ----------|-----------|-----------|---------------|-------------------------------------------------------------------
# [7:3]     | 11001     | R         | Manufacture ID| Contains the manufacture identification number
# ----------------------------------------------------------------------------------------------------------------------

import pigpio
import time

SENS_MSG_BOOT = 'Temperature Sensor'
SENS_MSG_REV = 'Rev'
SENS_MSG_CONNECT = 'Connecting Sensor'
SENS_MSG_DISCONNECT = 'Disconnecting Sensor'

VEND_ANALOG_DEVICES = 'Analog Devices'
VEND_ANALOG_DEVICES_ID = 0b11001

sens_vendor = dict({VEND_ANALOG_DEVICES_ID: VEND_ANALOG_DEVICES})


def c2f(temp):
    return temp * 9 / 5 + 32


class ADT7420:
    I2C_REG_MSB_TEMP = 0x00
    I2C_REG_LSB_TEMP = 0x01
    I2C_REG_STATUS = 0x02
    I2C_REG_CONFIG = 0x03
    I2C_REG_ID = 0x0B
    I2C_MODE = 0b10000000  # Table 11
    DEV_MASK_REV_ID = 0b00000111
    DEV_MASK_MAN_ID = 0b00011111

    class I2CData:
        I2C_REG_SIGN = 0b10000000000000000

        def __init__(self, msb, lsb):
            self.msb = msb
            self.lsb = lsb

        def convert(self):
            adc_code = ((self.msb << 8) | self.lsb)
            if adc_code & self.I2C_REG_SIGN:
                temp = (adc_code - 65536) / 128.0
            else:
                temp = adc_code / 128.0
            return temp

    def __init__(self, bus, addr, delay, mon_file):
        self.temp = None
        self.time = None
        self.time_str = None
        self.log = None
        self.i2c_bus = bus
        self.i2c_addr = addr
        self.i2c_delay = delay
        self.mon_file = mon_file
        self.i2c_flags = 0

        self.dev_pi = pigpio.pi()
        self.dev_temp = self.dev_pi.i2c_open(self.i2c_bus, self.i2c_addr, self.i2c_flags)

        self.dev_id = self.dev_pi.i2c_read_byte_data(self.dev_temp, self.I2C_REG_ID)
        self.dev_rev_id = self.DEV_MASK_REV_ID & self.dev_id
        self.dev_man_id = self.DEV_MASK_MAN_ID & (self.dev_id >> 3)
        self.open_log()
        self.log_connection()
        self.log_sensor_info()
        self.dev_pi.i2c_write_byte_data(self.dev_temp, self.I2C_REG_CONFIG, self.I2C_MODE)

    def __del__(self):
        self.disconnect()
        self.log_disconnection()
        self.close_log()

    def read_i2c(self):
        msb = self.dev_pi.i2c_read_byte_data(self.dev_temp, self.I2C_REG_MSB_TEMP)
        lsb = self.dev_pi.i2c_read_byte_data(self.dev_temp, self.I2C_REG_LSB_TEMP)
        return self.I2CData(msb, lsb)

    def read_time(self):
        self.time = time.time()
        self.time_str = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.time)))

    def read(self):
        i2c_data = self.read_i2c()
        self.read_time()
        self.temp = c2f(i2c_data.convert())

    def read_once(self):
        self.read()
        self.log_data()
        time.sleep(self.i2c_delay)

    def disconnect(self):
        r = self.dev_pi.i2c_close(self.dev_temp)
        return r

    def monitor(self):
        try:
            while True:
                self.read_once()

        except KeyboardInterrupt:
            pass

    # Log information
    def log_connection(self):
        self.read_time()
        msg = '{0}, {1}, {2}'.format(self.time_str, SENS_MSG_CONNECT, hex(self.dev_id))
        print(msg)
        self.log.write('{0}\n'.format(msg))

    def log_disconnection(self):
        self.read_time()
        msg = '{0}, {1}, {2}'.format(self.time_str, SENS_MSG_DISCONNECT, hex(self.dev_id))
        print(msg)
        self.log.write('{0}\n'.format(msg))

    def log_sensor_info(self):
        self.read_time()
        msg = '{0}, {1}, {2}, {3}, {4}'.format(self.time_str, sens_vendor[self.dev_man_id], SENS_MSG_BOOT, SENS_MSG_REV, self.dev_rev_id)
        print(msg)
        self.log.write('{0}\n'.format(msg))

    def log_data(self):
        msg = '{0}, {1}'.format(self.time_str, str(self.temp))
        print(msg)
        self.log.write('{0}\n'.format(msg))

    def open_log(self):
        self.log = open(self.mon_file, 'w')

    def close_log(self):
        self.log.close()


def mon_temp():
    ts = ADT7420(1, 0x49, 1, '/home/pi/temp_mon.csv')
    ts.monitor()


def main():
    mon_temp()


if __name__== "__main__":
    main()
