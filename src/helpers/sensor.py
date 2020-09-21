'''
Sensor class for retrieving data, including temperature,
eCO2, relative humidity, and barometric pressure.

Authors:
Michael Rakowiecki
Kevin Kraydich <kevin.kraydich@gmail.com>
'''

import smbus2
import bme280


class EnvComboSensor:
    index = None

    # Register values for BME
    bme = {
        'addr': 0x00,       # default is 0x77
        'hum_lsb': 0xFE,
        'hum_msb': 0xFD,
        'temp_xlsb': 0xFC,  # only bits 7-4 have data, rest are 0
        'temp_lsb': 0xFB,
        'temp_msb': 0xFA,
        'press_xlsb': 0xF9, # only bits 7-4 have data, rest are 0
        'press_lsb': 0xF8,
        'press_msb': 0xF7,
        'config': 0xF5,
        'ctrl_meas': 0xF4,
        'status': 0xF3,
        'ctrl_hum': 0xF2,
        'reset': 0xE0,
        'id': 0xD0
    }

    # Register values for CCS
    ccs = {
        'addr': 0x00,               # default is 0x5B
        'status': 0x00,             # R; 1b status
        'meas_mode': 0x01,          # R/W; 1b meas mode and conditions register
        'alg_data': 0x02,           # R; up to 8b. 2 most signifiicant bytes are ppm estim
        'raw_data': 0x03,           # R; 2b raw ADC values
        'env_data': 0x05,           # W; 4b temp & hum data for compensation
        'NTC': 0x06,                # R; 4b voltage to calc ambient temp
        'thresholds': 0x10,         # W; 5b thresholds if using interrupt mode
        'baseline': 0x11,           # R/W; 2b read current baseline or write new baseline
        'hw_id': 0x20,              # R; 1b hardware ID (0x81)
        'hw_version': 0x21,         # R; 1b hardware version
        'fw_boot_version': 0x23,    # R; 2b of fw version
        'fw_app_version': 0x24,     # R; 2b of fw version
        'error_id': 0xE0,           # R; 1b saying error source
        'sw_reset': 0xFF            # W; 4b write to reset device
    }

    '''Init fn of environmental combo sensor. Max 2 devices on 1 i2c bus'''
    def __init__(self, index=0) -> None:
        self.bme_addr = 0x77 - index
        self.ccs_addr = 0x5B - index
        self.bus = smbus2.SMBus(1)

    def read_bme280(self) -> dict:
        calibration_params = bme280.load_calibration_params(self.bus, self.bme_addr)
        data = bme280.sample(self.bus, self.bme_addr, calibration_params)
        
        print(data)

sensor = EnvComboSensor(0)
sensor.read_bme280()
