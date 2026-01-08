from typing import Dict
from dataclasses import dataclass

from BaseClasses import Item, ItemClassification, Region
from Options import OptionList, OptionSet, PerGameCommonOptions, Toggle, Range, OptionError
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import add_rule


class Victims(OptionList):
    """List of players to be locked out of the game."""


class AllVictims(Toggle):
    """Overrides Victim list to include all slots in the multiworld (excluding self) instead."""


class AutoHintGameStart(Toggle):
    """If the Game Start items should be prehinted."""


class RandomStartStart(Range):
    """adds that many random start games to start inventory, for randomizing everything"""
    range_start = 0
    range_end = 10
    default = 0


@dataclass
class ShahrazadOptions(PerGameCommonOptions):
    victims: Victims
    all_victims: AllVictims
    hint_game_start: AutoHintGameStart
    random_start: RandomStartStart


class ShahrazadWeb(WebWorld):
    tutorials = []


class ShahrazadItem(Item):
    game = "Shahrazad"


class ShahrazadWorld(World):
    game = "Shahrazad"
    topology_present = False
    item_name_to_id = {}  # will fill in stage_generate_basic()
    base_id = 980
    location_name_to_id = {
        "": -1001,
    }
    web = ShahrazadWeb()
    options_dataclass = ShahrazadOptions
    options: ShahrazadOptions
    item_pool_names: Dict[int, str]

    def generate_early(self):
        if self.options.all_victims:
            if not self.options.random_start:
                raise OptionError("All Victims cannot be used with random_start = 0")
            self.options.victims.value = [name for slot, name in self.multiworld.player_name.items() if slot != self.player]

        self.item_pool_names = {}
        for player in self.multiworld.player_ids:
            if self.multiworld.player_name[player] in self.options.victims.value:
                item_name = f"{self.multiworld.player_name[player]} Start"
                self.item_pool_names[player] = item_name

    @classmethod
    def stage_generate_early(cls, multiworld: "MultiWorld"):
        victims = {}
        item_id = cls.base_id
        for name in {n for w in multiworld.get_game_worlds(cls.game) for n in w.item_pool_names.values()}:
            victims[name] = item_id
            item_id += 1

        cls.item_name_to_id = victims
        # update datapackage checksum
        import worlds
        worlds.network_data_package["games"][cls.game] = cls.get_data_package_data()

    def create_regions(self):
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)
        menu.add_locations({name: None for i, name in enumerate(self.item_pool_names.values())
                            if i >= self.options.random_start})  # skip the amount of items we already precollect

    def create_item(self, name: str) -> Item:
        assert self.item_name_to_id[name]
        return ShahrazadItem(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    def create_items(self) -> None:
        item_pool = []
        for item in self.item_pool_names.values():
            item_pool.append(self.create_item(item))
            # this will make more items than locations, i don't want to make a
            # client so nothing i can really do about that besides try and
            # steal filler from others but I'd rather let core do that

        self.random.shuffle(item_pool)

        for _ in range(self.options.random_start.value):
            if item_pool:
                start_item = item_pool.pop()
                print(f"start item: {start_item.name}")
                self.multiworld.push_precollected(start_item)
            else:
                print(f"tried to add more games to start than games locked")

        self.multiworld.itempool += item_pool

    @classmethod
    def stage_pre_fill(cls, multiworld):
        if hasattr(multiworld, "generation_is_fake"):
            # UT has no way to get the unlock items so just skip locking altogether
            return
        for world in multiworld.get_game_worlds(cls.game):
            for victim_id, item_name in world.item_pool_names.items():
                victim_world = multiworld.worlds[victim_id]
                menu = victim_world.get_region(victim_world.origin_region_name)
                victim_world.options.progression_balancing.value = 0

                for exit in menu.exits:
                    add_rule(exit, lambda state, item_name=item_name: state.has(item_name, world.player))

                if menu.locations:
                    print(
                        f"found {len(menu.locations)} locations in {menu.name} "
                        f"for victim {victim_world.player_name}, "
                        f"applying access rules, this may slow generation down considerably")
                    for location in menu.locations:
                        add_rule(location, lambda state, item_name=item_name: state.has(item_name, world.player))

                if world.options.hint_game_start:
                    world.options.start_hints.value.add(item_name)

    def post_fill(self):
        # start inventory our locations because we can't actually check them
        for loc in self.multiworld.get_filled_locations(self.player):
            item = loc.item

            item.location = None
            loc.item = None
            self.multiworld.push_precollected(item)

            loc.place_locked_item(Item("Nothing", ItemClassification.filler, None, self.player))
