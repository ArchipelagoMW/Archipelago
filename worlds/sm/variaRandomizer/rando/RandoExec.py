import sys, random, time, utils.log

from logic.logic import Logic
from graph.graph_utils import GraphUtils, getAccessPoint
from rando.Restrictions import Restrictions
from rando.RandoServices import RandoServices
from rando.GraphBuilder import GraphBuilder
from rando.RandoSetup import RandoSetup
from rando.Filler import FrontFiller
from rando.FillerProgSpeed import FillerProgSpeed, FillerProgSpeedChozoSecondPhase
from rando.FillerRandom import FillerRandom, FillerRandomSpeedrun
from rando.FillerScavenger import FillerScavenger
from rando.Chozo import ChozoFillerFactory, ChozoWrapperFiller
from rando.Items import ItemManager
from rando.ItemLocContainer import ItemLocation
from utils.vcr import VCR
from utils.doorsmanager import DoorsManager

# entry point for rando execution ("randomize" method)
class RandoExec(object):
    def __init__(self, seedName, vcr, randoSettings, graphSettings):
        self.errorMsg = ""
        self.seedName = seedName
        self.vcr = vcr
        self.randoSettings = randoSettings
        self.graphSettings = graphSettings
        self.log = utils.log.get('RandoExec')

    def getFillerFactory(self, progSpeed, endDate):
        if self.restrictions.split != "Scavenger":
            if progSpeed == "basic":
                return lambda cont: FrontFiller(self.graphSettings.startAP, self.areaGraph, self.restrictions, cont, endDate)
            elif progSpeed == "speedrun":
                return lambda cont: FillerRandomSpeedrun(self.graphSettings, self.areaGraph, self.restrictions, cont, endDate)
            else:
                return lambda cont: FillerProgSpeed(self.graphSettings, self.areaGraph, self.restrictions, cont, endDate)
        else:
            return lambda cont: FillerScavenger(self.graphSettings.startAP, self.areaGraph, self.restrictions, cont, endDate)

    def createFiller(self, container, endDate):
        progSpeed = self.randoSettings.progSpeed
        fact = self.getFillerFactory(progSpeed, endDate)
        if self.randoSettings.restrictions['MajorMinor'] != "Chozo":
            return fact(container)
        else:
            if progSpeed in ['basic', 'speedrun']:
                secondPhase = lambda cont, prog: FillerRandom(self.graphSettings.startAP, self.areaGraph, self.restrictions, cont, endDate, diffSteps=100)
            else:
                secondPhase = lambda cont, prog: FillerProgSpeedChozoSecondPhase(self.graphSettings.startAP, self.areaGraph, self.restrictions, cont, endDate)
            chozoFact = ChozoFillerFactory(fact, secondPhase)
            return ChozoWrapperFiller(self.randoSettings, container, chozoFact)

    # processes settings to :
    # - create Restrictions and GraphBuilder objects
    # - create graph and item loc container using a RandoSetup instance: in area rando, if it fails, iterate on possible graph layouts
    # - create filler based on progression speed and run it
    # return (isStuck, itemLocs, progItemLocs)
    def randomize(self):
        vcr = VCR(self.seedName, 'rando') if self.vcr == True else None
        self.errorMsg = ""
        split = self.randoSettings.restrictions['MajorMinor']
        graphBuilder = GraphBuilder(self.graphSettings)
        container = None
        i = 0
        attempts = 500 if self.graphSettings.areaRando or self.graphSettings.doorsColorsRando or split == 'Scavenger' else 1
        now = time.process_time()
        endDate = sys.maxsize
        if self.randoSettings.runtimeLimit_s < endDate:
            endDate = now + self.randoSettings.runtimeLimit_s
        self.updateLocationsClass(split)
        while container is None and i < attempts and now <= endDate:
            self.restrictions = Restrictions(self.randoSettings)
            if self.graphSettings.doorsColorsRando == True:
                DoorsManager.randomize(self.graphSettings.allowGreyDoors)
            self.areaGraph = graphBuilder.createGraph()
            services = RandoServices(self.areaGraph, self.restrictions)
            setup = RandoSetup(self.graphSettings, Logic.locations, services)
            container = setup.createItemLocContainer(endDate, vcr)
            if container is None:
                sys.stdout.write('*')
                sys.stdout.flush()
                i += 1
            else:
                self.errorMsg += '\n'.join(setup.errorMsgs)
            now = time.process_time()
        if container is None:
            if self.graphSettings.areaRando:
                self.errorMsg += "Could not find an area layout with these settings"
            else:
                self.errorMsg += "Unable to process settings"
        #    return (True, [], [])
        self.areaGraph.printGraph()
        return container
        #filler = self.createFiller(container, endDate)
        #self.log.debug("ItemLocContainer dump before filling:\n"+container.dump())
        #ret = filler.generateItems(vcr=vcr)
        #if not ret[0]:
        #    scavEscape = (ret[1], ret[2]) if self.restrictions.scavEscape else None
        #    escapeOk = graphBuilder.escapeGraph(container, self.areaGraph, self.randoSettings.maxDiff, scavEscape)
        #    if not escapeOk:
        #        self.errorMsg += "Could not find a solution for escape"
        #        ret = (True, ret[1], ret[2])
        #self.errorMsg += filler.errorMsg
        #return ret

    def updateLocationsClass(self, split):
        if split != 'Full' and split != 'Scavenger':
            startAP = getAccessPoint(self.graphSettings.startAP)
            possibleMajLocs, preserveMajLocs, nMaj, nChozo = Logic.LocationsHelper.getStartMajors(startAP.Name)
            if split == 'Major':
                n = nMaj
            elif split == 'Chozo':
                n = nChozo
            GraphUtils.updateLocClassesStart(startAP.GraphArea, split, possibleMajLocs, preserveMajLocs, n)

    def postProcessItemLocs(self, itemLocs, hide):
        # hide some items like in dessy's
        if hide == True:
            for itemLoc in itemLocs:
                item = itemLoc.Item
                loc = itemLoc.Location
                if (item.Category != "Nothing"
                    and loc.CanHidden == True
                    and loc.Visibility == 'Visible'):
                    if bool(random.getrandbits(1)) == True:
                        loc.Visibility = 'Hidden'
        # put nothing in unfilled locations
        filledLocNames = [il.Location.Name for il in itemLocs]
        unfilledLocs = [loc for loc in Logic.locations if loc.Name not in filledLocNames]
        nothing = ItemManager.getItem('Nothing')
        for loc in unfilledLocs:
            loc.restricted = True
            itemLocs.append(ItemLocation(nothing, loc, False))
