from typing import Dict, Set, Optional, Callable

from BaseClasses import CollectionState, ItemClassification, Item
from worlds.generic.Rules import exclusion_rules, set_rule, add_rule, add_item_rule, forbid_item
from worlds.AutoWorld import World

from .Locations import location_data_table, DSTLocation
from .Options import DSTOptions
from .Items import item_data_table
from .ItemPool import DSTItemPool
from .Constants import REGION

class DSTRule:
    event:str
    rule:Callable[[CollectionState], bool]
    is_progression:bool = True
    def __init__(self, event:str, rule:Callable[[CollectionState], bool], player:int):
        self.event = f"(EVENT) {event}"
        self.rule = lambda state: state.has(self.event, player)

    def __call__(self, state: CollectionState) -> bool:
        # Eventually nothing should be calling this
        return self.rule(state)

def ALWAYS_TRUE(state: CollectionState) -> bool:
    return True

def ALWAYS_FALSE(state: CollectionState) -> bool:
    return False

def NO_ADVANCEMENT_ITEM(item: Item) -> bool:
    return not item.advancement

def combine_rules(a: Callable[[CollectionState], bool], b: Callable[[CollectionState], bool]) -> Callable[[CollectionState], bool]:
    if a == ALWAYS_FALSE or b == ALWAYS_FALSE:
        return ALWAYS_FALSE
    if a == ALWAYS_TRUE: return b
    if b == ALWAYS_TRUE: return a
    return lambda state: a(state) and b(state)

def either_rule(a: Callable[[CollectionState], bool], b: Callable[[CollectionState], bool]) -> Callable[[CollectionState], bool]:
    if a == ALWAYS_TRUE or b == ALWAYS_TRUE:
        return ALWAYS_TRUE
    if a == ALWAYS_FALSE: return b
    if b == ALWAYS_FALSE: return a
    return lambda state: a(state) or b(state)

class AssertionState(CollectionState):
    def has(self, item, player, count = 1):
        assert type(item) is str, item
        assert len(item)
        assert type(player) is int, player
        return super().has(item, player, count)
    
    def has_all(self, items, player):
        assert type(items) is list, items
        for item in items:
            assert type(item) is str, item
            assert len(item)
        assert type(player) is int, player
        return super().has_all(items, player)
    
    def has_any(self, items, player):
        assert type(items) is list, items
        for item in items:
            assert type(item) is str, item
            assert len(item)
        assert type(player) is int, player
        return super().has_any(items, player)

def assert_rule(rule: Callable[[CollectionState], bool], multiworld):
    state = AssertionState(multiworld)
    rule(state)

def set_rules(dst_world: World, itempool:DSTItemPool) -> None:
    multiworld = dst_world.multiworld
    player = dst_world.player
    options:DSTOptions = dst_world.options

    ADVANCED_PLAYER_BIAS = options.skill_level.value != options.skill_level.option_easy
    EXPERT_PLAYER_BIAS = options.skill_level.value == options.skill_level.option_expert
    BOSS_LOOT_LOGIC = options.boss_locations.value >= options.boss_locations.option_easy
    RAIDBOSS_LOOT_LOGIC = options.boss_locations.value >= options.boss_locations.option_all
    CREATURE_LOCATIONS_ENABLED = bool(options.creature_locations.value)
    WARLY_DISHES_ENABLED = options.cooking_locations.value == options.cooking_locations.option_warly_enabled
    CHESSPIECE_ITEMS_SHUFFLED = bool(options.chesspiece_sketch_items.value)
    CRAFT_WITH_LOCKED_RECIPES = True # TODO: Replace with CRAFT_WITH_LOCKED_RECIPES option
    PROGRESSION_UNLOCKS_SHUFFLED = False # TODO: Progression unlocks shuffle
    LIGHTING_LOGIC = bool(options.lighting_logic.value)
    WEAPON_LOGIC = bool(options.weapon_logic.value)
    SEASON_GEAR_LOGIC = bool(options.season_gear_logic.value)
    BASE_MAKING_LOGIC = bool(options.base_making_logic.value)
    BACKPACK_LOGIC = bool(options.backpack_logic.value)
    HEALING_LOGIC = bool(options.healing_logic.value)
    CHARACTER_SWITCHING_LOGIC = True
    CHARACTER_LOGIC = False

    # Build region whitelist
    REGION_WHITELIST = set([REGION.FOREST])
    if options.cave_regions.value >= options.cave_regions.option_light: REGION_WHITELIST.update([REGION.CAVE])
    if options.cave_regions.value >= options.cave_regions.option_full: REGION_WHITELIST.update([REGION.RUINS, REGION.ARCHIVE])
    if options.ocean_regions.value >= options.ocean_regions.option_light: REGION_WHITELIST.update([REGION.OCEAN, REGION.MOONQUAY])
    if options.ocean_regions.value >= options.ocean_regions.option_full: REGION_WHITELIST.update([REGION.MOONSTORM])
    if REGION.CAVE in REGION_WHITELIST or REGION.OCEAN in REGION_WHITELIST: REGION_WHITELIST.update([REGION.DUALREGION])
    if REGION.CAVE in REGION_WHITELIST and REGION.OCEAN in REGION_WHITELIST: REGION_WHITELIST.update([REGION.BOTHREGIONS])

    def is_locked(item_name:str): return item_name in itempool.locked_items
    def is_any_locked(*item_names:str):
        for item_name in item_names:
            if item_name in itempool.locked_items:
                return True
        return False

    # Make a rule that is just ALWAYS_TRUE
    def add_spawn_event():
        dst_rule = DSTRule("Spawn", ALWAYS_TRUE, player)
        region = multiworld.get_region(REGION.FOREST, player)
        loc = DSTLocation(player, dst_rule.event, None, region)
        loc.show_in_spoiler = False
        dst_rule.is_progression = False
        item = multiworld.create_item(dst_rule.event, player)
        item.classification = ItemClassification.progression
        loc.place_locked_item(item)
        region.locations.append(loc)
        return dst_rule
    spawn = add_spawn_event()

    def add_event(event:str, regionname:str, rule:Callable[[CollectionState], bool], custom_item:Optional[str] = None, hide_in_spoiler:bool = False):
        assert callable(rule)
        dst_rule = DSTRule(event, rule, player)
        # Create event for rule
        if regionname in REGION_WHITELIST and not rule == ALWAYS_FALSE:
            if rule == ALWAYS_TRUE:
                # No need to create an event if always true
                return spawn
            else:
                region = multiworld.get_region(regionname, player)
                loc = DSTLocation(player, dst_rule.event, None, region)
                loc.show_in_spoiler = False if hide_in_spoiler else (not event in item_data_table.keys())
                dst_rule.is_progression = rule != ALWAYS_TRUE
                item = multiworld.create_item(custom_item or dst_rule.event, player)
                item.classification = ItemClassification.progression
                loc.place_locked_item(item)
                region.locations.append(loc)
                add_rule(loc, rule)
        else:
            dst_rule.is_progression = False
        return dst_rule

    BOSS_COMPLETION_GOALS:Dict[str, str] = {}
    def add_boss_event(event:str, regionname:str, rule:Callable[[CollectionState], bool]):
        dst_rule = add_event(event, regionname, rule)
        BOSS_COMPLETION_GOALS[event] = dst_rule.event
        return dst_rule

    def add_farming_event(veggie_name:str, unshuffled_req:str, or_rule:Optional[Callable[[CollectionState], bool]] = None):
        assert unshuffled_req and len(unshuffled_req)
        return add_event(f"{veggie_name} Farming", REGION.FOREST,
            either_rule(
                (lambda state: state.has_all([basic_farming.event, f"{veggie_name} Seeds" if is_locked(f"{veggie_name} Seeds") else unshuffled_req], player)),
                or_rule if or_rule != None else ALWAYS_FALSE
            )
        )

    def add_hermit_event(event:str, rule:Callable[[CollectionState], bool]):
        return add_event(event, REGION.OCEAN, rule, "Crabby Hermit Friendship")

    # Misc rules
    def has_survived_num_days (day_goal:int, state: CollectionState) -> bool:
        return state.has(basic_survival.event, player)
        # Prioritize basic survival
        if not state.has(basic_survival.event, player):
            return False
        # Assume number of days lived based on items count
        item_count = state.count_group("all", player)
        if item_count < 4:
            return False
        return (day_goal if day_goal < 50 else 50) > (4 - (item_count/2))

    def has_survived_num_days_2 (day_goal:int, state: CollectionState) -> bool:
        if day_goal < 20:
            return state.has(basic_survival.event, player)
        elif day_goal < 35:
            return state.has(winter.event, player)
        elif day_goal < 55:
            return state.has(spring.event, player)
        elif day_goal < 70:
            return state.has(summer.event, player)
        elif day_goal < 90:
            return state.has(autumn.event, player)
        return state.has(late_game.event, player)

    def weregoose (state: CollectionState) -> bool:
        return state.has_all(["Woodie", basic_survival.event], player)

    ##### MILESTONES #####
    winter = add_event("Winter", REGION.FOREST, lambda state: state.has(winter_survival.event, player))
    spring = add_event("Spring", REGION.FOREST, lambda state: state.has_all([winter.event, spring_survival.event, deerclops.event], player))
    summer = add_event("Summer", REGION.FOREST, lambda state: state.has_all([spring.event, summer_survival.event, moosegoose.event], player))
    autumn = add_event("Autumn", REGION.FOREST, lambda state: state.has_all([summer.event, autumn_survival.event, antlion.event], player))
    late_game = add_event("Late Game", REGION.FOREST, lambda state: state.has_all([autumn.event, late_game_survival.event], player))


    ##### SEASONS #####
    # TODO: Seasons as items
    seasons_passed_1 = winter
    seasons_passed_2 = spring
    seasons_passed_3 = summer
    seasons_passed_4 = autumn
    seasons_passed_5 = late_game

    ##### TOOLS #####
    mining = add_event("Mining", REGION.FOREST, lambda state: state.has_any(["Pickaxe", "Opulent Pickaxe", "Woodie"], player))
    chopping = add_event("Chopping", REGION.FOREST, lambda state: state.has_any(["Axe", "Luxury Axe", "Woodie"], player))
    hammering = add_event("Hammering", REGION.FOREST, lambda state: state.has_any(["Hammer", "Woodie"], player))
    bug_catching = add_event("Bug Catching", REGION.FOREST, lambda state: state.has_all(["Bug Net", "Rope"], player))
    digging = add_event("Digging", REGION.FOREST, lambda state: state.has_any(["Shovel", "Regal Shovel"], player))
    bird_caging = add_event("Bird Caging", REGION.FOREST, lambda state: state.has_all(["Bird Trap", "Birdcage", "Papyrus"], player))
    ice_staff = add_event("Ice Staff", REGION.FOREST if WEAPON_LOGIC else REGION.NONE, lambda state: state.has_all(["Spear", "Rope", "Ice Staff", gem_digging.event], player))
    fire_staff = add_event("Fire Staff", REGION.FOREST if WEAPON_LOGIC else REGION.NONE, lambda state: state.has_all(["Spear", "Rope", "Fire Staff", gem_digging.event, nightmare_fuel.event], player))
    firestarting = add_event("Firestarting", REGION.FOREST, lambda state:
        state.has_any(["Torch", "Willow", fire_staff.event], player)
        or state.has_all(["Campfire", chopping.event], player)
    )
    hostile_flare = add_event("Hostile Flare", REGION.MOONQUAY, lambda state: state.has_all(["Flare", "Hostile Flare", mining.event, firestarting.event], player))
    backpack = add_event("Backpack", REGION.FOREST,
        (
            lambda state:(
                state.has("Backpack", player)
                or (state.has_all(["Piggyback", "Rope", pre_basic_combat.event], player))
            ) if BACKPACK_LOGIC
            else ALWAYS_TRUE
        )
    )
    morning_star = add_event("Morning Star", REGION.FOREST, lambda state:
        state.has_all([electrical_doodad.event, "Morning Star", ranged_aggression.event, desert_exploration.event, basic_combat.event], player)
    )
    weather_pain = add_event("Weather Pain", REGION.FOREST if WEAPON_LOGIC else REGION.NONE, lambda state: state.has_all(["Weather Pain", moosegoose.event, gears.event], player))
    pick_axe = add_event("Pick/Axe", REGION.DUALREGION,
        combine_rules(
            (
                (lambda state: state.has_all(["Pick/Axe", thulecite.event], player)) if is_locked("Pick/Axe")
                else (lambda state: state.has(ancient_altar.event, player)) if REGION.RUINS in REGION_WHITELIST
                else ALWAYS_TRUE # Allow obtaining from ocean region
            ),
            (
                (lambda state: state.has_all(["Opulent Pickaxe", "Luxury Axe"], player)) if REGION.RUINS in REGION_WHITELIST
                else (lambda state: state.has(sunken_chest.event, player)) if REGION.OCEAN in REGION_WHITELIST
                else ALWAYS_TRUE # Player probably chose caves but not ruins or ocean
            )
        )
    )
    cannon = add_event("Cannon", REGION.MOONQUAY, lambda state:
        state.has_all([moon_quay_exploration.event, "Cannon Kit", "Gunpowder", "Cut Stone", "Rope", charcoal.event, mining.event, bird_caging.event], player)
    )
    shaving = add_event("Shaving", REGION.FOREST,
        ALWAYS_TRUE if ADVANCED_PLAYER_BIAS
        else lambda state: state.has("Razor", player)
    )
    telelocator_staff = add_event("Telelocator Staff", REGION.OCEAN if EXPERT_PLAYER_BIAS else REGION.NONE, lambda state:
        state.has_all(["Telelocator Staff", purple_gem.event, chopping.event], player)
    )
    mooncaller_staff = add_event("Mooncaller Staff", REGION.FOREST if is_locked("Deconstruction Staff") else REGION.RUINS, lambda state: state.has(moon_stone_event.event, player))
    deconstruction_staff = add_event("Deconstruction Staff", REGION.FOREST if is_locked("Deconstruction Staff") else REGION.RUINS,
        (lambda state: state.has_all(["Deconstruction Staff", chopping.event, ruins_gems.event], player)) if is_locked("Deconstruction Staff")
        else (lambda state: state.has(ancient_altar.event, player))
    )
    beekeeper_hat = add_event("Beekeeper Hat", REGION.FOREST,
        (lambda state: state.has("Beekeeper Hat", player)) if WEAPON_LOGIC and (
            RAIDBOSS_LOOT_LOGIC
            or ((options.goal.value != options.goal.option_survival) and "Bee Queen" in options.required_bosses.value)
        ) else ALWAYS_TRUE
    )


    ##### RESOURCES #####
    nightmare_fuel = add_event("Nightmare Fuel", REGION.FOREST,
        ALWAYS_TRUE if CRAFT_WITH_LOCKED_RECIPES or not is_locked("Nightmare Fuel")
        else (lambda state: state.has("Nightmare Fuel", player))
    )
    gem_digging = add_event("Gem Digging", REGION.FOREST, lambda state: state.has_all([digging.event, basic_sanity_management.event], player))
    charcoal = add_event("Charcoal", REGION.FOREST, lambda state: state.has_all([chopping.event, firestarting.event], player))
    butter_luck = add_event("Butter Luck", REGION.FOREST, ALWAYS_TRUE if EXPERT_PLAYER_BIAS else lambda state: has_survived_num_days(40, state))
    can_get_feathers = add_event("Can Get Feathers", REGION.FOREST,
        (
            (
                lambda state: (
                    state.has_all(["Boomerang", "Boards", charcoal.event], player)
                    or state.has_any(["Bird Trap", ice_staff.event], player)
                )
            ) if WEAPON_LOGIC
            else ALWAYS_TRUE if EXPERT_PLAYER_BIAS
            else (lambda state: state.has("Bird Trap", player))
        )
    )
    gears = add_event("Gears", REGION.FOREST,
        ALWAYS_TRUE if EXPERT_PLAYER_BIAS # Tumbleweeds
        else (lambda state: state.has(ruins_exploration.event, player)) if REGION.RUINS in REGION_WHITELIST
        else (lambda state: state.has(advanced_combat.event, player))
    )
    ruins_gems = add_event("Ruins Gems", REGION.FOREST, lambda state: state.has_any([ruins_exploration.event, dragonfly.event, sunken_chest.event], player)) # This is not ruins exclusive
    purple_gem = add_event("Purple Gem", REGION.FOREST,
        combine_rules(
            (
                ALWAYS_TRUE if CRAFT_WITH_LOCKED_RECIPES
                else (lambda state: state.has("Purple Gem", player))
            ),
            lambda state: (
                state.has_all([gem_digging.event, "Purple Gem"], player)
                or state.has(ruins_gems.event, player)
            )
        )
    )
    canary = add_event("Canary", REGION.FOREST, lambda state: state.has_all(["Friendly Scarecrow", "Boards", pumpkin_farming.event], player)) # Pumpkin
    salt_crystals = add_event("Salt Crystals", REGION.OCEAN,
        (lambda state: state.has_all([pre_basic_boating.event, mining.event, basic_combat.event], player)) if WEAPON_LOGIC
        else lambda state: state.has_all([pre_basic_boating.event, mining.event], player)
    )
    thulecite = add_event("Thulecite", REGION.DUALREGION,
        combine_rules(
            (
                (lambda state: state.has("Thulecite", player)) if is_locked("Thulecite") and not CRAFT_WITH_LOCKED_RECIPES
                else ALWAYS_TRUE
            ),
            (
                (lambda state: state.has(ruins_exploration.event, player)) if REGION.RUINS in REGION_WHITELIST
                else (lambda state: state.has(archive_exploration.event, player)) if REGION.ARCHIVE in REGION_WHITELIST
                else (lambda state: state.has(sunken_chest.event, player)) if REGION.OCEAN in REGION_WHITELIST
                else ALWAYS_TRUE # Player probably chose caves but not ruins or ocean
            )
        )
    )
    leafy_meat = add_event("Leafy Meat", REGION.FOREST,
        either_rule(
            either_rule(
                (lambda state: state.has(spring.event, player)), # Lureplants, Carrats
                (
                    (lambda state: state.has(lunar_island.event, player)) if REGION.OCEAN in REGION_WHITELIST # Carrats
                    else ALWAYS_FALSE
                )
            ),
            (lambda state: state.has(cave_exploration.event, player)) if ADVANCED_PLAYER_BIAS and (REGION.CAVE in REGION_WHITELIST) # Carrats in lunar grotto
            else ALWAYS_FALSE
        )
    )
    electrical_doodad = add_event("Electrical Doodad", REGION.FOREST,
        either_rule(
            (lambda state: state.has_all(["Cut Stone", "Electrical Doodad", mining.event], player)),
            (lambda state: state.has_any([retinazor.event, spazmatism.event], player)) if RAIDBOSS_LOOT_LOGIC and EXPERT_PLAYER_BIAS
            else ALWAYS_FALSE
        )
    )


    ##### COMBAT #####
    basic_combat = add_event("Basic Combat", REGION.FOREST,
        (
            lambda state: (
                (
                    state.has_all(["Rope", "Spear"], player)
                    # or state.has("Wigfrid", player) # TODO: character logic
                )
                and state.has_any(["Log Suit", "Football Helmet"], player)
                and state.has(chopping.event, player) # Wood for the log suit, or at least a weapon before you get the spear
            )
        ) if WEAPON_LOGIC else ALWAYS_TRUE
    )
    pre_basic_combat = add_event("Pre-Basic Combat", REGION.FOREST,
        (
            lambda state: (
                state.has_all(["Grass Suit", chopping.event], player) # Axe as a weapon
                or state.has_any([basic_combat.event, "Wendy", "Wigfrid"], player) # TODO: character logic
            )
        ) if WEAPON_LOGIC else ALWAYS_TRUE
    )
    advanced_combat = add_event("Advanced Combat", REGION.FOREST,
        (
            lambda state: (
                state.has_all([basic_combat.event, "Log Suit", "Football Helmet"], player) # Both armor pieces
                and (
                    state.has("Ham Bat", player)
                    or state.has_all(["Dark Sword", nightmare_fuel.event], player)
                    or state.has_all(["Glass Cutter", "Boards"], player)
                )
                and (ADVANCED_PLAYER_BIAS or state.has(base_making.event, player))
            )
        ) if WEAPON_LOGIC else ALWAYS_TRUE
    )
    advanced_boss_combat = add_event("Advanced Boss Combat", REGION.FOREST,
        (lambda state: state.has_all([advanced_combat.event, quick_healing.event, year_round_survival.event], player)) if SEASON_GEAR_LOGIC
        else (lambda state: state.has_all([advanced_combat.event, quick_healing.event], player))
    )
    epic_combat = add_event("Epic Combat", REGION.FOREST,
        (lambda state: state.has(advanced_boss_combat.event, player)) if EXPERT_PLAYER_BIAS
        else lambda state: state.has_all([advanced_boss_combat.event, speed_boost.event, arena_building.event, character_switching.event, resurrecting.event], player)
    )
    ranged_combat = add_event("Ranged Combat", REGION.FOREST,
        (
            lambda state: (
                state.has(can_get_feathers.event, player)
                and (
                    state.has_all([winter.event, "Blow Dart"], player)
                    or state.has_all([canary.event, bird_caging.event, "Electric Dart"], player)
                )
            )
        ) if WEAPON_LOGIC else ALWAYS_TRUE
    )
    ranged_aggression = add_event("Ranged Aggression", REGION.FOREST,
        (
            lambda state: (
                state.has_all(["Boomerang", "Boards", charcoal.event], player)
                or (
                    state.has(can_get_feathers.event, player)
                    and (
                        state.has("Sleep Dart", player) or
                        state.has_all(["Fire Dart", charcoal.event], player)
                    )
                )
                or state.has_any([ranged_combat.event, ice_staff.event, fire_staff.event, cannon.event, "Walter"], player) # TODO: character logic
            )
        ) if WEAPON_LOGIC else ALWAYS_TRUE
    )
    dark_magic = add_event("Dark Magic", REGION.FOREST,
        combine_rules(
            (lambda state: state.has_all([nightmare_fuel.event, basic_sanity_management.event], player)),
            (
                lambda state: (
                    state.has("Dark Sword", player)
                    or (state.has_all(["Bat Bat", purple_gem.event], player))
                    or state.has_all(["Papyrus", "Night Armor"], player)
                )
            ) if WEAPON_LOGIC else ALWAYS_TRUE
        )
    )


    ##### HEALING #####
    basic_sanity_management = add_event("Basic Sanity Management", REGION.FOREST, lambda state: state.has("Top Hat", player)) # TODO: Walter doesn't get sanity from fashion
    nonperishable_quick_healing = add_event("Nonperishable Quick Healing", REGION.FOREST,
       (
           lambda state: (
                state.has_all(["Healing Salve", firestarting.event, mining.event], player) # Ash and rocks
                or state.has_all(["Honey Poultice", "Papyrus", honey_farming.event], player)
                or (WEAPON_LOGIC and state.has_all(["Bat Bat", purple_gem.event], player))
           )
       ) if HEALING_LOGIC
       else ALWAYS_TRUE
    )
    quick_healing = add_event("Quick Healing", REGION.FOREST,
        (lambda state: state.has_any([cooking.event, nonperishable_quick_healing.event], player)) if HEALING_LOGIC # TODO: Wormwood can't heal from food 
        else ALWAYS_TRUE
    )
    slow_healing = add_event("Slow Healing", REGION.FOREST,
        (
            lambda state: (
                state.has_all(["Tent", "Rope"], player)
                or state.has_all(["Siesta Lean-to", "Rope", "Boards", chopping.event], player)
                or (REGION.CAVE in REGION_WHITELIST and state.has_all(["Rope", "Straw Roll", "Fur Roll", mining.event, basic_combat.event, basic_sanity_management.event], player))
            )
            # TODO: Wickerbottom can't sleep
        ) if HEALING_LOGIC
        else ALWAYS_TRUE
    )
    healing = add_event("Healing", REGION.FOREST,
        (
            lambda state: (
                state.has_all(["Booster Shot", basic_sanity_management.event], player)
                and state.has_any([quick_healing.event, slow_healing.event], player)
            )
        ) if HEALING_LOGIC
        else (lambda state: state.has("Booster Shot", player)) if EXPERT_PLAYER_BIAS
        else (lambda state: state.has_all(["Booster Shot", basic_sanity_management.event], player))
    )
    resurrecting = add_event("Resurrecting", REGION.FOREST,
        (lambda state:
            state.has_all(["Life Giving Amulet", gem_digging.event, nightmare_fuel.event], player)
            or state.has_all(["Meat Effigy", "Boards", chopping.event, healing.event], player)
        ) if HEALING_LOGIC
        else ALWAYS_TRUE
    )


    ##### SURVIVAL #####
    basic_survival = add_event("Basic Survival", REGION.FOREST, 
        ALWAYS_TRUE if not CREATURE_LOCATIONS_ENABLED # Ignore basic survival in favor of having a sphere 1 with creature locations off
        else (
            lambda state: (
                state.has(firestarting.event, player)
                or state.has_all(["Straw Roll", "Rope"], player)
            )
        ) if EXPERT_PLAYER_BIAS
        else (
            lambda state: (
                state.has(firestarting.event, player)
                and state.has_any(["Axe", "Pickaxe"], player) # Have a flint tool at least
            )
        )
    )
    thermal_stone = add_event("Thermal Stone", REGION.FOREST, lambda state: state.has_all(["Thermal Stone", "Pickaxe"], player))
    winter_survival = add_event("Winter Survival", REGION.FOREST,
        (
            lambda state: (
                state.has_all([firestarting.event, shaving.event, thermal_stone.event, "Rabbit Earmuffs", "Pickaxe"], player)
                and state.has_any(["Puffy Vest", "Beefalo Hat", "Winter Hat", "Cat Cap"], player)
                and state.has_any(["Campfire", "Fire Pit"], player)
            )
        ) if SEASON_GEAR_LOGIC
        else (lambda state: state.has(firestarting.event, player))
    )
    electric_insulation = add_event("Electric Insulation", REGION.FOREST, lambda state:
        False if not state.has(hammering.event, player) # Everything requires bones and/or moleworms
        else (
            state.has_all(["Rain Coat", "Rope"], player)
            or state.has_all(["Rain Hat", "Straw Hat"], player)
            or state.has_all(["Eyebrella", deerclops.event], player)
        )
    )
    lightning_rod = add_event("Lightning Rod", REGION.FOREST if SEASON_GEAR_LOGIC else REGION.NONE, lambda state:
        state.has_all(["Lightning Rod", "Cut Stone"], player)
        or state.has_all(["Lightning Conductor", "Mast Kit", "Rope", "Boards"], player)
    )
    spring_survival = add_event("Spring Survival", REGION.FOREST,
        (
            lambda state: (
                state.has_any([electric_insulation.event, "Umbrella"], player)
                and state.has_all(["Straw Hat", "Pretty Parasol", lightning_rod.event], player) # Ensure basic stuff at this point
            )
        ) if SEASON_GEAR_LOGIC
        else ALWAYS_TRUE
    )
    has_cooling_source = add_event("Has Cooling Source", REGION.FOREST if SEASON_GEAR_LOGIC else REGION.NONE, lambda state:
        state.has_all([thermal_stone.event, "Ice Box", "Cut Stone"], player)
        or state.has_any(["Endothermic Fire", "Chilled Amulet"], player)
        or state.has_all(["Endothermic Fire Pit", electrical_doodad.event], player)
    )
    has_summer_insulation = add_event("Has Summer Insulation", REGION.FOREST if SEASON_GEAR_LOGIC else REGION.NONE, lambda state:
        state.has_any(["Umbrella", "Summer Frest", thermal_stone.event], player)
        or state.has_all(["Floral Shirt", "Papyrus"], player)
        or state.has_all(["Eyebrella", deerclops.event], player)
    )
    fire_suppression = add_event("Fire Suppression", REGION.FOREST, lambda state:
        False if not state.has(base_making.event, player)
        else (
            state.has_all([gears.event, "Ice Flingomatic"], player)
            or state.has_all(["Luxury Fan", moosegoose.event], player)
            or state.has("Empty Watering Can", player)
        )
    )
    summer_survival = add_event("Summer Survival", REGION.FOREST,
        (
            lambda state: state.has_all([has_cooling_source.event, has_summer_insulation.event, fire_suppression.event, "Straw Hat", "Pretty Parasol", "Whirly Fan"], player)
        ) if SEASON_GEAR_LOGIC
        else ALWAYS_TRUE
    )
    autumn_survival = add_event("Autumn Survival", REGION.FOREST,
        ALWAYS_TRUE if EXPERT_PLAYER_BIAS
        else lambda state: (
            state.has(basic_combat.event, player)
            and (not REGION.OCEAN in REGION_WHITELIST or state.has(basic_boating.event, player))
            and (not REGION.CAVE in REGION_WHITELIST or state.has(cave_exploration.event, player))
        )
    )
    year_round_survival = add_event("Year-Round Survival", REGION.FOREST, lambda state:
        state.has_all([winter_survival.event, spring_survival.event, summer_survival.event], player)
    )
    late_game_survival = add_event("Late Game Survival", REGION.FOREST,
        combine_rules(
            (lambda state: state.has_all([
                seasons_passed_4.event,
                epic_combat.event,
                cooking.event,
                basic_farming.event,
                bird_caging.event,
                honey_farming.event,
                dark_magic.event
            ], player)),
            (
                (lambda state: state.has(advanced_boating.event, player)) if REGION.OCEAN in REGION_WHITELIST
                else ALWAYS_TRUE
            )
        )
    )


    ##### BASE MAKING #####
    base_making = add_event("Base Making", REGION.FOREST,
        combine_rules(
            (lambda state: state.has_all(["Boards", "Cut Stone", "Electrical Doodad", "Rope", chopping.event, mining.event], player)),
            (
                (lambda state: state.has_all(["Chest", "Ice Box", "Fire Pit"], player)) if BASE_MAKING_LOGIC
                else ALWAYS_TRUE
            )
        )
    )
    fencing = add_event("Fencing", REGION.FOREST,
        (
            lambda state: (
                state.has_all([base_making.event, "Wood Gate and Fence"], player)
                and state.has_any(["Hay Wall", "Wood Wall", "Stone Wall"], player)
            )
        ) if BASE_MAKING_LOGIC else ALWAYS_TRUE
    )
    beefalo_domestication = add_event("Beefalo Domestication", REGION.FOREST,
        combine_rules(
            (lambda state: state.has_all(["Saddle", "Beefalo Hat", "Beefalo Bell"], player)),
            (
                (lambda state: state.has(fencing.event, player)) if BASE_MAKING_LOGIC
                else ALWAYS_TRUE
            )
        )
    )
    heavy_lifting = add_event("Heavy Lifting", REGION.FOREST, lambda state:
        state.has(beefalo_domestication.event, player)
        # or state.has_any(["Walter", "Wolfgang"], player) # Woby, mightiness # TODO: character logic
        # or state.has_all(["Wanda", winter.event, purple_gem.event], player) # Rift Watch # TODO: character logic
    )
    arena_building = add_event("Arena Building", REGION.FOREST,
        (
            lambda state: (
                (
                    state.has_any(["Pitchfork", "Snazzy Pitchfork"], player)
                    or state.has_all([antlion.event, "Turf-Raiser Helm", shaving.event], player)
                )
                and (
                    state.has_all(["Floorings", "Cut Stone", mining.event], player)
                    # or state.has("Wurt", player) # TODO: character logic
                )
            )
        ) if BASE_MAKING_LOGIC
        else ALWAYS_TRUE
    )
    character_switching = add_event("Character Switching", REGION.FOREST,
        combine_rules(
            (lambda state: state.has_all(["Cratered Moonrock", "Boards", "Rope", purple_gem.event], player)), # Crafting ingredients for moonrock portal
            combine_rules(
                (
                    ALWAYS_TRUE if is_locked("Moon Rock Idol") and is_locked("Portal Paraphernalia")
                    else (lambda state: state.has(celestial_orb.event, player)) # If either aren't shuffled, you'd have to make it at the celestial orb
                ),
                combine_rules(
                    (lambda state: state.has("Moon Rock Idol", player)) if is_locked("Moon Rock Idol") else ALWAYS_TRUE,
                    (lambda state: state.has("Portal Paraphernalia", player)) if is_locked("Portal Paraphernalia") else ALWAYS_TRUE
                )
            )
        ) if CHARACTER_SWITCHING_LOGIC
        else ALWAYS_TRUE
    )
    wall_building = add_event("Wall Building", REGION.FOREST,
        either_rule(
            (lambda state: state.has_all([base_making.event, "Stone Wall", "Potter's Wheel"], player)), # Sculptures are specifically pretty good for messing with mob pathfinding during moon stone event
            (
                ALWAYS_FALSE if not ADVANCED_PLAYER_BIAS
                else (lambda state: state.has_all(["Thulecite Wall", thulecite.event], player)) if is_locked("Thulecite Wall")
                else (lambda state: state.has_all([ancient_altar.event, thulecite.event], player)) # Can otherwise make walls at ancient altar
            )
        )
    )


    ##### EXPLORATION #####
    basic_exploration = add_event("Basic Exploration", REGION.FOREST,
        ALWAYS_TRUE if EXPERT_PLAYER_BIAS
        else lambda state: state.has_all(["Telltale Heart", "Torch", "Campfire", basic_survival.event, backpack.event, chopping.event, mining.event], player)
    )
    desert_exploration = add_event("Desert Exploration", REGION.FOREST,
        ALWAYS_TRUE if ADVANCED_PLAYER_BIAS
        else (lambda state: state.has_all([basic_survival.event, pre_basic_combat.event], player))
    )
    swamp_exploration = add_event("Swamp Exploration", REGION.FOREST,
        ALWAYS_TRUE if ADVANCED_PLAYER_BIAS
        else (lambda state: state.has_all([basic_survival.event, healing.event], player))
    )
    advanced_exploration = add_event("Advanced Exploration", REGION.FOREST,
        ALWAYS_TRUE if EXPERT_PLAYER_BIAS
        else lambda state: state.has_all([basic_exploration.event, speed_boost.event, digging.event, hammering.event], player)
    )
    speed_boost = add_event("Speed Boost", REGION.FOREST,
        either_rule(
            lambda state: state.has_all(["Walking Cane", winter.event], player),
            (
                ALWAYS_FALSE if not ADVANCED_PLAYER_BIAS # Encourage getting walking cane for easy difficulty
                else (lambda state: state.has_all([thulecite.event, ruins_gems.event, nightmare_fuel.event, "Magiluminescence"], player)) if is_locked("Magiluminescence")
                else (lambda state: state.has(ancient_altar.event, player))
            )
        )
    )
    light_source = add_event("Light Source", REGION.FOREST,
        (
            either_rule (
                (
                    (lambda state: state.has_all(["Lantern", "Rope"], player)) if REGION.CAVE in REGION_WHITELIST
                    else (lambda state: state.has_all(["Lantern", "Rope", sea_fishing.event], player)) # Skittersquids
                ),
                lambda state: (
                    state.has_all(["Miner Hat", bug_catching.event, "Straw Hat"], player)
                    or (ADVANCED_PLAYER_BIAS and state.has(morning_star.event, player))
                )
            )
        ) if LIGHTING_LOGIC
        else (lambda state: state.has("Torch", player))
    )
    cave_exploration = add_event("Cave Exploration", REGION.CAVE,
        (lambda state: state.has_all([mining.event, light_source.event], player)) if EXPERT_PLAYER_BIAS # Expert players just get a torch and pickaxe
        else (lambda state: state.has_all([light_source.event, basic_exploration.event, base_making.event], player)) # Have a base, backpack, and tools at this point
    )
    ruins_exploration = add_event("Ruins Exploration", REGION.RUINS,
        (lambda state: state.has(cave_exploration.event, player)) if EXPERT_PLAYER_BIAS
        else combine_rules(
            (
                lambda state: (
                    state.has_all([cave_exploration.event, advanced_combat.event], player)
                    or state.has_all([cave_exploration.event, healing.event, basic_combat.event], player)
                )
            ),
            (lambda state: state.has(cooking.event, player)) if BASE_MAKING_LOGIC # Allow cooking for easy difficulty
            else ALWAYS_TRUE
        )
    )
    basic_boating = add_event("Basic Boating", REGION.OCEAN, lambda state:
        state.has_all([basic_exploration.event, "Boat Kit", "Boards", "Oar", "Grass Raft Kit", "Boat Patch"], player)
    )
    pre_basic_boating = basic_boating if not EXPERT_PLAYER_BIAS else add_event("Pre-Basic Boating", REGION.OCEAN,
        lambda state: (
            state.has_any(["Oar", "Driftwood Oar"], player)
            and (
                state.has("Grass Raft Kit", player)
                or state.has_all(["Boat Kit", "Boards", chopping.event], player)
            )
        )
    )
    advanced_boating = add_event("Advanced Boating", REGION.OCEAN,
        combine_rules(
            (lambda state: state.has_all(["Driftwood Oar", basic_boating.event, light_source.event, base_making.event], player)),
            (
                ALWAYS_TRUE if EXPERT_PLAYER_BIAS
                else lambda state: state.has_all(["Anchor Kit", "Steering Wheel Kit", "Mast Kit"], player)
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
                # ,
                # (
                #     (lambda state: weregoose(state)) if CHARACTER_LOGIC # TODO: Character logic
                #     else ALWAYS_FALSE
                # )
        )
    )
    lunar_island = can_reach_islands
    hermit_island = add_event("Hermit Island", REGION.OCEAN, lambda state: state.has_all([cooking.event, base_making.event, can_reach_islands.event], player))
    hermit_sea_quests = add_event("Hermit Sea Quests", REGION.OCEAN,
        (lambda state: state.has(sea_fishing.event, player)) if ADVANCED_PLAYER_BIAS
        else lambda state: state.has_all([sea_fishing.event, advanced_boating.event], player)
    )
    archive_exploration = add_event("Archive Exploration", REGION.ARCHIVE, lambda state:
        state.has_all([iridescent_gem.event, healing.event], player)
    )
    storm_protection = add_event("Storm Protection", REGION.FOREST, lambda state:
        state.has_all(["Fashion Goggles", "Desert Goggles"], player)
        or (
            state.has("Astroggles", player) and (
                EXPERT_PLAYER_BIAS # Digging potato from junk pile
                or state.has(potato_farming.event, player) # Farming potato
            )
        )
    )
    moonstorm_exploration = add_event("Moonstorm Exploration", REGION.MOONSTORM, lambda state:
        state.has_all([unite_celestial_altars.event, storm_protection.event, electric_insulation.event], player) # Moonstorms have started; Moongleams
    )
    moon_quay_exploration = can_reach_islands if EXPERT_PLAYER_BIAS else add_event("Moon Quay Exploration", REGION.MOONQUAY,
        (lambda state: state.has_all([can_reach_islands.event, ruins_exploration.event], player)) if REGION.RUINS in REGION_WHITELIST # Encourage getting bananas from ruins, if enabled
        else (lambda state: state.has(can_reach_islands.event, player))
    )
    can_defend_against_pirates = add_event("Can Defend Against Pirates", REGION.MOONQUAY,
        ALWAYS_TRUE if EXPERT_PLAYER_BIAS
        else lambda state: state.has_all([cannon.event, basic_combat.event], player)
    )
    pirate_map = add_event("Pirate Map", REGION.MOONQUAY, lambda state:
        state.has_all([can_defend_against_pirates.event, moon_quay_exploration.event, hostile_flare.event, pre_basic_boating.event], player)
    )
    sunken_chest = add_event("Sunken Chest", REGION.OCEAN, lambda state:
        state.has_all(["Pinchin' Winch", advanced_boating.event], player)
        and state.has_any([hammering.event, deconstruction_staff.event], player)
    )


    ##### FARMING #####
    basic_farming = add_event("Basic Farming", REGION.FOREST, lambda state:
        state.has("Wormwood", player) or ( # Wormwood can plant directly on the ground
            state.has_any(["Garden Hoe", "Splendid Garden Hoe"], player)
            and state.has_all(["Garden Digamajig", "Rope", "Boards", chopping.event, digging.event], player)
        )
    )
    advanced_farming = add_event("Advanced Farming", REGION.FOREST, lambda state:
        # Implied you have chopping, rope, and boards already
        state.has_any(["Wormwood", "Garden Hoe", "Splendid Garden Hoe"], player)
        and state.has_all(["Garden Digamajig", "Empty Watering Can", base_making.event, digging.event], player)
         # TODO: Wes can't talk to plants 
    )
    asparagus_farming = add_farming_event("Asparagus", winter.event)
    garlic_farming = add_farming_event("Garlic", winter.event)
    pumpkin_farming = add_farming_event("Pumpkin", winter.event)
    corn_farming = add_farming_event("Corn", spring.event,
        (lambda state: state.has_all([basic_farming.event, bird_caging.event], player)) if EXPERT_PLAYER_BIAS # Catcoons
        else (lambda state: state.has_all([basic_farming.event, bird_caging.event, sea_fishing.event], player)) if ADVANCED_PLAYER_BIAS # Corn cod
        else None
    )
    onion_farming = add_farming_event("Onion", spring.event)
    potato_farming = add_farming_event("Potato", winter.event,
        (lambda state: state.has_all([basic_farming.event, bird_caging.event], player)) if ADVANCED_PLAYER_BIAS else None # Junk pile
    )
    dragonfruit_farming = add_farming_event("Dragon Fruit", spring.event,
        (lambda state: state.has_all([dragonfruit_from_saladmander.event, bird_caging.event], player)) if ADVANCED_PLAYER_BIAS else None # Saladmander
    )
    pomegranate_farming = add_farming_event("Pomegranate", spring.event)
    eggplant_farming = add_farming_event("Eggplant", spring.event)
    tomaroot_farming = add_farming_event("Toma Root", spring.event,
        (lambda state: state.has(basic_farming.event, player)) if EXPERT_PLAYER_BIAS else None # Catcoons
    )
    watermelon_farming = add_farming_event("Watermelon", spring.event)
    pepper_farming = add_farming_event("Pepper", summer.event)
    durian_farming = add_farming_event("Durian", spring.event)
    carrot_farming = add_farming_event("Carrot", bird_caging.event)
    honey_farming = add_event("Honey Farming", REGION.FOREST,
        (lambda state: state.has_all(["Bee Box", "Boards", bug_catching.event], player)) if BASE_MAKING_LOGIC
        else ALWAYS_TRUE
    )


    ##### COOKING #####
    cooking = add_event("Cooking", REGION.FOREST,
        ALWAYS_TRUE if WARLY_DISHES_ENABLED
        else lambda state: state.has_all(["Cut Stone", "Crock Pot", charcoal.event, mining.event], player)
    )
    fruits = add_event("Fruits", REGION.FOREST, lambda state:
        state.has_any([pomegranate_farming.event, watermelon_farming.event, durian_farming.event, ruins_exploration.event], player)
    )
    dragonfruit_from_saladmander = add_event("Dragon Fruit from Saladmander", REGION.OCEAN,
        combine_rules(
            (lambda state: state.has_all([lunar_island.event, basic_combat.event], player)),
            (lambda state: state.has("Bath Bomb", player)) if is_locked("Bath Bomb")
            else ALWAYS_TRUE
        )
    )
    dairy = add_event("Dairy", REGION.FOREST,
        either_rule(
            (
                ALWAYS_TRUE if EXPERT_PLAYER_BIAS
                else lambda state: state.has(butter_luck.event, player)
            ),
            lambda state: (
                state.has(eye_of_terror.event, player) # Milky whites
                or ( # Electric milk
                    state.has_all([morning_star.event, electric_insulation.event], player)
                    or state.has_all([canary.event, bird_caging.event, "Electric Dart"], player)
                )
            )
        )
    )


    ##### FISHING #####
    freshwater_fishing = add_event("Freshwater Fishing", REGION.FOREST, lambda state: state.has("Freshwater Fishing Rod", player))
    sea_fishing = add_event("Sea Fishing", REGION.OCEAN,
        combine_rules(
            (
                lambda state: (
                    state.has_all([pre_basic_boating.event, "Rope", "Boards"], player)
                    and state.has_any(["Ocean Trawler Kit", "Sea Fishing Rod"], player)
                )
            ),
            (
                (lambda state: state.has_all(["Tin Fishin' Bin", "Cut Stone", "Rope"], player)) if BASE_MAKING_LOGIC
                else ALWAYS_TRUE
            )
        )
    )
    fishing = add_event("Fishing", REGION.FOREST, lambda state: state.has_any([freshwater_fishing.event, sea_fishing.event], player))


    ##### KEY ITEMS #####
    celestial_sanctum_pieces = add_event("Celestial Sanctum Pieces", REGION.OCEAN, lambda state:
        state.has_all([thulecite.event, "Astral Detector", heavy_lifting.event], player)
    )
    moon_stone_event = add_event("Moon Stone Event", REGION.FOREST if is_locked("Star Caller's Staff") else REGION.RUINS, lambda state:
        (
            (EXPERT_PLAYER_BIAS or state.has(wall_building.event, player))
            and has_survived_num_days(11, state) # First full moon
        )
        and (
            state.has_all([nightmare_fuel.event, ruins_gems.event, "Star Caller's Staff"], player) if is_locked("Star Caller's Staff")
            else state.has_all([nightmare_fuel.event, ancient_altar.event], player)
        )
    )
    iridescent_gem = add_event("Iridescent Gem", REGION.FOREST if is_locked("Deconstruction Staff") else REGION.RUINS,
        (lambda state: state.has_all([mooncaller_staff.event, deconstruction_staff.event], player)) if is_locked("Deconstruction Staff")
        else (lambda state: state.has(mooncaller_staff.event, player)) # Should already be able to craft Deconstruction Staff
    )
    unite_celestial_altars = add_event("Unite Celestial Altars", REGION.MOONSTORM, lambda state:
        state.has_all([lunar_island.event, celestial_sanctum_pieces.event, inactive_celestial_tribute.event, "Pinchin' Winch"], player)
    )
    inactive_celestial_tribute = add_event("Inactive Celestial Tribute", REGION.OCEAN, lambda state: state.has(crab_king.event, player))
    shadow_atrium = add_event("Shadow Atrium", REGION.RUINS, 
        (lambda state: state.has_all(["Bishop Figure Sketch", "Rook Figure Sketch", "Knight Figure Sketch", shadow_pieces.event], player)) if CHESSPIECE_ITEMS_SHUFFLED
        else (lambda state: state.has(shadow_pieces.event, player))
    )
    ancient_key = add_event("Ancient Key", REGION.RUINS, lambda state: state.has(ancient_guardian.event, player))


    ##### CRAFTING STATIONS #####
    science_machine = add_event("Science Machine", REGION.FOREST, lambda state: state.has_all([basic_survival.event, chopping.event, mining.event], player))
    alchemy_engine = add_event("Alchemy Engine", REGION.FOREST, lambda state: state.has_all([base_making.event, science_machine.event], player))
    prestihatitor = add_event("Prestihatitor", REGION.FOREST, lambda state: state.has_all(["Top Hat", "Boards", science_machine.event, "Trap"], player))
    shadow_manipulator = add_event("Shadow Manipulator", REGION.FOREST, lambda state: state.has_all([purple_gem.event, nightmare_fuel.event, prestihatitor.event], player))
    think_tank = add_event("Think Tank", REGION.OCEAN, lambda state: state.has_all(["Boards", science_machine.event], player))
    ancient_altar = add_event("Ancient Pseudoscience Station", REGION.RUINS, lambda state: state.has(ruins_exploration.event, player))
    celestial_orb = add_event("Celestial Orb", REGION.FOREST, lambda state: has_survived_num_days(5, state) and state.has(mining.event, player))
    celestial_altar = add_event("Celestial Altar", REGION.OCEAN, lambda state:
        state.has(lunar_island.event, player)
        and (
            state.has(mining.event, player)
            # or state.has(celestial_sanctum_pieces.event, player) TODO: Mcguffin logic
            # or state.has(inactive_celestial_tribute.event, player)
        )
    )

    ##### BOSSES #####
    crab_king = add_boss_event("Crab King", REGION.OCEAN, lambda state:
        state.has_all([advanced_boating.event, advanced_boss_combat.event], player)
        and state.count("Crabby Hermit Friendship", player) >= 10
    )
    shadow_pieces = add_event("Shadow Pieces", REGION.FOREST,
        lambda state: (
            state.has_all([advanced_boss_combat.event, heavy_lifting.event, base_making.event, "Potter's Wheel", arena_building.event], player)
            ## TODO: This line probably doesn't work the way I want it to, so disabling
            # and (state.has(celestial_champion.event, player) or not state.has(unite_celestial_altars.event, player)) # Can't happen during moonstorms
        )
    )
    ancient_guardian = add_boss_event("Ancient Guardian", REGION.RUINS, lambda state: state.has_all([ruins_exploration.event, advanced_boss_combat.event], player))
    deerclops = add_boss_event("Deerclops", REGION.FOREST, lambda state: state.has_all([basic_combat.event, winter.event, seasons_passed_1.event], player))
    moosegoose = add_boss_event("Moose/Goose", REGION.FOREST, lambda state: state.has_all([basic_combat.event, spring.event, seasons_passed_2.event], player)) # Beginning of spring has to be at least 1.5 seasons in
    antlion = add_boss_event("Antlion", REGION.FOREST, lambda state:
        (
            state.has_all([freshwater_fishing.event, "Fashion Goggles", "Desert Goggles"], player) # Affects chance of fishing beach toy
            or state.has_all([advanced_boss_combat.event, thermal_stone.event, storm_protection.event], player) # Minimum for expert difficulty
        )
        and state.has(summer.event, player)
    )
    bearger = add_boss_event("Bearger", REGION.FOREST, lambda state: state.has_all([basic_combat.event, autumn.event, seasons_passed_1.event], player)) # TODO: Verify bearger's spawn conditions
    dragonfly = add_boss_event("Dragonfly", REGION.FOREST, lambda state: state.has_all([advanced_boss_combat.event, wall_building.event], player))
    bee_queen = add_boss_event("Bee Queen", REGION.FOREST, lambda state: state.has_all([epic_combat.event, hammering.event, beekeeper_hat.event], player))
    klaus = add_boss_event("Klaus", REGION.FOREST, lambda state: state.has_all([advanced_boss_combat.event, winter.event], player))
    malbatross = add_boss_event("Malbatross", REGION.OCEAN, lambda state: state.has_all([advanced_boss_combat.event, advanced_boating.event], player))
    toadstool = add_boss_event("Toadstool", REGION.CAVE,
        combine_rules(
            (lambda state: state.has_all([basic_combat.event, nonperishable_quick_healing.event, cave_exploration.event], player)),
            (
                lambda state: (
                    state.has_any(["Moon Glass Axe", "Woodie", pick_axe.event, weather_pain.event], player) # Dealing with sporecaps
                    and state.has(fire_staff.event, player)
                    and (
                        state.has("Dark Sword", player) # Nightmare fuel already required by fire staff
                        or state.has_all(["Glass Cutter", "Boards"], player)
                    )
                )
            ) if WEAPON_LOGIC
            else ALWAYS_TRUE
        )
    )
    ancient_fuelweaver = add_boss_event("Ancient Fuelweaver", REGION.RUINS,
        combine_rules(
            (
                (lambda state: state.has_all([shadow_atrium.event, ancient_key.event, advanced_boss_combat.event], player)) if EXPERT_PLAYER_BIAS
                else lambda state: (
                    state.has_all([shadow_atrium.event, ancient_key.event, dark_magic.event], player) # Requires nightmare fuel
                    and ( # Getting around obelisks
                        state.has("Nightmare Amulet", player)
                        or state.has_all(["The Lazy Explorer", "Walking Cane", winter.event], player)
                    )

                )
            ),
            (lambda state: state.has_any([weather_pain.event, "Wendy"], player)) if WEAPON_LOGIC # Dealing with woven shadows # TODO: Character logic
            else ALWAYS_TRUE
        )
    )
    lord_of_the_fruit_flies = add_boss_event("Lord of the Fruit Flies", REGION.FOREST, lambda state: state.has_all([basic_combat.event, advanced_farming.event, seasons_passed_2.event], player))
    celestial_champion = add_boss_event("Celestial Champion", REGION.MOONSTORM, lambda state:
        state.has_all(["Incomplete Experiment", celestial_orb.event, moonstorm_exploration.event, epic_combat.event, ranged_combat.event], player)
    )
    eye_of_terror = add_boss_event("Eye Of Terror", REGION.FOREST, lambda state: state.has(advanced_boss_combat.event, player))
    retinazor = add_boss_event("Retinazor", REGION.FOREST, lambda state: state.has(epic_combat.event, player))
    spazmatism = add_boss_event("Spazmatism", REGION.FOREST, lambda state: state.has(epic_combat.event, player))
    nightmare_werepig = add_boss_event("Nightmare Werepig", REGION.RUINS, lambda state: state.has_all([advanced_boss_combat.event, pick_axe.event, speed_boost.event], player))
    scrappy_werepig = add_boss_event("Scrappy Werepig", REGION.RUINS, lambda state: state.has_all([nightmare_werepig.event, arena_building.event], player))
    frostjaw = add_boss_event("Frostjaw", REGION.OCEAN, lambda state: state.has_all([advanced_boating.event, advanced_boss_combat.event, "Sea Fishing Rod"], player))

    # Events
    hermit_home_upgrade_1 = add_hermit_event("Hermit Home Upgrade (1)", lambda state: state.has_all([hermit_island.event, bug_catching.event], player)) # Cookie cutters, boards, fireflies
    hermit_home_upgrade_2 = add_hermit_event("Hermit Home Upgrade (2)", lambda state: state.can_reach_location(hermit_home_upgrade_1.event, player)) # Marble, cut stone, light bulb
    add_hermit_event("Hermit Home Upgrade (3)",                         lambda state: state.has("Floorings", player) and state.can_reach_location(hermit_home_upgrade_2.event, player)) # Moonrock, rope, carpet
    add_hermit_event("Hermit Island Drying Racks",                      hermit_island.rule)
    add_hermit_event("Hermit Island Plant 10 Flowers",                  lambda state: state.has_all([hermit_island.event, bug_catching.event], player))
    add_hermit_event("Hermit Island Plant 8 Berry Bushes",              lambda state: state.has_all([hermit_island.event, digging.event], player))
    add_hermit_event("Hermit Island Clear Underwater Salvageables",     lambda state: state.has_all([hermit_sea_quests.event, "Pinchin' Winch"], player))
    add_hermit_event("Hermit Island Kill Lureplant",                    lambda state: state.has_all([hermit_island.event, seasons_passed_2.event], player))
    add_hermit_event("Hermit Island Build Wooden Chair",                lambda state: state.has_all([hermit_island.event, "Sawhorse"], player))
    add_hermit_event("Give Crabby Hermit Umbrella",                     lambda state: state.has_all([hermit_island.event, spring.event], player) and state.has_any(["Umbrella", "Pretty Parasol"], player))
    add_hermit_event("Give Crabby Hermit Warm Clothing",                lambda state: state.has_all([hermit_island.event, winter.event], player) and state.has_any(["Breezy Vest", "Puffy Vest"], player))
    add_hermit_event("Give Crabby Hermit Flower Salad",                 lambda state: state.has_all([hermit_island.event, summer.event], player))
    add_hermit_event("Give Crabby Hermit Fallounder",                   lambda state: state.has_all([hermit_sea_quests.event, autumn.event], player))
    add_hermit_event("Give Crabby Hermit Bloomfin Tuna",                lambda state: state.has_all([hermit_sea_quests.event, spring.event], player))
    add_hermit_event("Give Crabby Hermit Scorching Sunfish",            lambda state: state.has_all([hermit_sea_quests.event, summer.event], player))
    add_hermit_event("Give Crabby Hermit Ice Bream",                    lambda state: state.has_all([hermit_sea_quests.event, winter.event], player))
    add_hermit_event("Give Crabby Hermit 5 Heavy Fish",                 hermit_sea_quests.rule)

    def survival_goal (state: CollectionState) -> bool:
        if options.goal.value != options.goal.option_survival: return False # Only relevant if your goal is to survive
        days_to_survive = options.days_to_survive.value
        if days_to_survive < 20:
            return state.has_all([advanced_boss_combat.event, autumn_survival.event], player) # Generic non-seasonal goal
        elif days_to_survive < 35:
            return state.has(seasons_passed_1.event, player)
        elif days_to_survive < 55:
            return state.has(seasons_passed_2.event, player)
        elif days_to_survive < 70:
            return state.has(seasons_passed_3.event, player)
        elif days_to_survive < 90:
            return state.has(seasons_passed_4.event, player)
        return state.has(seasons_passed_5.event, player)

    rules_lookup: Dict[str, Dict[str, Callable[[CollectionState], bool]]] = {
        # "regions": {
        #     REGION.CAVE: lambda state: REGION.CAVE in REGION_WHITELIST and state.has(mining.event, player), # Will mostly be used as a test
        #     REGION.ARCHIVE: lambda state: REGION.ARCHIVE in REGION_WHITELIST,
        #     REGION.RUINS: lambda state: REGION.RUINS in REGION_WHITELIST,
        #     REGION.OCEAN: lambda state: REGION.OCEAN in REGION_WHITELIST,
        #     REGION.MOONQUAY: lambda state: REGION.MOONQUAY in REGION_WHITELIST,
        #     REGION.MOONSTORM: lambda state: REGION.MOONSTORM in REGION_WHITELIST,
        #     REGION.DUALREGION: lambda state: REGION.OCEAN in REGION_WHITELIST or REGION.CAVE in REGION_WHITELIST,
        #     REGION.BOTHREGIONS: lambda state: REGION.OCEAN in REGION_WHITELIST and REGION.CAVE in REGION_WHITELIST,
        # },
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
            "Stagehand":                        lambda state: state.has_all([basic_survival.event, hammering.event], player),
            "Pirate Stash":                     lambda state: state.has_all([pirate_map.event, digging.event], player),
            "Moon Stone Event":                 moon_stone_event.rule,
            "Oasis":                            lambda state: state.has_all([freshwater_fishing.event, summer.event], player),
            "Poison Birchnut Tree":             lambda state: state.has_all([seasons_passed_4.event, autumn.event], player),
            "W.O.B.O.T.":                       lambda state: state.has(scrappy_werepig.event, player) or state.has_all(["Auto-Mat-O-Chanic", electrical_doodad.event], player),
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
            "Shadow Knight":                    (lambda state: state.has_all([shadow_pieces.event, "Knight Figure Sketch"], player)) if CHESSPIECE_ITEMS_SHUFFLED else shadow_pieces.rule,
            "Shadow Bishop":                    (lambda state: state.has_all([shadow_pieces.event, "Bishop Figure Sketch"], player)) if CHESSPIECE_ITEMS_SHUFFLED else shadow_pieces.rule,
            "Shadow Rook":                      (lambda state: state.has_all([shadow_pieces.event, "Rook Figure Sketch"], player)) if CHESSPIECE_ITEMS_SHUFFLED else shadow_pieces.rule,
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
            "Batilisk":                         lambda state: state.has_all([pre_basic_combat.event, mining.event], player),
            "Bee":                              lambda state: state.has_any([pre_basic_combat.event, bug_catching.event], player),
            "Beefalo":                          basic_survival.rule,
            "Clockwork Bishop":                 lambda state: state.has_all([advanced_combat.event, healing.event], player),
            "Bunnyman":                         cave_exploration.rule,
            "Butterfly":                        ALWAYS_TRUE,
            "Buzzard":                          basic_combat.rule,
            "Canary":                           lambda state: state.has_all([canary.event, can_get_feathers.event], player),
            "Carrat":                           lambda state: state.has_any([lunar_island.event, cave_exploration.event], player),
            "Catcoon":                          basic_survival.rule,
            "Cookie Cutter":                    advanced_boating.rule,
            "Crawling Horror":                  advanced_combat.rule,
            "Crow":                             can_get_feathers.rule,
            "Red Hound":                        lambda state: state.has_all([basic_combat.event, seasons_passed_2.event], player) and state.has_any([summer.event, autumn.event], player),
            "Frog":                             ALWAYS_TRUE,
            "Saladmander":                      lunar_island.rule,
            "Ghost":                            lambda state: state.has_all([basic_exploration.event, digging.event, pre_basic_combat.event], player),
            "Gnarwail":                         lambda state: state.has_all([basic_combat.event, advanced_boating.event], player),
            "Grass Gator":                      lambda state: state.has_all([basic_combat.event, advanced_boating.event, ranged_aggression.event], player),
            "Grass Gekko":                      lambda state: state.has_all([seasons_passed_2.event, digging.event], player) and state.has_any([autumn.event, spring.event, summer.event], player), # Not guaranteed on world gen so give time for spawned ones
            "Briar Wolf":                       basic_combat.rule,
            "Hound":                            lambda state: state.has_all([basic_combat.event, desert_exploration.event], player),
            "Blue Hound":                       lambda state: state.has_all([basic_combat.event, winter.event], player) or state.has_all([basic_combat.event, spring.event, seasons_passed_2.event], player),
            "Killer Bee":                       lambda state: state.has_any([pre_basic_combat.event, bug_catching.event], player),
            "Clockwork Knight":                 advanced_combat.rule,
            "Koalefant":                        lambda state: state.has_all([pre_basic_combat.event, ranged_aggression.event], player),
            "Krampus":                          lambda state: state.has_all([basic_combat.event, can_get_feathers.event, basic_survival.event], player),
            "Treeguard":                        lambda state: state.has_all([basic_combat.event, chopping.event, basic_survival.event], player),
            "Crustashine":                      lambda state: state.has_all([moon_quay_exploration.event, ranged_aggression.event], player),
            "Bulbous Lightbug":                 cave_exploration.rule,
            "Volt Goat":                        lambda state: state.has_all([basic_combat.event, ranged_aggression.event, desert_exploration.event], player),
            "Merm":                             lambda state: state.has_all([basic_combat.event, swamp_exploration.event], player),
            "Moleworm":                         ALWAYS_TRUE,
            "Naked Mole Bat":                   lambda state: state.has_all([basic_combat.event, cave_exploration.event], player),
            "Splumonkey":                       ruins_exploration.rule,
            "Moon Moth":                        can_reach_islands.rule,
            "Mosquito":                         lambda state: state.has(swamp_exploration.event, player) and (state.has_any([pre_basic_combat.event, bug_catching.event], player)),
            "Mosling":                          moosegoose.rule,
            "Mush Gnome":                       lambda state: state.has_all([basic_combat.event, cave_exploration.event], player),
            "Terrorclaw":                       lambda state: state.has_all([advanced_combat.event, advanced_boating.event], player),
            "Pengull":                          lambda state: state.has_all([basic_combat.event, winter.event], player),
            "Gobbler":                          basic_survival.rule,
            "Pig Man":                          basic_survival.rule,
            "Powder Monkey":                    lambda state: state.has_all([can_defend_against_pirates.event, moon_quay_exploration.event], player),
            "Prime Mate":                       pirate_map.rule,
            "Puffin":                           lambda state: state.has_all([can_get_feathers.event, pre_basic_boating.event], player),
            "Rabbit":                           ALWAYS_TRUE,
            "Redbird":                          can_get_feathers.rule,
            "Snowbird":                         lambda state: state.has_all([can_get_feathers.event, winter.event], player),
            "Rock Lobster":                     cave_exploration.rule,
            "Clockwork Rook":                   lambda state: state.has_all([advanced_combat.event, healing.event], player),
            "Rockjaw":                          lambda state: state.has_all([advanced_combat.event, advanced_boating.event], player) and (state.has_any([ranged_combat.event, cannon.event], player)),
            "Slurper":                          ruins_exploration.rule,
            "Slurtle":                          cave_exploration.rule,
            "Snurtle":                          cave_exploration.rule,
            "Ewecus":                           lambda state: state.has_all([advanced_combat.event, advanced_exploration.event, seasons_passed_4.event], player),
            "Spider":                           ALWAYS_TRUE,
            "Dangling Depth Dweller":           ruins_exploration.rule,
            "Cave Spider":                      lambda state: state.has_all([basic_combat.event, cave_exploration.event], player),
            "Nurse Spider":                     lambda state: state.has_all([advanced_combat.event, seasons_passed_2.event], player),
            "Shattered Spider":                 lambda state: state.has_all([basic_combat.event, lunar_island.event], player),
            "Spitter":                          lambda state: state.has_all([basic_combat.event, cave_exploration.event], player),
            "Spider Warrior":                   basic_combat.rule,
            "Sea Strider":                      lambda state: state.has_all([basic_combat.event, advanced_boating.event], player),
            "Spider Queen":                     lambda state: state.has_all([advanced_combat.event, seasons_passed_2.event], player),
            "Tallbird":                         lambda state: state.has_all([basic_combat.event, healing.event], player),
            "Tentacle":                         lambda state: state.has_all([basic_combat.event, swamp_exploration.event], player),
            "Big Tentacle":                     lambda state: state.has_all([advanced_combat.event, cave_exploration.event, healing.event], player),
            "Terrorbeak":                       lambda state: state.has_all([advanced_combat.event, basic_sanity_management.event], player),
            "MacTusk":                          lambda state: state.has_all([basic_combat.event, winter.event], player),
            "Varg":                             lambda state: state.has_all([advanced_combat.event, advanced_exploration.event, seasons_passed_4.event], player),
            "Varglet":                          lambda state: state.has_all([basic_combat.event, advanced_exploration.event, seasons_passed_2.event], player),
            "Depths Worm":                      ruins_exploration.rule,
            "Ancient Sentrypede":               lambda state: state.has_all([archive_exploration.event, advanced_combat.event], player),
            "Skittersquid":                     lambda state: state.has_all([basic_combat.event, advanced_boating.event], player),
            "Lure Plant":                       spring.rule,
            "Glommer":                          lambda state: has_survived_num_days(11, state),
            "Dust Moth":                        archive_exploration.rule,
            "No-Eyed Deer":                     winter.rule,
            "Moonblind Crow":                   lambda state: state.has_all([moonstorm_exploration.event, basic_combat.event], player),
            "Misshapen Bird":                   lambda state: state.has_all([moonstorm_exploration.event, basic_combat.event], player),
            "Moonrock Pengull":                 lambda state: state.has_all([lunar_island.event, basic_combat.event, winter.event], player),
            "Horror Hound":                     lambda state: state.has_all([moonstorm_exploration.event, basic_combat.event], player),
            "Resting Horror":                   ruins_exploration.rule,
            "Birchnutter":                      lambda state: state.has_all([seasons_passed_4.event, autumn.event], player),
            "Mandrake":                         basic_survival.rule,
            "Fruit Fly":                        lambda state: state.has_all([basic_farming.event, seasons_passed_2.event], player),
            "Sea Weed":                         advanced_boating.rule,
            "Marotter":                         basic_combat.rule,

            # Cook foods
            "Butter Muffin":                    ALWAYS_TRUE,
            "Froggle Bunwich":                  ALWAYS_TRUE,
            "Taffy":                            honey_farming.rule,
            "Pumpkin Cookies":                  lambda state: state.has_all([honey_farming.event, pumpkin_farming.event], player),
            "Stuffed Eggplant":                 eggplant_farming.rule,
            "Fishsticks":                       fishing.rule,
            "Honey Nuggets":                    honey_farming.rule,
            "Honey Ham":                        honey_farming.rule,
            "Dragonpie":                        lambda state: state.has_any([dragonfruit_from_saladmander.event, dragonfruit_farming.event], player),
            "Kabobs":                           ALWAYS_TRUE,
            "Mandrake Soup":                    ALWAYS_TRUE,
            "Bacon and Eggs":                   bird_caging.rule,
            "Meatballs":                        ALWAYS_TRUE,
            "Meaty Stew":                       ALWAYS_TRUE,
            "Pierogi":                          bird_caging.rule,
            "Turkey Dinner":                    pre_basic_combat.rule,
            "Ratatouille":                      ALWAYS_TRUE,
            "Fist Full of Jam":                 ALWAYS_TRUE,
            "Fruit Medley":                     fruits.rule,
            "Fish Tacos":                       lambda state: state.has_any([sea_fishing.event, corn_farming.event], player),
            "Waffles":                          lambda state: state.has_all([bird_caging.event, butter_luck.event], player),
            "Monster Lasagna":                  lambda state: state.has_all(["Cut Stone", "Crock Pot", charcoal.event, mining.event, pre_basic_combat.event], player), # Need basic crock pot, not portable
            "Powdercake":                       lambda state: state.has(honey_farming.event, player) and state.has_any([sea_fishing.event, corn_farming.event], player),
            "Unagi":                            lambda state: state.has_all([cave_exploration.event, freshwater_fishing.event], player),
            "Wet Goop":                         ALWAYS_TRUE,
            "Flower Salad":                     summer.rule,
            "Ice Cream":                        lambda state: state.has_all([honey_farming.event, dairy.event], player),
            "Melonsicle":                       watermelon_farming.rule,
            "Trail Mix":                        chopping.rule,
            "Spicy Chili":                      ALWAYS_TRUE,
            "Guacamole":                        ALWAYS_TRUE,
            "Jellybeans":                       bee_queen.rule,
            "Fancy Spiralled Tubers":           potato_farming.rule,
            "Creamy Potato Purée":              lambda state: state.has_all([potato_farming.event, garlic_farming.event], player),
            "Asparagus Soup":                   asparagus_farming.rule,
            "Vegetable Stinger":                lambda state: state.has_any([tomaroot_farming.event, asparagus_farming.event], player),
            "Banana Pop":                       lambda state: state.has_any([cave_exploration.event, moon_quay_exploration.event], player),
            "Frozen Banana Daiquiri":           lambda state: state.has_any([cave_exploration.event, moon_quay_exploration.event], player),
            "Banana Shake":                     lambda state: state.has_any([cave_exploration.event, moon_quay_exploration.event], player),
            "Ceviche":                          fishing.rule,
            "Salsa Fresca":                     tomaroot_farming.rule,
            "Stuffed Pepper Poppers":           pepper_farming.rule,
            "California Roll":                  sea_fishing.rule,
            "Seafood Gumbo":                    lambda state: state.has_all([cave_exploration.event, freshwater_fishing.event], player),
            "Surf 'n' Turf":                    fishing.rule,
            "Lobster Bisque":                   sea_fishing.rule,
            "Lobster Dinner":                   lambda state: state.has_all([sea_fishing.event, butter_luck.event], player),
            "Barnacle Pita":                    lambda state: state.has_all([sea_fishing.event, shaving.event], player),
            "Barnacle Nigiri":                  lambda state: state.has_all([sea_fishing.event, shaving.event], player),
            "Barnacle Linguine":                lambda state: state.has_all([sea_fishing.event, shaving.event], player),
            "Stuffed Fish Heads":               lambda state: state.has_all([sea_fishing.event, shaving.event], player),
            "Leafy Meatloaf":                   leafy_meat.rule,
            "Veggie Burger":                    lambda state: state.has_all([leafy_meat.event, onion_farming.event], player),
            "Jelly Salad":                      lambda state: state.has_all([honey_farming.event, leafy_meat.event], player),
            "Beefy Greens":                     leafy_meat.rule,
            "Mushy Cake":                       cave_exploration.rule,
            "Soothing Tea":                     basic_farming.rule,
            "Fig-Stuffed Trunk":                sea_fishing.rule,
            "Figatoni":                         sea_fishing.rule,
            "Figkabab":                         sea_fishing.rule,
            "Figgy Frogwich":                   sea_fishing.rule,
            "Bunny Stew":                       ALWAYS_TRUE,
            "Plain Omelette":                   bird_caging.rule,
            "Breakfast Skillet":                bird_caging.rule,
            "Tall Scotch Eggs":                 basic_combat.rule,
            "Steamed Twigs":                    ALWAYS_TRUE,
            "Beefalo Treats":                   basic_farming.rule,
            "Milkmade Hat":                     lambda state: state.has_all([cave_exploration.event, pre_basic_boating.event, dairy.event], player),
            "Amberosia":                        lambda state: state.has_all([salt_crystals.event, "Collected Dust"], player),
            "Stuffed Night Cap":                cave_exploration.rule,
            # Warly Dishes
            "Grim Galette":                     lambda state: state.has_all([potato_farming.event, onion_farming.event], player),
            "Volt Goat Chaud-Froid":            basic_combat.rule,
            "Glow Berry Mousse":                cave_exploration.rule,
            "Fish Cordon Bleu":                 sea_fishing.rule,
            "Hot Dragon Chili Salad":           lambda state: state.has(pepper_farming.event, player) and state.has_any([dragonfruit_from_saladmander.event, dragonfruit_farming.event], player),
            "Asparagazpacho":                   asparagus_farming.rule,
            "Puffed Potato Soufflé":            lambda state: state.has_all([bird_caging.event, potato_farming.event], player),
            "Monster Tartare":                  pre_basic_combat.rule,
            "Fresh Fruit Crepes":               lambda state: state.has_all([fruits.event, butter_luck.event], player),
            "Bone Bouillon":                    lambda state: state.has_all([hammering.event, onion_farming.event], player),
            "Moqueca":                          lambda state: state.has_all([sea_fishing.event, tomaroot_farming.event], player),
            # Farming
            "Grow Giant Asparagus":             lambda state: state.has_all([asparagus_farming.event, spring.event], player),
            "Grow Giant Garlic":                lambda state: state.has_all([garlic_farming.event, winter.event], player),
            "Grow Giant Pumpkin":               lambda state: state.has_all([pumpkin_farming.event, winter.event], player),
            "Grow Giant Corn":                  lambda state: state.has_all([corn_farming.event, spring.event], player),
            "Grow Giant Onion":                 lambda state: state.has_all([onion_farming.event, spring.event], player),
            "Grow Giant Potato":                lambda state: state.has_all([potato_farming.event, winter.event], player),
            "Grow Giant Dragon Fruit":          lambda state: state.has_all([dragonfruit_farming.event, spring.event], player),
            "Grow Giant Pomegranate":           lambda state: state.has_all([pomegranate_farming.event, spring.event], player),
            "Grow Giant Eggplant":              lambda state: state.has_all([eggplant_farming.event, spring.event], player),
            "Grow Giant Toma Root":             lambda state: state.has_all([tomaroot_farming.event, spring.event], player),
            "Grow Giant Watermelon":            lambda state: state.has_all([watermelon_farming.event, spring.event], player),
            "Grow Giant Pepper":                lambda state: state.has_all([pepper_farming.event, summer.event], player),
            "Grow Giant Durian":                lambda state: state.has_all([durian_farming.event, spring.event], player),
            "Grow Giant Carrot":                lambda state: state.has_all([carrot_farming.event, winter.event], player),
            # Research
            "Science (Nitre)":                  mining.rule,
            "Science (Salt Crystals)":          salt_crystals.rule,
            "Science (Ice)":                    mining.rule,
            "Science (Slurtle Slime)":          cave_exploration.rule,
            "Science (Gears)":                  gears.rule,
            "Science (Scrap)":                  basic_exploration.rule,
            "Science (Azure Feather)":          lambda state: state.has_all([winter.event, can_get_feathers.event], player),
            "Science (Crimson Feather)":        can_get_feathers.rule,
            "Science (Jet Feather)":            can_get_feathers.rule,
            "Science (Saffron Feather)":        lambda state: state.has_all([canary.event, can_get_feathers.event], player),
            "Science (Kelp Fronds)":            pre_basic_boating.rule,
            "Science (Steel Wool)":             lambda state: state.has_all([advanced_combat.event, advanced_exploration.event, seasons_passed_4.event], player),
            "Science (Electrical Doodad)":      electrical_doodad.rule,
            "Science (Ashes)":                  firestarting.rule,
            "Science (Cut Grass)":              ALWAYS_TRUE,
            "Science (Beefalo Horn)":           basic_combat.rule,
            "Science (Beefalo Wool)":           basic_combat.rule if ADVANCED_PLAYER_BIAS else shaving.rule,
            "Science (Cactus Flower)":          summer.rule,
            "Science (Honeycomb)":              basic_combat.rule,
            "Science (Petals)":                 ALWAYS_TRUE,
            "Science (Succulent)":              desert_exploration.rule,
            "Science (Foliage)":                mining.rule if (REGION.CAVE in REGION_WHITELIST) else desert_exploration.rule,
            "Science (Tillweeds)":              basic_farming.rule,
            "Science (Lichen)":                 ruins_exploration.rule,
            "Science (Banana)":                 lambda state: state.has_any([moon_quay_exploration.event, cave_exploration.event], player),
            "Science (Fig)":                    advanced_boating.rule,
            "Science (Tallbird Egg)":           basic_combat.rule,
            "Science (Hound's Tooth)":          basic_combat.rule,
            "Science (Bone Shards)":            lambda state: state.has_all([desert_exploration.event, hammering.event], player),
            "Science (Walrus Tusk)":            lambda state: state.has_all([basic_combat.event, winter.event], player),
            "Science (Silk)":                   ALWAYS_TRUE,
            "Science (Cut Stone)":              lambda state: state.has_all(["Cut Stone", mining.event], player),
            "Science (Palmcone Sprout)":        moon_quay_exploration.rule,
            "Science (Pine Cone)":              chopping.rule,
            "Science (Birchnut)":               chopping.rule,
            "Science (Driftwood Piece)":        pre_basic_boating.rule,
            "Science (Cookie Cutter Shell)":    lambda state: state.has_all([pre_basic_boating.event, basic_combat.event], player),
            "Science (Palmcone Scale)":         moon_quay_exploration.rule,
            "Science (Gnarwail Horn)":          lambda state: state.has_all([advanced_boating.event, basic_combat.event], player),
            "Science (Barnacles)":              lambda state: state.has_all([basic_boating.event, shaving.event], player),
            "Science (Frazzled Wires)":         (lambda state: state.has_all([ruins_exploration.event, hammering.event], player)) if REGION.RUINS in REGION_WHITELIST 
                                                else (lambda state: state.has_all([digging.event, basic_sanity_management.event], player)),
            "Science (Charcoal)":               charcoal.rule,
            "Science (Butter)":                 butter_luck.rule, # Excluded
            "Science (Asparagus)":              asparagus_farming.rule,
            "Science (Garlic)":                 garlic_farming.rule,
            "Science (Pumpkin)":                pumpkin_farming.rule,
            "Science (Corn)":                   corn_farming.rule,
            "Science (Onion)":                  onion_farming.rule,
            "Science (Potato)":                 ALWAYS_TRUE if EXPERT_PLAYER_BIAS else potato_farming.rule,
            "Science (Dragon Fruit)":           lambda state: state.has_any([dragonfruit_farming.event, dragonfruit_from_saladmander.event], player),
            "Science (Pomegranate)":            pomegranate_farming.rule,
            "Science (Eggplant)":               eggplant_farming.rule,
            "Science (Toma Root)":              tomaroot_farming.rule,
            "Science (Watermelon)":             watermelon_farming.rule,
            "Science (Pepper)":                 pepper_farming.rule,
            "Science (Durian)":                 durian_farming.rule,
            "Science (Carrot)":                 ALWAYS_TRUE,
            "Science (Stone Fruit)":            lambda state: state.has_any([lunar_island.event, cave_exploration.event], player),
            "Science (Marble)":                 mining.rule,
            "Science (Gold Nugget)":            mining.rule,
            "Science (Flint)":                  ALWAYS_TRUE,
            "Science (Honey)":                  ALWAYS_TRUE,
            "Science (Twigs)":                  ALWAYS_TRUE,
            "Science (Log)":                    chopping.rule,            
            "Magic (Blue Gem)":                 gem_digging.rule,
            "Magic (Living Log)":               lambda state: state.has_any([chopping.event, "Wormwood"], player),
            "Magic (Glommer's Goop)":           lambda state: has_survived_num_days(11, state),
            "Magic (Dark Petals)":              ALWAYS_TRUE,
            "Magic (Red Gem)":                  gem_digging.rule,
            "Magic (Slurper Pelt)":             ruins_exploration.rule,
            "Magic (Blue Spore)":               lambda state: state.has_all([cave_exploration.event, bug_catching.event, winter.event], player),
            "Magic (Red Spore)":                lambda state: state.has_all([cave_exploration.event, bug_catching.event, summer.event], player),
            "Magic (Green Spore)":              lambda state: state.has_all([cave_exploration.event, bug_catching.event, spring.event], player),
            "Magic (Broken Shell)":             cave_exploration.rule,
            "Magic (Leafy Meat)":               leafy_meat.rule,
            "Magic (Canary (Volatile))":        lambda state: state.has_all([canary.event, cave_exploration.event, bird_caging.event], player),
            "Magic (Life Giving Amulet)":       lambda state: state.has_all(["Life Giving Amulet", gem_digging.event, nightmare_fuel.event], player),
            "Magic (Nightmare Fuel)":           lambda state: state.has_all([basic_combat.event, nightmare_fuel.event], player),
            "Magic (Cut Reeds)":                swamp_exploration.rule,
            "Magic (Volt Goat Horn)":           basic_combat.rule,
            "Magic (Beard Hair)":               ALWAYS_TRUE,
            "Magic (Glow Berry)":               ruins_exploration.rule,
            "Magic (Tentacle Spots)":           basic_combat.rule,
            "Magic (Health)":                   healing.rule,
            "Magic (Sanity)":                   ALWAYS_TRUE,
            "Magic (Telltale Heart)":           lambda state: state.has_all([healing.event, "Telltale Heart"], player),
            "Magic (Forget-Me-Lots)":           basic_farming.rule,
            "Magic (Cat Tail)":                 pre_basic_combat.rule,
            "Magic (Bunny Puff)":               lambda state: state.has_all([cave_exploration.event, basic_combat.event], player),
            "Magic (Mosquito Sack)":            swamp_exploration.rule,
            "Magic (Spider Gland)":             ALWAYS_TRUE,
            "Magic (Monster Jerky)":            lambda state: state.has_all(["Drying Rack", "Rope", charcoal.event], player),
            "Magic (Pig Skin)":                 basic_combat.rule,
            "Magic (Batilisk Wing)":            mining.rule,
            "Magic (Stinger)":                  ALWAYS_TRUE,
            "Magic (Papyrus)":                  lambda state: state.has_all(["Papyrus", swamp_exploration.event], player),
            "Magic (Green Cap)":                ALWAYS_TRUE,
            "Magic (Blue Cap)":                 ALWAYS_TRUE,
            "Magic (Red Cap)":                  ALWAYS_TRUE,
            "Magic (Iridescent Gem)":           lambda state: state.has(iridescent_gem.event, player),
            "Magic (Desert Stone)":             lambda state: state.has_all([summer.event, storm_protection.event], player),
            "Magic (Naked Nostrils)":           cave_exploration.rule,
            "Magic (Frog Legs)":                ALWAYS_TRUE,
            "Magic (Spoiled Fish)":             fishing.rule if (ADVANCED_PLAYER_BIAS or not REGION.OCEAN in REGION_WHITELIST) else sea_fishing.rule,
            "Magic (Spoiled Fish Morsel)":      fishing.rule,
            "Magic (Rot)":                      lambda state: has_survived_num_days(15, state),
            "Magic (Rotten Egg)":               lambda state: state.has(bird_caging.event, player) and has_survived_num_days(20, state),
            "Magic (Carrat)":                   lambda state: state.has_any([lunar_island.event, cave_exploration.event], player) and state.has_any(["Trap", digging.event], player),
            "Magic (Moleworm)":                 hammering.rule,
            "Magic (Fireflies)":                bug_catching.rule,
            "Magic (Bulbous Lightbug)":         lambda state: state.has_all([cave_exploration.event, bug_catching.event], player),
            "Magic (Rabbit)":                   lambda state: state.has("Trap", player),
            "Magic (Butterfly)":                bug_catching.rule,
            "Magic (Mosquito)":                 lambda state: state.has_all([bug_catching.event, swamp_exploration.event], player),
            "Magic (Bee)":                      bug_catching.rule,
            "Magic (Killer Bee)":               bug_catching.rule,
            "Magic (Crustashine)":              moon_quay_exploration.rule,
            "Magic (Crow)":                     lambda state: state.has("Bird Trap", player),
            "Magic (Redbird)":                  lambda state: state.has("Bird Trap", player),
            "Magic (Snowbird)":                 lambda state: state.has_all(["Bird Trap", winter.event], player),
            "Magic (Canary)":                   lambda state: state.has_all(["Bird Trap", canary.event], player),
            "Magic (Puffin)":                   lambda state: state.has_all(["Bird Trap", pre_basic_boating.event], player),
            "Magic (Fossil Fragments)":         lambda state: state.has_all([cave_exploration.event, mining.event], player),
            "Think Tank (Freshwater Fish)":     freshwater_fishing.rule,
            "Think Tank (Live Eel)":            lambda state: state.has_all([cave_exploration.event, freshwater_fishing.event], player),
            "Think Tank (Runty Guppy)":         sea_fishing.rule,
            "Think Tank (Needlenosed Squirt)":  sea_fishing.rule,
            "Think Tank (Bitty Baitfish)":      sea_fishing.rule,
            "Think Tank (Smolt Fry)":           sea_fishing.rule,
            "Think Tank (Popperfish)":          sea_fishing.rule,
            "Think Tank (Fallounder)":          lambda state: state.has_all([advanced_boating.event, sea_fishing.event], player),
            "Think Tank (Bloomfin Tuna)":       lambda state: state.has_all([spring.event, sea_fishing.event], player),
            "Think Tank (Scorching Sunfish)":   lambda state: state.has_all([advanced_boating.event, summer.event, sea_fishing.event], player),
            "Think Tank (Spittlefish)":         lambda state: state.has_all([advanced_boating.event, sea_fishing.event], player),
            "Think Tank (Mudfish)":             sea_fishing.rule,
            "Think Tank (Deep Bass)":           lambda state: state.has_all([advanced_boating.event, sea_fishing.event], player),
            "Think Tank (Dandy Lionfish)":      lambda state: state.has_all([advanced_boating.event, sea_fishing.event], player),
            "Think Tank (Black Catfish)":       lambda state: state.has_all([advanced_boating.event, sea_fishing.event], player),
            "Think Tank (Corn Cod)":            lambda state: state.has_all([advanced_boating.event, sea_fishing.event], player),
            "Think Tank (Ice Bream)":           lambda state: state.has_all([advanced_boating.event, winter.event, sea_fishing.event], player),
            "Think Tank (Sweetish Fish)":       lambda state: state.has_all([advanced_boating.event, sea_fishing.event], player),
            "Think Tank (Wobster)":             lambda state: state.has_all([advanced_boating.event, sea_fishing.event], player),
            "Think Tank (Lunar Wobster)":       lambda state: state.has_all([lunar_island.event, sea_fishing.event], player),
            "Pseudoscience (Purple Gem)":       purple_gem.rule,
            "Pseudoscience (Yellow Gem)":       ALWAYS_TRUE,
            "Pseudoscience (Thulecite)":        thulecite.rule,
            "Pseudoscience (Orange Gem)":       ALWAYS_TRUE,
            "Pseudoscience (Green Gem)":        ALWAYS_TRUE,
            "Celestial (Moon Rock)":            ALWAYS_TRUE,
            "Celestial (Moon Shard)":           lambda state: state.has_any([cave_exploration.event, can_reach_islands.event], player),
            "Celestial (Moon Shroom)":          cave_exploration.rule,
            "Celestial (Moon Moth)":            lambda state: state.has_all([bug_catching.event, chopping.event], player),
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
            **{f"Survive {i} Days":             (lambda state: has_survived_num_days_2(i, state)) for i in range(1, 100)},
        },
    }

    EXISTING_LOCATIONS = [location.name for location in multiworld.get_locations(player)]
    SEASON_HELPER_ITEMS = [name for name, data in item_data_table.items() if "seasonhelper" in data.tags]
    TRAP_ITEMS = [name for name, data in item_data_table.items() if "trap" in data.tags]
    excluded:Set[str] = set()
    no_advancement:Set[str] = set()
    progression_required_bosses:Set = set()

    if options.goal.value != options.goal.option_survival:
        _required_bosses = options.required_bosses.value
        if "Ancient Fuelweaver" in _required_bosses: progression_required_bosses.add("Ancient Guardian")
        if "Celestial Champion" in _required_bosses: progression_required_bosses.add("Crab King")
        if "Scrappy Werepig" in _required_bosses: progression_required_bosses.add("Nightmare Werepig")

        ## Commented because now Boss Defeat items are placed here
        # if options.goal.value == options.goal.option_bosses_any:
        #     # Prevent goal bosses from having progression items if your goal is any
        #     excluded.update(_required_bosses)

        # elif options.goal.value == options.goal.option_bosses_all:
        #     # Don't exclude bosses in the path of your goal bosses
        #     excluded.update([boss_name for boss_name in _required_bosses if not boss_name in progression_required_bosses])

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

    LOCATION_ADVANCEMENT_CONDITIONS = {
        "Moon Stone Event":             REGION.RUINS in REGION_WHITELIST or RAIDBOSS_LOOT_LOGIC, # Avoid prioritizing if raid boss logic is off... 
        "Magic (Iridescent Gem)":       REGION.RUINS in REGION_WHITELIST or RAIDBOSS_LOOT_LOGIC, # and Dragonfly's only source of gems
        "Magic (Monster Jerky)":        BASE_MAKING_LOGIC,
        "Magic (Life Giving Amulet)":   resurrecting.is_progression,
    }
    
    # Set no-advancement to specific locations
    for location_name, advancement_allowed in LOCATION_ADVANCEMENT_CONDITIONS.items():
        if not advancement_allowed:
            no_advancement.add(location_name)

    # Set location rules
    for location_name, rule in rules_lookup["location_rules"].items():
        #assert_rule(rule, multiworld) # DEBUG
        if location_name in EXISTING_LOCATIONS:
            location = multiworld.get_location(location_name, player)
            required = False

            # Skip event locations
            if not location_name in location_data_table: continue

            location_data = location_data_table[location_name]

            # Prioritize required bosses
            for boss_name, tag_name in PRIORITY_TAGS.items():
                if boss_name in progression_required_bosses and tag_name in location_data.tags:
                    required = True
                    break

            if required:
                multiworld.priority_locations[player].value.add(location_name)
            elif ("priority" in location_data.tags
            or (options.boss_locations.value == options.boss_locations.option_prioritized and "boss" in location_data.tags and not "excluded" in location_data.tags)
            ):
                # Prioritize generic priority tag
                multiworld.priority_locations[player].value.add(location_name)

            # Exclude from having progression items if it meets the conditions
            if not required and ("excluded" in location_data.tags
            or (not options.seasonal_locations.value and "seasonal" in location_data.tags)
            or (not BOSS_LOOT_LOGIC and "boss" in location_data.tags)
            or (not RAIDBOSS_LOOT_LOGIC and "raidboss" in location_data.tags)
            or (not ADVANCED_PLAYER_BIAS and "advanced" in location_data.tags)
            or (not EXPERT_PLAYER_BIAS and "expert" in location_data.tags)
            ):
                excluded.add(location_name)

            else:
                # Set the rule as long as it's not excluded
                set_rule(location, rule)

                # Add respective research station rule to research locations
                if "research" in location_data.tags:
                    if "science" in location_data.tags:
                        add_rule(location, alchemy_engine.rule if "tier_2" in location_data.tags else science_machine.rule)
                    elif "magic" in location_data.tags:
                        add_rule(location, shadow_manipulator.rule if "tier_2" in location_data.tags else prestihatitor.rule)
                    elif "celestial" in location_data.tags:
                        add_rule(location, celestial_altar.rule if "tier_2" in location_data.tags else (lambda state: state.has_any([celestial_orb.event, celestial_altar.event], player)))
                    elif "seafaring" in location_data.tags:
                        add_rule(location, think_tank.rule)
                    elif "ancient" in location_data.tags:
                        add_rule(location, ancient_altar.rule)

                elif "farming" in location_data.tags:
                    add_rule(location, advanced_farming.rule)

                elif "cooking" in location_data.tags:
                    add_rule(location, cooking.rule)

            # Forbid season helpers in seasonal locations
            if "seasonal" in location_data.tags:
                for item_name in SEASON_HELPER_ITEMS:
                    forbid_item(location, item_name, player)

            # Forbid season helpers and traps in survive day locations
            elif "survivedays" in location_data.tags:
                for item_name in SEASON_HELPER_ITEMS:
                    forbid_item(location, item_name, player)
                for item_name in TRAP_ITEMS:
                    forbid_item(location, item_name, player)

            # Diallow progression for rng and seasonal locations
            if "rng" in location_data.tags or "seasonal" in location_data.tags:
                no_advancement.add(location_name)

            # Disallow progression for moonstorm region if Crab King is not progression
            if (
                not RAIDBOSS_LOOT_LOGIC 
                and not "Crab King" in progression_required_bosses
                and "moonstorm" in location_data.tags
            ):
                no_advancement.add(location_name)

    exclusion_rules(multiworld, player, excluded)

    # Apply no-advancement rules to non-priority locations
    for location_name in no_advancement:
        if (
            location_name in EXISTING_LOCATIONS
            and not (location_name in multiworld.priority_locations[player].value)
            and not (location_name in excluded)
        ):
            add_item_rule(multiworld.get_location(location_name, player), NO_ADVANCEMENT_ITEM)

    # # Set region rules
    # for region_name, rule in rules_lookup["regions"].items():
    #     region = multiworld.get_region(region_name, player)
    #     for entrance in region.entrances:
    #         set_rule(entrance, rule)

   # Decide win conditions
    victory_events:Set = set()
    if options.goal.value == options.goal.option_survival:
        survival_event = add_event("Survival Goal", REGION.FOREST, lambda state: survival_goal(state))
        victory_events.add(survival_event.event)
    elif options.goal.value == options.goal.option_bosses_any or options.goal.value == options.goal.option_bosses_all:
        victory_events.update([BOSS_COMPLETION_GOALS[bossname] for bossname in options.required_bosses.value])

    # Set the win conditions
    if options.goal.value == options.goal.option_bosses_any:
        multiworld.completion_condition[player] = lambda state: state.has_any(victory_events, player)
    else:
        multiworld.completion_condition[player] = lambda state: state.has_all(victory_events, player)

    itempool.set_progression_items({
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
        "Bird Trap":                True,
        "Birdcage":                 True,
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
        "Friendly Scarecrow":       True,
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
        "Eyebrella":                True,
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
        "Luxury Fan":               SEASON_GEAR_LOGIC,
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
        "Magiluminescence":         ADVANCED_PLAYER_BIAS,
        "Lantern":                  LIGHTING_LOGIC,
        "Miner Hat":                LIGHTING_LOGIC,
        "Boat Kit":                 True,
        "Oar":                      True,
        "Grass Raft Kit":           True,
        "Boat Patch":               True,
        "Driftwood Oar":            True,
        "Anchor Kit":               not EXPERT_PLAYER_BIAS,
        "Steering Wheel Kit":       not EXPERT_PLAYER_BIAS,
        "Fashion Goggles":          True,
        "Desert Goggles":           True,
        "Astroggles":               True,
        "Garden Hoe":               True,
        "Splendid Garden Hoe":      True,
        "Garden Digamajig":         True,
        "Bee Box":                  BASE_MAKING_LOGIC,
        "Crock Pot":                True,
        "Pinchin' Winch":           True,
        "Freshwater Fishing Rod":   True,
        "Ocean Trawler Kit":        True,
        "Tin Fishin' Bin":          BASE_MAKING_LOGIC,
        "Sea Fishing Rod":          True,
        "Astral Detector":          True,
        "Star Caller's Staff":      True,
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

