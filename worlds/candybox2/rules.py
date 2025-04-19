from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.candybox2.items import candy_box_2_base_id, items
from worlds.generic.Rules import add_rule
from .rooms import CandyBox2Room, entrance_friendly_names

if TYPE_CHECKING:
    from . import CandyBox2World

weapons = [
    "Nothing (Weapon)",
    "Wooden Sword",
    "Iron Axe",
    "Polished Silver Sword",
    "Troll's Bludgeon",
    "Monkey Wizard Staff",
    "Enchanted Monkey Wizard Staff",
    "Tribal Spear",
    "Summoning Tribal Spear",
    "Giant Spoon",
    "Scythe",
    "Giant Spoon of Doom",
]

armors = [
    "Lightweight Body Armour",
    "Knight Body Armour",
    "Enchanted Knight Body Armour"
]

def has_projectiles(world: "CandyBox2World", state: CollectionState, player: int):
    return state.has("Red Enchanted Gloves", player) or state.has("Octopus King Crown with Jaspers", player) or has_weapon(world, state, player, "Enchanted Monkey Wizard Staff")

def can_jump(state: CollectionState, player: int):
    return (state.has("Rocket Boots", player) or state.has("Desert bird feather", player)) and state.has("Pogo Stick", player)

def can_fly(state: CollectionState, player: int):
    return state.has("Rocket Boots", player) and state.has("Pogo Stick", player)

def can_escape_hole(state: CollectionState, player: int):
    return can_fly(state, player) or state.has("Beginners' Grimoire", player)

def sea_entrance(world: "CandyBox2World", state: CollectionState, player: int):
    return weapon_is_at_least(world, state, player, "Summoning Tribal Spear") and has_projectiles(world, state,
                                                                                                  player) and armor_is_at_least(state, player,
                                                                                             "Lightweight Body Armour")

def can_beat_sharks(world: "CandyBox2World", state: CollectionState, player: int):
    return sea_entrance(world, state, player) and weapon_is_at_least(world, state, player,
                                                                     "Enchanted Monkey Wizard Staff")

def set_rules(world: "CandyBox2World", player: int):

    add_rule(world.get_location("Disappointed Emote Chocolate Bar"), lambda state: can_farm_candies(state, player))

    # Cellar rules
    add_rule(world.get_location("Cellar Quest Cleared"), lambda state: weapon_is_at_least(world, state, player,
                                                                                          "Wooden Sword"))

    # Desert rules
    add_rule(world.get_location("Desert Quest Cleared"), lambda state: weapon_is_at_least(world, state, player,
                                                                                          "Iron Axe"))
    add_rule(world.get_location("Desert Bird Feather Acquired"), lambda state: weapon_is_at_least(world, state, player,
                                                                                                  "Iron Axe") and has_projectiles(
        world, state, player))

    # Wishing Well rules
    add_rule(world.get_location("Enchant Red Enchanted Gloves"), lambda state: state.has("Leather Gloves", player))
    add_rule(world.get_location("Enchant Pink Enchanted Gloves"), lambda state: state.has("Leather Gloves", player))
    add_rule(world.get_location("Enchant Summoning Tribal Spear"), lambda state: has_weapon(world, state, player, "Tribal Spear"))
    add_rule(world.get_location("Enchant Enchanted Monkey Wizard Staff"), lambda state: has_weapon(world, state, player, "Monkey Wizard Staff"))
    add_rule(world.get_location("Enchant Enchanted Knight Body Armour"), lambda state: state.has("Knight Body Armour", player))
    add_rule(world.get_location("Enchant Octopus King Crown with Jaspers"), lambda state: state.has("Octopus King Crown", player))
    add_rule(world.get_location("Enchant Octopus King Crown with Obsidian"), lambda state: state.has("Octopus King Crown", player))
    add_rule(world.get_location("Enchant Giant Spoon of Doom"), lambda state: has_weapon(world, state, player, "Giant Spoon"))

    # Bridge rules
    add_rule(world.get_location("Troll Defeated"), lambda state: weapon_is_at_least(world, state, player,
                                                                                    "Polished Silver Sword"))
    add_rule(world.get_location("The Troll's Bludgeon Acquired"),
             lambda state: weapon_is_at_least(world, state, player, "Polished Silver Sword"))

    # Cave rules
    add_rule(world.get_location("Octopus King Defeated"), lambda state: state.has("Sorceress' Cauldron", player) and weapon_is_at_least(
        world, state, player, "Troll's Bludgeon") and armor_is_at_least(state, player, "Lightweight Body Armour"))
    add_rule(world.get_location("Monkey Wizard Defeated"), lambda state: state.has("Boots of Introspection", player) and state.has("Beginners' Grimoire", player) and state.has("Octopus King Crown with Jaspers", player) and weapon_is_at_least(
        world, state, player, "Troll's Bludgeon") and armor_is_at_least(state, player, "Lightweight Body Armour"))

    # The Hole rules
    add_rule(world.get_location("The Hole Heart Pendant Acquired"), lambda state: can_jump(state, player))
    add_rule(world.get_location("The Hole Black Magic Grimoire Acquired"), lambda state: can_escape_hole(state, player) and state.has("Sponge", player))
    add_rule(world.get_location("The Hole Desert Fortress Key Acquired"), lambda state: can_escape_hole(state, player) and state.has("Sponge", player) and can_jump(state, player))
    add_rule(world.get_location("The Hole Tribal Warrior Defeated"), lambda state: can_escape_hole(state, player) and weapon_is_at_least(
        world, state, player, "Enchanted Monkey Wizard Staff") and state.has("Octopus King Crown with Jaspers", player) and armor_is_at_least(state, player, "Lightweight Body Armour"))
    add_rule(world.get_location("The Hole Four Chocolate Bars in The Hole Acquired"), lambda state: can_escape_hole(state, player) and weapon_is_at_least(
        world, state, player, "Enchanted Monkey Wizard Staff") and state.has("Octopus King Crown with Jaspers", player) and armor_is_at_least(state, player, "Lightweight Body Armour"))

    # The Forest rules
    add_rule(world.get_location("Forest Quest Cleared"), lambda state: weapon_is_at_least(world, state, player,
                                                                                          "Enchanted Monkey Wizard Staff") and state.has("Octopus King Crown with Jaspers", player) and armor_is_at_least(state, player, "Lightweight Body Armour"))

    # Castle Entrance rules
    add_rule(world.get_location("Castle Entrance Quest Cleared"), lambda state: weapon_is_at_least(world, state, player,
                                                                                                   "Enchanted Monkey Wizard Staff") and state.has("Octopus King Crown with Jaspers", player) and armor_is_at_least(state, player, "Lightweight Body Armour") and state.has("Unicorn Horn", player) and state.has("Xinopherydon Claw", player))
    add_rule(world.get_location("Knight Body Armour Acquired"), lambda state: weapon_is_at_least(world, state, player,
                                                                                                 "Enchanted Monkey Wizard Staff") and state.has("Octopus King Crown with Jaspers", player) and armor_is_at_least(state, player, "Lightweight Body Armour") and state.has("Unicorn Horn", player) and state.has("Xinopherydon Claw", player))

    # Castle rules
    add_rule(world.get_location("The Giant Nougat Monster Defeated"), lambda state: state.has("Purple Fin", player) and weapon_is_at_least(
        world, state, player, "Summoning Tribal Spear") and state.has("Boots of Introspection", player) and state.has("Octopus King Crown with Obsidian", player))

    # Egg Room
    add_rule(world.get_location("Egg Room Quest cleared"), lambda state: has_weapon(world, state, player, "Nothing (Weapon)"))

    # The Desert Fortress
    add_rule(world.get_location("Xinopherydon Defeated"), lambda state: can_fly(state, player) and (has_weapon(world, state, player, "Enchanted Monkey Wizard Staff") or state.has("Octopus King Crown with Jaspers", player)))
    add_rule(world.get_location("Xinopherydon Quest Unicorn Horn Acquired"), lambda state: can_fly(state, player))
    add_rule(world.get_location("Teapot Defeated"), lambda state: weapon_is_at_least(world, state, player,
                                                                                     "Scythe") and state.has("Octopus King Crown with Obsidian", player) and state.has("Sorceress' Cauldron", player) and state.has("Xinopherydon Claw", player))
    add_rule(world.get_location("Rocket Boots Acquired"), lambda state: can_fly(state, player) or (state.has("Boots of Introspection", player) and can_jump(state, player) and (state.has("Octopus King Crown with Obsidian", player) or has_weapon(world, state, player, "Summoning Tribal Spear"))))

    # Hell rules
    add_rule(world.get_location("Devil Defeated"), lambda state: state.has("Black Magic Grimoire", player) and state.has("Unicorn Horn", player) and state.has("Boots of Introspection", player) and armor_is_at_least(state, player, "Enchanted Knight Body Armour") and state.has("Pink Enchanted Gloves", player) and has_weapon(world, state, player, "Enchanted Monkey Wizard Staff"))

    # Developer rules
    add_rule(world.get_location("The Developer Defeated"), lambda state: state.has("Purple Fin", player) and state.has("Beginners' Grimoire", player))

    # The Sea rules

    add_rule(world.get_location("The Sponge Acquired"),
             lambda state: sea_entrance(world, state, player))

    add_rule(world.get_location("The Shell Powder Acquired"),
             lambda state: sea_entrance(world, state, player))

    add_rule(world.get_location("The Red Fin Acquired"),
             lambda state: can_beat_sharks(world, state, player) and state.has("Red Enchanted Gloves", player)
                           and state.has("Octopus King Crown with Jaspers", player))

    add_rule(world.get_location("The Green Fin Acquired"),
             lambda state: can_beat_sharks(world, state, player)
                           and state.has("Advanced Grimoire", player)
                           and state.has("Red Enchanted Gloves", player)
                           and state.has("Octopus King Crown with Jaspers", player))

    add_rule(world.get_location("The Purple Fin Acquired"),
             lambda state: can_beat_sharks(world, state, player) and state.has("Heart Pendant", player)
                           and state.has("Heart Plug", player)
                           and state.has("Advanced Grimoire", player) and state.has("Red Enchanted Gloves", player)
                           and state.has("Octopus King Crown with Jaspers", player)
                           and state.has("Unicorn Horn", player))

    # X Potion
    add_rule(world.get_location("Yourself Defeated"), lambda state: state.has("Octopus King Crown", player))

    # Sorceress items
    add_rule(world.get_location("Sorceress' Hut Beginner's Grimoire"), lambda state: can_grow_lollipops(state, player))
    add_rule(world.get_location("Sorceress' Hut Advanced Grimoire"), lambda state: can_grow_lollipops(state, player))
    add_rule(world.get_location("Sorceress' Hut Hat"), lambda state: can_farm_lollipops(state, player))
    add_rule(world.get_location("Sorceress' Hut Cauldron"), lambda state: can_grow_lollipops(state, player))

    # Merchant items
    add_rule(world.get_location("Village Shop Chocolate Bar"), lambda state: can_farm_candies(state, player))
    add_rule(world.get_location("Village Shop Candy Merchant's Hat"), lambda state: can_farm_candies(state, player))

def has_weapon(world: "CandyBox2World", state: CollectionState, player: int, weapon: str):
    if state.has(weapon, player):
        return True

    if world.starting_weapon == -1:
        if state.has("Progressive Weapon", player, weapons.index(weapon)):
            return True
    else:
        for item in items:
            if items[item].code - candy_box_2_base_id == world.starting_weapon and item == weapon:
                return True

    return False

def weapon_is_at_least(world: "CandyBox2World", state: CollectionState, player: int, minimum_weapon: str):
    for weapon in weapons[weapons.index(minimum_weapon):]:
        if has_weapon(world, state, player, weapon):
            return True
    return False

def armor_is_at_least(state: CollectionState, player: int, minimum_armor: str):
    for armor in armors[armors.index(minimum_armor):]:
        if state.has(armor, player):
            return True
    return False

def chocolate_count(state: CollectionState, player: int):
    return state.count("Chocolate Bar", player) + (4 * state.count("4 Chocolate Bars", player)) + (3 * state.count("3 Chocolate Bars", player))

def lollipop_count(state: CollectionState, player: int):
    return state.count("3 Lollipops", player)*3 + state.count("Lollipop", player)

# Allows the player to plant enough lollipops at the farm for 1/minute
def can_grow_lollipops(state: CollectionState, player: int):
    return lollipop_count(state, player) >= 11 and can_reach_room(state, CandyBox2Room.LOLLIPOP_FARM, player)

def can_farm_lollipops(state: CollectionState, player: int):
    return can_grow_lollipops(state, player) and can_reach_room(state, CandyBox2Room.LOLLIPOP_FARM, player) and state.has("Pitchfork", player) and state.has("Shell Powder", player) and state.has("Green Fin", player)

# Ideally allows the player to stumble upon a quest they can use to farm candies
def can_farm_candies(state: CollectionState, player: int):
    return can_farm_lollipops(state, player) and can_reach_room(state, CandyBox2Room.LOLLIPOP_FARM, player)

def can_reach_room(state: CollectionState, room: CandyBox2Room, player: int):
    return state.can_reach_region(entrance_friendly_names[room], player)