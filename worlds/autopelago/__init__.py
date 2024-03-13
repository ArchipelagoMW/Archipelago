import logging

# TODO: stabilize the imports, don't just import *
from .AutopelagoDefinitions import *

from BaseClasses import CollectionState, Entrance, Item, Location, Region, Tutorial
from worlds.AutoWorld import World, WebWorld


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

    def _is_satisfied(self, req: AutopelagoGameRequirement, state: CollectionState):
        if 'all' in req:
            return all(self._is_satisfied(sub_req, state) for sub_req in req['all'])
        elif 'any' in req:
            return any(self._is_satisfied(sub_req, state) for sub_req in req['any'])
        elif 'item' in req:
            return state.has(item_key_to_name[req['item']], self.player)
        elif 'rat_count' in req:
            return sum(item_name_to_rat_count[k] * i for k, i in state.prog_items[self.player].items() if k in item_name_to_rat_count) >= req['rat_count']
        else:
            assert 'ability_check_with_dc' in req, 'Only AutopelagoAbilityCheckRequirement is expected here'
            return True

    def create_item(self, name: str, classification: ItemClassification | None = None):
        id = item_name_to_id[name]
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

        category_to_next_offset = { category: 0 for category in generic_nonprogression_item_table }
        next_is_trap = False
        for nonprog_type in location_name_to_unrandomized_nonprogression_item.values():
            if nonprog_type == 'filler' and next_is_trap:
                nonprog_type = 'trap'
            next_is_trap = not next_is_trap
            classification = autopelago_item_classification_of(nonprog_type)
            if category_to_next_offset[nonprog_type] > len(nonprogression_item_table[nonprog_type]):
                nonprog_type = 'uncategorized'
            next_item = nonprogression_item_table[nonprog_type][category_to_next_offset[nonprog_type]]
            self.multiworld.itempool.append(self.create_item(next_item, classification))
            category_to_next_offset[nonprog_type] += 1

    def create_regions(self):
        new_regions = { r.key: self.create_region(r) for r in autopelago_regions.values() }
        for new_r in new_regions.values():
            self.multiworld.regions.append(new_r)

            old_r = autopelago_regions[new_r.name]
            for exit in old_r.exits:
                connection = Entrance(self.player, exit, new_r)
                connection.access_rule = lambda state: self._is_satisfied(old_r.requires, state)
                new_r.exits.append(connection)
                connection.connect(new_regions[exit])

        new_regions['goal'].locations[0].place_locked_item(self.create_item('goal', ItemClassification.progression))
        self.multiworld.completion_condition[self.player] = lambda state: state.has('goal', self.player)

    def create_region(self, r: AutopelagoRegionDefinition):
        region = Region(r.key, self.player, self.multiworld)
        for loc in r.locations:
            location_id = self.location_name_to_id[loc]
            location = AutopelagoLocation(self.player, loc, location_id, region)
            requires = location_name_to_requirement[loc]
            location.access_rule = lambda state: self._is_satisfied(requires, state)
            region.locations.append(location)
        return region

    def get_filler_item_name(self) -> str:
        return "Monkey's Paw"
