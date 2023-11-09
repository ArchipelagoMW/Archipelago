from dataclasses import dataclass
from typing import List, Tuple, Union, Optional, Set

from . import season_data as season
from .game_item import GameItem
from ..strings.fish_names import Fish, SVEFish
from ..strings.region_names import Region, SVERegion
from ..mods.mod_data import ModNames


@dataclass(frozen=True)
class FishItem(GameItem):
    locations: Tuple[str]
    seasons: Tuple[str]
    difficulty: int
    legendary: bool
    extended_family: bool
    mod_name: Optional[str] = None

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

crimson_badlands = (SVERegion.crimson_badlands,)
shearwater = (SVERegion.shearwater,)
highlands = (SVERegion.highlands,)
sprite_spring = (SVERegion.sprite_spring,)
fable_reef = (SVERegion.fable_reef,)
vineyard = (SVERegion.blue_moon_vineyard,)

all_fish: List[FishItem] = []


def create_fish(name: str, item_id: int, locations: Tuple[str, ...], seasons: Union[str, Tuple[str, ...]],
                difficulty: int, legendary: bool = False, extended_family: bool = False, mod_name: Optional[str] = None) -> FishItem:
    if isinstance(seasons, str):
        seasons = (seasons,)

    fish_item = FishItem(name, item_id, locations, seasons, difficulty, legendary, extended_family, mod_name)
    all_fish.append(fish_item)
    return fish_item


albacore = create_fish("Albacore", 705, ocean, (season.fall, season.winter), 60)
anchovy = create_fish("Anchovy", 129, ocean, (season.spring, season.fall), 30)
blue_discus = create_fish("Blue Discus", 838, ginger_island_river, season.all_seasons, 60)
bream = create_fish("Bream", 132, town_river + forest_river, season.all_seasons, 35)
bullhead = create_fish("Bullhead", 700, mountain_lake, season.all_seasons, 46)
carp = create_fish(Fish.carp, 142, mountain_lake + secret_woods + sewers + mutant_bug_lair, season.not_winter, 15)
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

angler = create_fish(Fish.angler, 160, town_river, season.fall, 85, True, False)
crimsonfish = create_fish(Fish.crimsonfish, 159, ocean, season.summer, 95, True, False)
glacierfish = create_fish(Fish.glacierfish, 775, forest_river, season.winter, 100, True, False)
legend = create_fish(Fish.legend, 163, mountain_lake, season.spring, 110, True, False)
mutant_carp = create_fish(Fish.mutant_carp, 682, sewers, season.all_seasons, 80, True, False)

ms_angler = create_fish(Fish.ms_angler, 160, town_river, season.fall, 85, True, True)
son_of_crimsonfish = create_fish(Fish.son_of_crimsonfish, 159, ocean, season.summer, 95, True, True)
glacierfish_jr = create_fish(Fish.glacierfish_jr, 775, forest_river, season.winter, 100, True, True)
legend_ii = create_fish(Fish.legend_ii, 163, mountain_lake, season.spring, 110, True, True)
radioactive_carp = create_fish(Fish.radioactive_carp, 682, sewers, season.all_seasons, 80, True, True)

baby_lunaloo = create_fish(SVEFish.baby_lunaloo, 3006, ginger_island_ocean, season.all_seasons, 15, mod_name=ModNames.sve)
bonefish = create_fish(SVEFish.bonefish, 3013, crimson_badlands, season.all_seasons, 70, mod_name=ModNames.sve)
bull_trout = create_fish(SVEFish.bull_trout, 3014, forest_river, season.not_spring, 45, mod_name=ModNames.sve)
butterfish = create_fish(SVEFish.butterfish, 3015, shearwater, season.not_winter, 75, mod_name=ModNames.sve)
clownfish = create_fish(SVEFish.clownfish, 3016, ginger_island_ocean, season.all_seasons, 45, mod_name=ModNames.sve)
daggerfish = create_fish(SVEFish.daggerfish, 3017, highlands, season.all_seasons, 50, mod_name=ModNames.sve)
frog = create_fish(SVEFish.frog, 3023, mountain_lake, (season.spring, season.summer), 70, mod_name=ModNames.sve)
gemfish = create_fish(SVEFish.gemfish, 3027, highlands, season.all_seasons, 100, mod_name=ModNames.sve)
goldenfish = create_fish(SVEFish.goldenfish, 3031, sprite_spring, season.all_seasons, 60, mod_name=ModNames.sve)
grass_carp = create_fish(SVEFish.grass_carp, 3034, secret_woods, (season.spring, season.summer), 85, mod_name=ModNames.sve)
king_salmon = create_fish(SVEFish.king_salmon, 3044, forest_river, (season.spring, season.summer), 80, mod_name=ModNames.sve)
kittyfish = create_fish(SVEFish.kittyfish, 3045, shearwater, (season.fall, season.winter), 85, mod_name=ModNames.sve)
lunaloo = create_fish(SVEFish.lunaloo, 3049, ginger_island_ocean, season.all_seasons, 70, mod_name=ModNames.sve)
meteor_carp = create_fish(SVEFish.meteor_carp, 3051, sprite_spring, season.all_seasons, 80, mod_name=ModNames.sve)
minnow = create_fish(SVEFish.minnow, 3052, town_river, season.all_seasons, 1, mod_name=ModNames.sve)
puppyfish = create_fish(SVEFish.puppyfish, 3061, shearwater, season.not_winter, 85, mod_name=ModNames.sve)
radioactive_bass = create_fish(SVEFish.radioactive_bass, 3062, sewers, season.all_seasons, 90, mod_name=ModNames.sve)
seahorse = create_fish(SVEFish.seahorse, 3068, ginger_island_ocean, season.all_seasons, 25, mod_name=ModNames.sve)
shiny_lunaloo = create_fish(SVEFish.shiny_lunaloo, 3070, ginger_island_ocean, season.all_seasons, 110, mod_name=ModNames.sve)
snatcher_worm = create_fish(SVEFish.snatcher_worm, 3075, mutant_bug_lair, season.all_seasons, 75, mod_name=ModNames.sve)
starfish = create_fish(SVEFish.starfish, 3079, ginger_island_ocean, season.all_seasons, 75, mod_name=ModNames.sve)
torpedo_trout = create_fish(SVEFish.torpedo_trout, 3084, fable_reef, season.all_seasons, 70, mod_name=ModNames.sve)
undeadfish = create_fish(SVEFish.undeadfish, 3085, crimson_badlands, season.all_seasons, 80, mod_name=ModNames.sve)
void_eel = create_fish(SVEFish.void_eel, 3087, witch_swamp, season.all_seasons, 100, mod_name=ModNames.sve)
water_grub = create_fish(SVEFish.water_grub, 3094, mutant_bug_lair, season.all_seasons, 60, mod_name=ModNames.sve)
sea_sponge = create_fish(SVEFish.sea_sponge, 3067, ginger_island_ocean, season.all_seasons, 40, mod_name=ModNames.sve)
dulse_seaweed = create_fish(SVEFish.dulse_seaweed, 3020, vineyard, season.all_seasons, 50, mod_name=ModNames.sve)


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

legendary_fish = [angler, crimsonfish, glacierfish, legend, mutant_carp]
extended_family = [ms_angler, son_of_crimsonfish, glacierfish_jr, legend_ii, radioactive_carp]
special_fish = [*legendary_fish, blob_fish, lava_eel, octopus, scorpion_carp, ice_pip, super_cucumber, dorado]
island_fish = [lionfish, blue_discus, stingray, *extended_family]

all_fish_by_name = {fish.name: fish for fish in all_fish}


def get_fish_for_mods(mods: Set[str]) -> List[FishItem]:
    fish_for_mods = []
    for fish in all_fish:
        if fish.mod_name and fish.mod_name not in mods:
            continue
        fish_for_mods.append(fish)
    return fish_for_mods
