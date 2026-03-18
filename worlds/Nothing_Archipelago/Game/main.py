import pygame, sys
from Level import Level
from ui import UI
from os.path import join
from support import *
from data import Data
from nothingarch import archipelagoUI

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((1920, 1080),pygame.SCALED | pygame.FULLSCREEN)
        self.import_assets()

        self.ui = UI(self.font,self.font2,self.font3, self.uiframes)
        self.data = Data(self.ui)

        
        
        pygame.display.set_caption('Nothing_Archipelago')
        
        self.clock = pygame.time.Clock()
        
        self.archui = archipelagoUI(self.font,self.data)
        self.current_stage = Level(self.data,self.audio_files)
        

    def import_assets(self):
        
        self.font = pygame.font.Font(join('graphics', 'ui', 'runescape_uf.ttf'), int((1920+1080)/75))
        self.font2 = pygame.font.Font(join('graphics', 'ui', 'runescape_uf.ttf'), int((1920+1080)/10))
        self.font3 = pygame.font.Font(join('graphics', 'ui', 'runescape_uf.ttf'), int((1920+1080)/25))
        self.uiframes = {
            'gear' : import_image('graphics', 'ui', 'gear')
        }

        self.audio_files = {
			'grub1': pygame.mixer.Sound(join('audio','Sounds', 'grub', 'grub1.wav')),
			'grub2': pygame.mixer.Sound(join('audio','Sounds', 'grub', 'grub2.wav')), 
			'grub3': pygame.mixer.Sound(join('audio','Sounds', 'grub', 'grub3.wav')),
			'grub4': pygame.mixer.Sound(join('audio','Sounds', 'grub', 'grub4.wav')),
            'grub5': pygame.mixer.Sound(join('audio','Sounds', 'grub', 'grub5.wav')),
            'grub6': pygame.mixer.Sound(join('audio','Sounds', 'grub', 'grub6.wav')),
            'grub7': pygame.mixer.Sound(join('audio','Sounds', 'grub', 'grub7.wav')),
            'grub8': pygame.mixer.Sound(join('audio','Sounds', 'grub', 'grub8.wav')),
            'grub9': pygame.mixer.Sound(join('audio','Sounds', 'grub', 'grub9.wav')),
            'pikmin1': pygame.mixer.Sound(join('audio','Sounds', 'pikmin', 'pikmin1.mp3')),
            'pikmin2': pygame.mixer.Sound(join('audio','Sounds', 'pikmin', 'pikmin2.mp3')),
            'pikmin3': pygame.mixer.Sound(join('audio','Sounds', 'pikmin', 'pikmin3.mp3')),
            'airhorn1': pygame.mixer.Sound(join('audio','Sounds', 'random', 'airhorn1.mp3')),
            'airhorn2': pygame.mixer.Sound(join('audio','Sounds', 'random', 'airhorn2.mp3')),
            'metal-pipe': pygame.mixer.Sound(join('audio','Sounds', 'random', 'metal-pipe.mp3')),
            'noot': pygame.mixer.Sound(join('audio','Sounds', 'random', 'noot.mp3')),
            'creeper': pygame.mixer.Sound(join('audio','Sounds', 'trolls', 'creeper.mp3')),
            'discord-leave': pygame.mixer.Sound(join('audio','Sounds', 'trolls', 'discord-leave.mp3')),
            'discord-join': pygame.mixer.Sound(join('audio','Sounds', 'trolls', 'discord-join.mp3')),
            'villager': pygame.mixer.Sound(join('audio','Sounds', 'weather', 'villager.mp3')),
            'weather1': pygame.mixer.Sound(join('audio','Sounds', 'weather', 'weather1.mp3')),
            'weather2': pygame.mixer.Sound(join('audio','Sounds', 'weather', 'weather2.mp3')),
            'weather3': pygame.mixer.Sound(join('audio','Sounds', 'weather', 'weather3.mp3')),
            'weather4': pygame.mixer.Sound(join('audio','Sounds', 'weather', 'weather4.mp3')),
            'hotwheel': pygame.mixer.Sound(join('audio','Sounds', 'why', 'hotwheels.mp3')),
            'zelda1': pygame.mixer.Sound(join('audio','Sounds', 'zelda', 'zelda1.mp3')),
            'zelda2': pygame.mixer.Sound(join('audio','Sounds', 'zelda', 'zelda2.mp3')),
            'zelda3': pygame.mixer.Sound(join('audio','Sounds', 'zelda', 'zelda3.mp3')),
            'zelda4': pygame.mixer.Sound(join('audio','Sounds', 'zelda', 'zelda4.mp3')),
            'zelda5': pygame.mixer.Sound(join('audio','Sounds', 'zelda', 'zelda5.mp3')),
            'bird1': pygame.mixer.Sound(join('audio','Sounds', 'bird', 'birds1.mp3')),
            'bird2': pygame.mixer.Sound(join('audio','Sounds', 'bird', 'birds2.mp3')),
            'bird3': pygame.mixer.Sound(join('audio','Sounds', 'bird', 'birds3.mp3')),
            'aoe1': pygame.mixer.Sound(join('audio','Sounds', 'aoe', 'aoe1.mp3')),
            'aoe2': pygame.mixer.Sound(join('audio','Sounds', 'aoe', 'aoe2.mp3')),
            'aoe3': pygame.mixer.Sound(join('audio','Sounds', 'aoe', 'aoe3.mp3')),
            'aoe4': pygame.mixer.Sound(join('audio','Sounds', 'aoe', 'aoe4.mp3')),
            'aoe5': pygame.mixer.Sound(join('audio','Sounds', 'aoe', 'aoe5.mp3')),
            'aoe6': pygame.mixer.Sound(join('audio','Sounds', 'aoe', 'aoe6.mp3')),
            'start1': pygame.mixer.Sound(join('audio','Sounds', 'songstart', 'start1.mp3')),
            'start2': pygame.mixer.Sound(join('audio','Sounds', 'songstart', 'start2.mp3')),
            'start3': pygame.mixer.Sound(join('audio','Sounds', 'songstart', 'start3.mp3')),
            'start4': pygame.mixer.Sound(join('audio','Sounds', 'songstart', 'start4.mp3')),
            'start5': pygame.mixer.Sound(join('audio','Sounds', 'songstart', 'start5.mp3')),
            'start6': pygame.mixer.Sound(join('audio','Sounds', 'songstart', 'start6.mp3')),
            'start7': pygame.mixer.Sound(join('audio','Sounds', 'songstart', 'start7.mp3')),
            'start8': pygame.mixer.Sound(join('audio','Sounds', 'songstart', 'start8.mp3')),
            'start9': pygame.mixer.Sound(join('audio','Sounds', 'songstart', 'start9.mp3')),
            'start10': pygame.mixer.Sound(join('audio','Sounds', 'songstart', 'start10.mp3'))
		}
        
        

    def musicplayer(self,data):
        if data.currentsong != data.musicselect:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload
            if data.musicselect == 0:
                pygame.mixer.music.load(join('audio','Music','song1.mp3'))
            elif data.musicselect == 1:
                pygame.mixer.music.load(join('audio','Music','song2.mp3'))
            elif data.musicselect == 2:
                pygame.mixer.music.load(join('audio','Music','song3.mp3'))
            elif data.musicselect == 3:
                pygame.mixer.music.load(join('audio','Music','song4.mp3'))
            elif data.musicselect == 4:
                pygame.mixer.music.load(join('audio','Music','song5.mp3'))
            elif data.musicselect == 5:
                pygame.mixer.music.load(join('audio','Music','song6.mp3'))
            elif data.musicselect == 6:
                pygame.mixer.music.load(join('audio','Music','song7.mp3'))
            elif data.musicselect == 7:
                pygame.mixer.music.load(join('audio','Music','song8.mp3'))
            elif data.musicselect == 8:
                pygame.mixer.music.load(join('audio','Music','song9.mp3'))
            elif data.musicselect == 9:
                pygame.mixer.music.load(join('audio','Music','song10.mp3'))
            data.currentsong = data.musicselect
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)


        


    def run(self):
        while True:
            self.clock.tick(60)
            dt = self.clock.get_time()/1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.data.leave == 1:
                    pygame.quit()
                    sys.exit()
                elif ((event.type == pygame.KEYDOWN or event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.JOYAXISMOTION or event.type == pygame.JOYBALLMOTION or event.type == pygame.JOYHATMOTION or event.type == pygame.JOYBUTTONDOWN) and (self.data.playingstate > 0 and self.data.playingstate < 4)):
                    #print("press")
                    self.current_stage.changegamestate()
                elif event.type == pygame.KEYDOWN and self.data.playingstate == 4:
                    if event.key == pygame.K_BACKSPACE:
                        self.data.inputs[self.data.activeinput] = self.data.inputs[self.data.activeinput] [:-1]
                    else:
                        self.data.inputs[self.data.activeinput] += event.unicode
                elif event.type == pygame.KEYDOWN and self.data.playingstate == 0:
                    if event.key == pygame.K_0:
                        self.data.devcount = 1
                    elif event.key == pygame.K_1 and self.data.devcount >= 1:
                        self.data.devcount = 2
                    elif event.key == pygame.K_2 and self.data.devcount >= 2:
                        self.data.devcount = 3
                    elif event.key == pygame.K_3 and self.data.devcount >= 3:
                        self.data.devcount = 4
                    elif event.key == pygame.K_4 and self.data.devcount >= 4:
                        self.data.devcount = 5

            if (self.data.shop[0][0][2] == 1 and (self.data.playingstate == 1 or self.data.playingstate == 3)) or self.data.forcestatechange == 1:
                self.current_stage.changegamestate()
            
            self.musicplayer(self.data)
            self.current_stage.run(dt)
            self.ui.update(self.data,dt)
            self.archui.update(self.data,dt)
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
