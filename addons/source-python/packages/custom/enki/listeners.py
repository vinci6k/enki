# ../enki/listeners.py

# Source.Python
from entities.constants import WORLD_ENTITY_INDEX
from entities.entity import Entity
from entities.hooks import EntityCondition, EntityPreHook
from listeners import ListenerManager, ListenerManagerDecorator
from players.constants import PlayerStates

# Enki
from .players.entity import EnkiPlayer


__all__ = (
    'OnPlayerEnterWater',
    'OnPlayerExitWater'
)


class OnPlayerEnterWater(ListenerManagerDecorator):
    """Register/unregister a OnPlayerEnterWater listener."""
    manager = ListenerManager()


class OnPlayerExitWater(ListenerManagerDecorator):
    """Register/unregister a OnPlayerExitWater listener."""
    manager = ListenerManager()


@EntityPreHook(EntityCondition.is_player, 'post_think')
def post_think_pre(stack_data):
    player = EnkiPlayer._obj(stack_data[0])

    # Is the player dead?
    if player.get_datamap_property_bool('pl.deadflag'):
        # No need to go further.
        return

    water_level = player.water_level
    last_water_level = player.last_water_level

    # Is the player touching the water for the first time?
    if last_water_level == 0 and water_level > 0:
        OnPlayerEnterWater.manager.notify(player=player)

        if player.walk_on_water:
            # Give the player a small push upwards to prevent them getting too
            # deep into the water.
            player.base_velocity += EnkiPlayer.velocity_bounce

    # Or are they getting out of it?
    elif last_water_level > 0 and water_level == 0:
        OnPlayerExitWater.manager.notify(player=player)

    # Should the player walk on water and are their feet in/touching water?
    if player.walk_on_water and water_level == 1:
        # Trick the player into thinking they're still walking on solid ground.
        player.ground_entity = Entity(WORLD_ENTITY_INDEX).inthandle
        # This makes sure appropriate animations get played while the player is
        # walking on water. (e.g. jumping)
        player.flags |= PlayerStates.ONGROUND

    # Keep track of the player's last water level.
    player.last_water_level = water_level
