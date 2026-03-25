import pygame
from .buttons import Button


class archipelagoUI:
    def __init__(self,font,data):
        self.display_surface = pygame.display.get_surface()
        self.font = font
        self.passbutton = Button(self.font,"password",data.WINDOW_WIDTH/2,data.WINDOW_HEIGHT/2,(255,255,255),0)
        self.portbutton = Button(self.font,"port",data.WINDOW_WIDTH/2,data.WINDOW_HEIGHT/2,(255,255,255),0)
        self.slotbutton = Button(self.font,"slot",data.WINDOW_WIDTH/2,data.WINDOW_HEIGHT/2,(255,255,255),0)
        self.addressbutton = Button(self.font,"adress",data.WINDOW_WIDTH/2,data.WINDOW_HEIGHT/2,(255,255,255),0)
        self.connectbutton = Button(self.font,"connect",data.WINDOW_WIDTH/2,data.WINDOW_HEIGHT/2,(255,255,255),0)

    def connected(self,data):
        if data.connected == 1:
            text_surf = self.font.render("Archipelago Connected",False,data.colors[data.colorselect][1])
        else:
            text_surf = self.font.render("Archipelago Disconnected",False,data.colors[data.colorselect][1])
        text_rect = text_surf.get_frect(topleft = (0,data.WINDOW_HEIGHT))
        self.display_surface.blit(text_surf, text_rect)
        if data.needsync == 1:
            self.sync_locations(data)


    def sync_locations(self,data):
        data.needsync = 0
        data.checked_locations_player = data.checked_locations
        for location in data.check_locations_player:
            if location <= 86400:
                data.milestones[location-1,1] = 1
                data.milestones[location-1,0] = 0
            else:
                data.spentcoins += data.shop[((location-86401)//10)%10][(location-86401)%10][3]
                data.shop[((location-86401)//10)%10][(location-86401)%10][1] = 1

    def checklocations(self,data, checked_locations) -> None:
        if data.checked_locations_player == checked_locations:
            return
        else:
            data.checked_locations = checked_locations
            data.needsync = 1



    def updateitems(self,data,items) -> None:
        digitcount = 0
        data.timecaps = 1
        data.giftcoins = 0
        for item in items:
            if item == 1:
                data.shop[0][0][2] = 1
            elif item == 2:
                data.shop[0][1][2] = 1
            elif item == 3:
                data.shop[0][2+digitcount][2] = 1
                digitcount +=1
            elif item == 4:
                data.timecaps += 1
                data.timecap = data.timecaps * data.timecapint
            elif item == 5:
                giftcoins += 1
            elif item == 11:
                data.shop[2][0][2] = 1
            elif item == 12:
                data.shop[2][1][2] = 1
            elif item == 13:
                data.shop[2][2][2] = 1
            elif item == 14:
                data.shop[2][3][2] = 1
            elif item == 15:
                data.shop[2][4][2] = 1
            elif item == 16:
                data.shop[2][5][2] = 1
            elif item == 17:
                data.shop[2][6][2] = 1
            elif item == 18:
                data.shop[2][7][2] = 1
            elif item == 19:
                data.shop[2][8][2] = 1
            elif item == 20:
                data.shop[2][9][2] = 1
            elif item == 21:
                data.shop[1][0][2] = 1
            elif item == 22:
                data.shop[1][1][2] = 1
            elif item == 23:
                data.shop[1][2][2] = 1
            elif item == 24:
                data.shop[1][3][2] = 1
            elif item == 25:
                data.shop[1][4][2] = 1
            elif item == 26:
                data.shop[1][5][2] = 1
            elif item == 27:
                data.shop[1][6][2] = 1
            elif item == 28:
                data.shop[1][7][2] = 1
            elif item == 29:
                data.shop[1][8][2] = 1
            elif item == 30:
                data.shop[1][9][2] = 1
            elif item == 32:
                data.shop[3][1][2] = 1
            elif item == 33:
                data.shop[3][2][2] = 1
            elif item == 34:
                data.shop[3][3][2] = 1
            elif item == 35:
                data.shop[3][4][2] = 1
            elif item == 36:
                data.shop[3][5][2] = 1
            elif item == 37:
                data.shop[3][6][2] = 1
            elif item == 38:
                data.shop[3][7][2] = 1
            elif item == 39:
                data.shop[3][8][2] = 1
            elif item == 40:
                data.shop[3][9][2] = 1
        
        if data.giftcoins > data.spentcoins:
            data.points += data.giftcoins - data.spentcoins
    
    def serverinputs(self,data):
        self.addressbutton.updatec("Address : " + data.inputs[0],data.WINDOW_WIDTH/2,data.WINDOW_HEIGHT/2-80,data.colors[data.colorselect][1],0)
        self.portbutton.updatec("Port : " + data.inputs[1],data.WINDOW_WIDTH/2,data.WINDOW_HEIGHT/2-40,data.colors[data.colorselect][1],0)
        self.slotbutton.updatec("Slot Name : " + data.inputs[2],data.WINDOW_WIDTH/2,data.WINDOW_HEIGHT/2,data.colors[data.colorselect][1],0)
        self.passbutton.updatec("Password : " + data.inputs[3],data.WINDOW_WIDTH/2,data.WINDOW_HEIGHT/2+40,data.colors[data.colorselect][1],0)
        self.connectbutton.updatec("Connnect",data.WINDOW_WIDTH/2,data.WINDOW_HEIGHT/2+80,data.colors[data.colorselect][1],0)
        if self.addressbutton.draw(self.display_surface):
            data.activeinput = 0
        if self.portbutton.draw(self.display_surface):
            data.activeinput = 1
        if self.slotbutton.draw(self.display_surface):
            data.activeinput = 2
        if self.passbutton.draw(self.display_surface):
            data.activeinput = 3
        if self.connectbutton.draw(self.display_surface):
            data.playingstate = 1
            data.archipelagoactive = True
    
    def update(self,data,dt):
        if data.playingstate == 4:
            self.serverinputs(data)
        elif data.playingstate > 0 and data.archipelagoactive == True:
            self.connected(data)