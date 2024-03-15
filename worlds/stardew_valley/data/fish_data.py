from dataclasses import dataclass
from typing import List, Tuple, Union, Optional, Set

from . import season_data as season
from ..strings.fish_names import Fish, SVEFish, DistantLandsFish
from ..strings.region_names import Region, SVERegion
from ..mods.mod_data import ModNames


@dataclass(frozen=True)
class FishItem:
    name: str
    locations: Tuple[str]
    seasons: Tuple[str]
    difficulty: int
    legendary: bool
    extended_family: bool
    mod_name: Optional[str] = None

    def __repr__(self):
        return f"{self.name} (Locations: {self.locations} |" \
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
highlands = (SVERegion.highlands_outside,)
sprite_spring = (SVERegion.sprite_spring,)
fable_reef = (SVERegion.fable_reef,)
vineyard = (SVERegion.blue_moon_vineyard,)

all_fish: List[FishItem] = []


def create_fish(name: str, locations: Tuple[str, ...], seasons: Union[str, Tuple[str, ...]],
                difficulty: int, legendary: bool = False, extended_family: bool = False, mod_name: Optional[str] = None) -> FishItem:
    if isinstance(seasons, str):
        seasons = (seasons,)

    fish_item = FishItem(name, locations, seasons, difficulty, legendary, extended_family, mod_name)
    all_fish.append(fish_item)
    return fish_item


albacore = create_fish("Albacore", ocean, (season.fall, season.winter), 60)
anchovy = create_fish("Anchovy", ocean, (season.spring, season.fall), 30)
blue_discus = create_fish("Blue Discus", ginger_island_river, season.all_seasons, 60)
bream = create_fish("Bream", town_river + forest_river, season.all_seasons, 35)
bullhead = create_fish("Bullhead", mountain_lake, season.all_seasons, 46)
carp = create_fish(Fish.carp, mountain_lake + secret_woods + sewers + mutant_bug_lair, season.not_winter, 15)
catfish = create_fish("Catfish", town_river + forest_river + secret_woods, (season.spring, season.fall), 75)
chub = create_fish("Chub", forest_river + mountain_lake, season.all_seasons, 35)
dorado = create_fish("Dorado", forest_river, season.summer, 78)
eel = create_fish("Eel", ocean, (season.spring, season.fall), 70)
flounder = create_fish("Flounder", ocean, (season.spring, season.summer), 50)
ghostfish = create_fish("Ghostfish", mines_floor_20 + mines_floor_60, season.all_seasons, 50)
halibut = create_fish("Halibut", ocean, season.not_fall, 50)
herring = create_fish("Herring", ocean, (season.spring, season.winter), 25)
ice_pip = create_fish("Ice Pip", mines_floor_60, season.all_seasons, 85)
largemouth_bass = create_fish("Largemouth Bass", mountain_lake, season.all_seasons, 50)
lava_eel = create_fish("Lava Eel", mines_floor_100, season.all_seasons, 90)
lingcod = create_fish("Lingcod", town_river + forest_river + mountain_lake, season.winter, 85)
lionfish = create_fish("Lionfish", ginger_island_ocean, season.all_seasons, 50)
midnight_carp = create_fish("Midnight Carp", mountain_lake + forest_pond + ginger_island_river,
                            (season.fall, season.winter), 55)
octopus = create_fish("Octopus", ocean, season.summer, 95)
perch = create_fish("Perch", town_river + forest_river + forest_pond + mountain_lake, season.winter, 35)
pike = create_fish("Pike", town_river + forest_river + forest_pond, (season.summer, season.winter), 60)
pufferfish = create_fish("Pufferfish", ocean + ginger_island_ocean, season.summer, 80)
rainbow_trout = create_fish("Rainbow Trout", town_river + forest_river + mountain_lake, season.summer, 45)
red_mullet = create_fish("Red Mullet", ocean, (season.summer, season.winter), 55)
red_snapper = create_fish("Red Snapper", ocean, (season.summer, season.fall), 40)
salmon = create_fish("Salmon", town_river + forest_river, season.fall, 50)
sandfish = create_fish("Sandfish", desert, season.all_seasons, 65)
sardine = create_fish("Sardine", ocean, (season.spring, season.fall, season.winter), 30)
scorpion_carp = create_fish("Scorpion Carp", desert, season.all_seasons, 90)
sea_cucumber = create_fish("Sea Cucumber", ocean, (season.fall, season.winter), 40)
shad = create_fish("Shad", town_river + forest_river, season.not_winter, 45)
slimejack = create_fish("Slimejack", mutant_bug_lair, season.all_seasons, 55)
smallmouth_bass = create_fish("Smallmouth Bass", town_river + forest_river, (season.spring, season.fall), 28)
squid = create_fish("Squid", ocean, season.winter, 75)
stingray = create_fish("Stingray", pirate_cove, season.all_seasons, 80)
stonefish = create_fish("Stonefish", mines_floor_20, season.all_seasons, 65)
sturgeon = create_fish("Sturgeon", mountain_lake, (season.summer, season.winter), 78)
sunfish = create_fish("Sunfish", town_river + forest_river, (season.spring, season.summer), 30)
super_cucumber = create_fish("Super Cucumber", ocean + ginger_island_ocean, (season.summer, season.fall), 80)
tiger_trout = create_fish("Tiger Trout", town_river + forest_river, (season.fall, season.winter), 60)
tilapia = create_fish("Tilapia", ocean + ginger_island_ocean, (season.summer, season.fall), 50)
# Tuna has different seasons on ginger island. Should be changed when the whole fish thing is refactored
tuna = create_fish("Tuna", ocean + ginger_island_ocean, (season.summer, season.winter), 70)
void_salmon = create_fish("Void Salmon", witch_swamp, season.all_seasons, 80)
walleye = create_fish("Walleye", town_river + forest_river + forest_pond + mountain_lake, season.fall, 45)
woodskip = create_fish("Woodskip", secret_woods, season.all_seasons, 50)

blob_fish = create_fish("Blobfish", night_market, season.winter, 75)
midnight_squid = create_fish("Midnight Squid", night_market, season.winter, 55)
spook_fish = create_fish("Spook Fish", night_market, season.winter, 60)

angler = create_fish(Fish.angler, town_river, season.fall, 85, True, False)
crimsonfish = create_fish(Fish.crimsonfish, ocean, season.summer, 95, True, False)
glacierfish = create_fish(Fish.glacierfish, forest_river, season.winter, 100, True, False)
legend = create_fish(Fish.legend, mountain_lake, season.spring, 110, True, False)
mutant_carp = create_fish(Fish.mutant_carp, sewers, season.all_seasons, 80, True, False)

ms_angler = create_fish(Fish.ms_angler, town_river, season.fall, 85, True, True)
son_of_crimsonfish = create_fish(Fish.son_of_crimsonfish, ocean, season.summer, 95, True, True)
glacierfish_jr = create_fish(Fish.glacierfish_jr, forest_river, season.winter, 100, True, True)
legend_ii = create_fish(Fish.legend_ii, mountain_lake, season.spring, 110, True, True)
radioactive_carp = create_fish(Fish.radioactive_carp, sewers, season.all_seasons, 80, True, True)

baby_lunaloo = create_fish(SVEFish.baby_lunaloo, ginger_island_ocean, season.all_seasons, 15, mod_name=ModNames.sve)
bonefish = create_fish(SVEFish.bonefish, crimson_badlands, season.all_seasons, 70, mod_name=ModNames.sve)
bull_trout = create_fish(SVEFish.bull_trout, forest_river, season.not_spring, 45, mod_name=ModNames.sve)
butterfish = create_fish(SVEFish.butterfish, shearwater, season.not_winter, 75, mod_name=ModNames.sve)
clownfish = create_fish(SVEFish.clownfish, ginger_island_ocean, season.all_seasons, 45, mod_name=ModNames.sve)
daggerfish = create_fish(SVEFish.daggerfish, highlands, season.all_seasons, 50, mod_name=ModNames.sve)
frog = create_fish(SVEFish.frog, mountain_lake, (season.spring, season.summer), 70, mod_name=ModNames.sve)
gemfish = create_fish(SVEFish.gemfish, highlands, season.all_seasons, 100, mod_name=ModNames.sve)
goldenfish = create_fish(SVEFish.goldenfish, sprite_spring, season.all_seasons, 60, mod_name=ModNames.sve)
grass_carp = create_fish(SVEFish.grass_carp, secret_woods, (season.spring, season.summer), 85, mod_name=ModNames.sve)
king_salmon = create_fish(SVEFish.king_salmon, forest_river, (season.spring, season.summer), 80, mod_name=ModNames.sve)
kittyfish = create_fish(SVEFish.kittyfish, shearwater, (season.fall, season.winter), 85, mod_name=ModNames.sve)
lunaloo = create_fish(SVEFish.lunaloo, ginger_island_ocean, season.all_seasons, 70, mod_name=ModNames.sve)
meteor_carp = create_fish(SVEFish.meteor_carp, sprite_spring, season.all_seasons, 80, mod_name=ModNames.sve)
minnow = create_fish(SVEFish.minnow, town_river, season.all_seasons, 1, mod_name=ModNames.sve)
puppyfish = create_fish(SVEFish.puppyfish, shearwater, season.not_winter, 85, mod_name=ModNames.sve)
radioactive_bass = create_fish(SVEFish.radioactive_bass, sewers, season.all_seasons, 90, mod_name=ModNames.sve)
seahorse = create_fish(SVEFish.seahorse, ginger_island_ocean, season.all_seasons, 25, mod_name=ModNames.sve)
shiny_lunaloo = create_fish(SVEFish.shiny_lunaloo, ginger_island_ocean, season.all_seasons, 110, mod_name=ModNames.sve)
snatcher_worm = create_fish(SVEFish.snatcher_worm, mutant_bug_lair, season.all_seasons, 75, mod_name=ModNames.sve)
starfish = create_fish(SVEFish.starfish, ginger_island_ocean, season.all_seasons, 75, mod_name=ModNames.sve)
torpedo_trout = create_fish(SVEFish.torpedo_trout, fable_reef, season.all_seasons, 70, mod_name=ModNames.sve)
undeadfish = create_fish(SVEFish.undeadfish, crimson_badlands, season.all_seasons, 80, mod_name=ModNames.sve)
void_eel = create_fish(SVEFish.void_eel, witch_swamp, season.all_seasons, 100, mod_name=ModNames.sve)
water_grub = create_fish(SVEFish.water_grub, mutant_bug_lair, season.all_seasons, 60, mod_name=ModNames.sve)
sea_sponge = create_fish(SVEFish.sea_sponge, ginger_island_ocean, season.all_seasons, 40, mod_name=ModNames.sve)
dulse_seaweed = create_fish(SVEFish.dulse_seaweed, vineyard, season.all_seasons, 50, mod_name=ModNames.sve)

void_minnow = create_fish(DistantLandsFish.void_minnow, witch_swamp, season.all_seasons, 15, mod_name=ModNames.distant_lands)
purple_algae = create_fish(DistantLandsFish.purple_algae, witch_swamp, season.all_seasons, 15, mod_name=ModNames.distant_lands)
swamp_leech = create_fish(DistantLandsFish.swamp_leech, witch_swamp, season.all_seasons, 15, mod_name=ModNames.distant_lands)
giant_horsehoe_crab = create_fish(DistantLandsFish.giant_horsehoe_crab, witch_swamp, season.all_seasons, 90, mod_name=ModNames.distant_lands)


clam = create_fish("Clam", ocean, season.all_seasons, -1)
cockle = create_fish("Cockle", ocean, season.all_seasons, -1)
crab = create_fish("Crab", ocean, season.all_seasons, -1)
crayfish = create_fish("Crayfish", fresh_water, season.all_seasons, -1)
lobster = create_fish("Lobster", ocean, season.all_seasons, -1)
mussel = create_fish("Mussel", ocean, season.all_seasons, -1)
oyster = create_fish("Oyster", ocean, season.all_seasons, -1)
periwinkle = create_fish("Periwinkle", fresh_water, season.all_seasons, -1)
shrimp = create_fish("Shrimp", ocean, season.all_seasons, -1)
snail = create_fish("Snail", fresh_water, season.all_seasons, -1)

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
