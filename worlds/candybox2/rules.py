from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.candybox2.items import candy_box_2_base_id, items, CandyBox2ItemName
from worlds.generic.Rules import add_rule
from .locations import CandyBox2LocationName
from .rooms import CandyBox2Room, entrance_friendly_names

if TYPE_CHECKING:
    from . import CandyBox2World

weapons = [
    CandyBox2ItemName.NOTHING_WEAPON,
    CandyBox2ItemName.WOODEN_SWORD,
    CandyBox2ItemName.IRON_AXE,
    CandyBox2ItemName.POLISHED_SILVER_SWORD,
    CandyBox2ItemName.TROLLS_BLUDGEON,
    CandyBox2ItemName.MONKEY_WIZARD_STAFF,
    CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF,
    CandyBox2ItemName.TRIBAL_SPEAR,
    CandyBox2ItemName.SUMMONING_TRIBAL_SPEAR,
    CandyBox2ItemName.GIANT_SPOON,
    CandyBox2ItemName.SCYTHE,
    CandyBox2ItemName.GIANT_SPOON_OF_DOOM,
]

weapon_strength = [
    CandyBox2ItemName.NOTHING_WEAPON,
    CandyBox2ItemName.WOODEN_SWORD,
    CandyBox2ItemName.IRON_AXE,
    CandyBox2ItemName.TRIBAL_SPEAR,
    CandyBox2ItemName.MONKEY_WIZARD_STAFF,
    CandyBox2ItemName.POLISHED_SILVER_SWORD,
    CandyBox2ItemName.TROLLS_BLUDGEON,
    CandyBox2ItemName.SUMMONING_TRIBAL_SPEAR,
    CandyBox2ItemName.GIANT_SPOON,
    CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF,
    CandyBox2ItemName.GIANT_SPOON_OF_DOOM,
    CandyBox2ItemName.SCYTHE,
]

armors = [
    CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR,
    CandyBox2ItemName.KNIGHT_BODY_ARMOUR,
    CandyBox2ItemName.ENCHANTED_KNIGHT_BODY_ARMOUR,
]

def has_projectiles(world: "CandyBox2World", state: CollectionState, player: int):
    return state.has(CandyBox2ItemName.RED_ENCHANTED_GLOVES, player) or state.has(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS, player) or has_weapon(world, state, player, CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF)

def can_jump(state: CollectionState, player: int):
    return ((state.has(CandyBox2ItemName.ROCKET_BOOTS, player) or state.has(CandyBox2ItemName.DESERT_BIRD_FEATHER, player)) and state.has(CandyBox2ItemName.POGO_STICK, player)) or state.has(CandyBox2ItemName.PROGRESSIVE_JUMP, player, 2)

def can_fly(state: CollectionState, player: int):
    return (state.has(CandyBox2ItemName.ROCKET_BOOTS, player) and state.has(CandyBox2ItemName.POGO_STICK, player)) or state.has(CandyBox2ItemName.PROGRESSIVE_JUMP, player, 3)

def can_escape_hole(state: CollectionState, player: int):
    return can_fly(state, player) or state.has(CandyBox2ItemName.BEGINNERS_GRIMOIRE, player)

def can_brew(state: CollectionState, player: int, also_require_lollipops: bool):
    return (state.has(CandyBox2ItemName.SORCERESS_CAULDRON, player) and can_farm_candies(state, player)
            and (not also_require_lollipops or can_farm_lollipops(state, player)))

def can_heal(state: CollectionState, player: int):
    return can_brew(state, player, False) or state.has(CandyBox2ItemName.PINK_ENCHANTED_GLOVES, player)

def sea_entrance(world: "CandyBox2World", state: CollectionState, player: int):
    return (weapon_is_at_least(world, state, player, CandyBox2ItemName.SUMMONING_TRIBAL_SPEAR)
            and has_projectiles(world, state, player)
            and armor_is_at_least(state, player,CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR)
            and can_heal(state, player))

def can_beat_sharks(world: "CandyBox2World", state: CollectionState, player: int):
    return sea_entrance(world, state, player) and weapon_is_at_least(world, state, player,
                                                                     CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF)

def set_rules(world: "CandyBox2World", player: int):

    add_rule(world.get_location(CandyBox2LocationName.DISAPPOINTED_EMOTE_CHOCOLATE_BAR), lambda state: can_farm_candies(state, player))

    add_rule(world.get_location(CandyBox2LocationName.VILLAGE_FORGE_BUY_POLISHED_SILVER_SWORD),
             lambda state: can_farm_candies(state, player))
    add_rule(world.get_location(CandyBox2LocationName.VILLAGE_FORGE_BUY_LIGHTWEIGHT_BODY_ARMOUR),
             lambda state: can_farm_candies(state, player) and state.has(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, player, 3))

    # TODO: Forge locations should depend on previous forge location where applicable
    add_rule(world.get_location(CandyBox2LocationName.VILLAGE_FORGE_BUY_SCYTHE),
            lambda state: can_farm_candies(state, player) and state.has(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, player, 3)
            and can_reach_room(state, CandyBox2Room.DRAGON, player))

    # Cellar rules
    add_rule(world.get_location(CandyBox2LocationName.CELLAR_QUEST_CLEARED), lambda state: weapon_is_at_least(world, state, player,
                                                                                          CandyBox2ItemName.WOODEN_SWORD))

    # Desert rules
    add_rule(world.get_location(CandyBox2LocationName.DESERT_QUEST_CLEARED), lambda state: weapon_is_at_least(world, state, player,
                                                                                          CandyBox2ItemName.IRON_AXE))

    add_rule(world.get_location(CandyBox2LocationName.DESERT_BIRD_FEATHER_ACQUIRED),
            lambda state: weapon_is_at_least(world, state, player,CandyBox2ItemName.IRON_AXE)
            and has_projectiles(world, state, player))

    # Wishing Well rules
    add_rule(world.get_location(CandyBox2LocationName.ENCHANT_RED_ENCHANTED_GLOVES), lambda state: state.has(CandyBox2ItemName.LEATHER_GLOVES, player) and has_all_chocolates(state, player))
    add_rule(world.get_location(CandyBox2LocationName.ENCHANT_PINK_ENCHANTED_GLOVES), lambda state: state.has(CandyBox2ItemName.LEATHER_GLOVES, player) and has_all_chocolates(state, player))
    add_rule(world.get_location(CandyBox2LocationName.ENCHANT_SUMMONING_TRIBAL_SPEAR), lambda state: has_weapon(world, state, player, CandyBox2ItemName.TRIBAL_SPEAR) and has_all_chocolates(state, player))
    add_rule(world.get_location(CandyBox2LocationName.ENCHANT_ENCHANTED_MONKEY_WIZARD_STAFF), lambda state: has_weapon(world, state, player, CandyBox2ItemName.MONKEY_WIZARD_STAFF) and has_all_chocolates(state, player))
    add_rule(world.get_location(CandyBox2LocationName.ENCHANT_ENCHANTED_KNIGHT_BODY_ARMOUR), lambda state: state.has(CandyBox2ItemName.KNIGHT_BODY_ARMOUR, player) and has_all_chocolates(state, player))
    add_rule(world.get_location(CandyBox2LocationName.ENCHANT_OCTOPUS_KING_CROWN_WITH_JASPERS), lambda state: state.has(CandyBox2ItemName.OCTOPUS_KING_CROWN, player) and has_all_chocolates(state, player))
    add_rule(world.get_location(CandyBox2LocationName.ENCHANT_OCTOPUS_KING_CROWN_WITH_OBSIDIAN), lambda state: state.has(CandyBox2ItemName.OCTOPUS_KING_CROWN, player) and has_all_chocolates(state, player))
    add_rule(world.get_location(CandyBox2LocationName.ENCHANT_GIANT_SPOON_OF_DOOM), lambda state: has_weapon(world, state, player, CandyBox2ItemName.GIANT_SPOON) and has_all_chocolates(state, player))

    # Bridge rules
    add_rule(world.get_location(CandyBox2LocationName.TROLL_DEFEATED),
             lambda state: weapon_is_at_least(world, state, player,CandyBox2ItemName.POLISHED_SILVER_SWORD))
    add_rule(world.get_location(CandyBox2LocationName.THE_TROLLS_BLUDGEON_ACQUIRED),
             lambda state: weapon_is_at_least(world, state, player, CandyBox2ItemName.POLISHED_SILVER_SWORD))

    # Cave rules
    add_rule(world.get_location(CandyBox2LocationName.OCTOPUS_KING_DEFEATED), lambda state: state.has(CandyBox2ItemName.SORCERESS_CAULDRON, player) and weapon_is_at_least(
        world, state, player, CandyBox2ItemName.TROLLS_BLUDGEON) and armor_is_at_least(state, player, CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR))
    add_rule(world.get_location(CandyBox2LocationName.MONKEY_WIZARD_DEFEATED), lambda state: state.has(CandyBox2ItemName.BOOTS_OF_INTROSPECTION, player) and state.has(CandyBox2ItemName.BEGINNERS_GRIMOIRE, player) and state.has(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS, player) and weapon_is_at_least(
        world, state, player, CandyBox2ItemName.TROLLS_BLUDGEON) and armor_is_at_least(state, player, CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR))

    # The Hole rules
    add_rule(world.get_location(CandyBox2LocationName.THE_HOLE_HEART_PENDANT_ACQUIRED), lambda state: can_jump(state, player))
    add_rule(world.get_location(CandyBox2LocationName.THE_HOLE_BLACK_MAGIC_GRIMOIRE_ACQUIRED), lambda state: can_escape_hole(state, player) and state.has(CandyBox2ItemName.SPONGE, player))
    add_rule(world.get_location(CandyBox2LocationName.THE_HOLE_DESERT_FORTRESS_KEY_ACQUIRED), lambda state: can_escape_hole(state, player) and state.has(CandyBox2ItemName.SPONGE, player) and can_jump(state, player))
    add_rule(world.get_location(CandyBox2LocationName.THE_HOLE_TRIBAL_WARRIOR_DEFEATED), lambda state: can_escape_hole(state, player) and weapon_is_at_least(
        world, state, player, CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF) and state.has(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS, player) and armor_is_at_least(state, player, CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR))

    # TODO: possibly fly over?
    add_rule(world.get_location(CandyBox2LocationName.THE_HOLE_FOUR_CHOCOLATE_BARS_ACQUIRED), lambda state: can_escape_hole(state, player) and weapon_is_at_least(
        world, state, player, CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF) and state.has(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS, player) and armor_is_at_least(state, player, CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR))

    # The Forest rules
    add_rule(world.get_location(CandyBox2LocationName.FOREST_QUEST_CLEARED), lambda state: weapon_is_at_least(world, state, player,
                                                                                          CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF) and state.has(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS, player) and armor_is_at_least(state, player, CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR))

    # Castle Entrance rules
    add_rule(world.get_location(CandyBox2LocationName.CASTLE_ENTRANCE_QUEST_CLEARED), lambda state: can_fly(state, player) or (weapon_is_at_least(world, state, player,
                                                                                                   CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF) and state.has(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS, player) and armor_is_at_least(state, player, CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR)))
    add_rule(world.get_location(CandyBox2LocationName.KNIGHT_BODY_ARMOUR_ACQUIRED), lambda state: weapon_is_at_least(world, state, player,
                                                                                                 CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF) and state.has(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS, player) and armor_is_at_least(state, player, CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR))

    # Castle rules
    add_rule(world.get_location(CandyBox2LocationName.GIANT_NOUGAT_MONSTER_DEFEATED), lambda state: state.has(CandyBox2ItemName.PURPLE_FIN, player) and weapon_is_at_least(
        world, state, player, CandyBox2ItemName.SUMMONING_TRIBAL_SPEAR) and state.has(CandyBox2ItemName.BOOTS_OF_INTROSPECTION, player) and state.has(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_OBSIDIAN, player))

    # Egg Room
    add_rule(world.get_location(CandyBox2LocationName.EGG_ROOM_QUEST_CLEARED), lambda state: can_fly(state, player) or has_weapon(world, state, player, CandyBox2ItemName.NOTHING_WEAPON))

    # The Desert Fortress
    add_rule(world.get_location(CandyBox2LocationName.XINOPHERYDON_DEFEATED), lambda state: can_fly(state, player) and (has_weapon(world, state, player, CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF) or state.has(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS, player)))
    add_rule(world.get_location(CandyBox2LocationName.XINOPHERYDON_QUEST_UNICORN_HORN_ACQUIRED), lambda state: can_fly(state, player))
    add_rule(world.get_location(CandyBox2LocationName.TEAPOT_DEFEATED), lambda state: weapon_is_at_least(world, state, player,
                                                                                     CandyBox2ItemName.SCYTHE) and state.has(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_OBSIDIAN, player) and state.has(CandyBox2ItemName.SORCERESS_CAULDRON, player) and state.has(CandyBox2ItemName.XINOPHERYDON_CLAW, player))
    add_rule(world.get_location(CandyBox2LocationName.ROCKET_BOOTS_ACQUIRED), lambda state: can_fly(state, player) or (state.has(CandyBox2ItemName.BOOTS_OF_INTROSPECTION, player) and can_jump(state, player) and state.has(CandyBox2ItemName.BEGINNERS_GRIMOIRE, player) and (state.has(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_OBSIDIAN, player) or has_weapon(world, state, player, CandyBox2ItemName.SUMMONING_TRIBAL_SPEAR))))

    # Hell rules
    add_rule(world.get_location(CandyBox2LocationName.DEVIL_DEFEATED), lambda state: state.has(CandyBox2ItemName.BLACK_MAGIC_GRIMOIRE, player) and state.has(CandyBox2ItemName.UNICORN_HORN, player) and state.has(CandyBox2ItemName.BOOTS_OF_INTROSPECTION, player) and armor_is_at_least(state, player, CandyBox2ItemName.ENCHANTED_KNIGHT_BODY_ARMOUR) and state.has(CandyBox2ItemName.PINK_ENCHANTED_GLOVES, player) and has_weapon(world, state, player, CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF))

    # Developer rules
    add_rule(world.get_location(CandyBox2LocationName.THE_DEVELOPER_DEFEATED), lambda state: can_farm_candies(state, player) and state.has(CandyBox2ItemName.PURPLE_FIN, player) and state.has(CandyBox2ItemName.BEGINNERS_GRIMOIRE, player))

    # The Sea rules

    add_rule(world.get_location(CandyBox2LocationName.THE_SPONGE_ACQUIRED),
             lambda state: sea_entrance(world, state, player))

    add_rule(world.get_location(CandyBox2LocationName.THE_SHELL_POWDER_ACQUIRED),
             lambda state: sea_entrance(world, state, player))

    add_rule(world.get_location(CandyBox2LocationName.THE_RED_FIN_ACQUIRED),
             lambda state: can_beat_sharks(world, state, player)
                           and state.has(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS, player))

    add_rule(world.get_location(CandyBox2LocationName.THE_GREEN_FIN_ACQUIRED),
             lambda state: can_beat_sharks(world, state, player)
                           and state.has(CandyBox2ItemName.ADVANCED_GRIMOIRE, player)
                           and state.has(CandyBox2ItemName.PINK_ENCHANTED_GLOVES, player)
                           and state.has(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS, player))

    add_rule(world.get_location(CandyBox2LocationName.THE_PURPLE_FIN_ACQUIRED),
             lambda state: can_beat_sharks(world, state, player)
                           and state.has(CandyBox2ItemName.HEART_PENDANT, player)
                           and state.has(CandyBox2ItemName.HEART_PLUG, player)
                           and state.has(CandyBox2ItemName.ADVANCED_GRIMOIRE, player)
                           and state.has(CandyBox2ItemName.PINK_ENCHANTED_GLOVES, player)
                           and state.has(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS, player)
                           and state.has(CandyBox2ItemName.UNICORN_HORN, player))

    # Cyclops Puzzle
    add_rule(world.get_location(CandyBox2LocationName.SOLVE_CYCLOPS_PUZZLE), lambda state: can_reach_room(state, CandyBox2Room.DRAGON, player))

    # X Potion
    add_rule(world.get_location(CandyBox2LocationName.YOURSELF_DEFEATED), lambda state: state.has(CandyBox2ItemName.OCTOPUS_KING_CROWN, player))

    # Cooking
    add_rule(world.get_location(CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_1), lambda state: chocolate_count(state, player) >= 9)
    add_rule(world.get_location(CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_2), lambda state: chocolate_count(state, player) >= 10)
    add_rule(world.get_location(CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_3), lambda state: chocolate_count(state, player) >= 11)
    add_rule(world.get_location(CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_4), lambda state: chocolate_count(state, player) >= 12)
    add_rule(world.get_location(CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_5), lambda state: has_all_chocolates(state, player))

    # Sorceress items
    add_rule(world.get_location(CandyBox2LocationName.SORCERESS_HUT_BEGINNERS_GRIMOIRE), lambda state: can_grow_lollipops(state, player))
    add_rule(world.get_location(CandyBox2LocationName.SORCERESS_HUT_ADVANCED_GRIMOIRE), lambda state: can_grow_lollipops(state, player))
    add_rule(world.get_location(CandyBox2LocationName.SORCERESS_HUT_HAT), lambda state: can_farm_lollipops(state, player))
    add_rule(world.get_location(CandyBox2LocationName.SORCERESS_HUT_CAULDRON), lambda state: can_grow_lollipops(state, player))

    # Merchant items
    add_rule(world.get_location(CandyBox2LocationName.VILLAGE_SHOP_CHOCOLATE_BAR), lambda state: can_farm_candies(state, player))
    add_rule(world.get_location(CandyBox2LocationName.VILLAGE_SHOP_CANDY_MERCHANTS_HAT), lambda state: can_farm_candies(state, player))

def has_weapon(world: "CandyBox2World", state: CollectionState, player: int, weapon: CandyBox2ItemName):
    if state.has(weapon, player):
        return True

    if world.starting_weapon == -1:
        if state.has(CandyBox2ItemName.PROGRESSIVE_WEAPON, player, weapons.index(weapon)):
            return True
    else:
        for item in items:
            if items[item].code - candy_box_2_base_id == world.starting_weapon and item == weapon:
                return True

    return False

def weapon_is_at_least(world: "CandyBox2World", state: CollectionState, player: int, minimum_weapon: CandyBox2ItemName):
    for weapon in weapon_strength[weapon_strength.index(minimum_weapon):]:
        if has_weapon(world, state, player, weapon):
            return True
    return False

def armor_is_at_least(state: CollectionState, player: int, minimum_armor: CandyBox2ItemName):
    for armor in armors[armors.index(minimum_armor):]:
        if state.has(armor, player):
            return True
    return False

def chocolate_count(state: CollectionState, player: int):
    return state.count(CandyBox2ItemName.CHOCOLATE_BAR, player) + (4 * state.count(CandyBox2ItemName.FOUR_CHOCOLATE_BARS, player)) + (3 * state.count(CandyBox2ItemName.THREE_CHOCOLATE_BARS, player))

def has_all_chocolates(state: CollectionState, player: int):
    return chocolate_count(state, player) >= 13

def lollipop_count(state: CollectionState, player: int):
    return state.count(CandyBox2ItemName.THREE_LOLLIPOPS, player)*3 + state.count(CandyBox2ItemName.LOLLIPOP, player)

# Allows the player to plant enough lollipops at the farm for 1/minute
def can_grow_lollipops(state: CollectionState, player: int):
    return lollipop_count(state, player) >= 11 and can_reach_room(state, CandyBox2Room.LOLLIPOP_FARM, player) and can_reach_room(state, CandyBox2Room.LOLLIPOP_FARM, player)

def can_farm_lollipops(state: CollectionState, player: int):
    return can_grow_lollipops(state, player) and can_reach_room(state, CandyBox2Room.LOLLIPOP_FARM, player) and state.has(CandyBox2ItemName.PITCHFORK, player) and state.has(CandyBox2ItemName.SHELL_POWDER, player) and state.has(CandyBox2ItemName.GREEN_FIN, player) and can_reach_room(state, CandyBox2Room.LOLLIPOP_FARM, player)

# Ideally allows the player to stumble upon a quest they can use to farm candies
def can_farm_candies(state: CollectionState, player: int):
    return can_farm_lollipops(state, player) and can_reach_room(state, CandyBox2Room.LOLLIPOP_FARM, player) and can_reach_room(state, CandyBox2Room.LOLLIPOP_FARM, player)

def can_reach_room(state: CollectionState, room: CandyBox2Room, player: int):
    return state.can_reach_region(entrance_friendly_names[room], player)