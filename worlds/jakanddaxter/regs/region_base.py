from typing import Iterable
from BaseClasses import MultiWorld, Region
from ..game_id import jak1_name
from ..locations import JakAndDaxterLocation, location_table
from ..locs import (orb_locations as orbs,
                    cell_locations as cells,
                    scout_locations as scouts,
                    special_locations as specials,
                    orb_cache_locations as caches)
from worlds.generic.Rules import CollectionRule


class JakAndDaxterRegion(Region):
    """
    Holds region information such as name, level name, number of orbs available, etc.
    We especially need orb counts to be tracked because we need to know when you can
    afford the Citizen and Oracle orb payments for more checks.
    """
    game: str = jak1_name
    level_name: str
    orb_count: int
    location_count: int = 0

    def __init__(self, name: str, player: int, multiworld: MultiWorld, level_name: str = "", orb_count: int = 0):
        formatted_name = f"{level_name} {name}".strip()
        super().__init__(formatted_name, player, multiworld)
        self.level_name = level_name
        self.orb_count = orb_count

    def add_cell_locations(self, locations: Iterable[int], access_rule: CollectionRule | None = None) -> None:
        """
        Adds a Power Cell Location to this region with the given access rule.
        Converts Game ID's to AP ID's for you.
        """
        for loc in locations:
            ap_id = cells.to_ap_id(loc)
            self.add_jak_location(ap_id, location_table[ap_id], access_rule)

    def add_fly_locations(self, locations: Iterable[int], access_rule: CollectionRule | None = None) -> None:
        """
        Adds a Scout Fly Location to this region with the given access rule.
        Converts Game ID's to AP ID's for you.
        """
        for loc in locations:
            ap_id = scouts.to_ap_id(loc)
            self.add_jak_location(ap_id, location_table[ap_id], access_rule)

    def add_special_locations(self, locations: Iterable[int], access_rule: CollectionRule | None = None) -> None:
        """
        Adds a Special Location to this region with the given access rule.
        Converts Game ID's to AP ID's for you.
        Special Locations should be matched alongside their respective
        Power Cell Locations, so you get 2 unlocks for these rather than 1.
        """
        for loc in locations:
            ap_id = specials.to_ap_id(loc)
            self.add_jak_location(ap_id, location_table[ap_id], access_rule)

    def add_cache_locations(self, locations: Iterable[int], access_rule: CollectionRule | None = None) -> None:
        """
        Adds an Orb Cache Location to this region with the given access rule.
        Converts Game ID's to AP ID's for you.
        """
        for loc in locations:
            ap_id = caches.to_ap_id(loc)
            self.add_jak_location(ap_id, location_table[ap_id], access_rule)

    def add_orb_locations(self, level_index: int, bundle_index: int, access_rule: CollectionRule | None = None) -> None:
        """
        Adds Orb Bundle Locations to this region equal to `bundle_count`. Used only when Per-Level Orbsanity is enabled.
        The orb factory class will handle AP ID enumeration.
        """
        bundle_address = orbs.create_address(level_index, bundle_index)
        location = JakAndDaxterLocation(self.player,
                                        f"{self.level_name} Orb Bundle {bundle_index + 1}".strip(),
                                        orbs.to_ap_id(bundle_address),
                                        self)
        if access_rule:
            location.access_rule = access_rule
        self.locations.append(location)
        self.location_count += 1

    def add_jak_location(self, ap_id: int, name: str, access_rule: CollectionRule | None = None) -> None:
        """
        Helper function to add Locations. Not to be used directly.
        """
        location = JakAndDaxterLocation(self.player, name, ap_id, self)
        if access_rule:
            location.access_rule = access_rule
        self.locations.append(location)
        self.location_count += 1
