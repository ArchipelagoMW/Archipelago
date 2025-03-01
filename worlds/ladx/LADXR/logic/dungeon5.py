from .requirements import *
from .location import Location
from ..locations.all import *


class Dungeon5:
    def __init__(self, options, world_setup, r):
        entrance = Location(dungeon=5)
        start_hookshot_chest = Location(dungeon=5).add(DungeonChest(0x1A0)).connect(entrance, HOOKSHOT)
        compass = Location(dungeon=5).add(DungeonChest(0x19E)).connect(entrance, r.attack_hookshot_powder)
        fourth_stalfos_area = Location(dungeon=5).add(DroppedKey(0x181)).connect(compass, AND(SWORD, FEATHER)) # crystal rocks can only be broken by sword

        area2 = Location(dungeon=5).connect(entrance, KEY5)
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=5).add(OwlStatue(0x19A)).connect(area2, STONE_BEAK5)
        Location(dungeon=5).add(DungeonChest(0x19B)).connect(area2, r.attack_hookshot_powder)  # map chest
        blade_trap_chest = Location(dungeon=5).add(DungeonChest(0x197)).connect(area2, HOOKSHOT)  # key chest on the left
        post_gohma = Location(dungeon=5).connect(area2, AND(HOOKSHOT, r.miniboss_requirements[world_setup.miniboss_mapping[4]], KEY5, FOUND(KEY5,2))) # staircase after gohma
        staircase_before_boss = Location(dungeon=5).connect(post_gohma, AND(HOOKSHOT, FEATHER)) # bottom right section pits room before boss door. Path via gohma
        after_keyblock_boss = Location(dungeon=5).connect(staircase_before_boss, AND(KEY5, FOUND(KEY5, 3))) # top right section pits room before boss door
        after_stalfos = Location(dungeon=5).add(DungeonChest(0x196)).connect(area2, AND(SWORD, BOMB)) # Need to defeat master stalfos once for this empty chest; l2 sword beams kill but obscure
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            butterfly_owl = Location(dungeon=5).add(OwlStatue(0x18A)).connect(after_stalfos, AND(FEATHER, STONE_BEAK5))
        else:
            butterfly_owl = None
        after_stalfos.connect(staircase_before_boss, AND(FEATHER, r.attack_hookshot_powder), one_way=True) # pathway from stalfos to staircase: past butterfly room and push the block
        north_of_crossroads = Location(dungeon=5).connect(after_stalfos, FEATHER)
        first_bridge_chest = Location(dungeon=5).add(DungeonChest(0x18E)).connect(north_of_crossroads, OR(HOOKSHOT, AND(FEATHER, PEGASUS_BOOTS))) # south of bridge
        north_bridge_chest = Location(dungeon=5).add(DungeonChest(0x188)).connect(north_of_crossroads, HOOKSHOT) # north bridge chest 50 rupees
        east_bridge_chest = Location(dungeon=5).add(DungeonChest(0x18F)).connect(north_of_crossroads, HOOKSHOT) # east bridge chest small key
        third_arena = Location(dungeon=5).connect(north_of_crossroads, AND(SWORD, BOMB)) # can beat 3rd m.stalfos
        stone_tablet = Location(dungeon=5).add(DungeonChest(0x183)).connect(north_of_crossroads, AND(POWER_BRACELET, r.attack_skeleton))  # stone tablet
        boss_key = Location(dungeon=5).add(DungeonChest(0x186)).connect(after_stalfos, AND(FLIPPERS, HOOKSHOT))  # nightmare key
        before_boss = Location(dungeon=5).connect(after_keyblock_boss, HOOKSHOT) 
        boss = Location(dungeon=5).add(HeartContainer(0x185), Instrument(0x182)).connect(before_boss, AND(r.boss_requirements[world_setup.boss_mapping[4]], NIGHTMARE_KEY5))

        # When we can reach the stone tablet chest, we can also reach the final location of master stalfos
        m_stalfos_drop = Location(dungeon=5).add(HookshotDrop()).connect(third_arena, AND(FEATHER, SWORD, BOMB)) # can reach fourth arena from entrance with feather and sword

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            blade_trap_chest.connect(area2, AND(FEATHER, r.attack_hookshot_powder)) # jump past the blade traps
            boss_key.connect(after_stalfos, AND(FLIPPERS, r.boots_jump)) # boots jump across
            after_stalfos.connect(after_keyblock_boss, AND(FEATHER, r.attack_hookshot_powder)) # circumvent stalfos by going past gohma and backwards from boss door
            if butterfly_owl:
                butterfly_owl.connect(after_stalfos, AND(r.boots_bonk, STONE_BEAK5)) # boots charge + bonk to cross 2d bridge
            after_stalfos.connect(staircase_before_boss, AND(r.boots_bonk, r.attack_hookshot_powder), one_way=True) # pathway from stalfos to staircase: boots charge + bonk to cross bridge, past butterfly room and push the block
            staircase_before_boss.connect(post_gohma, AND(r.boots_bonk, HOOKSHOT)) # boots bonk in 2d section to skip feather
            north_of_crossroads.connect(after_stalfos, r.hookshot_over_pit) # hookshot to the right block to cross pits
            first_bridge_chest.connect(north_of_crossroads, AND(r.wall_clip, r.tight_jump)) # tight jump from bottom wall clipped to make it over the pits
            after_keyblock_boss.connect(after_stalfos, AND(FEATHER, r.attack_hookshot_powder)) # jump from bottom left to top right, skipping the keyblock 
            before_boss.connect(after_stalfos, AND(r.boots_jump, r.attack_hookshot_powder)) # cross pits room from bottom left to top left with boots jump
            
        if options.logic == 'glitched' or options.logic == 'hell':
            start_hookshot_chest.connect(entrance, r.pit_buffer) # 1 pit buffer to clip bottom wall and jump across the pits
            post_gohma.connect(area2, HOOKSHOT) # glitch through the blocks/pots with hookshot. Zoomerang can be used but has no logical implications because of 2d section requiring hookshot
            north_bridge_chest.connect(north_of_crossroads, r.pit_buffer) # 1 pit buffer to clip bottom wall and jump across the pits
            east_bridge_chest.connect(first_bridge_chest, r.pit_buffer) # 1 pit buffer to clip bottom wall and jump across the pits
            #after_stalfos.connect(staircase_before_boss, AND(r.text_clip, r.super_jump)) # use the keyblock to get a wall clip in right wall to perform a superjump over the pushable block
            after_stalfos.connect(staircase_before_boss, r.super_jump_boots) # charge a boots dash in bottom right corner to the right, jump before hitting the wall and use weapon to the left side before hitting the wall
         
        if  options.logic == 'hell':
            start_hookshot_chest.connect(entrance, r.pit_buffer_boots) # use pit buffer to clip into the bottom wall and boots bonk off the wall again
            fourth_stalfos_area.connect(compass, AND(r.boots_bonk_2d_hell, SWORD)) # do an incredibly hard boots bonk setup to get across the hanging platforms in the 2d section
            blade_trap_chest.connect(area2, AND(r.pit_buffer_boots, r.attack_hookshot_powder)) # boots bonk + pit buffer past the blade traps
            post_gohma.connect(area2, AND(PEGASUS_BOOTS, FEATHER, POWER_BRACELET, r.attack_hookshot_powder)) # use boots jump in room with 2 zols + flying arrows to pit buffer above pot, then jump across. Sideways block push + pick up pots to reach post_gohma
            staircase_before_boss.connect(post_gohma, r.boots_jump) # to pass 2d section, tight jump on left screen: hug left wall on little platform, then dash right off platform and jump while in midair to bonk against right wall
            after_stalfos.connect(staircase_before_boss, r.super_jump_sword) # unclipped superjump in bottom right corner of staircase before boss room, jumping left over the pushable block. reverse is push block
            after_stalfos.connect(area2, SWORD) # knock master stalfos down 255 times (about 23 minutes)
            after_stalfos.connect(staircase_before_boss, r.zoomerang) # use zoomerang dashing left to get an unclipped boots superjump off the right wall over the block. reverse is push block
            north_bridge_chest.connect(north_of_crossroads, r.boots_bonk_pit) # boots bonk across the pits with pit buffering
            first_bridge_chest.connect(north_of_crossroads, r.boots_bonk_pit) # get to first chest via the north chest with pit buffering
            east_bridge_chest.connect(first_bridge_chest, r.boots_bonk_pit) # boots bonk across the pits with pit buffering
            third_arena.connect(north_of_crossroads, SWORD) # can beat 3rd m.stalfos with 255 sword spins
            m_stalfos_drop.connect(third_arena, AND(FEATHER, SWORD)) # beat master stalfos by knocking it down 255 times x 4 (takes about 1.5h total)
            m_stalfos_drop.connect(third_arena, AND(r.boots_bonk_2d_hell, SWORD)) # can reach fourth arena from entrance with pegasus boots and sword
            boss_key.connect(after_stalfos, AND(r.pit_buffer_itemless, FLIPPERS)) # pit buffer across
            if butterfly_owl:
                after_keyblock_boss.connect(butterfly_owl, AND(r.pit_buffer_itemless, STONE_BEAK5), one_way=True) # pit buffer from top right to bottom in right pits room
            before_boss.connect(after_stalfos, r.super_jump_sword) # cross pits room from bottom left to top left by unclipped superjump on bottom wall on top of side wall, then jump across            

        self.entrance = entrance


class NoDungeon5:
    def __init__(self, options, world_setup, r):
        entrance = Location(dungeon=5)
        Location(dungeon=5).add(HeartContainer(0x185), Instrument(0x182)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[4]])

        self.entrance = entrance
