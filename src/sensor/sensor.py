import smbus
import time
from abc import ABC, abstractmethod

class Sensor:
    
    # abstract method
    def __init__(self) -> None:
        # establish an address for the new sensor

class EnvComboSensor(Sensor):
    index = None

    bme_addr = 0x00 # default is 0x77
    bme_hum_lsb = 0xFE # 
    bme_hum_msb = 0xFD
    bme_temp_xlsb = 0xFC # only bits 7-4 have data, rest are 0
    bme_temp_lsb = 0xFB
    bme_temp_msb = 0xFA
    bme_press_xlsb = 0xF9 # only bits 7-4 have data, rest are 0
    bme_press_lsb = 0xF8
    bme_press_msb = 0xF7
    bme_config = 0xF5
    bme_ctrl_meas = 0xF4
    bme_status = 0xF3
    bme_ctrl_hum = 0xF2
    bme_reset = 0xE0
    bme_id = 0xD0

    ccs_addr = 0x00 # default is 0x5B
    ccs_status = 0x00 # R; 1b status
    ccs_meas_mode = 0x01 # R/W; 1b meas mode and conditions register
    ccs_alg_data = 0x02 # R; up to 8b. 2 most signifiicant bytes are ppm estim
    ccs_raw_data = 0x03 # R; 2b raw ADC values
    ccs_env_data = 0x05 # W; 4b temp & hum data for compensation
    ccs_NTC = 0x06 # R; 4b voltage to calc ambient temp
    ccs_thresholds = 0x10 # W; 5b thresholds if using interrupt mode
    ccs_baseline = 0x11 # R/W; 2b read current baseline or write new baseline
    ccs_hw_id = 0x20 # R; 1b hardware ID (0x81)
    ccs_hw_version = 0x21 # R; 1b hardware version
    ccs_fw_boot_version = 0x23 # R; 2b of fw version
    ccs_fw_app_version = 0x24 # R; 2b of fw version
    ccs_error_id = 0xE0 # R; 1b saying error source
    ccs_sw_reset = 0xFF # W; 4b write to reset device

    """Init fn of environmental combo sensor. Max 2 devices on 1 i2c bus"""
    def __init__(self, index=0) -> None:
        bme_addr = 0x77 - index
        ccs_addr = 0x5B - index

    def read_eCO2() -> TBD:

    

class SomeOtherSensor(Sensor):

