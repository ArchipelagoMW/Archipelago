import logging
import os

logger = logging.getLogger("Ocarina of Time")

from .Location import OOTLocation, LocationFactory
from .Entrance import OOTEntrance
from .Items import item_table, MakeEventItem
from .Regions import TimeOfDay
# from .Rules import set_rules
from .RuleParser import Rule_AST_Transformer
from .Options import oot_options
from .Utils import data_path, read_json
from .DungeonList import create_dungeons

import Utils
from BaseClasses import Region, Entrance, Location, MultiWorld, Item
from ..AutoWorld import World


class OOTWorld(World):
    game: str = "Ocarina of Time"
    options = oot_options

    def __init__(self, world, player):
        super(OOTWorld, self).__init__(world, player)
        self.parser = Rule_AST_Transformer(self, self.player)
        for (option_name, option) in oot_options.items(): 
            setattr(self, option_name, getattr(self.world, option_name, option.default))
        self.ensure_tod_access = False
        # self.ensure_tod_access = self.shuffle_interior_entrances or self.shuffle_overworld_entrances or self.randomize_overworld_spawns

    def load_regions_from_json(self, file_path):
        region_json = read_json(file_path)
            
        for region in region_json:
            new_region = OOTRegion(region['region_name'], None, None, self.player)
            new_region.world = self.world
            if 'scene' in region:
                new_region.scene = region['scene']
            if 'hint' in region:
                new_region.hint_text = region['hint']  # changed from new_region.hint
            if 'dungeon' in region:
                new_region.dungeon = region['dungeon']
            if 'time_passes' in region:
                new_region.time_passes = region['time_passes']
                new_region.provides_time = TimeOfDay.ALL
            if new_region.name == 'Ganons Castle Grounds':
                new_region.provides_time = TimeOfDay.DAMPE
            if 'locations' in region:
                for location, rule in region['locations'].items():
                    new_location = LocationFactory(location, self.player)
                    new_location.parent_region = new_region
                    new_location.rule_string = rule
                    if self.world.logic_rules != 'none':
                        self.parser.parse_spot_rule(new_location)
                    if new_location.never:
                        # We still need to fill the location even if ALR is off.
                        logging.getLogger('').debug('Unreachable location: %s', new_location.name)
                    # new_location.world = world
                    new_location.player = self.player
                    new_region.locations.append(new_location)
            if 'events' in region:
                for event, rule in region['events'].items():
                    # Allow duplicate placement of events
                    lname = '%s from %s' % (event, new_region.name)
                    new_location = OOTLocation(lname, type='Event', parent=new_region)
                    new_location.rule_string = rule
                    if self.world.logic_rules != 'none':
                        self.parser.parse_spot_rule(new_location)
                    if new_location.never:
                        logging.getLogger('').debug('Dropping unreachable event: %s', new_location.name)
                    else:
                        # new_location.world = world
                        new_location.player = self.player
                        new_region.locations.append(new_location)
                        MakeEventItem(self.world, self.player, event, new_location)
            if 'exits' in region:
                for exit, rule in region['exits'].items():
                    new_exit = OOTEntrance(self.player, '%s -> %s' % (new_region.name, exit), new_region)
                    new_exit.connected_region = exit
                    new_exit.rule_string = rule
                    if self.world.logic_rules != 'none':
                        self.parser.parse_spot_rule(new_exit)
                    if new_exit.never:
                        logging.getLogger('').debug('Dropping unreachable exit: %s', new_exit.name)
                    else:
                        new_region.exits.append(new_exit)
            self.world.regions.append(new_region)


    def create_regions(self):  # build_world_graphs
        logger.info('Generating World.')
        overworld_data_path = data_path('World', 'Overworld.json')
        self.load_regions_from_json(overworld_data_path)
        create_dungeons(self)
        self.parser.create_delayed_rules() # replaces self.create_internal_locations(); I don't know exactly what it does though

        # if settings.shopsanity != 'off':
        #     world.random_shop_prices()
        # world.set_scrub_prices()

        # logger.info('Generating Item Pool.')
        # generate_itempool(world)
        # set_shop_rules(world)
        # set_drop_location_names(world)
        # world.fill_bosses()

        # if settings.triforce_hunt:
        #     settings.distribution.configure_triforce_hunt(worlds)

        # logger.info('Setting Entrances.')
        # set_entrances(worlds)
        # return worlds


    def set_rules(self):  # what does this even have to do?
        logger.info('Calculating Access Rules.')


    def generate_basic(self):  # link entrances, generate item pools, place fixed items
        logger.info('Generating Item Pool.')
        # generate_itempool(world)
        # set_shop_rules(world)
        # set_drop_location_names(world)
        # world.fill_bosses()

        # if settings.triforce_hunt:
        #     settings.distribution.configure_triforce_hunt(worlds)

        logger.info('Setting Entrances.')
        # set_entrances(worlds)
        # return worlds


    def generate_output(self):  # ROM patching, cosmetics, etc. 
        logger.info('Patching ROM.') 



class OOTRegion(Region): 
    game: str = "Ocarina of Time"

    def __init__(self, name: str, type, hint, player: int):
        super(OOTRegion, self).__init__(name, type, hint, player)

