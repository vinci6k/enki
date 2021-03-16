# ../bouncy_water/bouncy_water.py

# Enki
from enki.listeners import OnPlayerEnterWater


@OnPlayerEnterWater
def on_player_enter_water(player):
    """Called when the player starts touching water."""
    # Get the direction the player is moving in.
    direction = player.velocity.normalized()
    # Exaggerate the Z axis - this will make the player go up.
    direction.z = 0.9
    # Push the player away from the water surface.
    player.teleport(velocity=direction * 450)
