import sys
from os.path import join
import pygame
from .Level import Level
from .ui import UI
from pathlib import Path
from .support import *
from .data import Data
from .nothingarch import archipelagoUI
import asyncio
from ..client.nothing_archipelago_client import main

class Game:
    def __init__(self, goal = 86400, shop_upgrades = True, shop_colors = True,
                  shop_music = True, shop_sounds = True, gift_coins = True, milestone_interval = 1,
                    timecap_interval = 1, Starting_coin_count = 0, Death_link = False, Death_link_mercy = 1, Time_dilation = 1):
        pygame.init()
        self.display_surface = pygame.display.set_mode((1920, 1080),pygame.SCALED | pygame.FULLSCREEN)
        self.current_dir = Path(__file__).parent.resolve()
        if ".apworld" in str(self.current_dir):
            import zipfile
            self.current_dir = Path(__file__).parent.parent.parent.resolve()
            self.archive = zipfile.ZipFile(self.current_dir,'r')
            self.iszip = True
        else:
            self.iszip = False
        
        self.import_assets()
        
        self.ui = UI(self.font,self.font2,self.font3, self.uiframes)
        self.data = Data(self.ui, goal, shop_upgrades, shop_colors, shop_music, shop_sounds, gift_coins,
                          milestone_interval, timecap_interval, Starting_coin_count, Death_link, Death_link_mercy, Time_dilation)
        pygame.display.set_caption('nothing_archipelago')
        
        self.clock = pygame.time.Clock()
        
        self.archui = archipelagoUI(self.font,self.data)
        self.current_stage = Level(self.data,self.audio_files)
        #asyncio.create_task(main(self.data,self.archui),name="clientcreator")
        
    def update_settings(self, goal = 86400, shop_upgrades = True, shop_colors = True, shop_music = True, shop_sounds = True, gift_coins = True,
                         milestone_interval = 1, timecap_interval = 1, Starting_coin_count = 0, Death_link = False, 
                         Death_link_mercy = 1, Time_dilation = 1):
        self.data.update_arch_settings(self,goal, shop_upgrades, shop_colors, shop_music, shop_sounds, gift_coins,
                          milestone_interval, timecap_interval, Starting_coin_count, Death_link, Death_link_mercy, Time_dilation)

    def update_items(self,items):
        self.archui.updateitems(self.data,items)

    def verifylocations(self,locations):
        self.archui.checklocations(self.data,locations)

    def import_assets(self):
        if self.iszip:
            import io
            self.fontfile = self.archive.read(join('nothing_archipelago','Game','graphics', 'ui', 'runescape_uf.ttf'))
            self.gearfile = self.archive.read(join('nothing_archipelago','Game','graphics', 'ui', 'gear.png'))
            self.grub1file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'grub', 'grub1.wav'))
            self.grub2file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'grub', 'grub2.wav'))
            self.grub3file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'grub', 'grub3.wav'))
            self.grub4file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'grub', 'grub4.wav'))
            self.grub5file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'grub', 'grub5.wav'))
            self.grub6file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'grub', 'grub6.wav'))
            self.grub7file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'grub', 'grub7.wav'))
            self.grub8file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'grub', 'grub8.wav'))
            self.grub9file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'grub', 'grub9.wav'))
            self.pikmin1file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'pikmin', 'pikmin1.mp3'))
            self.pikmin2file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'pikmin', 'pikmin2.mp3'))
            self.pikmin3file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'pikmin', 'pikmin3.mp3'))
            self.airhorn1file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'random', 'airhorn1.mp3'))
            self.airhorn2file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'random', 'airhorn2.mp3'))
            self.metalpipefile = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'random', 'metal-pipe.mp3'))
            self.nootfile = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'random', 'noot.mp3'))
            self.creeperfile = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'trolls', 'creeper.mp3'))
            self.discordleavefile = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'trolls', 'discord-leave.mp3'))
            self.discordjoinfile = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'trolls', 'discord-join.mp3'))
            self.villagerfile = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'weather', 'villager.mp3'))
            self.weather1file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'weather', 'weather1.mp3'))
            self.weather2file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'weather', 'weather2.mp3'))
            self.weather3file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'weather', 'weather3.mp3'))
            self.weather4file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'weather', 'weather4.mp3'))
            self.hotwheelfile = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'why', 'hotwheels.mp3'))
            self.zelda1file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'zelda', 'zelda1.mp3'))
            self.zelda2file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'zelda', 'zelda2.mp3'))
            self.zelda3file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'zelda', 'zelda3.mp3'))
            self.zelda4file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'zelda', 'zelda4.mp3'))
            self.zelda5file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'zelda', 'zelda5.mp3'))
            self.bird1file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'bird', 'birds1.mp3'))
            self.bird2file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'bird', 'birds2.mp3'))
            self.bird3file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'bird', 'birds3.mp3'))
            self.aoe1file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'aoe', 'aoe1.mp3'))
            self.aoe2file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'aoe', 'aoe2.mp3'))
            self.aoe3file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'aoe', 'aoe3.mp3'))
            self.aoe4file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'aoe', 'aoe4.mp3'))
            self.aoe5file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'aoe', 'aoe5.mp3'))
            self.aoe6file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'aoe', 'aoe6.mp3'))
            self.start1file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'songstart', 'start1.mp3'))
            self.start2file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'songstart', 'start2.mp3'))
            self.start3file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'songstart', 'start3.mp3'))
            self.start4file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'songstart', 'start4.mp3'))
            self.start5file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'songstart', 'start5.mp3'))
            self.start6file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'songstart', 'start6.mp3'))
            self.start7file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'songstart', 'start7.mp3'))
            self.start8file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'songstart', 'start8.mp3'))
            self.start9file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'songstart', 'start9.mp3'))
            self.start10file = self.archive.read(join('nothing_archipelago','Game','audio','Sounds', 'songstart', 'start10.mp3'))
            self.song1file = self.archive.read(join('nothing_archipelago','Game','audio','Music','song1.mp3'))
            self.song1 = io.BytesIO(self.song1file)
            self.song2file = self.archive.read(join('nothing_archipelago','Game','audio','Music','song2.mp3'))
            self.song2 = io.BytesIO(self.song2file)
            self.song3file = self.archive.read(join('nothing_archipelago','Game','audio','Music','song3.mp3'))
            self.song3 = io.BytesIO(self.song3file)
            self.song4file = self.archive.read(join('nothing_archipelago','Game','audio','Music','song4.mp3'))
            self.song4 = io.BytesIO(self.song4file)
            self.song5file = self.archive.read(join('nothing_archipelago','Game','audio','Music','song5.mp3'))
            self.song5 = io.BytesIO(self.song5file)
            self.song6file = self.archive.read(join('nothing_archipelago','Game','audio','Music','song6.mp3'))
            self.song6 = io.BytesIO(self.song6file)
            self.song7file = self.archive.read(join('nothing_archipelago','Game','audio','Music','song7.mp3'))
            self.song7 = io.BytesIO(self.song7file)
            self.song8file = self.archive.read(join('nothing_archipelago','Game','audio','Music','song8.mp3'))
            self.song8 = io.BytesIO(self.song8file)
            self.song9file = self.archive.read(join('nothing_archipelago','Game','audio','Music','song9.mp3'))
            self.song9 = io.BytesIO(self.song9file)
            self.song10file = self.archive.read(join('nothing_archipelago','Game','audio','Music','song10.mp3'))
            self.song10 = io.BytesIO(self.song10file)


            self.font = pygame.font.Font(io.BytesIO(self.fontfile), int((1920+1080)/75))
            self.font2 = pygame.font.Font(io.BytesIO(self.fontfile), int((1920+1080)/10))
            self.font3 = pygame.font.Font(io.BytesIO(self.fontfile), int((1920+1080)/25))
            self.uiframes = {
                'gear' : import_image(io.BytesIO(self.gearfile))
            }

            self.audio_files = {
                'grub1': pygame.mixer.Sound(io.BytesIO(self.grub1file)),
                'grub2': pygame.mixer.Sound(io.BytesIO(self.grub2file)), 
                'grub3': pygame.mixer.Sound(io.BytesIO(self.grub3file)),
                'grub4': pygame.mixer.Sound(io.BytesIO(self.grub4file)),
                'grub5': pygame.mixer.Sound(io.BytesIO(self.grub5file)),
                'grub6': pygame.mixer.Sound(io.BytesIO(self.grub6file)),
                'grub7': pygame.mixer.Sound(io.BytesIO(self.grub7file)),
                'grub8': pygame.mixer.Sound(io.BytesIO(self.grub8file)),
                'grub9': pygame.mixer.Sound(io.BytesIO(self.grub9file)),
                'pikmin1': pygame.mixer.Sound(io.BytesIO(self.pikmin1file)),
                'pikmin2': pygame.mixer.Sound(io.BytesIO(self.pikmin2file)),
                'pikmin3': pygame.mixer.Sound(io.BytesIO(self.pikmin3file)),
                'airhorn1': pygame.mixer.Sound(io.BytesIO(self.airhorn1file)),
                'airhorn2': pygame.mixer.Sound(io.BytesIO(self.airhorn2file)),
                'metal-pipe': pygame.mixer.Sound(io.BytesIO(self.metalpipefile)),
                'noot': pygame.mixer.Sound(io.BytesIO(self.nootfile)),
                'creeper': pygame.mixer.Sound(io.BytesIO(self.creeperfile)),
                'discord-leave': pygame.mixer.Sound(io.BytesIO(self.discordleavefile)),
                'discord-join': pygame.mixer.Sound(io.BytesIO(self.discordjoinfile)),
                'villager': pygame.mixer.Sound(io.BytesIO(self.villagerfile)),
                'weather1': pygame.mixer.Sound(io.BytesIO(self.weather1file)),
                'weather2': pygame.mixer.Sound(io.BytesIO(self.weather2file)),
                'weather3': pygame.mixer.Sound(io.BytesIO(self.weather3file)),
                'weather4': pygame.mixer.Sound(io.BytesIO(self.weather4file)),
                'hotwheel': pygame.mixer.Sound(io.BytesIO(self.hotwheelfile)),
                'zelda1': pygame.mixer.Sound(io.BytesIO(self.zelda1file)),
                'zelda2': pygame.mixer.Sound(io.BytesIO(self.zelda2file)),
                'zelda3': pygame.mixer.Sound(io.BytesIO(self.zelda3file)),
                'zelda4': pygame.mixer.Sound(io.BytesIO(self.zelda4file)),
                'zelda5': pygame.mixer.Sound(io.BytesIO(self.zelda5file)),
                'bird1': pygame.mixer.Sound(io.BytesIO(self.bird1file)),
                'bird2': pygame.mixer.Sound(io.BytesIO(self.bird2file)),
                'bird3': pygame.mixer.Sound(io.BytesIO(self.bird3file)),
                'aoe1': pygame.mixer.Sound(io.BytesIO(self.aoe1file)),
                'aoe2': pygame.mixer.Sound(io.BytesIO(self.aoe2file)),
                'aoe3': pygame.mixer.Sound(io.BytesIO(self.aoe3file)),
                'aoe4': pygame.mixer.Sound(io.BytesIO(self.aoe4file)),
                'aoe5': pygame.mixer.Sound(io.BytesIO(self.aoe5file)),
                'aoe6': pygame.mixer.Sound(io.BytesIO(self.aoe6file)),
                'start1': pygame.mixer.Sound(io.BytesIO(self.start1file)),
                'start2': pygame.mixer.Sound(io.BytesIO(self.start2file)),
                'start3': pygame.mixer.Sound(io.BytesIO(self.start3file)),
                'start4': pygame.mixer.Sound(io.BytesIO(self.start4file)),
                'start5': pygame.mixer.Sound(io.BytesIO(self.start5file)),
                'start6': pygame.mixer.Sound(io.BytesIO(self.start6file)),
                'start7': pygame.mixer.Sound(io.BytesIO(self.start7file)),
                'start8': pygame.mixer.Sound(io.BytesIO(self.start8file)),
                'start9': pygame.mixer.Sound(io.BytesIO(self.start9file)),
                'start10': pygame.mixer.Sound(io.BytesIO(self.start10file))
            }
        else:
            self.font = pygame.font.Font(join(self.current_dir,'graphics', 'ui', 'runescape_uf.ttf'), int((1920+1080)/75))
            self.font2 = pygame.font.Font(join(self.current_dir,'graphics', 'ui', 'runescape_uf.ttf'), int((1920+1080)/10))
            self.font3 = pygame.font.Font(join(self.current_dir,'graphics', 'ui', 'runescape_uf.ttf'), int((1920+1080)/25))
            self.uiframes = {
                'gear' : import_image(join(self.current_dir,'graphics', 'ui', 'gear.png'))
            }

            self.audio_files = {
                'grub1': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'grub', 'grub1.wav')),
                'grub2': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'grub', 'grub2.wav')), 
                'grub3': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'grub', 'grub3.wav')),
                'grub4': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'grub', 'grub4.wav')),
                'grub5': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'grub', 'grub5.wav')),
                'grub6': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'grub', 'grub6.wav')),
                'grub7': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'grub', 'grub7.wav')),
                'grub8': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'grub', 'grub8.wav')),
                'grub9': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'grub', 'grub9.wav')),
                'pikmin1': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'pikmin', 'pikmin1.mp3')),
                'pikmin2': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'pikmin', 'pikmin2.mp3')),
                'pikmin3': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'pikmin', 'pikmin3.mp3')),
                'airhorn1': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'random', 'airhorn1.mp3')),
                'airhorn2': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'random', 'airhorn2.mp3')),
                'metal-pipe': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'random', 'metal-pipe.mp3')),
                'noot': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'random', 'noot.mp3')),
                'creeper': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'trolls', 'creeper.mp3')),
                'discord-leave': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'trolls', 'discord-leave.mp3')),
                'discord-join': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'trolls', 'discord-join.mp3')),
                'villager': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'weather', 'villager.mp3')),
                'weather1': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'weather', 'weather1.mp3')),
                'weather2': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'weather', 'weather2.mp3')),
                'weather3': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'weather', 'weather3.mp3')),
                'weather4': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'weather', 'weather4.mp3')),
                'hotwheel': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'why', 'hotwheels.mp3')),
                'zelda1': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'zelda', 'zelda1.mp3')),
                'zelda2': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'zelda', 'zelda2.mp3')),
                'zelda3': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'zelda', 'zelda3.mp3')),
                'zelda4': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'zelda', 'zelda4.mp3')),
                'zelda5': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'zelda', 'zelda5.mp3')),
                'bird1': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'bird', 'birds1.mp3')),
                'bird2': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'bird', 'birds2.mp3')),
                'bird3': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'bird', 'birds3.mp3')),
                'aoe1': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'aoe', 'aoe1.mp3')),
                'aoe2': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'aoe', 'aoe2.mp3')),
                'aoe3': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'aoe', 'aoe3.mp3')),
                'aoe4': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'aoe', 'aoe4.mp3')),
                'aoe5': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'aoe', 'aoe5.mp3')),
                'aoe6': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'aoe', 'aoe6.mp3')),
                'start1': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'songstart', 'start1.mp3')),
                'start2': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'songstart', 'start2.mp3')),
                'start3': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'songstart', 'start3.mp3')),
                'start4': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'songstart', 'start4.mp3')),
                'start5': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'songstart', 'start5.mp3')),
                'start6': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'songstart', 'start6.mp3')),
                'start7': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'songstart', 'start7.mp3')),
                'start8': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'songstart', 'start8.mp3')),
                'start9': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'songstart', 'start9.mp3')),
                'start10': pygame.mixer.Sound(join(self.current_dir,'audio','Sounds', 'songstart', 'start10.mp3'))
            }
        
        

    def musicplayer(self,data):
        if data.currentsong != data.musicselect:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload
            if self.iszip:
                if data.musicselect == 0:
                    pygame.mixer.music.load(self.song1)
                elif data.musicselect == 1:
                    pygame.mixer.music.load(self.song2)
                elif data.musicselect == 2:
                    pygame.mixer.music.load(self.song3)
                elif data.musicselect == 3:
                    pygame.mixer.music.load(self.song4)
                elif data.musicselect == 4:
                    pygame.mixer.music.load(self.song5)
                elif data.musicselect == 5:
                    pygame.mixer.music.load(self.song6)
                elif data.musicselect == 6:
                    pygame.mixer.music.load(self.song7)
                elif data.musicselect == 7:
                    pygame.mixer.music.load(self.song8)
                elif data.musicselect == 8:
                    pygame.mixer.music.load(self.song9)
                elif data.musicselect == 9:
                    pygame.mixer.music.load(self.song10)
            else:
                if data.musicselect == 0:
                    pygame.mixer.music.load(join(self.current_dir,'audio','Music','song1.mp3'))
                elif data.musicselect == 1:
                    pygame.mixer.music.load(join(self.current_dir,'audio','Music','song2.mp3'))
                elif data.musicselect == 2:
                    pygame.mixer.music.load(join(self.current_dir,'audio','Music','song3.mp3'))
                elif data.musicselect == 3:
                    pygame.mixer.music.load(join(self.current_dir,'audio','Music','song4.mp3'))
                elif data.musicselect == 4:
                    pygame.mixer.music.load(join(self.current_dir,'audio','Music','song5.mp3'))
                elif data.musicselect == 5:
                    pygame.mixer.music.load(join(self.current_dir,'audio','Music','song6.mp3'))
                elif data.musicselect == 6:
                    pygame.mixer.music.load(join(self.current_dir,'audio','Music','song7.mp3'))
                elif data.musicselect == 7:
                    pygame.mixer.music.load(join(self.current_dir,'audio','Music','song8.mp3'))
                elif data.musicselect == 8:
                    pygame.mixer.music.load(join(self.current_dir,'audio','Music','song9.mp3'))
                elif data.musicselect == 9:
                    pygame.mixer.music.load(join(self.current_dir,'audio','Music','song10.mp3'))
            data.currentsong = data.musicselect
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)


        
    #make connection fail reset archipelago active at aome point please
    #make sure the client closes
    #implement deathlink

    async def run(self):
        await asyncio.sleep(0)
        test = 0
        while True:
            if test == 0 and self.data.archipelagoactive == True:
                asyncio.create_task(main(self.data,self.archui),name="clientcreator")
                test = 1
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
                    await asyncio.sleep(0)
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
            await asyncio.sleep(0)
            self.musicplayer(self.data)
            self.current_stage.run(dt)
            self.ui.update(self.data,dt)
            self.archui.update(self.data,dt)
            pygame.display.update()

            await asyncio.sleep(0)
            self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()
