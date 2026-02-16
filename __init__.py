DOMAIN = "mon_integration"

async def async_setup(hass, config):
    hass.data[DOMAIN] = {}
    return True
