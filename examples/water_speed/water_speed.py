# ../water_speed/water_speed.py

# Enki
from enki.listeners import OnPlayerEnterWater, OnPlayerExitWater


@OnPlayerEnterWater
def on_player_enter_water(player):
    """Called when a player starts touching water."""
    player.speed += 2


@OnPlayerExitWater
def on_player_exit_water(player):
    """Called when a player stops touching water."""
    player.speed -= 2
