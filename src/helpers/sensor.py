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

    '''Init fn of environmental combo sensor. Max 2 devices on 1 i2c bus'''
    def __init__(self, index=0) -> None:
        self.bme_addr = 0x77 - index
        self.ccs_addr = 0x5B - index
        self.bus = smbus2.SMBus(1)

    '''Returns values from the BME280 sensor.'''
    def read_bme(self) -> dict:
        calibration_params = bme280.load_calibration_params(self.bus, self.bme_addr)
        output = bme280.sample(self.bus, self.bme_addr, calibration_params)

        return {
            'id': output.id,
            'timestamp': output.timestamp,
            'temperature': output.temperature * (9/5) + 32,
            'pressure': output.pressure,
            'humidity': output.humidity
        }
    
    '''Returns values from the CCS811 sensor.'''
    def read_ccs(self) -> dict:
        pass
        

sensor = EnvComboSensor(0)
sensor.read_bme()
