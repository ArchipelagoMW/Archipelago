from typing import Callable, List, TYPE_CHECKING

from BaseClasses import CollectionState

if TYPE_CHECKING:
    from worlds.pokepark import PokeparkWorld
from worlds.pokepark.rules import can_battle, can_battle_intermediate, can_battle_thunderbolt_immune_advanced, \
    can_battle_thunderbolt_immune_intermediate, \
    can_dash_overworld, \
    can_destroy_objects_overworld, can_farm_berries, \
    can_play_catch, \
    can_play_catch_intermediate

REGION_TO_ENTRANCES: dict[str, List[str]] = {
    "Treehouse": [
        "Treehouse Meadow Zone Gate",
        "Treehouse Drifblim Fast Travel Meadow Zone",
        "Treehouse Beach Zone Gate",
        "Treehouse Drifblim Fast Travel Beach Zone", "Treehouse Drifblim Fast Travel Ice Zone",
        "Treehouse Cavern Zone Gate", "Treehouse Drifblim Fast Travel Cavern Zone",
        "Treehouse Drifblim Fast Travel Magma Zone",
        "Treehouse Haunted Zone Gate",
        "Treehouse Drifblim Fast Travel Haunted Zone",
        "Treehouse Granite Zone Gate",
        "Treehouse Drifblim Fast Travel Granite Zone",
        "Treehouse Drifblim Fast Travel Flower Zone",
        "Treehouse Piplup Air Balloon",
    ],
    "Meadow Zone Main Area": [
        "Meadow Zone Main Area - Bulbasaur's Daring Dash Attraction",
        "Meadow Zone Main Area - Venusaur's Gate",
    ],
    "Meadow Zone Venusaur Area": ["Meadow Zone Venusaur Area - Venusaur's Vine Swing Attraction"],
    "Beach Zone Main Area": ["Beach Zone Main Area - Pelipper's Circle Circuit Attraction",
                             "Beach Zone Main Area Lapras Travel", "Beach Zone Bridge 2", "Beach Zone Bridge 1"],
    "Beach Zone Recycle Area": ["Beach Zone Recycle Area - Gyarados' Aqua Dash Attraction"],
    "Ice Zone Main Area": ["Ice Zone Main Area Lift", "Ice Zone Main Area Empoleon Gate", "Ice Zone Frozen Lake"],
    "Ice Zone Empoleon Area": ["Ice Zone Empoleon Area - Empoleon's Snow Slide Attraction"],
    "Cavern Zone Main Area": ["Cavern Zone Main Area - Bastiodon's Panel Crush Attraction",
                              "Cavern Zone Magma Zone Gate"],
    "Magma Zone Main Area": ["Magma Zone Fire Wall"],
    "Magma Zone Circle Area": ["Magma Zone Blaziken Gate",
                               "Magma Zone Circle Area - Rhyperior's Bumper Burn Attraction"],
    "Magma Zone Blaziken Area": ["Magma Zone Blaziken Area - Blaziken's Boulder Bash Attraction"],
    "Haunted Zone Main Area": ["Haunted Zone Main Area - Tangrowth's Swing-Along Attraction",
                               "Haunted Zone Mansion Entrance", "Haunted Zone Main Area Riolu",
                               "Haunted Zone Main Area Drifloon"],
    "Haunted Zone Mansion Area": ["Haunted Zone Mansion Area - Dusknoir's Speed Slam Attraction",
                                  "Haunted Zone Mansion White Gem Door",
                                  "Haunted Zone Mansion Red Gem Door",
                                  "Haunted Zone Mansion Blue Gem Door",
                                  "Haunted Zone Mansion Green Gem Door",
                                  "Haunted Zone Mansion Area Riolu"
                                  ],
    "Haunted Zone Mansion Ballroom Area": ["Haunted Zone Ballroom Area Drifloon"],
    "Haunted Zone Mansion Study Area": ["Haunted Zone Mansion Rotom's Hidden Entrance"],
    "Haunted Zone Rotom Area": ["Haunted Zone Rotom Area - Rotom's Spooky Shoot-'em-Up Attraction"],
    "Granite Zone Main Area": [
        "Granite Zone Main Area - Absol's Hurdle Bounce Attraction",
        "Granite Zone Flygon Door"
    ],
    "Granite Zone Salamence Area": ["Granite Zone Flower Zone Entrance",
                                    "Granite Zone Salamence Area - Salamence's Sky Race Attraction",
                                    ],
    "Flower Zone Main Area": [
        "Flower Zone Main Area - Rayquaza's Balloon Panic Attraction"
    ]
}

ADDITIONAL_REGION_TO_ENTRANCES: dict[str, List[str]] = {
    "Treehouse": [
        "Treehouse Abra"
    ],
    "Meadow Zone Main Area": [
        "Meadow Zone Spearow",
        "Meadow Zone Starly",
        "Meadow Zone Bonsly",
        "Meadow Zone Bonsly Unlocks",
        "Meadow Zone Chimchar",
        "Meadow Zone Sudowoodo",
        "Meadow Zone Aipom",
        "Meadow Zone Aipom Unlocks",
        "Meadow Zone Ambipom",
    ],
    "Beach Zone Main Area": [
        "Beach Zone Spearow",
        "Beach Zone Starly",
        "Beach Zone Krabby",
        "Beach Zone Mudkip",
        "Beach Zone Taillow",
        "Beach Zone Staravia",
        "Beach Zone Wingull",
        "Beach Zone Corphish",
    ],
    "Ice Zone Main Area": [
        "Ice Zone Starly",
        "Ice Zone Krabby",
        "Ice Zone Mudkip",
        "Ice Zone Taillow",
        "Ice Zone Staravia",
        "Ice Zone Teddiursa"
    ],
    "Ice Zone Lower Lift Area": [
        "Ice Zone Wingull",
        "Ice Zone Corphish"
    ],
    "Cavern Zone Main Area": [
        "Cavern Zone Bonsly",
        "Cavern Zone Bonsly Unlocks",
        "Cavern Zone Chimchar",
        "Cavern Zone Sudowoodo",
        "Cavern Zone Teddiursa",
        "Cavern Zone Aron",
        "Cavern Zone Torchic",
        "Cavern Zone Geodude",
        "Cavern Zone Raichu",
        "Cavern Zone Meowth",
        "Cavern Zone Marowak",

    ],
    "Magma Zone Main Area": [
        "Magma Zone Bonsly",
        "Magma Zone Chimchar",
        "Magma Zone Aron",
        "Magma Zone Torchic",
        "Magma Zone Geodude",
        "Magma Zone Baltoy",
        "Magma Zone Baltoy Unlocks",
        "Magma Zone Meditite",
        "Magma Zone Claydol"

    ],
    "Haunted Zone Main Area": [
        "Haunted Zone Aipom",
        "Haunted Zone Aipom Unlocks",
        "Haunted Zone Ambipom",
        "Haunted Zone Raichu",
        "Haunted Zone Meowth",
        "Haunted Zone Drifloon",
    ],
    "Haunted Zone Mansion Antic Area": [
        "Haunted Zone Abra"
    ],
    "Granite Zone Main Area": [
        "Granite Zone Marowak",
        "Granite Zone Baltoy",
        "Granite Zone Baltoy Unlocks",
        "Granite Zone Drifloon",
        "Granite Zone Furret",
        "Granite Zone Claydol"
    ],
    "Granite Zone Salamence Area": [
        "Granite Zone Taillow"
    ],
    "Flower Zone Main Area": [
        "Flower Zone Teddiursa",
        "Flower Zone Meditite",
        "Flower Zone Furret"
    ],
}

VANILLA_ENTRANCES_TO_EXITS: dict[str, str] = {
    "Treehouse Meadow Zone Gate": "Meadow Zone Main Area",
    "Treehouse Drifblim Fast Travel Meadow Zone": "Meadow Zone Main Area",
    "Meadow Zone Main Area - Venusaur's Gate": "Meadow Zone Venusaur Area",

    "Treehouse Beach Zone Gate": "Beach Zone Main Area",
    "Treehouse Drifblim Fast Travel Beach Zone": "Beach Zone Main Area",
    "Beach Zone Bridge 2": "Beach Zone Recycle Area",
    "Beach Zone Bridge 1": "Beach Zone Middle Isle",

    "Beach Zone Main Area Lapras Travel": "Ice Zone Main Area",
    "Treehouse Drifblim Fast Travel Ice Zone": "Ice Zone Main Area",
    "Ice Zone Main Area Lift": "Ice Zone Lower Lift Area",
    "Ice Zone Frozen Lake": "Ice Zone Frozen Lake Area",
    "Ice Zone Main Area Empoleon Gate": "Ice Zone Empoleon Area",

    "Treehouse Cavern Zone Gate": "Cavern Zone Main Area",
    "Treehouse Drifblim Fast Travel Cavern Zone": "Cavern Zone Main Area",

    "Cavern Zone Magma Zone Gate": "Magma Zone Main Area",
    "Treehouse Drifblim Fast Travel Magma Zone": "Magma Zone Main Area",
    "Magma Zone Blaziken Gate": "Magma Zone Blaziken Area",
    "Magma Zone Fire Wall": "Magma Zone Circle Area",

    "Treehouse Haunted Zone Gate": "Haunted Zone Main Area",
    "Treehouse Drifblim Fast Travel Haunted Zone": "Haunted Zone Main Area",
    "Haunted Zone Mansion Entrance": "Haunted Zone Mansion Area",
    "Haunted Zone Mansion White Gem Door": "Haunted Zone Mansion Ballroom Area",
    "Haunted Zone Mansion Red Gem Door": "Haunted Zone Mansion Study Area",
    "Haunted Zone Mansion Blue Gem Door": "Haunted Zone Mansion Gengar Area",
    "Haunted Zone Mansion Green Gem Door": "Haunted Zone Mansion Antic Area",
    "Haunted Zone Mansion Rotom's Hidden Entrance": "Haunted Zone Rotom Area",

    "Treehouse Granite Zone Gate": "Granite Zone Main Area",
    "Treehouse Drifblim Fast Travel Granite Zone": "Granite Zone Main Area",
    "Granite Zone Flygon Door": "Granite Zone Salamence Area",

    "Granite Zone Flower Zone Entrance": "Flower Zone Main Area",
    "Treehouse Drifblim Fast Travel Flower Zone": "Flower Zone Main Area",

    "Treehouse Piplup Air Balloon": "Skygarden",

    "Haunted Zone Main Area Riolu": "Riolu",
    "Haunted Zone Mansion Area Riolu": "Riolu",
    "Haunted Zone Main Area Drifloon": "Drifloon",
    "Haunted Zone Ballroom Area Drifloon": "Drifloon",
}
ATTRACTION_ENTRANCES_TO_EXITS: dict[str, str] = {
    "Meadow Zone Main Area - Bulbasaur's Daring Dash Attraction": "Bulbasaur's Daring Dash Attraction",
    "Meadow Zone Venusaur Area - Venusaur's Vine Swing Attraction": "Venusaur's Vine Swing Attraction",
    "Beach Zone Main Area - Pelipper's Circle Circuit Attraction": "Pelipper's Circle Circuit Attraction",
    "Beach Zone Recycle Area - Gyarados' Aqua Dash Attraction": "Gyarados' Aqua Dash Attraction",
    "Ice Zone Empoleon Area - Empoleon's Snow Slide Attraction": "Empoleon's Snow Slide Attraction",
    "Cavern Zone Main Area - Bastiodon's Panel Crush Attraction": "Bastiodon's Panel Crush Attraction",
    "Magma Zone Circle Area - Rhyperior's Bumper Burn Attraction": "Rhyperior's Bumper Burn Attraction",
    "Magma Zone Blaziken Area - Blaziken's Boulder Bash Attraction": "Blaziken's Boulder Bash Attraction",
    "Haunted Zone Main Area - Tangrowth's Swing-Along Attraction": "Tangrowth's Swing-Along Attraction",
    "Haunted Zone Mansion Area - Dusknoir's Speed Slam Attraction": "Dusknoir's Speed Slam Attraction",
    "Haunted Zone Rotom Area - Rotom's Spooky Shoot-'em-Up Attraction": "Rotom's Spooky Shoot-'em-Up Attraction",
    "Granite Zone Main Area - Absol's Hurdle Bounce Attraction": "Absol's Hurdle Bounce Attraction",
    "Granite Zone Salamence Area - Salamence's Sky Race Attraction": "Salamence's Sky Race Attraction",
    "Flower Zone Main Area - Rayquaza's Balloon Panic Attraction": "Rayquaza's Balloon Panic Attraction",

}

ADDITIONAL_ENTRANCES_TO_EXITS: dict[str, str] = {
    "Treehouse Abra": "Abra",
    "Haunted Zone Abra": "Abra",

    "Meadow Zone Spearow": "Spearow",
    "Beach Zone Spearow": "Spearow",

    "Meadow Zone Starly": "Starly",
    "Beach Zone Starly": "Starly",
    "Ice Zone Starly": "Starly",

    "Meadow Zone Bonsly": "Bonsly",
    "Meadow Zone Bonsly Unlocks": "Bonsly Unlocks",
    "Cavern Zone Bonsly": "Bonsly",
    "Cavern Zone Bonsly Unlocks": "Bonsly Unlocks",
    "Magma Zone Bonsly": "Bonsly",

    "Meadow Zone Chimchar": "Chimchar",
    "Cavern Zone Chimchar": "Chimchar",
    "Magma Zone Chimchar": "Chimchar",

    "Meadow Zone Sudowoodo": "Sudowoodo",
    "Cavern Zone Sudowoodo": "Sudowoodo",

    "Meadow Zone Aipom": "Aipom",
    "Meadow Zone Aipom Unlocks": "Aipom Unlocks",
    "Haunted Zone Aipom": "Aipom",
    "Haunted Zone Aipom Unlocks": "Aipom Unlocks",

    "Meadow Zone Ambipom": "Ambipom",
    "Haunted Zone Ambipom": "Ambipom",

    "Beach Zone Krabby": "Krabby",
    "Ice Zone Krabby": "Krabby",

    "Beach Zone Mudkip": "Mudkip",
    "Ice Zone Mudkip": "Mudkip",

    "Beach Zone Taillow": "Taillow",
    "Ice Zone Taillow": "Taillow",
    "Granite Zone Taillow": "Taillow",

    "Beach Zone Staravia": "Staravia",
    "Ice Zone Staravia": "Staravia",

    "Beach Zone Wingull": "Wingull",
    "Ice Zone Wingull": "Wingull",

    "Beach Zone Corphish": "Corphish",
    "Ice Zone Corphish": "Corphish",

    "Ice Zone Teddiursa": "Teddiursa",
    "Cavern Zone Teddiursa": "Teddiursa",
    "Flower Zone Teddiursa": "Teddiursa",

    "Cavern Zone Aron": "Aron",
    "Magma Zone Aron": "Aron",

    "Cavern Zone Torchic": "Torchic",
    "Magma Zone Torchic": "Torchic",

    "Cavern Zone Geodude": "Geodude",
    "Magma Zone Geodude": "Geodude",

    "Cavern Zone Raichu": "Raichu",
    "Haunted Zone Raichu": "Raichu",

    "Cavern Zone Meowth": "Meowth",
    "Haunted Zone Meowth": "Meowth",

    "Cavern Zone Marowak": "Marowak",
    "Granite Zone Marowak": "Marowak",

    "Magma Zone Baltoy": "Baltoy",
    "Magma Zone Baltoy Unlocks": "Baltoy Unlocks",
    "Magma Zone Claydol": "Claydol",

    "Granite Zone Baltoy": "Baltoy",
    "Granite Zone Baltoy Unlocks": "Baltoy Unlocks",
    "Granite Zone Claydol": "Claydol",

    "Magma Zone Meditite": "Meditite",
    "Flower Zone Meditite": "Meditite",

    "Haunted Zone Drifloon": "Drifloon",
    "Granite Zone Drifloon": "Drifloon",

    "Granite Zone Furret": "Furret",
    "Flower Zone Furret": "Furret",

}


class EntranceRandomizer:
    def __init__(self, world: "PokeparkWorld"):
        self.world = world
        self.multiworld = world.multiworld
        self.player = world.player
        self.entrances_to_exits: dict[str, str] = {}
        self.region_to_entrances: dict[str, str] = {}
        self.entrances_rules: dict[str, Callable[[CollectionState], bool]] = {}

    def set_entrance_rules(self):
        player = self.player
        options = self.world.options
        ENTRANCE_RULES: dict[str, Callable[[CollectionState], bool]] = {
            "Treehouse Meadow Zone Gate": lambda state: True,
            "Treehouse Drifblim Fast Travel Meadow Zone": lambda state: state.has(
                "Meadow Zone Fast Travel",
                player
            ) and can_farm_berries(
                state,
                player
            ),
            "Meadow Zone Main Area - Bulbasaur's Daring Dash Attraction": lambda state: True,
            "Meadow Zone Main Area - Venusaur's Gate": lambda state: state.has("Bulbasaur Prisma", player),
            "Meadow Zone Venusaur Area - Venusaur's Vine Swing Attraction": lambda state: True,

            "Treehouse Beach Zone Gate": lambda state: state.has("Venusaur Prisma", player),
            "Treehouse Drifblim Fast Travel Beach Zone": lambda state: state.has(
                "Beach Zone Fast Travel", player
            ) and can_farm_berries(
                state,
                player
            ),
            "Beach Zone Main Area - Pelipper's Circle Circuit Attraction": lambda state: True,
            "Beach Zone Recycle Area - Gyarados' Aqua Dash Attraction": lambda state: True,
            "Beach Zone Bridge 2": lambda state: state.has("Beach Bridge 2 Unlock", player),
            "Beach Zone Middle Isle Bridge 2": lambda state: state.has("Beach Bridge 2 Unlock", player),
            "Beach Zone Bridge 1": lambda state: state.has("Beach Bridge 1 Unlock", player) or state.has(
                "Beach "
                "Bridge 2 "
                "Unlock", player
            ),

            "Beach Zone Main Area Lapras Travel": lambda state: state.has("Gyarados Prisma", player),
            "Treehouse Drifblim Fast Travel Ice Zone": lambda state: state.has(
                "Ice Zone Fast Travel", player
            ) and can_farm_berries(
                state,
                player
            ),
            "Ice Zone Main Area Lift": lambda state: state.has("Ice Zone Lift Unlock", player),
            "Ice Zone Frozen Lake": lambda state: state.has("Ice Zone Frozen Lake Unlock", player),
            "Ice Zone Main Area Empoleon Gate": lambda state: state.has("Gyarados Prisma", player),
            "Ice Zone Empoleon Area - Empoleon's Snow Slide Attraction": lambda state: True,

            "Treehouse Cavern Zone Gate": lambda state: state.has("Empoleon Prisma", player),
            "Treehouse Drifblim Fast Travel Cavern Zone": lambda state: state.has(
                "Cavern Zone Fast Travel", player
            ) and can_farm_berries(
                state,
                player
            ),
            "Cavern Zone Main Area - Bastiodon's Panel Crush Attraction": lambda state: state.count_group(
                "Friendship Items",
                player
            ) >= 50,

            "Cavern Zone Magma Zone Gate": lambda state: state.has("Bastiodon Prisma", player),
            "Treehouse Drifblim Fast Travel Magma Zone": lambda state: state.has(
                "Magma Zone Fast Travel", player
            ) and can_farm_berries(
                state,
                player
            ),
            "Magma Zone Circle Area - Rhyperior's Bumper Burn Attraction": lambda state: True,
            "Magma Zone Blaziken Gate": lambda state: state.has("Rhyperior Prisma", player),
            "Magma Zone Blaziken Area - Blaziken's Boulder Bash Attraction": lambda state: True,
            "Magma Zone Fire Wall": lambda state: state.has("Magma Zone Fire Wall Unlock", player),

            "Treehouse Haunted Zone Gate": lambda state: state.has("Blaziken Prisma", player),
            "Treehouse Drifblim Fast Travel Haunted Zone": lambda state: state.has(
                "Haunted Zone Fast Travel", player
            ) and can_farm_berries(
                state,
                player
            ),
            "Haunted Zone Main Area - Tangrowth's Swing-Along Attraction": lambda state: True,
            "Haunted Zone Mansion Entrance": lambda state: state.has("Tangrowth Prisma", player),
            "Haunted Zone Mansion Area - Dusknoir's Speed Slam Attraction": lambda state: state.has(
                "Dusknoir Unlock", player
            ),
            "Haunted Zone Mansion White Gem Door": lambda state: state.has("Haunted Zone Mansion Doors Unlock", player),
            "Haunted Zone Mansion Red Gem Door": lambda state: state.has("Haunted Zone Mansion Doors Unlock", player),
            "Haunted Zone Mansion Blue Gem Door": lambda state: state.has("Haunted Zone Mansion Doors Unlock", player),
            "Haunted Zone Mansion Green Gem Door": lambda state: state.has("Haunted Zone Mansion Doors Unlock", player),
            "Haunted Zone Mansion Rotom's Hidden Entrance": lambda state: state.has("Dusknoir Prisma", player),
            "Haunted Zone Rotom Area - Rotom's Spooky Shoot-'em-Up Attraction": lambda state: state.count_group(
                "Friendship Items",
                player
            ) >= 65,

            "Treehouse Granite Zone Gate": lambda state: state.has("Rotom Prisma", player),
            "Treehouse Drifblim Fast Travel Granite Zone": lambda state: state.has(
                "Granite Zone Fast Travel", player
            ) and can_farm_berries(
                state,
                player
            ),
            "Granite Zone Main Area - Absol's Hurdle Bounce Attraction": lambda state: True,
            "Granite Zone Flygon Door": lambda state: state.has("Absol Prisma", player),
            "Granite Zone Salamence Area - Salamence's Sky Race Attraction": lambda state: state.count_group(
                "Friendship Items",
                player
            ) >= 80,

            "Granite Zone Flower Zone Entrance": lambda state: True,
            "Treehouse Drifblim Fast Travel Flower Zone": lambda state: state.has(
                "Flower Zone Fast Travel", player
            ) and can_farm_berries(
                state,
                player
            ),
            "Flower Zone Main Area - Rayquaza's Balloon Panic Attraction": lambda state: state.has(
                "Rayquaza Unlock", player
            ),

            "Treehouse Piplup Air Balloon": lambda state: state.count_group("Prisma Items", player) >=
                                                          options.num_required_prisma_count_skygarden.value,
            #
            #
            #
            "Treehouse Abra": lambda state: True,
            "Haunted Zone Abra": lambda state: True,

            "Meadow Zone Spearow": lambda state: True,
            "Beach Zone Spearow": lambda state: True,

            "Meadow Zone Starly": lambda state: state.has("Starly Unlock", player) or state.has(
                "Starly 2 Unlock", player
            ),
            "Beach Zone Starly": lambda state: True,
            "Ice Zone Starly": lambda state: True,

            "Meadow Zone Bonsly": lambda state: state.has("Bonsly Unlock", player),
            "Meadow Zone Bonsly Unlocks": lambda state: state.has("Bonsly Unlock", player),
            "Cavern Zone Bonsly": lambda state: True,
            "Cavern Zone Bonsly Unlocks": lambda state: True,
            "Magma Zone Bonsly": lambda state: True,

            "Meadow Zone Chimchar": lambda state: state.has("Chimchar Unlock", player) and can_battle(
                state, player,
                options
            ),
            "Cavern Zone Chimchar": lambda state: can_battle_intermediate(
                state, player,
                options
            ),
            "Magma Zone Chimchar": lambda state: can_battle_intermediate(
                state, player,
                options
            ),

            "Meadow Zone Sudowoodo": lambda state: state.has("Sudowoodo Unlock", player),
            "Cavern Zone Sudowoodo": lambda state: state.has("Sudowoodo Unlock", player),

            "Meadow Zone Aipom": lambda state: can_play_catch(state, player, options),
            "Meadow Zone Aipom Unlocks": lambda state: can_play_catch(state, player, options),
            "Haunted Zone Aipom": lambda state: can_play_catch(state, player, options),
            "Haunted Zone Aipom Unlocks": lambda state: can_play_catch(state, player, options),

            "Haunted Zone Main Area Riolu": lambda state: True,
            "Haunted Zone Mansion Area Riolu": lambda state: True,

            "Haunted Zone Main Area Drifloon": lambda state: True,
            "Haunted Zone Ballroom Area Drifloon": lambda state: True,

            "Meadow Zone Ambipom": lambda state: state.has("Ambipom Unlock", player) and can_battle(
                state,
                player,
                options
            ),
            "Haunted Zone Ambipom": lambda state: state.has("Ambipom Unlock", player) and can_battle_intermediate(
                state,
                player,
                options
            ),

            "Beach Zone Krabby": lambda state: state.has("Krabby Unlock", player) and can_play_catch(
                state, player, options
            ),
            "Ice Zone Krabby": lambda state: state.has("Krabby Unlock", player) and can_play_catch(
                state, player, options
            ),

            "Beach Zone Mudkip": lambda state: state.has("Mudkip Unlock", player),
            "Ice Zone Mudkip": lambda state: state.has("Mudkip Unlock", player),

            "Beach Zone Taillow": lambda state: can_play_catch(
                state, player, options
            ),
            "Ice Zone Taillow": lambda state: can_play_catch(
                state, player, options
            ),
            "Granite Zone Taillow": lambda state: can_play_catch(
                state, player, options
            ),

            "Beach Zone Staravia": lambda state: can_battle(state, player, options),
            "Ice Zone Staravia": lambda state: can_battle(state, player, options),

            "Beach Zone Wingull": lambda state: can_play_catch(state, player, options),
            "Ice Zone Wingull": lambda state: can_play_catch(state, player, options),

            "Beach Zone Corphish": lambda state: state.has("Corphish Unlock", player) and can_battle(
                state, player, options
            ),
            "Ice Zone Corphish": lambda state: state.has("Corphish Unlock", player) and can_battle(
                state, player, options
            ),

            "Ice Zone Teddiursa": lambda state: can_play_catch(state, player, options),
            "Cavern Zone Teddiursa": lambda state: True,
            "Flower Zone Teddiursa": lambda state: True,

            "Cavern Zone Aron": lambda state: can_destroy_objects_overworld(state, player),
            "Magma Zone Aron": lambda state: can_dash_overworld(state, player),

            "Cavern Zone Torchic": lambda state: can_battle_intermediate(state, player, options),
            "Magma Zone Torchic": lambda state: can_battle_intermediate(state, player, options),

            "Cavern Zone Geodude": lambda state: True,
            "Magma Zone Geodude": lambda state: True,

            "Cavern Zone Raichu": lambda state: state.has("Raichu Unlock", player) and can_play_catch_intermediate(
                state,
                player, options
            ),
            "Haunted Zone Raichu": lambda state: can_play_catch_intermediate(
                state,
                player, options
            ),

            "Cavern Zone Meowth": lambda state: True,
            "Haunted Zone Meowth": lambda state: True,

            "Cavern Zone Marowak": lambda state: can_battle_intermediate(state, player, options),
            "Granite Zone Marowak": lambda state: can_battle_intermediate(state, player, options),

            "Magma Zone Baltoy": lambda state: state.has(
                "Baltoy Unlock", player
            ) and can_battle_thunderbolt_immune_intermediate(
                state, player, options
            ),
            "Magma Zone Baltoy Unlocks": lambda state: state.has(
                "Baltoy Unlock", player
            ) and can_battle_thunderbolt_immune_intermediate(
                state, player, options
            ),
            "Granite Zone Baltoy": lambda state: state.has(
                "Baltoy Unlock", player
            ) and can_battle_thunderbolt_immune_advanced(
                state, player, options
            ),
            "Granite Zone Baltoy Unlocks": lambda state: state.has(
                "Baltoy Unlock", player
            ) and can_battle_thunderbolt_immune_advanced(
                state, player, options
            ),

            "Magma Zone Claydol": lambda state: state.has(
                "Claydol Unlock", player
            ) and can_battle_thunderbolt_immune_intermediate(
                state, player, options
            ),
            "Granite Zone Claydol": lambda state: state.has(
                "Claydol Unlock", player
            ) and can_battle_thunderbolt_immune_advanced(
                state, player, options
            ),
            "Magma Zone Meditite": lambda state: True,
            "Flower Zone Meditite": lambda state: True,

            "Haunted Zone Drifloon": lambda state: state.has("Rotom Prisma", player),
            "Granite Zone Drifloon": lambda state: True,

            "Granite Zone Furret": lambda state: True,
            "Flower Zone Furret": lambda state: True,
        }
        self.entrances_rules = ENTRANCE_RULES

    def randomize_attraction_entrances(self):
        entrances = list(ATTRACTION_ENTRANCES_TO_EXITS.keys())
        exits = list(ATTRACTION_ENTRANCES_TO_EXITS.values())
        self.world.random.shuffle(exits)

        return dict(zip(entrances, exits))

    def set_entrances_to_exits(self):
        options = self.world.options
        entrances_to_exits = VANILLA_ENTRANCES_TO_EXITS.copy()

        if options.randomize_attraction_entrances == options.randomize_attraction_entrances.option_true:
            entrances_to_exits |= self.randomize_attraction_entrances()
        else:
            entrances_to_exits |= ATTRACTION_ENTRANCES_TO_EXITS

        if options.each_zone == options.each_zone.option_false:
            entrances_to_exits |= ADDITIONAL_ENTRANCES_TO_EXITS

        self.entrances_to_exits = entrances_to_exits

    def set_region_to_entrances(self):
        options = self.world.options
        region_to_entrances = {region: list(entrances) for region, entrances in REGION_TO_ENTRANCES.items()}
        if options.each_zone == options.each_zone.option_false:
            for region, entrances in ADDITIONAL_REGION_TO_ENTRANCES.items():
                region_to_entrances.setdefault(region, []).extend(entrances)

        self.region_to_entrances = region_to_entrances

    def generate_entrance_data(self):
        self.set_entrances_to_exits()
        self.set_region_to_entrances()
        self.set_entrance_rules()
