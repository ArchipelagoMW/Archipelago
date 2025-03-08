from BaseClasses import Location
from worlds.pokepark.logic import REGIONS


class PokeparkLocation(Location):
    game: str = "PokePark"

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
