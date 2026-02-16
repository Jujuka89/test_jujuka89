from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfTemperature
from . import DOMAIN

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([MonCapteur()])

class MonCapteur(SensorEntity):
    def __init__(self):
        self._state = 25

    @property
    def name(self):
        return "Température Test"

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return UnitOfTemperature.CELSIUS
