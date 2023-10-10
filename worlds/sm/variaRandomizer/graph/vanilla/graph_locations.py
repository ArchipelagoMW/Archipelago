from ...logic.helpers import Bosses
from ...utils.parameters import Settings
from ...rom.rom_patches import RomPatches
from ...logic.smbool import SMBool
from ...graph.location import locationsDict

locationsDict["Energy Tank, Gauntlet"].AccessFrom = {
    'Landing Site': lambda sm: SMBool(True)
}
locationsDict["Energy Tank, Gauntlet"].Available = (
    lambda sm: sm.wor(sm.canEnterAndLeaveGauntlet(),
                      sm.wand(sm.canShortCharge(),
                              sm.canEnterAndLeaveGauntletQty(1, 0)), # thanks ponk! https://youtu.be/jil5zTBCF1s
                      sm.canDoLowGauntlet())
)
locationsDict["Bomb"].AccessFrom = {
    'Landing Site': lambda sm: SMBool(True)
}
locationsDict["Bomb"].Available = (
    lambda sm: sm.wand(sm.haveItem('Morph'),
                       sm.traverse('FlywayRight'))
)
locationsDict["Bomb"].PostAvailable = (
    lambda sm: sm.wor(sm.knowsAlcatrazEscape(),
                      sm.canPassBombPassages())
)
locationsDict["Energy Tank, Terminator"].AccessFrom = {
    'Landing Site': lambda sm: sm.canPassTerminatorBombWall(),
    'Lower Mushrooms Left': lambda sm: sm.canPassCrateriaGreenPirates(),
    'Gauntlet Top': lambda sm: sm.haveItem('Morph')
}
locationsDict["Energy Tank, Terminator"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Reserve Tank, Brinstar"].AccessFrom = {
    'Green Brinstar Elevator': lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.BrinReserveBlueDoors), sm.traverse('MainShaftRight'))
}
locationsDict["Reserve Tank, Brinstar"].Available = (
    lambda sm: sm.wand(sm.wor(sm.canMockball(),
                              sm.haveItem('SpeedBooster')),
                       sm.wor(RomPatches.has(sm.player, RomPatches.BrinReserveBlueDoors), sm.traverse('EarlySupersRight')))
)
locationsDict["Charge Beam"].AccessFrom = {
    'Big Pink': lambda sm: SMBool(True)
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
    'Blue Brinstar Elevator Bottom': lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.BlueBrinstarBlueDoor), sm.traverse('ConstructionZoneRight'))
}
locationsDict["Energy Tank, Brinstar Ceiling"].Available = (

    lambda sm: sm.wor(sm.knowsCeilingDBoost(),
                      sm.canFly(),
                      sm.wor(sm.haveItem('HiJump'),
                             sm.haveItem('Ice'),
                             sm.wand(sm.canUsePowerBombs(),
                                     sm.haveItem('SpeedBooster')),
                             sm.canSimpleShortCharge()))
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
                       sm.haveItem('SpeedBooster'),
                       sm.wor(sm.haveItem('Gravity'),
                              sm.canSimpleShortCharge())) # from the blocks above the water
)
locationsDict["Energy Tank, Brinstar Gate"].AccessFrom = {
    'Big Pink': lambda sm: SMBool(True)
}
locationsDict["Energy Tank, Brinstar Gate"].Available = (
    lambda sm: sm.wand(sm.traverse('BigPinkRight'),
                       sm.wor(sm.haveItem('Wave'),
                              sm.wand(sm.haveItem('Super'),
                                      sm.haveItem('HiJump'),
                                      sm.knowsReverseGateGlitch()),
                              sm.wand(sm.haveItem('Super'),
                                      sm.knowsReverseGateGlitchHiJumpLess())))
)
locationsDict["X-Ray Scope"].AccessFrom = {
    'Red Tower Top Left': lambda sm: SMBool(True)
}
locationsDict["X-Ray Scope"].Available = (
    lambda sm: sm.wand(sm.canUsePowerBombs(),
                       sm.traverse('RedTowerLeft'),
                       sm.traverse('RedBrinstarFirefleaLeft'),
                       sm.wor(sm.haveItem('Grapple'),
                              sm.haveItem('SpaceJump'),
                              sm.wand(sm.energyReserveCountOkHardRoom('X-Ray'),
                                      sm.wor(sm.knowsXrayDboost(),
                                             sm.wand(sm.haveItem('Ice'),
                                                     sm.wor(sm.haveItem('HiJump'), sm.knowsXrayIce())),
                                             sm.canInfiniteBombJump(),
                                             sm.wand(sm.haveItem('HiJump'),
                                                     sm.wor(sm.haveItem('SpeedBooster'),
                                                            sm.canSpringBallJump()))))))
)
locationsDict["Spazer"].AccessFrom = {
    'East Tunnel Right': lambda sm: SMBool(True)
}
locationsDict["Spazer"].Available = (
    lambda sm: sm.wand(sm.traverse('BelowSpazerTopRight'),
                       sm.wor(sm.canPassBombPassages(),
                              sm.wand(sm.haveItem('Morph'),
                                      RomPatches.has(sm.player, RomPatches.SpazerShotBlock))))
)
locationsDict["Energy Tank, Kraid"].AccessFrom = {
    'Warehouse Zeela Room Left': lambda sm: SMBool(True)
}
locationsDict["Energy Tank, Kraid"].Available = (
    lambda sm: sm.wand(Bosses.bossDead(sm, 'Kraid'),
                       # kill the beetoms to unlock the door to get out
                       sm.canKillBeetoms())
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
                       sm.wor(sm.canPassBombPassages(), # to exit, or if you fail entrance
                              sm.wand(sm.haveItem('Ice'), # harder strat
                                      sm.haveItem('Morph'),
                                      sm.knowsIceEscape())),
                       sm.wor(sm.wand(sm.haveItem('Morph'),
                                      sm.knowsMockball()),
                              sm.haveItem('SpeedBooster')))
)
locationsDict["Energy Tank, Crocomire"].AccessFrom = {
    'Crocomire Room Top': lambda sm: SMBool(True)
}
locationsDict["Energy Tank, Crocomire"].Available = (
    lambda sm: sm.wand(sm.haveItem('Crocomire'),
                       sm.wor(sm.haveItem('Grapple'),
                              sm.haveItem('SpaceJump'),
                              sm.energyReserveCountOk(3/sm.getDmgReduction()[0])))
)
locationsDict["Hi-Jump Boots"].AccessFrom = {
    'Business Center': lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.HiJumpAreaBlueDoor), sm.traverse('BusinessCenterBottomLeft'))
}
locationsDict["Hi-Jump Boots"].Available = (
    lambda sm: sm.haveItem('Morph')
)
locationsDict["Hi-Jump Boots"].PostAvailable = (
    lambda sm: sm.wor(sm.canPassBombPassages(),
                      sm.wand(sm.haveItem('Morph'), RomPatches.has(sm.player, RomPatches.HiJumpShotBlock)))
)
locationsDict["Grapple Beam"].AccessFrom = {
    'Crocomire Room Top': lambda sm: SMBool(True)
}
locationsDict["Grapple Beam"].Available = (
    lambda sm: sm.wand(sm.haveItem('Crocomire'),
                       sm.wor(sm.wand(sm.haveItem('Morph'),
                                      sm.canFly()),
                              sm.wand(sm.haveItem('SpeedBooster'),
                                      sm.wor(sm.knowsShortCharge(),
                                             sm.canUsePowerBombs())),
                              sm.wand(sm.haveItem('Morph'),
                                      sm.wor(sm.haveItem('SpeedBooster'),
                                             sm.canSpringBallJump()),
                                      sm.haveItem('HiJump')), # jump from the yellow plateform ennemy
                              sm.canGreenGateGlitch()))
)
locationsDict["Grapple Beam"].PostAvailable = (
    lambda sm: sm.wor(sm.haveItem('Morph'), # regular exit
                      sm.wand(sm.haveItem('Super'), # grapple escape reverse
                              sm.wor(sm.canFly(), # Grapple Tutorial Room 2
                                     sm.haveItem('HiJump'),
                                     sm.haveItem('Grapple')),
                              sm.wor(sm.haveItem('Gravity'), # Grapple Tutorial Room 3
                                     sm.haveItem('SpaceJump'),
                                     sm.haveItem('Grapple'))))
)
locationsDict["Reserve Tank, Norfair"].AccessFrom = {
    'Bubble Mountain': lambda sm: sm.canEnterNorfairReserveAreaFromBubbleMoutain(),
    'Bubble Mountain Top': lambda sm: sm.canEnterNorfairReserveAreaFromBubbleMoutainTop(),
}
locationsDict["Reserve Tank, Norfair"].Available = (
    lambda sm: sm.wand(sm.haveItem('Morph'), sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Norfair Reserve']))
)
locationsDict["Speed Booster"].AccessFrom = {
    'Bubble Mountain Top': lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.SpeedAreaBlueDoors),
                                             sm.wand(sm.traverse('BubbleMountainTopRight'),
                                                     sm.traverse('SpeedBoosterHallRight')))
}
locationsDict["Speed Booster"].Available = (
    lambda sm: sm.canHellRunToSpeedBooster()
)
locationsDict["Wave Beam"].AccessFrom = {
    'Bubble Mountain Top': lambda sm: sm.canAccessDoubleChamberItems()
}
locationsDict["Wave Beam"].Available = (
    lambda sm: sm.traverse('DoubleChamberRight')
)
locationsDict["Wave Beam"].PostAvailable = (
    lambda sm: sm.canExitWaveBeam()
)
locationsDict["Ridley"].AccessFrom = {
    'RidleyRoomIn': lambda sm: SMBool(True)
}
locationsDict["Ridley"].Available = (
    lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']), sm.enoughStuffsRidley())
)
locationsDict["Energy Tank, Ridley"].AccessFrom = {
    'RidleyRoomIn': lambda sm: sm.wand(sm.haveItem('Ridley'), sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']))
}
locationsDict["Energy Tank, Ridley"].Available = (
    lambda sm: sm.haveItem('Morph')
)
locationsDict["Screw Attack"].AccessFrom = {
    'Screw Attack Bottom': lambda sm: SMBool(True)
}
locationsDict["Screw Attack"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Screw Attack"].PostAvailable = (
    lambda sm: sm.canExitScrewAttackArea()
)
locationsDict["Energy Tank, Firefleas"].AccessFrom = {
    'Firefleas': lambda sm: SMBool(True)
}
locationsDict["Energy Tank, Firefleas"].Available = (
    lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.FirefleasRemoveFune),
                      # get past the fune
                                     sm.haveItem('Super'),
                      sm.canPassBombPassages(),
                      sm.canUseSpringBall())
)
locationsDict["Energy Tank, Firefleas"].PostAvailable = (
    lambda sm: sm.wor(sm.knowsFirefleasWalljump(),
                      sm.wor(sm.haveItem('Ice'),
                             sm.haveItem('HiJump'),
                             sm.canFly(),
                             sm.canSpringBallJump()))
)
locationsDict["Reserve Tank, Wrecked Ship"].AccessFrom = {
    'Wrecked Ship Main': lambda sm: SMBool(True)
}
locationsDict["Reserve Tank, Wrecked Ship"].Available = (
    lambda sm: sm.wand(sm.canUsePowerBombs(),
                       sm.haveItem('SpeedBooster'),
                       sm.canPassBowling())
)
locationsDict["Energy Tank, Wrecked Ship"].AccessFrom = {
    'Wrecked Ship Back': lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.WsEtankBlueDoor),
                                           sm.traverse('ElectricDeathRoomTopLeft'))
}
locationsDict["Energy Tank, Wrecked Ship"].Available = (
    lambda sm: sm.wor(Bosses.bossDead(sm, 'Phantoon'),
                      RomPatches.has(sm.player, RomPatches.WsEtankPhantoonAlive))
)
locationsDict["Phantoon"].AccessFrom = {
    'PhantoonRoomIn': lambda sm: SMBool(True)
}
locationsDict["Phantoon"].Available = (
    lambda sm: sm.enoughStuffsPhantoon()
)
locationsDict["Right Super, Wrecked Ship"].AccessFrom = {
    'Wrecked Ship Main': lambda sm: Bosses.bossDead(sm, 'Phantoon')
}
locationsDict["Right Super, Wrecked Ship"].Available = (
    lambda sm: sm.canPassBombPassages()
)
locationsDict["Gravity Suit"].AccessFrom = {
    'Wrecked Ship Main': lambda sm: SMBool(True)
}
locationsDict["Gravity Suit"].Available = (
    lambda sm: sm.wand(sm.canPassBombPassages(),
                       sm.canPassBowling())
)
locationsDict["Energy Tank, Mama turtle"].AccessFrom = {
    'Main Street Bottom': lambda sm: sm.wand(sm.canDoOuterMaridia(),
                                             sm.wor(sm.traverse('FishTankRight'),
                                                    RomPatches.has(sm.player, RomPatches.MamaTurtleBlueDoor)),
                                             sm.wor(sm.wor(sm.canFly(),
                                                           sm.wand(sm.haveItem('Gravity'),
                                                                   sm.haveItem('SpeedBooster')),
                                                           sm.wand(sm.haveItem('HiJump'),
                                                                   sm.haveItem('SpeedBooster'),
                                                                   sm.knowsHiJumpMamaTurtle())),
                                                    sm.wor(sm.wand(sm.canUseSpringBall(),
                                                                   sm.wor(sm.wand(sm.haveItem('HiJump'),
                                                                                  sm.knowsSpringBallJump()),
                                                                          sm.knowsSpringBallJumpFromWall())),
                                                           sm.haveItem('Grapple')))),
    'Mama Turtle': lambda sm: SMBool(True)
}
locationsDict["Energy Tank, Mama turtle"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Plasma Beam"].AccessFrom = {
    'Toilet Top': lambda sm: SMBool(True)
}
locationsDict["Plasma Beam"].Available = (
    lambda sm: Bosses.bossDead(sm, 'Draygon')
)
locationsDict["Plasma Beam"].PostAvailable = (
    lambda sm: sm.wand(sm.wor(sm.wand(sm.canShortCharge(),
                                      sm.knowsKillPlasmaPiratesWithSpark()),
                              sm.wand(sm.canFireChargedShots(),
                                      sm.knowsKillPlasmaPiratesWithCharge(),
                                      # 160/80/40 dmg * 4 ground plasma pirates
                                      # => 640/320/160 damage take required
                                      # check below is 1099/599/299 (give margin for taking dmg a bit)
                                      # (* 4 for nerfed charge, since you need to take hits 4 times instead of one)
                                                       sm.energyReserveCountOk(int(10.0 * sm.getPiratesPseudoScrewCoeff()/sm.getDmgReduction(False)[0]))),
                              sm.haveItem('ScrewAttack'),
                              sm.haveItem('Plasma')),
                       sm.wor(sm.canFly(),
                              sm.wand(sm.haveItem('HiJump'),
                                      sm.knowsGetAroundWallJump()),
                              sm.canShortCharge(),
                              sm.wand(sm.canSpringBallJump(),
                                      sm.knowsSpringBallJumpFromWall())))
)
locationsDict["Reserve Tank, Maridia"].AccessFrom = {
    'Left Sandpit': lambda sm: sm.canClimbWestSandHole()
}
locationsDict["Reserve Tank, Maridia"].Available = (
    lambda sm: sm.canAccessItemsInWestSandHole()
)
locationsDict["Spring Ball"].AccessFrom = {
    'Oasis Bottom': lambda sm: sm.canTraverseSandPits()
}
locationsDict["Spring Ball"].Available = (
    lambda sm: sm.wand(sm.canAccessShaktoolFromPantsRoom(),
                       sm.canUsePowerBombs(), # in Shaktool room to let Shaktool access the sand blocks
                       sm.wor(sm.haveItem('Gravity'), sm.canUseSpringBall())) # acess the item in spring ball room
)
locationsDict["Spring Ball"].PostAvailable = (
    lambda sm: sm.wor(sm.wand(sm.haveItem('Gravity'),
                              sm.wor(sm.haveItem('HiJump'),
                                     sm.canFly(),
                                     sm.knowsMaridiaWallJumps())),
                      sm.canSpringBallJump())
)
locationsDict["Energy Tank, Botwoon"].AccessFrom = {
    'Post Botwoon': lambda sm: sm.canJumpUnderwater()
}
locationsDict["Energy Tank, Botwoon"].Available = (
    lambda sm: sm.haveItem('Morph')
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
    lambda sm: SMBool(True)
)
locationsDict["Space Jump"].PostAvailable = (
    lambda sm: Bosses.bossDead(sm, 'Draygon')
)
locationsDict["Mother Brain"].AccessFrom = {
    'Golden Four': lambda sm: sm.canPassG4()
}
locationsDict["Mother Brain"].Available = (
    lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.NoTourian),
                      sm.enoughStuffTourian())
)
locationsDict["Spore Spawn"].AccessFrom = {
    'Big Pink': lambda sm: SMBool(True)
}
locationsDict["Spore Spawn"].Available = (
    lambda sm: sm.wand(sm.traverse('BigPinkTopRight'),
                       sm.enoughStuffSporeSpawn())
)
locationsDict["Botwoon"].AccessFrom = {
    'Aqueduct Bottom': lambda sm: sm.canJumpUnderwater()
}
locationsDict["Botwoon"].Available = (
    # includes botwoon hallway conditions
    lambda sm: sm.canDefeatBotwoon()
)
locationsDict["Crocomire"].AccessFrom = {
    'Crocomire Room Top': lambda sm: SMBool(True)
}
locationsDict["Crocomire"].Available = (
    lambda sm: sm.enoughStuffCroc()
)
locationsDict["Golden Torizo"].AccessFrom = {
    'Screw Attack Bottom': lambda sm: SMBool(True)
}
locationsDict["Golden Torizo"].Available = (
    lambda sm: sm.enoughStuffGT()
)
locationsDict["Power Bomb (Crateria surface)"].AccessFrom = {
    'Landing Site': lambda sm: SMBool(True)
}
locationsDict["Power Bomb (Crateria surface)"].Available = (
    lambda sm: sm.wand(sm.traverse('LandingSiteTopRight'),
                       sm.wor(sm.haveItem('SpeedBooster'),
                              sm.canFly()))
)
locationsDict["Missile (outside Wrecked Ship bottom)"].AccessFrom = {
    'West Ocean Left': lambda sm: SMBool(True)
}
locationsDict["Missile (outside Wrecked Ship bottom)"].Available = (
    lambda sm: sm.haveItem('Morph')
)
locationsDict["Missile (outside Wrecked Ship bottom)"].PostAvailable = (
    lambda sm: sm.canPassBombPassages()
)
locationsDict["Missile (outside Wrecked Ship top)"].AccessFrom = {
    'Wrecked Ship Main': lambda sm: SMBool(True)
}
locationsDict["Missile (outside Wrecked Ship top)"].Available = (
    lambda sm: Bosses.bossDead(sm, 'Phantoon')
)
locationsDict["Missile (outside Wrecked Ship middle)"].AccessFrom = {
    'Wrecked Ship Main': lambda sm: SMBool(True)
}
locationsDict["Missile (outside Wrecked Ship middle)"].Available = (
    lambda sm: sm.wand(sm.haveItem('Super'), sm.haveItem('Morph'), Bosses.bossDead(sm, 'Phantoon'))
)
locationsDict["Missile (Crateria moat)"].AccessFrom = {
    'Moat Left': lambda sm: SMBool(True)
}
locationsDict["Missile (Crateria moat)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Missile (Crateria bottom)"].AccessFrom = {
    'Landing Site': lambda sm: SMBool(True)
}
locationsDict["Missile (Crateria bottom)"].Available = (
    lambda sm: sm.wor(sm.canDestroyBombWalls(),
                      sm.wand(sm.haveItem('SpeedBooster'),
                              sm.knowsOldMBWithSpeed()))
)
locationsDict["Missile (Crateria gauntlet right)"].AccessFrom = {
    'Landing Site': lambda sm: sm.wor(sm.wand(sm.canEnterAndLeaveGauntlet(),
                                              sm.canPassBombPassages()),
                                      sm.canDoLowGauntlet()),
    'Gauntlet Top': lambda sm: SMBool(True)
}
locationsDict["Missile (Crateria gauntlet right)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Missile (Crateria gauntlet left)"].AccessFrom = {
    'Landing Site': lambda sm: sm.wor(sm.wand(sm.canEnterAndLeaveGauntlet(),
                                              sm.canPassBombPassages()),
                                      sm.canDoLowGauntlet()),
    'Gauntlet Top': lambda sm: SMBool(True)
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
                       sm.haveItem('SpeedBooster'),
                       # reserves are hard to trigger midspark when not having ETanks
                                      sm.wor(sm.wand(sm.energyReserveCountOk(2), sm.itemCountOk('ETank', 1)), # need energy to get out
                                             sm.wand(sm.itemCountOk('ETank', 1),
                                                     sm.wor(sm.haveItem('Grapple'), # use grapple/space or dmg protection to get out
                                                            sm.haveItem('SpaceJump'),
                                                            sm.heatProof()))),
                       sm.wor(sm.haveItem('Ice'),
                              sm.wand(sm.canSimpleShortCharge(), sm.canUsePowerBombs()))) # there's also a dboost involved in simple short charge or you have to kill the yellow enemies with some power bombs
)
locationsDict["Missile (Crateria middle)"].AccessFrom = {
    'Landing Site': lambda sm: SMBool(True)
}
locationsDict["Missile (Crateria middle)"].Available = (
    lambda sm: sm.canPassBombPassages()
)
locationsDict["Power Bomb (green Brinstar bottom)"].AccessFrom = {
    'Etecoons Bottom': lambda sm: SMBool(True)
}
locationsDict["Power Bomb (green Brinstar bottom)"].Available = (
    lambda sm: sm.wand(sm.haveItem('Morph'),
                       sm.canKillBeetoms())
)
locationsDict["Super Missile (pink Brinstar)"].AccessFrom = {
    'Big Pink': lambda sm: SMBool(True)
}
locationsDict["Super Missile (pink Brinstar)"].Available = (
    lambda sm: sm.wor(sm.wand(sm.traverse('BigPinkTopRight'),
                              sm.haveItem('SporeSpawn')),
                      # back way into spore spawn
                      sm.wand(sm.canOpenGreenDoors(),
                              sm.canPassBombPassages()))
)
locationsDict["Super Missile (pink Brinstar)"].PostAvailable = (
    lambda sm: sm.wand(sm.canOpenGreenDoors(),
                       sm.canPassBombPassages())
)
locationsDict["Missile (green Brinstar below super missile)"].AccessFrom = {
    'Green Brinstar Elevator': lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.BrinReserveBlueDoors), sm.traverse('MainShaftRight'))
}
locationsDict["Missile (green Brinstar below super missile)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Missile (green Brinstar below super missile)"].PostAvailable = (
    lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.EarlySupersShotBlock), sm.canPassBombPassages())
)
locationsDict["Super Missile (green Brinstar top)"].AccessFrom = {
    'Green Brinstar Elevator': lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.BrinReserveBlueDoors), sm.traverse('MainShaftRight'))
}
locationsDict["Super Missile (green Brinstar top)"].Available = (
    lambda sm: sm.wor(sm.canMockball(),
                      sm.haveItem('SpeedBooster'))
)
locationsDict["Missile (green Brinstar behind missile)"].AccessFrom = {
    'Green Brinstar Elevator': lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.BrinReserveBlueDoors), sm.traverse('MainShaftRight'))
}
locationsDict["Missile (green Brinstar behind missile)"].Available = (
    lambda sm: sm.wand(sm.haveItem('Morph'),
                       sm.wor(sm.canMockball(),
                              sm.haveItem('SpeedBooster')),
                       sm.traverse('EarlySupersRight'),
                       sm.wor(sm.canPassBombPassages(),
                              sm.wand(sm.knowsRonPopeilScrew(),
                                      sm.haveItem('ScrewAttack'))))
)
locationsDict["Missile (green Brinstar behind reserve tank)"].AccessFrom = {
    'Green Brinstar Elevator': lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.BrinReserveBlueDoors), sm.traverse('MainShaftRight'))
}
locationsDict["Missile (green Brinstar behind reserve tank)"].Available = (
    lambda sm: sm.wand(sm.traverse('EarlySupersRight'),
                       sm.haveItem('Morph'),
                       sm.wor(sm.canMockball(),
                              sm.haveItem('SpeedBooster')))
)
locationsDict["Missile (pink Brinstar top)"].AccessFrom = {
    'Big Pink': lambda sm: SMBool(True)
}
locationsDict["Missile (pink Brinstar top)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Missile (pink Brinstar bottom)"].AccessFrom = {
    'Big Pink': lambda sm: SMBool(True)
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
    lambda sm: sm.haveItem('Morph')
)
locationsDict["Power Bomb (blue Brinstar)"].AccessFrom = {
    'Blue Brinstar Elevator Bottom': lambda sm: sm.canUsePowerBombs(),
    'Morph Ball Room Left': lambda sm: sm.wor(sm.canPassBombPassages(),
                                              sm.wand(sm.haveItem('Morph'),
                                                      sm.canShortCharge())) # speedball
}
locationsDict["Power Bomb (blue Brinstar)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Missile (blue Brinstar middle)"].AccessFrom = {
    'Blue Brinstar Elevator Bottom': lambda sm: SMBool(True)
}
locationsDict["Missile (blue Brinstar middle)"].Available = (
    lambda sm: sm.wand(sm.wor(RomPatches.has(sm.player, RomPatches.BlueBrinstarMissile), sm.haveItem('Morph')),
                       sm.wor(RomPatches.has(sm.player, RomPatches.BlueBrinstarBlueDoor), sm.traverse('ConstructionZoneRight')))
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
    'Red Brinstar Elevator': lambda sm: SMBool(True)
}
locationsDict["Power Bomb (red Brinstar spike room)"].Available = (
    lambda sm: sm.traverse('RedTowerElevatorBottomLeft')
)
locationsDict["Missile (red Brinstar spike room)"].AccessFrom = {
    'Red Brinstar Elevator': lambda sm: SMBool(True)
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
locationsDict["Missile (lava room)"].AccessFrom = {
    'Cathedral': lambda sm: SMBool(True)
}
locationsDict["Missile (lava room)"].Available = (
    lambda sm: sm.haveItem('Morph')
)
locationsDict["Missile (below Ice Beam)"].AccessFrom = {
    'Business Center': lambda sm: sm.wand(sm.traverse('BusinessCenterTopLeft'),
                                          sm.canUsePowerBombs(),
                                          sm.canHellRun(**Settings.hellRunsTable['Ice']['Norfair Entrance -> Ice Beam']),
                                          sm.wor(sm.wand(sm.haveItem('Morph'),
                                                         sm.knowsMockball()),
                                                 sm.haveItem('SpeedBooster'))),
    'Crocomire Speedway Bottom': lambda sm: sm.wand(sm.canUseCrocRoomToChargeSpeed(),
                                                    sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Croc -> Ice Missiles']),
                                                    sm.haveItem('SpeedBooster'),
                                                    sm.knowsIceMissileFromCroc())
}
locationsDict["Missile (below Ice Beam)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Missile (above Crocomire)"].AccessFrom = {
    'Grapple Escape': lambda sm: SMBool(True)
}
locationsDict["Missile (above Crocomire)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Missile (Hi-Jump Boots)"].AccessFrom = {
    'Business Center': lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.HiJumpAreaBlueDoor), sm.traverse('BusinessCenterBottomLeft'))
}
locationsDict["Missile (Hi-Jump Boots)"].Available = (
    lambda sm: sm.haveItem('Morph')
)
locationsDict["Missile (Hi-Jump Boots)"].PostAvailable = (
    lambda sm: sm.wor(sm.canPassBombPassages(),
                      sm.wand(RomPatches.has(sm.player, RomPatches.HiJumpShotBlock), sm.haveItem('Morph')))
)
locationsDict["Energy Tank (Hi-Jump Boots)"].AccessFrom = {
    'Business Center': lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.HiJumpAreaBlueDoor), sm.traverse('BusinessCenterBottomLeft'))
}
locationsDict["Energy Tank (Hi-Jump Boots)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Power Bomb (Crocomire)"].AccessFrom = {
    'Crocomire Room Top': lambda sm: SMBool(True)
}
locationsDict["Power Bomb (Crocomire)"].Available = (
    lambda sm: sm.wand(sm.traverse('PostCrocomireUpperLeft'),
                       sm.haveItem('Crocomire'),
                       sm.wor(sm.wor(sm.canFly(),
                                     sm.haveItem('Grapple'),
                                     sm.wand(sm.haveItem('SpeedBooster'),
                                             sm.wor(sm.heatProof(),
                                                    sm.energyReserveCountOk(1)))), # spark from the room before
                              sm.wor(sm.haveItem('HiJump'), # run and jump from yellow platform
                                     sm.wand(sm.haveItem('Ice'),
                                             sm.knowsCrocPBsIce()),
                                     sm.knowsCrocPBsDBoost())))
)
locationsDict["Missile (below Crocomire)"].AccessFrom = {
    'Crocomire Room Top': lambda sm: SMBool(True)
}
locationsDict["Missile (below Crocomire)"].Available = (
    lambda sm: sm.wand(sm.traverse('PostCrocomireShaftRight'), sm.haveItem('Crocomire'), sm.haveItem('Morph'))
)
locationsDict["Missile (Grapple Beam)"].AccessFrom = {
    'Crocomire Room Top': lambda sm: SMBool(True)
}
locationsDict["Missile (Grapple Beam)"].Available = (
    lambda sm: sm.wand(sm.haveItem('Crocomire'),
                       sm.wor(sm.wor(sm.wand(sm.haveItem('Morph'), # from below
                                             sm.canFly()),
                                     sm.wand(sm.haveItem('SpeedBooster'),
                                             sm.wor(sm.knowsShortCharge(),
                                                    sm.canUsePowerBombs()))),
                              sm.wand(sm.canGreenGateGlitch(), # from grapple room
                                      sm.canFly()))) # TODO::test if accessible with a spark (short charge), and how many etanks required
)
locationsDict["Missile (Grapple Beam)"].PostAvailable = (
    lambda sm: sm.wor(sm.haveItem('Morph'), # normal exit
                      sm.wand(sm.haveItem('Super'), # go back to grapple room
                              sm.wor(sm.haveItem('SpaceJump'),
                                     sm.wand(sm.haveItem('SpeedBooster'), sm.haveItem('HiJump'))))) # jump from the yellow plateform ennemy
)
locationsDict["Missile (Norfair Reserve Tank)"].AccessFrom = {
    'Bubble Mountain': lambda sm: sm.canEnterNorfairReserveAreaFromBubbleMoutain(),
    'Bubble Mountain Top': lambda sm: sm.canEnterNorfairReserveAreaFromBubbleMoutainTop()
}
locationsDict["Missile (Norfair Reserve Tank)"].Available = (
    lambda sm: sm.wand(sm.haveItem('Morph'), sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Norfair Reserve']))
)
locationsDict["Missile (bubble Norfair green door)"].AccessFrom = {
    'Bubble Mountain': lambda sm: sm.canEnterNorfairReserveAreaFromBubbleMoutain(),
    'Bubble Mountain Top': lambda sm: sm.canEnterNorfairReserveAreaFromBubbleMoutainTop()
}
locationsDict["Missile (bubble Norfair green door)"].Available = (
    lambda sm: sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Norfair Reserve Missiles'])
)
locationsDict["Missile (bubble Norfair)"].AccessFrom = {
    'Bubble Mountain': lambda sm: SMBool(True)
}
locationsDict["Missile (bubble Norfair)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Missile (Speed Booster)"].AccessFrom = {
    'Bubble Mountain Top': lambda sm: sm.wor(RomPatches.has(sm.player, RomPatches.SpeedAreaBlueDoors),
                                             sm.traverse('BubbleMountainTopRight'))
}
locationsDict["Missile (Speed Booster)"].Available = (
    lambda sm: sm.canHellRunToSpeedBooster()
)
locationsDict["Missile (Speed Booster)"].PostAvailable = (
    lambda sm: sm.canHellRunBackFromSpeedBoosterMissile()
)
locationsDict["Missile (Wave Beam)"].AccessFrom = {
    'Bubble Mountain Top': lambda sm: sm.canAccessDoubleChamberItems()
}
locationsDict["Missile (Wave Beam)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Missile (Gold Torizo)"].AccessFrom = {
    'LN Above GT': lambda sm: SMBool(True)
}
locationsDict["Missile (Gold Torizo)"].Available = (
    lambda sm: sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main'])
)
locationsDict["Missile (Gold Torizo)"].PostAvailable = (
    lambda sm: sm.enoughStuffGT()
)
locationsDict["Super Missile (Gold Torizo)"].AccessFrom = {
    'Screw Attack Bottom': lambda sm: SMBool(True)
}
locationsDict["Super Missile (Gold Torizo)"].Available = (
    lambda sm: sm.canDestroyBombWalls()
)
locationsDict["Super Missile (Gold Torizo)"].PostAvailable = (
    lambda sm: sm.enoughStuffGT()
)
locationsDict["Missile (Mickey Mouse room)"].AccessFrom = {
    'LN Entrance': lambda sm: sm.wand(sm.canUsePowerBombs(), sm.canPassWorstRoom()),
}
locationsDict["Missile (Mickey Mouse room)"].Available = (
    lambda sm: sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main'])
)
locationsDict["Missile (lower Norfair above fire flea room)"].AccessFrom = {
    'Firefleas': lambda sm: sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main'])
}
locationsDict["Missile (lower Norfair above fire flea room)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Power Bomb (lower Norfair above fire flea room)"].AccessFrom = {
    'Firefleas Top': lambda sm: SMBool(True)
}
locationsDict["Power Bomb (lower Norfair above fire flea room)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Power Bomb (Power Bombs of shame)"].AccessFrom = {
    'Wasteland': lambda sm: sm.canUsePowerBombs()
}
locationsDict["Power Bomb (Power Bombs of shame)"].Available = (
    lambda sm: SMBool(True)
)
locationsDict["Missile (lower Norfair near Wave Beam)"].AccessFrom = {
    'Firefleas': lambda sm: SMBool(True)
}
locationsDict["Missile (lower Norfair near Wave Beam)"].Available = (
    lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Main']),
                       sm.canDestroyBombWalls(),
                       sm.haveItem('Morph'))
)
locationsDict["Missile (Wrecked Ship middle)"].AccessFrom = {
    'Wrecked Ship Main': lambda sm: SMBool(True)
}
locationsDict["Missile (Wrecked Ship middle)"].Available = (
    lambda sm: sm.canPassBombPassages()
)
locationsDict["Missile (Gravity Suit)"].AccessFrom = {
    'Wrecked Ship Main': lambda sm: SMBool(True)
}
locationsDict["Missile (Gravity Suit)"].Available = (
    lambda sm: sm.wand(sm.canPassBowling(),
                       sm.canPassBombPassages())
)
locationsDict["Missile (Wrecked Ship top)"].AccessFrom = {
    'Wrecked Ship Main': lambda sm: SMBool(True)
}
locationsDict["Missile (Wrecked Ship top)"].Available = (
    lambda sm: Bosses.bossDead(sm, 'Phantoon')
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
                       sm.wor(sm.wand(sm.traverse('MainStreetBottomRight'), # run from room on the right
                                      sm.wor(RomPatches.has(sm.player, RomPatches.AreaRandoGatesOther),
                                             sm.haveItem('Super')),
                                      sm.itemCountOk('ETank', 1)), # etank for the spark since sparking from low ground
                              sm.canSimpleShortCharge())) # run from above
)
locationsDict["Super Missile (green Maridia)"].AccessFrom = {
    'Main Street Bottom': lambda sm: sm.canDoOuterMaridia()
}
locationsDict["Super Missile (green Maridia)"].Available = (
    lambda sm: sm.haveItem('Morph')
)
locationsDict["Missile (green Maridia tatori)"].AccessFrom = {
    'Main Street Bottom': lambda sm: sm.wand(sm.wor(sm.traverse('FishTankRight'),
                                                    RomPatches.has(sm.player, RomPatches.MamaTurtleBlueDoor)),
                                             sm.canDoOuterMaridia()),
    'Mama Turtle': lambda sm: SMBool(True)
}
locationsDict["Missile (green Maridia tatori)"].Available = (
    lambda sm: SMBool(True)
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
locationsDict["Missile (left Maridia sand pit room)"].AccessFrom = {
    'Left Sandpit': lambda sm: sm.canClimbWestSandHole()
}
locationsDict["Missile (left Maridia sand pit room)"].Available = (
    lambda sm: sm.canAccessItemsInWestSandHole()
)
locationsDict["Missile (right Maridia sand pit room)"].AccessFrom = {
    'Right Sandpit': lambda sm: SMBool(True)
}
locationsDict["Missile (right Maridia sand pit room)"].Available = (
    lambda sm: sm.wor(sm.haveItem('Gravity'),
                      sm.wand(sm.haveItem('HiJump'),
                              sm.knowsGravLessLevel3()))
)
locationsDict["Power Bomb (right Maridia sand pit room)"].AccessFrom = {
    'Right Sandpit': lambda sm: sm.haveItem('Morph')
}
locationsDict["Power Bomb (right Maridia sand pit room)"].Available = (
    lambda sm: sm.wor(sm.haveItem('Gravity'),
                      sm.wand(sm.knowsGravLessLevel3(),
                              sm.haveItem('HiJump'),
                              sm.canSpringBallJump())) # https://www.youtube.com/watch?v=7LYYxphRRT0
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

# TODO::use the dict in solver/randomizer
# create the list that the solver/randomizer use
locations = [loc for loc in locationsDict.values()]

class LocationsHelper:
    # used by FillerRandom to know how many front fill steps it must perform
    def getRandomFillHelp(startLocation):
        helpByAp = {
            "Firefleas Top": 3,
            "Aqueduct": 1,
            "Mama Turtle": 1,
            "Watering Hole": 2,
            "Etecoons Supers": 2,
            "Gauntlet Top":1,
            "Bubble Mountain":1
        }
        return helpByAp[startLocation] if startLocation in helpByAp else 0

    # for a given start AP, gives:
    # - locations that can be used as majors/chozo in the start area
    # - locations to preserve in the split
    # - number of necessary majors locations to add in the start area,
    # - number of necessary chozo locations to add in the start area
    # locs are taken in the first n in the list
    def getStartMajors(startLocation):
        majLocsByAp = {
            'Gauntlet Top': ([
                "Missile (Crateria gauntlet right)",
                "Missile (Crateria gauntlet left)"
            ], ["Energy Tank, Terminator"], 1, 2),
            'Green Brinstar Elevator': ([
                "Missile (green Brinstar below super missile)"
            ], ["Reserve Tank, Brinstar"], 1, 1),
            'Big Pink': ([
                "Missile (pink Brinstar top)",
                "Missile (pink Brinstar bottom)"
            ], ["Charge Beam"], 1, 2),
            'Etecoons Supers': ([
                "Energy Tank, Etecoons",
                "Super Missile (green Brinstar bottom)",
            ], ["Energy Tank, Etecoons"], 1, 2),
            'Firefleas Top': ([
                "Power Bomb (lower Norfair above fire flea room)",
                "Energy Tank, Firefleas",
                "Missile (lower Norfair near Wave Beam)",
                "Missile (lower Norfair above fire flea room)"
            ], ["Energy Tank, Firefleas"], 3, 4),
            'Business Center': ([
                "Energy Tank (Hi-Jump Boots)",
            ], ["Hi-Jump Boots"], 1, 1),
            'Bubble Mountain': ([
                "Missile (bubble Norfair)"
            ], ["Speed Booster", "Wave Beam"], 1, 1),
            'Mama Turtle': ([
                "Energy Tank, Mama turtle",
                "Missile (green Maridia tatori)",
                "Super Missile (green Maridia)"
            ], ["Energy Tank, Mama turtle"], 2, 3),
            'Watering Hole': ([
                "Missile (yellow Maridia super missile)",
                "Super Missile (yellow Maridia)",
                "Missile (yellow Maridia false wall)"
            ], [], 2, 3),
            'Aqueduct': ([
                "Missile (pink Maridia)",
                "Super Missile (pink Maridia)",
                "Missile (right Maridia sand pit room)"
            ], ["Reserve Tank, Maridia"], 2, 3)
        }
        return majLocsByAp[startLocation] if startLocation in majLocsByAp else ([],[],0,0)
