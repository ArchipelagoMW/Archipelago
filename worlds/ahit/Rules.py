from worlds.AutoWorld import CollectionState
from worlds.generic.Rules import add_rule, set_rule
from .Locations import location_table, zipline_unlocks, is_location_valid, shop_locations, event_locs
from .Types import HatType, ChapterIndex, hat_type_to_item, Difficulty, HitType
from BaseClasses import Location, Entrance, Region
from typing import TYPE_CHECKING, List, Callable, Union, Dict
from .Options import EndGoal, CTRLogic, NoTicketSkips

if TYPE_CHECKING:
    from . import HatInTimeWorld
    

act_connections = {
    "Mafia Town - Act 2": ["Mafia Town - Act 1"],
    "Mafia Town - Act 3": ["Mafia Town - Act 1"],
    "Mafia Town - Act 4": ["Mafia Town - Act 2", "Mafia Town - Act 3"],
    "Mafia Town - Act 6": ["Mafia Town - Act 4"],
    "Mafia Town - Act 7": ["Mafia Town - Act 4"],
    "Mafia Town - Act 5": ["Mafia Town - Act 6", "Mafia Town - Act 7"],

    "Battle of the Birds - Act 2": ["Battle of the Birds - Act 1"],
    "Battle of the Birds - Act 3": ["Battle of the Birds - Act 1"],
    "Battle of the Birds - Act 4": ["Battle of the Birds - Act 2", "Battle of the Birds - Act 3"],
    "Battle of the Birds - Act 5": ["Battle of the Birds - Act 2", "Battle of the Birds - Act 3"],
    "Battle of the Birds - Finale A": ["Battle of the Birds - Act 4", "Battle of the Birds - Act 5"],
    "Battle of the Birds - Finale B": ["Battle of the Birds - Finale A"],

    "Subcon Forest - Finale": ["Subcon Forest - Act 1", "Subcon Forest - Act 2",
                               "Subcon Forest - Act 3", "Subcon Forest - Act 4",
                               "Subcon Forest - Act 5"],

    "The Arctic Cruise - Act 2":  ["The Arctic Cruise - Act 1"],
    "The Arctic Cruise - Finale": ["The Arctic Cruise - Act 2"],
}


def can_use_hat(state: CollectionState, world: "HatInTimeWorld", hat: HatType) -> bool:
    if world.options.HatItems:
        return state.has(hat_type_to_item[hat], world.player)

    if world.hat_yarn_costs[hat] <= 0:  # this means the hat was put into starting inventory
        return True

    return state.has("Yarn", world.player, get_hat_cost(world, hat))


def get_hat_cost(world: "HatInTimeWorld", hat: HatType) -> int:
    cost = 0
    for h in world.hat_craft_order:
        cost += world.hat_yarn_costs[h]
        if h == hat:
            break

    return cost


def painting_logic(world: "HatInTimeWorld") -> bool:
    return bool(world.options.ShuffleSubconPaintings)


# -1 = Normal, 0 = Moderate, 1 = Hard, 2 = Expert
def get_difficulty(world: "HatInTimeWorld") -> Difficulty:
    return Difficulty(world.options.LogicDifficulty)


def has_paintings(state: CollectionState, world: "HatInTimeWorld", count: int, allow_skip: bool = True) -> bool:
    if not painting_logic(world):
        return True

    if not world.options.NoPaintingSkips and allow_skip:
        # In Moderate there is a very easy trick to skip all the walls, except for the one guarding the boss arena
        if get_difficulty(world) >= Difficulty.MODERATE:
            return True

    return state.has("Progressive Painting Unlock", world.player, count)


def zipline_logic(world: "HatInTimeWorld") -> bool:
    return bool(world.options.ShuffleAlpineZiplines)


def can_use_hookshot(state: CollectionState, world: "HatInTimeWorld"):
    return state.has("Hookshot Badge", world.player)


def can_hit(state: CollectionState, world: "HatInTimeWorld", umbrella_only: bool = False):
    if not world.options.UmbrellaLogic:
        return True

    return state.has("Umbrella", world.player) or not umbrella_only and can_use_hat(state, world, HatType.BREWING)


def has_relic_combo(state: CollectionState, world: "HatInTimeWorld", relic: str) -> bool:
    return state.has_group(relic, world.player, len(world.item_name_groups[relic]))


def get_relic_count(state: CollectionState, world: "HatInTimeWorld", relic: str) -> int:
    return state.count_group(relic, world.player)


# This is used to determine if the player can clear an act that's required to unlock a Time Rift
def can_clear_required_act(state: CollectionState, world: "HatInTimeWorld", act_entrance: str) -> bool:
    entrance: Entrance = world.multiworld.get_entrance(act_entrance, world.player)
    if not state.can_reach(entrance.connected_region, "Region", world.player):
        return False

    if "Free Roam" in entrance.connected_region.name:
        return True

    name: str = f"Act Completion ({entrance.connected_region.name})"
    return world.multiworld.get_location(name, world.player).access_rule(state)


def can_clear_alpine(state: CollectionState, world: "HatInTimeWorld") -> bool:
    return state.has("Birdhouse Cleared", world.player) and state.has("Lava Cake Cleared", world.player) \
            and state.has("Windmill Cleared", world.player) and state.has("Twilight Bell Cleared", world.player)


def can_clear_metro(state: CollectionState, world: "HatInTimeWorld") -> bool:
    return state.has("Nyakuza Intro Cleared", world.player) \
           and state.has("Yellow Overpass Station Cleared", world.player) \
           and state.has("Yellow Overpass Manhole Cleared", world.player) \
           and state.has("Green Clean Station Cleared", world.player) \
           and state.has("Green Clean Manhole Cleared", world.player) \
           and state.has("Bluefin Tunnel Cleared", world.player) \
           and state.has("Pink Paw Station Cleared", world.player) \
           and state.has("Pink Paw Manhole Cleared", world.player)


def set_rules(world: "HatInTimeWorld"):
    # First, chapter access
    starting_chapter = ChapterIndex(world.options.StartingChapter)
    world.chapter_timepiece_costs[starting_chapter] = 0

    # Chapter costs increase progressively. Randomly decide the chapter order, except for Finale
    chapter_list: List[ChapterIndex] = [ChapterIndex.MAFIA, ChapterIndex.BIRDS,
                                        ChapterIndex.SUBCON, ChapterIndex.ALPINE]

    final_chapter = ChapterIndex.FINALE
    if world.options.EndGoal == EndGoal.option_rush_hour:
        final_chapter = ChapterIndex.METRO
        chapter_list.append(ChapterIndex.FINALE)
    elif world.options.EndGoal == EndGoal.option_seal_the_deal:
        final_chapter = None
        chapter_list.append(ChapterIndex.FINALE)

    if world.is_dlc1():
        chapter_list.append(ChapterIndex.CRUISE)

    if world.is_dlc2() and final_chapter != ChapterIndex.METRO:
        chapter_list.append(ChapterIndex.METRO)

    chapter_list.remove(starting_chapter)
    world.random.shuffle(chapter_list)

    # Make sure Alpine is unlocked before any DLC chapters are, as the Alpine door needs to be open to access them
    if starting_chapter != ChapterIndex.ALPINE and (world.is_dlc1() or world.is_dlc2()):
        index1 = 69
        index2 = 69
        pos: int
        lowest_index: int
        chapter_list.remove(ChapterIndex.ALPINE)

        if world.is_dlc1():
            index1 = chapter_list.index(ChapterIndex.CRUISE)

        if world.is_dlc2() and final_chapter != ChapterIndex.METRO:
            index2 = chapter_list.index(ChapterIndex.METRO)

        lowest_index = min(index1, index2)
        if lowest_index == 0:
            pos = 0
        else:
            pos = world.random.randint(0, lowest_index)

        chapter_list.insert(pos, ChapterIndex.ALPINE)

    lowest_cost: int = world.options.LowestChapterCost.value
    highest_cost: int = world.options.HighestChapterCost.value
    cost_increment: int = world.options.ChapterCostIncrement.value
    min_difference: int = world.options.ChapterCostMinDifference.value
    last_cost = 0

    for i, chapter in enumerate(chapter_list):
        min_range: int = lowest_cost + (cost_increment * i)
        if min_range >= highest_cost:
            min_range = highest_cost-1

        value: int = world.random.randint(min_range, min(highest_cost, max(lowest_cost, last_cost + cost_increment)))
        cost = world.random.randint(value, min(value + cost_increment, highest_cost))
        if i >= 1:
            if last_cost + min_difference > cost:
                cost = last_cost + min_difference

        cost = min(cost, highest_cost)
        world.chapter_timepiece_costs[chapter] = cost
        last_cost = cost

    if final_chapter is not None:
        final_chapter_cost: int
        if world.options.FinalChapterMinCost == world.options.FinalChapterMaxCost:
            final_chapter_cost = world.options.FinalChapterMaxCost.value
        else:
            final_chapter_cost = world.random.randint(world.options.FinalChapterMinCost.value,
                                                      world.options.FinalChapterMaxCost.value)

        world.chapter_timepiece_costs[final_chapter] = final_chapter_cost

    add_rule(world.multiworld.get_entrance("Telescope -> Mafia Town", world.player),
             lambda state: state.has("Time Piece", world.player, world.chapter_timepiece_costs[ChapterIndex.MAFIA]))

    add_rule(world.multiworld.get_entrance("Telescope -> Battle of the Birds", world.player),
             lambda state: state.has("Time Piece", world.player, world.chapter_timepiece_costs[ChapterIndex.BIRDS]))

    add_rule(world.multiworld.get_entrance("Telescope -> Subcon Forest", world.player),
             lambda state: state.has("Time Piece", world.player, world.chapter_timepiece_costs[ChapterIndex.SUBCON]))

    add_rule(world.multiworld.get_entrance("Telescope -> Alpine Skyline", world.player),
             lambda state: state.has("Time Piece", world.player, world.chapter_timepiece_costs[ChapterIndex.ALPINE]))

    add_rule(world.multiworld.get_entrance("Telescope -> Time's End", world.player),
             lambda state: state.has("Time Piece", world.player, world.chapter_timepiece_costs[ChapterIndex.FINALE])
             and can_use_hat(state, world, HatType.BREWING) and can_use_hat(state, world, HatType.DWELLER))

    if world.is_dlc1():
        add_rule(world.multiworld.get_entrance("Telescope -> Arctic Cruise", world.player),
                 lambda state: state.has("Time Piece", world.player, world.chapter_timepiece_costs[ChapterIndex.ALPINE])
                 and state.has("Time Piece", world.player, world.chapter_timepiece_costs[ChapterIndex.CRUISE]))

    if world.is_dlc2():
        add_rule(world.multiworld.get_entrance("Telescope -> Nyakuza Metro", world.player),
                 lambda state: state.has("Time Piece", world.player, world.chapter_timepiece_costs[ChapterIndex.ALPINE])
                 and state.has("Time Piece", world.player, world.chapter_timepiece_costs[ChapterIndex.METRO])
                 and can_use_hat(state, world, HatType.DWELLER) and can_use_hat(state, world, HatType.ICE))

    if not world.options.ActRandomizer:
        set_default_rift_rules(world)

    table = {**location_table, **event_locs}
    for (key, data) in table.items():
        if not is_location_valid(world, key):
            continue

        loc = world.multiworld.get_location(key, world.player)

        for hat in data.required_hats:
            add_rule(loc, lambda state, h=hat: can_use_hat(state, world, h))

        if data.hookshot:
            add_rule(loc, lambda state: can_use_hookshot(state, world))

        if data.paintings > 0 and world.options.ShuffleSubconPaintings:
            add_rule(loc, lambda state, paintings=data.paintings: has_paintings(state, world, paintings))

        if data.hit_type != HitType.none and world.options.UmbrellaLogic:
            if data.hit_type == HitType.umbrella:
                add_rule(loc, lambda state: state.has("Umbrella", world.player))

            elif data.hit_type == HitType.umbrella_or_brewing:
                add_rule(loc, lambda state: state.has("Umbrella", world.player)
                         or can_use_hat(state, world, HatType.BREWING))

            elif data.hit_type == HitType.dweller_bell:
                add_rule(loc, lambda state: state.has("Umbrella", world.player)
                         or can_use_hat(state, world, HatType.BREWING)
                         or can_use_hat(state, world, HatType.DWELLER))

        for misc in data.misc_required:
            add_rule(loc, lambda state, item=misc: state.has(item, world.player))

    set_specific_rules(world)

    # Putting all of this here, so it doesn't get overridden by anything
    # Illness starts the player past the intro
    alpine_entrance = world.multiworld.get_entrance("AFR -> Alpine Skyline Area", world.player)
    add_rule(alpine_entrance, lambda state: can_use_hookshot(state, world))
    if world.options.UmbrellaLogic:
        add_rule(alpine_entrance, lambda state: state.has("Umbrella", world.player))

    if zipline_logic(world):
        add_rule(world.multiworld.get_entrance("-> The Birdhouse", world.player),
                 lambda state: state.has("Zipline Unlock - The Birdhouse Path", world.player))

        add_rule(world.multiworld.get_entrance("-> The Lava Cake", world.player),
                 lambda state: state.has("Zipline Unlock - The Lava Cake Path", world.player))

        add_rule(world.multiworld.get_entrance("-> The Windmill", world.player),
                 lambda state: state.has("Zipline Unlock - The Windmill Path", world.player))

        add_rule(world.multiworld.get_entrance("-> The Twilight Bell", world.player),
                 lambda state: state.has("Zipline Unlock - The Twilight Bell Path", world.player))

        add_rule(world.multiworld.get_location("Act Completion (The Illness has Spread)", world.player),
                 lambda state: state.has("Zipline Unlock - The Birdhouse Path", world.player)
                 and state.has("Zipline Unlock - The Lava Cake Path", world.player)
                 and state.has("Zipline Unlock - The Windmill Path", world.player))

    if zipline_logic(world):
        for (loc, zipline) in zipline_unlocks.items():
            add_rule(world.multiworld.get_location(loc, world.player),
                     lambda state, z=zipline: state.has(z, world.player))

    dummy_entrances: List[Entrance] = []
      
    for (key, acts) in act_connections.items():
        if "Arctic Cruise" in key and not world.is_dlc1():
            continue

        entrance: Entrance = world.multiworld.get_entrance(key, world.player)
        region: Region = entrance.connected_region
        access_rules: List[Callable[[CollectionState], bool]] = []
        dummy_entrances.append(entrance)

        # Entrances to this act that we have to set access_rules on
        entrances: List[Entrance] = []

        for i, act in enumerate(acts, start=1):
            act_entrance: Entrance = world.multiworld.get_entrance(act, world.player)
            access_rules.append(act_entrance.access_rule)
            required_region = act_entrance.connected_region
            name: str = f"{key}: Connection {i}"
            new_entrance: Entrance = required_region.connect(region, name)
            entrances.append(new_entrance)

            # Copy access rules from act completions
            if "Free Roam" not in required_region.name:
                rule: Callable[[CollectionState], bool]
                name = f"Act Completion ({required_region.name})"
                rule = world.multiworld.get_location(name, world.player).access_rule
                access_rules.append(rule)

        for e in entrances:
            for rules in access_rules:
                add_rule(e, rules)

    for e in dummy_entrances:
        set_rule(e, lambda state: False)

    set_event_rules(world)

    if world.options.EndGoal == EndGoal.option_finale:
        world.multiworld.completion_condition[world.player] = lambda state: state.has("Time Piece Cluster", world.player)
    elif world.options.EndGoal == EndGoal.option_rush_hour:
        world.multiworld.completion_condition[world.player] = lambda state: state.has("Rush Hour Cleared", world.player)


def set_specific_rules(world: "HatInTimeWorld"):
    add_rule(world.multiworld.get_location("Mafia Boss Shop Item", world.player),
             lambda state: state.has("Time Piece", world.player, 12)
             and state.has("Time Piece", world.player, world.chapter_timepiece_costs[ChapterIndex.BIRDS]))

    set_mafia_town_rules(world)
    set_botb_rules(world)
    set_subcon_rules(world)
    set_alps_rules(world)

    if world.is_dlc1():
        set_dlc1_rules(world)

    if world.is_dlc2():
        set_dlc2_rules(world)

    difficulty: Difficulty = get_difficulty(world)

    if difficulty >= Difficulty.MODERATE:
        set_moderate_rules(world)

    if difficulty >= Difficulty.HARD:
        set_hard_rules(world)

    if difficulty >= Difficulty.EXPERT:
        set_expert_rules(world)


def set_moderate_rules(world: "HatInTimeWorld"):
    # Moderate: Gallery without Brewing Hat
    set_rule(world.multiworld.get_location("Act Completion (Time Rift - Gallery)", world.player), lambda state: True)

    # Moderate: Above Boats via Ice Hat Sliding
    add_rule(world.multiworld.get_location("Mafia Town - Above Boats", world.player),
             lambda state: can_use_hat(state, world, HatType.ICE), "or")

    # Moderate: Clock Tower Chest + Ruined Tower with nothing
    set_rule(world.multiworld.get_location("Mafia Town - Clock Tower Chest", world.player), lambda state: True)
    set_rule(world.multiworld.get_location("Mafia Town - Top of Ruined Tower", world.player), lambda state: True)

    # Moderate: enter and clear The Subcon Well without Hookshot and without hitting the bell
    for loc in world.multiworld.get_region("The Subcon Well", world.player).locations:
        set_rule(loc, lambda state: has_paintings(state, world, 1))

    # Moderate: Vanessa Manor with nothing
    for loc in world.multiworld.get_region("Queen Vanessa's Manor", world.player).locations:
        set_rule(loc, lambda state: has_paintings(state, world, 1))

    set_rule(world.multiworld.get_location("Subcon Forest - Manor Rooftop", world.player),
             lambda state: has_paintings(state, world, 1))

    # Moderate: Village Time Rift with nothing IF umbrella logic is off
    if not world.options.UmbrellaLogic:
        set_rule(world.multiworld.get_location("Act Completion (Time Rift - Village)", world.player), lambda state: True)

    # Moderate: get to Birdhouse/Yellow Band Hills without Brewing Hat
    set_rule(world.multiworld.get_entrance("-> The Birdhouse", world.player),
             lambda state: can_use_hookshot(state, world))
    set_rule(world.multiworld.get_location("Alpine Skyline - Yellow Band Hills", world.player),
             lambda state: can_use_hookshot(state, world))

    # Moderate: The Birdhouse - Dweller Platforms Relic with only Birdhouse access
    set_rule(world.multiworld.get_location("Alpine Skyline - The Birdhouse: Dweller Platforms Relic", world.player),
             lambda state: True)

    # Moderate: Twilight Path without Dweller Mask
    set_rule(world.multiworld.get_location("Alpine Skyline - The Twilight Path", world.player), lambda state: True)

    # Moderate: Mystifying Time Mesa time trial without hats
    set_rule(world.multiworld.get_location("Alpine Skyline - Mystifying Time Mesa: Zipline", world.player),
             lambda state: True)

    # Moderate: Goat Refinery from TIHS with Sprint only
    add_rule(world.multiworld.get_location("Alpine Skyline - Goat Refinery", world.player),
             lambda state: state.has("TIHS Access", world.player)
             and can_use_hat(state, world, HatType.SPRINT), "or")

    # Moderate: Finale Telescope with only Ice Hat
    add_rule(world.multiworld.get_entrance("Telescope -> Time's End", world.player),
             lambda state: state.has("Time Piece", world.player, world.chapter_timepiece_costs[ChapterIndex.FINALE])
             and can_use_hat(state, world, HatType.ICE), "or")

    # Moderate: Finale without Hookshot
    set_rule(world.multiworld.get_location("Act Completion (The Finale)", world.player),
             lambda state: can_use_hat(state, world, HatType.DWELLER))

    if world.is_dlc1():
        # Moderate: clear Rock the Boat without Ice Hat
        set_rule(world.multiworld.get_location("Rock the Boat - Post Captain Rescue", world.player), lambda state: True)
        set_rule(world.multiworld.get_location("Act Completion (Rock the Boat)", world.player), lambda state: True)

        # Moderate: clear Deep Sea without Ice Hat
        set_rule(world.multiworld.get_location("Act Completion (Time Rift - Deep Sea)", world.player),
                 lambda state: can_use_hookshot(state, world) and can_use_hat(state, world, HatType.DWELLER))

    # There is a glitched fall damage volume near the Yellow Overpass time piece that warps the player to Pink Paw.
    # Yellow Overpass time piece can also be reached without Hookshot quite easily.
    if world.is_dlc2():
        # No Hookshot
        set_rule(world.multiworld.get_location("Act Completion (Yellow Overpass Station)", world.player),
                 lambda state: True)

        # No Dweller, Hookshot, or Time Stop for these
        set_rule(world.multiworld.get_location("Pink Paw Station - Cat Vacuum", world.player), lambda state: True)
        set_rule(world.multiworld.get_location("Pink Paw Station - Behind Fan", world.player), lambda state: True)
        set_rule(world.multiworld.get_location("Pink Paw Station - Pink Ticket Booth", world.player), lambda state: True)
        set_rule(world.multiworld.get_location("Act Completion (Pink Paw Station)", world.player), lambda state: True)
        for key in shop_locations.keys():
            if "Pink Paw Station Thug" in key and is_location_valid(world, key):
                set_rule(world.multiworld.get_location(key, world.player), lambda state: True)

        # Moderate: clear Rush Hour without Hookshot
        set_rule(world.multiworld.get_location("Act Completion (Rush Hour)", world.player),
                 lambda state: state.has("Metro Ticket - Pink", world.player)
                 and state.has("Metro Ticket - Yellow", world.player)
                 and state.has("Metro Ticket - Blue", world.player)
                 and can_use_hat(state, world, HatType.ICE)
                 and can_use_hat(state, world, HatType.BREWING))

        # Moderate: Bluefin Tunnel + Pink Paw Station without tickets
        if not world.options.NoTicketSkips:
            set_rule(world.multiworld.get_entrance("-> Pink Paw Station", world.player), lambda state: True)
            set_rule(world.multiworld.get_entrance("-> Bluefin Tunnel", world.player), lambda state: True)


def set_hard_rules(world: "HatInTimeWorld"):
    # Hard: clear Time Rift - The Twilight Bell with Sprint+Scooter only
    add_rule(world.multiworld.get_location("Act Completion (Time Rift - The Twilight Bell)", world.player),
             lambda state: can_use_hat(state, world, HatType.SPRINT)
             and state.has("Scooter Badge", world.player), "or")

    # No Dweller Mask required
    set_rule(world.multiworld.get_location("Subcon Forest - Dweller Floating Rocks", world.player),
             lambda state: has_paintings(state, world, 3))
    set_rule(world.multiworld.get_location("Subcon Forest - Dweller Platforming Tree B", world.player),
             lambda state: has_paintings(state, world, 3))

    # Cherry bridge over boss arena gap
    set_rule(world.get_entrance("SF Behind Boss Firewall -> SF Boss Arena"), lambda state: True)

    set_rule(world.multiworld.get_location("Subcon Forest - Noose Treehouse", world.player),
             lambda state: has_paintings(state, world, 2, True))
    set_rule(world.multiworld.get_location("Subcon Forest - Long Tree Climb Chest", world.player),
             lambda state: has_paintings(state, world, 2, True))
    set_rule(world.multiworld.get_location("Subcon Forest - Tall Tree Hookshot Swing", world.player),
             lambda state: has_paintings(state, world, 3, True))

    # SDJ
    add_rule(world.multiworld.get_location("Act Completion (Time Rift - Curly Tail Trail)", world.player),
             lambda state: can_use_hat(state, world, HatType.SPRINT), "or")

    # Hard: Goat Refinery from TIHS with nothing
    add_rule(world.multiworld.get_location("Alpine Skyline - Goat Refinery", world.player),
             lambda state: state.has("TIHS Access", world.player), "or")

    if world.is_dlc1():
        # Hard: clear Deep Sea without Dweller Mask
        set_rule(world.multiworld.get_location("Act Completion (Time Rift - Deep Sea)", world.player),
                 lambda state: can_use_hookshot(state, world))

    if world.is_dlc2():
        # Hard: clear Green Clean Manhole without Dweller Mask
        set_rule(world.multiworld.get_location("Act Completion (Green Clean Manhole)", world.player),
                 lambda state: can_use_hat(state, world, HatType.ICE))

        # Hard: clear Rush Hour with Brewing Hat only
        if world.options.NoTicketSkips != NoTicketSkips.option_true:
            set_rule(world.multiworld.get_location("Act Completion (Rush Hour)", world.player),
                     lambda state: can_use_hat(state, world, HatType.BREWING))
        else:
            set_rule(world.multiworld.get_location("Act Completion (Rush Hour)", world.player),
                     lambda state: can_use_hat(state, world, HatType.BREWING)
                     and state.has("Metro Ticket - Yellow", world.player)
                     and state.has("Metro Ticket - Blue", world.player)
                     and state.has("Metro Ticket - Pink", world.player))


def set_expert_rules(world: "HatInTimeWorld"):
    # Finale Telescope with no hats
    set_rule(world.multiworld.get_entrance("Telescope -> Time's End", world.player),
             lambda state: state.has("Time Piece", world.player, world.chapter_timepiece_costs[ChapterIndex.FINALE]))

    # Expert: Mafia Town - Above Boats, Top of Lighthouse, and Hot Air Balloon with nothing
    set_rule(world.multiworld.get_location("Mafia Town - Above Boats", world.player), lambda state: True)
    set_rule(world.multiworld.get_location("Mafia Town - Top of Lighthouse", world.player), lambda state: True)
    # There are not enough buckets/beach balls to bucket/ball hover in Heating Up Mafia Town, so any other Mafia Town
    # act is required.
    add_rule(world.multiworld.get_location("Mafia Town - Hot Air Balloon", world.player),
             lambda state: state.can_reach_region("Mafia Town Area", world.player), "or")

    # Expert: Clear Dead Bird Studio with nothing
    for loc in world.multiworld.get_region("Dead Bird Studio - Post Elevator Area", world.player).locations:
        set_rule(loc, lambda state: True)

    set_rule(world.multiworld.get_location("Act Completion (Dead Bird Studio)", world.player), lambda state: True)

    # Expert: Clear Dead Bird Studio Basement without Hookshot
    for loc in world.multiworld.get_region("Dead Bird Studio Basement", world.player).locations:
        set_rule(loc, lambda state: True)

    # Expert: get to and clear Twilight Bell without Dweller Mask.
    # Dweller Mask OR Sprint Hat OR Brewing Hat OR Time Stop + Umbrella required to complete act.
    add_rule(world.multiworld.get_entrance("-> The Twilight Bell", world.player),
             lambda state: can_use_hookshot(state, world), "or")

    add_rule(world.multiworld.get_location("Act Completion (The Twilight Bell)", world.player),
             lambda state: can_use_hat(state, world, HatType.BREWING)
             or can_use_hat(state, world, HatType.DWELLER)
             or can_use_hat(state, world, HatType.SPRINT)
             or (can_use_hat(state, world, HatType.TIME_STOP) and state.has("Umbrella", world.player)))

    # Expert: Time Rift - Curly Tail Trail with nothing
    # Time Rift - Twilight Bell and Time Rift - Village with nothing
    set_rule(world.multiworld.get_location("Act Completion (Time Rift - Curly Tail Trail)", world.player),
             lambda state: True)

    set_rule(world.multiworld.get_location("Act Completion (Time Rift - Village)", world.player), lambda state: True)
    set_rule(world.multiworld.get_location("Act Completion (Time Rift - The Twilight Bell)", world.player),
             lambda state: True)

    # Expert: Cherry Hovering
    # Skipping the boss firewall is possible with a Cherry Hover.
    set_rule(world.get_entrance("SF Area -> SF Behind Boss Firewall"),
             lambda state: has_paintings(state, world, 1, True))
    # The boss arena gap can be crossed in reverse with a Cherry Hover.
    subcon_boss_arena = world.get_region("Subcon Forest Boss Arena")
    subcon_behind_boss_firewall = world.get_region("Subcon Forest Behind Boss Firewall")
    subcon_boss_arena.connect(subcon_behind_boss_firewall, "SF Boss Arena -> SF Behind Boss Firewall")

    subcon_area = world.get_region("Subcon Forest Area")

    # The boss firewall can be skipped in reverse with a Cherry Hover, but it is not possible to remove the boss
    # firewall from reverse because the paintings to burn to remove the firewall are on the other side of the firewall.
    # Therefore, a painting skip is required. The paintings could be burned by already having access to
    # "Subcon Forest Area" through another entrance, but making a new connection to "Subcon Forest Area" in that case
    # would be pointless.
    if not world.options.NoPaintingSkips:
        # The import cannot be done at the module-level because it would cause a circular import.
        from .Regions import get_region_shuffled_to

        subcon_behind_boss_firewall.connect(subcon_area, "SF Behind Boss Firewall -> SF Area")

        # Because the Your Contract has Expired entrance can now reach "Subcon Forest Area", it needs to be connected to
        # each of the Subcon Forest Time Rift entrances, like the other Subcon Forest Acts.
        yche = world.get_region("Your Contract has Expired")

        def connect_to_shuffled_act_at(original_act_name):
            region_name = get_region_shuffled_to(world, original_act_name)
            return yche.connect(world.get_region(region_name), f"{original_act_name} Portal - Entrance YCHE")

        # Rules copied from `Rules.set_rift_rules()` with painting logic removed because painting skips must be
        # available.
        entrance = connect_to_shuffled_act_at("Time Rift - Pipe")
        add_rule(entrance, lambda state: can_clear_required_act(state, world, "Subcon Forest - Act 2"))
        reg_act_connection(world, world.get_entrance("Subcon Forest - Act 2").connected_region, entrance)

        entrance = connect_to_shuffled_act_at("Time Rift - Village")
        add_rule(entrance, lambda state: can_clear_required_act(state, world, "Subcon Forest - Act 4"))
        reg_act_connection(world, world.get_entrance("Subcon Forest - Act 4").connected_region, entrance)

        entrance = connect_to_shuffled_act_at("Time Rift - Sleepy Subcon")
        add_rule(entrance, lambda state: has_relic_combo(state, world, "UFO"))

    set_rule(world.multiworld.get_location("Act Completion (Toilet of Doom)", world.player),
             lambda state: can_use_hookshot(state, world) and can_hit(state, world)
             and has_paintings(state, world, 1, True))

    # Set painting rules only. Skipping paintings is determined in has_paintings
    set_rule(world.multiworld.get_location("Subcon Forest - Magnet Badge Bush", world.player),
             lambda state: has_paintings(state, world, 3, True))

    # You can cherry hover to Snatcher's post-fight cutscene, which completes the level without having to fight him
    yche_post_fight = world.get_region("Your Contract has Expired - Post Fight")
    subcon_area.connect(yche_post_fight, "Snatcher Hover")
    # Cherry Hover from YCHE also works, so there are no requirements for the Act Completion.
    set_rule(world.get_location("Act Completion (Your Contract has Expired)"), lambda state: True)

    if world.is_dlc2():
        # Expert: clear Rush Hour with nothing
        if world.options.NoTicketSkips != NoTicketSkips.option_true:
            set_rule(world.multiworld.get_location("Act Completion (Rush Hour)", world.player), lambda state: True)
        else:
            set_rule(world.multiworld.get_location("Act Completion (Rush Hour)", world.player),
                     lambda state: state.has("Metro Ticket - Yellow", world.player)
                     and state.has("Metro Ticket - Blue", world.player)
                     and state.has("Metro Ticket - Pink", world.player))

        # Expert: Yellow/Green Manhole with nothing using a Boop Clip
        set_rule(world.multiworld.get_location("Act Completion (Yellow Overpass Manhole)", world.player),
                 lambda state: True)
        set_rule(world.multiworld.get_location("Act Completion (Green Clean Manhole)", world.player),
                 lambda state: True)


def set_mafia_town_rules(world: "HatInTimeWorld"):
    add_rule(world.multiworld.get_location("Mafia Town - Behind HQ Chest", world.player),
             lambda state: state.can_reach("Act Completion (Heating Up Mafia Town)", "Location", world.player)
             or state.can_reach("Down with the Mafia!", "Region", world.player)
             or state.can_reach("Cheating the Race", "Region", world.player)
             or state.can_reach("The Golden Vault", "Region", world.player))

    # Old guys don't appear in SCFOS
    add_rule(world.multiworld.get_location("Mafia Town - Old Man (Steel Beams)", world.player),
             lambda state: state.can_reach("Welcome to Mafia Town", "Region", world.player)
             or state.can_reach("Barrel Battle", "Region", world.player)
             or state.can_reach("Cheating the Race", "Region", world.player)
             or state.can_reach("The Golden Vault", "Region", world.player)
             or state.can_reach("Down with the Mafia!", "Region", world.player))

    add_rule(world.multiworld.get_location("Mafia Town - Old Man (Seaside Spaghetti)", world.player),
             lambda state: state.can_reach("Welcome to Mafia Town", "Region", world.player)
             or state.can_reach("Barrel Battle", "Region", world.player)
             or state.can_reach("Cheating the Race", "Region", world.player)
             or state.can_reach("The Golden Vault", "Region", world.player)
             or state.can_reach("Down with the Mafia!", "Region", world.player))

    # Only available outside She Came from Outer Space
    add_rule(world.multiworld.get_location("Mafia Town - Mafia Geek Platform", world.player),
             lambda state: state.can_reach("Welcome to Mafia Town", "Region", world.player)
             or state.can_reach("Barrel Battle", "Region", world.player)
             or state.can_reach("Down with the Mafia!", "Region", world.player)
             or state.can_reach("Cheating the Race", "Region", world.player)
             or state.can_reach("Heating Up Mafia Town", "Region", world.player)
             or state.can_reach("The Golden Vault", "Region", world.player))

    # Only available outside Down with the Mafia! (for some reason)
    add_rule(world.multiworld.get_location("Mafia Town - On Scaffolding", world.player),
             lambda state: state.can_reach("Welcome to Mafia Town", "Region", world.player)
             or state.can_reach("Barrel Battle", "Region", world.player)
             or state.can_reach("She Came from Outer Space", "Region", world.player)
             or state.can_reach("Cheating the Race", "Region", world.player)
             or state.can_reach("Heating Up Mafia Town", "Region", world.player)
             or state.can_reach("The Golden Vault", "Region", world.player))

    # For some reason, the brewing crate is removed in HUMT
    add_rule(world.multiworld.get_location("Mafia Town - Secret Cave", world.player),
             lambda state: state.has("HUMT Access", world.player), "or")

    # Can bounce across the lava to get this without Hookshot (need to die though)
    add_rule(world.multiworld.get_location("Mafia Town - Above Boats", world.player),
             lambda state: state.has("HUMT Access", world.player), "or")

    if world.options.CTRLogic == CTRLogic.option_nothing:
        set_rule(world.multiworld.get_location("Act Completion (Cheating the Race)", world.player), lambda state: True)
    elif world.options.CTRLogic == CTRLogic.option_sprint:
        add_rule(world.multiworld.get_location("Act Completion (Cheating the Race)", world.player),
                 lambda state: can_use_hat(state, world, HatType.SPRINT), "or")
    elif world.options.CTRLogic == CTRLogic.option_scooter:
        add_rule(world.multiworld.get_location("Act Completion (Cheating the Race)", world.player),
                 lambda state: can_use_hat(state, world, HatType.SPRINT)
                 and state.has("Scooter Badge", world.player), "or")


def set_botb_rules(world: "HatInTimeWorld"):
    if not world.options.UmbrellaLogic and get_difficulty(world) < Difficulty.MODERATE:
        set_rule(world.multiworld.get_location("Dead Bird Studio - DJ Grooves Sign Chest", world.player),
                 lambda state: state.has("Umbrella", world.player) or can_use_hat(state, world, HatType.BREWING))
        set_rule(world.multiworld.get_location("Dead Bird Studio - Tepee Chest", world.player),
                 lambda state: state.has("Umbrella", world.player) or can_use_hat(state, world, HatType.BREWING))
        set_rule(world.multiworld.get_location("Dead Bird Studio - Conductor Chest", world.player),
                 lambda state: state.has("Umbrella", world.player) or can_use_hat(state, world, HatType.BREWING))
        set_rule(world.multiworld.get_location("Act Completion (Dead Bird Studio)", world.player),
                 lambda state: state.has("Umbrella", world.player) or can_use_hat(state, world, HatType.BREWING))


def set_subcon_rules(world: "HatInTimeWorld"):
    set_rule(world.multiworld.get_location("Act Completion (Time Rift - Village)", world.player),
             lambda state: can_use_hat(state, world, HatType.BREWING) or state.has("Umbrella", world.player)
             or can_use_hat(state, world, HatType.DWELLER))

    # You can't skip over the boss arena wall without cherry hover.
    set_rule(world.get_entrance("SF Area -> SF Behind Boss Firewall"),
             lambda state: has_paintings(state, world, 1, False))

    # The hookpoints to cross the boss arena gap are only present in Toilet of Doom.
    set_rule(world.get_entrance("SF Behind Boss Firewall -> SF Boss Arena"),
             lambda state: state.has("TOD Access", world.player)
             and can_use_hookshot(state, world))

    # The Act Completion is in the Toilet of Doom region, so the same rules as passing the boss firewall and crossing
    # the boss arena gap are required. "TOD Access" is implied from the region so does not need to be included in the
    # rule.
    set_rule(world.multiworld.get_location("Act Completion (Toilet of Doom)", world.player),
             lambda state: can_use_hookshot(state, world) and can_hit(state, world)
             and has_paintings(state, world, 1, False))

    add_rule(world.multiworld.get_entrance("Subcon Forest - Act 2", world.player),
             lambda state: state.has("Snatcher's Contract - The Subcon Well", world.player))

    add_rule(world.multiworld.get_entrance("Subcon Forest - Act 3", world.player),
             lambda state: state.has("Snatcher's Contract - Toilet of Doom", world.player))

    add_rule(world.multiworld.get_entrance("Subcon Forest - Act 4", world.player),
             lambda state: state.has("Snatcher's Contract - Queen Vanessa's Manor", world.player))

    add_rule(world.multiworld.get_entrance("Subcon Forest - Act 5", world.player),
             lambda state: state.has("Snatcher's Contract - Mail Delivery Service", world.player))

    if painting_logic(world):
        add_rule(world.multiworld.get_location("Act Completion (Contractual Obligations)", world.player),
                 lambda state: has_paintings(state, world, 1, False))


def set_alps_rules(world: "HatInTimeWorld"):
    add_rule(world.multiworld.get_entrance("-> The Birdhouse", world.player),
             lambda state: can_use_hookshot(state, world) and can_use_hat(state, world, HatType.BREWING))

    add_rule(world.multiworld.get_entrance("-> The Lava Cake", world.player),
             lambda state: can_use_hookshot(state, world))

    add_rule(world.multiworld.get_entrance("-> The Windmill", world.player),
             lambda state: can_use_hookshot(state, world))

    add_rule(world.multiworld.get_entrance("-> The Twilight Bell", world.player),
             lambda state: can_use_hookshot(state, world) and can_use_hat(state, world, HatType.DWELLER))

    add_rule(world.multiworld.get_location("Alpine Skyline - Mystifying Time Mesa: Zipline", world.player),
             lambda state: can_use_hat(state, world, HatType.SPRINT) or can_use_hat(state, world, HatType.TIME_STOP))

    add_rule(world.multiworld.get_entrance("Alpine Skyline - Finale", world.player),
             lambda state: can_clear_alpine(state, world))

    add_rule(world.multiworld.get_location("Alpine Skyline - Goat Refinery", world.player),
             lambda state: state.has("AFR Access", world.player)
             and can_use_hookshot(state, world)
             and can_hit(state, world, True))


def set_dlc1_rules(world: "HatInTimeWorld"):
    add_rule(world.multiworld.get_entrance("Cruise Ship Entrance BV", world.player),
             lambda state: can_use_hookshot(state, world))

    # This particular item isn't present in Act 3 for some reason, yes in vanilla too
    add_rule(world.multiworld.get_location("The Arctic Cruise - Toilet", world.player),
             lambda state: (state.can_reach("Bon Voyage!", "Region", world.player) and can_use_hookshot(state, world))
             or state.can_reach("Ship Shape", "Region", world.player))


def set_dlc2_rules(world: "HatInTimeWorld"):
    add_rule(world.multiworld.get_entrance("-> Bluefin Tunnel", world.player),
             lambda state: state.has("Metro Ticket - Green", world.player)
             or state.has("Metro Ticket - Blue", world.player))

    add_rule(world.multiworld.get_entrance("-> Pink Paw Station", world.player),
             lambda state: state.has("Metro Ticket - Pink", world.player)
             or state.has("Metro Ticket - Yellow", world.player) and state.has("Metro Ticket - Blue", world.player))

    add_rule(world.multiworld.get_entrance("Nyakuza Metro - Finale", world.player),
             lambda state: can_clear_metro(state, world))

    add_rule(world.multiworld.get_location("Act Completion (Rush Hour)", world.player),
             lambda state: state.has("Metro Ticket - Yellow", world.player)
             and state.has("Metro Ticket - Blue", world.player)
             and state.has("Metro Ticket - Pink", world.player))

    for key in shop_locations.keys():
        if "Green Clean Station Thug B" in key and is_location_valid(world, key):
            add_rule(world.multiworld.get_location(key, world.player),
                     lambda state: state.has("Metro Ticket - Yellow", world.player), "or")


def reg_act_connection(world: "HatInTimeWorld", region: Union[str, Region], unlocked_entrance: Union[str, Entrance]):
    reg: Region
    entrance: Entrance
    if isinstance(region, str):
        reg = world.multiworld.get_region(region, world.player)
    else:
        reg = region

    if isinstance(unlocked_entrance, str):
        entrance = world.multiworld.get_entrance(unlocked_entrance, world.player)
    else:
        entrance = unlocked_entrance

    world.multiworld.register_indirect_condition(reg, entrance)


# See randomize_act_entrances in Regions.py
# Called before set_rules
def set_rift_rules(world: "HatInTimeWorld", regions: Dict[str, Region]):

    # This is accessing the regions in place of these time rifts, so we can set the rules on all the entrances.
    for entrance in regions["Time Rift - Gallery"].entrances:
        add_rule(entrance, lambda state: can_use_hat(state, world, HatType.BREWING)
                 and state.has("Time Piece", world.player, world.chapter_timepiece_costs[ChapterIndex.BIRDS]))

    for entrance in regions["Time Rift - The Lab"].entrances:
        add_rule(entrance, lambda state: can_use_hat(state, world, HatType.DWELLER)
                 and state.has("Time Piece", world.player, world.chapter_timepiece_costs[ChapterIndex.ALPINE]))

    for entrance in regions["Time Rift - Sewers"].entrances:
        add_rule(entrance, lambda state: can_clear_required_act(state, world, "Mafia Town - Act 4"))
        reg_act_connection(world, world.multiworld.get_entrance("Mafia Town - Act 4",
                                                                world.player).connected_region, entrance)

    for entrance in regions["Time Rift - Bazaar"].entrances:
        add_rule(entrance, lambda state: can_clear_required_act(state, world, "Mafia Town - Act 6"))
        reg_act_connection(world, world.multiworld.get_entrance("Mafia Town - Act 6",
                                                                world.player).connected_region, entrance)

    for entrance in regions["Time Rift - Mafia of Cooks"].entrances:
        add_rule(entrance, lambda state: has_relic_combo(state, world, "Burger"))

    for entrance in regions["Time Rift - The Owl Express"].entrances:
        add_rule(entrance, lambda state: can_clear_required_act(state, world, "Battle of the Birds - Act 2"))
        add_rule(entrance, lambda state: can_clear_required_act(state, world, "Battle of the Birds - Act 3"))
        reg_act_connection(world, world.multiworld.get_entrance("Battle of the Birds - Act 2",
                                                                world.player).connected_region, entrance)
        reg_act_connection(world, world.multiworld.get_entrance("Battle of the Birds - Act 3",
                                                                world.player).connected_region, entrance)

    for entrance in regions["Time Rift - The Moon"].entrances:
        add_rule(entrance, lambda state: can_clear_required_act(state, world, "Battle of the Birds - Act 4"))
        add_rule(entrance, lambda state: can_clear_required_act(state, world, "Battle of the Birds - Act 5"))
        reg_act_connection(world, world.multiworld.get_entrance("Battle of the Birds - Act 4",
                                                                world.player).connected_region, entrance)
        reg_act_connection(world, world.multiworld.get_entrance("Battle of the Birds - Act 5",
                                                                world.player).connected_region, entrance)

    for entrance in regions["Time Rift - Dead Bird Studio"].entrances:
        add_rule(entrance, lambda state: has_relic_combo(state, world, "Train"))

    for entrance in regions["Time Rift - Pipe"].entrances:
        add_rule(entrance, lambda state: can_clear_required_act(state, world, "Subcon Forest - Act 2"))
        reg_act_connection(world, world.multiworld.get_entrance("Subcon Forest - Act 2",
                                                                world.player).connected_region, entrance)
        if painting_logic(world):
            add_rule(entrance, lambda state: has_paintings(state, world, 2))

    for entrance in regions["Time Rift - Village"].entrances:
        add_rule(entrance, lambda state: can_clear_required_act(state, world, "Subcon Forest - Act 4"))
        reg_act_connection(world, world.multiworld.get_entrance("Subcon Forest - Act 4",
                                                                world.player).connected_region, entrance)

        if painting_logic(world):
            add_rule(entrance, lambda state: has_paintings(state, world, 2))

    for entrance in regions["Time Rift - Sleepy Subcon"].entrances:
        add_rule(entrance, lambda state: has_relic_combo(state, world, "UFO"))
        if painting_logic(world):
            add_rule(entrance, lambda state: has_paintings(state, world, 3))

    for entrance in regions["Time Rift - Curly Tail Trail"].entrances:
        add_rule(entrance, lambda state: state.has("Windmill Cleared", world.player))

    for entrance in regions["Time Rift - The Twilight Bell"].entrances:
        add_rule(entrance, lambda state: state.has("Twilight Bell Cleared", world.player))

    for entrance in regions["Time Rift - Alpine Skyline"].entrances:
        add_rule(entrance, lambda state: has_relic_combo(state, world, "Crayon"))
        if entrance.parent_region.name == "Alpine Free Roam":
            add_rule(entrance,
                     lambda state: can_use_hookshot(state, world) and can_hit(state, world, umbrella_only=True))

    if world.is_dlc1():
        for entrance in regions["Time Rift - Balcony"].entrances:
            add_rule(entrance, lambda state: can_clear_required_act(state, world, "The Arctic Cruise - Finale"))
            reg_act_connection(world, world.multiworld.get_entrance("The Arctic Cruise - Finale",
                                                                    world.player).connected_region, entrance)

        for entrance in regions["Time Rift - Deep Sea"].entrances:
            add_rule(entrance, lambda state: has_relic_combo(state, world, "Cake"))

    if world.is_dlc2():
        for entrance in regions["Time Rift - Rumbi Factory"].entrances:
            add_rule(entrance, lambda state: has_relic_combo(state, world, "Necklace"))


# Basically the same as above, but without the need of the dict since we are just setting defaults
# Called if Act Rando is disabled
def set_default_rift_rules(world: "HatInTimeWorld"):

    for entrance in world.multiworld.get_region("Time Rift - Gallery", world.player).entrances:
        add_rule(entrance, lambda state: can_use_hat(state, world, HatType.BREWING)
                 and state.has("Time Piece", world.player, world.chapter_timepiece_costs[ChapterIndex.BIRDS]))

    for entrance in world.multiworld.get_region("Time Rift - The Lab", world.player).entrances:
        add_rule(entrance, lambda state: can_use_hat(state, world, HatType.DWELLER)
                 and state.has("Time Piece", world.player, world.chapter_timepiece_costs[ChapterIndex.ALPINE]))

    for entrance in world.multiworld.get_region("Time Rift - Sewers", world.player).entrances:
        add_rule(entrance, lambda state: can_clear_required_act(state, world, "Mafia Town - Act 4"))
        reg_act_connection(world, "Down with the Mafia!", entrance.name)

    for entrance in world.multiworld.get_region("Time Rift - Bazaar", world.player).entrances:
        add_rule(entrance, lambda state: can_clear_required_act(state, world, "Mafia Town - Act 6"))
        reg_act_connection(world, "Heating Up Mafia Town", entrance.name)

    for entrance in world.multiworld.get_region("Time Rift - Mafia of Cooks", world.player).entrances:
        add_rule(entrance, lambda state: has_relic_combo(state, world, "Burger"))

    for entrance in world.multiworld.get_region("Time Rift - The Owl Express", world.player).entrances:
        add_rule(entrance, lambda state: can_clear_required_act(state, world, "Battle of the Birds - Act 2"))
        add_rule(entrance, lambda state: can_clear_required_act(state, world, "Battle of the Birds - Act 3"))
        reg_act_connection(world, "Murder on the Owl Express", entrance.name)
        reg_act_connection(world, "Picture Perfect", entrance.name)

    for entrance in world.multiworld.get_region("Time Rift - The Moon", world.player).entrances:
        add_rule(entrance, lambda state: can_clear_required_act(state, world, "Battle of the Birds - Act 4"))
        add_rule(entrance, lambda state: can_clear_required_act(state, world, "Battle of the Birds - Act 5"))
        reg_act_connection(world, "Train Rush", entrance.name)
        reg_act_connection(world, "The Big Parade", entrance.name)

    for entrance in world.multiworld.get_region("Time Rift - Dead Bird Studio", world.player).entrances:
        add_rule(entrance, lambda state: has_relic_combo(state, world, "Train"))

    for entrance in world.multiworld.get_region("Time Rift - Pipe", world.player).entrances:
        add_rule(entrance, lambda state: can_clear_required_act(state, world, "Subcon Forest - Act 2"))
        reg_act_connection(world, "The Subcon Well", entrance.name)
        if painting_logic(world):
            add_rule(entrance, lambda state: has_paintings(state, world, 2))

    for entrance in world.multiworld.get_region("Time Rift - Village", world.player).entrances:
        add_rule(entrance, lambda state: can_clear_required_act(state, world, "Subcon Forest - Act 4"))
        reg_act_connection(world, "Queen Vanessa's Manor", entrance.name)
        if painting_logic(world):
            add_rule(entrance, lambda state: has_paintings(state, world, 2))

    for entrance in world.multiworld.get_region("Time Rift - Sleepy Subcon", world.player).entrances:
        add_rule(entrance, lambda state: has_relic_combo(state, world, "UFO"))
        if painting_logic(world):
            add_rule(entrance, lambda state: has_paintings(state, world, 3))

    for entrance in world.multiworld.get_region("Time Rift - Curly Tail Trail", world.player).entrances:
        add_rule(entrance, lambda state: state.has("Windmill Cleared", world.player))

    for entrance in world.multiworld.get_region("Time Rift - The Twilight Bell", world.player).entrances:
        add_rule(entrance, lambda state: state.has("Twilight Bell Cleared", world.player))

    for entrance in world.multiworld.get_region("Time Rift - Alpine Skyline", world.player).entrances:
        add_rule(entrance, lambda state: has_relic_combo(state, world, "Crayon"))
        if entrance.parent_region.name == "Alpine Free Roam":
            add_rule(entrance,
                     lambda state: can_use_hookshot(state, world) and can_hit(state, world, umbrella_only=True))

    if world.is_dlc1():
        for entrance in world.multiworld.get_region("Time Rift - Balcony", world.player).entrances:
            add_rule(entrance, lambda state: can_clear_required_act(state, world, "The Arctic Cruise - Finale"))
            reg_act_connection(world, "Rock the Boat", entrance.name)

        for entrance in world.multiworld.get_region("Time Rift - Deep Sea", world.player).entrances:
            add_rule(entrance, lambda state: has_relic_combo(state, world, "Cake"))

    if world.is_dlc2():
        for entrance in world.multiworld.get_region("Time Rift - Rumbi Factory", world.player).entrances:
            add_rule(entrance, lambda state: has_relic_combo(state, world, "Necklace"))


def set_event_rules(world: "HatInTimeWorld"):
    for (name, data) in event_locs.items():
        if not is_location_valid(world, name):
            continue

        event: Location = world.multiworld.get_location(name, world.player)

        if data.act_event:
            add_rule(event, world.multiworld.get_location(f"Act Completion ({data.region})", world.player).access_rule)
