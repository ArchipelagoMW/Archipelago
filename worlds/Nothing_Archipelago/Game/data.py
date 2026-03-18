import numpy

class Data:
    def __init__(self,ui):
        self.ui = ui
        self.milestoneint = 1
        self.archipelagoactive = False
        self.goal = 600
        self._milestonesforce = 1
        self._points = 0
        self.timecapint = 1

        self.WINDOW_WIDTH = 1920
        self.WINDOW_HEIGHT = 1080

        self.activeinput = 3
        self.inputs = [0 for _ in range(4)]
        self.inputs[0] = "Archipelago.gg"
        self.inputs[1] = "25655"
        self.inputs[2] = "Slot Name"
        self.inputs[3] = ""
        
        self.devcount = 0
        self.timescale = 1
        self.devmode = 0

        self.connected = 0
        self._maxtime = 0
        self._currenttime = 0
        self._playingstate = 0
        self._shopstate = 0
        self._peaktime = 0
        self._timecaps = 1
        self._forcestatechange = 0
        self._timecap = self.timecapint
        self._digits = 1
        self._colorselect = 0
        self._musicselect = 11
        self.currentsong = self._musicselect
        self.goalled = False
        self.leave = 0
        self._milestones = numpy.zeros((86400,4))
        
        self.names = [[0 for _ in range(4)] for _ in range (10)]
        self.names[0][0] = "Auto-restart      : "
        self.names[1][0] = "Auto-milestone   : "
        self.names[2][0] = "Unlock next Digit : "
        self.names[3][0] = "Unlock next Digit : "
        self.names[4][0] = "Unlock next Digit : "
        self.names[5][0] = "Unlock next Digit : "
        self.names[6][0] = "Unlock next Digit : "
        self.names[7][0] = "Unlock next Digit : "
        self.names[8][0] = ""
        self.names[9][0] = ""
        self.names[0][1] = "Gray       : "
        self.names[1][1] = "Blue        : "
        self.names[2][1] = "Green     : "
        self.names[3][1] = "Pink        : "
        self.names[4][1] = "White     : "
        self.names[5][1] = "Black      : "
        self.names[6][1] = "Orange  : "
        self.names[7][1] = "Yellow    : "
        self.names[8][1] = "Purple   : "
        self.names[9][1] = "Cyan      : "
        self.names[0][2] = "song1    : "
        self.names[1][2] = "song2   : "
        self.names[2][2] = "song3   : "
        self.names[3][2] = "song4   : "
        self.names[4][2] = "song5   : "
        self.names[5][2] = "song6   : "
        self.names[6][2] = "song7   : "
        self.names[7][2] = "song8   : "
        self.names[8][2] = "song9   : "
        self.names[9][2] = "song10 : "
        self.names[0][3] = "Sound1    : "
        self.names[1][3] = "Sound2   : "
        self.names[2][3] = "Sound2   : "
        self.names[3][3] = "Sound2   : "
        self.names[4][3] = "Sound2   : "
        self.names[5][3] = "Sound2   : "
        self.names[6][3] = "Sound2   : "
        self.names[7][3] = "Sound2   : "
        self.names[8][3] = "Sound2   : "
        self.names[9][3] = "Sound10 : "
        self.colors =[[0 for _ in range (2)] for _ in range (11)]
        self.colors[0][0] = (100,100,100)
        self.colors[0][1] = (255,255,255)
        self.colors[1][0] = (0,0,255)
        self.colors[1][1] = (255,255,255)
        self.colors[2][0] = (35,140,35)
        self.colors[2][1] = (255,255,255)
        self.colors[3][0] = (255,0,255)
        self.colors[3][1] = (255,255,255)
        self.colors[4][0] = (255,255,255)
        self.colors[4][1] = (0,0,0)
        self.colors[5][0] = (0,0,0)
        self.colors[5][1] = (255,255,255)
        self.colors[6][0] = (255,140,0)
        self.colors[6][1] = (255,255,255)
        self.colors[7][0] = (255,255,0)
        self.colors[7][1] = (0,0,0)
        self.colors[8][0] = (140,0,140)
        self.colors[8][1] = (255,255,255)
        self.colors[9][0] = (0,140,140)
        self.colors[9][1] = (255,255,255)
        self.colors[10][0] = (0,0,0)
        self.colors[10][1] = (40,200,40)
        for x in range(86400):
            self._milestones[x,0] = (x+1)*self.milestoneint
            self._milestones[x,2] = x+1
        self._shop = [[[0 for _ in range (4)] for _ in range (10)] for _ in range (4)]
        self._shop[1][0][1] = 1
        self._shop[1][0][2] = 1
        for x in range (4):
            for y in range (10):
                if x == 0 and y > 1:
                    self._shop[x][y][3] = 1
                else:
                    self._shop[x][y][3] = 2
        self._shop[0][8][3] = ""
        self._shop[0][9][3] = ""
        

    @property
    def currenttime(self):
        return self._currenttime
    
    @currenttime.setter
    def currenttime(self,value):
        self._currenttime = value
        self.ui.timer(self.currenttime)

    @property
    def maxtime(self):
        return self._maxtime
    
    @maxtime.setter
    def maxtime(self,value):
        self._maxtime = value
        self.ui.maxtimer(self.maxtime)

    @property
    def peaktime(self):
        return self._peaktime
    
    @peaktime.setter
    def peaktime(self,value):
        self._peaktime = value
        self.ui.peaktimer(self.peaktime)
    
    @property
    def points(self):
        return self._points
    
    @points.setter
    def points(self,value):
        self._points = value
        self.ui.pointer(self.points)

    @property
    def playingstate(self):
        return self._playingstate
    
    @playingstate.setter
    def playingstate(self,value):
        self._playingstate = value
        self.ui.playingstater(self.playingstate)

    @property
    def shopstate(self):
        return self._shopstate
    
    @shopstate.setter
    def shopstate(self,value):
        self._shopstate = value
        self.ui.shopstater(self.shopstate)

    @property
    def timecap(self):
        return self._timecap
    
    @timecap.setter
    def timecap(self,value):
        self._timecap = value
        self.ui.timecaper(self.timecap)

    @property
    def timecaps(self):
        return self._timecaps
    
    @timecaps.setter
    def timecaps(self,value):
        self._timecaps = value
        self.ui.timecapser(self.timecaps)

    @property
    def digits(self):
        return self._digits
    
    @digits.setter
    def digits(self,value):
        self._digits = value
        self.ui.digitser(self.digits)

    @property
    def forcestatechange(self):
        return self._forcestatechange
    
    @forcestatechange.setter
    def forcestatechange(self,value):
        self._forcestatechange = value
        self.ui.forcestatechanger(self.forcestatechange)

    @property
    def milestonesforce(self):
        return self._milestonesforce
    
    @milestonesforce.setter
    def milestonesforce(self,value):
        self._milestonesforce = value
        self.ui.milestoneforcer(self.milestonesforce)

    @property
    def milestones(self):
        return self._milestones
    
    @milestones.setter
    def milestones(self,value,row):
        self._milestones[row,1] = value
        self.ui.milestoner(self.milestones)

    @property
    def shop(self):
        return self._shop
    
    @shop.setter
    def shop(self,value,state,position,row):
        self._shop[state][position][row] = value
        self.ui.shoper(self.shop)

    @property
    def colorselect(self):
        return self._colorselect
    
    @colorselect.setter
    def colorselect(self,value):
        self._colorselect = value
        self.ui.colorselecter(self.colorselect)

    @property
    def musicselect(self):
        return self._musicselect
    
    @musicselect.setter
    def musicselect(self,value):
        self._musicselect = value
        self.ui.musicselecter(self.musicselect)
        