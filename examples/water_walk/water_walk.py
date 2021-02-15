# ../water_walk/water_walk.py

# Source.Python
from commands import CommandReturn
from commands.client import ClientCommand
from messages import HintText

# Enki
from enki.players.entity import EnkiPlayer


@ClientCommand('+lookatweapon')
def inspect_weapon_pressed(command, index):
    """Called when a player presses their weapon inspect key."""
    EnkiPlayer(index).enable_water_walking()
    # Tell the player that they can walk on water.
    HintText('You can now walk on water.').send(index)
    # Block the inspect animation from playing.
    return CommandReturn.BLOCK


@ClientCommand('-lookatweapon')
def inspect_weapon_released(command, index):
    """Called when a player releases their weapon inspect key."""
    EnkiPlayer(index).disable_water_walking()
    HintText('You can no longer walk on water!').send(index)
    return CommandReturn.BLOCK
