[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)
[![paypalme_badge](https://img.shields.io/badge/Donate-PayPal-0070ba)](https://paypal.me/MrGroch)
[![Buy me a coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/MrGroch)

# ESA NASK Air Quality Sensor

A Home Assistant custom Integration for [ESA NASK Air Quality](https://esa.nask.pl/) sensors.

Integration supports the following sensors of ESA NASK stations:

- Particulate matter (PM10)
- Particulate matter (PM2,5)
- Atmospheric pressure
- Humidity
- Temperature
- Dew Point Temperature

Diffrent stations may support diffrent data, integration will recognise all parameters (availible in station) according to list of integration's supported sensors.

## Installation

### Using [HACS](https://hacs.xyz/) (recommended)

This integration can be installed using HACS. To do it search for `ESA NASK Air Quality` in Integrations section.

### Manual

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `esa_nask`.
4. Download _all_ the files from the `custom_components/esa_nask/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant.
7. [Configure](#Configuration) custom component using Config Flow UI.

## Configuration

After installation of the custom component, it needs to be added using **Config Flow UI**.

To configure this integration go to: _Configuration_ -> _Integrations_ -> _Add integration_ -> _ESA NASK Air Quality Sensor_.

You can also use following [My Home Assistant](http://my.home-assistant.io/) link

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=esa_nask)

In popup window you need to fill:

- ID of ESA NASK station (required) - it is needed to put just a number that you can find in URL on ESA NASK website on station details page (eg. esa.nask.pl/szkola/id/**2010**),

You can add more than 1 station.
