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
from homeassistant.helpers.update_coordinator import CoordinatorEntity
import logging

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

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
        _LOGGER.error("Could not find vacuum entity in hass.data[%s][%s]", DOMAIN, config_entry.entry_id)
        return

class XiaomiVacuumBatterySensor(SensorEntity):
    """Representation of a Xiaomi vacuum battery sensor."""

    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_should_poll = True  # Explicitly enable polling

    def __init__(self, vacuum):
        """Initialize the sensor."""
        self._vacuum = vacuum
        self._attr_unique_id = f"{vacuum.unique_id}_battery"
        self._attr_name = f"{vacuum.name} Battery"
        self._last_battery_level = None
        self._last_charging_state = None
        
        # Link this entity to the same device as the vacuum
        self._attr_device_info = vacuum.device_info

    @property
    def native_value(self):
        """Return the state of the sensor."""
        try:
            # First check if vacuum has updated state
            if not hasattr(self._vacuum, 'vacuum_state') or self._vacuum.vacuum_state is None:
                _LOGGER.debug("Vacuum state is None or missing")
                return self._last_battery_level
            
            # Get battery level from vacuum state
            battery_level = self._vacuum.vacuum_state.get('battary_life')  # Note: misspelled in original
            
            if battery_level is not None:
                try:
                    battery_level = int(battery_level)
                    # Validate battery level is in reasonable range
                    if 0 <= battery_level <= 100:
                        self._last_battery_level = battery_level
                        return battery_level
                    else:
                        _LOGGER.warning("Battery level %s is out of range (0-100)", battery_level)
                        return self._last_battery_level
                except (ValueError, TypeError):
                    _LOGGER.warning("Could not convert battery level to int: %s", battery_level)
                    return self._last_battery_level
            else:
                _LOGGER.debug("Battery level is None in vacuum state")
                return self._last_battery_level
                
        except Exception as exc:
            _LOGGER.error("Error getting battery level: %s", exc)
            return self._last_battery_level

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        # Sensor is available if vacuum is available and has state data
        return (
            hasattr(self._vacuum, '_available') 
            and self._vacuum._available 
            and hasattr(self._vacuum, 'vacuum_state') 
            and self._vacuum.vacuum_state is not None
        )

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the sensor."""
        attributes = {}
        try:
            if hasattr(self._vacuum, 'vacuum_state') and isinstance(self._vacuum.vacuum_state, dict):
                # Convert the is_charge value to a boolean (0 means charging, 1 means not charging)
                is_charge_value = self._vacuum.vacuum_state.get('is_charge')
                if is_charge_value is not None:
                    try:
                        charging = int(is_charge_value) == 0
                        attributes['is_charging'] = charging
                        self._last_charging_state = charging
                    except (ValueError, TypeError):
                        _LOGGER.warning("Could not convert is_charge to int: %s", is_charge_value)
                        if self._last_charging_state is not None:
                            attributes['is_charging'] = self._last_charging_state
                elif self._last_charging_state is not None:
                    attributes['is_charging'] = self._last_charging_state
                    

                
        except Exception as exc:
            _LOGGER.error("Error getting battery attributes: %s", exc)
            
        return attributes

    @property
    def icon(self):
        """Return the icon of the sensor."""
        try:
            charging = self.extra_state_attributes.get('is_charging', False)
            battery_level = self.native_value

            if battery_level is None:
                return 'mdi:battery-unknown'
            
            if charging:
                if battery_level >= 99:
                    return 'mdi:battery-charging'
                elif battery_level >= 90:
                    return 'mdi:battery-charging-100'
                elif battery_level >= 70:
                    return 'mdi:battery-charging-80'
                elif battery_level >= 60:
                    return 'mdi:battery-charging-70'
                elif battery_level >= 50:
                    return 'mdi:battery-charging-60'
                elif battery_level >= 40:
                    return 'mdi:battery-charging-50'
                elif battery_level >= 30:
                    return 'mdi:battery-charging-40'
                elif battery_level >= 20:
                    return 'mdi:battery-charging-30'
                elif battery_level >= 10:
                    return 'mdi:battery-charging-20'
                else:
                    return 'mdi:battery-charging-10'
            else:
                if battery_level >= 95:
                    return 'mdi:battery'
                elif battery_level >= 85:
                    return 'mdi:battery-90'
                elif battery_level >= 75:
                    return 'mdi:battery-80'
                elif battery_level >= 65:
                    return 'mdi:battery-70'
                elif battery_level >= 55:
                    return 'mdi:battery-60'
                elif battery_level >= 45:
                    return 'mdi:battery-50'
                elif battery_level >= 35:
                    return 'mdi:battery-40'
                elif battery_level >= 25:
                    return 'mdi:battery-30'
                elif battery_level >= 15:
                    return 'mdi:battery-20'
                elif battery_level >= 5:
                    return 'mdi:battery-10'
                else:
                    return 'mdi:battery-outline'
        except Exception as exc:
            _LOGGER.error("Error determining battery icon: %s", exc)
            return 'mdi:battery-unknown'

    async def async_update(self):
        """Update the sensor state."""
        try:
            # Ensure the vacuum has updated its state
            if hasattr(self._vacuum, 'async_update'):
                await self._vacuum.async_update()
            elif hasattr(self._vacuum, 'update'):
                # Call synchronous update in executor
                await self.hass.async_add_executor_job(self._vacuum.update)
            
            _LOGGER.debug(
                "Battery sensor update: level=%s, charging=%s, available=%s",
                self.native_value,
                self.extra_state_attributes.get('is_charging'),
                self.available
            )
            
        except Exception as exc:
            _LOGGER.error("Error updating battery sensor: %s", exc)
