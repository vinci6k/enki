# ../enki/listeners.py

# Source.Python
from cvars import ConVar
from entities.constants import WORLD_ENTITY_INDEX
from entities.entity import Entity
from entities.helpers import index_from_pointer
from entities.hooks import EntityCondition, EntityPreHook
from events import Event
from listeners import ListenerManager, ListenerManagerDecorator
from players.constants import PlayerStates
from players.helpers import index_from_userid

# Enki
from .players.dictionary import player_instances
from .players.entity import EnkiPlayer


__all__ = (
    'OnPlayerEnterWater',
    'OnPlayerExitWater'
)


tv_enable = ConVar('tv_enable')


class OnPlayerEnterWater(ListenerManagerDecorator):
    """Register/unregister a OnPlayerEnterWater listener."""
    manager = ListenerManager()


class OnPlayerExitWater(ListenerManagerDecorator):
    """Register/unregister a OnPlayerExitWater listener."""
    manager = ListenerManager()


@Event('player_spawn')
def player_spawn(event):
    """Called when a player spawns."""
    userid = event['userid']

    # Is this SourceTV/GOTV?
    if tv_enable.get_int() > 0 and userid == 2:
        # Skip it.
        return

    player = EnkiPlayer.from_userid(userid)
    # Store the EnkiPlayer instance to keep track of live players.
    player_instances[player.index] = player


@Event('player_death')
def player_death(event):
    """Called when a player dies."""
    index = index_from_userid(event['userid'])
    player = player_instances[index]

    # Did the player die in water?
    if player.last_water_level > 0:
        # Stop pushing the player up.
        player.rise_think.stop()
        # Fire the OnPlayerExitWater listener manually.
        OnPlayerExitWater.manager.notify(player=player)
        # Reset the 'last_water_level' attribute.
        player.last_water_level = 0

    # Player died, remove the EnkiPlayer instance from the dictionary.
    del player_instances[index]


@EntityPreHook(EntityCondition.is_player, 'post_think')
def post_think_pre(stack_data):
    try:
        # Try to get an EnkiPlayer instance.
        player = player_instances[index_from_pointer(stack_data[0])]
    except KeyError:
        # Player is not alive, don't go further.
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
