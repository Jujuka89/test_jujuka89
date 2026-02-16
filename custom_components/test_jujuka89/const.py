""" Les constantes pour l'intégration Test Jujuka89 """

from homeassistant.const import Platform

DOMAIN = "test_jujuka89"
PLATFORMS: list[Platform] = [Platform.SENSOR]

CONF_NAME = "name"
CONF_DEVICE_ID = "device_id"
DEFAULT_BASE_TEMP = 18.0
DEVICE_MANUFACTURER = "JUJUKA89"
