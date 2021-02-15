# ../enki/constants.py

# Python
from enum import IntEnum


__all__ = (
    'WaterLevel',
)


class WaterLevel(IntEnum):
    """Identifies how submerged in water a player is."""
    NOT_IN_WATER = 0
    FEET = 1
    WAIST = 2
    EYES = 3
