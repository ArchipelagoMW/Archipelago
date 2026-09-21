"""
    Ensures a target level can be reached with available resources
    """
from worlds.generic.Rules import CollectionRule, add_rule
from .Names import RegionNames, ItemNames


def get_fishing_skill_rule(level, player, options) -> CollectionRule:
    if options.max_fishing_level < level:
        return lambda state: False

    if options.brutal_grinds or level < 5:
        return lambda state: state.can_reach_region(RegionNames.Shrimp, player)
    if level < 20:
        return lambda state: state.can_reach_region(RegionNames.Shrimp, player) and \
                             state.can_reach_region(RegionNames.Port_Sarim, player)
    else:
        return lambda state: state.can_reach_region(RegionNames.Shrimp, player) and \
                             state.can_reach_region(RegionNames.Port_Sarim, player) and \
                             state.can_reach_region(RegionNames.Fly_Fish, player)


def get_mining_skill_rule(level, player, options) -> CollectionRule:
    if options.max_mining_level < level:
        return lambda state: False

    if options.brutal_grinds or level < 15:
        return lambda state: state.can_reach_region(RegionNames.Bronze_Ores, player) or \
                             state.can_reach_region(RegionNames.Clay_Rock, player)
    else:
        # Iron is the best way to train all the way to 99, so having access to iron is all you need to check for
        return lambda state: (state.can_reach_region(RegionNames.Bronze_Ores, player) or
                              state.can_reach_region(RegionNames.Clay_Rock, player)) and \
                             state.can_reach_region(RegionNames.Iron_Rock, player)


def get_woodcutting_skill_rule(level, player, options) -> CollectionRule:
    if options.max_woodcutting_level < level:
        return lambda state: False

    if options.brutal_grinds or level < 15:
        # I've checked. There is not a single chunk in the f2p that does not have at least one normal tree.
        # Even the desert.
        return lambda state: True
    if level < 30:
        return lambda state: state.can_reach_region(RegionNames.Oak_Tree, player)
    else:
        return lambda state: state.can_reach_region(RegionNames.Oak_Tree, player) and \
                             state.can_reach_region(RegionNames.Willow_Tree, player)


def get_smithing_skill_rule(level, player, options) -> CollectionRule:
    if options.max_smithing_level < level:
        return lambda state: False

    if options.brutal_grinds:
        return lambda state: state.can_reach_region(RegionNames.Bronze_Ores, player) and \
                             state.can_reach_region(RegionNames.Furnace, player)
    if level < 15:
        # Lumbridge has a special bronze-only anvil. This is the only anvil of its type so it's not included
        # in the "Anvil" resource region. We still need to check for it though.
        return lambda state: state.can_reach_region(RegionNames.Bronze_Ores, player) and \
                             state.can_reach_region(RegionNames.Furnace, player) and \
                             (state.can_reach_region(RegionNames.Anvil, player) or
                              state.can_reach_region(RegionNames.Lumbridge, player))
    if level < 30:
        # For levels between 15 and 30, the lumbridge anvil won't cut it. Only a real one will do
        return lambda state: state.can_reach_region(RegionNames.Bronze_Ores, player) and \
                             state.can_reach_region(RegionNames.Iron_Rock, player) and \
                             state.can_reach_region(RegionNames.Furnace, player) and \
                             state.can_reach_region(RegionNames.Anvil, player)
    else:
        return lambda state: state.can_reach_region(RegionNames.Bronze_Ores, player) and \
                             state.can_reach_region(RegionNames.Iron_Rock, player) and \
                             state.can_reach_region(RegionNames.Coal_Rock, player) and \
                             state.can_reach_region(RegionNames.Furnace, player) and \
                             state.can_reach_region(RegionNames.Anvil, player)


def get_crafting_skill_rule(level, player, options):
    if options.max_crafting_level < level:
        return lambda state: False

    # Crafting is really complex. Need a lot of sub-rules to make this even remotely readable
    def can_spin(state):
        return state.can_reach_region(RegionNames.Sheep, player) and \
            state.can_reach_region(RegionNames.Spinning_Wheel, player)

    def can_pot(state):
        return state.can_reach_region(RegionNames.Clay_Rock, player) and \
            state.can_reach_region(RegionNames.Barbarian_Village, player)

    def can_tan(state):
        return state.can_reach_region(RegionNames.Milk, player) and \
            state.can_reach_region(RegionNames.Al_Kharid, player)

    def mould_access(state):
        return state.can_reach_region(RegionNames.Al_Kharid, player) or \
            state.can_reach_region(RegionNames.Rimmington, player)

    def can_silver(state):
        return state.can_reach_region(RegionNames.Silver_Rock, player) and \
            state.can_reach_region(RegionNames.Furnace, player) and mould_access(state)

    def can_gold(state):
        return state.can_reach_region(RegionNames.Gold_Rock, player) and \
            state.can_reach_region(RegionNames.Furnace, player) and mould_access(state)

    if options.brutal_grinds or level < 5:
        return lambda state: can_spin(state) or can_pot(state) or can_tan(state)

    can_smelt_gold = get_smithing_skill_rule(40, player, options)
    can_smelt_silver = get_smithing_skill_rule(20, player, options)
    if level < 16:
        return lambda state: can_pot(state) or can_tan(state) or (can_gold(state) and can_smelt_gold(state))
    else:
        return lambda state: can_tan(state) or (can_silver(state) and can_smelt_silver(state)) or \
                             (can_gold(state) and can_smelt_gold(state))


def get_cooking_skill_rule(level, player, options) -> CollectionRule:
    if options.max_cooking_level < level:
        return lambda state: False

    if options.brutal_grinds or level < 15:
        return lambda state: state.can_reach_region(RegionNames.Milk, player) or \
                             state.can_reach_region(RegionNames.Egg, player) or \
                             state.can_reach_region(RegionNames.Shrimp, player) or \
                             (state.can_reach_region(RegionNames.Wheat, player) and
                              state.can_reach_region(RegionNames.Windmill, player))
    else:
        can_catch_fly_fish = get_fishing_skill_rule(20, player, options)

        return lambda state: (
                                 (state.can_reach_region(RegionNames.Fly_Fish, player) and can_catch_fly_fish(state)) or
                                 (state.can_reach_region(RegionNames.Port_Sarim, player))
                             ) and (
                              state.can_reach_region(RegionNames.Milk, player) or
                              state.can_reach_region(RegionNames.Egg, player) or
                              state.can_reach_region(RegionNames.Shrimp, player) or
                              (state.can_reach_region(RegionNames.Wheat, player) and
                               state.can_reach_region(RegionNames.Windmill, player))
                             )


def get_runecraft_skill_rule(level, player, options) -> CollectionRule:
    if options.max_runecraft_level < level:
        return lambda state: False
    if not options.brutal_grinds:
        # Ensure access to the relevant altars
        if level >= 5:
            return lambda state: state.has(ItemNames.QP_Rune_Mysteries, player) and \
                                 state.can_reach_region(RegionNames.Falador_Farm, player) and \
                                 state.can_reach_region(RegionNames.Lumbridge_Swamp, player)
        if level >= 9:
            return lambda state: state.has(ItemNames.QP_Rune_Mysteries, player) and \
                                 state.can_reach_region(RegionNames.Falador_Farm, player) and \
                                 state.can_reach_region(RegionNames.Lumbridge_Swamp, player) and \
                                 state.can_reach_region(RegionNames.East_Of_Varrock, player)
        if level >= 14:
            return lambda state: state.has(ItemNames.QP_Rune_Mysteries, player) and \
                                 state.can_reach_region(RegionNames.Falador_Farm, player) and \
                                 state.can_reach_region(RegionNames.Lumbridge_Swamp, player) and \
                                 state.can_reach_region(RegionNames.East_Of_Varrock, player) and \
                                 state.can_reach_region(RegionNames.Al_Kharid, player)

    return lambda state: state.has(ItemNames.QP_Rune_Mysteries, player) and \
                         state.can_reach_region(RegionNames.Falador_Farm, player)


def get_magic_skill_rule(level, player, options) -> CollectionRule:
    if options.max_magic_level < level:
        return lambda state: False

    return lambda state: state.can_reach_region(RegionNames.Mind_Runes, player)


def get_firemaking_skill_rule(level, player, options) -> CollectionRule:
    if options.max_firemaking_level < level:
        return lambda state: False
    if not options.brutal_grinds:
        if level >= 30:
            can_chop_willows = get_woodcutting_skill_rule(30, player, options)
            return lambda state: state.can_reach_region(RegionNames.Willow_Tree, player) and can_chop_willows(state)
        if level >= 15:
            can_chop_oaks = get_woodcutting_skill_rule(15, player, options)
            return lambda state: state.can_reach_region(RegionNames.Oak_Tree, player) and can_chop_oaks(state)
    # If brutal grinds are on, or if the level is less than 15, you can train it.
    return lambda state: True


def get_skill_rule(skill, level, player, options) -> CollectionRule:
    if level <= 1:
        return lambda state: True
    if skill.lower() == "fishing":
        return get_fishing_skill_rule(level, player, options)
    if skill.lower() == "mining":
        return get_mining_skill_rule(level, player, options)
    if skill.lower() == "woodcutting":
        return get_woodcutting_skill_rule(level, player, options)
    if skill.lower() == "smithing":
        return get_smithing_skill_rule(level, player, options)
    if skill.lower() == "crafting":
        return get_crafting_skill_rule(level, player, options)
    if skill.lower() == "cooking":
        return get_cooking_skill_rule(level, player, options)
    if skill.lower() == "runecraft":
        return get_runecraft_skill_rule(level, player, options)
    if skill.lower() == "magic":
        return get_magic_skill_rule(level, player, options)
    if skill.lower() == "firemaking":
        return get_firemaking_skill_rule(level, player, options)

    return lambda state: True


def generate_special_rules_for(entrance, region_row, outbound_region_name, player, options, world):
    if outbound_region_name == RegionNames.Cooks_Guild:
        add_rule(entrance, get_cooking_skill_rule(32, player, options))
        # Since there's goblins in this chunk, checking for hat access is superfluous, you'd always have it anyway
    elif outbound_region_name == RegionNames.Crafting_Guild:
        add_rule(entrance, get_crafting_skill_rule(40, player, options))
        # Literally the only brown apron access in the entirety of f2p is buying it in varrock
        add_rule(entrance, lambda state: state.can_reach_region(RegionNames.Central_Varrock, player))
    elif outbound_region_name == RegionNames.Corsair_Cove:
        # Need to be able to start Corsair Curse in addition to having the item
        add_rule(entrance, lambda state: state.can_reach(RegionNames.Falador_Farm, "Region", player))
    elif outbound_region_name == "Camdozaal*":
        add_rule(entrance, lambda state: state.has(ItemNames.QP_Below_Ice_Mountain, player))
    elif region_row.name == "Dwarven Mountain Pass" and outbound_region_name == "Anvil*":
        add_rule(entrance, lambda state: state.has(ItemNames.QP_Dorics_Quest, player))
    elif outbound_region_name == RegionNames.Crandor:
        add_rule(entrance, lambda state: state.can_reach_region(RegionNames.South_Of_Varrock, player))
        add_rule(entrance, lambda state: state.can_reach_region(RegionNames.Edgeville, player))
        add_rule(entrance, lambda state: state.can_reach_region(RegionNames.Lumbridge, player))
        add_rule(entrance, lambda state: state.can_reach_region(RegionNames.Rimmington, player))
        add_rule(entrance, lambda state: state.can_reach_region(RegionNames.Monastery, player))
        add_rule(entrance, lambda state: state.can_reach_region(RegionNames.Dwarven_Mines, player))
        add_rule(entrance, lambda state: state.can_reach_region(RegionNames.Port_Sarim, player))
        add_rule(entrance, lambda state: state.can_reach_region(RegionNames.Draynor_Village, player))
        add_rule(entrance, lambda state: world.quest_points(state) >= 32)


    # Special logic for canoes
    canoe_regions = [RegionNames.Lumbridge, RegionNames.South_Of_Varrock, RegionNames.Barbarian_Village,
                     RegionNames.Edgeville, RegionNames.Wilderness]
    if region_row.name in canoe_regions:
        # Skill rules for greater distances
        woodcutting_rule_d1 = get_woodcutting_skill_rule(12, player, options)
        woodcutting_rule_d2 = get_woodcutting_skill_rule(27, player, options)
        woodcutting_rule_d3 = get_woodcutting_skill_rule(42, player, options)
        woodcutting_rule_all = get_woodcutting_skill_rule(57, player, options)

        if region_row.name == RegionNames.Lumbridge:
            # Canoe Tree access for the Location
            if outbound_region_name == RegionNames.Canoe_Tree:
                add_rule(entrance,
                    lambda state: (state.can_reach_region(RegionNames.South_Of_Varrock, player)
                                   and woodcutting_rule_d1(state)) or
                                  (state.can_reach_region(RegionNames.Barbarian_Village, player)
                                   and woodcutting_rule_d2(state)) or
                                  (state.can_reach_region(RegionNames.Edgeville, player)
                                   and woodcutting_rule_d3(state)) or
                                  (state.can_reach_region(RegionNames.Wilderness, player)
                                   and woodcutting_rule_all(state)))

            # Access to other chunks based on woodcutting settings
            elif outbound_region_name == RegionNames.South_Of_Varrock:
                add_rule(entrance, woodcutting_rule_d1)
            elif outbound_region_name == RegionNames.Barbarian_Village:
                add_rule(entrance, woodcutting_rule_d2)
            elif outbound_region_name == RegionNames.Edgeville:
                add_rule(entrance, woodcutting_rule_d3)
            elif outbound_region_name == RegionNames.Wilderness:
                add_rule(entrance, woodcutting_rule_all)

        elif region_row.name == RegionNames.South_Of_Varrock:
            if outbound_region_name == RegionNames.Canoe_Tree:
                add_rule(entrance,
                    lambda state: (state.can_reach_region(RegionNames.Lumbridge, player)
                                   and woodcutting_rule_d1(state)) or
                                  (state.can_reach_region(RegionNames.Barbarian_Village, player)
                                   and woodcutting_rule_d1(state)) or
                                  (state.can_reach_region(RegionNames.Edgeville, player)
                                   and woodcutting_rule_d2(state)) or
                                  (state.can_reach_region(RegionNames.Wilderness, player)
                                   and woodcutting_rule_d3(state)))

            # Access to other chunks based on woodcutting settings
            elif outbound_region_name == RegionNames.Lumbridge:
                add_rule(entrance, woodcutting_rule_d1)
            elif outbound_region_name == RegionNames.Barbarian_Village:
                add_rule(entrance, woodcutting_rule_d1)
            elif outbound_region_name == RegionNames.Edgeville:
                add_rule(entrance, woodcutting_rule_d3)
            elif outbound_region_name == RegionNames.Wilderness:
                add_rule(entrance, woodcutting_rule_all)
        elif region_row.name == RegionNames.Barbarian_Village:
            if outbound_region_name == RegionNames.Canoe_Tree:
                add_rule(entrance,
                    lambda state: (state.can_reach_region(RegionNames.Lumbridge, player)
                                   and woodcutting_rule_d2(state)) or (state.can_reach_region(RegionNames.South_Of_Varrock, player)
                                   and woodcutting_rule_d1(state)) or (state.can_reach_region(RegionNames.Edgeville, player)
                                   and woodcutting_rule_d1(state)) or (state.can_reach_region(RegionNames.Wilderness, player)
                                   and woodcutting_rule_d2(state)))

            # Access to other chunks based on woodcutting settings
            elif outbound_region_name == RegionNames.Lumbridge:
                add_rule(entrance, woodcutting_rule_d2)
            elif outbound_region_name == RegionNames.South_Of_Varrock:
                add_rule(entrance, woodcutting_rule_d1)
            # Edgeville does not need to be checked, because it's already adjacent
            elif outbound_region_name == RegionNames.Wilderness:
                add_rule(entrance, woodcutting_rule_d3)
        elif region_row.name == RegionNames.Edgeville:
            if outbound_region_name == RegionNames.Canoe_Tree:
                add_rule(entrance,
                    lambda state: (state.can_reach_region(RegionNames.Lumbridge, player)
                                   and woodcutting_rule_d3(state)) or
                                  (state.can_reach_region(RegionNames.South_Of_Varrock, player)
                                   and woodcutting_rule_d2(state)) or
                                  (state.can_reach_region(RegionNames.Barbarian_Village, player)
                                   and woodcutting_rule_d1(state)) or
                                  (state.can_reach_region(RegionNames.Wilderness, player)
                                   and woodcutting_rule_d1(state)))

            # Access to other chunks based on woodcutting settings
            elif outbound_region_name == RegionNames.Lumbridge:
                add_rule(entrance, woodcutting_rule_d3)
            elif outbound_region_name == RegionNames.South_Of_Varrock:
                add_rule(entrance, woodcutting_rule_d2)
            # Barbarian Village does not need to be checked, because it's already adjacent
            # Wilderness does not need to be checked, because it's already adjacent
        elif region_row.name == RegionNames.Wilderness:
            if outbound_region_name == RegionNames.Canoe_Tree:
                add_rule(entrance,
                    lambda state: (state.can_reach_region(RegionNames.Lumbridge, player)
                                   and woodcutting_rule_all(state)) or
                                  (state.can_reach_region(RegionNames.South_Of_Varrock, player)
                                   and woodcutting_rule_d3(state)) or
                                  (state.can_reach_region(RegionNames.Barbarian_Village, player)
                                   and woodcutting_rule_d2(state)) or
                                  (state.can_reach_region(RegionNames.Edgeville, player)
                                   and woodcutting_rule_d1(state)))

            # Access to other chunks based on woodcutting settings
            elif outbound_region_name == RegionNames.Lumbridge:
                add_rule(entrance, woodcutting_rule_all)
            elif outbound_region_name == RegionNames.South_Of_Varrock:
                add_rule(entrance, woodcutting_rule_d3)
            elif outbound_region_name == RegionNames.Barbarian_Village:
                add_rule(entrance, woodcutting_rule_d2)
            # Edgeville does not need to be checked, because it's already adjacent
