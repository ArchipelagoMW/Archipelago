#!/usr/bin/python3
import sys, argparse

from solver.interactiveSolver import InteractiveSolver
from solver.standardSolver import StandardSolver
from solver.conf import Conf
import utils.log

def interactiveSolver(args):
    # to init, requires interactive/romFileName/presetFileName/output parameters in standard/plando mode
    # to init, requires interactive/presetFileName/output parameters in seedless mode
    # to iterate, requires interactive/state/[loc]/[item]/action/output parameters in item scope
    # to iterate, requires interactive/state/[startPoint]/[endPoint]/action/output parameters in area scope
    if args.action == 'init':
        # init
        if args.mode != 'seedless' and args.romFileName == None:
            print("Missing romFileName parameter for {} mode".format(args.mode))
            sys.exit(1)

        if args.presetFileName == None or args.output == None:
            print("Missing preset or output parameter")
            sys.exit(1)

        solver = InteractiveSolver(args.output, args.logic)
        solver.initialize(args.mode, args.romFileName, args.presetFileName, magic=args.raceMagic, fill=args.fill, startLocation=args.startLocation)
    else:
        # iterate
        params = {}
        if args.scope == 'common':
            if args.action == "save":
                params["lock"] = args.lock
                params["escapeTimer"] = args.escapeTimer
            elif args.action == "randomize":
                params["minorQty"] = args.minorQty
                params["energyQty"] = args.energyQty
                params["forbiddenItems"] = args.forbiddenItems.split(',') if args.forbiddenItems is not None else []
        elif args.scope == 'item':
            if args.state == None or args.action == None or args.output == None:
                print("Missing state/action/output parameter")
                sys.exit(1)
            if args.action in ["add", "replace"]:
                if args.mode not in ['seedless', 'race', 'debug'] and args.loc == None:
                    print("Missing loc parameter when using action add for item")
                    sys.exit(1)
                if args.mode == 'plando':
                    if args.item == None:
                        print("Missing item parameter when using action add in plando/suitless mode")
                        sys.exit(1)
                params = {'loc': args.loc, 'item': args.item, 'hide': args.hide}
            elif args.action == "remove":
                if args.loc != None:
                    params = {'loc': args.loc}
                elif args.item != None:
                    params = {'item': args.item}
                else:
                    params = {'count': args.count}
            elif args.action == "toggle":
                params = {'item': args.item}
        elif args.scope == 'area':
            if args.state == None or args.action == None or args.output == None:
                print("Missing state/action/output parameter")
                sys.exit(1)
            if args.action == "add":
                if args.startPoint == None or args.endPoint == None:
                    print("Missing start or end point parameter when using action add for item")
                    sys.exit(1)
                params = {'startPoint': args.startPoint, 'endPoint': args.endPoint}
            if args.action == "remove" and args.startPoint != None:
                params = {'startPoint': args.startPoint}
        elif args.scope == 'door':
            if args.state == None or args.action == None or args.output == None:
                print("Missing state/action/output parameter")
                sys.exit(1)
            if args.action == "replace":
                if args.doorName is None or args.newColor is None:
                    print("Missing doorName or newColor parameter when using action replace for door")
                    sys.exit(1)
                params = {'doorName': args.doorName, 'newColor': args.newColor}
            elif args.action == "toggle":
                if args.doorName is None:
                    print("Missing doorName parameter when using action toggle for door")
                    sys.exit(1)
                params = {'doorName': args.doorName}
        elif args.scope == 'dump':
            if args.action == "import":
                if args.dump is None:
                    print("Missing dump parameter when import a dump")
                params = {'dump': args.dump}
        params["debug"] = args.mode == 'debug'

        solver = InteractiveSolver(args.output, args.logic)
        solver.iterate(args.state, args.scope, args.action, params)

def standardSolver(args):
    if args.romFileName is None:
        print("Parameter --romFileName mandatory when not in interactive mode")
        sys.exit(1)

    if args.difficultyTarget is None:
        difficultyTarget = Conf.difficultyTarget
    else:
        difficultyTarget = args.difficultyTarget

    if args.pickupStrategy is None:
        pickupStrategy = Conf.itemsPickup
    else:
        pickupStrategy = args.pickupStrategy

    # itemsForbidden is like that: [['Varia'], ['Reserve'], ['Gravity']], fix it
    args.itemsForbidden = [item[0] for item in args.itemsForbidden]

    solver = StandardSolver(args.romFileName, args.presetFileName, difficultyTarget,
                            pickupStrategy, args.itemsForbidden, type=args.type,
                            firstItemsLog=args.firstItemsLog, extStatsFilename=args.extStatsFilename,
                            extStatsStep=args.extStatsStep,
                            displayGeneratedPath=args.displayGeneratedPath,
                            outputFileName=args.output, magic=args.raceMagic,
                            checkDuplicateMajor=args.checkDuplicateMajor, vcr=args.vcr,
                            runtimeLimit_s=args.runtimeLimit_s)

    solver.solveRom()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Random Metroid Solver")
    parser.add_argument('--romFileName', '-r', help="the input rom", nargs='?',
                        default=None, dest="romFileName")
    parser.add_argument('--preset', '-p', help="the preset file", nargs='?',
                        default=None, dest='presetFileName')
    parser.add_argument('--difficultyTarget', '-t',
                        help="the difficulty target that the solver will aim for",
                        dest='difficultyTarget', nargs='?', default=None, type=int)
    parser.add_argument('--pickupStrategy', '-s', help="Pickup strategy for the Solver",
                        dest='pickupStrategy', nargs='?', default=None,
                        choices=['all', 'any'])
    parser.add_argument('--itemsForbidden', '-f', help="Item not picked up during solving",
                        dest='itemsForbidden', nargs='+', default=[], action='append')

    parser.add_argument('--type', '-y', help="web or console", dest='type', nargs='?',
                        default='console', choices=['web', 'console'])
    parser.add_argument('--checkDuplicateMajor', dest="checkDuplicateMajor", action='store_true',
                        help="print a warning if the same major is collected more than once")
    parser.add_argument('--debug', '-d', help="activate debug logging", dest='debug', action='store_true')
    parser.add_argument('--firstItemsLog', '-1',
                        help="path to file where for each item type the first time it was found and where will be written (spoilers!)",
                        nargs='?', default=None, type=str, dest='firstItemsLog')
    parser.add_argument('--ext_stats', help="Generate extended stats",
                        nargs='?', default=None, dest='extStatsFilename')
    parser.add_argument('--ext_stats_step', help="what extended stats to generate",
                        nargs='?', default=None, dest='extStatsStep', type=int)
    parser.add_argument('--displayGeneratedPath', '-g', help="display the generated path (spoilers!)",
                        dest='displayGeneratedPath', action='store_true')
    parser.add_argument('--race', help="Race mode magic number", dest='raceMagic', type=int)
    parser.add_argument('--vcr', help="Generate VCR output file", dest='vcr', action='store_true')
    # standard/interactive, web site
    parser.add_argument('--output', '-o', help="When called from the website, contains the result of the solver",
                        dest='output', nargs='?', default=None)
    # interactive, web site
    parser.add_argument('--interactive', '-i', help="Activate interactive mode for the solver",
                        dest='interactive', action='store_true')
    parser.add_argument('--state', help="JSON file of the Solver state (used in interactive mode)",
                        dest="state", nargs='?', default=None)
    parser.add_argument('--loc', help="Name of the location to action on (used in interactive mode)",
                        dest="loc", nargs='?', default=None)
    parser.add_argument('--action', help="Pickup item at location, remove last pickedup location, clear all (used in interactive mode)",
                        dest="action", nargs="?", default=None, choices=['init', 'add', 'remove', 'clear', 'get', 'save', 'replace', 'randomize', 'toggle', 'import'])
    parser.add_argument('--item', help="Name of the item to place in plando mode (used in interactive mode)",
                        dest="item", nargs='?', default=None)
    parser.add_argument('--hide', help="Hide the item to place in plando mode (used in interactive mode)",
                        dest="hide", action='store_true')
    parser.add_argument('--startPoint', help="The start AP to connect (used in interactive mode)",
                        dest="startPoint", nargs='?', default=None)
    parser.add_argument('--endPoint', help="The destination AP to connect (used in interactive mode)",
                        dest="endPoint", nargs='?', default=None)

    parser.add_argument('--mode', help="Solver mode: standard/seedless/plando (used in interactive mode)",
                        dest="mode", nargs="?", default=None, choices=['standard', 'seedless', 'plando', 'race', 'debug'])
    parser.add_argument('--scope', help="Scope for the action: common/area/item (used in interactive mode)",
                        dest="scope", nargs="?", default=None, choices=['common', 'area', 'item', 'door', 'dump'])
    parser.add_argument('--count', help="Number of item rollback (used in interactive mode)",
                        dest="count", type=int)
    parser.add_argument('--lock', help="lock the plando seed (used in interactive mode)",
                        dest="lock", action='store_true')
    parser.add_argument('--escapeTimer', help="escape timer like 03:00", dest="escapeTimer", default=None)
    parser.add_argument('--fill', help="in plando load all the source seed locations/transitions as a base (used in interactive mode)",
                        dest="fill", action='store_true')
    parser.add_argument('--startLocation', help="in plando/seedless: the start location", dest="startLocation", default="Landing Site")
    parser.add_argument('--minorQty', help="rando plando  (used in interactive mode)",
                        dest="minorQty", nargs="?", default=None, choices=[str(i) for i in range(0,101)])
    parser.add_argument('--energyQty', help="rando plando  (used in interactive mode)",
                        dest="energyQty", nargs="?", default=None, choices=["sparse", "medium", "vanilla"])
    parser.add_argument('--forbiddenItems', help="rando plando  (used in interactive mode)",
                        dest="forbiddenItems", nargs="?", default=None)
    parser.add_argument('--doorName', help="door to replace (used in interactive mode)",
                        dest="doorName", nargs="?", default=None)
    parser.add_argument('--newColor', help="new color for door (used in interactive mode)",
                        dest="newColor", nargs="?", default=None)
    parser.add_argument('--logic', help='logic to use (used in interactive mode)', dest='logic', nargs='?', default="vanilla", choices=["vanilla", "rotation"])
    parser.add_argument('--runtime',
                        help="Maximum runtime limit in seconds. If 0 or negative, no runtime limit.",
                        dest='runtimeLimit_s', nargs='?', default=0, type=int)
    parser.add_argument('--dump', help="dump file with autotracker state (used in interactive mode)",
                        dest="dump", nargs="?", default=None)

    args = parser.parse_args()

    if args.presetFileName is None:
        args.presetFileName = 'worlds/sm/variaRandomizer/standard_presets/regular.json'

    if args.raceMagic != None:
        if args.raceMagic <= 0 or args.raceMagic >= 0x10000:
            print("Invalid magic")
            sys.exit(-1)

    if args.count != None:
        if args.count < 1 or args.count > 0x80:
            print("Invalid count")
            sys.exit(-1)

    utils.log.init(args.debug)

    if args.interactive == True:
        interactiveSolver(args)
    else:
        standardSolver(args)
