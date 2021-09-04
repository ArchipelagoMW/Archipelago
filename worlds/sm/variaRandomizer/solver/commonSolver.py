import logging, time

from logic.smboolmanager import SMBoolManagerPlando as SMBoolManager
from logic.smbool import SMBool, smboolFalse
from logic.helpers import Bosses
from rom.romloader import RomLoader
from rom.rom_patches import RomPatches
from graph.graph import AccessGraphSolver as AccessGraph
from utils.utils import PresetLoader
from solver.conf import Conf
from graph.graph_utils import vanillaTransitions, vanillaBossesTransitions, vanillaEscapeTransitions, GraphUtils, getAccessPoint
from utils.parameters import easy, medium, hard, harder, hardcore, mania, infinity
from utils.doorsmanager import DoorsManager
from logic.logic import Logic

class CommonSolver(object):
    def loadRom(self, rom, interactive=False, magic=None, startLocation=None):
        self.scavengerOrder = []
        # startLocation param is only use for seedless
        if rom == None:
            # TODO::add a --logic parameter for seedless
            Logic.factory('vanilla')
            self.romFileName = 'seedless'
            self.majorsSplit = 'Full'
            self.masterMajorsSplit = 'Full'
            self.areaRando = True
            self.bossRando = True
            self.escapeRando = False
            self.escapeTimer = "03:00"
            self.startLocation = startLocation
            RomPatches.setDefaultPatches(startLocation)
            self.startArea = getAccessPoint(startLocation).Start['solveArea']
            # in seedless load all the vanilla transitions
            self.areaTransitions = vanillaTransitions[:]
            self.bossTransitions = vanillaBossesTransitions[:]
            self.escapeTransition = [vanillaEscapeTransitions[0]]
            # in seedless we allow mixing of area and boss transitions
            self.hasMixedTransitions = True
            self.curGraphTransitions = self.bossTransitions + self.areaTransitions + self.escapeTransition
            self.locations = Logic.locations
            for loc in self.locations:
                loc.itemName = 'Nothing'
            # set doors related to default patches
            DoorsManager.setDoorsColor()
            self.doorsRando = False
            self.hasNothing = False
        else:
            self.romFileName = rom
            self.romLoader = RomLoader.factory(rom, magic)
            Logic.factory(self.romLoader.readLogic())
            self.romLoader.readNothingId()
            self.locations = Logic.locations
            (self.majorsSplit, self.masterMajorsSplit) = self.romLoader.assignItems(self.locations)
            (self.startLocation, self.startArea, startPatches) = self.romLoader.getStartAP()
            if not GraphUtils.isStandardStart(self.startLocation) and self.majorsSplit != 'Full':
                # update major/chozo locs in non standard start
                self.romLoader.updateSplitLocs(self.majorsSplit, self.locations)
            (self.areaRando, self.bossRando, self.escapeRando) = self.romLoader.loadPatches()
            RomPatches.ActivePatches += startPatches
            self.escapeTimer = self.romLoader.getEscapeTimer()
            self.doorsRando = self.romLoader.loadDoorsColor()
            self.hasNothing = self.checkLocsForNothing()
            if self.majorsSplit == 'Scavenger':
                self.scavengerOrder = self.romLoader.loadScavengerOrder(self.locations)

            if interactive == False:
                print("ROM {} majors: {} area: {} boss: {} escape: {} patches: {} activePatches: {}".format(rom, self.majorsSplit, self.areaRando, self.bossRando, self.escapeRando, sorted(self.romLoader.getPatches()), sorted(RomPatches.ActivePatches)))
            else:
                print("majors: {} area: {} boss: {} escape: {} activepatches: {}".format(self.majorsSplit, self.areaRando, self.bossRando, self.escapeRando, sorted(RomPatches.ActivePatches)))

            (self.areaTransitions, self.bossTransitions, self.escapeTransition, self.hasMixedTransitions) = self.romLoader.getTransitions()
            if interactive == True and self.debug == False:
                # in interactive area mode we build the graph as we play along
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
            else:
                self.curGraphTransitions = self.bossTransitions + self.areaTransitions + self.escapeTransition

        self.smbm = SMBoolManager()
        self.areaGraph = AccessGraph(Logic.accessPoints, self.curGraphTransitions)

        # store at each step how many locations are available
        self.nbAvailLocs = []

        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("Display items at locations:")
            for loc in self.locations:
                self.log.debug('{:>50}: {:>16}'.format(loc.Name, loc.itemName))

    def loadPreset(self, presetFileName):
        presetLoader = PresetLoader.factory(presetFileName)
        presetLoader.load()
        self.smbm.createKnowsFunctions()

        if self.log.getEffectiveLevel() == logging.DEBUG:
            presetLoader.printToScreen()

    def getLoc(self, locName):
        for loc in self.locations:
            if loc.Name == locName:
                return loc

    def getNextDifficulty(self, difficulty):
        nextDiffs = {
            0: easy,
            easy: medium,
            medium: hard,
            hard: harder,
            harder: hardcore,
            hardcore: mania,
            mania: infinity
        }
        return nextDiffs[difficulty]

    def checkLocsForNothing(self):
        # for the auto tracker, need to know if we have to track nothing items
        return any(loc.itemName == "Nothing" for loc in self.locations)

    def computeLocationsDifficulty(self, locations, phase="major"):
        difficultyTarget = Conf.difficultyTarget
        nextLocations = locations

        # before looping on all diff targets, get only the available locations with diff target infinity
        if difficultyTarget != infinity:
            self.areaGraph.getAvailableLocations(nextLocations, self.smbm, infinity, self.lastAP)
            nextLocations = [loc for loc in nextLocations if loc.difficulty]

        while True:
            self.areaGraph.getAvailableLocations(nextLocations, self.smbm, difficultyTarget, self.lastAP)
            # check post available functions too
            for loc in nextLocations:
                loc.evalPostAvailable(self.smbm)

            self.areaGraph.useCache(True)
            # also check if we can come back to current AP from the location
            for loc in nextLocations:
                loc.evalComeBack(self.smbm, self.areaGraph, self.lastAP)
            self.areaGraph.useCache(False)

            nextLocations = [loc for loc in nextLocations if not loc.difficulty]
            if not nextLocations:
                break

            if difficultyTarget == infinity:
                # we've tested all the difficulties
                break

            # start a new loop with next difficulty
            difficultyTarget = self.getNextDifficulty(difficultyTarget)

        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("available {} locs:".format(phase))
            for loc in locations:
                if loc.difficulty.bool == True:
                    print("{:>48}: {:>8}".format(loc.Name, round(loc.difficulty.difficulty, 2)))
                    print("                                          smbool: {}".format(loc.difficulty))
                    print("                                            path: {}".format([ap.Name for ap in loc.path]))

    def collectMajor(self, loc, itemName=None):
        self.majorLocations.remove(loc)
        self.visitedLocations.append(loc)
        self.collectItem(loc, itemName)
        return loc

    def collectMinor(self, loc):
        self.minorLocations.remove(loc)
        self.visitedLocations.append(loc)
        self.collectItem(loc)
        return loc

    def collectItem(self, loc, item=None):
        if item == None:
            item = loc.itemName

        if self.vcr != None:
            self.vcr.addLocation(loc.Name, item)

        if self.firstLogFile is not None:
            if item not in self.collectedItems:
                self.firstLogFile.write("{};{};{};{}\n".format(item, loc.Name, loc.Area, loc.GraphArea))

        if item not in Conf.itemsForbidden:
            self.collectedItems.append(item)
            if self.checkDuplicateMajor == True:
                if item not in ['Nothing', 'NoEnergy', 'Missile', 'Super', 'PowerBomb', 'ETank', 'Reserve']:
                    if self.smbm.haveItem(item):
                        print("WARNING: {} has already been picked up".format(item))

            self.smbm.addItem(item)
        else:
            # update the name of the item
            item = "-{}-".format(item)
            loc.itemName = item
            self.collectedItems.append(item)
            # we still need the boss difficulty
            if not loc.isBoss():
                loc.difficulty = smboolFalse

        if self.log.getEffectiveLevel() == logging.DEBUG:
            print("---------------------------------------------------------------")
            print("collectItem: {:<16} at {:<48}".format(item, loc.Name))
            print("---------------------------------------------------------------")

        # last loc is used as root node for the graph.
        # when loading a plando we can load locations from non connected areas, so they don't have an access point.
        if loc.accessPoint is not None:
            self.lastAP = loc.accessPoint
            self.lastArea = loc.SolveArea

    def getLocIndex(self, locName):
        for (i, loc) in enumerate(self.visitedLocations):
            if loc.Name == locName:
                return i

    def removeItemAt(self, locNameWeb):
        locName = self.locNameWeb2Internal(locNameWeb)
        locIndex = self.getLocIndex(locName)
        if locIndex is None:
            self.errorMsg = "Location '{}' has not been visited".format(locName)
            return

        loc = self.visitedLocations.pop(locIndex)
        # removeItemAt is only used from the tracker, so all the locs are in majorLocations
        self.majorLocations.append(loc)

        # access point
        if len(self.visitedLocations) == 0:
            self.lastAP = self.startLocation
            self.lastArea = self.startArea
        else:
            self.lastAP = self.visitedLocations[-1].accessPoint
            self.lastArea = self.visitedLocations[-1].SolveArea

        # delete location params which are set when the location is available
        if loc.difficulty is not None:
            loc.difficulty = None
        if loc.distance is not None:
            loc.distance = None
        if loc.accessPoint is not None:
            loc.accessPoint = None
        if loc.path is not None:
            loc.path = None

        # item
        item = loc.itemName

        if self.mode in ['seedless', 'race', 'debug']:
            # in seedless remove the first nothing found as collectedItems is not ordered
            self.collectedItems.remove(item)
        else:
            self.collectedItems.pop(locIndex)

        # if multiple majors in plando mode, remove it from smbm only when it's the last occurence of it
        if self.smbm.isCountItem(item):
            self.smbm.removeItem(item)
        else:
            if item not in self.collectedItems:
                self.smbm.removeItem(item)

    def cancelLastItems(self, count):
        if self.vcr != None:
            self.vcr.addRollback(count)

        if self.interactive == False:
            self.nbAvailLocs = self.nbAvailLocs[:-count]

        for _ in range(count):
            if len(self.visitedLocations) == 0:
                return

            loc = self.visitedLocations.pop()
            if self.majorsSplit == 'Full':
                self.majorLocations.append(loc)
            else:
                if loc.isClass(self.majorsSplit) or loc.isBoss():
                    self.majorLocations.append(loc)
                else:
                    self.minorLocations.append(loc)

            # access point
            if len(self.visitedLocations) == 0:
                self.lastAP = self.startLocation
                self.lastArea = self.startArea
            else:
                self.lastAP = self.visitedLocations[-1].accessPoint
                if self.lastAP is None:
                    # default to location first access from access point
                    self.lastAP = list(self.visitedLocations[-1].AccessFrom.keys())[0]
                self.lastArea = self.visitedLocations[-1].SolveArea

            # delete location params which are set when the location is available
            if loc.difficulty is not None:
                loc.difficulty = None
            if loc.distance is not None:
                loc.distance = None
            if loc.accessPoint is not None:
                loc.accessPoint = None
            if loc.path is not None:
                loc.path = None

            # item
            item = loc.itemName
            if item != self.collectedItems[-1]:
                raise Exception("Item of last collected loc {}: {} is different from last collected item: {}".format(loc.Name, item, self.collectedItems[-1]))

            # in plando we have to remove the last added item,
            # else it could be used in computing the postAvailable of a location
            if self.mode in ['plando', 'seedless', 'race', 'debug']:
                loc.itemName = 'Nothing'

            self.collectedItems.pop()

            # if multiple majors in plando mode, remove it from smbm only when it's the last occurence of it
            if self.smbm.isCountItem(item):
                self.smbm.removeItem(item)
            else:
                if item not in self.collectedItems:
                    self.smbm.removeItem(item)

    def printLocs(self, locs, phase):
        if len(locs) > 0:
            print("{}:".format(phase))
            print('{:>48} {:>12} {:>8} {:>8} {:>34} {:>10}'.format("Location Name", "Difficulty", "Distance", "ComeBack", "SolveArea", "AreaWeight"))
            for loc in locs:
                print('{:>48} {:>12} {:>8} {:>8} {:>34} {:>10}'.
                      format(loc.Name, round(loc.difficulty[1], 2), round(loc.distance, 2),
                             loc.comeBack, loc.SolveArea, loc.areaWeight if loc.areaWeight is not None else -1))

    def getAvailableItemsList(self, locations, threshold):
        # locations without distance are not available
        locations = [loc for loc in locations if loc.distance is not None]

        if len(locations) == 0:
            return []

        # add nocomeback locations which has been selected by the comeback step (areaWeight == 1)
        around = [loc for loc in locations if( (loc.areaWeight is not None and loc.areaWeight == 1)
                                               or ((loc.SolveArea == self.lastArea or loc.distance < 3)
                                                   and loc.difficulty.difficulty <= threshold
                                                   and not Bosses.areaBossDead(self.smbm, self.lastArea)
                                                   and loc.comeBack is not None and loc.comeBack == True) )]
        outside = [loc for loc in locations if not loc in around]

        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.printLocs(around, "around1")
            self.printLocs(outside, "outside1")

        around.sort(key=lambda loc: (
            # locs in the same area
            0 if loc.SolveArea == self.lastArea
            else 1,
            # nearest locs
            loc.distance,
            # beating a boss
            0 if loc.isBoss()
            else 1,
            # easiest first
            loc.difficulty.difficulty
            )
        )

        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.printLocs(around, "around2")

        # we want to sort the outside locations by putting the ones in the same area first,
        # then we sort the remaining areas starting whith boss dead status.
        # we also want to sort by range of difficulty and not only with the difficulty threshold.
        ranged = {
            "areaWeight": [],
            "easy": [],
            "medium": [],
            "hard": [],
            "harder": [],
            "hardcore": [],
            "mania": [],
            "noComeBack": []
        }
        for loc in outside:
            if loc.areaWeight is not None:
                ranged["areaWeight"].append(loc)
            elif loc.comeBack is None or loc.comeBack == False:
                ranged["noComeBack"].append(loc)
            else:
                difficulty = loc.difficulty.difficulty
                if difficulty < medium:
                    ranged["easy"].append(loc)
                elif difficulty < hard:
                    ranged["medium"].append(loc)
                elif difficulty < harder:
                    ranged["hard"].append(loc)
                elif difficulty < hardcore:
                    ranged["harder"].append(loc)
                elif difficulty < mania:
                    ranged["hardcore"].append(loc)
                else:
                    ranged["mania"].append(loc)

        for key in ranged:
            ranged[key].sort(key=lambda loc: (
                # first locs in the same area
                0 if loc.SolveArea == self.lastArea else 1,
                # first nearest locs
                loc.distance,
                # beating a boss
                loc.difficulty.difficulty if (not Bosses.areaBossDead(self.smbm, loc.Area)
                                              and loc.isBoss())
                else 100000,
                # areas with boss still alive
                loc.difficulty.difficulty if (not Bosses.areaBossDead(self.smbm, loc.Area))
                else 100000,
                loc.difficulty.difficulty))


        if self.log.getEffectiveLevel() == logging.DEBUG:
            for key in ["areaWeight", "easy", "medium", "hard", "harder", "hardcore", "mania", "noComeBack"]:
                self.printLocs(ranged[key], "outside2:{}".format(key))

        outside = []
        for key in ["areaWeight", "easy", "medium", "hard", "harder", "hardcore", "mania", "noComeBack"]:
            outside += ranged[key]

        return around + outside

    def nextDecision(self, majorsAvailable, minorsAvailable, hasEnoughMinors, diffThreshold):
        # first take major items of acceptable difficulty in the current area
        if (len(majorsAvailable) > 0
            and majorsAvailable[0].SolveArea == self.lastArea
            and majorsAvailable[0].difficulty.difficulty <= diffThreshold
            and majorsAvailable[0].comeBack == True):
            return self.collectMajor(majorsAvailable.pop(0))
        # next item decision
        elif len(minorsAvailable) == 0 and len(majorsAvailable) > 0:
            self.log.debug('MAJOR')
            return self.collectMajor(majorsAvailable.pop(0))
        elif len(majorsAvailable) == 0 and len(minorsAvailable) > 0:
            # we don't check for hasEnoughMinors here, because we would be stuck, so pickup
            # what we can and hope it gets better
            self.log.debug('MINOR')
            return self.collectMinor(minorsAvailable.pop(0))
        elif len(majorsAvailable) > 0 and len(minorsAvailable) > 0:
            self.log.debug('BOTH|M={}, m={}'.format(majorsAvailable[0].Name, minorsAvailable[0].Name))
            # if both are available, decide based on area, difficulty and comeBack
            nextMajDifficulty = majorsAvailable[0].difficulty.difficulty
            nextMinDifficulty = minorsAvailable[0].difficulty.difficulty
            nextMajArea = majorsAvailable[0].SolveArea
            nextMinArea = minorsAvailable[0].SolveArea
            nextMajComeBack = majorsAvailable[0].comeBack
            nextMinComeBack = minorsAvailable[0].comeBack
            nextMajDistance = majorsAvailable[0].distance
            nextMinDistance = minorsAvailable[0].distance
            maxAreaWeigth = 10000
            nextMajAreaWeight = majorsAvailable[0].areaWeight if majorsAvailable[0].areaWeight is not None else maxAreaWeigth
            nextMinAreaWeight = minorsAvailable[0].areaWeight if minorsAvailable[0] .areaWeight is not None else maxAreaWeigth

            if self.log.getEffectiveLevel() == logging.DEBUG:
                print("     : {:>4} {:>32} {:>4} {:>4} {:>6}".format("diff", "area", "back", "dist", "weight"))
                print("major: {:>4} {:>32} {:>4} {:>4} {:>6}".format(round(nextMajDifficulty, 2), nextMajArea, nextMajComeBack, round(nextMajDistance, 2), nextMajAreaWeight))
                print("minor: {:>4} {:>32} {:>4} {:>4} {:>6}".format(round(nextMinDifficulty, 2), nextMinArea, nextMinComeBack, round(nextMinDistance, 2), nextMinAreaWeight))

            if hasEnoughMinors == True and self.haveAllMinorTypes() == True and self.smbm.haveItem('Charge') and nextMajAreaWeight != maxAreaWeigth:
                # we have charge, no longer need minors
                self.log.debug("we have charge, no longer need minors, take major")
                return self.collectMajor(majorsAvailable.pop(0))
            else:
                # respect areaweight first
                if nextMajAreaWeight != nextMinAreaWeight:
                    self.log.debug("maj/min != area weight")
                    if nextMajAreaWeight < nextMinAreaWeight:
                        return self.collectMajor(majorsAvailable.pop(0))
                    else:
                        return self.collectMinor(minorsAvailable.pop(0))
                # then take item from loc where you can come back
                elif nextMajComeBack != nextMinComeBack:
                    self.log.debug("maj/min != combeback")
                    if nextMajComeBack == True:
                        return self.collectMajor(majorsAvailable.pop(0))
                    else:
                        return self.collectMinor(minorsAvailable.pop(0))
                # difficulty over area (this is a difficulty estimator, not a speedrunning simulator)
                elif nextMinDifficulty <= diffThreshold and nextMajDifficulty <= diffThreshold:
                    # take the closer one
                    if nextMajDistance != nextMinDistance:
                        self.log.debug("!= distance and <= diffThreshold")
                        if nextMajDistance < nextMinDistance:
                            return self.collectMajor(majorsAvailable.pop(0))
                        else:
                            return self.collectMinor(minorsAvailable.pop(0))
                    # take the easier
                    elif nextMinDifficulty < nextMajDifficulty:
                        self.log.debug("min easier and not enough minors")
                        return self.collectMinor(minorsAvailable.pop(0))
                    elif nextMajDifficulty < nextMinDifficulty:
                        self.log.debug("maj easier")
                        return self.collectMajor(majorsAvailable.pop(0))
                    # same difficulty and distance for minor and major, take major first
                    else:
                        return self.collectMajor(majorsAvailable.pop(0))
                # if not all the minors type are collected, start with minors
                elif nextMinDifficulty <= diffThreshold and not self.haveAllMinorTypes():
                    self.log.debug("not all minors types")
                    return self.collectMinor(minorsAvailable.pop(0))
                elif nextMinArea == self.lastArea and nextMinDifficulty <= diffThreshold:
                    self.log.debug("not enough minors")
                    return self.collectMinor(minorsAvailable.pop(0))
                elif nextMinDifficulty > diffThreshold and nextMajDifficulty > diffThreshold:
                    # take the easier
                    if nextMinDifficulty < nextMajDifficulty:
                        self.log.debug("min easier and not enough minors")
                        return self.collectMinor(minorsAvailable.pop(0))
                    elif nextMajDifficulty < nextMinDifficulty:
                        self.log.debug("maj easier")
                        return self.collectMajor(majorsAvailable.pop(0))
                    # take the closer one
                    elif nextMajDistance != nextMinDistance:
                        self.log.debug("!= distance and > diffThreshold")
                        if nextMajDistance < nextMinDistance:
                            return self.collectMajor(majorsAvailable.pop(0))
                        else:
                            return self.collectMinor(minorsAvailable.pop(0))
                    # same difficulty and distance for minor and major, take major first
                    else:
                        return self.collectMajor(majorsAvailable.pop(0))
                else:
                    if nextMinDifficulty < nextMajDifficulty:
                        self.log.debug("min easier and not enough minors")
                        return self.collectMinor(minorsAvailable.pop(0))
                    else:
                        self.log.debug("maj easier")
                        return self.collectMajor(majorsAvailable.pop(0))

        raise Exception("Can't take a decision")

    def checkMB(self, mbLoc, justCheck=False):
        # add mother brain loc and check if it's accessible
        self.majorLocations.append(mbLoc)
        self.computeLocationsDifficulty(self.majorLocations)
        if justCheck:
            self.majorLocations.remove(mbLoc)
            return mbLoc.difficulty == True
        if mbLoc.difficulty == True:
            self.log.debug("MB loc accessible")
            self.collectMajor(mbLoc)
            self.motherBrainKilled = True
        else:
            self.log.debug("MB loc not accessible")
            self.majorLocations.remove(mbLoc)
            self.motherBrainKilled = False
        return self.motherBrainKilled

    def computeDifficulty(self):
        # loop on the available locations depending on the collected items.
        # before getting a new item, loop on all of them and get their difficulty,
        # the next collected item is the one with the smallest difficulty,
        # if equality between major and minor, take major first.

        # remove mother brain location (there items pickup conditions on top of going to mother brain location)
        mbLoc = self.getLoc('Mother Brain')
        self.locations.remove(mbLoc)

        if self.majorsSplit == 'Major':
            self.majorLocations = [loc for loc in self.locations if loc.isMajor() or loc.isBoss()]
            self.minorLocations = [loc for loc in self.locations if loc.isMinor()]
        elif self.majorsSplit == 'Chozo':
            self.majorLocations = [loc for loc in self.locations if loc.isChozo() or loc.isBoss()]
            self.minorLocations = [loc for loc in self.locations if not loc.isChozo() and not loc.isBoss()]
        elif self.majorsSplit == 'Scavenger':
            self.majorLocations = [loc for loc in self.locations if loc.isScavenger() or loc.isBoss()]
            self.minorLocations = [loc for loc in self.locations if not loc.isScavenger() and not loc.isBoss()]
        else:
            # Full
            self.majorLocations = self.locations[:] # copy
            self.minorLocations = self.majorLocations

        self.visitedLocations = []
        self.collectedItems = []

        self.log.debug("{}: available major: {}, available minor: {}, visited: {}".format(Conf.itemsPickup, len(self.majorLocations), len(self.minorLocations), len(self.visitedLocations)))

        isEndPossible = False
        endDifficulty = mania
        diffThreshold = self.getDiffThreshold()
        self.motherBrainKilled = False
        self.motherBrainCouldBeKilled = False
        while True:
            # actual while condition
            hasEnoughMinors = self.pickup.enoughMinors(self.smbm, self.minorLocations)
            hasEnoughMajors = self.pickup.enoughMajors(self.smbm, self.majorLocations)
            hasEnoughItems = hasEnoughMajors and hasEnoughMinors
            canEndGame = self.canEndGame()
            (isEndPossible, endDifficulty) = (canEndGame.bool, canEndGame.difficulty)
            if isEndPossible and hasEnoughItems and self.scavengerHuntComplete():
                if endDifficulty <= diffThreshold:
                    if self.checkMB(mbLoc):
                        self.log.debug("checkMB: all end game checks are ok, END")
                        break
                    else:
                        self.log.debug("checkMB: canEnd but MB loc not accessible")
                else:
                    if not self.motherBrainCouldBeKilled:
                        self.motherBrainCouldBeKilled = self.checkMB(mbLoc, justCheck=True)
                    self.log.debug("checkMB: end checks ok except MB difficulty, MB could be killed: {}".format(self.motherBrainCouldBeKilled))

            # check time limit
            if self.runtimeLimit_s > 0:
                if time.process_time() - self.startTime > self.runtimeLimit_s:
                    self.log.debug("time limit exceeded ({})".format(self.runtimeLimit_s))
                    return (-1, False)

            self.log.debug("Current AP/Area: {}/{}".format(self.lastAP, self.lastArea))

            # compute the difficulty of all the locations
            self.computeLocationsDifficulty(self.majorLocations)
            if self.majorsSplit != 'Full':
                self.computeLocationsDifficulty(self.minorLocations, phase="minor")

            # keep only the available locations
            majorsAvailable = [loc for loc in self.majorLocations if loc.difficulty is not None and loc.difficulty.bool == True]
            minorsAvailable = [loc for loc in self.minorLocations if loc.difficulty is not None and loc.difficulty.bool == True]

            self.nbAvailLocs.append(len(self.getAllLocs(majorsAvailable, minorsAvailable)))

            # remove next scavenger locs before checking if we're stuck
            if self.majorsSplit == 'Scavenger':
                majorsAvailable = self.filterScavengerLocs(majorsAvailable)

            # check if we're stuck
            if len(majorsAvailable) == 0 and len(minorsAvailable) == 0:
                if not isEndPossible:
                    self.log.debug("STUCK MAJORS and MINORS")
                    if self.comeBack.rewind(len(self.collectedItems)) == True:
                        continue
                    else:
                        # we're really stucked
                        self.log.debug("STUCK CAN'T REWIND")
                        break
                else:
                    self.log.debug("HARD END 2")
                    if self.checkMB(mbLoc):
                        self.log.debug("all end game checks are ok, END")
                        break
                    else:
                        self.log.debug("We're stucked somewhere and can't reach mother brain")
                        # check if we were able to access MB and kill it.
                        # we do it before rollbacks to avoid endless rollbacks.
                        if self.motherBrainCouldBeKilled:
                            self.log.debug("we're stucked but we could have killed MB before")
                            self.motherBrainKilled = True
                            break
                        else:
                            # we're really stucked, try to rollback
                            if self.comeBack.rewind(len(self.collectedItems)) == True:
                                continue
                            else:
                                self.log.debug("We could end but we're STUCK CAN'T REWIND")
                                return (-1, False)

            # handle no comeback locations
            rewindRequired = self.comeBack.handleNoComeBack(self.getAllLocs(majorsAvailable, minorsAvailable),
                                                            len(self.collectedItems))
            if rewindRequired == True:
                if self.comeBack.rewind(len(self.collectedItems)) == True:
                    continue
                else:
                    # we're really stucked
                    self.log.debug("STUCK CAN'T REWIND")
                    break

            # sort them on difficulty and proximity
            self.log.debug("getAvailableItemsList majors")
            majorsAvailable = self.getAvailableItemsList(majorsAvailable, diffThreshold)
            if self.majorsSplit == 'Full':
                minorsAvailable = majorsAvailable
            else:
                self.log.debug("getAvailableItemsList minors")
                minorsAvailable = self.getAvailableItemsList(minorsAvailable, diffThreshold)

            # choose one to pick up
            self.nextDecision(majorsAvailable, minorsAvailable, hasEnoughMinors, diffThreshold)

            self.comeBack.cleanNoComeBack(self.getAllLocs(self.majorLocations, self.minorLocations))

        # compute difficulty value
        (difficulty, itemsOk) = self.computeDifficultyValue()

        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("difficulty={}".format(difficulty))
            self.log.debug("itemsOk={}".format(itemsOk))
            self.log.debug("{}: remaining major: {}, remaining minor: {}, visited: {}".format(Conf.itemsPickup, len(self.majorLocations), len(self.minorLocations), len(self.visitedLocations)))

            self.log.debug("remaining majors:")
            for loc in self.majorLocations:
                self.log.debug("{} ({})".format(loc.Name, loc.itemName))

            self.log.debug("bosses: {}".format([(boss, Bosses.bossDead(self.smbm, boss)) for boss in Bosses.Golden4()]))

        return (difficulty, itemsOk)

    def haveAllMinorTypes(self):
        # the first minor of each type can be seen as a major, so check for them first before going to far in zebes
        hasPB = 'PowerBomb' in self.collectedItems
        hasSuper = 'Super' in self.collectedItems
        hasMissile = 'Missile' in self.collectedItems
        return (hasPB and hasSuper and hasMissile)

    def canEndGame(self):
        # to finish the game you must:
        # - beat golden 4
        # - defeat metroids
        # - destroy/skip the zebetites
        # - beat Mother Brain
        return self.smbm.wand(Bosses.allBossesDead(self.smbm), self.smbm.enoughStuffTourian())

    def getAllLocs(self, majorsAvailable, minorsAvailable):
        if self.majorsSplit == 'Full':
            return majorsAvailable
        else:
            return majorsAvailable+minorsAvailable

    def computeDifficultyValue(self):
        if not self.canEndGame() or not self.motherBrainKilled:
            # we have aborted
            return (-1, False)
        else:
            # return the maximum difficulty
            difficultyMax = 0
            for loc in self.visitedLocations:
                difficultyMax = max(difficultyMax, loc.difficulty.difficulty)
            difficulty = difficultyMax

            # check if we have taken all the requested items
            if (self.pickup.enoughMinors(self.smbm, self.minorLocations)
                and self.pickup.enoughMajors(self.smbm, self.majorLocations)):
                return (difficulty, True)
            else:
                # can finish but can't take all the requested items
                return (difficulty, False)

    def filterScavengerLocs(self, majorsAvailable):
        # check where we are in the scavenger hunt
        huntInProgress = False
        for index, loc in enumerate(self.scavengerOrder):
            if loc not in self.visitedLocations:
                huntInProgress = True
                break

        if huntInProgress and index < len(self.scavengerOrder)-1:
            self.log.debug("Scavenger hunt in progress, {}/{}".format(index, len(self.scavengerOrder)-1))
            # remove all next locs in the hunt
            nextHuntLocs = self.scavengerOrder[index+1:]
            for loc in nextHuntLocs:
                self.log.debug("Scavenger hunt, try to remove loc {}".format(loc.Name))
                try:
                    majorsAvailable.remove(loc)
                except:
                    pass

        return majorsAvailable

    def scavengerHuntComplete(self):
        if self.majorsSplit != 'Scavenger':
            return True
        else:
            # check that last loc from the scavenger hunt list has been visited
            lastLoc = self.scavengerOrder[-1]
            return lastLoc in self.visitedLocations
