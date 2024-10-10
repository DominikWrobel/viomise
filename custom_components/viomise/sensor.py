"""Battery sensor for Xiaomi vacuum."""
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Xiaomi vacuum battery sensor."""
    try:
        vacuum = hass.data[DOMAIN][config_entry.entry_id]
        async_add_entities([XiaomiVacuumBatterySensor(vacuum)], True)
    except KeyError:
        return

class XiaomiVacuumBatterySensor(SensorEntity):
    """Representation of a Xiaomi vacuum battery sensor."""

    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, vacuum):
        """Initialize the sensor."""
        self._vacuum = vacuum
        self._attr_unique_id = f"{vacuum.unique_id}_battery"
        self._attr_name = f"{vacuum.name} Battery"
        
        # Link this entity to the same device as the vacuum
        self._attr_device_info = vacuum.device_info

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._vacuum.battery_level
