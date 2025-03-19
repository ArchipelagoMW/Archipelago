from BaseClasses import CollectionState
from worlds.AutoWorld import World
from worlds.candybox2 import CandyBox2Options
from worlds.generic.Rules import set_rule, add_rule

weapons = [
    "Wooden Sword",
    "Iron Axe",
    "The Monkey Wizard Staff",
    "Polished Silver Sword",
    "The Troll's Bludgeon",
    "Summoning Tribal Spear",
    "Enchanted Monkey Wizard Staff",
    "Giant Spoon of Doom",
    "Scythe"
]

armors = [
    "Lightweight Body Armour",
    "Knight Body Armour",
    "Enchanted Knight Body Armour"
]

def can_jump(state: CollectionState, player: int):
    return (state.has("Rocket Boots", player) or state.has("A desert bird feather", player)) and state.has("The Pogo Stick", player)

def set_rules(world: World, player: int):

    # The Hole rules
    add_rule(world.get_location("Heart Pendant Acquired"), lambda state: can_jump(state, player))
    add_rule(world.get_location("Black Magic Grimoire Acquired"), lambda state: state.has("The Sponge", player))
    add_rule(world.get_location("Desert Fortress Key Acquired"), lambda state: state.has("The Sponge", player) and can_jump(state, player))
    add_rule(world.get_location("Tribal Spear Acquired"), lambda state: weapon_is_at_least(state, player, "Enchanted Monkey Wizard Staff") and state.has("Octopus King Crown with Jaspers", player) and armor_is_at_least(state, player, "Lightweight Body Armour"))
    add_rule(world.get_location("Four Chocolate Bars in The Hole Acquired"), lambda state: weapon_is_at_least(state, player, "Enchanted Monkey Wizard Staff") and state.has("Octopus King Crown with Jaspers", player) and armor_is_at_least(state, player, "Lightweight Body Armour"))


def weapon_is_at_least(state: CollectionState, player: int, minimum_weapon: str):
    for weapon in weapons[weapons.index(minimum_weapon):]:
        if state.has(weapon, player):
            return True
    return False

def armor_is_at_least(state: CollectionState, player: int, minimum_armor: str):
    for armor in armors[armors.index(minimum_armor):]:
        if state.has(armor, player):
            return True
    return False
