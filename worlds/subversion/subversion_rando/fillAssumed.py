import random
from typing import Optional

from .area_rando_types import DoorPairs
from .fillInterface import FillAlgorithm
from .item_data import Item, Items, unique_items
from .loadout import Loadout
from .location_data import Location, spacePortLocs, majorLocs, eTankLocs
from .location_weights import frequencies
from .solver import solve

_minor_logic_items = {
    Items.DamageAmp: 6,
    Items.AccelCharge: 6,
    Items.Energy: 16,
    Items.SpaceJumpBoost: 8,
    Items.SmallAmmo: 12,
    Items.LargeAmmo: 18
}
""" minors placed with logic """

_minor_non_logic_items = {
    Items.Refuel: 7,
    Items.SmallAmmo: 26,
}
""" items placed without logic """


class FillAssumed(FillAlgorithm):
    door_pairs: DoorPairs

    prog_items: list[Item]
    extra_items: list[Item]
    itemLists: list[list[Item]]

    def __init__(self, door_pairs: DoorPairs) -> None:
        self.door_pairs = door_pairs

        self.prog_items = sorted(unique_items)  # sort because iterating through set will not be the same every time
        assert len(self.prog_items) == len(set(self.prog_items)), "duplicate majors?"
        for it, n in _minor_logic_items.items():
            self.prog_items.extend([it for _ in range(n)])

        self.extra_items = []
        for it, n in _minor_non_logic_items.items():
            self.extra_items.extend([it for _ in range(n)])

        self.itemLists = [self.prog_items, self.extra_items]

    def _get_accessible_locations(self, loadout: Loadout) -> list[Location]:
        _, _, locs = solve(loadout.game, loadout)
        return locs

    def _get_available_locations(self, loadout: Loadout) -> list[Location]:
        return [loc for loc in self._get_accessible_locations(loadout) if loc["item"] is None]

    def _get_empty_locations(self, all_locations: dict[str, Location]) -> list[Location]:
        return [loc for loc in all_locations.values() if loc["item"] is None]

    def transform_spaceport(self, available_locations: list[Location], item_to_place: Item) -> list[Location]:
        """
        transform the distribution of locations to work against spaceport front-loading

        because 1 progression item in space port
        will lead to more progression items in spaceport
        """
        if item_to_place in unique_items:
            distribution = available_locations.copy()
            for loc in available_locations:
                if (
                    (loc["fullitemname"] == "Torpedo Bay" and item_to_place == Items.GravityBoots) or

                    # if the locking item is already placed, then it's safe to put progression in spaceport
                    (loc["fullitemname"] == "Extract Storage" and (
                        (Items.PowerBomb not in self.prog_items) or (
                            (Items.MetroidSuit not in self.prog_items) and
                            (Items.Hypercharge not in self.prog_items) and
                            ((Items.Ice not in self.prog_items) or (Items.Super not in self.prog_items))
                        )
                    )) or
                    (loc["fullitemname"] == "Ready Room" and Items.Super not in self.prog_items) or
                    (loc["fullitemname"] in {
                        "Forward Battery", "Aft Battery"
                    } and Items.Morph not in self.prog_items) or
                    (loc["fullitemname"] in {
                        "Docking Port 3", "Docking Port 4"
                    } and Items.Grapple not in self.prog_items) or
                    loc["fullitemname"] not in spacePortLocs
                ):
                    # number of copies can be tuned
                    distribution.append(loc)
                    if item_to_place in {Items.Morph, Items.GravityBoots, Items.Missile}:
                        distribution.append(loc)
                        distribution.append(loc)
            return distribution
        return available_locations

    @staticmethod
    def transform_mmb(available_locations: list[Location], item_to_place: Item) -> list[Location]:
        """ transform the distribution of locations for major minor bias """
        tr: list[Location] = []
        for loc in available_locations:
            if item_to_place in unique_items and loc["fullitemname"] in majorLocs:
                for _ in range(40):
                    tr.append(loc)
            elif item_to_place not in unique_items and loc["fullitemname"] not in majorLocs:
                for _ in range(7):
                    tr.append(loc)
            else:
                tr.append(loc)
        return tr

    @staticmethod
    def transform_away_from_early(available_locations: list[Location], item_to_place: Item) -> list[Location]:
        """ transform the distribution of locations to push progression away from early game areas """
        tr: list[Location] = []
        for loc in available_locations:
            tr.append(loc)
            tr.append(loc)
            loc_name = loc["fullitemname"]
            if item_to_place in unique_items:
                if frequencies[loc_name] < 183:
                    tr.append(loc)
                    if frequencies[loc_name] < 154:
                        tr.append(loc)
            else:  # not unique item
                if frequencies[loc_name] > 153:
                    tr.append(loc)
                    if frequencies[loc_name] > 182:
                        tr.append(loc)
        return tr

    @staticmethod
    def transform_mm(available_locations: list[Location], item_to_place: Item) -> list[Location]:
        """ transform the distribution of locations for major minor """
        major = item_to_place in unique_items or item_to_place == Items.Energy
        tr: list[Location] = []
        for loc in available_locations:
            location_major = (loc["fullitemname"] in majorLocs or loc["fullitemname"] in eTankLocs)
            if major and location_major:
                tr.append(loc)
            elif (not major) and (not location_major):
                tr.append(loc)
        return tr

    def choose_placement(self,
                         availableLocations: list[Location],
                         loadout: Loadout) -> Optional[tuple[Location, Item]]:
        """ returns (location to place an item, which item to place there) """

        from_items = (
            self.prog_items if len(self.prog_items) else (
                self.extra_items
            )
        )

        assert len(from_items), "tried to place item when placement algorithm has 0 items left in item pool"

        if loadout.game.options.fill_choice == "MM" and Items.Morph in from_items:
            # major/minor and haven't placed morph yet
            item_to_place = Items.Morph
        else:
            item_to_place = random.choice(from_items)

        # If Missile is placed before Super, it's very likely that
        # Super will be in Torpedo Bay or some other really early place.
        # So this makes sure that Super is placed before Missile.
        # Consider disabling this in door rando (when Super can't open pink door).
        if item_to_place == Items.Missile:
            if Items.Super in from_items:
                item_to_place = Items.Super
        #         print("Super placed before Missile")
        #     else:
        #         print("Missile placed before Super")

        from_items.remove(item_to_place)

        if from_items is self.prog_items:
            loadout = Loadout(loadout.game)
            for item in from_items:
                loadout.append(item)
            available_locations = self._get_available_locations(loadout)
        else:  # extra
            available_locations = self._get_empty_locations(loadout.game.all_locations)
        if len(available_locations) == 0:
            return None

        if loadout.game.options.fill_choice == "B":
            available_locations = self.transform_mmb(available_locations, item_to_place)
        elif loadout.game.options.fill_choice == "MM":
            available_locations = self.transform_mm(available_locations, item_to_place)
        if False:  # testing
            available_locations = self.transform_away_from_early(available_locations, item_to_place)  # type: ignore
        if len(available_locations) == 0:
            # print(f"DEBUG: failing to place {item_to_place.name}")
            return None

        available_locations = self.transform_spaceport(available_locations, item_to_place)
        # if item_to_place == Items.Morph:
        #     print(f"DEBUG: morph locations: {[loc['fullitemname'] for loc in available_locations]}")

        return random.choice(available_locations), item_to_place

    def count_items_remaining(self) -> int:
        return sum(len(li) for li in self.itemLists)

    def remove_from_pool(self, item: Item) -> None:
        """ removes this item from the item pool """
        pass  # removed in placement function
