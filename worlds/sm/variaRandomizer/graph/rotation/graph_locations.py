from logic.helpers import Bosses
from utils.parameters import Settings
from rom.rom_patches import RomPatches
from logic.smbool import SMBool
from graph.location import locationsDict

#locationsDict["Energy Tank, Gauntlet"].AccessFrom = {
#    'Landing Site': lambda sm: SMBool(True)
#}
#locationsDict["Energy Tank, Gauntlet"].Available = (
# TODO::from gauntlet top to etank with vanilla suits behaviour:
# V + G + bomb: 3 energy
# 0 + 0 + bomb: dead with 13 energy
# V + 0 + bomb: 6 energy
# 0 + G + bomb: 3 energy
# V + G + 3 PB: 2 energy
#  from etank to landing site:
# V + G + bomb: 4 energy
# V + G + 5 PB: 3 energy
# V + 0 + 5 PB: 7 energy
#    lambda sm: sm.wor(sm.canEnterAndLeaveGauntlet(),
#                      sm.wand(sm.canShortCharge(),
#                              sm.canEnterAndLeaveGauntletQty(1, 0)), # thanks ponk! https://youtu.be/jil5zTBCF1s
#                      sm.canDoLowGauntlet())
#)
locationsDict["Bomb"].AccessFrom = {
    'Landing Site': lambda sm: SMBool(True)
}
locationsDict["Bomb"].Available = (
    lambda sm: sm.wand(sm.haveItem('Morph'),
                       sm.traverse('FlywayRight'))
)
locationsDict["Energy Tank, Terminator"].AccessFrom = {
    'Landing Site': lambda sm: sm.canPassTerminatorBombWall(),
    'Lower Mushrooms Left': lambda sm: sm.canPassCrateriaGreenPirates(),
#    'Gauntlet Top': lambda sm: sm.haveItem('Morph')
}
locationsDict["Energy Tank, Terminator"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Reserve Tank, Brinstar"].AccessFrom = {
    'Green Brinstar Elevator': lambda sm: sm.wor(RomPatches.has(RomPatches.BrinReserveBlueDoors), sm.traverse('MainShaftRight'))
}
locationsDict["Reserve Tank, Brinstar"].Available = (
    lambda sm: sm.wor(RomPatches.has(RomPatches.BrinReserveBlueDoors), sm.traverse('EarlySupersRight'))
)
locationsDict["Charge Beam"].AccessFrom = {
    'Big Pink': lambda sm: sm.haveItem('Morph')
}
locationsDict["Charge Beam"].Available = (
    lambda sm: sm.canPassBombPassages()
)
locationsDict["Morphing Ball"].AccessFrom = {
    'Blue Brinstar Elevator Bottom': lambda sm: SMBool(True)
}
locationsDict["Morphing Ball"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Energy Tank, Brinstar Ceiling"].AccessFrom = {
    'Blue Brinstar Elevator Bottom': lambda sm: sm.wor(RomPatches.has(RomPatches.BlueBrinstarBlueDoor), sm.traverse('ConstructionZoneRight'))
}
locationsDict["Energy Tank, Brinstar Ceiling"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Energy Tank, Etecoons"].AccessFrom = {
    'Etecoons Bottom': lambda sm: SMBool(True)
}
locationsDict["Energy Tank, Etecoons"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Energy Tank, Waterway"].AccessFrom = {
    'Big Pink': lambda sm: SMBool(True)
}
locationsDict["Energy Tank, Waterway"].Available = (
    lambda sm: sm.wand(sm.canUsePowerBombs(),
                       sm.traverse('BigPinkBottomLeft'),
                       sm.haveItem('SpeedBooster'))
)
locationsDict["Energy Tank, Brinstar Gate"].AccessFrom = {
    'Big Pink': lambda sm: SMBool(True)
}
locationsDict["Energy Tank, Brinstar Gate"].Available = (
    lambda sm: sm.traverse('BigPinkRight')
)
locationsDict["Energy Tank, Brinstar Gate"].PostAvailable = (
    # TODO::test with highjump
    lambda sm: sm.canFly()
)
locationsDict["X-Ray Scope"].AccessFrom = {
    'Red Tower Top Left': lambda sm: SMBool(True)
}
locationsDict["X-Ray Scope"].Available = (
    lambda sm: sm.wand(sm.canUsePowerBombs(),
                       sm.traverse('RedTowerLeft'),
                       sm.traverse('RedBrinstarFirefleaLeft'))
)
locationsDict["Spazer"].AccessFrom = {
    'East Tunnel Right': lambda sm: SMBool(True)
}
locationsDict["Spazer"].Available = (
    lambda sm: sm.wand(sm.traverse('BelowSpazerTopRight'),
                       sm.wor(sm.canPassBombPassages(),
                              sm.wand(sm.haveItem('Morph'),
                                      RomPatches.has(RomPatches.SpazerShotBlock))))
)
locationsDict["Spazer"].PostAvailable = (
    # either with a bomb jump/springball to exit on top, or with bomb/pb to exit in the middle
    lambda sm: sm.wor(sm.canPassBombPassages(),
                      sm.wand(RomPatches.has(RomPatches.SpazerShotBlock), sm.canUseSpringBall()))
)
locationsDict["Energy Tank, Kraid"].AccessFrom = {
    'Warehouse Zeela Room Left': lambda sm: sm.haveItem('Morph')
}
locationsDict["Energy Tank, Kraid"].Available = (
    lambda sm: Bosses.bossDead(sm, 'Kraid')
)
locationsDict["Kraid"].AccessFrom = {
    'KraidRoomIn': lambda sm: SMBool(True)
}
locationsDict["Kraid"].Available = (
    lambda sm: sm.enoughStuffsKraid()
)
locationsDict["Varia Suit"].AccessFrom = {
    'KraidRoomIn': lambda sm: SMBool(True)
}
locationsDict["Varia Suit"].Available = (
    lambda sm: Bosses.bossDead(sm, 'Kraid')
)
locationsDict["Ice Beam"].AccessFrom = {
    'Business Center': lambda sm: sm.traverse('BusinessCenterTopLeft')
}
locationsDict["Ice Beam"].Available = (
    lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['Ice']['Norfair Entrance -> Ice Beam']),
                       sm.haveItem('Morph'))
)
locationsDict["Energy Tank, Crocomire"].AccessFrom = {
    'Crocomire Room Top': lambda sm: SMBool(True)
}
locationsDict["Energy Tank, Crocomire"].Available = (
    lambda sm: sm.wand(sm.enoughStuffCroc(),
                       sm.wor(sm.haveItem('Grapple'),
                              sm.haveItem('SpaceJump'),
                              sm.energyReserveCountOk(3/sm.getDmgReduction()[0])))
)
locationsDict["Hi-Jump Boots"].AccessFrom = {
    'Business Center': lambda sm: sm.wor(RomPatches.has(RomPatches.HiJumpAreaBlueDoor), sm.traverse('BusinessCenterBottomLeft'))
}
locationsDict["Hi-Jump Boots"].Available = (
    lambda sm: sm.canPassBombPassages()
)
locationsDict["Hi-Jump Boots"].PostAvailable = (
    lambda sm: sm.wor(sm.canPassBombPassages(),
                      sm.wand(sm.haveItem('Morph'), RomPatches.has(RomPatches.HiJumpShotBlock)))
)
locationsDict["Grapple Beam"].AccessFrom = {
    'Crocomire Room Top': lambda sm: SMBool(True)
}
locationsDict["Grapple Beam"].Available = (
    lambda sm: sm.wand(sm.enoughStuffCroc(),
                              # through grapple exit
                       sm.wor(sm.wand(sm.haveItem('Gravity'),
                                      sm.wor(sm.wand(sm.haveItem('HiJump'), sm.haveItem('SpeedBooster')),
                                             sm.canFly())),
                              # through acid...
                              # TODO::test with space jump, get etank requirement (there's annoying enemies)
                              sm.wand(sm.haveItem('SpaceJump'), sm.energyReserveCountOk(10))))
)
#locationsDict["Reserve Tank, Norfair"].AccessFrom = {
#    'Bubble Mountain': lambda sm: sm.canEnterNorfairReserveAreaFromBubbleMoutain(),
#    'Bubble Mountain Top': lambda sm: sm.canEnterNorfairReserveAreaFromBubbleMoutainTop(),
#}
#locationsDict["Reserve Tank, Norfair"].Available = (
#    lambda sm: sm.wand(sm.haveItem('Morph'), sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Norfair Reserve']))
#)
locationsDict["Speed Booster"].AccessFrom = {
    'Bubble Mountain Top': lambda sm: sm.wand(sm.wor(RomPatches.has(RomPatches.SpeedAreaBlueDoors),
                                                     sm.wand(sm.traverse('BubbleMountainTopRight'),
                                                             sm.traverse('SpeedBoosterHallRight'))),
                                              sm.haveItem('Morph'))
}
locationsDict["Speed Booster"].Available = (
    lambda sm: sm.canFallToSpeedBooster()
)
locationsDict["Speed Booster"].PostAvailable = (
    lambda sm: sm.canGetBackFromSpeedBooster()
)
locationsDict["Wave Beam"].AccessFrom = {
    'Bubble Mountain Top': lambda sm: sm.canAccessDoubleChamberItems()
}
locationsDict["Wave Beam"].Available = (
    lambda sm: sm.traverse('DoubleChamberRight')
)
#locationsDict["Wave Beam"].PostAvailable = (
#    lambda sm: sm.wor(sm.haveItem('Morph'), # exit through lower passage under the spikes
#                      sm.wand(sm.wor(sm.haveItem('SpaceJump'), # exit through blue gate
#                                     sm.haveItem('Grapple')),
#                              sm.wor(sm.wand(sm.canBlueGateGlitch(), sm.heatProof()), # hell run + green gate glitch is too much
#                                     sm.haveItem('Wave'))))
#)
#locationsDict["Ridley"].AccessFrom = {
#    'RidleyRoomIn': lambda sm: SMBool(True)
#}
#locationsDict["Ridley"].Available = (
#    lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']), sm.enoughStuffsRidley())
#)
#locationsDict["Energy Tank, Ridley"].AccessFrom = {
#    'RidleyRoomIn': lambda sm: SMBool(True)
#}
#locationsDict["Energy Tank, Ridley"].Available = (
#    lambda sm: sm.haveItem('Ridley')
#)
#locationsDict["Screw Attack"].AccessFrom = {
#    'Screw Attack Bottom': lambda sm: SMBool(True)
#}
#locationsDict["Screw Attack"].Available = (
#    lambda sm: SMBool(True)
#)
#locationsDict["Screw Attack"].PostAvailable = (
#    lambda sm: sm.canExitScrewAttackArea()
#)
#locationsDict["Energy Tank, Firefleas"].AccessFrom = {
#    'Firefleas': lambda sm: SMBool(True)
#}
#locationsDict["Energy Tank, Firefleas"].Available = (
#    lambda sm: sm.wor(RomPatches.has(RomPatches.FirefleasRemoveFune),
#                      # get past the fune
#                                     sm.haveItem('Super'),
#                      sm.canPassBombPassages(),
#                      sm.canUseSpringBall())
#)
#locationsDict["Energy Tank, Firefleas"].PostAvailable = (
#    lambda sm: sm.wor(sm.knowsFirefleasWalljump(),
#                      sm.wor(sm.haveItem('Ice'),
#                             sm.haveItem('HiJump'),
#                             sm.canFly(),
#                             sm.canSpringBallJump()))
#)
locationsDict["Reserve Tank, Wrecked Ship"].AccessFrom = {
    'Wrecked Ship Outside Top': lambda sm: sm.haveItem('Morph')
}
locationsDict["Reserve Tank, Wrecked Ship"].Available = (
    lambda sm: sm.wand(sm.canUsePowerBombs(),
                       sm.haveItem('SpeedBooster'),
                       # new super block to access reserve tank
                       sm.haveItem('Super'))
)
locationsDict["Energy Tank, Wrecked Ship"].AccessFrom = {
    'Wrecked Ship Back': lambda sm: sm.wand(sm.wor(RomPatches.has(RomPatches.WsEtankBlueDoor),
                                                   sm.traverse('ElectricDeathRoomTopLeft')),
                                            sm.haveItem('Morph'))
}
locationsDict["Energy Tank, Wrecked Ship"].Available = (
    lambda sm: sm.wand(sm.wor(Bosses.bossDead(sm, 'Phantoon'),
                              RomPatches.has(RomPatches.WsEtankPhantoonAlive)),
                       # TODO::add knows break free of the water line without gravity while walljumping
                       sm.knowsSuitlessBreakFree())
)
locationsDict["Energy Tank, Wrecked Ship"].PostAvailable = (
    lambda sm: sm.canMorphJump()
)
locationsDict["Phantoon"].AccessFrom = {
    'PhantoonRoomIn': lambda sm: SMBool(True)
}
locationsDict["Phantoon"].Available = (
    lambda sm: sm.enoughStuffsPhantoon()
)
locationsDict["Phantoon"].PostAvailable = (
    # exit room
    lambda sm: sm.wor(sm.canFly(), sm.haveItem('HiJump'))
)
locationsDict["Right Super, Wrecked Ship"].AccessFrom = {
    'Wrecked Ship Main': lambda sm: Bosses.bossDead(sm, 'Phantoon')
}
locationsDict["Right Super, Wrecked Ship"].Available = (
    lambda sm: sm.canPassBombPassages()
)
locationsDict["Right Super, Wrecked Ship"].PostAvailable = (
    # if we use a bomb it opens the door under samus and she falls back in previous room
    lambda sm: sm.canUsePowerBombs()
)
locationsDict["Gravity Suit"].AccessFrom = {
    # just fall after passing the morph passage
    'Wrecked Ship Outside Top': lambda sm: sm.haveItem('Morph')
}
locationsDict["Gravity Suit"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Energy Tank, Mama turtle"].AccessFrom = {
    'Main Street Bottom': lambda sm: sm.wor(sm.traverse('FishTankRight'),
                                            RomPatches.has(RomPatches.MamaTurtleBlueDoor)),
    'Mama Turtle': lambda sm: SMBool(True)
}
locationsDict["Energy Tank, Mama turtle"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Energy Tank, Mama turtle"].PostAvailable = (
    lambda sm: sm.canExitMamaTurtle()
)
locationsDict["Plasma Beam"].AccessFrom = {
    'Toilet Top': lambda sm: SMBool(True)
}
locationsDict["Plasma Beam"].Available = (
    lambda sm: Bosses.bossDead(sm, 'Draygon')
)
locationsDict["Plasma Beam"].PostAvailable = (
    lambda sm: sm.wor(sm.wand(sm.canFireChargedShots(),
                              sm.knowsKillPlasmaPiratesWithCharge(),
                              # 160/80/40 dmg * 4 ground plasma pirates
                              # => 640/320/160 damage take required
                              # check below is 1099/599/299 (give margin for taking dmg a bit)
                              # (* 4 for nerfed charge, since you need to take hits 4 times instead of one)
                              sm.energyReserveCountOk(int(10.0 * sm.getPiratesPseudoScrewCoeff()/sm.getDmgReduction(False)[0]))),
                      sm.haveItem('ScrewAttack'),
                      sm.haveItem('Plasma'))
)
locationsDict["Reserve Tank, Maridia"].AccessFrom = {
    'Left Sandpit': lambda sm: SMBool(True)
}
locationsDict["Reserve Tank, Maridia"].Available = (
    # TODO::check if it's possible suitless ?, maybe with springball jump
    lambda sm: sm.wand(sm.haveItem('Gravity'), sm.haveItem('Morph'))
)
locationsDict["Spring Ball"].AccessFrom = {
    # just fall and avoid projectiles
    'Oasis Bottom': lambda sm: SMBool(True)
}
locationsDict["Spring Ball"].Available = (
    lambda sm: sm.wand(sm.canUsePowerBombs(), # in Shaktool room to let Shaktool access the sand blocks
                   sm.haveItem('Grapple'),
                   sm.canGravLessLevel1())
)
locationsDict["Spring Ball"].PostAvailable = (
    # to go back to oasis bottom
    lambda sm: sm.canTraverseSandPits()
)
locationsDict["Energy Tank, Botwoon"].AccessFrom = {
    'Post Botwoon': lambda sm: SMBool(True)
}
locationsDict["Energy Tank, Botwoon"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Draygon"].AccessFrom = {
    'Draygon Room Bottom': lambda sm: SMBool(True)
}
locationsDict["Draygon"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Space Jump"].AccessFrom = {
    'Draygon Room Bottom': lambda sm: SMBool(True)
}
locationsDict["Space Jump"].Available = (
    # suitless is just too complicated...
    lambda sm: sm.wand(sm.haveItem('Gravity'),
                       sm.wor(sm.canFly(),
                              sm.haveItem('HiJump'),
                              sm.canSpringBallJumpFromWall()))
)
locationsDict["Space Jump"].PostAvailable = (
    lambda sm: Bosses.bossDead(sm, 'Draygon')
)
#locationsDict["Mother Brain"].AccessFrom = {
#    'Golden Four': lambda sm: Bosses.allBossesDead(sm)
#}
#locationsDict["Mother Brain"].Available = (
#    lambda sm: sm.enoughStuffTourian()
#)
locationsDict["Power Bomb (Crateria surface)"].AccessFrom = {
    'Landing Site': lambda sm: SMBool(True)
}
locationsDict["Power Bomb (Crateria surface)"].Available = (
    lambda sm: sm.wand(sm.traverse('LandingSiteTopRight'),
                       # TODO::the room is filled with acid, compute how many etanks are required
                       sm.energyReserveCountOk(10))
)
locationsDict["Power Bomb (Crateria surface)"].PostAvailable = (
    # TODO::test if with hijump and walljumps it's ok
    lambda sm: sm.canFly()
)
locationsDict["Missile (outside Wrecked Ship bottom)"].AccessFrom = {
    'West Ocean Left': lambda sm: SMBool(True)
}
locationsDict["Missile (outside Wrecked Ship bottom)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Missile (outside Wrecked Ship top)"].AccessFrom = {
    'Wrecked Ship Outside Top': lambda sm: SMBool(True)
}
locationsDict["Missile (outside Wrecked Ship top)"].Available = (
    # just jump on the enemies, then walljump on the right side of the screen from the top enemy
    lambda sm: SMBool(True)
)
locationsDict["Missile (outside Wrecked Ship middle)"].AccessFrom = {
    'Wrecked Ship Outside Top': lambda sm: SMBool(True)
}
locationsDict["Missile (outside Wrecked Ship middle)"].Available = (
    lambda sm: sm.wand(sm.haveItem('Super'),
                       sm.haveItem('Morph'),
                       # destroy the shotblock
                       sm.wor(sm.canPassBombPassages(), sm.haveItem('Wave')))
)
locationsDict["Missile (outside Wrecked Ship middle)"].PostAvailable = (
    # need to be able to break the shot block to comeback
    # (it's possible to be fast enough to comeback before the shotblock and super block reappear)
    lambda sm: sm.wor(sm.canPassBombPassages(), sm.haveItem('Wave'))
)
locationsDict["Missile (Crateria moat)"].AccessFrom = {
    'Keyhunter Room Bottom': lambda sm: sm.traverse('KihunterRight'),
    'Moat Right': lambda sm: SMBool(True)
}
locationsDict["Missile (Crateria moat)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Missile (Crateria bottom)"].AccessFrom = {
    'Landing Site': lambda sm: SMBool(True)
}
locationsDict["Missile (Crateria bottom)"].Available = (
    lambda sm: sm.canPassBombPassages()
)
locationsDict["Missile (Crateria gauntlet right)"].AccessFrom = {
     # TODO::regular gauntlet, but it's filled with acid    
#    'Landing Site': lambda sm: sm.wor(sm.wand(sm.canEnterAndLeaveGauntlet(),
#                                              sm.canPassBombPassages()),
#                                      sm.canDoLowGauntlet()),
    'Landing Site': lambda sm: sm.canUsePowerBombs(), # from gauntlet back
    'Gauntlet Top': lambda sm: SMBool(True),
    # we can shoot blocks from the back, we can kill green pirate with power bomb, so no need for more
    'Lower Mushrooms Left': lambda sm: sm.canUsePowerBombs()
}
locationsDict["Missile (Crateria gauntlet right)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Missile (Crateria gauntlet left)"].AccessFrom = {
     # TODO::regular gauntlet, but it's filled with acid
#    'Landing Site': lambda sm: sm.wor(sm.wand(sm.canEnterAndLeaveGauntlet(),
#                                              sm.canPassBombPassages()),
#                                      sm.canDoLowGauntlet()),
    'Landing Site': lambda sm: sm.canUsePowerBombs(), # from gauntlet back
    'Gauntlet Top': lambda sm: SMBool(True),
    'Lower Mushrooms Left': lambda sm: sm.canUsePowerBombs()
}
locationsDict["Missile (Crateria gauntlet left)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Super Missile (Crateria)"].AccessFrom = {
    'Landing Site': lambda sm: SMBool(True)
}
locationsDict["Super Missile (Crateria)"].Available = (
    lambda sm: sm.wand(sm.canPassBombPassages(),
                       sm.traverse("ClimbRight"),
                       sm.haveItem('SpeedBooster')) # use speedbooster to get out too
)
locationsDict["Missile (Crateria middle)"].AccessFrom = {
    'Landing Site': lambda sm: SMBool(True)
}
locationsDict["Missile (Crateria middle)"].Available = (
    # the hidden path used to comeback in vanilla requires nothing in rotation
    lambda sm: SMBool(True)
)
locationsDict["Power Bomb (green Brinstar bottom)"].AccessFrom = {
    'Etecoons Bottom': lambda sm: SMBool(True)
}
locationsDict["Power Bomb (green Brinstar bottom)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Super Missile (pink Brinstar)"].AccessFrom = {
    'Big Pink': lambda sm: sm.haveItem('Morph'),
    'Green Hill Zone Top Right': lambda sm: SMBool(True)
}
locationsDict["Super Missile (pink Brinstar)"].Available = (
                      # spore spawn
    lambda sm: sm.wor(sm.wand(sm.traverse('BigPinkTopRight'),
                              sm.enoughStuffSporeSpawn(),
                              sm.haveItem('Morph')),
                      # back way into spore spawn
                      sm.wand(sm.canOpenGreenDoors(),
                              # TODO::try with screw attack to not require morph
                              sm.canPassBombPassages()))
)
locationsDict["Super Missile (pink Brinstar)"].PostAvailable = (
    # coming back to entrance after killing spore spawn requires super + morph
    # coming back to back door requires super + canpassbombpassages
    lambda sm: sm.wand(sm.canOpenGreenDoors(),
                       # TODO::try with screw attack to not require morph
                       sm.canPassBombPassages())
)
# no technique for morph from walljump to exit after super missile (green brinstar top)
# as you have to be able to 99% finish the hack before doing rando
locationsDict["Missile (green Brinstar below super missile)"].AccessFrom = {
    'Green Brinstar Elevator': lambda sm: sm.wor(RomPatches.has(RomPatches.BrinReserveBlueDoors), sm.traverse('MainShaftRight'))
}
locationsDict["Missile (green Brinstar below super missile)"].Available = (
    # TODO::check that we can destroy the block with screwattack
    lambda sm: sm.canDestroyBombWalls()
)
#locationsDict["Missile (green Brinstar below super missile)"].PostAvailable = (
#    lambda sm: sm.wor(RomPatches.has(RomPatches.EarlySupersShotBlock), sm.canPassBombPassages())
#)
locationsDict["Super Missile (green Brinstar top)"].AccessFrom = {
    'Green Brinstar Elevator': lambda sm: sm.wor(RomPatches.has(RomPatches.BrinReserveBlueDoors), sm.traverse('MainShaftRight'))
}
locationsDict["Super Missile (green Brinstar top)"].Available = (
    lambda sm: sm.haveItem('Morph')
)
locationsDict["Missile (green Brinstar behind missile)"].AccessFrom = {
    'Green Brinstar Elevator': lambda sm: sm.wor(RomPatches.has(RomPatches.BrinReserveBlueDoors), sm.traverse('MainShaftRight'))
}
locationsDict["Missile (green Brinstar behind missile)"].Available = (
    lambda sm: sm.wand(sm.traverse('EarlySupersRight'),
                       # TODO::check with screwattack
                       sm.canDestroyBombWalls())

)
locationsDict["Missile (green Brinstar behind missile)"].PostAvailable = (
    lambda sm: sm.haveItem('Morph')

)
locationsDict["Missile (green Brinstar behind reserve tank)"].AccessFrom = {
    'Green Brinstar Elevator': lambda sm: sm.wor(RomPatches.has(RomPatches.BrinReserveBlueDoors), sm.traverse('MainShaftRight'))
}
locationsDict["Missile (green Brinstar behind reserve tank)"].Available = (
    lambda sm: sm.traverse('EarlySupersRight')
)
locationsDict["Missile (green Brinstar behind reserve tank)"].PostAvailable = (
    lambda sm: sm.haveItem('Morph')
)
locationsDict["Missile (pink Brinstar top)"].AccessFrom = {
    'Big Pink': lambda sm: SMBool(True)
}
locationsDict["Missile (pink Brinstar top)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Missile (pink Brinstar bottom)"].AccessFrom = {
    'Big Pink': lambda sm: sm.haveItem('Morph')
}
locationsDict["Missile (pink Brinstar bottom)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Power Bomb (pink Brinstar)"].AccessFrom = {
    'Big Pink': lambda sm: SMBool(True)
}
locationsDict["Power Bomb (pink Brinstar)"].Available = (
    lambda sm: sm.wand(sm.canUsePowerBombs(),
                       sm.haveItem('Super'))
)
locationsDict["Missile (green Brinstar pipe)"].AccessFrom = {
    'Green Hill Zone Top Right': lambda sm: SMBool(True)
}
locationsDict["Missile (green Brinstar pipe)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Power Bomb (blue Brinstar)"].AccessFrom = {
    'Blue Brinstar Elevator Bottom': lambda sm: SMBool(True)
}
locationsDict["Power Bomb (blue Brinstar)"].Available = (
    lambda sm: sm.canUsePowerBombs()
)
locationsDict["Missile (blue Brinstar middle)"].AccessFrom = {
    'Blue Brinstar Elevator Bottom': lambda sm: SMBool(True)
}
locationsDict["Missile (blue Brinstar middle)"].Available = (
    lambda sm: sm.wor(RomPatches.has(RomPatches.BlueBrinstarBlueDoor), sm.traverse('ConstructionZoneRight'))
)
locationsDict["Super Missile (green Brinstar bottom)"].AccessFrom = {
    'Etecoons Supers': lambda sm: SMBool(True)
}
locationsDict["Super Missile (green Brinstar bottom)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Missile (blue Brinstar bottom)"].AccessFrom = {
    'Blue Brinstar Elevator Bottom': lambda sm: SMBool(True)
}
locationsDict["Missile (blue Brinstar bottom)"].Available = (
    lambda sm: sm.haveItem('Morph')
)
locationsDict["Missile (blue Brinstar top)"].AccessFrom = {
    'Blue Brinstar Elevator Bottom': lambda sm: SMBool(True)
}
locationsDict["Missile (blue Brinstar top)"].Available = (
    lambda sm: sm.canAccessBillyMays()
)
locationsDict["Missile (blue Brinstar behind missile)"].AccessFrom = {
    'Blue Brinstar Elevator Bottom': lambda sm: SMBool(True)
}
locationsDict["Missile (blue Brinstar behind missile)"].Available = (
    lambda sm: sm.canAccessBillyMays()
)
locationsDict["Power Bomb (red Brinstar sidehopper room)"].AccessFrom = {
    'Red Brinstar Elevator': lambda sm: SMBool(True)
}
locationsDict["Power Bomb (red Brinstar sidehopper room)"].Available = (
    lambda sm: sm.wand(sm.traverse('RedTowerElevatorTopLeft'),
                       sm.canUsePowerBombs())
)
locationsDict["Power Bomb (red Brinstar spike room)"].AccessFrom = {
    'Red Brinstar Elevator': lambda sm: sm.haveItem('Morph')
}
locationsDict["Power Bomb (red Brinstar spike room)"].Available = (
    lambda sm: sm.traverse('RedTowerElevatorBottomLeft')
)
locationsDict["Missile (red Brinstar spike room)"].AccessFrom = {
    'Red Brinstar Elevator': lambda sm: sm.haveItem('Morph')
}
locationsDict["Missile (red Brinstar spike room)"].Available = (
    lambda sm: sm.wand(sm.traverse('RedTowerElevatorBottomLeft'),
                       sm.canUsePowerBombs())
)
locationsDict["Missile (Kraid)"].AccessFrom = {
    'Warehouse Zeela Room Left': lambda sm: SMBool(True)
}
locationsDict["Missile (Kraid)"].Available = (
    lambda sm: sm.canUsePowerBombs()
)
#locationsDict["Missile (lava room)"].AccessFrom = {
#    'Cathedral': lambda sm: SMBool(True)
#}
#locationsDict["Missile (lava room)"].Available = (
#    lambda sm: sm.haveItem('Morph')
#)
locationsDict["Missile (below Ice Beam)"].AccessFrom = {
    'Business Center': lambda sm: sm.wand(sm.traverse('BusinessCenterTopLeft'),
                                          sm.canUsePowerBombs(),
                                          sm.canHellRun(**Settings.hellRunsTable['Ice']['Norfair Entrance -> Ice Beam'])),
#    'Crocomire Speedway Bottom': lambda sm: sm.wand(sm.isVanillaCroc(),
#                                                    sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Croc -> Ice Missiles']),
#                                                    sm.haveItem('SpeedBooster'),
#                                                    sm.knowsIceMissileFromCroc())
}
locationsDict["Missile (below Ice Beam)"].Available = (
    lambda sm: SMBool(True)
)
#locationsDict["Missile (above Crocomire)"].AccessFrom = {
#    'Crocomire Speedway Bottom': lambda sm: sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Croc -> Grapple Escape Missiles'])
#}
#locationsDict["Missile (above Crocomire)"].Available = (
#    lambda sm: sm.canGrappleEscape()
#)
locationsDict["Missile (Hi-Jump Boots)"].AccessFrom = {
    'Business Center': lambda sm: sm.wor(RomPatches.has(RomPatches.HiJumpAreaBlueDoor), sm.traverse('BusinessCenterBottomLeft'))
}
locationsDict["Missile (Hi-Jump Boots)"].Available = (
    lambda sm: sm.canPassBombPassages()
)
locationsDict["Energy Tank (Hi-Jump Boots)"].AccessFrom = {
    'Business Center': lambda sm: sm.wor(RomPatches.has(RomPatches.HiJumpAreaBlueDoor), sm.traverse('BusinessCenterBottomLeft'))
}
locationsDict["Energy Tank (Hi-Jump Boots)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Power Bomb (Crocomire)"].AccessFrom = {
    'Crocomire Room Top': lambda sm: SMBool(True)
}
locationsDict["Power Bomb (Crocomire)"].Available = (
    lambda sm: sm.wand(sm.traverse('PostCrocomireUpperLeft'),
                       sm.enoughStuffCroc(),
                       sm.wor(sm.canFly(),
                              sm.wand(sm.haveItem('HiJump'), sm.haveItem('SpeedBooster')),
                              sm.wand(sm.haveItem('HiJump'), sm.haveItem('Ice'), sm.knowsCrocPBsIce())))
)
locationsDict["Missile (below Crocomire)"].AccessFrom = {
    'Crocomire Room Top': lambda sm: SMBool(True)
}
locationsDict["Missile (below Crocomire)"].Available = (
    # door was blue
    lambda sm: sm.wand(sm.traverse('PostCrocomireShaftRight'),
                       sm.enoughStuffCroc())
)
locationsDict["Missile (below Crocomire)"].PostAvailable = (
    # TODO::room is full of acid, ask for both suits and energy to climb
    # TODO::create and use acid bath tables
    lambda sm: sm.wand(sm.haveItem('Gravity'), sm.haveItem('Varia'),
                       sm.energyReserveCountOk(4))
)
locationsDict["Missile (Grapple Beam)"].AccessFrom = {
    'Crocomire Room Top': lambda sm: SMBool(True)
}
locationsDict["Missile (Grapple Beam)"].Available = (
    lambda sm: sm.wand(sm.enoughStuffCroc(),
                       # there's acid all other the place.
                       # TODO::change energy requirement depending on the suits and beams (for annoying enemies)
                       sm.energyReserveCountOk(10))
)
#locationsDict["Missile (Norfair Reserve Tank)"].AccessFrom = {
#    'Bubble Mountain': lambda sm: sm.canEnterNorfairReserveAreaFromBubbleMoutain(),
#    'Bubble Mountain Top': lambda sm: sm.canEnterNorfairReserveAreaFromBubbleMoutainTop()
#}
#locationsDict["Missile (Norfair Reserve Tank)"].Available = (
#    lambda sm: sm.wand(sm.haveItem('Morph'), sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Norfair Reserve']))
#)
locationsDict["Missile (bubble Norfair green door)"].AccessFrom = {
    'Bubble Mountain': lambda sm: sm.canEnterNorfairReserveAreaFromBubbleMoutain()
}
locationsDict["Missile (bubble Norfair green door)"].Available = (
    lambda sm: sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Norfair Reserve Missiles'])
)
locationsDict["Missile (bubble Norfair)"].AccessFrom = {
    'Bubble Mountain': lambda sm: SMBool(True)
}
locationsDict["Missile (bubble Norfair)"].Available = (
    lambda sm: sm.canPassBombPassages()
)
locationsDict["Missile (Speed Booster)"].AccessFrom = {
    'Bubble Mountain Top': lambda sm: sm.wand(sm.wor(RomPatches.has(RomPatches.SpeedAreaBlueDoors),
                                                     sm.traverse('BubbleMountainTopRight')),
                                              sm.haveItem('Morph'))
}
locationsDict["Missile (Speed Booster)"].Available = (
    # fall
    lambda sm: sm.canFallToSpeedBooster()
)
locationsDict["Missile (Speed Booster)"].PostAvailable = (
    # get back all the way up
    lambda sm: sm.wand(sm.canGetBackFromSpeedBooster(),
                       # can't just roll out of the hole
                       sm.canMorphJump())
)
locationsDict["Missile (Wave Beam)"].AccessFrom = {
    'Bubble Mountain Top': lambda sm: sm.canAccessDoubleChamberItems()
}
locationsDict["Missile (Wave Beam)"].Available = (
    lambda sm: SMBool(True)
)
#locationsDict["Missile (Gold Torizo)"].AccessFrom = {
#    'LN Above GT': lambda sm: SMBool(True)
#}
#locationsDict["Missile (Gold Torizo)"].Available = (
#    lambda sm: sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main'])
#)
#locationsDict["Missile (Gold Torizo)"].PostAvailable = (
#    lambda sm: sm.enoughStuffGT()
#)
#locationsDict["Super Missile (Gold Torizo)"].AccessFrom = {
#    'Screw Attack Bottom': lambda sm: SMBool(True)
#}
#locationsDict["Super Missile (Gold Torizo)"].Available = (
#    lambda sm: SMBool(True)
#)
#locationsDict["Super Missile (Gold Torizo)"].PostAvailable = (
#    lambda sm: sm.enoughStuffGT()
#)
#locationsDict["Missile (Mickey Mouse room)"].AccessFrom = {
#    'LN Entrance': lambda sm: sm.wand(sm.canUsePowerBombs(), sm.canPassWorstRoom()),
#}
#locationsDict["Missile (Mickey Mouse room)"].Available = (
#    lambda sm: sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main'])
#)
#locationsDict["Missile (lower Norfair above fire flea room)"].AccessFrom = {
#    'Firefleas': lambda sm: sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main'])
#}
#locationsDict["Missile (lower Norfair above fire flea room)"].Available = (
#    lambda sm: SMBool(True)
#)
#locationsDict["Power Bomb (lower Norfair above fire flea room)"].AccessFrom = {
#    'Firefleas Top': lambda sm: SMBool(True)
#}
#locationsDict["Power Bomb (lower Norfair above fire flea room)"].Available = (
#    lambda sm: SMBool(True)
#)
#locationsDict["Power Bomb (Power Bombs of shame)"].AccessFrom = {
#    'Ridley Zone': lambda sm: sm.canUsePowerBombs()
#}
#locationsDict["Power Bomb (Power Bombs of shame)"].Available = (
#    lambda sm: sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main'])
#)
#locationsDict["Missile (lower Norfair near Wave Beam)"].AccessFrom = {
#    'Firefleas': lambda sm: SMBool(True)
#}
#locationsDict["Missile (lower Norfair near Wave Beam)"].Available = (
#    lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
#                       sm.canDestroyBombWalls(),
#                       sm.haveItem('Morph'))
#)
locationsDict["Missile (Wrecked Ship middle)"].AccessFrom = {
    'Wrecked Ship Main': lambda sm: SMBool(True)
}
locationsDict["Missile (Wrecked Ship middle)"].Available = (
    # TODO::check with screwattack
    lambda sm: sm.canPassBombPassages()
)
locationsDict["Missile (Gravity Suit)"].AccessFrom = {
    'Wrecked Ship Outside Top': lambda sm: sm.haveItem('Morph')
}
locationsDict["Missile (Gravity Suit)"].Available = (
    lambda sm: sm.canMorphJump()
)
locationsDict["Missile (Wrecked Ship top)"].AccessFrom = {
    'Wrecked Ship Main': lambda sm: sm.wand(sm.haveItem('Morph'),
                                            # to kill all enemies in attic
                                            sm.canClimbAttic(),
                                            Bosses.bossDead(sm, 'Phantoon'))
}
locationsDict["Missile (Wrecked Ship top)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Super Missile (Wrecked Ship left)"].AccessFrom = {
    'Wrecked Ship Main': lambda sm: SMBool(True)
}
locationsDict["Super Missile (Wrecked Ship left)"].Available = (
    lambda sm: Bosses.bossDead(sm, 'Phantoon')
)
locationsDict["Missile (green Maridia shinespark)"].AccessFrom = {
    'Main Street Bottom': lambda sm: SMBool(True)
}
locationsDict["Missile (green Maridia shinespark)"].Available = (
    lambda sm: sm.wand(sm.haveItem('Gravity'),
                       sm.haveItem('SpeedBooster'),
                       # speedball required
                       sm.knowsShortCharge())
)
locationsDict["Super Missile (green Maridia)"].AccessFrom = {
    'Main Street Bottom': lambda sm: sm.canGravLessLevel1()
}
locationsDict["Super Missile (green Maridia)"].Available = (
    lambda sm: sm.wand(sm.haveItem('Morph'),
                       sm.canGravLessLevel1(),
                       # hijump required when suitless & hard to avoid the crab when suitless
                       sm.wor(sm.haveItem('Gravity'),
                              sm.wand(sm.haveItem('HiJump'), sm.itemCountOk('ETank', 1))))
)
locationsDict["Missile (green Maridia tatori)"].AccessFrom = {
    # it's possible to crounched jump over the pink pirate when suitless without taking damage
    'Main Street Bottom': lambda sm: sm.wand(sm.wor(sm.traverse('FishTankRight'),
                                                    RomPatches.has(RomPatches.MamaTurtleBlueDoor))),
    'Mama Turtle': lambda sm: SMBool(True)
}
locationsDict["Missile (green Maridia tatori)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Missile (green Maridia tatori)"].PostAvailable = (
    lambda sm: sm.canExitMamaTurtle()
)
locationsDict["Super Missile (yellow Maridia)"].AccessFrom = {
    'Watering Hole Bottom': lambda sm: SMBool(True)
}
locationsDict["Super Missile (yellow Maridia)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Missile (yellow Maridia super missile)"].AccessFrom = {
    'Watering Hole Bottom': lambda sm: SMBool(True)
}
locationsDict["Missile (yellow Maridia super missile)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Missile (yellow Maridia false wall)"].AccessFrom = {
    'Beach': lambda sm: SMBool(True)
}
locationsDict["Missile (yellow Maridia false wall)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Missile (yellow Maridia false wall)"].PostAvailable = (
    lambda sm: sm.haveItem('Gravity')
)
locationsDict["Missile (left Maridia sand pit room)"].AccessFrom = {
    'Left Sandpit': lambda sm: SMBool(True)
}
locationsDict["Missile (left Maridia sand pit room)"].Available = (
    # TODO::check if it's possible suitless ?, maybe with springball jump
    lambda sm: sm.wand(sm.haveItem('Gravity'), sm.haveItem('Morph'))
)
locationsDict["Missile (right Maridia sand pit room)"].AccessFrom = {
    'Right Sandpit': lambda sm: SMBool(True)
}
locationsDict["Missile (right Maridia sand pit room)"].Available = (
    lambda sm: sm.wand(sm.wor(sm.haveItem('Gravity'),
                              # suitless with just hijump is enough
                              # TODO::check with springball jump
                              sm.wand(sm.knowsGravLessLevel1(), sm.haveItem('HiJump'))),
                       sm.haveItem('Morph'))
)
locationsDict["Missile (right Maridia sand pit room)"].PostAvailable = (
    lambda sm: sm.canMorphJump()
)
locationsDict["Power Bomb (right Maridia sand pit room)"].AccessFrom = {
    'Right Sandpit': lambda sm: SMBool(True)
}
locationsDict["Power Bomb (right Maridia sand pit room)"].Available = (
    lambda sm: sm.wand(sm.haveItem('Morph'),
                       sm.canGravLessLevel1())
)
locationsDict["Missile (pink Maridia)"].AccessFrom = {
    'Aqueduct': lambda sm: SMBool(True)
}
locationsDict["Missile (pink Maridia)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Super Missile (pink Maridia)"].AccessFrom = {
    'Aqueduct': lambda sm: SMBool(True)
}
locationsDict["Super Missile (pink Maridia)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Missile (Draygon)"].AccessFrom = {
    'Precious Room Top': lambda sm: SMBool(True)
}
locationsDict["Missile (Draygon)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Missile (Draygon)"].PostAvailable = (
    lambda sm: sm.canGravLessLevel1()
)

# TODO::use the dict in solver/randomizer
# create the list that the solver/randomizer use
locations = [loc for loc in locationsDict.values()]

class LocationsHelper:
    # used by FillerRandom to know how many front fill steps it must perform
    def getRandomFillHelp(startLocation):
        return 0

    def getStartMajors(startLocation):
        return ([],[],0,0)
