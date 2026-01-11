from .requirements import *
from .location import Location
from ..locations.all import *


class Dungeon3:
    def __init__(self, options, world_setup, r):
        entrance = Location(dungeon=3)
        dungeon3_reverse_eye = Location(dungeon=3).add(DungeonChest(0x153)).connect(entrance, PEGASUS_BOOTS) # Right side reverse eye
        area2 = Location(dungeon=3).connect(entrance, POWER_BRACELET)
        Location(dungeon=3).add(DungeonChest(0x151)).connect(area2, r.attack_hookshot_powder)  # First chest with key
        area2.add(DungeonChest(0x14F))  # Second chest with slime
        area3 = Location(dungeon=3).connect(area2, OR(r.attack_hookshot_powder, PEGASUS_BOOTS)) # need to kill slimes to continue or pass through left path
        dungeon3_zol_stalfos = Location(dungeon=3).add(DungeonChest(0x14E)).connect(area3, AND(PEGASUS_BOOTS, r.attack_skeleton))  # 3th chest requires killing the slime behind the crystal pillars

        # now we can go 4 directions,
        area_up = Location(dungeon=3).connect(area3, AND(KEY3, FOUND(KEY3, 8)))
        dungeon3_north_key_drop = Location(dungeon=3).add(DroppedKey(0x154)).connect(area_up, r.attack_skeleton) # north key drop
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=3).add(OwlStatue(0x154)).connect(area_up, STONE_BEAK3)
        dungeon3_raised_blocks_north = Location(dungeon=3).add(DungeonChest(0x14C)) # chest locked behind raised blocks near staircase
        dungeon3_raised_blocks_east = Location(dungeon=3).add(DungeonChest(0x150)) # chest locked behind raised blocks next to slime chest
        area_up.connect(dungeon3_raised_blocks_north, r.hit_switch, one_way=True) # hit switch to reach north chest
        area_up.connect(dungeon3_raised_blocks_east, r.hit_switch, one_way=True) # hit switch to reach east chest
        
        area_left = Location(dungeon=3).connect(area3, AND(KEY3, FOUND(KEY3, 8)))
        area_left_key_drop = Location(dungeon=3).add(DroppedKey(0x155)).connect(area_left, r.attack_hookshot) # west key drop (no longer requires feather to get across hole), can use boomerang to knock owls into pit

        area_down = Location(dungeon=3).connect(area3, AND(KEY3, FOUND(KEY3, 8)))
        dungeon3_south_key_drop = Location(dungeon=3).add(DroppedKey(0x158)).connect(area_down, r.attack_hookshot) # south keydrop, can use boomerang to knock owls into pit

        area_right = Location(dungeon=3).connect(area3, AND(KEY3, FOUND(KEY3, 4)))  # We enter the top part of the map here.
        Location(dungeon=3).add(DroppedKey(0x14D)).connect(area_right, r.attack_hookshot_powder)  # key after the stairs.

        dungeon3_nightmare_key_chest = Location(dungeon=3).add(DungeonChest(0x147)).connect(area_right, AND(BOMB, FEATHER, PEGASUS_BOOTS))  # nightmare key chest
        dungeon3_post_dodongo_chest = Location(dungeon=3).add(DungeonChest(0x146)).connect(area_right, AND(r.attack_hookshot_powder, r.miniboss_requirements[world_setup.miniboss_mapping[2]]))  # boots after the miniboss
        compass_chest = Location(dungeon=3).add(DungeonChest(0x142)).connect(area_right, OR(SWORD, BOMB, AND(SHIELD, r.attack_hookshot_powder))) # bomb only activates with sword, bomb or shield
        dungeon3_3_bombite_room = Location(dungeon=3).add(DroppedKey(0x141)).connect(compass_chest, BOMB) # 3 bombite room
        Location(dungeon=3).add(DroppedKey(0x148)).connect(area_right, r.attack_no_boomerang) # 2 zol 2 owl drop key
        Location(dungeon=3).add(DungeonChest(0x144)).connect(area_right, r.attack_skeleton)  # map chest
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=3).add(OwlStatue(0x140), OwlStatue(0x147)).connect(area_right, STONE_BEAK3)

        towards_boss1 = Location(dungeon=3).connect(area_right, AND(KEY3, FOUND(KEY3, 5)))
        towards_boss2 = Location(dungeon=3).connect(towards_boss1, AND(KEY3, FOUND(KEY3, 6)))
        towards_boss3 = Location(dungeon=3).connect(towards_boss2, AND(KEY3, FOUND(KEY3, 7)))
        towards_boss4 = Location(dungeon=3).connect(towards_boss3, AND(KEY3, FOUND(KEY3, 8)))

        # Just the whole area before the boss, requirements for the boss itself and the rooms before it are the same.
        pre_boss = Location(dungeon=3).connect(towards_boss4, AND(r.attack_no_boomerang, FEATHER, PEGASUS_BOOTS))
        pre_boss.add(DroppedKey(0x15B))

        boss = Location(dungeon=3).add(HeartContainer(0x15A), Instrument(0x159)).connect(pre_boss, AND(NIGHTMARE_KEY3, r.boss_requirements[world_setup.boss_mapping[2]]))

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            dungeon3_3_bombite_room.connect(area_right, BOOMERANG) # 3 bombite room from the left side, grab item with boomerang
            dungeon3_reverse_eye.connect(entrance, r.hookshot_over_pit) # hookshot the chest to get to the right side
            dungeon3_north_key_drop.connect(area_up, r.throw_pot) # use pots to kill the enemies
            dungeon3_south_key_drop.connect(area_down, r.throw_pot) # use pots to kill enemies
            area_up.connect(dungeon3_raised_blocks_north, r.throw_pot, one_way=True) # use pots to hit the switch
            area_up.connect(dungeon3_raised_blocks_east, AND(r.throw_pot, r.attack_hookshot_powder), one_way=True) # use pots to hit the switch

        if options.logic == 'glitched' or options.logic == 'hell':
            area2.connect(dungeon3_raised_blocks_east, AND(r.attack_hookshot_powder, r.super_jump_feather), one_way=True) # use superjump to get over the bottom left block
            area3.connect(dungeon3_raised_blocks_north, AND(OR(PEGASUS_BOOTS, r.hookshot_clip_block), r.shaq_jump), one_way=True) # use shagjump (unclipped superjump next to movable block) from north wall to get on the blocks. Instead of boots can also get to that area with a hookshot clip past the movable block
            area3.connect(dungeon3_zol_stalfos, r.hookshot_clip_block, one_way=True) # hookshot clip through the northern push block next to raised blocks chest to get to the zol
            dungeon3_nightmare_key_chest.connect(area_right, AND(r.super_jump_feather, BOMB)) # superjump to right side 3 gap via top wall and jump the 2 gap
            dungeon3_post_dodongo_chest.connect(area_right, AND(r.super_jump_feather, FOUND(KEY3, 6))) # superjump from keyblock path. use 2 keys to open enough blocks TODO: nag messages to skip a key
        
        if options.logic == 'hell':
            area2.connect(dungeon3_raised_blocks_east, r.boots_superhop, one_way=True) # use boots superhop to get over the bottom left block
            area3.connect(dungeon3_raised_blocks_north, r.boots_superhop, one_way=True) # use boots superhop off top wall or left wall to get on raised blocks
            area_up.connect(dungeon3_zol_stalfos, AND(r.super_jump_feather, r.attack_skeleton), one_way=True) # use superjump near top blocks chest to get to zol without boots, keep wall clip on right wall to get a clip on left wall or use obstacles
            area_left_key_drop.connect(area_left, r.shield_bump) # knock everything into the pit including the teleporting owls
            dungeon3_south_key_drop.connect(area_down, r.shield_bump) # knock everything into the pit including the teleporting owls
            dungeon3_nightmare_key_chest.connect(area_right, AND(r.super_jump_feather, r.shield_bump)) # superjump into jumping stalfos and shield bump to right ledge
            dungeon3_nightmare_key_chest.connect(area_right, AND(BOMB, r.pit_buffer_boots, HOOKSHOT)) # boots bonk across the pits with pit buffering and hookshot to the chest
            compass_chest.connect(dungeon3_3_bombite_room, OR(BOW, MAGIC_ROD, AND(OR(FEATHER, PEGASUS_BOOTS), OR(SWORD, MAGIC_POWDER))), one_way=True) # 3 bombite room from the left side, use a bombite to blow open the wall without bombs
            pre_boss.connect(towards_boss4, AND(r.attack_no_boomerang, FEATHER, POWER_BRACELET)) # use bracelet super bounce glitch to pass through first part underground section
            pre_boss.connect(towards_boss4, AND(r.attack_no_boomerang, r.boots_bonk_2d_spikepit)) # use medicine invulnerability to pass through the 2d section with a boots bonk to reach the staircase
            
        self.entrance = entrance


class NoDungeon3:
    def __init__(self, options, world_setup, r):
        entrance = Location(dungeon=3)
        Location(dungeon=3).add(HeartContainer(0x15A), Instrument(0x159)).connect(entrance, AND(POWER_BRACELET, r.boss_requirements[
            world_setup.boss_mapping[2]]))

        self.entrance = entrance
