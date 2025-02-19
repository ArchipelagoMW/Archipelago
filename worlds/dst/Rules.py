from typing import Dict, Set, Optional, Callable

from BaseClasses import CollectionState, Item
from worlds.generic.Rules import exclusion_rules, set_rule, add_rule, add_item_rule, forbid_item
from worlds.AutoWorld import World

from .Locations import location_data_table, DSTLocation
from .Options import DSTOptions
from .Items import item_data_table
from .ItemPool import DSTItemPool
from .Constants import REGION, PHASE, SEASON, SEASONS_PASSED, SPECIAL_TAGS, BOSS_PREREQUISITES
from . import Util

class DSTRule:
    event:str
    rule:Callable[[CollectionState], bool]
    optional_rule:Callable[[CollectionState], bool]
    optional_event:Callable[[CollectionState], bool]
    is_progression:bool = True
    is_rule:bool = True
    def __init__(self, event:str, player:int):
        self.event = f"(EVENT) {event}"
        self.optional_event = self.event
        self.rule = lambda state: state.has(self.event, player)
        self.optional_rule = self.rule

    def __call__(self, state: CollectionState) -> bool:
        # Eventually nothing should be calling this
        return self.rule(state)

def ALWAYS_TRUE(state: CollectionState) -> bool:
    return True

def ALWAYS_FALSE(state: CollectionState) -> bool:
    return False

def NO_ADVANCEMENT_ITEM(item: Item) -> bool:
    return not item.advancement

def combine_rules(*rules: Callable[[CollectionState], bool]) -> Callable[[CollectionState], bool]:
    for v in rules:
        assert callable(v), v
    if len(rules) == 1:
        return rules[0]
    a, b, *r = rules
    if a == ALWAYS_FALSE or b == ALWAYS_FALSE:
        return ALWAYS_FALSE
    if a == ALWAYS_TRUE: return combine_rules(b, *r)
    if b == ALWAYS_TRUE: return combine_rules(a, *r)
    new_rule = lambda state: a(state) and b(state)
    return combine_rules(new_rule, *r)

def either_rule(*rules: Callable[[CollectionState], bool]) -> Callable[[CollectionState], bool]:
    for v in rules:
        assert callable(v), v
    if len(rules) == 1:
        return rules[0]
    a, b, *r = rules
    if a == ALWAYS_TRUE or b == ALWAYS_TRUE:
        return ALWAYS_TRUE
    if a == ALWAYS_FALSE: return either_rule(b, *r)
    if b == ALWAYS_FALSE: return either_rule(a, *r)
    new_rule = lambda state: a(state) or b(state)
    return either_rule(new_rule, *r)

def set_rules(dst_world: World, itempool:DSTItemPool) -> None:
    multiworld = dst_world.multiworld
    player = dst_world.player
    options:DSTOptions = dst_world.options

    # I don't know if this is something I want to make an option for, so we'll just have priority locations controlled by this
    USE_PRIORITY_TAGS = False

    WHITELIST = Util.build_whitelist(options)
    EXISTING_LOCATIONS = {location.name for location in multiworld.get_locations(player)}
    SEASON_HELPER_ITEMS = {name for name, data in item_data_table.items() if "seasonhelper" in data.tags}
    TRAP_ITEMS = {name for name, data in item_data_table.items() if "trap" in data.tags}
    ADVANCED_PLAYER_BIAS = options.skill_level.value != options.skill_level.option_easy
    EXPERT_PLAYER_BIAS = options.skill_level.value == options.skill_level.option_expert
    CREATURE_LOCATIONS_ENABLED = bool(options.creature_locations.value)
    PEACEFUL_LOGIC = options.creature_locations.value == options.creature_locations.option_peaceful
    WARLY_DISHES_ENABLED = options.cooking_locations.value == options.cooking_locations.option_warly_enabled
    CHESSPIECE_ITEMS_SHUFFLED = bool(options.chesspiece_sketch_items.value)
    LOCKED_INGREDIENTS_LOGIC = bool(options.crafting_mode.value == options.crafting_mode.option_locked_ingredients)
    LIGHTING_LOGIC = bool(options.lighting_logic.value)
    WEAPON_LOGIC = bool(options.weapon_logic.value)
    SEASON_GEAR_LOGIC = bool(options.season_gear_logic.value)
    BASE_MAKING_LOGIC = bool(options.base_making_logic.value)
    BACKPACK_LOGIC = bool(options.backpack_logic.value)
    HEALING_LOGIC = bool(options.healing_logic.value)
    CHARACTER_SWITCHING_LOGIC = True
    NORMAL_SEASON_FLOW_LOGIC = options.season_flow.value != options.season_flow.option_unlockable_shuffled
    UNLOCKABLE_SEASON_LOGIC = options.season_flow.current_key.startswith("unlockable")
    STARTING_SEASON = (
        SEASON.WINTER      if options.starting_season.value == options.starting_season.option_winter
        else SEASON.SPRING if options.starting_season.value == options.starting_season.option_spring
        else SEASON.SUMMER if options.starting_season.value == options.starting_season.option_summer
        else SEASON.AUTUMN
    )
    DAMAGE_BONUSES_IN_WORLD = "Damage Bonus" in itempool.nonfiller_itempool or "Damage Bonus" in options.start_inventory.value.keys()


    # Easy way to check if items are locked
    def is_locked(item_name:str): return item_name in itempool.locked_items

    # Make a rule that is just ALWAYS_TRUE
    def add_spawn_event():
        dst_rule = DSTRule("Spawn", player)
        dst_rule.is_progression = False
        item = multiworld.create_item(dst_rule.event, player)
        multiworld.push_precollected(item)
        return dst_rule
    spawn = add_spawn_event()

    def add_event(event:str, regionname:str, rule:Callable[[CollectionState], bool], custom_item:Optional[str] = None, hide_in_spoiler:bool = False, force_unique:bool = False):
        assert callable(rule)
        dst_rule = DSTRule(event, player)
        # Create event for rule
        if regionname in WHITELIST and not rule == ALWAYS_FALSE:
            if rule == ALWAYS_TRUE and not force_unique:
                # No need to create an event if always true
                return spawn
            else:
                region = multiworld.get_region(regionname, player)
                loc = DSTLocation(player, dst_rule.event, None, region)
                loc.show_in_spoiler = False if hide_in_spoiler else (not event in item_data_table.keys())
                dst_rule.is_progression = True
                item = multiworld.create_item(custom_item or dst_rule.event, player)
                loc.place_locked_item(item)
                region.locations.append(loc)
                add_rule(loc, rule)
        else:
            dst_rule.is_progression = False
            dst_rule.is_rule = False
            dst_rule.optional_rule = ALWAYS_TRUE
            dst_rule.optional_event = spawn.event
        return dst_rule

    # Rules directly associated with a location, so additional rules would be added to the event rather than the location
    PARENT_EVENTS:Dict[str, str] = {}
    def add_parent_event(event:str, regionname:str, rule:Callable[[CollectionState], bool]):
        dst_rule = add_event(event, regionname, rule, hide_in_spoiler = True, force_unique = True)
        if dst_rule.is_progression:
            PARENT_EVENTS[event] = dst_rule.event
        return dst_rule

    BOSS_COMPLETION_GOALS:Dict[str, str] = {}
    def add_boss_event(event:str, regionname:str, rule:Callable[[CollectionState], bool]):
        dst_rule = add_event(event, regionname if event in EXISTING_LOCATIONS else REGION.NONE, rule, force_unique = True)
        BOSS_COMPLETION_GOALS[event] = dst_rule.event
        if dst_rule.is_progression:
            PARENT_EVENTS[event] = dst_rule.event
        return dst_rule

    # Build farm plant season rules
    def _get_season_rule_for_farmplant(veggie) -> Callable[[CollectionState], bool]:
        _intersect = location_data_table[f"Grow Giant {veggie}"].tags.intersection({"autumn","winter","spring","summer"})
        _lookup:Dict[str, Callable[[CollectionState], bool]] = {
            "autumn": lambda state: state.has(autumn.event, player),
            "winter": lambda state: state.has(winter.event, player),
            "spring": lambda state: state.has(spring.event, player),
            "summer": lambda state: state.has(summer.event, player),
        }
        _rules = [_lookup[tag_name] for tag_name in _intersect if SEASON.tag_lookup[tag_name] in WHITELIST]
        return (
            ALWAYS_FALSE if not SEASONS_PASSED.SEASONS_1 in WHITELIST
            else ALWAYS_TRUE if not len(_intersect)
            else ALWAYS_FALSE if not len(_rules)
            else either_rule(*_rules)
        )

    FARMPLANT_SEASON_RULES:Dict[str, Callable[[CollectionState], bool]] = {
        **{veggie_name: _get_season_rule_for_farmplant(veggie_name) for veggie_name in
            [
                "Asparagus",
                "Garlic",
                "Pumpkin",
                "Corn",
                "Onion",
                "Potato",
                "Dragon Fruit",
                "Pomegranate",
                "Eggplant",
                "Toma Root",
                "Watermelon",
                "Pepper",
                "Durian",
                "Carrot"
            ]
        },
    }

    def add_farming_event(veggie_name:str, or_rule:Optional[Callable[[CollectionState], bool]] = None):
        veggie_seeds_name = f"{veggie_name} Seeds"
        veggie_season_rule = FARMPLANT_SEASON_RULES.get(veggie_name, ALWAYS_TRUE)
        return add_event(f"{veggie_name} Farming",
            (
                REGION.FOREST if (
                    is_locked(veggie_seeds_name)
                    or (or_rule != None)
                    or (veggie_season_rule != ALWAYS_FALSE))
                else REGION.NONE
            ),
            either_rule(
                combine_rules(
                    lambda state: state.has(basic_farming.event, player),
                    (
                        (lambda state: state.has(veggie_seeds_name, player)) if is_locked(veggie_seeds_name)
                        else veggie_season_rule
                    )
                ),
                or_rule if or_rule != None else ALWAYS_FALSE
            )
        )

    def add_hermit_event(event:str, rule:Callable[[CollectionState], bool], is_rule:bool = True):
        return add_event(event, REGION.OCEAN if is_rule else REGION.NONE, rule, "Crabby Hermit Friendship")

    # Misc rules
    def has_survived_num_days_rule(day_goal: int) -> Callable[[CollectionState], bool]:
        conditions = {basic_survival.event}
        if day_goal > 7: conditions.add(basic_exploration.event)
        if day_goal > 11: conditions.add(seasons_passed_half.event)
        if day_goal > 14: conditions.add(base_making.event)
        if day_goal > 20: conditions.add(seasons_passed_1.event)
        if day_goal > 35: conditions.add(seasons_passed_2.event)
        if day_goal > 55: conditions.add(seasons_passed_3.event)
        if day_goal > 70: conditions.add(seasons_passed_4.event)
        if day_goal > 90: conditions.add(seasons_passed_5.event)
        
        return lambda state: state.has_all(conditions, player)

    # Create a cache to store progression item number later, since we don't know how many there are yet
    _prog_item_num_cache:Dict[float, int] = {}
    def set_num_prog_items():
        for frac in _prog_item_num_cache:
            _prog_item_num_cache[frac] = (frac*itempool.get_num_progression_items_in_pool()) + itempool.get_num_precollected_progression_items()
    itempool.on_finalize_itempool = lambda: set_num_prog_items()
    def fraction_of_prog_items_rule(fraction: float) -> Callable[[CollectionState], bool]:
        _prog_item_num_cache[fraction] = 0 # Set the key as a placeholder
        return lambda state: state.count_group("all", player) > _prog_item_num_cache[fraction]


    ##### DAY PHASES #####
    day =   add_event("Day",   REGION.FOREST if PHASE.DAY   in WHITELIST else REGION.NONE, ALWAYS_TRUE) # TODO: Can have day phases as an item potentially. Logic's set up already
    dusk =  add_event("Dusk",  REGION.FOREST if PHASE.DUSK  in WHITELIST else REGION.NONE, ALWAYS_TRUE)
    night = add_event("Night", REGION.FOREST if PHASE.NIGHT in WHITELIST else REGION.NONE, ALWAYS_TRUE)

    ##### SEASONS #####
    season_order = [
        _season for _season in [
            SEASON.AUTUMN, SEASON.WINTER, SEASON.SPRING, SEASON.SUMMER
        ] if _season in WHITELIST
    ]

    def shift_season():
        _ret = season_order.pop(0)
        season_order.append(_ret)
        return _ret

    # Align season order with starting season
    if NORMAL_SEASON_FLOW_LOGIC:
        if STARTING_SEASON in season_order:
            while season_order[0] != STARTING_SEASON:
                shift_season()

    SEASON_RULES:Dict[str, Callable[[CollectionState], bool]] = {
        SEASON.AUTUMN: (
            ALWAYS_TRUE if STARTING_SEASON == SEASON.AUTUMN
            else combine_rules(
                (lambda state: state.has("Autumn", player)) if UNLOCKABLE_SEASON_LOGIC
                else ALWAYS_TRUE
            )
        ),
        SEASON.WINTER: (
            ALWAYS_TRUE if STARTING_SEASON == SEASON.WINTER
            else combine_rules(
                lambda state: state.has(winter_survival.event, player),
                (lambda state: state.has("Winter", player)) if UNLOCKABLE_SEASON_LOGIC
                else ALWAYS_TRUE
            )
        ),
        SEASON.SPRING: (
            ALWAYS_TRUE if STARTING_SEASON == SEASON.SPRING
            else combine_rules(
                lambda state: state.has(spring_survival.event, player),
                (lambda state: state.has("Spring", player)) if UNLOCKABLE_SEASON_LOGIC
                else ALWAYS_TRUE
            )
        ),
        SEASON.SUMMER: (
            ALWAYS_TRUE if STARTING_SEASON == SEASON.SUMMER
            else combine_rules(
                lambda state: state.has(summer_survival.event, player),
                (lambda state: state.has("Summer", player)) if UNLOCKABLE_SEASON_LOGIC
                else ALWAYS_TRUE
            )
        ),
    }

    _season_event_cache:Dict[str, Optional[DSTRule]] = {
        SEASON.AUTUMN:  None,
        SEASON.WINTER:  None,
        SEASON.SPRING:  None,
        SEASON.SUMMER:  None,
    }

    # In normal season flow logic, season events will be combined with season-passed events, otherwise they'll be separate
    EQUIVALENT_SEASONS:Dict[DSTRule, str] = {}
    def add_season_passed_event(event:str, time_tag:str, rule:Callable[[CollectionState], bool], merge_with_season:bool = True) -> DSTRule:
        _regionname = REGION.FOREST
        if not NORMAL_SEASON_FLOW_LOGIC:
            dst_rule = add_event(event, _regionname, rule)
            dst_rule.is_progression = time_tag in WHITELIST
            return dst_rule
        else:
            _season = shift_season()
            _is_season_in_cache = _season_event_cache[_season] != None
            _event_name = (
                f"{event} - {_season}" if not UNLOCKABLE_SEASON_LOGIC
                else f"{_season} around {event}" if NORMAL_SEASON_FLOW_LOGIC and not _is_season_in_cache
                else event
            )
            dst_rule = add_event(_event_name, _regionname,
                combine_rules(
                    rule,
                    SEASON_RULES[_season] if not _is_season_in_cache
                    else ALWAYS_TRUE
                )
            )
            dst_rule.is_progression = time_tag in WHITELIST
            if not _is_season_in_cache:
                _season_event_cache[_season] = dst_rule if merge_with_season else spawn
            if not UNLOCKABLE_SEASON_LOGIC:
                EQUIVALENT_SEASONS[dst_rule] = _season
            return dst_rule

    seasons_passed_half =   add_season_passed_event("Day 11", SEASONS_PASSED.SEASONS_HALF,
                                combine_rules(
                                    fraction_of_prog_items_rule(.5/6),
                                    # Get you the rest of seasonal gear at this point in a non-autumn start
                                    (lambda state: state.has(winter_survival.event, player)) if STARTING_SEASON == SEASON.WINTER
                                    else (lambda state: state.has(spring_survival.event, player)) if STARTING_SEASON == SEASON.SPRING
                                    else (lambda state: state.has(summer_survival.event, player)) if STARTING_SEASON == SEASON.SUMMER
                                    else ALWAYS_TRUE
                                ),
                                merge_with_season = False)
    seasons_passed_1 =      add_season_passed_event("Day 21", SEASONS_PASSED.SEASONS_1,
                                combine_rules(
                                    fraction_of_prog_items_rule(1/6),
                                    lambda state: state.has(seasons_passed_half.event, player)
                                ))
    seasons_passed_2 =      add_season_passed_event("Day 36", SEASONS_PASSED.SEASONS_2,
                                combine_rules(
                                    fraction_of_prog_items_rule(2/6),
                                    lambda state: state.has(seasons_passed_1.event, player)
                                ))
    seasons_passed_3 =      add_season_passed_event("Day 56", SEASONS_PASSED.SEASONS_3,
                                combine_rules(
                                    fraction_of_prog_items_rule(3/6),
                                    lambda state: state.has(seasons_passed_2.event, player)
                                ))
    seasons_passed_4 =      add_season_passed_event("Day 71", SEASONS_PASSED.SEASONS_4,
                                combine_rules(
                                    fraction_of_prog_items_rule(4/6),
                                    lambda state: state.has(seasons_passed_3.event, player)
                                ))
    seasons_passed_5 =      add_season_passed_event("Day 91", SEASONS_PASSED.SEASONS_5,
                                combine_rules(
                                    fraction_of_prog_items_rule(5/6),
                                    lambda state: state.has(seasons_passed_4.event, player)
                                ))

    # These must be called after creating season-passed events
    def add_season_event(season:str) -> DSTRule:
        return (
            _season_event_cache[season] if _season_event_cache[season]
            else add_event(f"Switch to {season}", REGION.FOREST if season in WHITELIST else REGION.NONE, SEASON_RULES[season])
        )

    autumn = add_season_event(SEASON.AUTUMN)
    winter = add_season_event(SEASON.WINTER)
    spring = add_season_event(SEASON.SPRING)
    summer = add_season_event(SEASON.SUMMER)

    ##### FULL MOON #####
    full_moon = (
        add_event("Full Moon", REGION.FOREST if PHASE.NIGHT in WHITELIST else REGION.NONE,
            (lambda state: state.has_all({"Full Moon Phase Change", night.event, celestial_orb.event}, player)),
        ) if UNLOCKABLE_SEASON_LOGIC
        else seasons_passed_half
    )

    ##### TOOLS #####
    mining = add_event("Mining", REGION.FOREST,
        ALWAYS_TRUE if not is_locked("Pickaxe")
        else lambda state: state.has_any({"Pickaxe", "Opulent Pickaxe", "Woodie"}, player),
        hide_in_spoiler = True
    )
    chopping = add_event("Chopping", REGION.FOREST,
        ALWAYS_TRUE if not is_locked("Axe")
        else lambda state: state.has_any({"Axe", "Luxury Axe", "Woodie"}, player),
        hide_in_spoiler = True
    )
    hammering = add_event("Hammering", REGION.FOREST,
        ALWAYS_TRUE if not is_locked("Hammer")
        else lambda state: state.has_all({"Hammer", mining.event}, player),
        hide_in_spoiler = True
    )
    bug_catching = add_event("Bug Catching", REGION.FOREST, lambda state: state.has_all({"Bug Net", "Rope"}, player), hide_in_spoiler = True)
    digging = add_event("Digging", REGION.FOREST,
        ALWAYS_TRUE if not is_locked("Shovel")
        else lambda state: state.has_any({"Shovel", "Regal Shovel"}, player),
        hide_in_spoiler = True
    )
    bird_caging = add_event("Bird Caging", REGION.FOREST if PHASE.DAY_OR_DUSK in WHITELIST else REGION.NONE,
        lambda state: state.has_all({"Bird Trap", "Birdcage", "Papyrus", seeds.event}, player)
    )
    ice_staff = add_event("Ice Staff", REGION.FOREST if WEAPON_LOGIC else REGION.NONE,
        lambda state: state.has_all({"Spear", "Rope", "Ice Staff", gem_digging.event}, player)
    )
    fire_staff = add_event("Fire Staff", REGION.FOREST if WEAPON_LOGIC else REGION.NONE,
        lambda state: state.has_all({"Spear", "Rope", "Fire Staff", gem_digging.event, nightmare_fuel.event}, player)
    )
    firestarting = add_event("Firestarting", REGION.FOREST,
        lambda state: (
            state.has_any({"Torch", "Willow", fire_staff.event}, player)
            or state.has_all({"Campfire", chopping.event}, player)
        ),
        hide_in_spoiler = True
    )
    hostile_flare = add_event("Hostile Flare", REGION.MOONQUAY, lambda state: state.has_all({"Flare", "Hostile Flare", mining.event, firestarting.event}, player))
    backpack = add_event("Backpack", REGION.FOREST,
        (
            lambda state: (
                state.has("Backpack", player)
                or (state.has_all({"Piggyback", "Rope", pre_basic_combat.event}, player))
            )
        ) if BACKPACK_LOGIC
        else ALWAYS_TRUE,
        hide_in_spoiler = True
    )
    morning_star = add_event("Morning Star", REGION.FOREST,
        (lambda state: state.has_all({electrical_doodad.event, "Morning Star", ranged_aggression.event, desert_exploration.event, basic_combat.event}, player)),
        hide_in_spoiler = True
    )
    weather_pain = add_event("Weather Pain", REGION.FOREST if WEAPON_LOGIC and "Moose/Goose" in EXISTING_LOCATIONS else REGION.NONE,
        (lambda state: state.has_all({"Weather Pain", moosegoose.event, gears.event}, player)),
        hide_in_spoiler = True
    )
    pick_axe = add_event("Pick/Axe", REGION.DUALREGION if REGION.OCEAN in WHITELIST else REGION.RUINS,
        combine_rules(
            (
                (lambda state: state.has_all({"Pick/Axe", thulecite.event}, player)) if is_locked("Pick/Axe")
                else (lambda state: state.has(ancient_altar.event, player)) if REGION.RUINS in WHITELIST
                else ALWAYS_TRUE # Allow obtaining from ocean region
            ),
            (
                (lambda state: state.has_all({"Opulent Pickaxe", "Luxury Axe"}, player)) if REGION.RUINS in WHITELIST
                else (lambda state: state.has(sunken_chest.event, player)) if REGION.OCEAN in WHITELIST
                else ALWAYS_FALSE # Player probably chose caves but not ruins or ocean
            )
        ),
        hide_in_spoiler = True
    )
    cannon = add_event("Cannon", REGION.MOONQUAY if PHASE.DAY_OR_DUSK in WHITELIST or SEASON.WINTER in WHITELIST else REGION.NONE,
        lambda state: state.has_all({moon_quay_exploration.event, "Cannon Kit", "Gunpowder", "Cut Stone", "Rope", charcoal.event, mining.event, bird_eggs.event}, player),
        hide_in_spoiler = True
    )
    shaving = add_event("Shaving", REGION.FOREST,
        ALWAYS_TRUE if ADVANCED_PLAYER_BIAS and not PEACEFUL_LOGIC
        else lambda state: state.has("Razor", player),
        hide_in_spoiler = True
    )
    telelocator_staff = add_event("Telelocator Staff", REGION.OCEAN if EXPERT_PLAYER_BIAS else REGION.NONE,
        (lambda state: state.has_all({"Telelocator Staff", purple_gem.event, chopping.event}, player)),
        hide_in_spoiler = True
    )
    mooncaller_staff = add_event("Mooncaller Staff",
        (
            REGION.NONE if not "Moon Stone Event" in EXISTING_LOCATIONS
            else REGION.FOREST if is_locked("Deconstruction Staff")
            else REGION.RUINS
        ),
        lambda state: state.has(moon_stone_event.event, player)
    )
    deconstruction_staff = add_event("Deconstruction Staff",
        (
            REGION.FOREST if is_locked("Deconstruction Staff") and SPECIAL_TAGS.RUINS_GEMS in WHITELIST
            else REGION.RUINS
        ),
        (lambda state: state.has_all({"Deconstruction Staff", chopping.event, ruins_gems.event}, player)) if is_locked("Deconstruction Staff")
        else (lambda state: state.has(ancient_altar.event, player)),
        hide_in_spoiler = True
    )
    beekeeper_hat = add_event("Beekeeper Hat", REGION.FOREST,
        (lambda state: state.has("Beekeeper Hat", player)) if WEAPON_LOGIC and "Bee Queen" in EXISTING_LOCATIONS
        else ALWAYS_TRUE,
        hide_in_spoiler = True
    )


    ##### RESOURCES #####
    nightmare_fuel = add_event("Nightmare Fuel", REGION.FOREST,
        combine_rules(
            ALWAYS_TRUE if not WEAPON_LOGIC and not HEALING_LOGIC
            else (lambda state: state.has_all({basic_combat.event, basic_sanity_management.event}, player)),
            (lambda state: state.has("Nightmare Fuel", player)) if LOCKED_INGREDIENTS_LOGIC and is_locked("Nightmare Fuel")
            else ALWAYS_TRUE
        ),
        hide_in_spoiler = True
    )
    gem_digging = add_event("Gem Digging", REGION.FOREST,
        ALWAYS_TRUE if not is_locked("Shovel") and not is_locked("Garland")
        else lambda state: state.has_all({digging.event, basic_sanity_management.event}, player),
        hide_in_spoiler = True
    )
    charcoal = add_event("Charcoal", REGION.FOREST,
        ALWAYS_TRUE if not is_locked("Torch") and not is_locked("Axe")
        else lambda state: state.has_all({chopping.event, firestarting.event}, player),
        hide_in_spoiler = True
    )
    butter = add_event("Butter",
        (
            REGION.FOREST if PHASE.DAY in WHITELIST and SEASON.NONWINTER in WHITELIST
            else REGION.NONE
        ),
        combine_rules(
            lambda state: state.has(butterfly.event, player),
            fraction_of_prog_items_rule(0.5)
        )
    )
    can_get_feathers = add_event("Can Get Feathers", REGION.FOREST,
        (
            ALWAYS_TRUE if not PHASE.DAY_OR_DUSK in WHITELIST # Tumbleweeds
            else (
                lambda state: (
                    state.has_all({"Boomerang", "Boards", charcoal.event}, player)
                    or state.has_any({"Bird Trap", ice_staff.event}, player)
                )
            ) if WEAPON_LOGIC
            else ALWAYS_TRUE if EXPERT_PLAYER_BIAS # Tumbleweeds
            else (lambda state: state.has("Bird Trap", player))
        )
    )
    gears = add_event("Gears", REGION.FOREST,
        ALWAYS_TRUE if EXPERT_PLAYER_BIAS # Tumbleweeds
        else (lambda state: state.has(ruins_exploration.event, player)) if REGION.RUINS in WHITELIST
        else (lambda state: state.has(advanced_combat.event, player))
    )
    ruins_gems = add_event("Ruins Gems", REGION.FOREST if SPECIAL_TAGS.RUINS_GEMS in WHITELIST else REGION.NONE,
        # Yellow, green, orange, and purple gems; Not necessarily from ruins
        lambda state: state.has_any({ruins_exploration.event, dragonfly.event, sunken_chest.event}, player)
    )
    purple_gem = add_event("Purple Gem", REGION.FOREST,
        combine_rules(
            (
                (lambda state: state.has("Purple Gem", player)) if LOCKED_INGREDIENTS_LOGIC
                else ALWAYS_TRUE
            ),
            lambda state: (
                state.has_all({gem_digging.event, "Purple Gem"}, player)
                or state.has(ruins_gems.event, player)
            )
        ),
        hide_in_spoiler = True
    )
    salt_crystals = add_event("Salt Crystals", REGION.OCEAN,
        (lambda state: state.has_all({pre_basic_boating.event, mining.event, basic_combat.event}, player)) if WEAPON_LOGIC
        else lambda state: state.has_all({pre_basic_boating.event, mining.event}, player)
    )
    thulecite = add_event("Thulecite", REGION.DUALREGION if REGION.OCEAN in WHITELIST else REGION.RUINS,
        combine_rules(
            (
                (lambda state: state.has("Thulecite", player)) if LOCKED_INGREDIENTS_LOGIC and is_locked("Thulecite")
                else ALWAYS_TRUE
            ),
            (
                (lambda state: state.has(ruins_exploration.event, player)) if REGION.RUINS in WHITELIST
                else (lambda state: state.has(archive_exploration.event, player)) if REGION.ARCHIVE in WHITELIST
                else (lambda state: state.has(sunken_chest.event, player))
            )
        ),
        hide_in_spoiler = True
    )
    leafy_meat = add_event("Leafy Meat", REGION.FOREST if SPECIAL_TAGS.LEAFY_MEAT in WHITELIST else REGION.NONE,
        either_rule(
            # Lureplants; Might spawn sooner but account for rng
            (lambda state: state.has_all({spring.event, seasons_passed_2.event}, player)) if SEASON.SPRING in WHITELIST
            # Grass Gekkos
            else (lambda state: state.has_all({digging.event, seasons_passed_2.event}, player)) if SEASON.NONWINTER in WHITELIST
            else ALWAYS_FALSE,
            (lambda state: state.has(lunar_island.event, player)) if REGION.OCEAN in WHITELIST # Carrats
            else ALWAYS_FALSE,
            (
                (lambda state: state.has(cave_exploration.event, player)) if ( # Carrats in lunar grotto
                    (ADVANCED_PLAYER_BIAS or not SEASON.NONWINTER in WHITELIST)
                    and REGION.CAVE in WHITELIST
                ) else ALWAYS_FALSE
            )
        )
    )
    electrical_doodad = add_event("Electrical Doodad", REGION.FOREST,
        either_rule(
            (lambda state: state.has_all({"Cut Stone", "Electrical Doodad", mining.event}, player)),
            (lambda state: state.has_any({retinazor.event, spazmatism.event}, player)) if EXPERT_PLAYER_BIAS
            else ALWAYS_FALSE
        )
    )
    bird_eggs = add_event("Bird Eggs", REGION.FOREST if PHASE.DAY_OR_DUSK in WHITELIST or SEASON.WINTER in WHITELIST else REGION.NONE,
        (lambda state: state.has(bird_caging.event, player)) if PHASE.DAY_OR_DUSK in WHITELIST
        else (lambda state: state.has(winter.event, player))
    )
    seeds = add_event("Seeds", REGION.FOREST,
        # From tumbleweeds in a world we can't have birds
        (lambda state: state.has(desert_exploration.event, player)) if not PHASE.DAY_OR_DUSK in WHITELIST or not SEASON.NONWINTER in WHITELIST
        else lambda state: (
            state.has_any({day.event, dusk.event}, player)
            and state.has_any({autumn.event, spring.event, summer.event}, player)
        )
    )


    ##### LOCATIONS WITH SPECIAL RULES #####
    butterfly = add_parent_event("Butterfly",
        (
            REGION.FOREST if PHASE.DAY in WHITELIST and SEASON.NONWINTER in WHITELIST
            else REGION.NONE
        ),
        ALWAYS_TRUE # Butterfly already has day tag
    )
    batilisk = add_parent_event("Batilisk", REGION.CAVE,
        lambda state: (
            state.has_all({pre_basic_combat.event, mining.event}, player)
            and state.has_any({dusk.event, night.event, cave_exploration.event}, player)
        )
    )
    moleworm = add_parent_event("Moleworm", REGION.FOREST,
        (
            lambda state: (
                state.has_any({dusk.event, night.event}, player)
                and state.has(hammering.event, player)
            )
        ) if PHASE.DUSK_OR_NIGHT in WHITELIST and not DAMAGE_BONUSES_IN_WORLD # Hammers will kill moles if player has a damage bonus
        else (lambda state: state.has_all({digging.event, day.event}, player)) if PHASE.DAY in WHITELIST
        else (lambda state: state.has(basic_survival.event, player)) # Can otherwise come from catcoons, tumbleweeds, and caves
    )
    rabbit = add_parent_event("Rabbit", REGION.FOREST,
        lambda state: (
            (
                state.has_any({autumn.event, winter.event, summer.event}, player)
                and state.has(day.event, player)
            ) or state.has_any({digging.event, cave_exploration.event}, player)
        )
    )
    canary = add_parent_event("Canary",
        (
            REGION.FOREST if PHASE.DAY_OR_DUSK in WHITELIST and FARMPLANT_SEASON_RULES["Pumpkin"] != ALWAYS_FALSE
            else REGION.NONE
        ),
        lambda state: state.has_all({"Friendly Scarecrow", "Boards", pumpkin_farming.event}, player)
    )


    ##### COMBAT #####
    basic_combat = add_event("Basic Combat", REGION.FOREST,
        (
            lambda state: (
                (
                    state.has_all({"Rope", "Spear"}, player)
                    # or state.has("Wigfrid", player) # TODO: character logic
                )
                and state.has_any({"Log Suit", "Football Helmet"}, player)
                and state.has(chopping.event, player) # Wood for the log suit, or at least a weapon before you get the spear
            )
        ) if WEAPON_LOGIC else ALWAYS_TRUE
    )
    pre_basic_combat = add_event("Pre-Basic Combat", REGION.FOREST,
        ALWAYS_TRUE if not is_locked("Axe") and not is_locked("Grass Suit")
        else (
            lambda state: (
                state.has_all({"Grass Suit", chopping.event}, player) # Axe as a weapon
                or state.has_any({basic_combat.event, "Wendy", "Wigfrid"}, player) # TODO: character logic
            )
        ) if WEAPON_LOGIC else ALWAYS_TRUE,
        hide_in_spoiler = True
    )
    advanced_combat = add_event("Advanced Combat", REGION.FOREST,
        (
            lambda state: (
                state.has_all({basic_combat.event, "Log Suit", "Football Helmet"}, player) # Both armor pieces
                and (
                    state.has("Ham Bat", player)
                    or state.has_all({"Dark Sword", nightmare_fuel.event}, player)
                    or state.has_all({"Glass Cutter", "Boards"}, player)
                )
                and (ADVANCED_PLAYER_BIAS or state.has(base_making.event, player))
            )
        ) if WEAPON_LOGIC else ALWAYS_TRUE
    )
    advanced_boss_combat = add_event("Advanced Boss Combat", REGION.FOREST,
        lambda state: state.has_all({advanced_combat.event, quick_healing.event, year_round_survival.optional_event}, player)
    )
    epic_combat = add_event("Epic Combat", REGION.FOREST,
        (lambda state: state.has(advanced_boss_combat.event, player)) if EXPERT_PLAYER_BIAS
        else lambda state: state.has_all({
            advanced_boss_combat.event,
            speed_boost.optional_event,
            arena_building.optional_event,
            character_switching.optional_event,
            resurrecting.optional_event
        }, player)
    )
    ranged_combat = add_event("Ranged Combat",
        (
            REGION.FOREST if (
                not WEAPON_LOGIC
                or (
                    PHASE.DAY_OR_DUSK in WHITELIST
                    and (SEASON.WINTER in WHITELIST or FARMPLANT_SEASON_RULES["Pumpkin"] != ALWAYS_FALSE)
                )
            )
            else REGION.NONE
        ),
        (
            either_rule(
                (lambda state: state.has_all({can_get_feathers.event, winter.event, "Blow Dart"}, player))
                if SEASON.WINTER in WHITELIST else ALWAYS_FALSE,
                # Poisoned canary logic
                lambda state: state.has_all({can_get_feathers.event, canary.event, "Electric Dart", bird_caging.optional_event, cave_exploration.optional_event}, player)
            )
        ) if WEAPON_LOGIC
        else ALWAYS_TRUE
        # TODO: Walter logic
    )
    ranged_aggression = add_event("Ranged Aggression", REGION.FOREST,
        either_rule(
            lambda state: state.has_all({"Boomerang", "Boards", charcoal.event}, player),
            (
                lambda state: (
                    state.has_all({can_get_feathers.event, "Sleep Dart"}, player)
                    or state.has_all({can_get_feathers.event, "Fire Dart", charcoal.event}, player)
                )
            ) if PHASE.DAY_OR_DUSK in WHITELIST
            else ALWAYS_FALSE,
            lambda state: state.has_any({ranged_combat.event, ice_staff.event, fire_staff.event, cannon.event}, player)
            # TODO: Walter logic
        ) if WEAPON_LOGIC else ALWAYS_TRUE
    )
    dark_magic = add_event("Dark Magic", REGION.FOREST,
        combine_rules(
            (lambda state: state.has_all({nightmare_fuel.event, basic_sanity_management.event}, player)),
            (
                lambda state: (
                    state.has("Dark Sword", player)
                    or (state.has_all({"Bat Bat", purple_gem.event, batilisk.event}, player))
                    or state.has_all({"Papyrus", "Night Armor"}, player)
                )
            ) if WEAPON_LOGIC else ALWAYS_TRUE
        )
    )


    ##### HEALING #####
    basic_sanity_management = add_event("Basic Sanity Management", REGION.FOREST,
        # TODO: Walter doesn't get sanity from fashion
        (lambda state: state.has_any({"Top Hat", "Garland", "Fashion Goggles", slow_healing.event}, player)) if HEALING_LOGIC
        else ALWAYS_TRUE
    )
    nonperishable_quick_healing = add_event("Nonperishable Quick Healing", REGION.FOREST,
        either_rule(
            lambda state: (
                state.has_all({"Healing Salve", firestarting.event, mining.event}, player) # Ash and rocks
                or state.has_all({"Honey Poultice", "Papyrus", honey_farming.event}, player)
            ),
            (lambda state: state.has_all({"Bat Bat", purple_gem.event, batilisk.event}, player)) if WEAPON_LOGIC
            else ALWAYS_FALSE
        ) if HEALING_LOGIC
        else ALWAYS_TRUE
    )
    quick_healing = add_event("Quick Healing", REGION.FOREST,
        (lambda state: state.has_any({cooking.event, nonperishable_quick_healing.event}, player)) if HEALING_LOGIC # TODO: Wormwood can't heal from food
        else ALWAYS_TRUE,
        hide_in_spoiler = True
    )
    slow_healing = add_event("Slow Healing", REGION.FOREST,
        # TODO: Wickerbottom can't sleep
        either_rule(
            lambda state: (
                state.has_all({"Tent", "Rope"}, player)
                or state.has_all({"Siesta Lean-to", "Rope", "Boards", chopping.event}, player)
            ),
            lambda state: state.has_all({"Rope", "Straw Roll", "Fur Roll", mining.event, basic_combat.event}, player) if REGION.CAVE in WHITELIST
            else ALWAYS_FALSE
        ) if HEALING_LOGIC
        else ALWAYS_TRUE,
        hide_in_spoiler = True
    )
    healing = add_event("Healing", REGION.FOREST,
        (
            lambda state: (
                state.has_all({"Booster Shot", basic_sanity_management.event}, player)
                and state.has_any({quick_healing.event, slow_healing.event}, player)
            )
        ) if HEALING_LOGIC
        else (lambda state: state.has("Booster Shot", player)) if EXPERT_PLAYER_BIAS
        else (lambda state: state.has_all({"Booster Shot", basic_sanity_management.event}, player))
    )
    resurrecting = add_event("Resurrecting", REGION.FOREST,
        (lambda state:
            state.has_all({"Life Giving Amulet", gem_digging.event, nightmare_fuel.event}, player)
            or state.has_all({"Meat Effigy", "Boards", chopping.event, healing.event}, player)
        ) if HEALING_LOGIC
        else ALWAYS_TRUE
    )


    ##### SURVIVAL #####
    basic_survival = add_event("Basic Survival", REGION.FOREST,
        # Ignore basic survival in favor of having a sphere 1 with creature locations off
        ALWAYS_TRUE if not CREATURE_LOCATIONS_ENABLED or (PEACEFUL_LOGIC and is_locked("Torch") and is_locked("Axe"))
        else combine_rules(
            # Have a way to survive the night
            (
                ALWAYS_TRUE if not PHASE.NIGHT in WHITELIST
                else (
                    lambda state: (
                        state.has(firestarting.event, player)
                        or state.has_all({"Straw Roll", "Rope"}, player)
                    )
                ) if EXPERT_PLAYER_BIAS
                else (
                    lambda state: (
                        state.has(firestarting.event, player)
                        and state.has_any({"Axe", "Pickaxe"}, player) # Have a flint tool at least
                    )
                )
            ),
            # Winter/Spring start
            (lambda state: state.has(firestarting.event, player)) if STARTING_SEASON == SEASON.WINTER or STARTING_SEASON == SEASON.SPRING
            # Summer start
            else (
                lambda state: (
                    state.has_all({"Endothermic Fire", mining.event}, player)
                    or state.has_any({"Straw Hat", "Umbrella", "Pretty Parasol", "Whirly Fan"}, player)
                )
            ) if SEASON_GEAR_LOGIC and STARTING_SEASON == SEASON.SUMMER
            # Autumn start
            else ALWAYS_TRUE
        )
    )
    thermal_stone = add_event("Thermal Stone", REGION.FOREST, lambda state: state.has_all({"Thermal Stone", "Pickaxe"}, player), hide_in_spoiler = True)
    winter_survival = add_event("Can Survive Winter", REGION.FOREST,
        combine_rules(
            lambda state: state.has(basic_survival.event, player),
            (
                lambda state: (
                    state.has_all({firestarting.event, shaving.event, thermal_stone.event, "Rabbit Earmuffs", "Pickaxe"}, player)
                    and state.has_any({"Puffy Vest", "Beefalo Hat", "Winter Hat", "Cat Cap"}, player)
                    and state.has_any({"Campfire", "Fire Pit"}, player)
                )
            ) if SEASON_GEAR_LOGIC
            else (lambda state: state.has(firestarting.event, player))
        )
    )
    electric_insulation = add_event("Electric Insulation", REGION.FOREST,
        either_rule(
            (
                lambda state: (
                    state.has_all({"Rain Coat", "Rope", hammering.event}, player) # Bones
                    or state.has_all({"Rain Hat", "Straw Hat", moleworm.event}, player)
                )
            ),
            (lambda state: state.has_all({"Eyebrella", deerclops.event, hammering.event}, player)) if "Deerclops" in EXISTING_LOCATIONS
            else ALWAYS_FALSE
        )
    )
    lightning_rod = add_event("Lightning Rod", REGION.FOREST if SEASON_GEAR_LOGIC else REGION.NONE,
        lambda state: (
            state.has_all({"Lightning Rod", "Cut Stone"}, player)
            or state.has_all({"Lightning Conductor", "Mast Kit", "Rope", "Boards"}, player)
        ),
        hide_in_spoiler = True
    )
    spring_survival = add_event("Can Survive Spring", REGION.FOREST,
        combine_rules(
            lambda state: state.has(basic_survival.event, player),
            (
                lambda state: (
                    state.has_any({electric_insulation.event, "Umbrella"}, player)
                    and state.has_all({"Straw Hat", "Pretty Parasol", lightning_rod.event}, player) # Ensure basic stuff at this point
                )
            ) if SEASON_GEAR_LOGIC
            else ALWAYS_TRUE
        )
    )
    has_cooling_source = add_event("Has Cooling Source", REGION.FOREST if SEASON_GEAR_LOGIC else REGION.NONE, lambda state:
        state.has_all({thermal_stone.event, "Ice Box", "Cut Stone"}, player)
        or state.has_any({"Endothermic Fire", "Chilled Amulet"}, player)
        or state.has_all({"Endothermic Fire Pit", electrical_doodad.event}, player)
    )
    has_summer_insulation = add_event("Has Summer Insulation", REGION.FOREST if SEASON_GEAR_LOGIC else REGION.NONE,
        either_rule(
            (
                lambda state: (
                    state.has_any({"Umbrella", "Summer Frest", thermal_stone.event}, player)
                    or state.has_all({"Floral Shirt", "Papyrus"}, player)
                )
            ),
            (lambda state: state.has_all({"Eyebrella", deerclops.event, hammering.event}, player)) if "Deerclops" in EXISTING_LOCATIONS
            else ALWAYS_FALSE
        )
    )
    fire_suppression = add_event("Fire Suppression", REGION.FOREST, lambda state:
        False if not state.has(base_making.event, player)
        else (
            state.has_all({gears.event, "Ice Flingomatic"}, player)
            or state.has_all({"Luxury Fan", moosegoose.event}, player)
            or state.has("Empty Watering Can", player)
        )
    )
    summer_survival = add_event("Can Survive Summer", REGION.FOREST,
        combine_rules(
            lambda state: state.has(basic_survival.event, player),
            (
                lambda state: state.has_all({has_cooling_source.event, has_summer_insulation.event, fire_suppression.event, "Straw Hat", "Pretty Parasol", "Whirly Fan"}, player)
            ) if SEASON_GEAR_LOGIC
            else ALWAYS_TRUE
        )
    )
    year_round_survival = add_event(
        "Seasonal Stability" if UNLOCKABLE_SEASON_LOGIC else "Can Survive All Seasons",
        REGION.FOREST if SEASON_GEAR_LOGIC else REGION.NONE,
        either_rule(
            combine_rules(
                (lambda state: state.has(winter_survival.event, player)) if SEASON.WINTER in WHITELIST else ALWAYS_TRUE,
                (lambda state: state.has(spring_survival.event, player)) if SEASON.SPRING in WHITELIST else ALWAYS_TRUE,
                (lambda state: state.has(summer_survival.event, player)) if SEASON.SUMMER in WHITELIST else ALWAYS_TRUE
            ),
            (lambda state: state.has_all({basic_survival.event, autumn.event}, player)) if UNLOCKABLE_SEASON_LOGIC
            else ALWAYS_FALSE
        ),
        hide_in_spoiler = True
    )


    ##### BASE MAKING #####
    base_making = add_event("Base Making", REGION.FOREST,
        combine_rules(
            (lambda state: state.has_all({"Boards", "Cut Stone", "Electrical Doodad", "Rope", chopping.event, mining.event}, player)),
            (
                (lambda state: state.has_all({"Chest", "Ice Box", "Fire Pit"}, player)) if BASE_MAKING_LOGIC
                else ALWAYS_TRUE
            )
        )
    )
    fencing = add_event("Fencing", REGION.FOREST,
        (
            lambda state: (
                state.has_all({base_making.event, "Wood Gate and Fence"}, player)
                and state.has_any({"Hay Wall", "Wood Wall", "Stone Wall"}, player)
            )
        ) if BASE_MAKING_LOGIC else ALWAYS_TRUE,
        hide_in_spoiler = True
    )
    beefalo_domestication = add_event("Beefalo Domestication", REGION.FOREST,
        combine_rules(
            (lambda state: state.has_all({"Saddle", "Beefalo Hat", "Beefalo Bell"}, player)),
            (
                (lambda state: state.has(fencing.event, player)) if BASE_MAKING_LOGIC
                else ALWAYS_TRUE
            )
        )
    )
    heavy_lifting = add_event("Heavy Lifting", REGION.FOREST, lambda state:
        state.has(beefalo_domestication.event, player)
        # or state.has_any({"Walter", "Wolfgang"}, player) # Woby, mightiness # TODO: character logic
        # or state.has_all({"Wanda", winter.event, purple_gem.event}, player) # Rift Watch # TODO: character logic
    )
    arena_building = add_event("Arena Building", REGION.FOREST,
        (
            lambda state: (
                (
                    state.has_any({"Pitchfork", "Snazzy Pitchfork"}, player)
                    or state.has_all({antlion.event, "Turf-Raiser Helm", shaving.event}, player)
                )
                and (
                    state.has_all({"Floorings", "Cut Stone", mining.event}, player)
                    # or state.has("Wurt", player) # TODO: character logic
                )
            )
        ) if BASE_MAKING_LOGIC
        else ALWAYS_TRUE
    )
    character_switching = add_event("Character Switching", REGION.FOREST,
        combine_rules(
            (lambda state: state.has_all({"Cratered Moonrock", "Boards", "Rope", purple_gem.event}, player)), # Crafting ingredients for moonrock portal
            (
                ALWAYS_TRUE if is_locked("Moon Rock Idol") and is_locked("Portal Paraphernalia")
                else (lambda state: state.has(celestial_orb.event, player)) # If either aren't shuffled, you'd have to make it at the celestial orb
            ),
            (lambda state: state.has("Moon Rock Idol", player)) if is_locked("Moon Rock Idol") else ALWAYS_TRUE,
            (lambda state: state.has("Portal Paraphernalia", player)) if is_locked("Portal Paraphernalia") else ALWAYS_TRUE
        ) if CHARACTER_SWITCHING_LOGIC
        else ALWAYS_TRUE
    )
    wall_building = add_event("Wall Building", REGION.FOREST,
        either_rule(
            (lambda state: state.has_all({base_making.event, "Stone Wall", "Potter's Wheel"}, player)), # Sculptures can make good walls
            (
                ALWAYS_FALSE if not ADVANCED_PLAYER_BIAS
                else (lambda state: state.has_all({"Thulecite Wall", thulecite.event}, player)) if is_locked("Thulecite Wall")
                else (lambda state: state.has_all({ancient_altar.event, thulecite.event}, player)) # Can otherwise make walls at ancient altar
            )
        )
    )


    ##### EXPLORATION #####
    basic_exploration = add_event("Basic Exploration", REGION.FOREST,
        ALWAYS_TRUE if EXPERT_PLAYER_BIAS
        else lambda state: state.has_all({
            "Telltale Heart",
            "Torch",
            "Campfire",
            basic_survival.event,
            backpack.event,
            chopping.event,
            mining.event,
            seasons_passed_half.event
        }, player)
    )
    desert_exploration = add_event("Desert Exploration", REGION.FOREST,
        ALWAYS_TRUE if ADVANCED_PLAYER_BIAS
        else (lambda state: state.has_all({basic_survival.event, pre_basic_combat.event}, player)),
        hide_in_spoiler = True
    )
    swamp_exploration = add_event("Swamp Exploration", REGION.FOREST,
        ALWAYS_TRUE if ADVANCED_PLAYER_BIAS
        else (lambda state: state.has_all({basic_survival.event, healing.event}, player)),
        hide_in_spoiler = True
    )
    advanced_exploration = basic_exploration if ADVANCED_PLAYER_BIAS else add_event("Advanced Exploration", REGION.FOREST,
        lambda state: state.has_all({basic_exploration.event, speed_boost.optional_event, digging.event, hammering.event}, player),
        hide_in_spoiler = True
    )
    speed_boost = add_event("Speed Boost",
        (
            REGION.FOREST if SEASON.WINTER in WHITELIST
            else REGION.DUALREGION if REGION.OCEAN in WHITELIST else REGION.RUINS if is_locked("Magiluminescence")
            else REGION.RUINS,
        ),
        either_rule(
            (lambda state: state.has_all({"Walking Cane", winter.event}, player)) if SEASON.WINTER in WHITELIST
            else ALWAYS_FALSE,
            (
                ALWAYS_FALSE if not ADVANCED_PLAYER_BIAS and SEASON.WINTER in WHITELIST # Encourage getting walking cane for easy difficulty
                else (lambda state: state.has_all({thulecite.event, ruins_gems.event, nightmare_fuel.event, "Magiluminescence"}, player)) if is_locked("Magiluminescence")
                else (lambda state: state.has(ancient_altar.event, player))
            )
        )
    )
    light_source = add_event("Light Source", REGION.FOREST,
        (
            either_rule (
                (
                    (lambda state: state.has_all({"Lantern", "Rope", mining.event}, player)) if REGION.CAVE in WHITELIST
                    else (lambda state: state.has_all({"Lantern", "Rope", sea_fishing.event}, player)) # Skittersquids
                ),
                lambda state: (
                    state.has_all({"Miner Hat", bug_catching.event, "Straw Hat"}, player)
                    or (ADVANCED_PLAYER_BIAS and state.has(morning_star.event, player))
                )
            )
        ) if LIGHTING_LOGIC
        else (lambda state: state.has("Torch", player))
    )
    cave_exploration = add_event("Cave Exploration", REGION.CAVE,
        combine_rules(
            (lambda state: state.has_all({mining.event, light_source.event}, player)) if EXPERT_PLAYER_BIAS # Expert players just get a torch and pickaxe
            else (lambda state: state.has_all({light_source.event, basic_exploration.event, base_making.event}, player)), # Have a base, backpack, and tools at this point
            # Have either good weather or rain protection
            (lambda state: state.has_any({autumn.event, summer.event, "Umbrella", electric_insulation.event}, player))
            if SEASON_GEAR_LOGIC and (SEASON.WINTER in WHITELIST or SEASON.SPRING in WHITELIST)
            else ALWAYS_TRUE
        )
    )
    ruins_exploration = add_event("Ruins Exploration", REGION.RUINS,
        (lambda state: state.has(cave_exploration.event, player)) if EXPERT_PLAYER_BIAS
        else combine_rules(
            (
                lambda state: (
                    state.has_all({cave_exploration.event, advanced_combat.event}, player)
                    or state.has_all({cave_exploration.event, healing.event, basic_combat.event}, player)
                )
            ),
            (lambda state: state.has(cooking.event, player)) if BASE_MAKING_LOGIC # Allow cooking for easy difficulty
            else ALWAYS_TRUE
        )
    )
    basic_boating = add_event("Basic Boating", REGION.OCEAN, lambda state:
        state.has_all({basic_exploration.event, "Boat Kit", "Boards", "Oar", "Grass Raft Kit", "Boat Patch"}, player)
        and state.has_any({light_source.event, day.event, dusk.event}, player)
    )
    pre_basic_boating = basic_boating if not EXPERT_PLAYER_BIAS else add_event("Pre-Basic Boating", REGION.OCEAN,
        ALWAYS_TRUE if not is_locked("Oar") and not is_locked("Grass Raft Kit") # TODO: Check for day and dusk if they become AP items too
        else lambda state: (
            state.has_any({"Oar", "Driftwood Oar"}, player)
            and (
                state.has("Grass Raft Kit", player)
                or state.has_all({"Boat Kit", "Boards", chopping.event}, player)
            )
            and state.has_any({light_source.event, day.event, dusk.event}, player)
        )
    )
    advanced_boating = add_event("Advanced Boating", REGION.OCEAN,
        combine_rules(
            (lambda state: state.has_all({"Driftwood Oar", basic_boating.event, light_source.event, base_making.event}, player)),
            (
                ALWAYS_TRUE if EXPERT_PLAYER_BIAS
                else lambda state: state.has_all({"Anchor Kit", "Steering Wheel Kit", "Mast Kit"}, player)
            )
        )
    )
    can_reach_islands = add_event("Can Reach Islands", REGION.OCEAN,
        either_rule(
            (
                (lambda state: state.has(telelocator_staff.event, player)) if EXPERT_PLAYER_BIAS
                else ALWAYS_FALSE
            ),
            (
                (lambda state: state.has(pre_basic_boating.event, player)) if ADVANCED_PLAYER_BIAS
                else lambda state: state.has(advanced_boating.event, player)
            )
            # TODO: Weregoose logic here
        )
    )
    lunar_island = can_reach_islands
    hermit_island = add_event("Hermit Island", REGION.OCEAN, lambda state: state.has_all({base_making.event, can_reach_islands.event}, player))
    hermit_sea_quests = add_event("Hermit Sea Quests", REGION.OCEAN,
        (lambda state: state.has(sea_fishing.event, player)) if ADVANCED_PLAYER_BIAS
        else lambda state: state.has_all({sea_fishing.event, advanced_boating.event}, player)
    )
    archive_exploration = add_event("Archive Exploration", REGION.ARCHIVE, lambda state: state.has_all({iridescent_gem.event, healing.event}, player))
    storm_protection = add_event("Storm Protection", REGION.FOREST if SEASON.SUMMER in WHITELIST else REGION.MOONSTORM,
        either_rule(
            (lambda state: state.has_all({"Fashion Goggles", "Desert Goggles"}, player)) if SEASON.SUMMER in WHITELIST
            else ALWAYS_FALSE,
            (
                lambda state: (
                    state.has("Astroggles", player) and (
                        EXPERT_PLAYER_BIAS # Digging potato from junk pile
                        or state.has(potato_farming.event, player) # Farming potato
                    )
                )
            ) if REGION.MOONSTORM in WHITELIST
            else ALWAYS_FALSE
        )
    )
    moonstorm_exploration = add_event("Moonstorm Exploration", REGION.MOONSTORM,
        lambda state: state.has_all({unite_celestial_altars.event, storm_protection.event, electric_insulation.event}, player) # Moonstorms have started; Moongleams
    )
    moon_quay_exploration = can_reach_islands if EXPERT_PLAYER_BIAS else add_event("Moon Quay Exploration", REGION.MOONQUAY,
        (lambda state: state.has_all({can_reach_islands.event, ruins_exploration.event}, player)) if REGION.RUINS in WHITELIST # Encourage getting bananas from ruins, if enabled
        else (lambda state: state.has(can_reach_islands.event, player))
    )
    can_defend_against_pirates = add_event("Can Defend Against Pirates", REGION.MOONQUAY,
        ALWAYS_TRUE if EXPERT_PLAYER_BIAS
        else lambda state: state.has_all({cannon.optional_event, basic_combat.event}, player),
        hide_in_spoiler = True
    )
    pirate_map = add_event("Pirate Map", REGION.MOONQUAY, lambda state:
        state.has_all({can_defend_against_pirates.event, moon_quay_exploration.event, hostile_flare.event, pre_basic_boating.event}, player)
    )
    sunken_chest = add_event("Sunken Chest", REGION.OCEAN, lambda state:
        state.has_all({"Pinchin' Winch", advanced_boating.event}, player)
        and state.has_any({hammering.event, deconstruction_staff.event}, player)
    )


    ##### FARMING #####
    basic_farming = add_event("Basic Farming", REGION.FOREST,
        lambda state: (
            state.has_all({seasons_passed_1.event, seeds.event}, player) and (
                state.has("Wormwood", player) or ( # Wormwood can plant directly on the ground
                    state.has_any({"Garden Hoe", "Splendid Garden Hoe"}, player)
                    and state.has_all({"Garden Digamajig", "Rope", "Boards", chopping.event, digging.event}, player)
                )
            )
        )
    )
    advanced_farming = add_event("Advanced Farming", REGION.FOREST, lambda state:
        # Implied you have chopping, rope, and boards already
        state.has_any({"Wormwood", "Garden Hoe", "Splendid Garden Hoe"}, player)
        and state.has_all({"Garden Digamajig", "Empty Watering Can", base_making.event, digging.event, seasons_passed_1.event, seeds.event}, player)
         # TODO: Wes can't talk to plants
    )
    asparagus_farming = add_farming_event("Asparagus")
    garlic_farming = add_farming_event("Garlic")
    pumpkin_farming = add_farming_event("Pumpkin")
    corn_farming = add_farming_event("Corn",
        (lambda state: state.has(basic_farming.event, player)) if EXPERT_PLAYER_BIAS # Catcoons
        else None if not (PHASE.DAY_OR_DUSK in WHITELIST and SPECIAL_TAGS.CORN in WHITELIST)
        else (lambda state: state.has_all({basic_farming.event, bird_caging.event, sea_fishing.event}, player)) if ADVANCED_PLAYER_BIAS # Corn cod
        else None
    )
    onion_farming = add_farming_event("Onion")
    potato_farming = add_farming_event("Potato",
        None if not PHASE.DAY_OR_DUSK in WHITELIST
        else (lambda state: state.has_all({basic_farming.event, bird_caging.event}, player)) if ADVANCED_PLAYER_BIAS # Junk pile
        else None
    )
    dragonfruit_farming = add_farming_event("Dragon Fruit",
        None if not (PHASE.DAY_OR_DUSK in WHITELIST and REGION.OCEAN in WHITELIST)
        else (lambda state: state.has_all({basic_farming.event, dragonfruit_from_saladmander.event, bird_caging.event}, player)) if ADVANCED_PLAYER_BIAS # Saladmander
        else None
    )
    pomegranate_farming = add_farming_event("Pomegranate")
    eggplant_farming = add_farming_event("Eggplant")
    tomaroot_farming = add_farming_event("Toma Root",
        (lambda state: state.has(basic_farming.event, player)) if EXPERT_PLAYER_BIAS else None # Catcoons
    )
    watermelon_farming = add_farming_event("Watermelon")
    pepper_farming = add_farming_event("Pepper")
    durian_farming = add_farming_event("Durian")
    carrot_farming = add_farming_event("Carrot",
        None if not PHASE.DAY_OR_DUSK in WHITELIST
        else (lambda state: state.has_all({basic_farming.event, bird_caging.event}, player))
    )
    honey_farming = add_event("Honey Farming", REGION.FOREST,
        (
            lambda state: (
                state.has_all({"Bee Box", "Boards", bug_catching.event, day.event}, player)
                and state.has_any({autumn.event, spring.event, summer.event}, player)
            )
        ) if BASE_MAKING_LOGIC and PHASE.DAY in WHITELIST and SEASON.NONWINTER in WHITELIST
        else ALWAYS_TRUE # Getting honey directly from beehives
    )


    ##### COOKING #####
    cooking = add_event("Cooking", REGION.FOREST,
        ALWAYS_TRUE if WARLY_DISHES_ENABLED
        else lambda state: state.has_all({"Cut Stone", "Crock Pot", charcoal.event, mining.event}, player)
    )
    fruits = add_event("Fruits", REGION.FOREST if SPECIAL_TAGS.FRUITS in WHITELIST else REGION.NONE,
        lambda state: state.has_any({pomegranate_farming.event, watermelon_farming.event, durian_farming.event, ruins_exploration.event}, player)
    )
    dragonfruit_from_saladmander = add_event("Dragon Fruit from Saladmander", REGION.OCEAN,
        combine_rules(
            (lambda state: state.has_all({lunar_island.event, basic_combat.event}, player)),
            (lambda state: state.has("Bath Bomb", player)) if is_locked("Bath Bomb")
            else ALWAYS_TRUE
        )
    )
    dairy = add_event("Dairy", REGION.FOREST,
        lambda state: (
            state.has(eye_of_terror.event, player) # Milky whites
            or ( # Electric milk
                state.has_all({morning_star.event, electric_insulation.event}, player)
                or state.has_all({canary.event, can_get_feathers.event, "Electric Dart"}, player)
            )
        )
    )


    ##### FISHING #####
    freshwater_fishing = add_event("Freshwater Fishing", REGION.FOREST if SEASON.NONWINTER in WHITELIST else REGION.CAVE,
        lambda state: state.has("Freshwater Fishing Rod", player) and state.has_any({autumn.event, spring.event, summer.event, cave_exploration.event}, player)
    )
    sea_fishing = add_event("Sea Fishing", REGION.OCEAN,
        combine_rules(
            (
                lambda state: (
                    state.has_all({pre_basic_boating.event, "Rope", "Boards"}, player)
                    and state.has_any({"Ocean Trawler Kit", "Sea Fishing Rod"}, player)
                )
            ),
            (
                (lambda state: state.has_all({"Tin Fishin' Bin", "Cut Stone", "Rope"}, player)) if BASE_MAKING_LOGIC
                else ALWAYS_TRUE
            )
        )
    )
    fishing = add_event("Fishing", REGION.FOREST,
        (lambda state: state.has_any({freshwater_fishing.event, sea_fishing.event}, player)) if SEASON.NONWINTER in WHITELIST or REGION.DUALREGION in WHITELIST
        else (lambda state: state.has_all({swamp_exploration.event, basic_combat.event}, player)), # Merms
        hide_in_spoiler = True
    )


    ##### KEY ITEMS #####
    celestial_sanctum_pieces = add_event("Celestial Sanctum Pieces", REGION.MOONSTORM,
        lambda state: state.has_all({thulecite.event, "Astral Detector", heavy_lifting.event}, player)
    )
    moon_stone_event = add_parent_event("Moon Stone Event",
        (
            REGION.NONE if not "Moon Stone Event" in EXISTING_LOCATIONS
            else REGION.FOREST if is_locked("Star Caller's Staff")
            else REGION.RUINS
        ),
        combine_rules(
            lambda state: state.has_all({nightmare_fuel.event, full_moon.event}, player),
            (
                (lambda state: state.has(wall_building.event, player)) if BASE_MAKING_LOGIC
                else ALWAYS_TRUE
            ),
            (
                (lambda state: state.has_all({ruins_gems.event, "Star Caller's Staff"}, player)) if is_locked("Star Caller's Staff")
                else (lambda state: state.has(ancient_altar.event, player))
            )
        )
    )
    iridescent_gem = add_event("Iridescent Gem",
        (
            REGION.NONE if not "Moon Stone Event" in EXISTING_LOCATIONS
            else REGION.FOREST if is_locked("Deconstruction Staff")
            else REGION.RUINS
        ),
        (lambda state: state.has_all({mooncaller_staff.event, deconstruction_staff.event}, player)) if is_locked("Deconstruction Staff")
        else (lambda state: state.has(mooncaller_staff.event, player)) # Should already be able to craft Deconstruction Staff
    )
    unite_celestial_altars = add_event("Unite Celestial Altars", REGION.MOONSTORM, lambda state:
        state.has_all({lunar_island.event, celestial_sanctum_pieces.event, inactive_celestial_tribute.event, "Pinchin' Winch"}, player)
    )
    inactive_celestial_tribute = add_event("Inactive Celestial Tribute", REGION.MOONSTORM,
        lambda state: state.has(crab_king.event, player)
    )
    shadow_atrium = add_event("Shadow Atrium", REGION.RUINS if "Ancient Fuelweaver" in EXISTING_LOCATIONS else REGION.NONE,
        (lambda state: state.has_all({"Bishop Figure Sketch", "Rook Figure Sketch", "Knight Figure Sketch", shadow_pieces.event}, player)) if CHESSPIECE_ITEMS_SHUFFLED
        else (lambda state: state.has(shadow_pieces.event, player))
    )
    ancient_key = add_event("Ancient Key", REGION.RUINS if "Ancient Fuelweaver" in EXISTING_LOCATIONS else REGION.NONE,
        lambda state: state.has(ancient_guardian.event, player)
    )


    ##### CRAFTING STATIONS #####
    science_machine = add_event("Science Machine", REGION.FOREST, lambda state: state.has_all({basic_survival.event, chopping.event, mining.event}, player))
    alchemy_engine = add_event("Alchemy Engine", REGION.FOREST, lambda state: state.has_all({base_making.event, science_machine.event}, player))
    prestihatitor = add_event("Prestihatitor", REGION.FOREST, lambda state: state.has_all({"Top Hat", "Boards", science_machine.event, "Trap", rabbit.event}, player))
    shadow_manipulator = add_event("Shadow Manipulator", REGION.FOREST, lambda state: state.has_all({purple_gem.event, nightmare_fuel.event, prestihatitor.event}, player))
    think_tank = add_event("Think Tank", REGION.OCEAN, lambda state: state.has_all({"Boards", science_machine.event}, player))
    ancient_altar = add_event("Ancient Pseudoscience Station", REGION.RUINS, lambda state: state.has(ruins_exploration.event, player))
    celestial_orb = add_event("Celestial Orb", REGION.FOREST, lambda state: state.has_all({basic_survival.event, mining.event, seasons_passed_1.optional_event}, player))
    celestial_altar = add_event("Celestial Altar", REGION.OCEAN, lambda state:
        state.has(lunar_island.event, player)
        and (
            state.has(mining.event, player)
            # or state.has(celestial_sanctum_pieces.event, player) TODO: key item logic
            # or state.has(inactive_celestial_tribute.event, player)
        )
    )

    ##### BOSSES #####
    crab_king = add_boss_event("Crab King", REGION.OCEAN, lambda state:
        state.has_all({advanced_boating.event, advanced_boss_combat.event}, player)
        and state.count("Crabby Hermit Friendship", player) >= 10
    )
    shadow_pieces = add_event("Shadow Pieces", REGION.FOREST if PHASE.NIGHT in WHITELIST else REGION.NONE,
        combine_rules(
            lambda state: (
                state.has_all({advanced_boss_combat.event, heavy_lifting.event, base_making.event, "Potter's Wheel", arena_building.event, night.event}, player)
            ),
            (lambda state: state.has_all({"New Moon Phase Change", celestial_orb.event}, player)) if UNLOCKABLE_SEASON_LOGIC
            else ALWAYS_TRUE
        )
    )
    ancient_guardian = add_boss_event("Ancient Guardian", REGION.RUINS, lambda state: state.has_all({ruins_exploration.event, advanced_boss_combat.event}, player))
    deerclops = add_boss_event("Deerclops", REGION.FOREST, lambda state: state.has(basic_combat.event, player))
    moosegoose = add_boss_event("Moose/Goose", REGION.FOREST,
        # Spring is in the tags already. Moose/Goose needs seasons to change at all to spawn
        lambda state: state.has(basic_combat.event, player) and state.has_any({autumn.event, winter.event, summer.event}, player)
    )
    antlion = add_boss_event("Antlion", REGION.FOREST,
        either_rule(
            (lambda state: state.has_all({"Freshwater Fishing Rod", "Fashion Goggles", "Desert Goggles"}, player)), # Affects chance of fishing beach toy
            ALWAYS_FALSE if PEACEFUL_LOGIC
            else (lambda state: state.has_all({advanced_boss_combat.event, thermal_stone.event, storm_protection.event}, player)) # Minimum for expert difficulty
        )
    )
    bearger = add_boss_event("Bearger", REGION.FOREST, lambda state: state.has(basic_combat.event, player))
    dragonfly = add_boss_event("Dragonfly", REGION.FOREST, lambda state: state.has_all({advanced_boss_combat.event, wall_building.event}, player))
    bee_queen = add_boss_event("Bee Queen", REGION.FOREST, lambda state: state.has_all({epic_combat.event, hammering.event, beekeeper_hat.event}, player))
    klaus = add_boss_event("Klaus", REGION.FOREST, lambda state: state.has(advanced_boss_combat.event, player))
    malbatross = add_boss_event("Malbatross", REGION.OCEAN, lambda state: state.has_all({advanced_boss_combat.event, advanced_boating.event}, player))
    toadstool = add_boss_event("Toadstool", REGION.CAVE,
        combine_rules(
            (lambda state: state.has_all({basic_combat.event, nonperishable_quick_healing.event, cave_exploration.event}, player)),
            combine_rules(
                lambda state: (
                    state.has(fire_staff.event, player)
                    and (
                        state.has("Dark Sword", player) # Nightmare fuel already required by fire staff
                        or state.has_all({"Glass Cutter", "Boards"}, player)
                    )
                ),
                # Chopping sporecaps
                (lambda state: state.has_any({"Moon Glass Axe", pick_axe.event, weather_pain.event}, player))
                if is_locked("Moon Glass Axe") or REGION.RUINS in WHITELIST or SPECIAL_TAGS.MOOSEGOOSE in WHITELIST
                else ALWAYS_TRUE
            ) if WEAPON_LOGIC
            else ALWAYS_TRUE
        )
    )
    ancient_fuelweaver = add_boss_event("Ancient Fuelweaver", REGION.RUINS,
        combine_rules(
            (
                (lambda state: state.has_all({shadow_atrium.event, ancient_key.event, advanced_boss_combat.event}, player)) if EXPERT_PLAYER_BIAS
                else lambda state: (
                    state.has_all({shadow_atrium.event, ancient_key.event, dark_magic.event}, player) # Requires nightmare fuel
                    and ( # Getting around obelisks
                        state.has("Nightmare Amulet", player)
                        or state.has_all({"The Lazy Explorer", "Walking Cane", winter.event}, player)
                        # TODO: Wortox teleport logic
                    )

                )
            ),
            (lambda state: state.has_any({weather_pain.optional_event, "Wendy"}, player)) if WEAPON_LOGIC # Dealing with woven shadows # TODO: Character logic
            else ALWAYS_TRUE
        )
    )
    lord_of_the_fruit_flies = add_boss_event("Lord of the Fruit Flies", REGION.FOREST, lambda state: state.has_all({basic_combat.event, advanced_farming.event}, player))
    celestial_champion = add_boss_event("Celestial Champion", REGION.MOONSTORM, lambda state:
        state.has_all({"Incomplete Experiment", celestial_orb.event, moonstorm_exploration.event, epic_combat.event, ranged_combat.optional_event}, player)
    )
    eye_of_terror = add_boss_event("Eye Of Terror", REGION.FOREST, lambda state: state.has(advanced_boss_combat.event, player))
    retinazor = add_boss_event("Retinazor", REGION.FOREST, lambda state: state.has(epic_combat.event, player))
    spazmatism = add_boss_event("Spazmatism", REGION.FOREST, lambda state: state.has(epic_combat.event, player))
    nightmare_werepig = add_boss_event("Nightmare Werepig", REGION.RUINS,
        lambda state: state.has_all({advanced_boss_combat.event, pick_axe.event, cave_exploration.event, speed_boost.optional_event}, player)
    )
    scrappy_werepig = add_boss_event("Scrappy Werepig", REGION.RUINS, lambda state: state.has_all({nightmare_werepig.event, arena_building.event}, player))
    frostjaw = add_boss_event("Frostjaw", REGION.OCEAN, lambda state: state.has_all({advanced_boating.event, advanced_boss_combat.event, "Sea Fishing Rod"}, player))


    # Events
    hermit_home_upgrade_1 = add_hermit_event("Hermit Home Upgrade (1)", combine_rules(hermit_island.rule, bug_catching.rule, night.rule if night.is_rule else cave_exploration.rule),
                                                                        night.is_rule or cave_exploration.is_rule) # Cookie cutters, boards, fireflies
    hermit_home_upgrade_2 = add_hermit_event("Hermit Home Upgrade (2)", combine_rules(
                                                                            lambda state: state.can_reach_location(hermit_home_upgrade_1.event, player),
                                                                            sea_fishing.rule if not REGION.CAVE in WHITELIST else ALWAYS_TRUE # Lightbulbs from skittersquids
                                                                        ),
                                                                        hermit_home_upgrade_1.is_rule) # Marble, cut stone, light bulb
    add_hermit_event("Hermit Home Upgrade (3)",                         lambda state: state.has("Floorings", player)
                                                                            and state.can_reach_location(hermit_home_upgrade_2.event, player),
                                                                        hermit_home_upgrade_2.is_rule) # Moonrock, rope, carpet
    add_hermit_event("Hermit Island Drying Racks",                      hermit_island.rule)
    add_hermit_event("Hermit Island Plant 10 Flowers",                  lambda state: state.has_all({hermit_island.event, bug_catching.event}, player), butterfly.is_rule)
    add_hermit_event("Hermit Island Plant 8 Berry Bushes",              lambda state: state.has_all({hermit_island.event, digging.event}, player))
    add_hermit_event("Hermit Island Clear Underwater Salvageables",     lambda state: state.has_all({hermit_sea_quests.event, "Pinchin' Winch"}, player))
    add_hermit_event("Hermit Island Kill Lure Plant",                   combine_rules(hermit_island.rule, spring.rule, either_rule(autumn.rule, winter.rule, summer.rule)),
                                                                        spring.is_rule and SEASON.NONSPRING in WHITELIST)
    add_hermit_event("Hermit Island Build Wooden Chair",                lambda state: state.has_all({hermit_island.event, "Sawhorse"}, player))
    add_hermit_event("Give Crabby Hermit Umbrella",                     combine_rules(
                                                                            lambda state: state.has_any({"Umbrella", "Pretty Parasol"}, player),
                                                                            hermit_island.rule,
                                                                            spring.rule if spring.is_rule else autumn.rule
                                                                        ), spring.is_rule or autumn.is_rule)
    add_hermit_event("Give Crabby Hermit Warm Clothing",                lambda state: state.has_all({hermit_island.event, winter.event}, player)
                                                                            and state.has_any({"Breezy Vest", "Puffy Vest", "Rain Coat"}, player),
                                                                        winter.is_rule)
    add_hermit_event("Give Crabby Hermit Flower Salad",                 lambda state: state.has_all({hermit_island.event, summer.event, cooking.event}, player),
                                                                        summer.is_rule)
    add_hermit_event("Give Crabby Hermit Fallounder",                   lambda state: state.has_all({hermit_sea_quests.event, autumn.event}, player), autumn.is_rule)
    add_hermit_event("Give Crabby Hermit Bloomfin Tuna",                lambda state: state.has_all({hermit_sea_quests.event, spring.event}, player), spring.is_rule)
    add_hermit_event("Give Crabby Hermit Scorching Sunfish",            lambda state: state.has_all({hermit_sea_quests.event, summer.event}, player), summer.is_rule)
    add_hermit_event("Give Crabby Hermit Ice Bream",                    lambda state: state.has_all({hermit_sea_quests.event, winter.event}, player), winter.is_rule)
    add_hermit_event("Give Crabby Hermit 5 Heavy Fish",                 hermit_sea_quests.rule)

    survival_goal = add_event("Survival Goal", REGION.FOREST if options.goal.value == options.goal.option_survival else REGION.NONE,
        combine_rules(
            has_survived_num_days_rule(options.days_to_survive.value),
            (
                (lambda state: state.has_all({advanced_boss_combat.event, basic_boating.optional_event, cave_exploration.optional_event}, player))
                if options.days_to_survive.value < 21 # Generic non-seasonal goal
                else ALWAYS_TRUE
            )
        )
    )

    rules_lookup: Dict[str, Dict[str, Callable[[CollectionState], bool]]] = {
        "location_rules": {
            # Tasks
            "Distilled Knowledge (Yellow)":     archive_exploration.rule,
            "Distilled Knowledge (Blue)":       archive_exploration.rule,
            "Distilled Knowledge (Red)":        archive_exploration.rule,
            "Wagstaff during Moonstorm":        moonstorm_exploration.rule,
            "Queen of Moon Quay":               moon_quay_exploration.rule,
            "Pig King":                         basic_survival.rule,
            "Chester":                          basic_survival.rule,
            "Hutch":                            cave_exploration.rule,
            "Stagehand":                        lambda state: state.has_all({basic_survival.event, hammering.event}, player),
            "Pirate Stash":                     lambda state: state.has_all({pirate_map.event, digging.event}, player),
            "Moon Stone Event":                 moon_stone_event.rule,
            "Oasis":                            lambda state: state.has("Freshwater Fishing Rod", player),
            "Poison Birchnut Tree":             chopping.rule,
            "W.O.B.O.T.":                       lambda state: state.has(scrappy_werepig.event, player) or state.has_all({"Auto-Mat-O-Chanic", electrical_doodad.event}, player),
            "Friendly Fruit Fly":               lord_of_the_fruit_flies.rule,

            # Bosses
            "Deerclops":                        deerclops.rule,
            "Moose/Goose":                      moosegoose.rule,
            "Antlion":                          antlion.rule,
            "Bearger":                          bearger.rule,
            "Ancient Guardian":                 ancient_guardian.rule,
            "Dragonfly":                        dragonfly.rule,
            "Bee Queen":                        bee_queen.rule,
            "Crab King":                        crab_king.rule,
            "Klaus":                            klaus.rule,
            "Malbatross":                       malbatross.rule,
            "Toadstool":                        toadstool.rule,
            "Shadow Knight":                    (lambda state: state.has_all({shadow_pieces.event, "Knight Figure Sketch"}, player)) if CHESSPIECE_ITEMS_SHUFFLED else shadow_pieces.rule,
            "Shadow Bishop":                    (lambda state: state.has_all({shadow_pieces.event, "Bishop Figure Sketch"}, player)) if CHESSPIECE_ITEMS_SHUFFLED else shadow_pieces.rule,
            "Shadow Rook":                      (lambda state: state.has_all({shadow_pieces.event, "Rook Figure Sketch"}, player)) if CHESSPIECE_ITEMS_SHUFFLED else shadow_pieces.rule,
            "Ancient Fuelweaver":               ancient_fuelweaver.rule,
            "Lord of the Fruit Flies":          lord_of_the_fruit_flies.rule,
            "Celestial Champion":               celestial_champion.rule,
            "Eye Of Terror":                    eye_of_terror.rule,
            "Retinazor":                        retinazor.rule,
            "Spazmatism":                       spazmatism.rule,
            "Nightmare Werepig":                nightmare_werepig.rule,
            "Scrappy Werepig":                  scrappy_werepig.rule,
            "Frostjaw":                         frostjaw.rule,

            # Creatures
            "Batilisk":                         batilisk.rule,
            "Bee":                              bug_catching.rule if PEACEFUL_LOGIC else ALWAYS_TRUE,
            "Beefalo":                          either_rule(autumn.rule, winter.rule, summer.rule, basic_combat.rule),
            "Clockwork Bishop":                 lambda state: state.has_all({ruins_exploration.optional_event, advanced_combat.event, healing.event}, player),
            "Bunnyman":                         cave_exploration.rule,
            "Butterfly":                        butterfly.rule,
            "Buzzard":                          basic_combat.rule,
            "Canary":                           combine_rules(canary.rule, (lambda state: state.has_all({"Bird Trap"}, player)) if PEACEFUL_LOGIC else can_get_feathers.rule),
            "Carrat":                           lambda state: state.has_any({lunar_island.event, cave_exploration.event}, player) and state.has_any({"Trap", digging.event}, player),
            "Catcoon":                          basic_survival.rule,
            "Cookie Cutter":                    advanced_boating.rule,
            "Crawling Horror":                  advanced_combat.rule,
            "Crow":                             (lambda state: state.has("Bird Trap", player)) if PEACEFUL_LOGIC else can_get_feathers.rule,
            "Red Hound":                        basic_combat.rule,
            "Frog":                             lambda state: state.has_any({"Trap", pre_basic_combat.event}, player),
            "Saladmander":                      lunar_island.rule,
            "Ghost":                            lambda state: state.has_all({basic_exploration.event, digging.event, pre_basic_combat.event}, player),
            "Gnarwail":                         lambda state: state.has_all({basic_combat.event, advanced_boating.event}, player),
            "Grass Gator":                      lambda state: state.has_all({basic_combat.event, advanced_boating.event, ranged_aggression.event}, player),
            "Grass Gekko":                      digging.rule,
            "Briar Wolf":                       basic_combat.rule,
            "Hound":                            lambda state: state.has_all({basic_combat.event, desert_exploration.event}, player),
            "Blue Hound":                       lambda state: state.has_all({basic_combat.event, winter.event}, player) or state.has_all({basic_combat.event, spring.event, seasons_passed_2.event}, player),
            "Killer Bee":                       bug_catching.rule if PEACEFUL_LOGIC else ALWAYS_TRUE,
            "Clockwork Knight":                 combine_rules(ruins_exploration.optional_rule, advanced_combat.rule),
            "Koalefant":                        lambda state: state.has_all({pre_basic_combat.event, ranged_aggression.event}, player),
            "Krampus":                          combine_rules(basic_combat.rule, either_rule(ranged_aggression.rule, full_moon.rule)),
            "Treeguard":                        lambda state: state.has_all({basic_combat.event, chopping.event, basic_survival.event}, player),
            "Crustashine":                      (lambda state: state.has_all({"Trap", moon_quay_exploration.event}, player)) if PEACEFUL_LOGIC
                                                else (lambda state: state.has_all({ranged_aggression.event, moon_quay_exploration.event}, player)),
            "Bulbous Lightbug":                 combine_rules(bug_catching.rule if PEACEFUL_LOGIC else ALWAYS_TRUE, cave_exploration.rule),
            "Volt Goat":                        lambda state: state.has_all({basic_combat.event, ranged_aggression.event, desert_exploration.event}, player),
            "Merm":                             lambda state: state.has_all({basic_combat.event, swamp_exploration.event}, player),
            "Moleworm":                         moleworm.rule if PEACEFUL_LOGIC else lambda state: state.has_any({dusk.event, night.event, digging.event}, player),
            "Naked Mole Bat":                   lambda state: state.has_all({basic_combat.event, cave_exploration.event}, player),
            "Splumonkey":                       ruins_exploration.rule,
            "Moon Moth":                        combine_rules(can_reach_islands.rule, chopping.rule, bug_catching.rule if PEACEFUL_LOGIC else ALWAYS_TRUE),
            "Mosquito":                         combine_rules(swamp_exploration.rule, bug_catching.rule if PEACEFUL_LOGIC else ALWAYS_TRUE),
            "Mosling":                          moosegoose.rule,
            "Mush Gnome":                       lambda state: state.has_all({basic_combat.event, cave_exploration.event}, player),
            "Terrorclaw":                       lambda state: state.has_all({advanced_combat.event, advanced_boating.event}, player),
            "Pengull":                          basic_combat.rule,
            "Gobbler":                          basic_survival.rule,
            "Pig Man":                          lambda state: state.has(basic_survival.event, player) and state.has_any({day.event, hammering.event, deconstruction_staff.event}, player),
            "Powder Monkey":                    lambda state: state.has_all({can_defend_against_pirates.event, moon_quay_exploration.event}, player),
            "Prime Mate":                       pirate_map.rule,
            "Puffin":                           combine_rules(pre_basic_boating.rule, (lambda state: state.has_all({"Bird Trap"}, player)) if PEACEFUL_LOGIC else can_get_feathers.rule),
            "Rabbit":                           combine_rules(rabbit.rule, (lambda state: state.has("Trap", player) if PEACEFUL_LOGIC else ALWAYS_TRUE)),
            "Redbird":                          (lambda state: state.has("Bird Trap", player)) if PEACEFUL_LOGIC else can_get_feathers.rule,
            "Snowbird":                         (lambda state: state.has("Bird Trap", player)) if PEACEFUL_LOGIC else can_get_feathers.rule,
            "Rock Lobster":                     cave_exploration.rule,
            "Clockwork Rook":                   lambda state: state.has_all({ruins_exploration.optional_event, advanced_combat.event, healing.event}, player),
            "Rockjaw":                          combine_rules(advanced_combat.rule, advanced_boating.rule, either_rule(ranged_combat.optional_rule, cannon.optional_rule)),
            "Slurper":                          ruins_exploration.rule,
            "Slurtle":                          cave_exploration.rule,
            "Snurtle":                          cave_exploration.rule,
            "Ewecus":                           lambda state: state.has_all({advanced_combat.event, advanced_exploration.event}, player),
            "Spider":                           (lambda state: state.has("Trap", player)) if PEACEFUL_LOGIC else ALWAYS_TRUE,
            "Dangling Depth Dweller":           combine_rules((lambda state: state.has("Trap", player)) if PEACEFUL_LOGIC else ALWAYS_TRUE, basic_combat.rule, cave_exploration.rule),
            "Cave Spider":                      combine_rules((lambda state: state.has("Trap", player)) if PEACEFUL_LOGIC else ALWAYS_TRUE, basic_combat.rule, cave_exploration.rule),
            "Nurse Spider":                     combine_rules((lambda state: state.has("Trap", player)) if PEACEFUL_LOGIC else ALWAYS_TRUE, advanced_combat.rule),
            "Shattered Spider":                 combine_rules((lambda state: state.has("Trap", player)) if PEACEFUL_LOGIC else ALWAYS_TRUE, basic_combat.rule, lunar_island.rule),
            "Spitter":                          combine_rules((lambda state: state.has("Trap", player)) if PEACEFUL_LOGIC else ALWAYS_TRUE, basic_combat.rule, cave_exploration.rule),
            "Spider Warrior":                   combine_rules((lambda state: state.has("Trap", player)) if PEACEFUL_LOGIC else ALWAYS_TRUE, basic_combat.rule),
            "Sea Strider":                      combine_rules((lambda state: state.has("Trap", player)) if PEACEFUL_LOGIC else ALWAYS_TRUE, basic_combat.rule, advanced_boating.rule),
            "Spider Queen":                     advanced_combat.rule,
            "Tallbird":                         seasons_passed_half.rule if PEACEFUL_LOGIC else lambda state: state.has_all({basic_combat.event, healing.event}, player),
            "Tentacle":                         lambda state: state.has_all({basic_combat.event, swamp_exploration.event}, player),
            "Big Tentacle":                     lambda state: state.has_all({advanced_combat.event, cave_exploration.event, healing.event}, player),
            "Terrorbeak":                       lambda state: state.has_all({advanced_combat.event, basic_sanity_management.event}, player),
            "MacTusk":                          basic_combat.rule,
            "Varg":                             lambda state: state.has_all({advanced_combat.event, advanced_exploration.event}, player),
            "Varglet":                          lambda state: state.has_all({basic_combat.event, advanced_exploration.event}, player),
            "Depths Worm":                      ruins_exploration.rule,
            "Ancient Sentrypede":               lambda state: state.has_all({archive_exploration.event, advanced_combat.event}, player),
            "Skittersquid":                     lambda state: state.has_all({basic_combat.event, advanced_boating.event}, player),
            "Lure Plant":                       pre_basic_combat.rule,
            "Glommer":                          full_moon.rule,
            "Dust Moth":                        archive_exploration.rule,
            "No-Eyed Deer":                     basic_survival.rule,
            "Moonblind Crow":                   combine_rules(moonstorm_exploration.rule, (lambda state: state.has_any({"Trap", "Bird Trap"}, player)) if PEACEFUL_LOGIC else basic_combat.rule),
            "Misshapen Bird":                   combine_rules(moonstorm_exploration.rule, (lambda state: state.has_any({"Trap", "Bird Trap"}, player)) if PEACEFUL_LOGIC else basic_combat.rule),
            "Moonrock Pengull":                 lambda state: state.has_all({lunar_island.event, basic_combat.event}, player),
            "Horror Hound":                     lambda state: state.has_all({moonstorm_exploration.event, basic_combat.event}, player),
            "Resting Horror":                   ruins_exploration.rule,
            "Birchnutter":                      chopping.rule,
            "Mandrake":                         basic_survival.rule,
            "Fruit Fly":                        basic_farming.rule,
            "Sea Weed":                         lambda state: state.has_all({advanced_boating.event, shaving.event}, player),
            "Marotter":                         basic_combat.rule,

            # Cook foods
            "Butter Muffin":                    lambda state: state.has(butterfly.event, player) or state.has_all({can_reach_islands.event, chopping.event}, player),
            "Froggle Bunwich":                  ALWAYS_TRUE,
            "Taffy":                            honey_farming.rule,
            "Pumpkin Cookies":                  lambda state: state.has_all({honey_farming.event, pumpkin_farming.event}, player),
            "Stuffed Eggplant":                 eggplant_farming.rule,
            "Fishsticks":                       fishing.rule,
            "Honey Nuggets":                    honey_farming.rule,
            "Honey Ham":                        honey_farming.rule,
            "Dragonpie":                        lambda state: state.has_any({dragonfruit_from_saladmander.event, dragonfruit_farming.event}, player),
            "Kabobs":                           ALWAYS_TRUE,
            "Mandrake Soup":                    ALWAYS_TRUE,
            "Bacon and Eggs":                   bird_eggs.optional_rule,
            "Meatballs":                        ALWAYS_TRUE,
            "Meaty Stew":                       ALWAYS_TRUE,
            "Pierogi":                          bird_eggs.optional_rule,
            "Turkey Dinner":                    pre_basic_combat.rule,
            "Ratatouille":                      ALWAYS_TRUE,
            "Fist Full of Jam":                 ALWAYS_TRUE,
            "Fruit Medley":                     fruits.rule,
            "Fish Tacos":                       lambda state: state.has_any({sea_fishing.event, corn_farming.event}, player),
            "Waffles":                          combine_rules(bird_eggs.optional_rule, butter.rule),
            "Monster Lasagna":                  lambda state: state.has_all({"Cut Stone", "Crock Pot", charcoal.event, mining.event, pre_basic_combat.event}, player), # Need basic crock pot, not portable
            "Powdercake":                       lambda state: state.has(honey_farming.event, player) and state.has_any({sea_fishing.event, corn_farming.event}, player),
            "Unagi":                            lambda state: state.has_all({cave_exploration.event, "Freshwater Fishing Rod"}, player),
            "Wet Goop":                         ALWAYS_TRUE,
            "Flower Salad":                     ALWAYS_TRUE,
            "Ice Cream":                        lambda state: state.has_all({honey_farming.event, dairy.event}, player),
            "Melonsicle":                       watermelon_farming.rule,
            "Trail Mix":                        chopping.rule,
            "Spicy Chili":                      ALWAYS_TRUE,
            "Guacamole":                        moleworm.rule,
            "Jellybeans":                       bee_queen.rule,
            "Fancy Spiralled Tubers":           potato_farming.rule,
            "Creamy Potato Purée":              lambda state: state.has_all({potato_farming.event, garlic_farming.event}, player),
            "Asparagus Soup":                   asparagus_farming.rule,
            "Vegetable Stinger":                lambda state: state.has_any({tomaroot_farming.event, asparagus_farming.event}, player),
            "Banana Pop":                       lambda state: state.has_any({cave_exploration.event, moon_quay_exploration.event}, player),
            "Frozen Banana Daiquiri":           lambda state: state.has_any({cave_exploration.event, moon_quay_exploration.event}, player),
            "Banana Shake":                     lambda state: state.has_any({cave_exploration.event, moon_quay_exploration.event}, player),
            "Ceviche":                          either_rule(sea_fishing.rule,
                                                (lambda state: state.has_all({cave_exploration.event, "Freshwater Fishing Rod"}, player)) if REGION.CAVE in WHITELIST else ALWAYS_FALSE),
            "Salsa Fresca":                     tomaroot_farming.rule,
            "Stuffed Pepper Poppers":           pepper_farming.rule,
            "California Roll":                  sea_fishing.rule,
            "Seafood Gumbo":                    lambda state: state.has_all({cave_exploration.event, "Freshwater Fishing Rod"}, player),
            "Surf 'n' Turf":                    fishing.rule,
            "Lobster Bisque":                   sea_fishing.rule,
            "Lobster Dinner":                   lambda state: state.has_all({sea_fishing.event, butter.event}, player) and state.has_any({dusk.event, night.event}, player),
            "Barnacle Pita":                    lambda state: state.has_all({sea_fishing.event, shaving.event}, player),
            "Barnacle Nigiri":                  lambda state: state.has_all({sea_fishing.event, shaving.event}, player),
            "Barnacle Linguine":                lambda state: state.has_all({sea_fishing.event, shaving.event}, player),
            "Stuffed Fish Heads":               lambda state: state.has_all({sea_fishing.event, shaving.event}, player),
            "Leafy Meatloaf":                   leafy_meat.rule,
            "Veggie Burger":                    lambda state: state.has_all({leafy_meat.event, onion_farming.event}, player),
            "Jelly Salad":                      lambda state: state.has_all({honey_farming.event, leafy_meat.event}, player),
            "Beefy Greens":                     leafy_meat.rule,
            "Mushy Cake":                       cave_exploration.rule,
            "Soothing Tea":                     basic_farming.rule,
            "Fig-Stuffed Trunk":                advanced_boating.rule,
            "Figatoni":                         advanced_boating.rule,
            "Figkabab":                         advanced_boating.rule,
            "Figgy Frogwich":                   advanced_boating.rule,
            "Bunny Stew":                       ALWAYS_TRUE,
            "Plain Omelette":                   bird_eggs.optional_rule,
            "Breakfast Skillet":                bird_eggs.rule,
            "Tall Scotch Eggs":                 basic_combat.rule,
            "Steamed Twigs":                    ALWAYS_TRUE,
            "Beefalo Treats":                   basic_farming.rule,
            "Milkmade Hat":                     lambda state: state.has_all({cave_exploration.event, pre_basic_boating.event, dairy.event, basic_combat.event}, player),
            "Amberosia":                        lambda state: state.has_all({salt_crystals.event, "Collected Dust"}, player),
            "Stuffed Night Cap":                cave_exploration.rule,
            # Warly Dishes
            "Grim Galette":                     lambda state: state.has_all({potato_farming.event, onion_farming.event}, player),
            "Volt Goat Chaud-Froid":            basic_combat.rule,
            "Glow Berry Mousse":                cave_exploration.rule,
            "Fish Cordon Bleu":                 sea_fishing.rule,
            "Hot Dragon Chili Salad":           lambda state: state.has(pepper_farming.event, player) and state.has_any({dragonfruit_from_saladmander.event, dragonfruit_farming.event}, player),
            "Asparagazpacho":                   asparagus_farming.rule,
            "Puffed Potato Soufflé":            combine_rules(bird_eggs.optional_rule, potato_farming.rule),
            "Monster Tartare":                  pre_basic_combat.rule,
            "Fresh Fruit Crepes":               lambda state: state.has_all({fruits.event, butter.event}, player),
            "Bone Bouillon":                    lambda state: state.has_all({hammering.event, onion_farming.event}, player),
            "Moqueca":                          lambda state: state.has_all({sea_fishing.event, tomaroot_farming.event}, player),
            # Farming
            "Grow Giant Asparagus":             combine_rules(FARMPLANT_SEASON_RULES["Asparagus"], asparagus_farming.rule),
            "Grow Giant Garlic":                combine_rules(FARMPLANT_SEASON_RULES["Garlic"], garlic_farming.rule),
            "Grow Giant Pumpkin":               combine_rules(FARMPLANT_SEASON_RULES["Pumpkin"], pumpkin_farming.rule),
            "Grow Giant Corn":                  combine_rules(FARMPLANT_SEASON_RULES["Corn"], corn_farming.rule),
            "Grow Giant Onion":                 combine_rules(FARMPLANT_SEASON_RULES["Onion"], onion_farming.rule),
            "Grow Giant Potato":                combine_rules(FARMPLANT_SEASON_RULES["Potato"], potato_farming.rule),
            "Grow Giant Dragon Fruit":          combine_rules(FARMPLANT_SEASON_RULES["Dragon Fruit"], dragonfruit_farming.rule),
            "Grow Giant Pomegranate":           combine_rules(FARMPLANT_SEASON_RULES["Pomegranate"], pomegranate_farming.rule),
            "Grow Giant Eggplant":              combine_rules(FARMPLANT_SEASON_RULES["Eggplant"], eggplant_farming.rule),
            "Grow Giant Toma Root":             combine_rules(FARMPLANT_SEASON_RULES["Toma Root"], tomaroot_farming.rule),
            "Grow Giant Watermelon":            combine_rules(FARMPLANT_SEASON_RULES["Watermelon"], watermelon_farming.rule),
            "Grow Giant Pepper":                combine_rules(FARMPLANT_SEASON_RULES["Pepper"], pepper_farming.rule),
            "Grow Giant Durian":                combine_rules(FARMPLANT_SEASON_RULES["Durian"], durian_farming.rule),
            "Grow Giant Carrot":                combine_rules(FARMPLANT_SEASON_RULES["Carrot"], carrot_farming.rule),
            # Research
            "Science (Nitre)":                  mining.rule,
            "Science (Salt Crystals)":          salt_crystals.rule,
            "Science (Ice)":                    mining.rule,
            "Science (Slurtle Slime)":          cave_exploration.rule,
            "Science (Gears)":                  gears.rule,
            "Science (Scrap)":                  basic_exploration.rule,
            "Science (Azure Feather)":          can_get_feathers.rule,
            "Science (Crimson Feather)":        can_get_feathers.rule,
            "Science (Jet Feather)":            can_get_feathers.rule,
            "Science (Saffron Feather)":        lambda state: state.has_all({canary.event, can_get_feathers.event}, player),
            "Science (Kelp Fronds)":            pre_basic_boating.rule,
            "Science (Steel Wool)":             lambda state: state.has_all({advanced_combat.event, advanced_exploration.event}, player),
            "Science (Electrical Doodad)":      electrical_doodad.rule,
            "Science (Ashes)":                  firestarting.rule,
            "Science (Cut Grass)":              ALWAYS_TRUE,
            "Science (Beefalo Horn)":           basic_combat.rule,
            "Science (Beefalo Wool)":           basic_combat.rule if not shaving.is_progression or not SEASON.NONSPRING in WHITELIST
                                                else combine_rules(shaving.rule, either_rule(autumn.rule, winter.rule, summer.rule)),
            "Science (Cactus Flower)":          ALWAYS_TRUE,
            "Science (Honeycomb)":              basic_combat.rule,
            "Science (Petals)":                 ALWAYS_TRUE,
            "Science (Succulent)":              desert_exploration.rule,
            "Science (Foliage)":                mining.rule if (REGION.CAVE in WHITELIST) else desert_exploration.rule,
            "Science (Tillweeds)":              basic_farming.rule,
            "Science (Lichen)":                 ruins_exploration.rule,
            "Science (Banana)":                 lambda state: state.has_any({moon_quay_exploration.event, cave_exploration.event}, player),
            "Science (Fig)":                    advanced_boating.rule,
            "Science (Tallbird Egg)":           basic_combat.rule,
            "Science (Hound's Tooth)":          basic_combat.rule,
            "Science (Bone Shards)":            lambda state: state.has_all({desert_exploration.event, hammering.event}, player),
            "Science (Walrus Tusk)":            basic_combat.rule,
            "Science (Silk)":                   ALWAYS_TRUE,
            "Science (Cut Stone)":              lambda state: state.has_all({"Cut Stone", mining.event}, player),
            "Science (Palmcone Sprout)":        moon_quay_exploration.rule,
            "Science (Pine Cone)":              chopping.rule,
            "Science (Birchnut)":               chopping.rule,
            "Science (Driftwood Piece)":        pre_basic_boating.rule,
            "Science (Cookie Cutter Shell)":    lambda state: state.has_all({pre_basic_boating.event, basic_combat.event}, player),
            "Science (Palmcone Scale)":         moon_quay_exploration.rule,
            "Science (Gnarwail Horn)":          lambda state: state.has_all({advanced_boating.event, basic_combat.event}, player),
            "Science (Barnacles)":              lambda state: state.has_all({basic_boating.event, shaving.event}, player),
            "Science (Frazzled Wires)":         (lambda state: state.has_all({ruins_exploration.event, hammering.event}, player)) if REGION.RUINS in WHITELIST
                                                else (lambda state: state.has_all({digging.event, basic_sanity_management.event}, player)),
            "Science (Charcoal)":               charcoal.rule,
            "Science (Butter)":                 butter.rule,
            "Science (Asparagus)":              asparagus_farming.rule,
            "Science (Garlic)":                 garlic_farming.rule,
            "Science (Pumpkin)":                pumpkin_farming.rule,
            "Science (Corn)":                   lambda state: state.has_any({sea_fishing.event, corn_farming.event}, player),
            "Science (Onion)":                  onion_farming.rule,
            "Science (Potato)":                 ALWAYS_TRUE if EXPERT_PLAYER_BIAS else potato_farming.rule,
            "Science (Dragon Fruit)":           lambda state: state.has_any({dragonfruit_farming.event, dragonfruit_from_saladmander.event}, player),
            "Science (Pomegranate)":            pomegranate_farming.rule,
            "Science (Eggplant)":               eggplant_farming.rule,
            "Science (Toma Root)":              tomaroot_farming.rule,
            "Science (Watermelon)":             watermelon_farming.rule,
            "Science (Pepper)":                 pepper_farming.rule,
            "Science (Durian)":                 durian_farming.rule,
            "Science (Carrot)":                 ALWAYS_TRUE,
            "Science (Stone Fruit)":            lambda state: state.has_any({lunar_island.event, cave_exploration.event}, player),
            "Science (Marble)":                 mining.rule,
            "Science (Gold Nugget)":            mining.rule,
            "Science (Flint)":                  ALWAYS_TRUE,
            "Science (Honey)":                  ALWAYS_TRUE,
            "Science (Twigs)":                  ALWAYS_TRUE,
            "Science (Log)":                    chopping.rule,
            "Science (Rocks)":                  mining.rule,
            "Science (Light Bulb)":             mining.rule if REGION.CAVE in WHITELIST else sea_fishing.rule,
            "Magic (Blue Gem)":                 gem_digging.rule,
            "Magic (Living Log)":               chopping.rule,
            "Magic (Glommer's Goop)":           full_moon.rule,
            "Magic (Dark Petals)":              ALWAYS_TRUE,
            "Magic (Red Gem)":                  gem_digging.rule,
            "Magic (Slurper Pelt)":             ruins_exploration.rule,
            "Magic (Blue Spore)":               lambda state: state.has_all({cave_exploration.event, bug_catching.event}, player), # TODO: Can use funcap logic potentially
            "Magic (Red Spore)":                lambda state: state.has_all({cave_exploration.event, bug_catching.event}, player),
            "Magic (Green Spore)":              lambda state: state.has_all({cave_exploration.event, bug_catching.event}, player),
            "Magic (Broken Shell)":             cave_exploration.rule,
            "Magic (Leafy Meat)":               leafy_meat.rule,
            "Magic (Canary (Volatile))":        lambda state: state.has_all({canary.event, cave_exploration.event, bird_caging.event}, player),
            "Magic (Life Giving Amulet)":       (lambda state: state.has_all({"Life Giving Amulet", gem_digging.event, nightmare_fuel.event}, player)) if resurrecting.is_progression
                                                else gem_digging.rule,
            "Magic (Nightmare Fuel)":           lambda state: state.has_all({basic_combat.event, nightmare_fuel.event}, player),
            "Magic (Cut Reeds)":                swamp_exploration.rule,
            "Magic (Volt Goat Horn)":           basic_combat.rule,
            "Magic (Beard Hair)":               ALWAYS_TRUE,
            "Magic (Glow Berry)":               ruins_exploration.rule,
            "Magic (Tentacle Spots)":           basic_combat.rule,
            "Magic (Health)":                   healing.rule,
            "Magic (Sanity)":                   ALWAYS_TRUE,
            "Magic (Telltale Heart)":           lambda state: state.has_all({healing.event, "Telltale Heart"}, player),
            "Magic (Forget-Me-Lots)":           basic_farming.rule,
            "Magic (Cat Tail)":                 pre_basic_combat.rule,
            "Magic (Bunny Puff)":               (lambda state: state.has_all({cave_exploration.event, basic_combat.event}, player)
                                                and state.has_any({dusk.event, night.event, hammering.event, deconstruction_staff.event}, player)),
            "Magic (Mosquito Sack)":            swamp_exploration.rule,
            "Magic (Spider Gland)":             ALWAYS_TRUE,
            "Magic (Monster Jerky)":            (lambda state: state.has_all({"Drying Rack", "Rope", charcoal.event}, player)) if BASE_MAKING_LOGIC else charcoal.rule,
            "Magic (Pig Skin)":                 lambda state: state.has_any({hammering.event, deconstruction_staff.event}, player) or state.has_all({day.event, basic_combat.event}, player),
            "Magic (Batilisk Wing)":            batilisk.rule,
            "Magic (Stinger)":                  ALWAYS_TRUE,
            "Magic (Papyrus)":                  lambda state: state.has_all({"Papyrus", swamp_exploration.event}, player),
            "Magic (Green Cap)":                lambda state: state.has_any({digging.event, cave_exploration.event, dusk.event}, player),
            "Magic (Blue Cap)":                 lambda state: state.has_any({digging.event, cave_exploration.event, night.event}, player),
            "Magic (Red Cap)":                  lambda state: state.has_any({digging.event, cave_exploration.event, day.event}, player),
            "Magic (Iridescent Gem)":           iridescent_gem.rule,
            "Magic (Desert Stone)":             storm_protection.rule,
            "Magic (Naked Nostrils)":           cave_exploration.rule,
            "Magic (Frog Legs)":                ALWAYS_TRUE,
            "Magic (Spoiled Fish)":             fishing.rule if (ADVANCED_PLAYER_BIAS or not REGION.OCEAN in WHITELIST) else sea_fishing.rule,
            "Magic (Spoiled Fish Morsel)":      fishing.rule,
            "Magic (Rot)":                      basic_exploration.rule,
            "Magic (Rotten Egg)":               bird_eggs.rule,
            "Magic (Carrat)":                   lambda state: state.has_any({lunar_island.event, cave_exploration.event}, player) and state.has_any({"Trap", digging.event}, player),
            "Magic (Moleworm)":                 moleworm.rule,
            "Magic (Fireflies)":                bug_catching.rule,
            "Magic (Bulbous Lightbug)":         lambda state: state.has_all({cave_exploration.event, bug_catching.event}, player),
            "Magic (Rabbit)":                   lambda state: state.has_all({"Trap", rabbit.event}, player),
            "Magic (Butterfly)":                lambda state: state.has_all({butterfly.event, bug_catching.event}, player),
            "Magic (Mosquito)":                 lambda state: state.has_all({bug_catching.event, swamp_exploration.event}, player),
            "Magic (Bee)":                      bug_catching.rule,
            "Magic (Killer Bee)":               bug_catching.rule,
            "Magic (Crustashine)":              moon_quay_exploration.rule,
            "Magic (Crow)":                     lambda state: state.has("Bird Trap", player),
            "Magic (Redbird)":                  lambda state: state.has("Bird Trap", player),
            "Magic (Snowbird)":                 lambda state: state.has("Bird Trap", player),
            "Magic (Canary)":                   lambda state: state.has_all({"Bird Trap", canary.event}, player),
            "Magic (Puffin)":                   lambda state: state.has_all({"Bird Trap", pre_basic_boating.event}, player),
            "Magic (Fossil Fragments)":         lambda state: state.has_all({cave_exploration.event, mining.event}, player),
            "Think Tank (Freshwater Fish)":     freshwater_fishing.rule if freshwater_fishing.is_progression else combine_rules(basic_combat.rule, swamp_exploration.rule), # Merms
            "Think Tank (Live Eel)":            lambda state: state.has_all({cave_exploration.event, "Freshwater Fishing Rod"}, player),
            "Think Tank (Runty Guppy)":         sea_fishing.rule,
            "Think Tank (Needlenosed Squirt)":  sea_fishing.rule,
            "Think Tank (Bitty Baitfish)":      sea_fishing.rule,
            "Think Tank (Smolt Fry)":           sea_fishing.rule,
            "Think Tank (Popperfish)":          sea_fishing.rule,
            "Think Tank (Fallounder)":          lambda state: state.has_all({advanced_boating.event, sea_fishing.event}, player),
            "Think Tank (Bloomfin Tuna)":       sea_fishing.rule,
            "Think Tank (Scorching Sunfish)":   lambda state: state.has_all({advanced_boating.event, sea_fishing.event}, player),
            "Think Tank (Spittlefish)":         lambda state: state.has_all({advanced_boating.event, sea_fishing.event}, player),
            "Think Tank (Mudfish)":             sea_fishing.rule,
            "Think Tank (Deep Bass)":           lambda state: state.has_all({advanced_boating.event, sea_fishing.event}, player),
            "Think Tank (Dandy Lionfish)":      lambda state: state.has_all({advanced_boating.event, sea_fishing.event}, player),
            "Think Tank (Black Catfish)":       lambda state: state.has_all({advanced_boating.event, sea_fishing.event}, player),
            "Think Tank (Corn Cod)":            lambda state: state.has_all({advanced_boating.event, sea_fishing.event}, player),
            "Think Tank (Ice Bream)":           lambda state: state.has_all({advanced_boating.event, sea_fishing.event}, player),
            "Think Tank (Sweetish Fish)":       lambda state: state.has_all({advanced_boating.event, sea_fishing.event}, player),
            "Think Tank (Wobster)":             lambda state: state.has_all({advanced_boating.event, sea_fishing.event}, player),
            "Think Tank (Lunar Wobster)":       lambda state: state.has_all({lunar_island.event, sea_fishing.event}, player),
            "Pseudoscience (Purple Gem)":       purple_gem.rule,
            "Pseudoscience (Yellow Gem)":       ALWAYS_TRUE,
            "Pseudoscience (Thulecite)":        thulecite.rule,
            "Pseudoscience (Orange Gem)":       ALWAYS_TRUE,
            "Pseudoscience (Green Gem)":        ALWAYS_TRUE,
            "Celestial (Moon Rock)":            ALWAYS_TRUE,
            "Celestial (Moon Shard)":           lambda state: state.has_any({cave_exploration.event, can_reach_islands.event}, player),
            "Celestial (Moon Shroom)":          cave_exploration.rule,
            "Celestial (Moon Moth)":            lambda state: state.has_all({bug_catching.event, chopping.event}, player),
            "Celestial (Lune Tree Blossom)":    ALWAYS_TRUE,
            "Bottle Exchange (1)":              lambda state: state.count("Crabby Hermit Friendship", player) >= 1,
            "Bottle Exchange (2)":              lambda state: state.count("Crabby Hermit Friendship", player) >= 1,
            "Bottle Exchange (3)":              lambda state: state.count("Crabby Hermit Friendship", player) >= 3,
            "Bottle Exchange (4)":              lambda state: state.count("Crabby Hermit Friendship", player) >= 3,
            "Bottle Exchange (5)":              lambda state: state.count("Crabby Hermit Friendship", player) >= 3,
            "Bottle Exchange (6)":              lambda state: state.count("Crabby Hermit Friendship", player) >= 6,
            "Bottle Exchange (7)":              lambda state: state.count("Crabby Hermit Friendship", player) >= 6,
            "Bottle Exchange (8)":              lambda state: state.count("Crabby Hermit Friendship", player) >= 8,
            "Bottle Exchange (9)":              lambda state: state.count("Crabby Hermit Friendship", player) >= 8,
            "Bottle Exchange (10)":             lambda state: state.count("Crabby Hermit Friendship", player) >= 8,

            # Experimental; Will probably won't keep at all
            # **{f"Survive {i} Days":             has_survived_num_days_rule(i) for i in range(1, 100)},
        },
    }

    excluded:Set[str] = set()
    no_advancement:Set[str] = set()
    progression_required_bosses:Set[str] = set()

    if options.goal.value != options.goal.option_survival:
        _required_bosses = frozenset(options.required_bosses.value)
        for boss_name in _required_bosses:
            progression_required_bosses.update(BOSS_PREREQUISITES.get(boss_name, set()))

        # Unify progression bosses with required bosses
        progression_required_bosses.update(_required_bosses)

    PRIORITY_TAGS = {
        "Ancient Fuelweaver": "priority_fuelweaver_boss",
        "Celestial Champion": "priority_celestial_boss",
        "Ancient Guardian": "priority_ruins_boss",
        "Crab King": "priority_crabking_boss",
        "Nightmare Werepig": "priority_ruins_boss",
        "Scrappy Werepig": "priority_scrappywerepig_boss",
        "Antlion": "priority_antlion_boss",
    }

    LOCATIONS_THAT_NEED_SPECIFIC_ITEMS_TO_BE_PROGRESSION = {
        "Magic (Monster Jerky)":        BASE_MAKING_LOGIC,
        "Magic (Life Giving Amulet)":   resurrecting.is_progression,
    }

    # Excluded certain locations because required items aren't progression
    for location_name, useful_allowed in LOCATIONS_THAT_NEED_SPECIFIC_ITEMS_TO_BE_PROGRESSION.items():
        if not useful_allowed:
            excluded.add(location_name)

    # Set location rules
    for location_name, rule in rules_lookup["location_rules"].items():
        Util.assert_rule(rule, multiworld) # DEBUG

        if not location_name in location_data_table:
            continue

        location_data = location_data_table[location_name]
        if location_name in EXISTING_LOCATIONS:
            location = multiworld.get_location(location_name, player)
            required = False

            # Prioritize required bosses
            for boss_name, tag_name in PRIORITY_TAGS.items():
                if boss_name in progression_required_bosses and tag_name in location_data.tags:
                    required = True
                    break

            if required and USE_PRIORITY_TAGS:
                multiworld.priority_locations[player].value.add(location_name)
            elif (
                ("priority" in location_data.tags and USE_PRIORITY_TAGS)
                or (options.boss_fill_items.value == options.boss_fill_items.option_priority and "boss" in location_data.tags)
            ):
                # Prioritize generic priority tag
                multiworld.priority_locations[player].value.add(location_name)

            # Exclude from having progression items if it meets the conditions
            if not required and (
                   (options.boss_fill_items.value == options.boss_fill_items.option_filler and "boss" in location_data.tags)
                or (options.boss_fill_items.value == options.boss_fill_items.option_filler and "raidboss" in location_data.tags)
            ):
                excluded.add(location_name)

            # Disallow progression for rng or advanced locations
            if (
                "rng" in location_data.tags
                or (not ADVANCED_PLAYER_BIAS and "advanced" in location_data.tags)
                # or (not EXPERT_PLAYER_BIAS and "expert" in location_data.tags) # There's no expert tags rn
            ):
                no_advancement.add(location_name)

            if not UNLOCKABLE_SEASON_LOGIC and "seasonal" in location_data.tags:
                # Disallow progression in seasonal locations when season flow is not unlockable
                no_advancement.add(location_name)

                # Forbid season helpers in seasonal locations when not progression
                for item_name in SEASON_HELPER_ITEMS:
                    forbid_item(location, item_name, player)

            # Forbid season helpers and traps in survive day locations
            elif "survivedays" in location_data.tags:
                for item_name in SEASON_HELPER_ITEMS:
                    forbid_item(location, item_name, player)
                for item_name in TRAP_ITEMS:
                    forbid_item(location, item_name, player)

            # Set the rule
            set_rule(location, rule)

        # Add additional rules to locations and their parent events
        if location_name in EXISTING_LOCATIONS or location_name in PARENT_EVENTS:
            # Put rules on parent event if it exists, otherwise put on the location itself
            location = multiworld.get_location(PARENT_EVENTS.get(location_name, location_name), player)

            # Add respective research station rule to research locations
            if "research" in location_data.tags:
                if "science" in location_data.tags:
                    add_rule(location, alchemy_engine.rule if "tier_2" in location_data.tags else science_machine.rule)
                elif "magic" in location_data.tags:
                    add_rule(location, shadow_manipulator.rule if "tier_2" in location_data.tags else prestihatitor.rule)
                elif "celestial" in location_data.tags:
                    add_rule(location, celestial_altar.rule if "tier_2" in location_data.tags else (lambda state: state.has_any({celestial_orb.event, celestial_altar.event}, player)))
                elif "seafaring" in location_data.tags:
                    add_rule(location, think_tank.rule)
                elif "ancient" in location_data.tags:
                    add_rule(location, ancient_altar.rule)
                elif "hermitcrab" in location_data.tags:
                    add_rule(location, pre_basic_boating.rule) # Getting bottles from ocean

            elif "farming" in location_data.tags:
                add_rule(location, advanced_farming.rule)

            elif "cooking" in location_data.tags:
                add_rule(location, cooking.rule)

            def add_tag_group_rule(tag_lookup:Dict[str, str]):
                items = {tag_lookup[tagname] for tagname in location_data.tags.intersection(set(tag_lookup.keys()))}
                if len(items):
                    add_rule(location, lambda state: state.has_any(items, player))

            # Season rules
            add_tag_group_rule({
                "autumn": autumn.event,
                "winter": winter.event,
                "spring": spring.event,
                "summer": summer.event,
            })

            # Day phase rules
            add_tag_group_rule({
                "day":   day.event,
                "dusk":  dusk.event,
                "night": night.event,
            })

            # Season passed rules
            def get_season_passed_event() -> Optional[DSTRule]:
                _season_passed_event:Optional[DSTRule] = (
                    seasons_passed_half if "seasons_passed_half" in location_data.tags
                    else seasons_passed_1 if "seasons_passed_1" in location_data.tags
                    else seasons_passed_2 if "seasons_passed_2" in location_data.tags
                    else seasons_passed_3 if "seasons_passed_3" in location_data.tags
                    else seasons_passed_4 if "seasons_passed_4" in location_data.tags
                    else seasons_passed_5 if "seasons_passed_5" in location_data.tags
                    else None
                )

                if UNLOCKABLE_SEASON_LOGIC or not _season_passed_event:
                    return _season_passed_event

                _next_rule_lookup:Dict[DSTRule, Optional[DSTRule]] = {
                    seasons_passed_half: seasons_passed_1 if seasons_passed_1.is_rule else None,
                    seasons_passed_1:    seasons_passed_2 if seasons_passed_2.is_rule else None,
                    seasons_passed_2:    seasons_passed_3 if seasons_passed_3.is_rule else None,
                    seasons_passed_3:    seasons_passed_4 if seasons_passed_4.is_rule else None,
                    seasons_passed_4:    seasons_passed_5 if seasons_passed_5.is_rule else None,
                    seasons_passed_5:    None,
                }

                _valid_seasons = {SEASON.tag_lookup[_season_tag] for _season_tag in location_data.tags.intersection({"autumn", "winter", "spring", "summer"})}
                if not len(_valid_seasons):
                    return _season_passed_event

                # Align valid season with season passed rule
                _equivalent_season = EQUIVALENT_SEASONS.get(_season_passed_event, None)
                _last_event = _season_passed_event
                while _season_passed_event and _equivalent_season and not _equivalent_season in _valid_seasons:
                    _last_event = _season_passed_event
                    _season_passed_event = _next_rule_lookup.get(_season_passed_event, None)
                    _equivalent_season = EQUIVALENT_SEASONS.get(_season_passed_event, None)

                return _season_passed_event if _season_passed_event else _last_event

            _season_passed_event = get_season_passed_event()
            if _season_passed_event:
                add_rule(location, _season_passed_event.rule)

    exclusion_rules(multiworld, player, excluded)

    # Apply no-advancement rules to non-priority locations
    for location_name in no_advancement:
        if (
            location_name in EXISTING_LOCATIONS
            and not (location_name in multiworld.priority_locations[player].value)
            and not (location_name in excluded)
        ):
            add_item_rule(multiworld.get_location(location_name, player), NO_ADVANCEMENT_ITEM)

   # Decide win conditions
    victory_events:Set = set()
    if options.goal.value == options.goal.option_survival:
        victory_events.add(survival_goal.event)
    elif options.goal.value == options.goal.option_bosses_any or options.goal.value == options.goal.option_bosses_all:
        victory_events.update([BOSS_COMPLETION_GOALS[bossname] for bossname in options.required_bosses.value])

    # Set the win conditions
    if options.goal.value == options.goal.option_bosses_any:
        multiworld.completion_condition[player] = lambda state: state.has_any(victory_events, player)
    else:
        multiworld.completion_condition[player] = lambda state: state.has_all(victory_events, player)

    itempool.set_progression_items({
        "Autumn":                   UNLOCKABLE_SEASON_LOGIC,
        "Winter":                   UNLOCKABLE_SEASON_LOGIC,
        "Spring":                   UNLOCKABLE_SEASON_LOGIC,
        "Summer":                   UNLOCKABLE_SEASON_LOGIC,
        "Full Moon Phase Change":   UNLOCKABLE_SEASON_LOGIC,
        "New Moon Phase Change":    UNLOCKABLE_SEASON_LOGIC,
        "Asparagus Seeds":          True,
        "Garlic Seeds":             True,
        "Pumpkin Seeds":            True,
        "Corn Seeds":               True,
        "Onion Seeds":              True,
        "Potato Seeds":             True,
        "Dragon Fruit Seeds":       True,
        "Pomegranate Seeds":        True,
        "Eggplant Seeds":           True,
        "Toma Root Seeds":          True,
        "Watermelon Seeds":         True,
        "Pepper Seeds":             True,
        "Durian Seeds":             True,
        "Carrot Seeds":             True,
        "Pickaxe":                  True,
        "Opulent Pickaxe":          True,
        "Axe":                      True,
        "Luxury Axe":               True,
        "Hammer":                   True,
        "Bug Net":                  True,
        "Rope":                     True,
        "Shovel":                   True,
        "Regal Shovel":             True,
        "Bird Trap":                bird_caging.is_progression,
        "Birdcage":                 bird_caging.is_progression,
        "Papyrus":                  True,
        "Spear":                    True,
        "Ice Staff":                ice_staff.is_progression,
        "Fire Staff":               fire_staff.is_progression,
        "Torch":                    True,
        "Campfire":                 True,
        "Flare":                    hostile_flare.is_progression,
        "Hostile Flare":            hostile_flare.is_progression,
        "Backpack":                 BACKPACK_LOGIC,
        "Piggyback":                BACKPACK_LOGIC,
        "Cut Stone":                True,
        "Electrical Doodad":        True,
        "Morning Star":             True,
        "Weather Pain":             weather_pain.is_progression,
        "Pick/Axe":                 True,
        "Cannon Kit":               True,
        "Gunpowder":                cannon.is_progression,
        "Razor":                    shaving.is_progression,
        "Telelocator Staff":        telelocator_staff.is_progression,
        "Deconstruction Staff":     True,
        "Nightmare Fuel":           nightmare_fuel.is_progression,
        "Boomerang":                WEAPON_LOGIC,
        "Boards":                   True,
        "Purple Gem":               True,
        "Friendly Scarecrow":       PHASE.DAY_OR_DUSK in WHITELIST,
        "Thulecite":                True,
        "Log Suit":                 WEAPON_LOGIC,
        "Football Helmet":          WEAPON_LOGIC,
        "Grass Suit":               WEAPON_LOGIC,
        "Beekeeper Hat":            beekeeper_hat.is_progression,
        "Ham Bat":                  WEAPON_LOGIC,
        "Dark Sword":               WEAPON_LOGIC,
        "Glass Cutter":             WEAPON_LOGIC,
        "Blow Dart":                WEAPON_LOGIC,
        "Electric Dart":            WEAPON_LOGIC,
        "Sleep Dart":               WEAPON_LOGIC,
        "Fire Dart":                WEAPON_LOGIC,
        "Bat Bat":                  WEAPON_LOGIC,
        "Night Armor":              WEAPON_LOGIC,
        "Top Hat":                  True,
        "Garland":                  basic_sanity_management.is_progression,
        "Healing Salve":            quick_healing.is_progression,
        "Honey Poultice":           quick_healing.is_progression,
        "Tent":                     slow_healing.is_progression,
        "Siesta Lean-to":           slow_healing.is_progression,
        "Straw Roll":               slow_healing.is_progression or EXPERT_PLAYER_BIAS,
        "Fur Roll":                 slow_healing.is_progression,
        "Booster Shot":             True,
        "Life Giving Amulet":       resurrecting.is_progression,
        "Meat Effigy":              resurrecting.is_progression,
        "Thermal Stone":            True,
        "Rabbit Earmuffs":          SEASON_GEAR_LOGIC,
        "Puffy Vest":               SEASON_GEAR_LOGIC or hermit_island.is_progression,
        "Beefalo Hat":              True,
        "Winter Hat":               SEASON_GEAR_LOGIC,
        "Cat Cap":                  SEASON_GEAR_LOGIC,
        "Fire Pit":                 True,
        "Rain Coat":                True,
        "Rain Hat":                 True,
        "Straw Hat":                True,
        "Eyebrella":                deerclops.is_progression,
        "Lightning Rod":            SEASON_GEAR_LOGIC,
        "Lightning Conductor":      SEASON_GEAR_LOGIC,
        "Mast Kit":                 SEASON_GEAR_LOGIC or not EXPERT_PLAYER_BIAS,
        "Umbrella":                 SEASON_GEAR_LOGIC or hermit_island.is_progression,
        "Pretty Parasol":           SEASON_GEAR_LOGIC or hermit_island.is_progression,
        "Ice Box":                  BASE_MAKING_LOGIC or SEASON_GEAR_LOGIC,
        "Endothermic Fire":         SEASON_GEAR_LOGIC,
        "Chilled Amulet":           SEASON_GEAR_LOGIC,
        "Endothermic Fire Pit":     SEASON_GEAR_LOGIC,
        "Summer Frest":             SEASON_GEAR_LOGIC,
        "Floral Shirt":             SEASON_GEAR_LOGIC,
        "Ice Flingomatic":          SEASON_GEAR_LOGIC,
        "Luxury Fan":               SEASON_GEAR_LOGIC and moosegoose.is_progression,
        "Empty Watering Can":       True,
        "Whirly Fan":               SEASON_GEAR_LOGIC,
        "Chest":                    BASE_MAKING_LOGIC,
        "Wood Gate and Fence":      BASE_MAKING_LOGIC,
        "Hay Wall":                 BASE_MAKING_LOGIC,
        "Wood Wall":                BASE_MAKING_LOGIC,
        "Stone Wall":               True,
        "Saddle":                   True,
        "Beefalo Bell":             True,
        "Pitchfork":                arena_building.is_progression,
        "Snazzy Pitchfork":         arena_building.is_progression,
        "Turf-Raiser Helm":         arena_building.is_progression,
        "Floorings":                arena_building.is_progression or hermit_island.is_progression,
        "Cratered Moonrock":        character_switching.is_progression,
        "Moon Rock Idol":           character_switching.is_progression,
        "Portal Paraphernalia":     character_switching.is_progression,
        "Thulecite Wall":           ADVANCED_PLAYER_BIAS,
        "Potter's Wheel":           True,
        "Telltale Heart":           True,
        "Magiluminescence":         True,
        "Lantern":                  LIGHTING_LOGIC,
        "Miner Hat":                LIGHTING_LOGIC,
        "Boat Kit":                 True,
        "Oar":                      True,
        "Grass Raft Kit":           True,
        "Boat Patch":               True,
        "Driftwood Oar":            True,
        "Anchor Kit":               not EXPERT_PLAYER_BIAS,
        "Steering Wheel Kit":       not EXPERT_PLAYER_BIAS,
        "Fashion Goggles":          basic_sanity_management.is_progression or SEASON.SUMMER in WHITELIST,
        "Desert Goggles":           True,
        "Astroggles":               True,
        "Garden Hoe":               True,
        "Splendid Garden Hoe":      True,
        "Garden Digamajig":         True,
        "Bee Box":                  honey_farming.is_progression,
        "Crock Pot":                True,
        "Pinchin' Winch":           True,
        "Freshwater Fishing Rod":   True,
        "Ocean Trawler Kit":        True,
        "Tin Fishin' Bin":          BASE_MAKING_LOGIC,
        "Sea Fishing Rod":          True,
        "Astral Detector":          True,
        "Star Caller's Staff":      moon_stone_event.is_progression,
        "Bishop Figure Sketch":     CHESSPIECE_ITEMS_SHUFFLED,
        "Rook Figure Sketch":       CHESSPIECE_ITEMS_SHUFFLED,
        "Knight Figure Sketch":     CHESSPIECE_ITEMS_SHUFFLED,
        "Trap":                     True,
        "Moon Glass Axe":           toadstool.is_progression and WEAPON_LOGIC,
        "Nightmare Amulet":         ancient_fuelweaver.is_progression and not EXPERT_PLAYER_BIAS,
        "The Lazy Explorer":        ancient_fuelweaver.is_progression and not EXPERT_PLAYER_BIAS,
        "Walking Cane":             True,
        "Incomplete Experiment":    True,
        "Sawhorse":                 hermit_island.is_progression,
        "Breezy Vest":              hermit_island.is_progression,
        "Auto-Mat-O-Chanic":        "W.O.B.O.T." in EXISTING_LOCATIONS,
        "Collected Dust":           "Amberosia" in EXISTING_LOCATIONS,
        "Drying Rack":              BASE_MAKING_LOGIC,
        "Bath Bomb":                dragonfruit_from_saladmander.is_progression,
    })