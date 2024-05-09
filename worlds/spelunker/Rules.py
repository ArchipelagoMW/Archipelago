from worlds.generic.Rules import set_rule
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import SpelunkerWorld


def set_rules(world: "SpelunkerWorld") -> None:
    player = world.player

    set_rule(world.multiworld.get_location("B1F - Past Boulder", player), lambda state: state.has("Dynamite", player, 1))
    set_rule(world.multiworld.get_location("B1F - Side Shaft Ledge", player), lambda state: state.has("Dynamite", player, 1))
    set_rule(world.multiworld.get_location("B1F - Side Shaft Mound", player), lambda state: state.has("Dynamite", player, 1))
    set_rule(world.multiworld.get_location("B1F - Side Shaft Bottom Left", player), lambda state: state.has("Dynamite", player, 1))
    set_rule(world.multiworld.get_location("B1F - Side Shaft Bottom Right", player), lambda state: state.has("Dynamite", player, 1))
    set_rule(world.multiworld.get_location("B1F - Side Shaft Ladder Right", player), lambda state: state.has("Dynamite", player, 1))

    set_rule(world.multiworld.get_location("B3F - Bat Item", player), lambda state: state.has("Flare", player, 1))
    set_rule(world.multiworld.get_location("B3F - Ladder Left", player), lambda state: state.has("Flare", player, 1))
    set_rule(world.multiworld.get_location("B3F - Bombable Wall", player), lambda state: state.has("Dynamite", player, 1) and state.has("Flare", player, 1))

    set_rule(world.multiworld.get_location("B5F - Near Ramp", player), lambda state: state.has("Dynamite", player, 1) and state.has("Blue Key", player, 1))
    set_rule(world.multiworld.get_location("B5F - Ladder Left", player), lambda state: state.has("Dynamite", player, 1) and state.has("Blue Key", player, 1))
    set_rule(world.multiworld.get_location("B5F - Ladder Right", player), lambda state: state.has("Dynamite", player, 1) and state.has("Blue Key", player, 1))

    set_rule(world.multiworld.get_location("B8F - Rope 1", player), lambda state: state.has("Dynamite", player, 2))
    set_rule(world.multiworld.get_location("B8F - Rope 2", player), lambda state: state.has("Dynamite", player, 2))
    set_rule(world.multiworld.get_location("B8F - Boulder Pit 1", player), lambda state: state.has("Dynamite", player, 2))
    set_rule(world.multiworld.get_location("B8F - Boulder Pit 2", player), lambda state: state.has("Dynamite", player, 2))

    set_rule(world.multiworld.get_location("B11F - Boulder Pit", player), lambda state: state.has("Dynamite", player, 2))

    set_rule(world.multiworld.get_location("B10F - Solo Rope", player), lambda state: state.has("Flare", player, 1))
    set_rule(world.multiworld.get_location("B10F - Platform Item", player), lambda state: state.has("Flare", player, 1))
    set_rule(world.multiworld.get_location("B11F - Bombable Wall", player), lambda state: state.has("Dynamite", player, 2) and state.has("Flare", player, 1))

    set_rule(world.multiworld.get_location("B12F - Pit Item 1", player), lambda state: state.has("Blue Key", player, 3))
    set_rule(world.multiworld.get_location("B12F - Pit Item 2", player), lambda state: state.has("Blue Key", player, 3))
    set_rule(world.multiworld.get_location("B12F - Pit Item 3", player), lambda state: state.has("Blue Key", player, 3))
    set_rule(world.multiworld.get_location("B12F - Locked Item", player), lambda state: state.has("Blue Key", player, 4))

    set_rule(world.multiworld.get_location("B14F - Boulder Item", player), lambda state: state.has("Dynamite", player, 4))

    set_rule(world.multiworld.get_location("B15F - Past Boulder", player), lambda state: state.has("Dynamite", player, 4))
    set_rule(world.multiworld.get_location("B15F - Upper Ledge", player), lambda state: state.has("Dynamite", player, 4))
    set_rule(world.multiworld.get_location("B15F - Three in a Row 1", player), lambda state: state.has("Dynamite", player, 4))
    set_rule(world.multiworld.get_location("B15F - Three in a Row 2", player), lambda state: state.has("Dynamite", player, 4))
    set_rule(world.multiworld.get_location("B15F - Three in a Row 3", player), lambda state: state.has("Dynamite", player, 4))
    set_rule(world.multiworld.get_location("B15F - Right Wall", player), lambda state: state.has("Dynamite", player, 4))

    set_rule(world.multiworld.get_location("B16F - Undulating Rocks", player), lambda state: state.has("Blue Key", player, 4))
    set_rule(world.multiworld.get_location("B16F - Top of Waterfall", player), lambda state: state.has("Blue Key", player, 4))
    set_rule(world.multiworld.get_location("B16F - Below Waterfall", player), lambda state: state.has("Blue Key", player, 4))
    set_rule(world.multiworld.get_location("B16F - Bat 2", player), lambda state: state.has("Blue Key", player, 4) and state.has("Flare", player, 1))
    set_rule(world.multiworld.get_location("B16F - Bat 2", player), lambda state: state.has("Blue Key", player, 4) and state.has("Flare", player, 1))

    set_rule(world.multiworld.get_location("B20F - Boulder 1", player), lambda state: state.has("Dynamite", player, 4))
    set_rule(world.multiworld.get_location("B20F - Boulder 2", player), lambda state: state.has("Dynamite", player, 4))
    set_rule(world.multiworld.get_location("B20F - Boulder 3", player), lambda state: state.has("Dynamite", player, 4))

    set_rule(world.multiworld.get_location("B19F - Past Boulder", player), lambda state: state.has("Dynamite", player, 4))
    set_rule(world.multiworld.get_location("B20F - Right Side Bombable Wall", player), lambda state: state.has("Dynamite", player, 5))

    set_rule(world.multiworld.get_location("B21F - Bat Pit 1", player), lambda state: state.has("Flare", player, 1))
    set_rule(world.multiworld.get_location("B21F - Bat Pit 2", player), lambda state: state.has("Flare", player, 1))
    set_rule(world.multiworld.get_location("B21F - Bat Pit 3", player), lambda state: state.has("Flare", player, 1))

    set_rule(world.multiworld.get_location("B23F - Pyramid Bombable Wall", player), lambda state: state.has("Dynamite", player, 4))

    set_rule(world.multiworld.get_location("B23F - Just After Door", player), lambda state: state.has("Red Key", player, 4))
    set_rule(world.multiworld.get_location("B23F - Ropes Right Wall", player), lambda state: state.has("Red Key", player, 4))
    set_rule(world.multiworld.get_location("B25F - Ropes Item", player), lambda state: state.has("Red Key", player, 4))

    set_rule(world.multiworld.get_location("B23F - Just After Door", player), lambda state: state.has("Red Key", player, 4))
    set_rule(world.multiworld.get_location("B26F - Rope Right 1", player), lambda state: state.has("Red Key", player, 4))
    set_rule(world.multiworld.get_location("B26F - Rope Right 2", player), lambda state: state.has("Red Key", player, 4))
    set_rule(world.multiworld.get_location("B26F - So Close You Can Smell It Item", player), lambda state: state.has("Red Key", player, 4))
    set_rule(world.multiworld.get_location("B27F - Right of Pit 1", player), lambda state: state.has("Red Key", player, 4))
    set_rule(world.multiworld.get_location("B27F - Right of Pit 2", player), lambda state: state.has("Red Key", player, 4))
    set_rule(world.multiworld.get_location("B27F - Entry Item", player), lambda state: state.has("Red Key", player, 4))

    set_rule(world.multiworld.get_location("B28F - Boulder Item", player), lambda state: state.has("Red Key", player, 4) and state.has("Dynamite", player, 4))
    set_rule(world.multiworld.get_location("B28F - Bat Ledge", player), lambda state: state.has("Red Key", player, 4) and state.has("Dynamite", player, 4) and state.has("Flare", player, 1))

    set_rule(world.multiworld.get_location("B29F - Ladder Ledge", player), lambda state: state.has("Red Key", player, 4) and state.has("Dynamite", player, 4))
    set_rule(world.multiworld.get_location("B29F - Pit Trap", player), lambda state: state.has("Red Key", player, 4) and state.has("Dynamite", player, 4))
    set_rule(world.multiworld.get_location("B29F - Before Pit Trap", player), lambda state: state.has("Red Key", player, 4) and state.has("Dynamite", player, 4))
    set_rule(world.multiworld.get_location("B29F - Rope Alcove", player), lambda state: state.has("Red Key", player, 4) and state.has("Dynamite", player, 4))

    set_rule(world.multiworld.get_location("B30F - Far Bottom Right", player), lambda state: state.has("Red Key", player, 4) and state.has("Dynamite", player, 4))
    set_rule(world.multiworld.get_location("B30F - Undulating Rocks", player), lambda state: state.has("Red Key", player, 4) and state.has("Dynamite", player, 4))

    set_rule(world.multiworld.get_location("B30F - Mound Item", player), lambda state: state.has("Red Key", player, 4) and state.has("Dynamite", player, 4) and state.has("Blue Key", player, 5))

    set_rule(world.multiworld.get_location("B30F - Far Bottom Left", player), lambda state: state.has("Red Key", player, 4) and state.has("Dynamite", player, 5) and state.has("Blue Key", player, 5))
    set_rule(world.multiworld.get_location("B29F - Left Wall Rope Ledge", player), lambda state: state.has("Red Key", player, 4) and state.has("Dynamite", player, 5) and state.has("Blue Key", player, 5))
    set_rule(world.multiworld.get_location("B29F - Left Pit Item", player), lambda state: state.has("Red Key", player, 4) and state.has("Dynamite", player, 5) and state.has("Blue Key", player, 5))

    set_rule(world.multiworld.get_location("B29F - Bombable Wall", player), lambda state: state.has("Red Key", player, 4) and state.has("Dynamite", player, 6) and state.has("Blue Key", player, 5))

    set_rule(world.multiworld.get_location("B29F - Left Wall Item", player), lambda state: state.has("Red Key", player, 4) and state.has("Dynamite", player, 5) and state.has("Blue Key", player, 5))

    set_rule(world.multiworld.get_location("B28F - Locked Item 1", player), lambda state: state.has("Red Key", player, 5) and state.has("Dynamite", player, 5) and state.has("Blue Key", player, 5))
    set_rule(world.multiworld.get_location("B28F - Locked Item 2", player), lambda state: state.has("Red Key", player, 5) and state.has("Dynamite", player, 5) and state.has("Blue Key", player, 5))

    set_rule(world.multiworld.get_location("B28F - Final Rope Left", player), lambda state: state.has("Red Key", player, 4) and state.has("Dynamite", player, 5) and state.has("Blue Key", player, 5))
    set_rule(world.multiworld.get_location("B28F - Final Rope Right", player), lambda state: state.has("Red Key", player, 4) and state.has("Dynamite", player, 5) and state.has("Blue Key", player, 5))

    set_rule(world.multiworld.get_location("B28F - Final Boulder", player), lambda state: state.has("Red Key", player, 4) and state.has("Dynamite", player, 6) and state.has("Blue Key", player, 5))

    set_rule(world.multiworld.get_location("Golden Pyramid", player), lambda state: state.has("Red Key", player, 5) and state.has("Dynamite", player, 6) and state.has("Blue Key", player, 6))

    hidden_rules(world)
    

def hidden_rules(world: "YoshisIslandWorld") -> None:
    player = world.player
    if not world.options.hidden_items:
        return
    set_rule(world.multiworld.get_location("B1F - Side Shaft Hidden Item", player), lambda state: state.has("Dynamite", player, 1))
    set_rule(world.multiworld.get_location("B8F - Boulder Pit Hidden Item", player), lambda state: state.has("Dynamite", player, 2))
    set_rule(world.multiworld.get_location("B16F - Blue Door Hidden Item", player), lambda state: state.has("Blue Key", player, 4))