from enum import IntEnum,IntFlag
import copy
from ..logic.smbool import SMBool
from ..rom.rom_patches import RomPatches
import logging

from ..utils import log
LOG = log.get('DoorsManager')

colorsList = ['red', 'green', 'yellow', 'wave', 'spazer', 'plasma', 'ice']
# 1/15 chance to have the door set to grey
colorsListGrey = colorsList * 2 + ['grey']

class Facing(IntEnum):
    Left = 0
    Right = 1
    Top = 2
    Bottom = 3

# door facing left - right - top   - bottom
plmRed    = [0xc88a, 0xc890, 0xc896, 0xc89c]
plmGreen  = [0xc872, 0xc878, 0xc87e, 0xc884]
plmYellow = [0xc85a, 0xc860, 0xc866, 0xc86c]
plmGrey   = [0xc842, 0xc848, 0xc84e, 0xc854]
plmWave   = [0xf763, 0xf769, 0xf70f, 0xf715]
plmSpazer = [0xf733, 0xf739, 0xf73f, 0xf745]
plmPlasma = [0xf74b, 0xf751, 0xf757, 0xf75d]
plmIce    = [0xf71b, 0xf721, 0xf727, 0xf72d]

colors2plm = {
    'red': plmRed,
    'green': plmGreen,
    'yellow': plmYellow,
    'grey': plmGrey,
    'wave': plmWave,
    'spazer': plmSpazer,
    'plasma': plmPlasma,
    'ice': plmIce
}

# door color indicators PLMs (flashing on the other side of colored doors)
indicatorsDirection = {
    Facing.Left: Facing.Right,
    Facing.Right: Facing.Left,
    Facing.Top: Facing.Bottom,
    Facing.Bottom: Facing.Top
}

# door facing        left -   right - top   - bottom
plmRedIndicator    = [0xFBB0, 0xFBB6, 0xFBBC, 0xFBC2]
plmGreenIndicator  = [0xFBC8, 0xFBCE, 0xFBD4, 0xFBDA]
plmYellowIndicator = [0xFBE0, 0xFBE6, 0xFBEC, 0xFBF2]
plmGreyIndicator   = [0xFBF8, 0xFBFE, 0xFC04, 0xFC0A]
plmWaveIndicator   = [0xF60B, 0xF611, 0xF617, 0xF61D]
plmSpazerIndicator = [0xF63B, 0xF641, 0xF647, 0xF64D]
plmPlasmaIndicator = [0xF623, 0xF629, 0xF62F, 0xF635]
plmIceIndicator    = [0xF653, 0xF659, 0xF65F, 0xF665]

colors2plmIndicator = {
    'red': plmRedIndicator,
    'green': plmGreenIndicator,
    'yellow': plmYellowIndicator,
    'grey': plmGreyIndicator,
    'wave': plmWaveIndicator,
    'spazer': plmSpazerIndicator,
    'plasma': plmPlasmaIndicator,
    'ice': plmIceIndicator
}

class IndicatorFlag(IntFlag):
    Standard = 1
    AreaRando = 2
    DoorRando = 4

# indicator always there
IndicatorAll = IndicatorFlag.Standard | IndicatorFlag.AreaRando | IndicatorFlag.DoorRando
# indicator there when not in area rando
IndicatorDoor = IndicatorFlag.Standard | IndicatorFlag.DoorRando

class Door(object):
    __slots__ = ('name', 'address', 'vanillaColor', 'color', 'forced', 'facing', 'hidden', 'id', 'canGrey', 'forbiddenColors','indicator')
    def __init__(self, name, address, vanillaColor, facing, id=None, canGrey=False, forbiddenColors=None,indicator=0):
        self.name = name
        self.address = address
        self.vanillaColor = vanillaColor
        self.setColor(vanillaColor)
        self.forced = False
        self.facing = facing
        self.hidden = False
        self.canGrey = canGrey
        self.id = id
        # list of forbidden colors
        self.forbiddenColors = forbiddenColors
        self.indicator = indicator

    def forceBlue(self):
        # custom start location, area, patches can force doors to blue
        self.setColor('blue')
        self.forced = True

    def setColor(self, color):
        self.color = color

    def getColor(self):
        if self.hidden:
            return 'grey'
        else:
            return self.color

    def isRandom(self):
        return self.color != self.vanillaColor and not self.isBlue()

    def isBlue(self):
        return self.color == 'blue'

    def canRandomize(self):
        return not self.forced and self.id is None

    def filterColorList(self, colorsList):
        if self.forbiddenColors is None:
            return colorsList
        else:
            return [color for color in colorsList if color not in self.forbiddenColors]

    def randomize(self, allowGreyDoors, random):
        if self.canRandomize():
            if self.canGrey and allowGreyDoors:
                self.setColor(random.choice(self.filterColorList(colorsListGrey)))
            else:
                self.setColor(random.choice(self.filterColorList(colorsList)))

    def traverse(self, smbm):
        if self.hidden or self.color == 'grey':
            return SMBool(False)
        elif self.color == 'red':
            return smbm.canOpenRedDoors()
        elif self.color == 'green':
            return smbm.canOpenGreenDoors()
        elif self.color == 'yellow':
            return smbm.canOpenYellowDoors()
        elif self.color == 'wave':
            return smbm.haveItem('Wave')
        elif self.color == 'spazer':
            return smbm.haveItem('Spazer')
        elif self.color == 'plasma':
            return smbm.haveItem('Plasma')
        elif self.color == 'ice':
            return smbm.haveItem('Ice')
        else:
            return SMBool(True)

    def __repr__(self):
        return "Door({}, {})".format(self.name, self.color)

    def isRefillSave(self):
        return self.address is None

    def writeColor(self, rom, writeWordFunc):
        if self.isBlue() or self.isRefillSave():
            return

        writeWordFunc(colors2plm[self.color][self.facing], self.address)

        # also set plm args high byte to never opened, even during escape
        if self.color == 'grey':
            rom.writeByte(0x90, self.address+5)

    def readColor(self, rom, readWordFunc):
        if self.forced or self.isRefillSave():
            return

        plm = readWordFunc(self.address)
        if plm in plmRed:
            self.setColor('red')
        elif plm in plmGreen:
            self.setColor('green')
        elif plm in plmYellow:
            self.setColor('yellow')
        elif plm in plmGrey:
            self.setColor('grey')
        elif plm in plmWave:
            self.setColor('wave')
        elif plm in plmSpazer:
            self.setColor('spazer')
        elif plm in plmPlasma:
            self.setColor('plasma')
        elif plm in plmIce:
            self.setColor('ice')
        else:
            # we can't read the color, handle as grey door (can happen in race protected seeds)
            self.setColor('grey')

    # gives the PLM ID for matching indicator door
    def getIndicatorPLM(self, indicatorFlags):
        ret = None
        if (indicatorFlags & self.indicator) != 0 and self.color in colors2plmIndicator:
            ret = colors2plmIndicator[self.color][indicatorsDirection[self.facing]]
        return ret

    # for tracker
    def canHide(self):
        return self.color != 'blue'

    def hide(self):
        if self.canHide():
            self.hidden = True

    def reveal(self):
        self.hidden = False

    def switch(self):
        if self.hidden:
            self.reveal()
        else:
            self.hide()

    # to send/receive state to tracker/plando
    def serialize(self):
        return (self.color, self.facing, self.hidden)

    def unserialize(self, data):
        self.setColor(data[0])
        self.facing = data[1]
        self.hidden = data[2]

class DoorsManager():
    doorsDict = {}
    doors = {
        # crateria
        'LandingSiteRight': Door('LandingSiteRight', 0x78018, 'green', Facing.Left, canGrey=True, indicator=IndicatorAll),
        'LandingSiteTopRight': Door('LandingSiteTopRight', 0x07801e, 'yellow', Facing.Left),
        'KihunterBottom': Door('KihunterBottom', 0x78228, 'yellow', Facing.Top, canGrey=True, indicator=IndicatorDoor),
        'KihunterRight': Door('KihunterRight', 0x78222, 'yellow', Facing.Left, canGrey=True, indicator=IndicatorAll),
        'FlywayRight': Door('FlywayRight', 0x78420, 'red', Facing.Left),
        'GreenPiratesShaftBottomRight': Door('GreenPiratesShaftBottomRight', 0x78470, 'red', Facing.Left, canGrey=True),
        'RedBrinstarElevatorTop': Door('RedBrinstarElevatorTop', 0x78256, 'yellow', Facing.Bottom),
        'ClimbRight': Door('ClimbRight', 0x78304, 'yellow', Facing.Left),
        # blue brinstar
        'ConstructionZoneRight': Door('ConstructionZoneRight', 0x78784, 'red', Facing.Left),
        # green brinstar
        'GreenHillZoneTopRight': Door('GreenHillZoneTopRight', 0x78670, 'yellow', Facing.Left, canGrey=True, indicator=IndicatorFlag.DoorRando),
        'NoobBridgeRight': Door('NoobBridgeRight', 0x787a6, 'green', Facing.Left, canGrey=True, indicator=IndicatorDoor),
        'MainShaftRight': Door('MainShaftRight', 0x784be, 'red', Facing.Left),
        'MainShaftBottomRight': Door('MainShaftBottomRight', 0x784c4, 'red', Facing.Left, canGrey=True, indicator=IndicatorAll),
        'EarlySupersRight': Door('EarlySupersRight', 0x78512, 'red', Facing.Left),
        'EtecoonEnergyTankLeft': Door('EtecoonEnergyTankLeft', 0x787c8, 'green', Facing.Right),
        # pink brinstar
        'BigPinkTopRight': Door('BigPinkTopRight', 0x78626, 'red', Facing.Left),
        'BigPinkRight': Door('BigPinkRight', 0x7861a, 'yellow', Facing.Left),
        'BigPinkBottomRight': Door('BigPinkBottomRight', 0x78620, 'green', Facing.Left, canGrey=True, indicator=IndicatorAll),
        'BigPinkBottomLeft': Door('BigPinkBottomLeft', 0x7862c, 'red', Facing.Right),
        # red brinstar
        'RedTowerLeft': Door('RedTowerLeft', 0x78866, 'yellow', Facing.Right),
        'RedBrinstarFirefleaLeft': Door('RedBrinstarFirefleaLeft', 0x7886e, 'red', Facing.Right),
        'RedTowerElevatorTopLeft': Door('RedTowerElevatorTopLeft', 0x788aa, 'green', Facing.Right),
        'RedTowerElevatorLeft': Door('RedTowerElevatorLeft', 0x788b0, 'yellow', Facing.Right, indicator=IndicatorAll),
        'RedTowerElevatorBottomLeft': Door('RedTowerElevatorBottomLeft', 0x788b6, 'green', Facing.Right),
        'BelowSpazerTopRight': Door('BelowSpazerTopRight', 0x78966, 'green', Facing.Left),
        # Wrecked ship
        'WestOceanRight': Door('WestOceanRight', 0x781e2, 'green', Facing.Left, canGrey=True, indicator=IndicatorAll),
        'LeCoudeBottom': Door('LeCoudeBottom', 0x7823e, 'yellow', Facing.Top, canGrey=True, indicator=IndicatorDoor),
        'WreckedShipMainShaftBottom': Door('WreckedShipMainShaftBottom', 0x7c277, 'green', Facing.Top, indicator=IndicatorFlag.AreaRando),
        'ElectricDeathRoomTopLeft': Door('ElectricDeathRoomTopLeft', 0x7c32f, 'red', Facing.Right),
        # Upper Norfair
        'BusinessCenterTopLeft': Door('BusinessCenterTopLeft', 0x78b00, 'green', Facing.Right),
        'BusinessCenterBottomLeft': Door('BusinessCenterBottomLeft', 0x78b0c, 'red', Facing.Right),
        'CathedralEntranceRight': Door('CathedralEntranceRight', 0x78af2, 'red', Facing.Left, canGrey=True, indicator=IndicatorAll),
        'CathedralRight': Door('CathedralRight', 0x78aea, 'green', Facing.Left, indicator=IndicatorAll),
        'BubbleMountainTopRight': Door('BubbleMountainTopRight', 0x78c60, 'green', Facing.Left),
        'BubbleMountainTopLeft': Door('BubbleMountainTopLeft', 0x78c5a, 'green', Facing.Right),
        'SpeedBoosterHallRight': Door('SpeedBoosterHallRight', 0x78c7a, 'red', Facing.Left),
        'SingleChamberRight': Door('SingleChamberRight', 0x78ca8, 'red', Facing.Left),
        'DoubleChamberRight': Door('DoubleChamberRight', 0x78cc2, 'red', Facing.Left),
        'KronicBoostBottomLeft': Door('KronicBoostBottomLeft', 0x78d4e, 'yellow', Facing.Right, canGrey=True),
        'CrocomireSpeedwayBottom': Door('CrocomireSpeedwayBottom', 0x78b96, 'green', Facing.Top, canGrey=True),
        # Crocomire
        'PostCrocomireUpperLeft': Door('PostCrocomireUpperLeft', 0x78bf4, 'red', Facing.Right),
        'PostCrocomireShaftRight': Door('PostCrocomireShaftRight', 0x78c0c, 'red', Facing.Left),
        # Lower Norfair
        'RedKihunterShaftBottom': Door('RedKihunterShaftBottom', 0x7902e, 'yellow', Facing.Top, indicator=IndicatorFlag.AreaRando),
        'WastelandLeft': Door('WastelandLeft', 0x790ba, 'green', Facing.Right, forbiddenColors=['yellow'], indicator=IndicatorFlag.AreaRando),
        # Maridia
        'MainStreetBottomRight': Door('MainStreetBottomRight', 0x7c431, 'red', Facing.Left, indicator=IndicatorAll),
        'FishTankRight': Door('FishTankRight', 0x7c475, 'red', Facing.Left),
        'CrabShaftRight': Door('CrabShaftRight', 0x7c4fb, 'green', Facing.Left, indicator=IndicatorDoor),
        'ColosseumBottomRight': Door('ColosseumBottomRight', 0x7c6fb, 'green', Facing.Left, indicator=IndicatorFlag.AreaRando),
        'PlasmaSparkBottom': Door('PlasmaSparkBottom', 0x7c577, 'green', Facing.Top),
        'OasisTop': Door('OasisTop', 0x7c5d3, 'green', Facing.Bottom),
        # refill/save
        'GreenBrinstarSaveStation': Door('GreenBrinstarSaveStation', None, 'red', Facing.Right, id=0x1f),
        'MaridiaBottomSaveStation': Door('MaridiaBottomSaveStation', None, 'red', Facing.Left, id=0x8c),
        'MaridiaAqueductSaveStation': Door('MaridiaAqueductSaveStation', None, 'red', Facing.Right, id=0x96),
        'ForgottenHighwaySaveStation': Door('ForgottenHighwaySaveStation', None, 'red', Facing.Left, id=0x92),
        'DraygonSaveRefillStation': Door('DraygonSaveRefillStation', None, 'red', Facing.Left, id=0x98),
        'KraidRefillStation': Door('KraidRefillStation', None, 'green', Facing.Left, id=0x44),
        'RedBrinstarEnergyRefill': Door('RedBrinstarEnergyRefill', None, 'green', Facing.Right, id=0x38),
        'GreenBrinstarMissileRefill': Door('GreenBrinstarMissileRefill', None, 'red', Facing.Right, id=0x23)
    }

    # call from logic
    def traverse(self, smbm, doorName):
        return DoorsManager.doorsDict[smbm.player][doorName].traverse(smbm)

    @staticmethod
    def setDoorsColor(player=0):
        DoorsManager.doorsDict[player] = copy.deepcopy(DoorsManager.doors)
        currentDoors = DoorsManager.doorsDict[player]

        # depending on loaded patches, force some doors to blue, excluding them from randomization
        if RomPatches.has(player, RomPatches.BlueBrinstarBlueDoor):
            currentDoors['ConstructionZoneRight'].forceBlue()
        if RomPatches.has(player, RomPatches.BrinReserveBlueDoors):
            currentDoors['MainShaftRight'].forceBlue()
            currentDoors['EarlySupersRight'].forceBlue()
        if RomPatches.has(player, RomPatches.EtecoonSupersBlueDoor):
            currentDoors['EtecoonEnergyTankLeft'].forceBlue()
        #if RomPatches.has(player, RomPatches.SpongeBathBlueDoor):
        #    currentDoors[''].forceBlue()
        if RomPatches.has(player, RomPatches.HiJumpAreaBlueDoor):
            currentDoors['BusinessCenterBottomLeft'].forceBlue()
        if RomPatches.has(player, RomPatches.SpeedAreaBlueDoors):
            currentDoors['BubbleMountainTopRight'].forceBlue()
            currentDoors['SpeedBoosterHallRight'].forceBlue()
        if RomPatches.has(player, RomPatches.MamaTurtleBlueDoor):
            currentDoors['FishTankRight'].forceBlue()
        if RomPatches.has(player, RomPatches.HellwayBlueDoor):
            currentDoors['RedTowerElevatorLeft'].forceBlue()
        if RomPatches.has(player, RomPatches.RedTowerBlueDoors):
            currentDoors['RedBrinstarElevatorTop'].forceBlue()
        if RomPatches.has(player, RomPatches.AreaRandoBlueDoors):
            currentDoors['GreenHillZoneTopRight'].forceBlue()
            currentDoors['NoobBridgeRight'].forceBlue()
            currentDoors['LeCoudeBottom'].forceBlue()
            currentDoors['KronicBoostBottomLeft'].forceBlue()
        else:
            # no area rando, prevent some doors to be in the grey doors pool
            currentDoors['GreenPiratesShaftBottomRight'].canGrey = False
            currentDoors['CrocomireSpeedwayBottom'].canGrey = False
            currentDoors['KronicBoostBottomLeft'].canGrey = False
        if RomPatches.has(player, RomPatches.AreaRandoMoreBlueDoors):
            currentDoors['KihunterBottom'].forceBlue()
            currentDoors['GreenPiratesShaftBottomRight'].forceBlue()
        if RomPatches.has(player, RomPatches.CrocBlueDoors):
            currentDoors['CrocomireSpeedwayBottom'].forceBlue()
        if RomPatches.has(player, RomPatches.CrabShaftBlueDoor):
            currentDoors['CrabShaftRight'].forceBlue()

    @staticmethod
    def randomize(allowGreyDoors, player, random):
        for door in DoorsManager.doorsDict[player].values():
            door.randomize(allowGreyDoors, random)
        # set both ends of toilet to the same color to avoid soft locking in area rando
        toiletTop = DoorsManager.doorsDict[player]['PlasmaSparkBottom']
        toiletBottom = DoorsManager.doorsDict[player]['OasisTop']
        if toiletTop.color != toiletBottom.color:
            toiletBottom.setColor(toiletTop.color)
        DoorsManager.debugDoorsColor()

    # call from rom loader
    @staticmethod
    def loadDoorsColor(rom, readWordFunc):
        # force to blue some doors depending on patches
        DoorsManager.setDoorsColor()
        # for each door store it's color
        for door in DoorsManager.doors.values():
            door.readColor(rom, readWordFunc)
        DoorsManager.debugDoorsColor()

        # tell that we have randomized doors
        isRandom = DoorsManager.isRandom()
        if isRandom:
            DoorsManager.setRefillSaveToBlue()
        return isRandom

    @staticmethod
    def isRandom(player):
        return any(door.isRandom() for door in DoorsManager.doorsDict[player].values())

    @staticmethod
    def setRefillSaveToBlue(player):
        for door in DoorsManager.doorsDict[player].values():
            if door.id is not None:
                door.forceBlue()

    @staticmethod
    def debugDoorsColor():
        if LOG.getEffectiveLevel() == logging.DEBUG:
            for door in DoorsManager.doors.values():
                LOG.debug("{:>32}: {:>6}".format(door.name, door.color))

    # call from rom patcher
    @staticmethod
    def writeDoorsColor(rom, doors, player, readWordFunc):
        for door in DoorsManager.doorsDict[player].values():
            door.writeColor(rom, readWordFunc)
            # also set save/refill doors to blue
            if door.id is not None:
                doors.append(door.id)

    # returns a dict {'DoorName': indicatorPlmType }
    @staticmethod
    def getIndicatorPLMs(player, indicatorFlags):
        ret = {}
        for doorName,door in DoorsManager.doorsDict[player].items():
            plm = door.getIndicatorPLM(indicatorFlags)
            if plm is not None:
                ret[doorName] = plm
        return ret


    # call from web
    @staticmethod
    def getAddressesToRead():
        return [door.address for door in DoorsManager.doors.values() if door.address is not None] + [door.address+1 for door in DoorsManager.doors.values() if door.address is not None]

    # for isolver state
    @staticmethod
    def serialize():
        return {door.name: door.serialize() for door in DoorsManager.doors.values()}

    @staticmethod
    def unserialize(state):
        for name, data in state.items():
            DoorsManager.doors[name].unserialize(data)

    @staticmethod
    def allDoorsRevealed():
        for door in DoorsManager.doors.values():
            if door.hidden:
                return False
        return True

    # when using the tracker, first set all colored doors to grey until the user clicks on it
    @staticmethod
    def initTracker():
        for door in DoorsManager.doors.values():
            door.hide()

    # when the user clicks on a door in the tracker
    @staticmethod
    def switchVisibility(name):
        DoorsManager.doors[name].switch()

    # when the user clicks on a door in the race tracker or the plando
    @staticmethod
    def setColor(name, color):
        # in race mode the doors are hidden
        DoorsManager.doors[name].reveal()
        DoorsManager.doors[name].setColor(color)

    # in autotracker we need the current doors state
    @staticmethod
    def getDoorsState():
        hiddenDoors = set([door.name for door in DoorsManager.doors.values() if door.hidden])
        revealedDoor = set([door.name for door in DoorsManager.doors.values() if (not door.hidden) and door.canHide()])
        return (hiddenDoors, revealedDoor)
