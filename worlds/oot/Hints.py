import io
import hashlib
import logging
import os
import struct
import random
from collections import OrderedDict
import urllib.request
from urllib.error import URLError, HTTPError
import json
from enum import Enum

from BaseClasses import Region
from .Items import OOTItem
from .HintList import getHint, getHintGroup, Hint, hintExclusions, \
    misc_item_hint_table, misc_location_hint_table
from .Messages import COLOR_MAP, update_message_by_id
from .TextBox import line_wrap, character_table, rom_safe_text
from .Utils import data_path, read_json


bingoBottlesForHints = (
    "Bottle", "Bottle with Red Potion","Bottle with Green Potion", "Bottle with Blue Potion",
    "Bottle with Fairy", "Bottle with Fish", "Bottle with Blue Fire", "Bottle with Bugs",
    "Bottle with Big Poe", "Bottle with Poe",
)

defaultHintDists = [
    'async.json', 'balanced.json', 'bingo.json', 'chaos.json', 'coop2.json',
    'ddr.json', 'league.json', 'mw3.json', 'scrubs.json', 'strong.json',
    'tournament.json', 'useless.json', 'very_strong.json',
    'very_strong_magic.json', 'weekly.json'
]

class RegionRestriction(Enum):
    NONE = 0,
    DUNGEON = 1,
    OVERWORLD = 2,


class GossipStone():
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.reachable = True


class GossipText():
    def __init__(self, text, colors=None, prefix="They say that "):
        text = prefix + text
        text = text[:1].upper() + text[1:]
        self.text = text
        self.colors = colors


    def to_json(self):
        return {'text': self.text, 'colors': self.colors}


    def __str__(self):
        return get_raw_text(line_wrap(colorText(self)))

#   Abbreviations
#       DMC     Death Mountain Crater
#       DMT     Death Mountain Trail
#       GC      Goron City
#       GV      Gerudo Valley
#       HC      Hyrule Castle
#       HF      Hyrule Field
#       KF      Kokiri Forest
#       LH      Lake Hylia
#       LW      Lost Woods
#       SFM     Sacred Forest Meadow
#       ToT     Temple of Time
#       ZD      Zora's Domain
#       ZF      Zora's Fountain
#       ZR      Zora's River

gossipLocations = {
    0x0405: GossipStone('DMC (Bombable Wall)',              'DMC Gossip Stone'),
    0x0404: GossipStone('DMT (Biggoron)',                   'DMT Gossip Stone'),
    0x041A: GossipStone('Colossus (Spirit Temple)',         'Colossus Gossip Stone'),
    0x0414: GossipStone('Dodongos Cavern (Bombable Wall)',  'Dodongos Cavern Gossip Stone'),
    0x0411: GossipStone('GV (Waterfall)',                   'GV Gossip Stone'),
    0x0415: GossipStone('GC (Maze)',                        'GC Maze Gossip Stone'),
    0x0419: GossipStone('GC (Medigoron)',                   'GC Medigoron Gossip Stone'),
    0x040A: GossipStone('Graveyard (Shadow Temple)',        'Graveyard Gossip Stone'),
    0x0412: GossipStone('HC (Malon)',                       'HC Malon Gossip Stone'),
    0x040B: GossipStone('HC (Rock Wall)',                   'HC Rock Wall Gossip Stone'),
    0x0413: GossipStone('HC (Storms Grotto)',               'HC Storms Grotto Gossip Stone'),
    0x041F: GossipStone('KF (Deku Tree Left)',              'KF Deku Tree Gossip Stone (Left)'),
    0x0420: GossipStone('KF (Deku Tree Right)',             'KF Deku Tree Gossip Stone (Right)'),
    0x041E: GossipStone('KF (Outside Storms)',              'KF Gossip Stone'),
    0x0403: GossipStone('LH (Lab)',                         'LH Lab Gossip Stone'),
    0x040F: GossipStone('LH (Southeast Corner)',            'LH Gossip Stone (Southeast)'),
    0x0408: GossipStone('LH (Southwest Corner)',            'LH Gossip Stone (Southwest)'),
    0x041D: GossipStone('LW (Bridge)',                      'LW Gossip Stone'),
    0x0416: GossipStone('SFM (Maze Lower)',                 'SFM Maze Gossip Stone (Lower)'),
    0x0417: GossipStone('SFM (Maze Upper)',                 'SFM Maze Gossip Stone (Upper)'),
    0x041C: GossipStone('SFM (Saria)',                      'SFM Saria Gossip Stone'),
    0x0406: GossipStone('ToT (Left)',                       'ToT Gossip Stone (Left)'),
    0x0407: GossipStone('ToT (Left-Center)',                'ToT Gossip Stone (Left-Center)'),
    0x0410: GossipStone('ToT (Right)',                      'ToT Gossip Stone (Right)'),
    0x040E: GossipStone('ToT (Right-Center)',               'ToT Gossip Stone (Right-Center)'),
    0x0409: GossipStone('ZD (Mweep)',                       'ZD Gossip Stone'),
    0x0401: GossipStone('ZF (Fairy)',                       'ZF Fairy Gossip Stone'),
    0x0402: GossipStone('ZF (Jabu)',                        'ZF Jabu Gossip Stone'),
    0x040D: GossipStone('ZR (Near Grottos)',                'ZR Near Grottos Gossip Stone'),
    0x040C: GossipStone('ZR (Near Domain)',                 'ZR Near Domain Gossip Stone'),
    0x041B: GossipStone('HF (Cow Grotto)',                  'HF Cow Grotto Gossip Stone'),

    0x0430: GossipStone('HF (Near Market Grotto)',          'HF Near Market Grotto Gossip Stone'),
    0x0432: GossipStone('HF (Southeast Grotto)',            'HF Southeast Grotto Gossip Stone'),
    0x0433: GossipStone('HF (Open Grotto)',                 'HF Open Grotto Gossip Stone'),
    0x0438: GossipStone('Kak (Open Grotto)',                'Kak Open Grotto Gossip Stone'),
    0x0439: GossipStone('ZR (Open Grotto)',                 'ZR Open Grotto Gossip Stone'),
    0x043C: GossipStone('KF (Storms Grotto)',               'KF Storms Grotto Gossip Stone'),
    0x0444: GossipStone('LW (Near Shortcuts Grotto)',       'LW Near Shortcuts Grotto Gossip Stone'),
    0x0447: GossipStone('DMT (Storms Grotto)',              'DMT Storms Grotto Gossip Stone'),
    0x044A: GossipStone('DMC (Upper Grotto)',               'DMC Upper Grotto Gossip Stone'),
}

gossipLocations_reversemap = {
    stone.name : stone_id for stone_id, stone in gossipLocations.items()
}

def getItemGenericName(item):
    if item.game != "Ocarina of Time":
        return item.name
    elif item.dungeonitem:
        return item.type
    else:
        return item.name


def isRestrictedDungeonItem(dungeon, item):
    if not isinstance(item, OOTItem):
        return False
    if (item.map or item.compass) and dungeon.world.options.shuffle_mapcompass == 'dungeon':
        return item in dungeon.dungeon_items
    if item.type == 'SmallKey' and dungeon.world.options.shuffle_smallkeys == 'dungeon':
        return item in dungeon.small_keys
    if item.type == 'BossKey' and dungeon.world.options.shuffle_bosskeys == 'dungeon':
        return item in dungeon.boss_key
    if item.type == 'GanonBossKey' and dungeon.world.options.shuffle_ganon_bosskey == 'dungeon':
        return item in dungeon.boss_key
    return False


# Attach a player name to the item or location text.
# If the associated player of the item/location and the world are the same, does nothing.
# Otherwise, attaches the object's player's name to the string, calling rom_safe_text for foreign items/locations.
def attach_name(text, hinted_object, world):
    if hinted_object.player == world.player:
        return text
    return rom_safe_text(f"{world.multiworld.get_player_name(hinted_object.player)}'s {text}")


def add_hint(world, groups, gossip_text, count, location=None, force_reachable=False):
    world.hint_rng.shuffle(groups)
    skipped_groups = []
    duplicates = []
    first = True
    success = True
    # early failure if not enough
    if len(groups) < int(count):
        return False
    # Randomly round up, if we have enough groups left
    total = int(world.hint_rng.random() + count) if len(groups) > count else int(count)
    while total:
        if groups:
            group = groups.pop(0)

            if any(map(lambda id: gossipLocations[id].reachable, group)):
                stone_names = [gossipLocations[id].location for id in group]
                # stone_locations = [world.get_location(stone_name) for stone_name in stone_names]
                # Taking out all checks on gossip stone reachability and hint logic
                if not first or True: # or any(map(lambda stone_location: can_reach_hint(worlds, stone_location, location), stone_locations)):
                    # if first and location:
                    #     # just name the event item after the gossip stone directly
                    #     event_item = None
                    #     for i, stone_name in enumerate(stone_names):
                    #         # place the same event item in each location in the group
                    #         if event_item is None:
                    #             event_item = MakeEventItem(stone_name, stone_locations[i], event_item)
                    #         else:
                    #             MakeEventItem(stone_name, stone_locations[i], event_item)

                    #     # This mostly guarantees that we don't lock the player out of an item hint
                    #     # by establishing a (hint -> item) -> hint -> item -> (first hint) loop
                    #     location.add_rule(world.parser.parse_rule(repr(event_item.name)))

                    total -= 1
                    first = False
                    for id in group:
                        world.gossip_hints[id] = gossip_text
                    # Immediately start choosing duplicates from stones we passed up earlier
                    while duplicates and total:
                        group = duplicates.pop(0)
                        total -= 1
                        for id in group:
                            world.gossip_hints[id] = gossip_text
                else:
                    # Temporarily skip this stone but consider it for duplicates
                    duplicates.append(group)
            else:
                if not force_reachable:
                    # The stones are not readable at all in logic, so we ignore any kind of logic here
                    if not first:
                        total -= 1
                        for id in group:
                            world.gossip_hints[id] = gossip_text
                    else:
                        # Temporarily skip this stone but consider it for duplicates
                        duplicates.append(group)
                else:
                    # If flagged to guarantee reachable, then skip
                    # If no stones are reachable, then this will place nothing
                    skipped_groups.append(group)
        else:
            # Out of groups
            if not force_reachable and len(duplicates) >= total:
                # Didn't find any appropriate stones for this hint, but maybe enough completely unreachable ones.
                # We'd rather not use reachable stones for this.
                unr = [group for group in duplicates if all(map(lambda id: not gossipLocations[id].reachable, group))]
                if len(unr) >= total:
                    duplicates = [group for group in duplicates if group not in unr[:total]]
                    for group in unr[:total]:
                        for id in group:
                            world.gossip_hints[id] = gossip_text
                    # Success
                    break
            # Failure
            success = False
            break
    groups.extend(duplicates)
    groups.extend(skipped_groups)
    return success



def writeGossipStoneHints(world, messages):
    for id, gossip_text in world.gossip_hints.items():
        update_message_by_id(messages, id, str(gossip_text), 0x23)


def filterTrailingSpace(text):
    if text.endswith('& '):
        return text[:-1]
    else:
        return text


hintPrefixes = [
    'a few ',
    'some ',
    'plenty of ',
    'a ',
    'an ',
    'the ',
    '',
]

def getSimpleHintNoPrefix(item, rand):
    hint = getHint(item.name, rand, True).text

    for prefix in hintPrefixes:
        if hint.startswith(prefix):
            # return without the prefix
            return hint[len(prefix):]

    # no prefex
    return hint


def colorText(gossip_text):
    text = gossip_text.text
    colors = list(gossip_text.colors) if gossip_text.colors is not None else []
    color = 'White'

    while '#' in text:
        splitText = text.split('#', 2)
        if len(colors) > 0:
            color = colors.pop()

        for prefix in hintPrefixes:
            if splitText[1].startswith(prefix):
                splitText[0] += splitText[1][:len(prefix)]
                splitText[1] = splitText[1][len(prefix):]
                break

        splitText[1] = '\x05' + COLOR_MAP[color] + splitText[1] + '\x05\x40'
        text = ''.join(splitText)

    return text


class HintAreaNotFound(RuntimeError):
    pass


class HintArea(Enum):
    # internal name          prepositions        display name                  short name                color         internal dungeon name
    #                        vague     clear
    ROOT                   = 'in',     'in',     "Link's pocket",              'Free',                   'White',      None
    HYRULE_FIELD           = 'in',     'in',     'Hyrule Field',               'Hyrule Field',           'Light Blue', None
    LON_LON_RANCH          = 'at',     'at',     'Lon Lon Ranch',              'Lon Lon Ranch',          'Light Blue', None
    MARKET                 = 'in',     'in',     'the Market',                 'Market',                 'Light Blue', None
    TEMPLE_OF_TIME         = 'inside', 'inside', 'the Temple of Time',         'Temple of Time',         'Light Blue', None
    CASTLE_GROUNDS         = 'on',     'on',     'the Castle Grounds',         None,                     'Light Blue', None # required for warp songs
    HYRULE_CASTLE          = 'at',     'at',     'Hyrule Castle',              'Hyrule Castle',          'Light Blue', None
    OUTSIDE_GANONS_CASTLE  = None,     None,     "outside Ganon's Castle",     "Outside Ganon's Castle", 'Light Blue', None
    INSIDE_GANONS_CASTLE   = 'inside', None,     "inside Ganon's Castle",      "Inside Ganon's Castle",  'Light Blue', 'Ganons Castle'
    GANONDORFS_CHAMBER     = 'in',     'in',     "Ganondorf's Chamber",        "Ganondorf's Chamber",    'Light Blue', None
    KOKIRI_FOREST          = 'in',     'in',     'Kokiri Forest',              "Kokiri Forest",          'Green',      None
    DEKU_TREE              = 'inside', 'inside', 'the Deku Tree',              "Deku Tree",              'Green',      'Deku Tree'
    LOST_WOODS             = 'in',     'in',     'the Lost Woods',             "Lost Woods",             'Green',      None
    SACRED_FOREST_MEADOW   = 'at',     'at',     'the Sacred Forest Meadow',   "Sacred Forest Meadow",   'Green',      None
    FOREST_TEMPLE          = 'in',     'in',     'the Forest Temple',          "Forest Temple",          'Green',      'Forest Temple'
    DEATH_MOUNTAIN_TRAIL   = 'on',     'on',     'the Death Mountain Trail',   "Death Mountain Trail",   'Red',        None
    DODONGOS_CAVERN        = 'within', 'in',     "Dodongo's Cavern",           "Dodongo's Cavern",       'Red',        'Dodongos Cavern'
    GORON_CITY             = 'in',     'in',     'Goron City',                 "Goron City",             'Red',        None
    DEATH_MOUNTAIN_CRATER  = 'in',     'in',     'the Death Mountain Crater',  "Death Mountain Crater",  'Red',        None
    FIRE_TEMPLE            = 'on',     'in',     'the Fire Temple',            "Fire Temple",            'Red',        'Fire Temple'
    ZORA_RIVER             = 'at',     'at',     "Zora's River",               "Zora's River",           'Blue',       None
    ZORAS_DOMAIN           = 'at',     'at',     "Zora's Domain",              "Zora's Domain",          'Blue',       None
    ZORAS_FOUNTAIN         = 'at',     'at',     "Zora's Fountain",            "Zora's Fountain",        'Blue',       None
    JABU_JABUS_BELLY       = 'in',     'inside', "Jabu Jabu's Belly",          "Jabu Jabu's Belly",      'Blue',       'Jabu Jabus Belly'
    ICE_CAVERN             = 'inside', 'in'    , 'the Ice Cavern',             "Ice Cavern",             'Blue',       'Ice Cavern'
    LAKE_HYLIA             = 'at',     'at',     'Lake Hylia',                 "Lake Hylia",             'Blue',       None
    WATER_TEMPLE           = 'under',  'in',     'the Water Temple',           "Water Temple",           'Blue',       'Water Temple'
    KAKARIKO_VILLAGE       = 'in',     'in',     'Kakariko Village',           "Kakariko Village",       'Pink',       None
    BOTTOM_OF_THE_WELL     = 'within', 'at',     'the Bottom of the Well',     "Bottom of the Well",     'Pink',       'Bottom of the Well'
    GRAVEYARD              = 'in',     'in',     'the Graveyard',              "Graveyard",              'Pink',       None
    SHADOW_TEMPLE          = 'within', 'in',     'the Shadow Temple',          "Shadow Temple",          'Pink',       'Shadow Temple'
    GERUDO_VALLEY          = 'at',     'at',     'Gerudo Valley',              "Gerudo Valley",          'Yellow',     None
    GERUDO_FORTRESS        = 'at',     'at',     "Gerudo's Fortress",          "Gerudo's Fortress",      'Yellow',     None
    GERUDO_TRAINING_GROUND = 'within', 'on',     'the Gerudo Training Ground', "Gerudo Training Ground", 'Yellow',     'Gerudo Training Ground'
    HAUNTED_WASTELAND      = 'in',     'in',     'the Haunted Wasteland',      "Haunted Wasteland",      'Yellow',     None
    DESERT_COLOSSUS        = 'at',     'at',     'the Desert Colossus',        "Desert Colossus",        'Yellow',     None
    SPIRIT_TEMPLE          = 'inside', 'in',     'the Spirit Temple',          "Spirit Temple",          'Yellow',     'Spirit Temple'

    # Performs a breadth first search to find the closest hint area from a given spot (region, location, or entrance).
    # May fail to find a hint if the given spot is only accessible from the root and not from any other region with a hint area
    @staticmethod
    def at(spot, use_alt_hint=False):
        if isinstance(spot, Region):
            original_parent = spot
        else:
            original_parent = spot.parent_region
        already_checked = []
        spot_queue = [spot]

        while spot_queue:
            current_spot = spot_queue.pop(0)
            already_checked.append(current_spot)

            if isinstance(current_spot, Region):
                parent_region = current_spot
            else:
                parent_region = current_spot.parent_region

            if parent_region.hint and (original_parent.name == 'Root' or parent_region.name != 'Root'):
                if use_alt_hint and parent_region.alt_hint:
                    return parent_region.alt_hint
                return parent_region.hint

            spot_queue.extend(filter(lambda ent: ent not in already_checked, parent_region.entrances))

        raise HintAreaNotFound('No hint area could be found for %s [World %d]' % (spot, spot.player))

    @classmethod
    def for_dungeon(cls, dungeon_name: str):
        if '(' in dungeon_name and ')' in dungeon_name:
            # A dungeon item name was passed in - get the name of the dungeon from it.
            dungeon_name = dungeon_name[dungeon_name.index('(') + 1:dungeon_name.index(')')]

        if dungeon_name == "Thieves Hideout":
            # Special case for Thieves' Hideout - change this if it gets its own hint area.
            return HintArea.GERUDO_FORTRESS

        for hint_area in cls:
            if hint_area.dungeon_name == dungeon_name:
                return hint_area
        return None

    def preposition(self, clearer_hints):
        return self.value[1 if clearer_hints else 0]

    def __str__(self):
        return self.value[2]

    # used for dungeon reward locations in the pause menu
    @property
    def short_name(self):
        return self.value[3]

    # Hint areas are further grouped into colored sections of the map by association with the medallions.
    # These colors are used to generate the text boxes for shuffled warp songs.
    @property
    def color(self):
        return self.value[4]

    @property
    def dungeon_name(self):
        return self.value[5]

    @property
    def is_dungeon(self):
        return self.dungeon_name is not None

    def is_dungeon_item(self, item):
        for dungeon in item.world.dungeons:
            if dungeon.name == self.dungeon_name:
                return dungeon.is_dungeon_item(item)
        return False

    # Formats the hint text for this area with proper grammar.
    # Dungeons are hinted differently depending on the clearer_hints setting.
    def text(self, rand, clearer_hints, preposition=False, world=None):
        if self.is_dungeon:
            text = getHint(self.dungeon_name, rand, clearer_hints).text
        else:
            text = str(self)
        prefix, suffix = text.replace('#', '').split(' ', 1)
        if world is None:
            if prefix == "Link's":
                text = f"@'s {suffix}"
        else:
            replace_prefixes = ('a', 'an', 'the')
            move_prefixes = ('outside', 'inside')
            if prefix in replace_prefixes:
                text = f"world {world}'s {suffix}"
            elif prefix in move_prefixes:
                text = f"{prefix} world {world}'s {suffix}"
            elif prefix == "Link's":
                text = f"player {world}'s {suffix}"
            else:
                text = f"world {world}'s {text}"
        if '#' not in text:
            text = f'#{text}#'
        if preposition and self.preposition(clearer_hints) is not None:
            text = f'{self.preposition(clearer_hints)} {text}'
        return text


# Peforms a breadth first search to find the closest hint area from a given spot (location or entrance)
# May fail to find a hint if the given spot is only accessible from the root and not from any other region with a hint area
# Returns the name of the location if the spot is not in OoT
def get_hint_area(spot):
    if spot.game == 'Ocarina of Time':
        already_checked = []
        spot_queue = [spot]

        while spot_queue:
            current_spot = spot_queue.pop(0)
            already_checked.append(current_spot)

            parent_region = current_spot.parent_region
        
            if parent_region.dungeon:
                return parent_region.dungeon.hint_text
            elif parent_region.hint and (spot.parent_region.name == 'Root' or parent_region.name != 'Root'):
                return parent_region.hint_text

            spot_queue.extend(list(filter(lambda ent: ent not in already_checked, parent_region.entrances)))

        raise HintAreaNotFound('No hint area could be found for %s [World %d]' % (spot, spot.player))
    else:
        return spot.name


def get_woth_hint(world, checked):
    locations = world.required_locations
    locations = list(filter(lambda location:
        location.name not in checked[location.player]
        and not (world.woth_dungeon >= world.hint_dist_user['dungeons_woth_limit']
                 and getattr(location.parent_region, "dungeon", None))
        and location.name not in world.hint_exclusions
        and location.name not in world.hint_type_overrides['woth']
        and location.item.name not in world.item_hint_type_overrides['woth'],
        locations))

    if not locations:
        return None

    location = world.hint_rng.choice(locations)
    checked[location.player].add(location.name)

    if getattr(location.parent_region, "dungeon", None):
        world.woth_dungeon += 1
        location_text = getHint(location.parent_region.dungeon.name, world.random, world.clearer_hints).text
    else:
        location_text = get_hint_area(location)

    if world.triforce_hunt:
        return (GossipText('#%s# is on the path of gold.' % location_text, ['Light Blue']), location)
    else:
        return (GossipText('#%s# is on the way of the hero.' % location_text, ['Light Blue']), location)


def get_barren_hint(world, checked):
    if not hasattr(world, 'get_barren_hint_prev'):
        world.get_barren_hint_prev = RegionRestriction.NONE

    areas = list(filter(lambda area:
        area not in checked[world.player]
        and area not in world.hint_type_overrides['barren']
        and not (world.barren_dungeon >= world.hint_dist_user['dungeons_barren_limit'] and world.empty_areas[area]['dungeon']),
        world.empty_areas.keys()))

    if not areas:
        return None

    # Randomly choose between overworld or dungeon
    dungeon_areas = list(filter(lambda area: world.empty_areas[area]['dungeon'], areas))
    overworld_areas = list(filter(lambda area: not world.empty_areas[area]['dungeon'], areas))
    if not dungeon_areas:
        # no dungeons left, default to overworld
        world.get_barren_hint_prev = RegionRestriction.OVERWORLD
    elif not overworld_areas:
        # no overworld left, default to dungeons
        world.get_barren_hint_prev = RegionRestriction.DUNGEON
    else:
        if world.get_barren_hint_prev == RegionRestriction.NONE:
            # 50/50 draw on the first hint
            world.get_barren_hint_prev = world.hint_rng.choices([RegionRestriction.DUNGEON, RegionRestriction.OVERWORLD], [0.5, 0.5])[0]
        elif world.get_barren_hint_prev == RegionRestriction.DUNGEON:
            # weights 75% against drawing dungeon again
            world.get_barren_hint_prev = world.hint_rng.choices([RegionRestriction.DUNGEON, RegionRestriction.OVERWORLD], [0.25, 0.75])[0]
        elif world.get_barren_hint_prev == RegionRestriction.OVERWORLD:
            # weights 75% against drawing overworld again
            world.get_barren_hint_prev = world.hint_rng.choices([RegionRestriction.DUNGEON, RegionRestriction.OVERWORLD], [0.75, 0.25])[0]

    if world.get_barren_hint_prev == RegionRestriction.DUNGEON:
        areas = dungeon_areas
    else:
        areas = overworld_areas
    if not areas:
        return None

    area_weights = [world.empty_areas[area]['weight'] for area in areas]
    if not any(area_weights):
        return None

    area = world.hint_rng.choices(areas, weights=area_weights)[0]
    if world.empty_areas[area]['dungeon']:
        world.barren_dungeon += 1

    checked[world.player].add(area)

    return (GossipText("plundering #%s# is a foolish choice." % area, ['Pink']), None)


def is_not_checked(location, checked):
    return not (location.name in checked[location.player] or get_hint_area(location) in checked)


def get_good_item_hint(world, checked):
    locations = list(filter(lambda location:
        is_not_checked(location, checked)
        and not location.locked
        and location.name not in world.hint_exclusions
        and location.name not in world.hint_type_overrides['item']
        and location.item.name not in world.item_hint_type_overrides['item'],
        world.major_item_locations))
    if not locations:
        return None

    location = world.hint_rng.choice(locations)
    checked[location.player].add(location.name)

    item_text = getHint(getItemGenericName(location.item), world.hint_rng, world.clearer_hints).text
    if getattr(location.parent_region, "dungeon", None):
        location_text = getHint(location.parent_region.dungeon.name, world.hint_rng, world.clearer_hints).text
        return (GossipText('#%s# hoards #%s#.' % (attach_name(location_text, location, world), attach_name(item_text, location.item, world)), 
            ['Green', 'Red']), location)
    else:
        location_text = get_hint_area(location)
        return (GossipText('#%s# can be found at #%s#.' % (attach_name(item_text, location.item, world), attach_name(location_text, location, world)), 
            ['Red', 'Green']), location)


def get_specific_item_hint(world, checked):
    if len(world.named_item_pool) == 0:
        logger = logging.getLogger('')
        logger.info("Named item hint requested, but pool is empty.")
        return None  
    while True:
        itemname = world.named_item_pool.pop(0)
        if itemname == "Bottle" and world.hint_dist == "bingo":
            locations = [
                location for location in world.multiworld.get_filled_locations()
                if (is_not_checked(location, checked)
                    and location.name not in world.hint_exclusions
                    and location.item.name in bingoBottlesForHints
                    and not location.locked
                    and location.name not in world.hint_type_overrides['named-item'])
            ]
        else:
            locations = [
                location for location in world.multiworld.get_filled_locations()
                if (is_not_checked(location, checked)
                    and location.name not in world.hint_exclusions
                    and location.item.name == itemname
                    and not location.locked
                    and location.name not in world.hint_type_overrides['named-item'])
            ]
        if len(locations) > 0:
            break
        if len(world.named_item_pool) == 0:
            return None

    location = world.hint_rng.choice(locations)
    checked[location.player].add(location.name)
    item_text = getHint(getItemGenericName(location.item), world.hint_rng, world.clearer_hints).text

    if getattr(location.parent_region, "dungeon", None):
        location_text = getHint(location.parent_region.dungeon.name, world.hint_rng, world.clearer_hints).text
        if world.hint_dist_user.get('vague_named_items', False):
            return (GossipText('#%s# may be on the hero\'s path.' % (location_text), ['Green']), location)
        else:
            return (GossipText('#%s# hoards #%s#.' % (attach_name(location_text, location, world), attach_name(item_text, location.item, world)), 
                ['Green', 'Red']), location)
    else:
        location_text = get_hint_area(location)
        if world.hint_dist_user.get('vague_named_items', False):
            return (GossipText('#%s# may be on the hero\'s path.' % (location_text), ['Green']), location)
        else:
            return (GossipText('#%s# can be found at #%s#.' % (attach_name(item_text, location.item, world), attach_name(location_text, location, world)), 
                ['Red', 'Green']), location)


def get_random_location_hint(world, checked):
    locations = list(filter(lambda location:
        is_not_checked(location, checked)
        and not (isinstance(location.item, OOTItem) and location.item.type in ('Drop', 'Event', 'Shop', 'DungeonReward'))
        # and not (location.parent_region.dungeon and isRestrictedDungeonItem(location.parent_region.dungeon, location.item)) # AP already locks dungeon items
        and not location.locked
        and location.name not in world.hint_exclusions
        and location.name not in world.hint_type_overrides['item']
        and location.item.name not in world.item_hint_type_overrides['item'],
                            world.multiworld.get_filled_locations(world.player)))
    if not locations:
        return None

    location = world.hint_rng.choice(locations)
    checked[location.player].add(location.name)
    dungeon = location.parent_region.dungeon

    item_text = getHint(getItemGenericName(location.item), world.hint_rng, world.clearer_hints).text
    if dungeon:
        location_text = getHint(dungeon.name, world.hint_rng, world.clearer_hints).text
        return (GossipText('#%s# hoards #%s#.' % (attach_name(location_text, location, world), attach_name(item_text, location.item, world)), 
            ['Green', 'Red']), location)
    else:
        location_text = get_hint_area(location)
        return (GossipText('#%s# can be found at #%s#.' % (attach_name(item_text, location.item, world), attach_name(location_text, location, world)), 
            ['Red', 'Green']), location)


def get_specific_hint(world, checked, type):
    hintGroup = getHintGroup(type, world)
    hintGroup = list(filter(lambda hint: is_not_checked(world.get_location(hint.name), checked), hintGroup))
    if not hintGroup:
        return None

    hint = world.hint_rng.choice(hintGroup)
    location = world.get_location(hint.name)
    checked[location.player].add(location.name)

    if location.name in world.hint_text_overrides:
        location_text = world.hint_text_overrides[location.name]
    else:
        location_text = hint.text
    if '#' not in location_text:
        location_text = '#%s#' % location_text
    item_text = getHint(getItemGenericName(location.item), world.hint_rng, world.clearer_hints).text

    return (GossipText('%s #%s#.' % (attach_name(location_text, location, world), attach_name(item_text, location.item, world)), 
        ['Green', 'Red']), location)


def get_sometimes_hint(world, checked):
    return get_specific_hint(world, checked, 'sometimes')


def get_song_hint(world, checked):
    return get_specific_hint(world, checked, 'song')


def get_overworld_hint(world, checked):
    return get_specific_hint(world, checked, 'overworld')


def get_dungeon_hint(world, checked):
    return get_specific_hint(world, checked, 'dungeon')


# probably broken
def get_entrance_hint(world, checked):
    if not world.entrance_shuffle:
        return None

    entrance_hints = list(filter(lambda hint: hint.name not in checked[world.player], getHintGroup('entrance', world)))
    shuffled_entrance_hints = list(filter(lambda entrance_hint: world.get_entrance(entrance_hint.name).shuffled, entrance_hints))

    regions_with_hint = [hint.name for hint in getHintGroup('region', world)]
    valid_entrance_hints = list(filter(lambda entrance_hint:
                                       (world.get_entrance(entrance_hint.name).connected_region.name in regions_with_hint or
                                        world.get_entrance(entrance_hint.name).connected_region.dungeon), shuffled_entrance_hints))

    if not valid_entrance_hints:
        return None

    entrance_hint = world.hint_rng.choice(valid_entrance_hints)
    entrance = world.get_entrance(entrance_hint.name)
    checked[world.player].add(entrance.name)

    entrance_text = entrance_hint.text

    if '#' not in entrance_text:
        entrance_text = '#%s#' % entrance_text

    connected_region = entrance.connected_region
    if connected_region.dungeon:
        region_text = getHint(connected_region.dungeon.name, world.hint_rng, world.clearer_hints).text
    else:
        region_text = getHint(connected_region.name, world.hint_rng, world.clearer_hints).text

    if '#' not in region_text:
        region_text = '#%s#' % region_text

    return (GossipText('%s %s.' % (entrance_text, region_text), ['Light Blue', 'Green']), None)


def get_junk_hint(world, checked):
    hints = getHintGroup('junk', world)
    hints = list(filter(lambda hint: hint.name not in checked[world.player], hints))
    if not hints:
        return None

    hint = world.hint_rng.choice(hints)
    checked[world.player].add(hint.name)

    return (GossipText(hint.text, prefix=''), None)


hint_func = {
    'trial':      lambda world, checked: None,
    'always':     lambda world, checked: None,
    'woth':             get_woth_hint,
    'barren':           get_barren_hint,
    'item':             get_good_item_hint,
    'sometimes':        get_sometimes_hint,
    'song':             get_song_hint,
    'overworld':        get_overworld_hint,
    'dungeon':          get_dungeon_hint,
    'entrance':         get_entrance_hint,
    'random':           get_random_location_hint,
    'junk':             get_junk_hint,
    'named-item':       get_specific_item_hint
}

hint_dist_keys = {
    'trial',
    'always',
    'woth',
    'barren',
    'item',
    'song',
    'overworld',
    'dungeon',
    'entrance',
    'sometimes',
    'random',
    'junk',
    'named-item'
}



# builds out general hints based on location and whether an item is required or not
def buildWorldGossipHints(world, checkedLocations=None):

    # rebuild hint exclusion list
    hintExclusions(world, clear_cache=True)

    world.barren_dungeon = 0
    world.woth_dungeon = 0

    if checkedLocations is None:
        checkedLocations = {player: set() for player in world.multiworld.get_all_ids()}

    # If Ganondorf hints Light Arrows and is reachable without them, add to checkedLocations to prevent extra hinting
    # Can only be forced with vanilla bridge or trials
    if world.bridge != 'vanilla' and world.trials == 0 and 'ganondorf' in world.misc_hints:
        try:
            light_arrow_location = world.multiworld.find_item("Light Arrows", world.player)
            checkedLocations[light_arrow_location.player].add(light_arrow_location.name)
        except StopIteration: # start with them
            pass

    stoneIDs = list(gossipLocations.keys())

    if 'disabled' in world.hint_dist_user:
        for stone_name in world.hint_dist_user['disabled']:
            try:
                stone_id = gossipLocations_reversemap[stone_name]
            except KeyError:
                raise ValueError(f'Gossip stone location "{stone_name}" is not valid')
            stoneIDs.remove(stone_id)
            (gossip_text, _) = get_junk_hint(world, checkedLocations)
            world.gossip_hints[stone_id] = gossip_text

    stoneGroups = []
    if 'groups' in world.hint_dist_user:
        for group_names in world.hint_dist_user['groups']:
            group = []
            for stone_name in group_names:
                try:
                    stone_id = gossipLocations_reversemap[stone_name]
                except KeyError:
                    raise ValueError(f'Gossip stone location "{stone_name}" is not valid')

                stoneIDs.remove(stone_id)
                group.append(stone_id)
            stoneGroups.append(group)
    # put the remaining locations into singleton groups
    stoneGroups.extend([[id] for id in stoneIDs])

    world.hint_rng.shuffle(stoneGroups)


    # Load hint distro from distribution file or pre-defined settings
    #
    # 'fixed' key is used to mimic the tournament distribution, creating a list of fixed hint types to fill
    # Once the fixed hint type list is exhausted, weighted random choices are taken like all non-tournament sets
    # This diverges from the tournament distribution where leftover stones are filled with sometimes hints (or random if no sometimes locations remain to be hinted)
    sorted_dist = {}
    type_count = 1
    hint_dist = OrderedDict({})
    fixed_hint_types = []
    max_order = 0
    for hint_type in world.hint_dist_user['distribution']:
        if world.hint_dist_user['distribution'][hint_type]['order'] > 0:
            hint_order = int(world.hint_dist_user['distribution'][hint_type]['order'])
            sorted_dist[hint_order] = hint_type
            if max_order < hint_order:
                max_order = hint_order
            type_count = type_count + 1
    if (type_count - 1) < max_order:
        raise Exception("There are gaps in the custom hint orders. Please revise your plando file to remove them.")
    for i in range(1, type_count):
        hint_type = sorted_dist[i]
        if world.hint_dist_user['distribution'][hint_type]['copies'] > 0:
            fixed_num = world.hint_dist_user['distribution'][hint_type]['fixed']
            hint_weight = world.hint_dist_user['distribution'][hint_type]['weight']
        else:
            fixed_num = 0
            hint_weight = 0
        hint_dist[hint_type] = (hint_weight, world.hint_dist_user['distribution'][hint_type]['copies'])
        hint_dist.move_to_end(hint_type)
        fixed_hint_types.extend([hint_type] * int(fixed_num))

    hint_types, hint_prob = zip(*hint_dist.items())
    hint_prob, _ = zip(*hint_prob)

    # Add required location hints, only if hint copies > 0
    if hint_dist['always'][1] > 0:
        alwaysLocations = getHintGroup('always', world)
        for hint in alwaysLocations:
            location = world.get_location(hint.name)
            checkedLocations[location.player].add(hint.name)
            if location.item.name in bingoBottlesForHints and world.hint_dist == 'bingo':
                always_item = 'Bottle'
            else:
                always_item = location.item.name
            if always_item in world.named_item_pool:
                world.named_item_pool.remove(always_item)

            if location.name in world.hint_text_overrides:
                location_text = world.hint_text_overrides[location.name]
            else:
                location_text = getHint(location.name, world.hint_rng, world.clearer_hints).text
            if '#' not in location_text:
                location_text = '#%s#' % location_text
            item_text = getHint(getItemGenericName(location.item), world.hint_rng, world.clearer_hints).text
            add_hint(world, stoneGroups, GossipText('%s #%s#.' % (attach_name(location_text, location, world), attach_name(item_text, location.item, world)), 
                ['Green', 'Red']), hint_dist['always'][1], location, force_reachable=True)
            logging.getLogger('').debug('Placed always hint for %s.', location.name)

    # Add trial hints, only if hint copies > 0
    if hint_dist['trial'][1] > 0:
        if world.trials_random and world.trials == 6:
            add_hint(world, stoneGroups, GossipText("#Ganon's Tower# is protected by a powerful barrier.", ['Pink']), hint_dist['trial'][1], force_reachable=True)
        elif world.trials_random and world.trials == 0:
            add_hint(world, stoneGroups, GossipText("Sheik dispelled the barrier around #Ganon's Tower#.", ['Yellow']), hint_dist['trial'][1], force_reachable=True)
        elif world.trials < 6 and world.trials > 3:
            for trial,skipped in world.skipped_trials.items():
                if skipped:
                    add_hint(world, stoneGroups,GossipText("the #%s Trial# was dispelled by Sheik." % trial, ['Yellow']), hint_dist['trial'][1], force_reachable=True)
        elif world.trials <= 3 and world.trials > 0:
            for trial,skipped in world.skipped_trials.items():
                if not skipped:
                    add_hint(world, stoneGroups, GossipText("the #%s Trial# protects Ganon's Tower." % trial, ['Pink']), hint_dist['trial'][1], force_reachable=True)

    # Add user-specified hinted item locations if using a built-in hint distribution
    # Raise error if hint copies is zero
    if len(world.named_item_pool) > 0 and world.hint_dist_user['named_items_required']:
        if hint_dist['named-item'][1] == 0:
            raise Exception('User-provided item hints were requested, but copies per named-item hint is zero')
        else:
            for i in range(0, len(world.named_item_pool)):
                hint = get_specific_item_hint(world, checkedLocations)
                if hint == None:
                    raise Exception('No valid hints for user-provided item')
                else:
                    gossip_text, location = hint
                    place_ok = add_hint(world, stoneGroups, gossip_text, hint_dist['named-item'][1], location)
                    if not place_ok:
                        raise Exception('Not enough gossip stones for user-provided item hints')
    
    # Shuffle named items hints
    # When all items are not required to be hinted, this allows for
    # opportunity-style hints to be drawn at random from the defined list.
    world.hint_rng.shuffle(world.named_item_pool)

    hint_types = list(hint_types)
    hint_prob  = list(hint_prob)
    hint_counts = {}

    custom_fixed = True
    while stoneGroups:
        if fixed_hint_types:
            hint_type = fixed_hint_types.pop(0)
            copies = hint_dist[hint_type][1]
            if copies > len(stoneGroups):
                # Quiet to avoid leaking information.
                logging.getLogger('').debug(f'Not enough gossip stone locations ({len(stoneGroups)} groups) for fixed hint type {hint_type} with {copies} copies, proceeding with available stones.')
                copies = len(stoneGroups)
        else:
            custom_fixed = False
            # Make sure there are enough stones left for each hint type
            num_types = len(hint_types)
            hint_types = list(filter(lambda htype: hint_dist[htype][1] <= len(stoneGroups), hint_types))
            new_num_types = len(hint_types)
            if new_num_types == 0:
                raise Exception('Not enough gossip stone locations for remaining weighted hint types.')
            elif new_num_types < num_types:
                hint_prob = []
                for htype in hint_types:
                    hint_prob.append(hint_dist[htype][0])
            try:
                # Weight the probabilities such that hints that are over the expected proportion
                # will be drawn less, and hints that are under will be drawn more.
                # This tightens the variance quite a bit. The variance can be adjusted via the power
                weighted_hint_prob = []
                for w1_type, w1_prob in zip(hint_types, hint_prob):
                    p = w1_prob
                    if p != 0: # If the base prob is 0, then it's 0
                        for w2_type, w2_prob in zip(hint_types, hint_prob):
                            if w2_prob != 0: # If the other prob is 0, then it has no effect
                                # Raising this term to a power greater than 1 will decrease variance
                                # Conversely, a power less than 1 will increase variance
                                p = p * (((hint_counts.get(w2_type, 0) / w2_prob) + 1) / ((hint_counts.get(w1_type, 0) / w1_prob) + 1))
                    weighted_hint_prob.append(p)

                hint_type = world.hint_rng.choices(hint_types, weights=weighted_hint_prob)[0]
                copies = hint_dist[hint_type][1]
            except IndexError:
                raise Exception('Not enough valid hints to fill gossip stone locations.')

        hint = hint_func[hint_type](world, checkedLocations)

        if hint == None:
            index = hint_types.index(hint_type)
            hint_prob[index] = 0
            # Zero out the probability in the base distribution in case the probability list is modified
            # to fit hint types in remaining gossip stones
            hint_dist[hint_type] = (0.0, copies)
        else:
            gossip_text, location = hint
            place_ok = add_hint(world, stoneGroups, gossip_text, copies, location)
            if place_ok:
                hint_counts[hint_type] = hint_counts.get(hint_type, 0) + 1
                if location is None:
                    logging.getLogger('').debug('Placed %s hint.', hint_type)
                else:
                    logging.getLogger('').debug('Placed %s hint for %s.', hint_type, location.name)
            if not place_ok and custom_fixed:
                logging.getLogger('').debug('Failed to place %s fixed hint for %s.', hint_type, location.name)
                fixed_hint_types.insert(0, hint_type)


# builds text that is displayed at the temple of time altar for child and adult, rewards pulled based off of item in a fixed order.
def buildAltarHints(world, messages, include_rewards=True, include_wincons=True):
    # text that appears at altar as a child.
    child_text = '\x08'
    if include_rewards:
        bossRewardsSpiritualStones = [
            ('Kokiri Emerald',   'Green'), 
            ('Goron Ruby',       'Red'), 
            ('Zora Sapphire',    'Blue'),
        ]
        child_text += getHint('Spiritual Stone Text Start', world.hint_rng, world.clearer_hints).text + '\x04'
        for (reward, color) in bossRewardsSpiritualStones:
            child_text += buildBossString(reward, color, world)
    child_text += getHint('Child Altar Text End', world.hint_rng, world.clearer_hints).text
    child_text += '\x0B'
    update_message_by_id(messages, 0x707A, get_raw_text(child_text), 0x20)

    # text that appears at altar as an adult.
    adult_text = '\x08'
    adult_text += getHint('Adult Altar Text Start', world.hint_rng, world.clearer_hints).text + '\x04'
    if include_rewards:
        bossRewardsMedallions = [
            ('Light Medallion',  'Light Blue'),
            ('Forest Medallion', 'Green'),
            ('Fire Medallion',   'Red'),
            ('Water Medallion',  'Blue'),
            ('Shadow Medallion', 'Pink'),
            ('Spirit Medallion', 'Yellow'),
        ]
        for (reward, color) in bossRewardsMedallions:
            adult_text += buildBossString(reward, color, world)
    if include_wincons:
        adult_text += buildBridgeReqsString(world)
        adult_text += '\x04'
        adult_text += buildGanonBossKeyString(world)
    else:
        adult_text += getHint('Adult Altar Text End', world.hint_rng, world.clearer_hints).text
    adult_text += '\x0B'
    update_message_by_id(messages, 0x7057, get_raw_text(adult_text), 0x20)


# pulls text string from hintlist for reward after sending the location to hintlist.
def buildBossString(reward, color, world):
    item_icon = chr(world.create_item(reward).special['item_id'])
    if world.multiworld.state.has(reward, world.player):
        if world.clearer_hints:
            text = GossipText(f"\x08\x13{item_icon}One #@ already has#...", [color], prefix='')
        else:
            text = GossipText(f"\x08\x13{item_icon}One in #@'s pocket#...", [color], prefix='')
    else:
        location = world.hinted_dungeon_reward_locations[reward]
        location_text = HintArea.at(location).text(world.hint_rng, world.clearer_hints, preposition=True)
        text = GossipText(f"\x08\x13{item_icon}One {location_text}...", [color], prefix='')
    return str(text) + '\x04'


def buildBridgeReqsString(world):
    string = "\x13\x12" # Light Arrow Icon
    if world.bridge == 'open':
        string += "The awakened ones will have #already created a bridge# to the castle where the evil dwells."
    else:
        item_req_string = getHint('bridge_' + world.bridge, world.hint_rng, world.clearer_hints).text
        if world.bridge == 'medallions':
            item_req_string = str(world.bridge_medallions) + ' ' + item_req_string
        elif world.bridge == 'stones':
            item_req_string = str(world.bridge_stones) + ' ' + item_req_string
        elif world.bridge == 'dungeons':
            item_req_string = str(world.bridge_rewards) + ' ' + item_req_string
        elif world.bridge == 'tokens':
            item_req_string = str(world.bridge_tokens) + ' ' + item_req_string
        elif world.bridge == 'hearts':
            item_req_string = str(world.bridge_hearts) + ' ' + item_req_string
        if '#' not in item_req_string:
            item_req_string = '#%s#' % item_req_string
        string += "The awakened ones will await for the Hero to collect %s." % item_req_string
    return str(GossipText(string, ['Green'], prefix=''))


def buildGanonBossKeyString(world):
    string = "\x13\x74" # Boss Key Icon
    if world.shuffle_ganon_bosskey == 'remove':
        string += "And the door to the \x05\x41evil one\x05\x40's chamber will be left #unlocked#."
    else:
        if world.shuffle_ganon_bosskey == 'on_lacs':
            item_req_string = getHint('lacs_' + world.lacs_condition, world.hint_rng, world.clearer_hints).text
            if world.lacs_condition == 'medallions':
                item_req_string = str(world.lacs_medallions) + ' ' + item_req_string
            elif world.lacs_condition == 'stones':
                item_req_string = str(world.lacs_stones) + ' ' + item_req_string
            elif world.lacs_condition == 'dungeons':
                item_req_string = str(world.lacs_rewards) + ' ' + item_req_string
            elif world.lacs_condition == 'tokens':
                item_req_string = str(world.lacs_tokens) + ' ' + item_req_string
            elif world.lacs_condition == 'hearts':
                item_req_string = str(world.lacs_hearts) + ' ' + item_req_string
            if '#' not in item_req_string:
                item_req_string = '#%s#' % item_req_string
            bk_location_string = "provided by Zelda once %s are retrieved" % item_req_string
        elif world.shuffle_ganon_bosskey in ['stones', 'medallions', 'dungeons', 'tokens', 'hearts']:
            item_req_string = getHint('ganonBK_' + world.shuffle_ganon_bosskey, world.hint_rng, world.clearer_hints).text
            if world.shuffle_ganon_bosskey == 'medallions':
                item_req_string = str(world.ganon_bosskey_medallions) + ' ' + item_req_string
            elif world.shuffle_ganon_bosskey == 'stones':
                item_req_string = str(world.ganon_bosskey_stones) + ' ' + item_req_string
            elif world.shuffle_ganon_bosskey == 'dungeons':
                item_req_string = str(world.ganon_bosskey_rewards) + ' ' + item_req_string
            elif world.shuffle_ganon_bosskey == 'tokens':
                item_req_string = str(world.ganon_bosskey_tokens) + ' ' + item_req_string
            elif world.shuffle_ganon_bosskey == 'hearts':
                item_req_string = str(world.ganon_bosskey_hearts) + ' ' + item_req_string
            if '#' not in item_req_string:
                item_req_string = '#%s#' % item_req_string
            bk_location_string = "automatically granted once %s are retrieved" % item_req_string
        else:
            bk_location_string = getHint('ganonBK_' + world.shuffle_ganon_bosskey, world.hint_rng, world.clearer_hints).text
        string += "And the \x05\x41evil one\x05\x40's key will be %s." % bk_location_string
    return str(GossipText(string, ['Yellow'], prefix=''))


# fun new lines for Ganon during the final battle
def buildGanonText(world, messages):
    # empty now unused messages to make space for ganon lines
    update_message_by_id(messages, 0x70C8, " ")
    update_message_by_id(messages, 0x70C9, " ")
    update_message_by_id(messages, 0x70CA, " ")

    # lines before battle
    ganonLines = getHintGroup('ganonLine', world)
    world.hint_rng.shuffle(ganonLines)
    text = get_raw_text(ganonLines.pop().text)
    update_message_by_id(messages, 0x70CB, text)


# Modified from original. Uses optimized AP methods, no support for custom items. 
def buildMiscItemHints(world, messages):
    for hint_type, data in misc_item_hint_table.items():
        if hint_type in world.misc_hints:
            item_locations = world.multiworld.find_item_locations(data['default_item'], world.player)
            if data['local_only']:
                item_locations = [loc for loc in item_locations if loc.player == world.player]

            if world.multiworld.state.has(data['default_item'], world.player) > 0:
                text = data['default_item_text'].format(area='#your pocket#')
            elif item_locations:
                location = world.hint_rng.choice(item_locations)
                player_text = ''
                if location.player != world.player:
                    player_text = world.multiworld.get_player_name(location.player) + "'s "
                if location.game == 'Ocarina of Time':
                    area = HintArea.at(location, use_alt_hint=data['use_alt_hint']).text(world.hint_rng, world.clearer_hints, world=None)
                else:
                    area = location.name
                text = data['default_item_text'].format(area=rom_safe_text(player_text + area))
            elif 'default_item_fallback' in data:
                text = data['default_item_fallback']
            else:
                text = getHint('Validation Line', world.hint_rng, world.clearer_hints).text
                location = world.get_location('Ganons Tower Boss Key Chest')
                text += f"#{getHint(getItemGenericName(location.item), world.hint_rng, world.clearer_hints).text}#"
            for find, replace in data.get('replace', {}).items():
                text = text.replace(find, replace)

            update_message_by_id(messages, data['id'], str(GossipText(text, ['Green'], prefix='')))


# Modified from original to use optimized AP methods
def buildMiscLocationHints(world, messages):
    for hint_type, data in misc_location_hint_table.items():
        text = data['location_fallback']
        if hint_type in world.misc_hints:
            location = world.get_location(data['item_location'])
            item = location.item
            item_text = getHint(getItemGenericName(item), world.hint_rng, world.clearer_hints).text
            if item.player != world.player:
                item_text += f' for {world.multiworld.get_player_name(item.player)}'
            text = data['location_text'].format(item=rom_safe_text(item_text))

        update_message_by_id(messages, data['id'], str(GossipText(text, ['Green'], prefix='')), 0x23)


def get_raw_text(string):
    text = ''
    for char in string:
        if char == '^':
            text += '\x04' # box break
        elif char == '&':
            text += '\x01' # new line
        elif char == '@':
            text += '\x0F' # print player name
        elif char == '#':
            text += '\x05\x40' # sets color to white
        else:
            text += char
    return text


def HintDistFiles():
    return [os.path.join(data_path('Hints/'), d) for d in defaultHintDists] + [
            os.path.join(data_path('Hints/'), d)
            for d in sorted(os.listdir(data_path('Hints/')))
            if d.endswith('.json') and d not in defaultHintDists]


def HintDistList():
    dists = {}
    for d in HintDistFiles():
        dist = read_json(d)
        dist_name = dist['name']
        gui_name = dist['gui_name']
        dists.update({ dist_name: gui_name })
    return dists


def HintDistTips():
    tips = ""
    first_dist = True
    line_char_limit = 33
    for d in HintDistFiles():
        if not first_dist:
            tips = tips + "\n"
        else:
            first_dist = False
        dist = read_json(d)
        gui_name = dist['gui_name']
        desc = dist['description']
        i = 0
        end_of_line = False
        tips = tips + "<b>"
        for c in gui_name:
            if c == " " and end_of_line:
                tips = tips + "\n"
                end_of_line = False
            else:
                tips = tips + c
                i = i + 1
                if i > line_char_limit:
                    end_of_line = True
                    i = 0
        tips = tips + "</b>: "
        i = i + 2
        for c in desc:
            if c == " " and end_of_line:
                tips = tips + "\n"
                end_of_line = False
            else:
                tips = tips + c
                i = i + 1
                if i > line_char_limit:
                    end_of_line = True
                    i = 0
        tips = tips + "\n"
    return tips
