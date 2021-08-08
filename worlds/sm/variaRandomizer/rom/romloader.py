import os, json

from rom.rom_patches import RomPatches
from rom.rom import RealROM, FakeROM
from rom.romreader import RomReader
from utils.doorsmanager import DoorsManager
from graph.graph_utils import getAccessPoint

class RomLoader(object):
    @staticmethod
    def factory(rom, magic=None):
        # can be a real rom. can be a json or a dict with the ROM address/values
        if type(rom) == str:
            ext = os.path.splitext(rom)
            if ext[1].lower() == '.sfc' or ext[1].lower() == '.smc':
                return RomLoaderSfc(rom, magic)
            elif ext[1].lower() == '.json':
                return RomLoaderJson(rom, magic)
            else:
                raise Exception("wrong rom file type: {}".format(ext[1]))
        elif type(rom) is dict:
            return RomLoaderDict(rom, magic)

    def assignItems(self, locations):
        return self.romReader.loadItems(locations)

    def getTransitions(self):
        return self.romReader.loadTransitions()

    def hasPatch(self, patchName):
        return self.romReader.patchPresent(patchName)

    def loadPatches(self):
        RomPatches.ActivePatches = []
        isArea = False
        isBoss = False
        isEscape = False

        # check total base (blue bt and red tower blue door)
        if self.hasPatch("startCeres") or self.hasPatch("startLS"):
            RomPatches.ActivePatches += [RomPatches.BlueBrinstarBlueDoor,
                                         RomPatches.RedTowerBlueDoors]

        if self.hasPatch("newGame"):
            RomPatches.ActivePatches.append(RomPatches.RedTowerBlueDoors)

        # check total soft lock protection
        if self.hasPatch("layout"):
            RomPatches.ActivePatches += RomPatches.TotalLayout

        # check total casual (blue brinstar missile swap)
        if self.hasPatch("casual"):
            RomPatches.ActivePatches.append(RomPatches.BlueBrinstarMissile)

        # check gravity heat protection
        if self.hasPatch("gravityNoHeatProtection"):
            RomPatches.ActivePatches.append(RomPatches.NoGravityEnvProtection)

        if self.hasPatch("progressiveSuits"):
            RomPatches.ActivePatches.append(RomPatches.ProgressiveSuits)
        if self.hasPatch("nerfedCharge"):
            RomPatches.ActivePatches.append(RomPatches.NerfedCharge)
        if self.hasPatch('nerfedRainbowBeam'):
            RomPatches.ActivePatches.append(RomPatches.NerfedRainbowBeam)

        # check varia tweaks
        if self.hasPatch("variaTweaks"):
            RomPatches.ActivePatches += RomPatches.VariaTweaks

        # check area
        if self.hasPatch("area"):
            RomPatches.ActivePatches += [RomPatches.SingleChamberNoCrumble,
                                         RomPatches.AreaRandoGatesBase,
                                         RomPatches.AreaRandoBlueDoors]
            if self.hasPatch("newGame"):
                RomPatches.ActivePatches.append(RomPatches.AreaRandoMoreBlueDoors)
            # use croc patch for separate croc and maridia split in two
            if self.hasPatch("croc_area"):
                RomPatches.ActivePatches += [RomPatches.CrocBlueDoors, RomPatches.CrabShaftBlueDoor, RomPatches.MaridiaSandWarp]
            isArea = True

        # check area layout
        if self.hasPatch("areaLayout"):
            RomPatches.ActivePatches.append(RomPatches.AreaRandoGatesOther)
        if self.hasPatch("traverseWreckedShip"):
            RomPatches.ActivePatches += [RomPatches.EastOceanPlatforms, RomPatches.SpongeBathBlueDoor]

        # check boss rando
        isBoss = self.isBoss()

        # check escape rando
        isEscape = self.hasPatch("areaEscape")

        # minimizer
        if self.hasPatch("minimizer_bosses"):
            RomPatches.ActivePatches.append(RomPatches.NoGadoras)
        if self.hasPatch("minimizer_tourian"):
            RomPatches.ActivePatches.append(RomPatches.TourianSpeedup)
        if self.hasPatch("open_zebetites"):
            RomPatches.ActivePatches.append(RomPatches.OpenZebetites)

        # red doors
        if self.hasPatch('red_doors'):
            RomPatches.ActivePatches.append(RomPatches.RedDoorsMissileOnly)

        return (isArea, isBoss, isEscape)

    def getPatches(self):
        return self.romReader.getPatches()

    def getRawPatches(self):
        # used in interactive solver
        return self.romReader.getRawPatches()

    def getAllPatches(self):
        # used in cli
        return self.romReader.getAllPatches()

    def getPlandoAddresses(self):
        return self.romReader.getPlandoAddresses()

    def getPlandoTransitions(self, maxTransitions):
        return self.romReader.getPlandoTransitions(maxTransitions)

    def decompress(self, address):
        return self.romReader.decompress(address)

    def getROM(self):
        return self.romReader.romFile

    def isBoss(self):
        romFile = self.getROM()
        phOut = getAccessPoint('PhantoonRoomOut')
        doorPtr = phOut.ExitInfo['DoorPtr']
        romFile.seek((0x10000 | doorPtr) + 10)
        asmPtr = romFile.readWord()
        return asmPtr != 0 # this is at 0 in vanilla

    def getEscapeTimer(self):
        return self.romReader.getEscapeTimer()

    def readNothingId(self):
        self.romReader.readNothingId()

    def getStartAP(self):
        return self.romReader.getStartAP()

    def loadDoorsColor(self):
        return DoorsManager.loadDoorsColor(self.romReader.romFile)

    def readLogic(self):
        return self.romReader.readLogic()

    def updateSplitLocs(self, split, locations):
        locIds = self.romReader.getLocationsIds()
        for loc in locations:
            if loc.isBoss():
                continue
            elif loc.Id in locIds:
                loc.setClass([split])
            else:
                loc.setClass(["Minor"])

    def loadScavengerOrder(self, locations):
        return self.romReader.loadScavengerOrder(locations)

class RomLoaderSfc(RomLoader):
    # standard usage (when calling from the command line)
    def __init__(self, romFileName, magic=None):
        super(RomLoaderSfc, self).__init__()
        realROM = RealROM(romFileName)
        self.romReader = RomReader(realROM, magic)

class RomLoaderDict(RomLoader):
    # when called from the website (the js in the browser uploads a dict of address: value)
    def __init__(self, dictROM, magic=None):
        super(RomLoaderDict, self).__init__()
        fakeROM = FakeROM(dictROM)
        self.romReader = RomReader(fakeROM, magic)

class RomLoaderJson(RomLoaderDict):
    # when called from the test suite and the website (when loading already uploaded roms converted to json)
    def __init__(self, jsonFileName, magic=None):
        with open(jsonFileName) as jsonFile:
            tmpDictROM = json.load(jsonFile)
            dictROM = {}
            # in json keys are strings
            for address in tmpDictROM:
                dictROM[int(address)] = tmpDictROM[address]
            super(RomLoaderJson, self).__init__(dictROM, magic)
