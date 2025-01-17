from typing import Dict, Set, FrozenSet, Callable, Type
from BaseClasses import CollectionState, MultiWorld
from .Constants import REGION, PHASE, SEASON, SEASONS_PASSED, SPECIAL_TAGS
from .Options import DSTOptions

class AssertionState(CollectionState):
    def has(self, item, player, count = 1):
        assert type(item) is str, item
        assert len(item)
        assert type(player) is int, player
        return super().has(item, player, count)

    def has_all(self, items, player):
        assert type(items) is set, items
        for item in items:
            assert type(item) is str, item
            assert len(item)
        assert type(player) is int, player
        return super().has_all(items, player)

    def has_any(self, items, player):
        assert type(items) is set, items
        for item in items:
            assert type(item) is str, item
            assert len(item)
        assert type(player) is int, player
        return super().has_any(items, player)

def assert_rule(rule: Callable[[CollectionState], bool], multiworld:MultiWorld):
    state = AssertionState(multiworld)
    assert callable(rule), rule
    true_or_false = rule(state)
    assert true_or_false == True or true_or_false == False

def build_whitelist(options: DSTOptions) -> FrozenSet[str]:
    _whitelist:Set[str] = set()
    # Day phase
    _whitelist.update(options.day_phases.value)
    if len(_whitelist.intersection({PHASE.DAY, PHASE.DUSK})): _whitelist.add(PHASE.DAY_OR_DUSK)
    if len(_whitelist.intersection({PHASE.DUSK, PHASE.NIGHT})): _whitelist.add(PHASE.DUSK_OR_NIGHT)

    # Seasons passed
    _day_goal = (
        140 if options.goal.value != options.goal.option_survival
        else options.days_to_survive.value
    )
    _num_seasons:int = 1
    if _day_goal > 11: _whitelist.add(SEASONS_PASSED.SEASONS_HALF)
    if _day_goal > 20: _whitelist.add(SEASONS_PASSED.SEASONS_1); _num_seasons = 2
    if _day_goal > 35: _whitelist.add(SEASONS_PASSED.SEASONS_2); _num_seasons = 3
    if _day_goal > 55: _whitelist.add(SEASONS_PASSED.SEASONS_3); _num_seasons = 4
    if _day_goal > 70: _whitelist.add(SEASONS_PASSED.SEASONS_4); _num_seasons = 5
    if _day_goal > 90: _whitelist.add(SEASONS_PASSED.SEASONS_5); _num_seasons = 6

    # Seasons
    season_order = [
        _season for _season in [
            SEASON.AUTUMN, SEASON.WINTER, SEASON.SPRING, SEASON.SUMMER
        ] if _season in options.seasons.value
    ]
    _lookup = {
        options.starting_season.option_autumn: SEASON.AUTUMN,
        options.starting_season.option_winter: SEASON.WINTER,
        options.starting_season.option_spring: SEASON.SPRING,
        options.starting_season.option_summer: SEASON.SUMMER,
    }

    # Player chose a starting season that's not enabled; Change it
    if not _lookup[options.starting_season.value] in season_order:
        for raw_season_value in [
            options.starting_season.option_autumn,
            options.starting_season.option_winter,
            options.starting_season.option_spring,
            options.starting_season.option_summer,
        ]:
            if _lookup[raw_season_value] in season_order:
                options.starting_season.value = raw_season_value

    # Align season order with starting season
    while season_order[0] != _lookup[options.starting_season.value]:
        season_order.append(season_order.pop(0))

    # Build the season whitelist
    if options.season_flow.value != options.season_flow.option_unlockable_shuffled:
        # In normal season flow, seasons line up with seasons passed
        for _ in range(0, _num_seasons):
            if not len(season_order): break
            _whitelist.add(season_order.pop(0))
        # Might as well change the enabled season option so it's seen in the spoiler
        options.seasons.value.intersection_update(_whitelist)
    else:
        # Add all seasons when unlockable
        _whitelist.update(options.seasons.value)

    if len(_whitelist.intersection({SEASON.AUTUMN, SEASON.SPRING, SEASON.SUMMER})): _whitelist.add(SEASON.NONWINTER)
    if len(_whitelist.intersection({SEASON.AUTUMN, SEASON.WINTER, SEASON.SUMMER})): _whitelist.add(SEASON.NONSPRING)
    if len(_whitelist.intersection({SEASON.AUTUMN, SEASON.WINTER, SEASON.SPRING})): _whitelist.add(SEASON.NONSUMMER)

    # Region
    _whitelist.update({REGION.MENU, REGION.FOREST})
    if options.cave_regions.value >= options.cave_regions.option_light: _whitelist.add(REGION.CAVE)
    if options.cave_regions.value >= options.cave_regions.option_full: _whitelist.add(REGION.RUINS)
    if _whitelist.issuperset({REGION.RUINS, SEASONS_PASSED.SEASONS_HALF, PHASE.NIGHT}): _whitelist.add(REGION.ARCHIVE)
    if options.ocean_regions.value >= options.ocean_regions.option_light: _whitelist.update({REGION.OCEAN, REGION.MOONQUAY})
    if options.ocean_regions.value >= options.ocean_regions.option_full: _whitelist.add(REGION.MOONSTORM)
    if REGION.CAVE in _whitelist or REGION.OCEAN in _whitelist: _whitelist.add(REGION.DUALREGION)
    if REGION.CAVE in _whitelist and REGION.OCEAN in _whitelist: _whitelist.add(REGION.BOTHREGIONS)

    # Force more time in logic for farming locations, and moonstorm too since potato is required for astroggles
    if options.farming_locations.value or REGION.MOONSTORM in _whitelist:
        _whitelist.update({SEASONS_PASSED.SEASONS_HALF, SEASONS_PASSED.SEASONS_1})

    # Hermit Crab Friendship (Min reachable 7)
    _HERMIT_FRIENDSHIP_CONDITIONS = [
        PHASE.NIGHT in _whitelist or REGION.CAVE in _whitelist, # Hermit Home 1
        PHASE.NIGHT in _whitelist or REGION.CAVE in _whitelist, # Hermit Home 2
        PHASE.NIGHT in _whitelist or REGION.CAVE in _whitelist, # Hermit Home 3
        True, # Drying Racks
        PHASE.DAY in _whitelist and SEASON.NONWINTER in _whitelist, # Plant flowers
        True, # Berry bushes
        True, # Clear underwater salvageables
        SEASON.SPRING in _whitelist and SEASON.NONSPRING in _whitelist, # Lure plant; Spawns when changing to or from spring
        True, # Wooden chair
        SEASON.AUTUMN in _whitelist or SEASON.SPRING in _whitelist, # Umbrella
        SEASON.WINTER in _whitelist, # Warm clothing
        SEASON.SUMMER in _whitelist, # Flower Salad
        SEASON.AUTUMN in _whitelist, # Fallounder
        SEASON.SPRING in _whitelist, # Bloomfin Tuna
        SEASON.SUMMER in _whitelist, # Scorching Sunfish
        SEASON.WINTER in _whitelist, # Ice Bream
        True, # 5 heavy fish
    ]

    # Special tags
    _whitelist.update({tag for tag, istrue in {
        SPECIAL_TAGS.RUINS_GEMS:        (options.boss_locations.value >= options.boss_locations.option_all)
                                        or (len(_whitelist.intersection({REGION.RUINS, REGION.OCEAN})) > 0),
        SPECIAL_TAGS.MOOSEGOOSE:        _whitelist.issuperset({SEASON.SPRING, SEASON.NONSPRING}),
        SPECIAL_TAGS.BUTTER_MUFFIN:     REGION.OCEAN in _whitelist or _whitelist.issuperset({PHASE.DAY, SEASON.NONWINTER}),
        SPECIAL_TAGS.LOBSTER_DINNER:    _whitelist.issuperset({REGION.OCEAN, PHASE.DAY, PHASE.DUSK_OR_NIGHT}),
        SPECIAL_TAGS.LEAFY_MEAT:        REGION.DUALREGION in _whitelist
                                        or _whitelist.issuperset({SEASON.NONWINTER, SEASONS_PASSED.SEASONS_2}),
        SPECIAL_TAGS.FRUITS:            (
                                            (options.cooking_locations.value != options.cooking_locations.option_none)
                                            and (options.cooking_locations.value != options.cooking_locations.option_meat_only)
                                            and (
                                                REGION.RUINS in _whitelist
                                                or bool(options.seed_items.value)
                                                or (
                                                    SEASONS_PASSED.SEASONS_1 in _whitelist
                                                    and len(_whitelist.intersection({SEASON.SPRING, SEASON.SUMMER})) > 0
                                                )
                                            )
                                        ),
        SPECIAL_TAGS.BANANA:            len(_whitelist.intersection({REGION.RUINS, REGION.MOONQUAY})) > 0,
        SPECIAL_TAGS.CORN:              (
                                            REGION.OCEAN in _whitelist
                                            or bool(options.seed_items.value)
                                            or _whitelist.issuperset({SEASONS_PASSED.SEASONS_1, SEASON.NONWINTER})
                                        ),
        SPECIAL_TAGS.HERMIT_8:          _HERMIT_FRIENDSHIP_CONDITIONS.count(True) >= 8,
        SPECIAL_TAGS.HERMIT_10:         _HERMIT_FRIENDSHIP_CONDITIONS.count(True) >= 10,
    }.items() if istrue})

    return frozenset(_whitelist)

def create_tag_group_validation_fn(options: DSTOptions) -> Callable[[Type, Set[str]], bool]:
    WHITELIST = build_whitelist(options)
    _valid_lookups:Dict[Type, Dict[str, bool]] = {
        REGION:         {tag_name: tag in WHITELIST for tag_name, tag in REGION.tag_lookup.items()},
        SEASON:         {tag_name: tag in WHITELIST for tag_name, tag in SEASON.tag_lookup.items()},
        PHASE:          {tag_name: tag in WHITELIST for tag_name, tag in PHASE.tag_lookup.items()},
        SEASONS_PASSED: {tag_name: tag in WHITELIST for tag_name, tag in SEASONS_PASSED.tag_lookup.items()},
        SPECIAL_TAGS:   {tag_name: tag in WHITELIST for tag_name, tag in SPECIAL_TAGS.tag_lookup.items()},
    }
    def is_enabled_in_tag_group(tag_group_type:Type, tags:Set[str]) -> bool:
        _enabled = True
        for tag, istrue in _valid_lookups.get(tag_group_type, {}).items():
            if tag in tags:
                _enabled = False
                if istrue:
                    return True
        return _enabled
    return is_enabled_in_tag_group
