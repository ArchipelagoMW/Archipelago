import sys, json, os

from solver.commonSolver import CommonSolver
from logic.smbool import SMBool
from logic.smboolmanager import SMBoolManagerPlando as SMBoolManager
from logic.helpers import Pickup
from rom.rompatcher import RomPatcher
from rom.rom_patches import RomPatches
from graph.graph import AccessGraphSolver as AccessGraph
from graph.graph_utils import vanillaTransitions, vanillaBossesTransitions, vanillaEscapeTransitions, GraphUtils
from graph.location import define_location
from utils.utils import removeChars
from solver.conf import Conf
from utils.parameters import hard, infinity
from solver.solverState import SolverState
from solver.comeback import ComeBack
from rando.ItemLocContainer import ItemLocation
from utils.doorsmanager import DoorsManager
from logic.logic import Logic
import utils.log

class InteractiveSolver(CommonSolver):
    def __init__(self, output, logic):
        self.interactive = True
        self.errorMsg = ""
        self.checkDuplicateMajor = False
        self.vcr = None
        self.log = utils.log.get('Solver')

        self.outputFileName = output
        self.firstLogFile = None

        Logic.factory(logic)
        self.locations = Logic.locations

        (self.locsAddressName, self.locsWeb2Internal) = self.initLocsAddressName()
        self.transWeb2Internal = self.initTransitionsName()

        Conf.difficultyTarget = infinity

        # no time limitation
        self.runtimeLimit_s = 0

        # used by auto tracker to know how many locs have changed
        self.locDelta = 0

    def initLocsAddressName(self):
        addressName = {}
        web2Internal = {}
        for loc in Logic.locations:
            webName = self.locNameInternal2Web(loc.Name)
            addressName[loc.Address % 0x10000] = webName
            web2Internal[webName] = loc.Name
        return (addressName, web2Internal)

    def initTransitionsName(self):
        web2Internal = {}
        for (startPoint, endPoint) in vanillaTransitions + vanillaBossesTransitions + vanillaEscapeTransitions:
            for point in [startPoint, endPoint]:
                web2Internal[self.apNameInternal2Web(point)] = point
        return web2Internal

    def dumpState(self):
        state = SolverState(self.debug)
        state.fromSolver(self)

        state.toJson(self.outputFileName)

    def initialize(self, mode, rom, presetFileName, magic, fill, startLocation):
        # load rom and preset, return first state
        self.debug = mode == "debug"
        self.mode = mode
        if self.mode != "seedless":
            self.seed = os.path.basename(os.path.splitext(rom)[0])+'.sfc'
        else:
            self.seed = "seedless"

        self.smbm = SMBoolManager()

        self.presetFileName = presetFileName
        self.loadPreset(self.presetFileName)

        self.loadRom(rom, interactive=True, magic=magic, startLocation=startLocation)
        # in plando/tracker always consider that we're doing full
        self.majorsSplit = 'Full'

        # hide doors
        if self.doorsRando and mode in ['standard', 'race']:
            DoorsManager.initTracker()

        self.clearItems()

        # in debug mode don't load plando locs/transitions
        if self.mode == 'plando' and self.debug == False:
            if fill == True:
                # load the source seed transitions and items/locations
                self.curGraphTransitions = self.bossTransitions + self.areaTransitions + self.escapeTransition
                self.areaGraph = AccessGraph(Logic.accessPoints, self.curGraphTransitions)
                self.fillPlandoLocs()
            else:
                if self.areaRando == True or self.bossRando == True:
                    plandoTrans = self.loadPlandoTransitions()
                    if len(plandoTrans) > 0:
                        self.curGraphTransitions = plandoTrans
                    self.areaGraph = AccessGraph(Logic.accessPoints, self.curGraphTransitions)

                self.loadPlandoLocs()

        # compute new available locations
        self.computeLocationsDifficulty(self.majorLocations)

        self.dumpState()

    def iterate(self, stateJson, scope, action, params):
        self.debug = params["debug"]
        self.smbm = SMBoolManager()

        state = SolverState()
        state.fromJson(stateJson)
        state.toSolver(self)

        self.loadPreset(self.presetFileName)

        # add already collected items to smbm
        self.smbm.addItems(self.collectedItems)

        if scope == 'item':
            if action == 'clear':
                self.clearItems(True)
            else:
                if action == 'add':
                    if self.mode in ['plando', 'seedless', 'race', 'debug']:
                        if params['loc'] != None:
                            if self.mode == 'plando':
                                self.setItemAt(params['loc'], params['item'], params['hide'])
                            else:
                                itemName = params.get('item', 'Nothing')
                                if itemName is None:
                                    itemName = 'Nothing'
                                self.setItemAt(params['loc'], itemName, False)
                        else:
                            self.increaseItem(params['item'])
                    else:
                        # pickup item at locName
                        self.pickItemAt(params['loc'])
                elif action == 'remove':
                    if 'loc' in params:
                        self.removeItemAt(params['loc'])
                    elif 'count' in params:
                        # remove last collected item
                        self.cancelLastItems(params['count'])
                    else:
                        self.decreaseItem(params['item'])
                elif action == 'replace':
                    self.replaceItemAt(params['loc'], params['item'], params['hide'])
                elif action == 'toggle':
                    self.toggleItem(params['item'])
        elif scope == 'area':
            if action == 'clear':
                self.clearTransitions()
            else:
                if action == 'add':
                    startPoint = params['startPoint']
                    endPoint = params['endPoint']
                    self.addTransition(self.transWeb2Internal[startPoint], self.transWeb2Internal[endPoint])
                elif action == 'remove':
                    if 'startPoint' in params:
                        self.cancelTransition(self.transWeb2Internal[params['startPoint']])
                    else:
                        # remove last transition
                        self.cancelLastTransition()
        elif scope == 'door':
            if action == 'replace':
                doorName = params['doorName']
                newColor = params['newColor']
                DoorsManager.setColor(doorName, newColor)
            elif action == 'toggle':
                doorName = params['doorName']
                DoorsManager.switchVisibility(doorName)
            elif action == 'clear':
                DoorsManager.initTracker()
        elif scope == 'dump':
            if action == 'import':
                self.importDump(params["dump"])

        self.areaGraph = AccessGraph(Logic.accessPoints, self.curGraphTransitions)

        if scope == 'common':
            if action == 'save':
                return self.savePlando(params['lock'], params['escapeTimer'])
            elif action == 'randomize':
                self.randoPlando(params)

        rewindLimit = self.locDelta if scope == 'dump' and self.locDelta > 0 else 1
        lastVisitedLocs = []
        # if last loc added was a sequence break, recompute its difficulty,
        # as it may be available with the newly placed item.
        # generalize it for auto-tracker where we can add more than one loc at once.
        if len(self.visitedLocations) > 0:
            for i in range(1, rewindLimit+1):
                if i > len(self.visitedLocations):
                    break
                else:
                    loc = self.visitedLocations[-i]
                    if loc.difficulty.difficulty == -1:
                        lastVisitedLocs.append(loc)

            for loc in lastVisitedLocs:
                self.visitedLocations.remove(loc)
                self.majorLocations.append(loc)

        # compute new available locations
        self.clearLocs(self.majorLocations)
        self.computeLocationsDifficulty(self.majorLocations)

        while True:
            remainLocs = []
            okLocs = []

            for loc in lastVisitedLocs:
                if loc.difficulty == False:
                    remainLocs.append(loc)
                else:
                    okLocs.append(loc)

            if len(remainLocs) == len(lastVisitedLocs):
                # all remaining locs are seq break
                for loc in lastVisitedLocs:
                    self.majorLocations.remove(loc)
                    self.visitedLocations.append(loc)
                    if loc.difficulty == False:
                        # if the loc is still sequence break, put it back as sequence break
                        loc.difficulty = SMBool(True, -1)
                break
            else:
                # add available locs
                for loc in okLocs:
                    lastVisitedLocs.remove(loc)
                    self.majorLocations.remove(loc)
                    self.visitedLocations.append(loc)

            # compute again
            self.clearLocs(self.majorLocations)
            self.computeLocationsDifficulty(self.majorLocations)

        # return them
        self.dumpState()

    def getLocNameFromAddress(self, address):
        return self.locsAddressName[address]

    def loadPlandoTransitions(self):
        # add escape transition
        transitionsAddr = self.romLoader.getPlandoTransitions(len(vanillaBossesTransitions) + len(vanillaTransitions) + 1)
        return GraphUtils.getTransitions(transitionsAddr)

    def loadPlandoLocs(self):
        # get the addresses of the already filled locs, with the correct order
        addresses = self.romLoader.getPlandoAddresses()

        # create a copy of the locations to avoid removing locs from self.locations
        self.majorLocations = self.locations[:]

        for address in addresses:
            # TODO::compute only the difficulty of the current loc
            self.computeLocationsDifficulty(self.majorLocations)

            locName = self.getLocNameFromAddress(address)
            self.pickItemAt(locName)

    def fillPlandoLocs(self):
        self.pickup = Pickup("all")
        self.comeBack = ComeBack(self)

        # backup
        mbLoc = self.getLoc("Mother Brain")
        locationsBck = self.locations[:]

        self.lastAP = self.startLocation
        self.lastArea = self.startArea
        (self.difficulty, self.itemsOk) = self.computeDifficulty()

        # put back mother brain location
        if mbLoc not in self.majorLocations and mbLoc not in self.visitedLocations:
            self.majorLocations.append(mbLoc)

        if self.itemsOk == False:
            # add remaining locs as sequence break
            for loc in self.majorLocations[:]:
                loc.difficulty = SMBool(True, -1)
                if loc.accessPoint is not None:
                    # take first ap of the loc
                    loc.accessPoint = list(loc.AccessFrom)[0]
                self.collectMajor(loc)

        self.locations = locationsBck

    def fillGraph(self):
        # add self looping transitions on unused acces points
        usedAPs = {}
        for (src, dst) in self.curGraphTransitions:
            usedAPs[src] = True
            usedAPs[dst] = True

        singleAPs = []
        for ap in Logic.accessPoints:
            if ap.isInternal() == True:
                continue

            if ap.Name not in usedAPs:
                singleAPs.append(ap.Name)

        transitions = self.curGraphTransitions[:]
        for apName in singleAPs:
            transitions.append((apName, apName))

        return transitions

    def randoPlando(self, parameters):
        # if all the locations are visited, do nothing
        if len(self.majorLocations) == 0:
            return

        plandoLocsItems = {}
        for loc in self.visitedLocations:
            plandoLocsItems[loc.Name] = loc.itemName

        plandoCurrent = {
            "locsItems": plandoLocsItems,
            "transitions": self.fillGraph(),
            "patches": RomPatches.ActivePatches,
            "doors": DoorsManager.serialize(),
            "forbiddenItems": parameters["forbiddenItems"]
        }

        plandoCurrentJson = json.dumps(plandoCurrent)

        pythonExec = "python{}.{}".format(sys.version_info.major, sys.version_info.minor)
        params = [
            pythonExec,  os.path.expanduser("~/RandomMetroidSolver/randomizer.py"),
            '--runtime', '10',
            '--param', self.presetFileName,
            '--output', self.outputFileName,
            '--plandoRando', plandoCurrentJson,
            '--progressionSpeed', 'speedrun',
            '--minorQty', parameters["minorQty"],
            '--maxDifficulty', 'hardcore',
            '--energyQty', parameters["energyQty"],
            '--startLocation', self.startLocation
        ]

        import subprocess
        subprocess.call(params)

        with open(self.outputFileName, 'r') as jsonFile:
            data = json.load(jsonFile)

        self.errorMsg = data["errorMsg"]

        # load the locations
        if "itemLocs" in data:
            self.clearItems(reload=True)
            itemsLocs = data["itemLocs"]

            # create a copy because we need self.locations to be full, else the state will be empty
            self.majorLocations = self.locations[:]

            for itemLoc in itemsLocs:
                locName = itemLoc["Location"]["Name"]
                loc = self.getLoc(locName)
                # we can have locations from non connected areas
                if "difficulty" in itemLoc["Location"]:
                    difficulty = itemLoc["Location"]["difficulty"]
                    smbool = SMBool(difficulty["bool"], difficulty["difficulty"], difficulty["knows"], difficulty["items"])
                    loc.difficulty = smbool
                    itemName = itemLoc["Item"]["Type"]
                    loc.itemName = itemName
                    loc.accessPoint = itemLoc["Location"]["accessPoint"]
                    self.collectMajor(loc)

    def savePlando(self, lock, escapeTimer):
        # store filled locations addresses in the ROM for next creating session
        from rando.Items import ItemManager
        locsItems = {}
        itemLocs = []
        for loc in self.visitedLocations:
            locsItems[loc.Name] = loc.itemName
        for loc in self.locations:
            if loc.Name in locsItems:
                itemLocs.append(ItemLocation(ItemManager.getItem(loc.itemName), loc))
            else:
                # put nothing items in unused locations
                itemLocs.append(ItemLocation(ItemManager.getItem("Nothing"), loc))

        # patch the ROM
        if lock == True:
            import random
            magic = random.randint(1, 0xffff)
        else:
            magic = None
        romPatcher = RomPatcher(magic=magic, plando=True)
        patches = ['credits_varia.ips', 'tracking.ips', "Escape_Animals_Disable"]
        if DoorsManager.isRandom():
            patches += RomPatcher.IPSPatches['DoorsColors']
            patches.append("Enable_Backup_Saves")
        if magic != None:
            patches.insert(0, 'race_mode.ips')
            patches.append('race_mode_credits.ips')
        romPatcher.addIPSPatches(patches)

        plms = []
        if self.areaRando == True or self.bossRando == True or self.escapeRando == True:
            doors = GraphUtils.getDoorConnections(AccessGraph(Logic.accessPoints, self.fillGraph()), self.areaRando, self.bossRando, self.escapeRando, False)
            romPatcher.writeDoorConnections(doors)
            if magic == None:
                doorsPtrs = GraphUtils.getAps2DoorsPtrs()
                romPatcher.writePlandoTransitions(self.curGraphTransitions, doorsPtrs,
                                                  len(vanillaBossesTransitions) + len(vanillaTransitions))
            if self.escapeRando == True and escapeTimer != None:
                # convert from '03:00' to number of seconds
                escapeTimer = int(escapeTimer[0:2]) * 60 + int(escapeTimer[3:5])
                romPatcher.applyEscapeAttributes({'Timer': escapeTimer, 'Animals': None, 'patches': []}, plms)

        # write plm table & random doors
        romPatcher.writePlmTable(plms, self.areaRando, self.bossRando, self.startLocation)

        romPatcher.writeItemsLocs(itemLocs)
        romPatcher.writeItemsNumber()
        romPatcher.writeSpoiler(itemLocs)
        # plando is considered Full
        majorsSplit = self.masterMajorsSplit if self.masterMajorsSplit in ["FullWithHUD", "Scavenger"] else "Full"
        # for scavenger hunt, use a location with id and hud at 0xff, ie. scavenger locs list terminator
        dummyLocation = define_location(Area="", GraphArea="", SolveArea="", Name="", Address=0, Id=0xff, Class=[], CanHidden=False, Visibility="", Room='', HUD=0xff)
        romPatcher.writeSplitLocs(majorsSplit, itemLocs, [ItemLocation(Location=dummyLocation)])
        romPatcher.writeMajorsSplit(majorsSplit)
        class FakeRandoSettings:
            def __init__(self):
                self.qty = {'energy': 'plando'}
                self.progSpeed = 'plando'
                self.progDiff = 'plando'
                self.restrictions = {'Suits': False, 'Morph': 'plando'}
                self.superFun = {}
        randoSettings = FakeRandoSettings()
        romPatcher.writeRandoSettings(randoSettings, itemLocs)
        if magic != None:
            romPatcher.writeMagic()
        else:
            romPatcher.writePlandoAddresses(self.visitedLocations)

        romPatcher.commitIPS()
        romPatcher.end()

        data = romPatcher.romFile.data
        preset = os.path.splitext(os.path.basename(self.presetFileName))[0]
        seedCode = 'FX'
        if self.bossRando == True:
            seedCode = 'B'+seedCode
        if DoorsManager.isRandom():
            seedCode = 'D'+seedCode
        if self.areaRando == True:
            seedCode = 'A'+seedCode
        from time import gmtime, strftime
        fileName = 'VARIA_Plandomizer_{}{}_{}.sfc'.format(seedCode, strftime("%Y%m%d%H%M%S", gmtime()), preset)
        data["fileName"] = fileName
        # error msg in json to be displayed by the web site
        data["errorMsg"] = ""
        with open(self.outputFileName, 'w') as jsonFile:
            json.dump(data, jsonFile)

    def locNameInternal2Web(self, locName):
        return removeChars(locName, " ,()-")

    def locNameWeb2Internal(self, locNameWeb):
        return self.locsWeb2Internal[locNameWeb]

    def apNameInternal2Web(self, apName):
        return apName[0].lower() + removeChars(apName[1:], " ")

    def getWebLoc(self, locNameWeb):
        locName = self.locNameWeb2Internal(locNameWeb)
        for loc in self.locations:
            if loc.Name == locName:
                return loc
        raise Exception("Location '{}' not found".format(locName))

    def pickItemAt(self, locName):
        # collect new item at newLoc
        loc = self.getWebLoc(locName)

        # check that location has not already been visited
        if loc in self.visitedLocations:
            self.errorMsg = "Location '{}' has already been visited".format(loc.Name)
            return

        if loc.difficulty is None or loc.difficulty == False:
            # sequence break
            loc.difficulty = SMBool(True, -1)
        if loc.accessPoint is None:
            # take first ap of the loc
            loc.accessPoint = list(loc.AccessFrom)[0]
        self.collectMajor(loc)

    def setItemAt(self, locName, itemName, hide):
        # set itemName at locName

        loc = self.getWebLoc(locName)

        # check if location has not already been visited
        if loc in self.visitedLocations:
            self.errorMsg = "Location {} has already been visited".format(loc.Name)
            return

        # plando mode
        loc.itemName = itemName

        if loc.difficulty is None:
            # sequence break
            loc.difficulty = SMBool(True, -1)
        if loc.accessPoint is None:
            # take first ap of the loc
            loc.accessPoint = list(loc.AccessFrom)[0]

        if hide == True:
            loc.Visibility = 'Hidden'

        self.collectMajor(loc, itemName)

    def replaceItemAt(self, locName, itemName, hide):
        # replace itemName at locName
        loc = self.getWebLoc(locName)
        oldItemName = loc.itemName

        # replace item at the old item spot in collectedItems
        try:
            index = next(i for i, vloc in enumerate(self.visitedLocations) if vloc.Name == loc.Name)
        except Exception as e:
            self.errorMsg = "Empty location {}".format(locName)
            return

        # major item can be set multiple times in plando mode
        count = self.collectedItems.count(oldItemName)
        isCount = self.smbm.isCountItem(oldItemName)

        # update item in collected items after we check the count
        self.collectedItems[index] = itemName
        loc.itemName = itemName

        # update smbm if count item or major was only there once
        if isCount == True or count == 1:
            self.smbm.removeItem(oldItemName)

        if hide == True:
            loc.Visibility = 'Hidden'
        elif loc.CanHidden == True and loc.Visibility == 'Hidden':
            # the loc was previously hidden, set it back to visible
            loc.Visibility = 'Visible'

        self.smbm.addItem(itemName)

    def increaseItem(self, item):
        # add item at begining of collectedItems to not mess with item removal when cancelling a location
        self.collectedItems.insert(0, item)
        self.smbm.addItem(item)

    def decreaseItem(self, item):
        if item in self.collectedItems:
            self.collectedItems.remove(item)
            self.smbm.removeItem(item)

    def toggleItem(self, item):
        # add or remove a major item
        if item in self.collectedItems:
            self.collectedItems.remove(item)
            self.smbm.removeItem(item)
        else:
            self.collectedItems.insert(0, item)
            self.smbm.addItem(item)

    def clearItems(self, reload=False):
        self.collectedItems = []
        self.visitedLocations = []
        self.lastAP = self.startLocation
        self.lastArea = self.startArea
        self.majorLocations = self.locations
        if reload == True:
            for loc in self.majorLocations:
                loc.difficulty = None
        self.smbm.resetItems()

    def addTransition(self, startPoint, endPoint):
        # already check in controller if transition is valid for seed
        self.curGraphTransitions.append((startPoint, endPoint))

    def cancelLastTransition(self):
        if self.areaRando == True and self.bossRando == True:
            if len(self.curGraphTransitions) > 0:
                self.curGraphTransitions.pop()
        elif self.areaRando == True:
            if len(self.curGraphTransitions) > len(self.bossTransitions) + (1 if self.escapeRando == False else 0):
                self.curGraphTransitions.pop()
        elif self.bossRando == True:
            print("len cur graph: {} len area: {} len escape: {} len sum: {}".format(len(self.curGraphTransitions), len(self.areaTransitions), 1 if self.escapeRando == False else 0, len(self.areaTransitions) + (1 if self.escapeRando == False else 0)))
            if len(self.curGraphTransitions) > len(self.areaTransitions) + (1 if self.escapeRando == False else 0):
                self.curGraphTransitions.pop()
        elif self.escapeRando == True:
            if len(self.curGraphTransitions) > len(self.areaTransitions) + len(self.bossTransitions):
                self.curGraphTransitions.pop()

    def cancelTransition(self, startPoint):
        # get end point
        endPoint = None
        for (i, (start, end)) in enumerate(self.curGraphTransitions):
            if start == startPoint:
                endPoint = end
                break
            elif end == startPoint:
                endPoint = start
                break

        if endPoint == None:
            # shouldn't happen
            return

        # check that transition is cancelable
        if self.areaRando == True and self.bossRando == True and self.escapeRando == True:
            if len(self.curGraphTransitions) == 0:
                return
        elif self.areaRando == True and self.escapeRando == False:
            if len(self.curGraphTransitions) == len(self.bossTransitions) + len(self.escapeTransition):
                return
            elif [startPoint, endPoint] in self.bossTransitions or [endPoint, startPoint] in self.bossTransitions:
                return
            elif [startPoint, endPoint] in self.escapeTransition or [endPoint, startPoint] in self.escapeTransition:
                return
        elif self.bossRando == True and self.escapeRando == False:
            if len(self.curGraphTransitions) == len(self.areaTransitions) + len(self.escapeTransition):
                return
            elif [startPoint, endPoint] in self.areaTransitions or [endPoint, startPoint] in self.areaTransitions:
                return
            elif [startPoint, endPoint] in self.escapeTransition or [endPoint, startPoint] in self.escapeTransition:
                return
        elif self.areaRando == True and self.escapeRando == True:
            if len(self.curGraphTransitions) == len(self.bossTransitions):
                return
            elif [startPoint, endPoint] in self.bossTransitions or [endPoint, startPoint] in self.bossTransitions:
                return
        elif self.bossRando == True and self.escapeRando == True:
            if len(self.curGraphTransitions) == len(self.areaTransitions):
                return
            elif [startPoint, endPoint] in self.areaTransitions or [endPoint, startPoint] in self.areaTransitions:
                return
        elif self.escapeRando == True and self.areaRando == False and self.bossRando == False:
            if len(self.curGraphTransitions) == len(self.areaTransitions) + len(self.bossTransitions):
                return
            elif [startPoint, endPoint] in self.areaTransitions or [endPoint, startPoint] in self.areaTransitions:
                return
            elif [startPoint, endPoint] in self.bossTransitions or [endPoint, startPoint] in self.bossTransitions:
                return

        # remove transition
        self.curGraphTransitions.pop(i)

    def clearTransitions(self):
        if self.areaRando == True and self.bossRando == True:
            self.curGraphTransitions = []
        elif self.areaRando == True:
            self.curGraphTransitions = self.bossTransitions[:]
        elif self.bossRando == True:
            self.curGraphTransitions = self.areaTransitions[:]
        else:
            self.curGraphTransitions = self.bossTransitions + self.areaTransitions

        if self.escapeRando == False:
            self.curGraphTransitions += self.escapeTransition

    def clearLocs(self, locs):
        for loc in locs:
            loc.difficulty = None

    def getDiffThreshold(self):
        # in interactive solver we don't have the max difficulty parameter
        epsilon = 0.001
        return hard - epsilon

    # byteIndex is area index
    bossBitMasks = {
        "Kraid": {"byteIndex": 0x01, "bitMask": 0x01},
        "Ridley": {"byteIndex": 0x02, "bitMask": 0x01},
        "Phantoon": {"byteIndex": 0x03, "bitMask": 0x01},
        "Draygon": {"byteIndex": 0x04, "bitMask": 0x01},
        "Mother Brain": {"byteIndex": 0x05, "bitMask": 0x02}
    }

    areaAccessPoints = {
        "Lower Mushrooms Left": {"byteIndex": 36, "bitMask": 1, "room": 0x9969, "area": "Crateria"},
        "Green Pirates Shaft Bottom Right": {"byteIndex": 37, "bitMask": 16, "room": 0x99bd, "area": "Crateria"},
        "Moat Right": {"byteIndex": 148, "bitMask": 4, "room": 0x95ff, "area": "Crateria"},
        "Keyhunter Room Bottom": {"byteIndex": 156, "bitMask": 32, "room": 0x948c, "area": "Crateria"},
        "Morph Ball Room Left": {"byteIndex": 46, "bitMask": 4, "room": 0x9e9f, "area": "Brinstar"},
        "Green Brinstar Elevator": {"byteIndex": 36, "bitMask": 2, "room": 0x9938, "area": "Crateria"},
        "Green Hill Zone Top Right": {"byteIndex": 46, "bitMask": 8, "room": 0x9e52, "area": "Brinstar"},
        "Noob Bridge Right": {"byteIndex": 184, "bitMask": 128, "room": 0x9fba, "area": "Brinstar"},
        "West Ocean Left": {"byteIndex": 148, "bitMask": 2, "room": 0x93fe, "area": "Crateria"},
        "Crab Maze Left": {"byteIndex": 170, "bitMask": 4, "room": 0x957d, "area": "Crateria"},
        "Lava Dive Right": {"byteIndex": 47, "bitMask": 64, "room": 0xaf14, "area": "Norfair"},
        "Three Muskateers Room Left": {"byteIndex": 19, "bitMask": 2, "room": 0xb656, "area": "Norfair"},
        "Warehouse Zeela Room Left": {"byteIndex": 205, "bitMask": 8, "room": 0xa471, "area": "Brinstar"},
        "Warehouse Entrance Left": {"byteIndex": 205, "bitMask": 64, "room": 0xa6a1, "area": "Brinstar"},
        "Warehouse Entrance Right": {"byteIndex": 205, "bitMask": 16, "room": 0xa6a1, "area": "Brinstar"},
        "Single Chamber Top Right": {"byteIndex": 19, "bitMask": 4, "room": 0xad5e, "area": "Norfair"},
        "Kronic Boost Room Bottom Left": {"byteIndex": 47, "bitMask": 32, "room": 0xae74, "area": "Norfair"},
        "Crocomire Speedway Bottom": {"byteIndex": 41, "bitMask": 1, "room": 0xa923, "area": "Norfair"},
        "Crocomire Room Top": {"byteIndex": 45, "bitMask": 1, "room": 0xa98d, "area": "Norfair"},
        "Main Street Bottom": {"byteIndex": 69, "bitMask": 16, "room": 0xcfc9, "area": "Maridia"},
        "Crab Hole Bottom Left": {"byteIndex": 74, "bitMask": 128, "room": 0xd21c, "area": "Maridia"},
        "Red Fish Room Left": {"byteIndex": 33, "bitMask": 8, "room": 0xd104, "area": "Maridia"},
        "Crab Shaft Right": {"byteIndex": 46, "bitMask": 16, "room": 0xd1a3, "area": "Maridia"},
        "Aqueduct Top Left": {"byteIndex": 46, "bitMask": 8, "room": 0xd5a7, "area": "Maridia"},
        "Le Coude Right": {"byteIndex": 170, "bitMask": 8, "room": 0x95a8, "area": "Crateria"},
        "Red Tower Top Left": {"byteIndex": 184, "bitMask": 64, "room": 0xa253, "area": "Brinstar"},
        "Caterpillar Room Top Right": {"byteIndex": 160, "bitMask": 1, "room": 0xa322, "area": "Brinstar"},
        "Red Brinstar Elevator": {"byteIndex": 160, "bitMask": 32, "room": 0x962a, "area": "Crateria"},
        "East Tunnel Right": {"byteIndex": 77, "bitMask": 8, "room": 0xcf80, "area": "Maridia"},
        "East Tunnel Top Right": {"byteIndex": 73, "bitMask": 1, "room": 0xcf80, "area": "Maridia"},
        "Glass Tunnel Top": {"byteIndex": 73, "bitMask": 16, "room": 0xcefb, "area": "Maridia"},
        "Golden Four": {"byteIndex": 37, "bitMask": 8, "room": 0xa5ed, "area": "Crateria"}
    }

    bossAccessPoints = {
        "PhantoonRoomOut": {"byteIndex": 82, "bitMask": 32, "room": 0xcc6f, "area": "WreckedShip"},
        "PhantoonRoomIn": {"byteIndex": 82, "bitMask": 16, "room": 0xcd13, "area": "WreckedShip"},
        "RidleyRoomOut": {"byteIndex": 71, "bitMask": 128, "room": 0xb37a, "area": "Norfair"},
        "RidleyRoomIn": {"byteIndex": 70, "bitMask": 1, "room": 0xb32e, "area": "Norfair"},
        "KraidRoomOut": {"byteIndex": 210, "bitMask": 2, "room": 0xa56b, "area": "Brinstar"},
        "KraidRoomIn": {"byteIndex": 210, "bitMask": 1, "room": 0xa59f, "area": "Brinstar"},
        "DraygonRoomOut": {"byteIndex": 169, "bitMask": 64, "room": 0xd78f, "area": "Maridia"},
        "DraygonRoomIn": {"byteIndex": 169, "bitMask": 128, "room": 0xda60, "area": "Maridia"}
    }

    nothingScreens = {
        "Energy Tank, Gauntlet": {"byteIndex": 14, "bitMask": 64, "room": 0x965b, "area": "Crateria"},
        "Bomb": {"byteIndex": 31, "bitMask": 64, "room": 0x9804, "area": "Crateria"},
        "Energy Tank, Terminator": {"byteIndex": 29, "bitMask": 8, "room": 0x990d, "area": "Crateria"},
        "Reserve Tank, Brinstar": {"byteIndex": 21, "bitMask": 4, "room": 0x9c07, "area": "Brinstar"},
        "Charge Beam": {"byteIndex": 50, "bitMask": 64, "room": 0x9d19, "area": "Brinstar"},
        "Morphing Ball": {"byteIndex": 47, "bitMask": 64, "room": 0x9e9f, "area": "Brinstar"},
        "Energy Tank, Brinstar Ceiling": {"byteIndex": 47, "bitMask": 1, "room": 0x9f64, "area": "Brinstar"},
        "Energy Tank, Etecoons": {"byteIndex": 44, "bitMask": 2, "room": 0xa011, "area": "Brinstar"},
        "Energy Tank, Waterway": {"byteIndex": 57, "bitMask": 128, "room": 0xa0d2, "area": "Brinstar"},
        "Energy Tank, Brinstar Gate": {"byteIndex": 38, "bitMask": 4, "room": 0xa15b, "area": "Brinstar"},
        "X-Ray Scope": {"byteIndex": 66, "bitMask": 1, "room": 0xa2ce, "area": "Brinstar"},
        "Spazer": {"byteIndex": 200, "bitMask": 2, "room": 0xa447, "area": "Brinstar"},
        "Energy Tank, Kraid": {"byteIndex": 209, "bitMask": 16, "room": 0xa4b1, "area": "Brinstar"},
        "Varia Suit": {"byteIndex": 211, "bitMask": 64, "room": 0xa6e2, "area": "Brinstar"},
        "Ice Beam": {"byteIndex": 12, "bitMask": 4, "room": 0xa890, "area": "Norfair"},
        "Energy Tank, Crocomire": {"byteIndex": 46, "bitMask": 16, "room": 0xa98d, "area": "Norfair"},
        "Hi-Jump Boots": {"byteIndex": 28, "bitMask": 1, "room": 0xa9e5, "area": "Norfair"},
        "Grapple Beam": {"byteIndex": 68, "bitMask": 16, "room": 0xac2b, "area": "Norfair"},
        "Reserve Tank, Norfair": {"byteIndex": 14, "bitMask": 32, "room": 0xac5a, "area": "Norfair"},
        "Speed Booster": {"byteIndex": 140, "bitMask": 4, "room": 0xad1b, "area": "Norfair"},
        "Wave Beam": {"byteIndex": 23, "bitMask": 4, "room": 0xadde, "area": "Norfair"},
        "Energy Tank, Ridley": {"byteIndex": 74, "bitMask": 2, "room": 0xb698, "area": "Norfair"},
        "Screw Attack": {"byteIndex": 70, "bitMask": 8, "room": 0xb6c1, "area": "Norfair"},
        "Energy Tank, Firefleas": {"byteIndex": 176, "bitMask": 4, "room": 0xb6ee, "area": "Norfair"},
        "Reserve Tank, Wrecked Ship": {"byteIndex": 49, "bitMask": 1, "room": 0xc98e, "area": "WreckedShip"},
        "Energy Tank, Wrecked Ship": {"byteIndex": 58, "bitMask": 32, "room": 0xcc27, "area": "WreckedShip"},
        "Right Super, Wrecked Ship": {"byteIndex": 74, "bitMask": 4, "room": 0xcdf1, "area": "WreckedShip"},
        "Gravity Suit": {"byteIndex": 57, "bitMask": 32, "room": 0xce40, "area": "WreckedShip"},
        "Energy Tank, Mama turtle": {"byteIndex": 54, "bitMask": 16, "room": 0xd055, "area": "Maridia"},
        "Plasma Beam": {"byteIndex": 15, "bitMask": 8, "room": 0xd2aa, "area": "Maridia"},
        "Reserve Tank, Maridia": {"byteIndex": 62, "bitMask": 8, "room": 0xd4ef, "area": "Maridia"},
        "Spring Ball": {"byteIndex": 196, "bitMask": 64, "room": 0xd6d0, "area": "Maridia"},
        "Energy Tank, Botwoon": {"byteIndex": 39, "bitMask": 4, "room": 0xd7e4, "area": "Maridia"},
        "Space Jump": {"byteIndex": 172, "bitMask": 2, "room": 0xd9aa, "area": "Maridia"},
        "Power Bomb (Crateria surface)": {"byteIndex": 136, "bitMask": 64, "room": 0x93aa, "area": "Crateria"},
        "Missile (outside Wrecked Ship bottom)": {"byteIndex": 152, "bitMask": 2, "room": 0x93fe, "area": "Crateria"},
        "Missile (outside Wrecked Ship top)": {"byteIndex": 132, "bitMask": 1, "room": 0x93fe, "area": "Crateria"},
        "Missile (outside Wrecked Ship middle)": {"byteIndex": 140, "bitMask": 2, "room": 0x93fe, "area": "Crateria"},
        "Missile (Crateria moat)": {"byteIndex": 148, "bitMask": 8, "room": 0x95ff, "area": "Crateria"},
        "Missile (Crateria bottom)": {"byteIndex": 78, "bitMask": 8, "room": 0x975c, "area": "Crateria"},
        "Missile (Crateria gauntlet right)": {"byteIndex": 17, "bitMask": 16, "room": 0x99bd, "area": "Crateria"},
        "Missile (Crateria gauntlet left)": {"byteIndex": 17, "bitMask": 16, "room": 0x99bd, "area": "Crateria"},
        "Super Missile (Crateria)": {"byteIndex": 43, "bitMask": 128, "room": 0x99f9, "area": "Crateria"},
        "Missile (Crateria middle)": {"byteIndex": 34, "bitMask": 128, "room": 0x9a90, "area": "Crateria"},
        "Power Bomb (green Brinstar bottom)": {"byteIndex": 33, "bitMask": 8, "room": 0x9ad9, "area": "Brinstar"},
        "Super Missile (pink Brinstar)": {"byteIndex": 43, "bitMask": 128, "room": 0x9b5b, "area": "Brinstar"},
        "Missile (green Brinstar below super missile)": {"byteIndex": 21, "bitMask": 16, "room": 0x9bc8, "area": "Brinstar"},
        "Super Missile (green Brinstar top)": {"byteIndex": 17, "bitMask": 32, "room": 0x9bc8, "area": "Brinstar"},
        "Missile (green Brinstar behind missile)": {"byteIndex": 21, "bitMask": 2, "room": 0x9c07, "area": "Brinstar"},
        "Missile (green Brinstar behind reserve tank)": {"byteIndex": 21, "bitMask": 2, "room": 0x9c07, "area": "Brinstar"},
        "Missile (pink Brinstar top)": {"byteIndex": 34, "bitMask": 64, "room": 0x9d19, "area": "Brinstar"},
        "Missile (pink Brinstar bottom)": {"byteIndex": 46, "bitMask": 64, "room": 0x9d19, "area": "Brinstar"},
        "Power Bomb (pink Brinstar)": {"byteIndex": 37, "bitMask": 1, "room": 0x9e11, "area": "Brinstar"},
        "Missile (green Brinstar pipe)": {"byteIndex": 50, "bitMask": 2, "room": 0x9e52, "area": "Brinstar"},
        "Power Bomb (blue Brinstar)": {"byteIndex": 46, "bitMask": 1, "room": 0x9e9f, "area": "Brinstar"},
        "Missile (blue Brinstar middle)": {"byteIndex": 172, "bitMask": 128, "room": 0x9f64, "area": "Brinstar"},
        "Super Missile (green Brinstar bottom)": {"byteIndex": 44, "bitMask": 4, "room": 0xa051, "area": "Brinstar"},
        "Missile (blue Brinstar bottom)": {"byteIndex": 51, "bitMask": 8, "room": 0xa107, "area": "Brinstar"},
        "Missile (blue Brinstar top)": {"byteIndex": 39, "bitMask": 4, "room": 0xa1d8, "area": "Brinstar"},
        "Missile (blue Brinstar behind missile)": {"byteIndex": 39, "bitMask": 4, "room": 0xa1d8, "area": "Brinstar"},
        "Power Bomb (red Brinstar sidehopper room)": {"byteIndex": 164, "bitMask": 16, "room": 0xa37c, "area": "Brinstar"},
        "Power Bomb (red Brinstar spike room)": {"byteIndex": 176, "bitMask": 16, "room": 0xa3ae, "area": "Brinstar"},
        "Missile (red Brinstar spike room)": {"byteIndex": 176, "bitMask": 32, "room": 0xa3ae, "area": "Brinstar"},
        "Missile (Kraid)": {"byteIndex": 205, "bitMask": 1, "room": 0xa4da, "area": "Brinstar"},
        "Missile (lava room)": {"byteIndex": 22, "bitMask": 128, "room": 0xa788, "area": "Norfair"},
        "Missile (below Ice Beam)": {"byteIndex": 20, "bitMask": 32, "room": 0xa8f8, "area": "Norfair"},
        "Missile (above Crocomire)": {"byteIndex": 29, "bitMask": 16, "room": 0xaa0e, "area": "Norfair"},
        "Missile (Hi-Jump Boots)": {"byteIndex": 25, "bitMask": 128, "room": 0xaa41, "area": "Norfair"},
        "Energy Tank (Hi-Jump Boots)": {"byteIndex": 25, "bitMask": 64, "room": 0xaa41, "area": "Norfair"},
        "Power Bomb (Crocomire)": {"byteIndex": 45, "bitMask": 64, "room": 0xaade, "area": "Norfair"},
        "Missile (below Crocomire)": {"byteIndex": 65, "bitMask": 2, "room": 0xab3b, "area": "Norfair"},
        "Missile (Grapple Beam)": {"byteIndex": 65, "bitMask": 128, "room": 0xab8f, "area": "Norfair"},
        "Missile (Norfair Reserve Tank)": {"byteIndex": 14, "bitMask": 32, "room": 0xac5a, "area": "Norfair"},
        "Missile (bubble Norfair green door)": {"byteIndex": 14, "bitMask": 4, "room": 0xac83, "area": "Norfair"},
        "Missile (bubble Norfair)": {"byteIndex": 26, "bitMask": 1, "room": 0xacb3, "area": "Norfair"},
        "Missile (Speed Booster)": {"byteIndex": 140, "bitMask": 8, "room": 0xacf0, "area": "Norfair"},
        "Missile (Wave Beam)": {"byteIndex": 23, "bitMask": 32, "room": 0xadad, "area": "Norfair"},
        "Missile (Gold Torizo)": {"byteIndex": 66, "bitMask": 32, "room": 0xb283, "area": "Norfair"},
        "Super Missile (Gold Torizo)": {"byteIndex": 66, "bitMask": 16, "room": 0xb283, "area": "Norfair"},
        "Missile (Mickey Mouse room)": {"byteIndex": 47, "bitMask": 8, "room": 0xb40a, "area": "Norfair"},
        "Missile (lower Norfair above fire flea room)": {"byteIndex": 152, "bitMask": 16, "room": 0xb510, "area": "Norfair"},
        "Power Bomb (lower Norfair above fire flea room)": {"byteIndex": 156, "bitMask": 4, "room": 0xb55a, "area": "Norfair"},
        "Power Bomb (Power Bombs of shame)": {"byteIndex": 188, "bitMask": 128, "room": 0xb5d5, "area": "Norfair"},
        "Missile (lower Norfair near Wave Beam)": {"byteIndex": 27, "bitMask": 4, "room": 0xb656, "area": "Norfair"},
        "Missile (Wrecked Ship middle)": {"byteIndex": 69, "bitMask": 8, "room": 0xcaf6, "area": "WreckedShip"},
        "Missile (Gravity Suit)": {"byteIndex": 57, "bitMask": 4, "room": 0xc98e, "area": "WreckedShip"},
        "Missile (Wrecked Ship top)": {"byteIndex": 46, "bitMask": 4, "room": 0xcaae, "area": "WreckedShip"},
        "Super Missile (Wrecked Ship left)": {"byteIndex": 73, "bitMask": 1, "room": 0xcda8, "area": "WreckedShip"},
        "Missile (green Maridia shinespark)": {"byteIndex": 53, "bitMask": 32, "room": 0xcfc9, "area": "Maridia"},
        "Super Missile (green Maridia)": {"byteIndex": 49, "bitMask": 16, "room": 0xcfc9, "area": "Maridia"},
        "Missile (green Maridia tatori)": {"byteIndex": 58, "bitMask": 16, "room": 0xd055, "area": "Maridia"},
        # TODO::check these two if they are not swapped on the map ?
        "Super Missile (yellow Maridia)": {"byteIndex": 29, "bitMask": 8, "room": 0xd13b, "area": "Maridia"},
        "Missile (yellow Maridia super missile)": {"byteIndex": 29, "bitMask": 8, "room": 0xd13b, "area": "Maridia"},
        "Missile (yellow Maridia false wall)": {"byteIndex": 30, "bitMask": 8, "room": 0xd1dd, "area": "Maridia"},
        "Missile (left Maridia sand pit room)": {"byteIndex": 62, "bitMask": 8, "room": 0xd4ef, "area": "Maridia"},
        "Missile (right Maridia sand pit room)": {"byteIndex": 62, "bitMask": 1, "room": 0xd51e, "area": "Maridia"},
        "Power Bomb (right Maridia sand pit room)": {"byteIndex": 67, "bitMask": 128, "room": 0xd51e, "area": "Maridia"},
        "Missile (pink Maridia)": {"byteIndex": 43, "bitMask": 128, "room": 0xd5a7, "area": "Maridia"},
        "Super Missile (pink Maridia)": {"byteIndex": 43, "bitMask": 64, "room": 0xd5a7, "area": "Maridia"},
        "Missile (Draygon)": {"byteIndex": 161, "bitMask": 32, "room": 0xd78f, "area": "Maridia"}
    }

    doorsScreen = {
        # crateria
        'LandingSiteRight': {"byteIndex": 23, "bitMask": 1, "room": 0x91f8, "area": "Crateria"},
        'LandingSiteTopRight': {"byteIndex": 11, "bitMask": 1, "room": 0x91f8, "area": "Crateria"},
        'KihunterBottom': {"byteIndex": 156, "bitMask": 32, "room": 0x948c, "area": "Crateria"},
        'KihunterRight': {"byteIndex": 148, "bitMask": 16, "room": 0x948c, "area": "Crateria"},
        'FlywayRight': {"byteIndex": 31, "bitMask": 128, "room": 0x9879, "area": "Crateria"},
        'GreenPiratesShaftBottomRight': {"byteIndex": 37, "bitMask": 16, "room": 0x99bd, "area": "Crateria"},
        'RedBrinstarElevatorTop': {"byteIndex": 160, "bitMask": 32, "room": 0x962a, "area": "Crateria"},
        'ClimbRight': {"byteIndex": 70, "bitMask": 8, "room": 0x96ba, "area": "Crateria"},
        # blue brinstar
        'ConstructionZoneRight': {"byteIndex": 47, "bitMask": 4, "room": 0x9f11, "area": "Brinstar"},
        # green brinstar
        'GreenHillZoneTopRight': {"byteIndex": 46, "bitMask": 8, "room": 0x9e52, "area": "Brinstar"},
        'NoobBridgeRight': {"byteIndex": 184, "bitMask": 128, "room": 0x9fba, "area": "Brinstar"},
        'MainShaftRight': {"byteIndex": 21, "bitMask": 64, "room": 0x9ad9, "area": "Brinstar"},
        'MainShaftBottomRight': {"byteIndex": 29, "bitMask": 64, "room": 0x9ad9, "area": "Brinstar"},
        'EarlySupersRight': {"byteIndex": 21, "bitMask": 8, "room": 0x9bc8, "area": "Brinstar"},
        'EtecoonEnergyTankLeft': {"byteIndex": 44, "bitMask": 2, "room": 0xa011, "area": "Brinstar"},
        # pink brinstar
        'BigPinkTopRight': {"byteIndex": 22, "bitMask": 32, "room": 0x9d19, "area": "Brinstar"},
        'BigPinkRight': {"byteIndex": 38, "bitMask": 32, "room": 0x9d19, "area": "Brinstar"},
        'BigPinkBottomRight': {"byteIndex": 46, "bitMask": 32, "room": 0x9d19, "area": "Brinstar"},
        'BigPinkBottomLeft': {"byteIndex": 57, "bitMask": 1, "room": 0x9d19, "area": "Brinstar"},
        # red brinstar
        'RedTowerLeft': {"byteIndex": 192, "bitMask": 64, "room": 0xa253, "area": "Brinstar"},
        'RedBrinstarFirefleaLeft': {"byteIndex": 67, "bitMask": 64, "room": 0xa293, "area": "Brinstar"},
        'RedTowerElevatorTopLeft': {"byteIndex": 160, "bitMask": 4, "room": 0xa322, "area": "Brinstar"},
        'RedTowerElevatorLeft': {"byteIndex": 168, "bitMask": 4, "room": 0xa322, "area": "Brinstar"},
        'RedTowerElevatorBottomLeft': {"byteIndex": 176, "bitMask": 4, "room": 0xa322, "area": "Brinstar"},
        'BelowSpazerTopRight': {"byteIndex": 200, "bitMask": 4, "room": 0xa408, "area": "Brinstar"},
        # Wrecked ship
        'WestOceanRight': {"byteIndex": 149, "bitMask": 4, "room": 0x93fe, "area": "Crateria"},
        'LeCoudeBottom': {"byteIndex": 170, "bitMask": 8, "room": 0x95a8, "area": "Crateria"},
        'WreckedShipMainShaftBottom': {"byteIndex": 78, "bitMask": 128, "room": 0xcaf6, "area": "WreckedShip"},
        'ElectricDeathRoomTopLeft': {"byteIndex": 58, "bitMask": 4, "room": 0xcbd5, "area": "WreckedShip"},
        # Upper Norfair
        'BusinessCenterTopLeft': {"byteIndex": 17, "bitMask": 32, "room": 0xa7de, "area": "Norfair"},
        'BusinessCenterBottomLeft': {"byteIndex": 25, "bitMask": 32, "room": 0xa7de, "area": "Norfair"},
        'CathedralEntranceRight': {"byteIndex": 17, "bitMask": 4, "room": 0xa7b3, "area": "Norfair"},
        'CathedralRight': {"byteIndex": 22, "bitMask": 128, "room": 0xa788, "area": "Norfair"},
        'BubbleMountainTopRight': {"byteIndex": 14, "bitMask": 1, "room": 0xacb3, "area": "Norfair"},
        'BubbleMountainTopLeft': {"byteIndex": 14, "bitMask": 2, "room": 0xacb3, "area": "Norfair"},
        'SpeedBoosterHallRight': {"byteIndex": 140, "bitMask": 8, "room": 0xacf0, "area": "Norfair"},
        'SingleChamberRight': {"byteIndex": 23, "bitMask": 128, "room": 0xad5e, "area": "Norfair"},
        'DoubleChamberRight': {"byteIndex": 23, "bitMask": 8, "room": 0xadad, "area": "Norfair"},
        'KronicBoostBottomLeft': {"byteIndex": 47, "bitMask": 32, "room": 0xae74, "area": "Norfair"},
        'CrocomireSpeedwayBottom': {"byteIndex": 41, "bitMask": 1, "room": 0xa923, "area": "Norfair"},
        # Crocomire
        'PostCrocomireUpperLeft': {"byteIndex": 45, "bitMask": 32, "room": 0xaa82, "area": "Norfair"},
        'PostCrocomireShaftRight': {"byteIndex": 65, "bitMask": 32, "room": 0xab07, "area": "Norfair"},
        # Lower Norfair
        'RedKihunterShaftBottom': {"byteIndex": 184, "bitMask": 4, "room": 0xb585, "area": "Norfair"},
        'WastelandLeft': {"byteIndex": 196, "bitMask": 64, "room": 0xb5d5, "area": "Norfair"},
        # Maridia
        'MainStreetBottomRight': {"byteIndex": 69, "bitMask": 16, "room": 0xcfc9, "area": "Maridia"},
        'FishTankRight': {"byteIndex": 66, "bitMask": 128, "room": 0xd017, "area": "Maridia"},
        'CrabShaftRight': {"byteIndex": 46, "bitMask": 16, "room": 0xd1a3, "area": "Maridia"},
        'ColosseumBottomRight': {"byteIndex": 161, "bitMask": 128, "room": 0xd72a, "area": "Maridia"},
        'PlasmaSparkBottom': {"byteIndex": 22, "bitMask": 2, "room": 0xd340, "area": "Maridia"},
        'OasisTop': {"byteIndex": 66, "bitMask": 2, "room": 0xd48e, "area": "Maridia"}
    }

    mapOffsetEnum = {
        "Crateria": 0,
        "Brinstar": 0x100,
        "Norfair": 0x200,
        "WreckedShip": 0x300,
        "Maridia": 0x400
    }

    def importDump(self, dumpFileName):
        with open(dumpFileName, 'r') as jsonFile:
            dumpData = json.load(jsonFile)

        dataEnum = {
            "state": '1',
            "map": '2',
            "curMap": '3',
            "samus": '4',
            "items": '5',
            "boss": '6'
        }

        currentState = dumpData["currentState"]
        self.locDelta = 0

        for dataType, offset in dumpData["stateDataOffsets"].items():
            if dataType == dataEnum["items"]:
                # get item data, loop on all locations to check if they have been visited
                for loc in self.locations:
                    # loc id is used to index in the items data, boss locations don't have an Id
                    if loc.Id is None:
                        continue
                    # nothing locs are handled later
                    if loc.itemName == 'Nothing':
                        continue
                    byteIndex = loc.Id >> 3
                    bitMask = 0x01 << (loc.Id & 7)
                    if currentState[offset + byteIndex] & bitMask != 0:
                        if loc not in self.visitedLocations:
                            print("add visited loc: {}".format(loc.Name))
                            self.pickItemAt(self.locNameInternal2Web(loc.Name))
                            self.locDelta += 1
                    else:
                        if loc in self.visitedLocations:
                            print("remove visited loc: {}".format(loc.Name))
                            self.removeItemAt(self.locNameInternal2Web(loc.Name))
            elif dataType == dataEnum["boss"]:
                for boss, bossData in self.bossBitMasks.items():
                    byteIndex = bossData["byteIndex"]
                    bitMask = bossData["bitMask"]
                    loc = self.getLoc(boss)
                    if currentState[offset + byteIndex] & bitMask != 0:
                        if loc not in self.visitedLocations:
                            print("add boss loc: {}".format(loc.Name))
                            self.pickItemAt(self.locNameInternal2Web(loc.Name))
                            self.locDelta += 1
                    else:
                        if loc in self.visitedLocations:
                            print("remove visited boss loc: {}".format(loc.Name))
                            self.removeItemAt(self.locNameInternal2Web(loc.Name))
            elif dataType == dataEnum["map"]:
                if self.areaRando or self.bossRando:
                    availAPs = set()
                    for apName, apData in self.areaAccessPoints.items():
                        if self.isElemAvailable(currentState, offset, apData):
                            availAPs.add(apName)
                    for apName, apData in self.bossAccessPoints.items():
                        if self.isElemAvailable(currentState, offset, apData):
                            availAPs.add(apName)

                    # static transitions
                    if self.areaRando == True and self.bossRando == True:
                        staticTransitions = []
                        possibleTransitions = self.bossTransitions + self.areaTransitions
                    elif self.areaRando == True:
                        staticTransitions = self.bossTransitions[:]
                        possibleTransitions = self.areaTransitions[:]
                    elif self.bossRando == True:
                        staticTransitions = self.areaTransitions[:]
                        possibleTransitions = self.bossTransitions[:]
                    if self.escapeRando == False:
                        staticTransitions += self.escapeTransition

                    # remove static transitions from current transitions
                    dynamicTransitions = self.curGraphTransitions[:]
                    for transition in self.curGraphTransitions:
                        if transition in staticTransitions:
                            dynamicTransitions.remove(transition)

                    # remove dynamic transitions not visited
                    for transition in dynamicTransitions:
                        if transition[0] not in availAPs and transition[1] not in availAPs:
                            print("remove transition: {}".format(transition))
                            self.curGraphTransitions.remove(transition)

                    # add new transitions
                    for transition in possibleTransitions:
                        if transition[0] in availAPs and transition[1] in availAPs:
                            print("add transition: {}".format(transition))
                            self.curGraphTransitions.append(transition)

                if self.hasNothing:
                    # get locs with nothing
                    locsNothing = [loc for loc in self.locations if loc.itemName == 'Nothing']
                    for loc in locsNothing:
                        locData = self.nothingScreens[loc.Name]
                        if self.isElemAvailable(currentState, offset, locData):
                            # nothing has been seen, check if loc is already visited
                            if not loc in self.visitedLocations:
                                # visit it
                                print("add visited nothing loc: {}".format(loc.Name))
                                self.pickItemAt(self.locNameInternal2Web(loc.Name))
                                self.locDelta += 1
                        else:
                            # nothing not yet seed, check if loc is already visited
                            if loc in self.visitedLocations:
                                # unvisit it
                                print("remove visited nothing loc: {}".format(loc.Name))
                                self.removeItemAt(self.locNameInternal2Web(loc.Name))
                if self.doorsRando:
                    # get currently hidden / revealed doors names in sets
                    (hiddenDoors, revealedDoor) = DoorsManager.getDoorsState()
                    for doorName in hiddenDoors:
                        # check if door is still hidden
                        doorData = self.doorsScreen[doorName]
                        if self.isElemAvailable(currentState, offset, doorData):
                            DoorsManager.switchVisibility(doorName)
                    for doorName in revealedDoor:
                        # check if door is still visible
                        doorData = self.doorsScreen[doorName]
                        if not self.isElemAvailable(currentState, offset, doorData):
                            DoorsManager.switchVisibility(doorName)

    def isElemAvailable(self, currentState, offset, apData):
        byteIndex = apData["byteIndex"]
        bitMask = apData["bitMask"]
        return currentState[offset + byteIndex + self.mapOffsetEnum[apData["area"]]] & bitMask != 0
