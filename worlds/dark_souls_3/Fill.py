from typing import List, Optional, Set, Union

from BaseClasses import ItemClassification, LocationProgressType, MultiWorld

from .Items import item_dictionary
from .Locations import location_tables

class Fill:
    """A utility class for prefilling items to provide smoother progression."""

    world: "DarkSouls3World"
    """The world that's running this fill."""

    regions: List[str]
    """A list of region names to which prefilled items might be randomized.

    This is roughly in order from earlier to later game, although when the player actually reaches
    each region is highly dependent on their seed and settings. This ordering is roughly based on
    where upgrade items become available in the base game.
    """

    @property
    def multiworld(self) -> MultiWorld:
        """The MultiWorld object for the currently generating multiworld."""
        return self.world.multiworld

    @property
    def player(self) -> int:
        """The ID of the player for which this world is being generated."""
        return self.world.player


    def __init__(self, world: "DarkSouls3World"):
        self.world = world
        self.regions = [
            "Cemetery of Ash",
            "Firelink Shrine",
            "High Wall of Lothric",
            "Undead Settlement",
            "Road of Sacrifices",
            "Farron Keep",
            "Cathedral of the Deep",
            "Catacombs of Carthus",
            "Smouldering Lake",
            "Irithyll of the Boreal Valley",
            "Irithyll Dungeon",
            # The first half of Painted World has one Titanite Slab but mostly Large Titanite Shards,
            # much like Irithyll Dungeon.
            "Painted World of Ariandel (Before Contraption)",
            "Anor Londo",
            "Profaned Capital",
            # The second half of Painted World has two Titanite Chunks and two Titanite Slabs, which
            # puts it on the low end of the post-Lothric Castle areas in terms of rewards.
            "Painted World of Ariandel (After Contraption)",
            "Lothric Castle",
            "Consumed King's Garden",
            "Untended Graves",
            "Grand Archives",
            "Archdragon Peak",
            "Kiln of the First Flame",
            # Both areas of DLC2 have premium rewards.
            "Dreg Heap",
            "Ringed City",
        ]


    def fill(
            self,
            name_or_names: Union[str, Set[str]],
            start: Optional[str] = None,
            through: Optional[str] = None,
            count: int = 0,
            no_excluded = False) -> None:
        """Fills the given item into open locations in the given region.

        This fills open slots from start through through, inclusive, ordered by how good their
        rewards are in the base game. If either start or through isn't passed, this fills from the
        beginning or through the end of the game, respectively.

        The name can be a set of names, in which case the items to place are chosen randomly from
        among all unplaced items with one of those names.

        If count is positive, this will place up to that many copies of the item. If it's negative,
        this will place all but that many copies with the expectation that the remainder will be
        placed in other worlds. If it's 0, this will place all remaining copies in the item pool.

        If there's only one world, negative counts will be treated as None.

        If no_excluded is True, this won't place items into excluded locations. This never places
        important items in excluded locations.
        """

        if isinstance(name_or_names, str):
            all_items = [
                item for item in self.multiworld.itempool
                if item.name == name_or_names and not item.location
            ]
        else:
            all_items = [
                item for item in self.multiworld.itempool
                if item.name in name_or_names and not item.location
            ]

        if count == 0 or count < 0 and len(self.multiworld.worlds) == 1:
            self.multiworld.random.shuffle(all_items)
            chosen_items = all_items
        else:
            if count < 0:
                count += len(all_items)
                if count < 1: return 
            chosen_items = self.multiworld.random.sample(all_items, k = min(count, len(all_items)))
        if len(chosen_items) == 0: return

        if start: assert start in self.regions
        if through: assert through in self.regions
        region_start = self.regions.index(start) if start else 0
        region_end = self.regions.index(through) + 1 if through else -1
        selected_regions = self.regions[region_start:region_end]

        # All items are expected to have the same properties, so we choose one arbitrarily
        item = chosen_items[0]
        filler = item.classification == ItemClassification.filler and not no_excluded
        possible_locations = [
            location for location in (
                self.multiworld.get_location(location.name, self.player)
                for region in selected_regions
                for location in location_tables[region]
                if (
                    self.world.is_location_available(location)
                    and not location.missable
                    and not location.conditional
                    and not (location.shop and item.souls)
                )
            )
            # Don't put important items in excluded locations.
            if not location.item
            and (filler or location.progress_type != LocationProgressType.EXCLUDED)
        ]
        if len(possible_locations) == 0: return
        if len(possible_locations) < len(chosen_items):
            chosen_items = self.multiworld.random.sample(chosen_items, k = len(possible_locations))

        locations = self.multiworld.random.sample(possible_locations, k = len(chosen_items))
        for item, location in zip(chosen_items, locations):
            location.place_locked_item(item)


    def save(self):
        """Removes all allocated items from the multiworld itempool."""
        self.multiworld.itempool = [
            item for item in self.multiworld.itempool
            if not item.location
        ]
