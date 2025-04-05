from argparse import Namespace
import random
from typing import Any, ClassVar, Dict, cast
import typing

from BaseClasses import CollectionState, MultiWorld, get_seed
from worlds import AutoWorld
from Generate import get_seed_name  # type: ignore
from test.bases import WorldTestBase
from .. import MetroidPrimeWorld, MultiworldWithPassthrough

DEFAULT_TEST_SEED = get_seed(1)


class MetroidPrimeTestBase(WorldTestBase):
    game = "Metroid Prime"
    player: ClassVar[int] = 1
    world: "MetroidPrimeWorld"

    seed = DEFAULT_TEST_SEED

    def world_setup(self, *args, **kwargs):  # type: ignore
        super().world_setup(seed=self.seed)
        if self.constructed:
            self.world = self.multiworld.worlds[self.player]  # type: ignore


class MetroidPrimeWithOverridesTestBase(MetroidPrimeTestBase):
    overrides: Dict[str, Any] = {}

    def pre_steps(self):
        for key, value in self.overrides.items():
            setattr(self.world, key, value)

    # Copied from bases.py, overriden at the end to manually set some values before generate_early
    def world_setup(self, seed: typing.Optional[int] = None) -> None:
        self.multiworld = MultiWorld(1)
        self.multiworld.game[self.player] = self.game
        self.multiworld.player_name = {self.player: "Tester"}
        self.multiworld.set_seed(seed)
        self.multiworld.state = CollectionState(self.multiworld)
        random.seed(self.multiworld.seed)
        self.multiworld.seed_name = get_seed_name(
            random
        )  # only called to get same RNG progression as Generate.py
        args = Namespace()
        for name, option in AutoWorld.AutoWorldRegister.world_types[
            self.game
        ].options_dataclass.type_hints.items():
            setattr(
                args,
                name,
                {1: option.from_any(self.options.get(name, option.default))},
            )
        self.multiworld.set_options(args)
        self.world = self.multiworld.worlds[self.player]  # type: ignore
        self.pre_steps()

        self.world.generate_early()

        # A couple tests rely on this being set, it does not happen in the test base for some reason
        if self.world.options.start_inventory_from_pool.value:
            for item in self.world.options.start_inventory_from_pool.value.keys():
                self.multiworld.push_precollected(self.world.create_item(item))
        if self.world.options.start_inventory.value:
            for item in self.world.options.start_inventory.value.keys():
                self.multiworld.push_precollected(self.world.create_item(item))

        gen_steps = (
            "create_regions",
            "create_items",
            "set_rules",
            "generate_basic",
            "pre_fill",
        )

        for step in gen_steps:
            AutoWorld.call_all(self.multiworld, step)


class MetroidPrimeUniversalTrackerTestBase(MetroidPrimeWithOverridesTestBase):
    game = "Metroid Prime"
    player: ClassVar[int] = 1
    world: "MetroidPrimeWorld"

    seed = DEFAULT_TEST_SEED

    def pre_steps(self):
        super().pre_steps()
        setattr(self.multiworld, "generation_is_fake", True)

    def world_setup(self, *args, **kwargs):  # type: ignore
        super().world_setup(seed=self.seed)
        if self.constructed:
            self.tracker_multiworld = cast(MultiworldWithPassthrough, self.multiworld)

    def init_passhthrough(self, slot_data: Dict[Any, str]):
        self.tracker_multiworld.re_gen_passthrough = {self.game: slot_data}
