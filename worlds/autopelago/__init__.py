import logging
from collections import deque
from typing import Callable, Dict, Literal, Optional, Set

from .AutopelagoDefinitions import GAME_NAME, version_stamp, AutopelagoGameRequirement, AutopelagoAllRequirement, \
    AutopelagoAnyRequirement, AutopelagoAnyTwoRequirement, AutopelagoItemRequirement, item_key_to_name, \
    AutopelagoRatCountRequirement, item_name_to_rat_count, location_name_to_id, location_name_to_requirement, \
    AutopelagoRegionDefinition, item_name_to_id, ItemClassification, item_name_to_classification, \
    location_name_to_progression_item_name, game_specific_nonprogression_items, generic_nonprogression_item_table, \
    total_available_rat_count, max_required_rat_count, AutopelagoNonProgressionItemType, \
    autopelago_item_classification_of, location_name_to_nonprogression_item, autopelago_regions, item_name_groups, \
    location_name_groups
from .options import ArchipelagoGameOptions, VictoryLocation

from BaseClasses import CollectionState, Item, Location, MultiWorld, Region, Tutorial
from worlds.AutoWorld import World, WebWorld

the_logger = logging.getLogger(GAME_NAME)


def _is_trivial(req: AutopelagoGameRequirement):
    if 'all' in req:
        return not req['all']
    elif 'rat_count' in req:
        return req['rat_count'] == 0
    else:
        return False


def _is_satisfied(player: int, req: AutopelagoGameRequirement, state: CollectionState):
    if 'all' in req:
        req: AutopelagoAllRequirement
        return all(_is_satisfied(player, sub_req, state) for sub_req in req['all'])
    elif 'any' in req:
        req: AutopelagoAnyRequirement
        return any(_is_satisfied(player, sub_req, state) for sub_req in req['any'])
    elif 'any_two' in req:
        req: AutopelagoAnyTwoRequirement
        return sum(1 if _is_satisfied(player, sub_req, state) else 0 for sub_req in req['any_two']) > 1
    elif 'item' in req:
        req: AutopelagoItemRequirement
        return state.has(item_key_to_name[req['item']], player)
    else:
        assert 'rat_count' in req, 'Only AutopelagoRatCountRequirement is expected here'
        req: AutopelagoRatCountRequirement
        return sum(item_name_to_rat_count[k] * i for k, i in state.prog_items[player].items() if
                   k in item_name_to_rat_count) >= req['rat_count']


class AutopelagoItem(Item):
    game = GAME_NAME


class AutopelagoLocation(Location):
    game = GAME_NAME

    def __init__(self, player: int, name: str, parent: Region):
        super().__init__(player, name, location_name_to_id[name] if name in location_name_to_id else None, parent)
        if name in location_name_to_requirement:
            req = location_name_to_requirement[name]
            if not _is_trivial(req):
                self.access_rule = lambda state: _is_satisfied(player, req, state)


class AutopelagoRegion(Region):
    game = GAME_NAME
    autopelago_definition: AutopelagoRegionDefinition

    def __init__(self, autopelago_definition: AutopelagoRegionDefinition, player: int, multiworld: MultiWorld,
                 hint: Optional[str] = None):
        super().__init__(autopelago_definition.key, player, multiworld, hint)
        self.autopelago_definition = autopelago_definition
        self.locations += (AutopelagoLocation(player, loc, self) for loc in autopelago_definition.locations)


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
    """
    An idle game, in the same vein as ArchipIDLE but intended to be more sophisticated.
    """
    game = GAME_NAME
    topology_present = False  # it's static, so setting this to True isn't actually helpful
    web = AutopelagoWebWorld()
    options_dataclass = ArchipelagoGameOptions
    options: ArchipelagoGameOptions
    victory_location: str
    regions_in_scope: Set[str]
    locations_in_scope: Set[str]

    # item_name_to_id and location_name_to_id must be filled VERY early, but seemingly only because
    # they are used in Main.main to log the ID ranges in use. if not for that, we probably could've
    # been able to get away with populating these just based on what we actually need.
    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)

    # insert other ClassVar values... suggestions include:
    # - item_descriptions
    # - location_descriptions
    # - hint_blacklist (should it include the goal item?)

    def generate_early(self):
        if self.options.victory_location == VictoryLocation.option_captured_goldfish:
            self.victory_location = 'Captured Goldfish'
        elif self.options.victory_location == VictoryLocation.option_secret_cache:
            self.victory_location = 'Secret Cache'
        else:
            self.victory_location = 'Snakes on a Planet'

        self.locations_in_scope = set()
        q = deque(('Menu',))
        self.regions_in_scope = {'Menu',}
        while q:
            r = autopelago_regions[q.popleft()]
            locations_set = {l for l in r.locations}
            self.locations_in_scope.update(locations_set)
            if self.victory_location in locations_set:
                continue
            for next_exit in r.exits:
                if next_exit in self.regions_in_scope:
                    continue
                self.regions_in_scope.add(next_exit)
                q.append(next_exit)

    def create_item(self, name: str):
        item_id = item_name_to_id[name]
        classification = item_name_to_classification[name]
        item = AutopelagoItem(name, classification, item_id, self.player)
        return item

    def create_items(self):
        new_items = [self.create_item(item)
                     for location, item in location_name_to_progression_item_name.items()
                     if location in self.locations_in_scope and item != 'Moon Shoes']

        # skip balancing for the pack_rat items that take us beyond the minimum limit
        rat_items = sorted(
            (item for item in new_items if item.name in item_name_to_rat_count),
            key=lambda item: (item_name_to_rat_count[item.name], 0 if item.name == item_key_to_name['pack_rat'] else 1)
        )
        for i in range(total_available_rat_count - max_required_rat_count):
            assert rat_items[i].name == item_key_to_name[
                'pack_rat'], 'Expected there to be enough pack_rat fillers for this calculation.'
            rat_items[i].classification |= ItemClassification.skip_balancing

        self.multiworld.itempool += new_items

        nonprogression_item_table = {c: [item_name for item_name in items] for c, items in
                                     generic_nonprogression_item_table.items()}
        dlc_games = {game for game in game_specific_nonprogression_items}
        for category, items in nonprogression_item_table.items():
            self.multiworld.random.shuffle(items)
            replacements_made = 0
            for game_name in self.multiworld.game.values():
                if game_name not in dlc_games:
                    continue
                dlc_games.remove(game_name)
                for item in game_specific_nonprogression_items[game_name][category]:
                    items[replacements_made] = item
                    replacements_made += 1

        category_to_next_offset: Dict[AutopelagoNonProgressionItemType, int] = {category: 0 for category in
                                                                                generic_nonprogression_item_table}
        next_filler_becomes_trap = False
        nonprog_type: Literal['useful_nonprogression', 'filler', 'trap']
        for l, nonprog_type in location_name_to_nonprogression_item.items():
            if l not in self.locations_in_scope:
                continue

            if nonprog_type == 'filler':
                if next_filler_becomes_trap:
                    nonprog_type = 'trap'
                next_filler_becomes_trap = not next_filler_becomes_trap

            if category_to_next_offset[nonprog_type] >= len(nonprogression_item_table[nonprog_type]):
                if nonprog_type == 'filler':
                    nonprog_type = 'trap'
                elif nonprog_type == 'trap':
                    nonprog_type = 'filler'
            next_item = nonprogression_item_table[nonprog_type][category_to_next_offset[nonprog_type]]
            self.multiworld.itempool.append(self.create_item(next_item))
            category_to_next_offset[nonprog_type] += 1

    def create_regions(self):
        victory_region = Region('Victory', self.player, self.multiworld)
        self.multiworld.regions.append(victory_region)
        self.multiworld.completion_condition[self.player] =\
            lambda state: state.can_reach(victory_region)

        new_regions = {r.key: AutopelagoRegion(r, self.player, self.multiworld)
                       for key, r in autopelago_regions.items()
                       if key in self.regions_in_scope}
        for r in new_regions.values():
            self.multiworld.regions.append(r)
            req = r.autopelago_definition.requires
            rule: Optional[Callable[[CollectionState], bool]]
            rule = None if _is_trivial(req) \
                else (lambda req_: lambda state: _is_satisfied(self.player, req_, state))(req)
            if self.victory_location in r.autopelago_definition.locations:
                r.connect(victory_region, rule=rule)
                if self.options.victory_location == VictoryLocation.option_snakes_on_a_planet:
                    r.locations[0].place_locked_item(self.create_item('Moon Shoes'))
            else:
                for next_exit in r.autopelago_definition.exits:
                    r.connect(new_regions[next_exit], rule=rule)

    def get_filler_item_name(self):
        return "Monkey's Paw"

    def fill_slot_data(self):
        return {
            'version_stamp': version_stamp,
            'victory_location_name': self.victory_location,
        }
