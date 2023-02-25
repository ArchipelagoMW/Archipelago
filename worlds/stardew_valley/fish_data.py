from typing import List, Tuple

from .game_item import FishItem

spring = ("Spring",)
summer = ("Summer",)
fall = ("Fall",)
winter = ("Winter",)
spring_summer = (*spring, *summer)
spring_fall = (*spring, *fall)
spring_winter = (*spring, *winter)
summer_fall = (*summer, *fall)
summer_winter = (*summer, *winter)
fall_winter = (*fall, *winter)
spring_summer_fall = (*spring, *summer, *fall)
spring_summer_winter = (*spring, *summer, *winter)
spring_fall_winter = (*spring, *fall, *winter)
all_seasons = (*spring, *summer, *fall, *winter)

town = ("Town",)
beach = ("Beach",)
mountain = ("Mountain",)
forest = ("Forest",)
secret_woods = ("Secret Woods",)
desert = ("The Desert",)
mines_20 = ("The Mines - Floor 20",)
mines_60 = ("The Mines - Floor 60",)
mines_100 = ("The Mines - Floor 100",)
sewers = ("Sewers",)
mutant_bug_lair = ("Mutant Bug Lair",)
witch_swamp = ("Witch's Swamp",)
ginger_island = ("Ginger Island",)
ginger_island_ocean = ginger_island
ginger_island_river = ginger_island
pirate_cove = ginger_island
night_market = beach
lakes = (*mountain, *secret_woods, *sewers)
ocean = beach
rivers = (*town, *forest)
rivers_secret_woods = (*rivers, *secret_woods)
forest_mountain = (*forest, *mountain)
rivers_mountain_lake = (*town, *forest, *mountain)
mines_20_60 = (*mines_20, *mines_60)

all_fish_items: List[FishItem] = []


def fish(name: str, item_id: int, locations: Tuple[str, ...], seasons: Tuple[str, ...], difficulty: int) -> FishItem:
    fish_item = FishItem(name, item_id, locations, seasons, difficulty)
    all_fish_items.append(fish_item)
    return fish_item


carp = fish("Carp", 142, lakes, all_seasons, 15)
herring = fish("Herring", 147, ocean, spring_winter, 25)
smallmouth_bass = fish("Smallmouth Bass", 137, rivers, spring_fall, 28)
anchovy = fish("Anchovy", 129, ocean, spring_fall, 30)
sardine = fish("Sardine", 131, ocean, spring_fall_winter, 30)
sunfish = fish("Sunfish", 145, rivers, spring_summer, 30)
perch = fish("Perch", 141, rivers_mountain_lake, winter, 35)
chub = fish("Chub", 702, forest_mountain, all_seasons, 35)
bream = fish("Bream", 132, rivers, all_seasons, 35)
red_snapper = fish("Red Snapper", 150, ocean, summer_fall, 40)
sea_cucumber = fish("Sea Cucumber", 154, ocean, fall_winter, 40)
rainbow_trout = fish("Rainbow Trout", 138, rivers_mountain_lake, summer, 45)
walleye = fish("Walleye", 140, rivers_mountain_lake, fall, 45)
shad = fish("Shad", 706, rivers, spring_summer_fall, 45)
bullhead = fish("Bullhead", 700, mountain, all_seasons, 46)
largemouth_bass = fish("Largemouth Bass", 136, mountain, all_seasons, 50)
salmon = fish("Salmon", 139, rivers, fall, 50)
ghostfish = fish("Ghostfish", 156, mines_20_60, all_seasons, 50)
tilapia = fish("Tilapia", 701, ocean, summer_fall, 50)
woodskip = fish("Woodskip", 734, secret_woods, all_seasons, 50)
flounder = fish("Flounder", 267, ocean, spring_summer, 50)
halibut = fish("Halibut", 708, ocean, spring_summer_winter, 50)
lionfish = fish("Lionfish", 837, ginger_island_ocean, all_seasons, 50)
slimejack = fish("Slimejack", 796, mutant_bug_lair, all_seasons, 55)
midnight_carp = fish("Midnight Carp", 269, forest_mountain, fall_winter, 55)
red_mullet = fish("Red Mullet", 146, ocean, summer_winter, 55)
pike = fish("Pike", 144, rivers, summer_winter, 60)
tiger_trout = fish("Tiger Trout", 699, rivers, fall_winter, 60)
blue_discus = fish("Blue Discus", 838, ginger_island_river, all_seasons, 60)
albacore = fish("Albacore", 705, ocean, fall_winter, 60)
sandfish = fish("Sandfish", 164, desert, all_seasons, 65)
stonefish = fish("Stonefish", 158, mines_20, all_seasons, 65)
tuna = fish("Tuna", 130, ocean, summer_winter, 70)
eel = fish("Eel", 148, ocean, spring_fall, 70)
catfish = fish("Catfish", 143, rivers_secret_woods, spring_fall, 75)
squid = fish("Squid", 151, ocean, winter, 75)
sturgeon = fish("Sturgeon", 698, mountain, summer_winter, 78)
dorado = fish("Dorado", 704, forest, summer, 78)
pufferfish = fish("Pufferfish", 128, ocean, summer, 80)
void_salmon = fish("Void Salmon", 795, witch_swamp, all_seasons, 80)
super_cucumber = fish("Super Cucumber", 155, ocean, summer_fall, 80)
stingray = fish("Stingray", 836, pirate_cove, all_seasons, 80)
ice_pip = fish("Ice Pip", 161, mines_60, all_seasons, 85)
lingcod = fish("Lingcod", 707, rivers_mountain_lake, winter, 85)
scorpion_carp = fish("Scorpion Carp", 165, desert, all_seasons, 90)
lava_eel = fish("Lava Eel", 162, mines_100, all_seasons, 90)
octopus = fish("Octopus", 149, ocean, summer, 95)

midnight_squid = fish("Midnight Squid", 798, night_market, winter, 55)
spook_fish = fish("Spook Fish", 799, night_market, winter, 60)
blob_fish = fish("Blobfish", 800, night_market, winter, 75)

crimsonfish = fish("Crimsonfish", 159, ocean, summer, 95)
angler = fish("Angler", 160, town, fall, 85)
legend = fish("Legend", 163, mountain, spring, 110)
glacierfish = fish("Glacierfish", 775, forest, winter, 100)
mutant_carp = fish("Mutant Carp", 682, sewers, all_seasons, 80)

crayfish = fish("Crayfish", 716, rivers, all_seasons, -1)
snail = fish("Snail", 721, rivers, all_seasons, -1)
periwinkle = fish("Periwinkle", 722, rivers, all_seasons, -1)
lobster = fish("Lobster", 715, ocean, all_seasons, -1)
clam = fish("Clam", 372, ocean, all_seasons, -1)
crab = fish("Crab", 717, ocean, all_seasons, -1)
cockle = fish("Cockle", 718, ocean, all_seasons, -1)
mussel = fish("Mussel", 719, ocean, all_seasons, -1)
shrimp = fish("Shrimp", 720, ocean, all_seasons, -1)
oyster = fish("Oyster", 723, ocean, all_seasons, -1)

legendary_fish = [crimsonfish, angler, legend, glacierfish, mutant_carp]
special_fish = [*legendary_fish, blob_fish, lava_eel, octopus, scorpion_carp, ice_pip, super_cucumber, dorado]

all_fish_items_by_name = {fish.name: fish for fish in all_fish_items}
all_fish_items_by_id = {fish.item_id: fish for fish in all_fish_items}
