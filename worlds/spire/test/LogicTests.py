from typing import List, Optional

from typing_extensions import NamedTuple, Iterable

from BaseClasses import CollectionState
from worlds.spire.Rules import PowerLevel
from worlds.spire.test import SpireTestBase

def _create_floor_check(start: int, end: int) -> List[str]:
    return [f"Reached Floor {i}" for i in range(start, end + 1)]

def _create_shop_check(start: int, end: int) -> List[str]:
    return [f"Shop Slot {i}" for i in range(start, end + 1)]

def _create_combat_check(start: int, end: int) -> List[str]:
    return [f"Combat Gold {i}" for i in range(start, end + 1)]

logic_map: dict[PowerLevel, List[str]] = {
    PowerLevel(): [
        "Card Reward 1",
        "Card Reward 2",
        "Act 1 Campfire 1",
        "Act 1 Campfire 2",
        "Potion Drop 1",
        "Potion Drop 2",
        *_create_floor_check(1,10),
        *_create_combat_check(1,4),
    ],
    PowerLevel(gold=2): [
        *_create_shop_check(1, 5),
    ],
    PowerLevel(1): [
        "Relic 1",
    ],
    PowerLevel(draw=0,relic=1, rest=1): [
        "Card Reward 3",
        "Card Reward 4",
    ],
    PowerLevel(draw=2,rest=1, shop=2): [
        "Relic 2",
        "Relic 3",
        "Elite Gold 1",
        "Elite Gold 2",
        "Potion Drop 3",
        *_create_combat_check(5, 6),
        *_create_floor_check(11, 15)
    ],
    PowerLevel(draw=3,relic=2, rest=1, smith=1, shop=3, shop_remove=1, gold=2): [
        "Act 1 Boss",
        "Rare Card Reward 1",
        "Boss Relic 1",
        "Boss Gold 1",
        "Card Reward 5",
        "Card Reward 6",
        "Potion Drop 4",
        "Act 2 Campfire 1",
        "Act 2 Campfire 2",
        *_create_floor_check(16, 22),
        *_create_combat_check(7, 8),
    ],
    PowerLevel(draw=3,relic=2, rest=1, smith=1, shop=3, shop_remove=1, gold=5): [
        *_create_shop_check(6, 10),
    ],
    PowerLevel(draw=6,relic=2, rest=2,smith=1, shop=4, shop_remove=1, gold=2): [
        "Potion Drop 5",
        *_create_floor_check(23, 27)
    ],
    PowerLevel(draw=6, relic=3, rest=2, smith=1, shop=4, shop_remove=1, gold=2): [
        "Card Reward 7",
        *_create_combat_check(9, 10),
    ],
    PowerLevel(draw=6, relic=3, rest=2, smith=1, shop=5, shop_remove=1, gold=2): [
        "Potion Drop 6",
        *_create_floor_check(28, 32)
    ],
    PowerLevel(draw=6, relic=4, rest=2, smith=1, shop=5, shop_remove=1, gold=2): [
        "Card Reward 8",
        *_create_combat_check(11, 12),
    ],
    PowerLevel(draw=7, relic=2, rest=2,smith=1, shop=4, shop_remove=1, gold=2): [
        "Relic 4",
        "Relic 5",
        "Elite Gold 3",
    ],
    PowerLevel(draw=7, relic=3, rest=2,smith=1, shop=5, shop_remove=1, gold=2): [
        "Relic 6",
        "Elite Gold 4",
    ],
    PowerLevel(draw=7, relic=3, boss_relic=1, rest=2, smith=2, shop=6, shop_remove=2, gold=5): [
        "Act 2 Boss",
        "Rare Card Reward 2",
        "Boss Relic 2",
        "Boss Gold 2",
        "Card Reward 9",
        "Card Reward 10",
        "Potion Drop 7",
        "Act 3 Campfire 1",
        "Act 3 Campfire 2",
        *_create_floor_check(33, 39),
        *_create_combat_check(13, 14),
    ],
    PowerLevel(draw=7, relic=3, boss_relic=1, rest=2, smith=2, shop=6, shop_remove=2, gold=9): [
        *_create_shop_check(11, 16),
    ],
    PowerLevel(draw=8,relic=4,boss_relic=1, rest=3,smith=2, shop=8, shop_remove=2, gold=5): [
        "Relic 7",
        "Relic 8",
        "Card Reward 11",
        "Elite Gold 5",
        "Potion Drop 8",
        *_create_floor_check(40, 44),
        *_create_combat_check(15, 16),
    ],
    PowerLevel(draw=9,relic=6,boss_relic=1, rest=3,smith=2, shop=10, shop_remove=2, gold=5): [
        "Card Reward 12",
        "Card Reward 13",
        "Potion Drop 9",
        *_create_floor_check(45, 49),
        *_create_combat_check(17, 18),
    ],
    PowerLevel(draw=9,relic=6,boss_relic=1, rest=3,smith=2, shop=10, shop_remove=2, gold=5): [
        "Relic 9",
        "Relic 10",
        "Elite Gold 6",
        "Elite Gold 7",
    ],
    PowerLevel(draw=10,relic=7,boss_relic=2,rest=3,smith=3, shop=10,shop_remove=3, gold=9): [
        "Act 3 Boss",
        "Heart Room",
        * _create_floor_check(50, 55)
    ],
}

def setup_power_map(map: dict[PowerLevel, List[str]], prefix: str) -> dict[PowerLevel, List[str]]:
    return {key: [f"{prefix} {x}" for x in val] for key, val in map.items()}

class LogicTestBase(SpireTestBase):

    options = {
        'characters': ["silent"],
        'final_act': 1,
        'campfire_sanity':1,
        'shop_sanity': 1,
        'shop_card_slots': 5,
        'shop_neutral_card_slots': 2,
        'shop_relic_slots': 3,
        'shop_potion_slots': 3,
        'shop_remove_slots': 1,
        'gold_sanity': 1,
        'potion_sanity': 1,
    }

    def _setup_state_accessible(self, power: PowerLevel) -> CollectionState:

        state = CollectionState(self.multiworld)

        draw = self.get_item_by_name(f"{self.prefix} Card Reward")
        for _ in range(power.draw):
            state.collect(draw)

        relic = self.get_item_by_name(f"{self.prefix} Relic")
        for _ in range(power.relic):
            state.collect(relic)

        boss_relic = self.get_item_by_name(f"{self.prefix} Boss Relic")
        for _ in range(power.boss_relic):
            state.collect(boss_relic)

        rest = self.get_item_by_name(f"{self.prefix} Progressive Rest")
        for _ in range(power.rest):
            state.collect(rest)

        smith = self.get_item_by_name(f"{self.prefix} Progressive Smith")
        for _ in range(power.smith):
            state.collect(smith)

        shop = self.get_item_by_name(f"{self.prefix} Shop Card Slot")
        for _ in range(power.shop):
            state.collect(shop)

        gold = self.get_item_by_name(f"{self.prefix} 30 Gold")
        for _ in range(power.gold):
            state.collect(gold)

        remove = self.get_item_by_name(f"{self.prefix} Progressive Shop Remove")
        for _ in range(power.shop_remove):
            state.collect(remove)

        return state

    def _setup_state_inaccessible(self, power: PowerLevel, type: str):

        state = CollectionState(self.multiworld)

        draw = self.get_item_by_name(f"{self.prefix} Card Reward")
        draws = [draw for _ in range(power.draw)]

        relic = self.get_item_by_name(f"{self.prefix} Relic")
        relics = [relic for _ in range(power.relic)]

        boss_relic = self.get_item_by_name(f"{self.prefix} Boss Relic")
        boss_relics = [boss_relic for _ in range(power.boss_relic)]

        rest = self.get_item_by_name(f"{self.prefix} Progressive Rest")
        rests = [rest for _ in range(power.rest)]

        smith = self.get_item_by_name(f"{self.prefix} Progressive Smith")
        smiths = [smith for _ in range(power.smith)]

        shop = self.get_item_by_name(f"{self.prefix} Shop Card Slot")
        shops = [shop for _ in range(power.shop)]

        remove = self.get_item_by_name(f"{self.prefix} Progressive Shop Remove")
        removes = [remove for _ in range(power.shop_remove)]

        gold = self.get_item_by_name(f"{self.prefix} 30 Gold")
        golds = [gold for _ in range(power.gold)]

        if type == "Card Reward":
            draws.pop()
        elif type == "Relic":
            relics.pop()
        elif type == "Boss Relic":
            boss_relics.pop()
        elif type == "Progressive Rest":
            rests.pop()
        elif type == "Progressive Smith":
            smiths.pop()
        elif type == "Shop Card Slot":
            shops.pop()
        elif type == "Progressive Shop Remove":
            removes.pop()
        elif type == "30 Gold":
            golds.pop()

        for list in [draws, relics, boss_relics, rests, smiths, shops, removes, golds]:
            for item in list:
                state.collect(item)

        return state

    def _test_inaccessible(self, power: PowerLevel, locations: Iterable[str]):

        for i, type in enumerate([ x for x in ['Card Reward', 'Relic', 'Boss Relic', 'Progressive Rest', 'Progressive Smith', "Shop Card Slot", "Progressive Shop Remove", "30 Gold"]]):
            if power[i] == 0:
                continue
            state = self._setup_state_inaccessible(power, type)

            for location in locations:
                with self.subTest(f"Cannot access {location} while missing one {type}", reqs=power):
                    loc = self.world.get_location(location)
                    self.assertFalse(loc.can_reach(state),
                                    f"Location {location} can be reached with power level {power}, but missing one {type}; state {state.prog_items}")

    def _test_accessible(self, power: PowerLevel, locations: Iterable[str]):
        state = self._setup_state_accessible(power)

        for location in locations:
            with self.subTest(f"Can access {location} with all reqs", reqs=power):
                loc = self.world.get_location(location)
                self.assertTrue(loc.can_reach(state),
                                f"Location {location} cannot be reached with power level {power} and state {state.prog_items}")


class LogicTests(LogicTestBase):

    power_map: dict[PowerLevel, List[str]]

    def setUp(self) -> None:
        super().setUp()
        self.power_map = setup_power_map(logic_map, self.prefix)

    def test_accessible(self):
        for key, value in self.power_map.items():
            self._test_accessible(key, value)

    def test_inaccessible(self):
        for key, value in self.power_map.items():
            self._test_inaccessible(key, value)

class CustomCharTest(LogicTests):
    prefix = "Custom Character 1"
    options = {
        'use_advanced_characters': 1,
        'advanced_characters': {
            "foobar": {
                'final_act': 1,
                'ascension': 1,
            }
        },
        'campfire_sanity': 1,
        'shop_sanity': 1,
        'shop_card_slots': 5,
        'shop_neutral_card_slots': 2,
        'shop_relic_slots': 3,
        'shop_potion_slots': 3,
        'shop_remove_slots': 1,
        'gold_sanity': 1,
        'potion_sanity': 1,
    }
