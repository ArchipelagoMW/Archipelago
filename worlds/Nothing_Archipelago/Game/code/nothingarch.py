from settings import *
from buttons import Button
from Narchipelago import Archipelago


class archipelagoUI:
    def __init__(self,font):
        self.display_surface = pygame.display.get_surface()
        self.font = font
        self.passbutton = Button(self.font,"password",WINDOW_WIDTH/2,WINDOW_HEIGHT/2,(255,255,255),0)
        self.portbutton = Button(self.font,"port",WINDOW_WIDTH/2,WINDOW_HEIGHT/2,(255,255,255),0)
        self.slotbutton = Button(self.font,"slot",WINDOW_WIDTH/2,WINDOW_HEIGHT/2,(255,255,255),0)
        self.addressbutton = Button(self.font,"adress",WINDOW_WIDTH/2,WINDOW_HEIGHT/2,(255,255,255),0)
        self.connectbutton = Button(self.font,"connect",WINDOW_WIDTH/2,WINDOW_HEIGHT/2,(255,255,255),0)

    def connected(self,data):
        text_surf = self.font.render("Archipelago Connected",False,data.colors[data.colorselect][1])
        text_rect = text_surf.get_frect(topleft = (0,WINDOW_HEIGHT))
        self.display_surface.blit(text_surf, text_rect)
        self.archipelago.run()
    
    def serverinputs(self,data):
        self.addressbutton.updatec("Address : " + data.inputs[0],WINDOW_WIDTH/2,WINDOW_HEIGHT/2-80,data.colors[data.colorselect][1],0)
        self.portbutton.updatec("Port : " + data.inputs[1],WINDOW_WIDTH/2,WINDOW_HEIGHT/2-40,data.colors[data.colorselect][1],0)
        self.slotbutton.updatec("Slot Name : " + data.inputs[2],WINDOW_WIDTH/2,WINDOW_HEIGHT/2,data.colors[data.colorselect][1],0)
        self.passbutton.updatec("Password : " + data.inputs[3],WINDOW_WIDTH/2,WINDOW_HEIGHT/2+40,data.colors[data.colorselect][1],0)
        self.connectbutton.updatec("Connnect",WINDOW_WIDTH/2,WINDOW_HEIGHT/2+80,data.colors[data.colorselect][1],0)
        if self.addressbutton.draw(self.display_surface):
            data.activeinput = 0
        if self.portbutton.draw(self.display_surface):
            data.activeinput = 1
        if self.slotbutton.draw(self.display_surface):
            data.activeinput = 2
        if self.passbutton.draw(self.display_surface):
            data.activeinput = 3
        if self.connectbutton.draw(self.display_surface):
            self.archipelago = Archipelago(data.inputs[0], int(data.inputs[1]), data.inputs[2], data.inputs[3])
            self.archipelago.connect()
            data.playingstate = 1
            data.archipelagoactive = True
    
    def update(self,data,dt):
        if data.playingstate == 4:
            self.serverinputs(data)
        elif data.connected == 1 and data.playingstate > 0:
            self.connected(data)