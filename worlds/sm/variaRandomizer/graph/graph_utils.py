import copy
from ..logic.logic import Logic
from ..utils.parameters import Knows
from ..graph.location import locationsDict
from ..rom.rom import snes_to_pc
from ..utils import log

# order expected by ROM patches
graphAreas = [
    "Ceres",
    "Crateria",
    "GreenPinkBrinstar",
    "RedBrinstar",
    "WreckedShip",
    "Kraid",
    "Norfair",
    "Crocomire",
    "LowerNorfair",
    "WestMaridia",
    "EastMaridia",
    "Tourian"
]

vanillaTransitions = [
    ('Lower Mushrooms Left', 'Green Brinstar Elevator'),
    ('Morph Ball Room Left', 'Green Hill Zone Top Right'),
    ('Moat Right', 'West Ocean Left'),
    ('Keyhunter Room Bottom', 'Red Brinstar Elevator'),
    ('Noob Bridge Right', 'Red Tower Top Left'),
    ('Crab Maze Left', 'Le Coude Right'),
    ('Kronic Boost Room Bottom Left', 'Lava Dive Right'),
    ('Crocomire Speedway Bottom', 'Crocomire Room Top'),
    ('Three Muskateers Room Left', 'Single Chamber Top Right'),
    ('Warehouse Entrance Left', 'East Tunnel Right'),
    ('East Tunnel Top Right', 'Crab Hole Bottom Left'),
    ('Caterpillar Room Top Right', 'Red Fish Room Left'),
    ('Glass Tunnel Top', 'Main Street Bottom'),
    ('Green Pirates Shaft Bottom Right', 'Golden Four'),
    ('Warehouse Entrance Right', 'Warehouse Zeela Room Left'),
    ('Crab Shaft Right', 'Aqueduct Top Left')
]

vanillaBossesTransitions = [
    ('KraidRoomOut', 'KraidRoomIn'),
    ('PhantoonRoomOut', 'PhantoonRoomIn'),
    ('DraygonRoomOut', 'DraygonRoomIn'),
    ('RidleyRoomOut', 'RidleyRoomIn')
]

# vanilla escape transition in first position
vanillaEscapeTransitions = [
    ('Tourian Escape Room 4 Top Right', 'Climb Bottom Left'),
    ('Brinstar Pre-Map Room Right', 'Green Brinstar Main Shaft Top Left'),
    ('Wrecked Ship Map Room', 'Basement Left'),
    ('Norfair Map Room', 'Business Center Mid Left'),
    ('Maridia Map Room', 'Crab Hole Bottom Right')
]

vanillaEscapeAnimalsTransitions = [
    ('Flyway Right 0', 'Bomb Torizo Room Left'),
    ('Flyway Right 1', 'Bomb Torizo Room Left'),
    ('Flyway Right 2', 'Bomb Torizo Room Left'),
    ('Flyway Right 3', 'Bomb Torizo Room Left'),
    ('Bomb Torizo Room Left Animals', 'Flyway Right')
]

escapeSource = 'Tourian Escape Room 4 Top Right'
escapeTargets = ['Green Brinstar Main Shaft Top Left', 'Basement Left', 'Business Center Mid Left', 'Crab Hole Bottom Right']

locIdsByAreaAddresses = {
    "Ceres": snes_to_pc(0xA1F568),
    "Crateria": snes_to_pc(0xA1F569),
    "GreenPinkBrinstar": snes_to_pc(0xA1F57B),
    "RedBrinstar": snes_to_pc(0xA1F58C),
    "WreckedShip": snes_to_pc(0xA1F592),
    "Kraid": snes_to_pc(0xA1F59E),
    "Norfair": snes_to_pc(0xA1F5A2),
    "Crocomire": snes_to_pc(0xA1F5B2),
    "LowerNorfair": snes_to_pc(0xA1F5B8),
    "WestMaridia": snes_to_pc(0xA1F5C3),
    "EastMaridia": snes_to_pc(0xA1F5CB),
    "Tourian": snes_to_pc(0xA1F5D7)
}

def getAccessPoint(apName, apList=None):
    if apList is None:
        apList = Logic.accessPoints
    return next(ap for ap in apList if ap.Name == apName)

class GraphUtils:
    log = log.get('GraphUtils')

    def getStartAccessPointNames():
        return [ap.Name for ap in Logic.accessPoints if ap.Start is not None]

    def getStartAccessPointNamesCategory():
        ret = {'regular': [], 'custom': [], 'area': []}
        for ap in Logic.accessPoints:
            if ap.Start == None:
                continue
            elif 'areaMode' in ap.Start and ap.Start['areaMode'] == True:
                ret['area'].append(ap.Name)
            elif GraphUtils.isStandardStart(ap.Name):
                ret['regular'].append(ap.Name)
            else:
                ret['custom'].append(ap.Name)
        return ret

    def isStandardStart(startApName):
        return startApName == 'Ceres' or startApName == 'Landing Site'

    def getPossibleStartAPs(areaMode, maxDiff, morphPlacement, player):
        ret = []
        refused = {}
        allStartAPs = GraphUtils.getStartAccessPointNames()
        for apName in allStartAPs:
            start = getAccessPoint(apName).Start
            ok = True
            cause = ""
            if 'knows' in start:
                for k in start['knows']:
                    if not Knows.knowsDict[player].knows(k, maxDiff):
                        ok = False
                        cause += Knows.desc[k]['display']+" is not known. "
                        break
            if 'areaMode' in start and start['areaMode'] != areaMode:
                ok = False
                cause += "Start location available only with area randomization enabled. "
            if 'forcedEarlyMorph' in start and start['forcedEarlyMorph'] == True and morphPlacement == 'late':
                ok = False
                cause += "Start location unavailable with late morph placement. "
            if ok:
                ret.append(apName)
            else:
                refused[apName] = cause
        return ret, refused

    @staticmethod
    def updateLocClassesStart(startGraphArea, split, possibleMajLocs, preserveMajLocs, nLocs, random):
        locs = locationsDict
        preserveMajLocs = [locs[locName] for locName in preserveMajLocs if locs[locName].isClass(split)]
        possLocs = [locs[locName] for locName in possibleMajLocs][:nLocs]
        GraphUtils.log.debug("possLocs="+str([loc.Name for loc in possLocs]))
        candidates = [loc for loc in locs.values() if loc.GraphArea == startGraphArea and loc.isClass(split) and loc not in preserveMajLocs]
        remLocs = [loc for loc in locs.values() if loc not in possLocs and loc not in candidates and loc.isClass(split)]
        newLocs = []
        while len(newLocs) < nLocs:
            if len(candidates) == 0:
                candidates = remLocs
            loc = possLocs.pop(random.randint(0,len(possLocs)-1))
            newLocs.append(loc)
            loc.setClass([split])
            if not loc in preserveMajLocs:
                GraphUtils.log.debug("newMajor="+loc.Name)
                loc = candidates.pop(random.randint(0,len(candidates)-1))
                loc.setClass(["Minor"])
                GraphUtils.log.debug("replaced="+loc.Name)

    def getGraphPatches(startApName):
        ap = getAccessPoint(startApName)
        return ap.Start['patches'] if 'patches' in ap.Start else []

    @staticmethod
    def createBossesTransitions(random):
        transitions = vanillaBossesTransitions
        def isVanilla():
            for t in vanillaBossesTransitions:
                if t not in transitions:
                    return False
            return True
        while isVanilla():
            transitions = []
            srcs = []
            dsts = []
            for (src,dst) in vanillaBossesTransitions:
                srcs.append(src)
                dsts.append(dst)
            while len(srcs) > 0:
                src = srcs.pop(random.randint(0,len(srcs)-1))
                dst = dsts.pop(random.randint(0,len(dsts)-1))
                transitions.append((src,dst))
        return transitions

    @staticmethod
    def createAreaTransitions(lightAreaRando=False, *, random):
        if lightAreaRando:
            return GraphUtils.createLightAreaTransitions(random=random)
        else:
            return GraphUtils.createRegularAreaTransitions(random=random)

    @staticmethod
    def createRegularAreaTransitions(apList=None, apPred=None, *, random):
        if apList is None:
            apList = Logic.accessPoints
        if apPred is None:
            apPred = lambda ap: ap.isArea()
        tFrom = []
        tTo = []
        apNames = [ap.Name for ap in apList if apPred(ap) == True]
        transitions = []

        def findTo(trFrom):
            ap = getAccessPoint(trFrom, apList)
            fromArea = ap.GraphArea
            targets = [apName for apName in apNames if apName not in tTo and getAccessPoint(apName, apList).GraphArea != fromArea]
            if len(targets) == 0: # fallback if no area transition is found
                targets = [apName for apName in apNames if apName != ap.Name]
                if len(targets) == 0: # extreme fallback: loop on itself
                    targets = [ap.Name]
            return random.choice(targets)

        def addTransition(src, dst):
            tFrom.append(src)
            tTo.append(dst)

        while len(apNames) > 0:
            sources = [apName for apName in apNames if apName not in tFrom]
            src = random.choice(sources)
            dst = findTo(src)
            transitions.append((src, dst))
            addTransition(src, dst)
            addTransition(dst, src)
            toRemove = [apName for apName in apNames if apName in tFrom and apName in tTo]
            for apName in toRemove:
                apNames.remove(apName)
        return transitions

    def getAPs(apPredicate, apList=None):
        if apList is None:
            apList = Logic.accessPoints
        return [ap for ap in apList if apPredicate(ap) == True]

    def loopUnusedTransitions(transitions, apList=None):
        if apList is None:
            apList = Logic.accessPoints
        usedAPs = set()
        for (src,dst) in transitions:
            usedAPs.add(getAccessPoint(src, apList))
            usedAPs.add(getAccessPoint(dst, apList))
        unusedAPs = [ap for ap in apList if not ap.isInternal() and ap not in usedAPs]
        for ap in unusedAPs:
            transitions.append((ap.Name, ap.Name))

    # crateria can be forced in corner cases
    @staticmethod
    def createMinimizerTransitions(startApName, locLimit, forcedAreas=None, *, random):
        if forcedAreas is None:
            forcedAreas = []
        if startApName == 'Ceres':
            startApName = 'Landing Site'
        startAp = getAccessPoint(startApName)
        def getNLocs(locsPredicate, locList=None):
            if locList is None:
                locList = Logic.locations
            # leave out bosses and count post boss locs systematically
            return len([loc for loc in locList if locsPredicate(loc) == True and not loc.SolveArea.endswith(" Boss") and not loc.isBoss()])
        availAreas = list(sorted({ap.GraphArea for ap in Logic.accessPoints if ap.GraphArea != startAp.GraphArea and getNLocs(lambda loc: loc.GraphArea == ap.GraphArea) > 0}))
        areas = [startAp.GraphArea]
        if startAp.GraphArea in forcedAreas:
            forcedAreas.remove(startAp.GraphArea)
        GraphUtils.log.debug("availAreas: {}".format(availAreas))
        GraphUtils.log.debug("forcedAreas: {}".format(forcedAreas))
        GraphUtils.log.debug("areas: {}".format(areas))
        inBossCheck = lambda ap: ap.Boss and ap.Name.endswith("In")
        nLocs = 0
        transitions = []
        usedAPs = []
        trLimit = 5
        locLimit -= 3 # 3 "post boss" locs will always be available, and are filtered out in getNLocs
        def openTransitions():
            nonlocal areas, inBossCheck, usedAPs
            return GraphUtils.getAPs(lambda ap: ap.GraphArea in areas and not ap.isInternal() and not inBossCheck(ap) and not ap in usedAPs)
        while nLocs < locLimit or len(openTransitions()) < trLimit or len(forcedAreas) > 0:
            GraphUtils.log.debug("openTransitions="+str([ap.Name for ap in openTransitions()]))
            fromAreas = availAreas
            if len(openTransitions()) <= 1: # dont' get stuck by adding dead ends
                GraphUtils.log.debug("avoid being stuck")
                fromAreas = [area for area in fromAreas if len(GraphUtils.getAPs(lambda ap: ap.GraphArea == area and not ap.isInternal())) > 1]
            elif len(forcedAreas) > 0: # no risk to get stuck, we can pick a forced area if necessary
                GraphUtils.log.debug("add forced area")
                fromAreas = forcedAreas
            elif nLocs >= locLimit: # we just need transitions, avoid adding a huge area
                GraphUtils.log.debug("not enough open transitions")
                fromAreas = []
                n = trLimit - len(openTransitions())
                while len(fromAreas) == 0:
                    fromAreas = [area for area in availAreas if len(GraphUtils.getAPs(lambda ap: not ap.isInternal())) > n]
                    n -= 1
                    minLocs = min([getNLocs(lambda loc: loc.GraphArea == area) for area in fromAreas])
                fromAreas = [area for area in fromAreas if getNLocs(lambda loc: loc.GraphArea == area) == minLocs]
            nextArea = random.choice(fromAreas)
            if nextArea in forcedAreas:
                forcedAreas.remove(nextArea)
            GraphUtils.log.debug("nextArea="+str(nextArea))
            apCheck = lambda ap: not ap.isInternal() and not inBossCheck(ap) and ap not in usedAPs
            possibleSources = GraphUtils.getAPs(lambda ap: ap.GraphArea in areas and apCheck(ap))
            possibleTargets = GraphUtils.getAPs(lambda ap: ap.GraphArea == nextArea and apCheck(ap))
            src = random.choice(possibleSources)
            dst = random.choice(possibleTargets)
            usedAPs += [src,dst]
            GraphUtils.log.debug("add transition: (src: {}, dst: {})".format(src.Name, dst.Name))
            transitions.append((src.Name,dst.Name))
            availAreas.remove(nextArea)
            areas.append(nextArea)
            GraphUtils.log.debug("areas: {}".format(areas))
            nLocs = getNLocs(lambda loc:loc.GraphArea in areas)
            GraphUtils.log.debug("nLocs: {}".format(nLocs))
        # we picked the areas, add transitions (bosses and tourian first)
        sourceAPs = openTransitions()
        random.shuffle(sourceAPs)
        targetAPs = GraphUtils.getAPs(lambda ap: (inBossCheck(ap) or ap.Name == "Golden Four") and not ap in usedAPs)
        random.shuffle(targetAPs)
        assert len(sourceAPs) >= len(targetAPs), "Minimizer: less source than target APs"
        while len(targetAPs) > 0:
            transitions.append((sourceAPs.pop().Name, targetAPs.pop().Name))
        transitions += GraphUtils.createRegularAreaTransitions(sourceAPs, lambda ap: not ap.isInternal())
        GraphUtils.log.debug("FINAL MINIMIZER transitions: {}".format(transitions))
        GraphUtils.loopUnusedTransitions(transitions)
        GraphUtils.log.debug("FINAL MINIMIZER nLocs: "+str(nLocs+3))
        GraphUtils.log.debug("FINAL MINIMIZER areas: "+str(areas))
        return transitions

    @staticmethod
    def createLightAreaTransitions(random):
        # group APs by area
        aps = {}
        totalCount = 0
        for ap in Logic.accessPoints:
            if not ap.isArea():
                continue
            if not ap.GraphArea in aps:
                aps[ap.GraphArea] = {'totalCount': 0, 'transCount': {}, 'apNames': []}
            aps[ap.GraphArea]['apNames'].append(ap.Name)
        # count number of vanilla transitions between each area
        for (srcName, destName) in vanillaTransitions:
            srcAP = getAccessPoint(srcName)
            destAP = getAccessPoint(destName)
            aps[srcAP.GraphArea]['transCount'][destAP.GraphArea] = aps[srcAP.GraphArea]['transCount'].get(destAP.GraphArea, 0) + 1
            aps[srcAP.GraphArea]['totalCount'] += 1
            aps[destAP.GraphArea]['transCount'][srcAP.GraphArea] = aps[destAP.GraphArea]['transCount'].get(srcAP.GraphArea, 0) + 1
            aps[destAP.GraphArea]['totalCount'] += 1
            totalCount += 1

        transitions = []
        while totalCount > 0:
            # choose transition
            srcArea = random.choice(list(aps.keys()))
            srcName = random.choice(aps[srcArea]['apNames'])
            src = getAccessPoint(srcName)
            destArea = random.choice(list(aps[src.GraphArea]['transCount'].keys()))
            destName = random.choice(aps[destArea]['apNames'])
            transitions.append((srcName, destName))

            # update counts
            totalCount -= 1
            aps[srcArea]['totalCount'] -= 1
            aps[destArea]['totalCount'] -= 1
            aps[srcArea]['transCount'][destArea] -= 1
            if aps[srcArea]['transCount'][destArea] == 0:
                del aps[srcArea]['transCount'][destArea]
            aps[destArea]['transCount'][srcArea] -= 1
            if aps[destArea]['transCount'][srcArea] == 0:
                del aps[destArea]['transCount'][srcArea]
            aps[srcArea]['apNames'].remove(srcName)
            aps[destArea]['apNames'].remove(destName)

            if aps[srcArea]['totalCount'] == 0:
                del aps[srcArea]
            if aps[destArea]['totalCount'] == 0:
                del aps[destArea]

        return transitions

    def getVanillaExit(apName):
        allVanillaTransitions = vanillaTransitions + vanillaBossesTransitions + vanillaEscapeTransitions
        for (src,dst) in allVanillaTransitions:
            if apName == src:
                return dst
            if apName == dst:
                return src
        return None

    def isEscapeAnimals(apName):
        return 'Flyway Right' in apName or 'Bomb Torizo Room Left' in apName

    # gets dict like
    # (RoomPtr, (vanilla entry screen X, vanilla entry screen Y)): AP
    def getRooms():
        rooms = {}
        for ap in Logic.accessPoints:
            if ap.Internal == True:
                continue
            # special ap for random escape animals surprise
            if GraphUtils.isEscapeAnimals(ap.Name):
                continue

            roomPtr = ap.RoomInfo['RoomPtr']

            vanillaExitName = GraphUtils.getVanillaExit(ap.Name)
            # special ap for random escape animals surprise
            if GraphUtils.isEscapeAnimals(vanillaExitName):
                continue

            connAP = getAccessPoint(vanillaExitName)
            entryInfo = connAP.ExitInfo
            rooms[(roomPtr, entryInfo['screen'], entryInfo['direction'])] = ap
            rooms[(roomPtr, entryInfo['screen'], (ap.EntryInfo['SamusX'], ap.EntryInfo['SamusY']))] = ap
            # for boss rando with incompatible ridley transition, also register this one
            if ap.Name == 'RidleyRoomIn':
                rooms[(roomPtr, (0x0, 0x1), 0x5)] = ap
                rooms[(roomPtr, (0x0, 0x1), (0xbf, 0x198))] = ap

        return rooms

    @staticmethod
    def escapeAnimalsTransitions(graph, possibleTargets, firstEscape, random):
        n = len(possibleTargets)
        assert (n < 4 and firstEscape is not None) or (n <= 4 and firstEscape is None), "Invalid possibleTargets list: " + str(possibleTargets)
        GraphUtils.log.debug("escapeAnimalsTransitions. possibleTargets="+str(possibleTargets)+", firstEscape="+str(firstEscape))
        if n >= 1:
            # complete possibleTargets. we need at least 2: one to
            # hide the animals in, and one to connect the vanilla
            # animals door to
            if not any(t[1].Name == 'Climb Bottom Left' for t in graph.InterAreaTransitions):
                # add standard Climb if not already in graph: it can be in Crateria-less minimizer + Disabled Tourian case
                possibleTargets.append('Climb Bottom Left')
            # make the escape possibilities loop by adding back the first escape
            if firstEscape is not None:
                possibleTargets.append(firstEscape)
            poss = possibleTargets[:]
            while len(possibleTargets) < 4:
                possibleTargets.append(poss.pop(random.randint(0, len(poss)-1)))
        n = len(possibleTargets)
        # check if we can both hide the animals and connect the vanilla animals door to a cycling escape
        if n >= 2:
            # get actual animals: pick the first of the remaining targets (will contain a map room AP)
            animalsAccess = possibleTargets.pop(0)
            graph.EscapeAttributes['Animals'] = animalsAccess
            # poss will contain the remaining map room AP(s) + optional AP(s) added above, to
            # get the cycling 4 escapes from vanilla animals room
            poss = possibleTargets[:]
            GraphUtils.log.debug("escapeAnimalsTransitions. poss="+str(poss))
            while len(possibleTargets) < 4:
                if len(poss) > 1:
                    possibleTargets.append(poss.pop(random.randint(0, len(poss)-1)))
                else:
                    # no more possible variety, spam the last possible escape
                    possibleTargets.append(poss[0])

        else:
            # failsafe: if not enough targets left, abort and do vanilla animals
            animalsAccess = 'Flyway Right'
            possibleTargets = ['Bomb Torizo Room Left'] * 4
        GraphUtils.log.debug("escapeAnimalsTransitions. animalsAccess="+animalsAccess)
        assert len(possibleTargets) == 4, "Invalid possibleTargets list: " + str(possibleTargets)
        # actually add the 4 connections for successive escapes challenge
        basePtr = 0xADAC
        btDoor = getAccessPoint('Flyway Right')
        for i in range(len(possibleTargets)):
            ap = copy.copy(btDoor)
            ap.Name += " " + str(i)
            ap.ExitInfo['DoorPtr'] = basePtr + i*24
            graph.addAccessPoint(ap)
            target = possibleTargets[i]
            graph.addTransition(ap.Name, target)
        # add the connection for animals access
        bt = getAccessPoint('Bomb Torizo Room Left')
        btCpy = copy.copy(bt)
        btCpy.Name += " Animals"
        btCpy.ExitInfo['DoorPtr'] = 0xAE00
        graph.addAccessPoint(btCpy)
        graph.addTransition(animalsAccess, btCpy.Name)

    def isHorizontal(dir):
        # up: 0x3, 0x7
        # down: 0x2, 0x6
        # left: 0x1, 0x5
        # right: 0x0, 0x4
        return dir in [0x1, 0x5, 0x0, 0x4]

    def removeCap(dir):
        if dir < 4:
            return dir
        return dir - 4

    def getDirection(src, dst):
        exitDir = src.ExitInfo['direction']
        entryDir = dst.EntryInfo['direction']
        # compatible transition
        if exitDir == entryDir:
            return exitDir
        # if incompatible but horizontal we keep entry dir (looks more natural)
        if GraphUtils.isHorizontal(exitDir) and GraphUtils.isHorizontal(entryDir):
            return entryDir
        # otherwise keep exit direction and remove cap
        return GraphUtils.removeCap(exitDir)

    def getBitFlag(srcArea, dstArea, origFlag):
        flags = origFlag
        if srcArea == dstArea:
            flags &= 0xBF
        else:
            flags |= 0x40
        return flags

    def getDoorConnections(graph, areas=True, bosses=False,
                           escape=True, escapeAnimals=True):
        transitions = []
        if areas:
            transitions += vanillaTransitions
        if bosses:
            transitions += vanillaBossesTransitions
        if escape:
            transitions += vanillaEscapeTransitions
            if escapeAnimals:
                transitions += vanillaEscapeAnimalsTransitions
        for srcName, dstName in transitions:
            src = graph.accessPoints[srcName]
            dst = graph.accessPoints[dstName]
            dst.EntryInfo.update(src.ExitInfo)
            src.EntryInfo.update(dst.ExitInfo)
        connections = []
        for src, dst in graph.InterAreaTransitions:
            if not (escape and src.Escape and dst.Escape):
                # area only
                if not bosses and src.Boss:
                    continue
                # boss only
                if not areas and not src.Boss:
                    continue
                # no random escape
                if not escape and src.Escape:
                    continue

            conn = {}
            conn['ID'] = str(src) + ' -> ' + str(dst)
            # remove duplicates (loop transitions)
            if any(c['ID'] == conn['ID'] for c in connections):
                continue
#            print(conn['ID'])
            # where to write
            conn['DoorPtr'] = src.ExitInfo['DoorPtr']
            # door properties
            conn['RoomPtr'] = dst.RoomInfo['RoomPtr']
            conn['doorAsmPtr'] = dst.EntryInfo['doorAsmPtr']
            if 'exitAsmPtr' in src.ExitInfo:
                conn['exitAsmPtr'] = src.ExitInfo['exitAsmPtr']
            conn['direction'] = GraphUtils.getDirection(src, dst)
            conn['bitFlag'] = GraphUtils.getBitFlag(src.RoomInfo['area'], dst.RoomInfo['area'],
                                                    dst.EntryInfo['bitFlag'])
            conn['cap'] = dst.EntryInfo['cap']
            conn['screen'] = dst.EntryInfo['screen']
            if conn['direction'] != src.ExitInfo['direction']: # incompatible transition
                conn['distanceToSpawn'] = 0
                conn['SamusX'] = dst.EntryInfo['SamusX']
                conn['SamusY'] = dst.EntryInfo['SamusY']
                if dst.Name == 'RidleyRoomIn': # special case: spawn samus on ridley platform
                    conn['screen'] = (0x0, 0x1)
            else:
                conn['distanceToSpawn'] = dst.EntryInfo['distanceToSpawn']
            if 'song' in dst.EntryInfo:
                conn['song'] = dst.EntryInfo['song']
                conn['songs'] = dst.RoomInfo['songs']
            connections.append(conn)
        return connections

    def getDoorsPtrs2Aps():
        ret = {}
        for ap in Logic.accessPoints:
            if ap.Internal == True:
                continue
            ret[ap.ExitInfo["DoorPtr"]] = ap.Name
        return ret

    def getAps2DoorsPtrs():
        ret = {}
        for ap in Logic.accessPoints:
            if ap.Internal == True:
                continue
            ret[ap.Name] = ap.ExitInfo["DoorPtr"]
        return ret

    def getTransitions(addresses):
        # build address -> name dict
        doorsPtrs = GraphUtils.getDoorsPtrs2Aps()

        transitions = []
        # (src.ExitInfo['DoorPtr'], dst.ExitInfo['DoorPtr'])
        for (srcDoorPtr, destDoorPtr) in addresses:
            transitions.append((doorsPtrs[srcDoorPtr], doorsPtrs[destDoorPtr]))

        return transitions

    def hasMixedTransitions(areaTransitions, bossTransitions):
        vanillaAPs = []
        for (src, dest) in vanillaTransitions:
            vanillaAPs += [src, dest]

        vanillaBossesAPs = []
        for (src, dest) in vanillaBossesTransitions:
            vanillaBossesAPs += [src, dest]

        for (src, dest) in areaTransitions:
            if src in vanillaBossesAPs or dest in vanillaBossesAPs:
                return True

        for (src, dest) in bossTransitions:
            if src in vanillaAPs or dest in vanillaAPs:
                return True

        return False
