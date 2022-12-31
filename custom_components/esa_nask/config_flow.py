"""Adds config flow for ESA NASK integration."""
from __future__ import annotations

from typing import Any

from .esa_nask_scrapper import EsaNaskScrapper

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from homeassistant.const import (
    CONF_ID
)
from .const import (
    DOMAIN
)


class EsaNaskConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ESA NASK integration."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle the initial step."""

        errors = {}

        data_schema = vol.Schema(
            {
                vol.Required(CONF_ID): cv.string
            }
        )

        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=data_schema
            )

        id = user_input[CONF_ID]
        scrapper = EsaNaskScrapper(id)
        await self.hass.async_add_executor_job(scrapper.update)

        validateData = scrapper.GetData()
        if validateData:
            if "status" in validateData:
                if validateData["status"] == 401:
                    errors["base"] = "invalid_token"
                else:
                    errors["base"] = "server_error"
            if "errorCode" in validateData:
                if validateData["errorCode"] == "sc-001":
                    errors["base"] = "unknow_station_id"
                else:
                    errors["base"] = "server_error"
        else:
            errors["base"] = "server_not_available"

        stationName = scrapper.GetStationName()
        stationFriendlyName = scrapper.GetStationFriendlyName()
        
        if not errors:
            await self.async_set_unique_id(stationName)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=stationFriendlyName,
                data={
                    CONF_ID: id
                }
            )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )

