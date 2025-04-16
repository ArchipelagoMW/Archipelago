from dataclasses import field, dataclass
from enum import Enum
from typing import NamedTuple, TYPE_CHECKING

from worlds.pokepark import FRIENDSHIP_ITEMS
from worlds.pokepark.LocationIds import MinigameLocationIds, QuestLocationIds, OverworldPokemonLocationIds, \
    UnlockLocationIds
from worlds.pokepark.items import UNLOCK_ITEMS, PRISM_ITEM

if TYPE_CHECKING:
    from . import PokeparkWorld


class PowerRequirement(Enum):
    none = 0
    can_battle = 1
    can_dash_overworld = 2
    can_play_catch = 3
    can_destroy_objects_overworld = 4
    can_thunderbolt_overworld = 5
    can_battle_thunderbolt_immune = 6
    can_farm_berries = 7
    can_play_catch_intermediate = 8


class WorldStateRequirement(Enum):
    none = 0
    meadow_zone_or_higher = 1
    beach_zone_or_higher = 2
    ice_zone_or_higher = 3
    cavern_and_magma_zone_or_higher = 4
    haunted_zone_or_higher = 5
    granite_and_flower_zone_or_higher = 6
    skygarden = 7


class MinigameRequirement(Enum):
    none = 0
    bulbasaur_dash_any = 1
    venusaur_vine_swing_any = 2
    venusaur_vine_swing_all = 3
    pelipper_circuit_any = 4
    pelipper_circuit_all = 5
    gyarados_aqua_any = 6
    gyarados_aqua_all = 7
    empoleon_slide_any = 8
    empoleon_slide_all = 9
    bastiodon_panel_any = 10
    bastiodon_panel_all = 11
    rhyperior_bumper_any = 12
    rhyperior_bumper_all = 13
    blaziken_boulder_any = 14
    blaziken_boulder_all = 15
    tangrowth_swing_any = 16
    tangrowth_swing_all = 17
    dusknoir_slam_any = 18
    dusknoir_slam_all = 19
    rotom_shoot_any = 20
    rotom_shoot_all = 21
    absol_hurdle_any = 22
    absol_hurdle_all = 23
    salamence_air_any = 24
    salamence_air_all = 25
    rayquaza_balloon_any = 26
    rayquaza_balloon_all = 27


class Requirements(NamedTuple):
    unlock_names: list[str] = []
    friendship_names: list[str] = []
    friendcount: int = 0
    prisma_names: list[str] = []
    oneof_item_names: list[list[str]] = []
    can_reach_locations: list[str] = []
    powers: PowerRequirement = PowerRequirement.none
    world_state: WorldStateRequirement = WorldStateRequirement.none
    minigame: MinigameRequirement = MinigameRequirement.none


class Location(NamedTuple):
    name: str
    id: int
    requirements: Requirements = Requirements()


@dataclass
class PokeparkRegion:
    name: str
    display: str
    requirements: Requirements = Requirements()
    friendship_locations: list[Location] = field(default_factory=list)
    unlock_location: list[Location] = field(default_factory=list)
    minigame_location: list[Location] = field(default_factory=list)
    quest_locations: list[Location] = field(default_factory=list)
    parent_regions: list[str] = field(default_factory=lambda: ["Menu"])


def generate_regions(world: "PokeparkWorld", get_all_locations: bool = False):
    all_regions: list[PokeparkRegion] = []

    treehouse = generate_treehouse_region(world, get_all_locations)
    all_regions.append(treehouse)

    meadow_zone_overworld_region = generate_meadow_zone_overworld_region(world, get_all_locations)
    all_regions.append(meadow_zone_overworld_region)

    meadow_zone_bulbasaur_minigame_region = generate_meadow_zone_bulbasaur_minigame_region(world, get_all_locations)
    all_regions.append(meadow_zone_bulbasaur_minigame_region)

    meadow_zone_venusaur_minigame_region = generate_meadow_zone_venusaur_minigame_region(world, get_all_locations)
    all_regions.append(meadow_zone_venusaur_minigame_region)

    beach_zone_overworld_region = generate_beach_zone_overworld_region(world, get_all_locations)
    all_regions.append(beach_zone_overworld_region)

    beach_zone_pelipper_minigame_region = generate_beach_zone_pelipper_minigame_region(world, get_all_locations)
    all_regions.append(beach_zone_pelipper_minigame_region)

    beach_zone_gyarados_minigame_region = generate_beach_zone_gyarados_minigame_region(world, get_all_locations)
    all_regions.append(beach_zone_gyarados_minigame_region)

    ice_zone_overworld_region = generate_ice_zone_overworld_region(world, get_all_locations)
    all_regions.append(ice_zone_overworld_region)

    ice_zone_overworld_lower_lift_region = generate_ice_zone_overworld_lower_lift_region(world, get_all_locations)
    all_regions.append(ice_zone_overworld_lower_lift_region)

    ice_zone_empoleon_minigame_region = generate_ice_zone_empoleon_minigame_region(world, get_all_locations)
    all_regions.append(ice_zone_empoleon_minigame_region)

    cavern_zone_overworld_region = generate_cavern_zone_overworld_region(world, get_all_locations)
    all_regions.append(cavern_zone_overworld_region)

    cavern_zone_bastiodon_minigame_region = generate_cavern_zone_bastiodon_minigame_region(world, get_all_locations)
    all_regions.append(cavern_zone_bastiodon_minigame_region)

    magma_zone_overworld_region = generate_magma_zone_overworld_region(world, get_all_locations)
    all_regions.append(magma_zone_overworld_region)

    magma_zone_rhyperior_minigame_region = generate_magma_zone_rhyperior_minigame_region(world, get_all_locations)
    all_regions.append(magma_zone_rhyperior_minigame_region)

    magma_zone_blaziken_minigame_region = generate_magma_zone_blaziken_minigame_region(world, get_all_locations)
    all_regions.append(magma_zone_blaziken_minigame_region)

    haunted_zone_overworld_region = generate_haunted_zone_overworld_region(world, get_all_locations)
    all_regions.append(haunted_zone_overworld_region)

    haunted_zone_tangrowth_minigame_region = generate_haunted_zone_tangrowth_minigame_region(world, get_all_locations)
    all_regions.append(haunted_zone_tangrowth_minigame_region)

    haunted_zone_overworld_mansion_region = generate_haunted_zone_overworld_mansion_region(world, get_all_locations)
    all_regions.append(haunted_zone_overworld_mansion_region)

    haunted_zone_mansion_dusknoir_minigame_region = generate_haunted_zone_mansion_dusknoir_minigame_region(world,
                                                                                                           get_all_locations)
    all_regions.append(haunted_zone_mansion_dusknoir_minigame_region)

    haunted_zone_mansion_rotom_minigame_region = generate_haunted_zone_mansion_rotom_minigame_region(world,
                                                                                                     get_all_locations)
    all_regions.append(haunted_zone_mansion_rotom_minigame_region)

    granite_zone_overworld_region = generate_granite_zone_overworld_region(world, get_all_locations)
    all_regions.append(granite_zone_overworld_region)

    granite_zone_absol_minigame_region = generate_granite_zone_absol_minigame_region(world, get_all_locations)
    all_regions.append(granite_zone_absol_minigame_region)

    granite_zone_salamence_minigame_region = generate_granite_zone_salamence_minigame_region(world, get_all_locations)
    all_regions.append(granite_zone_salamence_minigame_region)

    flower_zone_overworld_region = generate_flower_zone_overworld_region(world, get_all_locations)
    all_regions.append(flower_zone_overworld_region)

    flower_zone_rayquaza_minigame_region = generate_flower_zone_rayquaza_minigame_region(world, get_all_locations)
    all_regions.append(flower_zone_rayquaza_minigame_region)

    skygarden_overworld_region = generate_skygarden_overworld_region(world, get_all_locations)
    all_regions.append(skygarden_overworld_region)
    return all_regions


def generate_skygarden_overworld_region(world, get_all_locations: bool = False):
    skygarden_overworld_region: PokeparkRegion = (
        PokeparkRegion(name="Skygarden - Overworld",
                       display="Skygarden - Overworld",
                       requirements=Requirements(
                           unlock_names=["Skygarden Unlock"]
                       ), parent_regions=["Treehouse"]))

    skygarden_overworld_region.quest_locations.append(
        Location(name="Mew Challenge 1",
                 id=QuestLocationIds.MEW_CHALLENGE1.value),
    )
    skygarden_overworld_region.quest_locations.append(
        Location(name="Mew Challenge 2",
                 id=QuestLocationIds.MEW_CHALLENGE2.value,
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle,
                     can_reach_locations=["Skygarden - Overworld - Mew Challenge 1"]
                 )),
    )
    skygarden_overworld_region.quest_locations.append(
        Location(name="Mew Challenge 3",
                 id=QuestLocationIds.MEW_CHALLENGE3.value,
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle_thunderbolt_immune,
                     can_reach_locations=["Skygarden - Overworld - Mew Challenge 2"]
                 )),
    )
    skygarden_overworld_region.quest_locations.append(
        Location(name="Mew Challenge 4",
                 id=QuestLocationIds.MEW_CHALLENGE4.value,
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle,
                     can_reach_locations=["Skygarden - Overworld - Mew Challenge 3"]
                 )),
    )
    skygarden_overworld_region.quest_locations.append(
        Location(name="Mew Challenge completed",
                 id=QuestLocationIds.MEW_CHALLENGE_END.value,
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch_intermediate,
                     can_reach_locations=["Skygarden - Overworld - Mew Challenge 4"]

                 )),
    )
    if world.options.goal == world.options.goal.option_aftergame or get_all_locations:
        skygarden_overworld_region.quest_locations.append(
            Location(name="Completing Prisma",
                     id=QuestLocationIds.COMPLETE_PRISMA.value,
                     requirements=Requirements(
                         friendcount=193,
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]
                     )),
        )
    return skygarden_overworld_region


def generate_flower_zone_rayquaza_minigame_region(world, get_all_locations: bool = False):
    flower_zone_rayquaza_minigame_region: PokeparkRegion = (
        PokeparkRegion(name="Flower Zone - Rayquaza's Balloon Panic",
                       display="Flower Zone - Rayquaza's Balloon Panic",
                       requirements=Requirements(
                           unlock_names=["Rayquaza Unlock"]
                       ), parent_regions=["Flower Zone - Overworld"]))

    flower_zone_rayquaza_minigame_region.minigame_location.append(
        Location(name="Prisma",
                 id=PRISM_ITEM["Rayquaza Prisma"],
                 requirements=Requirements(
                     minigame=MinigameRequirement.rayquaza_balloon_any
                 )),
    )
    flower_zone_rayquaza_minigame_region.minigame_location.append(
        Location(name="Pikachu",
                 id=MinigameLocationIds.PIKACHU_BALLOON.value),
    )
    flower_zone_rayquaza_minigame_region.minigame_location.append(
        Location(name="Lucario",
                 id=MinigameLocationIds.LUCARIO_BALLOON.value,
                 requirements=Requirements(
                     friendship_names=["Lucario"])),
    )
    flower_zone_rayquaza_minigame_region.minigame_location.append(
        Location(name="Glaceon",
                 id=MinigameLocationIds.GLACEON_BALLOON.value,
                 requirements=Requirements(
                     friendship_names=["Glaceon"])),
    )
    flower_zone_rayquaza_minigame_region.minigame_location.append(
        Location(name="Luxray",
                 id=MinigameLocationIds.LUXRAY_BALLOON.value,
                 requirements=Requirements(
                     friendship_names=["Luxray"])),
    )
    flower_zone_rayquaza_minigame_region.minigame_location.append(
        Location(name="Mamoswine",
                 id=MinigameLocationIds.MAMOSWINE_BALLOON.value,
                 requirements=Requirements(
                     friendship_names=["Mamoswine"])),
    )
    flower_zone_rayquaza_minigame_region.minigame_location.append(
        Location(name="Infernape",
                 id=MinigameLocationIds.INFERNAPE_BALLOON.value,
                 requirements=Requirements(
                     friendship_names=["Infernape"])),
    )
    flower_zone_rayquaza_minigame_region.minigame_location.append(
        Location(name="Floatzel",
                 id=MinigameLocationIds.FLOATZEL_BALLOON.value,
                 requirements=Requirements(
                     friendship_names=["Floatzel"])),
    )
    flower_zone_rayquaza_minigame_region.minigame_location.append(
        Location(name="Rhyperior",
                 id=MinigameLocationIds.RHYPERIOR_BALLOON.value,
                 requirements=Requirements(
                     friendship_names=["Rhyperior"])),
    )
    flower_zone_rayquaza_minigame_region.minigame_location.append(
        Location(name="Absol",
                 id=MinigameLocationIds.ABSOL_BALLOON.value,
                 requirements=Requirements(
                     friendship_names=["Absol"])),
    )
    flower_zone_rayquaza_minigame_region.minigame_location.append(
        Location(name="Breloom",
                 id=MinigameLocationIds.BRELOOM_BALLOON.value,
                 requirements=Requirements(
                     friendship_names=["Breloom"])),
    )
    flower_zone_rayquaza_minigame_region.minigame_location.append(
        Location(name="Mareep",
                 id=MinigameLocationIds.MAREEP_BALLOON.value,
                 requirements=Requirements(
                     friendship_names=["Mareep"])),
    )
    flower_zone_rayquaza_minigame_region.minigame_location.append(
        Location(name="Cyndaquil",
                 id=MinigameLocationIds.CYNDAQUIL_BALLOON.value,
                 requirements=Requirements(
                     friendship_names=["Cyndaquil"])),
    )
    flower_zone_rayquaza_minigame_region.minigame_location.append(
        Location(name="Totodile",
                 id=MinigameLocationIds.TOTODILE_BALLOON.value,
                 requirements=Requirements(
                     friendship_names=["Totodile"])),
    )
    flower_zone_rayquaza_minigame_region.minigame_location.append(
        Location(name="Chikorita",
                 id=MinigameLocationIds.CHIKORITA_BALLOON.value,
                 requirements=Requirements(
                     friendship_names=["Chikorita"])),
    )
    flower_zone_rayquaza_minigame_region.minigame_location.append(
        Location(name="Mime Jr.",
                 id=MinigameLocationIds.MIMEJR_BALLOON.value,
                 requirements=Requirements(
                     friendship_names=["Mime Jr."])),
    )
    if world.options.goal == world.options.goal.option_aftergame or get_all_locations:
        flower_zone_rayquaza_minigame_region.minigame_location.append(
            Location(name="Deoxys",
                     id=MinigameLocationIds.DEOXYS_BALLOON.value,
                     requirements=Requirements(
                         friendship_names=["Deoxys"],
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]
                     )),
        )
        flower_zone_rayquaza_minigame_region.friendship_locations.append(
            Location(name="Deoxys Unlock",
                     id=FRIENDSHIP_ITEMS["Deoxys"],
                     requirements=Requirements(
                         minigame=MinigameRequirement.rayquaza_balloon_all,
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]
                     )),
        )
    return flower_zone_rayquaza_minigame_region


def generate_flower_zone_overworld_region(world, get_all_locations: bool = False):
    flower_zone_overworld_region: PokeparkRegion = (
        PokeparkRegion(name="Flower Zone - Overworld",
                       display="Flower Zone - Overworld",
                       requirements=Requirements(
                           unlock_names=["Granite Zone & Flower Zone Unlock"]
                       ), parent_regions=["Granite Zone - Overworld",
                                          "Treehouse"]))

    flower_zone_overworld_region.friendship_locations.append(
        Location(name="Skiploom",
                 id=FRIENDSHIP_ITEMS["Skiploom"]),
    )
    flower_zone_overworld_region.friendship_locations.append(
        Location(name="Budew",
                 id=FRIENDSHIP_ITEMS["Budew"]),
    )
    flower_zone_overworld_region.friendship_locations.append(
        Location(name="Cyndaquil",
                 id=FRIENDSHIP_ITEMS["Cyndaquil"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    flower_zone_overworld_region.friendship_locations.append(
        Location(name="Lucario",
                 id=FRIENDSHIP_ITEMS["Lucario"],
                 requirements=Requirements(
                     friendcount=101,
                     powers=PowerRequirement.can_play_catch_intermediate
                 )),
    )
    flower_zone_overworld_region.friendship_locations.append(
        Location(name="Furret",
                 id=OverworldPokemonLocationIds.FURRET_FLOWER.value),
    )
    flower_zone_overworld_region.friendship_locations.append(
        Location(name="Teddiursa",
                 id=OverworldPokemonLocationIds.TEDDIURSA_FLOWER.value,
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    flower_zone_overworld_region.friendship_locations.append(
        Location(name="Meditite",
                 id=OverworldPokemonLocationIds.MEDITITE_FLOWER.value),
    )
    flower_zone_overworld_region.friendship_locations.append(
        Location(name="Dragonite",
                 id=FRIENDSHIP_ITEMS["Dragonite"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    flower_zone_overworld_region.friendship_locations.append(
        Location(name="Mareep",
                 id=FRIENDSHIP_ITEMS["Mareep"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    flower_zone_overworld_region.friendship_locations.append(
        Location(name="Bellossom",
                 id=FRIENDSHIP_ITEMS["Bellossom"],
                 requirements=Requirements(
                     world_state=WorldStateRequirement.skygarden
                 )),
    )
    return flower_zone_overworld_region


def generate_granite_zone_salamence_minigame_region(world, get_all_locations: bool = False):
    granite_zone_salamence_minigame_region: PokeparkRegion = (
        PokeparkRegion(name="Granite Zone - Salamence's Sky Race",
                       display="Granite Zone - Salamence's Sky Race",
                       requirements=Requirements(
                           friendcount=80
                       ),
                       parent_regions=["Granite Zone - Overworld"]))

    granite_zone_salamence_minigame_region.minigame_location.append(
        Location(name="Prisma",
                 id=PRISM_ITEM["Salamence Prisma"],
                 requirements=Requirements(
                     minigame=MinigameRequirement.salamence_air_any
                 )),
    )
    granite_zone_salamence_minigame_region.minigame_location.append(
        Location(name="Pikachu",
                 id=MinigameLocationIds.PIKACHU_SKY.value,
                 requirements=Requirements(
                     unlock_names=["Pikachu Balloon"]
                 )),
    )
    granite_zone_salamence_minigame_region.minigame_location.append(
        Location(name="Salamence",
                 id=MinigameLocationIds.SALAMENCE_SKY.value,
                 requirements=Requirements(
                     friendship_names=["Salamence"])),
    )
    granite_zone_salamence_minigame_region.minigame_location.append(
        Location(name="Charizard",
                 id=MinigameLocationIds.CHARIZARD_SKY.value,
                 requirements=Requirements(
                     friendship_names=["Charizard"])),
    )
    granite_zone_salamence_minigame_region.minigame_location.append(
        Location(name="Dragonite",
                 id=MinigameLocationIds.DRAGONITE_SKY.value,
                 requirements=Requirements(
                     friendship_names=["Dragonite"])),
    )
    granite_zone_salamence_minigame_region.minigame_location.append(
        Location(name="Flygon",
                 id=MinigameLocationIds.FLYGON_SKY.value,
                 requirements=Requirements(
                     friendship_names=["Flygon"])),
    )
    granite_zone_salamence_minigame_region.minigame_location.append(
        Location(name="Aerodactyl",
                 id=MinigameLocationIds.AERODACTYL_SKY.value,
                 requirements=Requirements(
                     friendship_names=["Aerodactyl"])),
    )
    granite_zone_salamence_minigame_region.minigame_location.append(
        Location(name="Staraptor",
                 id=MinigameLocationIds.STARAPTOR_SKY.value,
                 requirements=Requirements(
                     friendship_names=["Staraptor"])),
    )
    granite_zone_salamence_minigame_region.minigame_location.append(
        Location(name="Honchkrow",
                 id=MinigameLocationIds.HONCHKROW_SKY.value,
                 requirements=Requirements(
                     friendship_names=["Honchkrow"])),
    )
    granite_zone_salamence_minigame_region.minigame_location.append(
        Location(name="Gliscor",
                 id=MinigameLocationIds.GLISCOR_SKY.value,
                 requirements=Requirements(
                     friendship_names=["Gliscor"])),
    )
    granite_zone_salamence_minigame_region.minigame_location.append(
        Location(name="Pidgeotto",
                 id=MinigameLocationIds.PIDGEOTTO_SKY.value,
                 requirements=Requirements(
                     friendship_names=["Pidgeotto"])),
    )
    granite_zone_salamence_minigame_region.minigame_location.append(
        Location(name="Togekiss",
                 id=MinigameLocationIds.TOGEKISS_SKY.value,
                 requirements=Requirements(
                     friendship_names=["Togekiss"])),
    )
    granite_zone_salamence_minigame_region.minigame_location.append(
        Location(name="Golbat",
                 id=MinigameLocationIds.GOLBAT_SKY.value,
                 requirements=Requirements(
                     friendship_names=["Golbat"])),
    )
    granite_zone_salamence_minigame_region.minigame_location.append(
        Location(name="Taillow",
                 id=MinigameLocationIds.TAILLOW_SKY.value,
                 requirements=Requirements(
                     friendship_names=["Taillow"])),
    )
    granite_zone_salamence_minigame_region.minigame_location.append(
        Location(name="Murkrow",
                 id=MinigameLocationIds.MURKROW_SKY.value,
                 requirements=Requirements(
                     friendship_names=["Murkrow"])),
    )
    granite_zone_salamence_minigame_region.minigame_location.append(
        Location(name="Zubat",
                 id=MinigameLocationIds.ZUBAT_SKY.value,
                 requirements=Requirements(
                     friendship_names=["Zubat"])),
    )
    if world.options.goal == world.options.goal.option_aftergame or get_all_locations:
        granite_zone_salamence_minigame_region.minigame_location.append(
            Location(name="Latios",
                     id=MinigameLocationIds.LATIOS_SKY.value,
                     requirements=Requirements(
                         friendship_names=["Latios"],
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]
                     )),
        )
        granite_zone_salamence_minigame_region.friendship_locations.append(
            Location(name="Latios Unlock",
                     id=FRIENDSHIP_ITEMS["Latios"],
                     requirements=Requirements(
                         minigame=MinigameRequirement.salamence_air_all,
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]
                     )),
        )
    return granite_zone_salamence_minigame_region


def generate_granite_zone_absol_minigame_region(world, get_all_locations: bool = False):
    granite_zone_absol_minigame_region: PokeparkRegion = (
        PokeparkRegion(name="Granite Zone - Absol's Hurdle Bounce",
                       display="Granite Zone - Absol's Hurdle Bounce",
                       parent_regions=["Granite Zone - Overworld"]))

    granite_zone_absol_minigame_region.minigame_location.append(
        Location(name="Prisma",
                 id=PRISM_ITEM["Absol Prisma"],
                 requirements=Requirements(
                     minigame=MinigameRequirement.absol_hurdle_any
                 )),
    )
    granite_zone_absol_minigame_region.minigame_location.append(
        Location(name="Pikachu",
                 id=MinigameLocationIds.PIKACHU_HURDLE.value),
    )
    granite_zone_absol_minigame_region.minigame_location.append(
        Location(name="Chikorita",
                 id=MinigameLocationIds.CHIKORITA_HURDLE.value,
                 requirements=Requirements(
                     friendship_names=["Chikorita"])),
    )
    granite_zone_absol_minigame_region.minigame_location.append(
        Location(name="Absol",
                 id=MinigameLocationIds.ABSOL_HURDLE.value,
                 requirements=Requirements(
                     friendship_names=["Absol"])),
    )
    granite_zone_absol_minigame_region.minigame_location.append(
        Location(name="Lucario",
                 id=MinigameLocationIds.LUCARIO_HURDLE.value,
                 requirements=Requirements(
                     friendship_names=["Lucario"])),
    )
    granite_zone_absol_minigame_region.minigame_location.append(
        Location(name="Ponyta",
                 id=MinigameLocationIds.PONYTA_HURDLE.value,
                 requirements=Requirements(
                     friendship_names=["Ponyta"])),
    )
    granite_zone_absol_minigame_region.minigame_location.append(
        Location(name="Ninetales",
                 id=MinigameLocationIds.NINETALES_HURDLE.value,
                 requirements=Requirements(
                     friendship_names=["Ninetales"])),
    )
    granite_zone_absol_minigame_region.minigame_location.append(
        Location(name="Lopunny",
                 id=MinigameLocationIds.LOPUNNY_HURDLE.value,
                 requirements=Requirements(
                     friendship_names=["Lopunny"])),
    )
    granite_zone_absol_minigame_region.minigame_location.append(
        Location(name="Espeon",
                 id=MinigameLocationIds.ESPEON_HURDLE.value,
                 requirements=Requirements(
                     friendship_names=["Espeon"])),
    )
    granite_zone_absol_minigame_region.minigame_location.append(
        Location(name="Infernape",
                 id=MinigameLocationIds.INFERNAPE_HURDLE.value,
                 requirements=Requirements(
                     friendship_names=["Infernape"])),
    )
    granite_zone_absol_minigame_region.minigame_location.append(
        Location(name="Breloom",
                 id=MinigameLocationIds.BRELOOM_HURDLE.value,
                 requirements=Requirements(
                     friendship_names=["Breloom"])),
    )
    granite_zone_absol_minigame_region.minigame_location.append(
        Location(name="Riolu",
                 id=MinigameLocationIds.RIOLU_HURDLE.value,
                 requirements=Requirements(
                     friendship_names=["Riolu"])),
    )
    granite_zone_absol_minigame_region.minigame_location.append(
        Location(name="Furret",
                 id=MinigameLocationIds.FURRET_HURDLE.value,
                 requirements=Requirements(
                     friendship_names=["Furret"])),
    )
    granite_zone_absol_minigame_region.minigame_location.append(
        Location(name="Mareep",
                 id=MinigameLocationIds.MAREEP_HURDLE.value,
                 requirements=Requirements(
                     friendship_names=["Mareep"])),
    )
    granite_zone_absol_minigame_region.minigame_location.append(
        Location(name="Eevee",
                 id=MinigameLocationIds.EEVEE_HURDLE.value,
                 requirements=Requirements(
                     friendship_names=["Eevee"])),
    )
    granite_zone_absol_minigame_region.minigame_location.append(
        Location(name="Vulpix",
                 id=MinigameLocationIds.VULPIX_HURDLE.value,
                 requirements=Requirements(
                     friendship_names=["Vulpix"])),
    )
    if world.options.goal == world.options.goal.option_aftergame or get_all_locations:
        granite_zone_absol_minigame_region.minigame_location.append(
            Location(name="Shaymin",
                     id=MinigameLocationIds.SHAYMIN_HURDLE.value,
                     requirements=Requirements(
                         friendship_names=["Shaymin"],
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]
                     )),
        )
        granite_zone_absol_minigame_region.friendship_locations.append(
            Location(name="Shaymin Unlock",
                     id=FRIENDSHIP_ITEMS["Shaymin"],
                     requirements=Requirements(
                         minigame=MinigameRequirement.absol_hurdle_all,
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]
                     )),
        )
    return granite_zone_absol_minigame_region


def generate_granite_zone_overworld_region(world, get_all_locations: bool = False):
    granite_zone_overworld_region: PokeparkRegion = (
        PokeparkRegion(name="Granite Zone - Overworld",
                       display="Granite Zone - Overworld",
                       requirements=Requirements(
                           unlock_names=[
                               "Granite Zone & Flower Zone Unlock"]
                       ), parent_regions=["Treehouse"]))

    granite_zone_overworld_region.friendship_locations.append(
        Location(name="Lopunny",
                 id=FRIENDSHIP_ITEMS["Lopunny"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch,
                 )),
    )
    granite_zone_overworld_region.friendship_locations.append(
        Location(name="Eevee",
                 id=FRIENDSHIP_ITEMS["Eevee"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch,
                 )),
    )
    granite_zone_overworld_region.friendship_locations.append(
        Location(name="Furret",
                 id=FRIENDSHIP_ITEMS["Furret"]),
    )
    granite_zone_overworld_region.friendship_locations.append(
        Location(name="Charizard",
                 id=FRIENDSHIP_ITEMS["Charizard"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle,
                 )),
    )
    granite_zone_overworld_region.friendship_locations.append(
        Location(name="Drifloon",
                 id=OverworldPokemonLocationIds.DRIFLOON_GRANITE.value),
    )
    granite_zone_overworld_region.friendship_locations.append(
        Location(name="Flygon",
                 id=FRIENDSHIP_ITEMS["Flygon"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch_intermediate,
                 )),
    )
    granite_zone_overworld_region.friendship_locations.append(
        Location(name="Staraptor",
                 id=FRIENDSHIP_ITEMS["Staraptor"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle,
                 )),
    )
    granite_zone_overworld_region.friendship_locations.append(
        Location(name="Aerodactyl",
                 id=FRIENDSHIP_ITEMS["Aerodactyl"],
                 requirements=Requirements(
                     unlock_names=["Aerodactyl Unlock"],
                     powers=PowerRequirement.can_battle,
                 )),
    )
    granite_zone_overworld_region.friendship_locations.append(
        Location(name="Arcanine",
                 id=FRIENDSHIP_ITEMS["Arcanine"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch_intermediate,
                 )),
    )
    granite_zone_overworld_region.friendship_locations.append(
        Location(name="Taillow",
                 id=OverworldPokemonLocationIds.TAILLOW_GRANITE.value,
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch,
                 )),
    )
    granite_zone_overworld_region.friendship_locations.append(
        Location(name="Jolteon",
                 id=FRIENDSHIP_ITEMS["Jolteon"],
                 requirements=Requirements(
                     unlock_names=["Jolteon Unlock"],
                     powers=PowerRequirement.can_play_catch_intermediate,
                     friendcount=91
                 )),
    )
    granite_zone_overworld_region.friendship_locations.append(
        Location(name="Skorupi",
                 id=FRIENDSHIP_ITEMS["Skorupi"]),
    )
    granite_zone_overworld_region.friendship_locations.append(
        Location(name="Marowak",
                 id=OverworldPokemonLocationIds.MAROWAK_GRANITE.value,
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle_thunderbolt_immune
                 )),
    )
    granite_zone_overworld_region.friendship_locations.append(
        Location(name="Porygon-Z",
                 id=FRIENDSHIP_ITEMS["Porygon-Z"]),
    )
    granite_zone_overworld_region.friendship_locations.append(
        Location(name="Tyranitar",
                 id=FRIENDSHIP_ITEMS["Tyranitar"],
                 requirements=Requirements(
                     unlock_names=["Tyranitar Unlock"],
                     powers=PowerRequirement.can_battle
                 )),
    )
    granite_zone_overworld_region.friendship_locations.append(
        Location(name="Garchomp",
                 id=FRIENDSHIP_ITEMS["Garchomp"],
                 requirements=Requirements(
                     unlock_names=["Garchomp Unlock"],
                     powers=PowerRequirement.can_battle_thunderbolt_immune
                 )),
    )
    granite_zone_overworld_region.friendship_locations.append(
        Location(name="Baltoy",
                 id=OverworldPokemonLocationIds.BALTOY_GRANITE.value,
                 requirements=Requirements(
                     unlock_names=["Baltoy Unlock"],
                     powers=PowerRequirement.can_battle_thunderbolt_immune,
                 )),
    )
    granite_zone_overworld_region.friendship_locations.append(
        Location(name="Claydol",
                 id=OverworldPokemonLocationIds.CLAYDOL_GRANITE.value,
                 requirements=Requirements(
                     unlock_names=["Claydol Unlock"],
                     powers=PowerRequirement.can_battle_thunderbolt_immune
                 )),
    )

    granite_zone_overworld_region.unlock_location.append(
        Location(name="Eevee Friendship - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Jolteon Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Granite Zone - Overworld - Eevee"])),
    )
    granite_zone_overworld_region.unlock_location.append(
        Location(name="Staraptor Friendship - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Aerodactyl Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Granite Zone - Overworld - Staraptor"])),
    )
    granite_zone_overworld_region.unlock_location.append(
        Location(name="Baltoy Friendship - Pokemon Unlock",
                 id=UnlockLocationIds.CLAYDOL_GRANITE.value,
                 requirements=Requirements(
                     can_reach_locations=["Granite Zone - Overworld - Baltoy"])),
    )
    return granite_zone_overworld_region


def generate_haunted_zone_mansion_rotom_minigame_region(world, get_all_locations: bool = False):
    haunted_zone_mansion_rotom_minigame_region: PokeparkRegion = PokeparkRegion(
        name="Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up",
        display="Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up",
        requirements=Requirements(
            friendcount=65
        ), parent_regions=["Haunted Zone - Overworld - Mansion"])

    haunted_zone_mansion_rotom_minigame_region.minigame_location.append(
        Location(name="Prisma",
                 id=PRISM_ITEM["Rotom Prisma"],
                 requirements=Requirements(
                     minigame=MinigameRequirement.rotom_shoot_any
                 )),
    )
    haunted_zone_mansion_rotom_minigame_region.minigame_location.append(
        Location(name="Pikachu",
                 id=MinigameLocationIds.PIKACHU_SHOOT.value),
    )
    haunted_zone_mansion_rotom_minigame_region.minigame_location.append(
        Location(name="Magnemite",
                 id=MinigameLocationIds.MAGNEMITE_SHOOT.value,
                 requirements=Requirements(
                     friendship_names=["Magnemite"])),
    )
    haunted_zone_mansion_rotom_minigame_region.minigame_location.append(
        Location(name="Porygon-Z",
                 id=MinigameLocationIds.PORYGONZ_SHOOT.value,
                 requirements=Requirements(
                     friendship_names=["Porygon-Z"])),
    )
    haunted_zone_mansion_rotom_minigame_region.minigame_location.append(
        Location(name="Magnezone",
                 id=MinigameLocationIds.MAGNEZONE_SHOOT.value,
                 requirements=Requirements(
                     friendship_names=["Magnezone"])),
    )
    haunted_zone_mansion_rotom_minigame_region.minigame_location.append(
        Location(name="Gengar",
                 id=MinigameLocationIds.GENGAR_SHOOT.value,
                 requirements=Requirements(
                     friendship_names=["Gengar"])),
    )
    haunted_zone_mansion_rotom_minigame_region.minigame_location.append(
        Location(name="Magmortar",
                 id=MinigameLocationIds.MAGMORTAR_SHOOT.value,
                 requirements=Requirements(
                     friendship_names=["Magmortar"])),
    )
    haunted_zone_mansion_rotom_minigame_region.minigame_location.append(
        Location(name="Electivire",
                 id=MinigameLocationIds.ELECTIVIRE_SHOOT.value,
                 requirements=Requirements(
                     friendship_names=["Electivire"])),
    )
    haunted_zone_mansion_rotom_minigame_region.minigame_location.append(
        Location(name="Mismagius",
                 id=MinigameLocationIds.MISMAGIUS_SHOOT.value,
                 requirements=Requirements(
                     friendship_names=["Mismagius"])),
    )
    haunted_zone_mansion_rotom_minigame_region.minigame_location.append(
        Location(name="Claydol",
                 id=MinigameLocationIds.CLAYDOL_SHOOT.value,
                 requirements=Requirements(
                     friendship_names=["Claydol"])),
    )
    haunted_zone_mansion_rotom_minigame_region.minigame_location.append(
        Location(name="Electabuzz",
                 id=MinigameLocationIds.ELECTABUZZ_SHOOT.value,
                 requirements=Requirements(
                     friendship_names=["Electabuzz"])),
    )
    haunted_zone_mansion_rotom_minigame_region.minigame_location.append(
        Location(name="Haunter",
                 id=MinigameLocationIds.HAUNTER_SHOOT.value,
                 requirements=Requirements(
                     friendship_names=["Haunter"])),
    )
    haunted_zone_mansion_rotom_minigame_region.minigame_location.append(
        Location(name="Abra",
                 id=MinigameLocationIds.ABRA_SHOOT.value,
                 requirements=Requirements(
                     friendship_names=["Abra"])),
    )
    haunted_zone_mansion_rotom_minigame_region.minigame_location.append(
        Location(name="Elekid",
                 id=MinigameLocationIds.ELEKID_SHOOT.value,
                 requirements=Requirements(
                     friendship_names=["Elekid"])),
    )
    haunted_zone_mansion_rotom_minigame_region.minigame_location.append(
        Location(name="Mr. Mime",
                 id=MinigameLocationIds.MRMIME_SHOOT.value,
                 requirements=Requirements(
                     friendship_names=["Mr. Mime"])),
    )
    haunted_zone_mansion_rotom_minigame_region.minigame_location.append(
        Location(name="Baltoy",
                 id=MinigameLocationIds.BALTOY_SHOOT.value,
                 requirements=Requirements(
                     friendship_names=["Baltoy"])),
    )
    if world.options.goal == world.options.goal.option_aftergame or get_all_locations:
        haunted_zone_mansion_rotom_minigame_region.minigame_location.append(
            Location(name="Rotom",
                     id=MinigameLocationIds.ROTOM_SHOOT.value,
                     requirements=Requirements(
                         friendship_names=["Rotom"],
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]
                     )),
        )
        haunted_zone_mansion_rotom_minigame_region.friendship_locations.append(
            Location(name="Rotom Unlock",
                     id=FRIENDSHIP_ITEMS["Rotom"],
                     requirements=Requirements(
                         minigame=MinigameRequirement.rotom_shoot_all,
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]
                     )),
        )
    return haunted_zone_mansion_rotom_minigame_region


def generate_haunted_zone_mansion_dusknoir_minigame_region(world, get_all_locations: bool = False):
    haunted_zone_mansion_dusknoir_minigame_region: PokeparkRegion = PokeparkRegion(
        name="Haunted Zone - Mansion - Dusknoir's Speed Slam",
        display="Haunted Zone - Mansion - Dusknoir's Speed Slam",
        requirements=Requirements(
            unlock_names=["Dusknoir Unlock"]
        ), parent_regions=["Haunted Zone - Overworld - Mansion"])

    haunted_zone_mansion_dusknoir_minigame_region.minigame_location.append(
        Location(name="Prisma",
                 id=PRISM_ITEM["Dusknoir Prisma"],
                 requirements=Requirements(
                     minigame=MinigameRequirement.dusknoir_slam_any
                 )),
    )
    haunted_zone_mansion_dusknoir_minigame_region.minigame_location.append(
        Location(name="Pikachu",
                 id=MinigameLocationIds.PIKACHU_SLAM.value),
    )
    haunted_zone_mansion_dusknoir_minigame_region.minigame_location.append(
        Location(name="Stunky",
                 id=MinigameLocationIds.STUNKY_SLAM.value,
                 requirements=Requirements(
                     friendship_names=["Stunky"])),
    )
    haunted_zone_mansion_dusknoir_minigame_region.minigame_location.append(
        Location(name="Gengar",
                 id=MinigameLocationIds.GENGAR_SLAM.value,
                 requirements=Requirements(
                     friendship_names=["Gengar"])),
    )
    haunted_zone_mansion_dusknoir_minigame_region.minigame_location.append(
        Location(name="Mismagius",
                 id=MinigameLocationIds.MISMAGIUS_SLAM.value,
                 requirements=Requirements(
                     friendship_names=["Mismagius"])),
    )
    haunted_zone_mansion_dusknoir_minigame_region.minigame_location.append(
        Location(name="Scizor",
                 id=MinigameLocationIds.SCIZOR_SLAM.value,
                 requirements=Requirements(
                     friendship_names=["Scizor"])),
    )
    haunted_zone_mansion_dusknoir_minigame_region.minigame_location.append(
        Location(name="Espeon",
                 id=MinigameLocationIds.ESPEON_SLAM.value,
                 requirements=Requirements(
                     friendship_names=["Espeon"])),
    )
    haunted_zone_mansion_dusknoir_minigame_region.minigame_location.append(
        Location(name="Dusknoir",
                 id=MinigameLocationIds.DUSKNOIR_SLAM.value,
                 requirements=Requirements(
                     friendship_names=["Dusknoir"])),
    )
    haunted_zone_mansion_dusknoir_minigame_region.minigame_location.append(
        Location(name="Umbreon",
                 id=MinigameLocationIds.UMBREON_SLAM.value,
                 requirements=Requirements(
                     friendship_names=["Umbreon"])),
    )
    haunted_zone_mansion_dusknoir_minigame_region.minigame_location.append(
        Location(name="Cranidos",
                 id=MinigameLocationIds.CRANIDOS_SLAM.value,
                 requirements=Requirements(
                     friendship_names=["Cranidos"])),
    )
    haunted_zone_mansion_dusknoir_minigame_region.minigame_location.append(
        Location(name="Skuntank",
                 id=MinigameLocationIds.SKUNTANK_SLAM.value,
                 requirements=Requirements(
                     friendship_names=["Skuntank"])),
    )
    haunted_zone_mansion_dusknoir_minigame_region.minigame_location.append(
        Location(name="Electrode",
                 id=MinigameLocationIds.ELECTRODE_SLAM.value,
                 requirements=Requirements(
                     friendship_names=["Electrode"])),
    )
    haunted_zone_mansion_dusknoir_minigame_region.minigame_location.append(
        Location(name="Gastly",
                 id=MinigameLocationIds.GASTLY_SLAM.value,
                 requirements=Requirements(
                     friendship_names=["Gastly"])),
    )
    haunted_zone_mansion_dusknoir_minigame_region.minigame_location.append(
        Location(name="Duskull",
                 id=MinigameLocationIds.DUSKULL_SLAM.value,
                 requirements=Requirements(
                     friendship_names=["Duskull"])),
    )
    haunted_zone_mansion_dusknoir_minigame_region.minigame_location.append(
        Location(name="Misdreavus",
                 id=MinigameLocationIds.MISDREAVUS_SLAM.value,
                 requirements=Requirements(
                     friendship_names=["Misdreavus"])),
    )
    haunted_zone_mansion_dusknoir_minigame_region.minigame_location.append(
        Location(name="Krabby",
                 id=MinigameLocationIds.KRABBY_SLAM.value,
                 requirements=Requirements(
                     friendship_names=["Krabby"])),
    )
    if world.options.goal == world.options.goal.option_aftergame or get_all_locations:
        haunted_zone_mansion_dusknoir_minigame_region.minigame_location.append(
            Location(name="Darkrai",
                     id=MinigameLocationIds.DARKRAI_SLAM.value,
                     requirements=Requirements(
                         friendship_names=["Darkrai"],
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]
                     )),
        )
        haunted_zone_mansion_dusknoir_minigame_region.friendship_locations.append(
            Location(name="Darkrai Unlock",
                     id=FRIENDSHIP_ITEMS["Darkrai"],
                     requirements=Requirements(
                         minigame=MinigameRequirement.dusknoir_slam_all,
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]
                     )),
        )
    return haunted_zone_mansion_dusknoir_minigame_region


def generate_haunted_zone_overworld_mansion_region(world, get_all_locations: bool = False):
    haunted_zone_overworld_mansion_region: PokeparkRegion = (
        PokeparkRegion(name="Haunted Zone - Overworld - Mansion",
                       display="Haunted Zone - Overworld - Mansion",
                       parent_regions=["Haunted Zone - Overworld"]))

    haunted_zone_overworld_mansion_region.friendship_locations.append(
        Location(name="Duskull",
                 id=FRIENDSHIP_ITEMS["Duskull"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch,
                     prisma_names=["Dusknoir Prisma"]
                 )),
    )
    haunted_zone_overworld_mansion_region.friendship_locations.append(
        Location(name="Misdreavus",
                 id=FRIENDSHIP_ITEMS["Misdreavus"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    haunted_zone_overworld_mansion_region.friendship_locations.append(
        Location(name="Pichu",
                 id=FRIENDSHIP_ITEMS["Pichu"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    haunted_zone_overworld_mansion_region.friendship_locations.append(
        Location(name="Umbreon",
                 id=FRIENDSHIP_ITEMS["Umbreon"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch_intermediate,
                     friendcount=76  # + itself
                 )),
    )
    haunted_zone_overworld_mansion_region.friendship_locations.append(
        Location(name="Espeon",
                 id=FRIENDSHIP_ITEMS["Espeon"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch_intermediate,
                     unlock_names=["Espeon Unlock"]
                 )),
    )
    haunted_zone_overworld_mansion_region.friendship_locations.append(
        Location(name="Spinarak",
                 id=FRIENDSHIP_ITEMS["Spinarak"],
                 requirements=Requirements(
                     prisma_names=["Rotom Prisma"])),
    )
    haunted_zone_overworld_mansion_region.friendship_locations.append(
        Location(name="Abra",
                 id=FRIENDSHIP_ITEMS["Abra"]),
    )
    haunted_zone_overworld_mansion_region.friendship_locations.append(
        Location(name="Riolu",
                 id=FRIENDSHIP_ITEMS["Riolu"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle)),
    )
    haunted_zone_overworld_mansion_region.friendship_locations.append(
        Location(name="Voltorb",
                 id=FRIENDSHIP_ITEMS["Voltorb"],
                 requirements=Requirements(
                     unlock_names=["Voltorb Unlock"],
                     can_reach_locations=[
                         "Haunted Zone - Overworld - Mansion - Voltorb vase dash blue gem room"],
                     powers=PowerRequirement.can_battle_thunderbolt_immune)),
    )
    haunted_zone_overworld_mansion_region.friendship_locations.append(
        Location(name="Elekid",
                 id=FRIENDSHIP_ITEMS["Elekid"],
                 requirements=Requirements(
                     unlock_names=["Elekid Unlock"])),
    )
    haunted_zone_overworld_mansion_region.friendship_locations.append(
        Location(name="Electabuzz",
                 id=FRIENDSHIP_ITEMS["Electabuzz"],
                 requirements=Requirements(
                     unlock_names=["Electabuzz Unlock"],
                     powers=PowerRequirement.can_battle_thunderbolt_immune)),
    )
    haunted_zone_overworld_mansion_region.friendship_locations.append(
        Location(name="Luxray",
                 id=FRIENDSHIP_ITEMS["Luxray"],
                 requirements=Requirements(
                     unlock_names=["Luxray Unlock"],
                     powers=PowerRequirement.can_play_catch)),
    )
    haunted_zone_overworld_mansion_region.friendship_locations.append(
        Location(name="Stunky",
                 id=FRIENDSHIP_ITEMS["Stunky"],
                 requirements=Requirements(
                     unlock_names=["Stunky Unlock"],
                     powers=PowerRequirement.can_play_catch)),
    )
    haunted_zone_overworld_mansion_region.friendship_locations.append(
        Location(name="Skuntank",
                 id=FRIENDSHIP_ITEMS["Skuntank"],
                 requirements=Requirements(
                     unlock_names=["Skuntank Unlock"],
                     powers=PowerRequirement.can_battle)),
    )
    haunted_zone_overworld_mansion_region.friendship_locations.append(
        Location(name="Breloom",
                 id=FRIENDSHIP_ITEMS["Breloom"],
                 requirements=Requirements(
                     unlock_names=["Breloom Unlock"],
                     powers=PowerRequirement.can_battle_thunderbolt_immune)),
    )
    haunted_zone_overworld_mansion_region.friendship_locations.append(
        Location(name="Mismagius",
                 id=FRIENDSHIP_ITEMS["Mismagius"],
                 requirements=Requirements(
                     unlock_names=["Mismagius Unlock"],
                     powers=PowerRequirement.can_battle)),
    )
    haunted_zone_overworld_mansion_region.friendship_locations.append(
        Location(name="Electrode",
                 id=FRIENDSHIP_ITEMS["Electrode"],
                 requirements=Requirements(
                     unlock_names=["Electrode Unlock"],
                     prisma_names=["Rotom Prisma"])),
    )
    haunted_zone_overworld_mansion_region.friendship_locations.append(
        Location(name="Haunter",
                 id=FRIENDSHIP_ITEMS["Haunter"],
                 requirements=Requirements(
                     unlock_names=["Haunter Unlock"],
                     powers=PowerRequirement.can_play_catch)),
    )
    haunted_zone_overworld_mansion_region.friendship_locations.append(
        Location(name="Gastly",
                 id=FRIENDSHIP_ITEMS["Gastly"],
                 requirements=Requirements(
                     oneof_item_names=[["Gastly Unlock"], ["Gastly Unlock 2"]],
                     powers=PowerRequirement.can_play_catch)),
    )
    haunted_zone_overworld_mansion_region.friendship_locations.append(
        Location(name="Gengar",
                 id=FRIENDSHIP_ITEMS["Gengar"],
                 requirements=Requirements(
                     unlock_names=["Gengar Unlock"],
                     powers=PowerRequirement.can_battle)),
    )

    haunted_zone_overworld_mansion_region.quest_locations.append(
        Location(name="Gengar painting",
                 id=UNLOCK_ITEMS["Gengar Unlock"],
                 requirements=Requirements(
                     friendcount=85
                 )),
    )
    haunted_zone_overworld_mansion_region.unlock_location.append(
        Location(name="Voltorb vase dash blue gem room",
                 id=UNLOCK_ITEMS["Voltorb Unlock"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_destroy_objects_overworld)),
    )
    haunted_zone_overworld_mansion_region.unlock_location.append(
        Location(name="Elekid Friendship - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Electabuzz Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Haunted Zone - Overworld - Mansion - Elekid"])),
    )
    haunted_zone_overworld_mansion_region.unlock_location.append(
        Location(name="Stunky Friendship - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Skuntank Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Haunted Zone - Overworld - Mansion - Stunky"])),
    )
    haunted_zone_overworld_mansion_region.unlock_location.append(
        Location(name="Umbreon Friendship - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Espeon Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Haunted Zone - Overworld - Mansion - Umbreon"])),
    )
    return haunted_zone_overworld_mansion_region


def generate_haunted_zone_tangrowth_minigame_region(world, get_all_locations: bool = False):
    haunted_zone_tangrowth_minigame_region: PokeparkRegion = PokeparkRegion(
        name="Haunted Zone - Tangrowth's Swing-Along",
        display="Haunted Zone - Tangrowth's Swing-Along",
        parent_regions=["Haunted Zone - Overworld"])

    haunted_zone_tangrowth_minigame_region.minigame_location.append(
        Location(name="Prisma",
                 id=PRISM_ITEM["Tangrowth Prisma"],
                 requirements=Requirements(
                     minigame=MinigameRequirement.tangrowth_swing_any
                 )),
    )
    haunted_zone_tangrowth_minigame_region.minigame_location.append(
        Location(name="Pikachu",
                 id=MinigameLocationIds.PIKACHU_SWING.value),
    )
    haunted_zone_tangrowth_minigame_region.minigame_location.append(
        Location(name="Meowth",
                 id=MinigameLocationIds.MEOWTH_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Meowth"])),
    )
    haunted_zone_tangrowth_minigame_region.minigame_location.append(
        Location(name="Pichu",
                 id=MinigameLocationIds.PICHU_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Pichu"])),
    )
    haunted_zone_tangrowth_minigame_region.minigame_location.append(
        Location(name="Lucario",
                 id=MinigameLocationIds.LUCARIO_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Lucario"])),
    )
    haunted_zone_tangrowth_minigame_region.minigame_location.append(
        Location(name="Infernape",
                 id=MinigameLocationIds.INFERNAPE_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Infernape"])),
    )
    haunted_zone_tangrowth_minigame_region.minigame_location.append(
        Location(name="Blaziken",
                 id=MinigameLocationIds.BLAZIKEN_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Blaziken"])),
    )
    haunted_zone_tangrowth_minigame_region.minigame_location.append(
        Location(name="Riolu",
                 id=MinigameLocationIds.RIOLU_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Riolu"])),
    )
    haunted_zone_tangrowth_minigame_region.minigame_location.append(
        Location(name="Sneasel",
                 id=MinigameLocationIds.SNEASEL_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Sneasel"])),
    )
    haunted_zone_tangrowth_minigame_region.minigame_location.append(
        Location(name="Raichu",
                 id=MinigameLocationIds.RAICHU_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Raichu"])),
    )
    haunted_zone_tangrowth_minigame_region.minigame_location.append(
        Location(name="Ambipom",
                 id=MinigameLocationIds.AMBIPOM_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Ambipom"])),
    )
    haunted_zone_tangrowth_minigame_region.minigame_location.append(
        Location(name="Primeape",
                 id=MinigameLocationIds.PRIMEAPE_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Primeape"])),
    )
    haunted_zone_tangrowth_minigame_region.minigame_location.append(
        Location(name="Aipom",
                 id=MinigameLocationIds.AIPOM_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Aipom"])),
    )
    haunted_zone_tangrowth_minigame_region.minigame_location.append(
        Location(name="Electabuzz",
                 id=MinigameLocationIds.ELECTABUZZ_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Electabuzz"])),
    )
    haunted_zone_tangrowth_minigame_region.minigame_location.append(
        Location(name="Chimchar",
                 id=MinigameLocationIds.CHIMCHAR_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Chimchar"])),
    )
    haunted_zone_tangrowth_minigame_region.minigame_location.append(
        Location(name="Croagunk",
                 id=MinigameLocationIds.CROAGUNK_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Croagunk"])),
    )
    if world.options.goal == world.options.goal.option_aftergame or get_all_locations:
        haunted_zone_tangrowth_minigame_region.minigame_location.append(
            Location(name="Celebi",
                     id=MinigameLocationIds.CELEBI_SWING.value,
                     requirements=Requirements(
                         friendship_names=["Celebi"],
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]
                     )),
        )
        haunted_zone_tangrowth_minigame_region.friendship_locations.append(
            Location(name="Celebi Unlock",
                     id=FRIENDSHIP_ITEMS["Celebi"],
                     requirements=Requirements(
                         minigame=MinigameRequirement.tangrowth_swing_all,
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]
                     )),
        )
    return haunted_zone_tangrowth_minigame_region


def generate_haunted_zone_overworld_region(world, get_all_locations: bool = False):
    haunted_zone_overworld_region: PokeparkRegion = (
        PokeparkRegion(name="Haunted Zone - Overworld",
                       display="Haunted Zone - Overworld",
                       requirements=Requirements(
                           unlock_names=["Haunted Zone Unlock"]),
                       parent_regions=["Treehouse"]))

    haunted_zone_overworld_region.friendship_locations.append(
        Location(name="Drifloon",
                 id=FRIENDSHIP_ITEMS["Drifloon"],
                 requirements=Requirements(
                     prisma_names=["Rotom Prisma"]
                 )),
    )
    haunted_zone_overworld_region.friendship_locations.append(
        Location(name="Raichu",
                 id=OverworldPokemonLocationIds.RAICHU_HAUNTED.value,
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    haunted_zone_overworld_region.friendship_locations.append(
        Location(name="Meowth",
                 id=OverworldPokemonLocationIds.MEOWTH_HAUNTED.value),
    )
    haunted_zone_overworld_region.friendship_locations.append(
        Location(name="Aipom",
                 id=OverworldPokemonLocationIds.AIPOM_HAUNTED.value,
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    haunted_zone_overworld_region.friendship_locations.append(
        Location(name="Ambipom",
                 id=OverworldPokemonLocationIds.AMBIPOM_HAUNTED.value,
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle,
                     unlock_names=["Ambipom Unlock"]
                 )),
    )
    haunted_zone_overworld_region.friendship_locations.append(
        Location(name="Murkrow",
                 id=FRIENDSHIP_ITEMS["Murkrow"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    haunted_zone_overworld_region.friendship_locations.append(
        Location(name="Honchkrow",
                 id=FRIENDSHIP_ITEMS["Honchkrow"],
                 requirements=Requirements(
                     unlock_names=["Honchkrow Unlock"],
                     powers=PowerRequirement.can_battle
                 )),
    )
    haunted_zone_overworld_region.friendship_locations.append(
        Location(name="Gliscor",
                 id=FRIENDSHIP_ITEMS["Gliscor"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle_thunderbolt_immune
                 )),
    )
    haunted_zone_overworld_region.friendship_locations.append(
        Location(name="Metapod",
                 id=FRIENDSHIP_ITEMS["Metapod"],
                 requirements=Requirements(
                     prisma_names=["Rotom Prisma"],
                     unlock_names=["Metapod Unlock"],
                     can_reach_locations=[
                         "Haunted Zone - Overworld - Metapod Tree Dash left Entrance Side"]
                 )),
    )
    haunted_zone_overworld_region.friendship_locations.append(
        Location(name="Kakuna",
                 id=FRIENDSHIP_ITEMS["Kakuna"],
                 requirements=Requirements(
                     prisma_names=["Rotom Prisma"],
                     unlock_names=["Kakuna Unlock"],
                     can_reach_locations=[
                         "Haunted Zone - Overworld - Kakuna Tree Dash right Entrance Side"]
                 )),
    )

    haunted_zone_overworld_region.unlock_location.append(
        Location(name="Aipom Friendship - Pokemon Unlock",
                 id=UnlockLocationIds.AMBIPOM_HAUNTED.value,
                 requirements=Requirements(
                     can_reach_locations=["Haunted Zone - Overworld - Aipom"])),
    )
    haunted_zone_overworld_region.unlock_location.append(
        Location(name="Murkrow Friendship - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Honchkrow Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Haunted Zone - Overworld - Murkrow"])),
    )
    haunted_zone_overworld_region.unlock_location.append(
        Location(name="Metapod Tree Dash left Entrance Side",
                 id=UNLOCK_ITEMS["Metapod Unlock"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_dash_overworld)),
    )
    haunted_zone_overworld_region.unlock_location.append(
        Location(name="Kakuna Tree Dash right Entrance Side",
                 id=UNLOCK_ITEMS["Kakuna Unlock"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_dash_overworld)),
    )
    return haunted_zone_overworld_region


def generate_magma_zone_blaziken_minigame_region(world, get_all_locations: bool = False):
    magma_zone_blaziken_minigame_region: PokeparkRegion = (
        PokeparkRegion(name="Magma Zone - Blaziken's Boulder Bash",
                       display="Magma Zone - Blaziken's Boulder Bash",
                       parent_regions=["Magma Zone - Overworld"]))

    magma_zone_blaziken_minigame_region.minigame_location.append(
        Location(name="Prisma",
                 id=PRISM_ITEM["Blaziken Prisma"],
                 requirements=Requirements(
                     minigame=MinigameRequirement.blaziken_boulder_any
                 )),
    )
    magma_zone_blaziken_minigame_region.minigame_location.append(
        Location(name="Pikachu",
                 id=MinigameLocationIds.PIKACHU_BOULDER.value),
    )
    magma_zone_blaziken_minigame_region.minigame_location.append(
        Location(name="Geodude",
                 id=MinigameLocationIds.GEODUDE_BOULDER.value,
                 requirements=Requirements(
                     friendship_names=["Geodude"])),
    )
    magma_zone_blaziken_minigame_region.minigame_location.append(
        Location(name="Phanpy",
                 id=MinigameLocationIds.PHANPY_BOULDER.value,
                 requirements=Requirements(
                     friendship_names=["Phanpy"])),
    )
    magma_zone_blaziken_minigame_region.minigame_location.append(
        Location(name="Blaziken",
                 id=MinigameLocationIds.BLAZIKEN_BOULDER.value,
                 requirements=Requirements(
                     friendship_names=["Blaziken"])),
    )
    magma_zone_blaziken_minigame_region.minigame_location.append(
        Location(name="Garchomp",
                 id=MinigameLocationIds.GARCHOMP_BOULDER.value,
                 requirements=Requirements(
                     friendship_names=["Garchomp"])),
    )
    magma_zone_blaziken_minigame_region.minigame_location.append(
        Location(name="Scizor",
                 id=MinigameLocationIds.SCIZOR_BOULDER.value,
                 requirements=Requirements(
                     friendship_names=["Scizor"])),
    )
    magma_zone_blaziken_minigame_region.minigame_location.append(
        Location(name="Magmortar",
                 id=MinigameLocationIds.MAGMORTAR_BOULDER.value,
                 requirements=Requirements(
                     friendship_names=["Magmortar"])),
    )
    magma_zone_blaziken_minigame_region.minigame_location.append(
        Location(name="Hitmonchan",
                 id=MinigameLocationIds.HITMONCHAN_BOULDER.value,
                 requirements=Requirements(
                     friendship_names=["Hitmonchan"])),
    )
    magma_zone_blaziken_minigame_region.minigame_location.append(
        Location(name="Machamp",
                 id=MinigameLocationIds.MACHAMP_BOULDER.value,
                 requirements=Requirements(
                     friendship_names=["Machamp"])),
    )
    magma_zone_blaziken_minigame_region.minigame_location.append(
        Location(name="Marowak",
                 id=MinigameLocationIds.MAROWAK_BOULDER.value,
                 requirements=Requirements(
                     friendship_names=["Marowak"])),
    )
    magma_zone_blaziken_minigame_region.minigame_location.append(
        Location(name="Farfetch'd",
                 id=MinigameLocationIds.FARFETCHD_BOULDER.value,
                 requirements=Requirements(
                     friendship_names=["Farfetch'd"])),
    )
    magma_zone_blaziken_minigame_region.minigame_location.append(
        Location(name="Cranidos",
                 id=MinigameLocationIds.CRANIDOS_BOULDER.value,
                 requirements=Requirements(
                     friendship_names=["Cranidos"])),
    )
    magma_zone_blaziken_minigame_region.minigame_location.append(
        Location(name="Camerupt",
                 id=MinigameLocationIds.CAMERUPT_BOULDER.value,
                 requirements=Requirements(
                     friendship_names=["Camerupt"])),
    )
    magma_zone_blaziken_minigame_region.minigame_location.append(
        Location(name="Bastiodon",
                 id=MinigameLocationIds.BASTIODON_BOULDER.value,
                 requirements=Requirements(
                     friendship_names=["Bastiodon"])),
    )
    magma_zone_blaziken_minigame_region.minigame_location.append(
        Location(name="Mawile",
                 id=MinigameLocationIds.MAWILE_BOULDER.value,
                 requirements=Requirements(
                     friendship_names=["Mawile"])),
    )
    if world.options.goal == world.options.goal.option_aftergame or get_all_locations:
        magma_zone_blaziken_minigame_region.minigame_location.append(
            Location(name="Groudon",
                     id=MinigameLocationIds.GROUDON_BOULDER.value,
                     requirements=Requirements(
                         friendship_names=["Groudon"],
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]
                     )),
        )
        magma_zone_blaziken_minigame_region.friendship_locations.append(
            Location(name="Groudon Unlock",
                     id=FRIENDSHIP_ITEMS["Groudon"],
                     requirements=Requirements(
                         minigame=MinigameRequirement.blaziken_boulder_all,
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]
                     )),
        )
    return magma_zone_blaziken_minigame_region


def generate_magma_zone_rhyperior_minigame_region(world, get_all_locations: bool = False):
    magma_zone_rhyperior_minigame_region: PokeparkRegion = (
        PokeparkRegion(name="Magma Zone - Rhyperior's Bumper Burn",
                       display="Magma Zone - Rhyperior's Bumper Burn",
                       requirements=Requirements(
                           can_reach_locations=[
                               "Magma Zone - Overworld - Rhyperior Iron Disc"]),
                       parent_regions=["Magma Zone - Overworld"]))

    magma_zone_rhyperior_minigame_region.minigame_location.append(
        Location(name="Prisma",
                 id=PRISM_ITEM["Rhyperior Prisma"],
                 requirements=Requirements(
                     minigame=MinigameRequirement.rhyperior_bumper_any
                 )),
    )
    magma_zone_rhyperior_minigame_region.minigame_location.append(
        Location(name="Pikachu",
                 id=MinigameLocationIds.PIKACHU_BUMPER.value),
    )
    magma_zone_rhyperior_minigame_region.minigame_location.append(
        Location(name="Magnemite",
                 id=MinigameLocationIds.MAGNEMITE_BUMPER.value,
                 requirements=Requirements(
                     friendship_names=["Magnemite"])),
    )
    magma_zone_rhyperior_minigame_region.minigame_location.append(
        Location(name="Rhyperior",
                 id=MinigameLocationIds.RHYPERIOR_BUMPER.value,
                 requirements=Requirements(
                     friendship_names=["Rhyperior"])),
    )
    magma_zone_rhyperior_minigame_region.minigame_location.append(
        Location(name="Tyranitar",
                 id=MinigameLocationIds.TYRANITAR_BUMPER.value,
                 requirements=Requirements(
                     friendship_names=["Tyranitar"])),
    )
    magma_zone_rhyperior_minigame_region.minigame_location.append(
        Location(name="Hitmontop",
                 id=MinigameLocationIds.HITMONTOP_BUMPER.value,
                 requirements=Requirements(
                     friendship_names=["Hitmontop"])),
    )
    magma_zone_rhyperior_minigame_region.minigame_location.append(
        Location(name="Flareon",
                 id=MinigameLocationIds.FLAREON_BUMPER.value,
                 requirements=Requirements(
                     friendship_names=["Flareon"])),
    )
    magma_zone_rhyperior_minigame_region.minigame_location.append(
        Location(name="Venusaur",
                 id=MinigameLocationIds.VENUSAUR_BUMPER.value,
                 requirements=Requirements(
                     friendship_names=["Venusaur"])),
    )
    magma_zone_rhyperior_minigame_region.minigame_location.append(
        Location(name="Snorlax",
                 id=MinigameLocationIds.SNORLAX_BUMPER.value,
                 requirements=Requirements(
                     friendship_names=["Snorlax"])),
    )
    magma_zone_rhyperior_minigame_region.minigame_location.append(
        Location(name="Torterra",
                 id=MinigameLocationIds.TORTERRA_BUMPER.value,
                 requirements=Requirements(
                     friendship_names=["Torterra"])),
    )
    magma_zone_rhyperior_minigame_region.minigame_location.append(
        Location(name="Magnezone",
                 id=MinigameLocationIds.MAGNEZONE_BUMPER.value,
                 requirements=Requirements(
                     friendship_names=["Magnezone"])),
    )
    magma_zone_rhyperior_minigame_region.minigame_location.append(
        Location(name="Claydol",
                 id=MinigameLocationIds.CLAYDOL_BUMPER.value,
                 requirements=Requirements(
                     friendship_names=["Claydol"])),
    )
    magma_zone_rhyperior_minigame_region.minigame_location.append(
        Location(name="Quilava",
                 id=MinigameLocationIds.QUILAVA_BUMPER.value,
                 requirements=Requirements(
                     friendship_names=["Quilava"])),
    )
    magma_zone_rhyperior_minigame_region.minigame_location.append(
        Location(name="Torkoal",
                 id=MinigameLocationIds.TORKOAL_BUMPER.value,
                 requirements=Requirements(
                     friendship_names=["Torkoal"])),
    )
    magma_zone_rhyperior_minigame_region.minigame_location.append(
        Location(name="Baltoy",
                 id=MinigameLocationIds.BALTOY_BUMPER.value,
                 requirements=Requirements(
                     friendship_names=["Baltoy"])),
    )
    magma_zone_rhyperior_minigame_region.minigame_location.append(
        Location(name="Bonsly",
                 id=MinigameLocationIds.BONSLY_BUMPER.value,
                 requirements=Requirements(
                     friendship_names=["Bonsly"])),
    )
    if world.options.goal == world.options.goal.option_aftergame or get_all_locations:
        magma_zone_rhyperior_minigame_region.minigame_location.append(
            Location(name="Heatran",
                     id=MinigameLocationIds.HEATRAN_BUMPER.value,
                     requirements=Requirements(
                         friendship_names=["Heatran"],
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]
                     )),
        )
        magma_zone_rhyperior_minigame_region.friendship_locations.append(
            Location(name="Heatran Unlock",
                     id=FRIENDSHIP_ITEMS["Heatran"],
                     requirements=Requirements(
                         minigame=MinigameRequirement.rhyperior_bumper_all,
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]

                     )),
        )
    return magma_zone_rhyperior_minigame_region


def generate_magma_zone_overworld_region(world, get_all_locations: bool = False):
    magma_zone_overworld_region: PokeparkRegion = (
        PokeparkRegion(name="Magma Zone - Overworld",
                       display="Magma Zone - Overworld",
                       requirements=Requirements(
                           unlock_names=["Cavern Zone & Magma Zone Unlock"]),
                       parent_regions=["Cavern Zone - Overworld",
                                       "Treehouse"]))

    magma_zone_overworld_region.friendship_locations.append(
        Location(name="Aron",
                 id=OverworldPokemonLocationIds.ARON_MAGMA.value,
                 requirements=Requirements(
                     powers=PowerRequirement.can_dash_overworld
                 )),
    )
    magma_zone_overworld_region.friendship_locations.append(
        Location(name="Torchic",
                 id=OverworldPokemonLocationIds.TORCHIC_MAGMA.value,
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle
                 )),
    )
    magma_zone_overworld_region.friendship_locations.append(
        Location(name="Chimchar",
                 id=OverworldPokemonLocationIds.CHIMCHAR_MAGMA.value,
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle
                 )),
    )
    magma_zone_overworld_region.friendship_locations.append(
        Location(name="Geodude",
                 id=OverworldPokemonLocationIds.GEODUDE_MAGMA.value),
    )
    magma_zone_overworld_region.friendship_locations.append(
        Location(name="Bonsly",
                 id=OverworldPokemonLocationIds.BONSLY_MAGMA.value),
    )
    magma_zone_overworld_region.friendship_locations.append(
        Location(name="Camerupt",
                 id=FRIENDSHIP_ITEMS["Camerupt"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle_thunderbolt_immune
                 )),
    )
    magma_zone_overworld_region.friendship_locations.append(
        Location(name="Magby",
                 id=FRIENDSHIP_ITEMS["Magby"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    magma_zone_overworld_region.friendship_locations.append(
        Location(name="Magby - Battle",
                 id=OverworldPokemonLocationIds.MAGBY_MAGMA_BATTLE.value,
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle
                 )),
    )
    magma_zone_overworld_region.friendship_locations.append(
        Location(name="Vulpix",
                 id=FRIENDSHIP_ITEMS["Vulpix"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    magma_zone_overworld_region.friendship_locations.append(
        Location(name="Ninetales",
                 id=FRIENDSHIP_ITEMS["Ninetales"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch_intermediate,
                     unlock_names=["Ninetales Unlock"]
                 )),
    )
    magma_zone_overworld_region.friendship_locations.append(
        Location(name="Quilava",
                 id=FRIENDSHIP_ITEMS["Quilava"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle
                 )),
    )
    magma_zone_overworld_region.friendship_locations.append(
        Location(name="Flareon",
                 id=FRIENDSHIP_ITEMS["Flareon"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle,
                     friendcount=61
                 )),
    )
    magma_zone_overworld_region.friendship_locations.append(
        Location(name="Infernape",
                 id=FRIENDSHIP_ITEMS["Infernape"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle,
                     unlock_names=["Infernape Unlock"]
                 )),
    )
    magma_zone_overworld_region.friendship_locations.append(
        Location(name="Farfetch'd",
                 id=FRIENDSHIP_ITEMS["Farfetch'd"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle
                 )),
    )
    magma_zone_overworld_region.friendship_locations.append(
        Location(name="Ponyta",
                 id=FRIENDSHIP_ITEMS["Ponyta"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch_intermediate,
                     unlock_names=["Ponyta Unlock"]
                 )),
    )
    magma_zone_overworld_region.friendship_locations.append(
        Location(name="Torkoal",
                 id=FRIENDSHIP_ITEMS["Torkoal"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle,
                     unlock_names=["Torkoal Unlock"]
                 )),
    )
    magma_zone_overworld_region.friendship_locations.append(
        Location(name="Golem",
                 id=FRIENDSHIP_ITEMS["Golem"],
                 requirements=Requirements(
                     unlock_names=["Golem Unlock"]
                 )),
    )
    magma_zone_overworld_region.friendship_locations.append(
        Location(name="Baltoy",
                 id=FRIENDSHIP_ITEMS["Baltoy"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle_thunderbolt_immune,
                     unlock_names=["Baltoy Unlock"],
                     can_reach_locations=["Magma Zone - Overworld - Baltoy Crate Dash"]
                 )),
    )
    magma_zone_overworld_region.friendship_locations.append(
        Location(name="Claydol",
                 id=FRIENDSHIP_ITEMS["Claydol"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle_thunderbolt_immune,
                     unlock_names=["Claydol Unlock"]
                 )),
    )
    magma_zone_overworld_region.friendship_locations.append(
        Location(name="Hitmonchan",
                 id=FRIENDSHIP_ITEMS["Hitmonchan"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle,
                     unlock_names=["Hitmonchan Unlock"]
                 )),
    )
    magma_zone_overworld_region.friendship_locations.append(
        Location(name="Hitmontop",
                 id=FRIENDSHIP_ITEMS["Hitmontop"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_dash_overworld,
                 )),
    )
    magma_zone_overworld_region.friendship_locations.append(
        Location(name="Magmortar",
                 id=FRIENDSHIP_ITEMS["Magmortar"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle,
                     unlock_names=["Magmortar Unlock"]
                 )),
    )
    magma_zone_overworld_region.friendship_locations.append(
        Location(name="Blaziken",
                 id=FRIENDSHIP_ITEMS["Blaziken"],
                 requirements=Requirements(
                     prisma_names=[
                         "Bulbasaur Prisma",
                         "Venusaur Prisma",
                         "Pelipper Prisma",
                         "Gyarados Prisma",
                         "Empoleon Prisma",
                         "Bastiodon Prisma",
                         "Rhyperior Prisma",
                         "Blaziken Prisma",
                         "Tangrowth Prisma",
                         "Dusknoir Prisma",
                         "Rotom Prisma",
                         "Absol Prisma",
                         "Salamence Prisma",
                         "Rayquaza Prisma"]
                 )),
    )

    magma_zone_overworld_region.unlock_location.append(
        Location(name="Chimchar Friendship - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Infernape Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Magma Zone - Overworld - Chimchar"])),
    )
    magma_zone_overworld_region.unlock_location.append(
        Location(name="Vulpix Friendship - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Ninetales Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Magma Zone - Overworld - Vulpix"])),
    )
    magma_zone_overworld_region.unlock_location.append(
        Location(name="Baltoy Crate Dash",
                 id=UNLOCK_ITEMS["Baltoy Unlock"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_destroy_objects_overworld
                 )),
    )
    magma_zone_overworld_region.unlock_location.append(
        Location(name="Baltoy Friendship - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Claydol Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Magma Zone - Overworld - Baltoy"])),
    )
    magma_zone_overworld_region.unlock_location.append(
        Location(name="Hitmonchan Friendship - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Hitmonlee Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Magma Zone - Overworld - Hitmonchan"])),
    )

    magma_zone_overworld_region.quest_locations.append(
        Location(name="Meditite Quiz",
                 id=QuestLocationIds.MEDITITE_QUIZ.value),
    )
    magma_zone_overworld_region.quest_locations.append(
        Location(name="Rhyperior Iron Disc",
                 id=QuestLocationIds.RHYPERIOR_DISC.value,
                 requirements=Requirements(
                     powers=PowerRequirement.can_dash_overworld
                 )),
    )

    return magma_zone_overworld_region


def generate_cavern_zone_bastiodon_minigame_region(world, get_all_locations: bool = False):
    cavern_zone_bastiodon_minigame_region: PokeparkRegion = (
        PokeparkRegion(name="Cavern Zone - Bastiodon's Panel Crush",
                       display="Cavern Zone - Bastiodon's Panel Crush",
                       requirements=Requirements(
                           friendcount=50),
                       parent_regions=["Cavern Zone - Overworld"]))

    cavern_zone_bastiodon_minigame_region.minigame_location.append(
        Location(name="Prisma",
                 id=PRISM_ITEM["Bastiodon Prisma"],
                 requirements=Requirements(
                     minigame=MinigameRequirement.bastiodon_panel_any
                 )),
    )
    cavern_zone_bastiodon_minigame_region.minigame_location.append(
        Location(name="Pikachu",
                 id=MinigameLocationIds.PIKACHU_PANEL.value),
    )
    cavern_zone_bastiodon_minigame_region.minigame_location.append(
        Location(name="Sableye",
                 id=MinigameLocationIds.SABLEYE_PANEL.value,
                 requirements=Requirements(
                     friendship_names=["Sableye"])),
    )
    cavern_zone_bastiodon_minigame_region.minigame_location.append(
        Location(name="Meowth",
                 id=MinigameLocationIds.MEOWTH_PANEL.value,
                 requirements=Requirements(
                     friendship_names=["Meowth"])),
    )
    cavern_zone_bastiodon_minigame_region.minigame_location.append(
        Location(name="Torchic",
                 id=MinigameLocationIds.TORCHIC_PANEL.value,
                 requirements=Requirements(
                     friendship_names=["Torchic"])),
    )
    cavern_zone_bastiodon_minigame_region.minigame_location.append(
        Location(name="Electivire",
                 id=MinigameLocationIds.ELECTIVIRE_PANEL.value,
                 requirements=Requirements(
                     friendship_names=["Electivire"])),
    )
    cavern_zone_bastiodon_minigame_region.minigame_location.append(
        Location(name="Magmortar",
                 id=MinigameLocationIds.MAGMORTAR_PANEL.value,
                 requirements=Requirements(
                     friendship_names=["Magmortar"])),
    )
    cavern_zone_bastiodon_minigame_region.minigame_location.append(
        Location(name="Hitmonlee",
                 id=MinigameLocationIds.HITMONLEE_PANEL.value,
                 requirements=Requirements(
                     friendship_names=["Hitmonlee"])),
    )
    cavern_zone_bastiodon_minigame_region.minigame_location.append(
        Location(name="Ursaring",
                 id=MinigameLocationIds.URSARING_PANEL.value,
                 requirements=Requirements(
                     friendship_names=["Ursaring"])),
    )
    cavern_zone_bastiodon_minigame_region.minigame_location.append(
        Location(name="Mr. Mime",
                 id=MinigameLocationIds.MRMIME_PANEL.value,
                 requirements=Requirements(
                     friendship_names=["Mr. Mime"])),
    )
    cavern_zone_bastiodon_minigame_region.minigame_location.append(
        Location(name="Raichu",
                 id=MinigameLocationIds.RAICHU_PANEL.value,
                 requirements=Requirements(
                     friendship_names=["Raichu"])),
    )
    cavern_zone_bastiodon_minigame_region.minigame_location.append(
        Location(name="Sudowoodo",
                 id=MinigameLocationIds.SUDOWOODO_PANEL.value,
                 requirements=Requirements(
                     friendship_names=["Sudowoodo"])),
    )
    cavern_zone_bastiodon_minigame_region.minigame_location.append(
        Location(name="Charmander",
                 id=MinigameLocationIds.CHARMANDER_PANEL.value,
                 requirements=Requirements(
                     friendship_names=["Charmander"])),
    )
    cavern_zone_bastiodon_minigame_region.minigame_location.append(
        Location(name="Gible",
                 id=MinigameLocationIds.GIBLE_PANEL.value,
                 requirements=Requirements(
                     friendship_names=["Gible"])),
    )
    cavern_zone_bastiodon_minigame_region.minigame_location.append(
        Location(name="Chimchar",
                 id=MinigameLocationIds.CHIMCHAR_PANEL.value,
                 requirements=Requirements(
                     friendship_names=["Chimchar"])),
    )
    cavern_zone_bastiodon_minigame_region.minigame_location.append(
        Location(name="Magby",
                 id=MinigameLocationIds.MAGBY_PANEL.value,
                 requirements=Requirements(
                     friendship_names=["Magby"])),
    )
    if world.options.goal == world.options.goal.option_aftergame or get_all_locations:
        cavern_zone_bastiodon_minigame_region.minigame_location.append(
            Location(name="Metagross",
                     id=MinigameLocationIds.METAGROSS_PANEL.value,
                     requirements=Requirements(
                         friendship_names=["Metagross"],
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]
                     )),
        )
        cavern_zone_bastiodon_minigame_region.friendship_locations.append(
            Location(name="Metagross Unlock",
                     id=FRIENDSHIP_ITEMS["Metagross"],
                     requirements=Requirements(
                         minigame=MinigameRequirement.bastiodon_panel_all,
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]
                     )),
        )
    return cavern_zone_bastiodon_minigame_region


def generate_cavern_zone_overworld_region(world, get_all_locations: bool = False):
    cavern_zone_overworld_region: PokeparkRegion = (
        PokeparkRegion(name="Cavern Zone - Overworld",
                       display="Cavern Zone - Overworld",
                       requirements=Requirements(
                           unlock_names=["Cavern Zone & Magma Zone Unlock"]),
                       parent_regions=["Treehouse"]))

    cavern_zone_overworld_region.friendship_locations.append(
        Location(name="Magnemite",
                 id=FRIENDSHIP_ITEMS["Magnemite"],
                 requirements=Requirements(
                     unlock_names=["Magnemite Unlock"],
                     can_reach_locations=["Cavern Zone - Overworld - Magnemite Crate Dash Entrance Area"]
                 )),
    )
    cavern_zone_overworld_region.friendship_locations.append(
        Location(name="Magnemite 2",
                 id=OverworldPokemonLocationIds.MAGNEMITE_CAVERN_2.value,
                 requirements=Requirements(
                     unlock_names=["Magnemite Unlock 2"],
                     can_reach_locations=[
                         "Cavern Zone - Overworld - Magnemite Crate Dash Magma Zone Entrance"]
                 )),
    )
    cavern_zone_overworld_region.friendship_locations.append(
        Location(name="Magnemite 3",
                 id=OverworldPokemonLocationIds.MAGNEMITE_CAVERN_3.value,
                 requirements=Requirements(
                     unlock_names=["Magnemite Unlock 3"],
                     can_reach_locations=[
                         "Cavern Zone - Overworld - Magnemite Crate Dash Magma Zone Entrance"]
                 )),
    )
    cavern_zone_overworld_region.friendship_locations.append(
        Location(name="Magnezone",
                 id=FRIENDSHIP_ITEMS["Magnezone"],
                 requirements=Requirements(
                     unlock_names=["Magnezone Unlock"],
                     powers=PowerRequirement.can_battle_thunderbolt_immune
                 )),
    )
    cavern_zone_overworld_region.friendship_locations.append(
        Location(name="Geodude",
                 id=FRIENDSHIP_ITEMS["Geodude"]),
    )
    cavern_zone_overworld_region.friendship_locations.append(
        Location(name="Torchic",
                 id=FRIENDSHIP_ITEMS["Torchic"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle
                 )),
    )
    cavern_zone_overworld_region.friendship_locations.append(
        Location(name="Machamp",
                 id=FRIENDSHIP_ITEMS["Machamp"]),
    )
    cavern_zone_overworld_region.friendship_locations.append(
        Location(name="Machamp - Battle",
                 id=OverworldPokemonLocationIds.MACHAMP_CAVERN_BATTLE.value,
                 requirements=Requirements(
                     unlock_names=["Machamp Unlock"],
                     powers=PowerRequirement.can_battle
                 )),
    )
    cavern_zone_overworld_region.friendship_locations.append(
        Location(name="Teddiursa",
                 id=OverworldPokemonLocationIds.TEDDIURSA_CAVERN.value),
    )
    cavern_zone_overworld_region.friendship_locations.append(
        Location(name="Meowth",
                 id=FRIENDSHIP_ITEMS["Meowth"]),
    )
    cavern_zone_overworld_region.friendship_locations.append(
        Location(name="Bonsly",
                 id=OverworldPokemonLocationIds.BONSLY_CAVERN.value),
    )
    cavern_zone_overworld_region.friendship_locations.append(
        Location(name="Chimchar",
                 id=OverworldPokemonLocationIds.CHIMCHAR_CAVERN.value,
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle
                 )),
    )
    cavern_zone_overworld_region.friendship_locations.append(
        Location(name="Cranidos",
                 id=FRIENDSHIP_ITEMS["Cranidos"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle
                 )),
    )
    cavern_zone_overworld_region.friendship_locations.append(
        Location(name="Zubat",
                 id=FRIENDSHIP_ITEMS["Zubat"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    cavern_zone_overworld_region.friendship_locations.append(
        Location(name="Golbat",
                 id=FRIENDSHIP_ITEMS["Golbat"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch_intermediate
                 )),
    )
    cavern_zone_overworld_region.friendship_locations.append(
        Location(name="Sudowoodo",
                 id=OverworldPokemonLocationIds.SUDOWOODO_CAVERN.value,
                 requirements=Requirements(
                     unlock_names=["Sudowoodo Unlock"])),
    )
    cavern_zone_overworld_region.friendship_locations.append(
        Location(name="Scizor",
                 id=FRIENDSHIP_ITEMS["Scizor"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle
                 )),
    )
    cavern_zone_overworld_region.friendship_locations.append(
        Location(name="Marowak",
                 id=FRIENDSHIP_ITEMS["Marowak"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle_thunderbolt_immune
                 )),
    )
    cavern_zone_overworld_region.friendship_locations.append(
        Location(name="Aron",
                 id=FRIENDSHIP_ITEMS["Aron"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_destroy_objects_overworld
                 )),
    )
    cavern_zone_overworld_region.friendship_locations.append(
        Location(name="Dugtrio",
                 id=FRIENDSHIP_ITEMS["Dugtrio"]),
    )
    cavern_zone_overworld_region.friendship_locations.append(
        Location(name="Gible",
                 id=FRIENDSHIP_ITEMS["Gible"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle_thunderbolt_immune
                 )),
    )
    cavern_zone_overworld_region.friendship_locations.append(
        Location(name="Phanpy",
                 id=FRIENDSHIP_ITEMS["Phanpy"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_destroy_objects_overworld,
                     unlock_names=["Phanpy Unlock"]
                 )),
    )
    cavern_zone_overworld_region.friendship_locations.append(
        Location(name="Raichu",
                 id=FRIENDSHIP_ITEMS["Raichu"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch_intermediate,
                     unlock_names=["Raichu Unlock"]
                 )),
    )
    cavern_zone_overworld_region.friendship_locations.append(
        Location(name="Hitmonlee",
                 id=FRIENDSHIP_ITEMS["Hitmonlee"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle,
                     unlock_names=["Hitmonlee Unlock"]
                 )),
    )
    cavern_zone_overworld_region.friendship_locations.append(
        Location(name="Electivire",
                 id=FRIENDSHIP_ITEMS["Electivire"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle,
                     unlock_names=["Electivire Unlock"]
                 )),
    )

    cavern_zone_overworld_region.unlock_location.append(
        Location(name="Magnemite Crate Dash Entrance Area",
                 id=UNLOCK_ITEMS["Magnemite Unlock"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_destroy_objects_overworld
                 )),
    )
    cavern_zone_overworld_region.unlock_location.append(
        Location(name="Magnemite Crate Dash Magma Zone Entrance",
                 id=UNLOCK_ITEMS["Magnemite Unlock 2"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_destroy_objects_overworld
                 )),
    )
    cavern_zone_overworld_region.unlock_location.append(
        Location(name="Magnemite Crate Dash Deep Inside",
                 id=UNLOCK_ITEMS["Magnemite Unlock 3"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_destroy_objects_overworld
                 )),
    )
    cavern_zone_overworld_region.unlock_location.append(
        Location(name="Machamp Friendship - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Machamp Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Cavern Zone - Overworld - Machamp"])),
    )
    cavern_zone_overworld_region.unlock_location.append(
        Location(name="Bonsly Friendship - Pokemon Unlock",
                 id=UnlockLocationIds.SUDOWOODO_CAVERN.value,
                 requirements=Requirements(
                     can_reach_locations=["Cavern Zone - Overworld - Bonsly"])),
    )
    cavern_zone_overworld_region.unlock_location.append(
        Location(name="Diglett Crate Dash",
                 id=UNLOCK_ITEMS["Diglett Unlock"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_destroy_objects_overworld
                 )),
    )
    return cavern_zone_overworld_region


def generate_ice_zone_empoleon_minigame_region(world, get_all_locations: bool = False):
    ice_zone_empoleon_minigame_region: PokeparkRegion = (
        PokeparkRegion(name="Ice Zone - Empoleon's Snow Slide",
                       display="Ice Zone - Empoleon's Snow Slide",
                       parent_regions=["Ice Zone - Overworld"]))

    ice_zone_empoleon_minigame_region.minigame_location.append(
        Location(name="Prisma",
                 id=PRISM_ITEM["Empoleon Prisma"],
                 requirements=Requirements(
                     minigame=MinigameRequirement.empoleon_slide_any
                 )),
    )
    ice_zone_empoleon_minigame_region.minigame_location.append(
        Location(name="Pikachu",
                 id=MinigameLocationIds.PIKACHU_SLIDE.value,
                 requirements=Requirements(
                     unlock_names=["Pikachu Snowboard"])),
    )
    ice_zone_empoleon_minigame_region.minigame_location.append(
        Location(name="Teddiursa",
                 id=MinigameLocationIds.TEDDIURSA_SLIDE.value,
                 requirements=Requirements(
                     friendship_names=["Teddiursa"])),
    )
    ice_zone_empoleon_minigame_region.minigame_location.append(
        Location(name="Magikarp",
                 id=MinigameLocationIds.MAGIKARP_SLIDE.value,
                 requirements=Requirements(
                     friendship_names=["Magikarp"])),
    )
    ice_zone_empoleon_minigame_region.minigame_location.append(
        Location(name="Empoleon",
                 id=MinigameLocationIds.EMPOLEON_SLIDE.value,
                 requirements=Requirements(
                     friendship_names=["Empoleon"])),
    )
    ice_zone_empoleon_minigame_region.minigame_location.append(
        Location(name="Glaceon",
                 id=MinigameLocationIds.GLACEON_SLIDE.value,
                 requirements=Requirements(
                     friendship_names=["Glaceon"])),
    )
    ice_zone_empoleon_minigame_region.minigame_location.append(
        Location(name="Blastoise",
                 id=MinigameLocationIds.BLASTOISE_SLIDE.value,
                 requirements=Requirements(
                     friendship_names=["Blastoise"])),
    )
    ice_zone_empoleon_minigame_region.minigame_location.append(
        Location(name="Glalie",
                 id=MinigameLocationIds.GLALIE_SLIDE.value,
                 requirements=Requirements(
                     friendship_names=["Glalie"])),
    )
    ice_zone_empoleon_minigame_region.minigame_location.append(
        Location(name="Lapras",
                 id=MinigameLocationIds.LAPRAS_SLIDE.value,
                 requirements=Requirements(
                     friendship_names=["Lapras"])),
    )
    ice_zone_empoleon_minigame_region.minigame_location.append(
        Location(name="Delibird",
                 id=MinigameLocationIds.DELIBIRD_SLIDE.value,
                 requirements=Requirements(
                     friendship_names=["Delibird"])),
    )
    ice_zone_empoleon_minigame_region.minigame_location.append(
        Location(name="Piloswine",
                 id=MinigameLocationIds.PILOSWINE_SLIDE.value,
                 requirements=Requirements(
                     friendship_names=["Piloswine"])),
    )
    ice_zone_empoleon_minigame_region.minigame_location.append(
        Location(name="Prinplup",
                 id=MinigameLocationIds.PRINPLUP_SLIDE.value,
                 requirements=Requirements(
                     friendship_names=["Prinplup"])),
    )
    ice_zone_empoleon_minigame_region.minigame_location.append(
        Location(name="Squirtle",
                 id=MinigameLocationIds.SQUIRTLE_SLIDE.value,
                 requirements=Requirements(
                     friendship_names=["Squirtle"])),
    )
    ice_zone_empoleon_minigame_region.minigame_location.append(
        Location(name="Piplup",
                 id=MinigameLocationIds.PIPLUP_SLIDE.value,
                 requirements=Requirements(
                     friendship_names=["Piplup"])),
    )
    ice_zone_empoleon_minigame_region.minigame_location.append(
        Location(name="Quagsire",
                 id=MinigameLocationIds.QUAGSIRE_SLIDE.value,
                 requirements=Requirements(
                     friendship_names=["Quagsire"])),
    )
    ice_zone_empoleon_minigame_region.minigame_location.append(
        Location(name="Spheal",
                 id=MinigameLocationIds.SPHEAL_SLIDE.value,
                 requirements=Requirements(
                     friendship_names=["Spheal"])),
    )
    if world.options.goal == world.options.goal.option_aftergame or get_all_locations:
        ice_zone_empoleon_minigame_region.minigame_location.append(
            Location(name="Suicune",
                     id=MinigameLocationIds.SUICUNE_SLIDE.value,
                     requirements=Requirements(
                         friendship_names=["Suicune"],
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]
                     )),
        )
        ice_zone_empoleon_minigame_region.friendship_locations.append(
            Location(name="Suicune Unlock",
                     id=FRIENDSHIP_ITEMS["Suicune"],
                     requirements=Requirements(
                         minigame=MinigameRequirement.empoleon_slide_all,
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]

                     )),
        )
    return ice_zone_empoleon_minigame_region


def generate_ice_zone_overworld_lower_lift_region(world, get_all_locations: bool = False):
    ice_zone_overworld_lower_lift_region: PokeparkRegion = PokeparkRegion(
        name="Ice Zone - Overworld - Lower Lift Region",
        display="Ice Zone - Overworld - Lower Lift Region",
        requirements=Requirements(
            friendship_names=["Prinplup"]), parent_regions=["Ice Zone - Overworld"])

    ice_zone_overworld_lower_lift_region.friendship_locations.append(
        Location(name="Corphish",
                 id=OverworldPokemonLocationIds.CORPHISH_ICE.value,
                 requirements=Requirements(
                     unlock_names=["Corphish Unlock"],
                     powers=PowerRequirement.can_battle
                 )),
    )
    ice_zone_overworld_lower_lift_region.friendship_locations.append(
        Location(name="Wingull",
                 id=OverworldPokemonLocationIds.WINGULL_ICE.value,
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    ice_zone_overworld_lower_lift_region.friendship_locations.append(
        Location(name="Quagsire",
                 id=FRIENDSHIP_ITEMS["Quagsire"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_destroy_objects_overworld
                 )),
    )
    return ice_zone_overworld_lower_lift_region


def generate_ice_zone_overworld_region(world, get_all_locations: bool = False):
    ice_zone_overworld_region: PokeparkRegion = (
        PokeparkRegion(name="Ice Zone - Overworld",
                       display="Ice Zone - Overworld",
                       requirements=Requirements(
                           unlock_names=["Ice Zone Unlock"]),
                       parent_regions=["Treehouse", "Beach Zone - Overworld"]))

    ice_zone_overworld_region.friendship_locations.append(
        Location(name="Lapras",
                 id=FRIENDSHIP_ITEMS["Lapras"]),
    )
    ice_zone_overworld_region.friendship_locations.append(
        Location(name="Spheal",
                 id=FRIENDSHIP_ITEMS["Spheal"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    ice_zone_overworld_region.friendship_locations.append(
        Location(name="Krabby",
                 id=OverworldPokemonLocationIds.KRABBY_ICE.value,
                 requirements=Requirements(
                     unlock_names=["Krabby Unlock"],
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    ice_zone_overworld_region.friendship_locations.append(
        Location(name="Mudkip",
                 id=OverworldPokemonLocationIds.MUDKIP_ICE.value,
                 requirements=Requirements(
                     unlock_names=["Mudkip Unlock"])),
    )
    ice_zone_overworld_region.friendship_locations.append(
        Location(name="Octillery",
                 id=FRIENDSHIP_ITEMS["Octillery"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle
                 )),
    )
    ice_zone_overworld_region.friendship_locations.append(
        Location(name="Teddiursa",
                 id=FRIENDSHIP_ITEMS["Teddiursa"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    ice_zone_overworld_region.friendship_locations.append(
        Location(name="Taillow",
                 id=OverworldPokemonLocationIds.TAILLOW_ICE.value,
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    ice_zone_overworld_region.friendship_locations.append(
        Location(name="Starly",
                 id=OverworldPokemonLocationIds.STARLY_ICE.value,
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    ice_zone_overworld_region.friendship_locations.append(
        Location(name="Staravia",
                 id=OverworldPokemonLocationIds.STARAVIA_ICE.value,
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle
                 )),
    )
    ice_zone_overworld_region.friendship_locations.append(
        Location(name="Delibird",
                 id=FRIENDSHIP_ITEMS["Delibird"],
                 requirements=Requirements(
                     can_reach_locations=["Ice Zone - Overworld - Christmas Tree Present 4"]
                 )),
    )
    ice_zone_overworld_region.friendship_locations.append(
        Location(name="Smoochum",
                 id=FRIENDSHIP_ITEMS["Smoochum"],
                 requirements=Requirements(
                     unlock_names=["Smoochum Unlock"],
                     powers=PowerRequirement.can_battle
                 )),
    )
    ice_zone_overworld_region.friendship_locations.append(
        Location(name="Squirtle",
                 id=FRIENDSHIP_ITEMS["Squirtle"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle,
                     unlock_names=["Squirtle Unlock"])),
    )
    ice_zone_overworld_region.friendship_locations.append(
        Location(name="Glaceon",
                 id=FRIENDSHIP_ITEMS["Glaceon"],
                 requirements=Requirements(
                     friendcount=51,
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    ice_zone_overworld_region.friendship_locations.append(
        Location(name="Prinplup",
                 id=FRIENDSHIP_ITEMS["Prinplup"],
                 requirements=Requirements(
                     can_reach_locations=["Ice Zone - Overworld - Igloo Quest 3"],
                     powers=PowerRequirement.can_battle
                 )),
    )
    ice_zone_overworld_region.friendship_locations.append(
        Location(name="Sneasel",
                 id=FRIENDSHIP_ITEMS["Sneasel"],
                 requirements=Requirements(
                     unlock_names=["Sneasel Unlock"],
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    ice_zone_overworld_region.friendship_locations.append(
        Location(name="Piloswine",
                 id=FRIENDSHIP_ITEMS["Piloswine"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle_thunderbolt_immune
                 )),
    )
    ice_zone_overworld_region.friendship_locations.append(
        Location(name="Glalie",
                 id=FRIENDSHIP_ITEMS["Glalie"],
                 requirements=Requirements(
                     can_reach_locations=["Ice Zone - Overworld - Igloo Quest 3"]
                 )),
    )
    ice_zone_overworld_region.friendship_locations.append(
        Location(name="Primeape",
                 id=FRIENDSHIP_ITEMS["Primeape"],
                 requirements=Requirements(
                     unlock_names=["Primeape Unlock"],
                     powers=PowerRequirement.can_battle
                 )),
    )
    ice_zone_overworld_region.friendship_locations.append(
        Location(name="Ursaring",
                 id=FRIENDSHIP_ITEMS["Ursaring"],
                 requirements=Requirements(
                     unlock_names=["Ursaring Unlock"],
                     powers=PowerRequirement.can_battle
                 )),
    )
    ice_zone_overworld_region.friendship_locations.append(
        Location(name="Mamoswine",
                 id=FRIENDSHIP_ITEMS["Mamoswine"],
                 requirements=Requirements(
                     unlock_names=["Mamoswine Unlock"],
                     powers=PowerRequirement.can_battle_thunderbolt_immune
                 )),
    )
    ice_zone_overworld_region.friendship_locations.append(
        Location(name="Kirlia",
                 id=FRIENDSHIP_ITEMS["Kirlia"],
                 requirements=Requirements(
                     friendship_names=["Delibird"],
                     can_reach_locations=["Ice Zone - Overworld - Delibird"]
                 )),
    )

    ice_zone_overworld_region.unlock_location.append(
        Location(name="Igloo Quest 1 - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Primeape Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Ice Zone - Overworld - Igloo Quest 1"]
                 )),
    )
    ice_zone_overworld_region.unlock_location.append(
        Location(name="Igloo Quest 2 - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Ursaring Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Ice Zone - Overworld - Igloo Quest 2"]
                 )),
    )

    ice_zone_overworld_region.quest_locations.append(
        Location(name="Igloo Quest 1",
                 id=QuestLocationIds.IGLOO_QUEST1.value,
                 requirements=Requirements(
                     unlock_names=["Glalie Unlock"]
                 )),
    )
    ice_zone_overworld_region.quest_locations.append(
        Location(name="Igloo Quest 2",
                 id=QuestLocationIds.IGLOO_QUEST2.value,
                 requirements=Requirements(
                     can_reach_locations=["Ice Zone - Overworld - Igloo Quest 1"]
                 )),
    )
    ice_zone_overworld_region.quest_locations.append(
        Location(name="Igloo Quest 3",
                 id=QuestLocationIds.IGLOO_QUEST3.value,
                 requirements=Requirements(
                     can_reach_locations=["Ice Zone - Overworld - Igloo Quest 2"]
                 )),
    )

    ice_zone_overworld_region.quest_locations.append(
        Location(name="Christmas Tree Present 1",
                 id=QuestLocationIds.CHRISTMAS_TREE1.value,
                 requirements=Requirements(
                     friendship_names=["Spheal"],
                     unlock_names=["Delibird Unlock"]
                 )),
    )
    ice_zone_overworld_region.quest_locations.append(
        Location(name="Christmas Tree Present 2",
                 id=QuestLocationIds.CHRISTMAS_TREE2.value,
                 requirements=Requirements(
                     friendship_names=["Teddiursa"],
                     can_reach_locations=["Ice Zone - Overworld - Christmas Tree Present 1"]
                 )),
    )
    ice_zone_overworld_region.quest_locations.append(
        Location(name="Christmas Tree Present 3",
                 id=QuestLocationIds.CHRISTMAS_TREE3.value,
                 requirements=Requirements(
                     unlock_names=["Squirtle Unlock"],
                     friendship_names=["Squirtle"],
                     can_reach_locations=["Ice Zone - Overworld - Christmas Tree Present 2"]
                 )),
    )
    ice_zone_overworld_region.quest_locations.append(
        Location(name="Christmas Tree Present 4",
                 id=QuestLocationIds.CHRISTMAS_TREE4.value,
                 requirements=Requirements(
                     friendship_names=["Smoochum"],
                     unlock_names=["Smoochum Unlock"],
                     can_reach_locations=["Ice Zone - Overworld - Christmas Tree Present 3"]
                 )),
    )
    return ice_zone_overworld_region


def generate_beach_zone_gyarados_minigame_region(world, get_all_locations: bool = False):
    beach_zone_gyarados_mingame_region: PokeparkRegion = (
        PokeparkRegion(name="Beach Zone - Gyarados' Aqua Dash",
                       display="Beach Zone - Gyarados' Aqua Dash",
                       parent_regions=["Beach Zone - Overworld"]))

    beach_zone_gyarados_mingame_region.minigame_location.append(
        Location(name="Prisma",
                 id=PRISM_ITEM["Gyarados Prisma"],
                 requirements=Requirements(
                     minigame=MinigameRequirement.gyarados_aqua_any
                 )),
    )
    beach_zone_gyarados_mingame_region.minigame_location.append(
        Location(name="Pikachu",
                 id=MinigameLocationIds.PIKACHU_AQUA.value,
                 requirements=Requirements(
                     unlock_names=["Pikachu Surfboard"])),
    )
    beach_zone_gyarados_mingame_region.minigame_location.append(
        Location(name="Psyduck",
                 id=MinigameLocationIds.PSYDUCK_AQUA.value,
                 requirements=Requirements(
                     friendship_names=["Psyduck"])),
    )
    beach_zone_gyarados_mingame_region.minigame_location.append(
        Location(name="Azurill",
                 id=MinigameLocationIds.AZURILL_AQUA.value,
                 requirements=Requirements(
                     friendship_names=["Azurill"])),
    )
    beach_zone_gyarados_mingame_region.minigame_location.append(
        Location(name="Slowpoke",
                 id=MinigameLocationIds.SLOWPOKE_AQUA.value,
                 requirements=Requirements(
                     friendship_names=["Slowpoke"])),
    )
    beach_zone_gyarados_mingame_region.minigame_location.append(
        Location(name="Empoleon",
                 id=MinigameLocationIds.EMPOLEON_AQUA.value,
                 requirements=Requirements(
                     friendship_names=["Empoleon"])),
    )
    beach_zone_gyarados_mingame_region.minigame_location.append(
        Location(name="Floatzel",
                 id=MinigameLocationIds.FLOATZEL_AQUA.value,
                 requirements=Requirements(
                     friendship_names=["Floatzel"])),
    )
    beach_zone_gyarados_mingame_region.minigame_location.append(
        Location(name="Feraligatr",
                 id=MinigameLocationIds.FERALIGATR_AQUA.value,
                 requirements=Requirements(
                     friendship_names=["Feraligatr"])),
    )
    beach_zone_gyarados_mingame_region.minigame_location.append(
        Location(name="Golduck",
                 id=MinigameLocationIds.GOLDUCK_AQUA.value,
                 requirements=Requirements(
                     friendship_names=["Golduck"])),
    )
    beach_zone_gyarados_mingame_region.minigame_location.append(
        Location(name="Vaporeon",
                 id=MinigameLocationIds.VAPOREON_AQUA.value,
                 requirements=Requirements(
                     friendship_names=["Vaporeon"])),
    )
    beach_zone_gyarados_mingame_region.minigame_location.append(
        Location(name="Prinplup",
                 id=MinigameLocationIds.PRINPLUP_AQUA.value,
                 requirements=Requirements(
                     friendship_names=["Prinplup"])),
    )
    beach_zone_gyarados_mingame_region.minigame_location.append(
        Location(name="Bibarel",
                 id=MinigameLocationIds.BIBAREL_AQUA.value,
                 requirements=Requirements(
                     friendship_names=["Bibarel"])),
    )
    beach_zone_gyarados_mingame_region.minigame_location.append(
        Location(name="Buizel",
                 id=MinigameLocationIds.BUIZEL_AQUA.value,
                 requirements=Requirements(
                     friendship_names=["Buizel"])),
    )
    beach_zone_gyarados_mingame_region.minigame_location.append(
        Location(name="Corsola",
                 id=MinigameLocationIds.CORSOLA_AQUA.value,
                 requirements=Requirements(
                     friendship_names=["Corsola"])),
    )
    beach_zone_gyarados_mingame_region.minigame_location.append(
        Location(name="Piplup",
                 id=MinigameLocationIds.PIPLUP_AQUA.value,
                 requirements=Requirements(
                     friendship_names=["Piplup"])),
    )
    beach_zone_gyarados_mingame_region.minigame_location.append(
        Location(name="Lotad",
                 id=MinigameLocationIds.LOTAD_AQUA.value,
                 requirements=Requirements(
                     friendship_names=["Lotad"])),
    )
    if world.options.goal == world.options.goal.option_aftergame or get_all_locations:
        beach_zone_gyarados_mingame_region.minigame_location.append(
            Location(name="Manaphy",
                     id=MinigameLocationIds.MANAPHY_AQUA.value,
                     requirements=Requirements(
                         friendship_names=["Manaphy"],
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]
                     )),
        )
        beach_zone_gyarados_mingame_region.friendship_locations.append(
            Location(name="Manaphy Unlock",
                     id=FRIENDSHIP_ITEMS["Manaphy"],
                     requirements=Requirements(
                         minigame=MinigameRequirement.gyarados_aqua_all,
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]

                     )),
        )
    return beach_zone_gyarados_mingame_region


def generate_beach_zone_pelipper_minigame_region(world, get_all_locations: bool = False):
    beach_zone_pelipper_mingame_region: PokeparkRegion = (
        PokeparkRegion(name="Beach Zone - Pelipper's Circle Circuit",
                       display="Beach Zone - Pelipper's Circle Circuit",
                       parent_regions=["Beach Zone - Overworld"]))

    beach_zone_pelipper_mingame_region.minigame_location.append(
        Location(name="Prisma",
                 id=PRISM_ITEM["Pelipper Prisma"],
                 requirements=Requirements(
                     minigame=MinigameRequirement.pelipper_circuit_any
                 )),
    )
    beach_zone_pelipper_mingame_region.minigame_location.append(
        Location(name="Pikachu",
                 id=MinigameLocationIds.PIKACHU_CIRCLE.value,
                 requirements=Requirements(
                     unlock_names=["Pikachu Balloon"])),
    )
    beach_zone_pelipper_mingame_region.minigame_location.append(
        Location(name="Staraptor",
                 id=MinigameLocationIds.STARAPTOR_CIRCLE.value,
                 requirements=Requirements(
                     friendship_names=["Staraptor"])),
    )
    beach_zone_pelipper_mingame_region.minigame_location.append(
        Location(name="Togekiss",
                 id=MinigameLocationIds.TOGEKISS_CIRCLE.value,
                 requirements=Requirements(
                     friendship_names=["Togekiss"])),
    )
    beach_zone_pelipper_mingame_region.minigame_location.append(
        Location(name="Honchkrow",
                 id=MinigameLocationIds.HONCHKROW_CIRCLE.value,
                 requirements=Requirements(
                     friendship_names=["Honchkrow"])),
    )
    beach_zone_pelipper_mingame_region.minigame_location.append(
        Location(name="Gliscor",
                 id=MinigameLocationIds.GLISCOR_CIRCLE.value,
                 requirements=Requirements(
                     friendship_names=["Gliscor"])),
    )
    beach_zone_pelipper_mingame_region.minigame_location.append(
        Location(name="Pelipper",
                 id=MinigameLocationIds.PELIPPER_CIRCLE.value,
                 requirements=Requirements(
                     friendship_names=["Pelipper"])),
    )
    beach_zone_pelipper_mingame_region.minigame_location.append(
        Location(name="Staravia",
                 id=MinigameLocationIds.STARAVIA_CIRCLE.value,
                 requirements=Requirements(
                     friendship_names=["Staravia"])),
    )
    beach_zone_pelipper_mingame_region.minigame_location.append(
        Location(name="Pidgeotto",
                 id=MinigameLocationIds.PIDGEOTTO_CIRCLE.value,
                 requirements=Requirements(
                     friendship_names=["Pidgeotto"])),
    )
    beach_zone_pelipper_mingame_region.minigame_location.append(
        Location(name="Butterfree",
                 id=MinigameLocationIds.BUTTERFREE_CIRCLE.value,
                 requirements=Requirements(
                     friendship_names=["Butterfree"])),
    )
    beach_zone_pelipper_mingame_region.minigame_location.append(
        Location(name="Tropius",
                 id=MinigameLocationIds.TROPIUS_CIRCLE.value,
                 requirements=Requirements(friendship_names=["Tropius"])),
    )
    beach_zone_pelipper_mingame_region.minigame_location.append(
        Location(name="Murkrow",
                 id=MinigameLocationIds.MURKROW_CIRCLE.value,
                 requirements=Requirements(
                     friendship_names=["Murkrow"])),
    )
    beach_zone_pelipper_mingame_region.minigame_location.append(
        Location(name="Taillow",
                 id=MinigameLocationIds.TAILLOW_CIRCLE.value,
                 requirements=Requirements(
                     friendship_names=["Taillow"])),
    )
    beach_zone_pelipper_mingame_region.minigame_location.append(
        Location(name="Spearow",
                 id=MinigameLocationIds.SPEAROW_CIRCLE.value,
                 requirements=Requirements(
                     friendship_names=["Spearow"])),
    )
    beach_zone_pelipper_mingame_region.minigame_location.append(
        Location(name="Starly",
                 id=MinigameLocationIds.STARLY_CIRCLE.value,
                 requirements=Requirements(
                     friendship_names=["Starly"])),
    )
    beach_zone_pelipper_mingame_region.minigame_location.append(
        Location(name="Wingull",
                 id=MinigameLocationIds.WINGULL_CIRCLE.value,
                 requirements=Requirements(
                     friendship_names=["Wingull"])),
    )
    if world.options.goal == world.options.goal.option_aftergame or get_all_locations:
        beach_zone_pelipper_mingame_region.minigame_location.append(
            Location(name="Latias",
                     id=MinigameLocationIds.LATIAS_CIRCLE.value,
                     requirements=Requirements(
                         friendship_names=["Latias"],
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]
                     )),
        )
        beach_zone_pelipper_mingame_region.friendship_locations.append(
            Location(name="Latias Unlock",
                     id=FRIENDSHIP_ITEMS["Latias"],
                     requirements=Requirements(
                         minigame=MinigameRequirement.pelipper_circuit_all,
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]

                     )),
        )
    return beach_zone_pelipper_mingame_region


def generate_beach_zone_overworld_region(world, get_all_locations: bool = False):
    beach_zone_overworld_region: PokeparkRegion = PokeparkRegion(
        name="Beach Zone - Overworld",
        display="Beach Zone - Overworld",
        requirements=Requirements(
            unlock_names=["Beach Zone Unlock"]),
        parent_regions=["Treehouse"]
    )

    beach_zone_overworld_region.friendship_locations.append(
        Location(name="Buizel",
                 id=FRIENDSHIP_ITEMS["Buizel"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    beach_zone_overworld_region.friendship_locations.append(
        Location(name="Psyduck",
                 id=FRIENDSHIP_ITEMS["Psyduck"]),
    )
    beach_zone_overworld_region.friendship_locations.append(
        Location(name="Slowpoke",
                 id=FRIENDSHIP_ITEMS["Slowpoke"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    beach_zone_overworld_region.friendship_locations.append(
        Location(name="Azurill",
                 id=FRIENDSHIP_ITEMS["Azurill"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    beach_zone_overworld_region.friendship_locations.append(
        Location(name="Totodile",
                 id=FRIENDSHIP_ITEMS["Totodile"],
                 requirements=Requirements(
                     unlock_names=["Totodile Unlock"],
                     powers=PowerRequirement.can_battle
                 )),
    )
    beach_zone_overworld_region.friendship_locations.append(
        Location(name="Mudkip",
                 id=FRIENDSHIP_ITEMS["Mudkip"],
                 requirements=Requirements(
                     unlock_names=["Mudkip Unlock"])),
    )
    beach_zone_overworld_region.friendship_locations.append(
        Location(name="Pidgeotto",
                 id=FRIENDSHIP_ITEMS["Pidgeotto"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle
                 )),
    )
    beach_zone_overworld_region.friendship_locations.append(
        Location(name="Taillow",
                 id=FRIENDSHIP_ITEMS["Taillow"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    beach_zone_overworld_region.friendship_locations.append(
        Location(name="Wingull",
                 id=FRIENDSHIP_ITEMS["Wingull"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    beach_zone_overworld_region.friendship_locations.append(
        Location(name="Staravia",
                 id=FRIENDSHIP_ITEMS["Staravia"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle
                 )),
    )
    beach_zone_overworld_region.friendship_locations.append(
        Location(name="Corsola",
                 id=FRIENDSHIP_ITEMS["Corsola"]),
    )
    beach_zone_overworld_region.friendship_locations.append(
        Location(name="Floatzel",
                 id=FRIENDSHIP_ITEMS["Floatzel"],
                 requirements=Requirements(
                     unlock_names=["Floatzel Unlock"],
                     powers=PowerRequirement.can_battle
                 )),
    )
    beach_zone_overworld_region.friendship_locations.append(
        Location(name="Vaporeon",
                 id=FRIENDSHIP_ITEMS["Vaporeon"],
                 requirements=Requirements(
                     friendcount=31,
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    beach_zone_overworld_region.friendship_locations.append(
        Location(name="Golduck",
                 id=FRIENDSHIP_ITEMS["Golduck"],
                 requirements=Requirements(
                     unlock_names=["Golduck Unlock"],
                     powers=PowerRequirement.can_battle
                 )),
    )
    beach_zone_overworld_region.friendship_locations.append(
        Location(name="Krabby",
                 id=FRIENDSHIP_ITEMS["Krabby"],
                 requirements=Requirements(
                     unlock_names=["Krabby Unlock"],
                     powers=PowerRequirement.can_play_catch,
                     can_reach_locations=["Beach Zone - Overworld - Bottle Recycling 2 - Pokemon Unlock"]
                 )),
    )
    beach_zone_overworld_region.friendship_locations.append(
        Location(name="Wailord",
                 id=FRIENDSHIP_ITEMS["Wailord"],
                 requirements=Requirements(
                     can_reach_locations=["Beach Zone - Overworld - Bottle Recycling 6"]
                 )),
    )
    beach_zone_overworld_region.friendship_locations.append(
        Location(name="Corphish",
                 id=FRIENDSHIP_ITEMS["Corphish"],
                 requirements=Requirements(
                     unlock_names=["Corphish Unlock"],
                     powers=PowerRequirement.can_battle,
                     can_reach_locations=["Beach Zone - Overworld - Bottle Recycling 4 - Pokemon Unlock"]

                 )),
    )
    beach_zone_overworld_region.friendship_locations.append(
        Location(name="Feraligatr",
                 id=FRIENDSHIP_ITEMS["Feraligatr"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle
                 )),
    )
    beach_zone_overworld_region.friendship_locations.append(
        Location(name="Starly",
                 id=OverworldPokemonLocationIds.STARLY_BEACH.value,
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    beach_zone_overworld_region.friendship_locations.append(
        Location(name="Blastoise",
                 id=FRIENDSHIP_ITEMS["Blastoise"],
                 requirements=Requirements(
                     unlock_names=["Blastoise Unlock"],
                     powers=PowerRequirement.can_battle
                 )),
    )

    beach_zone_overworld_region.unlock_location.append(
        Location(name="Buizel Friendship - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Floatzel Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Beach Zone - Overworld - Buizel"]
                 )),
    )
    beach_zone_overworld_region.unlock_location.append(
        Location(name="Psyduck Friendship - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Golduck Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Beach Zone - Overworld - Psyduck"]
                 )),
    )
    beach_zone_overworld_region.unlock_location.append(
        Location(name="Slowpoke Friendship - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Mudkip Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Beach Zone - Overworld - Slowpoke"]
                 )),
    )
    beach_zone_overworld_region.unlock_location.append(
        Location(name="Azurill Friendship - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Totodile Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Beach Zone - Overworld - Azurill"]
                 )),
    )
    beach_zone_overworld_region.unlock_location.append(
        Location(name="Bottle Recycling 2 - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Krabby Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Beach Zone - Overworld - Bottle Recycling 2"],

                 )),
    )
    beach_zone_overworld_region.unlock_location.append(
        Location(name="Bottle Recycling 4 - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Corphish Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Beach Zone - Overworld - Bottle Recycling 4"]
                 )),
    )

    beach_zone_overworld_region.quest_locations.append(
        Location(name="Bottle Recycling 1",
                 id=QuestLocationIds.BEACH_BOTTLE1.value,
                 ),
    )
    beach_zone_overworld_region.quest_locations.append(
        Location(name="Bottle Recycling 2",
                 id=QuestLocationIds.BEACH_BOTTLE2.value,
                 requirements=Requirements(
                     can_reach_locations=["Beach Zone - Overworld - Bottle Recycling 1"]
                 )),
    )
    beach_zone_overworld_region.quest_locations.append(
        Location(name="Bottle Recycling 3",
                 id=QuestLocationIds.BEACH_BOTTLE3.value,
                 requirements=Requirements(
                     can_reach_locations=["Beach Zone - Overworld - Bottle Recycling 2"]
                 )),
    )
    beach_zone_overworld_region.quest_locations.append(
        Location(name="Bottle Recycling 4",
                 id=QuestLocationIds.BEACH_BOTTLE4.value,
                 requirements=Requirements(
                     can_reach_locations=["Beach Zone - Overworld - Bottle Recycling 3"]
                 )),
    )
    beach_zone_overworld_region.quest_locations.append(
        Location(name="Bottle Recycling 5",
                 id=QuestLocationIds.BEACH_BOTTLE5.value,
                 requirements=Requirements(
                     can_reach_locations=["Beach Zone - Overworld - Bottle Recycling 4"]
                 )),
    )
    beach_zone_overworld_region.quest_locations.append(
        Location(name="Bottle Recycling 6",
                 id=QuestLocationIds.BEACH_BOTTLE6.value,
                 requirements=Requirements(
                     can_reach_locations=["Beach Zone - Overworld - Bottle Recycling 5"]
                 )),
    )

    return beach_zone_overworld_region


def generate_meadow_zone_venusaur_minigame_region(world: "PokeparkWorld", get_all_locations: bool = False):
    meadow_zone_venusaur_minigame_region: PokeparkRegion = (
        PokeparkRegion(name="Meadow Zone - Venusaur's Vine Swing",
                       display="Meadow Zone - Venusaur's Vine Swing",
                       requirements=Requirements(
                           friendship_names=["Croagunk",
                                             "Spearow"]),
                       parent_regions=["Meadow Zone - Overworld"]))

    meadow_zone_venusaur_minigame_region.minigame_location.append(
        Location(name="Prisma",
                 id=PRISM_ITEM["Venusaur Prisma"],
                 requirements=Requirements(
                     minigame=MinigameRequirement.venusaur_vine_swing_any
                 )),
    )
    meadow_zone_venusaur_minigame_region.minigame_location.append(
        Location(name="Pikachu",
                 id=MinigameLocationIds.PIKACHU_VINE_SWING.value),
    )
    meadow_zone_venusaur_minigame_region.minigame_location.append(
        Location(name="Munchlax",
                 id=MinigameLocationIds.MUNCHLAX_VINE_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Munchlax"])),
    )
    meadow_zone_venusaur_minigame_region.minigame_location.append(
        Location(name="Magikarp",
                 id=MinigameLocationIds.MAGIKARP_VINE_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Magikarp"])),
    )
    meadow_zone_venusaur_minigame_region.minigame_location.append(
        Location(name="Blaziken",
                 id=MinigameLocationIds.BLAZIKEN_VINE_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Blaziken"])),
    )
    meadow_zone_venusaur_minigame_region.minigame_location.append(
        Location(name="Infernape",
                 id=MinigameLocationIds.INFERNAPE_VINE_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Infernape"])),
    )
    meadow_zone_venusaur_minigame_region.minigame_location.append(
        Location(name="Lucario",
                 id=MinigameLocationIds.LUCARIO_VINE_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Lucario"])),
    )
    meadow_zone_venusaur_minigame_region.minigame_location.append(
        Location(name="Primeape",
                 id=MinigameLocationIds.PRIMEAPE_VINE_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Primeape"])),
    )
    meadow_zone_venusaur_minigame_region.minigame_location.append(
        Location(name="Tangrowth",
                 id=MinigameLocationIds.TANGROWTH_VINE_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Tangrowth"])),
    )
    meadow_zone_venusaur_minigame_region.minigame_location.append(
        Location(name="Ambipom",
                 id=MinigameLocationIds.AMBIPOM_VINE_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Ambipom"])),
    )
    meadow_zone_venusaur_minigame_region.minigame_location.append(
        Location(name="Croagunk",
                 id=MinigameLocationIds.CROAGUNK_VINE_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Croagunk"])),
    )
    meadow_zone_venusaur_minigame_region.minigame_location.append(
        Location(name="Mankey",
                 id=MinigameLocationIds.MANKEY_VINE_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Mankey"])),
    )
    meadow_zone_venusaur_minigame_region.minigame_location.append(
        Location(name="Aipom",
                 id=MinigameLocationIds.AIPOM_VINE_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Aipom"])),
    )
    meadow_zone_venusaur_minigame_region.minigame_location.append(
        Location(name="Chimchar",
                 id=MinigameLocationIds.CHIMCHAR_VINE_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Chimchar"])),
    )
    meadow_zone_venusaur_minigame_region.minigame_location.append(
        Location(name="Treecko",
                 id=MinigameLocationIds.TREECKO_VINE_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Treecko"])),
    )
    meadow_zone_venusaur_minigame_region.minigame_location.append(
        Location(name="Pachirisu",
                 id=MinigameLocationIds.PACHIRISU_VINE_SWING.value,
                 requirements=Requirements(
                     friendship_names=["Pachirisu"])),
    )
    if world.options.goal == world.options.goal.option_aftergame or get_all_locations:
        meadow_zone_venusaur_minigame_region.minigame_location.append(
            Location(name="Jirachi",
                     id=MinigameLocationIds.JIRACHI_VINE_SWING.value,
                     requirements=Requirements(
                         friendship_names=["Jirachi"],
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]
                     )),
        )
        meadow_zone_venusaur_minigame_region.friendship_locations.append(
            Location(name="Jirachi Unlock",
                     id=FRIENDSHIP_ITEMS["Jirachi"],
                     requirements=Requirements(
                         minigame=MinigameRequirement.venusaur_vine_swing_all,
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]

                     )),
        )
    return meadow_zone_venusaur_minigame_region


def generate_meadow_zone_bulbasaur_minigame_region(world: "PokeparkWorld", get_all_locations: bool = False):
    meadow_zone_bulbasaur_minigame: PokeparkRegion = PokeparkRegion(
        name="Meadow Zone - Bulbasaur's Daring Dash Minigame",
        display="Meadow Zone - Bulbasaur's Daring Dash Minigame",
        parent_regions=["Meadow Zone - Overworld"])

    meadow_zone_bulbasaur_minigame.minigame_location.append(
        Location(name="Prisma",
                 id=PRISM_ITEM["Bulbasaur Prisma"],
                 requirements=Requirements(
                     minigame=MinigameRequirement.bulbasaur_dash_any
                 )),
    )
    meadow_zone_bulbasaur_minigame.minigame_location.append(
        Location(name="Pikachu",
                 id=MinigameLocationIds.PIKACHU_DASH.value),
    )
    meadow_zone_bulbasaur_minigame.minigame_location.append(
        Location(name="Turtwig",
                 id=MinigameLocationIds.TURTWIG_DASH.value,
                 requirements=Requirements(
                     friendship_names=["Turtwig"])),
    )
    meadow_zone_bulbasaur_minigame.minigame_location.append(
        Location(name="Munchlax",
                 id=MinigameLocationIds.MUNCHLAX_DASH.value,
                 requirements=Requirements(
                     friendship_names=["Munchlax"])),
    )
    meadow_zone_bulbasaur_minigame.minigame_location.append(
        Location(name="Chimchar",
                 id=MinigameLocationIds.CHIMCHAR_DASH.value,
                 requirements=Requirements(
                     friendship_names=["Chimchar"])),
    )
    meadow_zone_bulbasaur_minigame.minigame_location.append(
        Location(name="Treecko",
                 id=MinigameLocationIds.TREECKO_DASH.value,
                 requirements=Requirements(
                     friendship_names=["Treecko"])),
    )
    meadow_zone_bulbasaur_minigame.minigame_location.append(
        Location(name="Bibarel",
                 id=MinigameLocationIds.BIBAREL_DASH.value,
                 requirements=Requirements(
                     friendship_names=["Bibarel"])),
    )
    meadow_zone_bulbasaur_minigame.minigame_location.append(
        Location(name="Bulbasaur",
                 id=MinigameLocationIds.BULBASAUR_DASH.value,
                 requirements=Requirements(
                     friendship_names=["Bulbasaur"])),
    )
    meadow_zone_bulbasaur_minigame.minigame_location.append(
        Location(name="Bidoof",
                 id=MinigameLocationIds.BIDOOF_DASH.value,
                 requirements=Requirements(
                     friendship_names=["Bidoof"])),
    )
    meadow_zone_bulbasaur_minigame.minigame_location.append(
        Location(name="Oddish",
                 id=MinigameLocationIds.ODDISH_DASH.value,
                 requirements=Requirements(
                     friendship_names=["Oddish"])),
    )
    meadow_zone_bulbasaur_minigame.minigame_location.append(
        Location(name="Shroomish",
                 id=MinigameLocationIds.SHROOMISH_DASH.value,
                 requirements=Requirements(
                     friendship_names=["Shroomish"])),
    )
    meadow_zone_bulbasaur_minigame.minigame_location.append(
        Location(name="Bonsly",
                 id=MinigameLocationIds.BONSLY_DASH.value,
                 requirements=Requirements(
                     friendship_names=["Bonsly"])),
    )
    meadow_zone_bulbasaur_minigame.minigame_location.append(
        Location(name="Lotad",
                 id=MinigameLocationIds.LOTAD_DASH.value,
                 requirements=Requirements(
                     friendship_names=["Lotad"])),
    )
    meadow_zone_bulbasaur_minigame.minigame_location.append(
        Location(name="Weedle",
                 id=MinigameLocationIds.WEEDLE_DASH.value,
                 requirements=Requirements(
                     friendship_names=["Weedle"])),
    )
    meadow_zone_bulbasaur_minigame.minigame_location.append(
        Location(name="Caterpie",
                 id=MinigameLocationIds.CATERPIE_DASH.value,
                 requirements=Requirements(
                     friendship_names=["Caterpie"])),
    )
    meadow_zone_bulbasaur_minigame.minigame_location.append(
        Location(name="Magikarp",
                 id=MinigameLocationIds.MAGIKARP_DASH.value,
                 requirements=Requirements(
                     friendship_names=["Magikarp"])),
    )
    meadow_zone_bulbasaur_minigame.minigame_location.append(
        Location(name="Jolteon",
                 id=MinigameLocationIds.JOLTEON_DASH.value,
                 requirements=Requirements(
                     friendship_names=["Jolteon"])),
    )
    meadow_zone_bulbasaur_minigame.minigame_location.append(
        Location(name="Arcanine",
                 id=MinigameLocationIds.ARCANINE_DASH.value,
                 requirements=Requirements(
                     friendship_names=["Arcanine"])),
    )
    meadow_zone_bulbasaur_minigame.minigame_location.append(
        Location(name="Leafeon",
                 id=MinigameLocationIds.LEAFEON_DASH.value,
                 requirements=Requirements(
                     friendship_names=["Leafeon"])),
    )
    meadow_zone_bulbasaur_minigame.minigame_location.append(
        Location(name="Scyther",
                 id=MinigameLocationIds.SCYTHER_DASH.value,
                 requirements=Requirements(
                     friendship_names=["Scyther"])),
    )
    meadow_zone_bulbasaur_minigame.minigame_location.append(
        Location(name="Ponyta",
                 id=MinigameLocationIds.PONYTA_DASH.value,
                 requirements=Requirements(
                     friendship_names=["Ponyta"])),
    )
    meadow_zone_bulbasaur_minigame.minigame_location.append(
        Location(name="Shinx",
                 id=MinigameLocationIds.SHINX_DASH.value,
                 requirements=Requirements(
                     friendship_names=["Shinx"])),
    )
    meadow_zone_bulbasaur_minigame.minigame_location.append(
        Location(name="Eevee",
                 id=MinigameLocationIds.EEVEE_DASH.value,
                 requirements=Requirements(
                     friendship_names=["Eevee"])),
    )
    meadow_zone_bulbasaur_minigame.minigame_location.append(
        Location(name="Pachirisu",
                 id=MinigameLocationIds.PACHIRISU_DASH.value,
                 requirements=Requirements(
                     friendship_names=["Pachirisu"])),
    )
    meadow_zone_bulbasaur_minigame.minigame_location.append(
        Location(name="Buneary",
                 id=MinigameLocationIds.BUNEARY_DASH.value,
                 requirements=Requirements(
                     friendship_names=["Buneary"])),
    )
    meadow_zone_bulbasaur_minigame.minigame_location.append(
        Location(name="Croagunk",
                 id=MinigameLocationIds.CROAGUNK_DASH.value,
                 requirements=Requirements(
                     friendship_names=["Croagunk"])),
    )
    if world.options.goal == world.options.goal.option_aftergame or get_all_locations:
        meadow_zone_bulbasaur_minigame.minigame_location.append(
            Location(name="Mew",
                     id=MinigameLocationIds.MEW_DASH.value,
                     requirements=Requirements(
                         friendship_names=["Mew"],
                         can_reach_locations=["Skygarden - Overworld - Mew Challenge completed"]
                     )),
        )

    return meadow_zone_bulbasaur_minigame


def generate_meadow_zone_overworld_region(world: "PokeparkWorld", get_all_locations: bool = False):
    meadow_zone_overworld: PokeparkRegion = (
        PokeparkRegion(name="Meadow Zone - Overworld",
                       display="Meadow Zone - Overworld",
                       requirements=Requirements(
                           unlock_names=["Meadow Zone Unlock"]
                       ),
                       parent_regions=["Treehouse"]))

    meadow_zone_overworld.friendship_locations.append(
        Location(name="Bulbasaur",
                 id=FRIENDSHIP_ITEMS["Bulbasaur"],
                 requirements=Requirements(
                     prisma_names=["Bulbasaur Prisma"])),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Munchlax",
                 id=FRIENDSHIP_ITEMS["Munchlax"],
                 requirements=Requirements(
                     prisma_names=["Bulbasaur Prisma"],
                     powers=PowerRequirement.can_destroy_objects_overworld
                 )),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Tropius",
                 id=FRIENDSHIP_ITEMS["Tropius"],
                 requirements=Requirements(
                     unlock_names=["Tropius Unlock"],
                     prisma_names=["Bulbasaur Prisma"],
                     powers=PowerRequirement.can_destroy_objects_overworld
                 )),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Turtwig",
                 id=FRIENDSHIP_ITEMS["Turtwig"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch)
                 ),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Bonsly",
                 id=FRIENDSHIP_ITEMS["Bonsly"],
                 requirements=Requirements(
                     unlock_names=["Bonsly Unlock"])),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Pachirisu",
                 id=FRIENDSHIP_ITEMS["Pachirisu"],
                 requirements=Requirements(
                     unlock_names=["Pachirisu Unlock"],
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Sudowoodo",
                 id=FRIENDSHIP_ITEMS["Sudowoodo"],
                 requirements=Requirements(
                     unlock_names=["Sudowoodo Unlock"])),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Buneary",
                 id=FRIENDSHIP_ITEMS["Buneary"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Shinx",
                 id=FRIENDSHIP_ITEMS["Shinx"],
                 requirements=Requirements(
                     unlock_names=["Shinx Unlock"],
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Spearow",
                 id=FRIENDSHIP_ITEMS["Spearow"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle
                 )),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Croagunk",
                 id=FRIENDSHIP_ITEMS["Croagunk"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_battle
                 )),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Lotad",
                 id=FRIENDSHIP_ITEMS["Lotad"],
                 requirements=Requirements(
                     unlock_names=["Lotad Unlock"],
                     powers=PowerRequirement.can_battle
                 )),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Treecko",
                 id=FRIENDSHIP_ITEMS["Treecko"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Caterpie",
                 id=FRIENDSHIP_ITEMS["Caterpie"],
                 requirements=Requirements(
                     unlock_names=["Caterpie Unlock"],
                     powers=PowerRequirement.can_play_catch,
                     can_reach_locations=["Meadow Zone - Overworld - Caterpie Tree Dash"]
                 )),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Butterfree",
                 id=FRIENDSHIP_ITEMS["Butterfree"],
                 requirements=Requirements(
                     unlock_names=["Butterfree Unlock"],
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Chimchar",
                 id=FRIENDSHIP_ITEMS["Chimchar"],
                 requirements=Requirements(
                     unlock_names=["Chimchar Unlock"],
                     powers=PowerRequirement.can_battle
                 )),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Aipom",
                 id=FRIENDSHIP_ITEMS["Aipom"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Ambipom",
                 id=FRIENDSHIP_ITEMS["Ambipom"],
                 requirements=Requirements(
                     unlock_names=["Ambipom Unlock"],
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Weedle",
                 id=FRIENDSHIP_ITEMS["Weedle"],
                 requirements=Requirements(
                     unlock_names=["Weedle Unlock"],
                     powers=PowerRequirement.can_dash_overworld,
                     # generation tweak so battle and unlock location are reachable
                     can_reach_locations=["Meadow Zone - Overworld - Weedle Tree Dash"]

                 )),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Shroomish",
                 id=FRIENDSHIP_ITEMS["Shroomish"],
                 requirements=Requirements(
                     unlock_names=["Shroomish Unlock"],
                     powers=PowerRequirement.can_play_catch,
                     can_reach_locations=["Meadow Zone - Overworld - Shroomish Crate Dash"]
                 )),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Magikarp",
                 id=FRIENDSHIP_ITEMS["Magikarp"],
                 requirements=Requirements(
                     unlock_names=["Magikarp Unlock"],
                     powers=PowerRequirement.can_play_catch,
                     can_reach_locations=["Meadow Zone - Overworld - Magikarp electrocuted"]
                 )),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Oddish",
                 id=FRIENDSHIP_ITEMS["Oddish"]),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Bidoof",
                 id=FRIENDSHIP_ITEMS["Bidoof"],
                 requirements=Requirements(
                     can_reach_locations=["Meadow Zone - Overworld - Bidoof Housing 4"])),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Bibarel",
                 id=FRIENDSHIP_ITEMS["Bibarel"],
                 requirements=Requirements(
                     unlock_names=["Bibarel Unlock"],
                     powers=PowerRequirement.can_battle
                 )),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Leafeon",
                 id=FRIENDSHIP_ITEMS["Leafeon"],
                 requirements=Requirements(
                     friendcount=21,
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Torterra",
                 id=FRIENDSHIP_ITEMS["Torterra"],
                 requirements=Requirements(
                     unlock_names=["Torterra Unlock"],
                     powers=PowerRequirement.can_battle_thunderbolt_immune
                 )),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Starly",
                 id=FRIENDSHIP_ITEMS["Starly"],
                 requirements=Requirements(
                     oneof_item_names=[["Starly Unlock"], ["Starly Unlock 2"]],
                     powers=PowerRequirement.can_play_catch
                 )),
    )
    meadow_zone_overworld.friendship_locations.append(
        Location(name="Scyther",
                 id=FRIENDSHIP_ITEMS["Scyther"],
                 requirements=Requirements(
                     unlock_names=["Scyther Unlock"],
                     powers=PowerRequirement.can_battle
                 )),
    )
    meadow_zone_overworld.unlock_location.append(
        Location(name="Munchlax Friendship - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Tropius Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Meadow Zone - Overworld - Munchlax"]
                 )),
    )
    meadow_zone_overworld.unlock_location.append(
        Location(name="Turtwig Friendship - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Pachirisu Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Meadow Zone - Overworld - Turtwig"]
                 )),
    )
    meadow_zone_overworld.unlock_location.append(
        Location(name="Bonsly Friendship - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Sudowoodo Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Meadow Zone - Overworld - Bonsly"]
                 )),
    )
    meadow_zone_overworld.unlock_location.append(
        Location(name="Buneary Friendship - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Lotad Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Meadow Zone - Overworld - Buneary"]
                 )),
    )
    meadow_zone_overworld.unlock_location.append(
        Location(name="Croagunk Friendship - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Scyther Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Meadow Zone - Overworld - Croagunk"]
                 )),
    )
    meadow_zone_overworld.unlock_location.append(
        Location(name="Caterpie Tree Dash",
                 id=UNLOCK_ITEMS["Caterpie Unlock"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_dash_overworld,
                 )),
    )
    meadow_zone_overworld.unlock_location.append(
        Location(name="Caterpie Friendship - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Butterfree Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Meadow Zone - Overworld - Caterpie"]
                 )),
    )
    meadow_zone_overworld.unlock_location.append(
        Location(name="Aipom Friendship - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Ambipom Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Meadow Zone - Overworld - Aipom"]
                 )),
    )
    meadow_zone_overworld.unlock_location.append(
        Location(name="Weedle Tree Dash",
                 id=UNLOCK_ITEMS["Weedle Unlock"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_dash_overworld,
                 )),
    )
    meadow_zone_overworld.unlock_location.append(
        Location(name="Shroomish Crate Dash",
                 id=UNLOCK_ITEMS["Shroomish Unlock"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_destroy_objects_overworld,
                 )),
    )
    meadow_zone_overworld.unlock_location.append(
        Location(name="Magikarp electrocuted",
                 id=UNLOCK_ITEMS["Magikarp Unlock"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_thunderbolt_overworld
                 )),
    )
    meadow_zone_overworld.unlock_location.append(
        Location(name="Bidoof Housing 1 - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Bidoof Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Meadow Zone - Overworld - Bidoof Housing 1"])),
    )
    meadow_zone_overworld.unlock_location.append(
        Location(name="Bidoof Housing 2 - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Bidoof Unlock 2"],
                 requirements=Requirements(
                     can_reach_locations=["Meadow Zone - Overworld - Bidoof Housing 2"])),
    )
    meadow_zone_overworld.unlock_location.append(
        Location(name="Bidoof Housing 3 - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Bidoof Unlock 3"],
                 requirements=Requirements(
                     can_reach_locations=["Meadow Zone - Overworld - Bidoof Housing 3"])),
    )
    meadow_zone_overworld.unlock_location.append(
        Location(name="Bidoof Housing 4 - Pokemon Unlock",
                 id=UNLOCK_ITEMS["Bibarel Unlock"],
                 requirements=Requirements(
                     can_reach_locations=["Meadow Zone - Overworld - Bidoof Housing 4"])),
    )
    meadow_zone_overworld.quest_locations.append(
        Location(name="Bidoof Housing 1",
                 id=QuestLocationIds.MEADOW_BIDOOF_HOUSING1.value,
                 requirements=Requirements(
                     friendship_names=["Mankey"],
                     powers=PowerRequirement.can_destroy_objects_overworld
                 )),
    )
    meadow_zone_overworld.quest_locations.append(
        Location(name="Bidoof Housing 2",
                 id=QuestLocationIds.MEADOW_BIDOOF_HOUSING2.value,
                 requirements=Requirements(
                     can_reach_locations=["Meadow Zone - Overworld - Bidoof Housing 1"])),
    )
    meadow_zone_overworld.quest_locations.append(
        Location(name="Bidoof Housing 3",
                 id=QuestLocationIds.MEADOW_BIDOOF_HOUSING3.value,
                 requirements=Requirements(
                     can_reach_locations=["Meadow Zone - Overworld - Bidoof Housing 2"])),
    )
    meadow_zone_overworld.quest_locations.append(
        Location(name="Bidoof Housing 4",
                 id=QuestLocationIds.MEADOW_BIDOOF_HOUSING4.value,
                 requirements=Requirements(
                     can_reach_locations=["Meadow Zone - Overworld - Bidoof Housing 3"])),
    )
    return meadow_zone_overworld


def generate_treehouse_region(world: "PokeparkWorld", get_all_locations: bool = False):
    treehouse: PokeparkRegion = PokeparkRegion(name="Treehouse",
                                               display="Treehouse")
    treehouse.friendship_locations.append(
        Location(name="Burmy",
                 id=FRIENDSHIP_ITEMS["Burmy"],
                 requirements=Requirements(
                     world_state=WorldStateRequirement.ice_zone_or_higher))
    )
    treehouse.friendship_locations.append(
        Location(name="Mime Jr.",
                 id=FRIENDSHIP_ITEMS["Mime Jr."],
                 requirements=Requirements(
                     world_state=WorldStateRequirement.cavern_and_magma_zone_or_higher)),
    )
    treehouse.friendship_locations.append(
        Location(name="Drifblim",
                 id=FRIENDSHIP_ITEMS["Drifblim"],
                 requirements=Requirements(
                     powers=PowerRequirement.can_farm_berries)),
    )
    treehouse.friendship_locations.append(
        Location(name="Abra",
                 id=OverworldPokemonLocationIds.ABRA_TREEHOUSE.value,
                 requirements=Requirements(
                     world_state=WorldStateRequirement.haunted_zone_or_higher)),
    )

    treehouse.quest_locations.append(
        Location(name="Thunderbolt Upgrade 1",
                 id=QuestLocationIds.THUNDERBOLT_POWERUP1.value,
                 requirements=Requirements(
                     powers=PowerRequirement.can_farm_berries,
                     oneof_item_names=[["100 Berries", "50 Berries", "10 Berries"]]  # generation tweak
                 )),
    )
    treehouse.quest_locations.append(
        Location(name="Thunderbolt Upgrade 2",
                 id=QuestLocationIds.THUNDERBOLT_POWERUP2.value,
                 requirements=Requirements(
                     can_reach_locations=["Treehouse - Thunderbolt Upgrade 1"])),
    )
    treehouse.quest_locations.append(
        Location(name="Thunderbolt Upgrade 3",
                 id=QuestLocationIds.THUNDERBOLT_POWERUP3.value,
                 requirements=Requirements(
                     can_reach_locations=["Treehouse - Thunderbolt Upgrade 2"])),
    )
    treehouse.quest_locations.append(
        Location(name="Dash Upgrade 1",
                 id=QuestLocationIds.DASH_POWERUP1.value,
                 requirements=Requirements(
                     prisma_names=["Pelipper Prisma"],
                     powers=PowerRequirement.can_farm_berries,
                     oneof_item_names=[["100 Berries", "50 Berries", "10 Berries"]]
                 )),
    )
    treehouse.quest_locations.append(
        Location(name="Dash Upgrade 2",
                 id=QuestLocationIds.DASH_POWERUP2.value,
                 requirements=Requirements(
                     can_reach_locations=["Treehouse - Dash Upgrade 1"])),
    )
    treehouse.quest_locations.append(
        Location(name="Dash Upgrade 3",
                 id=QuestLocationIds.DASH_POWERUP3.value,
                 requirements=Requirements(
                     can_reach_locations=["Treehouse - Dash Upgrade 2"])),
    )
    treehouse.quest_locations.append(
        Location(name="Health Upgrade 1",
                 id=QuestLocationIds.HEALTH_POWERUP1.value,
                 requirements=Requirements(
                     unlock_names=["Beach Zone Unlock"],
                     powers=PowerRequirement.can_farm_berries,
                     oneof_item_names=[["100 Berries", "50 Berries", "10 Berries"]]
                 )),
    )
    treehouse.quest_locations.append(
        Location(name="Health Upgrade 2",
                 id=QuestLocationIds.HEALTH_POWERUP2.value,
                 requirements=Requirements(
                     can_reach_locations=["Treehouse - Health Upgrade 1"]
                 )),
    )
    treehouse.quest_locations.append(
        Location(name="Health Upgrade 3",
                 id=QuestLocationIds.HEALTH_POWERUP3.value,
                 requirements=Requirements(
                     can_reach_locations=["Treehouse - Health Upgrade 2"])),
    )
    treehouse.quest_locations.append(
        Location(name="Iron Tail Upgrade 1",
                 id=QuestLocationIds.IRON_TAIL_POWERUP1.value,
                 requirements=Requirements(
                     world_state=WorldStateRequirement.ice_zone_or_higher,
                     powers=PowerRequirement.can_farm_berries,
                     oneof_item_names=[["100 Berries", "50 Berries", "10 Berries"]]
                 )),
    )
    treehouse.quest_locations.append(
        Location(name="Iron Tail Upgrade 2",
                 id=QuestLocationIds.IRON_TAIL_POWERUP2.value,
                 requirements=Requirements(
                     can_reach_locations=["Treehouse - Iron Tail Upgrade 1"]))
    )
    treehouse.quest_locations.append(
        Location(name="Iron Tail Upgrade 3",
                 id=QuestLocationIds.IRON_TAIL_POWERUP3.value,
                 requirements=Requirements(
                     can_reach_locations=["Treehouse - Iron Tail Upgrade 2"]))
    )
    return treehouse
