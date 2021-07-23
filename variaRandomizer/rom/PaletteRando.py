import colorsys, random
from rom.rom import pc_to_snes
from rom.romloader import RomLoader
from rando.palettes import palettes
from varia_custom_sprites.sprite_palettes import sprite_palettes
import utils.log

#Palette Hue Shift

#Most palette info taken from http://www.metroidconstruction.com/SMMM/ and http://patrickjohnston.org/bank/9B#f9400
#Every palette consists of sixteen 2-byte-sets, suit palettes are uncompressed

#To-Do | Adjustments:

#Suits:
#find crystal flash, maybe D96C0-5F  | visor oddities that might be missing: DA3C6-02 Samus' visor flashing yellow in dark rooms. ,1652C-00 Samus' green visor when first entering a room. 

#Enemies:
#Kzan is not changed, would look odd

#glowing elevator platform palette pointer seems to be messed up, need to find the real palette location at some point. might be using the general palette.

#excluded lava-like enemies from hue shifting because lava color is not being shifted yet. e.g.: hibashi, puromi, lavaman



#Information about compressed palettes for main areas:
#
#$00 normal Crateria:                C2AD7C    0x212D7C  
#$01 red Cratera:                    C2AE5D    0x212E5D
#$02 old Crateria:                   C2AF43    0x212F43
#$03 old Crateria:                   C2B015    0x213015
#$04 Wrecked Ship:                   C2B0E7    0x2130E7
#$05 Wrecked Ship:                   C2B1A6    0x2131A6
#$06 Green Brinstar:                 C2B264    0x213264
#$07 Red Brinstar:                   C2B35F    0x21335F
#$08 Red Brinstar:                   C2B447    0x213447
#$09 Norfair:                        C2B5E4    0x2135E4
#$0A Norfair:                        C2B6BB    0x2136BB
#$0B Maridia:                        C2B83C    0x21383C
#$0C Maridia:                        C2B92E    0x21392E
#$0D Tourian:                        C2BAED    0x213AED
#$0E Tourian:                        C2BBC1    0x213BC1
#$0F Ceres:                          C2C104    0x214104
#$10 Ceres:                          C2C1E3    0x2141E3
#$11 Mode 7 Ceres:                   C2C104    0x214104
#$12 Mode 7 Ceres:                   C2C1E3    0x2141E3
#$13 Mode 7 Ridley:                  C2C104    0x214104
#$14 Mode 7 Ridley:                  C2C1E3    0x2141E3
#$15 Save/G4 [0]:                    C2BC9C    0x213C9C
#$16 Save/G4 [1]:                    C2BD7B    0x213D7B
#$17 Save/G4 [2]:                    C2BE58    0x213E58
#$18 Save/G4 [3]:                    C2BF3D    0x213F3D
#$19 Save/G4 [4]:                    C2C021    0x214021
#$1A Kraid room:                     C2B510    0x213510
#$1B Crocomire room:                 C2B798    0x213798
#$1C Draygon room:                   C2BA2C    0x213A2C


#Pointer Locations:

#$00    0x7E6A8 = 7C AD C2   
#$01    0x7E6B1 = 5D AE C2
#$02    0x7E6BA = 43 AF C2
#$03    0x7E6C3 = 15 B0 C2
#$04    0x7E6CC = E7 B0 C2
#$05    0x7E6D5 = A6 B1 C2
#$06    0x7E6DE = 64 B2 C2
#$07    0x7E6E7 = 5F B3 C2
#$08    0x7E6F0 = 47 B4 C2
#$09    0x7E6F9 = E4 B5 C2
#$0A    0x7E702 = BB B6 C2
#$0B    0x7E70B = 3C B8 C2
#$0C    0x7E714 = 2E B9 C2
#$0D    0x7E71D = ED BA C2
#$0E    0x7E726 = C1 BB C2
#$0F    0x7E72F = 04 C1 C2
#$10    0x7E738 = E3 C1 C2

#Mode 7 stuff, probably best to leave this alone for now
#$11    0x7E741 = 04 C1 C2
#$12    0x7E74A = E3 C1 C2
#$13    0x7E753 = 04 C1 C2
#$14    0x7E75C = E3 C1 C2

#Back to normal room palettes
#$15    0x7E765 = 9C BC C2
#$16    0x7E76E = 7B BD C2
#$17    0x7E777 = 58 BE C2
#$18    0x7E780 = 3D BF C2
#$19    0x7E789 = 21 C0 C2
#$1A    0x7E792 = 10 B5 C2
#$1B    0x7E79B = 98 B7 C2
#$1C    0x7E7A4 = 2C BA C2


#Inserting palettes around 0x2FE050
#
#Decompressed palette info:
#        2                    +    26                            +     2            +    2            =    32 bytes used per palette (hex-size = 0x20)   ||||| 32 * 8 = 256 bytes per palette set
# Transparency Color | 13 colors used in tileset palette | default white | default black


class PaletteRando(object):
    def __init__(self, romPatcher, settings, sprite):
        self.logger = utils.log.get('Palette')

        self.romPatcher = romPatcher
        if sprite is not None:
            palettes.update(sprite_palettes[sprite])
        self.romLoader = RomLoader.factory(palettes)
        self.palettesROM = self.romLoader.getROM()
        self.outFile = romPatcher.romFile

        self.max_degree = settings["max_degree"]
        self.min_degree = settings["min_degree"]
        self.invert = settings["invert"]

        #boss_tileset_palettes = [0x213510,0x213798,0x213A2C,0x213BC1]
        #boss_pointer_addresses = [0x7E792,0x7E79B,0x7E7A4,0x7E726]
        #gray doors + hud elements [0x28,0x2A,0x2C,0x2E]
        self.tileset_palette_offsets = [0x212D7C,0x212E5D,0x212F43,0x213015,0x2130E7,0x2131A6,0x213264,0x21335F,0x213447,0x2135E4,0x2136BB,0x21383C,0x21392E,0x213AED,0x213BC1,0x214104,0x2141E3,0x213C9C,0x213D7B,0x213E58,0x213F3D,0x214021,0x213510,0x213798,0x213A2C]
        self.bluedoor_bytes = [0x62,0x64,0x66]
        self.palette_single_bytes = [0x08,0x0A,0x0C,0x0E,0x48,0x4A,0x4C,0x4E,0x50,0x52,0x54,0x56,0x58,0x5A,0x68,0x6A,0x6C,0x6E,0x70,0x72,0x74,0x76,0x78,0x7A]  

        #replaced crateria $00 with $01 pointer for nicer colors on surface crateria (was [0x7E6A8,0x7E6B1,[...] before the change)
        self.pointer_addresses = [0x7E6A8,0x7E6B1,0x7E6BA,0x7E6C3,0x7E6CC,0x7E6D5,0x7E6DE,0x7E6E7,0x7E6F0,0x7E6F9,0x7E702,0x7E70B,0x7E714,0x7E71D,0x7E726,0x7E72F,0x7E738,0x7E765,0x7E76E,0x7E777,0x7E780,0x7E789,0x7E792,0x7E79B,0x7E7A4]
        self.pointers_to_insert = []


        #Fx1 palettes and the length of each individual color palette
        #Ridley room fade-in
        self.fx1_palettes_ri = [0x132509]
        self.fx1_length_ri = [0xD1]
        #Brinstar blue glow
        self.fx1_palettes_gb = [0x6ED9F,0x6EDA9,0x6EDB3,0x6EDBD,0x6EDC7,0x6EDD1,0x6EDDB,0x6EDE5,0x6EDEF,0x6EDF9,0x6EE03,0x6EE0D,0x6EE17,0x6EE21]
        self.fx1_length_gb = [0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02]
        #Red brinstar glow purple
        self.fx1_palettes_rb = [0x6EEDD,0x6EEF1,0x6EF05,0x6EF19,0x6EF2D,0x6EF41,0x6EF55,0x6EF69,0x6EF7D,0x6EF91,0x6EFA5,0x6EFB9,0x6EFCD,0x6EFE1]
        self.fx1_length_rb = [0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07]
        #Wrecked Ship green glow
        self.fx1_palettes_ws = [0x6EAE8,0x6EAF0,0x6EAF8,0x6EB00,0x6EB08,0x6EB10,0x6EB18,0x6EB20,0x13CA61]
        self.fx1_length_ws = [0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x6F]
        #Crateria pulse red, 
        self.fx1_palettes_cr = [0x6FD03,0x6FD15,0x6FD27,0x6FD39,0x6FD4B,0x6FD5D,0x6FD6F,0x6FD81,0x6FD93,0x6FDA5,0x6FDB7,0x6FDC9,0x6FDDB,0x6FDED]
        self.fx1_length_cr = [0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06]
        #Tourian slow pulse red/blue,
        self.fx1_palettes_tr = [0x6F640,0x6F656,0x6F66C,0x6F682,0x6F698,0x6F6AE,0x6F6C4,0x6F6DA,0x6F6F0,0x6F706,0x6F71C,0x6F7AF,0x6F7BF,0x6F7CF,0x6F7DF,0x6F7EF,0x6F7FF,0x6F80F,0x6F81F,0x6F82F,0x6F83F,0x6F84F,0x6F85F,0x6F86F,0x6F87F,0x6F94F,0x6F963,0x6F977,0x6F98B,0x6F99F,0x6F9B3,0x6F9C7,0x6F9DB,0x6F9EF,0x6FA03,0x6FA17,0x6FA2B,0x6FA3F,0x6FA53,0x6F897,0x6F8A3,0x6F8AF,0x6F8BB,0x6F8C7,0x6F8D3,0x6F8DF,0x6F8EB,0x6F8F7,0x6F903,0x6F90F,0x6F91B,0x6F927,0x6F933]
        self.fx1_length_tr = [0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03]
        #Maridia quicksand etc.
        self.fx1_palettes_ma = [0x6F4EF,0x6F503,0x6F517,0x6F52B,0x6F547,0x6F553,0x6F55F,0x6F56B,0x6F57F,0x6F593,0x6F5A7,0x6F5BB,0x6F5CF,0x6F5E3,0x6F5F7,0x6F60B]
        self.fx1_length_ma = [0x07,0x07,0x07,0x07,0x03,0x03,0x03,0x03,0x07,0x07,0x07,0x07,0x07,0x07,0x07,0x07]
        #Lantern glow
        self.fx1_palettes_lanterns = [0x6EFFD,0x6F00B,0x6F019,0x6F027,0x6F035,0x6F043,0x6F054,0x6F062,0x6F070,0x6F07E]
        self.fx1_length_lanterns = [0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02]

        #this isn't implemented, the other elevator colors are probably managed via the global palette D01A0-0F
        self.ceres_elevator_palettes = [0x137871,0x137881,0x137891,0x1378A1,0x1378B1,0x1378C1,0x1378D1,0x1378E1]
        self.ceres_elevator_palettes_length = [0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05]

        self.beam_palettes = [0x843E1]
        self.beam_palettes_length = [0x4F]

        #This is in the general palette so as a side-effect it also changes things like energy drops, missile tip colors and other things
        self.wave_beam_trail_palettes = [0xD01AA]
        self.wave_beam_trail_length = [0x02]
        
        #Palette used for the tip of super missiles
        self.super_missile_palettes = [0xD01B0]
        self.super_missile_length = [0x02]

        #Single address for grapple extension color, shifted with same hue as beam palette
        self.grapple_beam_palettes = [0xDC687]
        self.grapple_beam_length = [0x00]
        
        #Space Pirate / Mbrain beam color | excluded for now as it also affects a lot of explosion effects
        self.mbrain_beam_palettes = [0xD01A4]
        self.mbrain_beam_length = [0x02]
        
        
        #Boss palettes
        #[sporespawn,kraid,phantoon,botwoon,draygon,crocomire,bomb-torizo,gold-torizo,ridley,mbrain]

        #Draygon, Kraid, Crocomire and Mother Brain have seperate colors hidden in tileset palettes which are addressed in the boss shift function
        #self.spore_spawn_palettes = [0x12E359,0x12E3D9]
        #self.spore_spawn_length = [0x3F,0x8F]
        self.spore_spawn_palettes = [0x12E359]
        self.spore_spawn_length = [0x3F]
        self.kraid_palettes = [0x138687,0x13B3F3,0x13B533,0x13AAB0,0x1386C7]
        self.kraid_length = [0x1F,0x8F,0x7F,0x03,0x0F]
        self.phantoon_palettes = [0x13CA01,0x13CB41]
        self.phantoon_length = [0x0F,0x7F]
        self.botwoon_palettes = [0x199319,0x19971B]
        self.botwoon_length = [0x0F,0x7F]
        #draygon projectiles: 12A237-0F , they are gray so wouldn't shift well to begin with, leaving this out
        self.draygon_palettes = [0x12A1F7,0x1296AF]
        self.draygon_length = [0x4F, 0x1F]
        self.crocomire_palettes = [0x12387D,0x1238CB,0x1238FD]
        self.crocomire_length = [0x1F, 0x08,0x0F]
        self.bomb_torizo_palettes = [0x1506C7,0x150707]
        self.bomb_torizo_length = [0x1F, 0x1F]
        self.gold_torizo_palettes = [0x150747,0x150787,0x020032]
        self.gold_torizo_length = [0x1F,0x1F,0xFF]
        self.ridley_palettes = [0x1362AA,0x13631A,0x13646A]
        self.ridley_length = [0x2F,0xA7,0x29]
        self.mbrain_palettes = [0x149472,0x1494B2,0x14D264,0x16E448,0x16E648,0x16E6AC,0x16E74C,0x16EA08,0x16EC08,0x16EDAC,0x16EF97,0x16F117,0x1494F2,0x14D082,0x16F281]
        self.mbrain_length = [0x1F,0x0F,0x3F,0xFF,0x2C,0x4A,0x4A,0xFF,0xC0,0x98,0xA8,0x78,0x1F,0x5F,0xC4]

        #All enemy palettes have a length of 0x0F
        #enemy_names = [boyon,tatori+young tatori,puyo,cacatac,owtch,mellow,mella,memu,multiviola,polyp,rio,squeept,geruta,holtz,oum,chute,gripper,ripperII,ripper,dragon,shutter1-4,kamer,waver,metaree,fireflea,skultera,sciser,zero,tripper,kamer,sbug+sbug(glitched),sidehopper,desgeega,big sidehopper,big sidehopper(tourian),big desgeega,zoa,viola,skree,yard,"samus" geemer,zeela,norfair geemer,geemer,grey geemer,boulder,ebi+projectile,fune,namihe,coven,yapping maw,kago,beetom,powamp,work robot+work robot(disabled),bull,alcoon,atomic,green kihunter,greenish kihunter,red kihunter,shaktool,zeb,zebbo,gamet,geega,grey zebesian,green zebesian,red zebesian,gold zebesian,pink zebesian,black zebesian]
        self.enemy_palettes = [0x110687,0x110B60,0x11198D,0x111E6A,0x11238B,0x112FF3,0x11320C,0x113264,0x1132BC,0x113A7B,0x113E1C,0x1140D1,0x1145FA,0x114A2B,0x11580C,0x11617B,0x1162C0,0x116457,0x11657B,0x116978,0x116DC7,0x118687,0x1188F0,0x118C0F,0x11900A,0x11965B,0x11980B,0x119B7B,0x119B9B,0x11A051,0x11B0A5,0x11B3A1,0x11B5B3,0x11C63E,0x11C8A6,0x11DFA2,0x11E23C,0x11E57C,0x11E5B0,0x11E5D0,0x130687,0x140687,0x141379,0x14159D,0x1419AC,0x141F4F,0x142AFE,0x14365E,0x144143,0x1446B3,0x145821,0x145BC7,0x146230,0x14699A,0x1469BA,0x1469DA,0x155911,0x19878B,0x1989FD,0x198AC1,0x198EDC,0x190687,0x1906A7,0x1906E7,0x190727,0x1906C7,0x190707 ]

        ####Enemy Palette Groups####
        #Animal "enemies"
        self.animal_palettes = [0x13E7FE,0x13F225,0x19E525,0x19E944]

        #Sidehopper enemies
        self.sidehopper_palettes = [0x11AA48, 0x11B085]

        #Desgeega enemies
        self.desgeega_palettes = [0x11AF85,0x11B217]

        #Lava enemies | not implementing these unless lava color gets randomized eventually | not sure if multiviola should be in here
        #hibashi,puromi,magdollite
        self.lava_enemy_palettes = [0x130CFB,0x131470,0x142C1C]

        #All Metroid-colored enemies:
        self.metroid_palettes = [0x11A725,0x11E9AF,0x14F8E6,0x1494D2]

        self.various_metroid_palettes = [0x14F6D1,0x16E892,0x16E7F2,0x16E8F0]
        self.various_metroid_length = [0x3F,0x27,0x47,0x61]

        #Crateria security eye + face tile
        self.crateria_special_enemies = [0x140F8C,0x1467AC]

        #Wrecked ship sparks
        self.wrecked_ship_special_enemies = [0x146587]

        #Tourian rinka and undocumented zebetite animation palette
        self.tourian_special_enemies = [0x113A5B,0x137D87]

        #Ship is treated as an enemy in the game
        self.ship_palette = 0x11259E

        #G4 statue 2nd half, 1st half is handled via one of the saveroom shifts
        self.statue_palette_ridley = 0x155745
        self.statue_palette_phantoon = 0x155765
        self.statue_base = 0x155785
        self.statue_fadeout_palettes = [0x6E242,0x6E256,0x6E26A,0x6E27E,0x6E292,0x6E2A6,0x6E2BA,0x6E2CE,0x3839C]
        self.statue_fadeout_size = [0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x06,0x07]

        #Degree shuffle array for individual tileset shuffles
        #Insert two entries for [0,1,2,4,5,6,7,8]
        #[0 0 1 1 2 2 3 4 4 5 5 6 6 7 7 8 8 9 10 11 12 13 14 15 16]
        self.degree_list=[]

        #Boss degree list follows this order: [sporespawn,kraid,phantoon,botwoon,draygon,crocomire,bomb-torizo,gold-torizo,ridley,mbrain]
        self.boss_degree_list=[]

        ###########################
        #Suit Palette Information:#
        ###########################
        #Loading and heat-damage glow palettes:
        #Every heat palette is seperated by 2 (unused?) bytes
        #Loader Power Suit: 0x6DB6B, 0x6DBBA, 0x6DC09, 0x6DC58, 0x6DCA4 
        #Heat Power Suit: 0x6E466, 0x6E488, 0x6E4AA, 0x6E4CC, 0x6E4EE, 0x6E510, 0x6E532, 0x6E554, 0x6E576, 0x6E598, 0x6E5BA, 0x6E5DC, 0x6E5FE, 0x6E620, 0x6E642, 0x6E664  |||| final one: 0x6E664 ?
        #Loader Varia Suit: 0x6DCD1, 0x6DD20, 0x6DD6F, 0x6DDBE, 0x6DE0A
        #Heat Varia Suit : 0x6E692, 0x6E6B4, 0x6E6D6, 0x6E6F8, 0x6E71A, 0x6E73C, 0x6E75E, 0x6E780, 0x6E7A2, 0x6E7C4, 0x6E7E6, 0x6E808, 0x6E82A, 0x6E84C, 0x6E86E, 0x6E890  |||| final one: 0x6E890 ?
        #Loader Gravity Suit: 0x6DE37, 0x6DE86, 0x6DED5, 0x6DF24, 0x6DF70
        #Heat Gravity Suit: 0x6E8BE, 0x6E8E0, 0x6E902, 0x6E924, 0x6E946, 0x6E968, 0x6E98A, 0x6E9AC, 0x6E9CE, 0x6E9F0, 0x6EA12, 0x6EA34, 0x6EA56, 0x6EA78, 0x6EA9A, 0x6EABC |||| final one: 0x6EABC ?
        #[$9B:9540-$9B:97E0] not suit palettes?
        #other_palette_offsets = [0x0D9400,0x0D9520,0x0D9540,0x0D9560,0x0D9580,0x0D95A0,0x0D95C0,0x0D95E0,0x0D9600,0x0D9620,0x0D9640,0x0D9660,0x0D9680,0x0D96A0,0x0D9780,0x0D97A0,0x0D97C0,0x0D97E0,0x0D9800,0x0D9820,0x0D9840,0x0D9860,0x0D9880,0x0D98A0,0x0D98C0,0x0D98E0,0x0D9900,0x0D9920,0x0D9940,0x0D9960,0x0D9980,0x0D99A0,0x0D99C0,0x0D99E0,0x0D9A00,0x0D9A20,0x0D9A40,0x0D9A60,0x0D9A80,0x0D9AA0,0x0D9AC0,0x0D9AE0,0x0D9B00,0x0D9B20,0x0D9B40,0x0D9B60,0x0D9B80,0x0D9BA0,0x0D9BC0,0x0D9BE0,0x0D9C00,0x0D9C20,0x0D9C40,0x0D9C60,0x0D9C80,0x0D9CA0,0x0D9CC0,0x0D9CE0,0x0D9D00,0x0D9D20,0x0D9D40,0x0D9D60,0x0D9D80,0x0D9DA0,0x0D9DC0,0x0D9DE0,0x0D9E00,0x0D9E20,0x0D9E40,0x0D9E60,0x0D9E80,0x0D9EA0,0x0D9EC0,0x0D9EE0,0x0D9F00,0x0D9F20,0x0D9F40,0x0D9F60,0x0D9F80,0x0D9FA0,0x0D9FC0,0x0D9FE0,0x0DA000,0x0DA020,0x0DA040,0x0DA060,0x0DA080,0x0DA0A0,0x0DA0C0,0x0DA0E0,0x0DA100]


        #########################
        #        SETTINGS        #
        #########################
        self.settings = settings

        #set to True if all suits should get a separate hue-shift degree
        #"individual_suit_shift": True,
        #set to True if all tileset palettes should get a separate hue-shift degree
        #"individual_tileset_shift": True,
        #Match ship palette with power suit palette
        #"match_ship_and_power": True,
        #Group up similar looking enemy palettes to give them similar looks after hue-shifting
        #(e.g. metroids, big+small sidehoppers)
        #"seperate_enemy_palette_groups": True,
        #Match boss palettes with boss room degree
        #"match_room_shift_with_boss": False,
        ### These variables define what gets shifted
        #"shift_tileset_palette": True,
        #"shift_boss_palettes": True,
        #"shift_suit_palettes": True,
        #"shift_enemy_palettes": True,
        #"shift_beam_palettes": True,
        #"shift_ship_palette": True

        #Change offsets to work with SM practice rom, this was just used for easier feature debugging, changes where new palettes are inserted.
        self.practice_rom = False

        # base address to relocate the compressed palettes
        if self.practice_rom == True:
            # practice rom free space 0x2F51C0 -> 0x2F7FFF
            self.base_address = 0x2F51C0
        else:
            # after the custom credits
            self.base_address = 0x2fe200

        self.power_palette_offsets = [0x0D9400,0x0D9820,0x0D9840,0x0D9860,0x0D9880,0x0D98A0,0x0D98C0,0x0D98E0,0x0D9900,0x0D9B20,0x0D9B40,0x0D9B60,0x0D9B80,0x0D9BA0,0x0D9BC0,0x0D9BE0,0x0D9C00,0x0D9C20,0x0D9C40,0x0D9C60,0x0D9C80,0x0D9CA0,0x0D9CC0,0x0D9CE0,0x0D9D00,0x6DB6B, 0x6DBBA, 0x6DC09, 0x6DC58, 0x6DCA4,0x6E466, 0x6E488, 0x6E4AA, 0x6E4CC, 0x6E4EE, 0x6E510, 0x6E532, 0x6E554, 0x6E576, 0x6E598, 0x6E5BA, 0x6E5DC, 0x6E5FE, 0x6E620, 0x6E642, 0x6E664,0x6DB8F,0x6DC2D,0x6DC7C,0x6DBDE]
        self.varia_palette_offsets = [0x0D9520,0x0D9920,0x0D9940,0x0D9960,0x0D9980,0x0D99A0,0x0D99C0,0x0D99E0,0x0D9A00,0x0D9D20,0x0D9D40,0x0D9D60,0x0D9D80,0x0D9DA0,0x0D9DC0,0x0D9DE0,0x0D9E00,0x0D9E20,0x0D9E40,0x0D9E60,0x0D9E80,0x0D9EA0,0x0D9EC0,0x0D9EE0,0x0D9F00,0x6DCD1, 0x6DD20, 0x6DD6F, 0x6DDBE, 0x6DE0A,0x6E692, 0x6E6B4, 0x6E6D6, 0x6E6F8, 0x6E71A, 0x6E73C, 0x6E75E, 0x6E780, 0x6E7A2, 0x6E7C4, 0x6E7E6, 0x6E808, 0x6E82A, 0x6E84C, 0x6E86E, 0x6E890,0x6DCF5,0x6DD44,0x6DD93,0x6DDE2]
        self.gravity_palette_offsets = [0x0D9540,0x0D9560,0x0D9580,0x0D95A0,0x0D95C0,0x0D95E0,0x0D9600,0x0D9620,0x0D9640,0x0D9660,0x0D9680,0x0D96A0,0x0D9780,0x0D97A0,0x0D97C0,0x0D97E0,0x0D9800,0x0D9A20,0x0D9A40,0x0D9A60,0x0D9A80,0x0D9AA0,0x0D9AC0,0x0D9AE0,0x0D9B00,0x0D9F20,0x0D9F40,0x0D9F60,0x0D9F80,0x0D9FA0,0x0D9FC0,0x0D9FE0,0x0DA000,0x0DA020,0x0DA040,0x0DA060,0x0DA080,0x0DA0A0,0x0DA0C0,0x0DA0E0,0x0DA100,0x6DE37, 0x6DE86, 0x6DED5, 0x6DF24, 0x6DF70,0x6E8BE, 0x6E8E0, 0x6E902, 0x6E924, 0x6E946, 0x6E968, 0x6E98A, 0x6E9AC, 0x6E9CE, 0x6E9F0, 0x6EA12, 0x6EA34, 0x6EA56, 0x6EA78, 0x6EA9A, 0x6EABC,0x6DE5B,0x6DEAA,0x6DEF9,0x6DF48]

    def adjust_hue_degree(self, hsl_color, degree):
        hue = hsl_color[0] * 360
        hue_adj = (hue + degree) % 360
        self.logger.debug("Original hue: {}".format(hue))
        self.logger.debug("Adjusted hue: {}".format(hue_adj))
        self.logger.debug("Degree: {}".format(degree))

        return hue_adj

    def adjust_sat(self, hsl_color, adjustment):
        sat = hsl_color[1] * 100
        sat_adj = (sat+ adjustment) % 100
        self.logger.debug("Original sat: {}".format(sat))
        self.logger.debug("Adjusted sat: {}".format(sat_adj))
        self.logger.debug("Adjustment: {}".format(adjustment))

        return sat_adj

    def adjust_light(self, hsl_color, adjustment):
        lit = hsl_color[2] * 100
        lit_adj = (lit + adjustment) % 100
        self.logger.debug("Original lit: {}".format(lit))
        self.logger.debug("Adjusted lit: {}".format(lit_adj))
        self.logger.debug("Adjustment: {}".format(adjustment))

        return lit_adj

    def RGB_24_to_15(self, color_tuple):
        R_adj = int(color_tuple[0])//8
        G_adj = int(color_tuple[1])//8
        B_adj = int(color_tuple[2])//8

        c = B_adj * 1024 + G_adj * 32 + R_adj
        return (c)

    def RGB_15_to_24(self, SNESColor):
        R = ((SNESColor      ) % 32) * 8
        G = ((SNESColor//32  ) % 32) * 8
        B = ((SNESColor//1024) % 32) * 8

        return (R,G,B)

    def read_word(self, address):
        return self.palettesROM.readWord(address)

    def write_word(self, address, value):
        self.outFile.writeWord(value, address)

    def write_pointer(self, address, value):
        self.outFile.writeBytes(value, 3, address)

    def get_word(self, data, index):
        #print("pr@{}".format(index))
        return data[index] + (data[index+1] << 8)

    def set_word(self, data, index, value):
        (w0, w1) = (value & 0xFF, (value & 0xFF00) >> 8)
        data[index] = w0
        data[index+1] = w1

    #Only used for individual tileset degrees (required to adjust fx1 effects accordingly)
    #Insert two entries for [0,1,2,4,5,6,7,8]
    #[0 0 1 1 2 2 3 4 4 5 5 6 6 7 7 8 8 9 10 11 12 13] 14 15 16
    def generate_tileset_degrees(self):
        for count in range(17):
            if count in (3,9,10,11,12,13,14,15,16):
                degree = self.getDegree()
                self.degree_list.append(degree)
            else:
                degree = self.getDegree()
                self.degree_list.append(degree)
                self.degree_list.append(degree)

    def generate_boss_degrees(self):
        #[sporespawn,kraid,phantoon,botwoon,draygon,crocomire,bomb-torizo,gold-torizo,ridley,mbrain]
        for count in range(11):
            degree = self.getDegree()
            self.boss_degree_list.append(degree)

    def hue_shift_palette_lists(self, degree, address_list, size_list):
        for count, address in enumerate(address_list):
            for i in range(size_list[count]+1):
                self.logger.debug("Fx1 address: {} at offset: {}".format(hex(address), hex(i*2)))

                read_address = address + (i*2)
                int_value_LE = self.read_word(read_address)

                #Convert 15bit RGB to 24bit RGB
                rgb_value_24 = self.RGB_15_to_24(int_value_LE)

                #24bit RGB to HLS
                hls_col = colorsys.rgb_to_hls(rgb_value_24[0]/255.0,
                                              rgb_value_24[1]/255.0,
                                              rgb_value_24[2]/255.0)

                #Generate new hue based on degree
                new_hue = self.adjust_hue_degree(hls_col, degree)/360.0

                rgb_final = colorsys.hls_to_rgb(new_hue, hls_col[1], hls_col[2])

                #Colorspace is in [0...1] format during conversion and needs to be multiplied by 255
                rgb_final = (int(rgb_final[0]*255), int(rgb_final[1]*255), int(rgb_final[2]*255))

                BE_hex_color = self.RGB_24_to_15(rgb_final)

                self.write_word(read_address, BE_hex_color)

    def hue_shift_palette_single_offsets(self, data, offset_list, degree, address):
        #if green brinstar or crateria palette, shuffle blue door caps to also shuffle lower crateria color
        if not self.settings['no_blue_door_palette'] and ( (address == 0x213264) or (address == 0x21335F) ):
            copy_offset_list = (offset_list+self.bluedoor_bytes)
        else:
            copy_offset_list = offset_list

        copy_offset_list = offset_list
        for offset in copy_offset_list:
            #Convert from LE to BE
            int_value_LE = self.get_word(data, offset)

            #Convert 15bit RGB to 24bit RGB
            rgb_value_24 = self.RGB_15_to_24(int_value_LE)

            self.logger.debug("24RGB: {}".format(rgb_value_24))

            #24bit RGB to HLS
            hls_col = colorsys.rgb_to_hls(rgb_value_24[0]/255.0,rgb_value_24[1]/255.0,rgb_value_24[2]/255.0)

            self.logger.debug("hls_col: {}".format(hls_col))

            #Generate new hue based on degree
            new_hue = self.adjust_hue_degree(hls_col, degree)/360.0

            rgb_final = colorsys.hls_to_rgb(new_hue,hls_col[1],hls_col[2])

            #Colorspace is in [0...1] format during conversion and needs to be multiplied by 255
            rgb_final = (int(rgb_final[0]*255),int(rgb_final[1]*255),int(rgb_final[2]*255))

            self.logger.debug("New 24RGB 1 {}".format(rgb_final))

            BE_hex_color = self.RGB_24_to_15(rgb_final)

            self.logger.debug("15bit BE_hex_color: {}".format(hex(BE_hex_color)))

            self.set_word(data, offset, BE_hex_color)

            self.logger.debug("write decomp palette offset: {} value: {}".format(hex(offset), BE_hex_color))

    #Function to shift palette hues by set degree for a palette with fixed size 0x0F
    def hue_shift_fixed_size_palette(self, base_address, degree,size, exclude = [""]):
        self.logger.debug("Shifting suit palette at {} by degree {}".format(hex(base_address), degree))
        
        for i in range(0,size+1):
		
            if i in exclude:
                continue
                
            read_address=base_address+(i*2)
            int_value_LE = self.read_word(read_address)

            #Convert 15bit RGB to 24bit RGB
            rgb_value_24 = self.RGB_15_to_24(int_value_LE)

            #24bit RGB to HLS
            hls_col = colorsys.rgb_to_hls(rgb_value_24[0]/255.0, rgb_value_24[1]/255.0, rgb_value_24[2]/255.0)

            #Generate new hue based on degree
            new_hue = self.adjust_hue_degree(hls_col, degree)/360.0

            rgb_final = colorsys.hls_to_rgb(new_hue,hls_col[1],hls_col[2])

            #Colorspace is in [0...1] format during conversion and needs to be multiplied by 255
            rgb_final = (int(rgb_final[0]*255), int(rgb_final[1]*255), int(rgb_final[2]*255))

            BE_hex_color = self.RGB_24_to_15(rgb_final)

            self.write_word(read_address, BE_hex_color)

    def hue_shift_tileset_palette(self, degree):
        count=-1
        for address in self.tileset_palette_offsets:
            count = count+1
            if self.settings["individual_tileset_shift"]:
                degree = self.degree_list[count]

            data = self.decompress(address)

            self.hue_shift_palette_single_offsets(data, self.palette_single_bytes, degree, address)

            #special case for mother brain room
            if address == 0x213BC1:
                temp_TLS_palette_subsets = [0xA0,0xC0,0xE0]
            #and kraids room
            elif address == 0x213510: 
                temp_TLS_palette_subsets = [0x80,0xA0,0xC0]
            #and draygons room
            elif address == 0x213A2C:
                temp_TLS_palette_subsets = [0x80,0xC0,0xE0]
            else:
                temp_TLS_palette_subsets = [0x80,0xA0,0xC0,0xE0]

            #skip 2-byte-pair at index 0 (this is the transparency color)
            for subset in temp_TLS_palette_subsets:
                for j in range(1,15):
                    #Convert from LE to BE
                    int_value_LE = self.get_word(data, subset+(j*2))

                    #Convert 15bit RGB to 24bit RGB
                    rgb_value_24 = self.RGB_15_to_24(int_value_LE)

                    self.logger.debug("24RGB: {}".format(rgb_value_24))

                    #24bit RGB to HLS
                    hls_col = colorsys.rgb_to_hls(rgb_value_24[0]/255.0,rgb_value_24[1]/255.0,rgb_value_24[2]/255.0)

                    #Generate new hue based on degree
                    new_hue = self.adjust_hue_degree(hls_col, degree)/360.0

                    rgb_final = colorsys.hls_to_rgb(new_hue,hls_col[1],hls_col[2])

                    #Colorspace is in [0...1] format during conversion and needs to be multiplied by 255
                    rgb_final = (int(rgb_final[0]*255),int(rgb_final[1]*255),int(rgb_final[2]*255))

                    self.logger.debug("New 24RGB 2: {}".format(rgb_final))

                    BE_hex_color = self.RGB_24_to_15(rgb_final)

                    self.logger.debug("15bit BE_hex_color: {}".format(hex(BE_hex_color)))

                    self.set_word(data, subset+(j*2), BE_hex_color)

                    self.logger.debug("write decomp palette index: {} value: {}".format(hex(subset+(j*2)), BE_hex_color))

            insert_address = self.base_address + (count*0x100)
            assert insert_address <= 0x2FFF00, "Possible ROM corruption by palette rando"
            self.pointers_to_insert.append(insert_address)
            self.logger.debug("pointers_to_insert: {}".format(self.pointers_to_insert))

            #Recompress palette and re-insert at offset
            self.compress(insert_address, data)
        return

    def boss_palette_shift(self, degree):
        if self.settings["global_shift"] == True:
            self.hue_shift_palette_lists(degree, self.spore_spawn_palettes, self.spore_spawn_length)
            self.hue_shift_palette_lists(degree, self.kraid_palettes, self.kraid_length)
            self.hue_shift_palette_lists(degree, self.phantoon_palettes, self.phantoon_length)
            self.hue_shift_palette_lists(degree, self.botwoon_palettes, self.botwoon_length)
            self.hue_shift_palette_lists(degree, self.draygon_palettes, self.draygon_length)
            self.hue_shift_palette_lists(degree, self.crocomire_palettes, self.crocomire_length)
            self.hue_shift_palette_lists(degree, self.bomb_torizo_palettes, self.bomb_torizo_length)
            self.hue_shift_palette_lists(degree, self.gold_torizo_palettes, self.gold_torizo_length)
            self.hue_shift_palette_lists(degree, self.ridley_palettes, self.ridley_length)
            self.hue_shift_palette_lists(degree, self.mbrain_palettes, self.mbrain_length)
        elif self.settings["match_room_shift_with_boss"]:
            self.hue_shift_palette_lists(self.degree_list[6], self.spore_spawn_palettes, self.spore_spawn_length)
            self.hue_shift_palette_lists(self.degree_list[22], self.kraid_palettes, self.kraid_length)
            self.hue_shift_palette_lists(self.degree_list[4], self.phantoon_palettes, self.phantoon_length)
            self.hue_shift_palette_lists(self.degree_list[11], self.botwoon_palettes, self.botwoon_length)
            self.hue_shift_palette_lists(self.degree_list[24], self.draygon_palettes, self.draygon_length)
            self.hue_shift_palette_lists(self.degree_list[23], self.crocomire_palettes, self.crocomire_length)
            self.hue_shift_palette_lists(self.degree_list[0], self.bomb_torizo_palettes, self.bomb_torizo_length)
            self.hue_shift_palette_lists(self.degree_list[9], self.gold_torizo_palettes, self.gold_torizo_length)
            self.hue_shift_palette_lists(self.degree_list[9], self.ridley_palettes, self.ridley_length)
            self.hue_shift_palette_lists(self.degree_list[14], self.mbrain_palettes, self.mbrain_length)
        else:
            #[sporespawn,kraid,phantoon,botwoon,draygon,crocomire,bomb-torizo,gold-torizo,ridley,mbrain]
            self.hue_shift_palette_lists(self.boss_degree_list[0], self.spore_spawn_palettes, self.spore_spawn_length)
            self.hue_shift_palette_lists(self.boss_degree_list[1], self.kraid_palettes, self.kraid_length)
            self.hue_shift_palette_lists(self.boss_degree_list[2], self.phantoon_palettes, self.phantoon_length)
            self.hue_shift_palette_lists(self.boss_degree_list[3], self.botwoon_palettes, self.botwoon_length)
            self.hue_shift_palette_lists(self.boss_degree_list[4], self.draygon_palettes, self.draygon_length)
            self.hue_shift_palette_lists(self.boss_degree_list[5], self.crocomire_palettes, self.crocomire_length)
            self.hue_shift_palette_lists(self.boss_degree_list[6], self.bomb_torizo_palettes, self.bomb_torizo_length)
            self.hue_shift_palette_lists(self.boss_degree_list[7], self.gold_torizo_palettes, self.gold_torizo_length)
            self.hue_shift_palette_lists(self.boss_degree_list[8], self.ridley_palettes, self.ridley_length)
            self.hue_shift_palette_lists(self.boss_degree_list[9], self.mbrain_palettes, self.mbrain_length)    

        if self.settings["shift_tileset_palette"] and len(self.pointers_to_insert) == 0:
            raise Exception("tileset shifting needs to be called before boss palette shifting if both are active!")

        if self.settings["shift_tileset_palette"]:
            boss_address_list = [self.pointers_to_insert[14], self.pointers_to_insert[22], self.pointers_to_insert[24]]
        else:
            boss_address_list = [0x213BC1,0x213510,0x213A2C]

        for address in boss_address_list:
            #kraid's room tileset sub-palettes containing boss colors
            if address == 0x213510 or (self.settings["shift_tileset_palette"] and address == self.pointers_to_insert[22]):
                temp_TLS_palette_subsets = [0xE0]
                if self.settings["global_shift"] == False:
                    if self.settings["match_room_shift_with_boss"]:
                        degree = self.degree_list[22]
                    else:
                        degree = self.boss_degree_list[1]                
            #mother brain's room tileset sub-palettes containing boss colors
            if address == 0x213BC1 or (self.settings["shift_tileset_palette"] and address == self.pointers_to_insert[14]):
                temp_TLS_palette_subsets = [0x80]
                if self.settings["global_shift"] == False:
                    if self.settings["match_room_shift_with_boss"]:
                        degree = self.degree_list[14]
                    else:
                        degree = self.boss_degree_list[9]    
            #draygon's room tileset sub-palettes containing boss colors
            if address == 0x213A2C or (self.settings["shift_tileset_palette"] and address == self.pointers_to_insert[24]):
                temp_TLS_palette_subsets = [0xA0]
                if self.settings["global_shift"] == False:
                    if self.settings["match_room_shift_with_boss"]:
                        degree = self.degree_list[24]
                    else:
                        degree = self.boss_degree_list[4]

            data = self.decompress(address)

            for subset in temp_TLS_palette_subsets:
                for j in range(1,15):
                    #Convert from LE to BE
                    int_value_LE = self.get_word(data, subset+(j*2))

                    #Convert 15bit RGB to 24bit RGB
                    rgb_value_24 = self.RGB_15_to_24(int_value_LE)

                    self.logger.debug("24RGB: {}".format(rgb_value_24))

                    #24bit RGB to HLS
                    hls_col = colorsys.rgb_to_hls(rgb_value_24[0]/255.0,rgb_value_24[1]/255.0,rgb_value_24[2]/255.0)

                    #Generate new hue based on degree
                    new_hue = self.adjust_hue_degree(hls_col, degree)/360.0

                    rgb_final = colorsys.hls_to_rgb(new_hue,hls_col[1],hls_col[2])

                    #Colorspace is in [0...1] format during conversion and needs to be multiplied by 255
                    rgb_final = (int(rgb_final[0]*255),int(rgb_final[1]*255),int(rgb_final[2]*255))

                    self.logger.debug("New 24RGB 3: {}".format(rgb_final))

                    BE_hex_color = self.RGB_24_to_15(rgb_final)

                    self.logger.debug("15bit BE_hex_color: {}".format(hex(BE_hex_color)))

                    self.set_word(data, subset+(j*2), BE_hex_color)

                    self.logger.debug("write decomp palette index: {} value: {}".format(hex(subset+(j*2)), BE_hex_color))

            #quick hack to re-insert, should work without issues
            insert_address = address
                        
            if address == 0x213BC1 and not self.settings["shift_tileset_palette"]:
                insert_address= self.base_address + (0*0x100)
                self.compress(insert_address, data)
                self.write_pointer(self.pointer_addresses[14], pc_to_snes(insert_address))
            elif address == 0x213510 and not self.settings["shift_tileset_palette"]:
                insert_address = self.base_address + (1*0x100)
                self.compress(insert_address, data)
                self.write_pointer(self.pointer_addresses[22], pc_to_snes(insert_address))
            elif address == 0x213A2C and not self.settings["shift_tileset_palette"]:
                insert_address = self.base_address + (2*0x100)
                self.compress(insert_address, data)
                self.write_pointer(self.pointer_addresses[24], pc_to_snes(insert_address))
            else:        
                #Recompress palette and re-insert at offset
                self.compress(insert_address, data)

    def getDegree(self):
        if self.invert == True:
            # use [0-360] range for easier calculations
            minDegree = self.min_degree + 180
            maxDegree = self.max_degree + 180
            excludeRange = maxDegree - minDegree

            rand = random.randint(0, 360 - excludeRange)

            if rand > minDegree:
                rand += excludeRange
            rand -= 180

            return rand
        else:
            return random.randint(self.min_degree, self.max_degree)

    def randomize(self):
        degree = self.getDegree()

        if self.settings["global_shift"] == False:
            self.generate_tileset_degrees()
            self.generate_boss_degrees()

        if self.settings["shift_tileset_palette"]:
            self.hue_shift_tileset_palette(degree)

            if self.settings["individual_tileset_shift"]:
                self.hue_shift_palette_lists(self.degree_list[0], self.fx1_palettes_cr, self.fx1_length_cr)
                self.hue_shift_palette_lists(self.degree_list[6], self.fx1_palettes_gb, self.fx1_length_gb)
                self.hue_shift_palette_lists(self.degree_list[7], self.fx1_palettes_rb, self.fx1_length_rb)
                self.hue_shift_palette_lists(self.degree_list[4], self.fx1_palettes_ws, self.fx1_length_ws)
                self.hue_shift_palette_lists(self.degree_list[13], self.fx1_palettes_tr, self.fx1_length_tr)
                self.hue_shift_palette_lists(self.degree_list[11], self.fx1_palettes_ma, self.fx1_length_ma)
                self.hue_shift_palette_lists(self.degree_list[7], self.fx1_palettes_lanterns, self.fx1_length_lanterns)
                self.hue_shift_palette_lists(self.degree_list[6], self.crateria_special_enemies, [0x0F,0x0F]) 
                self.logger.debug("Wrecked Ship sparks shifted by {}".format(self.degree_list[4]))
                self.hue_shift_palette_lists(self.degree_list[4], self.wrecked_ship_special_enemies, [0x0F])
                self.hue_shift_palette_lists(self.degree_list[13], self.tourian_special_enemies, [0x0F,0x0F])
                self.hue_shift_fixed_size_palette(self.statue_palette_ridley, self.degree_list[17], 0x0F)
                self.hue_shift_fixed_size_palette(self.statue_palette_phantoon, self.degree_list[17], 0x0F)
                self.hue_shift_fixed_size_palette(self.statue_base, self.degree_list[17], 0x0F)
                self.hue_shift_palette_lists(self.degree_list[17], self.statue_fadeout_palettes, self.statue_fadeout_size)
            else:
                self.hue_shift_palette_lists(degree, self.fx1_palettes_cr, self.fx1_length_cr)
                self.hue_shift_palette_lists(degree, self.fx1_palettes_gb, self.fx1_length_gb)
                self.hue_shift_palette_lists(degree, self.fx1_palettes_rb, self.fx1_length_rb)
                self.hue_shift_palette_lists(degree, self.fx1_palettes_ws, self.fx1_length_ws)
                self.hue_shift_palette_lists(degree, self.fx1_palettes_tr, self.fx1_length_tr)
                self.hue_shift_palette_lists(degree, self.fx1_palettes_ma, self.fx1_length_ma)
                self.hue_shift_palette_lists(degree, self.fx1_palettes_lanterns, self.fx1_length_lanterns)
                self.hue_shift_palette_lists(degree, self.crateria_special_enemies, [0x0F,0x0F])
                self.hue_shift_palette_lists(degree, self.wrecked_ship_special_enemies, [0x0F])
                self.hue_shift_palette_lists(degree, self.tourian_special_enemies, [0x0F,0x0F])
                self.hue_shift_fixed_size_palette(self.statue_palette_ridley,degree, 0x0F)
                self.hue_shift_fixed_size_palette(self.statue_palette_phantoon,degree, 0x0F)
                self.hue_shift_fixed_size_palette(self.statue_base,degree, 0x0F)
                self.hue_shift_palette_lists(degree, self.statue_fadeout_palettes, self.statue_fadeout_size)


            i=-1
            for p_update in self.pointers_to_insert:
                i=i+1
                self.logger.debug("New Pointer Address: {}".format(p_update))
                self.logger.debug("Write this to file: {}".format(hex(pc_to_snes(p_update))))
                self.write_pointer(self.pointer_addresses[i], pc_to_snes(p_update))

        #this NEEDS to be called after the tileset palette shift function (if tileset shift actually gets called) because it references newly created pointers
        if self.settings["shift_boss_palettes"]:
            self.boss_palette_shift(degree)

        if self.settings["shift_enemy_palettes"]:
            if self.settings["seperate_enemy_palette_groups"]:
                enemy_degree = self.getDegree()
                self.hue_shift_palette_lists(enemy_degree, self.metroid_palettes, [0x0F,0x0F,0x0F,0x0F])
                self.hue_shift_palette_lists(enemy_degree, self.various_metroid_palettes, self.various_metroid_length)
                enemy_degree = self.getDegree()
                self.hue_shift_palette_lists(enemy_degree, self.desgeega_palettes, [0x0F,0x0F])
                enemy_degree = self.getDegree()
                self.hue_shift_palette_lists(enemy_degree, self.sidehopper_palettes, [0x0F,0x0F])
                enemy_degree = self.getDegree()
                self.hue_shift_palette_lists(enemy_degree, self.animal_palettes, [0x0F,0x0F,0x0F,0x0F])
                for address in self.enemy_palettes:
                    enemy_degree = self.getDegree()
                    self.hue_shift_fixed_size_palette(address, enemy_degree, 0x0F)
            else:
                self.enemy_palettes.extend(self.metroid_palettes)
                self.enemy_palettes.extend(self.desgeega_palettes)
                self.enemy_palettes.extend(self.sidehopper_palettes)
                self.enemy_palettes.extend(self.animal_palettes)
                if self.settings["global_shift"] == True:
                    enemy_degree = degree
                else:
                    enemy_degree = self.getDegree()
                self.hue_shift_palette_lists(enemy_degree, self.various_metroid_palettes, self.various_metroid_length)
                for address in self.enemy_palettes:
                    if self.settings["global_shift"] == True:
                        enemy_degree = degree
                    else:
                        enemy_degree = self.getDegree()
                    self.hue_shift_fixed_size_palette(address, enemy_degree, 0x0F)

        self.logger.debug("degree_list: {}".format(self.degree_list))

        if self.settings["shift_beam_palettes"]:
            if self.settings["global_shift"] == True:
                beam_degree = degree
            else:
                beam_degree = self.getDegree()
            self.hue_shift_palette_lists(beam_degree, self.beam_palettes, self.beam_palettes_length)
            self.hue_shift_palette_lists(beam_degree, self.wave_beam_trail_palettes, self.wave_beam_trail_length)
            self.hue_shift_palette_lists(beam_degree, self.grapple_beam_palettes, self.grapple_beam_length)
            self.hue_shift_palette_lists(beam_degree, self.super_missile_palettes, self.super_missile_length)

        if self.settings["shift_ship_palette"] and not self.settings["shift_suit_palettes"]:
                if self.settings["match_ship_and_power"]:
                    ship_degree = 0
                else:
                    if self.settings["global_shift"] == True:
                        ship_degree = degree
                    else:
                        ship_degree = self.getDegree()
                self.hue_shift_fixed_size_palette(self.ship_palette, ship_degree, 0x0F)

        if self.settings["shift_suit_palettes"]:
            if self.settings["global_shift"] == True:
                base_degree = degree
            else:
                base_degree = self.getDegree()

            for address in self.power_palette_offsets:
                self.hue_shift_fixed_size_palette(address, base_degree, 0x0F, [0x04])

            if self.settings["match_ship_and_power"]:
                ship_degree = base_degree
            else:
                ship_degree = self.getDegree()

            if self.settings["shift_ship_palette"]:
                self.hue_shift_fixed_size_palette(self.ship_palette, ship_degree, 0x0F)

            if self.settings["individual_suit_shift"]:
                degree = self.getDegree()

            for address in self.varia_palette_offsets:
                self.hue_shift_fixed_size_palette(address, degree, 0x0F, [0x04])

            if self.settings["individual_suit_shift"]:
                degree = self.getDegree()

            for address in self.gravity_palette_offsets:
                self.hue_shift_fixed_size_palette(address, degree, 0x0F, [0x04])    

    def compress(self, address, data):
        length = self.romPatcher.compress(address, data)

        # cp new compressed data into vanilla palettes data (used for boss palettes rando)
        self.outFile.seek(address)
        for i in range(length):
            self.palettesROM.data[address+i] = self.outFile.readByte()

    def decompress(self, address):
        (compressedLength, rawData) = self.romLoader.decompress(address)
        return rawData
