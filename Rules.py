import logging


def set_rules(world):
    global_rules(world)

    if world.logic == 'noglitches':
        no_glitches_rules(world)
    elif world.logic == 'minorglitches':
        logging.getLogger('').info('Minor Glitches may be buggy still. No guarantee for proper logic checks.')
    else:
        raise NotImplementedError('Not implemented yet')

    if world.mode == 'open':
        open_rules(world)
    elif world.mode == 'standard':
        standard_rules(world)
    else:
        raise NotImplementedError('Not implemented yet')

    if world.goal == 'dungeons':
        # require altar for ganon to enforce getting everything
        add_rule(world.get_location('Ganon'), lambda state: state.can_reach('Altar', 'Location'))

    set_blacksmith_rules(world)
    set_big_bomb_rules(world)

    # if swamp and dam have not been moved we require mirror for swamp palace
    if not world.swamp_patch_required:
        add_rule(world.get_entrance('Swamp Palace Moat'), lambda state: state.has_Mirror())

    return ''


def set_rule(spot, rule):
    spot.access_rule = rule


def add_rule(spot, rule, combine='and'):
    old_rule = spot.access_rule
    if combine == 'or':
        spot.access_rule = lambda state: rule(state) or old_rule(state)
    else:
        spot.access_rule = lambda state: rule(state) and old_rule(state)


def add_lamp_requirement(spot):
    add_rule(spot, lambda state: state.has('Lamp'))


def forbid_item(location, item):
    old_rule = location.item_rule
    location.item_rule = lambda i: i.name != item and old_rule(i)


def global_rules(world):
    # ganon can only carry triforce
    world.get_location('Ganon').item_rule = lambda item: item.name == 'Triforce'

    # these are default save&quit points and always accessible
    world.get_region('Links House').can_reach = lambda state: True
    world.get_region('Sanctuary').can_reach = lambda state: True

    # we can s&q to the old man house after we rescue him. This may be somewhere completely different if caves are shuffled!
    old_rule = world.get_region('Old Man House').can_reach
    world.get_region('Old Man House').can_reach = lambda state: state.can_reach('Old Mountain Man', 'Location') or old_rule(state)

    # overworld requirements
    set_rule(world.get_entrance('Kings Grave'), lambda state: state.has_Boots() and (state.can_lift_heavy_rocks() or (state.has_Mirror() and state.can_reach('West Dark World'))))
    set_rule(world.get_entrance('Bonk Fairy (Light)'), lambda state: state.has_Boots())
    set_rule(world.get_location('Piece of Heart (Dam)'), lambda state: state.can_reach('Dam'))
    set_rule(world.get_entrance('Bat Cave Drop Ledge'), lambda state: state.has('Hammer'))
    set_rule(world.get_entrance('Lumberjack Tree Tree'), lambda state: state.has_Boots() and state.can_reach('Top of Pyramid', 'Entrance'))
    set_rule(world.get_entrance('Bonk Rock Cave'), lambda state: state.has_Boots())
    set_rule(world.get_entrance('Desert Palace Stairs'), lambda state: state.has('Book of Mudora'))
    set_rule(world.get_entrance('Sanctuary Grave'), lambda state: state.can_lift_rocks())
    set_rule(world.get_entrance('20 Rupee Cave'), lambda state: state.can_lift_rocks())
    set_rule(world.get_entrance('50 Rupee Cave'), lambda state: state.can_lift_rocks())
    set_rule(world.get_entrance('Old Man Cave (West)'), lambda state: state.can_lift_rocks())
    set_rule(world.get_entrance('Flute Spot 1'), lambda state: state.has('Ocarina'))
    set_rule(world.get_entrance('Ice Palace'), lambda state: state.can_lift_heavy_rocks())
    set_rule(world.get_entrance('Dark Desert Teleporter'), lambda state: state.has('Ocarina') and state.can_lift_heavy_rocks())
    set_rule(world.get_entrance('East Hyrule Teleporter'), lambda state: state.has('Hammer') and state.can_lift_rocks() and state.has_Pearl())
    set_rule(world.get_entrance('South Hyrule Teleporter'), lambda state: state.has('Hammer') and state.can_lift_rocks() and state.has_Pearl())
    set_rule(world.get_entrance('Kakariko Teleporter'), lambda state: ((state.has('Hammer') and state.can_lift_rocks()) or state.can_lift_heavy_rocks()) and state.has_Pearl())
    set_rule(world.get_location('Haunted Grove'), lambda state: state.has('Shovel'))
    set_rule(world.get_location('Purple Chest'), lambda state: state.can_reach('Blacksmiths', 'Location'))

    set_rule(world.get_location('Piece of Heart (Zoras River)'), lambda state: state.has('Flippers'))
    set_rule(world.get_entrance('Waterfall of Wishing'), lambda state: state.has('Flippers'))  # can be fake flippered into, but is in weird state inside that might prevent you from doing things. Can be improved in future Todo
    set_rule(world.get_location('Blacksmiths'), lambda state: state.can_lift_heavy_rocks() and state.has_Mirror() and state.can_reach('West Dark World'))
    set_rule(world.get_location('Magic Bat'), lambda state: state.has('Magic Powder'))
    set_rule(world.get_location('Sick Kid'), lambda state: state.has('Bottle'))
    set_rule(world.get_location('Library'), lambda state: state.has_Boots())
    set_rule(world.get_location('Witch'), lambda state: state.has('Mushroom'))
    set_rule(world.get_entrance('Desert Palace Entrance (North) Rocks'), lambda state: state.can_lift_rocks())
    set_rule(world.get_entrance('Desert Ledge Return Rocks'), lambda state: state.can_lift_rocks())  # should we decide to place something that is not a dungeon end up there at some point
    set_rule(world.get_entrance('Desert Cave'), lambda state: state.can_lift_rocks())
    set_rule(world.get_location('Altar'), lambda state: state.can_collect('Red Pendant') and state.can_collect('Blue Pendant') and state.can_collect('Green Pendant'))
    set_rule(world.get_location('Sahasrahla'), lambda state: state.can_collect('Green Pendant'))
    set_rule(world.get_entrance('Agahnims Tower'), lambda state: state.has('Cape') or state.has_beam_sword() or state.can_reach('Agahnim 1'))  # barrier gets removed after killing agahnim, relevant for entrance shuffle
    set_rule(world.get_entrance('Agahnim 1'), lambda state: state.has_sword())
    set_rule(world.get_entrance('Old Man Cave Exit (West)'), lambda state: False)  # drop cannott be climbed up
    set_rule(world.get_entrance('Broken Bridge (West)'), lambda state: state.has('Hookshot'))
    set_rule(world.get_entrance('Broken Bridge (East)'), lambda state: state.has('Hookshot'))
    set_rule(world.get_entrance('East Death Mountain Teleporter'), lambda state: state.can_lift_heavy_rocks())
    set_rule(world.get_entrance('Death Mountain Fairy Drop Area Rocks'), lambda state: state.can_lift_rocks())
    set_rule(world.get_entrance('Death Mountain Climb Push Block Reverse'), lambda state: state.has('Mirror'))  # can erase block
    set_rule(world.get_entrance('Death Mountain (Top)'), lambda state: state.has('Hammer'))
    set_rule(world.get_entrance('Turtle Rock Teleporter'), lambda state: state.can_lift_heavy_rocks() and state.has('Hammer'))
    set_rule(world.get_entrance('Turtle Rock Skull Mirror Spot'), lambda state: state.has_Mirror() and state.has('Hammer'))  # if stuck, can mirror and hammer the pegs
    set_rule(world.get_entrance('Turtle Rock'), lambda state: state.can_reach('Turtle Rock Open Skull', 'Entrance'))
    set_rule(world.get_entrance('Turtle Rock Skull Reverse'), lambda state: state.can_reach('Turtle Rock Open Skull', 'Entrance'))
    set_rule(world.get_location('Ether Tablet'), lambda state: state.has('Book of Mudora') and state.has_beam_sword())
    set_rule(world.get_entrance('East Death Mountain (Top)'), lambda state: state.has('Hammer'))

    set_rule(world.get_location('Catfish'), lambda state: state.has_Pearl() and state.can_lift_rocks())
    set_rule(world.get_entrance('Dark World Potion Shop'), lambda state: state.has_Pearl() and (state.can_lift_rocks() or state.has('Hammer') or state.has('Flippers')))
    set_rule(world.get_entrance('South Dark World Bridge'), lambda state: state.has('Hammer') and state.has_Pearl())
    set_rule(world.get_entrance('Bonk Fairy (Dark)'), lambda state: state.has_Boots())
    set_rule(world.get_entrance('West Dark World Gap'), lambda state: state.has_Pearl() and state.has('Hookshot') and (state.has('Flippers') or state.has('Hammer') or state.can_lift_rocks()))
    set_rule(world.get_entrance('Palace of Darkness'), lambda state: state.has_Pearl() and state.can_reach('Palace of Darkness Pay Kiki', 'Entrance'))  # ToDo Not sure if required
    set_rule(world.get_entrance('Palace of Darkness Kiki Door Reverse'), lambda state: state.can_reach('Palace of Darkness Pay Kiki', 'Entrance'))  # prevent soft lock when coming from behind, not required
    set_rule(world.get_entrance('Hyrule Castle Ledge Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Dark Lake Hylia Drop (East)'), lambda state: (state.has_Pearl() and state.has('Flippers') or state.has_Mirror()))  # Overworld Bunny Revival
    set_rule(world.get_location('Bombos Tablet'), lambda state: state.has('Book of Mudora') and state.has_beam_sword() and state.has_Mirror())
    set_rule(world.get_entrance('Dark Lake Hylia Drop (South)'), lambda state: state.has('Flippers'))  # ToDo any fake flipper set up?
    set_rule(world.get_entrance('Dark Lake Hylia Ledge Spike Cave'), lambda state: state.can_lift_rocks())
    set_rule(world.get_entrance('Dark Lake Hylia Ledge'), lambda state: state.has_Pearl())  # To avoid Bunny nonsense for now
    set_rule(world.get_entrance('Dark Lake Hylia Teleporter'), lambda state: state.has_Pearl() and (state.has('Hammer') or state.can_lift_rocks()))  # Fake Flippers
    set_rule(world.get_entrance('Village of Outcasts Heavy Rock'), lambda state: state.can_lift_heavy_rocks())
    set_rule(world.get_entrance('Maze Race Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Cave South of Haunted Grove'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('East Dark World Bridge'), lambda state: state.has('Hammer'))
    set_rule(world.get_entrance('Lake Hylia Island Mirror Spot'), lambda state: state.has_Mirror() and state.has('Flippers'))
    set_rule(world.get_entrance('East Dark World River Pier'), lambda state: state.has('Flippers'))  # ToDo any fake flipper set up?
    set_rule(world.get_entrance('Graveyard Cave'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Bumper Cave (Bottom)'), lambda state: state.can_lift_rocks())
    set_rule(world.get_entrance('Bumper Cave Ledge Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Bat Cave Drop Ledge Mirror Spot'), lambda state: state.can_lift_heavy_rocks() and state.has_Mirror())
    set_rule(world.get_entrance('Dark World Hammer Peg Cave'), lambda state: state.can_lift_heavy_rocks() and state.has('Hammer'))
    set_rule(world.get_entrance('Dark World Shop'), lambda state: state.has('Hammer'))
    set_rule(world.get_entrance('Bumper Cave Exit (Top)'), lambda state: state.has('Cape'))
    set_rule(world.get_entrance('Bumper Cave Exit (Bottom)'), lambda state: state.has('Cape') or state.has('Hookshot'))
    set_rule(world.get_entrance('Skull Woods Burn Skull'), lambda state: state.has('Fire Rod'))
    set_rule(world.get_entrance('Skull Woods Final Section'), lambda state: state.can_reach('Skull Woods Burn Skull', 'Entrance'))  # prevent soft lock when coming from behind, not required
    set_rule(world.get_entrance('Skull Woods Skull Reverse'), lambda state: state.can_reach('Skull Woods Burn Skull', 'Entrance'))
    set_rule(world.get_entrance('Misery Mire'), lambda state: state.has_Pearl() and state.has_sword() and state.has_misery_mire_medallion())  # sword required to cast magic (!)
    set_rule(world.get_entrance('Desert Ledge (West) Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Desert Ledge Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Desert Palace Stairs Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Desert Palace Entrance (North) Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Dark Desert Cave'), lambda state: state.has_Pearl())  # ToDo Bunny Revival can give access to this cave in super bunny state. Not sure how to deal with shuffled entrances, as much easier to block of cave entrances than individual shuffled chests
    set_rule(world.get_entrance('Dark Desert Hint'), lambda state: state.has_Pearl())  # ToDo Bunny Revival can give access to this cave in super bunny state. Not sure how to deal with shuffled entrances, as much easier to block of cave entrances than individual shuffled chests
    set_rule(world.get_entrance('Dark Desert Fairy'), lambda state: state.has_Pearl())  # ToDo Bunny Revival can give access to this cave in super bunny state. Not sure how to deal with shuffled entrances, as much easier to block of cave entrances than individual shuffled chests
    set_rule(world.get_entrance('Spike Cave'), lambda state: state.has_Pearl())
    set_rule(world.get_entrance('Dark Death Mountain Fairy'), lambda state: state.has_Pearl())
    set_rule(world.get_entrance('Spectacle Rock Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Ganons Tower'), lambda state: state.can_collect('Crystal 1') and state.can_collect('Crystal 2') and state.can_collect('Crystal 3') and state.can_collect('Crystal 4') and state.can_collect('Crystal 5') and state.can_collect('Crystal 6') and state.can_collect('Crystal 7'))
    set_rule(world.get_entrance('Hookshot Cave'), lambda state: state.can_lift_rocks() and state.has_Pearl())
    set_rule(world.get_entrance('East Death Mountain (Top) Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Mimic Cave Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Death Mountain Fairy Drop Area Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Spiral Cave Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Death Mountain Fairy Drop Area Rocks'), lambda state: state.can_lift_rocks())
    set_rule(world.get_entrance('Death Mountain Fairy Drop Area Mirror Spot'), lambda state: state.has_Mirror() and state.has_Pearl())  # need to lift flowers
    set_rule(world.get_entrance('Isolated Ledge Mirror Spot'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Dark Death Mountain Climb (Top)'), lambda state: state.has_Pearl())  # Chests inside could be  collected with super bunny, but may be shuffled. rather limit access for now ToDo
    set_rule(world.get_entrance('Dark Death Mountain Climb (Bottom)'), lambda state: state.has_Pearl())
    set_rule(world.get_entrance('Cave Shop (Dark Death Mountain)'), lambda state: state.has_Pearl())  # just for save bunny algo for now
    set_rule(world.get_entrance('Dark Death Mountain Climb Exit (Bottom)'), lambda state: False)  # Cannot get to bottom exit from top. Just exists for shuffling
    set_rule(world.get_location('[cave-055] Spike Cave'), lambda state: state.has('Hammer') and state.can_lift_rocks())  # damage should be survivable always somehow. MAY need more logic ToDo
    set_rule(world.get_location('[cave-056] Hookshot Cave [top right chest]'), lambda state: state.has('Hookshot'))
    set_rule(world.get_location('[cave-056] Hookshot Cave [top left chest]'), lambda state: state.has('Hookshot'))
    set_rule(world.get_location('[cave-056] Hookshot Cave [bottom right chest]'), lambda state: state.has('Hookshot') or state.has('Pegasus Boots'))
    set_rule(world.get_location('[cave-056] Hookshot Cave [bottom left chest]'), lambda state: state.has('Hookshot'))
    set_rule(world.get_location('Piece of Heart (Death Mountain - Floating Island)'), lambda state: state.has_Mirror())
    set_rule(world.get_entrance('Turtle Rock'), lambda state: state.has_Pearl() and state.has_sword() and state.has_turtle_rock_medallion())  # sword required to cast magic (!)
    set_rule(world.get_location('[cave-013] Mimic Cave'), lambda state: state.has('Hammer'))

    set_rule(world.get_entrance('Sewers Door'), lambda state: state.can_collect('Small Key (Escape)'))
    set_rule(world.get_entrance('Sewers Back Door'), lambda state: state.can_collect('Small Key (Escape)'))

    set_rule(world.get_location('[dungeon-L1-1F] Eastern Palace - Big Chest'), lambda state: state.can_collect('Big Key (Eastern Palace)'))
    set_rule(world.get_location('Armos - Heart Container'), lambda state: state.has('Bow') and state.can_collect('Big Key (Eastern Palace)'))
    set_rule(world.get_location('Armos - Pendant'), lambda state: state.has('Bow') and state.can_collect('Big Key (Eastern Palace)'))
    for location in ['Armos - Heart Container', '[dungeon-L1-1F] Eastern Palace - Big Chest']:
        forbid_item(world.get_location(location), 'Big Key (Eastern Palace)')

    set_rule(world.get_location('[dungeon-L2-B1] Desert Palace - Big Chest'), lambda state: state.can_collect('Big Key (Desert Palace)'))
    set_rule(world.get_location('[dungeon-L2-B1] Desert Palace - Torch'), lambda state: state.has_Boots())
    set_rule(world.get_entrance('Desert Palace East Wing'), lambda state: state.can_collect('Small Key (Desert Palace)'))
    set_rule(world.get_location('Lanmolas - Pendant'), lambda state: state.can_collect('Small Key (Desert Palace)') and state.can_collect('Big Key (Desert Palace)') and state.has_fire_source() and
                                                                     (state.has_blunt_weapon() or state.has('Fire Rod') or state.has('Ice Rod') or state.has('Bow')))
    set_rule(world.get_location('Lanmolas - Heart Container'), lambda state: state.can_collect('Small Key (Desert Palace)') and state.can_collect('Big Key (Desert Palace)') and state.has_fire_source() and
                                                                     (state.has_blunt_weapon() or state.has('Fire Rod') or state.has('Ice Rod') or state.has('Bow')))
    for location in ['Lanmolas - Heart Container', '[dungeon-L2-B1] Desert Palace - Big Chest']:
        forbid_item(world.get_location(location), 'Big Key (Desert Palace)')

    set_rule(world.get_entrance('Tower of Hera Small Key Door'), lambda state: state.can_collect('Small Key (Tower of Hera)'))
    set_rule(world.get_entrance('Tower of Hera Big Key Door'), lambda state: state.can_collect('Big Key (Tower of Hera)'))
    set_rule(world.get_location('[dungeon-L3-1F] Tower of Hera - Big Chest'), lambda state: state.can_collect('Big Key (Tower of Hera)'))
    set_rule(world.get_location('[dungeon-L3-1F] Tower of Hera - Basement'), lambda state: state.has_fire_source())
    set_rule(world.get_location('Moldorm - Heart Container'), lambda state: state.has_blunt_weapon())
    set_rule(world.get_location('Moldorm - Pendant'), lambda state: state.has_blunt_weapon())
    for location in ['Moldorm - Heart Container', '[dungeon-L3-1F] Tower of Hera - Big Chest', '[dungeon-L3-1F] Tower of Hera - 4F [small chest]']:
        forbid_item(world.get_location(location), 'Big Key (Tower of Hera)')

    set_rule(world.get_entrance('Swamp Palace Moat'), lambda state: state.has('Flippers') and state.can_reach('Dam'))
    set_rule(world.get_entrance('Swamp Palace Small Key Door'), lambda state: state.can_collect('Small Key (Swamp Palace)'))
    set_rule(world.get_entrance('Swamp Palace (Center)'), lambda state: state.has('Hammer'))
    set_rule(world.get_location('[dungeon-D2-B1] Swamp Palace - Big Chest'), lambda state: state.can_collect('Big Key (Swamp Palace)'))
    set_rule(world.get_entrance('Swamp Palace (North)'), lambda state: state.has('Hookshot'))
    set_rule(world.get_location('Arrghus - Heart Container'), lambda state: state.has_blunt_weapon())
    set_rule(world.get_location('Arrghus - Crystal'), lambda state: state.has_blunt_weapon())
    for location in ['[dungeon-D2-B1] Swamp Palace - Big Chest', '[dungeon-D2-1F] Swamp Palace - First Room']:
        forbid_item(world.get_location(location), 'Big Key (Swamp Palace)')

    set_rule(world.get_entrance('Thieves Town Big Key Door'), lambda state: state.can_collect('Big Key (Thieves Town)'))
    set_rule(world.get_entrance('Blind Fight'), lambda state: state.can_collect('Small Key (Thieves Town)') and (state.has_blunt_weapon() or state.has('Cane of Somaria')))
    set_rule(world.get_location('[dungeon-D4-B2] Thieves Town - Big Chest'), lambda state: state.can_collect('Small Key (Thieves Town)') and state.has('Hammer'))
    set_rule(world.get_location('[dungeon-D4-1F] Thieves Town - Room above Boss'), lambda state: state.can_collect('Small Key (Thieves Town)'))
    for location in ['[dungeon-D4-1F] Thieves Town - Room above Boss', '[dungeon-D4-B2] Thieves Town - Big Chest', '[dungeon-D4-B2] Thieves Town - Chest next to Blind', 'Blind - Heart Container']:
        forbid_item(world.get_location(location), 'Big Key (Thieves Town)')

    set_rule(world.get_location('[dungeon-D3-B1] Skull Woods - Big Chest'), lambda state: state.can_collect('Big Key (Skull Woods)'))
    set_rule(world.get_entrance('Skull Woods Torch Room'), lambda state: state.can_collect('Small Key (Skull Woods)', 3) and state.has('Fire Rod') and state.has_sword())  # sword required for curtain
    for location in ['[dungeon-D3-B1] Skull Woods - Big Chest']:
        forbid_item(world.get_location(location), 'Big Key (Skull Woods)')

    set_rule(world.get_entrance('Ice Palace Entrance Room'), lambda state: state.has('Fire Rod') or (state.has('Bombos') and state.has_sword()))
    set_rule(world.get_location('[dungeon-D5-B5] Ice Palace - Big Chest'), lambda state: state.can_collect('Big Key (Ice Palace)'))
    set_rule(world.get_entrance('Ice Palace (Kholdstare)'), lambda state: state.can_lift_rocks() and state.has('Hammer') and state.can_collect('Big Key (Ice Palace)') and (state.can_collect('Small Key (Ice Palace)', 2) or (state.has('Cane of Somaria') and state.can_collect('Small Key (Ice Palace)', 1))))
    set_rule(world.get_entrance('Ice Palace (East)'), lambda state: state.has('Hookshot') or (state.can_collect('Small Key (Ice Palace)', 1) and ((state.world.get_location('[dungeon-D5-B3] Ice Palace - Spike Room').item is not None and state.world.get_location('[dungeon-D5-B3] Ice Palace - Spike Room').item.name in ['Big Key (Ice Palace)']) or
                                                                                                                                                  (state.world.get_location('[dungeon-D5-B1] Ice Palace - Big Key Room').item is not None and state.world.get_location('[dungeon-D5-B1] Ice Palace - Big Key Room').item.name in ['Big Key (Ice Palace)']) or
                                                                                                                                                  (state.world.get_location('[dungeon-D5-B2] Ice Palace - Map Room').item is not None and state.world.get_location('[dungeon-D5-B2] Ice Palace - Map Room').item.name in ['Big Key (Ice Palace)']))))  # if you do ipbj and waste SKs in the basement, you have to BJ over the hookshot room to fix your mess potentially. This seems fair
    set_rule(world.get_entrance('Ice Palace (East Top)'), lambda state: state.can_lift_rocks() and state.has('Hammer'))
    for location in ['[dungeon-D5-B5] Ice Palace - Big Chest', 'Kholdstare - Heart Container']:
        forbid_item(world.get_location(location), 'Big Key (Ice Palace)')

    set_rule(world.get_entrance('Misery Mire Entrance Gap'), lambda state: (state.has_Boots() or state.has('Hookshot')) and (state.has_sword() or state.has('Fire Rod') or state.has('Ice Rod') or state.has('Hammer') or state.has('Cane of Somaria') or state.has('Bow')))  # need to defeat wizzrobes, bombs don't work ...
    set_rule(world.get_location('[dungeon-D6-B1] Misery Mire - Big Chest'), lambda state: state.can_collect('Big Key (Misery Mire)'))
    set_rule(world.get_entrance('Misery Mire Big Key Door'), lambda state: state.can_collect('Big Key (Misery Mire)'))
    # we can place a small key in the West wing iff it also contains/blocks the Big Key, as we cannot reach and softlock with the basement key door yet
    set_rule(world.get_entrance('Misery Mire (West)'), lambda state: state.can_collect('Small Key (Misery Mire)', 3) if state.can_reach('Misery Mire (Final Area)') else state.can_collect('Small Key (Misery Mire)', 2))
    set_rule(world.get_entrance('Misery Mire (Vitreous)'), lambda state: state.has('Cane of Somaria') and (state.has('Bow') or state.has_blunt_weapon()))
    for location in ['[dungeon-D6-B1] Misery Mire - Big Chest', 'Vitreous - Heart Container']:
        forbid_item(world.get_location(location), 'Big Key (Misery Mire)')

    # ToDo: This needs a complete overhaul
    set_rule(world.get_entrance('Turtle Rock Entrance Gap'), lambda state: state.has('Cane of Somaria'))
    set_rule(world.get_entrance('Turtle Rock Entrance Gap Reverse'), lambda state: state.has('Cane of Somaria'))
    set_rule(world.get_location('[dungeon-D7-1F] Turtle Rock - Compass Room'), lambda state: state.has('Cane of Somaria'))  # We could get here from the middle section without Cane as we don't cross the entrance gap!
    set_rule(world.get_location('[dungeon-D7-1F] Turtle Rock - Map Room [left chest]'), lambda state: state.has('Cane of Somaria') and state.has('Fire Rod'))
    set_rule(world.get_location('[dungeon-D7-1F] Turtle Rock - Map Room [right chest]'), lambda state: state.has('Cane of Somaria') and state.has('Fire Rod'))
    set_rule(world.get_entrance('Turtle Rock Pokey Room'), lambda state: state.can_collect('Small Key (Turtle Rock)', 3) if state.can_reach('Turtle Rock (Dark Room) (North)', 'Entrance') else state.can_collect('Small Key (Turtle Rock)', 2) if state.can_reach('Turtle Rock (Eye Bridge)') else state.can_collect('Small Key (Turtle Rock)', 1))  # May waste keys from back entrance if accessible
    set_rule(world.get_entrance('Turtle Rock (Chain Chomp Room) (South)'), lambda state: state.can_collect('Small Key (Turtle Rock)', 4))  # Just to be save
    set_rule(world.get_entrance('Turtle Rock (Chain Chomp Room) (North)'), lambda state: state.can_collect('Small Key (Turtle Rock)', 4) if state.can_reach('Turtle Rock (Dark Room) (North)', 'Entrance') else state.can_collect('Small Key (Turtle Rock)', 3) if state.can_reach('Turtle Rock (Eye Bridge)') else state.can_collect('Small Key (Turtle Rock)', 2))  # May waste keys from back entrance if accessible
    set_rule(world.get_location('[dungeon-D7-B1] Turtle Rock - Big Chest'), lambda state: state.can_collect('Big Key (Turtle Rock)') and (state.has('Cane of Somaria') or state.has('Hookshot')))
    set_rule(world.get_entrance('Turtle Rock (Big Chest) (North)'), lambda state: state.has('Cane of Somaria') or state.has('Hookshot'))
    set_rule(world.get_entrance('Turtle Rock Big Key Door'), lambda state: state.can_collect('Big Key (Turtle Rock)'))
    set_rule(world.get_entrance('Turtle Rock Dark Room Staircase'), lambda state: state.can_collect('Small Key (Turtle Rock)', 3))
    set_rule(world.get_entrance('Turtle Rock (Dark Room) (North)'), lambda state: state.has('Cane of Somaria'))
    set_rule(world.get_entrance('Turtle Rock (Dark Room) (South)'), lambda state: state.has('Cane of Somaria'))
    set_rule(world.get_entrance('Turtle Rock (Trinexx)'), lambda state: state.can_collect('Small Key (Turtle Rock)', 4) and state.can_collect('Big Key (Turtle Rock)') and
                                                                        state.has('Cane of Somaria') and state.has('Fire Rod') and state.has('Ice Rod') and
                                                                        (state.has('Hammer') or state.has_beam_sword() or state.has('Bottle') or state.has('Half Magic') or state.has('Quarter Magic')))
    for location in ['[dungeon-D7-B1] Turtle Rock - Big Chest', 'Trinexx - Heart Container', '[dungeon-D7-B1] Turtle Rock - Roller Switch Room', '[dungeon-D7-B2] Turtle Rock - Eye Bridge Room [bottom left chest]',
                     '[dungeon-D7-B2] Turtle Rock - Eye Bridge Room [bottom right chest]', '[dungeon-D7-B2] Turtle Rock - Eye Bridge Room [top left chest]', '[dungeon-D7-B2] Turtle Rock - Eye Bridge Room [top right chest]']:  # ToDo Big Key can be elsewhere if we have an entrance shuffle
        forbid_item(world.get_location(location), 'Big Key (Turtle Rock)')

    set_rule(world.get_entrance('Dark Palace Bonk Wall'), lambda state: state.has('Bow'))
    set_rule(world.get_entrance('Dark Palace Hammer Peg Drop'), lambda state: state.has('Hammer'))
    set_rule(world.get_entrance('Dark Palace Bridge Room'), lambda state: state.can_collect('Small Key (Palace of Darkness)', 1))  # If we can reach any other small key door, we already have back door access to this area
    set_rule(world.get_entrance('Dark Palace Big Key Door'), lambda state: state.can_collect('Small Key (Palace of Darkness)', 6) and state.can_collect('Big Key (Palace of Darkness)') and state.has('Bow') and state.has('Hammer'))
    set_rule(world.get_entrance('Dark Palace Big Key Chest Staircase'), lambda state: state.can_collect('Small Key (Palace of Darkness)', 6) or (state.world.get_location('[dungeon-D1-1F] Dark Palace - Big Key Room').item is not None and (state.world.get_location('[dungeon-D1-1F] Dark Palace - Big Key Room').item.name in ['Small Key (Palace of Darkness)'])))
    set_rule(world.get_entrance('Dark Palace Spike Statue Room Door'), lambda state: state.can_collect('Small Key (Palace of Darkness)', 6) or (state.world.get_location('[dungeon-D1-1F] Dark Palace - Spike Statue Room').item is not None and (state.world.get_location('[dungeon-D1-1F] Dark Palace - Spike Statue Room').item.name in ['Small Key (Palace of Darkness)'])))
    set_rule(world.get_entrance('Dark Palace (North)'), lambda state: state.can_collect('Small Key (Palace of Darkness)', 4))
    set_rule(world.get_entrance('Dark Palace Maze Door'), lambda state: state.can_collect('Small Key (Palace of Darkness)', 6))
    set_rule(world.get_location('[dungeon-D1-1F] Dark Palace - Big Chest'), lambda state: state.can_collect('Big Key (Palace of Darkness)'))
    for location in ['[dungeon-D1-1F] Dark Palace - Big Chest', 'Helmasaur - Heart Container']:
        forbid_item(world.get_location(location), 'Big Key (Palace of Darkness)')

    # these key rules are conservative, you might be able to get away with more lenient rules
    set_rule(world.get_location('[dungeon-A2-1F] Ganons Tower - Torch'), lambda state: state.has_Boots())
    set_rule(world.get_entrance('Ganons Tower (Tile Room)'), lambda state: state.has('Cane of Somaria'))
    set_rule(world.get_entrance('Ganons Tower (Hookshot Room)'), lambda state: state.has('Hammer'))
    set_rule(world.get_entrance('Ganons Tower (Map Room)'), lambda state: state.can_collect('Small Key (Ganons Tower)', 3) or (state.world.get_location('[dungeon-A2-1F] Ganons Tower - Map Room').item is not None and state.world.get_location('[dungeon-A2-1F] Ganons Tower - Map Room').item.name == 'Small Key (Ganons Tower)'))
    set_rule(world.get_entrance('Ganons Tower (Double Switch Room)'), lambda state: state.can_collect('Small Key (Ganons Tower)', 2))
    set_rule(world.get_entrance('Ganons Tower (Firesnake Room)'), lambda state: state.can_collect('Small Key (Ganons Tower)', 3))
    set_rule(world.get_entrance('Ganons Tower (Tile Room) Key Door'), lambda state: state.can_collect('Small Key (Ganons Tower)', 3))  # possibly too pessimistic
    set_rule(world.get_location('[dungeon-A2-1F] Ganons Tower - Big Chest'), lambda state: state.can_collect('Big Key (Ganons Tower)'))
    set_rule(world.get_location('[dungeon-A2-B1] Ganons Tower - Armos Room [left chest]'), lambda state: state.has('Bow') or state.has_blunt_weapon())
    set_rule(world.get_location('[dungeon-A2-B1] Ganons Tower - Armos Room [bottom chest]'), lambda state: state.has('Bow') or state.has_blunt_weapon())
    set_rule(world.get_location('[dungeon-A2-B1] Ganons Tower - Armos Room [right chest]'), lambda state: state.has('Bow') or state.has_blunt_weapon())
    set_rule(world.get_entrance('Ganons Tower Big Key Door'), lambda state: state.can_collect('Big Key (Ganons Tower)'))
    set_rule(world.get_entrance('Ganons Tower Torch Rooms'), lambda state: state.has_fire_source())
    set_rule(world.get_entrance('Ganons Tower Moldorm Door'), lambda state: state.can_collect('Small Key (Ganons Tower)', 4))
    set_rule(world.get_entrance('Ganons Tower Moldorm Gap'), lambda state: state.has('Hookshot'))
    set_rule(world.get_entrance('Pyramid Hole'), lambda state: state.can_reach('East Dark World') and (state.has_sword() or state.has('Bottle') or state.has('Bug Catching Net')))  # some obscure hammer on pyramid soft lock potential scenarios
    for location in ['[dungeon-A2-1F] Ganons Tower - Big Chest', '[dungeon-A2-6F] Ganons Tower - Mini Helmasaur Room [left chest]', '[dungeon-A2-6F] Ganons Tower - Mini Helmasaur Room [right chest]',
                     '[dungeon-A2-6F] Ganons Tower - Room before Moldorm', '[dungeon-A2-6F] Ganons Tower - Moldorm Room']:
        forbid_item(world.get_location(location), 'Big Key (Ganons Tower)')

    set_rule(world.get_location('Ganon'), lambda state: state.has_beam_sword() and state.has_fire_source() and (state.has('Tempered Sword') or state.has('Golden Sword') or state.has('Silver Arrows') or state.has('Lamp') or state.has('Bottle') or state.has('Half Magic') or state.has('Quarter Magic')))  # need to light torch a sufficient amount of times


def no_glitches_rules(world):
    set_rule(world.get_entrance('Zoras River'), lambda state: state.has('Flippers') or state.can_lift_rocks())
    set_rule(world.get_entrance('Capacity Upgrade'), lambda state: state.has('Flippers'))  # can be fake flippered to
    set_rule(world.get_entrance('Hobo Bridge'), lambda state: state.has('Flippers'))
    add_rule(world.get_entrance('Ice Palace'), lambda state: state.has_Pearl() and state.has('Flippers'))
    set_rule(world.get_entrance('Dark Lake Hylia Drop (East)'), lambda state: state.has_Pearl() and state.has('Flippers'))
    set_rule(world.get_entrance('Dark Lake Hylia Teleporter'), lambda state: state.has_Pearl() and state.has('Flippers') and (state.has('Hammer') or state.can_lift_rocks()))
    set_rule(world.get_entrance('Dark Lake Hylia Ledge Drop'), lambda state: state.has('Flippers'))
    add_rule(world.get_entrance('Ganons Tower (Hookshot Room)'), lambda state: state.has('Hookshot'))
    set_rule(world.get_entrance('Death Mountain Climb Push Block Reverse'), lambda state: False)  # no glitches does not require block override
    set_rule(world.get_entrance('Death Mountain Climb Bomb Jump'), lambda state: False)

    # Light cones in standard depend on which world we actually are in, not which one the location would normally be
    # We add Lamp requirements only to those locations which lie in the dark world (or everything if open
    DW_Entrances = ['Bumper Cave (Bottom)', 'Dark Death Mountain Climb (Top)', 'Dark Death Mountain Climb (Bottom)', 'Hookshot Cave', 'Bumper Cave (Top)', 'Hookshot Cave Back Entrance', 'Dark Death Mountain Ledge (East)',
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
        if world.mode == 'open' or check_is_dark_world(world.get_region(region)):
            add_lamp_requirement(spot)

    add_conditional_lamp('Misery Mire (Vitreous)', 'Misery Mire (Entrance)', 'Entrance')
    add_conditional_lamp('Turtle Rock (Dark Room) (North)', 'Turtle Rock (Entrance)', 'Entrance')
    add_conditional_lamp('Turtle Rock (Dark Room) (South)', 'Turtle Rock (Entrance)', 'Entrance')
    add_conditional_lamp('Dark Palace Big Key Door', 'Dark Palace (Entrance)', 'Entrance')
    add_conditional_lamp('Dark Palace Maze Door', 'Dark Palace (Entrance)', 'Entrance')
    add_conditional_lamp('[dungeon-D1-B1] Dark Palace - Dark Room [left chest]', 'Dark Palace (Entrance)', 'Location')
    add_conditional_lamp('[dungeon-D1-B1] Dark Palace - Dark Room [right chest]', 'Dark Palace (Entrance)', 'Location')
    add_conditional_lamp('Agahnim 1', 'Agahnims Tower', 'Entrance')
    add_conditional_lamp('Old Mountain Man', 'Old Man Cave', 'Location')
    add_conditional_lamp('Old Man Cave Exit (East)', 'Old Man Cave', 'Entrance')
    add_conditional_lamp('Death Mountain Return Cave Exit (East)', 'Death Mountain Return Cave', 'Entrance')
    add_conditional_lamp('Death Mountain Return Cave Exit (West)', 'Death Mountain Return Cave', 'Entrance')
    add_conditional_lamp('Old Man House Front to Back', 'Old Man House', 'Entrance')
    add_conditional_lamp('Old Man House Back to Front', 'Old Man House', 'Entrance')
    add_conditional_lamp('[dungeon-L1-1F] Eastern Palace - Big Key Room', 'Eastern Palace', 'Location')
    add_conditional_lamp('Armos - Heart Container', 'Eastern Palace', 'Location')
    add_conditional_lamp('Armos - Pendant', 'Eastern Palace', 'Location')

    if world.state == 'open':
        # standard mode always has light cone in sewers and Hyrule Castle in Light world
        add_rule(world.get_location('[dungeon-C-B1] Escape - First B1 Room'), lambda state: state.has('Lamp'))


def open_rules(world):
    pass


def standard_rules(world):
    # easiest way to enforce key placement not relevant for open
    forbid_item(world.get_location('[dungeon-C-B1] Escape - Final Basement Room [left chest]'), 'Small Key (Escape)')
    forbid_item(world.get_location('[dungeon-C-B1] Escape - Final Basement Room [middle chest]'), 'Small Key (Escape)')
    forbid_item(world.get_location('[dungeon-C-B1] Escape - Final Basement Room [right chest]'), 'Small Key (Escape)')
    forbid_item(world.get_location('[dungeon-C-1F] Sanctuary'), 'Small Key (Escape)')
    add_rule(world.get_location('[dungeon-C-B1] Escape - Final Basement Room [left chest]'), lambda state: state.can_reach('Sewer Drop'))
    add_rule(world.get_location('[dungeon-C-B1] Escape - Final Basement Room [middle chest]'), lambda state: state.can_reach('Sewer Drop'))
    add_rule(world.get_location('[dungeon-C-B1] Escape - Final Basement Room [right chest]'), lambda state: state.can_reach('Sewer Drop'))
    add_rule(world.get_location('[dungeon-C-B1] Escape - First B1 Room'), lambda state: state.can_reach('Sewer Drop') or (state.world.get_location('[dungeon-C-B1] Escape - First B1 Room').item is not None and state.world.get_location('[dungeon-C-B1] Escape - First B1 Room').item.name in ['Small Key (Escape)']))  # you could skip this chest and be unable to go back until you can drop into escape


def set_blacksmith_rules(world):
    blacksmith_entrance = world.get_region('Blacksmiths Hut').entrances[0]
    # some special handling if shuffled as we cannot use connected caves to take the smith up to death mountain
    if blacksmith_entrance.name == 'Hookshot Fairy':
        add_rule(world.get_location('Blacksmiths'), lambda state: state.has('Ocarina') and (state.has('Hammer') or state.has('Hookshot')))


def set_big_bomb_rules(world):
    # this is a mess and needs to be worked out properly ToDo
    # very broad restrictions so can always get there
    set_rule(world.get_entrance('Pyramid Fairy'), lambda state: state.has_Mirror() and state.has_Pearl() and state.can_reach('Big Bomb Shop', 'Region') and state.can_collect('Crystal 5') and state.can_collect('Crystal 6') and
             state.has('Ocarina') and state.has('Hammer') and state.can_lift_rocks())
