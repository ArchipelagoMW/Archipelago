from dataclasses import dataclass
from typing import List, Tuple, Union, Optional

from . import season_data as season
from .game_item import GameItem
from ..strings.region_names import Region


@dataclass(frozen=True)
class FishItem(GameItem):
    locations: Tuple[str]
    seasons: Tuple[str]
    difficulty: int
    mod_name: Optional[str]

    def __repr__(self):
        return f"{self.name} [{self.item_id}] (Locations: {self.locations} |" \
               f" Seasons: {self.seasons} |" \
               f" Difficulty: {self.difficulty}) |" \
               f"Mod: {self.mod_name}"


fresh_water = (Region.farm, Region.forest, Region.town, Region.mountain)
ocean = (Region.beach,)
town_river = (Region.town,)
mountain_lake = (Region.mountain,)
forest_pond = (Region.forest,)
forest_river = (Region.forest,)
secret_woods = (Region.secret_woods,)
mines_floor_20 = (Region.mines_floor_20,)
mines_floor_60 = (Region.mines_floor_60,)
mines_floor_100 = (Region.mines_floor_100,)
sewers = (Region.sewer,)
desert = (Region.desert,)
mutant_bug_lair = (Region.mutant_bug_lair,)
witch_swamp = (Region.witch_swamp,)
night_market = (Region.beach,)
ginger_island_ocean = (Region.island_south, Region.island_west)
ginger_island_river = (Region.island_west,)
pirate_cove = (Region.pirate_cove,)

all_fish: List[FishItem] = []


def create_fish(name: str, item_id: int, locations: Tuple[str, ...], seasons: Union[str, Tuple[str, ...]],
                difficulty: int, mod_name: Optional[str] = None) -> FishItem:
    if isinstance(seasons, str):
        seasons = (seasons,)

    fish_item = FishItem(name, item_id, locations, seasons, difficulty, mod_name)
    all_fish.append(fish_item)
    return fish_item


albacore = create_fish("Albacore", 705, ocean, (season.fall, season.winter), 60)
anchovy = create_fish("Anchovy", 129, ocean, (season.spring, season.fall), 30)
blue_discus = create_fish("Blue Discus", 838, ginger_island_river, season.all_seasons, 60)
bream = create_fish("Bream", 132, town_river + forest_river, season.all_seasons, 35)
bullhead = create_fish("Bullhead", 700, mountain_lake, season.all_seasons, 46)
carp = create_fish("Carp", 142, mountain_lake + secret_woods + sewers + mutant_bug_lair, season.not_winter, 15)
catfish = create_fish("Catfish", 143, town_river + forest_river + secret_woods, (season.spring, season.fall), 75)
chub = create_fish("Chub", 702, forest_river + mountain_lake, season.all_seasons, 35)
dorado = create_fish("Dorado", 704, forest_river, season.summer, 78)
eel = create_fish("Eel", 148, ocean, (season.spring, season.fall), 70)
flounder = create_fish("Flounder", 267, ocean, (season.spring, season.summer), 50)
ghostfish = create_fish("Ghostfish", 156, mines_floor_20 + mines_floor_60, season.all_seasons, 50)
halibut = create_fish("Halibut", 708, ocean, season.not_fall, 50)
herring = create_fish("Herring", 147, ocean, (season.spring, season.winter), 25)
ice_pip = create_fish("Ice Pip", 161, mines_floor_60, season.all_seasons, 85)
largemouth_bass = create_fish("Largemouth Bass", 136, mountain_lake, season.all_seasons, 50)
lava_eel = create_fish("Lava Eel", 162, mines_floor_100, season.all_seasons, 90)
lingcod = create_fish("Lingcod", 707, town_river + forest_river + mountain_lake, season.winter, 85)
lionfish = create_fish("Lionfish", 837, ginger_island_ocean, season.all_seasons, 50)
midnight_carp = create_fish("Midnight Carp", 269, mountain_lake + forest_pond + ginger_island_river,
                            (season.fall, season.winter), 55)
octopus = create_fish("Octopus", 149, ocean, season.summer, 95)
perch = create_fish("Perch", 141, town_river + forest_river + forest_pond + mountain_lake, season.winter, 35)
pike = create_fish("Pike", 144, town_river + forest_river + forest_pond, (season.summer, season.winter), 60)
pufferfish = create_fish("Pufferfish", 128, ocean + ginger_island_ocean, season.summer, 80)
rainbow_trout = create_fish("Rainbow Trout", 138, town_river + forest_river + mountain_lake, season.summer, 45)
red_mullet = create_fish("Red Mullet", 146, ocean, (season.summer, season.winter), 55)
red_snapper = create_fish("Red Snapper", 150, ocean, (season.summer, season.fall), 40)
salmon = create_fish("Salmon", 139, town_river + forest_river, season.fall, 50)
sandfish = create_fish("Sandfish", 164, desert, season.all_seasons, 65)
sardine = create_fish("Sardine", 131, ocean, (season.spring, season.fall, season.winter), 30)
scorpion_carp = create_fish("Scorpion Carp", 165, desert, season.all_seasons, 90)
sea_cucumber = create_fish("Sea Cucumber", 154, ocean, (season.fall, season.winter), 40)
shad = create_fish("Shad", 706, town_river + forest_river, season.not_winter, 45)
slimejack = create_fish("Slimejack", 796, mutant_bug_lair, season.all_seasons, 55)
smallmouth_bass = create_fish("Smallmouth Bass", 137, town_river + forest_river, (season.spring, season.fall), 28)
squid = create_fish("Squid", 151, ocean, season.winter, 75)
stingray = create_fish("Stingray", 836, pirate_cove, season.all_seasons, 80)
stonefish = create_fish("Stonefish", 158, mines_floor_20, season.all_seasons, 65)
sturgeon = create_fish("Sturgeon", 698, mountain_lake, (season.summer, season.winter), 78)
sunfish = create_fish("Sunfish", 145, town_river + forest_river, (season.spring, season.summer), 30)
super_cucumber = create_fish("Super Cucumber", 155, ocean + ginger_island_ocean, (season.summer, season.fall), 80)
tiger_trout = create_fish("Tiger Trout", 699, town_river + forest_river, (season.fall, season.winter), 60)
tilapia = create_fish("Tilapia", 701, ocean + ginger_island_ocean, (season.summer, season.fall), 50)
# Tuna has different seasons on ginger island. Should be changed when the whole fish thing is refactored
tuna = create_fish("Tuna", 130, ocean + ginger_island_ocean, (season.summer, season.winter), 70)
void_salmon = create_fish("Void Salmon", 795, witch_swamp, season.all_seasons, 80)
walleye = create_fish("Walleye", 140, town_river + forest_river + forest_pond + mountain_lake, season.fall, 45)
woodskip = create_fish("Woodskip", 734, secret_woods, season.all_seasons, 50)

blob_fish = create_fish("Blobfish", 800, night_market, season.winter, 75)
midnight_squid = create_fish("Midnight Squid", 798, night_market, season.winter, 55)
spook_fish = create_fish("Spook Fish", 799, night_market, season.winter, 60)

angler = create_fish("Angler", 160, town_river, season.fall, 85)
crimsonfish = create_fish("Crimsonfish", 159, ocean, season.summer, 95)
glacierfish = create_fish("Glacierfish", 775, forest_river, season.winter, 100)
legend = create_fish("Legend", 163, mountain_lake, season.spring, 110)
mutant_carp = create_fish("Mutant Carp", 682, sewers, season.all_seasons, 80)

clam = create_fish("Clam", 372, ocean, season.all_seasons, -1)
cockle = create_fish("Cockle", 718, ocean, season.all_seasons, -1)
crab = create_fish("Crab", 717, ocean, season.all_seasons, -1)
crayfish = create_fish("Crayfish", 716, fresh_water, season.all_seasons, -1)
lobster = create_fish("Lobster", 715, ocean, season.all_seasons, -1)
mussel = create_fish("Mussel", 719, ocean, season.all_seasons, -1)
oyster = create_fish("Oyster", 723, ocean, season.all_seasons, -1)
periwinkle = create_fish("Periwinkle", 722, fresh_water, season.all_seasons, -1)
shrimp = create_fish("Shrimp", 720, ocean, season.all_seasons, -1)
snail = create_fish("Snail", 721, fresh_water, season.all_seasons, -1)

legendary_fish = [crimsonfish, angler, legend, glacierfish, mutant_carp]
special_fish = [*legendary_fish, blob_fish, lava_eel, octopus, scorpion_carp, ice_pip, super_cucumber, dorado]
island_fish = [lionfish, blue_discus, stingray]

all_fish_by_name = {fish.name: fish for fish in all_fish}
