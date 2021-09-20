from BaseClasses import MultiWorld

def create_regions(world: MultiWorld, player: int):
    from . import create_region

    world.regions += [
        create_region(world, player, 'Menu', ['Start Game']),
        create_region(world, player, 'Tutorial', ['Tutorial > Lake desolation']),
        create_region(world, player, 'Lake desolation', ['Lake desolation > Lower lake desolation', 'Lake desolation > Upper lake desolation', 'Lake desolation > Sealed Caves (Xarion)']),
        create_region(world, player, 'Upper lake desolation', ['Upper lake desolation > Lake desolation', 'Upper lake desolation > Lower lake desolation']),
        create_region(world, player, 'Lower lake desolation', ['Lower lake desolation > Lake desolation', 'Lower lake desolation > Libary']),
        create_region(world, player, 'Libary', ['Libary > Lower lake desolation', 'Libary > Libary top', 'Libary > Varndagroth tower left']),
        create_region(world, player, 'Libary top', ['Libary top > Libary']),
        create_region(world, player, 'Varndagroth tower left', ['Varndagroth tower left > Libary', 'Varndagroth tower left > Varndagroth tower right (upper)', 'Varndagroth tower left > Varndagroth tower right (lower)', 'Varndagroth tower left > Sealed Caves (Sirens)', 'Varndagroth tower left > Refugee Camp']),
        create_region(world, player, 'Varndagroth tower right (upper)', ['Varndagroth tower right (upper) > Varndagroth tower left', 'Varndagroth tower right (upper) > Varndagroth tower right (elevator)']),
        create_region(world, player, 'Varndagroth tower right (lower)', ['Varndagroth tower right (lower) > Varndagroth tower left', 'Varndagroth tower right (lower) > Varndagroth tower right (elevator)', 'Varndagroth tower right (lower) > Sealed Caves (Sirens)', 'Varndagroth tower right (lower) > Militairy Fortress']),
        create_region(world, player, 'Varndagroth tower right (elevator)', ['Varndagroth tower right (elevator) > Varndagroth tower right (upper)', 'Varndagroth tower right (elevator) > Varndagroth tower right (lower)']),
        create_region(world, player, 'Sealed Caves (Sirens)', ['Sealed Caves (Sirens) > Varndagroth tower left', 'Sealed Caves (Sirens) > Varndagroth tower right (lower)']),
        create_region(world, player, 'Militairy Fortress', ['Militairy Fortress > Varndagroth tower right (lower)', 'Militairy Fortress > The lab']),
        create_region(world, player, 'The lab', ['The lab > Militairy Fortress', 'The lab > The lab (power off)']),
        create_region(world, player, 'The lab (power off)', ['The lab (power off) > The lab', 'The lab (power off) > The lab (upper)']),
        create_region(world, player, 'The lab (upper)', ['The lab (upper) > The lab (power off)', 'The lab (upper) > Emperors tower', 'The lab (upper) > Ancient Pyramid (left)']),
        create_region(world, player, 'Emperors tower', ['Emperors tower > The lab (upper)']),
        create_region(world, player, 'Sealed Caves (Xarion)', ['Sealed Caves (Xarion) > Lake desolation']),
        create_region(world, player, 'Refugee Camp', ['Refugee Camp > Forest', 'Refugee Camp > Libary']),
        create_region(world, player, 'Forest', ['Forest > Refugee Camp', 'Forest > Upper Lake Sirine', 'Forest > Caves of Banishment (Sirens)', 'Forest > Caste Ramparts']),
        create_region(world, player, 'Upper Lake Sirine', ['Upper Lake Sirine > Forest', 'Upper Lake Sirine > Lower Lake Sirine']),
        create_region(world, player, 'Lower Lake Sirine', ['Lower Lake Sirine > Upper Lake Sirine', 'Lower Lake Sirine > Caves of Banishment (Maw)']),
        create_region(world, player, 'Caves of Banishment (Maw)', ['Caves of Banishment (Maw) > Lower Lake Sirine', 'Caves of Banishment (Maw) > Caves of Banishment (Sirens)']),
        create_region(world, player, 'Caves of Banishment (Sirens)', ['Caves of Banishment (Sirens) > Forest']),
        create_region(world, player, 'Caste Ramparts', ['Caste Ramparts > Forest', 'Caste Ramparts > Caste Keep']),
        create_region(world, player, 'Caste Keep', ['Caste Keep > Caste Ramparts', 'Caste Keep > Royal towers (lower)']),
        create_region(world, player, 'Royal towers (lower)', ['Royal towers (lower) > Caste Keep', 'Royal towers (lower) > Royal towers']),
        create_region(world, player, 'Royal towers', ['Royal towers > Royal towers (lower)', 'Royal towers > Royal towers (upper)']),
        create_region(world, player, 'Royal towers (upper)', ['Royal towers (upper) > Royal towers']),
        create_region(world, player, 'Ancient Pyramid (left)', ['Ancient Pyramid (left) > The lab (upper)', 'Ancient Pyramid (left) > Ancient Pyramid (right)']),
        create_region(world, player, 'Ancient Pyramid (right)', ['Ancient Pyramid (right) > Ancient Pyramid (left)']),
    ]

    world.get_entrance('Start Game', player).connect(world.get_region('Tutorial', player))

    connectEntrance(world, player, 'Tutorial > Lake desolation')

    connectEntrance(world, player, 'Lake desolation > Lower lake desolation', lambda state: state._timespinner_has_timestop(world, player or state.has('Talaria Attachment', player))) #TODO | R.GateKittyBoss | R.GateLeftLibrary)
    connectEntrance(world, player, 'Lake desolation > Upper lake desolation', lambda state: state._timespinner_has_fire(world, player) and state.can_reach('Upper Lake Sirine', 'Region', player))
    connectEntrance(world, player, 'Lake desolation > Sealed Caves (Xarion)', lambda state: state._timespinner_has_keycard_A(world, player) and state._timespinner_has_doublejump(world, player))

    connectEntrance(world, player, 'Upper lake desolation > Lake desolation')
    connectEntrance(world, player, 'Upper lake desolation > Lower lake desolation') 

    connectEntrance(world, player, 'Lower lake desolation > Lake desolation') 
    connectEntrance(world, player, 'Lower lake desolation > Libary') 

    connectEntrance(world, player, 'Libary > Lower lake desolation') 
    connectEntrance(world, player, 'Libary > Libary top', lambda state: state._timespinner_has_doublejump(world, player) or state.has('Talaria Attachment', player)) 
    connectEntrance(world, player, 'Libary > Varndagroth tower left', lambda state: state._timespinner_has_keycard_C(world, player))

    connectEntrance(world, player, 'Libary top > Libary')

    connectEntrance(world, player, 'Varndagroth tower left > Libary')
    connectEntrance(world, player, 'Varndagroth tower left > Varndagroth tower right (upper)', lambda state: state._timespinner_has_keycard_C(world, player))
    connectEntrance(world, player, 'Varndagroth tower left > Varndagroth tower right (lower)', lambda state: state._timespinner_has_keycard_B(world, player))
    connectEntrance(world, player, 'Varndagroth tower left > Sealed Caves (Sirens)', lambda state: state._timespinner_has_keycard_B(world, player) and state.has('Elevator Keycard', player))
    connectEntrance(world, player, 'Varndagroth tower left > Refugee Camp', lambda state: state.has('Timespinner Wheel', player) and state.has('Timespinner Spindle', player))

    connectEntrance(world, player, 'Varndagroth tower right (upper) > Varndagroth tower left')
    connectEntrance(world, player, 'Varndagroth tower right (upper) > Varndagroth tower right (elevator)', lambda state: state.has('Elevator Keycard', player))

    connectEntrance(world, player, 'Varndagroth tower right (elevator) > Varndagroth tower right (upper)')
    connectEntrance(world, player, 'Varndagroth tower right (elevator) > Varndagroth tower right (lower)')

    connectEntrance(world, player, 'Varndagroth tower right (lower) > Varndagroth tower left')
    connectEntrance(world, player, 'Varndagroth tower right (lower) > Varndagroth tower right (elevator)', lambda state: state.has('Elevator Keycard', player))
    connectEntrance(world, player, 'Varndagroth tower right (lower) > Sealed Caves (Sirens)', lambda state: state._timespinner_has_keycard_B(world, player) and state.has('Elevator Keycard', player))
    connectEntrance(world, player, 'Varndagroth tower right (lower) > Militairy Fortress', lambda state: state._timespinner_can_kill_all_3_bosses(world, player))

    connectEntrance(world, player, 'Sealed Caves (Sirens) > Varndagroth tower left', lambda state: state.has('Elevator Keycard', player))
    connectEntrance(world, player, 'Sealed Caves (Sirens) > Varndagroth tower right (lower)', lambda state: state.has('Elevator Keycard', player))

    connectEntrance(world, player, 'Militairy Fortress > Varndagroth tower right (lower)', lambda state: state._timespinner_can_kill_all_3_bosses(world, player))
    connectEntrance(world, player, 'Militairy Fortress > The lab', lambda state: state._timespinner_has_keycard_B(world, player) and state._timespinner_has_doublejump(world, player))

    connectEntrance(world, player, 'The lab > Militairy Fortress')
    connectEntrance(world, player, 'The lab > The lab (power off)', lambda state: state._timespinner_has_doublejump_of_npc(player, world))

    connectEntrance(world, player, 'The lab (power off) > The lab')
    connectEntrance(world, player, 'The lab (power off) > The lab (upper)', lambda state: state._timespinner_has_forwarddash_doublejump(world, player))

    connectEntrance(world, player, 'The lab (upper) > The lab (power off)')
    connectEntrance(world, player, 'The lab (upper) > Emperors tower', lambda state: state._timespinner_has_forwarddash_doublejump(world, player))
    connectEntrance(world, player, 'The lab (upper) > Ancient Pyramid (left)', lambda state: state._timespinner_can_kill_nightmare(world, player))

    connectEntrance(world, player, 'Emperors tower > The lab (upper)')

    connectEntrance(world, player, 'Sealed Caves (Xarion) > Lake desolation')

    connectEntrance(world, player, 'Refugee Camp > Forest')
    connectEntrance(world, player, 'Refugee Camp > Libary')

    connectEntrance(world, player, 'Forest > Refugee Camp')
    connectEntrance(world, player, 'Forest > Upper Lake Sirine', lambda state: state.has_any(['Timespinner Wheel', 'Talaria Attachment'], player) or state._timespinner_has_doublejump(world, player)) #to clear the moth R.TimeStop | R.Swimming //to clear bird height
    connectEntrance(world, player, 'Forest > Caves of Banishment (Sirens)')
    connectEntrance(world, player, 'Forest > Caste Ramparts')

    connectEntrance(world, player, 'Upper Lake Sirine > Forest')
    connectEntrance(world, player, 'Upper Lake Sirine > Lower Lake Sirine', lambda state: state.has('Water Mask', player))

    connectEntrance(world, player, 'Lower Lake Sirine > Upper Lake Sirine')
    connectEntrance(world, player, 'Lower Lake Sirine > Caves of Banishment (Maw)')

    connectEntrance(world, player, 'Caves of Banishment (Maw) > Lower Lake Sirine', lambda state: state.has('Water Mask', player))
    connectEntrance(world, player, 'Caves of Banishment (Maw) > Caves of Banishment (Sirens)')

    connectEntrance(world, player, 'Caves of Banishment (Sirens) > Forest')

    connectEntrance(world, player, 'Caste Ramparts > Forest')
    connectEntrance(world, player, 'Caste Ramparts > Caste Keep')

    connectEntrance(world, player, 'Caste Keep > Caste Ramparts')
    connectEntrance(world, player, 'Caste Keep > Royal towers (lower)', lambda state: state._timespinner_has_doublejump(world, player))

    connectEntrance(world, player, 'Royal towers (lower) > Caste Keep')
    connectEntrance(world, player, 'Royal towers (lower) > Royal towers', lambda state: state.has('Timespinner Wheel', player) or state._timespinner_has_forwarddash_doublejump(world, player))

    connectEntrance(world, player, 'Royal towers > Royal towers (lower)')
    connectEntrance(world, player, 'Royal towers > Royal towers (upper)', lambda state: state._timespinner_has_doublejump(world, player))

    connectEntrance(world, player, 'Royal towers (upper) > Royal towers')

    connectEntrance(world, player, 'Ancient Pyramid (left) > The lab (upper)')
    connectEntrance(world, player, 'Ancient Pyramid (left) > Ancient Pyramid (right)', lambda state: state._timespinner_has_upwarddash(world, player))

    connectEntrance(world, player, 'Ancient Pyramid (right) > Ancient Pyramid (left)')

def connectEntrance(world: MultiWorld, player: int, name: str, rule=None):
    entrance = world.get_entrance(name, player)

    if rule:
        entrance.access_rule = rule
    
    target = name.partition(' > ')[2]

    entrance.connect(world.get_region(target, player))



    
