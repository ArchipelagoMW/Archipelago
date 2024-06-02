"""
This module servies as an entrypoint into the Trails in the Sky the 3rd AP world.
"""
from typing import ClassVar, Dict, Set

from worlds.AutoWorld import WebWorld, World
from .items import TitsThe3rdItem
from .locations import create_locations as tits_the_third_create_locations
from .options import TitsThe3rdOptions
from .regions import create_regions as tits_the_third_create_regions
from .settings import TitsThe3rdSettings
from .web import TitsThe3rdWeb

class TitsThe3rdWorld(World):
    """
    Trails in the Sky the 3rd is a JRPG from the "Trails of" / "Kiseki" series,
    released in 2007 and developed by Nihon Falcom. Embark on an emotional rollercoaster
    following Father Kevin Graham and Ries Argent during their journey to escape the
    mysterious dimension of Phantasma. It is highly recommended to pick up the first two
    games before playing this one, Trails in the Sky FC / SC.
    """
    game: str = "Trails in the Sky the 3rd"
    options_dataclass = TitsThe3rdOptions
    options: TitsThe3rdOptions
    topology_present: bool = True
    settings: ClassVar[TitsThe3rdSettings]
    web: WebWorld = TitsThe3rdWeb()
    base_id: int = 1954308624560

    item_name_groups: Dict[str, Set[str]] = {}
    location_name_groups: Dict[str, Set[str]] = {}
    item_name_to_id: Dict[str, int] = {"Dummy Item": base_id}
    location_name_to_id: Dict[str, int] = {"Dummy Location": base_id}

    def create_item(self, name: str) -> TitsThe3rdItem:
        """Create a Trails in the Sky the 3rd item for this player"""
        item_classification = TitsThe3rdItem.get_item_classfication(name)
        return TitsThe3rdItem(name, item_classification, self.item_name_to_id[name], self.player)

    def create_event(self, name: str) -> TitsThe3rdItem:
        """Create a Trails in the Sky the 3rd event for this player"""
        return TitsThe3rdItem(name, True, None, self.player)

    def create_regions(self) -> None:
        """Define regions and locations for Trails in the Sky the 3rd AP"""
        tits_the_third_create_regions(self.multiworld, self.player)
        tits_the_third_create_locations(self.multiworld, self.player, self.location_name_to_id)

    def create_items(self) -> None:
        """Define items for Trails in the Sky the 3rd AP"""
        dummy_item = self.create_item("Dummy Item")
        self.multiworld.itempool.append(dummy_item)

    def set_rules(self) -> None:
        """Set remaining rules."""
        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has("Dummy Item", self.player)
