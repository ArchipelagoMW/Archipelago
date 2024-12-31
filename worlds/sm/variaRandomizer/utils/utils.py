import io
import os, json, re, random
import pathlib
import sys
from typing import Any
import zipfile

from ..utils.parameters import Knows, Settings, Controller, isKnows, isSettings, isButton
from ..utils.parameters import easy, medium, hard, harder, hardcore, mania, text2diff
from ..logic.smbool import SMBool


# support for AP world
isAPWorld = ".apworld" in sys.modules[__name__].__file__

def getZipFile():
    filename = sys.modules[__name__].__file__
    apworldExt = ".apworld"
    zipPath = pathlib.Path(filename[:filename.index(apworldExt) + len(apworldExt)])    
    return (zipfile.ZipFile(zipPath), zipPath.stem)

def openFile(resource: str, mode: str = "r", encoding: None = None):
    if isAPWorld:
        (zipFile, stem) = getZipFile()
        with zipFile as zf:
            zipFilePath = resource[resource.index(stem + "/"):]
            if mode == 'rb':
                return zf.open(zipFilePath, 'r')
            else:
                return io.TextIOWrapper(zf.open(zipFilePath, mode), encoding)
    else:
        return open(resource, mode)
    
def listDir(resource: str):
    if isAPWorld:
        (zipFile, stem) = getZipFile()
        with zipFile as zf:
            zipFilePath = resource[resource.index(stem + "/"):]
            path = zipfile.Path(zf, zipFilePath + "/")
            files = [f.at[len(zipFilePath)+1:] for f in path.iterdir()]
            return files
    else:
        return os.listdir(resource)    
    
def exists(resource: str):
    if isAPWorld:
        (zipFile, stem) = getZipFile()
        with zipFile as zf:
            if (stem in resource):
                zipFilePath = resource[resource.index(stem + "/"):]
                path = zipfile.Path(zf, zipFilePath)
                return path.exists()
            else:
                return False
    else:
        return os.path.exists(resource)   

def isStdPreset(preset):
    return preset in ['newbie', 'casual', 'regular', 'veteran', 'expert', 'master', 'samus', 'solution', 'Season_Races', 'SMRAT2021', 'Torneio_SGPT3']

def getPresetDir(preset) -> str:
    if isStdPreset(preset):
        return 'worlds/sm/variaRandomizer/standard_presets'
    else:
        return 'worlds/sm/variaRandomizer/community_presets'

def removeChars(string, toRemove):
    return re.sub('[{}]+'.format(toRemove), '', string)

def range_union(ranges):
    ret = []
    for rg in sorted([[r.start, r.stop] for r in ranges]):
        begin, end = rg[0], rg[-1]
        if ret and ret[-1][1] > begin:
            ret[-1][1] = max(ret[-1][1], end)
        else:
            ret.append([begin, end])
    return [range(r[0], r[1]) for r in ret]

# https://github.com/robotools/fontParts/commit/7cb561033929cfb4a723d274672e7257f5e68237
def normalizeRounding(n):
    # Normalizes rounding as Python 2 and Python 3 handing the rounding of halves (0.5, 1.5, etc) differently.
    # This normalizes rounding to be the same in both environments.
    if round(0.5) != 1 and n % 1 == .5 and not int(n) % 2:
        return int((round(n) + (abs(n) / n) * 1))
    else:
        return int(round(n))

# gauss random in [0, r] range
# the higher the slope, the less probable extreme values are.
def randGaussBounds(r, slope=5):
    r = float(r)
    n = normalizeRounding(random.gauss(r/2, r/slope))
    if n < 0:
        n = 0
    if n > r:
        n = int(r)
    return n

# from a relative weight dictionary, gives a normalized range dictionary
# example :
# { 'a' : 10, 'b' : 17, 'c' : 3 } => {'c': 0.1, 'a':0.4333333, 'b':1 }
def getRangeDict(weightDict):
    total = float(sum(weightDict.values()))
    rangeDict = {}
    current = 0.0
    for k in sorted(weightDict, key=weightDict.get):
        w = float(weightDict[k]) / total
        current += w
        rangeDict[k] = current

    return rangeDict

def chooseFromRange(rangeDict):
    r = random.random()
    val = None
    for v in sorted(rangeDict, key=rangeDict.get):
        val = v
        if r < rangeDict[v]:
            return v
    return val

class PresetLoader(object):
    @staticmethod
    def factory(params):
        # can be a json, a python file or a dict with the parameters
        if type(params) == str:
            ext = os.path.splitext(params)
            if ext[1].lower() == '.json':
                return PresetLoaderJson(params)
            else:
                raise Exception("PresetLoader: wrong parameters file type: {}".format(ext[1]))
        elif type(params) is dict:
            return PresetLoaderDict(params)
        else:
            raise Exception("wrong parameters input, is neither a string nor a json file name: {}::{}".format(params, type(params)))

    def __init__(self):
        if 'Knows' not in self.params:
            if 'knows' in self.params:     
                self.params['Knows'] = self.params['knows']
            else:
                self.params['Knows'] = {}
        if 'Settings' not in self.params:
            if 'settings' in self.params:     
                self.params['Settings'] = self.params['settings']
            else:
                self.params['Settings'] = {}
        if 'Controller' not in self.params:
            if 'controller' in self.params:     
                self.params['Controller'] = self.params['controller']
            else:
                self.params['Controller'] = {}
        self.params['score'] = self.computeScore()

    def load(self, player):
        # update the parameters in the parameters classes: Knows, Settings
        Knows.knowsDict[player] = Knows()
        Settings.SettingsDict[player] = Settings()
        Controller.ControllerDict[player] = Controller()

        # Knows
        for param in self.params['Knows']:
            if isKnows(param) and hasattr(Knows, param):
                setattr(Knows.knowsDict[player], param, SMBool(  self.params['Knows'][param][0],
                                                    self.params['Knows'][param][1],
                                                    ['{}'.format(param)]))
        # Settings
        ## hard rooms
        for hardRoom in ['X-Ray', 'Gauntlet']:
            if hardRoom in self.params['Settings']:
                Settings.SettingsDict[player].hardRooms[hardRoom] = Settings.hardRoomsPresets[hardRoom][self.params['Settings'][hardRoom]]

        ## bosses
        for boss in ['Kraid', 'Phantoon', 'Draygon', 'Ridley', 'MotherBrain']:
            if boss in self.params['Settings']:
                Settings.SettingsDict[player].bossesDifficulty[boss] = Settings.bossesDifficultyPresets[boss][self.params['Settings'][boss]]

        ## hellruns
        for hellRun in ['Ice', 'MainUpperNorfair', 'LowerNorfair']:
            if hellRun in self.params['Settings']:
                Settings.SettingsDict[player].hellRuns[hellRun] = Settings.hellRunPresets[hellRun][self.params['Settings'][hellRun]]

        # Controller
        for button in self.params['Controller']:
            if isButton(button):
                setattr(Controller.ControllerDict[player], button, self.params['Controller'][button])

    def dump(self, fileName):
        with open(fileName, 'w') as jsonFile:
            json.dump(self.params, jsonFile)

    def printToScreen(self):
        print("self.params: {}".format(self.params))

        print("loaded knows: ")
        for knows in Knows.__dict__:
            if isKnows(knows):
                print("{}: {}".format(knows, Knows.__dict__[knows]))
        print("loaded settings:")
        for setting in Settings.__dict__:
            if isSettings(setting):
                print("{}: {}".format(setting, Settings.__dict__[setting]))
        print("loaded controller:")
        for button in Controller.__dict__:
            if isButton(button):
                print("{}: {}".format(button, Controller.__dict__[button]))
        print("loaded score: {}".format(self.params['score']))

    def computeScore(self):
        # the more techniques you know and the smaller the difficulty of the techniques, the higher the score
        diff2score = {
            easy: 6,
            medium: 5,
            hard: 4,
            harder: 3,
            hardcore: 2,
            mania: 1
        }

        boss2score = {
            "He's annoying": 1,
            'A lot of trouble': 1,
            "I'm scared!": 1,
            "It can get ugly": 1,
            'Default': 2,
            'Quick Kill': 3,
            'Used to it': 3,
            'Is this really the last boss?': 3,
            'No problemo': 4,
            'Piece of cake': 4,
            'Nice cutscene bro': 4
        }

        hellrun2score = {
            'No thanks': 0,
            'Solution': 0,
            'Gimme energy': 2,
            'Default': 4,
            'Bring the heat': 6,
            'I run RBO': 8
        }

        hellrunLN2score = {
            'Default': 0,
            'Solution': 0,
            'Bring the heat': 6,
            'I run RBO': 12
        }

        xray2score = {
            'Aarghh': 0,
            'Solution': 0,
            "I don't like spikes": 1,
            'Default': 2,
            "I don't mind spikes": 3,
            'D-Boost master': 4
        }

        gauntlet2score = {
            'Aarghh': 0,
            "I don't like acid": 1,
            'Default': 2
        }

        score = 0

        # knows
        for know in Knows.__dict__:
            if isKnows(know):
                if know in self.params['Knows']:
                    if self.params['Knows'][know][0] == True:
                        score += diff2score[self.params['Knows'][know][1]]
                else:
                    # if old preset with not all the knows, use default values for the know
                    if Knows.__dict__[know].bool == True:
                        score += diff2score[Knows.__dict__[know].difficulty]

        # hard rooms
        hardRoom = 'X-Ray'
        if hardRoom in self.params['Settings']:
            score += xray2score[self.params['Settings'][hardRoom]]

        hardRoom = 'Gauntlet'
        if hardRoom in self.params['Settings']:
            score += gauntlet2score[self.params['Settings'][hardRoom]]

        # bosses
        for boss in ['Kraid', 'Phantoon', 'Draygon', 'Ridley', 'MotherBrain']:
            if boss in self.params['Settings']:
                score += boss2score[self.params['Settings'][boss]]

        # hellruns
        for hellRun in ['Ice', 'MainUpperNorfair']:
            if hellRun in self.params['Settings']:
                score += hellrun2score[self.params['Settings'][hellRun]]

        hellRun = 'LowerNorfair'
        if hellRun in self.params['Settings']:
            score += hellrunLN2score[self.params['Settings'][hellRun]]

        return score

class PresetLoaderJson(PresetLoader):
    # when called from the test suite
    def __init__(self, jsonFileName):
        with openFile(jsonFileName) as jsonFile:
            self.params = json.load(jsonFile)
        super(PresetLoaderJson, self).__init__()

class PresetLoaderDict(PresetLoader):
    # when called from the website
    def __init__(self, params):
        self.params = params
        super(PresetLoaderDict, self).__init__()

def getDefaultMultiValues():
    from ..graph.graph_utils import GraphUtils
    from ..utils.objectives import Objectives
    defaultMultiValues = {
        'startLocation': GraphUtils.getStartAccessPointNames(),
        'majorsSplit': ['Full', 'FullWithHUD', 'Major', 'Chozo', 'Scavenger'],
        'progressionSpeed': ['slowest', 'slow', 'medium', 'fast', 'fastest', 'basic', 'VARIAble', 'speedrun'],
        'progressionDifficulty': ['easier', 'normal', 'harder'],
        'morphPlacement': ['early', 'normal'], #['early', 'late', 'normal'],
        'energyQty': ['ultra sparse', 'sparse', 'medium', 'vanilla'],
        'gravityBehaviour': ['Vanilla', 'Balanced', 'Progressive'],
        'areaRandomization': ['off', 'full', 'light'],
        'objective': Objectives.getAllGoals(removeNothing=True),
        'tourian': ['Vanilla', 'Fast', 'Disabled']
    }
    return defaultMultiValues

def getPresetValues():
    return [
        "newbie",
        "casual",
        "regular",
        "veteran",
        "expert",
        "master",
        "samus",
        "Season_Races",
        "SMRAT2021",
        "solution",
        "custom",
        "varia_custom"
    ]

# from web to cli
def convertParam(randoParams, param, inverse=False):
    value = randoParams.get(param, "off" if inverse == False else "on")
    if value == "on":
        return True if inverse == False else False
    elif value == "off":
        return False if inverse == False else True
    elif value == "random":
        return "random"
    raise Exception("invalid value for parameter {}".format(param))

def loadRandoPreset(options, args):
    defaultMultiValues = getDefaultMultiValues()
    diffs = ["easy", "medium", "hard", "harder", "hardcore", "mania", "infinity"]
    presetValues = getPresetValues()

    args.animals = options.animals.value
    args.noVariaTweaks = not options.varia_tweaks.value
    args.maxDifficulty = diffs[options.max_difficulty.value]
    #args.suitsRestriction = options.suits_restriction.value
    args.hideItems = options.hide_items.value
    args.strictMinors = options.strict_minors.value
    args.noLayout = not options.layout_patches.value
    args.gravityBehaviour = defaultMultiValues["gravityBehaviour"][options.gravity_behaviour.value]
    args.nerfedCharge = options.nerfed_charge.value
    args.area = options.area_randomization.current_key
    if (args.area == "true"):
        args.area = "full"
    if args.area != "off":
        args.areaLayoutBase = not options.area_layout.value
    args.escapeRando = options.escape_rando.value
    args.noRemoveEscapeEnemies = not options.remove_escape_enemies.value
    args.doorsColorsRando = options.doors_colors_rando.value
    args.allowGreyDoors = options.allow_grey_doors.value
    args.bosses = options.boss_randomization.value
    if options.fun_combat.value:
        args.superFun.append("Combat")
    if options.fun_movement.value:
        args.superFun.append("Movement")
    if options.fun_suits.value:
        args.superFun.append("Suits") 

    ipsPatches = {  "spin_jump_restart":"spinjumprestart", 
                    "rando_speed":"rando_speed", 
                    "elevators_speed":"elevators_speed",
                    "fast_doors":"fast_doors",
                    "refill_before_save":"refill_before_save",
                    "relaxed_round_robin_cf":"relaxed_round_robin_cf"}
    for settingName, patchName in ipsPatches.items():
        if hasattr(options, settingName) and getattr(options, settingName).value:
            args.patches.append(patchName + '.ips')

    patches = {"no_music":"No_Music", "infinite_space_jump":"Infinite_Space_Jump"}
    for settingName, patchName in patches.items():
        if hasattr(options, settingName) and getattr(options, settingName).value:
            args.patches.append(patchName)
             
    args.hud = options.hud.value
    args.morphPlacement = defaultMultiValues["morphPlacement"][options.morph_placement.value]
    #args.majorsSplit
    #args.scavNumLocs
    #args.scavRandomized
    args.startLocation = defaultMultiValues["startLocation"][options.start_location.value]
    #args.progressionDifficulty
    #args.progressionSpeed
    args.missileQty = options.missile_qty.value / float(10)
    args.superQty = options.super_qty.value / float(10)
    args.powerBombQty = options.power_bomb_qty.value / float(10)
    args.minorQty = options.minor_qty.value
    args.energyQty = defaultMultiValues["energyQty"][options.energy_qty.value]
    args.objectiveRandom = options.custom_objective.value
    args.objectiveList = list(options.custom_objective_list.value)
    args.nbObjective = options.custom_objective_count.value
    args.objective = list(options.objective.value)
    args.tourian = defaultMultiValues["tourian"][options.tourian.value]
    #args.minimizerN
    #args.minimizerTourian

    return presetValues[options.preset.value]

def getRandomizerDefaultParameters():
    defaultParams = {}
    defaultMultiValues = getDefaultMultiValues()

    defaultParams['complexity'] = "simple"
    defaultParams['preset'] = 'regular'
    defaultParams['randoPreset'] = ""
    defaultParams['raceMode'] = "off"
    defaultParams['majorsSplit'] = "Full"
    defaultParams['majorsSplitMultiSelect'] = defaultMultiValues['majorsSplit']
    defaultParams['scavNumLocs'] = "10"
    defaultParams['scavRandomized'] = "off"
    defaultParams['startLocation'] = "Landing Site"
    defaultParams['startLocationMultiSelect'] = defaultMultiValues['startLocation']
    defaultParams['maxDifficulty'] = 'hardcore'
    defaultParams['progressionSpeed'] = "medium"
    defaultParams['progressionSpeedMultiSelect'] = defaultMultiValues['progressionSpeed']
    defaultParams['progressionDifficulty'] = 'normal'
    defaultParams['progressionDifficultyMultiSelect'] = defaultMultiValues['progressionDifficulty']
    defaultParams['morphPlacement'] = "early"
    defaultParams['morphPlacementMultiSelect'] = defaultMultiValues['morphPlacement']
    defaultParams['suitsRestriction'] = "on"
    defaultParams['hideItems'] = "off"
    defaultParams['strictMinors'] = "off"
    defaultParams['missileQty'] = "3"
    defaultParams['superQty'] = "2"
    defaultParams['powerBombQty'] = "1"
    defaultParams['minorQty'] = "100"
    defaultParams['energyQty'] = "vanilla"
    defaultParams['energyQtyMultiSelect'] = defaultMultiValues['energyQty']
    defaultParams['objectiveRandom'] = "off"
    defaultParams['nbObjective'] = "4"
    defaultParams['objective'] = ["kill all G4"]
    defaultParams['objectiveMultiSelect'] = defaultMultiValues['objective']
    defaultParams['tourian'] = "Vanilla"
    defaultParams['areaRandomization'] = "off"
    defaultParams['areaLayout'] = "off"
    defaultParams['doorsColorsRando'] = "off"
    defaultParams['allowGreyDoors'] = "off"
    defaultParams['escapeRando'] = "off"
    defaultParams['removeEscapeEnemies'] = "off"
    defaultParams['bossRandomization'] = "off"
    defaultParams['minimizer'] = "off"
    defaultParams['minimizerQty'] = "45"
    defaultParams['funCombat'] = "off"
    defaultParams['funMovement'] = "off"
    defaultParams['funSuits'] = "off"
    defaultParams['layoutPatches'] = "on"
    defaultParams['variaTweaks'] = "on"
    defaultParams['gravityBehaviour'] = "Balanced"
    defaultParams['gravityBehaviourMultiSelect'] = defaultMultiValues['gravityBehaviour']
    defaultParams['nerfedCharge'] = "off"
    defaultParams['relaxed_round_robin_cf'] = "off"
    defaultParams['itemsounds'] = "on"
    defaultParams['elevators_speed'] = "on"
    defaultParams['fast_doors'] = "on"
    defaultParams['spinjumprestart'] = "off"
    defaultParams['rando_speed'] = "off"
    defaultParams['Infinite_Space_Jump'] = "off"
    defaultParams['refill_before_save'] = "off"
    defaultParams['hud'] = "off"
    defaultParams['animals'] = "off"
    defaultParams['No_Music'] = "off"
    defaultParams['random_music'] = "off"

    return defaultParams

def fixEnergy(items):
    # display number of energy used
    energies = [i for i in items if i.find('ETank') != -1]
    if len(energies) > 0:
        (maxETank, maxReserve, maxEnergy) = (0, 0, 0)
        for energy in energies:
            nETank = int(energy[0:energy.find('-ETank')])
            if energy.find('-Reserve') != -1:
                nReserve = int(energy[energy.find(' - ')+len(' - '):energy.find('-Reserve')])
            else:
                nReserve = 0
            nEnergy = nETank + nReserve
            if nEnergy > maxEnergy:
                maxEnergy = nEnergy
                maxETank = nETank
                maxReserve = nReserve
            items.remove(energy)
        items.append('{}-ETank'.format(maxETank))
        if maxReserve > 0:
            items.append('{}-Reserve'.format(maxReserve))
    
    
    # keep biggest crystal flash
    cfs = [i for i in items if i.find('CrystalFlash') != -1]
    if len(cfs) > 1:
        maxCf = 0
        for cf in cfs:
            nCf = int(cf[0:cf.find('-CrystalFlash')])
            if nCf > maxCf:
                maxCf = nCf
            items.remove(cf)
        items.append('{}-CrystalFlash'.format(maxCf))
    return items

def dumpErrorMsg(outFileName, msg):
    print("DIAG: " + msg)
    if outFileName is not None:
        with open(outFileName, 'w') as jsonFile:
            json.dump({"errorMsg": msg}, jsonFile)