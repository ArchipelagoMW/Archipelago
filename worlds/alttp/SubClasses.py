"""Module extending BaseClasses.py for aLttP"""
from typing import Optional

from BaseClasses import Location, Item, ItemClassification


class ALttPLocation(Location):
    game: str = "A Link to the Past"
    crystal: bool
    player_address: Optional[int]
    _hint_text: Optional[str]
    shop_slot: Optional[int] = None
    """If given as integer, shop_slot is the shop's inventory index."""
    shop_slot_disabled: bool = False

    def __init__(self, player: int, name: str, address: Optional[int] = None, crystal: bool = False,
                 hint_text: Optional[str] = None, parent=None, player_address: Optional[int] = None):
        super(ALttPLocation, self).__init__(player, name, address, parent)
        self.crystal = crystal
        self.player_address = player_address
        self._hint_text = hint_text


class ALttPItem(Item):
    game: str = "A Link to the Past"
    type: Optional[str]
    _pedestal_hint_text: Optional[str]
    _hint_text: Optional[str]
    dungeon = None

    def __init__(self, name, player, classification=ItemClassification.filler, type=None, item_code=None,
                 pedestal_hint=None, hint_text=None):
        super(ALttPItem, self).__init__(name, classification, item_code, player)
        self.type = type
        self._pedestal_hint_text = pedestal_hint
        self._hint_text = hint_text

    @property
    def crystal(self) -> bool:
        return self.type == 'Crystal'

    @property
    def smallkey(self) -> bool:
        return self.type == 'SmallKey'

    @property
    def bigkey(self) -> bool:
        return self.type == 'BigKey'

    @property
    def map(self) -> bool:
        return self.type == 'Map'

    @property
    def compass(self) -> bool:
        return self.type == 'Compass'

    @property
    def dungeon_item(self) -> Optional[str]:
        if self.type in {"SmallKey", "BigKey", "Map", "Compass"}:
            return self.type

    @property
    def locked_dungeon_item(self):
        return self.location.locked and self.dungeon_item