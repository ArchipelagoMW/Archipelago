from .requirements import *
from .location import Location
from ..locations.all import *


class Dungeon6:
    def __init__(self, options, world_setup, r, *, raft_game_chest=True):
        entrance = Location(dungeon=6)
        Location(dungeon=6).add(DungeonChest(0x1CF)).connect(entrance, OR(BOMB, BOW, MAGIC_ROD, COUNT(POWER_BRACELET, 2))) # 50 rupees
        Location(dungeon=6).add(DungeonChest(0x1C9)).connect(entrance, COUNT(POWER_BRACELET, 2)) # 100 rupees start
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=6).add(OwlStatue(0x1BB)).connect(entrance, STONE_BEAK6)

        # Power bracelet chest
        bracelet_chest = Location(dungeon=6).add(DungeonChest(0x1CE)).connect(entrance, AND(BOMB, FEATHER))

        # left side
        Location(dungeon=6).add(DungeonChest(0x1C0)).connect(entrance, AND(POWER_BRACELET, OR(BOMB, BOW, MAGIC_ROD))) # 3 wizrobes raised blocks dont need to hit the switch
        left_side = Location(dungeon=6).add(DungeonChest(0x1B9)).add(DungeonChest(0x1B3)).connect(entrance, AND(POWER_BRACELET, OR(BOMB, BOOMERANG)))
        Location(dungeon=6).add(DroppedKey(0x1B4)).connect(left_side, OR(BOMB, BOW, MAGIC_ROD)) # 2 wizrobe drop key
        top_left = Location(dungeon=6).add(DungeonChest(0x1B0)).connect(left_side, COUNT(POWER_BRACELET, 2)) # top left chest horseheads
        if raft_game_chest:
            Location().add(Chest(0x06C)).connect(top_left, POWER_BRACELET)  # seashell chest in raft game

        # right side
        to_miniboss = Location(dungeon=6).connect(entrance, KEY6)
        miniboss = Location(dungeon=6).connect(to_miniboss, AND(BOMB, r.miniboss_requirements[world_setup.miniboss_mapping[5]]))
        lower_right_side = Location(dungeon=6).add(DungeonChest(0x1BE)).connect(entrance, AND(OR(BOMB, BOW, MAGIC_ROD), COUNT(POWER_BRACELET, 2))) # waterway key
        medicine_chest = Location(dungeon=6).add(DungeonChest(0x1D1)).connect(lower_right_side, FEATHER) # ledge chest medicine
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            lower_right_owl = Location(dungeon=6).add(OwlStatue(0x1D7)).connect(lower_right_side, AND(POWER_BRACELET, STONE_BEAK6))

        center_1 = Location(dungeon=6).add(DroppedKey(0x1C3)).connect(miniboss, AND(COUNT(POWER_BRACELET, 2), FEATHER)) # tile room key drop
        center_2_and_upper_right_side = Location(dungeon=6).add(DungeonChest(0x1B1)).connect(center_1, AND(KEY6, FOUND(KEY6, 2))) # top right chest horseheads
        boss_key = Location(dungeon=6).add(DungeonChest(0x1B6)).connect(center_2_and_upper_right_side, AND(AND(KEY6, FOUND(KEY6, 3), HOOKSHOT)))
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=6).add(OwlStatue(0x1B6)).connect(boss_key, STONE_BEAK6)

        boss = Location(dungeon=6).add(HeartContainer(0x1BC), Instrument(0x1b5)).connect(center_1, AND(NIGHTMARE_KEY6, r.boss_requirements[world_setup.boss_mapping[5]]))

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            bracelet_chest.connect(entrance, BOMB) # get through 2d section by "fake" jumping to the ladders
            center_1.connect(miniboss, AND(COUNT(POWER_BRACELET, 2), PEGASUS_BOOTS)) # use a boots dash to get over the platforms
            
        if options.logic == 'glitched' or options.logic == 'hell':
            entrance.connect(left_side, AND(POWER_BRACELET, FEATHER), one_way=True) # path from entrance to left_side: use superjumps to pass raised blocks
            lower_right_side.connect(center_2_and_upper_right_side, AND(FEATHER, OR(SWORD, BOW, MAGIC_ROD)), one_way=True) # path from lower_right_side to center_2:  superjump from waterway towards dodongos. superjump next to corner block, so weapons added
            center_2_and_upper_right_side.connect(center_1, AND(POWER_BRACELET, FEATHER), one_way=True) # going backwards from dodongos, use a shaq jump to pass by keyblock at tile room
            boss_key.connect(lower_right_side, FEATHER) # superjump from waterway to the left. POWER_BRACELET is implied from lower_right_side

        if options.logic == 'hell':
            entrance.connect(left_side, AND(POWER_BRACELET, PEGASUS_BOOTS, OR(BOW, MAGIC_ROD)), one_way=True) # can boots superhop off the top right corner in 3 wizrobe raised blocks room
            medicine_chest.connect(lower_right_side, AND(PEGASUS_BOOTS, OR(MAGIC_ROD, BOW))) # can boots superhop off the top wall with bow or magic rod
            center_1.connect(miniboss, AND(COUNT(POWER_BRACELET, 2))) # use a double damage boost from the sparks to get across (first one is free, second one needs to buffer while in midair for spark to get close enough)
            lower_right_side.connect(center_2_and_upper_right_side, FEATHER, one_way=True) # path from lower_right_side to center_2:  superjump from waterway towards dodongos. superjump next to corner block is super tight to get enough horizontal distance
            
        self.entrance = entrance


class NoDungeon6:
    def __init__(self, options, world_setup, r):
        entrance = Location(dungeon=6)
        Location(dungeon=6).add(HeartContainer(0x1BC), Instrument(0x1b5)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[5]])
        self.entrance = entrance
