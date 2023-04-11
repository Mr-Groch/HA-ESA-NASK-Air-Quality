"""Get station's air quality informations"""
from __future__ import annotations

import logging
from this import s

from .esa_nask_scrapper import EsaNaskScrapper

import json

import voluptuous as vol

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from homeassistant.const import (
    CONF_ID
)

from .const import (
    SENSORS,
    DOMAIN,
    SW_VERSION
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the ESA NASK sensor entry."""
    
    _LOGGER.debug("config ID:")
    _LOGGER.debug(entry.data[CONF_ID])
    
    id = entry.data[CONF_ID]
    scrapper = EsaNaskScrapper(id)
    
    await hass.async_add_executor_job(scrapper.update)

    scannedData = scrapper.GetData()
    scannedData = scannedData["sensors"][0]["lastMeasurement"]

    entities = []
    
    for res in SENSORS:
        if res in scannedData:
            entities.append(EsaNaskSensor(res, scrapper))

    async_add_entities(entities, update_before_add=True)



class EsaNaskSensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, resType: str, scrapper: EsaNaskScrapper) -> None:
        self._state = None
        self._AQI = None
        self._resType = resType
        self._scrapper = scrapper
        self._stationName = self._scrapper.GetStationName()
        self._stationFriendlyName = self._scrapper.GetStationFriendlyName()
        self._stationId = self._scrapper.GetStationId()
        self._updateLastTime = self._scrapper.GetUpdateLastTime()
        self._data = self._scrapper.GetData()
        self._name = f"{self._stationFriendlyName} {SENSORS[self._resType][0]}"

        self._attr_name = self._name
        self._attr_unique_id = f"{self._stationName}_{self._stationId}_{SENSORS[self._resType][0]}"
        self._attr_extra_state_attributes = {
            "Station Name": self._stationFriendlyName,
            "Station ID": self._stationId
        }
        self._attr_device_info = DeviceInfo(
            identifiers = {(DOMAIN, f"{self._stationName}_{self._stationId}")},
            manufacturer = "ESA NASK",
            model = f"Id: {self._stationId}",
            sw_version = SW_VERSION,
            name = self._stationFriendlyName,
            configuration_url=(f"https://esa.nask.pl/szkola/id/{self._stationId}")
        )
        self._attr_attribution = "Data provided by ESA NASK"
        self._attr_translation_key = DOMAIN

    @property
    def state(self):
        #Return the state of the sensor.
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        #Return the unit of measurement.
        return SENSORS[self._resType][1]

    @property
    def device_class(self) -> SensorDeviceClass | str | None:
        return SENSORS[self._resType][3]

    @property
    def state_class(self) -> SensorStateClass | str | None:
        return SENSORS[self._resType][4]

    @property
    def icon(self) -> str | None:
        return SENSORS[self._resType][2]

    def update(self) -> None:
        #Fetch new state data for the sensor.
        #This is the only method that should fetch new data for Home Assistant.

        self._scrapper.update()

        self._data = self._scrapper.GetData()
        self._updateLastTime = self._scrapper.GetUpdateLastTime()

        if self._resType == 'pm25' or self._resType == 'pm10':
            self._state = int(self._data["sensors"][0]["lastMeasurement"][self._resType]["value"])
            self._AQI = self._data["sensors"][0]["lastMeasurement"][self._resType]["icon"]
        else:
            self._state = round((self._data["sensors"][0]["lastMeasurement"][self._resType]), 2)
        
        self._attr_extra_state_attributes = {
            "Station Name": self._scrapper.GetStationFriendlyName(),
            "Station ID": self._scrapper.GetStationId(),
            "Last Update": self._scrapper.GetUpdateLastTime()
        }
        if self._AQI:
            self._attr_extra_state_attributes["AQI"] = self._AQI
