"""
Helper functions to deliver entrance/exit/region sets to OWG rules.
"""

from BaseClasses import Entrance

from .StateHelpers import can_lift_heavy_rocks, can_boots_clip_lw, can_boots_clip_dw, can_get_glitched_speed_dw


def get_sword_required_superbunny_mirror_regions():
    """
    Cave regions that superbunny can get through - but only with a sword.
    """
    yield 'Spiral Cave (Top)'


def get_boots_required_superbunny_mirror_regions():
    """
    Cave regions that superbunny can get through - but only with boots.
    """
    yield 'Two Brothers House'


def get_boots_required_superbunny_mirror_locations():
    """
    Cave locations that superbunny can access - but only with boots.
    """
    yield 'Sahasrahla\'s Hut - Left'
    yield 'Sahasrahla\'s Hut - Middle'
    yield 'Sahasrahla\'s Hut - Right'


def get_invalid_mirror_bunny_entrances():
    """
    Entrances that can't be superbunny-mirrored into.
    """
    yield 'Skull Woods Final Section'
    yield 'Hype Cave'
    yield 'Bonk Fairy (Dark)'
    yield 'Thieves Town'
    yield 'Dark World Hammer Peg Cave'
    yield 'Brewery'
    yield 'Hookshot Cave'
    yield 'Dark Lake Hylia Ledge Fairy'
    yield 'Dark Lake Hylia Ledge Spike Cave'
    yield 'Bonk Rock Cave'
    yield 'Bonk Fairy (Light)'
    yield '50 Rupee Cave'
    yield '20 Rupee Cave'
    yield 'Checkerboard Cave'
    yield 'Light Hype Fairy'
    yield 'Waterfall of Wishing'
    yield 'Light World Bomb Hut'
    yield 'Mini Moldorm Cave'
    yield 'Ice Rod Cave'
    yield 'Sanctuary Grave'
    yield 'Kings Grave'


def get_superbunny_accessible_locations():
    """
    Interior locations that can be accessed with superbunny state.
    """

    yield 'Waterfall of Wishing - Left'
    yield 'Waterfall of Wishing - Right'
    yield 'King\'s Tomb'
    yield 'Floodgate'
    yield 'Floodgate Chest'
    yield 'Cave 45'
    yield 'Bonk Rock Cave'
    yield 'Brewery'
    yield 'C-Shaped House'
    yield 'Chest Game'
    yield 'Mire Shed - Left'
    yield 'Mire Shed - Right'
    yield 'Secret Passage'
    yield 'Ice Rod Cave'
    yield 'Pyramid Fairy - Left'
    yield 'Pyramid Fairy - Right'
    yield 'Superbunny Cave - Top'
    yield 'Superbunny Cave - Bottom'
    yield 'Blind\'s Hideout - Left'
    yield 'Blind\'s Hideout - Right'
    yield 'Blind\'s Hideout - Far Left'
    yield 'Blind\'s Hideout - Far Right'
    yield 'Kakariko Well - Left'
    yield 'Kakariko Well - Middle'
    yield 'Kakariko Well - Right'
    yield 'Kakariko Well - Bottom'
    yield 'Kakariko Tavern'
    yield 'Library'
    yield 'Spiral Cave'
    for location in get_boots_required_superbunny_mirror_locations():
        yield location


def get_non_mandatory_exits(inverted):
    """
    Entrances that can be reached with full equipment using overworld glitches and don't need to be an exit.
    The following are still be mandatory exits:

    Open:
    Turtle Rock Isolated Ledge Entrance
    Skull Woods Second Section Door (West) (or Skull Woods Final Section)

    Inverted:
    Two Brothers House (West)
    Desert Palace Entrance (East)
    """

    yield 'Bumper Cave (Top)'
    yield 'Death Mountain Return Cave (West)'
    yield 'Hookshot Cave Back Entrance'

    if inverted:
        yield 'Desert Palace Entrance (North)'
        yield 'Desert Palace Entrance (West)'
        yield 'Inverted Ganons Tower'
        yield 'Hyrule Castle Entrance (West)'
        yield 'Hyrule Castle Entrance (East)'
    else:
        yield 'Dark Death Mountain Ledge (West)'
        yield 'Dark Death Mountain Ledge (East)'
        yield 'Mimic Cave'
        yield 'Desert Palace Entrance (East)'


def get_boots_clip_exits_lw(inverted = False):
    """
    Special Light World region exits that require boots clips.
    """

    yield ('Bat Cave River Clip Spot', 'Light World', 'Bat Cave Drop Ledge')
    yield ('Light World DMA Clip Spot', 'Light World', 'Death Mountain')
    yield ('Hera Ascent', 'Death Mountain', 'Death Mountain (Top)')
    yield ('Death Mountain Return Ledge Clip Spot', 'Light World', 'Death Mountain Return Ledge')
    yield ('Death Mountain Entrance Clip Spot', 'Light World', 'Death Mountain Entrance')
    yield ('Death Mountain Glitched Bridge', 'Death Mountain', 'East Death Mountain (Top)')
    yield ('Zora Descent Clip Spot', 'East Death Mountain (Top)', 'Zoras River')
    yield ('Desert Northern Cliffs', 'Light World', 'Desert Northern Cliffs')
    yield ('Desert Ledge Dropdown', 'Desert Northern Cliffs', 'Desert Ledge')
    yield ('Desert Palace Entrance Dropdown', 'Desert Northern Cliffs', 'Desert Palace Entrance (North) Spot')
    yield ('Lake Hylia Island Clip Spot', 'Light World', 'Lake Hylia Island')
    yield ('Death Mountain Descent', 'Death Mountain', 'Light World')
    yield ('Kings Grave Clip Spot', 'Death Mountain', 'Kings Grave Area')

    if not inverted:
        yield ('Graveyard Ledge Clip Spot', 'Death Mountain', 'Graveyard Ledge')
        yield ('Desert Ledge (Northeast) Dropdown', 'Desert Northern Cliffs', 'Desert Ledge (Northeast)')
        yield ('Spectacle Rock Clip Spot', 'Death Mountain (Top)', 'Spectacle Rock')
        yield ('Bombos Tablet Clip Spot', 'Light World', 'Bombos Tablet Ledge')
        yield ('Floating Island Clip Spot', 'East Death Mountain (Top)', 'Death Mountain Floating Island (Light World)')
        yield ('Cave 45 Clip Spot', 'Light World', 'Cave 45 Ledge')


def get_boots_clip_exits_dw(inverted, player):
    """
    Special Dark World region exits that require boots clips.
    """

    yield ('Dark World DMA Clip Spot', 'West Dark World', inverted and 'Dark Death Mountain' or 'Dark Death Mountain (West Bottom)')
    yield ('Bumper Cave Ledge Clip Spot', 'West Dark World', 'Bumper Cave Ledge')
    yield ('Bumper Cave Entrance Clip Spot', 'West Dark World', 'Bumper Cave Entrance')
    yield ('Catfish Descent', inverted and 'Dark Death Mountain' or 'Dark Death Mountain (Top)', 'Catfish')
    yield ('Hammer Pegs River Clip Spot', 'East Dark World', 'Hammer Peg Area')
    yield ('Dark Lake Hylia Ledge Clip Spot', 'East Dark World', 'Dark Lake Hylia Ledge')
    yield ('Dark Desert Cliffs Clip Spot', 'South Dark World', 'Dark Desert')
    yield ('DW Floating Island Clip Spot', 'Dark Death Mountain (East Bottom)', 'Death Mountain Floating Island (Dark World)')

    if not inverted:
        yield ('Dark Death Mountain Descent', 'Dark Death Mountain (West Bottom)', 'West Dark World')
        yield ('Ganons Tower Ascent', 'Dark Death Mountain (West Bottom)', 'Dark Death Mountain (Top)')  # This only gets you to the GT entrance
        yield ('Dark Death Mountain Glitched Bridge', 'Dark Death Mountain (West Bottom)', 'Dark Death Mountain (Top)')
        yield ('Turtle Rock (Top) Clip Spot', 'Dark Death Mountain (Top)', 'Turtle Rock (Top)')
        yield ('Ice Palace Clip', 'South Dark World', 'Dark Lake Hylia Central Island', lambda state: can_boots_clip_dw(state, player) and state.has('Flippers', player))
    else:
        yield ('Dark Desert Teleporter Clip Spot', 'Dark Desert', 'Dark Desert Ledge')


def get_glitched_speed_drops_dw(inverted = False):
    """
    Dark World drop-down ledges that require glitched speed.
    """
    yield ('Dark Death Mountain Ledge Clip Spot', inverted and 'Dark Death Mountain' or 'Dark Death Mountain (Top)', 'Dark Death Mountain Ledge')


def get_mirror_clip_spots_dw():
    """
    Out of bounds transitions using the mirror
    """
    yield ('Dark Death Mountain Bunny Descent Mirror Spot', 'Dark Death Mountain (West Bottom)', 'Dark Death Mountain Bunny Descent Area')
    yield ('West Dark World Bunny Descent', 'Dark Death Mountain Bunny Descent Area', 'West Dark World')
    yield ('Dark Death Mountain (East Bottom) Jump', 'Dark Death Mountain Bunny Descent Area', 'Dark Death Mountain (East Bottom)')
    yield ('Desert East Mirror Clip', 'Dark Desert', 'Desert Palace Lone Stairs')


def get_mirror_offset_spots_dw():
    """
    Mirror shenanigans placing a mirror portal with a broken camera
    """
    yield ('Dark Death Mountain Offset Mirror', 'Dark Death Mountain (West Bottom)', 'East Dark World')


def get_mirror_offset_spots_lw(player):
    """
    Mirror shenanigans placing a mirror portal with a broken camera
    """
    yield ('Death Mountain Offset Mirror', 'Death Mountain', 'Light World')
    yield ('Death Mountain Offset Mirror (Houlihan Exit)', 'Death Mountain', 'Hyrule Castle Ledge', lambda state: state.has('Magic Mirror', player) and can_boots_clip_dw(state, player) and state.has('Moon Pearl', player))


def get_invalid_bunny_revival_dungeons():
    """
    Dungeon regions that can't be bunny revived from without superbunny state.
    """
    yield 'Tower of Hera (Bottom)'
    yield 'Swamp Palace (Entrance)'
    yield 'Turtle Rock (Entrance)'
    yield 'Sanctuary'


def overworld_glitch_connections(world, player):
    # Boots-accessible locations.
    create_owg_connections(player, world, get_boots_clip_exits_lw(world.mode[player] == 'inverted'))
    create_owg_connections(player, world, get_boots_clip_exits_dw(world.mode[player] == 'inverted', player))

    # Glitched speed drops.
    create_owg_connections(player, world, get_glitched_speed_drops_dw(world.mode[player] == 'inverted'))

    # Mirror clip spots.
    if world.mode[player] != 'inverted':
        create_owg_connections(player, world, get_mirror_clip_spots_dw())
        create_owg_connections(player, world, get_mirror_offset_spots_dw())
    else:
        create_owg_connections(player, world, get_mirror_offset_spots_lw(player))


def overworld_glitches_rules(world, player):

    # Boots-accessible locations.
    set_owg_connection_rules(player, world, get_boots_clip_exits_lw(world.mode[player] == 'inverted'), lambda state: can_boots_clip_lw(state, player))
    set_owg_connection_rules(player, world, get_boots_clip_exits_dw(world.mode[player] == 'inverted', player), lambda state: can_boots_clip_dw(state, player))

    # Glitched speed drops.
    set_owg_connection_rules(player, world, get_glitched_speed_drops_dw(world.mode[player] == 'inverted'), lambda state: can_get_glitched_speed_dw(state, player))
    # Dark Death Mountain Ledge Clip Spot also accessible with mirror.
    if world.mode[player] != 'inverted':
        add_alternate_rule(world.get_entrance('Dark Death Mountain Ledge Clip Spot', player), lambda state: state.has('Magic Mirror', player))

    # Mirror clip spots.
    if world.mode[player] != 'inverted':
        set_owg_connection_rules(player, world, get_mirror_clip_spots_dw(), lambda state: state.has('Magic Mirror', player))
        set_owg_connection_rules(player, world, get_mirror_offset_spots_dw(), lambda state: state.has('Magic Mirror', player) and can_boots_clip_lw(state, player))
    else:
        set_owg_connection_rules(player, world, get_mirror_offset_spots_lw(player), lambda state: state.has('Magic Mirror', player) and can_boots_clip_dw(state, player))

    # Regions that require the boots and some other stuff.
    if world.mode[player] != 'inverted':
        world.get_entrance('Turtle Rock Teleporter', player).access_rule = lambda state: (can_boots_clip_lw(state, player) or can_lift_heavy_rocks(state, player)) and state.has('Hammer', player)
        add_alternate_rule(world.get_entrance('Waterfall of Wishing', player), lambda state: state.has('Moon Pearl', player) or state.has('Pegasus Boots', player))
    else:
        add_alternate_rule(world.get_entrance('Waterfall of Wishing Cave', player), lambda state: state.has('Moon Pearl', player))

    world.get_entrance('Dark Desert Teleporter', player).access_rule = lambda state: (state.has('Flute', player) or state.has('Pegasus Boots', player)) and can_lift_heavy_rocks(state, player)
    add_alternate_rule(world.get_entrance('Catfish Exit Rock', player), lambda state: can_boots_clip_dw(state, player))
    add_alternate_rule(world.get_entrance('East Dark World Broken Bridge Pass', player), lambda state: can_boots_clip_dw(state, player))

    # Zora's Ledge via waterwalk setup.
    add_alternate_rule(world.get_location('Zora\'s Ledge', player), lambda state: state.has('Pegasus Boots', player))


def add_alternate_rule(entrance, rule):
    old_rule = entrance.access_rule
    entrance.access_rule = lambda state: old_rule(state) or rule(state)


def create_no_logic_connections(player, world, connections):
    for entrance, parent_region, target_region, *rule_override in connections:
        parent = world.get_region(parent_region, player)
        target = world.get_region(target_region, player)
        connection = Entrance(player, entrance, parent)
        parent.exits.append(connection)
        connection.connect(target)


def create_owg_connections(player, world, connections):
    for entrance, parent_region, target_region, *rule_override in connections:
        parent = world.get_region(parent_region, player)
        target = world.get_region(target_region, player)
        connection = Entrance(player, entrance, parent)
        parent.exits.append(connection)
        connection.connect(target)


def set_owg_connection_rules(player, world, connections, default_rule):
    for entrance, _, _, *rule_override in connections:
        connection = world.get_entrance(entrance, player)
        rule = rule_override[0] if len(rule_override) > 0 else default_rule
        connection.access_rule = rule
