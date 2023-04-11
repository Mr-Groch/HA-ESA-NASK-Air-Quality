"""Constants for the ESA NASK integration."""

from datetime import timedelta

from homeassistant.const import (
    TEMP_CELSIUS,
    PRESSURE_HPA,
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    PERCENTAGE,
    Platform
)
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass
)

DOMAIN = "esa_nask"
PLATFORMS = [Platform.SENSOR]
SW_VERSION = "1.0.2"

SCAN_INTERVAL = timedelta(minutes=10)

SENSORS = {
    'pm10': ['PM10', CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, 'mdi:molecule', SensorDeviceClass.PM10, SensorStateClass.MEASUREMENT],
    'pm25': ['PM2.5', CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, 'mdi:molecule', SensorDeviceClass.PM25, SensorStateClass.MEASUREMENT],
    'humidity': ['Humidity', PERCENTAGE, 'mdi:water-percent', SensorDeviceClass.HUMIDITY, SensorStateClass.MEASUREMENT],
    'pressure': ['Pressure', PRESSURE_HPA, 'mdi:gauge', SensorDeviceClass.PRESSURE, SensorStateClass.MEASUREMENT],
    'temperature': ['Temperature', TEMP_CELSIUS, 'mdi:thermometer', SensorDeviceClass.TEMPERATURE, SensorStateClass.MEASUREMENT],
    'dewPoint': ['Dew Point', TEMP_CELSIUS, 'mdi:thermometer-lines', SensorDeviceClass.TEMPERATURE, SensorStateClass.MEASUREMENT]
}
