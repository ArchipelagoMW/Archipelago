from typing import Callable, Literal

from BaseClasses import CollectionState, Entrance, Item, ItemClassification, Location, MultiWorld, Region, Tutorial
from worlds.AutoWorld import World, WebWorld

from .ArbitraryGameDefs import \
    BASE_ID, GAME_NAME, AutopelagoRegion, num_locations_in, \
    rat_item_count_for_balancing, rat_item_count_skip_balancing, useful_item_count, filler_item_count, trap_item_count

from .Items import \
    normal_rat_item_name, a_item_name, b_item_name, c_item_name, d_item_name, e_item_name, f_item_name, goal_item_name, \
    all_item_names, generic_item_table, game_specific_items, item_name_to_defined_classification, item_name_to_rat_count

def _gen_ids():
    next_id = BASE_ID
    while True:
        yield next_id
        next_id += 1


class AutopelagoItem(Item):
    game = GAME_NAME


class AutopelagoLocation(Location):
    game = GAME_NAME


class AutopelagoWebWorld(WebWorld):
    theme = 'partyTime'
    tutorials = [
        Tutorial(
            tutorial_name='Setup Guide',
            description='A guide to playing Autopelago',
            language='English',
            file_name='guide_en.md',
            link='guide/en',
            authors=['Joe Amenta']
        )
    ]


class AutopelagoWorld(World):
    '''
    An idle game, in the same vein as ArchipIDLE but intended to be more sophisticated.
    '''
    game = GAME_NAME
    topology_present = False # it's static, so setting this to True isn't actually helpful
    data_version = 0
    web = AutopelagoWebWorld()

    # location_name_to_id and item_name_to_id must be filled VERY early, but seemingly only because
    # they are used in Main.main to log the ID ranges in use. if not for that, we probably could've
    # been able to get away with populating these just based on what we actually need.
    location_name_to_id = { }
    _id_gen = _gen_ids()
    for r in AutopelagoRegion:
        for i in range(num_locations_in[r]):
            location_name_to_id[r.get_location_name(i)] = next(_id_gen)
    item_name_to_id = { }
    _id_gen = _gen_ids()
    for item_name in all_item_names:
        item_name_to_id[item_name] = next(_id_gen)
    del _id_gen

    # insert other ClassVar values... suggestions include:
    # - item_name_groups
    # - item_descriptions
    # - location_name_groups
    # - location_descriptions
    # - hint_blacklist (should it include the goal item?)

    # other variables we use are INSTANCE variables that depend on the specific multiworld.
    _item_name_to_classification: dict[str, ItemClassification]
    _all_live_items_excluding_goal_and_normal_rats: list[str]
    _normal_rats_balancing_count: int | None
    _normal_rats_skip_balancing_count: int | None
    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self._item_name_to_classification = { item_name: classification for item_name, classification in item_name_to_defined_classification.items() if classification is not None }
        self._all_live_items_excluding_goal_and_normal_rats: list[str] = [a_item_name, b_item_name, c_item_name, d_item_name, e_item_name, f_item_name]
        self._normal_rats_balancing_count = None
        self._normal_rats_skip_balancing_count = None

    def generate_early(self):
        # finalize the list of possible items, based on which games are present in this multiworld.
        full_item_table = { c: [item_name for item_name in items] for c, items in generic_item_table.items() }
        dlc_games = { game for game in game_specific_items }
        for category, items in full_item_table.items():
            if category not in { 'useful_nonprogression', 'filler', 'trap', 'uncategorized' }:
                continue
            replacements_made = 0
            for game_name in self.multiworld.game.values():
                if game_name not in dlc_games:
                    continue
                dlc_games.remove(game_name)
                for item in game_specific_items[game_name][category]:
                    items[replacements_made] = item
                    replacements_made += 1

        category_to_next_offset = { category: 0 for category in full_item_table }
        category_to_next_offset['rat'] += 1
        def append_next_n_item_names(category: Literal['rat', 'useful_nonprogression', 'filler', 'trap', 'uncategorized'], n: int, classification: ItemClassification):
            def next_up_to_n_item_names(category: Literal['rat', 'useful_nonprogression', 'filler', 'trap', 'uncategorized'], n: int):
                items = full_item_table[category]
                offset = category_to_next_offset[category]
                avail = len(items) - offset
                if avail < n:
                    n = avail
                yield from (items[offset + i] for i in range(n))
                category_to_next_offset[category] += n

            for item_name in next_up_to_n_item_names(category, n):
                self._all_live_items_excluding_goal_and_normal_rats.append(item_name)
                self._item_name_to_classification[item_name] = classification
                n -= 1

            assert n == 0 or category == 'rat', f'Only normal rats should use the overflow ({n=}, {category=}, {classification=})'
            match classification:
                case ItemClassification.progression:
                    assert self._normal_rats_balancing_count is None, 'Normal rats should only be added once for balancing.'
                    self._normal_rats_balancing_count = n
                case ItemClassification.progression_skip_balancing:
                    assert self._normal_rats_skip_balancing_count is None, 'Normal rats should only be added once for non-balancing.'
                    self._normal_rats_skip_balancing_count = n

        append_next_n_item_names('rat', rat_item_count_for_balancing, ItemClassification.progression)
        append_next_n_item_names('rat', rat_item_count_skip_balancing, ItemClassification.progression_skip_balancing)
        append_next_n_item_names('useful_nonprogression', useful_item_count, ItemClassification.useful)
        append_next_n_item_names('filler', filler_item_count, ItemClassification.filler)
        append_next_n_item_names('trap', trap_item_count, ItemClassification.trap)

    def set_rules(self):
        def _connect(r_from: AutopelagoRegion, r_to: AutopelagoRegion, access_rule: Callable[[CollectionState], bool] | None = None):
            r_from_real = self.multiworld.get_region(r_from.name, self.player)
            r_to_real = self.multiworld.get_region(r_to.name, self.player)
            connection = Entrance(self.player, '', r_from_real)
            if access_rule:
                connection.access_rule = access_rule
            r_from_real.exits.append(connection)
            connection.connect(r_to_real)

        _connect(AutopelagoRegion.Before8Rats, AutopelagoRegion.Gate8Rats, lambda state: sum(item_name_to_rat_count[k] * i for k, i in state.prog_items[self.player].items() if k in item_name_to_rat_count) >= 8)
        _connect(AutopelagoRegion.Before8Rats, AutopelagoRegion.Gate8Rats, lambda state: sum(item_name_to_rat_count[k] * i for k, i in state.prog_items[self.player].items() if k in item_name_to_rat_count) >= 8)
        _connect(AutopelagoRegion.Gate8Rats, AutopelagoRegion.After8RatsBeforeA)
        _connect(AutopelagoRegion.Gate8Rats, AutopelagoRegion.After8RatsBeforeB)
        _connect(AutopelagoRegion.After8RatsBeforeA, AutopelagoRegion.A)
        _connect(AutopelagoRegion.After8RatsBeforeB, AutopelagoRegion.B)
        _connect(AutopelagoRegion.A, AutopelagoRegion.AfterABeforeC, lambda state: state.has(a_item_name, self.player))
        _connect(AutopelagoRegion.B, AutopelagoRegion.AfterBBeforeD, lambda state: state.has(b_item_name, self.player))
        _connect(AutopelagoRegion.AfterABeforeC, AutopelagoRegion.C)
        _connect(AutopelagoRegion.AfterBBeforeD, AutopelagoRegion.D)
        _connect(AutopelagoRegion.C, AutopelagoRegion.AfterCBefore20Rats, lambda state: state.has(c_item_name, self.player))
        _connect(AutopelagoRegion.D, AutopelagoRegion.AfterDBefore20Rats, lambda state: state.has(d_item_name, self.player))
        _connect(AutopelagoRegion.AfterCBefore20Rats, AutopelagoRegion.Gate20Rats, lambda state: sum(item_name_to_rat_count[k] * i for k, i in state.prog_items[self.player].items() if k in item_name_to_rat_count) >= 20)
        _connect(AutopelagoRegion.AfterDBefore20Rats, AutopelagoRegion.Gate20Rats, lambda state: sum(item_name_to_rat_count[k] * i for k, i in state.prog_items[self.player].items() if k in item_name_to_rat_count) >= 20)
        _connect(AutopelagoRegion.Gate20Rats, AutopelagoRegion.After20RatsBeforeE)
        _connect(AutopelagoRegion.Gate20Rats, AutopelagoRegion.After20RatsBeforeF)
        _connect(AutopelagoRegion.AfterDBefore20Rats, AutopelagoRegion.After20RatsBeforeE, lambda state: sum(item_name_to_rat_count[k] * i for k, i in state.prog_items[self.player].items() if k in item_name_to_rat_count) >= 20)
        _connect(AutopelagoRegion.AfterDBefore20Rats, AutopelagoRegion.After20RatsBeforeF, lambda state: sum(item_name_to_rat_count[k] * i for k, i in state.prog_items[self.player].items() if k in item_name_to_rat_count) >= 20)
        _connect(AutopelagoRegion.After20RatsBeforeE, AutopelagoRegion.E)
        _connect(AutopelagoRegion.After20RatsBeforeF, AutopelagoRegion.F)
        _connect(AutopelagoRegion.E, AutopelagoRegion.TryingForGoal, lambda state: state.has(e_item_name, self.player))
        _connect(AutopelagoRegion.F, AutopelagoRegion.TryingForGoal, lambda state: state.has(f_item_name, self.player))

        self.multiworld.get_location("goal", self.player).place_locked_item(self.create_item(goal_item_name))
        self.multiworld.completion_condition[self.player] = lambda state: state.has(goal_item_name, self.player)

    def create_item(self, name: str, classification: ItemClassification | None = None):
        id = self.item_name_to_id[name]
        classification = classification or self._item_name_to_classification[name]
        assert classification is not None, 'Classification should either be defined, calculated during generate_early, or hardcoded.'
        item = AutopelagoItem(name, classification, id, self.player)
        return item

    def create_items(self):
        self.multiworld.itempool += (self.create_item(name) for name in self._all_live_items_excluding_goal_and_normal_rats)
        self.multiworld.itempool += (self.create_item(normal_rat_item_name, ItemClassification.progression) for _ in range(self._normal_rats_balancing_count))
        self.multiworld.itempool += (self.create_item(normal_rat_item_name, ItemClassification.progression_skip_balancing) for _ in range(self._normal_rats_skip_balancing_count))

    def create_regions(self):
        self.multiworld.regions += (self.create_region(r) for r in AutopelagoRegion)

        # logic assumes that the player starts in a special hardcoded "Menu" region
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)
        entrance = Entrance(self.player, '', menu)
        menu.exits.append(entrance)
        entrance.connect(self.multiworld.get_region(AutopelagoRegion.Before8Rats.name, self.player))

    def create_region(self, r: AutopelagoRegion):
        region = Region(r.name, self.player, self.multiworld)
        for i in range(num_locations_in[r]):
            location_name = r.get_location_name(i)
            location_id = self.location_name_to_id[location_name]
            location = AutopelagoLocation(self.player, location_name, location_id, region)
            region.locations.append(location)
        return region

    def get_filler_item_name(self) -> str:
        return "Monkey's Paw"
