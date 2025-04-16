from BaseClasses import Location
from Options import ProgressionBalancing, Accessibility, LocalItems, NonLocalItems, StartInventory, StartHints, \
    StartLocationHints, ExcludeLocations, PriorityLocations, ItemLinks
from worlds.pokepark.logic import generate_regions
from worlds.pokepark.options import Powers, RandomStartingZones, Goal, PokeparkOptions


class PokeparkLocation(Location):
    game: str = "PokePark"


class DummyWorld:
    def __init__(self):
        self.options = PokeparkOptions(
            progression_balancing=ProgressionBalancing.default,
            accessibility=Accessibility.default,
            local_items=LocalItems.default,
            non_local_items=NonLocalItems.default,
            start_inventory=StartInventory.default,
            start_hints=StartHints.default,
            start_location_hints=StartLocationHints.default,
            exclude_locations=ExcludeLocations.default,
            priority_locations=PriorityLocations.default,
            item_links=ItemLinks.default,
            power_randomizer=Powers.default,
            starting_zone=RandomStartingZones.default,
            goal=Goal(0),
        )


REGIONS = generate_regions(world=DummyWorld(), get_all_locations=True)

ALL_LOCATIONS_TABLE: dict[str, int] = {}
for region in REGIONS:
    for friendship in region.friendship_locations:
        ALL_LOCATIONS_TABLE[f"{region.display} - {friendship.name}"] = friendship.id
    for unlock in region.unlock_location:
        ALL_LOCATIONS_TABLE[f"{region.display} - {unlock.name}"] = unlock.id
    for minigame in region.minigame_location:
        ALL_LOCATIONS_TABLE[f"{region.display} - {minigame.name}"] = minigame.id
    for ability in region.quest_locations:
        ALL_LOCATIONS_TABLE[f"{region.display} - {ability.name}"] = ability.id
