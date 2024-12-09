from .requirements import *
from .location import Location
from ..locations.all import *


class Dungeon8:
    def __init__(self, options, world_setup, r, *, back_entrance_heartpiece=True):
        entrance = Location(dungeon=8)
        entrance_up = Location(dungeon=8).connect(entrance, FEATHER)
        entrance_left = Location(dungeon=8).connect(entrance, r.attack_hookshot_no_bomb) # past hinox

        # left side
        entrance_left.add(DungeonChest(0x24D)) # zamboni room chest
        eye_magnet_chest = Location(dungeon=8).add(DungeonChest(0x25C)) # eye magnet chest bottom left below rolling bones
        eye_magnet_chest.connect(entrance_left, OR(BOW, MAGIC_ROD, BOOMERANG, AND(FEATHER, r.attack_hookshot))) # damageless roller should be default        
        if options.hardmode != "ohko":
            eye_magnet_chest.connect(entrance_left, r.attack_hookshot) # can take a hit
        vire_drop_key = Location(dungeon=8).add(DroppedKey(0x24C)).connect(entrance_left, r.attack_hookshot_no_bomb) # vire drop key
        sparks_chest = Location(dungeon=8).add(DungeonChest(0x255)).connect(entrance_left, OR(HOOKSHOT, FEATHER))  # chest before lvl1 miniboss
        Location(dungeon=8).add(DungeonChest(0x246)).connect(entrance_left, MAGIC_ROD)  # key chest that spawns after creating fire
        
        # right side
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            bottomright_owl = Location(dungeon=8).add(OwlStatue(0x253)).connect(entrance, AND(STONE_BEAK8, FEATHER, POWER_BRACELET)) # Two ways to reach this owl statue, but both require the same (except that one route requires bombs as well)
        else:
            bottomright_owl = None
        slime_chest = Location(dungeon=8).add(DungeonChest(0x259)).connect(entrance, OR(FEATHER, AND(r.attack_hookshot, POWER_BRACELET)))  # chest with slime
        bottom_right = Location(dungeon=8).add(DroppedKey(0x25A)).connect(entrance, AND(FEATHER, OR(BOMB, AND(r.attack_hookshot_powder, POWER_BRACELET)))) # zamboni key drop; bombs for entrance up through switch room, weapon + bracelet for NW zamboni staircase to bottom right past smasher
        bottomright_pot_chest = Location(dungeon=8).add(DungeonChest(0x25F)).connect(bottom_right, POWER_BRACELET) # 4 ropes pot room chest

        map_chest = Location(dungeon=8).add(DungeonChest(0x24F)).connect(entrance_up, None) # use the zamboni to get to the push blocks
        lower_center = Location(dungeon=8).connect(entrance_up, KEY8)
        upper_center = Location(dungeon=8).connect(lower_center, AND(KEY8, FOUND(KEY8, 2)))
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=8).add(OwlStatue(0x245)).connect(upper_center, STONE_BEAK8)
        gibdos_drop_key = Location(dungeon=8).add(DroppedKey(0x23E)).connect(upper_center, r.attack_gibdos) # 2 gibdos cracked floor; technically possible to use pits to kill but dumb
        medicine_chest = Location(dungeon=8).add(DungeonChest(0x235)).connect(upper_center, AND(FEATHER, HOOKSHOT))  # medicine chest

        middle_center_1 = Location(dungeon=8).connect(upper_center, BOMB)
        middle_center_2 = Location(dungeon=8).connect(middle_center_1, AND(KEY8, FOUND(KEY8, 4)))
        middle_center_3 = Location(dungeon=8).connect(middle_center_2, KEY8)
        miniboss_entrance = Location(dungeon=8).connect(middle_center_3, AND(HOOKSHOT, KEY8, FOUND(KEY8, 7))) # hookshot to get across to keyblock, 7 to fix keylock issues if keys are used on other keyblocks
        miniboss = Location(dungeon=8).connect(miniboss_entrance, AND(FEATHER, r.miniboss_requirements[world_setup.miniboss_mapping[7]]))  # feather for 2d section, sword to kill
        miniboss.add(DungeonChest(0x237)) # fire rod chest

        up_left = Location(dungeon=8).connect(upper_center, AND(r.attack_hookshot_powder, AND(KEY8, FOUND(KEY8, 4))))
        entrance_up.connect(up_left, AND(FEATHER, MAGIC_ROD), one_way=True) # alternate path with fire rod through 2d section to nightmare key
        up_left.add(DungeonChest(0x240)) # beamos blocked chest
        up_left.connect(entrance_left, None, one_way=True) # path from up_left to entrance_left by dropping of the ledge in torch room 
        Location(dungeon=8).add(DungeonChest(0x23D)).connect(up_left, BOMB) # dodongo chest
        up_left.connect(upper_center, None, one_way=True) # use the outside path of the dungeon to get to the right side
        if back_entrance_heartpiece:
            Location().add(HeartPiece(0x000)).connect(up_left, None)  # Outside the dungeon on the platform
        Location(dungeon=8).add(DroppedKey(0x241)).connect(up_left, BOW) # lava statue
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=8).add(OwlStatue(0x241)).connect(up_left, STONE_BEAK8)
        Location(dungeon=8).add(DungeonChest(0x23A)).connect(up_left, HOOKSHOT) # ledge chest left of boss door

        top_left_stairs = Location(dungeon=8).connect(entrance_up, AND(FEATHER, MAGIC_ROD)) 
        top_left_stairs.connect(up_left, None, one_way=True) # jump down from the staircase to the right
        nightmare_key = Location(dungeon=8).add(DungeonChest(0x232)).connect(top_left_stairs, AND(FEATHER, SWORD, KEY8, FOUND(KEY8, 7)))

        # Bombing from the center dark rooms to the left so you can access more keys.
        # The south walls of center dark room can be bombed from lower_center too with bomb and feather for center dark room access from the south, allowing even more access. Not sure if this should be logic since "obscure"
        middle_center_2.connect(up_left, AND(BOMB, FEATHER), one_way=True) # does this even skip a key? both middle_center_2 and up_left come from upper_center with 1 extra key

        bossdoor = Location(dungeon=8).connect(entrance_up, AND(FEATHER, MAGIC_ROD))
        boss = Location(dungeon=8).add(HeartContainer(0x234), Instrument(0x230)).connect(bossdoor, AND(NIGHTMARE_KEY8, r.boss_requirements[world_setup.boss_mapping[7]]))
        
        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            entrance_left.connect(entrance, BOMB) # use bombs to kill vire and hinox
            up_left.connect(vire_drop_key, BOMB, one_way=True) # use bombs to kill rolling bones and vire, do not allow pathway through hinox with just bombs, as not enough bombs are available
            bottom_right.connect(slime_chest, r.tight_jump) # diagonal jump over the pits to reach rolling rock / zamboni
            gibdos_drop_key.connect(upper_center, OR(HOOKSHOT, MAGIC_ROD)) # crack one of the floor tiles and hookshot the gibdos in, or burn the gibdos and make them jump into pit
            up_left.connect(lower_center, AND(BOMB, FEATHER)) # blow up hidden walls from peahat room -> dark room -> eye statue room
            slime_chest.connect(entrance, AND(r.attack_hookshot_powder, POWER_BRACELET))  # kill vire with powder or bombs 
        
        if options.logic == 'glitched' or options.logic == 'hell':
            sparks_chest.connect(entrance_left, r.pit_buffer_itemless) # 1 pit buffer across the pit. 
            entrance_up.connect(bottomright_pot_chest, r.super_jump_boots, one_way = True) # underground section with fire balls jumping up out of lava. Use boots superjump off left wall to jump over the pot blocking the way
            lower_center.connect(entrance_up, r.sideways_block_push) # sideways block push in peahat room to get past keyblock
            miniboss_entrance.connect(lower_center, AND(BOMB, r.bookshot)) # blow up hidden wall for darkroom, use feather + hookshot to clip past keyblock in front of stairs
            miniboss_entrance.connect(lower_center, AND(BOMB, r.super_jump_feather, FOUND(KEY8, 7))) # same as above, but without clipping past the keyblock
            up_left.connect(lower_center, r.jesus_jump) # use jesus jump in refill room left of peahats to clip bottom wall and push bottom block left, to get a place to super jump
            up_left.connect(upper_center, r.jesus_jump) # from up left you can jesus jump / lava swim around the key door next to the boss.
            top_left_stairs.connect(up_left, r.super_jump_feather) # superjump
            medicine_chest.connect(upper_center, AND(r.super_jump_feather, r.jesus_jump)) # jesus super jump
            up_left.connect(bossdoor, r.super_jump_feather, one_way=True) # superjump off the bottom or right wall to jump over to the boss door

        if options.logic == 'hell':
            if bottomright_owl:
                bottomright_owl.connect(entrance, AND(SWORD, POWER_BRACELET, r.boots_bonk_2d_hell, STONE_BEAK8)) # underground section past mimics, boots bonking across the gap to the ladder
            bottomright_pot_chest.connect(entrance, AND(SWORD, POWER_BRACELET, r.boots_bonk_2d_hell)) # underground section past mimics, boots bonking across the gap to the ladder
            entrance.connect(bottomright_pot_chest, r.shaq_jump, one_way=True) # use NW zamboni staircase backwards, and get a naked shaq jump off the bottom wall in the bottom right corner to pass by the pot
            gibdos_drop_key.connect(upper_center, AND(FEATHER, SHIELD)) # lock gibdos into pits and crack the tile they stand on, then use shield to bump them into the pit
            medicine_chest.connect(upper_center, AND(r.pit_buffer_boots, HOOKSHOT)) # boots bonk + lava buffer to the bottom wall, then bonk onto the middle section
            miniboss.connect(miniboss_entrance, AND(r.boots_bonk_2d_hell, r.miniboss_requirements[world_setup.miniboss_mapping[7]])) # get through 2d section with boots bonks
            top_left_stairs.connect(map_chest, AND(r.jesus_buffer, r.boots_bonk_2d_hell, MAGIC_ROD)) # boots bonk + lava buffer from map chest to entrance_up, then boots bonk through 2d section
            nightmare_key.connect(top_left_stairs, AND(r.boots_bonk_pit, SWORD, FOUND(KEY8, 7))) # use a boots bonk to cross the 2d section + the lava in cueball room
            bottom_right.connect(entrance_up, AND(POWER_BRACELET, r.jesus_buffer), one_way=True) # take staircase to NW zamboni room, boots bonk onto the lava and water buffer all the way down to push the zamboni
            bossdoor.connect(entrance_up, AND(r.boots_bonk_2d_hell, MAGIC_ROD)) # boots bonk through 2d section
            
        self.entrance = entrance


class NoDungeon8:
    def __init__(self, options, world_setup, r):
        entrance = Location(dungeon=8)
        boss = Location(dungeon=8).add(HeartContainer(0x234)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[7]])
        instrument = Location(dungeon=8).add(Instrument(0x230)).connect(boss, FEATHER) # jump over the lava to get to the instrument

        self.entrance = entrance
