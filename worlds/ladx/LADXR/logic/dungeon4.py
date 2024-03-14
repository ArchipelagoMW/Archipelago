from .requirements import *
from .location import Location
from ..locations.all import *


class Dungeon4:
    def __init__(self, options, world_setup, r):
        entrance = Location(dungeon=4)
        entrance.add(DungeonChest(0x179))  # stone slab chest
        entrance.add(DungeonChest(0x16A))  # map chest
        right_of_entrance = Location(dungeon=4).add(DungeonChest(0x178)).connect(entrance, AND(SHIELD, r.attack_hookshot_powder)) # 1 zol 2 spike beetles 1 spark chest
        Location(dungeon=4).add(DungeonChest(0x17B)).connect(right_of_entrance, AND(SHIELD, SWORD)) # room with key chest
        rightside_crossroads = Location(dungeon=4).connect(entrance, AND(FEATHER, PEGASUS_BOOTS))  # 2 key chests on the right.
        pushable_block_chest = Location(dungeon=4).add(DungeonChest(0x171)).connect(rightside_crossroads, BOMB) # lower chest
        puddle_crack_block_chest = Location(dungeon=4).add(DungeonChest(0x165)).connect(rightside_crossroads, OR(BOMB, FLIPPERS)) # top right chest
        
        double_locked_room = Location(dungeon=4).connect(right_of_entrance, AND(KEY4, FOUND(KEY4, 5)), one_way=True)
        right_of_entrance.connect(double_locked_room, KEY4, one_way=True)
        after_double_lock = Location(dungeon=4).connect(double_locked_room, AND(KEY4, FOUND(KEY4, 4), OR(FEATHER, FLIPPERS)), one_way=True)
        double_locked_room.connect(after_double_lock, AND(KEY4, FOUND(KEY4, 2), OR(FEATHER, FLIPPERS)), one_way=True)
        
        dungeon4_puddle_before_crossroads = Location(dungeon=4).add(DungeonChest(0x175)).connect(after_double_lock, FLIPPERS)
        north_crossroads = Location(dungeon=4).connect(after_double_lock, AND(FEATHER, PEGASUS_BOOTS))
        before_miniboss = Location(dungeon=4).connect(north_crossroads, AND(KEY4, FOUND(KEY4, 3)))
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=4).add(OwlStatue(0x16F)).connect(before_miniboss, STONE_BEAK4)
        sidescroller_key = Location(dungeon=4).add(DroppedKey(0x169)).connect(before_miniboss, AND(r.attack_hookshot_powder, FLIPPERS))  # key that drops in the hole and needs swim to get
        center_puddle_chest = Location(dungeon=4).add(DungeonChest(0x16E)).connect(before_miniboss, FLIPPERS)  # chest with 50 rupees
        left_water_area = Location(dungeon=4).connect(before_miniboss, OR(FEATHER, FLIPPERS)) # area left with zol chest and 5 symbol puzzle (water area)
        left_water_area.add(DungeonChest(0x16D))  # gel chest
        left_water_area.add(DungeonChest(0x168))  # key chest near the puzzle
        miniboss = Location(dungeon=4).connect(before_miniboss, AND(KEY4, FOUND(KEY4, 5), r.miniboss_requirements[world_setup.miniboss_mapping[3]])) 
        terrace_zols_chest = Location(dungeon=4).connect(before_miniboss, FLIPPERS) # flippers to move around miniboss through 5 tile room
        miniboss = Location(dungeon=4).connect(terrace_zols_chest, POWER_BRACELET, one_way=True) # reach flippers chest through the miniboss room
        terrace_zols_chest.add(DungeonChest(0x160))  # flippers chest
        terrace_zols_chest.connect(left_water_area, r.attack_hookshot_powder, one_way=True) # can move from flippers chest south to push the block to left area
        
        to_the_nightmare_key = Location(dungeon=4).connect(left_water_area, AND(FEATHER, OR(FLIPPERS, PEGASUS_BOOTS)))  # 5 symbol puzzle (does not need flippers with boots + feather)
        to_the_nightmare_key.add(DungeonChest(0x176))

        before_boss = Location(dungeon=4).connect(before_miniboss, AND(r.attack_hookshot, FLIPPERS, KEY4, FOUND(KEY4, 5)))
        boss = Location(dungeon=4).add(HeartContainer(0x166), Instrument(0x162)).connect(before_boss, AND(NIGHTMARE_KEY4, r.boss_requirements[world_setup.boss_mapping[3]]))

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            sidescroller_key.connect(before_miniboss, AND(FEATHER, BOOMERANG)) # grab the key jumping over the water and boomerang downwards
            sidescroller_key.connect(before_miniboss, AND(POWER_BRACELET, FLIPPERS)) # kill the zols with the pots in the room to spawn the key
            rightside_crossroads.connect(entrance, FEATHER) # jump across the corners
            puddle_crack_block_chest.connect(rightside_crossroads, FEATHER) # jump around the bombable block
            north_crossroads.connect(entrance, FEATHER) # jump across the corners
            after_double_lock.connect(entrance, FEATHER) # jump across the corners
            dungeon4_puddle_before_crossroads.connect(after_double_lock, FEATHER) # With a tight jump feather is enough to cross the puddle without flippers
            center_puddle_chest.connect(before_miniboss, FEATHER) # With a tight jump feather is enough to cross the puddle without flippers
            miniboss = Location(dungeon=4).connect(terrace_zols_chest, None, one_way=True) # reach flippers chest through the miniboss room without pulling the lever
            to_the_nightmare_key.connect(left_water_area, FEATHER) # With a tight jump feather is enough to reach the top left switch without flippers, or use flippers for puzzle and boots to get through 2d section
            before_boss.connect(left_water_area, FEATHER) # jump to the bottom right corner of boss door room
            
        if options.logic == 'glitched' or options.logic == 'hell':    
            pushable_block_chest.connect(rightside_crossroads, FLIPPERS) # sideways block push to skip bombs
            sidescroller_key.connect(before_miniboss, AND(FEATHER, OR(r.attack_hookshot_powder, POWER_BRACELET))) # superjump into the hole to grab the key while falling into the water
            miniboss.connect(before_miniboss, FEATHER) # use jesus jump to transition over the water left of miniboss
        
        if options.logic == 'hell':
            rightside_crossroads.connect(entrance, AND(PEGASUS_BOOTS, HOOKSHOT)) # pit buffer into the wall of the first pit, then boots bonk across the center, hookshot to get to the rightmost pit to a second villa buffer on the rightmost pit
            pushable_block_chest.connect(rightside_crossroads, OR(PEGASUS_BOOTS, FEATHER)) # use feather to water clip into the top right corner of the bombable block, and sideways block push to gain access. Can boots bonk of top right wall, then water buffer to top of chest and boots bonk to water buffer next to chest
            after_double_lock.connect(double_locked_room, AND(FOUND(KEY4, 4), PEGASUS_BOOTS), one_way=True) # use boots bonks to cross the water gaps
            north_crossroads.connect(entrance, AND(PEGASUS_BOOTS, HOOKSHOT)) # pit buffer into wall of the first pit, then boots bonk towards the top and hookshot spam to get across (easier with Piece of Power)
            after_double_lock.connect(entrance, PEGASUS_BOOTS) # boots bonk + pit buffer to the bottom
            dungeon4_puddle_before_crossroads.connect(after_double_lock, AND(PEGASUS_BOOTS, HOOKSHOT)) # boots bonk across the water bottom wall to the bottom left corner, then hookshot up
            to_the_nightmare_key.connect(left_water_area, AND(FLIPPERS, PEGASUS_BOOTS)) #  Use flippers for puzzle and boots bonk to get through 2d section
            before_boss.connect(left_water_area, PEGASUS_BOOTS) # boots bonk across bottom wall then boots bonk to the platform before boss door
            
        self.entrance = entrance


class NoDungeon4:
    def __init__(self, options, world_setup, r):
        entrance = Location(dungeon=4)
        Location(dungeon=4).add(HeartContainer(0x166), Instrument(0x162)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[3]])

        self.entrance = entrance
