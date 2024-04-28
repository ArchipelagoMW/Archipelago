from typing import List, Tuple

from . import SVTestBase
from .assertion import WorldAssertMixin
from .. import options, StardewItem
from ..strings.ap_names.ap_weapon_names import APWeapon
from ..strings.ap_names.transport_names import Transportation
from ..strings.fish_names import Fish
from ..strings.tool_names import APTool
from ..strings.wallet_item_names import Wallet


def collect_fishing_abilities(tester: SVTestBase):
    for i in range(4):
        tester.multiworld.state.collect(tester.world.create_item(APTool.fishing_rod), event=False)
        tester.multiworld.state.collect(tester.world.create_item(APTool.pickaxe), event=False)
        tester.multiworld.state.collect(tester.world.create_item(APTool.axe), event=False)
        tester.multiworld.state.collect(tester.world.create_item(APWeapon.weapon), event=False)
    for i in range(10):
        tester.multiworld.state.collect(tester.world.create_item("Fishing Level"), event=False)
        tester.multiworld.state.collect(tester.world.create_item("Combat Level"), event=False)
        tester.multiworld.state.collect(tester.world.create_item("Mining Level"), event=False)
    for i in range(17):
        tester.multiworld.state.collect(tester.world.create_item("Progressive Mine Elevator"), event=False)
    tester.multiworld.state.collect(tester.world.create_item("Spring"), event=False)
    tester.multiworld.state.collect(tester.world.create_item("Summer"), event=False)
    tester.multiworld.state.collect(tester.world.create_item("Fall"), event=False)
    tester.multiworld.state.collect(tester.world.create_item("Winter"), event=False)
    tester.multiworld.state.collect(tester.world.create_item(Transportation.desert_obelisk), event=False)
    tester.multiworld.state.collect(tester.world.create_item("Railroad Boulder Removed"), event=False)
    tester.multiworld.state.collect(tester.world.create_item("Island North Turtle"), event=False)
    tester.multiworld.state.collect(tester.world.create_item("Island West Turtle"), event=False)


def create_and_collect(tester: SVTestBase, item_name: str) -> StardewItem:
    item = tester.world.create_item(item_name)
    tester.multiworld.state.collect(item, event=False)
    return item


def create_and_collect_fishing_access_items(tester: SVTestBase) -> List[Tuple[StardewItem, str]]:
    items = [(create_and_collect(tester, Wallet.dark_talisman), Fish.void_salmon),
             (create_and_collect(tester, Wallet.rusty_key), Fish.slimejack),
             (create_and_collect(tester, "Progressive Mine Elevator"), Fish.lava_eel),
             (create_and_collect(tester, Transportation.island_obelisk), Fish.lionfish),
             (create_and_collect(tester, "Island Resort"), Fish.stingray)]
    return items


class TestMasterAnglerNoFishsanity(WorldAssertMixin, SVTestBase):
    options = {
        options.Goal.internal_name: options.Goal.option_master_angler,
        options.Fishsanity.internal_name: options.Fishsanity.option_none,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_false
    }

    def test_need_all_fish_to_win(self):
        collect_fishing_abilities(self)
        self.assert_cannot_reach_victory(self.multiworld)
        critical_items = create_and_collect_fishing_access_items(self)
        self.assert_can_reach_victory(self.multiworld)
        for item, fish in critical_items:
            with self.subTest(f"Needed: {fish}"):
                self.assert_item_was_necessary_for_victory(item, self.multiworld)


class TestMasterAnglerNoFishsanityNoGingerIsland(WorldAssertMixin, SVTestBase):
    options = {
        options.Goal.internal_name: options.Goal.option_master_angler,
        options.Fishsanity.internal_name: options.Fishsanity.option_none,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true
    }

    def test_need_fish_to_win(self):
        collect_fishing_abilities(self)
        self.assert_cannot_reach_victory(self.multiworld)
        items = create_and_collect_fishing_access_items(self)
        self.assert_can_reach_victory(self.multiworld)
        unecessary_items = [(item, fish) for (item, fish) in items if fish in [Fish.lionfish, Fish.stingray]]
        necessary_items = [(item, fish) for (item, fish) in items if (item, fish) not in unecessary_items]
        for item, fish in necessary_items:
            with self.subTest(f"Needed: {fish}"):
                self.assert_item_was_necessary_for_victory(item, self.multiworld)
        for item, fish in unecessary_items:
            with self.subTest(f"Not Needed: {fish}"):
                self.assert_item_was_not_necessary_for_victory(item, self.multiworld)


class TestMasterAnglerFishsanityNoHardFish(WorldAssertMixin, SVTestBase):
    options = {
        options.Goal.internal_name: options.Goal.option_master_angler,
        options.Fishsanity.internal_name: options.Fishsanity.option_exclude_hard_fish,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_false
    }

    def test_need_fish_to_win(self):
        collect_fishing_abilities(self)
        self.assert_cannot_reach_victory(self.multiworld)
        items = create_and_collect_fishing_access_items(self)
        self.assert_can_reach_victory(self.multiworld)
        unecessary_items = [(item, fish) for (item, fish) in items if fish in [Fish.void_salmon, Fish.stingray, Fish.lava_eel]]
        necessary_items = [(item, fish) for (item, fish) in items if (item, fish) not in unecessary_items]
        for item, fish in necessary_items:
            with self.subTest(f"Needed: {fish}"):
                self.assert_item_was_necessary_for_victory(item, self.multiworld)
        for item, fish in unecessary_items:
            with self.subTest(f"Not Needed: {fish}"):
                self.assert_item_was_not_necessary_for_victory(item, self.multiworld)
