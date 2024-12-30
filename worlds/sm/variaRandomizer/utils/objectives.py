import copy
from ..rom.addresses import Addresses
from ..rom.rom import pc_to_snes
from ..logic.helpers import Bosses
from ..logic.smbool import SMBool
from ..logic.logic import Logic
from ..graph.location import locationsDict
from ..utils.parameters import Knows
from ..utils import log
import logging

LOG = log.get('Objectives')

class Synonyms(object):
    killSynonyms = [
        "defeat",
        "massacre",
        "slay",
        "wipe out",
        "erase",
        "finish",
        "destroy",
        "wreck",
        "smash",
        "crush",
        "end"
    ]
    alreadyUsed = []
    @staticmethod
    def getVerb(random):
        verb = random.choice(Synonyms.killSynonyms)
        while verb in Synonyms.alreadyUsed:
            verb = random.choice(Synonyms.killSynonyms)
        Synonyms.alreadyUsed.append(verb)
        return verb

class Goal(object):
    def __init__(self, name, gtype, logicClearFunc, romClearFunc,
                 escapeAccessPoints=None, objCompletedFuncAPs=lambda ap: [ap],
                 exclusion=None, items=None, text=None, introText=None,
                 available=True, expandableList=None, category=None, area=None,
                 conflictFunc=None):
        self.name = name
        self.available = available
        self.clearFunc = logicClearFunc
        self.objCompletedFuncAPs = objCompletedFuncAPs
        # SNES addr in bank A1, see objectives.asm
        self.checkAddr = pc_to_snes(Addresses.getOne("objective[%s]" % romClearFunc)) & 0xffff
        self.escapeAccessPoints = escapeAccessPoints
        if self.escapeAccessPoints is None:
            self.escapeAccessPoints = (1, [])
        self.rank = -1
        # possible values:
        #  - boss
        #  - miniboss
        #  - other
        self.gtype = gtype
        # example for kill three g4
        # {
        #  "list": [list of objectives],
        #  "type: "boss",
        #  "limit": 2
        # }
        self.exclusion = exclusion
        if self.exclusion is None:
            self.exclusion = {"list": []}
        self.items = items
        if self.items is None:
            self.items = []
        self.text = name if text is None else text
        self.introText = introText
        self.useSynonym = text is not None
        self.expandableList = expandableList
        if self.expandableList is None:
            self.expandableList = []
        self.expandable = len(self.expandableList) > 0
        self.category = category
        self.area = area
        self.conflictFunc = conflictFunc
        # used by solver/isolver to know if a goal has been completed
        self.completed = False

    def setRank(self, rank):
        self.rank = rank

    def canClearGoal(self, smbm, ap=None):
        # not all objectives require an ap (like limit objectives)
        return self.clearFunc(smbm, ap)

    def getText(self, random):
        out = "{}. ".format(self.rank)
        if self.useSynonym:
            out += self.text.format(Synonyms.getVerb(random))
        else:
            out += self.text
        assert len(out) <= 28, "Goal text '{}' is too long: {}, max 28".format(out, len(out))
        if self.introText is not None:
            self.introText = "%d. %s" % (self.rank, self.introText)
        else:
            self.introText = out
        return out

    def getIntroText(self):
        assert self.introText is not None
        return self.introText

    def isLimit(self):
        return "type" in self.exclusion

    def __repr__(self):
        return self.name

def getBossEscapeAccessPoint(boss):
    return (1, [Bosses.accessPoints[boss]])

def getG4EscapeAccessPoints(n):
    return (n, [Bosses.accessPoints[boss] for boss in Bosses.Golden4()])

def getMiniBossesEscapeAccessPoints(n):
    return (n, [Bosses.accessPoints[boss] for boss in Bosses.miniBosses()])

def getAreaEscapeAccessPoints(area):
    return (1, list({list(loc.AccessFrom.keys())[0] for loc in Logic.locations if loc.GraphArea == area}))

_goalsList = [
    Goal("kill kraid", "boss", lambda sm, ap: Bosses.bossDead(sm, 'Kraid'), "kraid_is_dead",
         escapeAccessPoints=getBossEscapeAccessPoint("Kraid"),
         exclusion={"list": ["kill all G4", "kill one G4"]},
         items=["Kraid"],
         text="{} kraid",
         category="Bosses"),
    Goal("kill phantoon", "boss", lambda sm, ap: Bosses.bossDead(sm, 'Phantoon'), "phantoon_is_dead",
         escapeAccessPoints=getBossEscapeAccessPoint("Phantoon"),
         exclusion={"list": ["kill all G4", "kill one G4"]},
         items=["Phantoon"],
         text="{} phantoon",
         category="Bosses"),
    Goal("kill draygon", "boss", lambda sm, ap: Bosses.bossDead(sm, 'Draygon'), "draygon_is_dead",
         escapeAccessPoints=getBossEscapeAccessPoint("Draygon"),
         exclusion={"list": ["kill all G4", "kill one G4"]},
         items=["Draygon"],
         text="{} draygon",
         category="Bosses"),
    Goal("kill ridley", "boss", lambda sm, ap: Bosses.bossDead(sm, 'Ridley'), "ridley_is_dead",
         escapeAccessPoints=getBossEscapeAccessPoint("Ridley"),
         exclusion={"list": ["kill all G4", "kill one G4"]},
         items=["Ridley"],
         text="{} ridley",
         category="Bosses"),
    Goal("kill one G4", "other", lambda sm, ap: Bosses.xBossesDead(sm, 1), "boss_1_killed",
         escapeAccessPoints=getG4EscapeAccessPoints(1),
         exclusion={"list": ["kill kraid", "kill phantoon", "kill draygon", "kill ridley",
                             "kill all G4", "kill two G4", "kill three G4"],
                    "type": "boss",
                    "limit": 0},
         text="{} one golden4",
         category="Bosses"),
    Goal("kill two G4", "other", lambda sm, ap: Bosses.xBossesDead(sm, 2), "boss_2_killed",
         escapeAccessPoints=getG4EscapeAccessPoints(2),
         exclusion={"list": ["kill all G4", "kill one G4", "kill three G4"],
                    "type": "boss",
                    "limit": 1},
         text="{} two golden4",
         category="Bosses"),
    Goal("kill three G4", "other", lambda sm, ap: Bosses.xBossesDead(sm, 3), "boss_3_killed",
         escapeAccessPoints=getG4EscapeAccessPoints(3),
         exclusion={"list": ["kill all G4", "kill one G4", "kill two G4"],
                    "type": "boss",
                    "limit": 2},
         text="{} three golden4",
         category="Bosses"),
    Goal("kill all G4", "other", lambda sm, ap: Bosses.allBossesDead(sm), "all_g4_dead",
         escapeAccessPoints=getG4EscapeAccessPoints(4),
         exclusion={"list": ["kill kraid", "kill phantoon", "kill draygon", "kill ridley", "kill one G4", "kill two G4", "kill three G4"]},
         items=["Kraid", "Phantoon", "Draygon", "Ridley"],
         text="{} all golden4",
         expandableList=["kill kraid", "kill phantoon", "kill draygon", "kill ridley"],
         category="Bosses"),
    Goal("kill spore spawn", "miniboss", lambda sm, ap: Bosses.bossDead(sm, 'SporeSpawn'), "spore_spawn_is_dead",
         escapeAccessPoints=getBossEscapeAccessPoint("SporeSpawn"),
         exclusion={"list": ["kill all mini bosses", "kill one miniboss"]},
         items=["SporeSpawn"],
         text="{} spore spawn",
         category="Minibosses"),
    Goal("kill botwoon", "miniboss", lambda sm, ap: Bosses.bossDead(sm, 'Botwoon'), "botwoon_is_dead",
         escapeAccessPoints=getBossEscapeAccessPoint("Botwoon"),
         exclusion={"list": ["kill all mini bosses", "kill one miniboss"]},
         items=["Botwoon"],
         text="{} botwoon",
         category="Minibosses"),
    Goal("kill crocomire", "miniboss", lambda sm, ap: Bosses.bossDead(sm, 'Crocomire'), "crocomire_is_dead",
         escapeAccessPoints=getBossEscapeAccessPoint("Crocomire"),
         exclusion={"list": ["kill all mini bosses", "kill one miniboss"]},
         items=["Crocomire"],
         text="{} crocomire",
         category="Minibosses"),
    Goal("kill golden torizo", "miniboss", lambda sm, ap: Bosses.bossDead(sm, 'GoldenTorizo'), "golden_torizo_is_dead",
         escapeAccessPoints=getBossEscapeAccessPoint("GoldenTorizo"),
         exclusion={"list": ["kill all mini bosses", "kill one miniboss"]},
         items=["GoldenTorizo"],
         text="{} golden torizo",
         category="Minibosses",
         conflictFunc=lambda settings, player: settings.qty['energy'] == 'ultra sparse' and (not Knows.knowsDict[player].LowStuffGT or (Knows.knowsDict[player].LowStuffGT.difficulty > settings.maxDiff))),
    Goal("kill one miniboss", "other", lambda sm, ap: Bosses.xMiniBossesDead(sm, 1), "miniboss_1_killed",
         escapeAccessPoints=getMiniBossesEscapeAccessPoints(1),
         exclusion={"list": ["kill spore spawn", "kill botwoon", "kill crocomire", "kill golden torizo",
                             "kill all mini bosses", "kill two minibosses", "kill three minibosses"],
                    "type": "miniboss",
                    "limit": 0},
         text="{} one miniboss",
         category="Minibosses"),
    Goal("kill two minibosses", "other", lambda sm, ap: Bosses.xMiniBossesDead(sm, 2), "miniboss_2_killed",
         escapeAccessPoints=getMiniBossesEscapeAccessPoints(2),
         exclusion={"list": ["kill all mini bosses", "kill one miniboss", "kill three minibosses"],
                    "type": "miniboss",
                    "limit": 1},
         text="{} two minibosses",
         category="Minibosses"),
    Goal("kill three minibosses", "other", lambda sm, ap: Bosses.xMiniBossesDead(sm, 3), "miniboss_3_killed",
         escapeAccessPoints=getMiniBossesEscapeAccessPoints(3),
         exclusion={"list": ["kill all mini bosses", "kill one miniboss", "kill two minibosses"],
                    "type": "miniboss",
                    "limit": 2},
         text="{} three minibosses",
         category="Minibosses"),
    Goal("kill all mini bosses", "other", lambda sm, ap: Bosses.allMiniBossesDead(sm), "all_mini_bosses_dead",
         escapeAccessPoints=getMiniBossesEscapeAccessPoints(4),
         exclusion={"list": ["kill spore spawn", "kill botwoon", "kill crocomire", "kill golden torizo",
                             "kill one miniboss", "kill two minibosses", "kill three minibosses"]},
         items=["SporeSpawn", "Botwoon", "Crocomire", "GoldenTorizo"],
         text="{} all mini bosses",
         expandableList=["kill spore spawn", "kill botwoon", "kill crocomire", "kill golden torizo"],
         category="Minibosses",
         conflictFunc=lambda settings, player: settings.qty['energy'] == 'ultra sparse' and (not Knows.knowsDict[player].LowStuffGT or (Knows.knowsDict[player].LowStuffGT.difficulty > settings.maxDiff))),
    # not available in AP
    #Goal("finish scavenger hunt", "other", lambda sm, ap: SMBool(True), "scavenger_hunt_completed",
    #     exclusion={"list": []}, # will be auto-completed
    #     available=False),
    Goal("nothing", "other", lambda sm, ap: Objectives.objDict[sm.player].canAccess(sm, ap, "Landing Site"), "nothing_objective",
         escapeAccessPoints=(1, ["Landing Site"])), # with no objectives at all, escape auto triggers only in crateria
    Goal("collect 25% items", "items", lambda sm, ap: SMBool(True), "collect_25_items",
         exclusion={"list": ["collect 50% items", "collect 75% items", "collect 100% items"]},
         category="Items",
         introText="collect 25 percent of items"),
    Goal("collect 50% items", "items", lambda sm, ap: SMBool(True), "collect_50_items",
         exclusion={"list": ["collect 25% items", "collect 75% items", "collect 100% items"]},
         category="Items",
         introText="collect 50 percent of items"),
    Goal("collect 75% items", "items", lambda sm, ap: SMBool(True), "collect_75_items",
         exclusion={"list": ["collect 25% items", "collect 50% items", "collect 100% items"]},
         category="Items",
         introText="collect 75 percent of items"),
    Goal("collect 100% items", "items", lambda sm, ap: SMBool(True), "collect_100_items",
         exclusion={"list": ["collect 25% items", "collect 50% items", "collect 75% items", "collect all upgrades"]},
         category="Items",
         introText="collect all items"),
    Goal("collect all upgrades", "items", lambda sm, ap: SMBool(True), "all_major_items",
         category="Items"),
    Goal("clear crateria", "items", lambda sm, ap: SMBool(True), "crateria_cleared",
         category="Items",
         area="Crateria"),
    Goal("clear green brinstar", "items", lambda sm, ap: SMBool(True), "green_brin_cleared",
         category="Items",
         area="GreenPinkBrinstar"),
    Goal("clear red brinstar", "items", lambda sm, ap: SMBool(True), "red_brin_cleared",
         category="Items",
         area="RedBrinstar"),
    Goal("clear wrecked ship", "items", lambda sm, ap: SMBool(True), "ws_cleared",
         category="Items",
         area="WreckedShip"),
    Goal("clear kraid's lair", "items", lambda sm, ap: SMBool(True), "kraid_cleared",
         category="Items",
         area="Kraid"),
    Goal("clear upper norfair", "items", lambda sm, ap: SMBool(True), "upper_norfair_cleared",
         category="Items",
         area="Norfair"),
    Goal("clear croc's lair", "items", lambda sm, ap: SMBool(True), "croc_cleared",
         category="Items",
         area="Crocomire"),
    Goal("clear lower norfair", "items", lambda sm, ap: SMBool(True), "lower_norfair_cleared",
         category="Items",
         area="LowerNorfair"),
    Goal("clear west maridia", "items", lambda sm, ap: SMBool(True), "west_maridia_cleared",
         category="Items",
         area="WestMaridia"),
    Goal("clear east maridia", "items", lambda sm, ap: SMBool(True), "east_maridia_cleared",
         category="Items",
         area="EastMaridia"),
    Goal("tickle the red fish", "other",
         lambda sm, ap: sm.wand(sm.haveItem('Grapple'), Objectives.objDict[sm.player].canAccess(sm, ap, "Red Fish Room Bottom")),
         "fish_tickled",
         escapeAccessPoints=(1, ["Red Fish Room Bottom"]),
         objCompletedFuncAPs=lambda ap: ["Red Fish Room Bottom"],
         category="Memes"),
    Goal("kill the orange geemer", "other",
         lambda sm, ap: sm.wand(Objectives.objDict[sm.player].canAccess(sm, ap, "Bowling"), # XXX this unnecessarily adds canPassBowling as requirement
                                sm.wor(sm.haveItem('Wave'), sm.canUsePowerBombs())),
         "orange_geemer",
         escapeAccessPoints=(1, ["Bowling"]),
         objCompletedFuncAPs=lambda ap: ["Bowling"],
         text="{} orange geemer",
         category="Memes"),
    Goal("kill shaktool", "other",
         lambda sm, ap: sm.wand(Objectives.objDict[sm.player].canAccess(sm, ap, "Oasis Bottom"),
                                sm.canTraverseSandPits(),
                                sm.canAccessShaktoolFromPantsRoom()),
         "shak_dead",
         escapeAccessPoints=(1, ["Oasis Bottom"]),
         objCompletedFuncAPs=lambda ap: ["Oasis Bottom"],
         text="{} shaktool",
         category="Memes"),
    Goal("activate chozo robots", "other", lambda sm, ap: sm.wand(Objectives.objDict[sm.player].canAccessLocation(sm, ap, "Bomb"),
                                                                  Objectives.objDict[sm.player].canAccessLocation(sm, ap, "Gravity Suit"),
                                                                  sm.haveItem("GoldenTorizo"),
                                                                  sm.canPassLowerNorfairChozo()), # graph access implied by GT loc
         "all_chozo_robots",
         category="Memes",
         escapeAccessPoints=(3, ["Landing Site", "Screw Attack Bottom", "Bowling"]),
         objCompletedFuncAPs=lambda ap: ["Landing Site", "Screw Attack Bottom", "Bowling"],
         exclusion={"list": ["kill golden torizo"]},
         conflictFunc=lambda settings, player: settings.qty['energy'] == 'ultra sparse' and (not Knows.knowsDict[player].LowStuffGT or (Knows.knowsDict[player].LowStuffGT.difficulty > settings.maxDiff))),
    Goal("visit the animals", "other", lambda sm, ap: sm.wand(Objectives.objDict[sm.player].canAccess(sm, ap, "Big Pink"), sm.haveItem("SpeedBooster"), # dachora
                                                              Objectives.objDict[sm.player].canAccess(sm, ap, "Etecoons Bottom")), # Etecoons
         "visited_animals",
         category="Memes",
         escapeAccessPoints=(2, ["Big Pink", "Etecoons Bottom"]),
         objCompletedFuncAPs=lambda ap: ["Big Pink", "Etecoons Bottom"]),
    Goal("kill king cacatac", "other",
         lambda sm, ap: Objectives.objDict[sm.player].canAccess(sm, ap, 'Bubble Mountain Top'),
         "king_cac_dead",
         category="Memes",
         escapeAccessPoints=(1, ['Bubble Mountain Top']),
         objCompletedFuncAPs=lambda ap: ['Bubble Mountain Top'])
]


_goals = {goal.name:goal for goal in _goalsList}

def completeGoalData():
    # "nothing" is incompatible with everything
    _goals["nothing"].exclusion["list"] = [goal.name for goal in _goalsList]
    areaGoals = [goal.name for goal in _goalsList if goal.area is not None]
    # if we need 100% items, don't require "clear area", as it covers those
    _goals["collect 100% items"].exclusion["list"] += areaGoals[:]
    # if we have scav hunt, don't require "clear area" (HUD behaviour incompatibility)
    # not available in AP
    #_goals["finish scavenger hunt"].exclusion["list"] += areaGoals[:]
    # remove clear area goals if disabled tourian, as escape can trigger as soon as an area is cleared,
    # even if ship is not currently reachable
    for goal in areaGoals:
        _goals[goal].exclusion['tourian'] = "Disabled"

completeGoalData()

class Objectives(object):
    maxActiveGoals = 5
    vanillaGoals = ["kill kraid", "kill phantoon", "kill draygon", "kill ridley"]
    scavHuntGoal = ["finish scavenger hunt"]
    objDict = {}

    def __init__(self, player=0, tourianRequired=True, randoSettings=None):
        self.player = player
        self.activeGoals = []
        self.nbActiveGoals = 0
        self.totalItemsCount = 100
        self.goals = copy.deepcopy(_goals)
        self.graph = None
        self._tourianRequired = tourianRequired
        self.randoSettings = randoSettings
        Objectives.objDict[player] = self

    @property
    def tourianRequired(self):
        assert self._tourianRequired is not None
        return self._tourianRequired

    def resetGoals(self):
        self.activeGoals = []
        self.nbActiveGoals = 0

    def conflict(self, newGoal):
        if newGoal.exclusion.get('tourian') == "Disabled" and self.tourianRequired == False:
            LOG.debug("new goal %s conflicts with disabled Tourian" % newGoal.name)
            return True
        LOG.debug("check if new goal {} conflicts with existing active goals".format(newGoal.name))
        count = 0
        for goal in self.activeGoals:
            if newGoal.name in goal.exclusion["list"]:
                LOG.debug("new goal {} in exclusion list of active goal {}".format(newGoal.name, goal.name))
                return True
            if goal.name in newGoal.exclusion["list"]:
                LOG.debug("active goal {} in exclusion list of new goal {}".format(goal.name, newGoal.name))
                return True
            # count bosses/minibosses already active if new goal has a limit
            if newGoal.exclusion.get("type") == goal.gtype:
                count += 1
                LOG.debug("new goal limit type: {} same as active goal {}. count: {}".format(newGoal.exclusion["type"], goal.name, count))
        if count > newGoal.exclusion.get("limit", 0):
            LOG.debug("new goal {} limit {} is lower than active goals of type: {}".format(newGoal.name, newGoal.exclusion["limit"], newGoal.exclusion["type"]))
            return True
        LOG.debug("no direct conflict detected for new goal {}".format(newGoal.name))

        # if at least one active goal has a limit and new goal has the same type of one of the existing limit
        # check that new goal doesn't exceed the limit
        for goal in self.activeGoals:
            goalExclusionType = goal.exclusion.get("type")
            if goalExclusionType is not None and goalExclusionType == newGoal.gtype:
                count = 0
                for lgoal in self.activeGoals:
                    if lgoal.gtype == newGoal.gtype:
                        count += 1
                # add new goal to the count
                if count >= goal.exclusion["limit"]:
                    LOG.debug("new Goal {} would excess limit {} of active goal {}".format(newGoal.name, goal.exclusion["limit"], goal.name))
                    return True

        LOG.debug("no backward conflict detected for new goal {}".format(newGoal.name))

        if self.randoSettings is not None and newGoal.conflictFunc is not None:
            if newGoal.conflictFunc(self.randoSettings, self.player):
                LOG.debug("new Goal {} is conflicting with rando settings".format(newGoal.name))
                return True
            LOG.debug("no conflict with rando settings detected for new goal {}".format(newGoal.name))

        return False

    def addGoal(self, goalName, completed=False):
        LOG.debug("addGoal: {}".format(goalName))
        goal = self.goals[goalName]
        if self.conflict(goal):
            return
        self.nbActiveGoals += 1
        assert self.nbActiveGoals <= self.maxActiveGoals, "Too many active goals"
        goal.setRank(self.nbActiveGoals)
        goal.completed = completed
        self.activeGoals.append(goal)

    def removeGoal(self, goal):
        self.nbActiveGoals -= 1
        self.activeGoals.remove(goal)

    def clearGoals(self):
        self.nbActiveGoals = 0
        self.activeGoals.clear()

    def isGoalActive(self, goalName):
        return self.goals[goalName] in self.activeGoals

    # having graph as a global sucks but Objectives instances are all over the place,
    # goals must access it, and it doesn't change often
    def setGraph(self, graph, maxDiff):
        self.graph = graph
        self.maxDiff = maxDiff
        for goalName, goal in self.goals.items():
            if goal.area is not None:
                goal.escapeAccessPoints = getAreaEscapeAccessPoints(goal.area)

    def canAccess(self, sm, src, dst):
        return SMBool(self.graph.canAccess(sm, src, dst, self.maxDiff))

    def canAccessLocation(self, sm, ap, locName):
        loc = locationsDict[locName]
        availLocs = self.graph.getAvailableLocations([loc], sm, self.maxDiff, ap)
        return SMBool(loc in availLocs)

    def setVanilla(self):
        for goal in self.vanillaGoals:
            self.addGoal(goal)

    def isVanilla(self):
        # kill G4 and/or scav hunt
        if len(self.activeGoals) == 1:
            for goal in self.activeGoals:
                if goal.name not in self.scavHuntGoal:
                    return False
            return True
        elif len(self.activeGoals) == 4:
            for goal in self.activeGoals:
                if goal.name not in self.vanillaGoals:
                    return False
            return True
        elif len(self.activeGoals) == 5:
            for goal in self.activeGoals:
                if goal.name not in self.vanillaGoals + self.scavHuntGoal:
                    return False
            return True
        else:
            return False

    def setScavengerHunt(self):
        self.addGoal("finish scavenger hunt")

    def updateScavengerEscapeAccess(self, ap):
        assert self.isGoalActive("finish scavenger hunt")
        (_, apList) = self.goals['finish scavenger hunt'].escapeAccessPoints
        apList.append(ap)

    def _replaceEscapeAccessPoints(self, goal, aps):
        (_, apList) = self.goals[goal].escapeAccessPoints
        apList.clear()
        apList += aps

    def updateItemPercentEscapeAccess(self, collectedLocsAccessPoints):
        for pct in [25,50,75,100]:
            goal = 'collect %d%% items' % pct
            self._replaceEscapeAccessPoints(goal, collectedLocsAccessPoints)
        # not exactly accurate, but player has all upgrades to escape
        self._replaceEscapeAccessPoints("collect all upgrades", collectedLocsAccessPoints)

    def setScavengerHuntFunc(self, scavClearFunc):
        self.goals["finish scavenger hunt"].clearFunc = scavClearFunc

    def setItemPercentFuncs(self, totalItemsCount=None, allUpgradeTypes=None, container=None):
        def getPctFunc(total_needed, container):
            def f(sm, ap):
                nonlocal total_needed, container
                locs_checked = len(container.getUsedLocs(lambda loc: True))
                return SMBool(locs_checked >= total_needed)
            return f

        # AP: now based on location checks instead of local item
        for pct in [25,50,75,100]:
            goal = 'collect %d%% items' % pct
            self.goals[goal].clearFunc = getPctFunc(totalItemsCount * pct / 100, container)
        if allUpgradeTypes is not None:
            self.goals["collect all upgrades"].clearFunc = lambda sm, ap: sm.haveItems(allUpgradeTypes)

    def setAreaFuncs(self, funcsByArea):
        goalsByArea = {goal.area:goal for goalName, goal in self.goals.items()}
        for area, func in funcsByArea.items():
            if area in goalsByArea:
                goalsByArea[area].clearFunc = func

    def setSolverMode(self, solver):
        self.setScavengerHuntFunc(solver.scavengerHuntComplete)
        # in rando we know the number of items after randomizing, so set the functions only for the solver
        self.setItemPercentFuncs(allUpgradeTypes=solver.majorUpgrades)

        def getObjAreaFunc(area):
            def f(sm, ap):
                nonlocal solver, area
                visitedLocs = set([loc.Name for loc in solver.visitedLocations])
                return SMBool(all(locName in visitedLocs for locName in solver.splitLocsByArea[area]))
            return f
        self.setAreaFuncs({area:getObjAreaFunc(area) for area in solver.splitLocsByArea})

    def expandGoals(self):
        LOG.debug("Active goals:"+str(self.activeGoals))
        # try to replace 'kill all G4' with the four associated objectives.
        # we need at least 3 empty objectives out of the max (-1 +4)
        if self.maxActiveGoals - self.nbActiveGoals < 3:
            return

        expandable = None
        for goal in self.activeGoals:
            if goal.expandable:
                expandable = goal
                break

        if expandable is None:
            return

        LOG.debug("replace {} with {}".format(expandable.name, expandable.expandableList))
        self.removeGoal(expandable)
        for name in expandable.expandableList:
            self.addGoal(name)

        # rebuild ranks
        for i, goal in enumerate(self.activeGoals, 1):
            goal.rank = i

    # call from logic
    def canClearGoals(self, smbm, ap):
        result = SMBool(True)
        for goal in self.activeGoals:
            result = smbm.wand(result, goal.canClearGoal(smbm, ap))
        return result

    # call from solver
    def checkGoals(self, smbm, ap):
        ret = {}

        for goal in self.activeGoals:
            if goal.completed is True:
                continue
            # check if goal can be completed
            ret[goal.name] = goal.canClearGoal(smbm, ap)

        return ret

    def setGoalCompleted(self, goalName, completed):
        for goal in self.activeGoals:
            if goal.name == goalName:
                goal.completed = completed
                return
        assert False, "Can't set goal {} completion to {}, goal not active".format(goalName, completed)

    def allGoalsCompleted(self):
        for goal in self.activeGoals:
            if goal.completed is False:
                return False
        return True

    def getGoalFromCheckFunction(self, checkFunction):
        for name, goal in self.goals.items():
            if goal.checkAddr == checkFunction:
                return goal
        assert True, "Goal with check function {} not found".format(hex(checkFunction))

    def getTotalItemsCount(self):
        return self.totalItemsCount

    # call from web
    def getAddressesToRead(self):
        terminator = 1
        objectiveSize = 2
        bytesToRead = (self.maxActiveGoals + terminator) * objectiveSize
        return [Addresses.getOne('objectivesList')+i for i in range(0, bytesToRead+1)] + Addresses.getWeb('totalItems') + Addresses.getWeb("itemsMask") + Addresses.getWeb("beamsMask")

    def getExclusions(self):
        # to compute exclusions in the front end
        return {goalName: goal.exclusion for goalName, goal in self.goals.items()}

    def getObjectivesTypes(self):
        # to compute exclusions in the front end
        types = {'boss': [], 'miniboss': []}
        for goalName, goal in self.goals.items():
            if goal.gtype in types:
                types[goal.gtype].append(goalName)
        return types

    def getObjectivesSort(self):
        return list(self.goals.keys())

    def getObjectivesCategories(self):
        return {goal.name: goal.category for goal in self.goals.values() if goal.category is not None}

    # call from rando check pool and solver

    def getMandatoryBosses(self):
        r = [goal.items for goal in self.activeGoals]
        return [item for items in r for item in items]

    def checkLimitObjectives(self, beatableBosses):
        # check that there's enough bosses/minibosses for limit objectives
        from ..logic.smboolmanager import SMBoolManager
        smbm = SMBoolManager(self.player)
        smbm.addItems(beatableBosses)
        for goal in self.activeGoals:
            if not goal.isLimit():
                continue
            if not goal.canClearGoal(smbm):
                return False
        return True

    # call from solver
    def getGoalsList(self):
        return [goal.name for goal in self.activeGoals]

    # call from interactivesolver
    def getState(self):
        return {goal.name: goal.completed for goal in self.activeGoals}

    def setState(self, state):
        for goalName, completed in state.items():
            self.addGoal(goalName, completed)

    def resetGoals(self):
        for goal in self.activeGoals:
            goal.completed = False

    # call from rando
    @staticmethod
    def getAllGoals(removeNothing=False):
        return [goal.name for goal in _goals.values() if goal.available and (not removeNothing or goal.name != "nothing")]

    # call from rando
    def setRandom(self, nbGoals, availableGoals, random):
        while self.nbActiveGoals < nbGoals and availableGoals:
            goalName = random.choice(availableGoals)
            self.addGoal(goalName)
            availableGoals.remove(goalName)

    # call from solver
    def readGoals(self, romReader):
        self.resetGoals()
        romReader.romFile.seek(Addresses.getOne('objectivesList'))
        checkFunction = romReader.romFile.readWord()
        while checkFunction != 0x0000:
            goal = self.getGoalFromCheckFunction(checkFunction)
            self.activeGoals.append(goal)
            checkFunction = romReader.romFile.readWord()

        # read number of available items for items % objectives
        self.totalItemsCount = romReader.romFile.readByte(Addresses.getOne('totalItems'))

        for goal in self.activeGoals:
            LOG.debug("active goal: {}".format(goal.name))

        self._tourianRequired = not romReader.patchPresent('Escape_Trigger')
        LOG.debug("tourianRequired: {}".format(self.tourianRequired))

    # call from rando
    def writeGoals(self, romFile, random):
        # write check functions
        romFile.seek(Addresses.getOne('objectivesList'))
        for goal in self.activeGoals:
            romFile.writeWord(goal.checkAddr)
        # list terminator
        romFile.writeWord(0x0000)

        # compute chars
        char2tile = {
            '.': 0x4A,
            '?': 0x4B,
            '!': 0x4C,
            ' ': 0x00,
            '%': 0x02,
            '*': 0x03,
            '0': 0x04,
            'a': 0x30,
        }
        for i in range(1, ord('z')-ord('a')+1):
            char2tile[chr(ord('a')+i)] = char2tile['a']+i
        for i in range(1, ord('9')-ord('0')+1):
            char2tile[chr(ord('0')+i)] = char2tile['0']+i

        # write text
        tileSize = 2
        lineLength = 32 * tileSize
        firstChar = 3 * tileSize
        # start at 8th line
        baseAddr = Addresses.getOne('objectivesText') + lineLength * 8 + firstChar
        # space between two lines of text
        space = 3 if self.nbActiveGoals == 5 else 4
        for i, goal in enumerate(self.activeGoals):
            addr = baseAddr + i * lineLength * space
            text = goal.getText(random)
            romFile.seek(addr)
            for c in text:
                if c not in char2tile:
                    continue
                romFile.writeWord(0x3800 + char2tile[c])
        Synonyms.alreadyUsed = []
        # write goal completed positions y in sprites OAM
        baseY = 0x40
        addr = Addresses.getOne('objectivesSpritesOAM')
        spritemapSize = 5 + 2
        for i, goal in enumerate(self.activeGoals):
            y = baseY + i * space * 8
            # sprite center is at 128
            y = (y - 128) & 0xFF
            romFile.writeByte(y, addr+4 + i*spritemapSize)

    def writeIntroObjectives(self, rom, tourian):
        if self.isVanilla() and tourian == "Vanilla":
            return
        # objectives or tourian are not vanilla, prepare intro text
        # two \n for an actual newline
        text = "MISSION OBJECTIVES\n"
        for goal in self.activeGoals:
            text += "\n\n%s" % goal.getIntroText()
        text += "\n\n\nTOURIAN IS %s\n\n\n" % tourian
        text += "CHECK OBJECTIVES STATUS IN\n\n"
        text += "THE PAUSE SCREEN"
        # actually write text in ROM
        self._writeIntroText(rom, text.upper())

    def _writeIntroText(self, rom, text, startX=1, startY=2):
        # for character translation
        charCodes = {
            ' ': 0xD67D,
            '.': 0xD75D,
            '!': 0xD77B,
            "'": 0xD76F,
            '0': 0xD721,
            'A': 0xD685
        }
        def addCharRange(start, end, base): # inclusive range
            for c in range(ord(start), ord(end)+1):
                offset = c - ord(base)
                charCodes[chr(c)] = charCodes[base]+offset*6
        addCharRange('B', 'Z', 'A')
        addCharRange('1', '9', '0')
        # actually write chars
        x, y = startX, startY
        def writeChar(c, frameDelay=2):
            nonlocal rom, x, y
            assert x <= 0x1F and y <= 0x18, "Intro text formatting error (x=0x%x, y=0x%x):\n%s" % (x, y, text)
            if c == '\n':
                x = startX
                y += 1
            else:
                assert c in charCodes, "Invalid intro char "+c
                rom.writeWord(frameDelay)
                rom.writeByte(x)
                rom.writeByte(y)
                rom.writeWord(charCodes[c])
                x += 1
        rom.seek(Addresses.getOne('introText'))
        for c in text:
            writeChar(c)
        # write trailer, see intro_text.asm
        rom.writeWord(0xAE5B)
        rom.writeWord(0x9698)
