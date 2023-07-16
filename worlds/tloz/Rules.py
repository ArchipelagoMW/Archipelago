from typing import TYPE_CHECKING

from worlds.generic.Rules import add_rule
from .Locations import food_locations, shop_locations
from .ItemPool import dangerous_weapon_locations
from .Options import StartingPosition

if TYPE_CHECKING:
    from . import TLoZWorld

def set_rules(tloz_world: "TLoZWorld"):
    player = tloz_world.player
    world = tloz_world.multiworld

    # Boss events for a nicer spoiler log play through
    for level in range(1, 9):
        boss = world.get_location(f"Level {level} Boss", player)
        boss_event = world.get_location(f"Level {level} Boss Status", player)
        status = tloz_world.create_event(f"Boss {level} Defeated")
        boss_event.place_locked_item(status)
        add_rule(boss_event, lambda state, b=boss: state.can_reach(b, "Location", player))

    # No dungeons without weapons except for the dangerous weapon locations if we're dangerous, no unsafe dungeons
    for i, level in enumerate(tloz_world.levels[1:10]):
        for location in level.locations:
            if world.StartingPosition[player] < StartingPosition.option_dangerous \
                    or location.name not in dangerous_weapon_locations:
                add_rule(world.get_location(location.name, player),
                         lambda state: state.has_group("weapons", player))
            if i > 0:  # Don't need an extra heart for Level 1
                add_rule(world.get_location(location.name, player),
                         lambda state, hearts=i: state.has("Heart Container", player, hearts) or
                                       (state.has("Blue Ring", player) and
                                        state.has("Heart Container", player, int(hearts / 2))) or
                                       (state.has("Red Ring", player) and
                                        state.has("Heart Container", player, int(hearts / 4))))
            if "Pols Voice" in location.name:  # This enemy needs specific weapons
                add_rule(world.get_location(location.name, player),
                         lambda state: state.has_group("swords", player) or state.has("Bow", player))

    # No requiring anything in a shop until we can farm for money
    for location in shop_locations:
        add_rule(world.get_location(location, player),
                 lambda state: state.has_group("weapons", player))

    # Everything from 4 on up has dark rooms
    for level in tloz_world.levels[4:]:
        for location in level.locations:
            add_rule(world.get_location(location.name, player),
                     lambda state: state.has_group("candles", player)
                                   or (state.has("Magical Rod", player) and state.has("Book", player)))

    # Everything from 5 on up has gaps
    for level in tloz_world.levels[5:]:
        for location in level.locations:
            add_rule(world.get_location(location.name, player),
                     lambda state: state.has("Stepladder", player))

    add_rule(world.get_location("Level 5 Boss", player),
             lambda state: state.has("Recorder", player))

    add_rule(world.get_location("Level 6 Boss", player),
             lambda state: state.has("Bow", player) and state.has_group("arrows", player))

    add_rule(world.get_location("Level 7 Item (Red Candle)", player),
             lambda state: state.has("Recorder", player))
    add_rule(world.get_location("Level 7 Boss", player),
             lambda state: state.has("Recorder", player))
    if world.ExpandedPool[player]:
        add_rule(world.get_location("Level 7 Key Drop (Stalfos)", player),
                 lambda state: state.has("Recorder", player))
        add_rule(world.get_location("Level 7 Bomb Drop (Digdogger)", player),
                 lambda state: state.has("Recorder", player))
        add_rule(world.get_location("Level 7 Rupee Drop (Dodongos)", player),
                 lambda state: state.has("Recorder", player))

    for location in food_locations:
        if world.ExpandedPool[player] or "Drop" not in location:
            add_rule(world.get_location(location, player),
                     lambda state: state.has("Food", player))

    add_rule(world.get_location("Level 8 Item (Magical Key)", player),
             lambda state: state.has("Bow", player) and state.has_group("arrows", player))
    if world.ExpandedPool[player]:
        add_rule(world.get_location("Level 8 Bomb Drop (Darknuts North)", player),
                 lambda state: state.has("Bow", player) and state.has_group("arrows", player))

    for location in tloz_world.levels[9].locations:
        add_rule(world.get_location(location.name, player),
                 lambda state: state.has("Triforce Fragment", player, 8) and
                               state.has_group("swords", player))

    # Yes we are looping this range again for Triforce locations. No I can't add it to the boss event loop
    for level in range(1, 9):
        add_rule(world.get_location(f"Level {level} Triforce", player),
                 lambda state, l=level: state.has(f"Boss {l} Defeated", player))

    # Sword, raft, and ladder spots
    add_rule(world.get_location("White Sword Pond", player),
             lambda state: state.has("Heart Container", player, 2))
    add_rule(world.get_location("Magical Sword Grave", player),
             lambda state: state.has("Heart Container", player, 9))

    stepladder_locations = ["Ocean Heart Container", "Level 4 Triforce", "Level 4 Boss", "Level 4 Map"]
    stepladder_locations_expanded = ["Level 4 Key Drop (Keese North)"]
    for location in stepladder_locations:
        add_rule(world.get_location(location, player),
                 lambda state: state.has("Stepladder", player))
    if world.ExpandedPool[player]:
        for location in stepladder_locations_expanded:
            add_rule(world.get_location(location, player),
                     lambda state: state.has("Stepladder", player))

    # Don't allow Take Any Items until we can actually get in one
    if world.ExpandedPool[player]:
        add_rule(world.get_location("Take Any Item Left", player),
                 lambda state: state.has_group("candles", player) or
                               state.has("Raft", player))
        add_rule(world.get_location("Take Any Item Middle", player),
                 lambda state: state.has_group("candles", player) or
                               state.has("Raft", player))
        add_rule(world.get_location("Take Any Item Right", player),
                 lambda state: state.has_group("candles", player) or
                               state.has("Raft", player))
    for location in tloz_world.levels[4].locations:
        add_rule(world.get_location(location.name, player),
                 lambda state: state.has("Raft", player) or state.has("Recorder", player))
    for location in tloz_world.levels[7].locations:
        add_rule(world.get_location(location.name, player),
                 lambda state: state.has("Recorder", player))
    for location in tloz_world.levels[8].locations:
        add_rule(world.get_location(location.name, player),
                 lambda state: state.has("Bow", player))

    add_rule(world.get_location("Potion Shop Item Left", player),
             lambda state: state.has("Letter", player))
    add_rule(world.get_location("Potion Shop Item Middle", player),
             lambda state: state.has("Letter", player))
    add_rule(world.get_location("Potion Shop Item Right", player),
             lambda state: state.has("Letter", player))

    add_rule(world.get_location("Shield Shop Item Left", player),
             lambda state: state.has_group("candles", player) or
                           state.has("Bomb", player))
    add_rule(world.get_location("Shield Shop Item Middle", player),
             lambda state: state.has_group("candles", player) or
                           state.has("Bomb", player))
    add_rule(world.get_location("Shield Shop Item Right", player),
             lambda state: state.has_group("candles", player) or
                           state.has("Bomb", player))