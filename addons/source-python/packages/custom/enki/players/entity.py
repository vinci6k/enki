# ../enki/players/entity.py

# Source.Python
from engines.trace import (ContentMasks, GameTrace, Ray, TraceFilterSimple, 
    engine_trace)
from mathlib import Vector
from players.entity import Player

# Enki
from ..constants import WaterLevel


__all__ = (
    'EnkiPlayer',
)


class EnkiPlayer(Player):
    """Extended Player class.
    
    Args:
        index (int): A valid player index.
        caching (bool): Check for a cached instance?

    Attributes:
        last_water_level (int): The player's water level from the frame before.
        walk_on_water (bool): Should the player walk on water?
        rise_think (Repeat): Instance of Repeat() used for looping the
            `_rise_think()` function.
    """
    velocity_rise = Vector(0, 0, 50)
    velocity_bounce = Vector(0, 0, 300)

    def __init__(self, index, caching=True):
        """Initializes the object."""
        super().__init__(index, caching)

        self.last_water_level = self.water_level
        self.walk_on_water = False
        self.rise_think = self.repeat(self._rise_think)

    @property
    def is_in_water(self):
        """Returns whether the player is currently in/touching water."""
        return self.water_level != WaterLevel.NOT_IN_WATER

    def enable_water_walking(self):
        """Enables walking on water for the player."""
        # Can the player already walk on water?
        if self.walk_on_water:
            return

        self.walk_on_water = True

        # Is the player within/touching water?
        if self.water_level != WaterLevel.NOT_IN_WATER:
            # Let's push them to the surface.
            self.rise_think.start(0.05)

    def disable_water_walking(self):
        """Disables walking on water for the player."""
        if not self.walk_on_water:
            return

        self.walk_on_water = False
        self.rise_think.stop()
    
    def _rise_think(self):
        water_level = self.water_level
        
        # Is the player no longer touching the water?
        if water_level == WaterLevel.NOT_IN_WATER:
            self.rise_think.stop()

        # Or is the player touching the water with their feet?
        elif water_level == WaterLevel.FEET:
            # Find the exact position of the water surface.
            water_position = self.get_water_trace().end_position
            # Offset the Z axis slightly to better align the player.
            water_position.z += 2

            self.teleport(origin=water_position)
            self.rise_think.stop()

        # Push the player up.
        self.base_velocity += EnkiPlayer.velocity_rise

    def get_water_trace(self):
        """Fires a trace towards the player's feet, checking for water."""
        origin = self.origin

        trace = GameTrace()
        engine_trace.trace_ray(
            # Create a Ray() from the top of the player to their feet.
            ray=Ray(origin + Vector(0, 0, self.maxs.z), origin),
            mask=ContentMasks.WATER,
            filter=TraceFilterSimple(
                ignore=(self, )
                ),
            trace=trace
            )

        return trace
        
