from .requirements import *
from .location import Location
from ..locations.all import *


class Dungeon1:
    def __init__(self, options, world_setup, r):
        entrance = Location(dungeon=1)
        entrance.add(DungeonChest(0x113), DungeonChest(0x115), DungeonChest(0x10E))
        Location(dungeon=1).add(DroppedKey(0x116)).connect(entrance, OR(BOMB, r.push_hardhat)) # hardhat beetles (can kill with bomb)
        Location(dungeon=1).add(DungeonChest(0x10D)).connect(entrance, OR(r.attack_hookshot_powder, SHIELD)) # moldorm spawn chest
        stalfos_keese_room = Location(dungeon=1).add(DungeonChest(0x114)).connect(entrance, AND(OR(r.attack_skeleton, SHIELD),r.attack_hookshot_powder)) # 2 stalfos 2 keese room
        Location(dungeon=1).add(DungeonChest(0x10C)).connect(entrance, BOMB) # hidden seashell room
        dungeon1_upper_left = Location(dungeon=1).connect(entrance, AND(KEY1, FOUND(KEY1, 3)))
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=1).add(OwlStatue(0x103), OwlStatue(0x104)).connect(dungeon1_upper_left, STONE_BEAK1)
        feather_chest = Location(dungeon=1).add(DungeonChest(0x11D)).connect(dungeon1_upper_left, SHIELD)  # feather location, behind spike enemies. can shield bump into pit (only shield works)
        boss_key = Location(dungeon=1).add(DungeonChest(0x108)).connect(entrance, AND(FEATHER, KEY1, FOUND(KEY1, 3))) # boss key
        dungeon1_right_side = Location(dungeon=1).connect(entrance, AND(KEY1, FOUND(KEY1, 3)))
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=1).add(OwlStatue(0x10A)).connect(dungeon1_right_side, STONE_BEAK1)
        dungeon1_3_of_a_kind = Location(dungeon=1).add(DungeonChest(0x10A)).connect(dungeon1_right_side, OR(r.attack_hookshot_no_bomb, SHIELD)) # three of a kind, shield stops the suit from changing
        dungeon1_miniboss = Location(dungeon=1).connect(dungeon1_right_side, AND(r.miniboss_requirements[world_setup.miniboss_mapping[0]], FEATHER))
        dungeon1_boss = Location(dungeon=1).connect(dungeon1_miniboss, NIGHTMARE_KEY1)
        boss = Location(dungeon=1).add(HeartContainer(0x106), Instrument(0x102)).connect(dungeon1_boss, r.boss_requirements[world_setup.boss_mapping[0]])

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            stalfos_keese_room.connect(entrance, r.attack_hookshot_powder) # stalfos jump away when you press a button.
            dungeon1_3_of_a_kind.connect(dungeon1_right_side, BOMB) # use timed bombs to match the 3 of a kinds
        
        if options.logic == 'glitched' or options.logic == 'hell':
            boss_key.connect(entrance, r.super_jump_feather)  # super jump
            dungeon1_miniboss.connect(dungeon1_right_side, r.miniboss_requirements[world_setup.miniboss_mapping[0]]) # damage boost or buffer pause over the pit to cross or mushroom
        
        if options.logic == 'hell':
            feather_chest.connect(dungeon1_upper_left, SWORD)  # keep slashing the spiked beetles until they keep moving 1 pixel close towards you and the pit, to get them to fall
            boss_key.connect(entrance, AND(r.damage_boost, FOUND(KEY1,3))) # damage boost off the hardhat to cross the pit
            
        self.entrance = entrance


class NoDungeon1:
    def __init__(self, options, world_setup, r):
        entrance = Location(dungeon=1)
        Location(dungeon=1).add(HeartContainer(0x106), Instrument(0x102)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[0]])
        self.entrance = entrance
