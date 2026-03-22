import pygame
from random import randint


class Level:
    def __init__(self,data,audio_files):
        self.display_surface= pygame.display.get_surface()
        self.data = data
        self.delta = 0
        self.delta2 = 0
        self.audiofiles = audio_files
        self.data.timecap = self.data._timecap
        
        


    def currenttimespent(self,dt):
        if self.data.playingstate == 2:
            if self.data.currenttime > self.data.timecap:
                self.data.currenttime = self.data.timecap
            elif self.data.digits == 1 and self.data.currenttime > 9:
                self.data.currenttime = 9
                if self.data.points == 0:
                    self.data.points = 1
            elif self.data.digits == 2 and self.data.currenttime > 59:
                self.data.currenttime = 59
                if self.data.points == 0:
                    self.data.points = 1
            elif self.data.digits == 3 and self.data.currenttime > 599:
                self.data.currenttime = 599
                if self.data.points == 0:
                    self.data.points = 1
            elif self.data.digits == 4 and self.data.currenttime > 3599:
                self.data.currenttime = 3599
                if self.data.points == 0:
                    self.data.points = 1
            elif self.data.digits == 5 and self.data.currenttime > 35999:
                self.data.currenttime = 35999
                if self.data.points == 0:
                    self.data.points = 1
            elif self.data.digits == 6 and self.data.currenttime > 86399:
                self.data.currenttime = 86399
                if self.data.points == 0:
                    self.data.points = 1
            else:
                self.data.currenttime += dt * self.data.timescale
        else:
            self.data.currenttime = 0

    def maxtimespent(self):
        if self.data.currenttime > self.data.maxtime:
            self.data.maxtime = self.data.currenttime

    def changegamestate(self):
        check = 1.2
        if self.data.playingstate == 3 and self.delta > check:
            self.data.playingstate = 1
            self.delta = 0
        elif self.data.playingstate == 2 and self.delta > 0.7:
            self.data.playingstate = 3
            self.data.peaktime = self.data.currenttime
            self.delta = 0
            #print(self.data.peaktime)
        elif self.data.playingstate == 1 and self.delta > check:
            self.data.playingstate = 2
            self.delta = 0
        elif self.data.playingstate == 0:
            self.data.playingstate = 1
        self.data.forcestatechange = 0

    def checkgoal(self):
        if self.data.maxtime >= self.data.goal and self.data.goalled == False:
            self.data.playingstate = 5
            self.data.goalled = True
        
    def getpoints(self):
        if self.data.points < int(self.data.currenttime/600):
            self.data.points += 1
        
    def checkdigits(self):
        y = 1
        for x in range(6):
            y += self.data.shop[0][x+2][2]
        self.data.digits = y
            
    def sounds(self,data):
        y = randint(1,1000)
        soundcheck = 0
        if self.delta2 >= 20:
            pygame.mixer.music.set_volume(0.5)
        if data.shop[3][0][2] == 1 and self.delta2 > 20:
            if y == 1 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['metal-pipe'].play()
            elif y == 2 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['airhorn1'].play()
            elif y == 3 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['airhorn2'].play()
            elif y == 4 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['noot'].play()
        if data.shop[3][1][2] == 1 and self.delta2 > 20:
            if y == 5 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['pikmin1'].play()
            elif y == 6 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['pikmin2'].play()
            elif y == 7 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['pikmin3'].play()
        if data.shop[3][2][2] == 1 and self.delta2 > 20:
            if y == 8 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['grub1'].play()
            elif y == 9 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['grub2'].play()
            elif y == 10 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['grub3'].play()
            elif y == 11 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['grub4'].play()
            elif y == 12 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['grub5'].play()
            elif y == 13 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['grub6'].play()
            elif y == 14 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['grub7'].play()
            elif y == 15 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['grub8'].play()
            elif y == 16 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['grub9'].play()
        if data.shop[3][3][2] == 1 and self.delta2 > 20:
            if y == 17 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['bird1'].play()
            elif y == 18 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['bird2'].play()
            elif y == 19 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['bird3'].play()
        if data.shop[3][4][2] == 1 and self.delta2 > 20:
            if y == 20 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['aoe1'].play()
            elif y == 21 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['aoe2'].play()
            elif y == 22 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['aoe3'].play()
            elif y == 23 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['aoe4'].play()
            elif y == 24 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['aoe5'].play()
            elif y == 25 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['aoe6'].play()
        if data.shop[3][5][2] == 1 and self.delta2 > 20:
            if y == 26 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['zelda1'].play()
            elif y == 27 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['zelda2'].play()
            elif y == 28 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['zelda3'].play()
            elif y == 29 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['zelda4'].play()
            elif y == 30 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['zelda5'].play()
        if data.shop[3][6][2] == 1 and self.delta2 > 20:
            if y == 31 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['hotwheel'].play()
        if data.shop[3][7][2] == 1 and self.delta2 > 20:
            if y == 32 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['villager'].play()
            elif y == 33 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['weather1'].play()
            elif y == 34 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['weather2'].play()
            elif y == 35 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['weather3'].play()
            elif y == 36 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['weather4'].play()
        if data.shop[3][8][2] == 1 and self.delta2 > 20:
            if y == 37 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['creeper'].play()
            elif y == 38 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['discord-join'].play()
            elif y == 39 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['discord-leave'].play()
        if data.shop[3][9][2] == 1 and self.delta2 > 20:
            if y == 40 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['start1'].play()
                pygame.mixer.music.set_volume(0.05)
            elif y == 41 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['start2'].play()
                pygame.mixer.music.set_volume(0.05)
            elif y == 42 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['start3'].play()
                pygame.mixer.music.set_volume(0.05)
            elif y == 43 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['start4'].play()
                pygame.mixer.music.set_volume(0.05)
            elif y == 44 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['start5'].play()
                pygame.mixer.music.set_volume(0.05)
            elif y == 45 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['start6'].play()
                pygame.mixer.music.set_volume(0.05)
            elif y == 46 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['start7'].play()
                pygame.mixer.music.set_volume(0.05)
            elif y == 47 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['start8'].play()
                pygame.mixer.music.set_volume(0.05)
            elif y == 48 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['start9'].play()
                pygame.mixer.music.set_volume(0.05)
            elif y == 49 and soundcheck == 0:
                soundcheck = 1
                self.audiofiles['start10'].play()
                pygame.mixer.music.set_volume(0.05)
        if soundcheck == 1:
            self.delta2 = 0
            
            
            

    def run(self,dt):
        
        if self.data.playingstate > 0 and self.data.playingstate < 4:
            self.display_surface.fill(self.data.colors[self.data.colorselect][0])
            self.currenttimespent(dt)
            self.maxtimespent()
            self.getpoints()
            self.checkdigits()
            self.checkgoal()
            self.sounds(self.data)
            self.delta += dt
            self.delta2 += dt
        else:
            self.display_surface.fill(self.data.colors[self.data.colorselect][0])
        
        