# ../enki/players/__init__.py

# Source.Python
from events import Event

# Enki
from ..constants import WaterLevel
from ..listeners import OnPlayerExitWater
from .entity import EnkiPlayer


@Event('player_death')
def player_death(event):
    """Called when a player dies."""
    player = EnkiPlayer.from_userid(event['userid'])

    # Did the player die in water?
    if player.last_water_level != WaterLevel.NOT_IN_WATER:
        # Stop pushing the player up.
        player.rise_think.stop()
        # Fire the OnPlayerExitWater listener manually.
        OnPlayerExitWater.manager.notify(player=player)
        # Reset the 'last_water_level' attribute.
        player.last_water_level = WaterLevel.NOT_IN_WATER
