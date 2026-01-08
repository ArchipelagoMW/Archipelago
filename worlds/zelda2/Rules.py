from worlds.generic.Rules import set_rule, add_rule
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Z2World

def apply_location_rules(world, target, rule):
    add_rule(world.multiworld.get_location(target, world.player), rule)

def apply_region_rules(world, target, rule):
    add_rule(world.multiworld.get_entrance(target, world.player), rule)

def set_location_rules(world: "Z2World") -> None:
    can_get_high = ("Jump Spell", "Fairy Spell")

    if world.options.candle_required:
        apply_location_rules(world, "Northern Desert Cave", lambda state: state.has("Candle", world.player))
        apply_location_rules(world, "North Castle Cave", lambda state: state.has("Candle", world.player))
        apply_location_rules(world, "Western Swamp Cave", lambda state: state.has("Candle", world.player))
        apply_location_rules(world, "Clear Cave South of Rauru", lambda state: state.has("Candle", world.player))
        apply_location_rules(world, "Blocked Cave South of Rauru", lambda state: state.has("Candle", world.player))
        apply_location_rules(world, "Death Mountain Platforms", lambda state: state.has("Candle", world.player))
        apply_location_rules(world, "Death Mountain Staircase", lambda state: state.has("Candle", world.player))
        apply_location_rules(world, "Death Mountain Boulder Pit", lambda state: state.has("Candle", world.player))
        apply_location_rules(world, "Death Mountain Ending Item", lambda state: state.has("Candle", world.player))
        apply_location_rules(world, "Death Mountain East-Facing Dead End", lambda state: state.has("Candle", world.player))
        apply_location_rules(world, "Eastern Cave", lambda state: state.has("Candle", world.player))
        apply_location_rules(world, "Maze Island Right Hole", lambda state: state.has("Candle", world.player))
        apply_location_rules(world, "Southeastern Swamp Cave", lambda state: state.has("Candle", world.player))
        apply_location_rules(world, "Death Valley Entrance", lambda state: state.has("Candle", world.player))
        apply_location_rules(world, "Death Valley Midway Item", lambda state: state.has("Candle", world.player))
        apply_location_rules(world, "Sage of New Kasuto", lambda state: state.has("Candle", world.player))
        apply_location_rules(world, "New Kasuto Shrine", lambda state: state.has("Candle", world.player))
        apply_location_rules(world, "New Kasuto House", lambda state: state.has("Candle", world.player))

    if world.options.cross_required:
        apply_location_rules(world, "Sage of Kasuto", lambda state: state.has("Cross", world.player))
        apply_location_rules(world, "Death Valley Entrance", lambda state: state.has("Cross", world.player))
        apply_location_rules(world, "Death Valley Midway Item", lambda state: state.has("Cross", world.player))

    apply_location_rules(world, "Sage of Ruto", lambda state: state.has("Trophy", world.player))

    apply_location_rules(world, "Parapa Palace: Pedestal Item", lambda state: state.has("Parapa Palace Key", world.player, 3) or state.has("Magical Key", world.player))
    apply_location_rules(world, "Parapa Palace: Crumbling Bridge", lambda state: state.has("Parapa Palace Key", world.player) or state.has("Magical Key", world.player))
    apply_location_rules(world, "Parapa Palace: Stairwell", lambda state: state.has("Parapa Palace Key", world.player) or state.has("Magical Key", world.player))
    apply_location_rules(world, "Parapa Palace: Guarded Item", lambda state: state.has("Parapa Palace Key", world.player) or state.has("Magical Key", world.player))
    apply_location_rules(world, "Parapa Palace: Horsehead Drop", lambda state: state.has("Parapa Palace Key", world.player, 3) or state.has("Magical Key", world.player))
    apply_location_rules(world, "Parapa Palace: Statue", lambda state: state.has("Parapa Palace Key", world.player, 3) or state.has("Magical Key", world.player))

    apply_location_rules(world, "Western Swamp Cave", lambda state: state.has("Hammer", world.player))
    apply_location_rules(world, "Blocked Cave South of Rauru", lambda state: state.has("Hammer", world.player))

    apply_location_rules(world, "Midoro Palace: Lava Blocks Item", lambda state: state.has("Midoro Palace Key", world.player) or state.has("Magical Key", world.player))
    apply_location_rules(world, "Midoro Palace: Falling Blocks Item", lambda state: state.has("Midoro Palace Key", world.player, 3) or state.has("Magical Key", world.player))
    apply_location_rules(world, "Midoro Palace: Pedestal Item", lambda state: state.has("Midoro Palace Key", world.player, 4) or state.has("Magical Key", world.player))
    apply_location_rules(world, "Midoro Palace: Guarded Item", lambda state: (state.has("Midoro Palace Key", world.player) or state.has("Magical Key", world.player)) and state.has("Handy Glove", world.player))
    apply_location_rules(world, "Midoro Palace: Crumbling Blocks", lambda state: (state.has("Midoro Palace Key", world.player) or state.has("Magical Key", world.player)) and state.has("Handy Glove", world.player))
    apply_location_rules(world, "Midoro Palace: Helmethead Drop", lambda state: (state.has("Midoro Palace Key", world.player, 3) or state.has("Magical Key", world.player)) and state.has("Handy Glove", world.player))
    apply_location_rules(world, "Midoro Palace: Statue", lambda state: (state.has("Midoro Palace Key", world.player, 3) or state.has("Magical Key", world.player)) and state.has("Handy Glove", world.player))

    apply_location_rules(world, "Death Mountain Boulder Pit", lambda state: state.has("Hammer", world.player))
    apply_location_rules(world, "Death Mountain Platforms", lambda state: state.has("Jump Spell", world.player))

    apply_location_rules(world, "Sage of Mido", lambda state: state.has("Water of Life", world.player))
    apply_location_rules(world, "Mido Swordsman", lambda state: state.has_any(can_get_high, world.player))

    apply_location_rules(world, "Island Palace: Buried Item Left", lambda state: state.has_all(("Handy Glove", "Down Thrust"), world.player))
    apply_location_rules(world, "Island Palace: Buried Item Right", lambda state: state.has_all(("Handy Glove", "Down Thrust"), world.player))
    apply_location_rules(world, "Island Palace: Precarious Item", lambda state: (state.has("Island Palace Key", world.player, 3) or state.has("Magical Key", world.player)) and state.has("Handy Glove", world.player))
    apply_location_rules(world, "Island Palace: Pedestal Item", lambda state: (state.has("Island Palace Key", world.player, 4) or state.has("Magical Key", world.player)) and state.has("Handy Glove", world.player))
    apply_location_rules(world, "Island Palace: Block Mountain", lambda state: (state.has("Island Palace Key", world.player, 3) or state.has("Magical Key", world.player)) and state.has("Handy Glove", world.player))
    apply_location_rules(world, "Island Palace: Pillar Item", lambda state:(state.has("Island Palace Key", world.player, 4) or state.has("Magical Key", world.player)) and state.has("Jump Spell", world.player))
    apply_location_rules(world, "Island Palace: Guarded by Iron Knuckles", lambda state: (state.has("Island Palace Key", world.player, 4) or state.has("Magical Key", world.player)) and state.has_all(("Handy Glove", "Down Thrust"), world.player))
    apply_location_rules(world, "Island Palace: Rebonack Drop", lambda state:(state.has("Island Palace Key", world.player, 4) or state.has("Magical Key", world.player)) and state.has_all(("Handy Glove", "Down Thrust"), world.player))
    apply_location_rules(world, "Island Palace: Statue", lambda state:(state.has("Island Palace Key", world.player, 4) or state.has("Magical Key", world.player)) and state.has_all(("Handy Glove", "Down Thrust"), world.player))

    apply_location_rules(world, "Eastern Peninsula Secret", lambda state: state.has_any(("Boots", "Hammer"), world.player) and state.has("Jump Spell", world.player))
    apply_location_rules(world, "Ocean Item", lambda state: state.has("Boots", world.player))

    apply_location_rules(world, "Darunia Swordsman", lambda state: state.has("Jump Spell", world.player))
    apply_location_rules(world, "Sage of Darunia", lambda state: state.has("Child", world.player))

    apply_location_rules(world, "Maze Palace: Nook Item", lambda state: state.has("Down Thrust", world.player))
    apply_location_rules(world, "Maze Palace: Sealed Item", lambda state: (state.has("Maze Palace Key", world.player, 3) or state.has("Magical Key", world.player)) and state.has_all(("Handy Glove", "Up Thrust", "Jump Spell"), world.player))
    apply_location_rules(world, "Maze Palace: Block Mountain Left", lambda state: (state.has("Maze Palace Key", world.player, 4) or state.has("Magical Key", world.player)) and state.has("Handy Glove", world.player))
    apply_location_rules(world, "Maze Palace: Block Mountain Right", lambda state: (state.has("Maze Palace Key", world.player, 4) or state.has("Magical Key", world.player)) and state.has("Handy Glove", world.player))
    apply_location_rules(world, "Maze Palace: West Hall of Fire", lambda state: state.has("Maze Palace Key", world.player, 4) or state.has("Magical Key", world.player))
    apply_location_rules(world, "Maze Palace: Pedestal Item", lambda state: state.has("Maze Palace Key", world.player, 5) or state.has("Magical Key", world.player))
    apply_location_rules(world, "Maze Palace: Block Mountain Basement", lambda state: state.has("Handy Glove", world.player))
    apply_location_rules(world, "Maze Palace: Pillar Item", lambda state: (state.has("Maze Palace Key", world.player, 6) or state.has("Magical Key", world.player)) and state.has("Jump Spell", world.player))
    apply_location_rules(world, "Maze Palace: Carock Drop", lambda state: (state.has("Maze Palace Key", world.player, 6) or state.has("Magical Key", world.player)) and state.has("Reflect Spell", world.player))
    apply_location_rules(world, "Maze Palace: Statue", lambda state:(state.has("Maze Palace Key", world.player, 6) or state.has("Magical Key", world.player)) and state.has("Reflect Spell", world.player))

    apply_location_rules(world, "Palace on the Sea: Ledge Item", lambda state: state.has("Fairy Spell", world.player))
    apply_location_rules(world, "Palace on the Sea: Crumbling Bridge", lambda state: state.has("Fairy Spell", world.player))
    apply_location_rules(world, "Palace on the Sea: Falling Blocks", lambda state: state.has_all(("Fairy Spell", "Handy Glove"), world.player) and (state.has("Sea Palace Key", world.player) or state.has("Magical Key", world.player)))
    apply_location_rules(world, "Palace on the Sea: Above Elevator", lambda state: state.has_all(("Fairy Spell", "Jump Spell"), world.player) and (state.has("Sea Palace Key", world.player) or state.has("Magical Key", world.player)))
    apply_location_rules(world, "Palace on the Sea: Block Alcove", lambda state: state.has_all(("Fairy Spell", "Handy Glove", "Up Thrust", "Down Thrust"), world.player) and (state.has("Sea Palace Key", world.player) or state.has("Magical Key", world.player)))
    apply_location_rules(world, "Palace on the Sea: Knuckle Alcove", lambda state: state.has_all(("Fairy Spell", "Jump Spell"), world.player) and (state.has("Sea Palace Key", world.player) or state.has("Magical Key", world.player)))
    apply_location_rules(world, "Palace on the Sea: Pedestal Item", lambda state: state.has("Fairy Spell", world.player) and (state.has("Sea Palace Key", world.player, 5) or state.has("Magical Key", world.player)))
    apply_location_rules(world, "Palace on the Sea: Skeleton Key", lambda state: state.has("Fairy Spell", world.player) and (state.has("Sea Palace Key", world.player) or state.has("Magical Key", world.player)))
    apply_location_rules(world, "Palace on the Sea: West Wing", lambda state: state.has("Fairy Spell", world.player) and (state.has("Sea Palace Key", world.player, 4) or state.has("Magical Key", world.player)))
    apply_location_rules(world, "Palace on the Sea: Block Line", lambda state: state.has("Fairy Spell", world.player) and state.has_any(("Handy Glove", "Jump Spell"), world.player) and (state.has("Sea Palace Key", world.player, 4) or state.has("Magical Key", world.player)))
    apply_location_rules(world, "Palace on the Sea: West Knuckle Alcove", lambda state: state.has_all(("Fairy Spell", "Handy Glove", "Up Thrust", "Down Thrust"), world.player) and (state.has("Sea Palace Key", world.player, 4) or state.has("Magical Key", world.player)))
    apply_location_rules(world, "Palace on the Sea: Gooma Drop", lambda state: state.has("Fairy Spell", world.player) and (state.has("Sea Palace Key", world.player, 5) or state.has("Magical Key", world.player)))
    apply_location_rules(world, "Palace on the Sea: Statue", lambda state: state.has("Fairy Spell", world.player) and (state.has("Sea Palace Key", world.player, 5) or state.has("Magical Key", world.player)))

    apply_location_rules(world, "Southeastern Swamp", lambda state: state.has_any(can_get_high, world.player))
    apply_location_rules(world, "Sage of New Kasuto", lambda state: state.has("Hammer", world.player))
    apply_location_rules(world, "New Kasuto Shrine", lambda state: state.has_all(("Hammer", "Spell Spell"), world.player))
    apply_location_rules(world, "New Kasuto House", lambda state: state.has("Hammer", world.player) and state.has("Magic Container", world.player, 3))

    apply_location_rules(world, "Three-Eye Rock Palace: 1F Block Mountain", lambda state: state.has("Handy Glove", world.player))
    apply_location_rules(world, "Three-Eye Rock Palace: 1F Enclosed Item", lambda state: state.has_all(("Handy Glove", "Jump Spell", "Up Thrust"), world.player))
    apply_location_rules(world, "Three-Eye Rock Palace: Middle Pit", lambda state: state.has("Three-Eye Rock Palace Key", world.player) or state.has("Magical Key", world.player))
    apply_location_rules(world, "Three-Eye Rock Palace: Bottom Pit", lambda state: state.has("Three-Eye Rock Palace Key", world.player) or state.has("Magical Key", world.player))
    apply_location_rules(world, "Three-Eye Rock Palace: Pit of Sadness", lambda state: state.has("Handy Glove", world.player) and (state.has("Magical Key", world.player) or state.has("Three-Eye Rock Palace Key", world.player, 5)))
    apply_location_rules(world, "Three-Eye Rock Palace: Block Stairs", lambda state: state.has("Handy Glove", world.player) and (state.has("Magical Key", world.player) or state.has("Three-Eye Rock Palace Key", world.player, 5)))
    apply_location_rules(world, "Three-Eye Rock Palace: Pedestal Item", lambda state: state.has("Handy Glove", world.player) and (state.has("Magical Key", world.player) or state.has("Three-Eye Rock Palace Key", world.player, 7)))
    apply_location_rules(world, "Three-Eye Rock Palace: Return of Helmethead", lambda state: state.has("Handy Glove", world.player) and (state.has("Magical Key", world.player) or state.has("Three-Eye Rock Palace Key", world.player, 5)))
    apply_location_rules(world, "Three-Eye Rock Palace: Helmethead III: The Revengening", lambda state: state.has_all(("Handy Glove", "Fairy Spell"), world.player) and (state.has("Magical Key", world.player) or state.has("Three-Eye Rock Palace Key", world.player, 7)))
    apply_location_rules(world, "Three-Eye Rock Palace: Pit Hall", lambda state: state.has_all(("Handy Glove", "Fairy Spell"), world.player) and (state.has("Magical Key", world.player) or state.has("Three-Eye Rock Palace Key", world.player, 7)))
    apply_location_rules(world, "Three-Eye Rock Palace: Basement Block Mountain", lambda state: state.has_all(("Handy Glove", "Fairy Spell"), world.player) and (state.has("Magical Key", world.player) or state.has("Three-Eye Rock Palace Key", world.player, 3)))
    apply_location_rules(world, "Three-Eye Rock Palace: Barba Drop", lambda state: state.has_all(("Handy Glove", "Fairy Spell"), world.player) and (state.has("Magical Key", world.player) or state.has("Three-Eye Rock Palace Key", world.player, 7)))
    apply_location_rules(world, "Three-Eye Rock Palace: Statue", lambda state: state.has_all(("Handy Glove", "Fairy Spell"), world.player) and (state.has("Magical Key", world.player) or state.has("Three-Eye Rock Palace Key", world.player, 7)))

    apply_location_rules(world, "Great Palace - East Wing Item", lambda state: state.has_all(("Handy Glove", "Down Thrust"), world.player))
    apply_location_rules(world, "Great Palace - Thunderbird Drop", lambda state: state.has_all(("Handy Glove", "Down Thrust", "Thunder Spell"), world.player))
    apply_location_rules(world, "Dark Link", lambda state: state.has_all(("Handy Glove", "Down Thrust", "Thunder Spell"), world.player))
    

def set_region_rules(world: "Z2World") -> None:
    can_get_high = ("Jump Spell", "Fairy Spell")

    if world.options.candle_required:
        apply_region_rules(world, "Eastern Hyrule -> Northeastern Hyrule", lambda state: state.has_any(("Candle", "Boots"), world.player))
        apply_region_rules(world, "Southeastern Hyrule -> Great Palace", lambda state: state.has("Candle", world.player))
        apply_region_rules(world, "Western Coast -> Island Palace", lambda state: state.has("Candle", world.player))
        # If candle isn't required, this has no rule anyway
        if not world.options.remove_early_boulder:
            apply_region_rules(world, "Northwestern Hyrule -> Western Hyrule", lambda state: (state.has("Candle", world.player) and state.has_any(can_get_high, world.player)) or state.has("Hammer", world.player))
            apply_region_rules(world, "Western Hyrule -> Northwestern Hyrule", lambda state: state.has_any(("Candle", "Hammer"), world.player))

    if world.options.better_boots:
        apply_region_rules(world, "Death Mountain -> Western Hyrule", lambda state: state.has_any(("Bagu's Letter", "Fairy Spell", "Boots"), world.player))
        apply_region_rules(world, "Western Hyrule -> Death Mountain", lambda state: state.has_any(("Bagu's Letter", "Fairy Spell", "Boots"), world.player))
    else:
        apply_region_rules(world, "Death Mountain -> Western Hyrule", lambda state: state.has_any(("Bagu's Letter", "Fairy Spell"), world.player))
        apply_region_rules(world, "Western Hyrule -> Death Mountain", lambda state: state.has_any(("Bagu's Letter", "Fairy Spell"), world.player))

    if world.options.cross_required:
        apply_region_rules(world, "Southeastern Hyrule -> Great Palace", lambda state: state.has("Cross", world.player))

    apply_region_rules(world, "Western Hyrule -> Western Coast", lambda state: state.has("Hammer", world.player))

    apply_region_rules(world, "Western Coast -> Western Hyrule", lambda state: state.has("Hammer", world.player))
    apply_region_rules(world, "Western Coast -> Island Palace", lambda state: state.has("Fairy Spell", world.player))
    apply_region_rules(world, "Western Coast -> Eastern Hyrule", lambda state: state.has("Raft", world.player))
    apply_region_rules(world, "Eastern Hyrule -> Western Coast", lambda state: state.has("Raft", world.player))
    apply_region_rules(world, "Eastern Hyrule -> Southeastern Hyrule", lambda state: state.has("Flute", world.player))
    apply_region_rules(world, "Eastern Hyrule -> Palace on the Sea", lambda state: state.has("Boots", world.player))

    apply_region_rules(world, "Southeastern Hyrule -> Eastern Hyrule", lambda state: state.has("Flute", world.player))
    apply_region_rules(world, "Southeastern Hyrule -> Three-Eye Rock Palace", lambda state: state.has("Flute", world.player))

    apply_region_rules(world, "Southeastern Hyrule -> Great Palace", lambda state: state.has("Crystal Returned", world.player, world.options.required_crystals.value))