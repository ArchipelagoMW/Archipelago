import typing
from argparse import Namespace
from BaseClasses import CollectionState, MultiWorld
from Options import ItemLinks
from worlds.AutoWorld import AutoWorldRegister, call_all
from .. import HKWorld


class linkedTestHK():
    run_default_tests = False
    game = "Hollow Knight"
    world: HKWorld
    expected_grubs: int
    item_link_group: typing.List[typing.Dict[str, typing.Any]]

    def setup_item_links(self, args):
        setattr(args, "item_links",
                {
                    1: ItemLinks.from_any(self.item_link_group),
                    2: ItemLinks.from_any([{
                        "name": "ItemLinkTest",
                        "item_pool": ["Grub"],
                        "link_replacement": False,
                        "replacement_item": "One_Geo",
                    }])
                })
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
