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

def has_projectiles(state: CollectionState, player: int):
    return state.has("Red Enchanted Gloves", player) or state.has("Octopus King Crown with Jaspers", player) or state.has("Enchanted Monkey Wizard Staff", player)

def can_jump(state: CollectionState, player: int):
    return (state.has("Rocket Boots", player) or state.has("A desert bird feather", player)) and state.has("The Pogo Stick", player)

def can_fly(state: CollectionState, player: int):
    return state.has("Rocket Boots", player) and state.has("The Pogo Stick", player)

def sea_entrance(state: CollectionState, player: int):
    return weapon_is_at_least(state, player, "Enchanted Monkey Wizard Staff") and armor_is_at_least(state, player,
                                                                                             "Lightweight Body Armour")

def set_rules(world: World, player: int):

    # Cellar rules
    add_rule(world.get_location("Cellar Quest"), lambda state: weapon_is_at_least(state, player, "Wooden Sword"))

    # Desert rules
    add_rule(world.get_location("Desert Quest"), lambda state: weapon_is_at_least(state, player, "Iron Axe"))
    add_rule(world.get_location("Desert Bird Feather"), lambda state: weapon_is_at_least(state, player, "Iron Axe") and has_projectiles(state, player))

    # Bridge rules
    add_rule(world.get_location("Bridge Quest"), lambda state: weapon_is_at_least(state, player, "Polished Silver Sword"))
    add_rule(world.get_location("The Troll's Bludgeon Acquired"),
            lambda state: weapon_is_at_least(state, player, "Polished Silver Sword"))

    # Cave rules
    add_rule(world.get_location("Octopus King Quest"), lambda state: state.has("The Sorceress' Cauldron", player) and weapon_is_at_least(state, player, "The Troll's Bludgeon") and armor_is_at_least(state, player, "Lightweight Body Armour"))
    add_rule(world.get_location("Monkey Wizard Quest"), lambda state: state.has("Boots of Introspection", player) and state.has("The Beginners' Grimoire", player) and state.has("Octopus King Crown with Jaspers", player) and weapon_is_at_least(state, player, "The Troll's Bludgeon") and armor_is_at_least(state, player, "Lightweight Body Armour"))

    # The Hole rules
    add_rule(world.get_location("Heart Pendant Acquired"), lambda state: can_jump(state, player))
    add_rule(world.get_location("Black Magic Grimoire Acquired"), lambda state: state.has("The Sponge", player))
    add_rule(world.get_location("Desert Fortress Key Acquired"), lambda state: state.has("The Sponge", player) and can_jump(state, player))
    add_rule(world.get_location("Tribal Spear Acquired"), lambda state: weapon_is_at_least(state, player, "Enchanted Monkey Wizard Staff") and state.has("Octopus King Crown with Jaspers", player) and armor_is_at_least(state, player, "Lightweight Body Armour"))
    add_rule(world.get_location("Four Chocolate Bars in The Hole Acquired"), lambda state: weapon_is_at_least(state, player, "Enchanted Monkey Wizard Staff") and state.has("Octopus King Crown with Jaspers", player) and armor_is_at_least(state, player, "Lightweight Body Armour"))

    # The Forest rules
    add_rule(world.get_location("Forest Quest"), lambda state: weapon_is_at_least(state, player, "Enchanted Monkey Wizard Staff") and state.has("Octopus King Crown with Jaspers", player) and armor_is_at_least(state, player, "Lightweight Body Armour"))

    # Castle Entrance rules
    add_rule(world.get_location("Castle Entrance Quest"), lambda state: weapon_is_at_least(state, player, "Enchanted Monkey Wizard Staff") and state.has("Octopus King Crown with Jaspers", player) and armor_is_at_least(state, player, "Lightweight Body Armour") and state.has("Unicorn Horn", player) and state.has("Xinopherydon Claw", player))
    add_rule(world.get_location("Knight Body Armour Acquired"), lambda state: weapon_is_at_least(state, player, "Enchanted Monkey Wizard Staff") and state.has("Octopus King Crown with Jaspers", player) and armor_is_at_least(state, player, "Lightweight Body Armour") and state.has("Unicorn Horn", player) and state.has("Xinopherydon Claw", player))

    # Castle rules
    add_rule(world.get_location("The Giant Nougat Monster Quest"), lambda state: weapon_is_at_least(state, player, "Summoning Tribal Spear") and state.has("Boots of Introspection", player) and state.has("Octopus King Crown with Obsidian", player))

    # The Desert Fortress
    add_rule(world.get_location("Xinopherydon Claw Acquired"), lambda state: state.has("Enchanted Monkey Wizard Staff", player) or state.has("Octopus King Crown with Jaspers", player))
    add_rule(world.get_location("Unicorn Horn Acquired"), lambda state: state.has("The Pogo Stick", player) and state.has("Rocket Boots", player))
    add_rule(world.get_location("Giant Spoon Acquired"), lambda state: weapon_is_at_least(state, player, "Scythe") and state.has("Octopus King Crown with Obsidian", player) and state.has("The Sorceress' Cauldron", player) and state.has("Xinopherydon Claw", player))
    add_rule(world.get_location("Rocket Boots Acquired"), lambda state: can_fly(state, player) or (can_jump(state, player) and (state.has("Octopus King Crown with Obsidian", player) or state.has("Summoning Tribal Spear", player))))

    # Hell rules
    add_rule(world.get_location("Kill the Devil"), lambda state: state.has("Black Magic Grimoire", player) and state.has("Boots of Introspection", player) and state.has("Enchanted Monkey Wizard Staff", player))

    # Developer rules
    add_rule(world.get_location("Kill the Developer"), lambda state: weapon_is_at_least(state, player, "Scythe") and state.has("The Sorceress' Cauldron", player) and state.has("Xinopherydon Claw", player))

    # The Sea rules

    add_rule(world.get_location("The Sponge Acquired"),
             lambda state: sea_entrance(state, player))

    add_rule(world.get_location("The Shell Powder Acquired"),
             lambda state: sea_entrance(state, player))

    add_rule(world.get_location("The Red Fin Acquired"),
             lambda state: sea_entrance(state, player) and state.has("Red Enchanted Gloves", player) and state.has("Octopus King Crown with Jaspers",
                                                                                   player))
    add_rule(world.get_location("The Green Fin Acquired"),
             lambda state: sea_entrance(state, player) and state.has("Red Enchanted Gloves", player) and state.has("Octopus King Crown with Jaspers",
                                                                                   player))
    add_rule(world.get_location("The Purple Fin Acquired"),
             lambda state: sea_entrance(state, player) and state.has("Red Enchanted Gloves", player) and state.has("Octopus King Crown with Jaspers",
                                                                                   player))

    # X Potion
    add_rule(world.get_location("Boots of Introspection Acquired"), lambda state: state.has("The Octopus King Crown", player))

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
