import sys, time

from ..utils import log
from ..logic.logic import Logic
from ..graph.graph_utils import GraphUtils, getAccessPoint
from ..rando.Restrictions import Restrictions
from ..rando.RandoServices import RandoServices
from ..rando.GraphBuilder import GraphBuilder
from ..rando.RandoSetup import RandoSetup
from ..rando.Items import ItemManager
from ..rando.ItemLocContainer import ItemLocation
from ..utils.vcr import VCR
from ..utils.doorsmanager import DoorsManager

# entry point for rando execution ("randomize" method)
class RandoExec(object):
    def __init__(self, seedName, vcr, randoSettings, graphSettings, player, random):
        self.errorMsg = ""
        self.seedName = seedName
        self.vcr = vcr
        self.randoSettings = randoSettings
        self.graphSettings = graphSettings
        self.log = log.get('RandoExec')
        self.player = player
        self.random = random

    # processes settings to :
    # - create Restrictions and GraphBuilder objects
    # - create graph and item loc container using a RandoSetup instance: in area rando, if it fails, iterate on possible graph layouts
    # return container
    def randomize(self):
        vcr = VCR(self.seedName, 'rando') if self.vcr == True else None
        self.errorMsg = ""
        split = self.randoSettings.restrictions['MajorMinor']
        self.graphBuilder = GraphBuilder(self.graphSettings, self.random)
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
                DoorsManager.randomize(self.graphSettings.allowGreyDoors, self.player, self.random)
            self.areaGraph = self.graphBuilder.createGraph(self.randoSettings.maxDiff)
            services = RandoServices(self.areaGraph, self.restrictions, random=self.random)
            setup = RandoSetup(self.graphSettings, Logic.locations[:], services, self.player, self.random)
            self.setup = setup
            container = setup.createItemLocContainer(endDate, vcr)
            if container is None:
                sys.stdout.write('*')
                i += 1
            else:
                self.errorMsg += '; '.join(setup.errorMsgs)
            now = time.process_time()
        if container is None:
            if self.graphSettings.areaRando:
                self.errorMsg += "Could not find an area layout with these settings; "
            if self.graphSettings.doorsColorsRando:
                self.errorMsg += "Could not find a door color combination with these settings; "
            if split == "Scavenger":
                self.errorMsg += "Scavenger seed generation timed out; "
            if setup.errorMsgs:
                self.errorMsg += '; '.join(setup.errorMsgs)
            if self.errorMsg == "":
                self.errorMsg += "Unable to process settings; "
            raise Exception(self.errorMsg)
        self.areaGraph.printGraph()
        return container

    def updateLocationsClass(self, split):
        if split != 'Full' and split != 'Scavenger':
            startAP = getAccessPoint(self.graphSettings.startAP)
            possibleMajLocs, preserveMajLocs, nMaj, nChozo = Logic.LocationsHelper.getStartMajors(startAP.Name)
            if split == 'Major':
                n = nMaj
            elif split == 'Chozo':
                n = nChozo
            GraphUtils.updateLocClassesStart(startAP.GraphArea, split, possibleMajLocs, preserveMajLocs, n, self.random)

    def postProcessItemLocs(self, itemLocs, hide):
        # hide some items like in dessy's
        if hide == True:
            for itemLoc in itemLocs:
                item = itemLoc.Item
                loc = itemLoc.Location
                if (item.Category != "Nothing"
                    and loc.CanHidden == True
                    and loc.Visibility == 'Visible'):
                    if bool(self.random.getrandbits(1)) == True:
                        loc.Visibility = 'Hidden'
        # put nothing in unfilled locations
        filledLocNames = [il.Location.Name for il in itemLocs]
        unfilledLocs = [loc for loc in Logic.locations if loc.Name not in filledLocNames]
        nothing = ItemManager.getItem('Nothing')
        for loc in unfilledLocs:
            loc.restricted = True
            itemLocs.append(ItemLocation(nothing, loc, False))
