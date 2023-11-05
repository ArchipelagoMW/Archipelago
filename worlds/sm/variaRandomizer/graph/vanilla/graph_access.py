from ...graph.graph import AccessPoint
from ...utils.parameters import Settings
from ...rom.rom_patches import RomPatches
from ...logic.smbool import SMBool
from ...logic.helpers import Bosses
from ...logic.cache import Cache

# all access points and traverse functions
accessPoints = [
    ### Ceres Station
    AccessPoint('Ceres', 'Ceres', {
        'Landing Site': lambda sm: SMBool(True)
    }, internal=True,
       start={'spawn': 0xfffe, 'doors':[0x32], 'patches':[RomPatches.BlueBrinstarBlueDoor], 'solveArea': "Crateria Landing Site"}),
    ### Crateria and Blue Brinstar
    AccessPoint('Landing Site', 'Crateria', {
        'Lower Mushrooms Left': Cache.ldeco(lambda sm: sm.wand(sm.canPassTerminatorBombWall(),
                                                               sm.canPassCrateriaGreenPirates())),
        'Keyhunter Room Bottom': Cache.ldeco(lambda sm: sm.traverse('LandingSiteRight')),
        'Blue Brinstar Elevator Bottom': lambda sm: SMBool(True)
    }, internal=True,
       start={'spawn': 0x0000, 'doors':[0x32], 'patches':[RomPatches.BlueBrinstarBlueDoor], 'solveArea': "Crateria Landing Site"}),
    AccessPoint('Blue Brinstar Elevator Bottom', 'Crateria', {
        'Morph Ball Room Left': lambda sm: sm.canUsePowerBombs(),
        'Landing Site': lambda sm: SMBool(True)
    }, internal=True),
    AccessPoint('Gauntlet Top', 'Crateria', {
        'Green Pirates Shaft Bottom Right': Cache.ldeco(lambda sm: sm.wand(sm.haveItem('Morph'), sm.canPassCrateriaGreenPirates()))
    }, internal=True,
       start={'spawn': 0x0006, 'solveArea': "Crateria Gauntlet", 'save':"Save_Gauntlet", 'forcedEarlyMorph':True}),
    AccessPoint('Lower Mushrooms Left', 'Crateria', {
        'Landing Site': Cache.ldeco(lambda sm: sm.wand(sm.canPassTerminatorBombWall(False),
                                                       sm.canPassCrateriaGreenPirates())),
        'Green Pirates Shaft Bottom Right': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0x9969, "area": 0x0, 'songs':[0x997a]},
       exitInfo = {'DoorPtr':0x8c22, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x36, 'SamusY':0x88, 'song': 0x9},
       dotOrientation = 'nw'),
    AccessPoint('Green Pirates Shaft Bottom Right', 'Crateria', {
        'Lower Mushrooms Left': lambda sm: SMBool(True)
    }, traverse = Cache.ldeco(lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.AreaRandoMoreBlueDoors),
                                                sm.traverse('GreenPiratesShaftBottomRight'))),
       roomInfo = {'RoomPtr':0x99bd, "area": 0x0, 'songs':[0x99ce]},
       exitInfo = {'DoorPtr':0x8c52, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xcc, 'SamusY':0x688, 'song': 0x9},
       dotOrientation = 'e'),
    AccessPoint('Moat Right', 'Crateria', {
        'Moat Left': lambda sm: sm.canPassMoatReverse()
    }, roomInfo = {'RoomPtr':0x95ff, "area": 0x0, 'songs':[0x9610]},
       exitInfo = {'DoorPtr':0x8aea, 'direction': 0x4, "cap": (0x1, 0x46), "bitFlag": 0x0,
                   "screen": (0x0, 0x4), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x1cf, 'SamusY':0x88, 'song': 0xc},
       dotOrientation = 'ne'),
    AccessPoint('Moat Left', 'Crateria', {
        'Keyhunter Room Bottom': lambda sm: SMBool(True),
        'Moat Right': lambda sm: sm.canPassMoatFromMoat()
    }, internal=True),
    AccessPoint('Keyhunter Room Bottom', 'Crateria', {
        'Moat Left': Cache.ldeco(lambda sm: sm.traverse('KihunterRight')),
        'Moat Right': Cache.ldeco(lambda sm: sm.wand(sm.traverse('KihunterRight'), sm.canPassMoat())),
        'Landing Site': lambda sm: SMBool(True)
    }, traverse = Cache.ldeco(lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.AreaRandoMoreBlueDoors),
                                                sm.traverse('KihunterBottom'))),
       roomInfo = { 'RoomPtr':0x948c, "area": 0x0, 'songs':[0x949d] },
       exitInfo = {'DoorPtr':0x8a42, 'direction': 0x6, "cap": (0x6, 0x2), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x14c, 'SamusY':0x2b8, 'song': 0xc},
       dotOrientation = 'se'),
    AccessPoint('Morph Ball Room Left', 'Crateria', {
        'Blue Brinstar Elevator Bottom': lambda sm: sm.canUsePowerBombs()
    }, roomInfo = { 'RoomPtr':0x9e9f, "area": 0x1},
       exitInfo = {'DoorPtr':0x8e9e, 'direction': 0x5, "cap": (0x1e, 0x6), "bitFlag": 0x0,
                   "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x288},
       dotOrientation = 'sw'),
    # Escape APs
    AccessPoint('Climb Bottom Left', 'Crateria', {
        'Landing Site': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0x96ba, "area": 0x0},
       exitInfo = {'DoorPtr':0x8b6e, 'direction': 0x5, "cap": (0x2e, 0x16), "bitFlag": 0x0,
                   "screen": (0x2, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x888},
       escape = True,
       dotOrientation = 'ne'),
    AccessPoint('Flyway Right', 'Crateria', {},
       roomInfo = {'RoomPtr':0x9879, "area": 0x0},
       exitInfo = {'DoorPtr':0x8bc2, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000,
                   "exitAsmPtr": 0xf030}, # setup_next_escape in rando_escape.asm
       entryInfo = {'SamusX':0xffff, 'SamusY':0xffff}, # unused
       escape = True),
    AccessPoint('Bomb Torizo Room Left', 'Crateria', {},
       roomInfo = {'RoomPtr':0x9804, "area": 0x0},
       exitInfo = {'DoorPtr':0x8baa, 'direction': 0x5, "cap": (0x2e, 0x6), "bitFlag": 0x0,
                   "screen": (0x2, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0xb8},
       escape = True),
    ### Green and Pink Brinstar
    AccessPoint('Green Brinstar Elevator', 'GreenPinkBrinstar', {
        'Big Pink': Cache.ldeco(lambda sm: sm.wand(sm.canPassDachoraRoom(),
                                                   sm.traverse('MainShaftBottomRight'))),
        'Etecoons Bottom': lambda sm: sm.canAccessEtecoons()
    }, roomInfo = {'RoomPtr':0x9938, "area": 0x0},
       exitInfo = {'DoorPtr':0x8bfe, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xcc, 'SamusY':0x88},
       start = {'spawn': 0x0108, 'doors':[0x1f, 0x21, 0x26], 'patches':[RomPatches.BrinReserveBlueDoors], 'solveArea': "Green Brinstar"}, # XXX test if it would be better in brin reserve room with custom save
       dotOrientation = 'ne'),
    AccessPoint('Big Pink', 'GreenPinkBrinstar', {
        'Green Hill Zone Top Right': Cache.ldeco(lambda sm: sm.wand(sm.haveItem('Morph'),
                                                                    sm.traverse('BigPinkBottomRight'))),
        'Green Brinstar Elevator': lambda sm: sm.canPassDachoraRoom()
    }, internal=True, start={'spawn': 0x0100, 'solveArea': "Pink Brinstar"}),
    AccessPoint('Green Hill Zone Top Right', 'GreenPinkBrinstar', {
        'Noob Bridge Right': lambda sm: SMBool(True),
        'Big Pink': Cache.ldeco(lambda sm: sm.haveItem('Morph'))
    }, traverse=Cache.ldeco(lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.AreaRandoBlueDoors), sm.traverse('GreenHillZoneTopRight'))),
       roomInfo = {'RoomPtr':0x9e52, "area": 0x1 },
       exitInfo = {'DoorPtr':0x8e86, 'direction': 0x4, "cap": (0x1, 0x26), "bitFlag": 0x0,
                   "screen": (0x0, 0x2), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x1c7, 'SamusY':0x88},
       dotOrientation = 'e'),
    AccessPoint('Noob Bridge Right', 'GreenPinkBrinstar', {
        'Green Hill Zone Top Right': Cache.ldeco(lambda sm: sm.wor(sm.haveItem('Wave'),
                                                                   sm.wor(sm.canBlueGateGlitch(),
                                                                          RomPatches.has(sm.player, RomPatches.AreaRandoGatesOther))))
    }, traverse=Cache.ldeco(lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.AreaRandoBlueDoors), sm.traverse('NoobBridgeRight'))),
       roomInfo = {'RoomPtr':0x9fba, "area": 0x1 },
       exitInfo = {'DoorPtr':0x8f0a, 'direction': 0x4, "cap": (0x1, 0x46), "bitFlag": 0x0,
                   "screen": (0x0, 0x4), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x5ce, 'SamusY':0x88},
       dotOrientation = 'se'),
    AccessPoint('Green Brinstar Main Shaft Top Left', 'GreenPinkBrinstar', {
        'Green Brinstar Elevator': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0x9ad9, "area": 0x1},
       exitInfo = {'DoorPtr':0x8cb2, 'direction': 0x5, "cap": (0x2e, 0x6), "bitFlag": 0x0,
                   "screen": (0x2, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x488},
       escape = True,
       dotOrientation = 'ne'),
    AccessPoint('Brinstar Pre-Map Room Right', 'GreenPinkBrinstar', {
    }, roomInfo = {'RoomPtr':0x9b9d, "area": 0x1},
       exitInfo = {'DoorPtr':0x8d42, 'direction': 0x4, "cap": (0x1, 0x46), "bitFlag": 0x0,
                   "screen": (0x0, 0x4), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xffff, 'SamusY':0xffff}, # unused
       escape = True,
       dotOrientation = 'ne'),
    AccessPoint('Etecoons Supers', 'GreenPinkBrinstar', {
        'Etecoons Bottom': lambda sm: SMBool(True)
    }, internal=True,
       start={'spawn': 0x0107, 'doors':[0x34], 'patches':[RomPatches.EtecoonSupersBlueDoor],
              'save':"Save_Etecoons" ,'solveArea': "Green Brinstar",
              'forcedEarlyMorph':True, 'needsPreRando': True}),
    AccessPoint('Etecoons Bottom', 'GreenPinkBrinstar', {
        'Etecoons Supers': Cache.ldeco(lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.EtecoonSupersBlueDoor),
                                                         sm.traverse('EtecoonEnergyTankLeft'))),
        'Green Brinstar Elevator': lambda sm: sm.canUsePowerBombs()
    }, internal=True),
    ### Wrecked Ship
    AccessPoint('West Ocean Left', 'WreckedShip', {
        'Wrecked Ship Main': Cache.ldeco(lambda sm: sm.traverse('WestOceanRight'))
    }, roomInfo = {'RoomPtr':0x93fe, "area": 0x0},
       exitInfo = {'DoorPtr':0x89ca, 'direction': 0x5, "cap": (0x1e, 0x6), "bitFlag": 0x0,
                   "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x488},
       dotOrientation = 'w'),
    AccessPoint('Wrecked Ship Main', 'WreckedShip', {
        'West Ocean Left': lambda sm: SMBool(True),
        'Wrecked Ship Back': Cache.ldeco(lambda sm: sm.wor(sm.wand(Bosses.bossDead(sm, 'Phantoon'),
                                                                   sm.canPassSpongeBath()),
                                                           sm.wand(sm.wnot(Bosses.bossDead(sm, 'Phantoon')),
                                                                   RomPatches.has(sm.player, RomPatches.SpongeBathBlueDoor)))),
        'PhantoonRoomOut': Cache.ldeco(lambda sm: sm.wand(sm.traverse('WreckedShipMainShaftBottom'), sm.canPassBombPassages())),
        'Bowling': Cache.ldeco(lambda sm: sm.wand(sm.canMorphJump(),
                                                  sm.canPassBowling()))
    }, internal=True,
       start={'spawn':0x0300,
              'doors':[0x83,0x8b], 'patches':[RomPatches.SpongeBathBlueDoor, RomPatches.WsEtankBlueDoor],
              'solveArea': "WreckedShip Main",
              'needsPreRando':True}),
    AccessPoint('Wrecked Ship Back', 'WreckedShip', {
        'Wrecked Ship Main': lambda sm: SMBool(True),
        'Crab Maze Left': Cache.ldeco(lambda sm: sm.canPassForgottenHighway(True))
    }, internal=True),
    AccessPoint('Bowling', 'WreckedShip', {
        'West Ocean Left': lambda sm: SMBool(True)
    }, internal=True),
    AccessPoint('Crab Maze Left', 'WreckedShip', {
        'Wrecked Ship Back': Cache.ldeco(lambda sm: sm.canPassForgottenHighway(False))
    }, traverse=Cache.ldeco(lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.AreaRandoBlueDoors),
                                              sm.traverse('LeCoudeBottom'))), # it is not exactly coude's door
                                                                              # but it's equivalent in vanilla anyway
       roomInfo = {'RoomPtr':0x957d, "area": 0x0, 'songs':[0x958e]},
       exitInfo = {'DoorPtr':0x8aae, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x188, 'song': 0xc},
       dotOrientation = 'e'),
    AccessPoint('PhantoonRoomOut', 'WreckedShip', {
        'Wrecked Ship Main': lambda sm: sm.canPassBombPassages()
    }, boss = True,
       roomInfo = {'RoomPtr':0xcc6f, "area": 0x3},
       exitInfo = {'DoorPtr':0xa2ac, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0},
       entryInfo = {'SamusX':0x49f, 'SamusY':0xb8},
       traverse=lambda sm: sm.canOpenEyeDoors(),
       dotOrientation = 's'),
    AccessPoint('PhantoonRoomIn', 'WreckedShip', {},
       boss = True,
       roomInfo = {'RoomPtr':0xcd13, "area": 0x3},
       exitInfo = {'DoorPtr':0xa2c4, 'direction': 0x5, "cap": (0x4e, 0x6), "bitFlag": 0x0,
                   "screen": (0x4, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe1fe,
                   "exitAsmPtr": 0xf7f0},
       entryInfo = {'SamusX':0x2e, 'SamusY':0xb8},
       dotOrientation = 's'),
    AccessPoint('Basement Left', 'WreckedShip', {
        'Wrecked Ship Main': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0xcc6f, "area": 0x3},
       exitInfo = {'DoorPtr':0xa2a0, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x2e, 'SamusY':0x88},
       escape = True,
       dotOrientation = 'ne'),
    AccessPoint('Wrecked Ship Map Room', 'WreckedShip', {
    }, roomInfo = {'RoomPtr':0xcccb, "area": 0x3},
       exitInfo = {'DoorPtr':0xa2b8, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xffff, 'SamusY':0xffff}, # unused
       escape = True,
       dotOrientation = 'ne'),
    ### Lower Norfair
    AccessPoint('Lava Dive Right', 'LowerNorfair', {
        'LN Entrance': lambda sm: sm.canPassLavaPit()
    }, roomInfo = {'RoomPtr':0xaf14, "area": 0x2, 'songs':[0xaf25]},
       exitInfo = {'DoorPtr':0x96d2, 'direction': 0x4, "cap": (0x11, 0x26), "bitFlag": 0x0,
                   "screen": (0x1, 0x2), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x3d0, 'SamusY':0x88, 'song': 0x15},
       dotOrientation = 'w'),
    AccessPoint('LN Entrance', 'LowerNorfair', {
        'Lava Dive Right': lambda sm: sm.canPassLavaPitReverse(),
        'LN Above GT': lambda sm: sm.canPassLowerNorfairChozo(),
        'Screw Attack Bottom': Cache.ldeco(lambda sm: sm.wand(sm.canUsePowerBombs(),
                                                              sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                              sm.canGreenGateGlitch(),
                                                              sm.canDestroyBombWalls())),
        'Firefleas': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                    sm.canPassWorstRoom(),
                                                    sm.canUsePowerBombs()))
    }, internal=True),
    AccessPoint('LN Above GT', 'LowerNorfair', {
        'LN Entrance': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                      sm.canPassBombPassages())),
        'Screw Attack Bottom': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                              sm.enoughStuffGT()))
    }, internal=True),
    AccessPoint('Screw Attack Bottom', 'LowerNorfair', {
        'LN Entrance': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                      sm.canExitScrewAttackArea(),
                                                      sm.haveItem('Super'),
                                                      sm.canUsePowerBombs()))
    }, internal=True),
    AccessPoint('Firefleas', 'LowerNorfair', {
        'LN Entrance': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                      sm.canPassAmphitheaterReverse(),
                                                      sm.canPassWorstRoomPirates(),
                                                      sm.canUsePowerBombs())),
        'Three Muskateers Room Left': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                                     sm.haveItem('Morph'),
                                                                     # check for only 3 ki hunters this way
                                                                     sm.canPassRedKiHunters())),
        'Ridley Zone': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                      sm.traverse('WastelandLeft'),
                                                      sm.traverse('RedKihunterShaftBottom'),
                                                      sm.canGetBackFromRidleyZone(),
                                                      sm.canPassRedKiHunters(),
                                                      sm.canPassWastelandDessgeegas(),
                                                      sm.canPassNinjaPirates())),
        'Screw Attack Bottom': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                              sm.canPassAmphitheaterReverse(),
                                                              sm.canDestroyBombWalls(),
                                                              sm.canGreenGateGlitch())),
        'Firefleas Top': Cache.ldeco(lambda sm: sm.wand(sm.canPassBombPassages(),
                                                        sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main'])))
    }, internal=True),
    AccessPoint('Firefleas Top', 'LowerNorfair', {
        # this weird condition basically says: "if we start here, give heat protection"
        'Firefleas': Cache.ldeco(lambda sm: sm.wor(sm.wnot(RomPatches.has(sm.player, RomPatches.LowerNorfairPBRoomHeatDisable)),
                                                   sm.heatProof()))
    }, internal=True,
       start={'spawn':0x0207,
              'rom_patches': ['LN_PB_Heat_Disable', 'LN_Firefleas_Remove_Fune','firefleas_shot_block.ips'],
              'patches':[RomPatches.LowerNorfairPBRoomHeatDisable, RomPatches.FirefleasRemoveFune],
              'knows': ["FirefleasWalljump"],
              'save': "Save_Firefleas", 'needsPreRando': True,
              'solveArea': "Lower Norfair After Amphitheater",
              'forcedEarlyMorph':True}),
    AccessPoint('Ridley Zone', 'LowerNorfair', {
        'Firefleas': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                    sm.canGetBackFromRidleyZone(),
                                                    sm.canPassWastelandDessgeegas(),
                                                    sm.canPassRedKiHunters())),
        'RidleyRoomOut': Cache.ldeco(lambda sm: sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main'])),
        'Wasteland': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                    sm.canGetBackFromRidleyZone(),
                                                    sm.canPassWastelandDessgeegas()))
    }, internal=True),
    AccessPoint('Wasteland', 'LowerNorfair', {
        # no transition to firefleas to exlude pb of shame location when starting at firefleas top
        'Ridley Zone': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                      sm.traverse('WastelandLeft'),
                                                      sm.canGetBackFromRidleyZone(),
                                                      sm.canPassWastelandDessgeegas(),
                                                      sm.canPassNinjaPirates()))
    }, internal=True),
    AccessPoint('Three Muskateers Room Left', 'LowerNorfair', {
        'Firefleas': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                                    sm.haveItem('Morph'),
                                                    sm.canPassThreeMuskateers()))
    }, roomInfo = {'RoomPtr':0xb656, "area": 0x2},
       exitInfo = {'DoorPtr':0x9a4a, 'direction': 0x5, "cap": (0x5e, 0x6), "bitFlag": 0x0,
                   "screen": (0x5, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x134, 'SamusY':0x88},
       dotOrientation = 'n'),
    AccessPoint('RidleyRoomOut', 'LowerNorfair', {
        'Ridley Zone': Cache.ldeco(lambda sm: sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']))
    }, boss = True,
       roomInfo = {'RoomPtr':0xb37a, "area": 0x2},
       exitInfo = {'DoorPtr':0x98ca, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0},
       entryInfo = {'SamusX':0x2e, 'SamusY':0x98},
       traverse=Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                                               sm.canOpenEyeDoors())),
       dotOrientation = 'e'),
    AccessPoint('RidleyRoomIn', 'LowerNorfair', {},
       boss = True,
       roomInfo = {'RoomPtr':0xb32e, "area": 0x2},
       exitInfo = {'DoorPtr':0x98be, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0},
       entryInfo = {'SamusX':0xbf, 'SamusY':0x198}, # on Ridley's platform. entry screen has to be changed (see getDoorConnections)
       dotOrientation = 'e'),
    ### Kraid
    AccessPoint('Warehouse Zeela Room Left', 'Kraid', {
        'KraidRoomOut': lambda sm: sm.canPassBombPassages()
    }, roomInfo = {'RoomPtr': 0xa471, "area": 0x1, 'songs':[0xa482]},
       exitInfo = {'DoorPtr': 0x913e, 'direction': 0x5, "cap": (0x2e, 0x6), "bitFlag": 0x0,
                   "screen": (0x2, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xbd3f},
       entryInfo = {'SamusX':0x34, 'SamusY':0x88, 'song':0x12},
       dotOrientation = 'w'),
    AccessPoint('KraidRoomOut', 'Kraid', {
        'Warehouse Zeela Room Left': lambda sm: sm.canPassBombPassages()
    }, boss = True,
       roomInfo = {'RoomPtr':0xa56b, "area": 0x1,
                   # put red brin song in both pre-kraid rooms,
                   # (vanilla music only makes sense if kraid is
                   #  vanilla)
                   "songs":[0xa57c,0xa537,0xa551]},
       exitInfo = {'DoorPtr':0x91b6, 'direction': 0x4, "cap": (0x1, 0x16), "bitFlag": 0x0,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0},
       entryInfo = {'SamusX':0x1cd, 'SamusY':0x188, 'song':0x12},
       traverse=lambda sm: sm.canOpenEyeDoors(),
       dotOrientation = 'e'),
    AccessPoint('KraidRoomIn', 'Kraid', {},
       boss = True,
       roomInfo = {'RoomPtr':0xa59f, "area": 0x1},
       exitInfo = {'DoorPtr':0x91ce, 'direction': 0x5, "cap": (0x1e, 0x16), "bitFlag": 0x0,
                   "screen": (0x1, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0},
       entryInfo = {'SamusX':0x34, 'SamusY':0x188},
       dotOrientation = 'e'),
    ### Norfair
    AccessPoint('Warehouse Entrance Left', 'Norfair', {
        'Warehouse Entrance Right': lambda sm: sm.canAccessKraidsLair(),
        'Business Center': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0xa6a1, "area": 0x1},
       exitInfo = {'DoorPtr':0x922e, 'direction': 0x5, "cap": (0xe, 0x16), "bitFlag": 0x40,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xbdd1},
       entryInfo = {'SamusX':0x34, 'SamusY':0x88},
       dotOrientation = 'sw'),
    AccessPoint('Warehouse Entrance Right', 'Norfair', {
        'Warehouse Entrance Left': Cache.ldeco(lambda sm: sm.haveItem('Super'))
    }, roomInfo = {'RoomPtr': 0xa6a1, "area": 0x1},
       exitInfo = {'DoorPtr': 0x923a, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX': 0x2c7, 'SamusY': 0x98},
       dotOrientation = 'nw'),
    AccessPoint('Business Center', 'Norfair', {
        'Cathedral': Cache.ldeco(lambda sm: sm.canEnterCathedral(Settings.hellRunsTable['MainUpperNorfair']['Norfair Entrance -> Cathedral Missiles']['mult'])),
        'Bubble Mountain': Cache.ldeco(# go through cathedral
                                       lambda sm: sm.wand(sm.traverse('CathedralRight'),
                                                          sm.canEnterCathedral(Settings.hellRunsTable['MainUpperNorfair']['Norfair Entrance -> Bubble']['mult']))),
        'Bubble Mountain Bottom': Cache.ldeco(lambda sm: sm.haveItem('SpeedBooster')), # frog speedway
        'Crocomire Speedway Bottom': Cache.ldeco(lambda sm: sm.wor(sm.wand(sm.haveItem('SpeedBooster'), # frog speedway
                                                                           sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Norfair Entrance -> Croc via Frog w/Wave' if sm.haveItem('Wave') else 'Norfair Entrance -> Croc via Frog']),
                                                                           sm.wor(sm.canBlueGateGlitch(),
                                                                                  sm.haveItem('Wave'))),
                                                                   # below ice
                                                                   sm.wand(sm.traverse('BusinessCenterTopLeft'),
                                                                           sm.haveItem('SpeedBooster'),
                                                                           sm.canUsePowerBombs(),
                                                                           sm.canHellRun(**Settings.hellRunsTable['Ice']['Norfair Entrance -> Croc via Ice'])))),
        'Warehouse Entrance Left': lambda sm: SMBool(True)
    }, internal=True,
       start={'spawn':0x0208, 'doors':[0x4d], 'patches':[RomPatches.HiJumpAreaBlueDoor], 'solveArea': "Norfair Entrance", 'needsPreRando':True}),
    AccessPoint('Single Chamber Top Right', 'Norfair', {
        'Bubble Mountain Top': Cache.ldeco(lambda sm: sm.wand(sm.canDestroyBombWalls(),
                                                              sm.haveItem('Morph'),
                                                              sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Single Chamber <-> Bubble Mountain'])))
    },  roomInfo = {'RoomPtr':0xad5e, "area": 0x2},
        exitInfo = {'DoorPtr':0x95fa, 'direction': 0x4, "cap": (0x11, 0x6), "bitFlag": 0x0,
                    "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
        entryInfo = {'SamusX':0x5cf, 'SamusY':0x88},
        dotOrientation = 'ne'),
    AccessPoint('Cathedral', 'Norfair', {
        'Business Center': Cache.ldeco(lambda sm: sm.canExitCathedral(Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Cathedral Missiles'])),
        'Bubble Mountain': Cache.ldeco(lambda sm: sm.wand(sm.traverse('CathedralRight'),
                                                          sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Norfair Entrance -> Cathedral Missiles'])))
    }, internal=True),
    AccessPoint('Kronic Boost Room Bottom Left', 'Norfair', {
        'Bubble Mountain Bottom': Cache.ldeco(lambda sm: sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Single Chamber <-> Bubble Mountain'])),
        'Bubble Mountain Top': Cache.ldeco(lambda sm: sm.wand(sm.haveItem('Morph'),
                                                              sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Kronic Boost Room -> Bubble Mountain Top']))), # go all the way around
        'Crocomire Speedway Bottom': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Kronic Boost Room <-> Croc']),
                                                                    sm.wor(sm.haveItem('Wave'),
                                                                           sm.canBlueGateGlitch()))),
    }, traverse=Cache.ldeco(lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.AreaRandoBlueDoors), sm.traverse('KronicBoostBottomLeft'))),
       roomInfo = {'RoomPtr':0xae74, "area": 0x2, 'songs':[0xae85]},
       exitInfo = {'DoorPtr':0x967e, 'direction': 0x5, "cap": (0x3e, 0x6), "bitFlag": 0x0,
                   "screen": (0x3, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x134, 'SamusY':0x288, 'song': 0x15},
       dotOrientation = 'se'),
    AccessPoint('Crocomire Speedway Bottom', 'Norfair', {
        'Grapple Escape': lambda sm: sm.canGrappleEscape(),
        'Business Center': Cache.ldeco(lambda sm: sm.wand(sm.canPassFrogSpeedwayRightToLeft(),
                                                          sm.canHellRun(**Settings.hellRunsTable['Ice']['Croc -> Norfair Entrance']))),
        'Bubble Mountain Bottom': Cache.ldeco(lambda sm: sm.canHellRun(**Settings.hellRunsTable['Ice']['Croc -> Bubble Mountain'])),
        'Kronic Boost Room Bottom Left': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Kronic Boost Room <-> Croc']),
                                                                        sm.haveItem('Morph')))
    }, traverse=Cache.ldeco(lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.CrocBlueDoors), sm.traverse('CrocomireSpeedwayBottom'))),
       roomInfo = {'RoomPtr':0xa923, "area": 0x2},
       exitInfo = {'DoorPtr':0x93d2, 'direction': 0x6, "cap": (0x36, 0x2), "bitFlag": 0x0,
                   "screen": (0x3, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xc57, 'SamusY':0x2b8},
       dotOrientation = 'se'),
    AccessPoint('Grapple Escape', 'Norfair', {
        'Business Center': lambda sm: sm.haveItem('Super'),
        'Crocomire Speedway Bottom': lambda sm: sm.canHellRunBackFromGrappleEscape()
    }, internal=True),
    AccessPoint('Bubble Mountain', 'Norfair', {
        'Business Center': lambda sm: sm.canExitCathedral(Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Norfair Entrance']),
        'Bubble Mountain Top': lambda sm: sm.canClimbBubbleMountain(),
        'Cathedral': Cache.ldeco(lambda sm: sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Cathedral Missiles'])),
        'Bubble Mountain Bottom': lambda sm: sm.canPassBombPassages()
    }, internal=True,
       start={'spawn':0x0201, 'doors':[0x54,0x55], 'patches':[RomPatches.SpeedAreaBlueDoors], 'knows':['BubbleMountainWallJump'], 'solveArea': "Bubble Norfair Bottom"}),
    AccessPoint('Bubble Mountain Top', 'Norfair', {
        'Kronic Boost Room Bottom Left': Cache.ldeco(# go all the way around
                                                     lambda sm: sm.wand(sm.haveItem('Morph'),
                                                                        sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Kronic Boost Room wo/Bomb']))),
        'Single Chamber Top Right': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Single Chamber <-> Bubble Mountain']),
                                                                   sm.canDestroyBombWalls(),
                                                                   sm.haveItem('Morph'),
                                                                   RomPatches.has(sm.player, RomPatches.SingleChamberNoCrumble))),
        'Bubble Mountain': lambda sm: SMBool(True),
        # all the way around
        'Bubble Mountain Bottom': Cache.ldeco(lambda sm: sm.wand(sm.haveItem('Morph'),
                                                                 sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble Top <-> Bubble Bottom'])))
    }, internal=True),
    AccessPoint('Bubble Mountain Bottom', 'Norfair', {
        'Bubble Mountain': lambda sm: sm.canPassBombPassages(),
        'Crocomire Speedway Bottom': Cache.ldeco(lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Croc']),
                                                                    sm.wor(sm.canBlueGateGlitch(),
                                                                           sm.haveItem('Wave')))),
        'Kronic Boost Room Bottom Left': Cache.ldeco(lambda sm: sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Kronic Boost Room'])),
        'Business Center': lambda sm: sm.canPassFrogSpeedwayRightToLeft(),
        # all the way around
        'Bubble Mountain Top': Cache.ldeco(lambda sm: sm.wand(sm.haveItem('Morph'),
                                                              sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble Top <-> Bubble Bottom'])))
    }, internal=True),
    AccessPoint('Business Center Mid Left', 'Norfair', {
        'Warehouse Entrance Left': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0xa7de, "area": 0x2},
       exitInfo = {'DoorPtr':0x9306, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x488},
       escape = True,
       dotOrientation = 'ne'),
    AccessPoint('Norfair Map Room', 'Norfair', {
    }, roomInfo = {'RoomPtr':0xb0b4, "area": 0x2},
       exitInfo = {'DoorPtr':0x97c2, 'direction': 0x4, "cap": (0x1, 0x46), "bitFlag": 0x0,
                   "screen": (0x0, 0x4), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xffff, 'SamusY':0xffff}, # unused
       escape = True,
       dotOrientation = 'ne'),
    ### Croc
    AccessPoint('Crocomire Room Top', 'Crocomire', {
    }, traverse=Cache.ldeco(lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.CrocBlueDoors), sm.enoughStuffCroc())),
       roomInfo = {'RoomPtr':0xa98d, "area": 0x2, 'songs':[0xa9bd]},
       exitInfo = {'DoorPtr':0x93ea, 'direction': 0x7, "cap": (0xc6, 0x2d), "bitFlag": 0x0,
                   "screen": (0xc, 0x2), "distanceToSpawn": 0x1c0, "doorAsmPtr": 0x0000,
                   "exitAsmPtr": 0xf7f0},
       entryInfo = {'SamusX':0x383, 'SamusY':0x98, 'song': 0x15},
       dotOrientation = 'se'),
    ### West Maridia
    AccessPoint('Main Street Bottom', 'WestMaridia', {
        'Red Fish Room Bottom': lambda sm: sm.canGoUpMtEverest(),
        'Crab Hole Bottom Left': Cache.ldeco(lambda sm: sm.wand(sm.haveItem('Morph'),
                                                                sm.canTraverseCrabTunnelLeftToRight())),
        # this transition leads to EastMaridia directly
        'Oasis Bottom': Cache.ldeco(lambda sm: sm.wand(sm.wnot(RomPatches.has(sm.player, RomPatches.MaridiaSandWarp)),
                                                       sm.traverse('MainStreetBottomRight'),
                                                       sm.wor(sm.haveItem('Super'),
                                                              RomPatches.has(sm.player, RomPatches.AreaRandoGatesOther)),
                                                       sm.canTraverseWestSandHallLeftToRight())),
        'Crab Shaft Left': lambda sm: sm.canPassMtEverest()
    }, roomInfo = {'RoomPtr':0xcfc9, "area": 0x4},
       exitInfo = {'DoorPtr':0xa39c, 'direction': 0x6, "cap": (0x6, 0x2), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x170, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x14a, 'SamusY':0x7a8},
       dotOrientation = 's'),
    AccessPoint('Mama Turtle', 'WestMaridia', {
        'Main Street Bottom': lambda sm: sm.canJumpUnderwater()
    }, internal=True,
       start = {'spawn': 0x0406, 'solveArea': "Maridia Green",
                'save':"Save_Mama", 'needsPreRando':True,
                'patches':[RomPatches.MamaTurtleBlueDoor],
                'rom_patches':['mama_save.ips'], 'doors': [0x8e]}),
    AccessPoint('Crab Hole Bottom Left', 'WestMaridia', {
        'Main Street Bottom': Cache.ldeco(lambda sm: sm.wand(sm.canExitCrabHole(),
                                                             sm.wor(sm.canGreenGateGlitch(),
                                                                    RomPatches.has(sm.player, RomPatches.AreaRandoGatesOther)))),
        # this transition leads to EastMaridia directly
        'Oasis Bottom': Cache.ldeco(lambda sm: sm.wand(sm.wnot(RomPatches.has(sm.player, RomPatches.MaridiaSandWarp)),
                                                       sm.canExitCrabHole(),
                                                       sm.canTraverseWestSandHallLeftToRight()))
    }, roomInfo = {'RoomPtr':0xd21c, "area": 0x4},
       exitInfo = {'DoorPtr':0xa510, 'direction': 0x5,
                   "cap": (0x3e, 0x6), "screen": (0x3, 0x0), "bitFlag": 0x0,
                   "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x28, 'SamusY':0x188},
       dotOrientation = 'se'),
    AccessPoint('Red Fish Room Left', 'WestMaridia', {
        'Red Fish Room Bottom': Cache.ldeco(lambda sm: sm.haveItem('Morph')) # just go down
    }, roomInfo = {'RoomPtr':0xd104, "area": 0x4},
       exitInfo = {'DoorPtr':0xa480, 'direction': 0x5, "cap": (0x2e, 0x36), "bitFlag": 0x40,
                   "screen": (0x2, 0x3), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe367},
       entryInfo = {'SamusX':0x34, 'SamusY':0x88},
       dotOrientation = 'w'),
    AccessPoint('Red Fish Room Bottom', 'WestMaridia', {
        'Main Street Bottom': lambda sm: SMBool(True), # just go down
        'Red Fish Room Left': Cache.ldeco(lambda sm: sm.wand(sm.haveItem('Morph'),
                                                             sm.canJumpUnderwater()))
    }, internal=True),
    AccessPoint('Crab Shaft Left', 'WestMaridia', {
        'Main Street Bottom': lambda sm: SMBool(True), # fall down
        'Beach': lambda sm: sm.canDoOuterMaridia(),
        'Crab Shaft Right': lambda sm: SMBool(True)
    }, internal=True),
    AccessPoint('Watering Hole', 'WestMaridia', {
        'Beach': lambda sm: sm.haveItem('Morph'),
        'Watering Hole Bottom': lambda sm: SMBool(True)
    }, internal=True,
       start = {'spawn': 0x0407, 'solveArea': "Maridia Pink Bottom", 'save':"Save_Watering_Hole",
                'patches':[RomPatches.MaridiaTubeOpened], 'rom_patches':['wh_open_tube.ips'],
                'forcedEarlyMorph':True}),
    AccessPoint('Watering Hole Bottom', 'WestMaridia', {
        'Watering Hole': lambda sm: sm.canJumpUnderwater()
    }, internal=True),
    AccessPoint('Beach', 'WestMaridia', {
        'Crab Shaft Left': lambda sm: SMBool(True), # fall down
        'Watering Hole': Cache.ldeco(lambda sm: sm.wand(sm.wor(sm.canPassBombPassages(),
                                                               sm.canUseSpringBall()),
                                                        sm.canDoOuterMaridia()))
    }, internal=True),
    AccessPoint('Crab Shaft Right', 'WestMaridia', {
        'Crab Shaft Left': lambda sm: sm.canJumpUnderwater()
    }, traverse=Cache.ldeco(lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.CrabShaftBlueDoor),
                                              sm.traverse('CrabShaftRight'))),
       roomInfo = {'RoomPtr':0xd1a3, "area": 0x4},
       exitInfo = {'DoorPtr':0xa4c8, 'direction': 0x4, "cap": (0x1, 0x16), "bitFlag": 0x0,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0},
       entryInfo = {'SamusX':0x1ca, 'SamusY':0x388},
       dotOrientation = 'e'),
    # escape APs
    AccessPoint('Crab Hole Bottom Right', 'WestMaridia', {
        'Crab Hole Bottom Left': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0xd21c, "area": 0x4},
       exitInfo = {'DoorPtr':0xa51c, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xd7, 'SamusY':0x188},
       escape = True,
       dotOrientation = 'ne'),
    AccessPoint('Maridia Map Room', 'WestMaridia', {
    }, roomInfo = {'RoomPtr':0xd3b6, "area": 0x4},
       exitInfo = {'DoorPtr':0xa5e8, 'direction': 0x5, "cap": (0xe, 0x16), "bitFlag": 0x0,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe356},
       entryInfo = {'SamusX':0xffff, 'SamusY':0xffff}, # unused
       escape = True,
       dotOrientation = 'ne'),
    ### East Maridia
    AccessPoint('Aqueduct Top Left', 'EastMaridia', {
        'Aqueduct Bottom': lambda sm: sm.wor(sm.wand(RomPatches.has(sm.player, RomPatches.AqueductBombBlocks),
                                                     sm.canDestroyBombWallsUnderwater()),
                                             sm.canUsePowerBombs())
    }, roomInfo = {'RoomPtr':0xd5a7, "area": 0x4},
       exitInfo = {'DoorPtr':0xa708, 'direction': 0x5, "cap": (0x1e, 0x36), "bitFlag": 0x0,
                   "screen": (0x1, 0x3), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe398},
       entryInfo = {'SamusX':0x34, 'SamusY':0x188},
       dotOrientation = 'w'),
    AccessPoint('Aqueduct Bottom', 'EastMaridia', {
        'Aqueduct Top Left': Cache.ldeco(lambda sm: sm.wand(sm.canDestroyBombWallsUnderwater(), # top left bomb blocks
                                                            sm.canJumpUnderwater())),
        'Post Botwoon': Cache.ldeco(lambda sm: sm.wand(sm.canJumpUnderwater(),
                                                       sm.canPassBotwoonHallway(),
                                                       sm.haveItem('Botwoon'))),
        'Left Sandpit': lambda sm: sm.canAccessSandPits(),
        'Right Sandpit': lambda sm: sm.canAccessSandPits(),
        'Aqueduct': Cache.ldeco(lambda sm: sm.wand(sm.wor(sm.haveItem('SpeedBooster'),
                                                          sm.wand(sm.knowsSnailClip(),
                                                                  sm.haveItem('Morph'))),
                                                   sm.haveItem('Gravity')))
    }, internal=True),
    AccessPoint('Aqueduct', 'EastMaridia', {
        'Aqueduct Bottom': lambda sm: SMBool(True) # go down
    }, internal=True,
       start = {'spawn': 0x0405, 'solveArea': "Maridia Pink Bottom",
                'save':"Save_Aqueduct", 'needsPreRando':True,
                'doors': [0x96]}),
    AccessPoint('Post Botwoon', 'EastMaridia', {
        'Aqueduct Bottom': Cache.ldeco(lambda sm: sm.wor(sm.wand(sm.canJumpUnderwater(), # can't access the sand pits from the right side of the room
                                                                 sm.haveItem('Morph')),
                                                         sm.wand(sm.haveItem('Gravity'),
                                                                 sm.haveItem('SpeedBooster')))),
        'Colosseum Top Right': lambda sm: sm.canBotwoonExitToColosseum(),
        'Toilet Top': Cache.ldeco(lambda sm: sm.wand(sm.canReachCacatacAlleyFromBotowoon(),
                                                     sm.canPassCacatacAlley()))
    }, internal=True),
    AccessPoint('West Sand Hall Left', 'EastMaridia', {
        # XXX there might be some tech to do this suitless, but HJ+ice is not enough
        'Oasis Bottom': Cache.ldeco(lambda sm: sm.haveItem('Gravity')),
        'Aqueduct Bottom': Cache.ldeco(lambda sm: RomPatches.has(sm.player, RomPatches.MaridiaSandWarp)),
        # this goes directly to WestMaridia
        'Main Street Bottom': Cache.ldeco(lambda sm: sm.wand(sm.wnot(RomPatches.has(sm.player, RomPatches.MaridiaSandWarp)),
                                                             sm.wor(sm.canGreenGateGlitch(),
                                                                    RomPatches.has(sm.player, RomPatches.AreaRandoGatesOther)))),
        # this goes directly to WestMaridia
        'Crab Hole Bottom Left': Cache.ldeco(lambda sm: sm.wand(sm.wnot(RomPatches.has(sm.player, RomPatches.MaridiaSandWarp)),
                                                                sm.haveItem('Morph')))
    }, internal=True),
    AccessPoint('Left Sandpit', 'EastMaridia', {
        'West Sand Hall Left': lambda sm: sm.canAccessSandPits(),
        'Oasis Bottom': lambda sm: sm.canAccessSandPits()
    }, internal=True),
    AccessPoint('Oasis Bottom', 'EastMaridia', {
        'Toilet Top': Cache.ldeco(lambda sm: sm.wand(sm.traverse('OasisTop'), sm.canDestroyBombWallsUnderwater())),
        'West Sand Hall Left': lambda sm: sm.canAccessSandPits()
    }, internal=True),
    AccessPoint('Right Sandpit', 'EastMaridia', {
        'Oasis Bottom': lambda sm: sm.canAccessSandPits()
    }, internal=True),
    AccessPoint('Le Coude Right', 'EastMaridia', {
        'Toilet Top': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0x95a8, "area": 0x0},
       exitInfo = {'DoorPtr':0x8aa2, 'direction': 0x4, "cap": (0x1, 0x16), "bitFlag": 0x0,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xd1, 'SamusY':0x88},
       dotOrientation = 'ne'),
    AccessPoint('Toilet Top', 'EastMaridia', {
        'Oasis Bottom': Cache.ldeco(lambda sm: sm.wand(sm.traverse('PlasmaSparkBottom'), sm.canDestroyBombWallsUnderwater())),
        'Le Coude Right': lambda sm: SMBool(True),
        'Colosseum Top Right': Cache.ldeco(lambda sm: sm.wand(Bosses.bossDead(sm, 'Draygon'),
                                                              # suitless could be possible with this but unreasonable: https://youtu.be/rtLwytH-u8o
                                                              sm.haveItem('Gravity'),
                                                              sm.haveItem('Morph')))
    }, internal=True),
    AccessPoint('Colosseum Top Right', 'EastMaridia', {
        'Post Botwoon': lambda sm: sm.canColosseumToBotwoonExit(),
        'Precious Room Top': Cache.ldeco(lambda sm: sm.traverse('ColosseumBottomRight')), # go down
    }, internal = True),
    AccessPoint('Precious Room Top', 'EastMaridia', {
        'Colosseum Top Right': lambda sm: sm.canClimbColosseum(),
        'DraygonRoomOut': lambda sm: SMBool(True) # go down
    }, internal = True),
    # boss APs
    AccessPoint('DraygonRoomOut', 'EastMaridia', {
        'Precious Room Top': lambda sm: sm.canExitPreciousRoom()
    }, boss = True,
       roomInfo = {'RoomPtr':0xd78f, "area": 0x4, "songs":[0xd7a5]},
       exitInfo = {'DoorPtr':0xa840, 'direction': 0x5, "cap": (0x1e, 0x6), "bitFlag": 0x0,
                   "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0},
       entryInfo = {'SamusX':0x34, 'SamusY':0x288, 'song':0x1b},
       traverse=lambda sm: sm.canOpenEyeDoors(),
       dotOrientation = 'e'),
    AccessPoint('DraygonRoomIn', 'EastMaridia', {
        'Draygon Room Bottom': Cache.ldeco(lambda sm: sm.wor(Bosses.bossDead(sm, "Draygon"),
                                                             sm.wand(sm.canFightDraygon(),
                                                                     sm.enoughStuffsDraygon())))
    }, boss = True,
       roomInfo = {'RoomPtr':0xda60, "area": 0x4},
       exitInfo = {'DoorPtr':0xa96c, 'direction': 0x4, "cap": (0x1, 0x26), "bitFlag": 0x0,
                   "screen": (0x0, 0x2), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe3d9,
                   "exitAsmPtr": 0xf7f0},
       entryInfo = {'SamusX':0x1c8, 'SamusY':0x88},
       dotOrientation = 'e'),
    AccessPoint('Draygon Room Bottom', 'EastMaridia', {
       'DraygonRoomIn': Cache.ldeco(lambda sm: sm.wand(Bosses.bossDead(sm, 'Draygon'), sm.canExitDraygon()))
    }, internal = True),
    ### Red Brinstar. Main nodes: Red Tower Top Left, East Tunnel Right
    AccessPoint('Red Tower Top Left', 'RedBrinstar', {
        # go up
        'Red Brinstar Elevator': lambda sm: sm.canClimbRedTower(),
        'Caterpillar Room Top Right': Cache.ldeco(lambda sm: sm.wand(sm.canPassRedTowerToMaridiaNode(),
                                                                     sm.canClimbRedTower())),
        # go down
        'East Tunnel Right': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0xa253, "area": 0x1},
       exitInfo = {'DoorPtr':0x902a, 'direction': 0x5, "cap": (0x5e, 0x6), "bitFlag": 0x0,
                   "screen": (0x5, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x2f, 'SamusY':0x488},
       dotOrientation = 'w'),
    AccessPoint('Caterpillar Room Top Right', 'RedBrinstar', {
        'Red Brinstar Elevator': lambda sm: sm.canPassMaridiaToRedTowerNode()
    }, roomInfo = {'RoomPtr':0xa322, "area": 0x1},
       exitInfo = {'DoorPtr':0x90c6, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x40,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xbdaf},
       entryInfo = {'SamusX':0x2cd, 'SamusY':0x388},
       dotOrientation = 'ne'),
    AccessPoint('Red Brinstar Elevator', 'RedBrinstar', {
        'Caterpillar Room Top Right': lambda sm: sm.canPassRedTowerToMaridiaNode(),
        'Red Tower Top Left': Cache.ldeco(lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.HellwayBlueDoor), sm.traverse('RedTowerElevatorLeft')))
    }, traverse=Cache.ldeco(lambda sm:sm.wor(RomPatches.has(sm.player, RomPatches.RedTowerBlueDoors), sm.traverse('RedBrinstarElevatorTop'))),
       roomInfo = {'RoomPtr':0x962a, "area": 0x0},
       exitInfo = {'DoorPtr':0x8af6, 'direction': 0x7, "cap": (0x16, 0x2d), "bitFlag": 0x0,
                   "screen": (0x1, 0x2), "distanceToSpawn": 0x1c0, "doorAsmPtr": 0xb9f1},
       entryInfo = {'SamusX':0x80, 'SamusY':0x58},
       start={'spawn':0x010a, 'doors':[0x3c], 'patches':[RomPatches.HellwayBlueDoor], 'solveArea': "Red Brinstar Top", 'areaMode':True},
       dotOrientation = 'n'),
    AccessPoint('East Tunnel Right', 'RedBrinstar', {
        'East Tunnel Top Right': lambda sm: SMBool(True), # handled by room traverse function
        'Glass Tunnel Top': Cache.ldeco(lambda sm: sm.wand(sm.canUsePowerBombs(),
                                                           sm.wor(sm.haveItem('Gravity'),
                                                                  sm.haveItem('HiJump')))),
        'Red Tower Top Left': lambda sm: sm.canClimbBottomRedTower()
    }, roomInfo = {'RoomPtr':0xcf80, "area": 0x4},
       exitInfo = {'DoorPtr':0xa384, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x40,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xce, 'SamusY':0x188},
       dotOrientation = 'se'),
    AccessPoint('East Tunnel Top Right', 'RedBrinstar', {
        'East Tunnel Right': Cache.ldeco(lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.AreaRandoGatesBase),
                                                           sm.haveItem('Super')))
    }, traverse=Cache.ldeco(lambda sm: RomPatches.has(sm.player, RomPatches.AreaRandoGatesBase)),
       roomInfo = {'RoomPtr':0xcf80, "area": 0x4},
       exitInfo = {'DoorPtr':0xa390, 'direction': 0x4, "cap": (0x1, 0x16), "bitFlag": 0x0,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe356},
       entryInfo = {'SamusX':0x3c6, 'SamusY':0x88},
       dotOrientation = 'e'),
    AccessPoint('Glass Tunnel Top', 'RedBrinstar', {
        'East Tunnel Right': Cache.ldeco(lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.MaridiaTubeOpened),
                                                           sm.canUsePowerBombs()))
    }, traverse=Cache.ldeco(lambda sm: sm.wand(sm.wor(sm.haveItem('Gravity'),
                                                      sm.haveItem('HiJump')),
                                               sm.wor(RomPatches.has(sm.player, RomPatches.MaridiaTubeOpened),
                                                      sm.canUsePowerBombs()))),
       roomInfo = {'RoomPtr':0xcefb, "area": 0x4},
       exitInfo = {'DoorPtr':0xa330, 'direction': 0x7, "cap": (0x16, 0x7d), "bitFlag": 0x0,
                   "screen": (0x1, 0x7), "distanceToSpawn": 0x200, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x81, 'SamusY':0x78},
       dotOrientation = 's'),
    ### Tourian
    AccessPoint('Golden Four', 'Tourian', {},
       roomInfo = {'RoomPtr':0xa5ed, "area": 0x0},
       exitInfo = {'DoorPtr':0x91e6, 'direction': 0x5, "cap": (0xe, 0x66), "bitFlag": 0x0,
                   "screen": (0x0, 0x6), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x88},
       start={'spawn':0x0007, 'solveArea': "Tourian", "save": "Save_G4", 'areaMode':True},
       dotOrientation = 'w'),
    AccessPoint('Tourian Escape Room 4 Top Right', 'Tourian', {},
       roomInfo = {'RoomPtr':0xdede, "area": 0x5},
       exitInfo = {'DoorPtr':0xab34, 'direction': 0x4, "cap": (0x1, 0x86), "bitFlag": 0x40,
                   "screen": (0x0, 0x8), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe4cf},
       entryInfo = {'SamusX':0xffff, 'SamusY':0xffff}, # unused
       escape = True,
       dotOrientation = 'ne'),
]
