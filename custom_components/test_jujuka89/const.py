""" Les constantes pour l'intégration Tuto HACS """

from homeassistant.const import Platform

DOMAIN = "tuto_hacs"
PLATFORMS: list[Platform] = [Platform.SENSOR]

CONF_NAME = "name"
CONF_DEVICE_ID = "device_id"

DEVICE_MANUFACTURER = "JMCOLLIN"
