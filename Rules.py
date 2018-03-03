import collections
import logging


def set_rules(world):
    global_rules(world)

    if world.mode == 'open':
        open_rules(world)
    elif world.mode == 'standard':
        standard_rules(world)
    elif world.mode == 'swordless':
        swordless_rules(world)
    else:
        raise NotImplementedError('Not implemented yet')

    if world.logic == 'noglitches':
        no_glitches_rules(world)
    elif world.logic == 'minorglitches':
        logging.getLogger('').info('Minor Glitches may be buggy still. No guarantee for proper logic checks.')
    else:
        raise NotImplementedError('Not implemented yet')

    if world.goal == 'dungeons':
        # require all dungeons to beat ganon
        add_rule(world.get_location('Ganon'), lambda state: state.can_reach('Master Sword Pedestal', 'Location') and state.has('Beat Agahnim 1') and state.has('Beat Agahnim 2'))
    elif world.goal == 'ganon':
        # require aga2 to beat ganon
        add_rule(world.get_location('Ganon'), lambda state: state.has('Beat Agahnim 2'))

    set_big_bomb_rules(world)

    # if swamp and dam have not been moved we require mirror for swamp palace
    if not world.swamp_patch_required:
        add_rule(world.get_entrance('Swamp Palace Moat'), lambda state: state.has_Mirror())

    set_bunny_rules(world)


def set_rule(spot, rule):
    spot.access_rule = rule

def set_always_allow(spot, rule):
    spot.always_allow = rule


def add_rule(spot, rule, combine='and'):
    old_rule = spot.access_rule
    if combine == 'or':
        spot.access_rule = lambda state: rule(state) or old_rule(state)
    else:
        spot.access_rule = lambda state: rule(state) and old_rule(state)


def add_lamp_requirement(spot):
    add_rule(spot, lambda state: state.has('Lamp', state.world.lamps_needed_for_dark_rooms))


def forbid_item(location, item):
    old_rule = location.item_rule
    location.item_rule = lambda i: i.name != item and old_rule(i)


def item_in_locations(state, item, locations):
    for location in locations:
        if item_name(state, location) == item:
            return True
    return False

def item_name(state, location):
    location = state.world.get_location(location)
    if location.item is None:
        return None
    return location.item.name


def global_rules(world):
    # ganon can only carry triforce
    world.get_location('Ganon').item_rule = lambda item: item.name == 'Triforce'

    # these are default save&quit points and always accessible
    world.get_region('Links House').can_reach = lambda state: True
    world.get_region('Sanctuary').can_reach = lambda state: True

    # we can s&q to the old man house after we rescue him. This may be somewhere completely different if caves are shuffled!
    old_rule = world.get_region('Old Man House').can_reach
    world.get_region('Old Man House').can_reach = lambda state: state.can_reach('Old Man', 'Location') or old_rule(state)

    # overworld requirements
    set_rule(world.get_entrance('Kings Grave'), lambda state: state.has_Boots())
    set_rule(world.get_entrance('Kings Grave Outer Rocks'), lambda state: state.can_lift_heavy_rocks())
    set_rule(world.get_entrance('Kings Grave Inner Rocks'), lambda state: state.can_lift_heavy_rocks())
    set_rule(world.get_entrance('Kings Grave Mirror Spot'), lambda state: state.has_Pearl() and state.has_Mirror())
    # Caution: If king's grave is releaxed at all to account for reaching it via a two way cave's exit in insanity mode, then the bomb shop logic will need to be updated (that would involve create a small ledge-like Region for it)
    set_rule(world.get_entrance('Bonk Fairy (Light)'), lambda state: state.has_Boots())
    set_rule(world.get_location('Sunken Treasure'), lambda state: state.can_reach('Dam'))
    set_rule(world.get_entrance('Bat Cave Drop Ledge'), lambda state: state.has('Hammer'))
    set_rule(world.get_entrance('Lumberjack Tree Tree'), lambda state: state.has_Boots() and state.has('Beat Agahnim 1'))
    set_rule(world.get_entrance('Bonk Rock Cave'), lambda state: state.has_Boots())
    set_rule(world.get_entrance('Desert Palace Stairs'), lambda state: state.has('Book of Mudora'))
    set_rule(world.get_entrance('Sanctuary Grave'), lambda state: state.can_lift_rocks())
    set_rule(world.get_entrance('20 Rupee Cave'), lambda state: state.can_lift_rocks())
    set_rule(world.get_entrance('50 Rupee Cave'), lambda state: state.can_lift_rocks())
    set_rule(world.get_entrance('Death Mountain Entrance Rock'), lambda state: state.can_lift_rocks())
    set_rule(world.get_entrance('Bumper Cave Entrance Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Flute Spot 1'), lambda state: state.has('Ocarina'))
    set_rule(world.get_entrance('Lake Hylia Central Island Teleporter'), lambda state: state.can_lift_heavy_rocks())
    set_rule(world.get_entrance('Dark Desert Teleporter'), lambda state: state.has('Ocarina') and state.can_lift_heavy_rocks())
    set_rule(world.get_entrance('East Hyrule Teleporter'), lambda state: state.has('Hammer') and state.can_lift_rocks() and state.has_Pearl()) # bunny cannot use hammer
    set_rule(world.get_entrance('South Hyrule Teleporter'), lambda state: state.has('Hammer') and state.can_lift_rocks() and state.has_Pearl()) # bunny cannot use hammer
    set_rule(world.get_entrance('Kakariko Teleporter'), lambda state: ((state.has('Hammer') and state.can_lift_rocks()) or state.can_lift_heavy_rocks()) and state.has_Pearl()) # bunny cannot lift bushes
    set_rule(world.get_location('Flute Spot'), lambda state: state.has('Shovel'))
    set_rule(world.get_location('Purple Chest'), lambda state: state.can_reach('Blacksmith', 'Location'))  # Can S&Q with chest

    set_rule(world.get_location('Zora\'s Ledge'), lambda state: state.has('Flippers'))
    set_rule(world.get_entrance('Waterfall of Wishing'), lambda state: state.has('Flippers'))  # can be fake flippered into, but is in weird state inside that might prevent you from doing things. Can be improved in future Todo
    set_rule(world.get_location('Blacksmith'), lambda state: state.can_lift_heavy_rocks() and state.can_reach('West Dark World'))  # Can S&Q with smith
    set_rule(world.get_location('Magic Bat'), lambda state: state.has('Magic Powder'))
    set_rule(world.get_location('Sick Kid'), lambda state: state.has_bottle())
    set_rule(world.get_location('Library'), lambda state: state.has_Boots())
    set_rule(world.get_location('Potion Shop'), lambda state: state.has('Mushroom'))
    set_rule(world.get_entrance('Desert Palace Entrance (North) Rocks'), lambda state: state.can_lift_rocks())
    set_rule(world.get_entrance('Desert Ledge Return Rocks'), lambda state: state.can_lift_rocks())  # should we decide to place something that is not a dungeon end up there at some point
    set_rule(world.get_entrance('Checkerboard Cave'), lambda state: state.can_lift_rocks())
    set_rule(world.get_location('Master Sword Pedestal'), lambda state: state.has('Red Pendant') and state.has('Blue Pendant') and state.has('Green Pendant'))
    set_rule(world.get_location('Sahasrahla'), lambda state: state.has('Green Pendant'))
    set_rule(world.get_entrance('Agahnims Tower'), lambda state: state.has('Cape') or state.has_beam_sword() or state.has('Beat Agahnim 1'))  # barrier gets removed after killing agahnim, relevant for entrance shuffle
    set_rule(world.get_entrance('Agahnim 1'), lambda state: state.has_sword() and state.has('Small Key (Agahnims Tower)', 2))
    set_rule(world.get_location('Castle Tower - Dark Maze'), lambda state: state.has('Small Key (Agahnims Tower)'))
    set_rule(world.get_entrance('Top of Pyramid'), lambda state: state.has('Beat Agahnim 1'))
    set_rule(world.get_entrance('Old Man Cave Exit (West)'), lambda state: False)  # drop cannot be climbed up
    set_rule(world.get_entrance('Broken Bridge (West)'), lambda state: state.has('Hookshot'))
    set_rule(world.get_entrance('Broken Bridge (East)'), lambda state: state.has('Hookshot'))
    set_rule(world.get_entrance('East Death Mountain Teleporter'), lambda state: state.can_lift_heavy_rocks())
    set_rule(world.get_entrance('Fairy Ascension Rocks'), lambda state: state.can_lift_heavy_rocks())
    set_rule(world.get_entrance('Paradox Cave Push Block Reverse'), lambda state: state.has('Mirror'))  # can erase block
    set_rule(world.get_entrance('Death Mountain (Top)'), lambda state: state.has('Hammer'))
    set_rule(world.get_entrance('Turtle Rock Teleporter'), lambda state: state.can_lift_heavy_rocks() and state.has('Hammer'))
    set_rule(world.get_location('Ether Tablet'), lambda state: state.has('Book of Mudora') and state.has_beam_sword())
    set_rule(world.get_entrance('East Death Mountain (Top)'), lambda state: state.has('Hammer'))

    set_rule(world.get_location('Catfish'), lambda state: state.can_lift_rocks())
    set_rule(world.get_entrance('Northeast Dark World Broken Bridge Pass'), lambda state: state.has_Pearl() and (state.can_lift_rocks() or state.has('Hammer') or state.has('Flippers')))
    set_rule(world.get_entrance('East Dark World Broken Bridge Pass'), lambda state: state.has_Pearl() and (state.can_lift_rocks() or state.has('Hammer')))
    set_rule(world.get_entrance('South Dark World Bridge'), lambda state: state.has('Hammer') and state.has_Pearl())
    set_rule(world.get_entrance('Bonk Fairy (Dark)'), lambda state: state.has_Pearl() and state.has_Boots())
    set_rule(world.get_entrance('West Dark World Gap'), lambda state: state.has_Pearl() and state.has('Hookshot'))
    set_rule(world.get_entrance('Palace of Darkness'), lambda state: state.has_Pearl()) # kiki needs pearl
    set_rule(world.get_entrance('Hyrule Castle Ledge Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Hyrule Castle Main Gate'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Dark Lake Hylia Drop (East)'), lambda state: (state.has_Pearl() and state.has('Flippers') or state.has_Mirror()))  # Overworld Bunny Revival
    set_rule(world.get_location('Bombos Tablet'), lambda state: state.has('Book of Mudora') and state.has_beam_sword() and state.has_Mirror())
    set_rule(world.get_entrance('Dark Lake Hylia Drop (South)'), lambda state: state.has_Pearl() and state.has('Flippers'))  # ToDo any fake flipper set up?
    set_rule(world.get_entrance('Dark Lake Hylia Ledge Fairy'), lambda state: state.has_Pearl()) # bomb required
    set_rule(world.get_entrance('Dark Lake Hylia Ledge Spike Cave'), lambda state: state.can_lift_rocks() and state.has_Pearl())
    set_rule(world.get_entrance('Dark Lake Hylia Teleporter'), lambda state: state.has_Pearl() and (state.has('Hammer') or state.can_lift_rocks()))  # Fake Flippers
    set_rule(world.get_entrance('Village of Outcasts Heavy Rock'), lambda state: state.has_Pearl() and state.can_lift_heavy_rocks())
    set_rule(world.get_entrance('Hype Cave'), lambda state: state.has_Pearl()) # bomb required
    set_rule(world.get_entrance('Brewery'), lambda state: state.has_Pearl()) # bomb required
    set_rule(world.get_entrance('Thieves Town'), lambda state: state.has_Pearl()) # bunny cannot pull
    set_rule(world.get_entrance('Skull Woods First Section Hole (North)'), lambda state: state.has_Pearl()) # bunny cannot lift bush
    set_rule(world.get_entrance('Skull Woods Second Section Hole'), lambda state: state.has_Pearl()) # bunny cannot lift bush
    set_rule(world.get_entrance('Maze Race Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Cave 45 Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('East Dark World Bridge'), lambda state: state.has_Pearl() and state.has('Hammer'))
    set_rule(world.get_entrance('Lake Hylia Island Mirror Spot'), lambda state: state.has_Pearl() and state.has_Mirror() and state.has('Flippers'))
    set_rule(world.get_entrance('Lake Hylia Central Island Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('East Dark World River Pier'), lambda state: state.has_Pearl() and state.has('Flippers'))  # ToDo any fake flipper set up?
    set_rule(world.get_entrance('Graveyard Ledge Mirror Spot'), lambda state: state.has_Pearl() and state.has_Mirror())
    set_rule(world.get_entrance('Bumper Cave Entrance Rock'), lambda state: state.has_Pearl() and state.can_lift_rocks())
    set_rule(world.get_entrance('Bumper Cave Ledge Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Bat Cave Drop Ledge Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Dark World Hammer Peg Cave'), lambda state: state.has_Pearl() and state.has('Hammer'))
    set_rule(world.get_entrance('Village of Outcasts Eastern Rocks'), lambda state: state.has_Pearl() and state.can_lift_heavy_rocks())
    set_rule(world.get_entrance('Peg Area Rocks'), lambda state: state.has_Pearl() and state.can_lift_heavy_rocks())
    set_rule(world.get_entrance('Village of Outcasts Pegs'), lambda state: state.has_Pearl() and state.has('Hammer'))
    set_rule(world.get_entrance('Grassy Lawn Pegs'), lambda state: state.has_Pearl() and state.has('Hammer'))
    set_rule(world.get_entrance('Bumper Cave Exit (Top)'), lambda state: state.has('Cape'))
    set_rule(world.get_entrance('Bumper Cave Exit (Bottom)'), lambda state: state.has('Cape') or state.has('Hookshot'))

    set_rule(world.get_entrance('Skull Woods Final Section'), lambda state: state.has('Fire Rod') and state.has_Pearl()) # bunny cannot use fire rod
    set_rule(world.get_entrance('Misery Mire'), lambda state: state.has_Pearl() and state.has_sword() and state.has_misery_mire_medallion())  # sword required to cast magic (!)
    set_rule(world.get_entrance('Desert Ledge (Northeast) Mirror Spot'), lambda state: state.has_Mirror())

    set_rule(world.get_entrance('Desert Ledge Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Desert Palace Stairs Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Desert Palace Entrance (North) Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Spectacle Rock Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Ganons Tower'), lambda state: state.has('Crystal 1') and state.has('Crystal 2') and state.has('Crystal 3') and state.has('Crystal 4') and state.has('Crystal 5') and state.has('Crystal 6') and state.has('Crystal 7'))
    set_rule(world.get_entrance('Hookshot Cave'), lambda state: state.can_lift_rocks() and state.has_Pearl())

    set_rule(world.get_entrance('East Death Mountain (Top) Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Mimic Cave Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Spiral Cave Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Fairy Ascension Mirror Spot'), lambda state: state.has_Mirror() and state.has_Pearl())  # need to lift flowers
    set_rule(world.get_entrance('Isolated Ledge Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Superbunny Cave Exit (Bottom)'), lambda state: False)  # Cannot get to bottom exit from top. Just exists for shuffling

    set_rule(world.get_location('Spike Cave'), lambda state:
             state.has('Hammer') and state.can_lift_rocks() and
             ((state.has('Cape') and state.can_extend_magic(16, True)) or
                 (state.has('Cane of Byrna') and
                     (state.can_extend_magic(12, True) or
                     (state.world.can_take_damage and (state.has_Boots() or state.has_hearts(4))))))
            )

    set_rule(world.get_location('Hookshot Cave - Top Right'), lambda state: state.has('Hookshot'))
    set_rule(world.get_location('Hookshot Cave - Top Left'), lambda state: state.has('Hookshot'))
    set_rule(world.get_location('Hookshot Cave - Bottom Right'), lambda state: state.has('Hookshot') or state.has('Pegasus Boots'))
    set_rule(world.get_location('Hookshot Cave - Bottom Left'), lambda state: state.has('Hookshot'))
    set_rule(world.get_entrance('Floating Island Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Turtle Rock'), lambda state: state.has_Pearl() and state.has_sword() and state.has_turtle_rock_medallion() and state.can_reach('Turtle Rock (Top)', 'Region'))  # sword required to cast magic (!)
    set_rule(world.get_location('Mimic Cave'), lambda state: state.has('Hammer'))

    set_rule(world.get_entrance('Sewers Door'), lambda state: state.has('Small Key (Escape)'))
    set_rule(world.get_entrance('Sewers Back Door'), lambda state: state.has('Small Key (Escape)'))

    set_rule(world.get_location('Eastern Palace - Big Chest'), lambda state: state.has('Big Key (Eastern Palace)'))
    set_rule(world.get_location('Eastern Palace - Armos Knights'), lambda state: state.has('Bow') and state.has('Big Key (Eastern Palace)'))
    set_rule(world.get_location('Eastern Palace - Prize'), lambda state: state.has('Bow') and state.has('Big Key (Eastern Palace)'))
    for location in ['Eastern Palace - Armos Knights', 'Eastern Palace - Big Chest']:
        forbid_item(world.get_location(location), 'Big Key (Eastern Palace)')

    set_rule(world.get_location('Desert Palace - Big Chest'), lambda state: state.has('Big Key (Desert Palace)'))
    set_rule(world.get_location('Desert Palace - Torch'), lambda state: state.has_Boots())
    set_rule(world.get_entrance('Desert Palace East Wing'), lambda state: state.has('Small Key (Desert Palace)'))
    set_rule(world.get_location('Desert Palace - Prize'), lambda state: state.has('Small Key (Desert Palace)') and state.has('Big Key (Desert Palace)') and state.has_fire_source() and
                                                                     (state.has_blunt_weapon() or state.has('Fire Rod') or state.has('Ice Rod') or state.has('Bow')))
    set_rule(world.get_location('Desert Palace - Lanmolas'), lambda state: state.has('Small Key (Desert Palace)') and state.has('Big Key (Desert Palace)') and state.has_fire_source() and
                                                                     (state.has_blunt_weapon() or state.has('Fire Rod') or state.has('Ice Rod') or state.has('Bow')))
    for location in ['Desert Palace - Lanmolas', 'Desert Palace - Big Chest']:
        forbid_item(world.get_location(location), 'Big Key (Desert Palace)')

    for location in ['Desert Palace - Lanmolas', 'Desert Palace - Big Key Chest', 'Desert Palace - Compass Chest']:
        forbid_item(world.get_location(location), 'Small Key (Desert Palace)')

    set_rule(world.get_entrance('Tower of Hera Small Key Door'), lambda state: state.has('Small Key (Tower of Hera)') or item_name(state, 'Tower of Hera - Big Key Chest') == 'Small Key (Tower of Hera)')
    set_rule(world.get_entrance('Tower of Hera Big Key Door'), lambda state: state.has('Big Key (Tower of Hera)'))
    set_rule(world.get_location('Tower of Hera - Big Chest'), lambda state: state.has('Big Key (Tower of Hera)'))
    set_rule(world.get_location('Tower of Hera - Big Key Chest'), lambda state: state.has_fire_source())
    set_always_allow(world.get_location('Tower of Hera - Big Key Chest'), lambda state, item: item.name == 'Small Key (Tower of Hera)')
    set_rule(world.get_location('Tower of Hera - Moldorm'), lambda state: state.has_blunt_weapon())
    set_rule(world.get_location('Tower of Hera - Prize'), lambda state: state.has_blunt_weapon())
    for location in ['Tower of Hera - Moldorm', 'Tower of Hera - Big Chest', 'Tower of Hera - Compass Chest']:
        forbid_item(world.get_location(location), 'Big Key (Tower of Hera)')
    for location in ['Tower of Hera - Big Key Chest']:
        forbid_item(world.get_location(location), 'Small Key (Tower of Hera)')

    set_rule(world.get_entrance('Swamp Palace Moat'), lambda state: state.has('Flippers') and state.can_reach('Dam'))
    set_rule(world.get_entrance('Swamp Palace Small Key Door'), lambda state: state.has('Small Key (Swamp Palace)'))
    set_rule(world.get_entrance('Swamp Palace (Center)'), lambda state: state.has('Hammer'))
    set_rule(world.get_location('Swamp Palace - Big Chest'), lambda state: state.has('Big Key (Swamp Palace)') or item_name(state, 'Swamp Palace - Big Chest') == 'Big Key (Swamp Palace)')
    set_always_allow(world.get_location('Swamp Palace - Big Chest'), lambda state, item: item.name == 'Big Key (Swamp Palace)')
    set_rule(world.get_entrance('Swamp Palace (North)'), lambda state: state.has('Hookshot'))
    set_rule(world.get_location('Swamp Palace - Arrghus'), lambda state: state.has_blunt_weapon())
    set_rule(world.get_location('Swamp Palace - Prize'), lambda state: state.has_blunt_weapon())
    for location in ['Swamp Palace - Entrance']:
        forbid_item(world.get_location(location), 'Big Key (Swamp Palace)')

    set_rule(world.get_entrance('Thieves Town Big Key Door'), lambda state: state.has('Big Key (Thieves Town)'))
    set_rule(world.get_entrance('Blind Fight'), lambda state: state.has('Small Key (Thieves Town)') and (state.has_blunt_weapon() or state.has('Cane of Somaria') or state.has('Cane of Byrna')))
    set_rule(world.get_location('Thieves\' Town - Big Chest'), lambda state: (state.has('Small Key (Thieves Town)') or item_name(state, 'Thieves\' Town - Big Chest') == 'Small Key (Thieves Town)') and state.has('Hammer'))
    set_always_allow(world.get_location('Thieves\' Town - Big Chest'), lambda state, item: item.name == 'Small Key (Thieves Town)' and state.has('Hammer'))
    set_rule(world.get_location('Thieves\' Town - Attic'), lambda state: state.has('Small Key (Thieves Town)'))
    for location in ['Thieves\' Town - Attic', 'Thieves\' Town - Big Chest', 'Thieves\' Town - Blind\'s Cell', 'Thieves Town - Blind']:
        forbid_item(world.get_location(location), 'Big Key (Thieves Town)')
    for location in ['Thieves\' Town - Attic', 'Thieves Town - Blind']:
        forbid_item(world.get_location(location), 'Small Key (Thieves Town)')

    set_rule(world.get_entrance('Skull Woods First Section South Door'), lambda state: state.has('Small Key (Skull Woods)'))
    set_rule(world.get_entrance('Skull Woods First Section (Right) North Door'), lambda state: state.has('Small Key (Skull Woods)'))
    set_rule(world.get_entrance('Skull Woods First Section West Door'), lambda state: state.has('Small Key (Skull Woods)', 2))  # ideally would only be one key, but we may have spent thst key already on escaping the right section
    set_rule(world.get_entrance('Skull Woods First Section (Left) Door to Exit'), lambda state: state.has('Small Key (Skull Woods)', 2))
    set_rule(world.get_location('Skull Woods - Big Chest'), lambda state: state.has('Big Key (Skull Woods)') or item_name(state, 'Skull Woods - Big Chest') == 'Big Key (Skull Woods)')
    set_always_allow(world.get_location('Skull Woods - Big Chest'), lambda state, item: item.name == 'Big Key (Skull Woods)')
    set_rule(world.get_entrance('Skull Woods Torch Room'), lambda state: state.has('Small Key (Skull Woods)', 3) and state.has('Fire Rod') and state.has_sword())  # sword required for curtain
    for location in ['Skull Woods - Mothula']:
        forbid_item(world.get_location(location), 'Small Key (Skull Woods)')

    set_rule(world.get_entrance('Ice Palace Entrance Room'), lambda state: state.has('Fire Rod') or (state.has('Bombos') and state.has_sword()))
    set_rule(world.get_location('Ice Palace - Big Chest'), lambda state: state.has('Big Key (Ice Palace)'))
    set_rule(world.get_entrance('Ice Palace (Kholdstare)'), lambda state: state.can_lift_rocks() and state.has('Hammer') and state.has('Big Key (Ice Palace)') and (state.has('Small Key (Ice Palace)', 2) or (state.has('Cane of Somaria') and state.has('Small Key (Ice Palace)', 1))))
    set_rule(world.get_entrance('Ice Palace (East)'), lambda state: (state.has('Hookshot') or (item_in_locations(state, 'Big Key (Ice Palace)', ['Ice Palace - Spike Room', 'Ice Palace - Big Key Chest', 'Ice Palace - Map Chest']) and state.has('Small Key (Ice Palace)'))) and (state.world.can_take_damage or state.has('Hookshot') or state.has('Cape') or state.has('Cane of Byrna')))
    set_rule(world.get_entrance('Ice Palace (East Top)'), lambda state: state.can_lift_rocks() and state.has('Hammer'))
    for location in ['Ice Palace - Big Chest', 'Ice Palace - Kholdstare']:
        forbid_item(world.get_location(location), 'Big Key (Ice Palace)')

    set_rule(world.get_entrance('Misery Mire Entrance Gap'), lambda state: (state.has_Boots() or state.has('Hookshot')) and (state.has_sword() or state.has('Fire Rod') or state.has('Ice Rod') or state.has('Hammer') or state.has('Cane of Somaria') or state.has('Bow')))  # need to defeat wizzrobes, bombs don't work ...
    set_rule(world.get_location('Misery Mire - Big Chest'), lambda state: state.has('Big Key (Misery Mire)'))
    set_rule(world.get_location('Misery Mire - Spike Chest'), lambda state: (state.world.can_take_damage and state.has_hearts(4)) or state.has('Cane of Byrna') or state.has('Cape'))
    set_rule(world.get_entrance('Misery Mire Big Key Door'), lambda state: state.has('Big Key (Misery Mire)'))
    # you can squander the free small key from the pot by opening the south door to the north west switch room, locking you out of accessing a color switch ...
    # big key gives backdoor access to that from the teleporter in the north west
    set_rule(world.get_location('Misery Mire - Map Chest'), lambda state: state.has('Small Key (Misery Mire)', 1) or state.has('Big Key (Misery Mire)'))
    # in addition, you can open the door to the map room before getting access to a color switch, so this is locked behing 2 small keys or the big key...
    set_rule(world.get_location('Misery Mire - Main Lobby'), lambda state: state.has('Small Key (Misery Mire)', 2) or state.has('Big Key (Misery Mire)'))
    # we can place a small key in the West wing iff it also contains/blocks the Big Key, as we cannot reach and softlock with the basement key door yet
    set_rule(world.get_entrance('Misery Mire (West)'), lambda state: state.has('Small Key (Misery Mire)', 2) if ((item_name(state, 'Misery Mire - Compass Chest') in ['Big Key (Misery Mire)']) or
                                                                                                                 (item_name(state, 'Misery Mire - Big Key Chest') in ['Big Key (Misery Mire)'])) else state.has('Small Key (Misery Mire)', 3))
    set_rule(world.get_location('Misery Mire - Compass Chest'), lambda state: state.has_fire_source())
    set_rule(world.get_location('Misery Mire - Big Key Chest'), lambda state: state.has_fire_source())
    set_rule(world.get_entrance('Misery Mire (Vitreous)'), lambda state: state.has('Cane of Somaria') and (state.has('Bow') or state.has_blunt_weapon()))
    for location in ['Misery Mire - Big Chest', 'Misery Mire - Vitreous']:
        forbid_item(world.get_location(location), 'Big Key (Misery Mire)')

    set_rule(world.get_entrance('Turtle Rock Entrance Gap'), lambda state: state.has('Cane of Somaria'))
    set_rule(world.get_entrance('Turtle Rock Entrance Gap Reverse'), lambda state: state.has('Cane of Somaria'))
    set_rule(world.get_location('Turtle Rock - Compass Chest'), lambda state: state.has('Cane of Somaria'))  # We could get here from the middle section without Cane as we don't cross the entrance gap!
    set_rule(world.get_location('Turtle Rock - Roller Room - Left'), lambda state: state.has('Cane of Somaria') and state.has('Fire Rod'))
    set_rule(world.get_location('Turtle Rock - Roller Room - Right'), lambda state: state.has('Cane of Somaria') and state.has('Fire Rod'))
    set_rule(world.get_location('Turtle Rock - Big Chest'), lambda state: state.has('Big Key (Turtle Rock)') and (state.has('Cane of Somaria') or state.has('Hookshot')))
    set_rule(world.get_entrance('Turtle Rock (Big Chest) (North)'), lambda state: state.has('Cane of Somaria') or state.has('Hookshot'))
    set_rule(world.get_entrance('Turtle Rock Big Key Door'), lambda state: state.has('Big Key (Turtle Rock)'))
    set_rule(world.get_entrance('Turtle Rock Dark Room Staircase'), lambda state: state.has('Small Key (Turtle Rock)', 3))
    set_rule(world.get_entrance('Turtle Rock (Dark Room) (North)'), lambda state: state.has('Cane of Somaria'))
    set_rule(world.get_entrance('Turtle Rock (Dark Room) (South)'), lambda state: state.has('Cane of Somaria'))
    set_rule(world.get_location('Turtle Rock - Eye Bridge - Bottom Left'), lambda state: state.has('Cane of Byrna') or state.has('Cape') or state.has('Mirror Shield'))
    set_rule(world.get_location('Turtle Rock - Eye Bridge - Bottom Right'), lambda state: state.has('Cane of Byrna') or state.has('Cape') or state.has('Mirror Shield'))
    set_rule(world.get_location('Turtle Rock - Eye Bridge - Top Left'), lambda state: state.has('Cane of Byrna') or state.has('Cape') or state.has('Mirror Shield'))
    set_rule(world.get_location('Turtle Rock - Eye Bridge - Top Right'), lambda state: state.has('Cane of Byrna') or state.has('Cape') or state.has('Mirror Shield'))
    set_rule(world.get_entrance('Turtle Rock (Trinexx)'), lambda state: state.has('Small Key (Turtle Rock)', 4) and state.has('Big Key (Turtle Rock)') and state.has('Cane of Somaria') and state.has('Fire Rod') and state.has('Ice Rod') and
             (state.has('Hammer') or state.has_beam_sword() or (state.has_sword() and state.can_extend_magic(32))))

    set_trock_key_rules(world)

    set_rule(world.get_entrance('Palace of Darkness Bonk Wall'), lambda state: state.has('Bow'))
    set_rule(world.get_entrance('Palace of Darkness Hammer Peg Drop'), lambda state: state.has('Hammer'))
    set_rule(world.get_entrance('Palace of Darkness Bridge Room'), lambda state: state.has('Small Key (Palace of Darkness)', 1))  # If we can reach any other small key door, we already have back door access to this area
    set_rule(world.get_entrance('Palace of Darkness Big Key Door'), lambda state: state.has('Small Key (Palace of Darkness)', 6) and state.has('Big Key (Palace of Darkness)') and state.has('Bow') and state.has('Hammer'))
    set_rule(world.get_entrance('Palace of Darkness (North)'), lambda state: state.has('Small Key (Palace of Darkness)', 4))
    set_rule(world.get_location('Palace of Darkness - Big Chest'), lambda state: state.has('Big Key (Palace of Darkness)'))

    set_rule(world.get_entrance('Palace of Darkness Big Key Chest Staircase'), lambda state: state.has('Small Key (Palace of Darkness)', 6)  or (item_name(state, 'Palace of Darkness - Big Key Chest') in ['Small Key (Palace of Darkness)'] and state.has('Small Key (Palace of Darkness)', 3)))
    set_always_allow(world.get_location('Palace of Darkness - Big Key Chest'), lambda state, item: item.name == 'Small Key (Palace of Darkness)' and state.has('Small Key (Palace of Darkness)', 5))

    set_rule(world.get_entrance('Palace of Darkness Spike Statue Room Door'), lambda state: state.has('Small Key (Palace of Darkness)', 6) or (item_name(state, 'Palace of Darkness - Harmless Hellway') in ['Small Key (Palace of Darkness)'] and state.has('Small Key (Palace of Darkness)', 4)))
    set_always_allow(world.get_location('Palace of Darkness - Harmless Hellway'), lambda state, item: item.name == 'Small Key (Palace of Darkness)' and state.has('Small Key (Palace of Darkness)', 5))
    set_rule(world.get_entrance('Palace of Darkness Maze Door'), lambda state: state.has('Small Key (Palace of Darkness)', 6))

    # these key rules are conservative, you might be able to get away with more lenient rules
    randomizer_room_chests = ['Ganons Tower - Randomizer Room - Top Left', 'Ganons Tower - Randomizer Room - Top Right', 'Ganons Tower - Randomizer Room - Bottom Left', 'Ganons Tower - Randomizer Room - Bottom Right']
    compass_room_chests = ['Ganons Tower - Compass Room - Top Left', 'Ganons Tower - Compass Room - Top Right', 'Ganons Tower - Compass Room - Bottom Left', 'Ganons Tower - Compass Room - Bottom Right']

    set_rule(world.get_location('Ganons Tower - Bob\'s Torch'), lambda state: state.has_Boots())
    set_rule(world.get_entrance('Ganons Tower (Tile Room)'), lambda state: state.has('Cane of Somaria'))
    set_rule(world.get_entrance('Ganons Tower (Hookshot Room)'), lambda state: state.has('Hammer'))

    set_rule(world.get_entrance('Ganons Tower (Map Room)'), lambda state: state.has('Small Key (Ganons Tower)', 4) or (item_name(state, 'Ganons Tower - Map Chest') in ['Big Key (Ganons Tower)', 'Small Key (Ganons Tower)'] and state.has('Small Key (Ganons Tower)', 3)))
    set_always_allow(world.get_location('Ganons Tower - Map Chest'), lambda state, item: item.name == 'Small Key (Ganons Tower)' and state.has('Small Key (Ganons Tower)', 3))

    # It is possible to need more than 2 keys to get through this entance if you spend keys elsewhere. We reflect this in the chest requirements.
    # However we need to leave these at the lower values to derive that with 3 keys it is always possible to reach Bob and Ice Armos.
    set_rule(world.get_entrance('Ganons Tower (Double Switch Room)'), lambda state: state.has('Small Key (Ganons Tower)', 2))
    # It is possible to need more than 3 keys ....
    set_rule(world.get_entrance('Ganons Tower (Firesnake Room)'), lambda state: state.has('Small Key (Ganons Tower)', 3))

    #The actual requirements for these rooms to avoid key-lock
    set_rule(world.get_location('Ganons Tower - Firesnake Room'), lambda state: state.has('Small Key (Ganons Tower)', 3) or (item_in_locations(state, 'Big Key (Ganons Tower)', randomizer_room_chests) and state.has('Small Key (Ganons Tower)', 2)))
    for location in randomizer_room_chests:
        set_rule(world.get_location(location), lambda state: state.has('Small Key (Ganons Tower)', 4) or (item_in_locations(state, 'Big Key (Ganons Tower)', randomizer_room_chests) and state.has('Small Key (Ganons Tower)', 3)))

    # Once again it is possible to need more than 3 keys...
    set_rule(world.get_entrance('Ganons Tower (Tile Room) Key Door'), lambda state: state.has('Small Key (Ganons Tower)', 3) and state.has('Fire Rod'))
    # Actual requirements
    for location in compass_room_chests:
        set_rule(world.get_location(location), lambda state: state.has('Fire Rod') and (state.has('Small Key (Ganons Tower)', 4) or (item_in_locations(state, 'Big Key (Ganons Tower)', compass_room_chests) and state.has('Small Key (Ganons Tower)', 3))))

    set_rule(world.get_location('Ganons Tower - Big Chest'), lambda state: state.has('Big Key (Ganons Tower)'))
    set_rule(world.get_location('Ganons Tower - Big Key Room - Left'), lambda state: state.has('Bow') or state.has_blunt_weapon())
    set_rule(world.get_location('Ganons Tower - Big Key Chest'), lambda state: state.has('Bow') or state.has_blunt_weapon())
    set_rule(world.get_location('Ganons Tower - Big Key Room - Right'), lambda state: state.has('Bow') or state.has_blunt_weapon())
    set_rule(world.get_entrance('Ganons Tower Big Key Door'), lambda state: state.has('Big Key (Ganons Tower)') and state.has('Bow'))
    set_rule(world.get_entrance('Ganons Tower Torch Rooms'), lambda state: state.has_fire_source())
    set_rule(world.get_location('Ganons Tower - Pre-Moldorm Chest'), lambda state: state.has('Small Key (Ganons Tower)', 3))
    set_rule(world.get_entrance('Ganons Tower Moldorm Door'), lambda state: state.has('Small Key (Ganons Tower)', 4))
    set_rule(world.get_entrance('Ganons Tower Moldorm Gap'), lambda state: state.has('Hookshot') and state.has_blunt_weapon())
    set_rule(world.get_location('Agahnim 2'), lambda state: state.has_sword() or state.has('Hammer') or state.has('Bug Catching Net'))
    set_rule(world.get_entrance('Pyramid Hole'), lambda state: state.has('Beat Agahnim 2'))
    for location in ['Ganons Tower - Big Chest', 'Ganons Tower - Mini Helmasaur Room - Left', 'Ganons Tower - Mini Helmasaur Room - Right',
                     'Ganons Tower - Pre-Moldorm Chest', 'Ganons Tower - Validation Chest']:
        forbid_item(world.get_location(location), 'Big Key (Ganons Tower)')

    set_rule(world.get_location('Ganon'), lambda state: state.has_beam_sword() and state.has_fire_source() and state.has('Crystal 1') and state.has('Crystal 2')
                                                        and state.has('Crystal 3') and state.has('Crystal 4') and state.has('Crystal 5') and state.has('Crystal 6') and state.has('Crystal 7')
                                                        and (state.has('Tempered Sword') or state.has('Golden Sword') or (state.has('Silver Arrows') and state.has('Bow')) or state.has('Lamp') or state.can_extend_magic(12)))  # need to light torch a sufficient amount of times
    set_rule(world.get_entrance('Ganon Drop'), lambda state: state.has_beam_sword())  # need to damage ganon to get tiles to drop


def no_glitches_rules(world):
    set_rule(world.get_entrance('Zoras River'), lambda state: state.has('Flippers') or state.can_lift_rocks())
    set_rule(world.get_entrance('Lake Hylia Central Island Pier'), lambda state: state.has('Flippers'))  # can be fake flippered to
    set_rule(world.get_entrance('Hobo Bridge'), lambda state: state.has('Flippers'))
    set_rule(world.get_entrance('Dark Lake Hylia Drop (East)'), lambda state: state.has_Pearl() and state.has('Flippers'))
    set_rule(world.get_entrance('Dark Lake Hylia Teleporter'), lambda state: state.has_Pearl() and state.has('Flippers') and (state.has('Hammer') or state.can_lift_rocks()))
    set_rule(world.get_entrance('Dark Lake Hylia Ledge Drop'), lambda state: state.has_Pearl() and state.has('Flippers'))
    add_rule(world.get_entrance('Ganons Tower (Hookshot Room)'), lambda state: state.has('Hookshot'))
    set_rule(world.get_entrance('Paradox Cave Push Block Reverse'), lambda state: False)  # no glitches does not require block override
    set_rule(world.get_entrance('Paradox Cave Bomb Jump'), lambda state: False)
    set_rule(world.get_entrance('Skull Woods First Section Bomb Jump'), lambda state: False)

    # Light cones in standard depend on which world we actually are in, not which one the location would normally be
    # We add Lamp requirements only to those locations which lie in the dark world (or everything if open
    DW_Entrances = ['Bumper Cave (Bottom)', 'Superbunny Cave (Top)', 'Superbunny Cave (Bottom)', 'Hookshot Cave', 'Bumper Cave (Top)', 'Hookshot Cave Back Entrance', 'Dark Death Mountain Ledge (East)',
                    'Turtle Rock Isolated Ledge Entrance', 'Thieves Town', 'Skull Woods Final Section', 'Ice Palace', 'Misery Mire', 'Palace of Darkness', 'Swamp Palace', 'Turtle Rock', 'Dark Death Mountain Ledge (West)']

    def check_is_dark_world(region):
        for entrance in region.entrances:
            if entrance.name in DW_Entrances:
                return True
        return False

    def add_conditional_lamp(spot, region, spottype='Location'):
        if spottype == 'Location':
            spot = world.get_location(spot)
        else:
            spot = world.get_entrance(spot)
        if (not world.dark_world_light_cone and check_is_dark_world(world.get_region(region))) or (not world.light_world_light_cone and not check_is_dark_world(world.get_region(region))):
            add_lamp_requirement(spot)

    add_conditional_lamp('Misery Mire (Vitreous)', 'Misery Mire (Entrance)', 'Entrance')
    add_conditional_lamp('Turtle Rock (Dark Room) (North)', 'Turtle Rock (Entrance)', 'Entrance')
    add_conditional_lamp('Turtle Rock (Dark Room) (South)', 'Turtle Rock (Entrance)', 'Entrance')
    add_conditional_lamp('Palace of Darkness Big Key Door', 'Palace of Darkness (Entrance)', 'Entrance')
    add_conditional_lamp('Palace of Darkness Maze Door', 'Palace of Darkness (Entrance)', 'Entrance')
    add_conditional_lamp('Palace of Darkness - Dark Basement - Left', 'Palace of Darkness (Entrance)', 'Location')
    add_conditional_lamp('Palace of Darkness - Dark Basement - Right', 'Palace of Darkness (Entrance)', 'Location')
    add_conditional_lamp('Agahnim 1', 'Agahnims Tower', 'Entrance')
    add_conditional_lamp('Castle Tower - Dark Maze', 'Agahnims Tower', 'Location')
    add_conditional_lamp('Old Man', 'Old Man Cave', 'Location')
    add_conditional_lamp('Old Man Cave Exit (East)', 'Old Man Cave', 'Entrance')
    add_conditional_lamp('Death Mountain Return Cave Exit (East)', 'Death Mountain Return Cave', 'Entrance')
    add_conditional_lamp('Death Mountain Return Cave Exit (West)', 'Death Mountain Return Cave', 'Entrance')
    add_conditional_lamp('Old Man House Front to Back', 'Old Man House', 'Entrance')
    add_conditional_lamp('Old Man House Back to Front', 'Old Man House', 'Entrance')
    add_conditional_lamp('Eastern Palace - Big Key Chest', 'Eastern Palace', 'Location')
    add_conditional_lamp('Eastern Palace - Armos Knights', 'Eastern Palace', 'Location')
    add_conditional_lamp('Eastern Palace - Prize', 'Eastern Palace', 'Location')

    if not world.sewer_light_cone:
        add_lamp_requirement(world.get_location('Sewers - Dark Cross'))
        add_lamp_requirement(world.get_entrance('Sewers Back Door'))
        add_lamp_requirement(world.get_entrance('Throne Room'))


def open_rules(world):
    # softlock protection as you can reach the sewers small key door with a guard drop key
    forbid_item(world.get_location('Hyrule Castle - Boomerang Chest'), 'Small Key (Escape)')
    forbid_item(world.get_location('Hyrule Castle - Zelda\'s Chest'), 'Small Key (Escape)')

    set_rule(world.get_location('Hyrule Castle - Boomerang Chest'), lambda state: state.has('Small Key (Escape)'))
    set_rule(world.get_location('Hyrule Castle - Zelda\'s Chest'), lambda state: state.has('Small Key (Escape)'))


def swordless_rules(world):

    # for the time being swordless mode just inherits all fixes from open mode.
    # should there ever be fixes that apply to open mode but not swordless, this
    # can be revisited.
    open_rules(world)

    set_rule(world.get_entrance('Agahnims Tower'), lambda state: state.has('Cape') or state.has('Hammer') or state.has('Beat Agahnim 1'))  # barrier gets removed after killing agahnim, relevant for entrance shuffle
    set_rule(world.get_entrance('Agahnim 1'), lambda state: (state.has('Hammer') or (state.has('Bug Catching Net') and (state.has('Fire Rod') or state.has('Bow') or state.has('Cane of Somaria')))) and state.has('Small Key (Agahnims Tower)', 2))
    set_rule(world.get_location('Ether Tablet'), lambda state: state.has('Book of Mudora') and state.has('Hammer'))
    set_rule(world.get_location('Bombos Tablet'), lambda state: state.has('Book of Mudora') and state.has('Hammer') and state.has_Mirror())
    set_rule(world.get_entrance('Misery Mire'), lambda state: state.has_Pearl() and state.has_misery_mire_medallion())  # sword not required to use medallion for opening in swordless (!)
    set_rule(world.get_entrance('Turtle Rock'), lambda state: state.has_Pearl() and state.has_turtle_rock_medallion() and state.can_reach('Turtle Rock (Top)', 'Region'))   # sword not required to use medallion for opening in swordless (!)
    set_rule(world.get_entrance('Skull Woods Torch Room'), lambda state: state.has('Small Key (Skull Woods)', 3) and state.has('Fire Rod'))  # no curtain
    set_rule(world.get_entrance('Ice Palace Entrance Room'), lambda state: state.has('Fire Rod') or state.has('Bombos')) #in swordless mode bombos pads are present in the relevant parts of ice palace
    set_rule(world.get_location('Agahnim 2'), lambda state: state.has('Hammer') or state.has('Bug Catching Net'))
    set_rule(world.get_location('Ganon'), lambda state: state.has('Hammer') and state.has_fire_source() and state.has('Silver Arrows') and state.has('Bow') and state.has('Crystal 1') and state.has('Crystal 2')
                                                        and state.has('Crystal 3') and state.has('Crystal 4') and state.has('Crystal 5') and state.has('Crystal 6') and state.has('Crystal 7'))
    set_rule(world.get_entrance('Ganon Drop'), lambda state: state.has('Hammer'))  # need to damage ganon to get tiles to drop


def standard_rules(world):
    for loc in ['Sanctuary','Sewers - Secret Room - Left', 'Sewers - Secret Room - Middle',
                'Sewers - Secret Room - Right']:
        add_rule(world.get_location(loc), lambda state: state.can_kill_most_things() and state.has('Small Key (Escape)'))

    # easiest way to enforce key placement not relevant for open
    set_rule(world.get_location('Sewers - Dark Cross'), lambda state: state.can_kill_most_things())

    set_rule(world.get_location('Hyrule Castle - Boomerang Chest'), lambda state: state.can_kill_most_things())
    set_rule(world.get_location('Hyrule Castle - Zelda\'s Chest'), lambda state: state.can_kill_most_things())




def set_trock_key_rules(world):
    # ToDo If only second section entrance is available, we may very well run out of valid key locations currently.

    # this is good enough to allow even key distribution but may still prevent certain valid item combinations from being placed

    all_state = world.get_all_state()

    # check if the back entrance into trock can be accessed. As no small keys are placed yet, the rule on the dark room staircase door
    # prevents us from reach the eye bridge from within the dungeon (!)
    can_reach_back = all_state.can_reach(world.get_region('Turtle Rock (Eye Bridge)')) if world.can_access_trock_eyebridge is None else world.can_access_trock_eyebridge
    world.can_access_trock_eyebridge = can_reach_back

    # if we have backdoor access we can waste a key on the trinexx door, then have no lamp to reverse traverse the maze room. We simply require an additional key just to be super safe then. The backdoor access to the chest is otherwise free
    if not can_reach_back:
        set_rule(world.get_entrance('Turtle Rock Pokey Room'), lambda state: state.has('Small Key (Turtle Rock)', 1))
    else:
        set_rule(world.get_entrance('Turtle Rock Pokey Room'), lambda state: state.has('Small Key (Turtle Rock)', 2))

    # if we have front access this transition is useless. If we don't, it's a dead end so cannot hold any small keys
    set_rule(world.get_entrance('Turtle Rock (Chain Chomp Room) (South)'), lambda state: state.has('Small Key (Turtle Rock)', 4))

    # this is just the pokey room with one more key
    if not can_reach_back:
        set_rule(world.get_entrance('Turtle Rock (Chain Chomp Room) (North)'), lambda state: state.has('Small Key (Turtle Rock)', 2))
    else:
        set_rule(world.get_entrance('Turtle Rock (Chain Chomp Room) (North)'), lambda state: state.has('Small Key (Turtle Rock)', 3))

    # the most complicated one
    def tr_big_key_chest_keys_needed(state):
        item = item_name(state, 'Turtle Rock - Big Key Chest')
        # handle key for a key situation in the usual way (by letting us logically open the door using the key locked inside it)
        if item in ['Small Key (Turtle Rock)']:
            return 3
        # if we lack backdoor access and cannot reach the back before opening this chest because it contains the big key
        # then that means there are two doors left that we cannot have spent a key on, (crystalroller and trinexx) so we only need
        # two keys
        if item in ['Big Key (Turtle Rock)'] and not can_reach_back:
            return 2
        # otherwise we could potentially have opened every other door already, so we need all 4 keys.
        return 4

    set_rule(world.get_location('Turtle Rock - Big Key Chest'), lambda state: state.has('Small Key (Turtle Rock)', tr_big_key_chest_keys_needed(state)))
    set_always_allow(world.get_location('Turtle Rock - Big Key Chest'), lambda state, item: item.name == 'Small Key (Turtle Rock)' and state.has('Small Key (Turtle Rock)', 3))

    # set big key restrictions
    non_big_key_locations = ['Turtle Rock - Big Chest', 'Turtle Rock - Trinexx']
    if not can_reach_back:
        non_big_key_locations += ['Turtle Rock - Crystaroller Room', 'Turtle Rock - Eye Bridge - Bottom Left',
                                  'Turtle Rock - Eye Bridge - Bottom Right', 'Turtle Rock - Eye Bridge - Top Left',
                                  'Turtle Rock - Eye Bridge - Top Right']

    for location in non_big_key_locations:
        forbid_item(world.get_location(location), 'Big Key (Turtle Rock)')

    # small key restriction
    for location in ['Turtle Rock - Trinexx']:
        forbid_item(world.get_location(location), 'Small Key (Turtle Rock)')


def set_big_bomb_rules(world):
    # this is a mess
    bombshop_entrance = world.get_region('Big Bomb Shop').entrances[0]
    Normal_LW_entrances = ['Blinds Hideout',
                           'Bonk Fairy (Light)',
                           'Lake Hylia Fairy',
                           'Light Hype Fairy',
                           'Desert Fairy',
                           'Chicken House',
                           'Aginahs Cave',
                           'Sahasrahlas Hut',
                           'Cave Shop (Lake Hylia)',
                           'Blacksmiths Hut',
                           'Sick Kids House',
                           'Lost Woods Gamble',
                           'Fortune Teller (Light)',
                           'Snitch Lady (East)',
                           'Snitch Lady (West)',
                           'Bush Covered House',
                           'Tavern (Front)',
                           'Light World Bomb Hut',
                           'Kakariko Shop',
                           'Mini Moldorm Cave',
                           'Long Fairy Cave',
                           'Good Bee Cave',
                           '20 Rupee Cave',
                           '50 Rupee Cave',
                           'Ice Rod Cave',
                           'Bonk Rock Cave',
                           'Library',
                           'Potion Shop',
                           'Waterfall of Wishing',
                           'Dam',
                           'Lumberjack House',
                           'Lake Hylia Fortune Teller',
                           'Eastern Palace',
                           'Kakariko Gamble Game',
                           'Kakariko Well Cave',
                           'Bat Cave Cave',
                           'Elder House (East)',
                           'Elder House (West)',
                           'North Fairy Cave',
                           'Lost Woods Hideout Stump',
                           'Lumberjack Tree Cave',
                           'Two Brothers House (East)',
                           'Sanctuary',
                           'Hyrule Castle Entrance (South)',
                           'Hyrule Castle Secret Entrance Stairs']
    LW_walkable_entrances = ['Dark Lake Hylia Ledge Fairy',
                             'Dark Lake Hylia Ledge Spike Cave',
                             'Dark Lake Hylia Ledge Hint',
                             'Mire Shed',
                             'Dark Desert Hint',
                             'Dark Desert Fairy',
                             'Misery Mire']
    Northern_DW_entrances = ['Brewery',
                             'C-Shaped House',
                             'Chest Game',
                             'Dark World Hammer Peg Cave',
                             'Red Shield Shop',
                             'Dark Sanctuary Hint',
                             'Fortune Teller (Dark)',
                             'Dark World Shop',
                             'Dark World Lumberjack Shop',
                             'Thieves Town',
                             'Skull Woods First Section Door',
                             'Skull Woods Second Section Door (East)']
    Southern_DW_entrances = ['Hype Cave',
                             'Bonk Fairy (Dark)',
                             'Archery Game',
                             'Big Bomb Shop',
                             'Dark Lake Hylia Shop',
                             'Swamp Palace']
    Isolated_DW_entrances = ['Spike Cave',
                             'Cave Shop (Dark Death Mountain)',
                             'Dark Death Mountain Fairy',
                             'Mimic Cave',
                             'Skull Woods Second Section Door (West)',
                             'Skull Woods Final Section',
                             'Ice Palace',
                             'Turtle Rock',
                             'Dark Death Mountain Ledge (West)',
                             'Dark Death Mountain Ledge (East)',
                             'Bumper Cave (Top)',
                             'Superbunny Cave (Top)',
                             'Superbunny Cave (Bottom)',
                             'Hookshot Cave',
                             'Ganons Tower',
                             'Turtle Rock Isolated Ledge Entrance',
                             'Hookshot Cave Back Entrance']
    Isolated_LW_entrances = ['Capacity Upgrade',
                             'Tower of Hera',
                             'Death Mountain Return Cave (West)',
                             'Paradox Cave (Top)',
                             'Fairy Ascension Cave (Top)',
                             'Spiral Cave',
                             'Desert Palace Entrance (East)']
    West_LW_DM_entrances = ['Old Man Cave (East)',
                            'Old Man House (Bottom)',
                            'Old Man House (Top)',
                            'Death Mountain Return Cave (East)',
                            'Spectacle Rock Cave Peak',
                            'Spectacle Rock Cave',
                            'Spectacle Rock Cave (Bottom)']
    East_LW_DM_entrances = ['Paradox Cave (Bottom)',
                            'Paradox Cave (Middle)',
                            'Hookshot Fairy',
                            'Spiral Cave (Bottom)']
    Mirror_from_SDW_entrances = ['Two Brothers House (West)',
                                 'Cave 45']
    Castle_ledge_entrances = ['Hyrule Castle Entrance (West)',
                              'Hyrule Castle Entrance (East)',
                              'Agahnims Tower']
    Desert_mirrorable_ledge_entrances = ['Desert Palace Entrance (West)',
                                         'Desert Palace Entrance (North)',
                                         'Desert Palace Entrance (South)',
                                         'Checkerboard Cave',]

    set_rule(world.get_entrance('Pyramid Fairy'), lambda state: state.can_reach('East Dark World', 'Region') and state.can_reach('Big Bomb Shop', 'Region') and state.has('Crystal 5') and state.has('Crystal 6'))

    #crossing peg bridge starting from the southern dark world
    def cross_peg_bridge(state):
        return state.has('Hammer') and state.has_Pearl()

    # returning via the eastern and southern teleporters needs the same items, so we use the southern teleporter for out routing.
    # crossing preg bridge already requires hammer so we just add the gloves to the requirement
    def southern_teleporter(state):
        return state.can_lift_rocks() and cross_peg_bridge(state)

    # the basic routes assume you can reach eastern light world with the bomb.
    # you can then use the southern teleporter, or (if you have beaten Aga1) the hyrule castle gate warp
    def basic_routes(state):
        return southern_teleporter(state) or state.can_reach('Top of Pyramid', 'Entrance')

    # Key for below abbreviations:
    # P = pearl
    # A = Aga1
    # H = hammer
    # M = Mirror
    # G = Glove

    if bombshop_entrance.name in Normal_LW_entrances:
        #1. basic routes
        #2. Can reach Eastern dark world some other way, mirror, get bomb, return to mirror spot, walk to pyramid: Needs mirror
        # -> M or BR
        add_rule(world.get_entrance('Pyramid Fairy'), lambda state: basic_routes(state) or state.has_Mirror())
    elif bombshop_entrance.name in LW_walkable_entrances:
        #1. Mirror then basic routes
        # -> M and BR
        add_rule(world.get_entrance('Pyramid Fairy'), lambda state: state.has_Mirror() and basic_routes(state))
    elif bombshop_entrance.name in Northern_DW_entrances:
        #1. Mirror and basic routes
        #2. Go to south DW and then cross peg bridge: Need Mitts and hammer and moon pearl
        # -> (Mitts and CPB) or (M and BR)
        add_rule(world.get_entrance('Pyramid Fairy'), lambda state: (state.can_lift_heavy_rocks() and cross_peg_bridge(state)) or (state.has_Mirror() and basic_routes(state)))
    elif bombshop_entrance.name == 'Bumper Cave (Bottom)':
        #1. Mirror and Lift rock and basic_routes
        #2. Mirror and Flute and basic routes (can make difference if accessed via insanity or w/ mirror from connector, and then via hyrule castle gate, because no gloves are needed in that case)
        #3. Go to south DW and then cross peg bridge: Need Mitts and hammer and moon pearl
        # -> (Mitts and CPB) or (((G or Flute) and M) and BR))
        add_rule(world.get_entrance('Pyramid Fairy'), lambda state: (state.can_lift_heavy_rocks() and cross_peg_bridge(state)) or (((state.can_lift_rocks() or state.has('Ocarina')) and state.has_Mirror()) and basic_routes(state)))
    elif bombshop_entrance.name in Southern_DW_entrances:
        #1. Mirror and enter via gate: Need mirror and Aga1
        #2. cross peg bridge: Need hammer and moon pearl
        # -> CPB or (M and A)
        add_rule(world.get_entrance('Pyramid Fairy'), lambda state: cross_peg_bridge(state) or (state.has_Mirror() and state.can_reach('Top of Pyramid', 'Entrance')))
    elif bombshop_entrance.name in Isolated_DW_entrances:
        # 1. mirror then flute then basic routes
        # -> M and Flute and BR
        add_rule(world.get_entrance('Pyramid Fairy'), lambda state: state.has_Mirror() and state.has('Ocarina') and basic_routes(state))
    elif bombshop_entrance.name in Isolated_LW_entrances:
        # 1. flute then basic routes
        # Prexisting mirror spot is not permitted, because mirror might have been needed to reach these isolated locations.
        # -> Flute and BR
        add_rule(world.get_entrance('Pyramid Fairy'), lambda state: state.has('Ocarina') and basic_routes(state))
    elif bombshop_entrance.name in West_LW_DM_entrances:
        # 1. flute then basic routes or mirror
        # Prexisting mirror spot is permitted, because flute can be used to reach west DM directly.
        # -> Flute and (M or BR)
        add_rule(world.get_entrance('Pyramid Fairy'), lambda state: state.has('Ocarina') and (state.has_Mirror() or basic_routes(state)))
    elif bombshop_entrance.name in East_LW_DM_entrances:
        # 1. flute then basic routes or mirror and hookshot
        # Prexisting mirror spot is permitted, because flute can be used to reach west DM directly and then east DM via Hookshot
        # -> Flute and ((M and Hookshot) or BR)
        add_rule(world.get_entrance('Pyramid Fairy'), lambda state: state.has('Ocarina') and ((state.has_Mirror() and state.has('Hookshot')) or basic_routes(state)))
    elif bombshop_entrance.name == 'Fairy Ascension Cave (Bottom)':
        # Same as East_LW_DM_entrances except navigation without BR requires Mitts
        # -> Flute and ((M and Hookshot and Mitts) or BR)
        add_rule(world.get_entrance('Pyramid Fairy'), lambda state: state.has('Ocarina') and ((state.has_Mirror() and state.has('Hookshot') and state.can_lift_heavy_rocks()) or basic_routes(state)))
    elif bombshop_entrance.name in Castle_ledge_entrances:
        # 1. mirror on pyramid to castle ledge, grab bomb, return through mirror spot: Needs mirror
        # 2. flute then basic routes
        # -> M or (Flute and BR)
        add_rule(world.get_entrance('Pyramid Fairy'), lambda state: state.has_Mirror() or (state.has('Ocarina') and basic_routes(state)))
    elif bombshop_entrance.name in Desert_mirrorable_ledge_entrances:
        # Cases when you have mire access: Mirror to reach locations, return via mirror spot, move to center of desert, mirror anagin and:
        # 1. Have mire access, Mirror to reach locations, return via mirror spot, move to center of desert, mirror again and then basic routes
        # 2. flute then basic routes
        # -> (Mire access and M) or Flute) and BR
        add_rule(world.get_entrance('Pyramid Fairy'), lambda state: ((state.can_reach('Dark Desert', 'Region') and state.has_Mirror()) or state.has('Ocarina')) and basic_routes(state))
    elif bombshop_entrance.name == 'Old Man Cave (West)':
        # 1. Lift rock then basic_routes
        # 2. flute then basic_routes
        # -> (Flute or G) and BR
        add_rule(world.get_entrance('Pyramid Fairy'), lambda state: (state.has('Ocarina') or state.can_lift_rocks()) and basic_routes(state))
    elif bombshop_entrance.name == 'Graveyard Cave':
        # 1. flute then basic routes
        # 2. (has west dark world access) use existing mirror spot (required Pearl), mirror again off ledge
        # -> (Flute or (M and P and West Dark World access) and BR
        add_rule(world.get_entrance('Pyramid Fairy'), lambda state: (state.has('Ocarina') or (state.can_reach('West Dark World', 'Region') and state.has_Pearl() and state.has_Mirror())) and basic_routes(state))
    elif bombshop_entrance.name in Mirror_from_SDW_entrances:
        # 1. flute then basic routes
        # 2. (has South dark world access) use existing mirror spot, mirror again off ledge
        # -> (Flute or (M and South Dark World access) and BR
        add_rule(world.get_entrance('Pyramid Fairy'), lambda state: (state.has('Ocarina') or (state.can_reach('South Dark World', 'Region') and state.has_Mirror())) and basic_routes(state))
    elif bombshop_entrance.name == 'Dark World Potion Shop':
        # 1. walk down by lifting rock: needs gloves and pearl`
        # 2. walk down by hammering peg: needs hammer and pearl
        # 3. mirror and basic routes
        # -> (P and (H or Gloves)) or (M and BR)
        add_rule(world.get_entrance('Pyramid Fairy'), lambda state: (state.has_Pearl() and (state.has('Hammer') or state.can_lift_rocks())) or (state.has_Mirror() and basic_routes(state)))
    elif bombshop_entrance.name == 'Kings Grave':
        # same as the Normal_LW_entrances case except that the pre-existing mirror is only possible if you have mitts
        # (because otherwise mirror was used to reach the grave, so would cancel a pre-existing mirror spot)
        # to account for insanity, must consider a way to escape without a cave for basic_routes
        # -> (M and Mitts) or ((Mitts or Flute or (M and P and West Dark World access)) and BR)
        add_rule(world.get_entrance('Pyramid Fairy'), lambda state: (state.can_lift_heavy_rocks() and state.has_Mirror()) or ((state.can_lift_heavy_rocks() or state.has('Ocarina') or (state.can_reach('West Dark World', 'Region') and state.has_Pearl() and state.has_Mirror())) and basic_routes(state)))

def set_bunny_rules(world):

    # regions for the exits of multi-entrace caves/drops that bunny cannot pass
    # Note spiral cave may be technically passible, but it would be too absurd to require since OHKO mode is a thing.
    bunny_impassable_caves = ['Bumper Cave', 'Two Brothers House', 'Hookshot Cave', 'Skull Woods First Section (Right)', 'Skull Woods First Section (Left)', 'Skull Woods First Section (Top)', 'Turtle Rock (Entrance)', 'Turtle Rock (Second Section)', 'Turtle Rock (Big Chest)', 'Skull Woods Second Section (Drop)',
                              'Turtle Rock (Eye Bridge)', 'Sewers', 'Pyramid', 'Spiral Cave (Top)', 'Desert Palace Main (Inner)']

    bunny_accessible_locations = ['Link\'s Uncle', 'Sahasrahla', 'Sick Kid', 'Lost Woods Hideout', 'Lumberjack Tree', 'Checkerboard Cave', 'Potion Shop', 'Spectacle Rock Cave', 'Pyramid', 'Hype Cave - Generous Guy', 'Peg Cave', 'Bumper Cave Ledge']

    if world.get_region('Dam').is_dark_world:
        # if Dam is is dark world, then it is required to have the pearl to get the sunken item
        add_rule(world.get_location('Sunken Treasure'), lambda state: state.has_Pearl())
        # similarly we need perl to get across the swamp palace moat
        add_rule(world.get_entrance('Swamp Palace Moat'), lambda state: state.has_Pearl())

    def path_to_access_rule(path, entrance):
        return lambda state: state.can_reach(entrance) and all(rule(state) for rule in path)

    def options_to_access_rule(options):
        return lambda state: any(rule(state) for rule in options)

    def get_rule_to_add(region):
        if not region.is_light_world:
            return lambda state: state.has_Pearl()
        # in this case we are mixed region.
        # we collect possible options.

        # The base option is having the moon pearl
        possible_options = [lambda state: state.has_Pearl()]

        # We will search entrances recursively until we find
        # one that leads to an exclusively light world region
        # for each such entrance a new option ios aded that consist of:
        #    a) being able to reach it, and
        #    b) being able to access all entrances from there to `region`
        seen = set([region])
        queue = collections.deque([(region, [])])
        while queue:
            (current, path) = queue.popleft()
            for entrance in current.entrances:
                new_region = entrance.parent_region
                if new_region in seen:
                    continue
                new_path = path + [entrance.access_rule]
                seen.add(new_region)
                if not new_region.is_light_world:
                    continue # we don't care about pure dark world entrances
                if new_region.is_dark_world:
                    queue.append((new_region, new_path))
                else:
                    # we have reached pure light world, so we have a new possible option
                    possible_options.append(path_to_access_rule(new_path, entrance))
        return options_to_access_rule(possible_options)

    # Add requirements for bunny-impassible caves if they occur in the dark world
    for region in [world.get_region(name) for name in bunny_impassable_caves]:

        if not region.is_dark_world:
            continue
        rule = get_rule_to_add(region)
        for exit in region.exits:
            add_rule(exit, rule)

    # Add requirements for all locations that are actually in the dark world, except those available to the bunny
    for location in world.get_locations():
        if location.parent_region.is_dark_world:

            if location.name in bunny_accessible_locations:
                continue

            add_rule(location, get_rule_to_add(location.parent_region))
