import copy, logging
from operator import attrgetter
from ..utils import log
from ..logic.smbool import SMBool, smboolFalse
from ..utils.parameters import infinity
from ..logic.helpers import Bosses

class Path(object):
    __slots__ = ( 'path', 'pdiff', 'distance' )

    def __init__(self, path, pdiff, distance):
        self.path = path
        self.pdiff = pdiff
        self.distance = distance

class AccessPoint(object):
    # name : AccessPoint name
    # graphArea : graph area the node is located in
    # transitions : intra-area transitions
    # traverse: traverse function, will be wand to the added transitions
    # exitInfo : dict carrying vanilla door information : 'DoorPtr': door address, 'direction', 'cap', 'screen', 'bitFlag', 'distanceToSpawn', 'doorAsmPtr' : door properties
    # entryInfo : dict carrying forced samus X/Y position with keys 'SamusX' and 'SamusY'.
    #             (to be updated after reading vanillaTransitions and gather entry info from matching exit door)
    # roomInfo : dict with 'RoomPtr' : room address, 'area'
    # shortName : short name for the credits
    # internal : if true, shall not be used for connecting areas
    def __init__(self, name, graphArea, transitions,
                 traverse=lambda sm: SMBool(True),
                 exitInfo=None, entryInfo=None, roomInfo=None,
                 internal=False, boss=False, escape=False,
                 start=None,
                 dotOrientation='w'):
        self.Name = name
        self.GraphArea = graphArea
        self.ExitInfo = exitInfo
        self.EntryInfo = entryInfo
        self.RoomInfo = roomInfo
        self.Internal = internal
        self.Boss = boss
        self.Escape = escape
        self.Start = start
        self.DotOrientation = dotOrientation
        self.intraTransitions = self.sortTransitions(transitions)
        self.transitions = copy.copy(self.intraTransitions)
        self.traverse = traverse
        self.distance = 0
        # inter-area connection
        self.ConnectedTo = None

    def __copy__(self):
        exitInfo = copy.deepcopy(self.ExitInfo) if self.ExitInfo is not None else None
        entryInfo = copy.deepcopy(self.EntryInfo) if self.EntryInfo is not None else None
        roomInfo = copy.deepcopy(self.RoomInfo) if self.RoomInfo is not None else None
        start = copy.deepcopy(self.Start) if self.Start is not None else None
        # in any case, do not copy connections
        return AccessPoint(self.Name, self.GraphArea, self.intraTransitions, self.traverse,
                           exitInfo, entryInfo, roomInfo,
                           self.Internal, self.Boss, self.Escape,
                           start, self.DotOrientation)

    def __str__(self):
        return "[" + self.GraphArea + "] " + self.Name

    def __repr__(self):
        return self.Name

    def sortTransitions(self, transitions=None):
        # sort transitions before the loop in getNewAvailNodes.
        # as of python3.7 insertion order is guaranteed in dictionaires.
        if transitions is None:
            transitions = self.transitions
        return { key: transitions[key] for key in sorted(transitions.keys()) }

    # connect to inter-area access point
    def connect(self, destName):
        self.disconnect()
        if self.Internal is False:
            self.transitions[destName] = self.traverse
            self.ConnectedTo = destName
        else:
            raise RuntimeError("Cannot add an internal access point as inter-are transition")
        self.transitions = self.sortTransitions()

    def disconnect(self):
        if self.ConnectedTo is not None:
            if self.ConnectedTo not in self.intraTransitions:
                del self.transitions[self.ConnectedTo]
            else:
                self.transitions[self.ConnectedTo] = self.intraTransitions[self.ConnectedTo]
        self.ConnectedTo = None

    # tells if this node is to connect areas together
    def isArea(self):
        return not self.Internal and not self.Boss and not self.Escape

    # used by the solver to get area and boss APs
    def isInternal(self):
        return self.Internal or self.Escape

    def isLoop(self):
        return self.ConnectedTo == self.Name

class AccessGraph(object):
    __slots__ = ( 'log', 'accessPoints', 'InterAreaTransitions',
                  'EscapeAttributes', 'apCache', '_useCache',
                  'availAccessPoints' )

    def __init__(self, accessPointList, transitions, dotFile=None):
        self.log = log.get('Graph')
        self.accessPoints = {}
        self.InterAreaTransitions = []
        self.EscapeAttributes = {
            'Timer': None,
            'Animals': None
        }
        for ap in accessPointList:
            self.addAccessPoint(ap)
        for srcName, dstName in transitions:
            self.addTransition(srcName, dstName)
        if dotFile is not None:
            self.toDot(dotFile)
        self.apCache = {}
        self._useCache = False
        # store the avail access points to display in vcr
        self.availAccessPoints = {}

    def useCache(self, use):
        self._useCache = use
        if self._useCache:
            self.resetCache()

    def resetCache(self):
        self.apCache = {}

    def printGraph(self):
        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("Area graph:")
            for s, d in self.InterAreaTransitions:
                self.log.debug("{} -> {}".format(s.Name, d.Name))

    def addAccessPoint(self, ap):
        ap.distance = 0
        self.accessPoints[ap.Name] = copy.deepcopy(ap)

    def toDot(self, dotFile):
        colors = ['red', 'blue', 'green', 'yellow', 'skyblue', 'violet', 'orange',
                  'lawngreen', 'crimson', 'chocolate', 'turquoise', 'tomato',
                  'navyblue', 'darkturquoise', 'green', 'blue', 'maroon', 'magenta',
                  'bisque', 'coral', 'chartreuse', 'chocolate', 'cyan']
        with open(dotFile, "w") as f:
            f.write("digraph {\n")
            f.write('size="30,30!";\n')
            f.write('rankdir=LR;\n')
            f.write('ranksep=2.2;\n')
            f.write('overlap=scale;\n')
            f.write('edge [dir="both",arrowhead="box",arrowtail="box",arrowsize=0.5,fontsize=7,style=dotted];\n')
            f.write('node [shape="box",fontsize=10];\n')
            for area in set([ap.GraphArea for ap in self.accessPoints.values()]):
                f.write(area + ";\n") # TODO area long name and color
            drawn = []
            i = 0
            for src, dst in self.InterAreaTransitions:
                if src.Name in drawn:
                    continue
                f.write('%s:%s -> %s:%s [taillabel="%s",headlabel="%s",color=%s];\n' % (src.GraphArea, src.DotOrientation, dst.GraphArea, dst.DotOrientation, src.Name, dst.Name, colors[i]))
                drawn += [src.Name,dst.Name]
                i += 1
            f.write("}\n")

    def addTransition(self, srcName, dstName, both=True):
        src = self.accessPoints[srcName]
        dst = self.accessPoints[dstName]
        src.connect(dstName)
        self.InterAreaTransitions.append((src, dst))
        if both is True:
            self.addTransition(dstName, srcName, False)

    # remove transitions whose source or dest matches apName
    def removeTransitions(self, apName):
        toRemove = [t for t in self.InterAreaTransitions if t[0].Name == apName or t[1].Name == apName]
        for t in toRemove:
            src, dst = t
            self.InterAreaTransitions.remove(t)
            src.disconnect()
            dst.disconnect()

    # availNodes: all already available nodes
    # nodesToCheck: nodes we have to check transitions for
    # smbm: smbm to test logic on. if None, discard logic check, assume we can reach everything
    # maxDiff: difficulty limit
    # return newly opened access points
    def getNewAvailNodes(self, availNodes, nodesToCheck, smbm, maxDiff, item=None):
        newAvailNodes = {}
        # with python >= 3.6 the insertion order in a dict is keeps when looping on the keys,
        # so we no longer have to sort them.
        for src in nodesToCheck:
            for dstName in src.transitions:
                dst = self.accessPoints[dstName]
                if dst in availNodes or dst in newAvailNodes:
                    continue
                if smbm is not None:
                    if self._useCache == True and (src, dst, item) in self.apCache:
                        diff = self.apCache[(src, dst, item)]
                    else:
                        tFunc = src.transitions[dstName]
                        diff = tFunc(smbm)
                        if self._useCache == True:
                            self.apCache[(src, dst, item)] = diff
                else:
                    diff = SMBool(True)
                if diff.bool and diff.difficulty <= maxDiff:
                    if src.GraphArea == dst.GraphArea:
                        dst.distance = src.distance + 0.01
                    else:
                        dst.distance = src.distance + 1
                    newAvailNodes[dst] = { 'difficulty': diff, 'from': src }

                #self.log.debug("{} -> {}: {}".format(src.Name, dstName, diff))
        return newAvailNodes

    # rootNode: starting AccessPoint instance
    # smbm: smbm to test logic on. if None, discard logic check, assume we can reach everything
    # maxDiff: difficulty limit.
    # smbm: if None, discard logic check, assume we can reach everything
    # return available AccessPoint list
    def getAvailableAccessPoints(self, rootNode, smbm, maxDiff, item=None):
        availNodes = { rootNode : { 'difficulty' : SMBool(True, 0), 'from' : None } }
        newAvailNodes = availNodes
        rootNode.distance = 0
        while len(newAvailNodes) > 0:
            newAvailNodes = self.getNewAvailNodes(availNodes, newAvailNodes, smbm, maxDiff, item)
            availNodes.update(newAvailNodes)
        return availNodes

    # gets path from the root AP used to compute availAps
    def getPath(self, dstAp, availAps):
        path = []
        root = dstAp
        while root != None:
            path = [root] + path
            root = availAps[root]['from']

        return path

    def getAvailAPPaths(self, availAccessPoints, locsAPs):
        paths = {}
        for ap in availAccessPoints:
            if ap.Name in locsAPs:
                path = self.getPath(ap, availAccessPoints)
                pdiff = SMBool.wandmax(*(availAccessPoints[ap]['difficulty'] for ap in path))
                paths[ap.Name] = Path(path, pdiff, len(path))
        return paths

    def getSortedAPs(self, paths, locAccessFrom):
        ret = []

        for apName in locAccessFrom:
            path = paths.get(apName, None)
            if path is None:
                continue
            difficulty = paths[apName].pdiff.difficulty
            ret.append((difficulty if difficulty != -1 else infinity, path.distance, apName))
        ret.sort()
        return [apName for diff, dist, apName in ret]

    # locations: locations to check
    # items: collected items
    # maxDiff: difficulty limit
    # rootNode: starting AccessPoint
    # return available locations list, also stores difficulty in locations
    def getAvailableLocations(self, locations, smbm, maxDiff, rootNode='Landing Site'):
        rootAp = self.accessPoints[rootNode]
        self.availAccessPoints = self.getAvailableAccessPoints(rootAp, smbm, maxDiff)
        availAreas = set([ap.GraphArea for ap in self.availAccessPoints.keys()])
        availLocs = []

        # get all the current locations APs first to only compute these paths
        locsAPs = set()
        for loc in locations:
            for ap in loc.AccessFrom:
                locsAPs.add(ap)

        # sort availAccessPoints based on difficulty to take easier paths first
        availAPPaths = self.getAvailAPPaths(self.availAccessPoints, locsAPs)

        for loc in locations:
            if loc.GraphArea not in availAreas:
                loc.distance = 30000
                loc.difficulty = smboolFalse
                #if loc.Name == "Kraid":
                #    print("loc: {} locDiff is area nok".format(loc.Name))
                continue

            locAPs = self.getSortedAPs(availAPPaths, loc.AccessFrom)
            if len(locAPs) == 0:
                loc.distance = 40000
                loc.difficulty = smboolFalse
                #if loc.Name == "Kraid":
                #    print("loc: {} no aps".format(loc.Name))
                continue

            for apName in locAPs:
                if apName == None:
                    loc.distance = 20000
                    loc.difficulty = smboolFalse
                    #if loc.Name == "Kraid":
                    #    print("loc: {} ap is none".format(loc.Name))
                    break

                tFunc = loc.AccessFrom[apName]
                ap = self.accessPoints[apName]
                tdiff = tFunc(smbm)
                #if loc.Name == "Kraid":
                #    print("{} root: {} ap: {}".format(loc.Name, rootNode, apName))
                if tdiff.bool == True and tdiff.difficulty <= maxDiff:
                    diff = loc.Available(smbm)
                    if diff.bool == True:
                        path = availAPPaths[apName].path
                        #if loc.Name == "Kraid":
                        #    print("{} path: {}".format(loc.Name, [a.Name for a in path]))
                        pdiff = availAPPaths[apName].pdiff
                        (allDiff, locDiff) = self.computeLocDiff(tdiff, diff, pdiff)
                        if allDiff.bool == True and allDiff.difficulty <= maxDiff:
                            loc.distance = ap.distance + 1
                            loc.accessPoint = apName
                            loc.difficulty = allDiff
                            loc.path = path
                            # used only by solver
                            loc.pathDifficulty = pdiff
                            loc.locDifficulty = locDiff
                            availLocs.append(loc)
                            #if loc.Name == "Kraid":
                            #    print("{} diff: {} tdiff: {} pdiff: {}".format(loc.Name, diff, tdiff, pdiff))
                            break
                        else:
                            loc.distance = 1000 + tdiff.difficulty
                            loc.difficulty = smboolFalse
                            #if loc.Name == "Kraid":
                            #    print("loc: {} allDiff is false".format(loc.Name))
                    else:
                        loc.distance = 1000 + tdiff.difficulty
                        loc.difficulty = smboolFalse
                        #if loc.Name == "Kraid":
                        #    print("loc: {} allDiff is false".format(loc.Name))
                else:
                    loc.distance = 10000 + tdiff.difficulty
                    loc.difficulty = smboolFalse
                    #if loc.Name == "Kraid":
                    #    print("loc: {} tdiff is false".format(loc.Name))

            if loc.difficulty is None:
                #if loc.Name == "Kraid":
                #    print("loc: {} no difficulty in loc".format(loc.Name))
                loc.distance = 100000
                loc.difficulty = smboolFalse

            #if loc.Name == "Kraid":
            #    print("loc: {}: {}".format(loc.Name, loc))

        #print("availableLocs: {}".format([loc.Name for loc in availLocs]))
        return availLocs

    # test access from an access point to another, given an optional item
    def canAccess(self, smbm, srcAccessPointName, destAccessPointName, maxDiff, item=None):
        addAndRemoveItem = item is not None and (smbm.isCountItem(item) or not smbm.haveItem(item))
        if addAndRemoveItem:
            smbm.addItem(item)
        #print("canAccess: item: {}, src: {}, dest: {}".format(item, srcAccessPointName, destAccessPointName))
        destAccessPoint = self.accessPoints[destAccessPointName]
        srcAccessPoint = self.accessPoints[srcAccessPointName]
        availAccessPoints = self.getAvailableAccessPoints(srcAccessPoint, smbm, maxDiff, item)
        can = destAccessPoint in availAccessPoints
        # if not can:
        #     self.log.debug("canAccess KO: avail = {}".format([ap.Name for ap in availAccessPoints.keys()]))
        if addAndRemoveItem:
            smbm.removeItem(item)
        #print("canAccess: {}".format(can))
        return can

    # returns a list of AccessPoint instances from srcAccessPointName to destAccessPointName
    # (not including source ap)
    # or None if no possible path
    def accessPath(self, smbm, srcAccessPointName, destAccessPointName, maxDiff):
        destAccessPoint = self.accessPoints[destAccessPointName]
        srcAccessPoint = self.accessPoints[srcAccessPointName]
        availAccessPoints = self.getAvailableAccessPoints(srcAccessPoint, smbm, maxDiff)
        if destAccessPoint not in availAccessPoints:
            return None
        return self.getPath(destAccessPoint, availAccessPoints)

    # gives theoretically accessible APs in the graph (no logic check)
    def getAccessibleAccessPoints(self, rootNode='Landing Site'):
        rootAp = self.accessPoints[rootNode]
        inBossChk = lambda ap: ap.Boss and ap.Name.endswith("In")
        allAreas = {dst.GraphArea for (src, dst) in self.InterAreaTransitions if not inBossChk(dst) and not dst.isLoop()}
        self.log.debug("allAreas="+str(allAreas))
        nonBossAPs = [ap for ap in self.getAvailableAccessPoints(rootAp, None, 0) if ap.GraphArea in allAreas]
        bossesAPs = [self.accessPoints[boss+'RoomIn'] for boss in Bosses.Golden4()] + [self.accessPoints['Draygon Room Bottom']]
        return nonBossAPs + bossesAPs

    # gives theoretically accessible locations within a base list
    # returns locations with accessible GraphArea in this graph (no logic considered)
    def getAccessibleLocations(self, locations, rootNode='Landing Site'):
        availAccessPoints = self.getAccessibleAccessPoints(rootNode)
        self.log.debug("availAccessPoints="+str([ap.Name for ap in availAccessPoints]))
        return [loc for loc in locations if any(ap.Name in loc.AccessFrom for ap in availAccessPoints)]

class AccessGraphSolver(AccessGraph):
    def computeLocDiff(self, tdiff, diff, pdiff):
        # tdiff: difficulty from the location's access point to the location's room
        # diff: difficulty to reach the item in the location's room
        # pdiff: difficulty of the path from the current access point to the location's access point
        # in output we need the global difficulty but we also need to separate pdiff and (tdiff + diff)

        locDiff = SMBool.wandmax(tdiff, diff)
        allDiff = SMBool.wandmax(locDiff, pdiff)

        return (allDiff, locDiff)

class AccessGraphRando(AccessGraph):
    def computeLocDiff(self, tdiff, diff, pdiff):
        allDiff = SMBool.wandmax(tdiff, diff, pdiff)
        return (allDiff, None)
