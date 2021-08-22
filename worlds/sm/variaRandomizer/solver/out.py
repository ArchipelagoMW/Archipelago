import sys, json, os
from solver.conf import Conf
from solver.difficultyDisplayer import DifficultyDisplayer
from utils.utils import fixEnergy

class Out(object):
    @staticmethod
    def factory(output, solver):
        if output == 'web':
            return OutWeb(solver)
        elif output == 'console':
            return OutConsole(solver)
        elif output == 'rando':
            return OutRando(solver)
        else:
            raise Exception("Wrong output type for the Solver: {}".format(output))

class OutWeb(Out):
    def __init__(self, solver):
        self.solver = solver

    def out(self):
        s = self.solver
        if s.areaRando == True:
            dotFileName = os.path.basename(os.path.splitext(s.romFileName)[0])+'.json'
            dotFileName = os.path.join(os.path.expanduser('~/web2py/applications/solver/static/graph'), dotFileName)
            s.areaGraph.toDot(dotFileName)
            (pngFileName, pngThumbFileName) = self.generatePng(dotFileName)
            if pngFileName is not None and pngThumbFileName is not None:
                pngFileName = os.path.basename(pngFileName)
                pngThumbFileName = os.path.basename(pngThumbFileName)
        else:
            pngFileName = None
            pngThumbFileName = None

        randomizedRom = os.path.basename(os.path.splitext(s.romFileName)[0])+'.sfc'
        diffPercent = DifficultyDisplayer(s.difficulty).percent()
        generatedPath = self.getPath(s.visitedLocations)
        collectedItems = s.smbm.getItems()

        if s.difficulty == -1:
            remainTry = self.getPath(s.tryRemainingLocs())
            remainMajors = self.getPath(s.getRemainMajors())
            remainMinors = self.getPath(s.getRemainMinors())
            skippedMajors = None
            unavailMajors = None
        else:
            remainTry = None
            remainMajors = None
            remainMinors = None
            skippedMajors = self.getPath(s.getSkippedMajors())
            unavailMajors = self.getPath(s.getUnavailMajors())

        result = dict(randomizedRom=randomizedRom, difficulty=s.difficulty,
                      generatedPath=generatedPath, diffPercent=diffPercent,
                      knowsUsed=(s.knowsUsed, s.knowsKnown), itemsOk=s.itemsOk, patches=s.romLoader.getPatches(),
                      pngFileName=pngFileName, pngThumbFileName=pngThumbFileName,
                      remainTry=remainTry, remainMajors=remainMajors, remainMinors=remainMinors,
                      skippedMajors=skippedMajors, unavailMajors=unavailMajors, collectedItems=collectedItems)

        with open(s.outputFileName, 'w') as jsonFile:
            json.dump(result, jsonFile)

    def getPath(self, locations):
        if locations is None:
            return None

        out = []
        for loc in locations:
            if loc.locDifficulty is not None:
                # draygon fight is in it's path
                if loc.Name == 'Draygon':
                    loc.locDifficulty = loc.pathDifficulty

                fixEnergy(loc.locDifficulty.items)
                fixEnergy(loc.pathDifficulty.items)

                out.append([(loc.Name, loc.Room), loc.Area, loc.SolveArea, loc.itemName,
                            '{0:.2f}'.format(loc.locDifficulty.difficulty),
                            sorted(loc.locDifficulty.knows),
                            sorted(list(set(loc.locDifficulty.items))),
                            '{0:.2f}'.format(loc.pathDifficulty.difficulty),
                            sorted(loc.pathDifficulty.knows),
                            sorted(list(set(loc.pathDifficulty.items))),
                            [ap.Name for ap in loc.path] if loc.path is not None else None,
                            loc.Class])

            else:
                fixEnergy(loc.difficulty.items)

                out.append([(loc.Name, loc.Room), loc.Area, loc.SolveArea, loc.itemName,
                            '{0:.2f}'.format(loc.difficulty.difficulty),
                            sorted(loc.difficulty.knows),
                            sorted(list(set(loc.difficulty.items))),
                            '0.00', [], [],
                            [ap.Name for ap in loc.path] if loc.path is not None else None,
                            loc.Class])

        return out

    def generatePng(self, dotFileName):
        # use dot to generate the graph's image .png
        # use convert to generate the thumbnail
        # dotFileName: the /directory/image.dot
        # the png and thumbnails are generated in the same directory as the dot
        # requires that graphviz is installed
        import subprocess

        splited = os.path.splitext(dotFileName)
        pngFileName = splited[0] + '.png'
        pngThumbFileName = splited[0] + '_thumbnail.png'

        # dot -Tpng VARIA_Randomizer_AFX5399_noob.dot -oVARIA_Randomizer_AFX5399_noob.png
        params = ['dot', '-Tpng', dotFileName, '-o'+pngFileName]
        ret = subprocess.call(params)
        if ret != 0:
            print("Error calling dot {}: {}".format(params, ret))
            return (None, None)

        params = ['convert', pngFileName, '-resize', '1024', pngThumbFileName]
        ret = subprocess.call(params)
        if ret != 0:
            print("Error calling convert {}: {}".format(params, ret))
            os.remove(pngFileName)
            return (None, None)

        return (pngFileName, pngThumbFileName)

class OutConsole(Out):
    def __init__(self, solver):
        self.solver = solver

    def out(self):
        s = self.solver
        self.displayOutput()

        print("({}, {}): diff : {}".format(round(float(s.difficulty), 3), s.itemsOk, s.romFileName))
        print("{}/{}: knows Used : {}".format(s.knowsUsed, s.knowsKnown, s.romFileName))

        if s.difficulty >= 0:
            sys.exit(0)
        else:
            sys.exit(1)

    def printPath(self, message, locations, displayAPs=True):
        print("")
        print(message)
        print('{} {:>48} {:>12} {:>34} {:>8} {:>16} {:>14} {} {}'.format("Z", "Location Name", "Area", "Sub Area", "Distance", "Item", "Difficulty", "Knows used", "Items used"))
        print('-'*150)
        lastAP = None
        for loc in locations:
            if displayAPs == True and loc.path is not None:
                path = [ap.Name for ap in loc.path]
                lastAP = path[-1]
                if not (len(path) == 1 and path[0] == lastAP):
                    path = " -> ".join(path)
                    pathDiff = loc.pathDifficulty
                    print('{}: {} {} {} {}'.format('Path', path, round(float(pathDiff.difficulty), 2), sorted(pathDiff.knows), sorted(list(set(pathDiff.items)))))
            line = '{} {:>48}: {:>12} {:>34} {:>8} {:>16} {:>14} {} {}'

            if loc.locDifficulty is not None:
                fixEnergy(loc.locDifficulty.items)

                print(line.format('Z' if loc.isChozo() else ' ',
                                  loc.Name,
                                  loc.Area,
                                  loc.SolveArea,
                                  loc.distance if loc.distance is not None else 'nc',
                                  loc.itemName,
                                  round(float(loc.locDifficulty.difficulty), 2) if loc.locDifficulty is not None else 'nc',
                                  sorted(loc.locDifficulty.knows) if loc.locDifficulty is not None else 'nc',
                                  sorted(list(set(loc.locDifficulty.items))) if loc.locDifficulty is not None else 'nc'))
            elif loc.difficulty is not None:
                fixEnergy(loc.difficulty.items)

                print(line.format('Z' if loc.isChozo() else ' ',
                                  loc.Name,
                                  loc.Area,
                                  loc.SolveArea,
                                  loc.distance if loc.distance is not None else 'nc',
                                  loc.itemName,
                                  round(float(loc.difficulty.difficulty), 2),
                                  sorted(loc.difficulty.knows),
                                  sorted(list(set(loc.difficulty.items)))))
            else:
                print(line.format('Z' if loc.isChozo() else ' ',
                                  loc.Name,
                                  loc.Area,
                                  loc.SolveArea,
                                  loc.distance if loc.distance is not None else 'nc',
                                  loc.itemName,
                                  'nc',
                                  'nc',
                                  'nc'))

    def displayOutput(self):
        s = self.solver

        print("all patches: {}".format(s.romLoader.getAllPatches()))

        # print generated path
        if Conf.displayGeneratedPath == True:
            self.printPath("Generated path ({}/101):".format(len(s.visitedLocations)), s.visitedLocations)

            # if we've aborted, display missing techniques and remaining locations
            if s.difficulty == -1:
                self.printPath("Next locs which could have been available if more techniques were known:", s.tryRemainingLocs())

                remainMajors = s.getRemainMajors()
                if len(remainMajors) > 0:
                    self.printPath("Remaining major locations:", remainMajors, displayAPs=False)

                remainMinors = s.getRemainMinors()
                if remainMinors is not None and len(remainMinors) > 0:
                    self.printPath("Remaining minor locations:", remainMinors, displayAPs=False)

            else:
                # if some locs are not picked up display those which are available
                # and those which are not
                skippedMajors = s.getSkippedMajors()
                if len(skippedMajors) > 0:
                    self.printPath("Skipped major locations:", skippedMajors, displayAPs=False)
                else:
                    print("No skipped major locations")

                unavailMajors = s.getUnavailMajors()
                if len(unavailMajors) > 0:
                    self.printPath("Unaccessible major locations:", unavailMajors, displayAPs=False)
                else:
                    print("No unaccessible major locations")

            items = s.smbm.getItems()
            print("ETank: {}, Reserve: {}, Missile: {}, Super: {}, PowerBomb: {}".format(items['ETank'], items['Reserve'], items['Missile'], items['Super'], items['PowerBomb']))
            print("Majors: {}".format(sorted([item for item in items if items[item] == 1])))

        # display difficulty scale
        self.displayDifficulty(s.difficulty)

    def displayDifficulty(self, difficulty):
        if difficulty >= 0:
            text = DifficultyDisplayer(difficulty).scale()
            print("Estimated difficulty: {}".format(text))
        else:
            print("Aborted run, can't finish the game with the given prerequisites")

class OutRando(OutConsole):
    def __init__(self, solver):
        self.solver = solver

    def out(self):
        pass
