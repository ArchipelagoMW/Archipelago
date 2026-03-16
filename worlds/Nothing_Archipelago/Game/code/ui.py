from settings import *
from buttons import Button



class UI:
    def __init__(self, font, font2, font3, frames):
        self.display_surface = pygame.display.get_surface()
        self.font = font
        self.font2 = font2
        self.font3 = font3

        self.delta = 0
        self.delta2 = 0
        
        #Timer
        self.current_time = 0
        self.max_time = 0
        self.time_points = 0
        self.playing_state = 0
        self.playing_state
        self.force_state_change = 0
        self.milestones_force = 1
        self.peak_time = 0
        self.time_cap = 0
        self.time_caps = 1
        self.digit_s = 1
        self.music_select = 0
        self.color_select = 0
        self.shops = [[[0 for _ in range (4)] for _ in range (10)] for _ in range (4)]
        self.sound_s = [0 for _ in range(10)]
        self.gear_surf = frames['gear']
        self.mile_stones = numpy.zeros((86400,4))
        self.StartButton = Button(self.font,"Start Doing Nothing",WINDOW_WIDTH/2,WINDOW_HEIGHT/2,(255,255,255),0)
        self.quitbutton = Button(self.font,"Quit Doing Nothing",WINDOW_WIDTH/2,WINDOW_HEIGHT/2+80,(255,255,255),0)
        self.backbutton = Button(self.font,"Return to Menu",WINDOW_WIDTH-160,WINDOW_HEIGHT-40,(255,255,255),0)
        self.fullscreenbutton = Button(self.font,"Toggle Fullscreen",WINDOW_WIDTH/2,WINDOW_HEIGHT-40,(255,255,255),0)
        self.milestone1button = Button(self.font,"Milestone1",WINDOW_WIDTH-160,WINDOW_HEIGHT/2,(255,255,255),0)
        self.milestone2button = Button(self.font,"Milestone2",WINDOW_WIDTH-160,WINDOW_HEIGHT/2,(255,255,255),0)
        self.milestone3button = Button(self.font,"Milestone3",WINDOW_WIDTH-160,WINDOW_HEIGHT/2,(255,255,255),0)
        self.milestone4button = Button(self.font,"Milestone4",WINDOW_WIDTH-160,WINDOW_HEIGHT/2,(255,255,255),0)
        self.milestone5button = Button(self.font,"Milestone5",WINDOW_WIDTH-160,WINDOW_HEIGHT/2,(255,255,255),0)
        self.nextshopbutton = Button(self.font, "Next page", 280,WINDOW_HEIGHT/4,(255,255,255),0)
        self.prevshopbutton = Button(self.font, "Prev page",100,WINDOW_HEIGHT/4,(255,255,255),0)
        self.shopbutton1 = Button(self.font, "shop1",80,WINDOW_HEIGHT/4+40,(255,255,255),0)
        self.shopbutton2 = Button(self.font, "shop2",80,WINDOW_HEIGHT/4+80,(255,255,255),0)
        self.shopbutton3 = Button(self.font, "shop3",80,WINDOW_HEIGHT/4+120,(255,255,255),0)
        self.shopbutton4 = Button(self.font, "shop4",80,WINDOW_HEIGHT/4+160,(255,255,255),0)
        self.shopbutton5 = Button(self.font, "shop5",80,WINDOW_HEIGHT/4+200,(255,255,255),0)
        self.shopbutton6 = Button(self.font, "shop6",80,WINDOW_HEIGHT/4+240,(255,255,255),0)
        self.shopbutton7 = Button(self.font, "shop7",80,WINDOW_HEIGHT/4+280,(255,255,255),0)
        self.shopbutton8 = Button(self.font, "shop8",80,WINDOW_HEIGHT/4+320,(255,255,255),0)
        self.shopbutton9 = Button(self.font, "shop9",80,WINDOW_HEIGHT/4+360,(255,255,255),0)
        self.shopbutton10 = Button(self.font, "shop10",80,WINDOW_HEIGHT/4+400,(255,255,255),0)
        self.continuebutton = Button(self.font, "[CONTINUE]",WINDOW_WIDTH/2,WINDOW_HEIGHT/2+160,(255,255,255),0)
        self.archipelagobutton = Button(self.font, "Archipelago",WINDOW_WIDTH/2,WINDOW_HEIGHT/2+40,(255,255,255),0)
        #max timer


    def display_timer(self,data):
        seconds = int(self.current_time) % 60
        minutes = int(self.current_time/60) % 60
        hours = int(self.current_time/3600) % 24
        days = int(self.current_time/86400)
        if days > 0:
            timeformated = str(days) + " days, " + str(hours) + " hours, " + str(minutes) + " minutes, and " + str(seconds) + " seconds"
        elif hours > 0:
            timeformated = str(hours) + " hours, " + str(minutes) + " minutes, and " + str(seconds) + " seconds"
        elif minutes > 0:
            timeformated = str(minutes) + " minutes and " + str(seconds) + " seconds"
        else:
            timeformated = str(seconds) + " seconds"
        
        pseconds = int(self.peak_time) % 60
        pminutes = int(self.peak_time/60) % 60
        phours = int(self.peak_time/3600) % 24
        pdays = int(self.peak_time/86400)
        if pdays > 0:
            ptimeformated = str(pdays) + " days, " + str(phours) + " hours, " + str(pminutes) + " minutes, and " + str(pseconds) + " seconds"
        elif phours > 0:
            ptimeformated = str(phours) + " hours, " + str(pminutes) + " minutes, and " + str(pseconds) + " seconds"
        elif pminutes > 0:
            ptimeformated = str(pminutes) + " minutes and " + str(pseconds) + " seconds"
        else:
            ptimeformated = str(pseconds) + " seconds"
        
        if self.playing_state == 1:
            text_surf6 = self.font.render("Press any key to start doing nothing",False,data.colors[data.colorselect][1])
            text_rect6 = text_surf6.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
            self.display_surface.blit(text_surf6, text_rect6)
        elif self.playing_state == 2:
            text_surf6 = self.font.render("You have been doing Nothing for ",False,data.colors[data.colorselect][1])
            text_rect6 = text_surf6.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2-20))
            text_surf7 = self.font.render(timeformated,False,data.colors[data.colorselect][1])
            text_rect7 = text_surf7.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2+20))
            self.display_surface.blit(text_surf6, text_rect6)
            self.display_surface.blit(text_surf7, text_rect7)
        elif self.playing_state == 3:
            text_surf6 = self.font.render(str("You did Something, you lost"),False,data.colors[data.colorselect][1])
            text_rect6 = text_surf6.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2-20))
            text_surf7 = self.font.render("You did Nothing for "+ptimeformated,False,data.colors[data.colorselect][1])
            text_rect7 = text_surf7.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2+20))
            self.display_surface.blit(text_surf6, text_rect6)
            self.display_surface.blit(text_surf7, text_rect7)
              
    def display_maxtimer(self,data):
        seconds = int(self.max_time) % 60
        minutes = int(self.max_time/60) % 60
        hours = int(self.max_time/3600) % 24
        days = int(self.max_time/86400)
        if days > 0:
            timeformated = str(days) + " days, " + str(hours) + " hours, " + str(minutes) + " minutes, and " + str(seconds) + " seconds"
        elif hours > 0:
            timeformated = str(hours) + " hours, " + str(minutes) + " minutes, and " + str(seconds) + " seconds"
        elif minutes > 0:
            timeformated = str(minutes) + " minutes and " + str(seconds) + " seconds"
        else:
            timeformated = str(seconds) + " seconds"
        text_surf5 = self.font.render("Longest time spent doing Nothing: "+timeformated,False,data.colors[data.colorselect][1])
        text_rect5 = text_surf5.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT-40))
        self.display_surface.blit(text_surf5, text_rect5)

    def display_shop(self,data):
        text_surf4 = self.font.render("Shop",False,data.colors[data.colorselect][1])
        text_rect4 = text_surf4.get_frect(center = (200,WINDOW_HEIGHT/4-40))
        self.display_surface.blit(text_surf4, text_rect4)
        

        if self.nextshopbutton.draw(self.display_surface) and self.delta > 0.5:
            if data.shopstate == 3:
                data.shopstate = 0
            else:
                data.shopstate += 1
            self.delta = 0
            
        if self.prevshopbutton.draw(self.display_surface) and self.delta > 0.5:
            if data.shopstate == 0:
                data.shopstate = 3
            else:
                data.shopstate -= 1
            self.delta = 0
        
        self.shopbutton1.updatetl(data.shop[data.shopstate][0][0],40,WINDOW_HEIGHT/4+20,data.colors[data.colorselect][1],0)
        self.shopbutton2.updatetl(data.shop[data.shopstate][1][0],40,WINDOW_HEIGHT/4+60,data.colors[data.colorselect][1],0)
        self.shopbutton3.updatetl(data.shop[data.shopstate][2][0],40,WINDOW_HEIGHT/4+100,data.colors[data.colorselect][1],0)
        self.shopbutton4.updatetl(data.shop[data.shopstate][3][0],40,WINDOW_HEIGHT/4+140,data.colors[data.colorselect][1],0)
        self.shopbutton5.updatetl(data.shop[data.shopstate][4][0],40,WINDOW_HEIGHT/4+180,data.colors[data.colorselect][1],0)
        self.shopbutton6.updatetl(data.shop[data.shopstate][5][0],40,WINDOW_HEIGHT/4+220,data.colors[data.colorselect][1],0)
        self.shopbutton7.updatetl(data.shop[data.shopstate][6][0],40,WINDOW_HEIGHT/4+260,data.colors[data.colorselect][1],0)
        self.shopbutton8.updatetl(data.shop[data.shopstate][7][0],40,WINDOW_HEIGHT/4+300,data.colors[data.colorselect][1],0)
        self.shopbutton9.updatetl(data.shop[data.shopstate][8][0],40,WINDOW_HEIGHT/4+340,data.colors[data.colorselect][1],0)
        self.shopbutton10.updatetl(data.shop[data.shopstate][9][0],40,WINDOW_HEIGHT/4+380,data.colors[data.colorselect][1],0)

        self.nextshopbutton.updatec("Next page", 280,WINDOW_HEIGHT/4,data.colors[data.colorselect][1],0)
        self.prevshopbutton.updatec("Prev page",100,WINDOW_HEIGHT/4,data.colors[data.colorselect][1],0)
        self.StartButton.updatec("Start Doing Nothing",WINDOW_WIDTH/2,WINDOW_HEIGHT/2,data.colors[data.colorselect][1],0)
        self.quitbutton.updatec("Quit Doing Nothing",WINDOW_WIDTH/2,WINDOW_HEIGHT/2+80,data.colors[data.colorselect][1],0)
        self.archipelagobutton.updatec("Archipelago",WINDOW_WIDTH/2,WINDOW_HEIGHT/2+40,data.colors[data.colorselect][1],0)
        self.backbutton.updatec("Return to Menu",WINDOW_WIDTH-160,WINDOW_HEIGHT-40,data.colors[data.colorselect][1],0)
        self.fullscreenbutton.updatec("Toggle Fullscreen",WINDOW_WIDTH/2,WINDOW_HEIGHT-40,data.colors[data.colorselect][1],0)

        if self.shopbutton1.draw(self.display_surface):
            if data.points >= data.shop[data.shopstate][0][3] and data.shop[data.shopstate][0][1] == 0:
                data.points -= data.shop[data.shopstate][0][3]
                data.shop[data.shopstate][0][1] = 1
                if data.archipelagoactive == False:
                    data.shop[data.shopstate][0][2] = 1
            elif data.shopstate == 1 and data.shop[data.shopstate][0][2] == 1:
                    data.colorselect = 0
            elif data.shopstate == 2 and data.shop[data.shopstate][0][2] == 1:
                    data.musicselect = 0

        if self.shopbutton2.draw(self.display_surface):
            if data.points >= data.shop[data.shopstate][1][3] and data.shop[data.shopstate][1][1] == 0:
                data.points -= data.shop[data.shopstate][1][3]
                data.shop[data.shopstate][1][1] = 1
                if data.archipelagoactive == False:
                    data.shop[data.shopstate][1][2] = 1
            elif data.shopstate == 1 and data.shop[data.shopstate][1][2] == 1:
                    data.colorselect = 1
            elif data.shopstate == 2 and data.shop[data.shopstate][1][2] == 1:
                    data.musicselect = 1
        
        if self.shopbutton3.draw(self.display_surface):
            if data.points >= data.shop[data.shopstate][2][3] and data.shop[data.shopstate][2][1] == 0:
                data.points -= data.shop[data.shopstate][2][3]
                data.shop[data.shopstate][2][1] = 1
                if data.archipelagoactive == False:
                    data.shop[data.shopstate][2][2] = 1
            elif data.shopstate == 1 and data.shop[data.shopstate][2][2] == 1:
                    data.colorselect = 2
            elif data.shopstate == 2 and data.shop[data.shopstate][2][2] == 1:
                    data.musicselect = 2

        if self.shopbutton4.draw(self.display_surface):
            if data.points >= data.shop[data.shopstate][3][3] and data.shop[data.shopstate][3][1] == 0:
                data.points -= data.shop[data.shopstate][3][3]
                data.shop[data.shopstate][3][1] = 1
                if data.archipelagoactive == False:
                    data.shop[data.shopstate][3][2] = 1
            elif data.shopstate == 1 and data.shop[data.shopstate][3][2] == 1:
                    data.colorselect = 3
            elif data.shopstate == 2 and data.shop[data.shopstate][3][2] == 1:
                    data.musicselect = 3

        if self.shopbutton5.draw(self.display_surface):
            if data.points >= data.shop[data.shopstate][4][3] and data.shop[data.shopstate][4][1] == 0:
                data.points -= data.shop[data.shopstate][4][3]
                data.shop[data.shopstate][4][1] = 1
                if data.archipelagoactive == False:
                    data.shop[data.shopstate][4][2] = 1
            elif data.shopstate == 1 and data.shop[data.shopstate][4][2] == 1:
                    data.colorselect = 4
            elif data.shopstate == 2 and data.shop[data.shopstate][4][2] == 1:
                    data.musicselect = 4

        if self.shopbutton6.draw(self.display_surface):
            if data.points >= data.shop[data.shopstate][5][3] and data.shop[data.shopstate][5][1] == 0:
                data.points -= data.shop[data.shopstate][5][3]
                data.shop[data.shopstate][5][1] = 1
                if data.archipelagoactive == False:
                    data.shop[data.shopstate][5][2] = 1
            elif data.shopstate == 1 and data.shop[data.shopstate][5][2] == 1:
                    data.colorselect = 5
            elif data.shopstate == 2 and data.shop[data.shopstate][5][2] == 1:
                    data.musicselect = 5

        if self.shopbutton7.draw(self.display_surface):
            if data.points >= data.shop[data.shopstate][6][3] and data.shop[data.shopstate][6][1] == 0:
                data.points -= data.shop[data.shopstate][6][3]
                data.shop[data.shopstate][6][1] = 1
                if data.archipelagoactive == False:
                    data.shop[data.shopstate][6][2] = 1
            elif data.shopstate == 1 and data.shop[data.shopstate][6][2] == 1:
                    data.colorselect = 6
            elif data.shopstate == 2 and data.shop[data.shopstate][6][2] == 1:
                    data.musicselect = 6

        if self.shopbutton8.draw(self.display_surface):
            if data.points >= data.shop[data.shopstate][7][3] and data.shop[data.shopstate][7][1] == 0:
                data.points -= data.shop[data.shopstate][7][3]
                data.shop[data.shopstate][7][1] = 1
                if data.archipelagoactive == False:
                    data.shop[data.shopstate][7][2] = 1
            elif data.shopstate == 1 and data.shop[data.shopstate][7][2] == 1:
                    data.colorselect = 7
            elif data.shopstate == 2 and data.shop[data.shopstate][7][2] == 1:
                    data.musicselect = 7

        if self.shopbutton9.draw(self.display_surface):
            if data.points >= data.shop[data.shopstate][8][3] and data.shop[data.shopstate][8][1] == 0:
                data.points -= data.shop[data.shopstate][8][3]
                data.shop[data.shopstate][8][1] = 1
                if data.archipelagoactive == False:
                    data.shop[data.shopstate][8][2] = 1
            elif data.shopstate == 1 and data.shop[data.shopstate][8][2] == 1:
                    data.colorselect = 8
            elif data.shopstate == 2 and data.shop[data.shopstate][8][2] == 1:
                    data.musicselect = 8

        if self.shopbutton10.draw(self.display_surface):
            if data.points >= data.shop[data.shopstate][9][3] and data.shop[data.shopstate][9][1] == 0:
                data.points -= data.shop[data.shopstate][9][3]
                data.shop[data.shopstate][9][1] = 1
                if data.archipelagoactive == False:
                    data.shop[data.shopstate][9][2] = 1
            elif data.shopstate == 1 and data.shop[data.shopstate][9][2] == 1:
                    data.colorselect = 9
            elif data.shopstate == 2 and data.shop[data.shopstate][9][2] == 1:
                    data.musicselect = 9

        for i in range(10):
            if data.shopstate == 1 and data.colorselect == i and data.shop[data.shopstate][i][2] == 1:
                extra = "Selected"
            elif data.shopstate == 2 and data.musicselect == i and data.shop[data.shopstate][i][2] == 1:
                extra = "Selected"
            elif (data.shopstate == 0 or data.shopstate == 3) and data.shop[data.shopstate][i][1] == 1:
                data.names[i][data.shopstate] = "SOLD OUT"
                extra = ""
            elif data.shop[data.shopstate][i][1] == 1 and data.shop[data.shopstate][i][2] == 0:
                extra = ""
            elif data.shop[data.shopstate][i][1] == 1 and data.shop[data.shopstate][i][2] == 1:
                extra = "Owned"
            elif data.shop[data.shopstate][i][1] == 0:
                extra = data.shop[data.shopstate][i][3]
            data.shop[data.shopstate][i][0] = data.names[i][data.shopstate] + str(extra)

        

    
    def display_pointer(self,data):
        text_surf = self.font.render("Time Coins : "+str(data.points),False,data.colors[data.colorselect][1])
        text_rect = text_surf.get_frect(center = (WINDOW_WIDTH/2,40))
        self.display_surface.blit(text_surf, text_rect)

    def display_digits(self,data):
        text_surf3 = self.font.render("Timer Digits : "+str(data.digits),False,data.colors[data.colorselect][1])
        text_rect3 = text_surf3.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2+100))
        self.display_surface.blit(text_surf3, text_rect3)

    def display_timecap(self,data):
        seconds = int(data.timecap) % 60
        minutes = int(data.timecap/60) % 60
        hours = int(data.timecap/3600) % 24
        days = int(data.timecap/86400)
        if days > 0:
            timeformated = str(days) + " days, " + str(hours) + " hours, " + str(minutes) + " minutes, and " + str(seconds) + " seconds"
        elif hours > 0:
            timeformated = str(hours) + " hours, " + str(minutes) + " minutes, and " + str(seconds) + " seconds"
        elif minutes > 0:
            timeformated = str(minutes) + " minutes and " + str(seconds) + " seconds"
        else:
            timeformated = str(seconds) + " seconds"
        text_surf2 = self.font.render("Time Cap : "+timeformated,False,data.colors[data.colorselect][1])
        text_rect2 = text_surf2.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2+60))
        self.display_surface.blit(text_surf2, text_rect2)

    def display_startmenu(self,data):
        text_surf = self.font2.render("NOTHING",False,data.colors[data.colorselect][1])
        text_rect = text_surf.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2-360))
        self.display_surface.blit(text_surf, text_rect)
        text_surf2 = self.font3.render("A Sisyphean Journey",False,data.colors[data.colorselect][1])
        text_rect5 = text_surf2.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2-200))
        self.display_surface.blit(text_surf2, text_rect5)
        if self.StartButton.draw(self.display_surface):
            data.playingstate = 1
        if self.archipelagobutton.draw(self.display_surface):
            data.playingstate = 4
        if self.quitbutton.draw(self.display_surface):
            data.leave = 1
        if self.fullscreenbutton.draw(self.display_surface):
            pygame.display.toggle_fullscreen()

    def display_interactables(self,data):
        text_surf8 = self.font.render("Milestones : ",False,data.colors[data.colorselect][1])
        text_rect8 = text_surf8.get_frect(topright = (WINDOW_WIDTH,WINDOW_HEIGHT/4-20))
        self.display_surface.blit(text_surf8, text_rect8)
        if self.backbutton.draw(self.display_surface):
            data.playingstate = 0
            self.playing_state = 0
        if data.shop[0][1][2] == 1 and self.max_time > self.milestone1button.value and self.delta > 0.5:
            test = int(self.milestone1button.value/data.milestoneint)-1
            data.milestones[test,1] = 1
            data.milestones[test,0] = 0
            if data.archipelagoactive == False:
                 data.timecaps += 1
            data.timecap = data.timecaps * data.timecapint
            self.milestone1button.value = 0
            self.delta = 0
            if data.milestonesforce == 1:
                 data.forcestatechange = 1
        if self.milestone1button.value == 0 or self.milestone2button.value == 0 or self.milestone3button.value == 0 or self.milestone4button.value == 0 or self.milestone5button.value ==0 or True:
            looping = True
            i = 0
            loc = 0
            while looping:
                if data.milestones[i,1] == 1:
                    i+=1
                else:
                    loc += 1
                    seconds = int(data.milestones[i,0]) % 60
                    minutes = int(data.milestones[i,0]/60) % 60
                    hours = int(data.milestones[i,0]/3600) % 24
                    days = int(data.milestones[i,0]/86400)
                    if days > 0:
                        timeformated = str(days) + " days, " + str(hours) + " hours, " + str(minutes) + " minutes, and " + str(seconds) + " seconds"
                    elif hours > 0:
                        timeformated = str(hours) + " hours, " + str(minutes) + " minutes, and " + str(seconds) + " seconds"
                    elif minutes > 0:
                        timeformated = str(minutes) + " minutes and " + str(seconds) + " seconds"
                    else:
                        timeformated = str(seconds) + " seconds"
                    if loc == 1:
                        self.milestone1button.updatetr(timeformated + " Milestone",WINDOW_WIDTH,WINDOW_HEIGHT/4+20,data.colors[data.colorselect][1],data.milestones[i,0])
                        if i == data.goal:
                            self.milestone2button.finished("Milestone Completed",WINDOW_WIDTH,WINDOW_HEIGHT/4+60,data.colors[data.colorselect][1],1)
                            self.milestone3button.finished("Milestone Completed",WINDOW_WIDTH,WINDOW_HEIGHT/4+100,data.colors[data.colorselect][1],1)
                            self.milestone4button.finished("Milestone Completed",WINDOW_WIDTH,WINDOW_HEIGHT/4+140,data.colors[data.colorselect][1],1)
                            self.milestone5button.finished("Milestone Completed",WINDOW_WIDTH,WINDOW_HEIGHT/4+180,data.colors[data.colorselect][1],1)
                    elif loc == 2:
                        self.milestone2button.updatetr(timeformated + " Milestone",WINDOW_WIDTH,WINDOW_HEIGHT/4+60,data.colors[data.colorselect][1],data.milestones[i,0])
                        if i == data.goal:
                            self.milestone3button.finished("Milestone Completed",WINDOW_WIDTH,WINDOW_HEIGHT/4+100,data.colors[data.colorselect][1],1)
                            self.milestone4button.finished("Milestone Completed",WINDOW_WIDTH,WINDOW_HEIGHT/4+140,data.colors[data.colorselect][1],1)
                            self.milestone5button.finished("Milestone Completed",WINDOW_WIDTH,WINDOW_HEIGHT/4+180,data.colors[data.colorselect][1],1)
                    elif loc == 3:
                        self.milestone3button.updatetr(timeformated + " Milestone",WINDOW_WIDTH,WINDOW_HEIGHT/4+100,data.colors[data.colorselect][1],data.milestones[i,0])
                        if i == data.goal:
                            self.milestone4button.finished("Milestone Completed",WINDOW_WIDTH,WINDOW_HEIGHT/4+140,data.colors[data.colorselect][1],1)
                            self.milestone5button.finished("Milestone Completed",WINDOW_WIDTH,WINDOW_HEIGHT/4+180,data.colors[data.colorselect][1],1)
                    elif loc == 4:
                        self.milestone4button.updatetr(timeformated + " Milestone",WINDOW_WIDTH,WINDOW_HEIGHT/4+140,data.colors[data.colorselect][1],data.milestones[i,0])
                        if i == data.goal:
                            self.milestone5button.finished("Milestone Completed",WINDOW_WIDTH,WINDOW_HEIGHT/4+180,data.colors[data.colorselect][1],1)
                    elif loc == 5:
                        self.milestone5button.updatetr(timeformated + " Milestone",WINDOW_WIDTH,WINDOW_HEIGHT/4+180,data.colors[data.colorselect][1],data.milestones[i,0])
                        looping = False
                    elif i == data.goal:
                        self.milestone1button.finished("Milestone Completed",WINDOW_WIDTH,WINDOW_HEIGHT/4+20,data.colors[data.colorselect][1],1)
                        self.milestone2button.finished("Milestone Completed",WINDOW_WIDTH,WINDOW_HEIGHT/4+60,data.colors[data.colorselect][1],1)
                        self.milestone3button.finished("Milestone Completed",WINDOW_WIDTH,WINDOW_HEIGHT/4+100,data.colors[data.colorselect][1],1)
                        self.milestone4button.finished("Milestone Completed",WINDOW_WIDTH,WINDOW_HEIGHT/4+140,data.colors[data.colorselect][1],1)
                        self.milestone5button.finished("Milestone Completed",WINDOW_WIDTH,WINDOW_HEIGHT/4+180,data.colors[data.colorselect][1],1)
                    i+=1
        if self.milestone1button.draw(self.display_surface) and self.max_time > self.milestone1button.value and self.delta > 0.5:
            test = int(self.milestone1button.value/data.milestoneint)-1
            data.milestones[test,1] = 1
            data.milestones[test,0] = 0
            if data.archipelagoactive == False:
                 data.timecaps += 1
            data.timecap = data.timecaps * data.timecapint
            self.milestone1button.value = 0
            self.delta = 0
        if self.milestone2button.draw(self.display_surface) and self.max_time > self.milestone2button.value and self.delta > 0.5:
            test = int(self.milestone2button.value/data.milestoneint)-1
            data.milestones[test,1] = 1
            data.milestones[test,0] = 0
            if data.archipelagoactive == False:
                 data.timecaps += 1
            data.timecap = data.timecaps * data.timecapint
            self.milestone2button.value = 0
            self.delta = 0
        if self.milestone3button.draw(self.display_surface) and self.max_time > self.milestone3button.value and self.delta > 0.5:
            test = int(self.milestone3button.value/data.milestoneint)-1
            data.milestones[test,1] = 1
            data.milestones[test,0] = 0
            if data.archipelagoactive == False:
                 data.timecaps += 1
            data.timecap = data.timecaps * data.timecapint
            self.milestone3button.value = 0
            self.delta = 0
        if self.milestone4button.draw(self.display_surface) and self.max_time > self.milestone4button.value and self.delta > 0.5:
            test = int(self.milestone4button.value/data.milestoneint)-1
            data.milestones[test,1] = 1
            data.milestones[test,0] = 0
            if data.archipelagoactive == False:
                 data.timecaps += 1
            data.timecap = data.timecaps * data.timecapint
            self.milestone4button.value = 0
            self.delta = 0
        if self.milestone5button.draw(self.display_surface) and self.max_time > self.milestone5button.value and self.delta > 0.5:
            test = int(self.milestone5button.value/data.milestoneint)-1
            data.milestones[test,1] = 1
            data.milestones[test,0] = 0
            if data.archipelagoactive == False:
                 data.timecaps += 1
            data.timecap = data.timecaps * data.timecapint
            self.milestone5button.value = 0
            self.delta = 0


    def Display_victory(self,data):
        text_surf = self.font.render("You did it...",False,data.colors[data.colorselect][1])
        text_rect = text_surf.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2-120))
        self.display_surface.blit(text_surf, text_rect)
        if self.delta2 > 2 :
            text_surf2 = self.font.render("You did nothing for...",False,data.colors[data.colorselect][1])
            text_rect2 = text_surf2.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2-80))
            self.display_surface.blit(text_surf2, text_rect2)
            if self.delta2 >4 :
                text_surf3 = self.font.render(str(data.goal) +" Seconds",False,data.colors[data.colorselect][1])
                text_rect3 = text_surf3.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2-40))
                self.display_surface.blit(text_surf3, text_rect3)
                if self.delta2 > 6:
                    text_surf4 = self.font.render("Why...",False,data.colors[data.colorselect][1])
                    text_rect4 = text_surf4.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
                    self.display_surface.blit(text_surf4, text_rect4)
                    if self.delta2 > 8:
                        text_surf5 = self.font.render("You know there are real games you can play right?",False,data.colors[data.colorselect][1])
                        text_rect5 = text_surf5.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2+40))
                        self.display_surface.blit(text_surf5, text_rect5)
                        if self.delta2 > 10:
                            text_surf6 = self.font.render("Well you've already come this far...",False,data.colors[data.colorselect][1])
                            text_rect6 = text_surf6.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2+80))
                            self.display_surface.blit(text_surf6, text_rect6)
                            if self.delta2 > 12:
                                text_surf7 = self.font.render("So why stop now",False,data.colors[data.colorselect][1])
                                text_rect7 = text_surf7.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2+120))
                                self.display_surface.blit(text_surf7, text_rect7)
                                if self.delta2 > 14:
                                    self.continuebutton.updatec("[CONUTINUE]",WINDOW_WIDTH/2,WINDOW_HEIGHT/2+160,data.colors[data.colorselect][1],1)
                                    if self.continuebutton.draw(self.display_surface):
                                        data.playingstate = 1
                                        self.delta2 = 0
                                        self.delta = 0

    def leavearch(self,data):
        self.backbutton.updatec("Return to Menu",WINDOW_WIDTH-160,WINDOW_HEIGHT-40,data.colors[data.colorselect][1],0)
        if self.backbutton.draw(self.display_surface):
            data.playingstate = 0
            self.playing_state = 0


    def timer(self,amount):
        self.current_time = amount

    def maxtimer(self,amount):
        self.max_time = amount

    def peaktimer(self,amount):
        self.peak_time = amount

    def pointer(self,amount):
        self.time_points = amount

    def timecaper(self,amount):
        self.time_cap = amount

    def forcestatechanger(self,amount):
        self.force_state_change = amount

    def milestoneforcer(self,amount):
        self.milestones_force = amount
    
    def timecapser(self,amount):
        self.time_caps = amount

    def playingstater(self,amount):
        self.playing_state = amount

    def shopstater(self,amount):
        self.shop_state = amount

    def digitser(self,amount):
        self.digit_s = amount

    def colorselecter(self,amount):
        self.color_select = amount

    def musicselecter(self,amount):
        self.music_select = amount

    def shoper(self,amount):
        self.shops = amount

    def milestoner(self,amount):
        self.Mile_stones = amount

    def update(self, data, dt):
        if self.playing_state > 0 and self.playing_state < 4:
            self.display_timer(data)
            self.display_maxtimer(data)
            self.display_pointer(data)
            self.display_timecap(data)
            self.display_shop(data)
            self.display_interactables(data)
            self.display_digits(data)
            self.delta += dt
        elif self.playing_state == 4:
            self.leavearch(data)
            self.delta = 0
        elif self.playing_state ==5:
            self.Display_victory(data)
            self.delta2 += dt
        else:
            self.display_startmenu(data)
            self.delta = 0

