import json, os, time

from solver.commonSolver import CommonSolver
from logic.helpers import Pickup
from utils.utils import PresetLoader
from solver.conf import Conf
from solver.out import Out
from solver.comeback import ComeBack
from utils.parameters import easy, medium, hard, harder, hardcore, mania, infinity
from utils.parameters import Knows, isKnows, Settings
from logic.logic import Logic
import utils.log

class StandardSolver(CommonSolver):
    # given a rom and parameters returns the estimated difficulty

    def __init__(self, rom, presetFileName, difficultyTarget, pickupStrategy, itemsForbidden=[], type='console',
                 firstItemsLog=None, extStatsFilename=None, extStatsStep=None, displayGeneratedPath=False,
                 outputFileName=None, magic=None, checkDuplicateMajor=False, vcr=False, runtimeLimit_s=0):
        self.interactive = False
        self.checkDuplicateMajor = checkDuplicateMajor
        if vcr == True:
            from utils.vcr import VCR
            self.vcr = VCR(rom, 'solver')
        else:
            self.vcr = None
        # for compatibility with some common methods of the interactive solver
        self.mode = 'standard'

        self.log = utils.log.get('Solver')

        self.setConf(difficultyTarget, pickupStrategy, itemsForbidden, displayGeneratedPath)

        self.firstLogFile = None
        if firstItemsLog is not None:
            self.firstLogFile = open(firstItemsLog, 'w')
            self.firstLogFile.write('Item;Location;Area\n')

        self.extStatsFilename = extStatsFilename
        self.extStatsStep = extStatsStep

        # can be called from command line (console) or from web site (web)
        self.type = type
        self.output = Out.factory(self.type, self)
        self.outputFileName = outputFileName

        self.loadRom(rom, magic=magic)

        self.presetFileName = presetFileName
        self.loadPreset(self.presetFileName)

        self.pickup = Pickup(Conf.itemsPickup)

        self.comeBack = ComeBack(self)

        self.runtimeLimit_s = runtimeLimit_s
        self.startTime = time.process_time()

    def setConf(self, difficultyTarget, pickupStrategy, itemsForbidden, displayGeneratedPath):
        Conf.difficultyTarget = difficultyTarget
        Conf.itemsPickup = pickupStrategy
        Conf.displayGeneratedPath = displayGeneratedPath
        Conf.itemsForbidden = itemsForbidden

    def solveRom(self):
        self.lastAP = self.startLocation
        self.lastArea = self.startArea

        (self.difficulty, self.itemsOk) = self.computeDifficulty()
        if self.firstLogFile is not None:
            self.firstLogFile.close()

        (self.knowsUsed, self.knowsKnown, knowsUsedList) = self.getKnowsUsed()

        if self.vcr != None:
            self.vcr.dump()

        if self.extStatsFilename != None:
            self.computeExtStats()

            firstMinor = {'Missile': False, 'Super': False, 'PowerBomb': False}
            locsItems = {}
            for loc in self.visitedLocations:
                if loc.itemName in firstMinor and firstMinor[loc.itemName] == False:
                    locsItems[loc.Name] = loc.itemName
                    firstMinor[loc.itemName] = True

            import utils.db as db
            with open(self.extStatsFilename, 'a') as extStatsFile:
                db.DB.dumpExtStatsSolver(self.difficulty, knowsUsedList, self.solverStats, locsItems, self.extStatsStep, extStatsFile)

        self.output.out()

        return self.difficulty

    def computeExtStats(self):
        # avgLocs: avg number of available locs, the higher the value the more open is a seed
        # open[1-4]4: how many location you have to visit to open 1/4, 1/2, 3/4, all locations.
        #             gives intel about prog item repartition.
        self.solverStats = {}
        self.solverStats['avgLocs'] = int(sum(self.nbAvailLocs)/len(self.nbAvailLocs))

        derivative = []
        for i in range(len(self.nbAvailLocs)-1):
            d = self.nbAvailLocs[i+1] - self.nbAvailLocs[i]
            derivative.append(d)

        sumD = sum([d for d in derivative if d != -1])
        (sum14, sum24, sum34, sum44) = (sumD/4, sumD/2, sumD*3/4, sumD)
        (open14, open24, open34, open44) = (-1, -1, -1, -1)

        sumD = 0
        for (i, d) in enumerate(derivative, 1):
            if d == -1:
                continue
            sumD += d
            if sumD >= sum14 and open14 == -1:
                open14 = i
                continue
            if sumD >= sum24 and open24 == -1:
                open24 = i
                continue
            if sumD >= sum34 and open34 == -1:
                open34 = i
                continue
            if sumD >= sum44 and open44 == -1:
                open44 = i
                break

        self.solverStats['open14'] = open14 if open14 != -1 else 0
        self.solverStats['open24'] = open24 if open24 != -1 else 0
        self.solverStats['open34'] = open34 if open34 != -1 else 0
        self.solverStats['open44'] = open44 if open44 != -1 else 0

    def getRemainMajors(self):
        return [loc for loc in self.majorLocations if loc.difficulty.bool == False and loc.itemName not in ['Nothing', 'NoEnergy']]

    def getRemainMinors(self):
        if self.majorsSplit == 'Full':
            return None
        else:
            return [loc for loc in self.minorLocations if loc.difficulty.bool == False and loc.itemName not in ['Nothing', 'NoEnergy']]

    def getSkippedMajors(self):
        return [loc for loc in self.majorLocations if loc.difficulty.bool == True and loc.itemName not in ['Nothing', 'NoEnergy']]

    def getUnavailMajors(self):
        return [loc for loc in self.majorLocations if loc.difficulty.bool == False and loc.itemName not in ['Nothing', 'NoEnergy']]


    def getDiffThreshold(self):
        target = Conf.difficultyTarget
        threshold = target
        epsilon = 0.001
        if target <= easy:
            threshold = medium - epsilon
        elif target <= medium:
            threshold = hard - epsilon
        elif target <= hard:
            threshold = harder - epsilon
        elif target <= harder:
            threshold = hardcore - epsilon
        elif target <= hardcore:
            threshold = mania - epsilon

        return threshold

    def getKnowsUsed(self):
        knowsUsed = []
        for loc in self.visitedLocations:
            knowsUsed += loc.difficulty.knows

        # get unique knows
        knowsUsed = list(set(knowsUsed))
        knowsUsedCount = len(knowsUsed)

        # get total of known knows
        knowsKnownCount = len([knows for  knows in Knows.__dict__ if isKnows(knows) and getattr(Knows, knows).bool == True])
        knowsKnownCount += len([hellRun for hellRun in Settings.hellRuns if Settings.hellRuns[hellRun] is not None])

        return (knowsUsedCount, knowsKnownCount, knowsUsed)

    def tryRemainingLocs(self):
        # use preset which knows every techniques to test the remaining locs to
        # find which technique could allow to continue the seed
        locations = self.majorLocations if self.majorsSplit == 'Full' else self.majorLocations + self.minorLocations

        # instanciate a new smbool manager to reset the cache
        from logic.smboolmanager import SMBoolManagerPlando as SMBoolManager
        self.smbm = SMBoolManager()
        presetFileName = os.path.expanduser('~/RandomMetroidSolver/standard_presets/solution.json')
        presetLoader = PresetLoader.factory(presetFileName)
        presetLoader.load()
        self.smbm.createKnowsFunctions()

        self.areaGraph.getAvailableLocations(locations, self.smbm, infinity, self.lastAP)

        return [loc for loc in locations if loc.difficulty.bool == True]
