import logging
from typing import Dict, Literal, Optional, Union

from .AutopelagoDefinitions import GAME_NAME, AutopelagoGameRequirement, AutopelagoAllRequirement, \
    AutopelagoAnyRequirement, AutopelagoAnyTwoRequirement, AutopelagoItemRequirement, item_key_to_name, \
    AutopelagoRatCountRequirement, item_name_to_rat_count, location_name_to_id, location_name_to_requirement, \
    AutopelagoRegionDefinition, item_name_to_id, ItemClassification, item_name_to_classification, \
    location_name_to_progression_item_name, location_names_with_fixed_rewards, game_specific_nonprogression_items, \
    generic_nonprogression_item_table, total_available_rat_count, max_required_rat_count, \
    AutopelagoNonProgressionItemType, autopelago_item_classification_of, location_name_to_nonprogression_item, \
    autopelago_regions, item_name_groups, location_name_groups
from .options import ArchipelagoGameOptions

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
    '''
    An idle game, in the same vein as ArchipIDLE but intended to be more sophisticated.
    '''
    game = GAME_NAME
    topology_present = False  # it's static, so setting this to True isn't actually helpful
    data_version = 0
    web = AutopelagoWebWorld()
    options_dataclass = ArchipelagoGameOptions
    options: ArchipelagoGameOptions

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

    def create_item(self, name: str, classification: Union[ItemClassification, None] = None):
        item_id = item_name_to_id[name] if name in item_name_to_id else None
        if classification is None:
            classification = item_name_to_classification[name]
        item = AutopelagoItem(name, classification, item_id, self.player)
        return item

    def create_items(self):
        new_items = [self.create_item(item)
                     for location, item in location_name_to_progression_item_name.items()
                     if location not in location_names_with_fixed_rewards]

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
        for nonprog_type in location_name_to_nonprogression_item.values():
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
        new_regions = {r.key: AutopelagoRegion(r, self.player, self.multiworld) for r in autopelago_regions.values()}
        for r in new_regions.values():
            self.multiworld.regions.append(r)
            req = r.autopelago_definition.requires
            for next_exit in r.autopelago_definition.exits:
                if next_exit == 'moon_comma_the':
                    continue
                rule = (lambda req_: lambda state: _is_satisfied(self.player, req_, state))(req)
                r.connect(new_regions[next_exit], rule=None if _is_trivial(req) else rule)
            for loc in r.locations:
                if loc.name in location_names_with_fixed_rewards:
                    item_name = location_name_to_progression_item_name[loc.name]
                    loc.place_locked_item(self.create_item(item_name))

        self.multiworld.completion_condition[self.player] =\
            lambda state: state.has('Lockheed SR-71 Blackbird', self.player)

    def get_filler_item_name(self):
        return "Monkey's Paw"
