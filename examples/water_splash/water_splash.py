# ../water_splash/water_splash.py

# Source.Python
from entities.entity import Entity
from stringtables import string_tables

# Enki
from enki.listeners import OnPlayerEnterWater


@OnPlayerEnterWater
def on_player_enter_water(player):
    """Called when a player starts touching water."""
    # Did the player enter the water at a reasonable velocity?
    if player.velocity.length > 300:
        # Let's make a big water splash!
        particle = Entity.create('info_particle_system')
        particle.origin = player.origin
        # NOTE: This particle effect only exists in CS:GO, there are similar
        # effects in other games, e.g. 'water_splash_01' in CS:S.
        particle.effect_name = 'explosion_basic_water'
        particle.effect_index = string_tables.ParticleEffectNames.add_string(
            'explosion_basic_water'
        )
        particle.start()
        particle.delay(1, particle.remove)
