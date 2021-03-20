# ../submerged_damage/submerged_damage.py

# Source.Python
from entities import TakeDamageInfo
from entities.hooks import EntityCondition, EntityPreHook
from players.entity import Player

# Enki
from enki.constants import WaterLevel


@EntityPreHook(EntityCondition.is_player, 'on_take_damage_alive')
def on_take_damage_alive_pre(stack_data):
    """Called when a player takes damage."""
    # Get the Player instance.
    player = Player._obj(stack_data[0])

    # Is the player fully submerged in water?
    if player.water_level == WaterLevel.EYES:
        # We need a TakeDamageInfo instance in order to modify the damage.
        info = TakeDamageInfo._obj(stack_data[1])
        # Lower the damage by half (50%).
        info.damage *= 0.5
