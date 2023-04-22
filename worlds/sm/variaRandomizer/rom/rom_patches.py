from ..logic.smbool import SMBool

# layout patches added by randomizers
class RomPatches:
    #### Patches definitions

    ### Layout
    # blue door to access the room with etank+missile
    BlueBrinstarBlueDoor      = 10
    # missile in the first room is a major item and accessible and ceiling is a minor
    BlueBrinstarMissile       = 11
    # shot block instead of bomb blocks for spazer access
    SpazerShotBlock           = 20
    # climb back up red tower from bottom no matter what
    RedTowerLeftPassage       = 21
    # exit red tower top to crateria
    RedTowerBlueDoors         = 22
    # shot block in crumble blocks at early supers
    EarlySupersShotBlock      = 23
    # brinstar reserve area door blue
    BrinReserveBlueDoors      = 24
    # red tower top PB door to hellway
    HellwayBlueDoor           = 25
    # etecoon supers blue door
    EtecoonSupersBlueDoor     = 26
    # shot block to exit hi jump area
    HiJumpShotBlock           = 30
    # access main upper norfair without anything
    CathedralEntranceWallJump = 31
    # graph blue doors
    HiJumpAreaBlueDoor        = 32
    SpeedAreaBlueDoors        = 33
    # LN start
    LowerNorfairPBRoomHeatDisable = 34
    FirefleasRemoveFune       = 35
    # moat bottom block
    MoatShotBlock             = 41
    #graph+forgotten hiway anti softlock
    SpongeBathBlueDoor        = 42
    # forgotten hiway anti softlock
    EastOceanPlatforms        = 43
    # maridia
    MaridiaTubeOpened         = 51
    MamaTurtleBlueDoor        = 52
    # ws start
    WsEtankBlueDoor           = 53
    ## Area rando patches
    # remove crumble block for reverse lower norfair door access
    SingleChamberNoCrumble    = 101
    # remove green gates for reverse maridia access
    AreaRandoGatesBase        = 102
    # remove crab green gate in maridia and blue gate in green brinstar
    AreaRandoGatesOther       = 103
    # disable Green Hill Yellow, Noob Bridge Green, Coude Yellow, and Kronic Boost yellow doors
    AreaRandoBlueDoors        = 104
    # crateria key hunter yellow, green pirates shaft red
    AreaRandoMoreBlueDoors    = 105
    # croc green+grey doors
    CrocBlueDoors             = 106
    # maridia crab shaft AP door
    CrabShaftBlueDoor         = 107
    # wrap door from sand halls left to under botwoon
    MaridiaSandWarp           = 108
    # Replace PB blocks at Aqueduct entrance with bomb blocks
    AqueductBombBlocks        = 109
    ## Minimizer Patches
    NoGadoras                 = 200
    TourianSpeedup            = 201
    OpenZebetites             = 202

    ### Other
    # Gravity no longer protects from environmental damage (heat, spikes...)
    NoGravityEnvProtection  = 1000
    # Wrecked Ship etank accessible when Phantoon is alive
    WsEtankPhantoonAlive    = 1001
    # Lower Norfair chozo (vanilla access to GT/Screw Area) : disable space jump check
    LNChozoSJCheckDisabled  = 1002
    # Progressive suits patch, mutually exclusive with NoGravityEnvProtection
    ProgressiveSuits        = 1003
    # Nerfed charge beam available from the start
    NerfedCharge            = 1004
    # Nerfed rainbow beam for ultra sparse energy qty
    NerfedRainbowBeam       = 1005
    # Red doors open with one missile, and don't react to supers: part of door color rando
    RedDoorsMissileOnly     = 1006
    # Escape auto-trigger on objectives completion (no Tourian)
    NoTourian               = 1007
    # BT wakes up on its item instead of bombs
    BombTorizoWake          = 1008
    # Round-Robin Crystal Flash patch
    RoundRobinCF            = 1009

    ### Hacks
    # rotation hack
    RotationHack            = 10000

    #### Patch sets
    # total randomizer
    TotalBase = [ BlueBrinstarBlueDoor, RedTowerBlueDoors, NoGravityEnvProtection ]
    # tournament and full
    TotalLayout = [ MoatShotBlock, EarlySupersShotBlock,
                    SpazerShotBlock, RedTowerLeftPassage,
                    HiJumpShotBlock, CathedralEntranceWallJump ]

    Total = TotalBase + TotalLayout

    # casual
    TotalCasual = [ BlueBrinstarMissile ] + Total

    # area rando patch set
    AreaBaseSet = [ SingleChamberNoCrumble, AreaRandoGatesBase,
                    AreaRandoBlueDoors, AreaRandoMoreBlueDoors,
                    CrocBlueDoors, CrabShaftBlueDoor, MaridiaSandWarp ]
    AreaComfortSet = [ AreaRandoGatesOther, SpongeBathBlueDoor, EastOceanPlatforms, AqueductBombBlocks ]
    AreaSet = AreaBaseSet + AreaComfortSet

    # VARIA specific patch set
    VariaTweaks = [ WsEtankPhantoonAlive, LNChozoSJCheckDisabled, BombTorizoWake ]

    # Tourian speedup in minimizer mode
    MinimizerTourian = [ TourianSpeedup, OpenZebetites ]

    # dessyreqt randomizer
    Dessy = []

    ### Active patches
    ActivePatches = {}

    @staticmethod
    def has(player, patch):
        return SMBool(patch in RomPatches.ActivePatches[player])

    @staticmethod
    def setDefaultPatches(startLocation):
        # called by the isolver in seedless mode.
        # activate only layout patch (the most common one), red tower blue doors, startLocation's patches and balanced suits.
        from graph.graph_utils import GraphUtils
        RomPatches.ActivePatches[0] = [RomPatches.RedTowerBlueDoors] + RomPatches.TotalLayout + GraphUtils.getGraphPatches(startLocation) + [RomPatches.NoGravityEnvProtection]
