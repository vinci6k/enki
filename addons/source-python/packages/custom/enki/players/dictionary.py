# ../enki/players/dictionary.py

# Source.Python
from players.dictionary import PlayerDictionary


__all__ = (
    'player_instances',
)


# Dictionary used to keep track of players that are currently alive.
player_instances = PlayerDictionary(factory=None)
