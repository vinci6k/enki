# Enki 
This is a small custom package for [Source.Python](https://github.com/Source-Python-Dev-Team/Source.Python) that gives plugin developers quick and easy access to the Player instance whenever the player starts or stops touching water.

<img src="https://i.giphy.com/media/Wayqf54mH2LabBeJlM/giphy.webp" width="412px" /> <img src="https://media0.giphy.com/media/pqWtHQWqZDcbV5cn1C/giphy.gif" width="412px" />  
*First gif: [water_spash.py](https://github.com/vinci6k/enki/blob/master/examples/water_splash/water_splash.py); Second gif: [water_walk.py](https://github.com/vinci6k/enki/blob/master/examples/water_walk/water_walk.py)*

## Installation
1. [Install Source.Python](http://wiki.sourcepython.com/general/installation.html).
2. Download [the latest release](https://github.com/vinci6k/enki/releases) of Enki.
3. Extract the files into your game server's root folder.<br/>(e.g. ../csgo/ for Counter-Strike: Global Offensive)
4. Restart your server.

## Usage
```py
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
```
There are a few more [examples](https://github.com/vinci6k/enki/tree/master/examples) which showcase how this package works.  
To see all the available imports/modules, head over to the [wiki](https://github.com/vinci6k/enki/wiki).


## Supported Games
Counter-Strike: Source  
Counter-Strike: Global Offensive  
Half Life 2: Deathmatch  
Team Fortress 2  
