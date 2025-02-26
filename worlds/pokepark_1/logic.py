from typing import NamedTuple

from worlds.pokepark_1 import FRIENDSHIP_ITEMS
from worlds.pokepark_1.LocationIds import MinigameLocationIds, QuestLocationIds, OverworldPokemonLocationIds
from worlds.pokepark_1.items import UNLOCK_ITEMS, PRISM_ITEM


class Requirements(NamedTuple):
    unlock_names: list[str] = []
    friendship_names: list[str] = []
    friendcount: int = 0
    prisma_names: list[str] = []
    oneof_item_names: list[list[str]] = []


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
    parent_region: str = "Menu"


REGIONS: list[PokeparkRegion] = [
    PokeparkRegion(name="Pokepark Entrance",
                   display="Pokepark Entrance"),

    PokeparkRegion(name="Meadow Zone - Overworld",
                   display="Meadow Zone - Overworld",
                   friendship_locations=[

                       Location(name="Bulbasaur",
                                id=FRIENDSHIP_ITEMS["Bulbasaur"],
                                requirements=Requirements(
                                    prisma_names=["Bulbasaur Prisma"])),

                       Location(name="Munchlax",
                                id=FRIENDSHIP_ITEMS["Munchlax"],
                                requirements=Requirements(
                                    prisma_names=["Bulbasaur Prisma"])),

                       Location(name="Tropius",
                                id=FRIENDSHIP_ITEMS["Tropius"],
                                requirements=Requirements(
                                    unlock_names=["Tropius Unlock"],
                                    prisma_names=["Bulbasaur Prisma"])),

                       Location(name="Turtwig",
                                id=FRIENDSHIP_ITEMS["Turtwig"]),

                       Location(name="Bonsly",
                                id=FRIENDSHIP_ITEMS["Bonsly"],
                                requirements=Requirements(
                                    unlock_names=["Bonsly Unlock"])),

                       Location(name="Pachirisu",
                                id=FRIENDSHIP_ITEMS["Pachirisu"],
                                requirements=Requirements(
                                    unlock_names=["Pachirisu Unlock"])),

                       Location(name="Sudowoodo",
                                id=FRIENDSHIP_ITEMS["Sudowoodo"],
                                requirements=Requirements(
                                    unlock_names=["Sudowoodo Unlock"])),

                       Location(name="Buneary",
                                id=FRIENDSHIP_ITEMS["Buneary"]),

                       Location(name="Shinx",
                                id=FRIENDSHIP_ITEMS["Shinx"],
                                requirements=Requirements(
                                    unlock_names=["Shinx Unlock"])),

                       Location(name="Spearow",
                                id=FRIENDSHIP_ITEMS["Spearow"]),

                       Location(name="Croagunk",
                                id=FRIENDSHIP_ITEMS["Croagunk"]),

                       Location(name="Lotad",
                                id=FRIENDSHIP_ITEMS["Lotad"],
                                requirements=Requirements(
                                    unlock_names=["Lotad Unlock"])),

                       Location(name="Treecko",
                                id=FRIENDSHIP_ITEMS["Treecko"]),

                       Location(name="Caterpie",
                                id=FRIENDSHIP_ITEMS["Caterpie"],
                                requirements=Requirements(
                                    unlock_names=["Caterpie Unlock"])),

                       Location(name="Butterfree",
                                id=FRIENDSHIP_ITEMS["Butterfree"],
                                requirements=Requirements(
                                    unlock_names=["Butterfree Unlock"])),

                       Location(name="Chimchar",
                                id=FRIENDSHIP_ITEMS["Chimchar"],
                                requirements=Requirements(
                                    unlock_names=["Chimchar Unlock"])),

                       Location(name="Aipom",
                                id=FRIENDSHIP_ITEMS["Aipom"]),

                       Location(name="Ambipom",
                                id=FRIENDSHIP_ITEMS["Ambipom"],
                                requirements=Requirements(
                                    unlock_names=["Ambipom Unlock"])),

                       Location(name="Weedle",
                                id=FRIENDSHIP_ITEMS["Weedle"],
                                requirements=Requirements(
                                    unlock_names=["Weedle Unlock"])),

                       Location(name="Shroomish",
                                id=FRIENDSHIP_ITEMS["Shroomish"],
                                requirements=Requirements(
                                    unlock_names=["Shroomish Unlock"])),

                       Location(name="Magikarp",
                                id=FRIENDSHIP_ITEMS["Magikarp"],
                                requirements=Requirements(
                                    unlock_names=["Magikarp Unlock"])),

                       Location(name="Oddish",
                                id=FRIENDSHIP_ITEMS["Oddish"]),

                       Location(name="Bidoof",
                                id=FRIENDSHIP_ITEMS["Bidoof"],
                                requirements=Requirements(
                                    friendship_names=["Mankey"])),

                       Location(name="Bibarel",
                                id=FRIENDSHIP_ITEMS["Bibarel"],
                                requirements=Requirements(
                                    unlock_names=["Bibarel Unlock"])),

                       Location(name="Leafeon",
                                id=FRIENDSHIP_ITEMS["Leafeon"],
                                requirements=Requirements(
                                    friendcount=21)),  # 21 Friend Requirement because Leafana itself is not counting

                       Location(name="Torterra",
                                id=FRIENDSHIP_ITEMS["Torterra"],
                                requirements=Requirements(
                                    unlock_names=["Torterra Unlock"])),

                       Location(name="Starly",
                                id=FRIENDSHIP_ITEMS["Starly"],
                                requirements=Requirements(
                                    oneof_item_names=[["Starly Unlock"], ["Starly Unlock 2"]])),

                       Location(name="Scyther",
                                id=FRIENDSHIP_ITEMS["Scyther"],
                                requirements=Requirements(
                                    unlock_names=["Scyther Unlock"]))
                   ],
                   unlock_location=[
                       Location(name="Munchlax Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Tropius Unlock"],
                                requirements=Requirements(
                                    prisma_names=["Bulbasaur Prisma"])),

                       Location(name="Turtwig Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Pachirisu Unlock"]),

                       Location(name="Bonsly Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Sudowoodo Unlock"],
                                requirements=Requirements(
                                    unlock_names=["Bonsly Unlock"])),

                       Location(name="Buneary Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Lotad Unlock"]),

                       Location(name="Croagunk Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Scyther Unlock"]),

                       Location(name="Caterpie Tree Dash",
                                id=UNLOCK_ITEMS["Caterpie Unlock"]),

                       Location(name="Caterpie Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Butterfree Unlock"],
                                requirements=Requirements(
                                    unlock_names=["Caterpie Unlock"])),

                       Location(name="Aipom Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Ambipom Unlock"]),

                       Location(name="Weedle Tree Dash",
                                id=UNLOCK_ITEMS["Weedle Unlock"]),

                       Location(name="Shroomish Crate Dash",
                                id=UNLOCK_ITEMS["Shroomish Unlock"]),

                       Location(name="Magikarp electrocuted",
                                id=UNLOCK_ITEMS["Magikarp Unlock"]),

                       Location(name="Bidoof Housing 1 - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Bidoof Unlock"],
                                requirements=Requirements(
                                    friendship_names=["Mankey"])),

                       Location(name="Bidoof Housing 2 - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Bidoof Unlock 2"],
                                requirements=Requirements(
                                    friendship_names=["Mankey"])),

                       Location(name="Bidoof Housing 3 - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Bidoof Unlock 3"],
                                requirements=Requirements(
                                    friendship_names=["Mankey"])),

                       Location(name="Bidoof Housing 4 - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Bibarel Unlock"],
                                requirements=Requirements(
                                    friendship_names=["Mankey"])),
                   ],
                   quest_locations=[
                       Location(name="Bidoof Housing 1",
                                id=QuestLocationIds.MEADOW_BIDOOF_HOUSING1.value,
                                requirements=Requirements(
                                    friendship_names=["Mankey"])),

                       Location(name="Bidoof Housing 2",
                                id=QuestLocationIds.MEADOW_BIDOOF_HOUSING2.value,
                                requirements=Requirements(
                                    friendship_names=["Mankey"])),

                       Location(name="Bidoof Housing 3",
                                id=QuestLocationIds.MEADOW_BIDOOF_HOUSING3.value,
                                requirements=Requirements(
                                    friendship_names=["Mankey"])),

                       Location(name="Bidoof Housing 4",
                                id=QuestLocationIds.MEADOW_BIDOOF_HOUSING4.value,
                                requirements=Requirements(
                                    friendship_names=["Mankey"])),
                   ],
                   parent_region="Pokepark Entrance"),

    PokeparkRegion(name="Treehouse",
                   display="Treehouse",
                   quest_locations=[
                       Location(name="Thunderbolt Upgrade 1",
                                id=QuestLocationIds.THUNDERBOLT_POWERUP1.value),

                       Location(name="Thunderbolt Upgrade 2",
                                id=QuestLocationIds.THUNDERBOLT_POWERUP2.value),

                       Location(name="Thunderbolt Upgrade 3",
                                id=QuestLocationIds.THUNDERBOLT_POWERUP3.value),
                       Location(name="Dash Upgrade 1",
                                id=QuestLocationIds.DASH_POWERUP1.value,
                                requirements=Requirements(
                                    prisma_names=["Pelipper Prisma"])),

                       Location(name="Dash Upgrade 2",
                                id=QuestLocationIds.DASH_POWERUP2.value,
                                requirements=Requirements(
                                    prisma_names=["Pelipper Prisma"])),

                       Location(name="Dash Upgrade 3",
                                id=QuestLocationIds.DASH_POWERUP3.value,
                                requirements=Requirements(
                                    prisma_names=["Pelipper Prisma"])),

                       Location(name="Health Upgrade 1",
                                id=QuestLocationIds.HEALTH_POWERUP1.value,
                                requirements=Requirements(
                                    unlock_names=["Beach Zone Unlock"])),

                       Location(name="Health Upgrade 2",
                                id=QuestLocationIds.HEALTH_POWERUP2.value,
                                requirements=Requirements(
                                    unlock_names=["Beach Zone Unlock"])),

                       Location(name="Health Upgrade 3",
                                id=QuestLocationIds.HEALTH_POWERUP3.value,
                                requirements=Requirements(
                                    unlock_names=["Beach Zone Unlock"]))
                   ],
                   parent_region="Meadow Zone - Overworld"),

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

                       # Location(name="Ponyta",
                       #          id=MinigameLocationIds.PONYTA_DASH.value,
                       #          requirements=Requirements(
                       #              friendship_names=["Ponyta"])), #not implemented yet

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

                   ], parent_region="Meadow Zone - Overworld"),

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

                       # Location(name="Infernape",
                       #          id=MinigameLocationIds.INFERNAPE_VINE_SWING.value,
                       #          requirements=Requirements(
                       #              friendship_names=["Infernape"])),

                       # Location(name="Lucario",
                       #          id=MinigameLocationIds.LUCARIO_VINE_SWING.value,
                       #          requirements=Requirements(
                       #              friendship_names= ["Lucario"])),

                       # Location(name="Primeape",
                       #          id=MinigameLocationIds.PRIMEAPE_VINE_SWING.value,
                       #          requirements=Requirements(
                       #              friendship_names=["Primeape"])),

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

                   ], parent_region="Meadow Zone - Overworld"),

    PokeparkRegion(name="Beach Zone - Overworld",
                   display="Beach Zone - Overworld",
                   requirements=Requirements(
                       unlock_names=["Beach Zone Unlock"]),
                   friendship_locations=[
                       Location(name="Buizel",
                                id=FRIENDSHIP_ITEMS["Buizel"]),

                       Location(name="Psyduck",
                                id=FRIENDSHIP_ITEMS["Psyduck"]),

                       Location(name="Slowpoke",
                                id=FRIENDSHIP_ITEMS["Slowpoke"]),

                       Location(name="Azurill",
                                id=FRIENDSHIP_ITEMS["Azurill"]),

                       Location(name="Totodile",
                                id=FRIENDSHIP_ITEMS["Totodile"],
                                requirements=Requirements(
                                    unlock_names=["Totodile Unlock"])),

                       Location(name="Mudkip",
                                id=FRIENDSHIP_ITEMS["Mudkip"],
                                requirements=Requirements(
                                    unlock_names=["Mudkip Unlock"])),

                       Location(name="Pidgeotto",
                                id=FRIENDSHIP_ITEMS["Pidgeotto"]),

                       Location(name="Taillow",
                                id=FRIENDSHIP_ITEMS["Taillow"]),

                       Location(name="Wingull",
                                id=FRIENDSHIP_ITEMS["Wingull"]),

                       Location(name="Staravia",
                                id=FRIENDSHIP_ITEMS["Staravia"]),

                       Location(name="Corsola",
                                id=FRIENDSHIP_ITEMS["Corsola"]),

                       Location(name="Floatzel",
                                id=FRIENDSHIP_ITEMS["Floatzel"],
                                requirements=Requirements(
                                    unlock_names=["Floatzel Unlock"])),

                       Location(name="Vaporeon",
                                id=FRIENDSHIP_ITEMS["Vaporeon"],
                                requirements=Requirements(friendcount=31)),  # +1 for itself

                       Location(name="Golduck",
                                id=FRIENDSHIP_ITEMS["Golduck"],
                                requirements=Requirements(
                                    unlock_names=["Golduck Unlock"])),

                       Location(name="Krabby",
                                id=FRIENDSHIP_ITEMS["Krabby"],
                                requirements=Requirements(
                                    unlock_names=["Krabby Unlock"])),

                       Location(name="Wailord",
                                id=FRIENDSHIP_ITEMS["Wailord"]),

                       Location(name="Corphish",
                                id=FRIENDSHIP_ITEMS["Corphish"],
                                requirements=Requirements(
                                    unlock_names=["Corphish Unlock"])),

                       Location(name="Feraligatr",
                                id=FRIENDSHIP_ITEMS["Feraligatr"]),

                       Location(name="Starly",
                                id=OverworldPokemonLocationIds.STARLY_BEACH.value),

                   ],
                   unlock_location=[
                       Location(name="Buizel Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Floatzel Unlock"]),

                       Location(name="Psyduck Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Golduck Unlock"]),

                       Location(name="Slowpoke Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Mudkip Unlock"]),

                       Location(name="Azurill Friendship - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Totodile Unlock"]),

                       Location(name="Bottle Recycling 2 - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Krabby Unlock"]),

                       Location(name="Bottle Recycling 4 - Pokemon Unlock",
                                id=UNLOCK_ITEMS["Corphish Unlock"]),
                   ],
                   quest_locations=[
                       Location(name="Bottle Recycling 1",
                                id=QuestLocationIds.BEACH_BOTTLE1.value),

                       Location(name="Bottle Recycling 2",
                                id=QuestLocationIds.BEACH_BOTTLE2.value),

                       Location(name="Bottle Recycling 3",
                                id=QuestLocationIds.BEACH_BOTTLE3.value),

                       Location(name="Bottle Recycling 4",
                                id=QuestLocationIds.BEACH_BOTTLE4.value),

                       Location(name="Bottle Recycling 5",
                                id=QuestLocationIds.BEACH_BOTTLE5.value),

                       Location(name="Bottle Recycling 6",
                                id=QuestLocationIds.BEACH_BOTTLE6.value),
                   ],
                   parent_region="Treehouse"),

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

                   ], parent_region="Beach Zone - Overworld"),

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

                       # Location(name="Empoleon",
                       #          id=MinigameLocationIds.EMPOLEON_AQUA.value,
                       #          requirements=Requirements(
                       #              friendship_names=["Empoleon"])), # Empoleon missing

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

                       # Location(name="Prinplup",
                       #          id=MinigameLocationIds.PRINPLUP_AQUA.value,
                       #          requirements=Requirements(
                       #              friendship_names=["Prinplup"])),

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
                   parent_region="Beach Zone - Overworld"),

    PokeparkRegion("Victory Region", "Victory Region",
                   Requirements(prisma_names=
                                ["Bulbasaur Prisma",
                                 "Venusaur Prisma",
                                 "Pelipper Prisma",
                                 "Gyarados Prisma"
                                 ]),
                   parent_region="Beach Zone - Overworld")
    # just some Victory Requirements for Demo so that meadow zone can be tested
]
