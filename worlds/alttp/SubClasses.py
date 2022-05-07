"""Module extending BaseClasses.py for aLttP"""
from typing import Optional

from BaseClasses import Location, Item


class ALttPLocation(Location):
    game: str = "A Link to the Past"

    def __init__(self, player: int, name: str = '', address=None, crystal: bool = False,
                 hint_text: Optional[str] = None, parent=None,
                 player_address=None):
        super(ALttPLocation, self).__init__(player, name, address, parent)
        self.crystal = crystal
        self.player_address = player_address
        self._hint_text: str = hint_text
