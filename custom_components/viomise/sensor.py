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
        return self._vacuum.battery_level if self._vacuum.battery_level is not None else None

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the sensor."""
        attributes = {}
        if hasattr(self._vacuum, 'vacuum_state') and isinstance(self._vacuum.vacuum_state, dict):
            # Convert the is_charge value to a boolean (0 means charging, 1 means not charging)
            is_charge_value = self._vacuum.vacuum_state.get('is_charge')
            if is_charge_value is not None:
                attributes['is_charging'] = is_charge_value == 0
        return attributes

    @property
    def icon(self):
        """Return the icon of the sensor."""
        charging = self.extra_state_attributes.get('is_charging', True)
        battery_level = self.native_value

        if battery_level is None:
            return 'mdi:battery-unknown'
        
        if charging:
            if battery_level >= 99:
                return 'mdi:battery-charging'
            elif battery_level >= 90:
                return 'mdi:battery-charging-100'
            elif battery_level >= 60:
                return 'mdi:battery-charging-70'
            elif battery_level >= 40:
                return 'mdi:battery-charging-50'
            elif battery_level >= 20:
                return 'mdi:battery-charging-30'
            else:
                return 'mdi:battery-charging-10'
        else:
            if battery_level >= 90:
                return 'mdi:battery'
            elif battery_level >= 60:
                return 'mdi:battery-70'
            elif battery_level >= 40:
                return 'mdi:battery-50'
            elif battery_level >= 20:
                return 'mdi:battery-30'
            else:
                return 'mdi:battery-10'
