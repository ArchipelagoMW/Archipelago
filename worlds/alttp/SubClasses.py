"""Module extending BaseClasses.py for aLttP"""
from typing import Optional
from enum import IntEnum

from BaseClasses import Location, Item, ItemClassification, Region, MultiWorld


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


class LTTPRegionType(IntEnum):
    LightWorld = 1
    DarkWorld = 2
    Cave = 3  # also houses
    Dungeon = 4

    @property
    def is_indoors(self) -> bool:
        """Shorthand for checking if Cave or Dungeon"""
        return self in (LTTPRegionType.Cave, LTTPRegionType.Dungeon)


class LTTPRegion(Region):
    type: LTTPRegionType

    def __init__(self, name: str, type_: LTTPRegionType, hint: str, player: int, multiworld: MultiWorld):
        super().__init__(name, player, multiworld, hint)
        self.type = type_

    @property
    def get_entrance(self):
        for entrance in self.entrances:
            if entrance.parent_region.type in (LTTPRegionType.DarkWorld, LTTPRegionType.LightWorld):
                return entrance
        for entrance in self.entrances:
            return entrance.parent_region.get_entrance
