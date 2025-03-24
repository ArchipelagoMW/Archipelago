from BaseClasses import CollectionState
from worlds.AutoWorld import World
from worlds.candybox2 import CandyBox2Options
from worlds.generic.Rules import set_rule, add_rule

weapons = [
    "Wooden Sword",
    "Iron Axe",
    "Monkey Wizard Staff",
    "Polished Silver Sword",
    "Troll's Bludgeon",
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
    return (state.has("Rocket Boots", player) or state.has("Desert bird feather", player)) and state.has("Pogo Stick", player)

def can_fly(state: CollectionState, player: int):
    return state.has("Rocket Boots", player) and state.has("Pogo Stick", player)

def can_escape_hole(state: CollectionState, player: int):
    return can_fly(state, player) or state.has("Beginners' Grimoire", player)

def sea_entrance(state: CollectionState, player: int):
    return weapon_is_at_least(state, player, "Enchanted Monkey Wizard Staff") and armor_is_at_least(state, player,
                                                                                             "Lightweight Body Armour")

def set_rules(world: World, player: int):

    add_rule(world.get_location("Disappointed Emote Chocolate Bar"), lambda state: can_farm_candies(state, player))

    # Cellar rules
    add_rule(world.get_location("Cellar Quest Cleared"), lambda state: weapon_is_at_least(state, player, "Wooden Sword"))

    # Desert rules
    add_rule(world.get_location("Desert Quest Cleared"), lambda state: weapon_is_at_least(state, player, "Iron Axe"))
    add_rule(world.get_location("Desert Bird Feather Acquired"), lambda state: weapon_is_at_least(state, player, "Iron Axe") and has_projectiles(state, player))

    # Bridge rules
    add_rule(world.get_location("Troll Defeated"), lambda state: weapon_is_at_least(state, player, "Polished Silver Sword"))
    add_rule(world.get_location("The Troll's Bludgeon Acquired"),
            lambda state: weapon_is_at_least(state, player, "Polished Silver Sword"))

    # Cave rules
    add_rule(world.get_location("Octopus King Defeated"), lambda state: state.has("Sorceress' Cauldron", player) and weapon_is_at_least(state, player, "Troll's Bludgeon") and armor_is_at_least(state, player, "Lightweight Body Armour"))
    add_rule(world.get_location("Monkey Wizard Defeated"), lambda state: state.has("Boots of Introspection", player) and state.has("Beginners' Grimoire", player) and state.has("Octopus King Crown with Jaspers", player) and weapon_is_at_least(state, player, "Troll's Bludgeon") and armor_is_at_least(state, player, "Lightweight Body Armour"))

    # The Hole rules
    add_rule(world.get_location("The Hole Heart Pendant Acquired"), lambda state: can_jump(state, player))
    add_rule(world.get_location("The Hole Black Magic Grimoire Acquired"), lambda state: can_escape_hole(state, player) and state.has("Sponge", player))
    add_rule(world.get_location("The Hole Desert Fortress Key Acquired"), lambda state: can_escape_hole(state, player) and state.has("Sponge", player) and can_jump(state, player))
    add_rule(world.get_location("The Hole Tribal Warrior Defeated"), lambda state: can_escape_hole(state, player) and weapon_is_at_least(state, player, "Enchanted Monkey Wizard Staff") and state.has("Octopus King Crown with Jaspers", player) and armor_is_at_least(state, player, "Lightweight Body Armour"))
    add_rule(world.get_location("The Hole Four Chocolate Bars in The Hole Acquired"), lambda state: can_escape_hole(state, player) and weapon_is_at_least(state, player, "Enchanted Monkey Wizard Staff") and state.has("Octopus King Crown with Jaspers", player) and armor_is_at_least(state, player, "Lightweight Body Armour"))

    # The Forest rules
    add_rule(world.get_location("Forest Quest Cleared"), lambda state: weapon_is_at_least(state, player, "Enchanted Monkey Wizard Staff") and state.has("Octopus King Crown with Jaspers", player) and armor_is_at_least(state, player, "Lightweight Body Armour"))

    # Castle Entrance rules
    add_rule(world.get_location("Castle Entrance Quest Cleared"), lambda state: weapon_is_at_least(state, player, "Enchanted Monkey Wizard Staff") and state.has("Octopus King Crown with Jaspers", player) and armor_is_at_least(state, player, "Lightweight Body Armour") and state.has("Unicorn Horn", player) and state.has("Xinopherydon Claw", player))
    add_rule(world.get_location("Knight Body Armour Acquired"), lambda state: weapon_is_at_least(state, player, "Enchanted Monkey Wizard Staff") and state.has("Octopus King Crown with Jaspers", player) and armor_is_at_least(state, player, "Lightweight Body Armour") and state.has("Unicorn Horn", player) and state.has("Xinopherydon Claw", player))

    # Castle rules
    add_rule(world.get_location("The Giant Nougat Monster Defeated"), lambda state: weapon_is_at_least(state, player, "Summoning Tribal Spear") and state.has("Boots of Introspection", player) and state.has("Octopus King Crown with Obsidian", player))

    # The Desert Fortress
    add_rule(world.get_location("Xinopherydon Defeated"), lambda state: can_fly(state, player) and (state.has("Enchanted Monkey Wizard Staff", player) or state.has("Octopus King Crown with Jaspers", player)))
    add_rule(world.get_location("Xinopherydon Quest Unicorn Horn Acquired"), lambda state: can_fly(state, player))
    add_rule(world.get_location("Teapot Defeated"), lambda state: weapon_is_at_least(state, player, "Scythe") and state.has("Octopus King Crown with Obsidian", player) and state.has("Sorceress' Cauldron", player) and state.has("Xinopherydon Claw", player))
    add_rule(world.get_location("Rocket Boots Acquired"), lambda state: can_fly(state, player) or (state.has("Boots of Introspection", player) and can_jump(state, player) and (state.has("Octopus King Crown with Obsidian", player) or state.has("Summoning Tribal Spear", player))))

    # Hell rules
    add_rule(world.get_location("Devil Defeated"), lambda state: state.has("Black Magic Grimoire", player) and state.has("Boots of Introspection", player) and state.has("Enchanted Monkey Wizard Staff", player))

    # Developer rules
    add_rule(world.get_location("The Developer Defeated"), lambda state: weapon_is_at_least(state, player, "Scythe") and state.has("Sorceress' Cauldron", player) and state.has("Xinopherydon Claw", player))

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
    add_rule(world.get_location("Yourself Defeated"), lambda state: state.has("Octopus King Crown", player))

    # Sorceress items
    add_rule(world.get_location("Sorceress' Hut Beginner's Grimoire"), lambda state: can_grow_lollipops(state, player))
    add_rule(world.get_location("Sorceress' Hut Advanced Grimoire"), lambda state: can_grow_lollipops(state, player))
    add_rule(world.get_location("Sorceress' Hut Hat"), lambda state: can_farm_lollipops(state, player))
    add_rule(world.get_location("Sorceress' Hut Cauldron"), lambda state: can_grow_lollipops(state, player))

    # Merchant items
    add_rule(world.get_location("Village Shop Chocolate Bar"), lambda state: can_farm_candies(state, player))
    add_rule(world.get_location("Village Shop Candy Merchant's Hat"), lambda state: can_farm_candies(state, player))

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

def chocolate_count(state: CollectionState, player: int):
    return state.count("Chocolate Bar", player) + (4 * state.count("4 Chocolate Bars", player)) + (3 * state.count("3 Chocolate Bars", player))

def lollipop_count(state: CollectionState, player: int):
    return state.count("3 Lollipops", player)*3 + state.count("Lollipop", player)

# Allows the player to plant enough lollipops at the farm for 1/minute
def can_grow_lollipops(state: CollectionState, player: int):
    return lollipop_count(state, player) >= 11

def can_farm_lollipops(state: CollectionState, player: int):
    return can_grow_lollipops(state, player) and state.has("Pitchfork", player) and state.has("Shell Powder", player) and state.has("Green Fin", player)

# Ideally allows the player to stumble upon a quest they can use to farm candies
def can_farm_candies(state: CollectionState, player: int):
    return can_farm_lollipops(state, player)
