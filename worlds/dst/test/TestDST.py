from typing import Dict, Set, Any, Optional

from unittest import TestCase
from . import DSTTestBase
from ..Constants import DSTAP_ITEMS, ITEM_ID_OFFSET, DSTAP_LOCATIONS, LOCATION_ID_OFFSET

def _make_options_template(extra_data:Optional[Dict[str, Any]]):
    options = {
        "goal": "bosses_any",
        "required_bosses": {"Random"},
        "cave_regions": "full",
        "ocean_regions": "full",
        "boss_locations": "all",
        "cooking_locations": "regular",
        "shuffle_starting_recipes": False,
        "shuffle_no_unlock_recipes": False,
        "seed_items": False,
        "season_flow": "unlockable",
        "skill_level": "easy",
        "lighting_logic": "enabled",
        "weapon_logic": "enabled",
        "season_gear_logic": "enabled",
        "base_making_logic": "none",
        "backpack_logic": "none",
        "healing_logic": "none",
    }
    if extra_data:
        options.update(extra_data)
    return options


# Check for errors in data
class TestConstants(TestCase):
    @staticmethod
    def test_no_duplicate_id_or_name_in_item_data():
        codes:Set[int] = set()
        names:Set[str] = set()
        for v in DSTAP_ITEMS:
            code:int = v[0] + ITEM_ID_OFFSET
            name:str = v[1]
            assert not code in codes, f"Item id {code} duplicate defined!"
            assert not name in names, f"Item name {name} duplicate defined!"
            codes.add(code)
            names.add(name)

    @staticmethod
    def test_no_duplicate_id_or_name_in_location_data():
        codes:Set[int] = set()
        names:Set[str] = set()
        for v in DSTAP_LOCATIONS:
            code:int = v[0] + LOCATION_ID_OFFSET
            name:str = v[1]
            assert not code in codes, f"Location id {code} duplicate defined!"
            assert not name in names, f"Location name {name} duplicate defined!"
            codes.add(code)
            names.add(name)

# Season tests
class TestSeasonAutumn(DSTTestBase):
    options = _make_options_template({"seasons": {"Autumn"}})

class TestSeasonWinter(DSTTestBase):
    options = _make_options_template({"seasons": {"Winter"}})

class TestSeasonSpring(DSTTestBase):
    options = _make_options_template({"seasons": {"Spring"}})

class TestSeasonSummer(DSTTestBase):
    options = _make_options_template({"seasons": {"Summer"}})

class TestSeasonNonAutumn(DSTTestBase):
    options = _make_options_template({"seasons": {"Winter", "Spring", "Summer"}})

class TestSeasonNonWinter(DSTTestBase):
    options = _make_options_template({"seasons": {"Autumn", "Spring", "Summer"}})

class TestSeasonNonSpring(DSTTestBase):
    options = _make_options_template({"seasons": {"Autumn", "Winter", "Summer"}})

class TestSeasonNonSummer(DSTTestBase):
    options = _make_options_template({"seasons": {"Autumn", "Winter", "Spring"}})

# Phase tests
class TestPhaseDay(DSTTestBase):
    options = _make_options_template({"day_phases": {"Day"}})

class TestPhaseDusk(DSTTestBase):
    options = _make_options_template({"day_phases": {"Dusk"}})

class TestPhaseNight(DSTTestBase):
    options = _make_options_template({"day_phases": {"Night"}})

class TestPhaseNoDay(DSTTestBase):
    options = _make_options_template({"day_phases": {"Dusk", "Night"}})

class TestPhaseNoDusk(DSTTestBase):
    options = _make_options_template({"day_phases": {"Day", "Night"}})

class TestPhaseNoNight(DSTTestBase):
    options = _make_options_template({"day_phases": {"Day", "Dusk"}})

# Cave and Ocean region combinations
class TestRegionLightCave(DSTTestBase):
    options = _make_options_template({
        "cave_regions": "light",
        "ocean_regions": "none",
    })

class TestRegionFullCave(DSTTestBase):
    options = _make_options_template({
        "cave_regions": "full",
        "ocean_regions": "none",
    })

class TestRegionLightOcean(DSTTestBase):
    options = _make_options_template({
        "cave_regions": "none",
        "ocean_regions": "light",
    })

class TestRegionFullOcean(DSTTestBase):
    options = _make_options_template({
        "cave_regions": "none",
        "ocean_regions": "full",
    })

class TestRegionLightBoth(DSTTestBase):
    options = _make_options_template({
        "cave_regions": "light",
        "ocean_regions": "light",
    })

class TestRegionFullBoth(DSTTestBase):
    options = _make_options_template({
        "cave_regions": "full",
        "ocean_regions": "full",
    })

class TestRegionLightCaveFullOcean(DSTTestBase):
    options = _make_options_template({
        "cave_regions": "light",
        "ocean_regions": "full",
    })

class TestRegionFullCaveLightOcean(DSTTestBase):
    options = _make_options_template({
        "cave_regions": "full",
        "ocean_regions": "light",
    })

# Logic toggles
class TestLogicAdvancedDifficulty(DSTTestBase):
    options = _make_options_template({"skill_level": "advanced"})

class TestLogicExpertDifficulty(DSTTestBase):
    options = _make_options_template({"skill_level": "expert"})

class TestLogicMinimal(DSTTestBase):
    options = _make_options_template({
        "lighting_logic": "none",
        "weapon_logic": "none",
        "season_gear_logic": "none",
        "base_making_logic": "none",
        "backpack_logic": "none",
        "healing_logic": "none",
    })

class TestLogicFull(DSTTestBase):
    options = _make_options_template({
        "lighting_logic" : "enabled",
        "weapon_logic" : "enabled",
        "season_gear_logic" : "enabled",
        "base_making_logic" : "enabled",
        "backpack_logic" : "enabled",
        "healing_logic" : "enabled",
    })

# Shuffles
class TestShuffleNoUnlockRecipes(DSTTestBase):
    options = _make_options_template({"shuffle_no_unlock_recipes": True})

class TestShuffleSeedItems(DSTTestBase):
    options = _make_options_template({"seed_items": True})

# Location toggles
class TestToggleFarmingLocations(DSTTestBase):
    options = _make_options_template({"farming_locations": True})

class TestToggleFarmingLocationsWithSeeds(DSTTestBase):
    options = _make_options_template({
        "farming_locations": True,
        "seed_items": True,
    })

class TestToggleWarlyCookingLocations(DSTTestBase):
    options = _make_options_template({"cooking_locations": "warly_enabled"})

class TestToggleWarlyCookingLocationsWithSeeds(DSTTestBase):
    options = _make_options_template({
        "cooking_locations": "warly_enabled",
        "seed_items": True,
    })
    
# Survival goals
class TestSurvivalShort(DSTTestBase):
    options = _make_options_template({
        "goal": "survival",
        "days_to_survive": 1,
        "season_flow": "normal",
    })

class TestSurvivalFullMoon(DSTTestBase):
    options = _make_options_template({
        "goal": "survival",
        "days_to_survive": 12, # One day after full moon
        "season_flow": "normal",
    })

class TestSurvival1Season(DSTTestBase):
    options = _make_options_template({
        "goal": "survival",
        "days_to_survive": 22, # 1 season passed
        "season_flow": "normal",
    })

class TestSurvival2Season(DSTTestBase):
    options = _make_options_template({
        "goal": "survival",
        "days_to_survive": 36, # 2 seasons passed
        "season_flow": "normal",
    })

class TestSurvival3Season(DSTTestBase):
    options = _make_options_template({
        "goal": "survival",
        "days_to_survive": 52, # 3 seasons passed
        "season_flow": "normal",
    })

class TestSurvival4Season(DSTTestBase):
    options = _make_options_template({
        "goal": "survival",
        "days_to_survive": 72, # 4 seasons passed
        "season_flow": "normal",
    })
    
class TestSurvivalLong(DSTTestBase):
    options = _make_options_template({
        "goal": "survival",
        "days_to_survive": 140, # 2 years passed
        "season_flow": "normal",
    })