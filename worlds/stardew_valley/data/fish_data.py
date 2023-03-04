from typing import List, Tuple

from worlds.stardew_valley.game_item import FishItem
from . import region_data as region, season_data as season

fresh_water = (region.farm, region.forest, region.town, region.mountain)
ocean = (region.beach,)
town_river = (region.town,)
mountain_lake = (region.mountain,)
forest_pond = (region.forest,)
forest_river = (region.forest,)
secret_woods = (region.secret_woods,)
mines_floor_20 = (region.mines_floor_20,)
mines_floor_60 = (region.mines_floor_60,)
mines_floor_100 = (region.mines_floor_100,)
sewers = (region.sewers,)
desert = (region.desert,)
mutant_bug_lair = (region.mutant_bug_lair,)
witch_swamp = (region.witch_swamp,)
night_market = (region.beach,)
ginder_island_ocean = (region.ginger_island,)
ginger_island_river = (region.ginger_island,)
pirate_cove = (region.ginger_island,)
all_fish_items: List[FishItem] = []


def fish(name: str, item_id: int, locations: Tuple[str, ...], seasons: Tuple[str, ...], difficulty: int) -> FishItem:
    if isinstance(seasons, str):
        seasons = (seasons,)

    fish_item = FishItem(name, item_id, locations, seasons, difficulty)
    all_fish_items.append(fish_item)
    return fish_item


albacore = fish("Albacore", 705, ocean, (season.fall, season.winter), 60)
anchovy = fish("Anchovy", 129, ocean, (season.spring, season.fall), 30)
blue_discus = fish("Blue Discus", 838, ginger_island_river, season.all_seasons, 60)
bream = fish("Bream", 132, town_river + forest_river, season.all_seasons, 35)
bullhead = fish("Bullhead", 700, mountain_lake, season.all_seasons, 46)
carp = fish("Carp", 142, mountain_lake + secret_woods + sewers + mutant_bug_lair, season.not_winter, 15)
catfish = fish("Catfish", 143, town_river + forest_river + secret_woods, (season.spring, season.fall), 75)
chub = fish("Chub", 702, forest_river + mountain_lake, season.all_seasons, 35)
dorado = fish("Dorado", 704, forest_river, season.summer, 78)
eel = fish("Eel", 148, ocean, (season.spring, season.fall), 70)
flounder = fish("Flounder", 267, ocean, (season.spring, season.summer), 50)
ghostfish = fish("Ghostfish", 156, mines_floor_20 + mines_floor_60, season.all_seasons, 50)
halibut = fish("Halibut", 708, ocean, season.not_fall, 50)
herring = fish("Herring", 147, ocean, (season.spring, season.winter), 25)
ice_pip = fish("Ice Pip", 161, mines_floor_60, season.all_seasons, 85)
largemouth_bass = fish("Largemouth Bass", 136, mountain_lake, season.all_seasons, 50)
lava_eel = fish("Lava Eel", 162, mines_floor_100, season.all_seasons, 90)
lingcod = fish("Lingcod", 707, town_river + forest_river + mountain_lake, season.winter, 85)
lionfish = fish("Lionfish", 837, ginder_island_ocean, season.all_seasons, 50)
midnight_carp = fish("Midnight Carp", 269, mountain_lake + forest_pond + ginger_island_river,
                     (season.fall, season.winter), 55)
octopus = fish("Octopus", 149, ocean, season.summer, 95)
perch = fish("Perch", 141, town_river + forest_river + forest_pond + mountain_lake, season.winter, 35)
pike = fish("Pike", 144, town_river + forest_river + forest_pond, (season.summer, season.winter), 60)
pufferfish = fish("Pufferfish", 128, ocean + ginder_island_ocean, season.summer, 80)
rainbow_trout = fish("Rainbow Trout", 138, town_river + forest_river + mountain_lake, season.summer, 45)
red_mullet = fish("Red Mullet", 146, ocean, (season.summer, season.winter), 55)
red_snapper = fish("Red Snapper", 150, ocean, (season.summer, season.fall), 40)
salmon = fish("Salmon", 139, town_river + forest_river, season.fall, 50)
sandfish = fish("Sandfish", 164, desert, season.all_seasons, 65)
sardine = fish("Sardine", 131, ocean, (season.spring, season.fall, season.winter), 30)
scorpion_carp = fish("Scorpion Carp", 165, desert, season.all_seasons, 90)
sea_cucumber = fish("Sea Cucumber", 154, ocean, (season.fall, season.winter), 40)
shad = fish("Shad", 706, town_river + forest_river, season.not_winter, 45)
slimejack = fish("Slimejack", 796, mutant_bug_lair, season.all_seasons, 55)
smallmouth_bass = fish("Smallmouth Bass", 137, town_river + forest_river, (season.spring, season.fall), 28)
squid = fish("Squid", 151, ocean, season.winter, 75)
stingray = fish("Stingray", 836, pirate_cove, season.all_seasons, 80)
stonefish = fish("Stonefish", 158, mines_floor_20, season.all_seasons, 65)
sturgeon = fish("Sturgeon", 698, mountain_lake, (season.summer, season.winter), 78)
sunfish = fish("Sunfish", 145, town_river + forest_river, (season.spring, season.summer), 30)
super_cucumber = fish("Super Cucumber", 155, ocean + ginder_island_ocean, (season.summer, season.fall), 80)
tiger_trout = fish("Tiger Trout", 699, town_river + forest_river, (season.fall, season.winter), 60)
tilapia = fish("Tilapia", 701, ocean + ginder_island_ocean, (season.summer, season.fall), 50)
tuna = fish("Tuna", 130, ocean + ginder_island_ocean, (season.summer, season.winter), 70)
void_salmon = fish("Void Salmon", 795, witch_swamp, season.all_seasons, 80)
walleye = fish("Walleye", 140, town_river + forest_river + forest_pond + mountain_lake, season.fall, 45)
woodskip = fish("Woodskip", 734, secret_woods, season.all_seasons, 50)

blob_fish = fish("Blobfish", 800, night_market, season.winter, 75)
midnight_squid = fish("Midnight Squid", 798, night_market, season.winter, 55)
spook_fish = fish("Spook Fish", 799, night_market, season.winter, 60)

angler = fish("Angler", 160, town_river, season.fall, 85)
crimsonfish = fish("Crimsonfish", 159, ocean, season.summer, 95)
glacierfish = fish("Glacierfish", 775, forest_river, season.winter, 100)
legend = fish("Legend", 163, mountain_lake, season.spring, 110)
mutant_carp = fish("Mutant Carp", 682, sewers, season.all_seasons, 80)

clam = fish("Clam", 372, ocean, season.all_seasons, -1)
cockle = fish("Cockle", 718, ocean, season.all_seasons, -1)
crab = fish("Crab", 717, ocean, season.all_seasons, -1)
crayfish = fish("Crayfish", 716, fresh_water, season.all_seasons, -1)
lobster = fish("Lobster", 715, ocean, season.all_seasons, -1)
mussel = fish("Mussel", 719, ocean, season.all_seasons, -1)
oyster = fish("Oyster", 723, ocean, season.all_seasons, -1)
periwinkle = fish("Periwinkle", 722, fresh_water, season.all_seasons, -1)
shrimp = fish("Shrimp", 720, ocean, season.all_seasons, -1)
snail = fish("Snail", 721, fresh_water, season.all_seasons, -1)

legendary_fish = [crimsonfish, angler, legend, glacierfish, mutant_carp]
special_fish = [*legendary_fish, blob_fish, lava_eel, octopus, scorpion_carp, ice_pip, super_cucumber, dorado]

all_fish_items_by_name = {fish.name: fish for fish in all_fish_items}
all_fish_items_by_id = {fish.item_id: fish for fish in all_fish_items}
