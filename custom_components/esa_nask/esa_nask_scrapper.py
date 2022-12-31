import json
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from homeassistant.util import Throttle
from homeassistant.const import (
    CONF_ID
)
from .const import SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

class EsaNaskScrapper(object):

    def __init__(self, id):
        self._id = id
        self._data = None
        self._stationName = None
        self._stationFriendlyName = None
        self._stationId = None
        self._updateLastTime = None

    @Throttle(SCAN_INTERVAL)
    def update(self):
        _LOGGER.debug("Updating ESA NASK sensors")
        try:
            _token = BeautifulSoup(requests.get("https://esa.nask.pl").content, "html.parser").find(id="security").get("data-value")
            _dat = requests.get(f"https://esa.nask.pl/api/data/id/{self._id}", headers={"authorization": f"Bearer {_token}"}).text
                
            if _dat:
                self._data = json.loads(_dat)
                if self._data:
                    if "id" in self._data:
                        self._stationId = self._data["id"]

                        if "name" in self._data:
                            self._stationFriendlyName = self._data["name"]
                        if "shortName" in self._data:
                            self._stationFriendlyName = self._data["shortName"]

                        if self._stationFriendlyName:
                            self._stationName = self._stationFriendlyName.replace(", ", "_").replace(" ", "_").replace("(", "").replace(")","").lower()
                        else:
                            self._stationName = "UnknownName_" + self._stationId
                        
                        self._updateLastTime = datetime.now()

        except requests.exceptions.RequestException as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc)
            self._data = None
            self._stationName = None
            self._stationFriendlyName = None
            self._stationId = None
            return False
    
    def GetData(self):
        return self._data

    def GetStationName(self):
        return self._stationName

    def GetStationFriendlyName(self):
        if self._stationFriendlyName:
            return self._stationFriendlyName
        return self._stationName
        
    def GetStationId(self):
        return self._stationId
        
    def GetUpdateLastTime(self):
        return self._updateLastTime
