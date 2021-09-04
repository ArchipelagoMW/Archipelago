import json

from logic.smbool import SMBool
from rom.rom_patches import RomPatches
from utils.utils import removeChars, fixEnergy
from utils.parameters import diff4solver, Knows
from utils.doorsmanager import DoorsManager
from rom.rom_patches import RomPatches

class SolverState(object):
    def __init__(self, debug=False):
        self.debug = debug

    def fromSolver(self, solver):
        self.state = {}
        # string
        self.state["majorsSplit"] = solver.majorsSplit
        # string
        self.state["masterMajorsSplit"] = solver.masterMajorsSplit
        # bool
        self.state["areaRando"] = solver.areaRando
        # bool
        self.state["bossRando"] = solver.bossRando
        # bool
        self.state["escapeRando"] = solver.escapeRando
        # string "03:00"
        self.state["escapeTimer"] = solver.escapeTimer
        # list of active patches
        self.state["patches"] = RomPatches.ActivePatches
        # start ap
        self.state["startLocation"] = solver.startLocation
        # start area
        self.state["startArea"] = solver.startArea
        # dict {locName: {itemName: "xxx", "accessPoint": "xxx"}, ...}
        self.state["locsData"] = self.getLocsData(solver.locations)
        # list [(ap1, ap2), (ap3, ap4), ...]
        self.state["areaTransitions"] = solver.areaTransitions
        # list [(ap1, ap2), (ap3, ap4), ...]
        self.state["bossTransitions"] = solver.bossTransitions
        # list [(ap1, ap2)]
        self.state["escapeTransition"] = solver.escapeTransition
        # list [(ap1, ap2), ...]
        self.state["curGraphTransitions"] = solver.curGraphTransitions
        # bool
        self.state["hasMixedTransitions"] = solver.hasMixedTransitions
        # preset file name
        self.state["presetFileName"] = solver.presetFileName
        ## items collected / locs visited / bosses killed
        # list [item1, item2, ...]
        self.state["collectedItems"] = solver.collectedItems
        # dict {locName: {index: 0, difficulty: (bool, diff, ...), ...} with index being the position of the loc in visitedLocations
        self.state["visitedLocations"] = self.getVisitedLocations(solver.visitedLocations)
        # dict {locName: (bool, diff, [know1, ...], [item1, ...]), ...}
        self.state["availableLocations"] = self.getAvailableLocations(solver.majorLocations)
        # string of last access point
        self.state["lastAP"] = solver.lastAP
        # dict {locNameWeb: {infos}, ...}
        self.state["availableLocationsWeb"] = self.getAvailableLocationsWeb(solver.majorLocations)
        # dict {locNameWeb: {infos}, ...}
        self.state["visitedLocationsWeb"] = self.getAvailableLocationsWeb(solver.visitedLocations)
        # dict {locNameWeb: {infos}, ...}
        self.state["remainLocationsWeb"] = self.getRemainLocationsWeb(solver.majorLocations)
        # string: standard/seedless/plando/race/debug
        self.state["mode"] = solver.mode
        # string:
        self.state["seed"] = solver.seed
        # dict {point: point, ...} / array of startPoints
        (self.state["linesWeb"], self.state["linesSeqWeb"]) = self.getLinesWeb(solver.curGraphTransitions)
        # bool
        self.state["allTransitions"] = len(solver.curGraphTransitions) == len(solver.areaTransitions) + len(solver.bossTransitions) + len(solver.escapeTransition)
        self.state["errorMsg"] = solver.errorMsg
        if len(solver.visitedLocations) > 0:
            self.state["last"] = {"loc": solver.visitedLocations[-1].Name,
                                  "item": solver.visitedLocations[-1].itemName}
        else:
            self.state["last"] = ""
        # store the inner graph transitions to display in vcr
        if self.debug == True:
            self.state["innerTransitions"] = self.getInnerTransitions(solver.areaGraph.availAccessPoints, solver.curGraphTransitions)
        else:
            self.state["innerTransitions"] = []
        # has nothing: bool
        self.state["hasNothing"] = solver.hasNothing
        # doors colors: dict {name: (color, facing, hidden)}
        self.state["doors"] = DoorsManager.serialize()
        # doorsRando: bool
        self.state["doorsRando"] = solver.doorsRando
        # allDoorsRevealed: bool
        self.state["allDoorsRevealed"] = DoorsManager.allDoorsRevealed()
        # roomsVisibility: array of string ['landingSiteSvg', 'MissileCrateriamoatSvg']
        self.state["roomsVisibility"] = self.getRoomsVisibility(solver, solver.areaGraph, solver.smbm)

    def toSolver(self, solver):
        solver.majorsSplit = self.state["majorsSplit"]
        solver.masterMajorsSplit = self.state["masterMajorsSplit"]
        solver.areaRando = self.state["areaRando"]
        solver.bossRando = self.state["bossRando"]
        solver.escapeRando = self.state["escapeRando"]
        solver.escapeTimer = self.state["escapeTimer"]
        RomPatches.ActivePatches = self.state["patches"]
        solver.startLocation = self.state["startLocation"]
        solver.startArea = self.state["startArea"]
        self.setLocsData(solver.locations)
        solver.areaTransitions = self.state["areaTransitions"]
        solver.bossTransitions = self.state["bossTransitions"]
        solver.escapeTransition = self.state["escapeTransition"]
        solver.curGraphTransitions = self.state["curGraphTransitions"]
        solver.hasMixedTransitions = self.state["hasMixedTransitions"]
        # preset
        solver.presetFileName = self.state["presetFileName"]
        # items collected / locs visited / bosses killed
        solver.collectedItems = self.state["collectedItems"]
        (solver.visitedLocations, solver.majorLocations) = self.setLocations(self.state["visitedLocations"],
                                                                             self.state["availableLocations"],
                                                                             solver.locations)
        solver.lastAP = self.state["lastAP"]
        solver.mode = self.state["mode"]
        solver.seed = self.state["seed"]
        solver.hasNothing = self.state["hasNothing"]
        DoorsManager.unserialize(self.state["doors"])
        solver.doorsRando = self.state["doorsRando"]

    def getRoomsVisibility(self, solver, areaGraph, sm):
        # add graph access points
        roomsVisibility = set([self.transition2isolver(ap.Name)+'Svg' for ap in solver.areaGraph.availAccessPoints])
        # add available locations
        roomsVisibility.update([loc+'Svg' for loc, data in self.state["availableLocationsWeb"].items() if data["difficulty"] != "break"])
        # add visited locations
        roomsVisibility.update([loc+'Svg' for loc, data in self.state["visitedLocationsWeb"].items() if 'accessPoint' in data and data['accessPoint']+'Svg' in roomsVisibility])
        # add special rooms that have conditions to traverse them but no item in them,
        # so we need to know if they are visible or not
        if 'crocomireRoomTopSvg' in roomsVisibility and sm.enoughStuffCroc():
            roomsVisibility.add('CrocomireSvg')
        if 'greenBrinstarElevatorSvg' in roomsVisibility and sm.traverse('MainShaftBottomRight'):
            roomsVisibility.add('DachoraRoomLeftSvg')
        if 'bigPinkSvg' in roomsVisibility and sm.canPassDachoraRoom():
            roomsVisibility.add('DachoraRoomCenterSvg')
        if ('redBrinstarElevatorSvg' in roomsVisibility and sm.wor(RomPatches.has(RomPatches.HellwayBlueDoor), sm.traverse('RedTowerElevatorLeft'))) or ('redTowerTopLeftSvg' in roomsVisibility and sm.canClimbRedTower()):
            roomsVisibility.add('HellwaySvg')
        if 'businessCenterSvg' in roomsVisibility and sm.haveItem('SpeedBooster'):
            roomsVisibility.add('FrogSpeedwayCenterSvg')
        if 'crabShaftLeftSvg' in roomsVisibility or 'redFishRoomLeftSvg' in roomsVisibility or ('mainStreetBottomSvg' in roomsVisibility and sm.canDoOuterMaridia()):
            roomsVisibility.add('westMaridiaSvg')
        if 'mainStreetBottomSvg' in roomsVisibility and sm.canTraverseCrabTunnelLeftToRight():
            roomsVisibility.add('CrabTunnelSvg')
        if 'SpaceJumpSvg' in roomsVisibility and ('colosseumTopRightSvg' in roomsVisibility or 'leCoudeRightSvg' in roomsVisibility):
            roomsVisibility.add('CacatacAlleySvg')

        return list(roomsVisibility)

    def getInnerTransitions(self, availAccessPoints, curGraphTransitions):
        innerTransitions = []
        for (apDst, dataSrc) in availAccessPoints.items():
            if dataSrc['from'] is None:
                continue
            src = dataSrc['from'].Name
            dst = apDst.Name
            if [src, dst] in curGraphTransitions or [dst, src] in curGraphTransitions:
                continue
            src = self.transition2isolver(src)
            dst = self.transition2isolver(dst)
            innerTransitions.append([src, dst, diff4solver(dataSrc['difficulty'].difficulty)])
        return innerTransitions

    def getLocsData(self, locations):
        ret = {}
        for loc in locations:
            ret[loc.Name] = {"itemName": loc.itemName}
            if loc.accessPoint != None:
                ret[loc.Name]["accessPoint"] = loc.accessPoint
        return ret

    def setLocsData(self, locations):
        for loc in locations:
            loc.itemName = self.state["locsData"][loc.Name]["itemName"]
            if "accessPoint" in self.state["locsData"][loc.Name]:
                loc.accessPoint = self.state["locsData"][loc.Name]["accessPoint"]

    def getVisitedLocations(self, visitedLocations):
        # need to keep the order (for cancelation)
        ret = {}
        i = 0
        for loc in visitedLocations:
            diff = loc.difficulty
            ret[loc.Name] = {"index": i,
                                "difficulty": (diff.bool, diff.difficulty, diff.knows, diff.items),
                                "Visibility": loc.Visibility}
            i += 1
        return ret

    def setLocations(self, visitedLocations, availableLocations, locations):
        retVis = []
        retMaj = []
        for loc in locations:
            if loc.Name in visitedLocations:
                # visitedLocations contains an index
                diff = visitedLocations[loc.Name]["difficulty"]
                loc.difficulty = SMBool(diff[0], diff[1], diff[2], diff[3])
                if "Visibility" in visitedLocations[loc.Name]:
                    loc.Visibility = visitedLocations[loc.Name]["Visibility"]
                retVis.append((visitedLocations[loc.Name]["index"], loc))
            else:
                if loc.Name in availableLocations:
                    diff = availableLocations[loc.Name]
                    loc.difficulty = SMBool(diff[0], diff[1], diff[2], diff[3])
                retMaj.append(loc)
        retVis.sort(key=lambda x: x[0])
        return ([loc for (i, loc) in retVis], retMaj)

    def name4isolver(self, locName):
        # remove space and special characters
        # sed -e 's+ ++g' -e 's+,++g' -e 's+(++g' -e 's+)++g' -e 's+-++g'
        return removeChars(locName, " ,()-")

    def knows2isolver(self, knows):
        result = []
        for know in knows:
            if know in Knows.desc:
                result.append(Knows.desc[know]['display'])
            else:
                result.append(know)
        return list(set(result))

    def transition2isolver(self, transition):
        transition = str(transition)
        return transition[0].lower() + removeChars(transition[1:], " ,()-")

    def getAvailableLocationsWeb(self, locations):
        ret = {}
        for loc in locations:
            if loc.difficulty is not None and loc.difficulty.bool == True:
                diff = loc.difficulty
                locName = self.name4isolver(loc.Name)
                ret[locName] = {"difficulty": diff4solver(diff.difficulty),
                                "knows": self.knows2isolver(diff.knows),
                                "items": fixEnergy(list(set(diff.items))),
                                "item": loc.itemName,
                                "name": loc.Name,
                                "canHidden": loc.CanHidden,
                                "visibility": loc.Visibility}

#                if loc.locDifficulty is not None:
#                    lDiff = loc.locDifficulty
#                    ret[locName]["locDifficulty"] = [diff4solver(lDiff.difficulty), self.knows2isolver(lDiff.knows), list(set(lDiff.items))]
#                if loc.pathDifficulty is not None:
#                    pDiff = loc.pathDifficulty
#                    ret[locName]["pathDifficulty"] = [diff4solver(pDiff.difficulty), self.knows2isolver(pDiff.knows), list(set(pDiff.items))]

                if loc.comeBack is not None:
                    ret[locName]["comeBack"] = loc.comeBack
                if loc.accessPoint is not None:
                    ret[locName]["accessPoint"] = self.transition2isolver(loc.accessPoint)
                    if loc.path is not None:
                        ret[locName]["path"] = [self.transition2isolver(a.Name) for a in loc.path]
                # for debug purpose
                if self.debug == True:
                    if loc.distance is not None:
                        ret[locName]["distance"] = loc.distance
        return ret

    def getRemainLocationsWeb(self, locations):
        ret = {}
        for loc in locations:
            if loc.difficulty is None or loc.difficulty.bool == False:
                locName = self.name4isolver(loc.Name)
                ret[locName] = {"item": loc.itemName,
                                "name": loc.Name,
                                "knows": ["Sequence Break"],
                                "items": [],
                                "canHidden": loc.CanHidden,
                                "visibility": loc.Visibility}
                if self.debug == True:
                    if loc.difficulty is not None:
                        ret[locName]["difficulty"] = str(loc.difficulty)
                    if loc.distance is not None:
                        ret[locName]["distance"] = loc.distance
        return ret

    def getLinesWeb(self, transitions):
        lines = {}
        linesSeq = []
        for (start, end) in transitions:
            startWeb = self.transition2isolver(start)
            endWeb = self.transition2isolver(end)
            lines[startWeb] = endWeb
            lines[endWeb] = startWeb
            linesSeq.append((startWeb, endWeb))
        return (lines, linesSeq)

    def getAvailableLocations(self, locations):
        ret = {}
        for loc in locations:
            if loc.difficulty is not None and loc.difficulty.bool == True:
                diff = loc.difficulty
                ret[loc.Name] = (diff.bool, diff.difficulty, diff.knows, diff.items)
        return ret

    def fromJson(self, stateJsonFileName):
        with open(stateJsonFileName, 'r') as jsonFile:
            self.state = json.load(jsonFile)
#        print("Loaded Json State:")
#        for key in self.state:
#            if key in ["availableLocationsWeb", "visitedLocationsWeb", "collectedItems", "availableLocations", "visitedLocations"]:
#                print("{}: {}".format(key, self.state[key]))
#        print("")

    def toJson(self, outputFileName):
        with open(outputFileName, 'w') as jsonFile:
            json.dump(self.state, jsonFile)
#        print("Dumped Json State:")
#        for key in self.state:
#            if key in ["availableLocationsWeb", "visitedLocationsWeb", "collectedItems", "visitedLocations"]:
#                print("{}: {}".format(key, self.state[key]))
#        print("")
