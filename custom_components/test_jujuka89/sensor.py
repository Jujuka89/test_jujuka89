from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from datetime import timedelta, datetime
from .const import DOMAIN, DEFAULT_BASE_TEMP

import statistics

SCAN_INTERVAL = timedelta(minutes=10)


async def async_setup_platform(hass: HomeAssistant, config, async_add_entities, discovery_info=None):

    outdoor_entity = config.get("outdoor_sensor")
    base_temp = config.get("base_temperature", DEFAULT_BASE_TEMP)

    async_add_entities([DJUSensor(hass, outdoor_entity, base_temp)])


class DJUSensor(SensorEntity, RestoreEntity):

    def __init__(self, hass, outdoor_entity, base_temp):
        self._hass = hass
        self._outdoor_entity = outdoor_entity
        self._base_temp = base_temp
        self._attr_name = "DJU Jour"
        self._attr_unit_of_measurement = "°C"
        self._temperatures = []
        self._state = 0

    async def async_added_to_hass(self):
        async_track_time_interval(
            self._hass, self.update_dju, SCAN_INTERVAL
        )

    async def update_dju(self, now):
        state = self._hass.states.get(self._outdoor_entity)

        if state and state.state not in ("unknown", "unavailable"):
            temp = float(state.state)
            self._temperatures.append(temp)

        # garde uniquement 24h (144 mesures de 10 min)
        if len(self._temperatures) > 144:
            self._temperatures.pop(0)

        if self._temperatures:
            moyenne = statistics.mean(self._temperatures)
            dju = max(0, self._base_temp - moyenne)
            self._state = round(dju, 2)

        self.async_write_ha_state()

    @property
    def state(self):
        return self._state
