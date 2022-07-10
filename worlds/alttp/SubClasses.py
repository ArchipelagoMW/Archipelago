"""Module extending BaseClasses.py for aLttP"""
from typing import Optional

from BaseClasses import Location, Item, ItemClassification


class ALttPLocation(Location):
    game: str = "A Link to the Past"

    def __init__(self, player: int, name: str = '', id: int = None, address=None, crystal: bool = False,
                 hint_text: Optional[str] = None, parent=None,
                 player_address=None):
        super().__init__(name, player, id, parent)
        self.lttp_address = address
        self.crystal = crystal
        self.player_address = player_address
        self._hint_text: str = hint_text
