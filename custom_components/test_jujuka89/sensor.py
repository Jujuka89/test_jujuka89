from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import track_time_interval
from datetime import timedelta
import statistics
from .const import DEFAULT_SCAN_INTERVAL, DEFAULT_BASE_TEMP
from homeassistant.util import dt as dt_util

def setup_platform(hass, config, add_entities, discovery_info=None):
    outdoor_sensor = config.get("outdoor_sensor")
    base_temp = config.get("base_temperature", DEFAULT_BASE_TEMP)
    add_entities([DJUSensor(hass, outdoor_sensor, base_temp)])


class DJUSensor(Entity):
    def __init__(self, hass, outdoor_sensor, base_temp):
        self._hass = hass
        self._outdoor_sensor = outdoor_sensor
        self._base_temp = base_temp
        self._temperatures = []
        self._state = 0
        self._last_day = dt_util.now().date()
        track_time_interval(hass, self.update, timedelta(seconds=DEFAULT_SCAN_INTERVAL))

    @property
    def name(self):
        return "DJU Journalier"

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return "°C"

    def update(self, now):
        current_day = dt_util.now().date()
        # Reset à minuit
        if current_day != self._last_day:
            self._temperatures = []
            self._state = 0
            self._last_day = current_day

        state = self._hass.states.get(self._outdoor_sensor)
        if state and state.state not in ("unknown", "unavailable"):
            temp = float(state.state)
            self._temperatures.append(temp)

        if self._temperatures:
            moyenne = statistics.mean(self._temperatures)
            self._state = round(max(0, self._base_temp - moyenne), 2)
