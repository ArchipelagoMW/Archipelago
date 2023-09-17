
import random, copy
from ..utils import log
from ..graph.graph_utils import GraphUtils, vanillaTransitions, vanillaBossesTransitions, escapeSource, escapeTargets, graphAreas, getAccessPoint
from ..logic.logic import Logic
from ..graph.graph import AccessGraphRando as AccessGraph
from ..logic.smbool import SMBool
from ..utils.objectives import Objectives
from ..rando.ItemLocContainer import getItemLocStr
from collections import defaultdict

# creates graph and handles randomized escape
class GraphBuilder(object):
    def __init__(self, graphSettings):
        self.graphSettings = graphSettings
        self.areaRando = graphSettings.areaRando
        self.bossRando = graphSettings.bossRando
        self.escapeRando = graphSettings.escapeRando
        self.minimizerN = graphSettings.minimizerN
        self.log = log.get('GraphBuilder')

    # builds everything but escape transitions
    def createGraph(self, maxDiff):
        transitions = self.graphSettings.plandoRandoTransitions
        if transitions is None:
            transitions = []
            if self.minimizerN is not None:
                forcedAreas = set()
                # if no Crateria and auto escape trigger, we connect door connected to G4 to climb instead (see below).
                # This wouldn't work here, as Tourian is isolated in the resulting seed (see below again)
                # (well we could do two different transitions on both sides of doors, but that would just be confusing)
                # so we force crateria to be in the graph
                if self.graphSettings.startAP == "Golden Four" and self.graphSettings.tourian == "Disabled":
                    forcedAreas.add('Crateria')
                # force areas required by objectives
                # 1st the 'clear area' ones
                forcedAreas = forcedAreas.union({goal.area for goal in Objectives.objDict[self.graphSettings.player].activeGoals if goal.area is not None})
                # for the rest, base ourselves on escapeAccessPoints :
                # - if only "1 of n" pick an area, preferably one already forced
                # - filter out G4 AP (always there)
                for goal in Objectives.objDict[self.graphSettings.player].activeGoals:
                    if goal.area is None:
                        n, apNames = goal.escapeAccessPoints
                        aps = [getAccessPoint(apName) for apName in apNames]
                        if len(aps) >= n:
                            n -= len([ap for ap in aps if ap.Boss])
                            escAreas = {ap.GraphArea for ap in aps if not ap.Boss}
                            objForced = forcedAreas.intersection(escAreas)
                            escAreasList = sorted(list(escAreas))
                            while len(objForced) < n and len(escAreasList) > 0:
                                objForced.add(escAreasList.pop(random.randint(0, len(escAreasList)-1)))
                            forcedAreas = forcedAreas.union(objForced)
                transitions = GraphUtils.createMinimizerTransitions(self.graphSettings.startAP, self.minimizerN, sorted(list(forcedAreas)))
            else:
                if not self.bossRando:
                    transitions += vanillaBossesTransitions
                else:
                    transitions += GraphUtils.createBossesTransitions()
                if not self.areaRando:
                    transitions += vanillaTransitions
                else:
                    transitions += GraphUtils.createAreaTransitions(self.graphSettings.lightAreaRando)
        ret = AccessGraph(Logic.accessPoints, transitions, self.graphSettings.dotFile)
        Objectives.objDict[self.graphSettings.player].setGraph(ret, maxDiff)
        return ret
    
    def addForeignItems(self, container, itemLocs):
        itemPoolCounts = {}
        for item in container.itemPool:
            if item.Code is not None:
                itemPoolCounts[item.Type] = itemPoolCounts.get(item.Type, 0) + 1
        itemLocsCounts = {}
        for il in itemLocs:
            if il.Item.Code is not None and il.player == container.sm.player:
                itemLocsCounts[il.Item.Type] = itemLocsCounts.get(il.Item.Type, 0) + 1

        for item, count in itemPoolCounts.items():
            for n in range(max(0, count - itemLocsCounts.get(item, 0))):
                container.sm.addItem(item)

    # fills in escape transitions if escape rando is enabled
    # escapeTrigger = None or (itemLocs, progItemlocs) couple from filler
    def escapeGraph(self, container, graph, maxDiff, escapeTrigger):
        if not self.escapeRando:
            return True
        emptyContainer = copy.copy(container)
        emptyContainer.resetCollected(reassignItemLocs=True)
        dst = None
        if escapeTrigger is None:
            possibleTargets, dst, path = self.getPossibleEscapeTargets(emptyContainer, graph, maxDiff)
            # update graph with escape transition
            graph.addTransition(escapeSource, dst)
            paths = [path]
        else:
            self.addForeignItems(emptyContainer, escapeTrigger[0])
            possibleTargets, paths = self.escapeTrigger(emptyContainer, graph, maxDiff, escapeTrigger)
            if paths is None:
                return False
        # get timer value
        self.escapeTimer(graph, paths, self.areaRando or escapeTrigger is not None)
        self.log.debug("escapeGraph: ({}, {}) timer: {}".format(escapeSource, dst, graph.EscapeAttributes['Timer']))
        # animals
        GraphUtils.escapeAnimalsTransitions(graph, possibleTargets, dst)
        return True

    def _getTargets(self, sm, graph, maxDiff):
        possibleTargets = [target for target in escapeTargets if graph.accessPath(sm, target, 'Landing Site', maxDiff) is not None]
        self.log.debug('_getTargets. targets='+str(possibleTargets))
        # failsafe
        if len(possibleTargets) == 0:
            self.log.debug("Can't randomize escape, fallback to vanilla")
            possibleTargets.append('Climb Bottom Left')
        random.shuffle(possibleTargets)
        return possibleTargets

    def getPossibleEscapeTargets(self, emptyContainer, graph, maxDiff):
        sm = emptyContainer.sm
        # setup smbm with item pool:
        # - Ice not usable because of hyper beam
        # - remove energy to avoid hell runs
        # - (will add bosses as well)
        sm.addItems([item.Type for item in emptyContainer.itemPool if item.Type != 'Ice' and item.Category != 'Energy'])
        sm.addItem('Hyper')
        possibleTargets = self._getTargets(sm, graph, maxDiff)
        # pick one
        dst = possibleTargets.pop()
        path = graph.accessPath(sm, dst, 'Landing Site', maxDiff)
        return (possibleTargets, dst, path)

    def escapeTrigger(self, emptyContainer, graph, maxDiff, escapeTrigger):
        container = emptyContainer
        sm = container.sm
        allItemLocs,progItemLocs,split = escapeTrigger[0],escapeTrigger[1],escapeTrigger[2]
        # check if crateria is connected, if not replace Tourian
        # connection with Climb and add special escape patch to Climb
        if not any(il.Location.GraphArea == "Crateria" for il in allItemLocs):
            escapeAttr = graph.EscapeAttributes
            if "patches" not in escapeAttr:
                escapeAttr['patches'] = []
            escapeAttr['patches'] += ['climb_disable_bomb_blocks.ips', "Climb_Asleep"]
            src, _ = next(t for t in graph.InterAreaTransitions if t[1].Name == "Golden Four")
            graph.removeTransitions("Golden Four")
            graph.addTransition(src.Name, "Climb Bottom Left")
            # disconnect the other side of G4
            graph.addTransition("Golden Four", "Golden Four")
        # remove vanilla escape transition
        graph.addTransition('Tourian Escape Room 4 Top Right', 'Tourian Escape Room 4 Top Right')
        # filter garbage itemLocs
        ilCheck = lambda il: not il.Location.isBoss() and not il.Location.restricted and il.Item.Category != "Nothing"
        # update item% objectives
        accessibleItems = [il.Item for il in allItemLocs if ilCheck(il)]
        majorUpgrades = [item.Type for item in accessibleItems if item.BeamBits != 0 or item.ItemBits != 0]
        if split == "Scavenger":
            # update escape access for scav with last scav loc
            lastScavItemLoc = progItemLocs[-1]
            sm.objectives.updateScavengerEscapeAccess(lastScavItemLoc.Location.accessPoint)
            sm.objectives.setScavengerHuntFunc(lambda sm, ap: sm.haveItem(lastScavItemLoc.Item.Type))
        else:
            # update "collect all items in areas" funcs
            availLocsByArea=defaultdict(list)
            for itemLoc in allItemLocs:
                if ilCheck(itemLoc) and (split.startswith("Full") or itemLoc.Location.isClass(split)):
                    availLocsByArea[itemLoc.Location.GraphArea].append(itemLoc.Location.Name)
            self.log.debug("escapeTrigger. availLocsByArea="+str(availLocsByArea))
            sm.objectives.setItemPercentFuncs(len(accessibleItems), majorUpgrades, container)
            sm.objectives.setAreaFuncs({area:lambda sm,ap:SMBool(len(container.getLocs(lambda loc: loc.Name in availLocsByArea[area]))==0) for area in availLocsByArea})
        self.log.debug("escapeTrigger. collect locs until G4 access")
        # collect all item/locations up until we can pass G4 (the escape triggers)
        itemLocs = allItemLocs[:]
        ap = "Landing Site" # dummy value it'll be overwritten at first collection
        while len(itemLocs) > 0 and not (sm.canPassG4() and graph.canAccess(sm, ap, "Landing Site", maxDiff)):
            il = itemLocs.pop(0)
            if il.Location.restricted or il.Item.Type == "ArchipelagoItem":
                continue
            self.log.debug("collecting " + getItemLocStr(il))
            container.collect(il)
            ap = il.Location.accessPoint
        # final update of item% obj
        collectedLocsAccessPoints = {il.Location.accessPoint for il in container.itemLocations}
        sm.objectives.updateItemPercentEscapeAccess(list(collectedLocsAccessPoints))
        possibleTargets = self._getTargets(sm, graph, maxDiff)
        # try to escape from all the possible objectives APs
        possiblePaths = []
        for goal in Objectives.objDict[self.graphSettings.player].activeGoals:
            n, possibleAccessPoints = goal.escapeAccessPoints
            count = 0
            for ap in possibleAccessPoints:
                self.log.debug("escapeTrigger. testing AP " + ap)
                path = graph.accessPath(sm, ap, 'Landing Site', maxDiff)
                if path is not None:
                    self.log.debug("escapeTrigger. add path from "+ap)
                    possiblePaths.append(path)
                    count += 1
            if count < n:
                # there is a goal we cannot escape from
                self.log.debug("escapeTrigger. goal %s: found %d/%d possible escapes, abort" % (goal.name, count, n))
                return (None, None)
        # try and get a path from all possible areas
        self.log.debug("escapeTrigger. completing paths")
        allAreas = {il.Location.GraphArea for il in allItemLocs if not il.Location.restricted and not il.Location.GraphArea in ["Tourian", "Ceres"]}
        def getStartArea(path):
            return path[0].GraphArea
        def apCheck(ap):
            nonlocal graph, possiblePaths
            apObj = graph.accessPoints[ap]
            return apObj.GraphArea not in [getStartArea(path) for path in possiblePaths]
        escapeAPs = [ap for ap in collectedLocsAccessPoints if apCheck(ap)]
        for ap in escapeAPs:
            path = graph.accessPath(sm, ap, 'Landing Site', maxDiff)
            if path is not None:
                self.log.debug("escapeTrigger. add path from "+ap)
                possiblePaths.append(path)
        def areaPathCheck():
            nonlocal allAreas, possiblePaths
            startAreas = {getStartArea(path) for path in possiblePaths}
            return len(allAreas - startAreas) == 0
        while not areaPathCheck() and len(itemLocs) > 0:
            il = itemLocs.pop(0)
            if il.Location.restricted or il.Item.Type == "ArchipelagoItem":
                continue
            self.log.debug("collecting " + getItemLocStr(il))
            container.collect(il)
            ap = il.Location.accessPoint
            if apCheck(ap):
                path = graph.accessPath(sm, ap, 'Landing Site', maxDiff)
                if path is not None:
                    self.log.debug("escapeTrigger. add path from "+ap)
                    possiblePaths.append(path)

        return (possibleTargets, possiblePaths)

    def _computeTimer(self, graph, path):
        traversedAreas = list(set([ap.GraphArea for ap in path]))
        self.log.debug("escapeTimer path: " + str([ap.Name for ap in path]))
        self.log.debug("escapeTimer traversedAreas: " + str(traversedAreas))
        # rough estimates of navigation within areas to reach "borders"
        # (can obviously be completely off wrt to actual path, but on the generous side)
        traversals = {
            'Crateria':90,
            'GreenPinkBrinstar':90,
            'WreckedShip':120,
            'LowerNorfair':135,
            'WestMaridia':75,
            'EastMaridia':100,
            'RedBrinstar':75,
            'Norfair': 120,
            'Kraid': 40,
            'Crocomire': 40,
            # can't be on the path
            'Tourian': 0,
        }
        t = 90 if self.areaRando else 0
        for area in traversedAreas:
            t += traversals[area]
        t = max(t, 180)
        return t


    # path: as returned by AccessGraph.accessPath
    def escapeTimer(self, graph, paths, compute):
        if len(paths) == 1:
            path = paths.pop()
            if compute == True:
                if path[0].Name == 'Climb Bottom Left':
                    graph.EscapeAttributes['Timer'] = None
                    return
                t = self._computeTimer(graph, path)
            else:
                escapeTargetsTimer = {
                    'Climb Bottom Left': None, # vanilla
                    'Green Brinstar Main Shaft Top Left': 210, # brinstar
                    'Basement Left': 210, # wrecked ship
                    'Business Center Mid Left': 270, # norfair
                    'Crab Hole Bottom Right': 270 # maridia
                }
                t = escapeTargetsTimer[path[0].Name]
            self.log.debug("escapeTimer. t="+str(t))
            graph.EscapeAttributes['Timer'] = t
        else:
            assert compute
            graph.EscapeAttributes['Timer'] = 0
            timerValues = {}
            graph.EscapeAttributes['TimerTable'] = timerValues
            for path in paths:
                area = path[0].GraphArea
                prev = timerValues.get(area, 0)
                t = max(prev, self._computeTimer(graph, path))
                timerValues[area] = t
                self.log.debug("escapeTimer. area=%s, t=%d" % (area, t))
            for area in graphAreas[1:-1]:  # no Ceres or Tourian
                if area not in timerValues:
                    # area not in graph most probably, still write a 10 minute "ultra failsafe" value
                    timerValues[area] = 600
