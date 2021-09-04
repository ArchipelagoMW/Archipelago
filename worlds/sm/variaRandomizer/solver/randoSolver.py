import time

from logic.smboolmanager import SMBoolManagerPlando as SMBoolManager
from logic.helpers import Pickup
from solver.conf import Conf
from graph.graph_utils import getAccessPoint
from solver.comeback import ComeBack
from solver.standardSolver import StandardSolver
from utils.parameters import easy
from solver.out import Out
import utils.log

class RandoSolver(StandardSolver):
    def __init__(self, majorsSplit, startLocation, areaGraph, locations, vcr=None):
        self.interactive = False
        self.checkDuplicateMajor = False
        self.vcr = vcr
        # for compatibility with some common methods of the interactive solver
        self.mode = 'standard'

        self.log = utils.log.get('Solver')

        # default conf
        self.setConf(easy, 'all', [], False)

        self.firstLogFile = None

        self.extStatsFilename = None
        self.extStatsStep = None

        self.type = 'rando'
        self.output = Out.factory(self.type, self)
        self.outputFileName = None

        self.locations = locations

        self.smbm = SMBoolManager()

        # preset already loaded by rando
        self.presetFileName = None

        self.pickup = Pickup(Conf.itemsPickup)

        self.comeBack = ComeBack(self)

        # load ROM info, patches are already loaded by the rando. get the graph from the rando too
        self.majorsSplit = majorsSplit
        self.startLocation = startLocation
        self.startArea = getAccessPoint(startLocation).Start['solveArea']
        self.areaGraph = areaGraph

        # store at each step how many locations are available
        self.nbAvailLocs = []

        # limit to a few seconds to avoid cases with a lot of rewinds which could last for minutes
        self.runtimeLimit_s = 5
        self.startTime = time.process_time()
