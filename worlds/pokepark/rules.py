from typing import TYPE_CHECKING, Callable

from BaseClasses import CollectionState
from ..generic.Rules import set_rule

if TYPE_CHECKING:
    from . import PokeparkWorld


def set_rules(world: "PokeparkWorld") -> None:
    def set_rule_if_exists(location_name: str, rule: Callable[[CollectionState], bool]) -> None:
        if location_name in world.locations:
            set_rule(world.get_location(location_name), rule)

    player = world.player

    # Treehouse
    set_rule_if_exists("Treehouse - Burmy - Friendship", lambda state: True)
    set_rule_if_exists("Treehouse - Mime Jr. - Friendship", lambda state: True)
    set_rule_if_exists("Treehouse - Drifblim - Friendship", lambda state: can_farm_berries(state, player))
    set_rule_if_exists("Treehouse - Power Up - Thunderbolt Upgrade 1", lambda state: can_farm_berries(state, player))
    set_rule_if_exists(
        "Treehouse - Power Up - Thunderbolt Upgrade 2",
        lambda state: state.can_reach_location("Treehouse - Power Up - Thunderbolt Upgrade 1", player)
    )
    set_rule_if_exists(
        "Treehouse - Power Up - Thunderbolt Upgrade 3",
        lambda state: state.can_reach_location("Treehouse - Power Up - Thunderbolt Upgrade 2", player)
    )
    set_rule_if_exists(
        "Treehouse - Power Up - Dash Upgrade 1",
        lambda state: can_farm_berries(state, player) and state.has("Pelipper Prisma", player)
    )
    set_rule_if_exists(
        "Treehouse - Power Up - Dash Upgrade 2",
        lambda state: state.can_reach_location("Treehouse - Power Up - Dash Upgrade 1", player)
    )
    set_rule_if_exists(
        "Treehouse - Power Up - Ponyta Unlocked",
        lambda state: state.can_reach_location("Treehouse - Power Up - Dash Upgrade 2", player)
    )
    set_rule_if_exists(
        "Treehouse - Power Up - Dash Upgrade 3",
        lambda state: state.can_reach_location("Treehouse - Power Up - Dash Upgrade 2", player)
    )
    set_rule_if_exists(
        "Treehouse - Power Up - Double Dash Upgrade",
        lambda state: True
    )
    set_rule_if_exists(
        "Treehouse - Power Up - Health Upgrade 1",
        lambda state: can_farm_berries(state, player) and state.has("Venusaur Prisma", player)
    )  # TODO: placeholder until defined
    set_rule_if_exists(
        "Treehouse - Power Up - Health Upgrade 2",
        lambda state: state.can_reach_location(
            "Treehouse - Power Up - Health Upgrade 1",
            player
        )
    )
    set_rule_if_exists(
        "Treehouse - Power Up - Health Upgrade 3",
        lambda state: state.can_reach_location(
            "Treehouse - Power Up - Health Upgrade 2",
            player
        )
    )
    set_rule_if_exists(
        "Treehouse - Power Up - Iron Tail Upgrade 1",
        lambda state: can_farm_berries(state, player) and state.has("Empoleon Prisma", player)
    )
    set_rule_if_exists(
        "Treehouse - Power Up - Iron Tail Upgrade 2",
        lambda state: state.can_reach_location(
            "Treehouse - Power Up - Iron Tail Upgrade 1",
            player
        )
    )
    set_rule_if_exists(
        "Treehouse - Power Up - Iron Tail Upgrade 3",
        lambda state: state.can_reach_location(
            "Treehouse - Power Up - Iron Tail Upgrade 2",
            player
        )
    )

    # Meadow Zone
    set_rule_if_exists(
        "Meadow Zone Main Area - Turtwig Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Turtwig Power Competition -- Pachirisu Unlocked",
        lambda state: can_play_catch(state, player)

    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Turtwig Power Competition -- Bonsly Unlocked",
        lambda state: can_play_catch(state, player)

    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Bulbasaur -- Friendship",
        lambda state: state.has("Bulbasaur Prisma", player) and state.can_reach_region(
            "Bulbasaur's Daring Dash Attraction", player
        )
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Buneary Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Buneary Power Competition -- Lotad Unlocked",
        lambda state: can_play_catch(state, player)

    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Buneary Power Competition -- Shinx Unlocked",
        lambda state: can_play_catch(state, player)

    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Munchlax Errand -- Friendship",
        lambda state: state.has("Bulbasaur Prisma", player) and can_destroy_objects_overworld(state, player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Munchlax Errand -- Tropius Unlocked",
        lambda state: state.has("Bulbasaur Prisma", player) and can_destroy_objects_overworld(state, player)

    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Tropius Errand -- Friendship",
        lambda state: state.has("Bulbasaur Prisma", player) and can_destroy_objects_overworld(
            state, player
        ) and state.has("Tropius Unlock", player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Pachirisu Power Competition -- Friendship",
        lambda state: can_play_catch(state, player) and state.has("Pachirisu Unlock", player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Shinx Power Competition -- Friendship",
        lambda state: can_play_catch(state, player) and state.has("Shinx Unlock", player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Mankey Power Competition -- Friendship",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Mankey Power Competition -- Chimchar Unlocked",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Spearow Power Competition -- Friendship",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Croagunk Power Competition -- Friendship",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Croagunk Power Competition -- Scyther Unlocked",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Lotad Power Competition -- Friendship",
        lambda state: can_battle(state, player) and state.has("Lotad Unlock", player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Treecko Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Caterpie Tree -- Caterpie Unlocked",
        lambda state: can_dash_overworld(state, player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Caterpie Power Competition -- Friendship",
        lambda state: can_play_catch(state, player) and state.has("Caterpie Unlock", player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Caterpie Power Competition -- Butterfree Unlocked",
        lambda state: can_play_catch(state, player) and state.has("Caterpie Unlock", player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Weedle Tree -- Weedle Unlocked",
        lambda state: can_dash_overworld(state, player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Weedle Power Competition -- Friendship",
        lambda state: can_battle(state, player) and state.has("Weedle Unlock", player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Shroomish Crate -- Shroomish Unlocked",
        lambda state: can_destroy_objects_overworld(state, player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Shroomish Power Competition -- Friendship",
        lambda state: can_play_catch(state, player) and state.has("Shroomish Unlock", player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Magikarp Rescue -- Magikarp Unlocked",
        lambda state: can_thunderbolt_overworld(state, player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Oddish Power Competition -- Friendship",
        lambda state: True
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Bidoof Housing -- Stage 1",
        lambda state: state.has("Mankey Friendship", player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Bidoof Housing -- Bidoof 1 Unlocked",
        lambda state: state.has("Mankey Friendship", player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Bidoof Housing -- Stage 2",
        lambda state: state.has("Mankey Friendship", player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Bidoof Housing -- Bidoof 2 Unlocked",
        lambda state: state.has("Mankey Friendship", player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Bidoof Housing -- Stage 3",
        lambda state: state.has("Mankey Friendship", player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Bidoof Housing -- Bidoof 3 Unlocked",
        lambda state: state.has("Mankey Friendship", player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Bidoof Housing -- Stage 4",
        lambda state: state.has("Mankey Friendship", player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Bidoof Housing -- Bibarel Unlocked",
        lambda state: state.has("Mankey Friendship", player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Bidoof Housing Completed -- Friendship",
        lambda state: state.has("Mankey Friendship", player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Bidoof Housing Completed -- Beach Bidoof Unlocked",
        lambda state: state.has("Mankey Friendship", player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Bibarel Power Competition -- Friendship",
        lambda state: can_battle(state, player) and state.has("Bibarel Unlock", player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Leafeon Power Competition -- Friendship",
        lambda state: can_play_catch(state, player) and state.count_group("Friendship Items", player) >= 20
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Torterra Power Competition -- Friendship",
        lambda state: state.has("Torterra Unlock", player) and can_battle_thunderbolt_immune(state, player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Scyther Power Competition -- Friendship",
        lambda state: state.has("Scyther Unlock", player) and can_battle(state, player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Starly Power Competition -- Friendship",
        lambda state: state.has("Starly 2 Unlock", player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Bonsly Power Competition -- Friendship",
        lambda state: state.has("Bonsly Unlock", player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Bonsly Power Competition -- Sudowoodo Unlocked",
        lambda state: state.has("Bonsly Unlock", player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Chimchar Power Competition -- Friendship",
        lambda state: state.has("Chimchar Unlock", player) and can_battle(state, player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Sudowoodo Power Competition -- Friendship",
        lambda state: state.has("Sudowoodo Unlock", player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Aipom Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Aipom Power Competition -- Ambipom Unlocked",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Meadow Zone Main Area - Ambipom Power Competition -- Friendship",
        lambda state: can_battle(state, player) and state.has("Ambipom Unlock", player)
    )

    # Bulbasaur Daring Dash Minigame
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Prisma",
        lambda state: can_beat_any_bulbasaur_daring_dash_record(state, player)
    )
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Pikachu",
        lambda state: True
    )
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Turtwig",
        lambda state: state.has("Turtwig Friendship", player)
    )
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Munchlax",
        lambda state: state.has("Munchlax Friendship", player)
    )
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Chimchar",
        lambda state: state.has("Chimchar Friendship", player)
    )
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Treecko",
        lambda state: state.has("Treecko Friendship", player)
    )
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Bibarel",
        lambda state: state.has("Bibarel Friendship", player)
    )
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Bulbasaur",
        lambda state: state.has("Bulbasaur Friendship", player)
    )
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Bidoof",
        lambda state: state.has("Bidoof Friendship", player)
    )
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Oddish",
        lambda state: state.has("Oddish Friendship", player)
    )
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Shroomish",
        lambda state: state.has("Shroomish Friendship", player)
    )
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Bonsly",
        lambda state: state.has("Bonsly Friendship", player)
    )
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Lotad",
        lambda state: state.has("Lotad Friendship", player)
    )
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Weedle",
        lambda state: state.has("Weedle Friendship", player)
    )
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Caterpie",
        lambda state: state.has("Caterpie Friendship", player)
    )
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Magikarp",
        lambda state: state.has("Magikarp Friendship", player)
    )
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Jolteon",
        lambda state: state.has("Jolteon Friendship", player)
    )
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Arcanine",
        lambda state: state.has("Arcanine Friendship", player)
    )
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Leafeon",
        lambda state: state.has("Leafeon Friendship", player)
    )
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Scyther",
        lambda state: state.has("Scyther Friendship", player)
    )
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Ponyta",
        lambda state: state.has("Ponyta Friendship", player)
    )
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Shinx",
        lambda state: state.has("Shinx Friendship", player)
    )
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Eevee",
        lambda state: state.has("Eevee Friendship", player)
    )
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Pachirisu",
        lambda state: state.has("Pachirisu Friendship", player)
    )
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Buneary",
        lambda state: state.has("Buneary Friendship", player)
    )
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Croagunk",
        lambda state: state.has("Croagunk Friendship", player)
    )
    set_rule_if_exists(
        "Bulbasaur's Daring Dash Attraction -- Mew",
        lambda state: state.has("Mew Friendship", player)
    )
    # Venusaur
    set_rule_if_exists(
        "Meadow Zone Venusaur Area - Venusaur -- Friendship",
        lambda state: state.has("Venusaur Prisma", player) and state.has("Empoleon Prisma", player) and state.has(
            "Blaziken Prisma", player
        )
    )

    # Venusaur's Vine Swing
    set_rule_if_exists(
        "Venusaur's Vine Swing Attraction -- Prisma",
        lambda state: can_beat_any_venusaur_vine_swing_record(state, player)
    )
    set_rule_if_exists(
        "Venusaur's Vine Swing Attraction -- Pikachu",
        lambda state: True
    )
    set_rule_if_exists(
        "Venusaur's Vine Swing Attraction -- Munchlax",
        lambda state: state.has("Munchlax Friendship", player)
    )
    set_rule_if_exists(
        "Venusaur's Vine Swing Attraction -- Magikarp",
        lambda state: state.has("Magikarp Friendship", player)
    )
    set_rule_if_exists(
        "Venusaur's Vine Swing Attraction -- Blaziken",
        lambda state: state.has("Blaziken Friendship", player)
    )
    set_rule_if_exists(
        "Venusaur's Vine Swing Attraction -- Infernape",
        lambda state: state.has("Infernape Friendship", player)
    )
    set_rule_if_exists(
        "Venusaur's Vine Swing Attraction -- Lucario",
        lambda state: state.has("Lucario Friendship", player)
    )
    set_rule_if_exists(
        "Venusaur's Vine Swing Attraction -- Primeape",
        lambda state: state.has("Primeape Friendship", player)
    )
    set_rule_if_exists(
        "Venusaur's Vine Swing Attraction -- Tangrowth",
        lambda state: state.has("Tangrowth Friendship", player)
    )
    set_rule_if_exists(
        "Venusaur's Vine Swing Attraction -- Ambipom",
        lambda state: state.has("Ambipom Friendship", player)
    )
    set_rule_if_exists(
        "Venusaur's Vine Swing Attraction -- Croagunk",
        lambda state: state.has("Croagunk Friendship", player)
    )
    set_rule_if_exists(
        "Venusaur's Vine Swing Attraction -- Mankey",
        lambda state: state.has("Mankey Friendship", player)
    )
    set_rule_if_exists(
        "Venusaur's Vine Swing Attraction -- Aipom",
        lambda state: state.has("Aipom Friendship", player)
    )
    set_rule_if_exists(
        "Venusaur's Vine Swing Attraction -- Chimchar",
        lambda state: state.has("Chimchar Friendship", player)
    )
    set_rule_if_exists(
        "Venusaur's Vine Swing Attraction -- Treecko",
        lambda state: state.has("Treecko Friendship", player)
    )
    set_rule_if_exists(
        "Venusaur's Vine Swing Attraction -- Pachirisu",
        lambda state: state.has("Pachirisu Friendship", player)
    )
    set_rule_if_exists(
        "Venusaur's Vine Swing Attraction -- Jirachi",
        lambda state: state.has("Jirachi Friendship", player)
    )
    set_rule_if_exists(
        "Venusaur's Vine Swing Attraction -- Jirachi Friendship",
        lambda state: can_beat_all_venusaur_vine_swing_records(state, player)
    )
    # Beach Zone
    set_rule_if_exists(
        "Beach Zone Main Area - Buizel Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Buizel Power Competition -- Floatzel Unlocked",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Psyduck Power Competition -- Friendship",
        lambda state: True
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Psyduck Power Competition -- Golduck Unlocked",
        lambda state: True
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Slowpoke Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Slowpoke Power Competition -- Mudkip Unlocked",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Azurill Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Azurill Power Competition -- Totodile Unlocked",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Totodile Power Competition -- Friendship",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Pidgeotto Power Competition -- Friendship",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Corsola Power Competition -- Friendship",
        lambda state: True
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Floatzel Power Competition -- Friendship",
        lambda state: can_battle(state, player) and state.has("Floatzel Unlock", player)
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Vaporeon Power Competition -- Friendship",
        lambda state: can_play_catch(state, player) and state.count_group("Friendship Items", player) >= 30
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Golduck Power Competition -- Friendship",
        lambda state: can_battle(state, player) and state.has("Golduck Unlock", player)
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Wailord Power Competition -- Friendship",
        lambda state: True
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Feraligatr Power Competition -- Friendship",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Blastoise Power Competition -- Friendship",
        lambda state: can_battle(state, player) and state.has("Blastoise Unlock", player)
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Bottle Recycling -- Stage 1",
        lambda state: True
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Bottle Recycling -- Stage 2",
        lambda state: True
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Bottle Recycling -- Stage 2 --- Krabby Unlocked",
        lambda state: True
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Bottle Recycling -- Stage 3",
        lambda state: True
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Bottle Recycling -- Stage 4",
        lambda state: True
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Bottle Recycling -- Stage 4 --- Corphish Unlocked",
        lambda state: True
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Bottle Recycling -- Stage 5",
        lambda state: True
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Bottle Recycling -- Stage 6",
        lambda state: True
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Krabby Power Competition -- Friendship",
        lambda state: can_play_catch(state, player) and state.has("Krabby Unlock", player)
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Starly Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Mudkip Power Competition -- Friendship",
        lambda state: can_play_catch(state, player) and state.has("Mudkip Unlock", player)
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Taillow Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Staravia Power Competition -- Friendship",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Beach Zone Main Area - Wingull Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )

    set_rule_if_exists(
        "Beach Zone Main Area - Pelipper -- Friendship",
        lambda state: state.has("Pelipper Prisma", player)
    )

    set_rule_if_exists(
        "Beach Zone Recycle Area - Gyarados -- Friendship",
        lambda state: state.has("Gyarados Prisma", player)
    )

    # Pelipper's Circle Circuit Attraction
    set_rule_if_exists(
        "Pelipper's Circle Circuit Attraction -- Prisma",
        lambda state: can_beat_any_pelipper_circle_circuit_record(state, player)
    )
    set_rule_if_exists(
        "Pelipper's Circle Circuit Attraction -- Pikachu",
        lambda state: state.has("Pikachu Balloon", player)
    )
    set_rule_if_exists(
        "Pelipper's Circle Circuit Attraction -- Staraptor",
        lambda state: state.has("Staraptor Friendship", player)
    )
    set_rule_if_exists(
        "Pelipper's Circle Circuit Attraction -- Togekiss",
        lambda state: state.has("Togekiss Friendship", player)
    )
    set_rule_if_exists(
        "Pelipper's Circle Circuit Attraction -- Honchkrow",
        lambda state: state.has("Honchkrow Friendship", player)
    )
    set_rule_if_exists(
        "Pelipper's Circle Circuit Attraction -- Gliscor",
        lambda state: state.has("Gliscor Friendship", player)
    )
    set_rule_if_exists(
        "Pelipper's Circle Circuit Attraction -- Pelipper",
        lambda state: state.has("Pelipper Friendship", player)
    )
    set_rule_if_exists(
        "Pelipper's Circle Circuit Attraction -- Staravia",
        lambda state: state.has("Staravia Friendship", player)
    )
    set_rule_if_exists(
        "Pelipper's Circle Circuit Attraction -- Pidgeotto",
        lambda state: state.has("Pidgeotto Friendship", player)
    )
    set_rule_if_exists(
        "Pelipper's Circle Circuit Attraction -- Butterfree",
        lambda state: state.has("Butterfree Friendship", player)
    )
    set_rule_if_exists(
        "Pelipper's Circle Circuit Attraction -- Tropius",
        lambda state: state.has("Tropius Friendship", player)
    )
    set_rule_if_exists(
        "Pelipper's Circle Circuit Attraction -- Murkrow",
        lambda state: state.has("Murkrow Friendship", player)
    )
    set_rule_if_exists(
        "Pelipper's Circle Circuit Attraction -- Taillow",
        lambda state: state.has("Taillow Friendship", player)
    )
    set_rule_if_exists(
        "Pelipper's Circle Circuit Attraction -- Spearow",
        lambda state: state.has("Spearow Friendship", player)
    )
    set_rule_if_exists(
        "Pelipper's Circle Circuit Attraction -- Starly",
        lambda state: state.has("Starly Friendship", player)
    )
    set_rule_if_exists(
        "Pelipper's Circle Circuit Attraction -- Wingull",
        lambda state: state.has("Wingull Friendship", player)
    )
    set_rule_if_exists(
        "Pelipper's Circle Circuit Attraction -- Latias",
        lambda state: state.has("Latias Friendship", player)
    )
    set_rule_if_exists(
        "Pelipper's Circle Circuit Attraction -- Latias Friendship",
        lambda state: can_beat_all_pelipper_circle_circuit_records(state, player)
    )

    # Gyarado's Aqua Dash
    set_rule_if_exists(
        "Gyarado's Aqua Dash Attraction -- Prisma",
        lambda state: can_beat_any_gyarados_aqua_dash_record(state, player)
    )
    set_rule_if_exists(
        "Gyarado's Aqua Dash Attraction -- Pikachu",
        lambda state: state.has("Pikachu Surfboard", player)
    )
    set_rule_if_exists(
        "Gyarado's Aqua Dash Attraction -- Psyduck",
        lambda state: state.has("Psyduck Friendship", player)
    )
    set_rule_if_exists(
        "Gyarado's Aqua Dash Attraction -- Azurill",
        lambda state: state.has("Azurill Friendship", player)
    )
    set_rule_if_exists(
        "Gyarado's Aqua Dash Attraction -- Slowpoke",
        lambda state: state.has("Slowpoke Friendship", player)
    )
    set_rule_if_exists(
        "Gyarado's Aqua Dash Attraction -- Empoleon",
        lambda state: state.has("Empoleon Friendship", player)
    )
    set_rule_if_exists(
        "Gyarado's Aqua Dash Attraction -- Floatzel",
        lambda state: state.has("Floatzel Friendship", player)
    )
    set_rule_if_exists(
        "Gyarado's Aqua Dash Attraction -- Feraligatr",
        lambda state: state.has("Feraligatr Friendship", player)
    )
    set_rule_if_exists(
        "Gyarado's Aqua Dash Attraction -- Golduck",
        lambda state: state.has("Golduck Friendship", player)
    )
    set_rule_if_exists(
        "Gyarado's Aqua Dash Attraction -- Vaporeon",
        lambda state: state.has("Vaporeon Friendship", player)
    )
    set_rule_if_exists(
        "Gyarado's Aqua Dash Attraction -- Prinplup",
        lambda state: state.has("Prinplup Friendship", player)
    )
    set_rule_if_exists(
        "Gyarado's Aqua Dash Attraction -- Bibarel",
        lambda state: state.has("Bibarel Friendship", player)
    )
    set_rule_if_exists(
        "Gyarado's Aqua Dash Attraction -- Buizel",
        lambda state: state.has("Buizel Friendship", player)
    )
    set_rule_if_exists(
        "Gyarado's Aqua Dash Attraction -- Corsola",
        lambda state: state.has("Corsola Friendship", player)
    )
    set_rule_if_exists(
        "Gyarado's Aqua Dash Attraction -- Piplup",
        lambda state: state.has("Piplup Friendship", player)
    )
    set_rule_if_exists(
        "Gyarado's Aqua Dash Attraction -- Lotad",
        lambda state: state.has("Lotad Friendship", player)
    )
    set_rule_if_exists(
        "Gyarado's Aqua Dash Attraction -- Manaphy",
        lambda state: state.has("Manaphy Friendship", player)
    )
    set_rule_if_exists(
        "Gyarado's Aqua Dash Attraction -- Manaphy Friendship",
        lambda state: can_beat_all_gyarados_aqua_dash_records(state, player)
    )
    # Ice Zone
    set_rule_if_exists(
        "Ice Zone Main Area - Lapras -- Friendship",
        lambda state: True
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Spheal Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Octillery Power Competition -- Friendship",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Delibird -- Friendship",
        lambda state: True  # Todo: Delibird Logic needs to be checked and rewritten
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Smoochum Power Competition -- Friendship",
        lambda state: can_battle(state, player) and state.has("Smoochum Unlock", player)
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Squirtle Power Competition -- Friendship",
        lambda state: can_battle(state, player) and state.has("Squirtle Unlock", player)
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Glaceon Power Competition -- Friendship",
        lambda state: can_play_catch(state, player) and state.count_group("Friendship Items", player) >= 50
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Prinplup Power Competition -- Friendship",
        lambda state: can_battle(state, player)  # TODO: dependency on Igloo Quest?
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Sneasel Power Competition -- Friendship",
        lambda state: can_play_catch(state, player) and state.has("Sneasel Unlock", player)
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Piloswine Power Competition -- Friendship",
        lambda state: can_battle_thunderbolt_immune(state, player)
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Glalie -- Friendship",
        lambda state: state.has("Glalie Unlock", player)
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Primeape Power Competition -- Friendship",
        lambda state: can_battle(state, player) and state.has("Primeape Unlock", player)
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Ursaring Power Competition -- Friendship",
        lambda state: can_battle(state, player) and state.has("Ursaring Unlock", player)
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Mamoswine Power Competition -- Friendship",
        lambda state: can_battle_thunderbolt_immune(state, player) and state.has("Mamoswine Unlock", player)
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Kirlia Power Competition -- Friendship",
        lambda state: state.has("Delibird Friendship", player)
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Igloo Quest -- Stage 1",
        lambda state: state.has("Glalie Unlock", player)
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Igloo Quest -- Stage 1 -- Primeape Unlocked",
        lambda state: state.has("Glalie Unlock", player)
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Igloo Quest -- Stage 2",
        lambda state: state.has("Glalie Unlock", player)
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Igloo Quest -- Stage 2 -- Ursaring Unlocked",
        lambda state: state.has("Glalie Unlock", player)
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Igloo Quest -- Stage 3",
        lambda state: state.has("Glalie Unlock", player)
    )

    set_rule_if_exists(
        "Ice Zone Main Area - Christmas Tree Present Quest -- Stage 1",
        lambda state: state.has("Delibird Unlock", player) and state.has("Spheal Friendship", player)
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Christmas Tree Present Quest -- Stage 2",
        lambda state: state.has("Delibird Unlock", player) and
                      state.has("Spheal Friendship", player) and
                      state.has("Teddiursa Friendship", player)
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Christmas Tree Present Quest -- Stage 3",
        lambda state: state.has("Delibird Unlock", player) and
                      state.has("Spheal Friendship", player) and
                      state.has("Teddiursa Friendship", player) and
                      state.has("Squirtle Unlock", player) and
                      state.has("Squirtle Friendship", player)
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Christmas Tree Present Quest -- Stage 4",
        lambda state: state.has("Delibird Unlock", player) and
                      state.has("Spheal Friendship", player) and
                      state.has("Teddiursa Friendship", player) and
                      state.has("Squirtle Unlock", player) and
                      state.has("Squirtle Friendship", player) and
                      state.has("Smoochum Friendship", player) and
                      state.has("Smoochum Unlock", player)
    )
    set_rule_if_exists(
        "Ice Zone Frozen Lake Area - Frozen Mamoswine -- Ice Rescue",
        lambda state: state.has("Ice Zone Frozen Lake Unlock", player) and can_dash_overworld(state, player)
    )
    set_rule_if_exists(
        "Ice Zone Lower Lift Area - Froslass Power Competition -- Friendship",
        lambda state: state.has("Ice Zone Lift Unlock", player) and can_battle(state, player)
    )
    set_rule_if_exists(
        "Ice Zone Empoleon Area - Empoleon -- Friendship",
        lambda state: state.has("Empoleon Prisma", player)
    )

    set_rule_if_exists(
        "Ice Zone Lower Lift Area - Quagsire -- Friendship",
        lambda state: can_destroy_objects_overworld(state, player)
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Starly Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Krabby Power Competition -- Friendship",
        lambda state: can_play_catch(state, player) and state.has("Krabby Unlock", player)
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Corphish Power Competition -- Friendship",
        lambda state: can_battle(state, player) and state.has("Corphish Unlock", player)
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Mudkip Power Competition -- Friendship",
        lambda state: state.has("Mudkip Unlock", player)
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Taillow Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Staravia Power Competition -- Friendship",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Teddiursa Power Competition -- Friendship",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Ice Zone Main Area - Wingull Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    # Empoleon's Snow Slide
    set_rule_if_exists(
        "Empoleon's Snow Slide Attraction -- Prisma",
        lambda state: can_beat_any_empoleon_snow_slide_record(state, player)
    )
    set_rule_if_exists(
        "Empoleon's Snow Slide Attraction -- Pikachu",
        lambda state: state.has("Pikachu Snowboard", player)
    )
    set_rule_if_exists(
        "Empoleon's Snow Slide Attraction -- Teddiursa",
        lambda state: state.has("Teddiursa Friendship", player)
    )
    set_rule_if_exists(
        "Empoleon's Snow Slide Attraction -- Magikarp",
        lambda state: state.has("Magikarp Friendship", player)
    )
    set_rule_if_exists(
        "Empoleon's Snow Slide Attraction -- Empoleon",
        lambda state: state.has("Empoleon Friendship", player)
    )
    set_rule_if_exists(
        "Empoleon's Snow Slide Attraction -- Glaceon",
        lambda state: state.has("Glaceon Friendship", player)
    )
    set_rule_if_exists(
        "Empoleon's Snow Slide Attraction -- Blastoise",
        lambda state: state.has("Blastoise Friendship", player)
    )
    set_rule_if_exists(
        "Empoleon's Snow Slide Attraction -- Glalie",
        lambda state: state.has("Glalie Friendship", player)
    )
    set_rule_if_exists(
        "Empoleon's Snow Slide Attraction -- Lapras",
        lambda state: state.has("Lapras Friendship", player)
    )
    set_rule_if_exists(
        "Empoleon's Snow Slide Attraction -- Delibird",
        lambda state: state.has("Delibird Friendship", player)
    )
    set_rule_if_exists(
        "Empoleon's Snow Slide Attraction -- Piloswine",
        lambda state: state.has("Piloswine Friendship", player)
    )
    set_rule_if_exists(
        "Empoleon's Snow Slide Attraction -- Prinplup",
        lambda state: state.has("Prinplup Friendship", player)
    )
    set_rule_if_exists(
        "Empoleon's Snow Slide Attraction -- Squirtle",
        lambda state: state.has("Squirtle Friendship", player)
    )
    set_rule_if_exists(
        "Empoleon's Snow Slide Attraction -- Piplup",
        lambda state: state.has("Piplup Friendship", player)
    )
    set_rule_if_exists(
        "Empoleon's Snow Slide Attraction -- Quagsire",
        lambda state: state.has("Quagsire Friendship", player)
    )

    set_rule_if_exists(
        "Empoleon's Snow Slide Attraction -- Spheal",
        lambda state: state.has("Spheal Friendship", player)
    )
    set_rule_if_exists(
        "Empoleon's Snow Slide Attraction -- Suicune",
        lambda state: state.has("Suicune Friendship", player)
    )
    set_rule_if_exists(
        "Empoleon's Snow Slide Attraction -- Suicune Friendship",
        lambda state: can_beat_all_empoleon_snow_slide_records(state, player)
    )
    # Cavern Zone
    set_rule_if_exists(
        "Cavern Zone Main Area - Magnemite -- Friendship",
        lambda state: state.has("Magnemite Unlock", player)
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Machamp Power Competition -- Friendship",
        lambda state: True
    )

    set_rule_if_exists(
        "Cavern Zone Main Area - Machamp Power Competition -- Machamp Unlocked",
        lambda state: True
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Cranidos Power Competition -- Friendship",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Zubat Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Golbat Power Competition -- Friendship",
        lambda state: can_play_catch_intermediate(state, player)
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Magnezone Power Competition -- Friendship",
        lambda state: state.has("Magnezone Unlock", player) and can_battle_thunderbolt_immune(state, player)
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Scizor Power Competition -- Friendship",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Dugtrio Power Competition -- Friendship",
        lambda state: True
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Gible Power Competition -- Friendship",
        lambda state: can_battle_thunderbolt_immune(state, player)
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Phanpy Power Competition -- Friendship",
        lambda state: can_destroy_objects_overworld(state, player) and state.has("Phanpy Unlock", player)
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Hitmonlee Power Competition -- Friendship",
        lambda state: can_battle(state, player) and state.has("Hitmonlee Unlock", player)
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Electivire Power Competition -- Friendship",
        lambda state: can_battle(state, player) and state.has("Electivire Unlock", player)
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Magnemite Crate Entrance -- Magnemite Unlocked",
        lambda state: can_destroy_objects_overworld(state, player)
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Magnemite Crate Magma Zone Entrance -- Magnemite Unlocked",
        lambda state: can_destroy_objects_overworld(state, player)
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Magnemite Crate Deep Inside -- Magnemite Unlocked",
        lambda state: can_destroy_objects_overworld(state, player)
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Diglett Crate -- Diglett Unlocked",
        lambda state: can_destroy_objects_overworld(state, player)
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Bonsly Power Competition -- Friendship",
        lambda state: True
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Bonsly Power Competition -- Sudowoodo Unlocked",
        lambda state: True
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Teddiursa Power Competition -- Friendship",
        lambda state: True
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Chimchar Power Competition -- Friendship",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Sudowoodo Power Competition -- Friendship",
        lambda state: True
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Aron Power Competition -- Friendship",
        lambda state: can_destroy_objects_overworld(state, player)
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Torchic Power Competition -- Friendship",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Geodude Power Competition -- Friendship",
        lambda state: True
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Raichu Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Meowth Power Competition -- Friendship",
        lambda state: True
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Marowak Power Competition -- Friendship",
        lambda state: can_battle_thunderbolt_immune(state, player)
    )
    set_rule_if_exists(
        "Cavern Zone Main Area - Mawile Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    # Bastiodon's Panel Crush

    set_rule_if_exists(
        "Bastiodon's Panel Crush Attraction -- Prisma",
        lambda state: can_beat_any_bastiodon_panel_crush_record(state, player)
    )
    set_rule_if_exists(
        "Bastiodon's Panel Crush Attraction -- Pikachu",
        lambda state: True
    )
    set_rule_if_exists(
        "Bastiodon's Panel Crush Attraction -- Sableye",
        lambda state: state.has("Sableye Friendship", player)
    )
    set_rule_if_exists(
        "Bastiodon's Panel Crush Attraction -- Meowth",
        lambda state: state.has("Meowth Friendship", player)
    )
    set_rule_if_exists(
        "Bastiodon's Panel Crush Attraction -- Torchic",
        lambda state: state.has("Torchic Friendship", player)
    )
    set_rule_if_exists(
        "Bastiodon's Panel Crush Attraction -- Electivire",
        lambda state: state.has("Electivire Friendship", player)
    )
    set_rule_if_exists(
        "Bastiodon's Panel Crush Attraction -- Magmortar",
        lambda state: state.has("Magmortar Friendship", player)
    )
    set_rule_if_exists(
        "Bastiodon's Panel Crush Attraction -- Hitmonlee",
        lambda state: state.has("Hitmonlee Friendship", player)
    )
    set_rule_if_exists(
        "Bastiodon's Panel Crush Attraction -- Ursaring",
        lambda state: state.has("Ursaring Friendship", player)
    )
    set_rule_if_exists(
        "Bastiodon's Panel Crush Attraction -- Mr. Mime",
        lambda state: state.has("Mr. Mime Friendship", player)
    )
    set_rule_if_exists(
        "Bastiodon's Panel Crush Attraction -- Raichu",
        lambda state: state.has("Raichu Friendship", player)
    )
    set_rule_if_exists(
        "Bastiodon's Panel Crush Attraction -- Sudowoodo",
        lambda state: state.has("Sudowoodo Friendship", player)
    )
    set_rule_if_exists(
        "Bastiodon's Panel Crush Attraction -- Charmander",
        lambda state: state.has("Charmander Friendship", player)
    )
    set_rule_if_exists(
        "Bastiodon's Panel Crush Attraction -- Gible",
        lambda state: state.has("Gible Friendship", player)
    )
    set_rule_if_exists(
        "Bastiodon's Panel Crush Attraction -- Chimchar",
        lambda state: state.has("Chimchar Friendship", player)
    )
    set_rule_if_exists(
        "Bastiodon's Panel Crush Attraction -- Magby",
        lambda state: state.has("Magby Friendship", player)
    )
    set_rule_if_exists(
        "Bastiodon's Panel Crush Attraction -- Metagross",
        lambda state: state.has("Metagross Friendship", player)
    )
    set_rule_if_exists(
        "Bastiodon's Panel Crush Attraction -- Metagross Friendship",
        lambda state: can_beat_all_bastiodon_panel_crush_records(state, player)
    )

    # Magma Zone
    set_rule_if_exists(
        "Magma Zone Main Area - Camerupt Power Competition -- Friendship",
        lambda state: can_battle_thunderbolt_immune(state, player)
    )
    set_rule_if_exists(
        "Magma Zone Main Area - Magby Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Magma Zone Main Area - Vulpix Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Magma Zone Main Area - Vulpix Power Competition -- Ninetales Unlocked",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Magma Zone Main Area - Drill -- Torkoal Unlocked",
        lambda state: can_dash_overworld(state, player)
    )
    set_rule_if_exists(
        "Magma Zone Main Area - Furnace -- Golem Unlocked",
        lambda state: can_dash_overworld(state, player)
    )
    set_rule_if_exists(
        "Magma Zone Circle Area - Charmander Power Competition -- Friendship",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Magma Zone Circle Area - Ninetales Power Competition -- Friendship",
        lambda state: can_play_catch_intermediate(state, player)
    )
    set_rule_if_exists(
        "Magma Zone Circle Area - Quilava Power Competition -- Friendship",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Magma Zone Circle Area - Flareon Power Competition -- Friendship",
        lambda state: can_battle(state, player) and state.count_group("Friendship Items", player) >= 60
    )
    set_rule_if_exists(
        "Magma Zone Circle Area - Infernape Power Competition -- Friendship",
        lambda state: can_battle(state, player) and state.has("Infernape Unlock", player)
    )
    set_rule_if_exists(
        "Magma Zone Circle Area - Farfetch'd Power Competition -- Friendship",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Magma Zone Circle Area - Ponyta Power Competition -- Friendship",
        lambda state: can_play_catch_intermediate(state, player)
    )
    set_rule_if_exists(
        "Magma Zone Main Area - Torkoal Power Competition -- Friendship",
        lambda state: can_battle(state, player) and state.has("Torkoal Unlock", player)
    )
    set_rule_if_exists(
        "Magma Zone Main Area - Golem Power Competition -- Friendship",
        lambda state: state.has("Golem Unlock", player)
    )
    set_rule_if_exists(
        "Magma Zone Circle Area - Hitmonchan Power Competition -- Friendship",
        lambda state: can_battle(state, player) and state.has("Hitmonchan Unlock", player)
    )
    set_rule_if_exists(
        "Magma Zone Circle Area - Hitmonchan Power Competition -- Hitmonlee Unlocked",
        lambda state: can_battle(state, player) and state.has("Hitmonchan Unlock", player)
    )
    set_rule_if_exists(
        "Magma Zone Main Area - Hitmontop Power Competition -- Friendship",
        lambda state: can_dash_overworld(state, player)
    )
    set_rule_if_exists(
        "Magma Zone Circle Area - Magmortar Power Competition -- Friendship",
        lambda state: can_battle(state, player) and state.has("Magmortar Unlock", player)
    )
    set_rule_if_exists(
        "Magma Zone Main Area - Blaziken Power Competition -- Friendship",
        lambda state: state.has("Rayquaza Prisma", player)
    )
    set_rule_if_exists(
        "Magma Zone Circle Area - Rhyperior Iron Disc -- Quest",
        lambda state: can_dash_overworld(state, player)
    )
    set_rule_if_exists(
        "Magma Zone Main Area - Baltoy Crate -- Baltoy Unlocked",
        lambda state: can_destroy_objects_overworld(state, player)
    )
    set_rule_if_exists(
        "Magma Zone Main Area - Bonsly Power Competition -- Friendship",
        lambda state: True
    )
    set_rule_if_exists(
        "Magma Zone Main Area - Chimchar Power Competition -- Friendship",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Magma Zone Main Area - Chimchar Power Competition -- Infernape Unlocked",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Magma Zone Main Area - Aron Power Competition -- Friendship",
        lambda state: can_dash_overworld(state, player)
    )
    set_rule_if_exists(
        "Magma Zone Main Area - Torchic Power Competition -- Friendship",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Magma Zone Main Area - Geodude Power Competition -- Friendship",
        lambda state: True
    )
    set_rule_if_exists(
        "Magma Zone Main Area - Baltoy Power Competition -- Friendship",
        lambda state: can_battle_thunderbolt_immune(state, player) and state.has("Baltoy Unlock", player)
    )
    set_rule_if_exists(
        "Magma Zone Main Area - Baltoy Power Competition -- Claydol Unlocked",
        lambda state: can_battle_thunderbolt_immune(state, player) and state.has("Baltoy Unlock", player)
    )
    set_rule_if_exists(
        "Magma Zone Circle Area - Meditite Power Competition -- Friendship",
        lambda state: True
    )

    # Rhyperior's Bumper Burn
    set_rule_if_exists(
        "Rhyperior's Bumper Burn Attraction -- Prisma",
        lambda state: can_beat_any_rhyperior_bumper_burn_record(state, player)
    )
    set_rule_if_exists(
        "Rhyperior's Bumper Burn Attraction -- Pikachu",
        lambda state: True
    )
    set_rule_if_exists(
        "Rhyperior's Bumper Burn Attraction -- Magnemite",
        lambda state: state.has("Magnemite Friendship", player)
    )
    set_rule_if_exists(
        "Rhyperior's Bumper Burn Attraction -- Rhyperior",
        lambda state: state.has("Rhyperior Friendship", player)
    )
    set_rule_if_exists(
        "Rhyperior's Bumper Burn Attraction -- Tyranitar",
        lambda state: state.has("Tyranitar Friendship", player)
    )
    set_rule_if_exists(
        "Rhyperior's Bumper Burn Attraction -- Hitmontop",
        lambda state: state.has("Hitmontop Friendship", player)
    )
    set_rule_if_exists(
        "Rhyperior's Bumper Burn Attraction -- Flareon",
        lambda state: state.has("Flareon Friendship", player)
    )
    set_rule_if_exists(
        "Rhyperior's Bumper Burn Attraction -- Venusaur",
        lambda state: state.has("Venusaur Friendship", player)
    )
    set_rule_if_exists(
        "Rhyperior's Bumper Burn Attraction -- Snorlax",
        lambda state: state.has("Snorlax Friendship", player)
    )
    set_rule_if_exists(
        "Rhyperior's Bumper Burn Attraction -- Torterra",
        lambda state: state.has("Torterra Friendship", player)
    )
    set_rule_if_exists(
        "Rhyperior's Bumper Burn Attraction -- Magnezone",
        lambda state: state.has("Magnezone Friendship", player)
    )
    set_rule_if_exists(
        "Rhyperior's Bumper Burn Attraction -- Claydol",
        lambda state: state.has("Claydol Friendship", player)
    )
    set_rule_if_exists(
        "Rhyperior's Bumper Burn Attraction -- Quilava",
        lambda state: state.has("Quilava Friendship", player)
    )
    set_rule_if_exists(
        "Rhyperior's Bumper Burn Attraction -- Torkoal",
        lambda state: state.has("Torkoal Friendship", player)
    )
    set_rule_if_exists(
        "Rhyperior's Bumper Burn Attraction -- Baltoy",
        lambda state: state.has("Baltoy Friendship", player)
    )
    set_rule_if_exists(
        "Rhyperior's Bumper Burn Attraction -- Bonsly",
        lambda state: state.has("Bonsly Friendship", player)
    )
    set_rule_if_exists(
        "Rhyperior's Bumper Burn Attraction -- Heatran",
        lambda state: state.has("Heatran Friendship", player)
    )
    set_rule_if_exists(
        "Rhyperior's Bumper Burn Attraction -- Heatran Friendship",
        lambda state: can_beat_all_rhyperior_bumper_burn_records(state, player)
    )

    # Blaziken's Boulder Bash
    set_rule_if_exists(
        "Blaziken's Boulder Bash Attraction -- Prisma",
        lambda state: can_beat_any_blaziken_boulder_bash_record(state, player)
    )
    set_rule_if_exists(
        "Blaziken's Boulder Bash Attraction -- Pikachu",
        lambda state: True
    )
    set_rule_if_exists(
        "Blaziken's Boulder Bash Attraction -- Geodude",
        lambda state: state.has("Geodude Friendship", player)
    )
    set_rule_if_exists(
        "Blaziken's Boulder Bash Attraction -- Phanpy",
        lambda state: state.has("Geodude Friendship", player)
    )
    set_rule_if_exists(
        "Blaziken's Boulder Bash Attraction -- Blaziken",
        lambda state: state.has("Blaziken Friendship", player)
    )
    set_rule_if_exists(
        "Blaziken's Boulder Bash Attraction -- Garchomp",
        lambda state: state.has("Garchomp Friendship", player)
    )
    set_rule_if_exists(
        "Blaziken's Boulder Bash Attraction -- Scizor",
        lambda state: state.has("Scizor Friendship", player)
    )
    set_rule_if_exists(
        "Blaziken's Boulder Bash Attraction -- Magmortar",
        lambda state: state.has("Magmortar Friendship", player)
    )
    set_rule_if_exists(
        "Blaziken's Boulder Bash Attraction -- Hitmonchan",
        lambda state: state.has("Hitmonchan Friendship", player)
    )
    set_rule_if_exists(
        "Blaziken's Boulder Bash Attraction -- Machamp",
        lambda state: state.has("Machamp Friendship", player)
    )
    set_rule_if_exists(
        "Blaziken's Boulder Bash Attraction -- Marowak",
        lambda state: state.has("Marowak Friendship", player)
    )
    set_rule_if_exists(
        "Blaziken's Boulder Bash Attraction -- Farfetch'd",
        lambda state: state.has("Farfetch'd Friendship", player)
    )
    set_rule_if_exists(
        "Blaziken's Boulder Bash Attraction -- Cranidos",
        lambda state: state.has("Cranidos Friendship", player)
    )
    set_rule_if_exists(
        "Blaziken's Boulder Bash Attraction -- Camerupt",
        lambda state: state.has("Camerupt Friendship", player)
    )
    set_rule_if_exists(
        "Blaziken's Boulder Bash Attraction -- Bastiodon",
        lambda state: state.has("Bastiodon Friendship", player)
    )
    set_rule_if_exists(
        "Blaziken's Boulder Bash Attraction -- Mawile",
        lambda state: state.has("Mawile Friendship", player)
    )
    set_rule_if_exists(
        "Blaziken's Boulder Bash Attraction -- Groudon",
        lambda state: state.has("Groudon Friendship", player)
    )
    set_rule_if_exists(
        "Blaziken's Boulder Bash Attraction -- Groudon Friendship",
        lambda state: can_beat_all_blaziken_boulder_bash_records(state, player)
    )

    # Haunted Zone
    set_rule_if_exists(
        "Haunted Zone Main Area - Murkrow Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Haunted Zone Main Area - Murkrow Power Competition -- Honchkrow Unlocked",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Haunted Zone Main Area - Hunchkrow Power Competition -- Friendship",
        lambda state: can_battle(state, player) and state.has("Hunchkrow Unlock")
    )
    set_rule_if_exists(
        "Haunted Zone Main Area - Gliscor Power Competition -- Friendship",
        lambda state: can_battle_thunderbolt_immune(state, player)
    )
    set_rule_if_exists(
        "Haunted Zone Main Area - Metapod Power Competition -- Friendship",
        lambda state: state.has("Rotom Prisma", player) and state.has("Metapod Unlock", player)
    )
    set_rule_if_exists(
        "Haunted Zone Main Area - Kakuna Power Competition -- Friendship",
        lambda state: state.has("Rotom Prisma", player) and state.has("Kakuna Unlock", player)
    )
    set_rule_if_exists(
        "Haunted Zone Main Area - Metapod Left Tree -- Metapod Unlocked",
        lambda state: can_dash_overworld(state, player)
    )
    set_rule_if_exists(
        "Haunted Zone Main Area - Kakuna Right Tree -- Metapod Unlocked",
        lambda state: can_dash_overworld(state, player)
    )
    set_rule_if_exists(
        "Haunted Zone Main Area - Raichu Power Competition -- Friendship",
        lambda state: can_play_catch_intermediate(state, player)
    )
    set_rule_if_exists(
        "Haunted Zone Main Area - Meowth Power Competition -- Friendship",
        lambda state: True
    )
    set_rule_if_exists(
        "Haunted Zone Main Area - Aipom Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Haunted Zone Main Area - Aipom Power Competition -- Ambipom Unlocked",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Haunted Zone Main Area - Ambipom Power Competition -- Friendship",
        lambda state: can_play_catch(state, player) and state.has("Ambipom Unlock", player)
    )
    set_rule_if_exists(
        "Haunted Zone Main Area - Drifloon Power Competition -- Friendship",
        lambda state: True
    )
    set_rule_if_exists(
        "Haunted Zone Main Area - Tangrowth -- Friendship",
        lambda state: state.has("Tangrowth Prisma", player)
    )
    # Tangrowth's Swing-Along
    set_rule_if_exists(
        "Tangrowth's Swing-Along Attraction -- Prisma",
        lambda state: can_beat_any_tangrowth_swing_along_record(state, player)
    )
    set_rule_if_exists(
        "Tangrowth's Swing-Along Attraction -- Pikachu",
        lambda state: True
    )
    set_rule_if_exists(
        "Tangrowth's Swing-Along Attraction -- Meowth",
        lambda state: state.has("Meowth Friendship", player)
    )
    set_rule_if_exists(
        "Tangrowth's Swing-Along Attraction -- Pichu",
        lambda state: state.has("Pichu Friendship", player)
    )
    set_rule_if_exists(
        "Tangrowth's Swing-Along Attraction -- Lucario",
        lambda state: state.has("Lucario Friendship", player)
    )
    set_rule_if_exists(
        "Tangrowth's Swing-Along Attraction -- Infernape",
        lambda state: state.has("Infernape Friendship", player)
    )
    set_rule_if_exists(
        "Tangrowth's Swing-Along Attraction -- Blaziken",
        lambda state: state.has("Blaziken Friendship", player)
    )
    set_rule_if_exists(
        "Tangrowth's Swing-Along Attraction -- Riolu",
        lambda state: state.has("Riolu Friendship", player)
    )
    set_rule_if_exists(
        "Tangrowth's Swing-Along Attraction -- Sneasel",
        lambda state: state.has("Sneasel Friendship", player)
    )
    set_rule_if_exists(
        "Tangrowth's Swing-Along Attraction -- Raichu",
        lambda state: state.has("Raichu Friendship", player)
    )
    set_rule_if_exists(
        "Tangrowth's Swing-Along Attraction -- Ambipom",
        lambda state: state.has("Ambipom Friendship", player)
    )
    set_rule_if_exists(
        "Tangrowth's Swing-Along Attraction -- Primeape",
        lambda state: state.has("Primeape Friendship", player)
    )
    set_rule_if_exists(
        "Tangrowth's Swing-Along Attraction -- Aipom",
        lambda state: state.has("Aipom Friendship", player)
    )
    set_rule_if_exists(
        "Tangrowth's Swing-Along Attraction -- Electabuzz",
        lambda state: state.has("Electabuzz Friendship", player)
    )
    set_rule_if_exists(
        "Tangrowth's Swing-Along Attraction -- Chimchar",
        lambda state: state.has("Chimchar Friendship", player)
    )
    set_rule_if_exists(
        "Tangrowth's Swing-Along Attraction -- Croagunk",
        lambda state: state.has("Croagunk Friendship", player)
    )
    set_rule_if_exists(
        "Tangrowth's Swing-Along Attraction -- Celebi",
        lambda state: state.has("Celebi Friendship", player)
    )
    set_rule_if_exists(
        "Tangrowth's Swing-Along Attraction -- Celebi Friendship",
        lambda state: can_beat_all_tangrowth_swing_along_records(state, player)
    )
    # Haunted Zone Mansion

    set_rule_if_exists(
        "Haunted Zone Mansion Area - Duskull Power Competition -- Friendship",
        lambda state: state.has("Dusknoir Prisma", player)
    )
    set_rule_if_exists(
        "Haunted Zone Mansion Area - Misdreavus Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Haunted Zone Mansion Area - Pichu Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Haunted Zone Mansion Area - Umbreon Power Competition -- Friendship",
        lambda state: can_play_catch_intermediate(state, player) and state.count_group("Friendship Items", player) >= 75
    )
    set_rule_if_exists(
        "Haunted Zone Mansion Area - Umbreon Power Competition -- Espeon Unlocked",
        lambda state: can_play_catch_intermediate(state, player) and state.count_group("Friendship Items", player) >= 75
    )
    set_rule_if_exists(
        "Haunted Zone Mansion Area - Espeon Power Competition -- Friendship",
        lambda state: can_play_catch_intermediate(state, player) and state.has("Espeon Unlock", player)
    )
    set_rule_if_exists(
        "Haunted Zone Mansion Area - Spinarak Power Competition -- Friendship",
        lambda state: state.has("Rotom Prisma", player)
    )
    set_rule_if_exists(
        "Haunted Zone Mansion Area - Riolu Power Competition -- Friendship",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Haunted Zone Mansion Area - Voltorb Power Competition -- Friendship",
        lambda state: can_battle_thunderbolt_immune(state, player) and state.has("Voltorb Unlock", player)
    )
    set_rule_if_exists(
        "Haunted Zone Mansion Area - Elekid Power Competition -- Friendship",
        lambda state: can_battle_thunderbolt_immune(state, player) and state.has("Elekid Unlock", player)
    )
    set_rule_if_exists(
        "Haunted Zone Mansion Area - Elekid Power Competition --  Electabuzz Unlocked",
        lambda state: can_battle_thunderbolt_immune(state, player) and state.has("Elekid Unlock", player)
    )
    set_rule_if_exists(
        "Haunted Zone Mansion Area - Electabuzz Power Competition -- Friendship",
        lambda state: can_battle_thunderbolt_immune(state, player) and state.has("Electabuzz Unlock", player)
    )
    set_rule_if_exists(
        "Haunted Zone Mansion Area - Luxray Power Competition -- Friendship",
        lambda state: can_play_catch(state, player) and state.has("Luxray Unlock", player)
    )
    set_rule_if_exists(
        "Haunted Zone Mansion Area - Stunky Power Competition -- Friendship",
        lambda state: can_play_catch(state, player) and state.has("Stunky Unlock", player)
    )
    set_rule_if_exists(
        "Haunted Zone Mansion Area - Stunky Power Competition -- Skuntank Unlocked",
        lambda state: can_play_catch(state, player) and state.has("Stunky Unlock", player)
    )
    set_rule_if_exists(
        "Haunted Zone Mansion Area - Skuntank Power Competition -- Friendship",
        lambda state: can_battle(state, player) and state.has("Skuntank Unlock", player)
    )
    set_rule_if_exists(
        "Haunted Zone Mansion Area - Breloom Power Competition -- Friendship",
        lambda state: can_battle_thunderbolt_immune(state, player) and state.has("Breloom Unlock", player)
    )
    set_rule_if_exists(
        "Haunted Zone Mansion Area - Mismagius Power Competition -- Friendship",
        lambda state: can_battle(state, player) and state.has("Mismagius Unlock", player)
    )
    set_rule_if_exists(
        "Haunted Zone Mansion Area - Electrode Power Competition -- Friendship",
        lambda state: state.has("Rotom Prisma", player) and state.has("Electrode Unlock", player)
    )
    set_rule_if_exists(
        "Haunted Zone Mansion Area - Haunter Power Competition -- Friendship",
        lambda state: can_play_catch(state, player) and state.has("Haunter Unlock", player)
    )

    set_rule_if_exists(
        "Haunted Zone Mansion Area - Gastly Power Competition -- Friendship",
        lambda state: state.has("Gastly Unlock", player) or state.has("Gastly 2 Unlock", player)
    )
    set_rule_if_exists(
        "Haunted Zone Mansion Area - Gengar Power Competition -- Friendship",
        lambda state: can_battle(state, player) and state.has("Gengar Unlock", player)
    )
    set_rule_if_exists(
        "Haunted Zone Mansion Area - Gengar Painting -- Gengar Unlocked",
        lambda state: state.count_group("Friendship Items", player) >= 85
    )
    set_rule_if_exists(
        "Haunted Zone Mansion Area - Voltorb Vase -- Voltorb Unlocked",
        lambda state: can_destroy_objects_overworld(state, player)
    )
    set_rule_if_exists(
        "Haunted Zone Mansion Area - Abra Power Competition -- Friendship",
        lambda state: state.has("Rotom Prisma", player)
    )
    set_rule_if_exists(
        "Haunted Zone Mansion Area - Dusknoir -- Friendship",
        lambda state: state.has("Dusknoir Prisma", player)
    )
    # Dusknoir's Speed Slam
    set_rule_if_exists(
        "Dusknoir's Speed Slam Attraction -- Prisma",
        lambda state: can_beat_any_dusknoir_speed_slam_record(state, player)
    )
    set_rule_if_exists(
        "Dusknoir's Speed Slam Attraction -- Pikachu",
        lambda state: True
    )
    set_rule_if_exists(
        "Dusknoir's Speed Slam Attraction -- Stunky",
        lambda state: state.has("Stunky Friendship", player)
    )
    set_rule_if_exists(
        "Dusknoir's Speed Slam Attraction -- Gengar",
        lambda state: state.has("Gengar Friendship", player)
    )
    set_rule_if_exists(
        "Dusknoir's Speed Slam Attraction -- Mismagius",
        lambda state: state.has("Mismagius Friendship", player)
    )
    set_rule_if_exists(
        "Dusknoir's Speed Slam Attraction -- Scizor",
        lambda state: state.has("Scizor Friendship", player)
    )
    set_rule_if_exists(
        "Dusknoir's Speed Slam Attraction -- Espeon",
        lambda state: state.has("Espeon Friendship", player)
    )
    set_rule_if_exists(
        "Dusknoir's Speed Slam Attraction -- Dusknoir",
        lambda state: state.has("Dusknoir Friendship", player)
    )
    set_rule_if_exists(
        "Dusknoir's Speed Slam Attraction -- Umbreon",
        lambda state: state.has("Umbreon Friendship", player)
    )
    set_rule_if_exists(
        "Dusknoir's Speed Slam Attraction -- Cranidos",
        lambda state: state.has("Cranidos Friendship", player)
    )
    set_rule_if_exists(
        "Dusknoir's Speed Slam Attraction -- Skuntank",
        lambda state: state.has("Skuntank Friendship", player)
    )
    set_rule_if_exists(
        "Dusknoir's Speed Slam Attraction -- Electrode",
        lambda state: state.has("Electrode Friendship", player)
    )
    set_rule_if_exists(
        "Dusknoir's Speed Slam Attraction -- Gastly",
        lambda state: state.has("Gastly Friendship", player)
    )
    set_rule_if_exists(
        "Dusknoir's Speed Slam Attraction -- Duskull",
        lambda state: state.has("Duskull Friendship", player)
    )
    set_rule_if_exists(
        "Dusknoir's Speed Slam Attraction -- Misdreavus",
        lambda state: state.has("Misdreavus Friendship", player)
    )
    set_rule_if_exists(
        "Dusknoir's Speed Slam Attraction -- Krabby",
        lambda state: state.has("Krabby Friendship", player)
    )
    set_rule_if_exists(
        "Dusknoir's Speed Slam Attraction -- Darkrai",
        lambda state: state.has("Darkrai Friendship", player)
    )
    set_rule_if_exists(
        "Dusknoir's Speed Slam Attraction -- Darkrai Friendship",
        lambda state: can_beat_all_dusknoir_speed_slam_records(state, player)
    )
    # Rotom's Spooky Shoot-'em-Up
    set_rule_if_exists(
        "Rotom's Spooky Shoot-'em-Up Attraction -- Prisma",
        lambda state: can_beat_any_rotom_spooky_shoot_record(state, player)
    )
    set_rule_if_exists(
        "Rotom's Spooky Shoot-'em-Up Attraction -- Pikachu",
        lambda state: True
    )
    set_rule_if_exists(
        "Rotom's Spooky Shoot-'em-Up Attraction -- Magnemite",
        lambda state: state.has("Magnemite Friendship", player)
    )
    set_rule_if_exists(
        "Rotom's Spooky Shoot-'em-Up Attraction -- Porygon-Z",
        lambda state: state.has("Porygon-Z Friendship", player)
    )
    set_rule_if_exists(
        "Rotom's Spooky Shoot-'em-Up Attraction -- Magnezone",
        lambda state: state.has("Magnezone Friendship", player)
    )
    set_rule_if_exists(
        "Rotom's Spooky Shoot-'em-Up Attraction -- Gengar",
        lambda state: state.has("Gengar Friendship", player)
    )
    set_rule_if_exists(
        "Rotom's Spooky Shoot-'em-Up Attraction -- Magmortar",
        lambda state: state.has("Magmortar Friendship", player)
    )
    set_rule_if_exists(
        "Rotom's Spooky Shoot-'em-Up Attraction -- Electivire",
        lambda state: state.has("Electivire Friendship", player)
    )
    set_rule_if_exists(
        "Rotom's Spooky Shoot-'em-Up Attraction -- Mismagius",
        lambda state: state.has("Mismagius Friendship", player)
    )
    set_rule_if_exists(
        "Rotom's Spooky Shoot-'em-Up Attraction -- Claydol",
        lambda state: state.has("Claydol Friendship", player)
    )
    set_rule_if_exists(
        "Rotom's Spooky Shoot-'em-Up Attraction -- Electabuzz",
        lambda state: state.has("Electabuzz Friendship", player)
    )
    set_rule_if_exists(
        "Rotom's Spooky Shoot-'em-Up Attraction -- Haunter",
        lambda state: state.has("Haunter Friendship", player)
    )
    set_rule_if_exists(
        "Rotom's Spooky Shoot-'em-Up Attraction -- Abra",
        lambda state: state.has("Abra Friendship", player)
    )
    set_rule_if_exists(
        "Rotom's Spooky Shoot-'em-Up Attraction -- Elekid",
        lambda state: state.has("Elekid Friendship", player)
    )
    set_rule_if_exists(
        "Rotom's Spooky Shoot-'em-Up Attraction -- Mr. Mime",
        lambda state: state.has("Mr. Mime Friendship", player)
    )
    set_rule_if_exists(
        "Rotom's Spooky Shoot-'em-Up Attraction -- Baltoy",
        lambda state: state.has("Baltoy Friendship", player)
    )
    set_rule_if_exists(
        "Rotom's Spooky Shoot-'em-Up Attraction -- Rotom",
        lambda state: state.has("Rotom Friendship", player)
    )
    set_rule_if_exists(
        "Rotom's Spooky Shoot-'em-Up Attraction -- Rotom Friendship",
        lambda state: can_beat_all_rotom_spooky_shoot_records(state, player)
    )

    # Granite Zone
    set_rule_if_exists(
        "Granite Zone Main Area - Lopunny Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Granite Zone Main Area - Eevee Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Granite Zone Main Area - Eevee Power Competition -- Jolteon Unlocked",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Granite Zone Main Area - Charizard Power Competition -- Friendship",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Granite Zone Main Area - Flygon Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Granite Zone Main Area - Staraptor Power Competition -- Friendship",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Granite Zone Main Area - Staraptor Power Competition -- Aerodactyl Unlocked",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Granite Zone Main Area - Aerodactyl Power Competition -- Friendship",
        lambda state: can_battle(state, player) and state.has("Aerodactyl Unlock", player)
    )
    set_rule_if_exists(
        "Granite Zone Main Area - Arcanine Power Competition -- Friendship",
        lambda state: can_play_catch_intermediate(state, player)
    )
    set_rule_if_exists(
        "Granite Zone Main Area - Jolteon Power Competition -- Friendship",
        lambda state: can_play_catch_intermediate(state, player) and state.count_group("Friendship Items", player) >= 90
    )
    set_rule_if_exists(
        "Granite Zone Main Area - Skorupi Power Competition -- Friendship",
        lambda state: True
    )
    set_rule_if_exists(
        "Granite Zone Main Area - Porygon-Z Power Competition -- Friendship",
        lambda state: True
    )
    set_rule_if_exists(
        "Granite Zone Main Area - Tyranitar Power Competition -- Friendship",
        lambda state: can_battle(state, player) and state.has("Tyranitar Unlock", player)
    )
    set_rule_if_exists(
        "Granite Zone Main Area - Garchomp Power Competition -- Friendship",
        lambda state: can_battle_thunderbolt_immune(state, player) and state.has("Garchomp Unlock", player)
    )
    set_rule_if_exists(
        "Granite Zone Main Area - Taillow Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Granite Zone Main Area - Drifloon Power Competition -- Friendship",
        lambda state: True
    )
    set_rule_if_exists(
        "Granite Zone Main Area - Marowak Power Competition -- Friendship",
        lambda state: can_battle_thunderbolt_immune(state, player)
    )
    set_rule_if_exists(
        "Granite Zone Main Area - Baltoy Power Competition -- Friendship",
        lambda state: can_battle_thunderbolt_immune(state, player) and state.has("Baltoy Unlock", player)
    )
    set_rule_if_exists(
        "Granite Zone Main Area - Baltoy Power Competition -- Claydol Unlocked",
        lambda state: can_battle_thunderbolt_immune(state, player) and state.has("Baltoy Unlock", player)
    )
    set_rule_if_exists(
        "Granite Zone Main Area - Furret Power Competition -- Friendship",
        lambda state: True
    )

    set_rule_if_exists(
        "Granite Zone Salamence Area - Salamence -- Friendship",
        lambda state: state.has("Salamence Prisma", player)
    )
    set_rule_if_exists(
        "Granite Zone Main Area - Absol -- Friendship",
        lambda state: state.has("Absol Prisma", player)
    )

    # Absol Hurdle Dash
    set_rule_if_exists(
        "Absol's Hurdle Bounce Attraction -- Prisma",
        lambda state: can_beat_any_absol_hurdle_bounde_record(state, player)
    )
    set_rule_if_exists(
        "Absol's Hurdle Bounce Attraction -- Pikachu",
        lambda state: True
    )
    set_rule_if_exists(
        "Absol's Hurdle Bounce Attraction -- Chikorita",
        lambda state: state.has("Chikorita Friendship", player)
    )
    set_rule_if_exists(
        "Absol's Hurdle Bounce Attraction -- Absol",
        lambda state: state.has("Absol Friendship", player)
    )
    set_rule_if_exists(
        "Absol's Hurdle Bounce Attraction -- Lucario",
        lambda state: state.has("Lucario Friendship", player)
    )
    set_rule_if_exists(
        "Absol's Hurdle Bounce Attraction -- Ponyta",
        lambda state: state.has("Ponyta Friendship", player)
    )
    set_rule_if_exists(
        "Absol's Hurdle Bounce Attraction -- Ninetales",
        lambda state: state.has("Ninetales Friendship", player)
    )
    set_rule_if_exists(
        "Absol's Hurdle Bounce Attraction -- Lopunny",
        lambda state: state.has("Lopunny Friendship", player)
    )
    set_rule_if_exists(
        "Absol's Hurdle Bounce Attraction -- Espeon",
        lambda state: state.has("Espeon Friendship", player)
    )
    set_rule_if_exists(
        "Absol's Hurdle Bounce Attraction -- Infernape",
        lambda state: state.has("Infernape Friendship", player)
    )
    set_rule_if_exists(
        "Absol's Hurdle Bounce Attraction -- Breloom",
        lambda state: state.has("Breloom Friendship", player)
    )
    set_rule_if_exists(
        "Absol's Hurdle Bounce Attraction -- Riolu",
        lambda state: state.has("Riolu Friendship", player)
    )
    set_rule_if_exists(
        "Absol's Hurdle Bounce Attraction -- Furret",
        lambda state: state.has("Furret Friendship", player)
    )
    set_rule_if_exists(
        "Absol's Hurdle Bounce Attraction -- Mareep",
        lambda state: state.has("Mareep Friendship", player)
    )
    set_rule_if_exists(
        "Absol's Hurdle Bounce Attraction -- Eevee",
        lambda state: state.has("Eevee Friendship", player)
    )
    set_rule_if_exists(
        "Absol's Hurdle Bounce Attraction -- Vulpix",
        lambda state: state.has("Vulpix Friendship", player)
    )
    set_rule_if_exists(
        "Absol's Hurdle Bounce Attraction -- Shaymin",
        lambda state: state.has("Shaymin Friendship", player)
    )
    set_rule_if_exists(
        "Absol's Hurdle Bounce Attraction -- Shaymin Friendship",
        lambda state: can_beat_all_absol_hurdle_bounde_records(state, player)
    )

    # Salamence's Sky Race
    set_rule_if_exists(
        "Salamence's Sky Race Attraction -- Prisma",
        lambda state: can_beat_any_salamence_sky_race_record(state, player)
    )
    set_rule_if_exists(
        "Salamence's Sky Race Attraction -- Pikachu",
        lambda state: state.has("Pikachu Balloon", player)
    )
    set_rule_if_exists(
        "Salamence's Sky Race Attraction -- Salamence",
        lambda state: state.has("Salamence Friendship", player)
    )
    set_rule_if_exists(
        "Salamence's Sky Race Attraction -- Charizard",
        lambda state: state.has("Charizard Friendship", player)
    )
    set_rule_if_exists(
        "Salamence's Sky Race Attraction -- Dragonite",
        lambda state: state.has("Dragonite Friendship", player)
    )
    set_rule_if_exists(
        "Salamence's Sky Race Attraction -- Flygon",
        lambda state: state.has("Flygon Friendship", player)
    )
    set_rule_if_exists(
        "Salamence's Sky Race Attraction -- Aerodactyl",
        lambda state: state.has("Aerodactyl Friendship", player)
    )
    set_rule_if_exists(
        "Salamence's Sky Race Attraction -- Staraptor",
        lambda state: state.has("Staraptor Friendship", player)
    )
    set_rule_if_exists(
        "Salamence's Sky Race Attraction -- Honchkrow",
        lambda state: state.has("Honchkrow Friendship", player)
    )
    set_rule_if_exists(
        "Salamence's Sky Race Attraction -- Gliscor",
        lambda state: state.has("Gliscor Friendship", player)
    )
    set_rule_if_exists(
        "Salamence's Sky Race Attraction -- Pidgeotto",
        lambda state: state.has("Pidgeotto Friendship", player)
    )
    set_rule_if_exists(
        "Salamence's Sky Race Attraction -- Togekiss",
        lambda state: state.has("Togekiss Friendship", player)
    )
    set_rule_if_exists(
        "Salamence's Sky Race Attraction -- Golbat",
        lambda state: state.has("Golbat Friendship", player)
    )
    set_rule_if_exists(
        "Salamence's Sky Race Attraction -- Taillow",
        lambda state: state.has("Taillow Friendship", player)
    )
    set_rule_if_exists(
        "Salamence's Sky Race Attraction -- Murkrow",
        lambda state: state.has("Murkrow Friendship", player)
    )
    set_rule_if_exists(
        "Salamence's Sky Race Attraction -- Zubat",
        lambda state: state.has("Zubat Friendship", player)
    )
    set_rule_if_exists(
        "Salamence's Sky Race Attraction -- Latios",
        lambda state: state.has("Latios Friendship", player)
    )
    set_rule_if_exists(
        "Salamence's Sky Race Attraction -- Latios Friendship",
        lambda state: can_beat_all_salamence_sky_race_records(state, player)
    )
    # Flower Zone

    set_rule_if_exists(
        "Flower Zone Main Area - Skiploom Power Competition -- Friendship",
        lambda state: True
    )
    set_rule_if_exists(
        "Flower Zone Main Area - Budew Power Competition -- Friendship",
        lambda state: True
    )
    set_rule_if_exists(
        "Flower Zone Main Area - Cyndaquil Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Flower Zone Main Area - Lucario Power Competition -- Friendship",
        lambda state: can_play_catch_intermediate(state, player) and state.count_group(
            "Friendship Items",
            player
        ) >= 100
    )
    set_rule_if_exists(
        "Flower Zone Main Area - Dragonite Power Competition -- Friendship",
        lambda state: can_play_catch_intermediate(state, player)
    )
    set_rule_if_exists(
        "Flower Zone Main Area - Mareep Power Competition -- Friendship",
        lambda state: can_play_catch(state, player)
    )
    set_rule_if_exists(
        "Flower Zone Main Area - Bellossom Power Competition -- Friendship",
        lambda state: True
    )
    set_rule_if_exists(
        "Flower Zone Main Area - Teddiursa Power Competition -- Friendship",
        lambda state: True
    )
    set_rule_if_exists(
        "Flower Zone Main Area - Furret Power Competition -- Friendship",
        lambda state: True
    )
    set_rule_if_exists(
        "Flower Zone Main Area - Meditite Power Competition -- Friendship",
        lambda state: True
    )

    set_rule_if_exists(
        "Flower Zone Main Area - Rayquaza -- Friendship",
        lambda state: state.has("Rayquaza Prisma", player)
    )

    # Rayquaza's Balloon Panic
    set_rule_if_exists(
        "Rayquaza's Balloon Panic Attraction -- Prisma",
        lambda state: can_beat_any_rayquaza_balloon_panic_record(state, player)
    )
    set_rule_if_exists(
        "Rayquaza's Balloon Panic Attraction -- Pikachu",
        lambda state: True
    )
    set_rule_if_exists(
        "Rayquaza's Balloon Panic Attraction -- Lucario",
        lambda state: state.has("Lucario Friendship", player)
    )
    set_rule_if_exists(
        "Rayquaza's Balloon Panic Attraction -- Glaceon",
        lambda state: state.has("Glaceon Friendship", player)
    )
    set_rule_if_exists(
        "Rayquaza's Balloon Panic Attraction -- Luxray",
        lambda state: state.has("Luxray Friendship", player)
    )
    set_rule_if_exists(
        "Rayquaza's Balloon Panic Attraction -- Mamoswine",
        lambda state: state.has("Mamoswine Friendship", player)
    )
    set_rule_if_exists(
        "Rayquaza's Balloon Panic Attraction -- Infernape",
        lambda state: state.has("Infernape Friendship", player)
    )
    set_rule_if_exists(
        "Rayquaza's Balloon Panic Attraction -- Floatzel",
        lambda state: state.has("Floatzel Friendship", player)
    )
    set_rule_if_exists(
        "Rayquaza's Balloon Panic Attraction -- Rhyperior",
        lambda state: state.has("Rhyperior Friendship", player)
    )
    set_rule_if_exists(
        "Rayquaza's Balloon Panic Attraction -- Absol",
        lambda state: state.has("Absol Friendship", player)
    )
    set_rule_if_exists(
        "Rayquaza's Balloon Panic Attraction -- Breloom",
        lambda state: state.has("Breloom Friendship", player)
    )
    set_rule_if_exists(
        "Rayquaza's Balloon Panic Attraction -- Mareep",
        lambda state: state.has("Mareep Friendship", player)
    )
    set_rule_if_exists(
        "Rayquaza's Balloon Panic Attraction -- Cyndaquil",
        lambda state: state.has("Cyndaquil Friendship", player)
    )
    set_rule_if_exists(
        "Rayquaza's Balloon Panic Attraction -- Totodile",
        lambda state: state.has("Totodile Friendship", player)
    )
    set_rule_if_exists(
        "Rayquaza's Balloon Panic Attraction -- Chikorita",
        lambda state: state.has("Chikorita Friendship", player)
    )
    set_rule_if_exists(
        "Rayquaza's Balloon Panic Attraction -- Mime Jr.",
        lambda state: state.has("Mime Jr. Friendship", player)
    )
    set_rule_if_exists(
        "Rayquaza's Balloon Panic Attraction -- Deoxys",
        lambda state: state.has("Deoxys Friendship", player)
    )
    set_rule_if_exists(
        "Rayquaza's Balloon Panic Attraction -- Deoxys Friendship",
        lambda state: can_beat_all_rayquaza_balloon_panic_records(state, player)
    )
    # Skygarden
    set_rule_if_exists(
        "Skygarden - Mew Power Competition -- Stage 1",
        lambda state: True
    )
    set_rule_if_exists(
        "Skygarden - Mew Power Competition -- Stage 2",
        lambda state: can_battle(state, player)
    )
    set_rule_if_exists(
        "Skygarden - Mew Power Competition -- Stage 3",
        lambda state: can_battle(state, player) and can_battle_thunderbolt_immune(state, player)
    )
    set_rule_if_exists(
        "Skygarden - Mew Power Competition -- Stage 4",
        lambda state: can_battle(state, player) and can_battle_thunderbolt_immune(state, player)
    )
    set_rule_if_exists(
        "Skygarden - Mew Power Competition -- Friendship",
        lambda state: can_battle(state, player) and can_battle_thunderbolt_immune(state, player) and
                      can_play_catch_intermediate(state, player)
    )
    set_rule_if_exists(
        "Skygarden - Prisma Completion -- Stage 1",
        lambda state: state.count_group("Friendship Items", player) >= 100
    )
    set_rule_if_exists(
        "Skygarden - Prisma Completion -- Stage 2",
        lambda state: state.count_group("Friendship Items", player) >= 150
    )
    set_rule_if_exists(
        "Skygarden - Prisma Completion -- Completed",
        lambda state: state.count_group("Friendship Items", player) >= 193
    )
    world.multiworld.completion_condition[player] = lambda state: state.has("Victory", player)


def can_beat_all_rayquaza_balloon_panic_records(state: CollectionState, player: int):
    return (
            state.has("Lucario Friendship", player) and
            state.has("Glaceon Friendship", player) and
            state.has("Luxray Friendship", player) and
            state.has("Mamoswine Friendship", player) and
            state.has("Infernape Friendship", player) and
            state.has("Floatzel Friendship", player) and
            state.has("Rhyperior Friendship", player) and
            state.has("Absol Friendship", player) and
            state.has("Breloom Friendship", player) and
            state.has("Mareep Friendship", player) and
            state.has("Cyndaquil Friendship", player) and
            state.has("Totodile Friendship", player) and
            state.has("Chikorita Friendship", player) and
            state.has("Mime Jr. Friendship", player)

    )


def can_beat_any_rayquaza_balloon_panic_record(state: CollectionState, player: int):
    return (
            state.has("Lucario Friendship", player) or
            state.has("Glaceon Friendship", player) or
            state.has("Luxray Friendship", player) or
            state.has("Mamoswine Friendship", player) or
            state.has("Infernape Friendship", player) or
            state.has("Floatzel Friendship", player) or
            state.has("Rhyperior Friendship", player) or
            state.has("Absol Friendship", player) or
            state.has("Breloom Friendship", player) or
            state.has("Mareep Friendship", player) or
            state.has("Cyndaquil Friendship", player) or
            state.has("Totodile Friendship", player) or
            state.has("Chikorita Friendship", player) or
            state.has("Mime Jr. Friendship", player) or
            state.has("Deoxys Friendship", player)

    )


def can_beat_all_salamence_sky_race_records(state: CollectionState, player: int):
    return (
            state.has("Pikachu Balloon", player) and
            state.has("Salamence Friendship", player) and
            state.has("Charizard Friendship", player) and
            state.has("Dragonite Friendship", player) and
            state.has("Flygon Friendship", player) and
            state.has("Aerodactyl Friendship", player) and
            state.has("Staraptor Friendship", player) and
            state.has("Honchkrow Friendship", player) and
            state.has("Gliscor Friendship", player) and
            state.has("Pidgeotto Friendship", player) and
            state.has("Togekiss Friendship", player) and
            state.has("Golbat Friendship", player) and
            state.has("Taillow Friendship", player) and
            state.has("Murkrow Friendship", player) and
            state.has("Zubat Friendship", player)
    )


def can_beat_any_salamence_sky_race_record(state: CollectionState, player: int):
    return (
            state.has("Pikachu Balloon", player) or
            state.has("Salamence Friendship", player) or
            state.has("Charizard Friendship", player) or
            state.has("Dragonite Friendship", player) or
            state.has("Flygon Friendship", player) or
            state.has("Aerodactyl Friendship", player) or
            state.has("Staraptor Friendship", player) or
            state.has("Honchkrow Friendship", player) or
            state.has("Gliscor Friendship", player) or
            state.has("Pidgeotto Friendship", player) or
            state.has("Togekiss Friendship", player) or
            state.has("Golbat Friendship", player) or
            state.has("Taillow Friendship", player) or
            state.has("Murkrow Friendship", player) or
            state.has("Zubat Friendship", player) or
            state.has("Latios Friendship", player)

    )


def can_beat_all_absol_hurdle_bounde_records(state: CollectionState, player: int):
    return (
            state.has("Chikorita Friendship", player) and
            state.has("Absol Friendship", player) and
            state.has("Lucario Friendship", player) and
            state.has("Ponyta Friendship", player) and
            state.has("Ninetales Friendship", player) and
            state.has("Lopunny Friendship", player) and
            state.has("Espeon Friendship", player) and
            state.has("Infernape Friendship", player) and
            state.has("Breloom Friendship", player) and
            state.has("Riolu Friendship", player) and
            state.has("Furret Friendship", player) and
            state.has("Mareep Friendship", player) and
            state.has("Eevee Friendship", player) and
            state.has("Vulpix Friendship", player)

    )


def can_beat_any_absol_hurdle_bounde_record(state: CollectionState, player: int):
    return (
            state.has("Chikorita Friendship", player) or
            state.has("Absol Friendship", player) or
            state.has("Lucario Friendship", player) or
            state.has("Ponyta Friendship", player) or
            state.has("Ninetales Friendship", player) or
            state.has("Lopunny Friendship", player) or
            state.has("Espeon Friendship", player) or
            state.has("Infernape Friendship", player) or
            state.has("Breloom Friendship", player) or
            state.has("Riolu Friendship", player) or
            state.has("Furret Friendship", player) or
            state.has("Mareep Friendship", player) or
            state.has("Eevee Friendship", player) or
            state.has("Vulpix Friendship", player) or
            state.has("Shaymin Friendship", player)

    )


def can_beat_all_rotom_spooky_shoot_records(state: CollectionState, player: int):
    return (
            state.has("Magnemite Friendship", player) and
            state.has("Porygon-Z Friendship", player) and
            state.has("Magnezone Friendship", player) and
            state.has("Gengar Friendship", player) and
            state.has("Magmortar Friendship", player) and
            state.has("Electivire Friendship", player) and
            state.has("Mismagius Friendship", player) and
            state.has("Claydol Friendship", player) and
            state.has("Electabuzz Friendship", player) and
            state.has("Abra Friendship", player) and
            state.has("Elekid Friendship", player) and
            state.has("Mr. Mime Friendship", player) and
            state.has("Baltoy Friendship", player)

    )


def can_beat_any_rotom_spooky_shoot_record(state: CollectionState, player: int):
    return (
            state.has("Magnemite Friendship", player) or
            state.has("Porygon-Z Friendship", player) or
            state.has("Magnezone Friendship", player) or
            state.has("Gengar Friendship", player) or
            state.has("Magmortar Friendship", player) or
            state.has("Electivire Friendship", player) or
            state.has("Mismagius Friendship", player) or
            state.has("Claydol Friendship", player) or
            state.has("Electabuzz Friendship", player) or
            state.has("Abra Friendship", player) or
            state.has("Elekid Friendship", player) or
            state.has("Mr. Mime Friendship", player) or
            state.has("Baltoy Friendship", player) or
            state.has("Rotom Friendship", player)

    )


def can_beat_all_dusknoir_speed_slam_records(state: CollectionState, player: int):
    return (
            state.has("Stunky Friendship", player) and
            state.has("Gengar Friendship", player) and
            state.has("Mismagius Friendship", player) and
            state.has("Scizor Friendship", player) and
            state.has("Espeon Friendship", player) and
            state.has("Dusknoir Friendship", player) and
            state.has("Umbreon Friendship", player) and
            state.has("Cranidos Friendship", player) and
            state.has("Skuntank Friendship", player) and
            state.has("Electrode Friendship", player) and
            state.has("Gastly Friendship", player) and
            state.has("Duskull Friendship", player) and
            state.has("Misdreavus Friendship", player) and
            state.has("Krabby Friendship", player)
    )


def can_beat_any_dusknoir_speed_slam_record(state: CollectionState, player: int):
    return (
            state.has("Stunky Friendship", player) or
            state.has("Gengar Friendship", player) or
            state.has("Mismagius Friendship", player) or
            state.has("Scizor Friendship", player) or
            state.has("Espeon Friendship", player) or
            state.has("Dusknoir Friendship", player) or
            state.has("Umbreon Friendship", player) or
            state.has("Cranidos Friendship", player) or
            state.has("Skuntank Friendship", player) or
            state.has("Electrode Friendship", player) or
            state.has("Gastly Friendship", player) or
            state.has("Duskull Friendship", player) or
            state.has("Misdreavus Friendship", player) or
            state.has("Krabby Friendship", player) or
            state.has("Darkrai Friendship", player)

    )


def can_beat_all_tangrowth_swing_along_records(state: CollectionState, player: int):
    return (
            state.has("Meowth Friendship", player) and
            state.has("Pichu Friendship", player) and
            state.has("Lucario Friendship", player) and
            state.has("Infernape Friendship", player) and
            state.has("Blaziken Friendship", player) and
            state.has("Riolu Friendship", player) and
            state.has("Sneasel Friendship", player) and
            state.has("Raichu Friendship", player) and
            state.has("Ambipom Friendship", player) and
            state.has("Primeape Friendship", player) and
            state.has("Aipom Friendship", player) and
            state.has("Electabuzz Friendship", player) and
            state.has("Chimchar Friendship", player) and
            state.has("Croagunk Friendship", player)
    )


def can_beat_any_tangrowth_swing_along_record(state: CollectionState, player: int):
    return (
            state.has("Meowth Friendship", player) or
            state.has("Pichu Friendship", player) or
            state.has("Lucario Friendship", player) or
            state.has("Infernape Friendship", player) or
            state.has("Blaziken Friendship", player) or
            state.has("Riolu Friendship", player) or
            state.has("Sneasel Friendship", player) or
            state.has("Raichu Friendship", player) or
            state.has("Ambipom Friendship", player) or
            state.has("Primeape Friendship", player) or
            state.has("Aipom Friendship", player) or
            state.has("Electabuzz Friendship", player) or
            state.has("Chimchar Friendship", player) or
            state.has("Croagunk Friendship", player) or
            state.has("Celebi Friendship", player)
    )


def can_beat_all_blaziken_boulder_bash_records(state: CollectionState, player: int):
    return (
            state.has("Geodude Friendship", player) and
            state.has("Phanpy Friendship", player) and
            state.has("Blaziken Friendship", player) and
            state.has("Garchomp Friendship", player) and
            state.has("Scizor Friendship", player) and
            state.has("Magmortar Friendship", player) and
            state.has("Hitmonchan Friendship", player) and
            state.has("Machamp Friendship", player) and
            state.has("Marowak Friendship", player) and
            state.has("Farfetch'd Friendship", player) and
            state.has("Cranidos Friendship", player) and
            state.has("Camerupt Friendship", player) and
            state.has("Bastiodon Friendship", player) and
            state.has("Mawile Friendship", player)
    )


def can_beat_any_blaziken_boulder_bash_record(state: CollectionState, player: int):
    return (
            state.has("Geodude Friendship", player) or
            state.has("Phanpy Friendship", player) or
            state.has("Blaziken Friendship", player) or
            state.has("Garchomp Friendship", player) or
            state.has("Scizor Friendship", player) or
            state.has("Magmortar Friendship", player) or
            state.has("Hitmonchan Friendship", player) or
            state.has("Machamp Friendship", player) or
            state.has("Marowak Friendship", player) or
            state.has("Farfetch'd Friendship", player) or
            state.has("Cranidos Friendship", player) or
            state.has("Camerupt Friendship", player) or
            state.has("Bastiodon Friendship", player) or
            state.has("Mawile Friendship", player) or
            state.has("Groudon Friendship", player)
    )


def can_beat_all_rhyperior_bumper_burn_records(state: CollectionState, player: int):
    return (
            state.has("Magnemite Friendship", player) and
            state.has("Rhyperior Friendship", player) and
            state.has("Tyranitar Friendship", player) and
            state.has("Hitmontop Friendship", player) and
            state.has("Flareon Friendship", player) and
            state.has("Venusaur Friendship", player) and
            state.has("Snorlax Friendship", player) and
            state.has("Torterra Friendship", player) and
            state.has("Magnezone Friendship", player) and
            state.has("Claydol Friendship", player) and
            state.has("Quilava Friendship", player) and
            state.has("Torkoal Friendship", player) and
            state.has("Baltoy Friendship", player) and
            state.has("Bonsly Friendship", player)
    )


def can_beat_any_rhyperior_bumper_burn_record(state: CollectionState, player: int):
    return (
            state.has("Magnemite Friendship", player) or
            state.has("Rhyperior Friendship", player) or
            state.has("Tyranitar Friendship", player) or
            state.has("Hitmontop Friendship", player) or
            state.has("Flareon Friendship", player) or
            state.has("Venusaur Friendship", player) or
            state.has("Snorlax Friendship", player) or
            state.has("Torterra Friendship", player) or
            state.has("Magnezone Friendship", player) or
            state.has("Claydol Friendship", player) or
            state.has("Quilava Friendship", player) or
            state.has("Torkoal Friendship", player) or
            state.has("Baltoy Friendship", player) or
            state.has("Bonsly Friendship", player) or
            state.has("Heatran Friendship", player)
    )


def can_beat_all_bastiodon_panel_crush_records(state: CollectionState, player: int):
    return (
            state.has("Sableye Friendship", player) and
            state.has("Meowth Friendship", player) and
            state.has("Torchic Friendship", player) and
            state.has("Electivire Friendship", player) and
            state.has("Magmortar Friendship", player) and
            state.has("Hitmonlee Friendship", player) and
            state.has("Ursaring Friendship", player) and
            state.has("Mr. Mime Friendship", player) and
            state.has("Raichu Friendship", player) and
            state.has("Sudowoodo Friendship", player) and
            state.has("Charmander Friendship", player) and
            state.has("Gible Friendship", player) and
            state.has("Chimchar Friendship", player) and
            state.has("Magby Friendship", player)
    )


def can_beat_any_bastiodon_panel_crush_record(state: CollectionState, player: int):
    return (
            state.has("Sableye Friendship", player) or
            state.has("Meowth Friendship", player) or
            state.has("Torchic Friendship", player) or
            state.has("Electivire Friendship", player) or
            state.has("Magmortar Friendship", player) or
            state.has("Hitmonlee Friendship", player) or
            state.has("Ursaring Friendship", player) or
            state.has("Mr. Mime Friendship", player) or
            state.has("Raichu Friendship", player) or
            state.has("Sudowoodo Friendship", player) or
            state.has("Charmander Friendship", player) or
            state.has("Gible Friendship", player) or
            state.has("Chimchar Friendship", player) or
            state.has("Magby Friendship", player) or
            state.has("Metagross Friendship", player)
    )


def can_beat_all_empoleon_snow_slide_records(state: CollectionState, player: int):
    return (
            state.has("Pikachu Snowboard", player) and
            state.has("Teddiursa Friendship", player) and
            state.has("Magikarp Friendship", player) and
            state.has("Empoleon Friendship", player) and
            state.has("Glaceon Friendship", player) and
            state.has("Blastoise Friendship", player) and
            state.has("Glalie Friendship", player) and
            state.has("Delibird Friendship", player) and
            state.has("Piloswine Friendship", player) and
            state.has("Prinplup Friendship", player) and
            state.has("Squirtle Friendship", player) and
            state.has("Piplup Friendship", player) and
            state.has("Quagsire Friendship", player) and
            state.has("Spheal Friendship", player)
    )


def can_beat_any_empoleon_snow_slide_record(state: CollectionState, player: int):
    return (
            state.has("Pikachu Snowboard Friendship", player) or
            state.has("Teddiursa Friendship", player) or
            state.has("Magikarp Friendship", player) or
            state.has("Empoleon Friendship", player) or
            state.has("Glaceon Friendship", player) or
            state.has("Blastoise Friendship", player) or
            state.has("Glalie Friendship", player) or
            state.has("Delibird Friendship", player) or
            state.has("Piloswine Friendship", player) or
            state.has("Prinplup Friendship", player) or
            state.has("Squirtle Friendship", player) or
            state.has("Piplup Friendship", player) or
            state.has("Quagsire Friendship", player) or
            state.has("Spheal Friendship", player) or
            state.has("Suicune Friendship", player)
    )


def can_beat_all_gyarados_aqua_dash_records(state: CollectionState, player: int):
    return (
            state.has("Pikachu Surfboard", player) and
            state.has("Psyduck Friendship", player) and
            state.has("Azurill Friendship", player) and
            state.has("Slowpoke Friendship", player) and
            state.has("Empoleon Friendship", player) and
            state.has("Floatzel Friendship", player) and
            state.has("Feraligatr Friendship", player) and
            state.has("Golduck Friendship", player) and
            state.has("Vaporeon Friendship", player) and
            state.has("Prinplup Friendship", player) and
            state.has("Bibarel Friendship", player) and
            state.has("Buizel Friendship", player) and
            state.has("Corsola Friendship", player) and
            state.has("Piplup Friendship", player) and
            state.has("Lotad Friendship", player)
    )


def can_beat_any_gyarados_aqua_dash_record(state: CollectionState, player: int):
    return (
            state.has("Pikachu Surfboard", player) or
            state.has("Psyduck Friendship", player) or
            state.has("Azurill Friendship", player) or
            state.has("Slowpoke Friendship", player) or
            state.has("Empoleon Friendship", player) or
            state.has("Floatzel Friendship", player) or
            state.has("Feraligatr Friendship", player) or
            state.has("Golduck Friendship", player) or
            state.has("Vaporeon Friendship", player) or
            state.has("Prinplup Friendship", player) or
            state.has("Bibarel Friendship", player) or
            state.has("Buizel Friendship", player) or
            state.has("Corsola Friendship", player) or
            state.has("Piplup Friendship", player) or
            state.has("Lotad Friendship", player) or
            state.has("Manaphy Friendship", player)
    )


def can_beat_all_pelipper_circle_circuit_records(state: CollectionState, player: int):
    return (
            state.has("Pikachu Balloon", player) and
            state.has("Staraptor Friendship", player) and
            state.has("Togekiss Friendship", player) and
            state.has("Honchkrow Friendship", player) and
            state.has("Gliscor Friendship", player) and
            state.has("Pelipper Friendship", player) and
            state.has("Staravia Friendship", player) and
            state.has("Pidgeotto Friendship", player) and
            state.has("Butterfree Friendship", player) and
            state.has("Tropius Friendship", player) and
            state.has("Murkrow Friendship", player) and
            state.has("Taillow Friendship", player) and
            state.has("Spearow Friendship", player) and
            state.has("Starly Friendship", player) and
            state.has("Wingull Friendship", player))


def can_beat_any_pelipper_circle_circuit_record(state: CollectionState, player: int):
    return (
            state.has("Pikachu Balloon", player) or
            state.has("Staraptor Friendship", player) or
            state.has("Togekiss Friendship", player) or
            state.has("Honchkrow Friendship", player) or
            state.has("Gliscor Friendship", player) or
            state.has("Pelipper Friendship", player) or
            state.has("Staravia Friendship", player) or
            state.has("Pidgeotto Friendship", player) or
            state.has("Butterfree Friendship", player) or
            state.has("Tropius Friendship", player) or
            state.has("Murkrow Friendship", player) or
            state.has("Taillow Friendship", player) or
            state.has("Spearow Friendship", player) or
            state.has("Starly Friendship", player) or
            state.has("Wingull Friendship", player) or
            state.has("Latias Friendship", player)
    )


def can_beat_all_venusaur_vine_swing_records(state: CollectionState, player: int):
    return (
            state.has("Munchlax Friendship", player) and
            state.has("Magikarp Friendship", player) and
            state.has("Blaziken Friendship", player) and
            state.has("Infernape Friendship", player) and
            state.has("Lucario Friendship", player) and
            state.has("Primeape Friendship", player) and
            state.has("Tangrowth Friendship", player) and
            state.has("Ambipom Friendship", player) and
            state.has("Croagunk Friendship", player) and
            state.has("Mankey Friendship", player) and
            state.has("Aipom Friendship", player) and
            state.has("Chimchar Friendship", player) and
            state.has("Treecko Friendship", player) and
            state.has("Pachirisu Friendship", player)
    )


def can_beat_any_venusaur_vine_swing_record(state: CollectionState, player: int):
    return (
            state.has("Munchlax Friendship", player) or
            state.has("Magikarp Friendship", player) or
            state.has("Blaziken Friendship", player) or
            state.has("Infernape Friendship", player) or
            state.has("Lucario Friendship", player) or
            state.has("Primeape Friendship", player) or
            state.has("Tangrowth Friendship", player) or
            state.has("Ambipom Friendship", player) or
            state.has("Croagunk Friendship", player) or
            state.has("Mankey Friendship", player) or
            state.has("Aipom Friendship", player) or
            state.has("Chimchar Friendship", player) or
            state.has("Treecko Friendship", player) or
            state.has("Pachirisu Friendship", player) or
            state.has("Jirachi Friendship", player)
    )


def can_beat_any_bulbasaur_daring_dash_record(state: CollectionState, player: int):
    return (
            state.has("Turtwig Friendship", player) or
            state.has("Munchlax Friendship", player) or
            state.has("Chimchar Friendship", player) or
            state.has("Treecko Friendship", player) or
            state.has("Bibarel Friendship", player) or
            state.has("Bulbasaur Friendship", player) or
            state.has("Bidoof Friendship", player) or
            state.has("Oddish Friendship", player) or
            state.has("Shroomish Friendship", player) or
            state.has("Bonsly Friendship", player) or
            state.has("Lotad Friendship", player) or
            state.has("Weedle Friendship", player) or
            state.has("Caterpie Friendship", player) or
            state.has("Magikarp Friendship", player) or
            state.has("Jolteon Friendship", player) or
            state.has("Arcanine Friendship", player) or
            state.has("Leafeon Friendship", player) or
            state.has("Scyther Friendship", player) or
            state.has("Ponyta Friendship", player) or
            state.has("Shinx Friendship", player) or
            state.has("Eevee Friendship", player) or
            state.has("Pachirisu Friendship", player) or
            state.has("Buneary Friendship", player) or
            state.has("Croagunk Friendship", player) or
            state.has("Mew Friendship", player)
    )


def can_battle_thunderbolt_immune(state: CollectionState, player: int):
    return (
            state.has("Progressive Dash", player) or
            state.has("Progressive Iron Tail", player)
    )


def can_farm_berries(state: CollectionState, player: int):
    return state.has("Progressive Dash", player)


def can_play_catch(state: CollectionState, player: int):
    return state.has("Progressive Dash", player)


def can_play_catch_intermediate(state: CollectionState, player: int):
    return state.has("Progressive Dash", player, 2)


def can_dash_overworld(state: CollectionState, player: int):
    return state.has("Progressive Dash", player)


def can_thunderbolt_overworld(state: CollectionState, player: int):
    return state.has("Progressive Thunderbolt", player)


def can_battle(state: CollectionState, player: int):
    return (
            state.has("Progressive Thunderbolt", player) or
            state.has("Progressive Dash", player) or
            state.has("Progressive Iron Tail", player)
    )


def can_destroy_objects_overworld(state: CollectionState, player: int):
    return state.has("Progressive Dash", player) or state.has("Progressive Thunderbolt", player)
