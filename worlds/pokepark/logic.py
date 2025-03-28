from enum import Enum
from typing import NamedTuple

from worlds.pokepark import FRIENDSHIP_ITEMS
from worlds.pokepark.LocationIds import MinigameLocationIds, QuestLocationIds, OverworldPokemonLocationIds, \
    UnlockLocationIds
from worlds.pokepark.items import UNLOCK_ITEMS, PRISM_ITEM


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


class Requirements(NamedTuple):
    unlock_names: list[str] = []
    friendship_names: list[str] = []
    friendcount: int = 0
    prisma_names: list[str] = []
    oneof_item_names: list[list[str]] = []
    can_reach_locations: list[str] = []
    powers: PowerRequirement = PowerRequirement.none
    world_state: WorldStateRequirement = WorldStateRequirement.none


class Location(NamedTuple):
    name: str
    id: int
    requirements: Requirements = Requirements()


class PokeparkRegion(NamedTuple):
    name: str
    display: str
    requirements: Requirements = Requirements()
    friendship_locations: list[Location] = []
    unlock_location: list[Location] = []
    minigame_location: list[Location] = []
    quest_locations: list[Location] = []
    parent_regions: list[str] = ["Menu"]


REGIONS: list[PokeparkRegion] = [

    PokeparkRegion(name="Treehouse",
                   display="Treehouse",
                   friendship_locations=[
                       Location(name="Burmy",
                                id=FRIENDSHIP_ITEMS["Burmy"],
                                requirements=Requirements(
                                    world_state=WorldStateRequirement.ice_zone_or_higher)),
                       Location(name="Mime Jr.",
                                id=FRIENDSHIP_ITEMS["Mime Jr."],
                                requirements=Requirements(
                                    world_state=WorldStateRequirement.cavern_and_magma_zone_or_higher)),
                       Location(name="Drifblim",
                                id=FRIENDSHIP_ITEMS["Drifblim"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_farm_berries)),
                   ],
                   quest_locations=[
                       Location(name="Thunderbolt Upgrade 1",
                                id=QuestLocationIds.THUNDERBOLT_POWERUP1.value,
                                requirements=Requirements(
                                    powers=PowerRequirement.can_farm_berries
                                )),

                       Location(name="Thunderbolt Upgrade 2",
                                id=QuestLocationIds.THUNDERBOLT_POWERUP2.value,
                                requirements=Requirements(
                                    can_reach_locations=["Treehouse - Thunderbolt Upgrade 1"])),

                       Location(name="Thunderbolt Upgrade 3",
                                id=QuestLocationIds.THUNDERBOLT_POWERUP3.value,
                                requirements=Requirements(
                                    can_reach_locations=["Treehouse - Thunderbolt Upgrade 2"])),

                       Location(name="Dash Upgrade 1",
                                id=QuestLocationIds.DASH_POWERUP1.value,
                                requirements=Requirements(
                                    prisma_names=["Pelipper Prisma"],
                                    powers=PowerRequirement.can_farm_berries
                                )),

                       Location(name="Dash Upgrade 2",
                                id=QuestLocationIds.DASH_POWERUP2.value,
                                requirements=Requirements(
                                    can_reach_locations=["Treehouse - Dash Upgrade 1"])),

                       Location(name="Dash Upgrade 3",
                                id=QuestLocationIds.DASH_POWERUP3.value,
                                requirements=Requirements(
                                    can_reach_locations=["Treehouse - Dash Upgrade 2"])),

                       Location(name="Health Upgrade 1",
                                id=QuestLocationIds.HEALTH_POWERUP1.value,
                                requirements=Requirements(
                                    unlock_names=["Beach Zone Unlock"],
                                    powers=PowerRequirement.can_farm_berries
                                )),

                       Location(name="Health Upgrade 2",
                                id=QuestLocationIds.HEALTH_POWERUP2.value,
                                requirements=Requirements(
                                    can_reach_locations=["Treehouse - Health Upgrade 1"])),

                       Location(name="Health Upgrade 3",
                                id=QuestLocationIds.HEALTH_POWERUP3.value,
                                requirements=Requirements(
                                    can_reach_locations=["Treehouse - Health Upgrade 2"])),

                       Location(name="Iron Tail Upgrade 1",
                                id=QuestLocationIds.IRON_TAIL_POWERUP1.value,
                                requirements=Requirements(
                                    world_state=WorldStateRequirement.ice_zone_or_higher,
                                    powers=PowerRequirement.can_farm_berries
                                )),
                       Location(name="Iron Tail Upgrade 2",
                                id=QuestLocationIds.IRON_TAIL_POWERUP2.value,
                                requirements=Requirements(
                                    can_reach_locations=["Treehouse - Iron Tail Upgrade 1"])),
                       Location(name="Iron Tail Upgrade 3",
                                id=QuestLocationIds.IRON_TAIL_POWERUP3.value,
                                requirements=Requirements(
                                    can_reach_locations=["Treehouse - Iron Tail Upgrade 2"])),
                   ]),

    PokeparkRegion(name="Meadow Zone - Overworld",
                   display="Meadow Zone - Overworld",
                   requirements=Requirements(
                       unlock_names=["Meadow Zone Unlock"]
                   ),
                   friendship_locations=[

                       Location(name="Bulbasaur",
                                id=FRIENDSHIP_ITEMS["Bulbasaur"],
                                requirements=Requirements(
                                    prisma_names=["Bulbasaur Prisma"])),

                       Location(name="Munchlax",
                                id=FRIENDSHIP_ITEMS["Munchlax"],
                                requirements=Requirements(
                                    prisma_names=["Bulbasaur Prisma"],
                                    powers=PowerRequirement.can_destroy_objects_overworld
                                )),

                       Location(name="Tropius",
                                id=FRIENDSHIP_ITEMS["Tropius"],
                                requirements=Requirements(
                                    unlock_names=["Tropius Unlock"],
                                    prisma_names=["Bulbasaur Prisma"],
                                    powers=PowerRequirement.can_destroy_objects_overworld
                                )),

                       Location(name="Turtwig",
                                id=FRIENDSHIP_ITEMS["Turtwig"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_play_catch
                                )
                                ),

                       Location(name="Bonsly",
                                id=FRIENDSHIP_ITEMS["Bonsly"],
                                requirements=Requirements(
                                    unlock_names=["Bonsly Unlock"])),

                       Location(name="Pachirisu",
                                id=FRIENDSHIP_ITEMS["Pachirisu"],
                                requirements=Requirements(
                                    unlock_names=["Pachirisu Unlock"],
                                    powers=PowerRequirement.can_play_catch
                                )),

                       Location(name="Sudowoodo",
                                id=FRIENDSHIP_ITEMS["Sudowoodo"],
                                requirements=Requirements(
                                    unlock_names=["Sudowoodo Unlock"])),

                       Location(name="Buneary",
                                id=FRIENDSHIP_ITEMS["Buneary"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_play_catch
                                )),

                       Location(name="Shinx",
                                id=FRIENDSHIP_ITEMS["Shinx"],
                                requirements=Requirements(
                                    unlock_names=["Shinx Unlock"],
                                    powers=PowerRequirement.can_play_catch
                                )),

                       Location(name="Spearow",
                                id=FRIENDSHIP_ITEMS["Spearow"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle
                                )),

                       Location(name="Croagunk",
                                id=FRIENDSHIP_ITEMS["Croagunk"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle
                                )),

                       Location(name="Lotad",
                                id=FRIENDSHIP_ITEMS["Lotad"],
                                requirements=Requirements(
                                    unlock_names=["Lotad Unlock"],
                                    powers=PowerRequirement.can_battle
                                )),

                       Location(name="Treecko",
                                id=FRIENDSHIP_ITEMS["Treecko"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_play_catch
                                )),

                       Location(name="Caterpie",
                                id=FRIENDSHIP_ITEMS["Caterpie"],
                                requirements=Requirements(
                                    unlock_names=["Caterpie Unlock"],
                                    powers=PowerRequirement.can_play_catch,
                                    can_reach_locations=["Meadow Zone - Overworld - Caterpie Tree Dash"]
                                )),

                       Location(name="Butterfree",
                                id=FRIENDSHIP_ITEMS["Butterfree"],
                                requirements=Requirements(
                                    unlock_names=["Butterfree Unlock"],
                                    powers=PowerRequirement.can_play_catch
                                )),

                       Location(name="Chimchar",
                                id=FRIENDSHIP_ITEMS["Chimchar"],
                                requirements=Requirements(
                                    unlock_names=["Chimchar Unlock"],
                                    powers=PowerRequirement.can_battle
                                )),

                       Location(name="Aipom",
                                id=FRIENDSHIP_ITEMS["Aipom"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_play_catch
                                )),

                       Location(name="Ambipom",
                                id=FRIENDSHIP_ITEMS["Ambipom"],
                                requirements=Requirements(
                                    unlock_names=["Ambipom Unlock"],
                                    powers=PowerRequirement.can_play_catch
                                )),

                       Location(name="Weedle",
                                id=FRIENDSHIP_ITEMS["Weedle"],
                                requirements=Requirements(
                                    unlock_names=["Weedle Unlock"],
                                    powers=PowerRequirement.can_dash_overworld, # generation tweak so battle and unlock location are reachable
                                    can_reach_locations=["Meadow Zone - Overworld - Weedle Tree Dash"]

                                )),

                       Location(name="Shroomish",
                                id=FRIENDSHIP_ITEMS["Shroomish"],
                                requirements=Requirements(
                                    unlock_names=["Shroomish Unlock"],
                                    powers=PowerRequirement.can_play_catch,
                                    can_reach_locations=["Meadow Zone - Overworld - Shroomish Crate Dash"]
                                )),

                       Location(name="Magikarp",
                                id=FRIENDSHIP_ITEMS["Magikarp"],
                                requirements=Requirements(
                                    unlock_names=["Magikarp Unlock"],
                                    powers=PowerRequirement.can_play_catch,
                                    can_reach_locations=["Meadow Zone - Overworld - Magikarp electrocuted"]
                                )),

                       Location(name="Oddish",
                                id=FRIENDSHIP_ITEMS["Oddish"]),

                       Location(name="Bidoof",
                                id=FRIENDSHIP_ITEMS["Bidoof"],
                                requirements=Requirements(
                                    can_reach_locations=["Meadow Zone - Overworld - Bidoof Housing 4"])),

                       Location(name="Bibarel",
                                id=FRIENDSHIP_ITEMS["Bibarel"],
                                requirements=Requirements(
                                    unlock_names=["Bibarel Unlock"],
                                    powers=PowerRequirement.can_battle
                                )),

                       Location(name="Leafeon",
                                id=FRIENDSHIP_ITEMS["Leafeon"],
                                requirements=Requirements(
                                    friendcount=21,
                                    powers=PowerRequirement.can_play_catch
                                )),  # 21 Friend Requirement because Leafana itself is not counting

                       Location(name="Torterra",
                                id=FRIENDSHIP_ITEMS["Torterra"],
                                requirements=Requirements(
                                    unlock_names=["Torterra Unlock"],
                                    powers=PowerRequirement.can_battle_thunderbolt_immune
                                )),

                       Location(name="Starly",
                                id=FRIENDSHIP_ITEMS["Starly"],
                                requirements=Requirements(
                                    oneof_item_names=[["Starly Unlock"], ["Starly Unlock 2"]],
                                    powers=PowerRequirement.can_play_catch
                                )),

                       Location(name="Scyther",
                                id=FRIENDSHIP_ITEMS["Scyther"],
                                requirements=Requirements(
                                    unlock_names=["Scyther Unlock"],
                                    powers=PowerRequirement.can_battle
                                )),
                   ],
                   unlock_location=[
                       Location(name="Munchlax Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Tropius Unlock"],
                                requirements=Requirements(
                                    can_reach_locations=["Meadow Zone - Overworld - Munchlax"]
                                )),

                       Location(name="Turtwig Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Pachirisu Unlock"],
                                requirements=Requirements(
                                    can_reach_locations=["Meadow Zone - Overworld - Turtwig"]
                                )),

                       Location(name="Bonsly Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Sudowoodo Unlock"],
                                requirements=Requirements(
                                    can_reach_locations=["Meadow Zone - Overworld - Bonsly"]
                                )),

                       Location(name="Buneary Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Lotad Unlock"],
                                requirements=Requirements(
                                    can_reach_locations=["Meadow Zone - Overworld - Buneary"]
                                )),

                       Location(name="Croagunk Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Scyther Unlock"],
                                requirements=Requirements(
                                    can_reach_locations=["Meadow Zone - Overworld - Croagunk"]
                                )),

                       Location(name="Caterpie Tree Dash",
                                id=UNLOCK_ITEMS["Caterpie Unlock"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_dash_overworld
                                )),

                       Location(name="Caterpie Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Butterfree Unlock"],
                                requirements=Requirements(
                                    can_reach_locations=["Meadow Zone - Overworld - Caterpie"]
                                )),

                       Location(name="Aipom Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Ambipom Unlock"],
                                requirements=Requirements(
                                    can_reach_locations=["Meadow Zone - Overworld - Aipom"]
                                )),

                       Location(name="Weedle Tree Dash",
                                id=UNLOCK_ITEMS["Weedle Unlock"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_dash_overworld
                                )),

                       Location(name="Shroomish Crate Dash",
                                id=UNLOCK_ITEMS["Shroomish Unlock"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_destroy_objects_overworld
                                )),

                       Location(name="Magikarp electrocuted",
                                id=UNLOCK_ITEMS["Magikarp Unlock"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_thunderbolt_overworld
                                )),

                       Location(name="Bidoof Housing 1 - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Bidoof Unlock"],
                                requirements=Requirements(
                                    can_reach_locations=["Meadow Zone - Overworld - Bidoof Housing 1"])),

                       Location(name="Bidoof Housing 2 - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Bidoof Unlock 2"],
                                requirements=Requirements(
                                    can_reach_locations=["Meadow Zone - Overworld - Bidoof Housing 2"])),

                       Location(name="Bidoof Housing 3 - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Bidoof Unlock 3"],
                                requirements=Requirements(
                                    can_reach_locations=["Meadow Zone - Overworld - Bidoof Housing 3"])),

                       Location(name="Bidoof Housing 4 - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Bibarel Unlock"],
                                requirements=Requirements(
                                    can_reach_locations=["Meadow Zone - Overworld - Bidoof Housing 4"])),
                   ],
                   quest_locations=[
                       Location(name="Bidoof Housing 1",
                                id=QuestLocationIds.MEADOW_BIDOOF_HOUSING1.value,
                                requirements=Requirements(
                                    friendship_names=["Mankey"],
                                    powers=PowerRequirement.can_destroy_objects_overworld
                                )),

                       Location(name="Bidoof Housing 2",
                                id=QuestLocationIds.MEADOW_BIDOOF_HOUSING2.value,
                                requirements=Requirements(
                                    can_reach_locations=["Meadow Zone - Overworld - Bidoof Housing 1"])),

                       Location(name="Bidoof Housing 3",
                                id=QuestLocationIds.MEADOW_BIDOOF_HOUSING3.value,
                                requirements=Requirements(
                                    can_reach_locations=["Meadow Zone - Overworld - Bidoof Housing 2"])),

                       Location(name="Bidoof Housing 4",
                                id=QuestLocationIds.MEADOW_BIDOOF_HOUSING4.value,
                                requirements=Requirements(
                                    can_reach_locations=["Meadow Zone - Overworld - Bidoof Housing 3"])),
                   ],
                   parent_regions=["Treehouse"]),

    PokeparkRegion(name="Meadow Zone - Bulbasaur's Daring Dash Minigame",
                   display="Meadow Zone - Bulbasaur's Daring Dash Minigame",
                   minigame_location=[
                       Location(name="Prisma",
                                id=PRISM_ITEM["Bulbasaur Prisma"]),

                       Location(name="Pikachu",
                                id=MinigameLocationIds.PIKACHU_DASH.value),

                       Location(name="Turtwig",
                                id=MinigameLocationIds.TURTWIG_DASH.value,
                                requirements=Requirements(
                                    friendship_names=["Turtwig"])),

                       Location(name="Munchlax",
                                id=MinigameLocationIds.MUNCHLAX_DASH.value,
                                requirements=Requirements(
                                    friendship_names=["Munchlax"])),

                       Location(name="Chimchar",
                                id=MinigameLocationIds.CHIMCHAR_DASH.value,
                                requirements=Requirements(
                                    friendship_names=["Chimchar"])),

                       Location(name="Treecko",
                                id=MinigameLocationIds.TREECKO_DASH.value,
                                requirements=Requirements(
                                    friendship_names=["Treecko"])),

                       Location(name="Bibarel",
                                id=MinigameLocationIds.BIBAREL_DASH.value,
                                requirements=Requirements(
                                    friendship_names=["Bibarel"])),

                       Location(name="Bulbasaur",
                                id=MinigameLocationIds.BULBASAUR_DASH.value,
                                requirements=Requirements(
                                    friendship_names=["Bulbasaur"])),

                       Location(name="Bidoof",
                                id=MinigameLocationIds.BIDOOF_DASH.value,
                                requirements=Requirements(
                                    friendship_names=["Bidoof"])),

                       Location(name="Oddish",
                                id=MinigameLocationIds.ODDISH_DASH.value,
                                requirements=Requirements(
                                    friendship_names=["Oddish"])),

                       Location(name="Shroomish",
                                id=MinigameLocationIds.SHROOMISH_DASH.value,
                                requirements=Requirements(
                                    friendship_names=["Shroomish"])),

                       Location(name="Bonsly",
                                id=MinigameLocationIds.BONSLY_DASH.value,
                                requirements=Requirements(
                                    friendship_names=["Bonsly"])),

                       Location(name="Lotad",
                                id=MinigameLocationIds.LOTAD_DASH.value,
                                requirements=Requirements(
                                    friendship_names=["Lotad"])),

                       Location(name="Weedle",
                                id=MinigameLocationIds.WEEDLE_DASH.value,
                                requirements=Requirements(
                                    friendship_names=["Weedle"])),

                       Location(name="Caterpie",
                                id=MinigameLocationIds.CATERPIE_DASH.value,
                                requirements=Requirements(
                                    friendship_names=["Caterpie"])),

                       Location(name="Magikarp",
                                id=MinigameLocationIds.MAGIKARP_DASH.value,
                                requirements=Requirements(
                                    friendship_names=["Magikarp"])),

                       # Location(name="Jolteon",
                       #          id=MinigameLocationIds.JOLTEON_DASH.value,
                       #          requirements=Requirements(friendship_names=["Jolteon"])), # not implemented yet

                       # Location(name="Arcanine",
                       #          id=MinigameLocationIds.ARCANINE_DASH.value,
                       #          requirements=Requirements(
                       #              friendship_names=["Arcanine"])), #not implemented yet

                       Location(name="Leafeon",
                                id=MinigameLocationIds.LEAFEON_DASH.value,
                                requirements=Requirements(
                                    friendship_names=["Leafeon"])),

                       Location(name="Scyther",
                                id=MinigameLocationIds.SCYTHER_DASH.value,
                                requirements=Requirements(
                                    friendship_names=["Scyther"])),

                       Location(name="Ponyta",
                                 id=MinigameLocationIds.PONYTA_DASH.value,
                                requirements=Requirements(
                                     friendship_names=["Ponyta"])),

                       Location(name="Shinx",
                                id=MinigameLocationIds.SHINX_DASH.value,
                                requirements=Requirements(
                                    friendship_names=["Shinx"])),

                       # Location(name="Eevee",
                       #          id=MinigameLocationIds.EEVEE_DASH.value,
                       #          requirements=Requirements(
                       #              friendship_names=["Eevee"])), # not implemented yet

                       Location(name="Pachirisu",
                                id=MinigameLocationIds.PACHIRISU_DASH.value,
                                requirements=Requirements(
                                    friendship_names=["Pachirisu"])),

                       Location(name="Buneary",
                                id=MinigameLocationIds.BUNEARY_DASH.value,
                                requirements=Requirements(
                                    friendship_names=["Buneary"])),

                       Location(name="Croagunk",
                                id=MinigameLocationIds.CROAGUNK_DASH.value,
                                requirements=Requirements(
                                    friendship_names=["Croagunk"])),

                   ],
                   parent_regions=["Meadow Zone - Overworld"]),

    PokeparkRegion(name="Meadow Zone - Venusaur's Vine Swing",
                   display="Meadow Zone - Venusaur's Vine Swing",
                   requirements=Requirements(
                       friendship_names=["Croagunk", "Spearow"]),

                   minigame_location=[
                       Location(name="Prisma",
                                id=PRISM_ITEM["Venusaur Prisma"]),

                       Location(name="Pikachu",
                                id=MinigameLocationIds.PIKACHU_VINE_SWING.value),

                       Location(name="Munchlax",
                                id=MinigameLocationIds.MUNCHLAX_VINE_SWING.value,
                                requirements=Requirements(
                                    friendship_names=["Munchlax"])),

                       Location(name="Magikarp",
                                id=MinigameLocationIds.MAGIKARP_VINE_SWING.value,
                                requirements=Requirements(
                                    friendship_names=["Magikarp"])),

                       # Location(name="Blaziken",
                       #          id=MinigameLocationIds.BLAZIKEN_VINE_SWING.value,
                       #          requirements=Requirements(
                       #              friendship_names=["Blaziken"])),

                       Location(name="Infernape",
                                 id=MinigameLocationIds.INFERNAPE_VINE_SWING.value,
                                 requirements=Requirements(
                                     friendship_names=["Infernape"])),

                       # Location(name="Lucario",
                       #          id=MinigameLocationIds.LUCARIO_VINE_SWING.value,
                       #          requirements=Requirements(
                       #              friendship_names= ["Lucario"])),

                       Location(name="Primeape",
                                id=MinigameLocationIds.PRIMEAPE_VINE_SWING.value,
                                requirements=Requirements(
                                    friendship_names=["Primeape"])),

                       # Location(name="Tangrowth",
                       #          id=MinigameLocationIds.TANGROWTH_VINE_SWING.value,
                       #          requirements=Requirements(
                       #              friendship_names= ["Tangrowth"])),

                       Location(name="Ambipom",
                                id=MinigameLocationIds.AMBIPOM_VINE_SWING.value,
                                requirements=Requirements(
                                    friendship_names=["Ambipom"])),

                       Location(name="Croagunk",
                                id=MinigameLocationIds.CROAGUNK_VINE_SWING.value,
                                requirements=Requirements(
                                    friendship_names=["Croagunk"])),

                       Location(name="Mankey",
                                id=MinigameLocationIds.MANKEY_VINE_SWING.value,
                                requirements=Requirements(
                                    friendship_names=["Mankey"])),

                       Location(name="Aipom",
                                id=MinigameLocationIds.AIPOM_VINE_SWING.value,
                                requirements=Requirements(
                                    friendship_names=["Aipom"])),

                       Location(name="Chimchar",
                                id=MinigameLocationIds.CHIMCHAR_VINE_SWING.value,
                                requirements=Requirements(
                                    friendship_names=["Chimchar"])),

                       Location(name="Treecko",
                                id=MinigameLocationIds.TREECKO_VINE_SWING.value,
                                requirements=Requirements(
                                    friendship_names=["Treecko"])),

                       Location(name="Pachirisu",
                                id=MinigameLocationIds.PACHIRISU_VINE_SWING.value,
                                requirements=Requirements(
                                    friendship_names=["Pachirisu"])),

                   ],
                   parent_regions=["Meadow Zone - Overworld"]),

    PokeparkRegion(name="Beach Zone - Overworld",
                   display="Beach Zone - Overworld",
                   requirements=Requirements(
                       unlock_names=["Beach Zone Unlock"]),
                   friendship_locations=[
                       Location(name="Buizel",
                                id=FRIENDSHIP_ITEMS["Buizel"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_play_catch
                                )),

                       Location(name="Psyduck",
                                id=FRIENDSHIP_ITEMS["Psyduck"]),

                       Location(name="Slowpoke",
                                id=FRIENDSHIP_ITEMS["Slowpoke"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_play_catch
                                )),

                       Location(name="Azurill",
                                id=FRIENDSHIP_ITEMS["Azurill"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_play_catch
                                )),
                       Location(name="Totodile",
                                id=FRIENDSHIP_ITEMS["Totodile"],
                                requirements=Requirements(
                                    unlock_names=["Totodile Unlock"],
                                    powers=PowerRequirement.can_battle
                                )),

                       Location(name="Mudkip",
                                id=FRIENDSHIP_ITEMS["Mudkip"],
                                requirements=Requirements(
                                    unlock_names=["Mudkip Unlock"])),

                       Location(name="Pidgeotto",
                                id=FRIENDSHIP_ITEMS["Pidgeotto"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle
                                )),
                       Location(name="Taillow",
                                id=FRIENDSHIP_ITEMS["Taillow"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_play_catch
                                )),

                       Location(name="Wingull",
                                id=FRIENDSHIP_ITEMS["Wingull"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_play_catch
                                )),

                       Location(name="Staravia",
                                id=FRIENDSHIP_ITEMS["Staravia"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle
                                )),

                       Location(name="Corsola",
                                id=FRIENDSHIP_ITEMS["Corsola"]),

                       Location(name="Floatzel",
                                id=FRIENDSHIP_ITEMS["Floatzel"],
                                requirements=Requirements(
                                    unlock_names=["Floatzel Unlock"],
                                    powers=PowerRequirement.can_battle
                                )),

                       Location(name="Vaporeon",
                                id=FRIENDSHIP_ITEMS["Vaporeon"],
                                requirements=Requirements(
                                    friendcount=31,
                                    powers=PowerRequirement.can_play_catch
                                )),  # +1 for itself

                       Location(name="Golduck",
                                id=FRIENDSHIP_ITEMS["Golduck"],
                                requirements=Requirements(
                                    unlock_names=["Golduck Unlock"],
                                    powers=PowerRequirement.can_battle
                                )),

                       Location(name="Krabby",
                                id=FRIENDSHIP_ITEMS["Krabby"],
                                requirements=Requirements(
                                    unlock_names=["Krabby Unlock"],
                                    powers=PowerRequirement.can_play_catch,
                                    can_reach_locations=["Beach Zone - Overworld - Bottle Recycling 2 - Pokemon Unlock"]

                                )),

                       Location(name="Wailord",
                                id=FRIENDSHIP_ITEMS["Wailord"]),

                       Location(name="Corphish",
                                id=FRIENDSHIP_ITEMS["Corphish"],
                                requirements=Requirements(
                                    unlock_names=["Corphish Unlock"],
                                    powers=PowerRequirement.can_battle,
                                    can_reach_locations=["Beach Zone - Overworld - Bottle Recycling 4 - Pokemon Unlock"]

                                )),

                       Location(name="Feraligatr",
                                id=FRIENDSHIP_ITEMS["Feraligatr"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle
                                )),

                       Location(name="Starly",
                                id=OverworldPokemonLocationIds.STARLY_BEACH.value,
                                requirements=Requirements(
                                    powers=PowerRequirement.can_play_catch
                                )),

                   ],
                   unlock_location=[
                       Location(name="Buizel Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Floatzel Unlock"],
                                requirements=Requirements(
                                    can_reach_locations=["Beach Zone - Overworld - Buizel"]
                                )),

                       Location(name="Psyduck Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Golduck Unlock"],
                                requirements=Requirements(
                                    can_reach_locations=["Beach Zone - Overworld - Psyduck"]
                                )),

                       Location(name="Slowpoke Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Mudkip Unlock"],
                                requirements=Requirements(
                                    can_reach_locations=["Beach Zone - Overworld - Slowpoke"]
                                )),

                       Location(name="Azurill Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Totodile Unlock"],
                                requirements=Requirements(
                                    can_reach_locations=["Beach Zone - Overworld - Azurill"]
                                )),

                       Location(name="Bottle Recycling 2 - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Krabby Unlock"],
                                requirements=Requirements(
                                    can_reach_locations=["Beach Zone - Overworld - Bottle Recycling 2"],

                                )),

                       Location(name="Bottle Recycling 4 - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Corphish Unlock"],
                                requirements=Requirements(
                                    can_reach_locations=["Beach Zone - Overworld - Bottle Recycling 4"]
                                )),
                   ],
                   quest_locations=[
                       Location(name="Bottle Recycling 1",
                                id=QuestLocationIds.BEACH_BOTTLE1.value,
                                ),

                       Location(name="Bottle Recycling 2",
                                id=QuestLocationIds.BEACH_BOTTLE2.value,
                                requirements=Requirements(
                                    can_reach_locations=["Beach Zone - Overworld - Bottle Recycling 1"]
                                )),

                       Location(name="Bottle Recycling 3",
                                id=QuestLocationIds.BEACH_BOTTLE3.value,
                                requirements=Requirements(
                                    can_reach_locations=["Beach Zone - Overworld - Bottle Recycling 2"]
                                )),

                       Location(name="Bottle Recycling 4",
                                id=QuestLocationIds.BEACH_BOTTLE4.value,
                                requirements=Requirements(
                                    can_reach_locations=["Beach Zone - Overworld - Bottle Recycling 3"]
                                )),

                       Location(name="Bottle Recycling 5",
                                id=QuestLocationIds.BEACH_BOTTLE5.value,
                                requirements=Requirements(
                                    can_reach_locations=["Beach Zone - Overworld - Bottle Recycling 4"]
                                )),

                       Location(name="Bottle Recycling 6",
                                id=QuestLocationIds.BEACH_BOTTLE6.value,
                                requirements=Requirements(
                                    can_reach_locations=["Beach Zone - Overworld - Bottle Recycling 5"]
                                )),
                   ],
                   parent_regions=["Treehouse"]),

    PokeparkRegion(name="Beach Zone - Pelipper's Circle Circuit",
                   display="Beach Zone - Pelipper's Circle Circuit",
                   minigame_location=[
                       Location(name="Prisma",
                                id=PRISM_ITEM["Pelipper Prisma"]),

                       Location(name="Pikachu",
                                id=MinigameLocationIds.PIKACHU_CIRCLE.value,
                                requirements=Requirements(
                                    unlock_names=["Pikachu Balloon"])),

                       # Location(name="Staraptor",
                       #          id=MinigameLocationIds.STARAPTOR_CIRCLE.value,
                       #          requirements=Requirements(
                       #              friendship_names=["Staraptor"])), # Staraptor missing

                       # Location(name="Togekiss",
                       #          id=MinigameLocationIds.TOGEKISS_CIRCLE.value,
                       #          requirements=Requirements(
                       #              friendship_names=["Togekiss"])), #togekiss is missing

                       # Location(name="Honchkrow",
                       #          id= MinigameLocationIds.HONCHKROW_CIRCLE.value,
                       #          requirements=Requirements(
                       #              friendship_names=["Honchkrow"])), #Honchkrow is missing

                       # Location(name="Gliscor",
                       #          id=MinigameLocationIds.GLISCOR_CIRCLE.value,
                       #          requirements=Requirements(
                       #              friendship_names=["Gliscor"])), #Gliscor is missing

                       Location(name="Pelipper",
                                id=MinigameLocationIds.PELIPPER_CIRCLE.value,
                                requirements=Requirements(
                                    friendship_names=["Pelipper"])),

                       Location(name="Staravia",
                                id=MinigameLocationIds.STARAVIA_CIRCLE.value,
                                requirements=Requirements(
                                    friendship_names=["Staravia"])),

                       Location(name="Pidgeotto",
                                id=MinigameLocationIds.PIDGEOTTO_CIRCLE.value,
                                requirements=Requirements(
                                    friendship_names=["Pidgeotto"])),

                       Location(name="Butterfree",
                                id=MinigameLocationIds.BUTTERFREE_CIRCLE.value,
                                requirements=Requirements(
                                    friendship_names=["Butterfree"])),

                       Location(name="Tropius",
                                id=MinigameLocationIds.TROPIUS_CIRCLE.value,
                                requirements=Requirements(friendship_names=["Tropius"])),

                       # Location(name="Murkrow",
                       #          id=MinigameLocationIds.MURKROW_CIRCLE.value,
                       #          requirements= Requirements(
                       #              friendship_names=["Murkrow"])), # Murkow is missing

                       Location(name="Taillow",
                                id=MinigameLocationIds.TAILLOW_CIRCLE.value,
                                requirements=Requirements(
                                    friendship_names=["Taillow"])),

                       Location(name="Spearow",
                                id=MinigameLocationIds.SPEAROW_CIRCLE.value,
                                requirements=Requirements(
                                    friendship_names=["Spearow"])),

                       Location(name="Starly",
                                id=MinigameLocationIds.STARLY_CIRCLE.value,
                                requirements=Requirements(
                                    friendship_names=["Starly"])),

                       Location(name="Wingull",
                                id=MinigameLocationIds.WINGULL_CIRCLE.value,
                                requirements=Requirements(
                                    friendship_names=["Wingull"])),

                   ],
                   parent_regions=["Beach Zone - Overworld"]),

    PokeparkRegion("Beach Zone - Gyarados' Aqua Dash", "Beach Zone - Gyarados' Aqua Dash",
                   minigame_location=[
                       Location(name="Prisma",
                                id=PRISM_ITEM["Gyarados Prisma"]),

                       Location(name="Pikachu",
                                id=MinigameLocationIds.PIKACHU_AQUA.value,
                                requirements=Requirements(
                                    unlock_names=["Pikachu Surfboard"])),

                       Location(name="Psyduck",
                                id=MinigameLocationIds.PSYDUCK_AQUA.value,
                                requirements=Requirements(
                                    friendship_names=["Psyduck"])),

                       Location(name="Azurill",
                                id=MinigameLocationIds.AZURILL_AQUA.value,
                                requirements=Requirements(
                                    friendship_names=["Azurill"])),

                       Location(name="Slowpoke",
                                id=MinigameLocationIds.SLOWPOKE_AQUA.value,
                                requirements=Requirements(
                                    friendship_names=["Slowpoke"])),

                       Location(name="Empoleon",
                                id=MinigameLocationIds.EMPOLEON_AQUA.value,
                                requirements=Requirements(
                                    friendship_names=["Empoleon"])),

                       Location(name="Floatzel",
                                id=MinigameLocationIds.FLOATZEL_AQUA.value,
                                requirements=Requirements(
                                    friendship_names=["Floatzel"])),

                       Location(name="Feraligatr",
                                id=MinigameLocationIds.FERALIGATR_AQUA.value,
                                requirements=Requirements(
                                    friendship_names=["Feraligatr"])),

                       Location(name="Golduck",
                                id=MinigameLocationIds.GOLDUCK_AQUA.value,
                                requirements=Requirements(
                                    friendship_names=["Golduck"])),

                       Location(name="Vaporeon",
                                id=MinigameLocationIds.VAPOREON_AQUA.value,
                                requirements=Requirements(
                                    friendship_names=["Vaporeon"])),

                       Location(name="Prinplup",
                                id=MinigameLocationIds.PRINPLUP_AQUA.value,
                                requirements=Requirements(
                                    friendship_names=["Prinplup"])),

                       Location(name="Bibarel",
                                id=MinigameLocationIds.BIBAREL_AQUA.value,
                                requirements=Requirements(
                                    friendship_names=["Bibarel"])),

                       Location(name="Buizel",
                                id=MinigameLocationIds.BUIZEL_AQUA.value,
                                requirements=Requirements(
                                    friendship_names=["Buizel"])),

                       Location(name="Corsola",
                                id=MinigameLocationIds.CORSOLA_AQUA.value,
                                requirements=Requirements(
                                    friendship_names=["Corsola"])),

                       Location(name="Piplup",
                                id=MinigameLocationIds.PIPLUP_AQUA.value,
                                requirements=Requirements(
                                    friendship_names=["Piplup"])),

                       Location(name="Lotad",
                                id=MinigameLocationIds.LOTAD_AQUA.value,
                                requirements=Requirements(
                                    friendship_names=["Lotad"])),

                   ],
                   parent_regions=["Beach Zone - Overworld"]),

    PokeparkRegion(name="Ice Zone - Overworld",
                   display="Ice Zone - Overworld",
                   requirements=Requirements(
                       unlock_names=["Ice Zone Unlock"]),
                   friendship_locations=[

                       Location(name="Lapras",
                                id=FRIENDSHIP_ITEMS["Lapras"]),
                       Location(name="Spheal",
                                id=FRIENDSHIP_ITEMS["Spheal"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_play_catch
                                )),
                       Location(name="Krabby",
                                id=OverworldPokemonLocationIds.KRABBY_ICE.value,
                                requirements=Requirements(
                                    unlock_names=["Krabby Unlock"],
                                    powers=PowerRequirement.can_play_catch
                                )),
                       Location(name="Mudkip",
                                id=OverworldPokemonLocationIds.MUDKIP_ICE.value,
                                requirements=Requirements(
                                    unlock_names=["Mudkip Unlock"])),
                       Location(name="Octillery",
                                id=FRIENDSHIP_ITEMS["Octillery"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle
                                )),
                       Location(name="Teddiursa",
                                id=FRIENDSHIP_ITEMS["Teddiursa"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_play_catch
                                )),
                       Location(name="Taillow",
                                id=OverworldPokemonLocationIds.TAILLOW_ICE.value,
                                requirements=Requirements(
                                    powers=PowerRequirement.can_play_catch
                                )),
                       Location(name="Starly",
                                id=OverworldPokemonLocationIds.STARLY_ICE.value,
                                requirements=Requirements(
                                    powers=PowerRequirement.can_play_catch
                                )),
                       Location(name="Staravia",
                                id=OverworldPokemonLocationIds.STARAVIA_ICE.value,
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle
                                )),
                       Location(name="Delibird",
                                id=FRIENDSHIP_ITEMS["Delibird"],
                                requirements=Requirements(
                                    can_reach_locations=["Ice Zone - Overworld - Christmas Tree Present 4"]
                                )),
                       Location(name="Smoochum",
                                id=FRIENDSHIP_ITEMS["Smoochum"],
                                requirements=Requirements(
                                    unlock_names=["Smoochum Unlock"],
                                    powers=PowerRequirement.can_battle
                                )),
                       Location(name="Squirtle",
                                id=FRIENDSHIP_ITEMS["Squirtle"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle,
                                    unlock_names=["Squirtle Unlock"])),
                       Location(name="Glaceon",
                                id=FRIENDSHIP_ITEMS["Glaceon"],
                                requirements=Requirements(
                                    friendcount=51,
                                    powers=PowerRequirement.can_play_catch
                                )),
                       Location(name="Prinplup",
                                id=FRIENDSHIP_ITEMS["Prinplup"],
                                requirements=Requirements(
                                    can_reach_locations=["Ice Zone - Overworld - Igloo Quest 3"],
                                    powers=PowerRequirement.can_battle
                                )),
                       Location(name="Sneasel",
                                id=FRIENDSHIP_ITEMS["Sneasel"],
                                requirements=Requirements(
                                    unlock_names=["Sneasel Unlock"],
                                    powers=PowerRequirement.can_play_catch
                                )),
                       Location(name="Piloswine",
                                id=FRIENDSHIP_ITEMS["Piloswine"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle_thunderbolt_immune
                                )),
                       Location(name="Glalie",  # Quest dependent and Unlock
                                id=FRIENDSHIP_ITEMS["Glalie"],
                                requirements=Requirements(
                                    can_reach_locations=["Ice Zone - Overworld - Igloo Quest 3"]
                                )),
                       Location(name="Primeape",
                                id=FRIENDSHIP_ITEMS["Primeape"],
                                requirements=Requirements(
                                    unlock_names=["Primeape Unlock"],
                                    powers=PowerRequirement.can_battle
                                )),
                       Location(name="Ursaring",
                                id=FRIENDSHIP_ITEMS["Ursaring"],
                                requirements=Requirements(
                                    unlock_names=["Ursaring Unlock"],
                                    powers=PowerRequirement.can_battle
                                )),
                       Location(name="Mamoswine",
                                id=FRIENDSHIP_ITEMS["Mamoswine"],
                                requirements=Requirements(
                                    unlock_names=["Mamoswine Unlock"],
                                    powers=PowerRequirement.can_battle_thunderbolt_immune
                                )),
                       Location(name="Kirlia",
                                id=FRIENDSHIP_ITEMS["Kirlia"],
                                requirements=Requirements(
                                    friendship_names=["Delibird"],
                                    can_reach_locations=["Ice Zone - Overworld - Delibird"]
                                )),
                   ],
                   unlock_location=[
                       Location(name="Igloo Quest 1 - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Primeape Unlock"],
                                requirements=Requirements(
                                    can_reach_locations=["Ice Zone - Overworld - Igloo Quest 1"]
                                )),
                       Location(name="Igloo Quest 2 - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Ursaring Unlock"],
                                requirements=Requirements(
                                    can_reach_locations=["Ice Zone - Overworld - Igloo Quest 2"]
                                )),
                   ],
                   quest_locations=[
                       Location(name="Igloo Quest 1",
                                id=QuestLocationIds.IGLOO_QUEST1.value,
                                requirements=Requirements(
                                    unlock_names=["Glalie Unlock"]
                                )),
                       Location(name="Igloo Quest 2",
                                id=QuestLocationIds.IGLOO_QUEST2.value,
                                requirements=Requirements(
                                    can_reach_locations=["Ice Zone - Overworld - Igloo Quest 1"]
                                )),
                       Location(name="Igloo Quest 3",
                                id=QuestLocationIds.IGLOO_QUEST3.value,
                                requirements=Requirements(
                                    can_reach_locations=["Ice Zone - Overworld - Igloo Quest 2"]
                                )),
                       Location(name="Christmas Tree Present 1",
                                id=QuestLocationIds.CHRISTMAS_TREE1.value,
                                requirements=Requirements(
                                    friendship_names=["Spheal"],
                                    unlock_names=["Delibird Unlock"]
                                )),
                       Location(name="Christmas Tree Present 2",
                                id=QuestLocationIds.CHRISTMAS_TREE2.value,
                                requirements=Requirements(
                                    friendship_names=["Teddiursa"],
                                    can_reach_locations=["Ice Zone - Overworld - Christmas Tree Present 1"]
                                )),
                       Location(name="Christmas Tree Present 3",
                                id=QuestLocationIds.CHRISTMAS_TREE3.value,
                                requirements=Requirements(
                                    unlock_names=["Squirtle Unlock"],
                                    friendship_names=["Squirtle"],
                                    can_reach_locations=["Ice Zone - Overworld - Christmas Tree Present 2"]
                                )),
                       Location(name="Christmas Tree Present 4",
                                id=QuestLocationIds.CHRISTMAS_TREE4.value,
                                requirements=Requirements(
                                    friendship_names=["Smoochum"],
                                    unlock_names=["Smoochum Unlock"],
                                    can_reach_locations=["Ice Zone - Overworld - Christmas Tree Present 3"]
                                )),

                   ],
                   parent_regions=["Treehouse", "Beach Zone - Overworld"]),
    PokeparkRegion(name="Ice Zone - Overworld - Lower Lift Region",
                   display="Ice Zone - Overworld - Lower Lift Region",
                   requirements=Requirements(
                       friendship_names=["Prinplup"]),
                   friendship_locations=[
                       Location(name="Corphish",
                                id=OverworldPokemonLocationIds.CORPHISH_ICE.value,
                                requirements=Requirements(
                                    unlock_names=["Corphish Unlock"],
                                    powers=PowerRequirement.can_battle
                                )),
                       Location(name="Wingull",
                                id=OverworldPokemonLocationIds.WINGULL_ICE.value,
                                requirements=Requirements(
                                    powers=PowerRequirement.can_play_catch
                                )),
                       Location(name="Quagsire",
                                id=FRIENDSHIP_ITEMS["Quagsire"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_destroy_objects_overworld
                                )),

                   ],
                   parent_regions=["Ice Zone - Overworld"]),

    PokeparkRegion(name="Ice Zone - Empoleon's Snow Slide",
                   display="Ice Zone - Empoleon's Snow Slide",
                   minigame_location=[Location(name="Prisma",
                                               id=PRISM_ITEM["Empoleon Prisma"]),

                                      Location(name="Pikachu",
                                               id=MinigameLocationIds.PIKACHU_SLIDE.value,
                                               requirements=Requirements(
                                                   unlock_names=["Pikachu Snowboard"])),
                                      Location(name="Teddiursa",
                                               id=MinigameLocationIds.TEDDIURSA_SLIDE.value,
                                               requirements=Requirements(
                                                   friendship_names=["Teddiursa"])),
                                      Location(name="Magikarp",
                                               id=MinigameLocationIds.MAGIKARP_SLIDE.value,
                                               requirements=Requirements(
                                                   friendship_names=["Magikarp"])),
                                      Location(name="Empoleon",
                                               id=MinigameLocationIds.EMPOLEON_SLIDE.value,
                                               requirements=Requirements(
                                                   friendship_names=["Empoleon"])),
                                      Location(name="Glaceon",
                                               id=MinigameLocationIds.GLACEON_SLIDE.value,
                                               requirements=Requirements(
                                                   friendship_names=["Glaceon"])),
                                      # Location(name="Blastoise",
                                      #          id=MinigameLocationIds.BLASTOISE_SLIDE.value,
                                      #          requirements=Requirements(
                                      #              friendship_names=["Blastoise"])),
                                      Location(name="Glalie",
                                               id=MinigameLocationIds.GLALIE_SLIDE.value,
                                               requirements=Requirements(
                                                   friendship_names=["Glalie"])),
                                      Location(name="Lapras",
                                               id=MinigameLocationIds.LAPRAS_SLIDE.value,
                                               requirements=Requirements(
                                                   friendship_names=["Lapras"])),
                                      Location(name="Delibird",
                                               id=MinigameLocationIds.DELIBIRD_SLIDE.value,
                                               requirements=Requirements(
                                                   friendship_names=["Delibird"])),
                                      Location(name="Piloswine",
                                               id=MinigameLocationIds.PILOSWINE_SLIDE.value,
                                               requirements=Requirements(
                                                   friendship_names=["Piloswine"])),
                                      Location(name="Prinplup",
                                               id=MinigameLocationIds.PRINPLUP_SLIDE.value,
                                               requirements=Requirements(
                                                   friendship_names=["Prinplup"])),
                                      Location(name="Squirtle",
                                               id=MinigameLocationIds.SQUIRTLE_SLIDE.value,
                                               requirements=Requirements(
                                                   friendship_names=["Squirtle"])),
                                      Location(name="Piplup",
                                               id=MinigameLocationIds.PIPLUP_SLIDE.value,
                                               requirements=Requirements(
                                                   friendship_names=["Piplup"])),
                                      Location(name="Quagsire",
                                               id=MinigameLocationIds.QUAGSIRE_SLIDE.value,
                                               requirements=Requirements(
                                                   friendship_names=["Quagsire"])),
                                      Location(name="Spheal",
                                               id=MinigameLocationIds.SPHEAL_SLIDE.value,
                                               requirements=Requirements(
                                                   friendship_names=["Spheal"])),
                                      ],
                   parent_regions=["Ice Zone - Overworld"]),
    PokeparkRegion(name="Cavern Zone - Overworld",
                   display="Cavern Zone - Overworld",
                   requirements=Requirements(
                       unlock_names=["Cavern Zone & Magma Zone Unlock"]),
                   friendship_locations=[
                       Location(name="Magnemite",
                                id=FRIENDSHIP_ITEMS["Magnemite"],
                                requirements=Requirements(
                                    unlock_names=["Magnemite Unlock"],
                                    can_reach_locations=["Cavern Zone - Overworld - Magnemite Crate Dash Entrance Area"]
                                )),
                       Location(name="Magnemite 2",
                                id=OverworldPokemonLocationIds.MAGNEMITE_CAVERN_2.value,
                                requirements=Requirements(
                                    unlock_names=["Magnemite Unlock 2"],
                                    can_reach_locations=[
                                        "Cavern Zone - Overworld - Magnemite Crate Dash Magma Zone Entrance"]
                                )),
                       Location(name="Magnemite 3",
                                id=OverworldPokemonLocationIds.MAGNEMITE_CAVERN_3.value,
                                requirements=Requirements(
                                    unlock_names=["Magnemite Unlock 3"],
                                    can_reach_locations=[
                                        "Cavern Zone - Overworld - Magnemite Crate Dash Magma Zone Entrance"]
                                )),
                       Location(name="Magnezone",
                                id=FRIENDSHIP_ITEMS["Magnezone"],
                                requirements=Requirements(
                                    unlock_names=["Magnezone Unlock"],
                                    powers=PowerRequirement.can_battle_thunderbolt_immune
                                )),
                       Location(name="Geodude",
                                id=FRIENDSHIP_ITEMS["Geodude"]),
                       Location(name="Torchic",
                                id=FRIENDSHIP_ITEMS["Torchic"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle
                                )),
                       Location(name="Machamp",
                                id=FRIENDSHIP_ITEMS["Machamp"]),
                       Location(name="Machamp - Battle",
                                id=OverworldPokemonLocationIds.MACHAMP_CAVERN_BATTLE.value,
                                requirements=Requirements(
                                    unlock_names=["Machamp Unlock"],
                                    powers=PowerRequirement.can_battle
                                )),
                       Location(name="Teddiursa",
                                id=OverworldPokemonLocationIds.TEDDIURSA_CAVERN.value),
                       Location(name="Meowth",
                                id=FRIENDSHIP_ITEMS["Meowth"]),
                       Location(name="Bonsly",
                                id=OverworldPokemonLocationIds.BONSLY_CAVERN.value),
                       Location(name="Chimchar",
                                id=OverworldPokemonLocationIds.CHIMCHAR_CAVERN.value,
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle
                                )),
                       Location(name="Cranidos",
                                id=FRIENDSHIP_ITEMS["Cranidos"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle
                                )),
                       Location(name="Zubat",
                                id=FRIENDSHIP_ITEMS["Zubat"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_play_catch
                                )),
                       Location(name="Golbat",
                                id=FRIENDSHIP_ITEMS["Golbat"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_play_catch_intermediate
                                )),
                       Location(name="Sudowoodo",
                                id=OverworldPokemonLocationIds.SUDOWOODO_CAVERN.value,
                                requirements=Requirements(
                                    unlock_names=["Sudowoodo Unlock"])),
                       Location(name="Scizor",
                                id=FRIENDSHIP_ITEMS["Scizor"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle
                                )),
                       # Location(name="Mawile", # story only
                       #          id=FRIENDSHIP_ITEMS["Mawile"],
                       #          requirements=Requirements(
                       #              powers=PowerRequirement.can_play_catch #? unsure if dash alone is enough needs testing
                       #          )),
                       Location(name="Marowak",
                                id=FRIENDSHIP_ITEMS["Marowak"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle_thunderbolt_immune
                                )),
                       Location(name="Aron",
                                id=FRIENDSHIP_ITEMS["Aron"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_destroy_objects_overworld
                                )),
                       Location(name="Dugtrio",
                                id=FRIENDSHIP_ITEMS["Dugtrio"]),
                       Location(name="Gible",
                                id=FRIENDSHIP_ITEMS["Gible"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle_thunderbolt_immune
                                )),
                       Location(name="Phanpy",
                                id=FRIENDSHIP_ITEMS["Phanpy"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_destroy_objects_overworld,
                                    unlock_names=["Phanpy Unlock"]
                                )),
                       Location(name="Raichu",
                                id=FRIENDSHIP_ITEMS["Raichu"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_play_catch_intermediate,
                                    unlock_names=["Raichu Unlock"]
                                )),
                       Location(name="Hitmonlee",
                                id=FRIENDSHIP_ITEMS["Hitmonlee"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle,
                                    unlock_names=["Hitmonlee Unlock"]
                                )),
                   ],
                   unlock_location=[
                       Location(name="Magnemite Crate Dash Entrance Area",
                                id=UNLOCK_ITEMS["Magnemite Unlock"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_destroy_objects_overworld
                                )),
                       Location(name="Magnemite Crate Dash Magma Zone Entrance",
                                id=UNLOCK_ITEMS["Magnemite Unlock 2"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_destroy_objects_overworld
                                )),
                       Location(name="Magnemite Crate Dash Deep Inside",
                                id=UNLOCK_ITEMS["Magnemite Unlock 3"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_destroy_objects_overworld
                                )),
                       Location(name="Machamp Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Machamp Unlock"],
                                requirements=Requirements(
                                    can_reach_locations=["Cavern Zone - Overworld - Machamp"])),
                       Location(name="Bonsly Friendship - Pokemon Unlock",
                                id=UnlockLocationIds.SUDOWOODO_CAVERN.value,
                                requirements=Requirements(
                                    can_reach_locations=["Cavern Zone - Overworld - Bonsly"])),
                       Location(name="Diglett Crate Dash",
                                id=UNLOCK_ITEMS["Diglett Unlock"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_destroy_objects_overworld
                                )),
                   ],
                   quest_locations=[

                   ],
                   parent_regions=["Treehouse"]),
PokeparkRegion(name="Cavern Zone - Bastiodon's Panel Crush",
                   display="Cavern Zone - Bastiodon's Panel Crush",
               requirements=Requirements(
                   friendcount=50),
                   minigame_location=[Location(name="Prisma",
                                               id=PRISM_ITEM["Bastiodon Prisma"]),

                                      Location(name="Pikachu",
                                               id=MinigameLocationIds.PIKACHU_PANEL.value),
                                      # Location(name="Sableye",
                                      #          id=MinigameLocationIds.SABLEYE_PANEL.value,
                                      #          requirements=Requirements(
                                      #              friendship_names=["Sableye"])),
                                      Location(name="Meowth",
                                               id=MinigameLocationIds.MEOWTH_PANEL.value,
                                               requirements=Requirements(
                                                   friendship_names=["Meowth"])),
                                      Location(name="Torchic",
                                               id=MinigameLocationIds.TORCHIC_PANEL.value,
                                               requirements=Requirements(
                                                   friendship_names=["Torchic"])),
                                      # Location(name="Electivire",
                                      #          id=MinigameLocationIds.ELECTIVIRE_PANEL.value,
                                      #          requirements=Requirements(
                                      #              friendship_names=["Electivire"])),
                                      # Location(name="Magmortar",
                                      #           id=MinigameLocationIds.MAGMORTAR_PANEL.value,
                                      #           requirements=Requirements(
                                      #               friendship_names=["Magmortar"])),
                                       Location(name="Hitmonlee",
                                                id=MinigameLocationIds.HITMONLEE_PANEL.value,
                                                requirements=Requirements(
                                                    friendship_names=["Hitmonlee"])),
                                      Location(name="Ursaring",
                                               id=MinigameLocationIds.URSARING_PANEL.value,
                                               requirements=Requirements(
                                                   friendship_names=["Ursaring"])),
                                      Location(name="Mr. Mime",
                                               id=MinigameLocationIds.MRMIME_PANEL.value,
                                               requirements=Requirements(
                                                   friendship_names=["Mr. Mime"])),
                                      Location(name="Raichu",
                                               id=MinigameLocationIds.RAICHU_PANEL.value,
                                               requirements=Requirements(
                                                   friendship_names=["Raichu"])),
                                      Location(name="Sudowoodo",
                                               id=MinigameLocationIds.SUDOWOODO_PANEL.value,
                                               requirements=Requirements(
                                                   friendship_names=["Sudowoodo"])),
                                      Location(name="Charmander",
                                                id=MinigameLocationIds.CHARMANDER_PANEL.value,
                                                requirements=Requirements(
                                                   friendship_names=["Charmander"])),
                                      Location(name="Gible",
                                               id=MinigameLocationIds.GIBLE_PANEL.value,
                                               requirements=Requirements(
                                                   friendship_names=["Gible"])),
                                      Location(name="Chimchar",
                                               id=MinigameLocationIds.CHIMCHAR_PANEL.value,
                                               requirements=Requirements(
                                                   friendship_names=["Chimchar"])),
                                      Location(name="Magby",
                                                id=MinigameLocationIds.MAGBY_PANEL.value,
                                                requirements=Requirements(
                                                    friendship_names=["Magby"])),
                                      ],
                   parent_regions=["Cavern Zone - Overworld"]),
    PokeparkRegion(name="Magma Zone - Overworld",
                   display="Magma Zone - Overworld",
                   requirements=Requirements(
                       unlock_names=["Cavern Zone & Magma Zone Unlock"]),
                   friendship_locations=[
                       Location(name="Aron",
                                id=OverworldPokemonLocationIds.ARON_MAGMA.value,
                                requirements=Requirements(
                                    powers=PowerRequirement.can_dash_overworld
                                )),
                       Location(name="Torchic",
                                id=OverworldPokemonLocationIds.TORCHIC_MAGMA.value,
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle
                                )),
                       Location(name="Chimchar",
                                id=OverworldPokemonLocationIds.CHIMCHAR_MAGMA.value,
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle
                                )),
                       Location(name="Geodude",
                                id=OverworldPokemonLocationIds.GEODUDE_MAGMA.value),
                       Location(name="Bonsly",
                                id=OverworldPokemonLocationIds.BONSLY_MAGMA.value),
                       Location(name="Camerupt",
                                id=FRIENDSHIP_ITEMS["Camerupt"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle_thunderbolt_immune
                                )),
                       Location(name="Magby",
                                id=FRIENDSHIP_ITEMS["Magby"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_play_catch
                                )),
                       Location(name="Magby - Battle",
                                id=OverworldPokemonLocationIds.MAGBY_MAGMA_BATTLE.value,
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle
                                )),
                       Location(name="Vulpix",
                                id=FRIENDSHIP_ITEMS["Vulpix"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_play_catch
                                )),
                       Location(name="Ninetales",
                                id=FRIENDSHIP_ITEMS["Ninetales"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_play_catch_intermediate,
                                    unlock_names=["Ninetales Unlock"]
                                )),
                       Location(name="Quilava",
                                id=FRIENDSHIP_ITEMS["Quilava"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle
                                )),
                       Location(name="Flareon",
                                id=FRIENDSHIP_ITEMS["Flareon"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle,
                                    friendcount=61
                                )),
                       Location(name="Infernape",
                                id=FRIENDSHIP_ITEMS["Infernape"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle,
                                    unlock_names=["Infernape Unlock"]
                                )),
                       Location(name="Farfetch'd",
                                id=FRIENDSHIP_ITEMS["Farfetch'd"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle
                                )),
                       Location(name="Ponyta",
                                id=FRIENDSHIP_ITEMS["Ponyta"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_play_catch_intermediate,
                                    unlock_names=["Ponyta Unlock"]
                                )),
                       Location(name="Torkoal",
                                id=FRIENDSHIP_ITEMS["Torkoal"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle,
                                    unlock_names=["Torkoal Unlock"]
                                )),
                       Location(name="Golem",
                                id=FRIENDSHIP_ITEMS["Golem"],
                                requirements=Requirements(
                                    unlock_names=["Golem Unlock"]
                                )),
                       Location(name="Baltoy",
                                id=FRIENDSHIP_ITEMS["Baltoy"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle_thunderbolt_immune,
                                    unlock_names=["Baltoy Unlock"]
                                )),
                       Location(name="Claydol",
                                id=FRIENDSHIP_ITEMS["Claydol"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle_thunderbolt_immune,
                                    unlock_names=["Claydol Unlock"]
                                )),
                       Location(name="Hitmonchan",
                                id=FRIENDSHIP_ITEMS["Hitmonchan"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_battle,
                                    unlock_names=["Hitmonchan Unlock"]
                                )),
                       Location(name="Hitmontop",
                                id=FRIENDSHIP_ITEMS["Hitmontop"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_dash_overworld,
                                )),
                   ],
                   unlock_location=[
                       Location(name="Chimchar Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Infernape Unlock"],
                                requirements=Requirements(
                                    can_reach_locations=["Magma Zone - Overworld - Chimchar"])),
                       Location(name="Vulpix Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Ninetales Unlock"],
                                requirements=Requirements(
                                    can_reach_locations=["Magma Zone - Overworld - Vulpix"])),
                       Location(name="Baltoy Crate Dash",
                                id=UNLOCK_ITEMS["Baltoy Unlock"],
                                requirements=Requirements(
                                    powers=PowerRequirement.can_destroy_objects_overworld
                                )),
                       Location(name="Baltoy Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Claydol Unlock"],
                                requirements=Requirements(
                                    can_reach_locations=["Magma Zone - Overworld - Baltoy"])),
                       Location(name="Hitmonchan Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Hitmonlee Unlock"],
                                requirements=Requirements(
                                    can_reach_locations=["Magma Zone - Overworld - Hitmonchan"])),
                   ],
                   quest_locations=[
                       Location(name="Meditite Quiz",
                                id=QuestLocationIds.MEDITITE_QUIZ.value),
                       Location(name="Rhyperior Iron Disc",
                                id=QuestLocationIds.RHYPERIOR_DISC.value,
                                requirements=Requirements(
                                        powers=PowerRequirement.can_dash_overworld
                                    )),
                   ],
                   parent_regions=["Cavern Zone - Overworld", "Treehouse"]),
PokeparkRegion(name="Magma Zone - Rhyperior's Bumper Burn",
                   display="Magma Zone - Rhyperior's Bumper Burn",
               requirements=Requirements(
                   can_reach_locations=["Magma Zone - Overworld - Rhyperior Iron Disc"]),
                   minigame_location=[Location(name="Prisma",
                                               id=PRISM_ITEM["Rhyperior Prisma"]),

                                      Location(name="Pikachu",
                                               id=MinigameLocationIds.PIKACHU_BUMPER.value),
                                      Location(name="Magnemite",
                                                id=MinigameLocationIds.MAGNEMITE_BUMPER.value,
                                                requirements=Requirements(
                                                    friendship_names=["Magnemite"])),
                                      Location(name="Rhyperior",
                                               id=MinigameLocationIds.RHYPERIOR_BUMPER.value,
                                               requirements=Requirements(
                                                   friendship_names=["Rhyperior"])),
                                      # Location(name="Tyranitar",
                                      #          id=MinigameLocationIds.TYRANITAR_BUMPER.value,
                                      #          requirements=Requirements(
                                      #              friendship_names=["Tyranitar"])),
                                      Location(name="Hitmontop",
                                                id=MinigameLocationIds.HITMONTOP_BUMPER.value,
                                                requirements=Requirements(
                                                    friendship_names=["Hitmontop"])),
                                      Location(name="Flareon",
                                                 id=MinigameLocationIds.FLAREON_BUMPER.value,
                                                 requirements=Requirements(
                                                    friendship_names=["Flareon"])),
                                      Location(name="Venusaur",
                                                id=MinigameLocationIds.VENUSAUR_BUMPER.value,
                                                requirements=Requirements(
                                                    friendship_names=["Venusaur"])),
                                      # Location(name="Snorlax",
                                      #          id=MinigameLocationIds.SNORLAX_BUMPER.value,
                                      #          requirements=Requirements(
                                      #              friendship_names=["Snorlax"])),
                                      Location(name="Torterra",
                                               id=MinigameLocationIds.TORTERRA_BUMPER.value,
                                               requirements=Requirements(
                                                   friendship_names=["Torterra"])),
                                      Location(name="Magnezone",
                                               id=MinigameLocationIds.MAGNEZONE_BUMPER.value,
                                               requirements=Requirements(
                                                   friendship_names=["Magnezone"])),
                                      Location(name="Claydol",
                                               id=MinigameLocationIds.CLAYDOL_BUMPER.value,
                                               requirements=Requirements(
                                                   friendship_names=["Claydol"])),
                                      Location(name="Quilava",
                                                id=MinigameLocationIds.QUILAVA_BUMPER.value,
                                                requirements=Requirements(
                                                    friendship_names=["Quilava"])),
                                      Location(name="Torkoal",
                                               id=MinigameLocationIds.TORKOAL_BUMPER.value,
                                               requirements=Requirements(
                                                   friendship_names=["Torkoal"])),
                                      Location(name="Baltoy",
                                               id=MinigameLocationIds.BALTOY_BUMPER.value,
                                               requirements=Requirements(
                                                   friendship_names=["Baltoy"])),
                                      Location(name="Bonsly",
                                                id=MinigameLocationIds.BONSLY_BUMPER.value,
                                                requirements=Requirements(
                                                    friendship_names=["Bonsly"])),
                                      ],
                   parent_regions=["Magma Zone - Overworld"]),

PokeparkRegion(name="Magma Zone - Blaziken's Boulder Bash",
                   display="Magma Zone - Blaziken's Boulder Bash",
                   minigame_location=[Location(name="Prisma",
                                               id=PRISM_ITEM["Blaziken Prisma"]),

                                      Location(name="Pikachu",
                                               id=MinigameLocationIds.PIKACHU_BOULDER.value),
                                      Location(name="Geodude",
                                                id=MinigameLocationIds.GEODUDE_BOULDER.value,
                                                requirements=Requirements(
                                                    friendship_names=["Geodude"])),
                                      Location(name="Phanpy",
                                               id=MinigameLocationIds.PHANPY_BOULDER.value,
                                               requirements=Requirements(
                                                   friendship_names=["Phanpy"])),
                                      # Location(name="Blaziken",
                                      #           id=MinigameLocationIds.BLAZIKEN_BOULDER.value,
                                      #           requirements=Requirements(
                                      #               friendship_names=["Blaziken"])),
                                      # Location(name="Garchomp",
                                      #           id=MinigameLocationIds.GARCHOMP_BOULDER.value,
                                      #           requirements=Requirements(
                                      #               friendship_names=["Garchomp"])),
                                      Location(name="Scizor",
                                                 id=MinigameLocationIds.SCIZOR_BOULDER.value,
                                                 requirements=Requirements(
                                                    friendship_names=["Scizor"])),
                                      # Location(name="Magmortar",
                                      #           id=MinigameLocationIds.MAGMORTAR_BOULDER.value,
                                      #           requirements=Requirements(
                                      #               friendship_names=["Magmortar"])),
                                      Location(name="Hitmonchan",
                                                id=MinigameLocationIds.HITMONCHAN_BOULDER.value,
                                                requirements=Requirements(
                                                    friendship_names=["Hitmonchan"])),
                                      Location(name="Machamp",
                                               id=MinigameLocationIds.MACHAMP_BOULDER.value,
                                               requirements=Requirements(
                                                   friendship_names=["Machamp"])),
                                      Location(name="Marowak",
                                               id=MinigameLocationIds.MAROWAK_BOULDER.value,
                                               requirements=Requirements(
                                                   friendship_names=["Marowak"])),
                                      Location(name="Farfetch'd",
                                               id=MinigameLocationIds.FARFETCHD_BOULDER.value,
                                               requirements=Requirements(
                                                   friendship_names=["Farfetch'd"])),
                                      Location(name="Cranidos",
                                                id=MinigameLocationIds.CRANIDOS_BOULDER.value,
                                                requirements=Requirements(
                                                    friendship_names=["Cranidos"])),
                                      Location(name="Camerupt",
                                               id=MinigameLocationIds.CAMERUPT_BOULDER.value,
                                               requirements=Requirements(
                                                   friendship_names=["Camerupt"])),
                                      Location(name="Bastiodon",
                                               id=MinigameLocationIds.BASTIODON_BOULDER.value,
                                               requirements=Requirements(
                                                   friendship_names=["Bastiodon"])),
                                      Location(name="Mawile",
                                                id=MinigameLocationIds.MAWILE_BOULDER.value,
                                                requirements=Requirements(
                                                    friendship_names=["Mawile"])),
                                      ],
                   parent_regions=["Magma Zone - Overworld"]),

    PokeparkRegion("Victory Region", "Victory Region",
                   Requirements(prisma_names=
                                ["Bulbasaur Prisma",
                                 "Venusaur Prisma",
                                 "Pelipper Prisma",
                                 "Gyarados Prisma",
                                 "Empoleon Prisma",
                                 "Bastiodon Prisma",
                                 "Rhyperior Prisma",
                                 "Blaziken Prisma"
                                 ]),
                   parent_regions=["Treehouse"])
    # just some Victory Requirements for Demo so that meadow zone can be tested
]
