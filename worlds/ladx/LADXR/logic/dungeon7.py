from .requirements import *
from .location import Location
from ..locations.all import *


class Dungeon7:
    def __init__(self, options, world_setup, r):
        entrance = Location(dungeon=7)
        first_key = Location(dungeon=7).add(DroppedKey(0x210)).connect(entrance, r.attack_hookshot_powder)
        topright_pillar_area = Location(dungeon=7).connect(entrance, KEY7)
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=7).add(OwlStatue(0x216)).connect(topright_pillar_area, STONE_BEAK7)
        topright_pillar = Location(dungeon=7).add(DungeonChest(0x212)).connect(topright_pillar_area, POWER_BRACELET)  # map chest
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=7).add(OwlStatue(0x204)).connect(topright_pillar_area, STONE_BEAK7)
        topright_pillar_area.add(DungeonChest(0x209))  # stone slab chest can be reached by dropping down a hole
        three_of_a_kind_north = Location(dungeon=7).add(DungeonChest(0x211)).connect(topright_pillar_area, OR(AND(r.hit_switch, r.attack_hookshot_no_bomb), AND(OR(BOMB, FEATHER), SHIELD)))  # compass chest; either hit the switch, or have feather to fall on top of raised blocks. No bracelet because ball does not reset
        bottomleftF2_area = Location(dungeon=7).connect(topright_pillar_area, r.hit_switch)  # area with hinox, be able to hit a switch to reach that area
        topleftF1_chest = Location(dungeon=7).add(DungeonChest(0x201)) # top left chest on F1
        bottomleftF2_area.connect(topleftF1_chest, None, one_way = True)  # drop down in left most holes of hinox room or tile room
        Location(dungeon=7).add(DroppedKey(0x21B)).connect(bottomleftF2_area, r.attack_hookshot) # hinox drop key
        # Most of the dungeon can be accessed at this point.
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            bottomleft_owl = Location(dungeon=7).add(OwlStatue(0x21C)).connect(bottomleftF2_area, AND(BOMB, STONE_BEAK7))
        nightmare_key = Location(dungeon=7).add(DungeonChest(0x224)).connect(bottomleftF2_area, r.miniboss_requirements[world_setup.miniboss_mapping[6]]) # nightmare key after the miniboss
        mirror_shield_chest = Location(dungeon=7).add(DungeonChest(0x21A)).connect(bottomleftF2_area, r.hit_switch)  # mirror shield chest, need to be able to hit a switch to reach or
        bottomleftF2_area.connect(mirror_shield_chest, AND(KEY7, FOUND(KEY7, 3)), one_way = True) # reach mirror shield chest from hinox area by opening keyblock
        toprightF1_chest = Location(dungeon=7).add(DungeonChest(0x204)).connect(bottomleftF2_area, r.hit_switch)  # chest on the F1 right ledge. Added attack_hookshot since switch needs to be hit to get back up
        final_pillar_area = Location(dungeon=7).add(DungeonChest(0x21C)).connect(bottomleftF2_area, AND(BOMB, HOOKSHOT))  # chest that needs to spawn to get to the last pillar
        final_pillar = Location(dungeon=7).connect(final_pillar_area, POWER_BRACELET) # decouple chest from pillar

        beamos_horseheads_area = Location(dungeon=7).connect(final_pillar, NIGHTMARE_KEY7) # area behind boss door
        beamos_horseheads = Location(dungeon=7).add(DungeonChest(0x220)).connect(beamos_horseheads_area, POWER_BRACELET) # 100 rupee chest / medicine chest (DX) behind boss door
        pre_boss = Location(dungeon=7).connect(beamos_horseheads_area, HOOKSHOT) # raised plateau before boss staircase
        boss = Location(dungeon=7).add(HeartContainer(0x223), Instrument(0x22c)).connect(pre_boss, r.boss_requirements[world_setup.boss_mapping[6]])

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            three_of_a_kind_north.connect(topright_pillar_area, BOMB) # use timed bombs to match the 3 of a kinds (south 3 of a kind room is implicite as normal logic can not reach chest without hookshot)
            
        if options.logic == 'glitched' or options.logic == 'hell':
            topright_pillar_area.connect(entrance, r.super_jump_sword) # superjump in the center to get on raised blocks, superjump in switch room to right side to walk down. center superjump has to be low so sword added
            toprightF1_chest.connect(topright_pillar_area, r.super_jump_feather) # superjump from F1 switch room
            topleftF2_area = Location(dungeon=7).connect(topright_pillar_area, r.super_jump_feather) # superjump in top left pillar room over the blocks from right to left, to reach tile room
            topleftF2_area.connect(topleftF1_chest, None, one_way = True) # fall down tile room holes on left side to reach top left chest on ground floor
            topleftF1_chest.connect(bottomleftF2_area, r.boots_jump, one_way = True) # without hitting the switch, jump on raised blocks at f1 pegs chest (0x209), and boots jump to stairs to reach hinox area
            final_pillar_area.connect(bottomleftF2_area, AND(r.sideways_block_push, OR(r.attack_hookshot, POWER_BRACELET, AND(FEATHER, SHIELD)))) # sideways block push to get to the chest and pillar, kill requirement for 3 of a kind enemies to access chest. Assumes you do not get ball stuck on raised pegs for bracelet path
            if options.owlstatues == "both" or options.owlstatues == "dungeon":
                bottomleft_owl.connect(bottomleftF2_area, AND(r.sideways_block_push, STONE_BEAK7)) # sideways block push to get to the owl statue
            final_pillar.connect(bottomleftF2_area, BOMB) # bomb trigger pillar
            pre_boss.connect(final_pillar, r.super_jump_feather) # superjump on top of goomba to extend superjump to boss door plateau
            pre_boss.connect(beamos_horseheads_area, None, one_way=True) # can drop down from raised plateau to beamos horseheads area
            
        if options.logic == 'hell':
            topright_pillar_area.connect(entrance, r.super_jump_feather) # superjump in the center to get on raised blocks, has to be low
            topright_pillar_area.connect(entrance, r.boots_superhop) # boots superhop in the center to get on raised blocks
            toprightF1_chest.connect(topright_pillar_area, r.boots_superhop) # boots superhop from F1 switch room
            pre_boss.connect(final_pillar, r.boots_superhop) # boots superhop on top of goomba to extend superhop to boss door plateau
        
        self.entrance = entrance


class NoDungeon7:
    def __init__(self, options, world_setup, r):
        entrance = Location(dungeon=7)
        boss = Location(dungeon=7).add(HeartContainer(0x223), Instrument(0x22c)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[6]])

        self.entrance = entrance
