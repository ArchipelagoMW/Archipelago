from typing import Dict, Callable, TYPE_CHECKING

from BaseClasses import CollectionState, Region, ItemClassification
from worlds.pokepark.locations import PokeparkLocation
from worlds.pokepark.logic import Requirements, PokeparkRegion, PowerRequirement, WorldStateRequirement, \
    MinigameRequirement, generate_regions

if TYPE_CHECKING:
    from . import PokeparkWorld

POWER_REQUIREMENT_CHECKS: Dict[PowerRequirement, Callable] = {
    PowerRequirement.none: lambda state, world: True,
    PowerRequirement.can_battle: lambda state, world: (
            state.has("Progressive Thunderbolt", world.player) or
            state.has("Progressive Dash", world.player) or
            state.has("Progressive Iron Tail", world.player)
    ),
    PowerRequirement.can_dash_overworld: lambda state, world: state.has("Progressive Dash", world.player),
    PowerRequirement.can_play_catch: lambda state, world: state.has("Progressive Dash", world.player),
    PowerRequirement.can_destroy_objects_overworld: lambda state, world: (
            state.has("Progressive Dash", world.player) or
            state.has("Progressive Thunderbolt", world.player)
    ),
    PowerRequirement.can_thunderbolt_overworld: lambda state, world: state.has("Progressive Thunderbolt", world.player),
    PowerRequirement.can_battle_thunderbolt_immune: lambda state, world: (
            state.has("Progressive Dash", world.player) or
            state.has("Progressive Iron Tail", world.player)
    ),
    PowerRequirement.can_farm_berries: lambda state, world: state.has("Progressive Dash", world.player),
    PowerRequirement.can_play_catch_intermediate: lambda state, world: state.has("Progressive Dash", world.player,
                                                                                 count=2),
}
WORLD_STATE_REQUIREMENT_CHECKS: Dict[WorldStateRequirement, Callable] = {
    WorldStateRequirement.none: lambda state, world: True,
    WorldStateRequirement.meadow_zone_or_higher: lambda state, world: (
            state.has("Meadow Zone Unlock", world.player) or
            state.has("Beach Zone Unlock", world.player) or
            state.has("Ice Zone Unlock", world.player) or
            state.has("Cavern Zone & Magma Zone Unlock", world.player) or
            state.has("Haunted Zone Unlock", world.player)

    ),
    WorldStateRequirement.beach_zone_or_higher: lambda state, world: (
            state.has("Beach Zone Unlock", world.player) or
            state.has("Ice Zone Unlock", world.player) or
            state.has("Cavern Zone & Magma Zone Unlock", world.player) or
            state.has("Haunted Zone Unlock", world.player)

    ),
    WorldStateRequirement.ice_zone_or_higher: lambda state, world: (
            state.has("Ice Zone Unlock", world.player) or
            state.has("Cavern Zone & Magma Zone Unlock", world.player) or
            state.has("Haunted Zone Unlock", world.player)

    ),
    WorldStateRequirement.cavern_and_magma_zone_or_higher: lambda state, world: (
            state.has("Cavern Zone & Magma Zone Unlock", world.player) or
            state.has("Haunted Zone Unlock", world.player) or
            state.has("Granite Zone & Flower Zone Unlock", world.player) or
            state.has("Skygarden Unlock", world.player)
    ),
    WorldStateRequirement.haunted_zone_or_higher: lambda state, world: (
            state.has("Haunted Zone Unlock", world.player) or
            state.has("Granite Zone & Flower Zone Unlock", world.player) or
            state.has("Skygarden Unlock", world.player)
    ),
    WorldStateRequirement.granite_and_flower_zone_or_higher: lambda state, world: (
            state.has("Granite Zone & Flower Zone Unlock", world.player) or
            state.has("Skygarden Unlock", world.player)
    ),
    WorldStateRequirement.skygarden: lambda state, world: (
        state.has("Skygarden Unlock", world.player)
    )
}
MINIGAME_REQUIREMENT_CHECKS: Dict[MinigameRequirement, Callable] = {
    MinigameRequirement.none: lambda state, world: True,
    MinigameRequirement.bulbasaur_dash_any: lambda state, world: (
            state.can_reach_location("Meadow Zone - Bulbasaur's Daring Dash Minigame - Pikachu", world.player) or
            state.can_reach_location("Meadow Zone - Bulbasaur's Daring Dash Minigame - Turtwig", world.player) or
            state.can_reach_location("Meadow Zone - Bulbasaur's Daring Dash Minigame - Munchlax", world.player) or
            state.can_reach_location("Meadow Zone - Bulbasaur's Daring Dash Minigame - Chimchar", world.player) or
            state.can_reach_location("Meadow Zone - Bulbasaur's Daring Dash Minigame - Treecko", world.player) or
            state.can_reach_location("Meadow Zone - Bulbasaur's Daring Dash Minigame - Bibarel", world.player) or
            state.can_reach_location("Meadow Zone - Bulbasaur's Daring Dash Minigame - Bulbasaur", world.player) or
            state.can_reach_location("Meadow Zone - Bulbasaur's Daring Dash Minigame - Bidoof", world.player) or
            state.can_reach_location("Meadow Zone - Bulbasaur's Daring Dash Minigame - Oddish", world.player) or
            state.can_reach_location("Meadow Zone - Bulbasaur's Daring Dash Minigame - Shroomish", world.player) or
            state.can_reach_location("Meadow Zone - Bulbasaur's Daring Dash Minigame - Bonsly", world.player) or
            state.can_reach_location("Meadow Zone - Bulbasaur's Daring Dash Minigame - Lotad", world.player) or
            state.can_reach_location("Meadow Zone - Bulbasaur's Daring Dash Minigame - Weedle", world.player) or
            state.can_reach_location("Meadow Zone - Bulbasaur's Daring Dash Minigame - Caterpie", world.player) or
            state.can_reach_location("Meadow Zone - Bulbasaur's Daring Dash Minigame - Magikarp", world.player) or
            state.can_reach_location("Meadow Zone - Bulbasaur's Daring Dash Minigame - Jolteon", world.player) or
            state.can_reach_location("Meadow Zone - Bulbasaur's Daring Dash Minigame - Arcanine", world.player) or
            state.can_reach_location("Meadow Zone - Bulbasaur's Daring Dash Minigame - Leafeon", world.player) or
            state.can_reach_location("Meadow Zone - Bulbasaur's Daring Dash Minigame - Scyther", world.player) or
            state.can_reach_location("Meadow Zone - Bulbasaur's Daring Dash Minigame - Ponyta", world.player) or
            state.can_reach_location("Meadow Zone - Bulbasaur's Daring Dash Minigame - Shinx", world.player) or
            state.can_reach_location("Meadow Zone - Bulbasaur's Daring Dash Minigame - Eevee", world.player) or
            state.can_reach_location("Meadow Zone - Bulbasaur's Daring Dash Minigame - Pachirisu", world.player) or
            state.can_reach_location("Meadow Zone - Bulbasaur's Daring Dash Minigame - Buneary", world.player) or
            state.can_reach_location("Meadow Zone - Bulbasaur's Daring Dash Minigame - Croagunk", world.player) or
            (world.options.goal == world.options.goal.option_aftergame and
             state.can_reach_location("Meadow Zone - Bulbasaur's Daring Dash Minigame - Mew", world.player))
    ),

    MinigameRequirement.venusaur_vine_swing_any: lambda state, world: (
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Pikachu", world.player) or
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Munchlax", world.player) or
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Magikarp", world.player) or
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Blaziken", world.player) or
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Infernape", world.player) or
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Lucario", world.player) or
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Primeape", world.player) or
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Tangrowth", world.player) or
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Ambipom", world.player) or
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Croagunk", world.player) or
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Mankey", world.player) or
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Aipom", world.player) or
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Chimchar", world.player) or
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Treecko", world.player) or
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Pachirisu", world.player) or
            (world.options.goal == world.options.goal.option_aftergame and
             state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Jirachi", world.player))
    ),
    MinigameRequirement.venusaur_vine_swing_all: lambda state, world: (
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Pikachu", world.player) and
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Munchlax", world.player) and
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Magikarp", world.player) and
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Blaziken", world.player) and
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Infernape", world.player) and
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Lucario", world.player) and
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Primeape", world.player) and
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Tangrowth", world.player) and
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Ambipom", world.player) and
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Croagunk", world.player) and
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Mankey", world.player) and
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Aipom", world.player) and
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Chimchar", world.player) and
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Treecko", world.player) and
            state.can_reach_location("Meadow Zone - Venusaur's Vine Swing - Pachirisu", world.player)
    ),
    MinigameRequirement.pelipper_circuit_any: lambda state, world: (
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Pikachu", world.player) or
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Staraptor", world.player) or
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Togekiss", world.player) or
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Honchkrow", world.player) or
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Gliscor", world.player) or
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Pelipper", world.player) or
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Staravia", world.player) or
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Pidgeotto", world.player) or
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Butterfree", world.player) or
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Tropius", world.player) or
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Murkrow", world.player) or
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Taillow", world.player) or
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Spearow", world.player) or
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Starly", world.player) or
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Wingull", world.player) or
            (world.options.goal == world.options.goal.option_aftergame and
             state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Latias", world.player))
    ),
    MinigameRequirement.pelipper_circuit_all: lambda state, world: (
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Pikachu", world.player) and
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Staraptor", world.player) and
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Togekiss", world.player) and
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Honchkrow", world.player) and
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Gliscor", world.player) and
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Pelipper", world.player) and
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Staravia", world.player) and
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Pidgeotto", world.player) and
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Butterfree", world.player) and
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Tropius", world.player) and
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Murkrow", world.player) and
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Taillow", world.player) and
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Spearow", world.player) and
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Starly", world.player) and
            state.can_reach_location("Beach Zone - Pelipper's Circle Circuit - Wingull", world.player)
    ),
    MinigameRequirement.gyarados_aqua_any: lambda state, world: (
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Pikachu", world.player) or
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Psyduck", world.player) or
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Azurill", world.player) or
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Slowpoke", world.player) or
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Empoleon", world.player) or
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Floatzel", world.player) or
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Feraligatr", world.player) or
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Golduck", world.player) or
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Vaporeon", world.player) or
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Prinplup", world.player) or
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Bibarel", world.player) or
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Buizel", world.player) or
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Corsola", world.player) or
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Piplup", world.player) or
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Lotad", world.player) or
            (world.options.goal == world.options.goal.option_aftergame and
             state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Manaphy", world.player))

    ),
    MinigameRequirement.gyarados_aqua_all: lambda state, world: (
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Pikachu", world.player) and
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Psyduck", world.player) and
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Azurill", world.player) and
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Slowpoke", world.player) and
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Empoleon", world.player) and
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Floatzel", world.player) and
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Feraligatr", world.player) and
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Golduck", world.player) and
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Vaporeon", world.player) and
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Prinplup", world.player) and
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Bibarel", world.player) and
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Buizel", world.player) and
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Corsola", world.player) and
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Piplup", world.player) and
            state.can_reach_location("Beach Zone - Gyarados' Aqua Dash - Lotad", world.player)

    ),
    MinigameRequirement.empoleon_slide_any: lambda state, world: (
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Pikachu", world.player) or
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Teddiursa", world.player) or
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Magikarp", world.player) or
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Empoleon", world.player) or
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Glaceon", world.player) or
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Blastoise", world.player) or
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Glalie", world.player) or
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Delibird", world.player) or
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Piloswine", world.player) or
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Prinplup", world.player) or
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Squirtle", world.player) or
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Piplup", world.player) or
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Quagsire", world.player) or
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Spheal", world.player) or
            (world.options.goal == world.options.goal.option_aftergame and
             state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Suicune", world.player))

    ),
    MinigameRequirement.empoleon_slide_all: lambda state, world: (
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Pikachu", world.player) and
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Teddiursa", world.player) and
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Magikarp", world.player) and
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Empoleon", world.player) and
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Glaceon", world.player) and
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Blastoise", world.player) and
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Glalie", world.player) and
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Delibird", world.player) and
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Piloswine", world.player) and
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Prinplup", world.player) and
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Squirtle", world.player) and
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Piplup", world.player) and
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Quagsire", world.player) and
            state.can_reach_location("Ice Zone - Empoleon's Snow Slide - Spheal", world.player)
    ),
    MinigameRequirement.bastiodon_panel_any: lambda state, world: (
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Pikachu", world.player) or
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Sableye", world.player) or
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Meowth", world.player) or
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Torchic", world.player) or
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Electivire", world.player) or
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Magmortar", world.player) or
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Hitmonlee", world.player) or
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Ursaring", world.player) or
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Mr. Mime", world.player) or
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Raichu", world.player) or
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Sudowoodo", world.player) or
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Charmander", world.player) or
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Gible", world.player) or
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Chimchar", world.player) or
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Magby", world.player) or
            (world.options.goal == world.options.goal.option_aftergame and
             state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Metagross", world.player))
    ),
    MinigameRequirement.bastiodon_panel_all: lambda state, world: (
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Pikachu", world.player) and
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Sableye", world.player) and
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Meowth", world.player) and
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Torchic", world.player) and
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Electivire", world.player) and
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Magmortar", world.player) and
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Hitmonlee", world.player) and
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Ursaring", world.player) and
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Mr. Mime", world.player) and
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Raichu", world.player) and
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Sudowoodo", world.player) and
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Charmander", world.player) and
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Gible", world.player) and
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Chimchar", world.player) and
            state.can_reach_location("Cavern Zone - Bastiodon's Panel Crush - Magby", world.player)
    ),
    MinigameRequirement.rhyperior_bumper_any: lambda state, world: (
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Pikachu", world.player) or
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Magnemite", world.player) or
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Rhyperior", world.player) or
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Tyranitar", world.player) or
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Hitmontop", world.player) or
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Flareon", world.player) or
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Venusaur", world.player) or
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Snorlax", world.player) or
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Torterra", world.player) or
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Magnezone", world.player) or
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Claydol", world.player) or
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Quilava", world.player) or
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Torkoal", world.player) or
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Baltoy", world.player) or
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Bonsly", world.player) or
            (world.options.goal == world.options.goal.option_aftergame and
             state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Heatran", world.player))
    ),
    MinigameRequirement.rhyperior_bumper_all: lambda state, world: (
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Pikachu", world.player) and
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Magnemite", world.player) and
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Rhyperior", world.player) and
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Tyranitar", world.player) and
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Hitmontop", world.player) and
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Flareon", world.player) and
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Venusaur", world.player) and
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Snorlax", world.player) and
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Torterra", world.player) and
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Magnezone", world.player) and
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Claydol", world.player) and
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Quilava", world.player) and
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Torkoal", world.player) and
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Baltoy", world.player) and
            state.can_reach_location("Magma Zone - Rhyperior's Bumper Burn - Bonsly", world.player)
    ),
    MinigameRequirement.blaziken_boulder_any: lambda state, world: (
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Pikachu", world.player) or
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Geodude", world.player) or
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Phanpy", world.player) or
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Blaziken", world.player) or
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Garchomp", world.player) or
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Scizor", world.player) or
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Magmortar", world.player) or
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Hitmonchan", world.player) or
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Machamp", world.player) or
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Marowak", world.player) or
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Farfetch'd", world.player) or
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Cranidos", world.player) or
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Camerupt", world.player) or
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Bastiodon", world.player) or
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Mawile", world.player) or
            (world.options.goal == world.options.goal.option_aftergame and
             state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Groudon", world.player))

    ),
    MinigameRequirement.blaziken_boulder_all: lambda state, world: (
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Pikachu", world.player) and
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Geodude", world.player) and
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Phanpy", world.player) and
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Blaziken", world.player) and
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Garchomp", world.player) and
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Scizor", world.player) and
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Magmortar", world.player) and
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Hitmonchan", world.player) and
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Machamp", world.player) and
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Marowak", world.player) and
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Farfetch'd", world.player) and
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Cranidos", world.player) and
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Camerupt", world.player) and
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Bastiodon", world.player) and
            state.can_reach_location("Magma Zone - Blaziken's Boulder Bash - Mawile", world.player)
    ),
    MinigameRequirement.tangrowth_swing_any: lambda state, world: (
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Pikachu", world.player) or
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Meowth", world.player) or
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Pichu", world.player) or
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Lucario", world.player) or
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Infernape", world.player) or
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Blaziken", world.player) or
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Riolu", world.player) or
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Sneasel", world.player) or
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Raichu", world.player) or
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Ambipom", world.player) or
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Primeape", world.player) or
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Aipom", world.player) or
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Electabuzz", world.player) or
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Chimchar", world.player) or
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Croagunk", world.player) or
            (world.options.goal == world.options.goal.option_aftergame and
             state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Celebi", world.player))

    ),
    MinigameRequirement.tangrowth_swing_all: lambda state, world: (
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Pikachu", world.player) and
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Meowth", world.player) and
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Pichu", world.player) and
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Lucario", world.player) and
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Infernape", world.player) and
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Blaziken", world.player) and
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Riolu", world.player) and
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Sneasel", world.player) and
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Raichu", world.player) and
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Ambipom", world.player) and
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Primeape", world.player) and
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Aipom", world.player) and
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Electabuzz", world.player) and
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Chimchar", world.player) and
            state.can_reach_location("Haunted Zone - Tangrowth's Swing-Along - Croagunk", world.player)

    ),
    MinigameRequirement.dusknoir_slam_any: lambda state, world: (
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Pikachu", world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Stunky", world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Gengar", world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Mismagius", world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Scizor", world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Espeon", world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Dusknoir", world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Umbreon", world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Cranidos", world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Skuntank", world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Electrode", world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Gastly", world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Duskull", world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Misdreavus", world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Krabby", world.player) or
            (world.options.goal == world.options.goal.option_aftergame and
             state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Darkrai", world.player))

    ),
    MinigameRequirement.dusknoir_slam_all: lambda state, world: (
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Pikachu", world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Stunky", world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Gengar", world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Mismagius", world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Scizor", world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Espeon", world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Dusknoir", world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Umbreon", world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Cranidos", world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Skuntank", world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Electrode", world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Gastly", world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Duskull", world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Misdreavus", world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Dusknoir's Speed Slam - Krabby", world.player)
    ),
    MinigameRequirement.rotom_shoot_any: lambda state, world: (
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Pikachu", world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Magnemite",
                                     world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Porygon-Z",
                                     world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Magnezone",
                                     world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Gengar", world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Magmortar",
                                     world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Electivire",
                                     world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Mismagius",
                                     world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Claydol", world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Electabuzz",
                                     world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Abra", world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Elekid", world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Mr. Mime", world.player) or
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Baltoy", world.player) or
            (world.options.goal == world.options.goal.option_aftergame and
             state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Rotom", world.player))
    ),
    MinigameRequirement.rotom_shoot_all: lambda state, world: (
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Pikachu", world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Magnemite",
                                     world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Porygon-Z",
                                     world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Magnezone",
                                     world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Gengar", world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Magmortar",
                                     world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Electivire",
                                     world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Mismagius",
                                     world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Claydol", world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Electabuzz",
                                     world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Abra", world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Elekid", world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Mr. Mime",
                                     world.player) and
            state.can_reach_location("Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Baltoy", world.player)
    ),
    MinigameRequirement.absol_hurdle_any: lambda state, world: (
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Pikachu", world.player) or
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Chikorita", world.player) or
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Absol", world.player) or
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Lucario", world.player) or
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Ponyta", world.player) or
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Ninetales", world.player) or
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Lopunny", world.player) or
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Espeon", world.player) or
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Infernape", world.player) or
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Breloom", world.player) or
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Riolu", world.player) or
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Furret", world.player) or
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Mareep", world.player) or
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Eevee", world.player) or
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Vulpix", world.player) or
            (world.options.goal == world.options.goal.option_aftergame and
             state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Shaymin", world.player))
    ),
    MinigameRequirement.absol_hurdle_all: lambda state, world: (
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Pikachu", world.player) and
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Chikorita", world.player) and
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Absol", world.player) and
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Lucario", world.player) and
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Ponyta", world.player) and
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Ninetales", world.player) and
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Lopunny", world.player) and
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Espeon", world.player) and
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Infernape", world.player) and
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Breloom", world.player) and
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Riolu", world.player) and
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Furret", world.player) and
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Mareep", world.player) and
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Eevee", world.player) and
            state.can_reach_location("Granite Zone - Absol's Hurdle Bounce - Vulpix", world.player)
    ),
    MinigameRequirement.salamence_air_any: lambda state, world: (
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Pikachu", world.player) or
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Salamence", world.player) or
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Charizard", world.player) or
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Dragonite", world.player) or
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Flygon", world.player) or
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Aerodactyl", world.player) or
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Staraptor", world.player) or
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Honchkrow", world.player) or
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Gliscor", world.player) or
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Pidgeotto", world.player) or
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Togekiss", world.player) or
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Golbat", world.player) or
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Taillow", world.player) or
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Murkrow", world.player) or
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Zubat", world.player) or
            (world.options.goal == world.options.goal.option_aftergame and
             state.can_reach_location("Granite Zone - Salamence's Sky Race - Latios", world.player))
    ),
    MinigameRequirement.salamence_air_all: lambda state, world: (
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Pikachu", world.player) and
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Salamence", world.player) and
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Charizard", world.player) and
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Dragonite", world.player) and
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Flygon", world.player) and
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Aerodactyl", world.player) and
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Staraptor", world.player) and
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Honchkrow", world.player) and
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Gliscor", world.player) and
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Pidgeotto", world.player) and
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Togekiss", world.player) and
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Golbat", world.player) and
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Taillow", world.player) and
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Murkrow", world.player) and
            state.can_reach_location("Granite Zone - Salamence's Sky Race - Zubat", world.player)
    ),
    MinigameRequirement.rayquaza_balloon_any: lambda state, world: (
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Pikachu", world.player) or
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Lucario", world.player) or
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Glaceon", world.player) or
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Luxray", world.player) or
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Mamoswine", world.player) or
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Infernape", world.player) or
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Floatzel", world.player) or
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Rhyperior", world.player) or
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Absol", world.player) or
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Breloom", world.player) or
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Mareep", world.player) or
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Cyndaquil", world.player) or
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Totodile", world.player) or
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Chikorita", world.player) or
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Mime Jr.", world.player) or
            (world.options.goal == world.options.goal.option_aftergame and
             state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Deoxys", world.player))

    ),
    MinigameRequirement.rayquaza_balloon_all: lambda state, world: (
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Pikachu", world.player) and
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Lucario", world.player) and
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Glaceon", world.player) and
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Luxray", world.player) and
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Mamoswine", world.player) and
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Infernape", world.player) and
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Floatzel", world.player) and
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Rhyperior", world.player) and
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Absol", world.player) and
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Breloom", world.player) and
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Mareep", world.player) and
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Cyndaquil", world.player) and
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Totodile", world.player) and
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Chikorita", world.player) and
            state.can_reach_location("Flower Zone - Rayquaza's Balloon Panic - Mime Jr.", world.player)
    ),
}


def pokepark_requirements_satisfied(state: CollectionState, requirements: Requirements, world: "PokeparkWorld"):
    has_required_unlocks = all(state.has(unlock, world.player) for unlock in requirements.unlock_names)
    has_required_friends = all(state.has(friend, world.player) for friend in requirements.friendship_names)
    has_required_prismas = all(state.has(prisma, world.player) for prisma in requirements.prisma_names)
    has_enough_friends = requirements.friendcount <= state.count_group("Friendship Items", world.player)
    can_reach_required_locations = all(
        state.can_reach_location(location, world.player) for location in requirements.can_reach_locations)
    if requirements.oneof_item_names:
        has_any = any(
            all(state.has(item, world.player) for item in item_list)
            for item_list in requirements.oneof_item_names
        )
    else:
        has_any = True
    has_required_power = POWER_REQUIREMENT_CHECKS[requirements.powers](state, world)
    has_required_world_state = WORLD_STATE_REQUIREMENT_CHECKS[requirements.world_state](state, world)
    has_required_minigames = MINIGAME_REQUIREMENT_CHECKS[requirements.minigame](state, world)

    return (has_required_unlocks and
            has_enough_friends and
            has_required_friends and
            has_required_prismas and
            has_any and
            can_reach_required_locations and
            has_required_power and
            has_required_world_state and
            has_required_minigames)


def create_region(region: PokeparkRegion, world: "PokeparkWorld"):
    new_region = Region(region.name, world.player, world.multiworld)

    def create_location(location):
        new_location = PokeparkLocation(
            world.player,
            f"{region.display} - {location.name}",
            location.id,
            new_region
        )

        new_location.access_rule = lambda state: pokepark_requirements_satisfied(state, location.requirements, world)
        if world.options.goal == world.options.goal.option_mew:
            if new_location.name == "Skygarden - Overworld - Mew Challenge completed":
                event_item = world.create_item("Victory")
                new_location.place_locked_item(event_item)
            if new_location.name == "Magma Zone - Overworld - Blaziken":
                event_item = world.create_item("Skygarden Unlock")
                new_location.place_locked_item(event_item)
        if world.options.goal == world.options.goal.option_aftergame:
            if new_location.name == "Skygarden - Overworld - Completing Prisma":
                event_item = world.create_item("Victory")
                new_location.place_locked_item(event_item)

        new_region.locations.append(new_location)

    for location in region.quest_locations:
        create_location(location)
    for location in region.unlock_location:
        create_location(location)
    for location in region.friendship_locations:
        create_location(location)
    for location in region.minigame_location:
        create_location(location)

    return new_region


def create_regions(world: "PokeparkWorld"):
    regions = {
        "Menu": Region("Menu", world.player, world.multiworld)
    }

    CREATEDREGIONS = generate_regions(world)

    for region in CREATEDREGIONS:
        regions[region.name] = create_region(region, world)

        for parent_name in region.parent_regions:
            if parent_name in regions:
                regions[parent_name].connect(regions[region.name], None,
                                             lambda state, r=region: pokepark_requirements_satisfied(state,
                                                                                                     r.requirements,
                                                                                                     world))

    world.multiworld.regions += regions.values()
    world.set_rules()
