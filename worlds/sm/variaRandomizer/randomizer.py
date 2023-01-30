#!/usr/bin/python3

from Utils import output_path
import argparse, os.path, json, sys, shutil, random, copy, requests

from rando.RandoSettings import RandoSettings, GraphSettings
from rando.RandoExec import RandoExec
from graph.graph_utils import vanillaTransitions, vanillaBossesTransitions, GraphUtils, getAccessPoint
from utils.parameters import Knows, Controller, easy, medium, hard, harder, hardcore, mania, infinity, text2diff, diff2text, appDir
from rom.rom_patches import RomPatches
from rom.rompatcher import RomPatcher
from utils.utils import PresetLoader, loadRandoPreset, getDefaultMultiValues, getPresetDir
from utils.version import displayedVersion
from logic.smbool import SMBool
from utils.doorsmanager import DoorsManager
from logic.logic import Logic

import utils.log
from worlds.sm.Options import StartLocation

# we need to know the logic before doing anything else
def getLogic():
    # check if --logic is there
    logic = 'vanilla'
    for i, param in enumerate(sys.argv):
        if param == '--logic' and i+1 < len(sys.argv):
            logic = sys.argv[i+1]
    return logic
Logic.factory(getLogic())
defaultMultiValues = getDefaultMultiValues()
speeds = defaultMultiValues['progressionSpeed']
energyQties = defaultMultiValues['energyQty']
progDiffs = defaultMultiValues['progressionDifficulty']
morphPlacements = defaultMultiValues['morphPlacement']
majorsSplits = defaultMultiValues['majorsSplit']
gravityBehaviours = defaultMultiValues['gravityBehaviour']

def randomMulti(args, param, defaultMultiValues):
    value = args[param]

    isRandom = False
    if value == "random":
        isRandom = True
        if args[param+"List"] != None:
            # use provided list
            choices = args[param+"List"].split(',')
            value = random.choice(choices)
        else:
            # use default list
            value = random.choice(defaultMultiValues)

    return (isRandom, value)

def dumpErrorMsg(outFileName, msg):
    print("DIAG: " + msg)
    if outFileName is not None:
        with open(outFileName, 'w') as jsonFile:
            json.dump({"errorMsg": msg}, jsonFile)

def dumpErrorMsgs(outFileName, msgs):
    dumpErrorMsg(outFileName, joinErrorMsgs(msgs))

def joinErrorMsgs(msgs):
    return '\n'.join(msgs)

def restricted_float(x):
    x = float(x)
    if x < 0.0 or x > 9.0:
        raise argparse.ArgumentTypeError("%r not in range [1.0, 9.0]"%(x,))
    return x

def to_pascal_case_with_space(snake_str):
    return snake_str.replace("_", " ").title()

class VariaRandomizer:

    parser = argparse.ArgumentParser(description="Random Metroid Randomizer")
    parser.add_argument('--patchOnly',
                        help="only apply patches, do not perform any randomization", action='store_true',
                        dest='patchOnly', default=False)
    parser.add_argument('--param', '-p', help="the input parameters",
                        default=None, dest='paramsFileName')
    parser.add_argument('--dir',
                        help="output directory for ROM and dot files",
                        dest='directory', nargs='?', default='.')
    parser.add_argument('--dot',
                        help="generate dot file with area graph",
                        action='store_true',dest='dot', default=False)
    parser.add_argument('--area', help="area mode",
                        dest='area', nargs='?', const=True, default=False)
    parser.add_argument('--areaLayoutBase',
                        help="use simple layout patch for area mode", action='store_true',
                        dest='areaLayoutBase', default=False)
    parser.add_argument('--lightArea', help="keep number of transitions between vanilla areas", action='store_true',
                        dest='lightArea', default=False)
    parser.add_argument('--escapeRando',
                        help="Randomize the escape sequence",
                        dest='escapeRando', nargs='?', const=True, default=False)
    parser.add_argument('--noRemoveEscapeEnemies',
                        help="Do not remove enemies during escape sequence", action='store_true',
                        dest='noRemoveEscapeEnemies', default=False)
    parser.add_argument('--bosses', help="randomize bosses",
                        dest='bosses', nargs='?', const=True, default=False)
    parser.add_argument('--minimizer', help="minimizer mode: area and boss mixed together. arg is number of non boss locations",
                        dest='minimizerN', nargs='?', const=35, default=None,
                        choices=[str(i) for i in range(30,101)]+["random"])
    parser.add_argument('--minimizerTourian',
                        help="Tourian speedup in minimizer mode",
                        dest='minimizerTourian', nargs='?', const=True, default=False)
    parser.add_argument('--startLocation', help="Name of the Access Point to start from",
                        dest='startLocation', nargs='?', default="Landing Site",
                        choices=['random'] + GraphUtils.getStartAccessPointNames())
    parser.add_argument('--startLocationList', help="list to choose from when random",
                        dest='startLocationList', nargs='?', default=None)
    parser.add_argument('--debug', '-d', help="activate debug logging", dest='debug',
                        action='store_true')
    parser.add_argument('--maxDifficulty', '-t',
                        help="the maximum difficulty generated seed will be for given parameters",
                        dest='maxDifficulty', nargs='?', default=None,
                        choices=['easy', 'medium', 'hard', 'harder', 'hardcore', 'mania', 'random'])
    parser.add_argument('--minDifficulty',
                        help="the minimum difficulty generated seed will be for given parameters (speedrun prog speed required)",
                        dest='minDifficulty', nargs='?', default=None,
                        choices=['easy', 'medium', 'hard', 'harder', 'hardcore', 'mania'])
    parser.add_argument('--seed', '-s', help="randomization seed to use", dest='seed',
                        nargs='?', default=0, type=int)
    parser.add_argument('--rom', '-r',
                        help="the vanilla ROM",
                        dest='rom', nargs='?', default=None)
    parser.add_argument('--output',
                        help="to choose the name of the generated json (for the webservice)",
                        dest='output', nargs='?', default=None)
    parser.add_argument('--preset',
                        help="the name of the preset (for the webservice)",
                        dest='preset', nargs='?', default=None)
    parser.add_argument('--patch', '-c',
                        help="optional patches to add",
                        dest='patches', nargs='?', default=[], action='append',
                        choices=['itemsounds.ips', 'elevators_doors_speed.ips', 'random_music.ips',
                                'spinjumprestart.ips', 'rando_speed.ips', 'No_Music', 'AimAnyButton.ips',
                                'max_ammo_display.ips', 'supermetroid_msu1.ips', 'Infinite_Space_Jump',
                                'refill_before_save.ips', 'remove_elevators_doors_speed.ips',
                                'remove_itemsounds.ips', 'vanilla_music.ips'])
    parser.add_argument('--missileQty', '-m',
                        help="quantity of missiles",
                        dest='missileQty', nargs='?', default=3,
                        type=restricted_float)
    parser.add_argument('--superQty', '-q',
                        help="quantity of super missiles",
                        dest='superQty', nargs='?', default=2,
                        type=restricted_float)
    parser.add_argument('--powerBombQty', '-w',
                        help="quantity of power bombs",
                        dest='powerBombQty', nargs='?', default=1,
                        type=restricted_float)
    parser.add_argument('--minorQty', '-n',
                        help="quantity of minors",
                        dest='minorQty', nargs='?', default=100,
                        choices=[str(i) for i in range(0,101)])
    parser.add_argument('--energyQty', '-g',
                        help="quantity of ETanks/Reserve Tanks",
                        dest='energyQty', nargs='?', default='vanilla',
                        choices=energyQties + ['random'])
    parser.add_argument('--energyQtyList', help="list to choose from when random",
                        dest='energyQtyList', nargs='?', default=None)
    parser.add_argument('--strictMinors',
                        help="minors quantities values will be strictly followed instead of being probabilities",
                        dest='strictMinors', nargs='?', const=True, default=False)
    parser.add_argument('--majorsSplit',
                        help="how to split majors/minors: Full, FullWithHUD, Major, Chozo, Scavenger",
                        dest='majorsSplit', nargs='?', choices=majorsSplits + ['random'], default='Full')
    parser.add_argument('--majorsSplitList', help="list to choose from when random",
                        dest='majorsSplitList', nargs='?', default=None)
    parser.add_argument('--scavNumLocs',
                        help="For Scavenger split, number of major locations in the mandatory route",
                        dest='scavNumLocs', nargs='?', default=10,
                        choices=["0"]+[str(i) for i in range(4,17)])
    parser.add_argument('--scavRandomized',
                        help="For Scavenger split, decide whether mandatory major locs will have non-vanilla items",
                        dest='scavRandomized', nargs='?', const=True, default=False)
    parser.add_argument('--scavEscape',
                        help="For Scavenger split, decide whether escape sequence shall be triggered as soon as the hunt is over",
                        dest='scavEscape', nargs='?', const=True, default=False)
    parser.add_argument('--suitsRestriction',
                        help="no suits in early game",
                        dest='suitsRestriction', nargs='?', const=True, default=False)
    parser.add_argument('--morphPlacement',
                        help="morph placement",
                        dest='morphPlacement', nargs='?', default='early',
                        choices=morphPlacements + ['random'])
    parser.add_argument('--morphPlacementList', help="list to choose from when random",
                        dest='morphPlacementList', nargs='?', default=None)
    parser.add_argument('--hideItems', help="Like in dessy's rando hide half of the items",
                        dest="hideItems", nargs='?', const=True, default=False)
    parser.add_argument('--progressionSpeed', '-i',
                        help="progression speed, from " + str(speeds) + ". 'random' picks a random speed from these. Pick a random speed from a subset using comma-separated values, like 'slow,medium,fast'.",
                        dest='progressionSpeed', nargs='?', default='medium', choices=speeds+['random'])
    parser.add_argument('--progressionSpeedList', help="list to choose from when random",
                        dest='progressionSpeedList', nargs='?', default=None)
    parser.add_argument('--progressionDifficulty',
                        help="",
                        dest='progressionDifficulty', nargs='?', default='normal',
                        choices=progDiffs + ['random'])
    parser.add_argument('--progressionDifficultyList', help="list to choose from when random",
                        dest='progressionDifficultyList', nargs='?', default=None)
    parser.add_argument('--superFun',
                        help="randomly remove major items from the pool for maximum enjoyment",
                        dest='superFun', nargs='?', default=[], action='append',
                        choices=['Movement', 'Combat', 'Suits', 'MovementRandom', 'CombatRandom', 'SuitsRandom'])
    parser.add_argument('--animals',
                        help="randomly change the save the animals room",
                        dest='animals', action='store_true', default=False)
    parser.add_argument('--nolayout',
                        help="do not include total randomizer layout patches",
                        dest='noLayout', action='store_true', default=False)
    parser.add_argument('--gravityBehaviour',
                        help="varia/gravity suits behaviour",
                        dest='gravityBehaviour', nargs='?', default='Balanced', choices=gravityBehaviours+['random'])
    parser.add_argument('--gravityBehaviourList', help="list to choose from when random",
                        dest='gravityBehaviourList', nargs='?', default=None)
    parser.add_argument('--nerfedCharge',
                        help="apply nerfed charge patch",
                        dest='nerfedCharge', action='store_true', default=False)
    parser.add_argument('--novariatweaks',
                        help="do not include VARIA randomizer tweaks",
                        dest='noVariaTweaks', action='store_true', default=False)
    parser.add_argument('--controls',
                        help="specify controls, comma-separated, in that order: Shoot,Jump,Dash,ItemSelect,ItemCancel,AngleUp,AngleDown. Possible values: A,B,X,Y,L,R,Select,None",
                        dest='controls')
    parser.add_argument('--moonwalk',
                        help="Enables moonwalk by default",
                        dest='moonWalk', action='store_true', default=False)
    parser.add_argument('--runtime',
                        help="Maximum runtime limit in seconds. If 0 or negative, no runtime limit. Default is 30.",
                        dest='runtimeLimit_s', nargs='?', default=30, type=int)
    parser.add_argument('--race', help="Race mode magic number, between 1 and 65535", dest='raceMagic',
                        type=int)
    parser.add_argument('--vcr', help="Generate VCR output file", dest='vcr', action='store_true')
    parser.add_argument('--palette', help="Randomize the palettes", dest='palette', action='store_true')
    parser.add_argument('--individual_suit_shift', help="palette param", action='store_true',
                        dest='individual_suit_shift', default=False)
    parser.add_argument('--individual_tileset_shift', help="palette param", action='store_true',
                        dest='individual_tileset_shift', default=False)
    parser.add_argument('--no_match_ship_and_power', help="palette param", action='store_false',
                        dest='match_ship_and_power', default=True)
    parser.add_argument('--seperate_enemy_palette_groups', help="palette param", action='store_true',
                        dest='seperate_enemy_palette_groups', default=False)
    parser.add_argument('--no_match_room_shift_with_boss', help="palette param", action='store_false',
                        dest='match_room_shift_with_boss', default=True)
    parser.add_argument('--no_shift_tileset_palette', help="palette param", action='store_false',
                        dest='shift_tileset_palette', default=True)
    parser.add_argument('--no_shift_boss_palettes', help="palette param", action='store_false',
                        dest='shift_boss_palettes', default=True)
    parser.add_argument('--no_shift_suit_palettes', help="palette param", action='store_false',
                        dest='shift_suit_palettes', default=True)
    parser.add_argument('--no_shift_enemy_palettes', help="palette param", action='store_false',
                        dest='shift_enemy_palettes', default=True)
    parser.add_argument('--no_shift_beam_palettes', help="palette param", action='store_false',
                        dest='shift_beam_palettes', default=True)
    parser.add_argument('--no_shift_ship_palette', help="palette param", action='store_false',
                        dest='shift_ship_palette', default=True)
    parser.add_argument('--min_degree', help="min hue shift", dest='min_degree', nargs='?', default=-180, type=int)
    parser.add_argument('--max_degree', help="max hue shift", dest='max_degree', nargs='?', default=180, type=int)
    parser.add_argument('--no_global_shift', help="", action='store_false', dest='global_shift', default=True)
    parser.add_argument('--invert', help="invert color range", dest='invert', action='store_true', default=False)
    parser.add_argument('--no_blue_door_palette', help="palette param", action='store_true',
                        dest='no_blue_door_palette', default=False)
    parser.add_argument('--ext_stats', help="dump extended stats SQL", nargs='?', default=None, dest='extStatsFilename')
    parser.add_argument('--randoPreset', help="rando preset file", dest="randoPreset", nargs='?', default=None)
    parser.add_argument('--fakeRandoPreset', help="for prog speed stats", dest="fakeRandoPreset", nargs='?', default=None)
    parser.add_argument('--plandoRando', help="json string with already placed items/locs", dest="plandoRando",
                        nargs='?', default=None)
    parser.add_argument('--sprite', help='use a custom sprite for Samus', dest='sprite', default=None)
    parser.add_argument('--no_spin_attack', help='when using a custom sprite, use the same animation for screw attack with or without Space Jump', dest='noSpinAttack', action='store_true', default=False)
    parser.add_argument('--customItemNames', help='add custom item names for some of them, related to the custom sprite',
                        dest='customItemNames', action='store_true', default=False)
    parser.add_argument('--ship', help='use a custom sprite for Samus ship', dest='ship', default=None)
    parser.add_argument('--seedIps', help='ips generated from previous seed', dest='seedIps', default=None)
    parser.add_argument('--jm,', help="display data used by jm for its stats", dest='jm', action='store_true', default=False)
    parser.add_argument('--doorsColorsRando', help='randomize color of colored doors', dest='doorsColorsRando',
                        nargs='?', const=True, default=False)
    parser.add_argument('--allowGreyDoors', help='add grey color in doors colors pool', dest='allowGreyDoors',
                        nargs='?', const=True, default=False)
    parser.add_argument('--logic', help='logic to use', dest='logic', nargs='?', default="varia", choices=["varia", "rotation"])
    parser.add_argument('--hud', help='Enable VARIA hud', dest='hud',
                        nargs='?', const=True, default=False)

    def __init__(self, world, rom, player):
        # parse args       
        self.args = copy.deepcopy(VariaRandomizer.parser.parse_args(["--logic", "varia"])) #dummy custom args to skip parsing _sys.argv while still get default values
        self.player = player
        args = self.args
        args.rom = rom
        # args.startLocation = to_pascal_case_with_space(world.startLocation[player].current_key)

        if args.output is None and args.rom is None:
            print("Need --output or --rom parameter")
            sys.exit(-1)
        elif args.output is not None and args.rom is not None:
            print("Can't have both --output and --rom parameters")
            sys.exit(-1)

        if args.plandoRando != None and args.output == None:
            print("plandoRando param requires output param")
            sys.exit(-1)

        utils.log.init(args.debug)
        logger = utils.log.get('Rando')

        Logic.factory(args.logic)

        # service to force an argument value and notify it
        argDict = vars(args)
        self.forcedArgs = {}
        self.optErrMsgs = [ ]
        optErrMsgs = self.optErrMsgs
        def forceArg(arg, value, msg, altValue=None, webArg=None, webValue=None):
            okValues = [value]
            if altValue is not None:
                okValues.append(altValue)

            if argDict[arg] not in okValues:
                argDict[arg] = value
                self.forcedArgs[webArg if webArg != None else arg] = webValue if webValue != None else value
                # print(msg)
                # optErrMsgs.append(msg)

        preset = loadRandoPreset(world, self.player, args)
        # use the skill preset from the rando preset
        if preset is not None and preset != 'custom' and preset != 'varia_custom' and args.paramsFileName is None:
            args.paramsFileName = os.path.join(appDir, getPresetDir(preset), preset+".json")

        # if diff preset given, load it
        if args.paramsFileName is not None:
            PresetLoader.factory(args.paramsFileName).load(self.player)
            preset = os.path.splitext(os.path.basename(args.paramsFileName))[0]

            if args.preset is not None:
                preset = args.preset
        else:
            if preset == 'custom':
                PresetLoader.factory(world.custom_preset[player].value).load(self.player)
            elif preset == 'varia_custom':
                if len(world.varia_custom_preset[player].value) == 0:
                    raise Exception("varia_custom was chosen but varia_custom_preset is missing.")
                url = 'https://randommetroidsolver.pythonanywhere.com/presetWebService'
                preset_name = next(iter(world.varia_custom_preset[player].value))
                payload = '{{"preset": "{}"}}'.format(preset_name)
                headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
                response = requests.post(url, data=payload, headers=headers)
                if response.ok:
                    PresetLoader.factory(json.loads(response.text)).load(self.player)
                else:
                    raise Exception("Got error {} {} {} from trying to fetch varia custom preset named {}".format(response.status_code, response.reason, response.text, preset_name))
            else:
                preset = 'default'
                PresetLoader.factory(os.path.join(appDir, getPresetDir('casual'), 'casual.json')).load(self.player)

        

        logger.debug("preset: {}".format(preset))

        # if no seed given, choose one
        if args.seed == 0:
            self.seed = random.randrange(sys.maxsize)
        else:
            self.seed = args.seed
        logger.debug("seed: {}".format(self.seed))

        if args.raceMagic is not None:
            if args.raceMagic <= 0 or args.raceMagic >= 0x10000:
                print("Invalid magic")
                sys.exit(-1)

        # if no max diff, set it very high
        if args.maxDifficulty:
            if args.maxDifficulty == 'random':
                diffs = ['easy', 'medium', 'hard', 'harder', 'hardcore', 'mania']
                self.maxDifficulty = text2diff[random.choice(diffs)]
            else:
                self.maxDifficulty = text2diff[args.maxDifficulty]
        else:
            self.maxDifficulty = infinity
        # same as solver, increase max difficulty
        threshold = self.maxDifficulty
        epsilon = 0.001
        if self.maxDifficulty <= easy:
            threshold = medium - epsilon
        elif self.maxDifficulty <= medium:
            threshold = hard - epsilon
        elif self.maxDifficulty <= hard:
            threshold = harder - epsilon
        elif self.maxDifficulty <= harder:
            threshold = hardcore - epsilon
        elif self.maxDifficulty <= hardcore:
            threshold = mania - epsilon
        maxDifficulty = threshold
        logger.debug("maxDifficulty: {}".format(self.maxDifficulty))

        # handle random parameters with dynamic pool of values
        (_, progSpeed) = randomMulti(args.__dict__, "progressionSpeed", speeds)
        (_, progDiff) = randomMulti(args.__dict__, "progressionDifficulty", progDiffs)
        (majorsSplitRandom, args.majorsSplit) = randomMulti(args.__dict__, "majorsSplit", majorsSplits)
        (_, self.gravityBehaviour) = randomMulti(args.__dict__, "gravityBehaviour", gravityBehaviours)
        if args.minDifficulty:
            minDifficulty = text2diff[args.minDifficulty]
            if progSpeed != "speedrun":
                optErrMsgs.append("Minimum difficulty setting ignored, as prog speed is not speedrun")
        else:
            minDifficulty = 0

        if args.area == True and args.bosses == True and args.minimizerN is not None:
            forceArg('majorsSplit', 'Full', "'Majors Split' forced to Full", altValue='FullWithHUD')
            if args.minimizerN == "random":
                self.minimizerN = random.randint(30, 60)
                logger.debug("minimizerN: {}".format(self.minimizerN))
            else:
                self.minimizerN = int(args.minimizerN)
        else:
            self.minimizerN = None
        areaRandom = False
        if args.area == 'random':
            areaRandom = True
            args.area = bool(random.getrandbits(1))
        logger.debug("area: {}".format(args.area))

        doorsColorsRandom = False
        if args.doorsColorsRando == 'random':
            doorsColorsRandom = True
            args.doorsColorsRando = bool(random.getrandbits(1))
        logger.debug("doorsColorsRando: {}".format(args.doorsColorsRando))

        bossesRandom = False
        if args.bosses == 'random':
            bossesRandom = True
            args.bosses = bool(random.getrandbits(1))
        logger.debug("bosses: {}".format(args.bosses))

        if args.escapeRando == 'random':
            args.escapeRando = bool(random.getrandbits(1))
        logger.debug("escapeRando: {}".format(args.escapeRando))

        if args.suitsRestriction != False and self.minimizerN is not None:
            forceArg('suitsRestriction', False, "'Suits restriction' forced to off", webValue='off')

        if args.suitsRestriction == 'random':
            if args.morphPlacement == 'late' and args.area == True:
                forceArg('suitsRestriction', False, "'Suits restriction' forced to off", webValue='off')
            else:
                args.suitsRestriction = bool(random.getrandbits(1))
        logger.debug("suitsRestriction: {}".format(args.suitsRestriction))

        if args.hideItems == 'random':
            args.hideItems = bool(random.getrandbits(1))

        if args.morphPlacement == 'random':
            if args.morphPlacementList != None:
                morphPlacements = args.morphPlacementList.split(',')
            args.morphPlacement = random.choice(morphPlacements)
        # Scavenger Hunt constraints
        if args.majorsSplit == 'Scavenger':
            forceArg('progressionSpeed', 'speedrun', "'Progression speed' forced to speedrun")
            progSpeed = "speedrun"
            forceArg('hud', True, "'VARIA HUD' forced to on", webValue='on')
            if not GraphUtils.isStandardStart(args.startLocation):
                forceArg('startLocation', "Landing Site", "Start Location forced to Landing Site because of Scavenger mode")
            if args.morphPlacement == 'late':
                forceArg('morphPlacement', 'normal', "'Morph Placement' forced to normal instead of late")
            if args.scavEscape == True:
                forceArg('escapeRando', True, "'Escape randomization' forced to on", webValue='on')
                forceArg('noRemoveEscapeEnemies', True, "Enemies enabled during escape sequence", webArg='removeEscapeEnemies', webValue='off')
        # random fill makes certain options unavailable
        if (progSpeed == 'speedrun' or progSpeed == 'basic') and args.majorsSplit != 'Scavenger':
            forceArg('progressionDifficulty', 'normal', "'Progression difficulty' forced to normal")
            progDiff = args.progressionDifficulty
        logger.debug("progressionDifficulty: {}".format(progDiff))

        if args.strictMinors == 'random':
            args.strictMinors = bool(random.getrandbits(1))

        # in plando rando we know that the start ap is ok
        if not GraphUtils.isStandardStart(args.startLocation) and args.plandoRando is None:
            if args.majorsSplit in ['Major', "Chozo"]:
                forceArg('hud', True, "'VARIA HUD' forced to on", webValue='on')
            forceArg('noVariaTweaks', False, "'VARIA tweaks' forced to on", webValue='on')
            forceArg('noLayout', False, "'Anti-softlock layout patches' forced to on", webValue='on')
            forceArg('suitsRestriction', False, "'Suits restriction' forced to off", webValue='off')
            forceArg('areaLayoutBase', False, "'Additional layout patches for easier navigation' forced to on", webValue='on')
            possibleStartAPs, reasons = GraphUtils.getPossibleStartAPs(args.area, self.maxDifficulty, args.morphPlacement, self.player)
            if args.startLocation == 'random':
                if args.startLocationList != None:
                    # to be able to give the list in jm we had to replace ' ' with '_', do the opposite operation
                    startLocationList = args.startLocationList.replace('_', ' ')
                    startLocationList = startLocationList.split(',')
                    # intersection between user whishes and reality
                    possibleStartAPs = sorted(list(set(possibleStartAPs).intersection(set(startLocationList))))
                    if len(possibleStartAPs) == 0:
                        optErrMsgs += ["%s : %s" % (apName, cause) for apName, cause in reasons.items() if apName in startLocationList]
                        optErrMsgs.append('Invalid start locations list with your settings.')
                        dumpErrorMsgs(args.output, optErrMsgs)
                        sys.exit(-1)
                args.startLocation = random.choice(possibleStartAPs)
            elif args.startLocation not in possibleStartAPs:
                args.startLocation = 'Landing Site'
                world.start_location[player] = StartLocation(StartLocation.default)
                #optErrMsgs.append('Invalid start location: {}.  {}'.format(args.startLocation, reasons[args.startLocation]))
                #optErrMsgs.append('Possible start locations with these settings: {}'.format(possibleStartAPs))
                #dumpErrorMsgs(args.output, optErrMsgs)
                #sys.exit(-1)
        ap = getAccessPoint(args.startLocation)
        if 'forcedEarlyMorph' in ap.Start and ap.Start['forcedEarlyMorph'] == True:
            forceArg('morphPlacement', 'early', "'Morph Placement' forced to early for custom start location")
        else:
            if progSpeed == 'speedrun':
                if args.morphPlacement == 'late':
                    forceArg('morphPlacement', 'normal', "'Morph Placement' forced to normal instead of late")
                elif (not GraphUtils.isStandardStart(args.startLocation)) and args.morphPlacement != 'normal':
                    forceArg('morphPlacement', 'normal', "'Morph Placement' forced to normal for custom start location")
            if args.majorsSplit == 'Chozo' and args.morphPlacement == "late":
                forceArg('morphPlacement', 'normal', "'Morph Placement' forced to normal for Chozo")
        #if args.patchOnly == False:
        #    print("SEED: " + str(self.seed))

        # fill restrictions dict
        restrictions = { 'Suits' : args.suitsRestriction, 'Morph' : args.morphPlacement, "doors": "normal" if not args.doorsColorsRando else "late" }
        restrictions['MajorMinor'] = 'Full' if args.majorsSplit == 'FullWithHUD' else args.majorsSplit
        if restrictions["MajorMinor"] == "Scavenger":
            scavNumLocs = int(args.scavNumLocs)
            if scavNumLocs == 0:
                scavNumLocs = random.randint(4,16)
            restrictions["ScavengerParams"] = {'numLocs':scavNumLocs, 'vanillaItems':not args.scavRandomized, 'escape': args.scavEscape}
        seedCode = 'X'
        if majorsSplitRandom == False:
            if restrictions['MajorMinor'] == 'Full':
                seedCode = 'FX'
            elif restrictions['MajorMinor'] == 'Chozo':
                seedCode = 'ZX'
            elif restrictions['MajorMinor'] == 'Major':
                seedCode = 'MX'
            elif restrictions['MajorMinor'] == 'Scavenger':
                seedCode = 'SX'
        if args.bosses == True and bossesRandom == False:
            seedCode = 'B'+seedCode
        if args.doorsColorsRando == True and doorsColorsRandom == False:
            seedCode = 'D'+seedCode
        if args.area == True and areaRandom == False:
            seedCode = 'A'+seedCode

        # output ROM name
        #if args.patchOnly == False:
        #    self.fileName = 'VARIA_Randomizer_' + seedCode + str(self.seed) + '_' + preset
        #    if args.progressionSpeed != "random":
        #        self.fileName += "_" + args.progressionSpeed
        #else:
        #    self.fileName = 'VARIA' # TODO : find better way to name the file (argument?)
        self.fileName = output_path
        seedName = self.fileName
        if args.directory != '.':
            self.fileName = args.directory + '/' + self.fileName
        if args.noLayout == True:
            RomPatches.ActivePatches[self.player] = RomPatches.TotalBase.copy()
        else:
            RomPatches.ActivePatches[self.player] = RomPatches.Total.copy()
        RomPatches.ActivePatches[self.player].remove(RomPatches.BlueBrinstarBlueDoor)
        RomPatches.ActivePatches[self.player] += GraphUtils.getGraphPatches(args.startLocation)
        if self.gravityBehaviour != "Balanced":
            RomPatches.ActivePatches[self.player].remove(RomPatches.NoGravityEnvProtection)
        if self.gravityBehaviour == "Progressive":
            RomPatches.ActivePatches[self.player].append(RomPatches.ProgressiveSuits)
        if args.nerfedCharge == True:
            RomPatches.ActivePatches[self.player].append(RomPatches.NerfedCharge)
        if args.noVariaTweaks == False:
            RomPatches.ActivePatches[self.player] += RomPatches.VariaTweaks
        if self.minimizerN is not None:
            RomPatches.ActivePatches[self.player].append(RomPatches.NoGadoras)
            if args.minimizerTourian == True:
                RomPatches.ActivePatches[self.player] += RomPatches.MinimizerTourian
        missileQty = float(args.missileQty)
        superQty = float(args.superQty)
        powerBombQty = float(args.powerBombQty)
        minorQty = int(args.minorQty)
        self.energyQty = args.energyQty
        if missileQty < 1:
            missileQty = random.randint(1, 9)
        if superQty < 1:
            superQty = random.randint(1, 9)
        if powerBombQty < 1:
            powerBombQty = random.randint(1, 9)
        if minorQty < 1:
            minorQty = random.randint(25, 100)
        if self.energyQty == 'random':
            if args.energyQtyList != None:
                # with jm can't have a list with space in it
                energyQtyList = args.energyQtyList.replace('_', ' ')
                energyQties = energyQtyList.split(',')
            self.energyQty = random.choice(energyQties)
        if self.energyQty == 'ultra sparse':
            # add nerfed rainbow beam patch
            RomPatches.ActivePatches[self.player].append(RomPatches.NerfedRainbowBeam)
        qty = {'energy': self.energyQty,
            'minors': minorQty,
            'ammo': { 'Missile': missileQty,
                        'Super': superQty,
                        'PowerBomb': powerBombQty },
            'strictMinors' : args.strictMinors }
        logger.debug("quantities: {}".format(qty))

        if len(args.superFun) > 0:
            superFun = []
            for fun in args.superFun:
                if fun.find('Random') != -1:
                    if bool(random.getrandbits(1)) == True:
                        superFun.append(fun[0:fun.find('Random')])
                else:
                    superFun.append(fun)
            args.superFun = superFun
        logger.debug("superFun: {}".format(args.superFun))
  
        ctrlButton = ["A", "B", "X", "Y", "L", "R", "Select"]
        ctrl = Controller.ControllerDict[self.player]
        self.ctrlDict = { getattr(ctrl, button) : button for button in ctrlButton }
        args.moonWalk = ctrl.Moonwalk

        PlandoOptions = None
        if args.plandoRando is not None:
            forceArg('progressionSpeed', 'speedrun', "'Progression Speed' forced to speedrun")
            progSpeed = 'speedrun'
            forceArg('majorsSplit', 'Full', "'Majors Split' forced to Full")
            forceArg('morphPlacement', 'normal', "'Morph Placement' forced to normal")
            forceArg('progressionDifficulty', 'normal', "'Progression difficulty' forced to normal")
            progDiff = 'normal'
            args.plandoRando = json.loads(args.plandoRando)
            RomPatches.ActivePatches[self.player] = args.plandoRando["patches"]
            DoorsManager.unserialize(args.plandoRando["doors"])
            PlandoOptions = {"locsItems": args.plandoRando['locsItems'], "forbiddenItems": args.plandoRando['forbiddenItems']}
        randoSettings = RandoSettings(self.maxDifficulty, progSpeed, progDiff, qty,
                                    restrictions, args.superFun, args.runtimeLimit_s,
                                    PlandoOptions, minDifficulty)

        # print some parameters for jm's stats
        if args.jm == True:
            print("startLocation:{}".format(args.startLocation))
            print("progressionSpeed:{}".format(progSpeed))
            print("majorsSplit:{}".format(args.majorsSplit))
            print("morphPlacement:{}".format(args.morphPlacement))

        dotFile = None
        if args.area == True:
            if args.dot == True:
                dotFile = args.directory + '/' + seedName + '.dot'
            RomPatches.ActivePatches[self.player] += RomPatches.AreaBaseSet
            if args.areaLayoutBase == False:
                RomPatches.ActivePatches[self.player] += RomPatches.AreaComfortSet
        if args.doorsColorsRando == True:
            RomPatches.ActivePatches[self.player].append(RomPatches.RedDoorsMissileOnly)
        graphSettings = GraphSettings(args.startLocation, args.area, args.lightArea, args.bosses,
                                    args.escapeRando, self.minimizerN, dotFile, args.doorsColorsRando, args.allowGreyDoors,
                                    args.plandoRando["transitions"] if args.plandoRando != None else None)

        if args.plandoRando is None:
            DoorsManager.setDoorsColor(self.player)

        self.escapeAttr = None
        if args.patchOnly == False:
            try:
                self.randoExec = RandoExec(seedName, args.vcr, randoSettings, graphSettings, self.player)
                self.container = self.randoExec.randomize()
                # if we couldn't find an area layout then the escape graph is not created either
                # and getDoorConnections will crash if random escape is activated.
                stuck = False
                if not stuck or args.vcr == True:
                    self.doors = GraphUtils.getDoorConnections(self.randoExec.areaGraph,
                                                        args.area, args.bosses,
                                                        args.escapeRando)
                    escapeAttr = self.randoExec.areaGraph.EscapeAttributes if args.escapeRando else None
                    if escapeAttr is not None:
                        escapeAttr['patches'] = []
                        if args.noRemoveEscapeEnemies == True:
                            escapeAttr['patches'].append("Escape_Rando_Enable_Enemies")
                        if args.scavEscape == True:
                            escapeAttr['patches'].append('Escape_Scavenger')
            except Exception as e:
                import traceback
                traceback.print_exc(file=sys.stdout)
                dumpErrorMsg(args.output, "Error: {}".format(e))
                sys.exit(-1)
        else:
            stuck = False
            itemLocs = []
            progItemLocs = None
        if stuck == True:
            dumpErrorMsg(args.output, self.randoExec.errorMsg)
            print("Can't generate " + self.fileName + " with the given parameters: {}".format(self.randoExec.errorMsg))
            # in vcr mode we still want the seed to be generated to analyze it
            if args.vcr == False:
                sys.exit(-1)
        #if args.patchOnly == False:
        #    randoExec.postProcessItemLocs(itemLocs, args.hideItems)

    def PatchRom(self, outputFilename, customPrePatchApply = None, customPostPatchApply = None):
        args = self.args
        optErrMsgs = self.optErrMsgs

        # choose on animal patch
        if args.animals == True:
            animalsPatches = ['animal_enemies.ips', 'animals.ips', 'draygonimals.ips', 'escapimals.ips',
                            'gameend.ips', 'grey_door_animals.ips', 'low_timer.ips', 'metalimals.ips',
                            'phantoonimals.ips', 'ridleyimals.ips']
            if args.escapeRando == False:
                args.patches.append(random.choice(animalsPatches))
                args.patches.append("Escape_Animals_Change_Event")
            else:
                optErrMsgs.append("Ignored animals surprise because of escape randomization")
        # # transform itemLocs in our usual dict(location, item), exclude minors, we'll get them with the solver
        # locsItems = {}
        # for itemLoc in itemLocs:
        #     locName = itemLoc.Location.Name
        #     itemType = itemLoc.Item.Type
        #     if itemType in ['Missile', 'Super', 'PowerBomb']:
        #         continue
        #     locsItems[locName] = itemType
        # if args.debug == True:
        #     for loc in sorted(locsItems.keys()):
        #         print('{:>50}: {:>16} '.format(loc, locsItems[loc]))

        # if args.plandoRando != None:
        #     with open(args.output, 'w') as jsonFile:
        #         json.dump({"itemLocs": [il.json() for il in itemLocs], "errorMsg": randoExec.errorMsg}, jsonFile)
        #     sys.exit(0)

        # # generate extended stats
        # if args.extStatsFilename != None:
        #     with open(args.extStatsFilename, 'a') as extStatsFile:
        #         skillPreset = os.path.splitext(os.path.basename(args.paramsFileName))[0]
        #         if args.fakeRandoPreset is not None:
        #             randoPreset = args.fakeRandoPreset
        #         else:
        #             randoPreset = os.path.splitext(os.path.basename(args.randoPreset))[0]
        #         db.DB.dumpExtStatsItems(skillPreset, randoPreset, locsItems, extStatsFile)

        try:
            # args.rom is not None: generate local rom named filename.sfc with args.rom as source
            # args.output is not None: generate local json named args.output
            if args.rom is not None:
                # patch local rom
                romFileName = args.rom
                shutil.copyfile(romFileName, outputFilename)
                romPatcher = RomPatcher(outputFilename, args.raceMagic, False, self.player)
            else:
                romPatcher = RomPatcher(magic=args.raceMagic)

            if customPrePatchApply != None:
                customPrePatchApply(romPatcher)

            if args.hud == True or args.majorsSplit == "FullWithHUD":
                args.patches.append("varia_hud.ips")
            if args.patchOnly == False:
                romPatcher.applyIPSPatches(args.startLocation, args.patches,
                                        args.noLayout, self.gravityBehaviour,
                                        args.area, args.bosses, args.areaLayoutBase,
                                        args.noVariaTweaks, args.nerfedCharge, self.energyQty == 'ultra sparse',
                                        self.escapeAttr, self.minimizerN, args.minimizerTourian,
                                        args.doorsColorsRando)
            else:
                 # from customizer permalink, apply previously generated seed ips first
                if args.seedIps != None:
                    romPatcher.applyIPSPatch(args.seedIps)

                romPatcher.addIPSPatches(args.patches)
                # don't color randomize custom ships
                args.shift_ship_palette = False

            if customPostPatchApply != None:
                customPostPatchApply(romPatcher)

            # we have to write ips to ROM before doing our direct modifications which will rewrite some parts (like in credits),
            # but in web mode we only want to generate a global ips at the end
#            if args.rom != None:
#                romPatcher.commitIPS()
            if args.patchOnly == False:
#                romPatcher.writeItemsLocs(itemLocs)
#                romPatcher.writeSplitLocs(args.majorsSplit, itemLocs, progItemLocs)
                 romPatcher.writeItemsNumber()
                 romPatcher.writeSeed(self.seed) # lol if race mode
#                romPatcher.writeSpoiler(itemLocs, progItemLocs)
#                romPatcher.writeRandoSettings(self.randoExec.randoSettings, itemLocs)
                 romPatcher.writeDoorConnections(self.doors)
                 romPatcher.writeVersion(displayedVersion)
            if self.ctrlDict is not None:
                romPatcher.writeControls(self.ctrlDict)
            if args.moonWalk == True:
                romPatcher.enableMoonWalk()
            if args.patchOnly == False:
                romPatcher.writeMagic()
                romPatcher.writeMajorsSplit(args.majorsSplit)
            # if args.palette == True:
            #     paletteSettings = {
            #         "global_shift": None,
            #         "individual_suit_shift": None,
            #         "individual_tileset_shift": None,
            #         "match_ship_and_power": None,
            #         "seperate_enemy_palette_groups": None,
            #         "match_room_shift_with_boss": None,
            #         "shift_tileset_palette": None,
            #         "shift_boss_palettes": None,
            #         "shift_suit_palettes": None,
            #         "shift_enemy_palettes": None,
            #         "shift_beam_palettes": None,
            #         "shift_ship_palette": None,
            #         "min_degree": None,
            #         "max_degree": None,
            #         "invert": None,
            #         "no_blue_door_palette": None
            #     }
            #     for param in paletteSettings:
            #         paletteSettings[param] = getattr(args, param)
            #     PaletteRando(romPatcher, paletteSettings, args.sprite).randomize()

            # web mode, generate only one ips at the end
            if args.rom == None:
                romPatcher.commitIPS()
            romPatcher.end()
            if args.patchOnly == False:
                if len(optErrMsgs) > 0:
#                    optErrMsgs.append(randoExec.errorMsg)
                    msg = joinErrorMsgs(optErrMsgs)
                else:
#                    msg = randoExec.errorMsg
                    msg = ''
            else:
                msg = ''
            if args.rom is None: # web mode
                data = romPatcher.romFile.data
                self.fileName = '{}.sfc'.format(self.fileName)
                data["fileName"] = self.fileName
                # error msg in json to be displayed by the web site
                data["errorMsg"] = msg
                # replaced parameters to update stats in database
                if len(self.forcedArgs) > 0:
                    data["forcedArgs"] = self.forcedArgs
                with open(outputFilename, 'w') as jsonFile:
                    json.dump(data, jsonFile)
            else: # CLI mode
                if msg != "":
                    print(msg)
        except Exception as e:
            import traceback
            traceback.print_exc(file=sys.stdout)
            msg = "Error patching {}: ({}: {})".format(outputFilename, type(e).__name__, e)
            dumpErrorMsg(args.output, msg)
            sys.exit(-1)

#        if stuck == True:
#            print("Rom generated for debug purpose: {}".format(self.fileName))
#        else:
        # print("Rom generated: {}".format(self.fileName))
