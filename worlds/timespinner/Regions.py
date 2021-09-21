from BaseClasses import MultiWorld
from .Options import is_option_enabled

def create_regions(world: MultiWorld, player: int):
    from . import create_region

    world.regions += [
        create_region(world, player, 'Menu', [
            'Start Game']),
        create_region(world, player, 'Tutorial', [
            'Tutorial > Starting Region']),
        create_region(world, player, 'Lake desolation', [
            'Lake desolation > Lower lake desolation', 
            'Lake desolation > Upper lake desolation', 
            'Lake desolation > Sealed Caves (Xarion)', 
            'Lake desolation > Space time continuum']),
        create_region(world, player, 'Upper lake desolation', [
            'Upper lake desolation > Lake desolation', 
            'Upper lake desolation > Lower lake desolation']),
        create_region(world, player, 'Lower lake desolation', [
            'Lower lake desolation > Lake desolation', 
            'Lower lake desolation > Libary', 
            'Lower lake desolation > Space time continuum']),
        create_region(world, player, 'Libary', [
            'Libary > Lower lake desolation', 
            'Libary > Libary top', 
            'Libary > Varndagroth tower left', 
            'Libary > Space time continuum']),
        create_region(world, player, 'Libary top', [
            'Libary top > Libary']),
        create_region(world, player, 'Varndagroth tower left', [
            'Varndagroth tower left > Libary', 
            'Varndagroth tower left > Varndagroth tower right (upper)', 
            'Varndagroth tower left > Varndagroth tower right (lower)',
            'Varndagroth tower left > Sealed Caves (Sirens)',
            'Varndagroth tower left > Refugee Camp']),
        create_region(world, player, 'Varndagroth tower right (upper)', [
            'Varndagroth tower right (upper) > Varndagroth tower left', 
            'Varndagroth tower right (upper) > Varndagroth tower right (elevator)']),
        create_region(world, player, 'Varndagroth tower right (lower)', [
            'Varndagroth tower right (lower) > Varndagroth tower left', 
            'Varndagroth tower right (lower) > Varndagroth tower right (elevator)', 
            'Varndagroth tower right (lower) > Sealed Caves (Sirens)', 
            'Varndagroth tower right (lower) > Militairy Fortress', 
            'Varndagroth tower right (lower) > Space time continuum']),
        create_region(world, player, 'Varndagroth tower right (elevator)', [
            'Varndagroth tower right (elevator) > Varndagroth tower right (upper)', 
            'Varndagroth tower right (elevator) > Varndagroth tower right (lower)']),
        create_region(world, player, 'Sealed Caves (Sirens)', [
            'Sealed Caves (Sirens) > Varndagroth tower left', 
            'Sealed Caves (Sirens) > Varndagroth tower right (lower)', 
            'Sealed Caves (Sirens) > Space time continuum']),
        create_region(world, player, 'Militairy Fortress', [
            'Militairy Fortress > Varndagroth tower right (lower)', 
            'Militairy Fortress > The lab']),
        create_region(world, player, 'The lab', [
            'The lab > Militairy Fortress', 
            'The lab > The lab (power off)']),
        create_region(world, player, 'The lab (power off)', [
            'The lab (power off) > The lab', 
            'The lab (power off) > The lab (upper)']),
        create_region(world, player, 'The lab (upper)', [
            'The lab (upper) > The lab (power off)', 
            'The lab (upper) > Emperors tower', 
            'The lab (upper) > Ancient Pyramid (left)']),
        create_region(world, player, 'Emperors tower', [
            'Emperors tower > The lab (upper)']),
        create_region(world, player, 'Sealed Caves (Xarion)', [
            'Sealed Caves (Xarion) > Lake desolation', 
            'Sealed Caves (Xarion) > Space time continuum']),
        create_region(world, player, 'Refugee Camp', [
            'Refugee Camp > Forest', 
            'Refugee Camp > Libary', 
            'Refugee Camp > Space time continuum']),
        create_region(world, player, 'Forest', [
            'Forest > Refugee Camp', 
            'Forest > Left Side forest Caves', 
            'Forest > Caves of Banishment (Sirens)', 
            'Forest > Caste Ramparts']),
        create_region(world, player, 'Left Side forest Caves', [
            'Left Side forest Caves > Forest', 
            'Left Side forest Caves > Upper Lake Sirine', 
            'Left Side forest Caves > Lower Lake Sirine', 
            'Left Side forest Caves > Space time continuum']),
        create_region(world, player, 'Upper Lake Sirine', [
            'Upper Lake Sirine > Left Side forest Caves', 
            'Upper Lake Sirine > Lower Lake Sirine']),
        create_region(world, player, 'Lower Lake Sirine', [
            'Lower Lake Sirine > Upper Lake Sirine', 
            'Lower Lake Sirine > Left Side forest Caves', 
            'Lower Lake Sirine > Caves of Banishment (upper)']),
        create_region(world, player, 'Caves of Banishment (upper)', [
            'Caves of Banishment (upper) > Upper Lake Sirine', 
            'Caves of Banishment (upper) > Caves of Banishment (Maw)', 
            'Caves of Banishment (upper) > Space time continuum']),
        create_region(world, player, 'Caves of Banishment (Maw)', [
            'Caves of Banishment (Maw) > Caves of Banishment (upper)', 
            'Caves of Banishment (Maw) > Caves of Banishment (Sirens)', 'Caves of Banishment (Maw) > Space time continuum']),
        create_region(world, player, 'Caves of Banishment (Sirens)', [
            'Caves of Banishment (Sirens) > Forest']),
        create_region(world, player, 'Caste Ramparts', [
            'Caste Ramparts > Forest', 
            'Caste Ramparts > Caste Keep', 
            'Caste Ramparts > Space time continuum']),
        create_region(world, player, 'Caste Keep', [
            'Caste Keep > Caste Ramparts', 
            'Caste Keep > Royal towers (lower)', 
            'Caste Keep > Space time continuum']),
        create_region(world, player, 'Royal towers (lower)', [
            'Royal towers (lower) > Caste Keep', 
            'Royal towers (lower) > Royal towers', 
            'Royal towers (lower) > Space time continuum']),
        create_region(world, player, 'Royal towers', [
            'Royal towers > Royal towers (lower)', 
            'Royal towers > Royal towers (upper)']),
        create_region(world, player, 'Royal towers (upper)', [
            'Royal towers (upper) > Royal towers']),
        create_region(world, player, 'Ancient Pyramid (left)', [
            'Ancient Pyramid (left) > The lab (upper)', 
            'Ancient Pyramid (left) > Ancient Pyramid (right)']),
        create_region(world, player, 'Ancient Pyramid (right)', [
            'Ancient Pyramid (right) > Ancient Pyramid (left)']),
        create_region(world, player, 'Space time continuum', [
            'Space time continuum > Starting Region', 
            'Space time continuum > Lake desolation',
            'Space time continuum > Lower lake desolation',
            'Space time continuum > Libary',
            'Space time continuum > Varndagroth tower right (lower)',
            'Space time continuum > Sealed Caves (Xarion)',
            'Space time continuum > Sealed Caves (Sirens)',
            'Space time continuum > Left Side forest Caves',
            'Space time continuum > Refugee Camp',
            'Space time continuum > Caste Ramparts',
            'Space time continuum > Caste Keep',
            'Space time continuum > Royal towers (lower)',
            'Space time continuum > Caves of Banishment (Maw)',
            'Space time continuum > Caves of Banishment (upper)'])
    ]

    world.get_entrance('Start Game', player).connect(world.get_region('Tutorial', player))

    if is_option_enabled(world, player, "Inverted"):
        starting_region = 'Refugee Camp'
    else:
        starting_region = 'Lake desolation'

    world.get_entrance('Tutorial > Starting Region', player).connect(world.get_region(starting_region, player))
    world.get_entrance('Space time continuum > Starting Region', player).connect(world.get_region(starting_region, player)) 

    connectEntrance(world, player, 'Lake desolation > Lower lake desolation', lambda state: state._timespinner_has_timestop(world, player or state.has('Talaria Attachment', player))) #TODO | R.GateKittyBoss | R.GateLeftLibrary)
    connectEntrance(world, player, 'Lake desolation > Upper lake desolation', lambda state: state._timespinner_has_fire(world, player) and state.can_reach('Upper Lake Sirine', 'Region', player))
    connectEntrance(world, player, 'Lake desolation > Sealed Caves (Xarion)', lambda state: state._timespinner_has_keycard_A(world, player) and state._timespinner_has_doublejump(world, player))
    connectEntrance(world, player, 'Lake desolation > Space time continuum', lambda state: state.has('Twin Pyramid Key', player))

    connectEntrance(world, player, 'Upper lake desolation > Lake desolation')
    connectEntrance(world, player, 'Upper lake desolation > Lower lake desolation') 

    connectEntrance(world, player, 'Lower lake desolation > Lake desolation') 
    connectEntrance(world, player, 'Lower lake desolation > Libary') 
    connectEntrance(world, player, 'Lower lake desolation > Space time continuum', lambda state: state.has('Twin Pyramid Key', player))

    connectEntrance(world, player, 'Libary > Lower lake desolation') 
    connectEntrance(world, player, 'Libary > Libary top', lambda state: state._timespinner_has_doublejump(world, player) or state.has('Talaria Attachment', player)) 
    connectEntrance(world, player, 'Libary > Varndagroth tower left', lambda state: state._timespinner_has_keycard_C(world, player))
    connectEntrance(world, player, 'Libary > Space time continuum', lambda state: state.has('Twin Pyramid Key', player))

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
    connectEntrance(world, player, 'Varndagroth tower right (lower) > Space time continuum', lambda state: state.has('Twin Pyramid Key', player))

    connectEntrance(world, player, 'Sealed Caves (Sirens) > Varndagroth tower left', lambda state: state.has('Elevator Keycard', player))
    connectEntrance(world, player, 'Sealed Caves (Sirens) > Varndagroth tower right (lower)', lambda state: state.has('Elevator Keycard', player))
    connectEntrance(world, player, 'Sealed Caves (Sirens) > Space time continuum', lambda state: state.has('Twin Pyramid Key', player))

    connectEntrance(world, player, 'Militairy Fortress > Varndagroth tower right (lower)', lambda state: state._timespinner_can_kill_all_3_bosses(world, player))
    connectEntrance(world, player, 'Militairy Fortress > The lab', lambda state: state._timespinner_has_keycard_B(world, player) and state._timespinner_has_doublejump(world, player))

    connectEntrance(world, player, 'The lab > Militairy Fortress')
    connectEntrance(world, player, 'The lab > The lab (power off)', lambda state: state._timespinner_has_doublejump_of_npc(world, player))

    connectEntrance(world, player, 'The lab (power off) > The lab')
    connectEntrance(world, player, 'The lab (power off) > The lab (upper)', lambda state: state._timespinner_has_forwarddash_doublejump(world, player))

    connectEntrance(world, player, 'The lab (upper) > The lab (power off)')
    connectEntrance(world, player, 'The lab (upper) > Emperors tower', lambda state: state._timespinner_has_forwarddash_doublejump(world, player))
    connectEntrance(world, player, 'The lab (upper) > Ancient Pyramid (left)', lambda state: state.has_all(['Timespinner Wheel', 'Timespinner Spindle', 'Timespinner Gear 1', 'Timespinner Gear 2', 'Timespinner Gear 3'], player))

    connectEntrance(world, player, 'Emperors tower > The lab (upper)')

    connectEntrance(world, player, 'Sealed Caves (Xarion) > Lake desolation')
    connectEntrance(world, player, 'Sealed Caves (Xarion) > Space time continuum', lambda state: state.has('Twin Pyramid Key', player))

    connectEntrance(world, player, 'Refugee Camp > Forest')
    connectEntrance(world, player, 'Refugee Camp > Libary', lambda state: is_option_enabled(world, player, "Inverted"))
    connectEntrance(world, player, 'Refugee Camp > Space time continuum', lambda state: state.has('Twin Pyramid Key', player))

    connectEntrance(world, player, 'Forest > Refugee Camp')
    connectEntrance(world, player, 'Forest > Left Side forest Caves', lambda state: state.has('Talaria Attachment', player) or state._timespinner_has_timestop(world, player))
    connectEntrance(world, player, 'Forest > Caves of Banishment (Sirens)')
    connectEntrance(world, player, 'Forest > Caste Ramparts')

    connectEntrance(world, player, 'Left Side forest Caves > Forest')
    connectEntrance(world, player, 'Left Side forest Caves > Upper Lake Sirine', lambda state: state._timespinner_has_timestop(world, player))
    connectEntrance(world, player, 'Left Side forest Caves > Lower Lake Sirine', lambda state: state.has('Water Mask', player))
    connectEntrance(world, player, 'Left Side forest Caves > Space time continuum', lambda state: state.has('Twin Pyramid Key', player))

    connectEntrance(world, player, 'Upper Lake Sirine > Left Side forest Caves')
    connectEntrance(world, player, 'Upper Lake Sirine > Lower Lake Sirine', lambda state: state.has('Water Mask', player))

    connectEntrance(world, player, 'Lower Lake Sirine > Upper Lake Sirine')
    connectEntrance(world, player, 'Lower Lake Sirine > Left Side forest Caves')
    connectEntrance(world, player, 'Lower Lake Sirine > Caves of Banishment (upper)')

    connectEntrance(world, player, 'Caves of Banishment (upper) > Upper Lake Sirine', lambda state: state.has('Water Mask', player))
    connectEntrance(world, player, 'Caves of Banishment (upper) > Caves of Banishment (Maw)')
    connectEntrance(world, player, 'Caves of Banishment (upper) > Space time continuum', lambda state: state.has('Twin Pyramid Key', player))

    connectEntrance(world, player, 'Caves of Banishment (Maw) > Caves of Banishment (upper)', lambda state: state._timespinner_has_forwarddash_doublejump(world, player))
    connectEntrance(world, player, 'Caves of Banishment (Maw) > Caves of Banishment (Sirens)')
    connectEntrance(world, player, 'Caves of Banishment (Maw) > Space time continuum', lambda state: state.has('Twin Pyramid Key', player))

    connectEntrance(world, player, 'Caves of Banishment (Sirens) > Forest')

    connectEntrance(world, player, 'Caste Ramparts > Forest')
    connectEntrance(world, player, 'Caste Ramparts > Caste Keep')
    connectEntrance(world, player, 'Caste Ramparts > Space time continuum', lambda state: state.has('Twin Pyramid Key', player))

    connectEntrance(world, player, 'Caste Keep > Caste Ramparts')
    connectEntrance(world, player, 'Caste Keep > Royal towers (lower)', lambda state: state._timespinner_has_doublejump(world, player))
    connectEntrance(world, player, 'Caste Keep > Space time continuum', lambda state: state.has('Twin Pyramid Key', player))

    connectEntrance(world, player, 'Royal towers (lower) > Caste Keep')
    connectEntrance(world, player, 'Royal towers (lower) > Royal towers', lambda state: state.has('Timespinner Wheel', player) or state._timespinner_has_forwarddash_doublejump(world, player))
    connectEntrance(world, player, 'Royal towers (lower) > Space time continuum', lambda state: state.has('Twin Pyramid Key', player))

    connectEntrance(world, player, 'Royal towers > Royal towers (lower)')
    connectEntrance(world, player, 'Royal towers > Royal towers (upper)', lambda state: state._timespinner_has_doublejump(world, player))

    connectEntrance(world, player, 'Royal towers (upper) > Royal towers')

    connectEntrance(world, player, 'Ancient Pyramid (left) > The lab (upper)')
    connectEntrance(world, player, 'Ancient Pyramid (left) > Ancient Pyramid (right)', lambda state: state._timespinner_has_upwarddash(world, player))

    connectEntrance(world, player, 'Ancient Pyramid (right) > Ancient Pyramid (left)')

    connectEntrance(world, player, 'Space time continuum > Lake desolation', lambda state: world.timespinner_pyramid_keys_unlock == "GateLakeDesolation")
    connectEntrance(world, player, 'Space time continuum > Lower lake desolation', lambda state: world.timespinner_pyramid_keys_unlock == "GateKittyBoss")
    connectEntrance(world, player, 'Space time continuum > Libary', lambda state: world.timespinner_pyramid_keys_unlock == "GateLeftLibrary")
    connectEntrance(world, player, 'Space time continuum > Varndagroth tower right (lower)', lambda state: world.timespinner_pyramid_keys_unlock == "GateMilitairyGate")
    connectEntrance(world, player, 'Space time continuum > Sealed Caves (Xarion)', lambda state: world.timespinner_pyramid_keys_unlock == "GateSealedCaves")
    connectEntrance(world, player, 'Space time continuum > Sealed Caves (Sirens)', lambda state: world.timespinner_pyramid_keys_unlock == "GateSealedSirensCave")
    connectEntrance(world, player, 'Space time continuum > Left Side forest Caves', lambda state: world.timespinner_pyramid_keys_unlock == "GateLakeSirineRight")
    connectEntrance(world, player, 'Space time continuum > Refugee Camp', lambda state: world.timespinner_pyramid_keys_unlock == "GateAccessToPast")
    connectEntrance(world, player, 'Space time continuum > Caste Ramparts', lambda state: world.timespinner_pyramid_keys_unlock == "GateCastleRamparts")
    connectEntrance(world, player, 'Space time continuum > Caste Keep', lambda state: world.timespinner_pyramid_keys_unlock == "GateCastleKeep")
    connectEntrance(world, player, 'Space time continuum > Royal towers (lower)', lambda state: world.timespinner_pyramid_keys_unlock == "GateRoyalTowers")
    connectEntrance(world, player, 'Space time continuum > Caves of Banishment (Maw)', lambda state: world.timespinner_pyramid_keys_unlock == "GateMaw")
    connectEntrance(world, player, 'Space time continuum > Caves of Banishment (upper)', lambda state: world.timespinner_pyramid_keys_unlock == "GateCavesOfBanishment")

def connectEntrance(world: MultiWorld, player: int, name: str, rule=None):
    entrance = world.get_entrance(name, player)

    if rule:
        entrance.access_rule = rule
    
    target = name.partition(' > ')[2]

    entrance.connect(world.get_region(target, player))