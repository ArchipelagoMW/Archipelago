import random
from argparse import Namespace
from collections.abc import Iterable
from typing import Any, ClassVar

from BaseClasses import CollectionState, MultiWorld
from Generate import get_seed_name
from Options import ItemLinks
from test.bases import WorldTestBase
from worlds.AutoWorld import AutoWorldRegister, call_all

from .. import HKWorld
from ..resource_state_vars import ResourceStateHandler
from ..state_mixin import default_state

RUN_FILL_TESTS = False


class HKTestBase(WorldTestBase):
    game = "Hollow Knight"
    world: HKWorld

    def test_fill(self):
        if RUN_FILL_TESTS:
            super().test_fill()


class HKGoalBase(HKTestBase):
    """Class to not run any default state tests and just check goal reachability"""
    run_default_tests = False
    # consider adding accessdependency-type code for all-but-required cannot beat

    def test_goal(self):
        """Asserts empty state cannot complete the goal but all state can"""
        self.assertBeatable(False)
        self.multiworld.state = self.multiworld.get_all_state()
        self.assertBeatable(True)


class SelectSeedHK(HKTestBase):
    seed = 0

    def world_setup(self, *args, **kwargs):
        super().world_setup(self.seed)


class NoStepHK(HKTestBase):
    run_default_tests = False

    def world_setup(self, seed: int | None = None) -> None:
        self.multiworld = MultiWorld(1)
        self.multiworld.game[self.player] = self.game
        self.multiworld.player_name = {self.player: "Tester"}
        self.multiworld.set_seed(seed)
        random.seed(self.multiworld.seed)
        self.multiworld.seed_name = get_seed_name(random)  # only called to get same RNG progression as Generate.py
        args = Namespace()
        for name, option in AutoWorldRegister.world_types[self.game].options_dataclass.type_hints.items():
            setattr(args, name, {
                1: option.from_any(self.options.get(name, option.default))
            })
        self.multiworld.set_options(args)
        self.multiworld.state = CollectionState(self.multiworld)
        self.world = self.multiworld.worlds[self.player]
        gen_steps = ("generate_early",)  # "create_regions", "create_items", "set_rules", "generate_basic")
        for step in gen_steps:
            call_all(self.multiworld, step)


class LinkedTestHK:
    run_default_tests = False
    game = "Hollow Knight"
    world: HKWorld
    expected_grubs: int
    item_link_group: list[dict[str, Any]]

    def setup_item_links(self, args):
        args.item_links = {
            1: ItemLinks.from_any(self.item_link_group),
            2: ItemLinks.from_any([{
                "name": "ItemLinkTest",
                "item_pool": ["Grub"],
                "link_replacement": False,
                "replacement_item": "One_Geo",
            }])
        }
        return args

    def world_setup(self) -> None:
        """
        Create a multiworld with two players that share an itemlink
        """
        self.multiworld = MultiWorld(2)
        self.multiworld.game = {1: self.game, 2: self.game}
        self.multiworld.player_name = {1: "Linker 1", 2: "Linker 2"}
        self.multiworld.set_seed()
        args = Namespace()
        options_dataclass = AutoWorldRegister.world_types[self.game].options_dataclass
        for name, option in options_dataclass.type_hints.items():
            setattr(args, name, {
                1: option.from_any(self.options.get(name, option.default)),
                2: option.from_any(self.options.get(name, option.default))
            })
        args = self.setup_item_links(args)
        self.multiworld.set_options(args)
        self.multiworld.set_item_links()
        # groups get added to state during its constructor so this has to be after item links are set
        self.multiworld.state = CollectionState(self.multiworld)
        gen_steps = ("generate_early", "create_regions", "create_items", "set_rules", "generate_basic")
        for step in gen_steps:
            call_all(self.multiworld, step)
        # link the items together and stop at prefill
        self.multiworld.link_items()
        self.multiworld._all_state = None
        call_all(self.multiworld, "pre_fill")

        self.world = self.multiworld.worlds[self.player]

    def test_grub_count(self) -> None:
        assert self.world.grub_count == self.expected_grubs, \
               f"Expected {self.expected_grubs} but found {self.world.grub_count}"


class StateVarSetup:
    key: str
    """relevant state variable key"""
    resource: ClassVar[dict[str, int]]
    """starting Resource State"""
    cs: ClassVar[dict[str, int]]
    """starting CollectionState"""
    prep_vars: Iterable[str]
    """other state variable keys to modify state before use"""
    notch_override: int | None = None
    """if set forces NOTCHES to be a specific value"""
    mask_override: int | None = None
    """if set forces MASKSHARDS to be a specific value"""

    @staticmethod
    def get_one_state(func, *args, **kwargs):
        states = list(func(*args, **kwargs))
        assert len(states) == 1, f"Expected one state but got {len(states)}"
        return states[0]

    def get_initialized_args(self):
        state = CollectionState(self.multiworld)
        for item, i in self.cs.items():
            # assert item in self.world.item_name_to_id, f"Unknown item collected {item}"
            for _ in range(i):
                state.collect(self.world.create_item(item))
        if self.notch_override is not None:
            state.prog_items[self.player]["NOTCHES"] = self.notch_override
        if self.mask_override is not None:
            state.prog_items[self.player]["MASKSHARDS"] = self.mask_override
        rs = default_state(self.resource)
        for prep in self.prep_vars:
            rs = self.get_one_state(ResourceStateHandler.get_handler(prep, self.player).modify_state, rs, state)
        return rs, state

    def get_handler(self, key=None):
        if not key:
            key = self.key
        return ResourceStateHandler.get_handler(key, self.player)

    def get_modified_state(self):
        rs, cs = self.get_initialized_args()

        handler = self.get_handler()
        return list(handler.modify_state(rs, cs))
