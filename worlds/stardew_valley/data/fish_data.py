from dataclasses import dataclass
from typing import Tuple, Union, Optional

from . import season_data as season
from ..mods.mod_data import ModNames
from ..strings.fish_names import Fish, SVEFish, DistantLandsFish
from ..strings.region_names import Region, SVERegion, LogicRegion


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
tide_pools = (Region.tide_pools,)
town_river = (Region.town,)
mountain_lake = (Region.mountain,)
forest_pond = (Region.forest,)
forest_river = (Region.forest,)
forest_waterfall = (LogicRegion.forest_waterfall,)
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
highlands_pond = (SVERegion.highlands_pond,)
highlands_cave = (SVERegion.highlands_cavern,)
sprite_spring = (SVERegion.sprite_spring,)
fable_reef = (SVERegion.fable_reef,)
vineyard = (SVERegion.blue_moon_vineyard,)


def create_fish(name: str, locations: Tuple[str, ...], seasons: Union[str, Tuple[str, ...]],
                difficulty: int, legendary: bool = False, extended_family: bool = False, mod_name: Optional[str] = None) -> FishItem:
    if isinstance(seasons, str):
        seasons = (seasons,)

    fish_item = FishItem(name, locations, seasons, difficulty, legendary, extended_family, mod_name)
    return fish_item


albacore = create_fish(Fish.albacore, ocean, (season.fall, season.winter), 60)
anchovy = create_fish(Fish.anchovy, ocean, (season.spring, season.fall), 30)
blue_discus = create_fish(Fish.blue_discus, ginger_island_river, season.all_seasons, 60)
bream = create_fish(Fish.bream, town_river + forest_river, season.all_seasons, 35)
bullhead = create_fish(Fish.bullhead, mountain_lake, season.all_seasons, 46)
carp = create_fish(Fish.carp, mountain_lake + secret_woods + sewers + mutant_bug_lair, season.not_winter, 15)
catfish = create_fish(Fish.catfish, town_river + forest_river + secret_woods, (season.spring, season.fall), 75)
chub = create_fish(Fish.chub, forest_river + mountain_lake, season.all_seasons, 35)
dorado = create_fish(Fish.dorado, forest_river, season.summer, 78)
eel = create_fish(Fish.eel, ocean, (season.spring, season.fall), 70)
flounder = create_fish(Fish.flounder, ocean, (season.spring, season.summer), 50)
ghostfish = create_fish(Fish.ghostfish, mines_floor_20 + mines_floor_60, season.all_seasons, 50)
goby = create_fish(Fish.goby, forest_waterfall, season.all_seasons, 55)
halibut = create_fish(Fish.halibut, ocean, season.not_fall, 50)
herring = create_fish(Fish.herring, ocean, (season.spring, season.winter), 25)
ice_pip = create_fish(Fish.ice_pip, mines_floor_60, season.all_seasons, 85)
largemouth_bass = create_fish(Fish.largemouth_bass, mountain_lake, season.all_seasons, 50)
lava_eel = create_fish(Fish.lava_eel, mines_floor_100, season.all_seasons, 90)
lingcod = create_fish(Fish.lingcod, town_river + forest_river + mountain_lake, season.winter, 85)
lionfish = create_fish(Fish.lionfish, ginger_island_ocean, season.all_seasons, 50)
midnight_carp = create_fish(Fish.midnight_carp, mountain_lake + forest_pond + ginger_island_river,
                            (season.fall, season.winter), 55)
octopus = create_fish(Fish.octopus, ocean, season.summer, 95)
perch = create_fish(Fish.perch, town_river + forest_river + forest_pond + mountain_lake, season.winter, 35)
pike = create_fish(Fish.pike, town_river + forest_river + forest_pond, (season.summer, season.winter), 60)
pufferfish = create_fish(Fish.pufferfish, ocean + ginger_island_ocean, season.summer, 80)
rainbow_trout = create_fish(Fish.rainbow_trout, town_river + forest_river + mountain_lake, season.summer, 45)
red_mullet = create_fish(Fish.red_mullet, ocean, (season.summer, season.winter), 55)
red_snapper = create_fish(Fish.red_snapper, ocean, (season.summer, season.fall), 40)
salmon = create_fish(Fish.salmon, town_river + forest_river, season.fall, 50)
sandfish = create_fish(Fish.sandfish, desert, season.all_seasons, 65)
sardine = create_fish(Fish.sardine, ocean, (season.spring, season.fall, season.winter), 30)
scorpion_carp = create_fish(Fish.scorpion_carp, desert, season.all_seasons, 90)
sea_cucumber = create_fish(Fish.sea_cucumber, ocean, (season.fall, season.winter), 40)
shad = create_fish(Fish.shad, town_river + forest_river, season.not_winter, 45)
slimejack = create_fish(Fish.slimejack, mutant_bug_lair, season.all_seasons, 55)
smallmouth_bass = create_fish(Fish.smallmouth_bass, town_river + forest_river, (season.spring, season.fall), 28)
squid = create_fish(Fish.squid, ocean, season.winter, 75)
stingray = create_fish(Fish.stingray, pirate_cove, season.all_seasons, 80)
stonefish = create_fish(Fish.stonefish, mines_floor_20, season.all_seasons, 65)
sturgeon = create_fish(Fish.sturgeon, mountain_lake, (season.summer, season.winter), 78)
sunfish = create_fish(Fish.sunfish, town_river + forest_river, (season.spring, season.summer), 30)
super_cucumber = create_fish(Fish.super_cucumber, ocean + ginger_island_ocean, (season.summer, season.fall), 80)
tiger_trout = create_fish(Fish.tiger_trout, town_river + forest_river, (season.fall, season.winter), 60)
tilapia = create_fish(Fish.tilapia, ocean + ginger_island_ocean, (season.summer, season.fall), 50)
# Tuna has different seasons on ginger island. Should be changed when the whole fish thing is refactored
tuna = create_fish(Fish.tuna, ocean + ginger_island_ocean, (season.summer, season.winter), 70)
void_salmon = create_fish(Fish.void_salmon, witch_swamp, season.all_seasons, 80)
walleye = create_fish(Fish.walleye, town_river + forest_river + forest_pond + mountain_lake, season.fall, 45)
woodskip = create_fish(Fish.woodskip, secret_woods, season.all_seasons, 50)

blobfish = create_fish(Fish.blobfish, night_market, season.winter, 75)
midnight_squid = create_fish(Fish.midnight_squid, night_market, season.winter, 55)
spook_fish = create_fish(Fish.spook_fish, night_market, season.winter, 60)

angler = create_fish(Fish.angler, town_river, season.fall, 85, True, False)
crimsonfish = create_fish(Fish.crimsonfish, tide_pools, season.summer, 95, True, False)
glacierfish = create_fish(Fish.glacierfish, forest_river, season.winter, 100, True, False)
legend = create_fish(Fish.legend, mountain_lake, season.spring, 110, True, False)
mutant_carp = create_fish(Fish.mutant_carp, sewers, season.all_seasons, 80, True, False)

ms_angler = create_fish(Fish.ms_angler, town_river, season.fall, 85, True, True)
son_of_crimsonfish = create_fish(Fish.son_of_crimsonfish, tide_pools, season.summer, 95, True, True)
glacierfish_jr = create_fish(Fish.glacierfish_jr, forest_river, season.winter, 100, True, True)
legend_ii = create_fish(Fish.legend_ii, mountain_lake, season.spring, 110, True, True)
radioactive_carp = create_fish(Fish.radioactive_carp, sewers, season.all_seasons, 80, True, True)

baby_lunaloo = create_fish(SVEFish.baby_lunaloo, ginger_island_ocean, season.all_seasons, 15, mod_name=ModNames.sve)
bonefish = create_fish(SVEFish.bonefish, crimson_badlands, season.all_seasons, 70, mod_name=ModNames.sve)
bull_trout = create_fish(SVEFish.bull_trout, forest_river, season.not_spring, 45, mod_name=ModNames.sve)
butterfish = create_fish(SVEFish.butterfish, shearwater, season.not_winter, 75, mod_name=ModNames.sve)
clownfish = create_fish(SVEFish.clownfish, ginger_island_ocean, season.all_seasons, 45, mod_name=ModNames.sve)
daggerfish = create_fish(SVEFish.daggerfish, highlands_pond, season.all_seasons, 50, mod_name=ModNames.sve)
frog = create_fish(SVEFish.frog, mountain_lake, (season.spring, season.summer), 70, mod_name=ModNames.sve)
gemfish = create_fish(SVEFish.gemfish, highlands_cave, season.all_seasons, 100, mod_name=ModNames.sve)
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

void_minnow = create_fish(DistantLandsFish.void_minnow, witch_swamp, season.all_seasons, 15, mod_name=ModNames.distant_lands)
purple_algae = create_fish(DistantLandsFish.purple_algae, witch_swamp, season.all_seasons, 15, mod_name=ModNames.distant_lands)
swamp_leech = create_fish(DistantLandsFish.swamp_leech, witch_swamp, season.all_seasons, 15, mod_name=ModNames.distant_lands)
giant_horsehoe_crab = create_fish(DistantLandsFish.giant_horsehoe_crab, witch_swamp, season.all_seasons, 90, mod_name=ModNames.distant_lands)

clam = create_fish(Fish.clam, ocean, season.all_seasons, -1)
cockle = create_fish(Fish.cockle, ocean, season.all_seasons, -1)
crab = create_fish(Fish.crab, ocean, season.all_seasons, -1)
crayfish = create_fish(Fish.crayfish, fresh_water, season.all_seasons, -1)
lobster = create_fish(Fish.lobster, ocean, season.all_seasons, -1)
mussel = create_fish(Fish.mussel, ocean, season.all_seasons, -1)
oyster = create_fish(Fish.oyster, ocean, season.all_seasons, -1)
periwinkle = create_fish(Fish.periwinkle, fresh_water, season.all_seasons, -1)
shrimp = create_fish(Fish.shrimp, ocean, season.all_seasons, -1)
snail = create_fish(Fish.snail, fresh_water, season.all_seasons, -1)

vanilla_legendary_fish = [angler, crimsonfish, glacierfish, legend, mutant_carp]
