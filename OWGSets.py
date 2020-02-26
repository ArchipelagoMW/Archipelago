'''
Helper functions to deliver entrance/exit/region sets to OWG rules.
'''

def get_immediately_accessible_entrances(world, player):
    '''
    Entrances that are available with no items at all.

    At this point, these are fake flipper spots.
    '''
    entrances = [
        'Hobo Bridge',
        'Zoras River',
        'Lake Hylia Central Island Pier',
        ]
    return entrances


def get_sword_required_superbunny_mirror_regions():
    '''
    Cave regions that superbunny can get through - but only with a sword.
    '''
    return [
        'Mini Moldorm Cave',
        'Spiral Cave (Top)',
        ]


def get_invalid_mirror_bunny_entrances_dw():
    '''
    Dark World entrances that can't be superbunny-mirrored into.
    '''
    return [
        'Skull Woods Final Section (Entrance)',
        'Hype Cave',
        'Bonk Fairy (Dark)',
        'Thieves Town',
        'Dark World Hammer Peg Cave',
        'Brewery',
        'Hookshot Cave',
        'Hookshot Cave Exit (South)',
        'Dark Lake Hylia Ledge Fairy',
        'Dark Lake Hylia Ledge Spike Cave',
        ]


def get_invalid_mirror_bunny_entrances_lw():
    '''
    Light World entrances that can't be superbunny-mirrored into.

    A couple of these, like Blind's Hideout, are odd cases where the pixel
    leading into the entrance prevents mirror superbunnying - generally due to
    there being stairs there. 
    '''
    return [
        'Bonk Rock Cave',
        'Bonk Fairy (Light)',
        'Blinds Hideout',
        '50 Rupee Cave',
        '20 Rupee Cave',
        'Checkerboard Cave',
        'Light Hype Fairy',
        'Waterfall of Wishing',
        'Light World Bomb Hut',
        'Mini Moldorm Cave',
        'Ice Rod Cave',
        'Hyrule Castle Secret Entrance Stairs',
        'Sanctuary Grave',
        'Kings Grave',
        'Tower of Hera',
        ]


def get_superbunny_accessible_locations():
    '''
    Interior locations that can be accessed with superbunny state.
    '''
    return [
        'Waterfall of Wishing - Left',
        'Waterfall of Wishing - Right',
        'King\'s Tomb', 'Floodgate',
        'Floodgate Chest',
        'Cave 45',
        'Bonk Rock Cave',
        'Brewery',
        'C-Shaped House',
        'Chest Game',
        'Mire Shed - Left',
        'Mire Shed - Right',
        'Secret Passage',
        'Ice Rod Cave',
        'Pyramid Fairy - Left',
        'Pyramid Fairy - Right',
        'Superbunny Cave - Top',
        'Superbunny Cave - Bottom',
        ]


def get_boots_clip_exits_lw(inverted = False):
    '''
    Special Light World region exits that require boots clips.
    '''
    exits = [
        'Bat Cave River Clip Spot',
        'Light World DMA Clip Spot',
        'Hera Ascent',
        'Death Mountain Return Ledge Clip Spot',
        'Death Mountain Glitched Bridge',
        'Zora Descent Clip Spot',
        'Desert Northern Cliffs',
        'Lake Hylia Island Clip Spot',
        'Death Mountain Descent',
        'Graveyard Ledge Clip Spot',
        # Also requires a waterwalk setup, but the point still remains.
        'Waterfall of Wishing',
        ]
    if not inverted:
        exits.append('Spectacle Rock Clip Spot')
        exits.append('Bombos Tablet Clip Spot')
        exits.append('Floating Island Clip Spot')
        exits.append('Cave 45 Clip Spot')
    return exits


def get_boots_clip_exits_dw(inverted = False):
    '''
    Special Dark World region exits that require boots clips.
    '''
    exits = [
        'Dark World DMA Clip Spot',
        'Bumper Cave Ledge Clip Spot',
        'Catfish Descent',
        'Hammer Pegs River Clip Spot',
        'Dark Lake Hylia Ledge Clip Spot',
        'Dark Desert Cliffs Clip Spot',
        'Dark Death Mountain Descent',
        ]
    if not inverted:
        exits.append('Ganons Tower Ascent')
        exits.append('Dark Death Mountain Glitched Bridge')
        exits.append('Turtle Rock (Top) Clip Spot')
    return exits


def get_glitched_speed_drops_dw():
    '''
    Dark World drop-down ledges that require glitched speed.
    '''
    return [
        'Dark Death Mountain Ledge Clip Spot',
        ]


def get_mirror_clip_spots_dw():
    '''
    Mirror shenanigans that are in logic even if the player is a bunny.
    '''
    return [
        'Dark Death Mountain Offset Mirror',
        'Dark Death Mountain Bunny Descent Mirror Spot',
        ]


def get_mirror_clip_spots_lw():
    '''
    Inverted mirror shenanigans in logic even if the player is a bunny.
    '''
    return [
        'Death Mountain Bunny Descent Mirror Spot',
        'Death Mountain Offset Mirror',
        ]


def get_invalid_bunny_revival_dungeons():
    '''
    Dungeon regions that can't be bunny revived from.
    '''
    return [
        'Tower of Hera (Bottom)',
        'Swamp Palace (Entrance)',
        'Turtle Rock (Entrance)',
        ]
