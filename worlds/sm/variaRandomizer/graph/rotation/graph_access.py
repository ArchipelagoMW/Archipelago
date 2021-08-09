from graph.graph import AccessPoint
from utils.parameters import Settings
from rom.rom_patches import RomPatches
from logic.smbool import SMBool, smboolFalse
from logic.helpers import Bosses
from logic.cache import Cache

# all access points and traverse functions
accessPoints = [
    ### Crateria and Blue Brinstar
    AccessPoint('Landing Site', 'Crateria', {
        'Lower Mushrooms Left': lambda sm: sm.wand(sm.canDestroyBombWalls(),
                                                   sm.canPassCrateriaGreenPirates()),
        'Gauntlet Top': lambda sm: sm.wand(sm.haveItem('Morph'),
                                           sm.canDestroyBombWalls()),
        'Keyhunter Room Bottom': lambda sm: sm.traverse('LandingSiteRight'),
        'Moat Right': lambda sm: sm.wand(sm.traverse('LandingSiteRight'),
                                         sm.traverse('KihunterRight')),
        'Blue Brinstar Elevator Bottom': lambda sm: SMBool(True)
    }, internal=True,
       start={'spawn': 0x0000, 'doors':[0x32], 'patches':[RomPatches.BlueBrinstarBlueDoor], 'solveArea': "Crateria Landing Site"}),
    AccessPoint('Blue Brinstar Elevator Bottom', 'Crateria', {
        # energy requirement is to kill the sidehoppers as two are stacked at the bottom of the room
        'Morph Ball Room Left': lambda sm: sm.wand(sm.canUsePowerBombs(),
                                                   sm.energyReserveCountOk(int(2.0/sm.getDmgReduction()[0]))),
        'Landing Site': lambda sm: SMBool(True)
    }, internal=True),
    AccessPoint('Gauntlet Top', 'Crateria', {
        'Green Pirates Shaft Bottom Right': lambda sm: sm.wand(sm.haveItem('Morph'),
                                                               sm.canPassCrateriaGreenPirates()),
        'Landing Site': lambda sm:  sm.wand(sm.haveItem('Morph'),
                                            sm.canDestroyBombWalls())
    }, internal=True,
       start={'spawn': 0x0006, 'solveArea': "Crateria Gauntlet", 'save':"Save_Gauntlet", 'forcedEarlyMorph':True}),
    AccessPoint('Lower Mushrooms Left', 'Crateria', {
        'Landing Site': Cache.ldeco('LML_LS', lambda sm: sm.wand(sm.canDestroyBombWalls(), sm.canPassCrateriaGreenPirates())),
        'Green Pirates Shaft Bottom Right': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0x9969, "area": 0x0, 'songs':[0x997a]},
       exitInfo = {'DoorPtr':0x8c22, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x36, 'SamusY':0x88, 'song': 0x9},
       dotOrientation = 'nw'),
    AccessPoint('Green Pirates Shaft Bottom Right', 'Crateria', {
        'Lower Mushrooms Left': lambda sm: SMBool(True),
        'Gauntlet Top': lambda sm: sm.wand(sm.haveItem('Morph'),
                                           sm.canPassCrateriaGreenPirates())
    }, traverse = lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoMoreBlueDoors),
                                    sm.traverse('GreenPiratesShaftBottomRight')),
       roomInfo = {'RoomPtr':0x99bd, "area": 0x0, 'songs':[0x99ce]},
       # the doorAsmPtr 7FE00 is set by the g4_skip.ips patch, we have to call it
       exitInfo = {'DoorPtr':0x8c52, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xfe00},
       entryInfo = {'SamusX':0xcc, 'SamusY':0x688, 'song': 0x9},
       dotOrientation = 'e'),
    AccessPoint('Moat Right', 'Crateria', {
        'Keyhunter Room Bottom': lambda sm: sm.wand(sm.canPassMoatReverse(), sm.haveItem('Morph'))
    }, roomInfo = {'RoomPtr':0x95ff, "area": 0x0, 'songs':[0x9610]},
       exitInfo = {'DoorPtr':0x8aea, 'direction': 0x4, "cap": (0x1, 0x46), "bitFlag": 0x0,
                   "screen": (0x0, 0x4), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x1cf, 'SamusY':0x88, 'song': 0xc},
       dotOrientation = 'ne'),
    AccessPoint('Keyhunter Room Bottom', 'Crateria', {
        'Moat Right': lambda sm: sm.wand(sm.traverse('KihunterRight'), sm.haveItem('Morph')),
        'Landing Site': lambda sm: sm.haveItem('Morph')
    }, traverse = lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoMoreBlueDoors),
                                    sm.traverse('KihunterBottom')),
       roomInfo = { 'RoomPtr':0x948c, "area": 0x0, 'songs':[0x949d] },
       exitInfo = {'DoorPtr':0x8a42, 'direction': 0x6, "cap": (0x6, 0x2), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x14c, 'SamusY':0x2b8, 'song': 0xc},
       dotOrientation = 'se'),
    AccessPoint('Morph Ball Room Left', 'Crateria', {
        'Blue Brinstar Elevator Bottom': lambda sm: sm.wand(sm.canUsePowerBombs(),
                                                            sm.energyReserveCountOk(int(2.0/sm.getDmgReduction()[0])))
    }, roomInfo = { 'RoomPtr':0x9e9f, "area": 0x1},
       exitInfo = {'DoorPtr':0x8e9e, 'direction': 0x5, "cap": (0x1e, 0x6), "bitFlag": 0x0,
                   "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x288},
       dotOrientation = 'sw'),
#    # Escape APs
#    AccessPoint('Climb Bottom Left', 'Crateria', {
#        'Landing Site': lambda sm: SMBool(True)
#    }, roomInfo = {'RoomPtr':0x96ba, "area": 0x0},
#       exitInfo = {'DoorPtr':0x8b6e, 'direction': 0x5, "cap": (0x2e, 0x16), "bitFlag": 0x0,
#                   "screen": (0x2, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
#       entryInfo = {'SamusX':0x34, 'SamusY':0x888},
#       escape = True,
#       dotOrientation = 'ne'),
#    AccessPoint('Flyway Right', 'Crateria', {},
#       roomInfo = {'RoomPtr':0x9879, "area": 0x0},
#       exitInfo = {'DoorPtr':0x8bc2, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
#                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000,
#                   "exitAsmPtr": 0xf030}, # setup_next_escape in rando_escape.asm
#       entryInfo = {'SamusX':0xffff, 'SamusY':0xffff}, # unused
#       escape = True),
#    AccessPoint('Bomb Torizo Room Left', 'Crateria', {},
#       roomInfo = {'RoomPtr':0x9804, "area": 0x0},
#       exitInfo = {'DoorPtr':0x8baa, 'direction': 0x5, "cap": (0x2e, 0x6), "bitFlag": 0x0,
#                   "screen": (0x2, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
#       entryInfo = {'SamusX':0x34, 'SamusY':0xb8},
#       escape = True),
#    ### Green and Pink Brinstar
    AccessPoint('Green Brinstar Elevator', 'GreenPinkBrinstar', {
        'Big Pink': Cache.ldeco('GBE_BP',
                                lambda sm: sm.wand(sm.canDestroyBombWalls(),
                                                   sm.traverse('MainShaftBottomRight'))),
        'Etecoons Bottom': lambda sm: sm.canAccessEtecoons()
    }, roomInfo = {'RoomPtr':0x9938, "area": 0x0},
       exitInfo = {'DoorPtr':0x8bfe, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xcc, 'SamusY':0x88},
       start = {'spawn': 0x0108, 'doors':[0x1f, 0x21, 0x26], 'patches':[RomPatches.BrinReserveBlueDoors], 'solveArea': "Green Brinstar"}, # XXX test if it would be better in brin reserve room with custom save
       dotOrientation = 'ne'),
    AccessPoint('Big Pink', 'GreenPinkBrinstar', {
        'Green Hill Zone Top Right': lambda sm: sm.wand(sm.haveItem('Morph'),
                                                        sm.traverse('BigPinkBottomRight')),
        'Green Brinstar Elevator': lambda sm: sm.canDestroyBombWalls()
    }, internal=True, start={'spawn': 0x0100, 'solveArea': "Pink Brinstar"}),
    AccessPoint('Green Hill Zone Top Right', 'GreenPinkBrinstar', {
        'Noob Bridge Right': lambda sm: SMBool(True),
        'Big Pink': lambda sm: sm.haveItem('Morph')
    }, traverse=lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoBlueDoors), sm.traverse('GreenHillZoneTopRight')),
       roomInfo = {'RoomPtr':0x9e52, "area": 0x1 },
       exitInfo = {'DoorPtr':0x8e86, 'direction': 0x4, "cap": (0x1, 0x26), "bitFlag": 0x0,
                   "screen": (0x0, 0x2), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x1c7, 'SamusY':0x88},
       dotOrientation = 'e'),
    AccessPoint('Noob Bridge Right', 'GreenPinkBrinstar', {
        'Green Hill Zone Top Right': lambda sm: SMBool(True)
    }, traverse=lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoBlueDoors), sm.traverse('NoobBridgeRight')),
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
#    AccessPoint('Brinstar Pre-Map Room Right', 'GreenPinkBrinstar', {
#    }, roomInfo = {'RoomPtr':0x9b9d, "area": 0x1},
#       exitInfo = {'DoorPtr':0x8d42, 'direction': 0x4, "cap": (0x1, 0x46), "bitFlag": 0x0,
#                   "screen": (0x0, 0x4), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
#       entryInfo = {'SamusX':0xffff, 'SamusY':0xffff}, # unused
#       escape = True,
#       dotOrientation = 'ne'),
    AccessPoint('Etecoons Supers', 'GreenPinkBrinstar', {
        # TODO::need clarification to know exactly where is etecoons bottom, up or down from the etank ?
        #       -> it's up
        'Etecoons Bottom': lambda sm: sm.haveItem('Morph')
    }, internal=True,
       start={'spawn': 0x0107, 'doors':[0x34], 'patches':[RomPatches.EtecoonSupersBlueDoor],
              'save':"Save_Etecoons" ,'solveArea': "Green Brinstar", 'forcedEarlyMorph':True}),
    AccessPoint('Etecoons Bottom', 'GreenPinkBrinstar', {
        'Etecoons Supers': lambda sm: sm.wor(RomPatches.has(RomPatches.EtecoonSupersBlueDoor),
                                             sm.traverse('EtecoonEnergyTankLeft')),
        'Green Brinstar Elevator': lambda sm: sm.canUsePowerBombs()
    }, internal=True),
    ### Wrecked Ship
    AccessPoint('West Ocean Left', 'WreckedShip', {
        'Wrecked Ship Main': lambda sm: sm.traverse('WestOceanRight')
    }, roomInfo = {'RoomPtr':0x93fe, "area": 0x0},
       exitInfo = {'DoorPtr':0x89ca, 'direction': 0x5, "cap": (0x1e, 0x6), "bitFlag": 0x0,
                   "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x488},
       dotOrientation = 'w'),
    AccessPoint('Wrecked Ship Main', 'WreckedShip', {
        'West Ocean Left': lambda sm: sm.wand(sm.haveItem('Gravity'),
                                              sm.wor(sm.haveItem('Hijump'),
                                                     # TODO::check if the IBJ is not too hard
                                                     sm.canFly())),
        'Wrecked Ship Back': Cache.ldeco('WSM_WSB', (
            # just have to fall through spongebath and spicky room
            lambda sm: sm.wand(sm.haveItem('Morph'),
                               sm.wor(Bosses.bossDead(sm, 'Phantoon'),
                                      sm.wand(sm.wnot(Bosses.bossDead(sm, 'Phantoon')),
                                              RomPatches.has(RomPatches.SpongeBathBlueDoor)))))),
        'PhantoonRoomOut': lambda sm: sm.wand(sm.traverse('WreckedShipMainShaftBottom'),
                                              sm.haveItem('Morph'),
                                              # TODO::check if screwattack can also break blocks before gadora
                                              sm.canPassBombPassages()),
        'Wrecked Ship Outside Top': (
            lambda sm: sm.wand(sm.haveItem('Morph'),
                               sm.canClimbAttic(),
                               Bosses.bossDead(sm, 'Phantoon'),
                               # need hijump when suitless
                               # TODO::check with other items than hijump when suitless
                               sm.wor(sm.haveItem('Gravity'),
                                      sm.wand(sm.knowsGravLessLevel1(), sm.haveItem('Hijump'))))
        )
    }, internal=True,
       start={'spawn':0x0300,
              'doors':[0x83,0x8b], 'patches':[RomPatches.SpongeBathBlueDoor, RomPatches.WsEtankBlueDoor],
              'solveArea': "WreckedShip Main",
              'needsPreRando':True}),
    AccessPoint('Wrecked Ship Outside Top', 'WreckedShip', {
        'Wrecked Ship Main': lambda sm: sm.haveItem('Morph')
    }, internal=True),
    AccessPoint('Wrecked Ship Back', 'WreckedShip', {
        'Wrecked Ship Main': lambda sm: sm.wand(sm.haveItem('Morph'),
                                                sm.knowsSuitlessBreakFree(),
                                                sm.canGravLessLevel1()),
        # all for crabe maze, just fall in east ocean
        'Crab Maze Left': lambda sm: sm.canPassForgottenHighway()
    }, internal=True),
    AccessPoint('Crab Maze Left', 'WreckedShip', {
        # exit crab maze & climb east ocean
        'Wrecked Ship Back': lambda sm: sm.canPassForgottenHighway()
    }, roomInfo = {'RoomPtr':0x957d, "area": 0x0, 'songs':[0x958e]},
       exitInfo = {'DoorPtr':0x8aae, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x188, 'song': 0xc},
       dotOrientation = 'e'),
    AccessPoint('PhantoonRoomOut', 'WreckedShip', {
        # TODO::test with screwattack
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
#    AccessPoint('Basement Left', 'WreckedShip', {
#        'Wrecked Ship Main': lambda sm: SMBool(True)
#    }, roomInfo = {'RoomPtr':0xcc6f, "area": 0x3},
#       exitInfo = {'DoorPtr':0xa2a0, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
#                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
#       entryInfo = {'SamusX':0x2e, 'SamusY':0x88},
#       escape = True,
#       dotOrientation = 'ne'),
#    AccessPoint('Wrecked Ship Map Room', 'WreckedShip', {
#    }, roomInfo = {'RoomPtr':0xcccb, "area": 0x3},
#       exitInfo = {'DoorPtr':0xa2b8, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
#                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
#       entryInfo = {'SamusX':0xffff, 'SamusY':0xffff}, # unused
#       escape = True,
#       dotOrientation = 'ne'),



#    ### Lower Norfair
#    AccessPoint('Lava Dive Right', 'LowerNorfair', {
#        'LN Entrance': lambda sm: sm.canPassLavaPit()
#    }, roomInfo = {'RoomPtr':0xaf14, "area": 0x2, 'songs':[0xaf25]},
#       exitInfo = {'DoorPtr':0x96d2, 'direction': 0x4, "cap": (0x11, 0x26), "bitFlag": 0x0,
#                   "screen": (0x1, 0x2), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
#       entryInfo = {'SamusX':0x3d0, 'SamusY':0x88, 'song': 0x15},
#       dotOrientation = 'w'),
#    AccessPoint('LN Entrance', 'LowerNorfair', {
#        'Lava Dive Right': lambda sm: sm.canPassLavaPitReverse(),
#        'LN Above GT': lambda sm: sm.canPassLowerNorfairChozo(),
#        'Screw Attack Bottom': Cache.ldeco('LNE_SAB',
#                                           lambda sm: sm.wand(sm.canUsePowerBombs(),
#                                                              sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
#                                                              sm.canGreenGateGlitch(),
#                                                              sm.canDestroyBombWalls())),
#        'Firefleas': Cache.ldeco('LNE_F',
#                                 lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
#                                                    sm.canPassWorstRoom(),
#                                                    sm.canUsePowerBombs()))
#    }, internal=True),
#    AccessPoint('LN Above GT', 'LowerNorfair', {
#        'Screw Attack Bottom': Cache.ldeco('LNAGT_SAB',
#                                           lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
#                                                              sm.enoughStuffGT()))
#    }, internal=True),
#    AccessPoint('Screw Attack Bottom', 'LowerNorfair', {
#        'LN Entrance': Cache.ldeco('SAB_LNE',
#                                   lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
#                                                      sm.canExitScrewAttackArea(),
#                                                      sm.haveItem('Super'),
#                                                      sm.canUsePowerBombs()))
#    }, internal=True),
#    AccessPoint('Firefleas', 'LowerNorfair', {
#        'LN Entrance': Cache.ldeco('F_LNE',
#                                   lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
#                                                      sm.canPassAmphitheaterReverse(),
#                                                      sm.canPassWorstRoomPirates(),
#                                                      sm.canUsePowerBombs())),
#        'Three Muskateers Room Left': Cache.ldeco('F_TMRL',
#                                                  lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
#                                                                     sm.haveItem('Morph'),
#                                                                     # check for only 3 ki hunters this way
#                                                                     sm.canPassRedKiHunters())),
#        'Ridley Zone': Cache.ldeco('F_RZ',
#                                   lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
#                                                      sm.traverse('WastelandLeft'),
#                                                      sm.traverse('RedKihunterShaftBottom'),
#                                                      sm.canUsePowerBombs(),
#                                                      sm.wand(sm.canGetBackFromRidleyZone(),
#                                                              sm.canPassRedKiHunters(),
#                                                              sm.canPassWastelandDessgeegas(),
#                                                              sm.canPassNinjaPirates()))),
#        'Screw Attack Bottom': Cache.ldeco('F_SAB',
#                                           lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
#                                                              sm.canPassAmphitheaterReverse(),
#                                                              sm.canDestroyBombWalls(),
#                                                              sm.canGreenGateGlitch())),
#        'Firefleas Top': Cache.ldeco('F_FT',
#                                     lambda sm: sm.wand(sm.canPassBombPassages(),
#                                                        sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main'])))
#    }, internal=True),
#    AccessPoint('Firefleas Top', 'LowerNorfair', {
#        # this weird condition basically says: "if we start here, give heat protection"
#        'Firefleas': lambda sm: sm.wor(sm.wnot(RomPatches.has(RomPatches.LowerNorfairPBRoomHeatDisable)),
#                                       sm.heatProof())
#    }, internal=True,
#       start={'spawn':0x0207,
#              'rom_patches': ['LN_PB_Heat_Disable', 'LN_Firefleas_Remove_Fune','firefleas_shot_block.ips'],
#              'patches':[RomPatches.LowerNorfairPBRoomHeatDisable, RomPatches.FirefleasRemoveFune],
#              'knows': ["FirefleasWalljump"],
#              'save': "Save_Firefleas", 'needsPreRando': True,
#              'solveArea': "Lower Norfair After Amphitheater",
#              'forcedEarlyMorph':True}),
#    AccessPoint('Ridley Zone', 'LowerNorfair', {
#        'Firefleas': Cache.ldeco('RZ_F',
#                                 lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
#                                                    sm.canUsePowerBombs(),
#                                                    sm.wand(sm.canGetBackFromRidleyZone(),
#                                                            sm.canPassWastelandDessgeegas(),
#                                                            sm.canPassRedKiHunters()))),
#        'RidleyRoomOut': lambda sm: sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main'])
#    }, internal=True),
#    AccessPoint('Three Muskateers Room Left', 'LowerNorfair', {
#        'Firefleas': Cache.ldeco('TMRL_F',
#                                 lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
#                                                    sm.haveItem('Morph'),
#                                                    sm.canPassThreeMuskateers()))
#    }, roomInfo = {'RoomPtr':0xb656, "area": 0x2},
#       exitInfo = {'DoorPtr':0x9a4a, 'direction': 0x5, "cap": (0x5e, 0x6), "bitFlag": 0x0,
#                   "screen": (0x5, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
#       entryInfo = {'SamusX':0x134, 'SamusY':0x88},
#       dotOrientation = 'n'),
#    AccessPoint('RidleyRoomOut', 'LowerNorfair', {
#        'Ridley Zone': lambda sm: sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main'])
#    }, boss = True,
#       roomInfo = {'RoomPtr':0xb37a, "area": 0x2},
#       exitInfo = {'DoorPtr':0x98ca, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
#                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0},
#       entryInfo = {'SamusX':0x2e, 'SamusY':0x98},
#       traverse=Cache.ldeco('RRO_T',
#                            lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
#                                               sm.canOpenEyeDoors())),
#       dotOrientation = 'e'),
#    AccessPoint('RidleyRoomIn', 'LowerNorfair', {},
#       boss = True,
#       roomInfo = {'RoomPtr':0xb32e, "area": 0x2},
#       exitInfo = {'DoorPtr':0x98be, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
#                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0},
#       entryInfo = {'SamusX':0xbf, 'SamusY':0x198}, # on Ridley's platform. entry screen has to be changed (see getDoorConnections)
#       dotOrientation = 'e'),
#    ### Kraid
    AccessPoint('Warehouse Zeela Room Left', 'Kraid', {
        'KraidRoomOut': lambda sm: sm.canPassBombPassages()
    }, roomInfo = {'RoomPtr': 0xa471, "area": 0x1, 'songs':[0xa482]},
       exitInfo = {'DoorPtr': 0x913e, 'direction': 0x5, "cap": (0x2e, 0x6), "bitFlag": 0x0,
                   "screen": (0x2, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xbd3f},
       entryInfo = {'SamusX':0x34, 'SamusY':0x88, 'song':0x12},
       dotOrientation = 'w'),
    AccessPoint('KraidRoomOut', 'Kraid', {
        'Warehouse Zeela Room Left': lambda sm: sm.wand(sm.canPassBombPassages(),
                                                        sm.wor(sm.haveItem('HiJump'),
                                                               sm.canFly()))
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
        'Warehouse Entrance Right': lambda sm: sm.haveItem('Super'),
        'Business Center': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0xa6a1, "area": 0x1},
       exitInfo = {'DoorPtr':0x922e, 'direction': 0x5, "cap": (0xe, 0x16), "bitFlag": 0x40,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xbdd1},
       entryInfo = {'SamusX':0x34, 'SamusY':0x88},
       dotOrientation = 'sw'),
    AccessPoint('Warehouse Entrance Right', 'Norfair', {
        'Warehouse Entrance Left': lambda sm: sm.haveItem('Super')
    }, roomInfo = {'RoomPtr': 0xa6a1, "area": 0x1},
       exitInfo = {'DoorPtr': 0x923a, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX': 0x2c7, 'SamusY': 0x98},
       dotOrientation = 'nw'),
    AccessPoint('Business Center', 'Norfair', {
        'Cathedral': lambda sm: sm.canEnterCathedral(Settings.hellRunsTable['MainUpperNorfair']['Norfair Entrance -> Cathedral Missiles']['mult']),
        'Bubble Mountain': Cache.ldeco('BC_BM', (
            lambda sm: sm.wor(sm.canPassBombPassages(), # frog speedway is opened, need pb in bubble mountain room
                              # go through cathedral
                              sm.wand(sm.traverse('CathedralRight'),
                                      sm.canEnterCathedral(Settings.hellRunsTable['MainUpperNorfair']['Norfair Entrance -> Bubble']['mult']))))),
        'Crocomire Speedway Bottom':Cache.ldeco('BC_CSB', (
            lambda sm: sm.wor(sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Norfair Entrance -> Croc via Frog']),
                              # below ice
                              sm.wand(sm.traverse('BusinessCenterTopLeft'),
                                      sm.canUsePowerBombs(),
                                      sm.canHellRun(**Settings.hellRunsTable['Ice']['Norfair Entrance -> Croc via Ice']))))),
        'Warehouse Entrance Left': lambda sm: SMBool(True)
    }, internal=True,
       start={'spawn':0x0208, 'doors':[0x4d], 'patches':[RomPatches.HiJumpAreaBlueDoor], 'solveArea': "Norfair Entrance", 'needsPreRando':True}),
    AccessPoint('Single Chamber Top Right', 'Norfair', {
        'Bubble Mountain Top': Cache.ldeco('SCTR_BBT',
                                           lambda sm: sm.wand(sm.canDestroyBombWalls(),
                                                              sm.haveItem('Morph'),
                                                              sm.haveItem('Super'),
                                                              sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Single Chamber <-> Bubble Mountain']))),
        'Kronic Boost Room Bottom Left': Cache.ldeco('SCTR_KBRNL', (
            lambda sm: sm.wand(sm.canDestroyBombWalls(),
                               sm.haveItem('Morph'),
                               sm.haveItem('Super'),
                               # there's a lot of lava in there...
                               sm.canWallJumpInLava(),
                               sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Single Chamber <-> Kronic Boost Room']))))
    },  roomInfo = {'RoomPtr':0xad5e, "area": 0x2},
        exitInfo = {'DoorPtr':0x95fa, 'direction': 0x4, "cap": (0x11, 0x6), "bitFlag": 0x0,
                    "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
        entryInfo = {'SamusX':0x5cf, 'SamusY':0x88},
        dotOrientation = 'ne'),
#    AccessPoint('Cathedral', 'Norfair', {
#        'Business Center': lambda sm: sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Cathedral Missiles']),
#        'Bubble Mountain': lambda sm: sm.wand(sm.traverse('CathedralRight'),
#                                             sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Norfair Entrance -> Cathedral Missiles']))
#    }, internal=True),
#    AccessPoint('Kronic Boost Room Bottom Left', 'Norfair', {
#        'Single Chamber Top Right': Cache.ldeco('KBRBL_SCTR',
#                                                lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Single Chamber <-> Kronic Boost Room']),
#                                                                   sm.canDestroyBombWalls(),
#                                                                   sm.haveItem('Morph'),
#                                                                   RomPatches.has(RomPatches.SingleChamberNoCrumble))),
#        'Bubble Mountain': Cache.ldeco('KBRBL_BM',
#                                       lambda sm: sm.wand(sm.canPassBombPassages(),
#                                                          sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Single Chamber <-> Bubble Mountain']))),
#        'Bubble Mountain Top': Cache.ldeco('KBRBL_BMT',
#                                           lambda sm: sm.wand(sm.haveItem('Morph'),
#                                                              sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Kronic Boost Room -> Bubble Mountain Top']))), # go all the way around
#        'Crocomire Speedway Bottom': Cache.ldeco('KBRBL_CSB',
#                                                 lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Kronic Boost Room <-> Croc']),
#                                                                    sm.wor(sm.haveItem('Wave'),
#                                                                           sm.canBlueGateGlitch()))),
#    }, traverse=lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoBlueDoors), sm.traverse('KronicBoostBottomLeft')),
#       roomInfo = {'RoomPtr':0xae74, "area": 0x2, 'songs':[0xae85]},
#       exitInfo = {'DoorPtr':0x967e, 'direction': 0x5, "cap": (0x3e, 0x6), "bitFlag": 0x0,
#                   "screen": (0x3, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
#       entryInfo = {'SamusX':0x134, 'SamusY':0x288, 'song': 0x15},
#       dotOrientation = 'se'),
    AccessPoint('Crocomire Speedway Bottom', 'Norfair', {
        'Business Center': Cache.ldeco('CSB_BC', (
                              # frog speedway, no item required
            lambda sm: sm.wor(sm.canHellRun(**Settings.hellRunsTable['Ice']['Croc -> Norfair Entrance']),
                              # croc speedway, only morph required
                              sm.wand(sm.canHellRun(**Settings.hellRunsTable['Ice']['']),
                                      sm.haveItem('Morph')),
                              # grapple escape
                              sm.wand(sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Croc -> Norfair Entrance']),
                                      sm.canWallJumpInLava(),
                                      sm.haveItem('Morph'))))),
        'Bubble Mountain': Cache.ldeco('CSB_BM', (
            # just falling TODO::adjust hellrun
            lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['Ice']['Croc -> Bubble Mountain'])))),
        'Kronic Boost Room Bottom Left': Cache.ldeco('CSB_KBRBL', (
            # just falling TODO::adjust hellrun
            lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Kronic Boost Room <-> Croc']))))
    }, traverse=lambda sm: sm.wor(RomPatches.has(RomPatches.CrocBlueDoors), sm.traverse('CrocomireSpeedwayBottom')),
       roomInfo = {'RoomPtr':0xa923, "area": 0x2},
       exitInfo = {'DoorPtr':0x93d2, 'direction': 0x6, "cap": (0x36, 0x2), "bitFlag": 0x0,
                   "screen": (0x3, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xc57, 'SamusY':0x2b8},
       dotOrientation = 'se'),
    AccessPoint('Bubble Mountain', 'Norfair', {
        # bottom left door -> frog speed way OR exit cathedral
        'Business Center': Cache.ldeco('BM_BC', (
            lambda sm: sm.wor(sm.canPassBombPassages(), # frog speedway is opened, need pb in bubble mountain room
                              # TODO::too many lava, too many enemies, no one want to do that without gravity
                              sm.wand(sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Norfair Entrance']),
                                      sm.canWallJumpInLava())))),
        'Bubble Mountain Top': lambda sm: SMBool(True),
        'Kronic Boost Room Bottom Left': Cache.ldeco('BM_KBRBL', (
            lambda sm: sm.wor(sm.wand(sm.haveItem('Morph'),
                                      # just fall
                                      sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Kronic Boost Room']))))),
        'Crocomire Speedway Bottom': Cache.ldeco('BM_CSB', (
            lambda sm: sm.wand(sm.canPassBombPassages(),
                               # just fall
                               sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Croc'])))),
        'Cathedral': lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Cathedral Missiles']),
                                        sm.canWallJumpInLava())
    }, internal=True,
       start={'spawn':0x0201, 'doors':[0x54,0x55], 'patches':[RomPatches.SpeedAreaBlueDoors], 'solveArea': "Bubble Norfair Bottom"}),
    AccessPoint('Bubble Mountain Top', 'Norfair', {
        'Single Chamber Top Right': Cache.ldeco('BMT_SCTR', (
            lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Single Chamber <-> Bubble Mountain']),
                               sm.canDestroyBombWalls(),
                               # crumble blocks are replaced with super blocks
                               sm.haveItem('Super'),
                               sm.haveItem('Morph')))),
        'Bubble Mountain': lambda sm: SMBool(True)
    }, internal=True),
#    AccessPoint('Business Center Mid Left', 'Norfair', {
#        'Warehouse Entrance Left': lambda sm: SMBool(True)
#    }, roomInfo = {'RoomPtr':0xa7de, "area": 0x2},
#       exitInfo = {'DoorPtr':0x9306, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
#                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
#       entryInfo = {'SamusX':0x34, 'SamusY':0x488},
#       escape = True,
#       dotOrientation = 'ne'),
#    AccessPoint('Norfair Map Room', 'Norfair', {
#    }, roomInfo = {'RoomPtr':0xb0b4, "area": 0x2},
#       exitInfo = {'DoorPtr':0x97c2, 'direction': 0x4, "cap": (0x1, 0x46), "bitFlag": 0x0,
#                   "screen": (0x0, 0x4), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
#       entryInfo = {'SamusX':0xffff, 'SamusY':0xffff}, # unused
#       escape = True,
#       dotOrientation = 'ne'),
    ### Croc
    AccessPoint('Crocomire Room Top', 'Crocomire', {
    }, traverse=lambda sm: sm.wor(RomPatches.has(RomPatches.CrocBlueDoors), sm.enoughStuffCroc()),
       roomInfo = {'RoomPtr':0xa98d, "area": 0x2, 'songs':[0xa9bd]},
       exitInfo = {'DoorPtr':0x93ea, 'direction': 0x7, "cap": (0xc6, 0x2d), "bitFlag": 0x0,
                   "screen": (0xc, 0x2), "distanceToSpawn": 0x1c0, "doorAsmPtr": 0x0000,
                   "exitAsmPtr": 0xf7f0},
       entryInfo = {'SamusX':0x383, 'SamusY':0x98, 'song': 0x15},
       dotOrientation = 'se'),
    ### West Maridia
    AccessPoint('Main Street Bottom', 'WestMaridia', {
        # from the red fish door to the AP door just need gravity
        'Red Fish Room Left': lambda sm: sm.haveItem('Gravity'),
        'Crab Hole Bottom Left': Cache.ldeco('MSB_CHBL', (
            lambda sm: sm.wand(sm.haveItem('Morph'),
                               # door is blue in rotation
                               sm.traverse('MainStreetBottomRight'),
                               # exit through door on ceiling
                               sm.wor(sm.haveItem('Gravity'),
                                      sm.canInfiniteBombJumpSuitless())))
        ),
        # this transition leads to EastMaridia directly
        'Oasis Bottom': Cache.ldeco('MSB_OB', (
            # just fall, but slow down to avoid crabs and projectiles
            lambda sm: sm.wand(sm.wnot(RomPatches.has(RomPatches.MaridiaSandWarp)),
                               sm.traverse('MainStreetBottomRight')))
        ),
        'Crab Shaft Left': lambda sm: SMBool(True) # possible suitless with some underwater walljumps
    }, roomInfo = {'RoomPtr':0xcfc9, "area": 0x4},
       exitInfo = {'DoorPtr':0xa39c, 'direction': 0x6, "cap": (0x6, 0x2), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x170, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x14a, 'SamusY':0x7a8},
       dotOrientation = 's'),
    AccessPoint('Mama Turtle', 'WestMaridia', {
        'Main Street Bottom': lambda sm: sm.canExitMamaTurtle()
    }, internal=True,
       start = {'spawn': 0x0406, 'solveArea': "Maridia Green", 'save':"Save_Mama",
                'patches':[RomPatches.MamaTurtleBlueDoor],
                'rom_patches':['mama_save.ips'], 'doors': [0x8e]}),
    AccessPoint('Crab Hole Bottom Left', 'WestMaridia', {
        'Main Street Bottom': Cache.ldeco('CHBL_MSB', (
            lambda sm: sm.wor(sm.haveItem('Gravity'),
                              # quite long walljumps...
                              sm.wand(sm.knowsGravLessLevel1(), sm.haveItem('HiJump'))))),
        # this transition leads to EastMaridia directly
        'Oasis Bottom': Cache.ldeco('CHBL_OB', (
            lambda sm: sm.wand(sm.wnot(RomPatches.has(RomPatches.MaridiaSandWarp)),
                               # morph to exit crab hole, then just fall
                               sm.haveItem('Morph'))))
    }, roomInfo = {'RoomPtr':0xd21c, "area": 0x4},
       exitInfo = {'DoorPtr':0xa510, 'direction': 0x5,
                   "cap": (0x3e, 0x6), "screen": (0x3, 0x0), "bitFlag": 0x0,
                   "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x28, 'SamusY':0x188},
       dotOrientation = 'se'),
    AccessPoint('Red Fish Room Left', 'WestMaridia', {
        'Main Street Bottom': lambda sm: sm.canGoUpMtEverest()
    }, roomInfo = {'RoomPtr':0xd104, "area": 0x4},
       exitInfo = {'DoorPtr':0xa480, 'direction': 0x5, "cap": (0x2e, 0x36), "bitFlag": 0x40,
                   "screen": (0x2, 0x3), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe367},
       entryInfo = {'SamusX':0x34, 'SamusY':0x88},
       dotOrientation = 'w'),
    AccessPoint('Crab Shaft Left', 'WestMaridia', {
                                         # go up Mt everest then left on main street
        'Main Street Bottom': lambda sm: sm.canGoUpMtEverest(),
        'Beach': lambda sm: sm.haveItem('Morph'),
        'Crab Shaft Right': lambda sm: sm.canMorphJump()
    }, internal=True),
    AccessPoint('Watering Hole', 'WestMaridia', {
        'Beach': lambda sm: SMBool(True),
        'Watering Hole Bottom': lambda sm: sm.haveItem('Morph')
    }, internal=True,
       start = {'spawn': 0x0407, 'solveArea': "Maridia Pink Bottom", 'save':"Save_Watering_Hole",
                'patches':[RomPatches.MaridiaTubeOpened], 'rom_patches':['wh_open_tube.ips'],
                'forcedEarlyMorph':True}),
    AccessPoint('Watering Hole Bottom', 'WestMaridia', {
        'Watering Hole': lambda sm: sm.haveItem('Morph')
    }, internal=True),
    AccessPoint('Beach', 'WestMaridia', {
        'Crab Shaft Left': lambda sm: sm.haveItem('Morph'),
        # TODO::try to pass the one block hole suitless with a springball jump
        'Watering Hole': lambda sm: sm.wor(sm.haveItem('Gravity'),
                                           # with hijump we can walljump high enough to pass the hole suitless
                                           sm.haveItem('Hijump'),
                                           # IBJ up the hole
                                           sm.canInfiniteBombJumpSuitless())
    }, internal=True),
    AccessPoint('Crab Shaft Right', 'WestMaridia', {
        # with suitless wall jumps and a morph mid air it's possible
        'Crab Shaft Left': lambda sm: sm.wand(sm.knowsGravLessLevel1(), sm.haveItem('Morph'))
    }, traverse=lambda sm: sm.wor(RomPatches.has(RomPatches.CrabShaftBlueDoor),
                                  sm.traverse('CrabShaftRight')),
       roomInfo = {'RoomPtr':0xd1a3, "area": 0x4},
       exitInfo = {'DoorPtr':0xa4c8, 'direction': 0x4, "cap": (0x1, 0x16), "bitFlag": 0x0,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0},
       entryInfo = {'SamusX':0x1ca, 'SamusY':0x388},
       dotOrientation = 'e'),
#    # escape APs
    AccessPoint('Crab Hole Bottom Right', 'WestMaridia', {
                                                   # exit through door on ceiling
        'Crab Hole Bottom Left': lambda sm: sm.wor(sm.haveItem('Gravity'),
                                                   sm.canInfiniteBombJumpSuitless())
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
        'Aqueduct Bottom': (
            lambda sm: sm.wand(sm.canUsePowerBombs(),
                               sm.wor(sm.haveItem('Gravity'),
                                      sm.wand(sm.knowsGravLessLevel1(),
                                              sm.wor(sm.canInfiniteBombJumpSuitless(),
                                                     sm.haveItem('HiJump'),
                                                     # wait for a snail to come to jump on it
                                                     SMBool(True)))))
            )
    }, roomInfo = {'RoomPtr':0xd5a7, "area": 0x4},
       exitInfo = {'DoorPtr':0xa708, 'direction': 0x5, "cap": (0x1e, 0x36), "bitFlag": 0x0,
                   "screen": (0x1, 0x3), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe398},
       entryInfo = {'SamusX':0x34, 'SamusY':0x188},
       dotOrientation = 'w'),
    AccessPoint('Aqueduct Bottom', 'EastMaridia', {
        'Aqueduct Top Left': lambda sm: sm.wand(sm.canUsePowerBombs(),
                                                sm.wor(sm.haveItem('Gravity'),
                                                       sm.wand(sm.knowsGravLessLevel1()))),
                                           # includes botwoon hallway conditions
        'Post Botwoon': lambda sm: sm.wor(sm.wand(sm.canDefeatBotwoon(),
                                                  # TODO::check for suitless beside IBJ (like with grapple)
                                                  sm.wand(sm.haveItem('Gravity'),
                                                          sm.wor(sm.canFly(),
                                                                 sm.haveItem('HiJump')))),
                                          # skip botwoon through the sandpits.
                                          # falling down "Below Botwoon Energy Tank" room looks like a softlock.
                                          sm.canGravLessLevel1()),
                                                  
        'Left Sandpit': lambda sm: sm.wand(sm.canGravLessLevel1(), sm.haveItem('Morph')),
        'Right Sandpit': lambda sm: sm.wand(sm.canGravLessLevel1(), sm.haveItem('Morph')),
        'Aqueduct': lambda sm: sm.wor(sm.canEnterExitAqueduct(),
                                      # there's also pb blocks down in the hole, can't be used to comeback suitless to aqueduct bottom
                                      sm.wand(sm.canUsePowerBombs(), sm.canGravLessLevel1()))
    }, internal=True),
    AccessPoint('Aqueduct', 'EastMaridia', {
        'Aqueduct Bottom': lambda sm: sm.canEnterExitAqueduct()
    }, internal=True,
       start = {'spawn': 0x0405, 'solveArea': "Maridia Pink Bottom", 'save':"Save_Aqueduct",
                'doors': [0x96]}),
    AccessPoint('Post Botwoon', 'EastMaridia', {
        'Aqueduct Bottom': lambda sm: sm.wor(sm.canEnterExitBotwoon(),
                                             # skip through sandipts
                                             # TODO::test what happen when you do that while botwoon is still alive
                                             sm.canGravLessLevel1()),
        'Colosseum Top Right': lambda sm: sm.wand(sm.haveItem('Morph'),
                                                  sm.canGravLessLevel1()),
        'Toilet Top': lambda sm: sm.wand(sm.canReachCacatacAlleyFromBotowoon(),
                                         sm.canPassCacatacAlley())
    }, internal=True),
#    AccessPoint('West Sand Hall Left', 'EastMaridia', {
#        # XXX there might be some tech to do this suitless, but HJ+ice is not enough
#        'Oasis Bottom': lambda sm: sm.haveItem('Gravity'),
#        'Aqueduct Bottom': lambda sm: RomPatches.has(RomPatches.MaridiaSandWarp),
#        # this goes directly to WestMaridia
#        'Main Street Bottom': Cache.ldeco('WSHL_MSB',
#                                          lambda sm: sm.wand(sm.wnot(RomPatches.has(RomPatches.MaridiaSandWarp)),
#                                                             sm.wor(sm.canGreenGateGlitch(),
#                                                                    RomPatches.has(RomPatches.AreaRandoGatesOther)))),
#        # this goes directly to WestMaridia
#        'Crab Hole Bottom Left': Cache.ldeco('WSHL_CHBL',
#                                             lambda sm: sm.wand(sm.wnot(RomPatches.has(RomPatches.MaridiaSandWarp)),
#                                                                sm.haveItem('Morph')))
#    }, internal=True),
    AccessPoint('Left Sandpit', 'EastMaridia', {
        'West Sand Hall Left': lambda sm: sm.canTraverseSandPitsBottom(),
        # just fall and avoid projectiles
        'Oasis Bottom': lambda sm: SMBool(True),
        'Aqueduct Bottom': lambda sm: sm.wand(sm.canGravLessLevel1(), sm.haveItem('Morph'))
    }, internal=True),
    AccessPoint('Oasis Bottom', 'EastMaridia', {
        # TODO::test if screwattack works under water in rotation
        'Toilet Top': lambda sm: sm.wand(sm.traverse('OasisTop'), sm.canDestroyBombWallsUnderwater()),
        'West Sand Hall Left': lambda sm: sm.canTraverseSandPitsBottom()
    }, internal=True),
    AccessPoint('Right Sandpit', 'EastMaridia', {
        'Oasis Bottom': lambda sm: sm.canTraverseSandPitsBottom(),
        'Aqueduct Bottom': lambda sm: sm.wand(sm.canGravLessLevel1(), sm.haveItem('Morph'))
    }, internal=True),
    AccessPoint('Le Coude Right', 'EastMaridia', {
        'Toilet Top': lambda sm: sm.wor(sm.haveItem('Gravity'),
                                        sm.wand(sm.knowsGravLessLevel1(),
                                                # the final jump to exit the needle room,
                                                # not an easy one, even with hijump...
                                                # way easier with space jump
                                                sm.wor(sm.haveItem('HiJump'),
                                                       sm.haveItem('SpaceJump'))))
    }, traverse=lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoBlueDoors), sm.traverse('LeCoudeBottom')),
       roomInfo = {'RoomPtr':0x95a8, "area": 0x0},
       exitInfo = {'DoorPtr':0x8aa2, 'direction': 0x4, "cap": (0x1, 0x16), "bitFlag": 0x0,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xd1, 'SamusY':0x88},
       dotOrientation = 'ne'),
    AccessPoint('Toilet Top', 'EastMaridia', {
        'Oasis Bottom': lambda sm: sm.wand(sm.traverse('PlasmaSparkBottom'), sm.canDestroyBombWallsUnderwater()),
        'Le Coude Right': lambda sm: sm.canGravLessLevel1(),
        'Precious Room Top': Cache.ldeco('TT_PRT', (
            # just fall all the way
            lambda sm: sm.canGravLessLevel1())
        )
    }, internal=True),
    AccessPoint('Colosseum Top Right', 'EastMaridia', {
        'Post Botwoon': lambda sm: sm.canEnterExitBotwoon(),
        'Precious Room Top': lambda sm: sm.traverse('ColosseumBottomRight'), # go left
    }, internal = True),
    AccessPoint('Precious Room Top', 'EastMaridia', {
        'Colosseum Top Right': lambda sm: sm.canGravLessLevel1(),
        'DraygonRoomOut': lambda sm: sm.wand(sm.haveItem('Morph'), sm.canGravLessLevel1())
    }, internal = True),
#    # boss APs
    AccessPoint('DraygonRoomOut', 'EastMaridia', {
        'Precious Room Top': lambda sm: sm.wand(sm.haveItem('Morph'), sm.canGravLessLevel1())
    }, boss = True,
       roomInfo = {'RoomPtr':0xd78f, "area": 0x4, "songs":[0xd7a5]},
       exitInfo = {'DoorPtr':0xa840, 'direction': 0x5, "cap": (0x1e, 0x6), "bitFlag": 0x0,
                   "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0},
       entryInfo = {'SamusX':0x34, 'SamusY':0x288, 'song':0x1b},
       traverse=lambda sm: sm.canOpenEyeDoors(),
       dotOrientation = 'e'),
    AccessPoint('DraygonRoomIn', 'EastMaridia', {
        'Draygon Room Bottom': Cache.ldeco('DRI_DRB',
                                           lambda sm: sm.wor(Bosses.bossDead(sm, "Draygon"),
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
       'DraygonRoomIn': lambda sm: sm.wand(Bosses.bossDead(sm, 'Draygon'), sm.canGravLessLevel1())
    }, internal = True),
    ### Red Brinstar. Main nodes: Red Tower Top Left, East Tunnel Right
    AccessPoint('Red Tower Top Left', 'RedBrinstar', {
        # go right
        'Red Brinstar Elevator': lambda sm: sm.haveItem('Morph'),
        'Caterpillar Room Top Right': lambda sm: sm.haveItem('Morph'),
        # go left
        'East Tunnel Right': lambda sm: SMBool(True)
    }, roomInfo = {'RoomPtr':0xa253, "area": 0x1},
       exitInfo = {'DoorPtr':0x902a, 'direction': 0x5, "cap": (0x5e, 0x6), "bitFlag": 0x0,
                   "screen": (0x5, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x2f, 'SamusY':0x488},
       dotOrientation = 'w'),
    AccessPoint('Caterpillar Room Top Right', 'RedBrinstar', {
        'Red Brinstar Elevator': lambda sm: SMBool(True), # wall jump up
        'Red Tower Top Left': lambda sm: sm.wand(sm.wor(RomPatches.has(RomPatches.HellwayBlueDoor),
                                                        sm.traverse('RedTowerElevatorLeft')),
                                                 # pass shot block right of tower climb
                                                 sm.haveItem('Morph'))
    }, roomInfo = {'RoomPtr':0xa322, "area": 0x1},
       exitInfo = {'DoorPtr':0x90c6, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x40,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xbdaf},
       entryInfo = {'SamusX':0x2cd, 'SamusY':0x388},
       dotOrientation = 'ne'),
    AccessPoint('Red Brinstar Elevator', 'RedBrinstar', {
        'Caterpillar Room Top Right': lambda sm: SMBool(True), # just fall
        'Red Tower Top Left': lambda sm: sm.wand(sm.wor(RomPatches.has(RomPatches.HellwayBlueDoor),
                                                        sm.traverse('RedTowerElevatorLeft')),
                                                 sm.canClimbRedTower())
    }, traverse=lambda sm:sm.wor(RomPatches.has(RomPatches.RedTowerBlueDoors), sm.traverse('RedBrinstarElevatorTop')),
       roomInfo = {'RoomPtr':0x962a, "area": 0x0},
       exitInfo = {'DoorPtr':0x8af6, 'direction': 0x7, "cap": (0x16, 0x2d), "bitFlag": 0x0,
                   "screen": (0x1, 0x2), "distanceToSpawn": 0x1c0, "doorAsmPtr": 0xb9f1},
       entryInfo = {'SamusX':0x80, 'SamusY':0x58},
       start={'spawn':0x010a, 'doors':[0x3c], 'patches':[RomPatches.HellwayBlueDoor], 'solveArea': "Red Brinstar Top", 'areaMode':True},
       dotOrientation = 'n'),
    AccessPoint('East Tunnel Right', 'RedBrinstar', {
        'East Tunnel Top Right': lambda sm: sm.haveItem('Morph'),
        # you can lay a pb on top of the room and have it detonate before falling back (cf. feral)
        # TODO::try it
        'Glass Tunnel Top': lambda sm: sm.canUsePowerBombs(),
        # there's water in Bat Room but we can wall jump underwater
        'Red Tower Top Left': lambda sm: sm.canGravLessLevel1()
    }, roomInfo = {'RoomPtr':0xcf80, "area": 0x4},
       exitInfo = {'DoorPtr':0xa384, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x40,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xce, 'SamusY':0x188},
       dotOrientation = 'se'),
    AccessPoint('East Tunnel Top Right', 'RedBrinstar', {
        'East Tunnel Right': lambda sm: sm.haveItem('Morph')
    }, roomInfo = {'RoomPtr':0xcf80, "area": 0x4},
       exitInfo = {'DoorPtr':0xa390, 'direction': 0x4, "cap": (0x1, 0x16), "bitFlag": 0x0,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe356},
       entryInfo = {'SamusX':0x3c6, 'SamusY':0x88},
       dotOrientation = 'e'),
#    AccessPoint('Glass Tunnel Top', 'RedBrinstar', {
#        'East Tunnel Right': lambda sm: sm.wor(RomPatches.has(RomPatches.MaridiaTubeOpened),
#                                               sm.canUsePowerBombs())
#    }, traverse=Cache.ldeco('GTT_T',
#                            lambda sm: sm.wand(sm.wor(sm.haveItem('Gravity'),
#                                                      sm.haveItem('HiJump')),
#                                               sm.wor(RomPatches.has(RomPatches.MaridiaTubeOpened),
#                                                      sm.canUsePowerBombs()))),
#       roomInfo = {'RoomPtr':0xcefb, "area": 0x4},
#       exitInfo = {'DoorPtr':0xa330, 'direction': 0x7, "cap": (0x16, 0x7d), "bitFlag": 0x0,
#                   "screen": (0x1, 0x7), "distanceToSpawn": 0x200, "doorAsmPtr": 0x0000},
#       entryInfo = {'SamusX':0x81, 'SamusY':0x78},
#       dotOrientation = 's'),
#    ### Tourian
#    AccessPoint('Golden Four', 'Tourian', {},
#       roomInfo = {'RoomPtr':0xa5ed, "area": 0x0},
#       exitInfo = {'DoorPtr':0x91e6, 'direction': 0x5, "cap": (0xe, 0x66), "bitFlag": 0x0,
#                   "screen": (0x0, 0x6), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
#       entryInfo = {'SamusX':0x34, 'SamusY':0x88},
#       start={'spawn':0x0007, 'solveArea': "Tourian", "save": "Save_G4", 'areaMode':True},
#       dotOrientation = 'w'),
#    AccessPoint('Tourian Escape Room 4 Top Right', 'Tourian', {},
#       roomInfo = {'RoomPtr':0xdede, "area": 0x5},
#       exitInfo = {'DoorPtr':0xab34, 'direction': 0x4, "cap": (0x1, 0x86), "bitFlag": 0x40,
#                   "screen": (0x0, 0x8), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe4cf},
#       entryInfo = {'SamusX':0xffff, 'SamusY':0xffff}, # unused
#       escape = True,
#       dotOrientation = 'ne'),
]
