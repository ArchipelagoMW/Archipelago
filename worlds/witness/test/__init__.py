from test.bases import WorldTestBase
from test.general import gen_steps, setup_multiworld
from test.multiworld.test_multiworlds import MultiworldTestBase
from typing import Any, ClassVar, Dict, Iterable, List, Union

from BaseClasses import Item

from worlds.witness import WitnessWorld


class WitnessTestBase(WorldTestBase):
    game = "The Witness"
    player: ClassVar[int] = 1

    world: WitnessWorld


class WitnessMultiworldTestBase(MultiworldTestBase):
    options_per_world: List[Dict[str, Any]]
    common_options: Dict[str, Any] = {}

    def setUp(self):
        self.multiworld = setup_multiworld([WitnessWorld] * len(self.options_per_world), ())

        for world, options in zip(self.multiworld.worlds.values(), self.options_per_world):
            for option_name, option_value in {**self.common_options, **options}.items():
                option = getattr(world.options, option_name)
                self.assertIsNotNone(option)

                option.value = option.from_any(option_value).value

        self.assertSteps(gen_steps)

    def collect_by_name(self, item_names: Union[str, Iterable[str]], player: int) -> List[Item]:
        items = self.get_items_by_name(item_names, player)
        for item in items:
            self.multiworld.state.collect(item)
        return items

    def get_items_by_name(self, item_names: Union[str, Iterable[str]], player: int) -> List[Item]:
        if isinstance(item_names, str):
            item_names = (item_names,)
        return [item for item in self.multiworld.itempool if item.name in item_names and item.player == player]
