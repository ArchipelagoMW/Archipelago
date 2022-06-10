"""Module extending BaseClasses.py for aLttP"""
from typing import Optional

from BaseClasses import Location, Item, ItemClassification


class ALttPLocation(Location):
    game: str = "A Link to the Past"

    def __init__(self, player: int, name: str = '', address=None, crystal: bool = False,
                 hint_text: Optional[str] = None, parent=None,
                 player_address=None):
        super(ALttPLocation, self).__init__(player, name, address, parent)
        self.crystal = crystal
        self.player_address = player_address
        self._hint_text: str = hint_text


class ALttPItem(Item):
    game: str = "A Link to the Past"
    dungeon = None

    def __init__(self, name, player, classification=ItemClassification.filler, type=None, item_code=None, pedestal_hint=None,
                 pedestal_credit=None, sick_kid_credit=None, zora_credit=None, witch_credit=None,
                 flute_boy_credit=None, hint_text=None):
        super(ALttPItem, self).__init__(name, classification, item_code, player)
        self.type = type
        self._pedestal_hint_text = pedestal_hint
        self.pedestal_credit_text = pedestal_credit
        self.sickkid_credit_text = sick_kid_credit
        self.zora_credit_text = zora_credit
        self.magicshop_credit_text = witch_credit
        self.fluteboy_credit_text = flute_boy_credit
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