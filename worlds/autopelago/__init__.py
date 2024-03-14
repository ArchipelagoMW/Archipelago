import logging

# TODO: stabilize the imports, don't just import *
from .AutopelagoDefinitions import *

from BaseClasses import CollectionState, Item, Location, MultiWorld, Region, Tutorial
from worlds.AutoWorld import World, WebWorld

def _is_trivial(req: AutopelagoGameRequirement):
    if 'all' in req:
        return not req['all']
    elif 'rat_count' in req:
        return req['rat_count'] == 0
    elif 'ability_check_with_dc' in req:
        return True
    else:
        return False

def _is_satisfied(player: int, req: AutopelagoGameRequirement, state: CollectionState):
    if 'all' in req:
        return all(_is_satisfied(player, sub_req, state) for sub_req in req['all'])
    elif 'any' in req:
        return any(_is_satisfied(player, sub_req, state) for sub_req in req['any'])
    elif 'item' in req:
        return state.has(item_key_to_name[req['item']], player)
    elif 'rat_count' in req:
        return sum(item_name_to_rat_count[k] * i for k, i in state.prog_items[player].items() if k in item_name_to_rat_count) >= req['rat_count']
    else:
        assert 'ability_check_with_dc' in req, 'Only AutopelagoAbilityCheckRequirement is expected here'
        return True


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

    def __init__(self, autopelago_definition: AutopelagoRegionDefinition, player: int, multiworld: MultiWorld, hint: Optional[str] = None):
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
    topology_present = False # it's static, so setting this to True isn't actually helpful
    data_version = 0
    web = AutopelagoWebWorld()

    # item_name_to_id and location_name_to_id must be filled VERY early, but seemingly only because
    # they are used in Main.main to log the ID ranges in use. if not for that, we probably could've
    # been able to get away with populating these just based on what we actually need.
    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
        self.logger = logging.getLogger(GAME_NAME)

    # insert other ClassVar values... suggestions include:
    # - item_name_groups
    # - item_descriptions
    # - location_name_groups
    # - location_descriptions
    # - hint_blacklist (should it include the goal item?)

    def create_item(self, name: str, classification: ItemClassification | None = None):
        id = item_name_to_id[name] if name in item_name_to_id else None
        classification = classification or item_name_to_defined_classification[name]
        assert classification is not None, 'Classification should either be defined, calculated during generate_early, or hardcoded.'
        item = AutopelagoItem(name, classification, id, self.player)
        return item

    def create_items(self):
        self.multiworld.itempool += (self.create_item(item) for item in location_name_to_unrandomized_progression_item_name.values())

        nonprogression_item_table = { c: [item_name for item_name in items] for c, items in generic_nonprogression_item_table.items() }
        dlc_games = { game for game in game_specific_nonprogression_items }
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

        category_to_next_offset: dict[AutopelagoNonProgressionItemType, int] = { category: 0 for category in generic_nonprogression_item_table }
        next_filler_becomes_trap = False
        for nonprog_type in location_name_to_unrandomized_nonprogression_item.values():
            if nonprog_type == 'filler':
                if next_filler_becomes_trap:
                    nonprog_type = 'trap'
                next_filler_becomes_trap = not next_filler_becomes_trap

            classification = autopelago_item_classification_of(nonprog_type)
            if category_to_next_offset[nonprog_type] > len(nonprogression_item_table[nonprog_type]):
                nonprog_type = 'uncategorized'
            next_item = nonprogression_item_table[nonprog_type][category_to_next_offset[nonprog_type]]
            self.multiworld.itempool.append(self.create_item(next_item, classification))
            category_to_next_offset[nonprog_type] += 1

    def create_regions(self):
        new_regions = { r.key: AutopelagoRegion(r, self.player, self.multiworld) for r in autopelago_regions.values() }
        for r in new_regions.values():
            self.multiworld.regions.append(r)
            req = r.autopelago_definition.requires
            for exit in r.autopelago_definition.exits:
                rule = lambda state: _is_satisfied(self.player, req, state)
                r.connect(new_regions[exit], '', None if _is_trivial(req) else rule)

        self.multiworld.get_location('Victory', self.player).place_locked_item(self.create_item('Victory', ItemClassification.progression))
        self.multiworld.completion_condition[self.player] = lambda state: state.has('Victory', self.player)

    def get_filler_item_name(self) -> str:
        return "Monkey's Paw"
