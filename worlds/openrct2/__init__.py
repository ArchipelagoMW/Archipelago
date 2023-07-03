from typing import NamedTuple, Union
import logging
import json
from .options import *

from BaseClasses import Item, Tutorial, ItemClassification

from ..AutoWorld import World, WebWorld
from NetUtils import SlotType


class OpenRCT2WebWorld(WebWorld):
    advanced_settings = Tutorial('Advanced YAML Guide',
                                 'A guide to reading YAML files and editing them to fully customize your game.',
                                 'English', 'advanced_settings_en.md', 'advanced_settings/en',
                                 ['alwaysintreble', 'Alchav'])
    commands = Tutorial('Archipelago Server and Client Commands',
                        'A guide detailing the commands available to the user when participating in an Archipelago session.',
                        'English', 'commands_en.md', 'commands/en', ['jat2980', 'Ijwu'])
    plando = Tutorial('Archipelago Plando Guide', 'A guide to understanding and using plando for your game.',
                      'English', 'plando_en.md', 'plando/en', ['alwaysintreble', 'Alchav'])
    setup = Tutorial('Getting Started',
                     'A guide to setting up the Archipelago software, and generating, hosting, and connecting to '
                     'multiworld games.',
                     'English', 'setup_en.md', 'setup/en', ['alwaysintreble'])
    triggers = Tutorial('Archipelago Triggers Guide', 'A guide to setting up and using triggers in your game settings.',
                        'English', 'triggers_en.md', 'triggers/en', ['alwaysintreble'])
    tutorials = [setup, mac, commands, advanced_settings, triggers, plando]


class OpenRCT2World(World):
    """
    OpenRCT2 is an awesome game! Blow up roller coasters!
    """

    game = "OpenRCT2"
    topology_present = True
    
    option_definitions = openRCT2_options  # options the player can set
    topology_present = True  # show path to required location checks in spoiler

    # ID of first item and location, could be hard-coded but code may be easier
    # to read with this as a propery.
    base_id = 2000000
    # Instead of dynamic numbering, IDs could be part of data.

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = {name: id for
                       id, name in enumerate(mygame_items, base_id)}
    location_name_to_id = {name: id for
                           id, name in enumerate(mygame_locations, base_id)}