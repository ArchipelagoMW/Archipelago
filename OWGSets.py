"""
Helper functions to deliver entrance/exit/region sets to OWG rules.
"""


def get_immediately_accessible_entrances():
    """
    Entrances that are available with no items at all.

    At this point, these are fake flipper spots.
    """
    yield 'Hobo Bridge'
    yield 'Zoras River'
    yield 'Lake Hylia Central Island Pier'


def get_sword_required_superbunny_mirror_regions():
    """
    Cave regions that superbunny can get through - but only with a sword.
    """
    yield 'Mini Moldorm Cave'
    yield 'Spiral Cave (Top)'


def get_invalid_mirror_bunny_entrances_dw():
    """
    Dark World entrances that can't be superbunny-mirrored into.
    """

    yield 'Skull Woods Final Section (Entrance)'
    yield 'Hype Cave'
    yield 'Bonk Fairy (Dark)'
    yield 'Thieves Town'
    yield 'Dark World Hammer Peg Cave'
    yield 'Brewery'
    yield 'Hookshot Cave'
    yield 'Hookshot Cave Exit (South)'
    yield 'Dark Lake Hylia Ledge Fairy'
    yield 'Dark Lake Hylia Ledge Spike Cave'


def get_invalid_mirror_bunny_entrances_lw():
    """
    Light World entrances that can't be superbunny-mirrored into.

    A couple of these, like Blind's Hideout, are odd cases where the pixel
    leading into the entrance prevents mirror superbunnying - generally due to
    there being stairs there. 
    """

    yield 'Bonk Rock Cave'
    yield 'Bonk Fairy (Light)'
    yield 'Blinds Hideout'
    yield '50 Rupee Cave'
    yield '20 Rupee Cave'
    yield 'Checkerboard Cave'
    yield 'Light Hype Fairy'
    yield 'Waterfall of Wishing'
    yield 'Light World Bomb Hut'
    yield 'Mini Moldorm Cave'
    yield 'Ice Rod Cave'
    yield 'Hyrule Castle Secret Entrance Stairs'
    yield 'Sanctuary Grave'
    yield 'Kings Grave'
    yield 'Tower of Hera'


def get_superbunny_accessible_locations():
    """
    Interior locations that can be accessed with superbunny state.
    """

    yield 'Waterfall of Wishing - Left'
    yield 'Waterfall of Wishing - Right'
    yield 'King\'s Tomb', 'Floodgate'
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


def get_boots_clip_exits_lw(inverted = False):
    """
    Special Light World region exits that require boots clips.
    """

    yield 'Bat Cave River Clip Spot'
    yield 'Light World DMA Clip Spot'
    yield 'Hera Ascent'
    yield 'Death Mountain Return Ledge Clip Spot'
    yield 'Death Mountain Glitched Bridge'
    yield 'Zora Descent Clip Spot'
    yield 'Desert Northern Cliffs'
    yield 'Lake Hylia Island Clip Spot'
    yield 'Death Mountain Descent'
    yield 'Graveyard Ledge Clip Spot'
    # Also requires a waterwalk setup, but the point still remains.
    yield 'Waterfall of Wishing'

    if not inverted:
        yield 'Spectacle Rock Clip Spot'
        yield 'Bombos Tablet Clip Spot'
        yield 'Floating Island Clip Spot'
        yield 'Cave 45 Clip Spot'


def get_boots_clip_exits_dw(inverted = False):
    """
    Special Dark World region exits that require boots clips.
    """

    yield 'Dark World DMA Clip Spot'
    yield 'Bumper Cave Ledge Clip Spot'
    yield 'Catfish Descent'
    yield 'Hammer Pegs River Clip Spot'
    yield 'Dark Lake Hylia Ledge Clip Spot'
    yield 'Dark Desert Cliffs Clip Spot'
    yield 'Dark Death Mountain Descent'

    if not inverted:
        yield 'Ganons Tower Ascent'
        yield 'Dark Death Mountain Glitched Bridge'
        yield 'Turtle Rock (Top) Clip Spot'


def get_glitched_speed_drops_dw():
    """
    Dark World drop-down ledges that require glitched speed.
    """
    yield 'Dark Death Mountain Ledge Clip Spot'


def get_mirror_clip_spots_dw():
    """
    Mirror shenanigans that are in logic even if the player is a bunny.
    """
    yield 'Dark Death Mountain Offset Mirror'
    yield 'Dark Death Mountain Bunny Descent Mirror Spot'


def get_mirror_clip_spots_lw():
    """
    Inverted mirror shenanigans in logic even if the player is a bunny.
    """
    yield 'Death Mountain Bunny Descent Mirror Spot'
    yield 'Death Mountain Offset Mirror'


def get_invalid_bunny_revival_dungeons():
    """
    Dungeon regions that can't be bunny revived from.
    """

    yield 'Tower of Hera (Bottom)'
    yield 'Swamp Palace (Entrance)'
    yield 'Turtle Rock (Entrance)'
