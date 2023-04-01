from .requirements import *
from .location import Location
from ..locations.all import *
from ..worldSetup import ENTRANCE_INFO


class World:
    def __init__(self, options, world_setup, r):
        self.overworld_entrance = {}
        self.indoor_location = {}

        mabe_village = Location("Mabe Village")
        Location().add(HeartPiece(0x2A4)).connect(mabe_village, r.bush)  # well
        Location().add(FishingMinigame()).connect(mabe_village, AND(r.bush, COUNT("RUPEES", 20)))  # fishing game, heart piece is directly done by the minigame.
        Location().add(Seashell(0x0A3)).connect(mabe_village, r.bush)  # bushes below the shop
        Location().add(Seashell(0x0D2)).connect(mabe_village, PEGASUS_BOOTS)  # smash into tree next to lv1
        Location().add(Song(0x092)).connect(mabe_village, OCARINA)  # Marins song
        rooster_cave = Location("Rooster Cave")
        Location().add(DroppedKey(0x1E4)).connect(rooster_cave, AND(OCARINA, SONG3))

        papahl_house = Location("Papahl House")
        papahl_house.connect(Location().add(TradeSequenceItem(0x2A6, TRADING_ITEM_RIBBON)), TRADING_ITEM_YOSHI_DOLL)

        trendy_shop = Location("Trendy Shop").add(TradeSequenceItem(0x2A0, TRADING_ITEM_YOSHI_DOLL))
        #trendy_shop.connect(Location())

        self._addEntrance("papahl_house_left", mabe_village, papahl_house, None)
        self._addEntrance("papahl_house_right", mabe_village, papahl_house, None)
        self._addEntrance("rooster_grave", mabe_village, rooster_cave, COUNT(POWER_BRACELET, 2))
        self._addEntranceRequirementExit("rooster_grave", None) # if exiting, you do not need l2 bracelet
        self._addEntrance("madambowwow", mabe_village, None, None)
        self._addEntrance("ulrira", mabe_village, None, None)
        self._addEntrance("mabe_phone", mabe_village, None, None)
        self._addEntrance("library", mabe_village, None, None)
        self._addEntrance("trendy_shop", mabe_village, trendy_shop, r.bush)
        self._addEntrance("d1", mabe_village, None, TAIL_KEY)
        self._addEntranceRequirementExit("d1", None) # if exiting, you do not need the key

        start_house = Location("Start House").add(StartItem())
        self._addEntrance("start_house", mabe_village, start_house, None)

        shop = Location("Shop")
        Location().add(ShopItem(0)).connect(shop, OR(COUNT("RUPEES", 500), SWORD))
        Location().add(ShopItem(1)).connect(shop, OR(COUNT("RUPEES", 1480), SWORD))
        self._addEntrance("shop", mabe_village, shop, None)

        dream_hut = Location("Dream Hut")
        dream_hut_right = Location().add(Chest(0x2BF)).connect(dream_hut, SWORD)
        if options.logic != "casual":
            dream_hut_right.connect(dream_hut, OR(BOOMERANG, HOOKSHOT, FEATHER))
        dream_hut_left = Location().add(Chest(0x2BE)).connect(dream_hut_right, PEGASUS_BOOTS)
        self._addEntrance("dream_hut", mabe_village, dream_hut, POWER_BRACELET)

        kennel = Location("Kennel").connect(Location().add(Seashell(0x2B2)), SHOVEL)  # in the kennel
        kennel.connect(Location().add(TradeSequenceItem(0x2B2, TRADING_ITEM_DOG_FOOD)), TRADING_ITEM_RIBBON)
        self._addEntrance("kennel", mabe_village, kennel, None)

        sword_beach = Location("Sword Beach").add(BeachSword()).connect(mabe_village, OR(r.bush, SHIELD, r.attack_hookshot))
        banana_seller = Location("Banana Seller")
        banana_seller.connect(Location().add(TradeSequenceItem(0x2FE, TRADING_ITEM_BANANAS)), TRADING_ITEM_DOG_FOOD)
        self._addEntrance("banana_seller", sword_beach, banana_seller, r.bush)
        boomerang_cave = Location("Boomerang Cave")
        if options.boomerang == 'trade':
            Location().add(BoomerangGuy()).connect(boomerang_cave, OR(BOOMERANG, HOOKSHOT, MAGIC_ROD, PEGASUS_BOOTS, FEATHER, SHOVEL))
        elif options.boomerang == 'gift':
            Location().add(BoomerangGuy()).connect(boomerang_cave, None)
        self._addEntrance("boomerang_cave", sword_beach, boomerang_cave, BOMB)
        self._addEntranceRequirementExit("boomerang_cave", None) # if exiting, you do not need bombs

        sword_beach_to_ghost_hut = Location("Sword Beach to Ghost House").add(Chest(0x0E5)).connect(sword_beach, POWER_BRACELET)
        ghost_hut_outside = Location("Outside Ghost House").connect(sword_beach_to_ghost_hut, POWER_BRACELET)
        ghost_hut_inside = Location("Ghost House").connect(Location().add(Seashell(0x1E3)), POWER_BRACELET)
        self._addEntrance("ghost_house", ghost_hut_outside, ghost_hut_inside, None)

        ## Forest area
        forest = Location("Forest").connect(mabe_village, r.bush) # forest stretches all the way from the start town to the witch hut
        Location().add(Chest(0x071)).connect(forest, POWER_BRACELET)  # chest at start forest with 2 zols
        forest_heartpiece = Location("Forest Heart Piece").add(HeartPiece(0x044))  # next to the forest, surrounded by pits
        forest.connect(forest_heartpiece, OR(BOOMERANG, FEATHER, HOOKSHOT, ROOSTER), one_way=True)

        witch_hut = Location().connect(Location().add(Witch()), TOADSTOOL)
        self._addEntrance("witch", forest, witch_hut, None)
        crazy_tracy_hut = Location("Outside Crazy Tracy's House").connect(forest, POWER_BRACELET)
        crazy_tracy_hut_inside = Location("Crazy Tracy's House")
        Location().add(KeyLocation("MEDICINE2")).connect(crazy_tracy_hut_inside, FOUND("RUPEES", 50))
        self._addEntrance("crazy_tracy", crazy_tracy_hut, crazy_tracy_hut_inside, None)
        start_house.connect(crazy_tracy_hut, SONG2, one_way=True) # Manbo's Mambo into the pond outside Tracy

        forest_madbatter = Location("Forest Mad Batter")
        Location().add(MadBatter(0x1E1)).connect(forest_madbatter, MAGIC_POWDER)
        self._addEntrance("forest_madbatter", forest, forest_madbatter, POWER_BRACELET)
        self._addEntranceRequirementExit("forest_madbatter", None) # if exiting, you do not need bracelet

        forest_cave = Location("Forest Cave")
        Location().add(Chest(0x2BD)).connect(forest_cave, SWORD)  # chest in forest cave on route to mushroom
        log_cave_heartpiece = Location().add(HeartPiece(0x2AB)).connect(forest_cave, POWER_BRACELET)  # piece of heart in the forest cave on route to the mushroom
        forest_toadstool = Location().add(Toadstool())
        self._addEntrance("toadstool_entrance", forest, forest_cave, None)
        self._addEntrance("toadstool_exit", forest_toadstool, forest_cave, None)

        hookshot_cave = Location("Hookshot Cave")
        hookshot_cave_chest = Location().add(Chest(0x2B3)).connect(hookshot_cave, OR(HOOKSHOT, ROOSTER))
        self._addEntrance("hookshot_cave", forest, hookshot_cave, POWER_BRACELET)

        swamp = Location("Swamp").connect(forest, AND(OR(MAGIC_POWDER, FEATHER, ROOSTER), r.bush))
        swamp.connect(forest, r.bush, one_way=True) # can go backwards past Tarin
        swamp.connect(forest_toadstool, OR(FEATHER, ROOSTER))
        swamp_chest = Location("Swamp Chest").add(Chest(0x034)).connect(swamp, OR(BOWWOW, HOOKSHOT, MAGIC_ROD, BOOMERANG))
        self._addEntrance("d2", swamp, None, OR(BOWWOW, HOOKSHOT, MAGIC_ROD, BOOMERANG))
        forest_rear_chest = Location().add(Chest(0x041)).connect(swamp, r.bush)  # tail key
        self._addEntrance("writes_phone", swamp, None, None)

        writes_hut_outside = Location("Outside Write's House").connect(swamp, OR(FEATHER, ROOSTER))  # includes the cave behind the hut
        writes_house = Location("Write's House")
        writes_house.connect(Location().add(TradeSequenceItem(0x2a8, TRADING_ITEM_BROOM)), TRADING_ITEM_LETTER)
        self._addEntrance("writes_house", writes_hut_outside, writes_house, None)
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            writes_hut_outside.add(OwlStatue(0x11))
        writes_cave = Location("Write's Cave")
        writes_cave_left_chest = Location().add(Chest(0x2AE)).connect(writes_cave, OR(FEATHER, ROOSTER, HOOKSHOT)) # 1st chest in the cave behind the hut
        Location().add(Chest(0x2AF)).connect(writes_cave, POWER_BRACELET)  # 2nd chest in the cave behind the hut.
        self._addEntrance("writes_cave_left", writes_hut_outside, writes_cave, None)
        self._addEntrance("writes_cave_right", writes_hut_outside, writes_cave, None)

        graveyard = Location("Graveyard").connect(forest, OR(FEATHER, ROOSTER, POWER_BRACELET))  # whole area from the graveyard up to the moblin cave
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            graveyard.add(OwlStatue(0x035))  # Moblin cave owl
        self._addEntrance("photo_house", graveyard, None, None)
        self._addEntrance("d0", graveyard, None, POWER_BRACELET)
        self._addEntranceRequirementExit("d0", None) # if exiting, you do not need bracelet
        ghost_grave = Location().connect(forest, POWER_BRACELET)
        Location().add(Seashell(0x074)).connect(ghost_grave, AND(r.bush, SHOVEL))  # next to grave cave, digging spot

        graveyard_cave_left = Location()
        graveyard_cave_right = Location().connect(graveyard_cave_left, OR(FEATHER, ROOSTER))
        graveyard_heartpiece = Location().add(HeartPiece(0x2DF)).connect(graveyard_cave_right, OR(AND(BOMB, OR(HOOKSHOT, PEGASUS_BOOTS), FEATHER), ROOSTER))  # grave cave
        self._addEntrance("graveyard_cave_left", ghost_grave, graveyard_cave_left, POWER_BRACELET)
        self._addEntrance("graveyard_cave_right", graveyard, graveyard_cave_right, None)
        moblin_cave = Location().connect(Location().add(Chest(0x2E2)), AND(r.attack_hookshot_powder, r.miniboss_requirements[world_setup.miniboss_mapping["moblin_cave"]]))
        self._addEntrance("moblin_cave", graveyard, moblin_cave, None)

        # "Ukuku Prairie"
        ukuku_prairie = Location().connect(mabe_village, POWER_BRACELET).connect(graveyard, POWER_BRACELET)
        ukuku_prairie.connect(Location().add(TradeSequenceItem(0x07B, TRADING_ITEM_STICK)), TRADING_ITEM_BANANAS)
        ukuku_prairie.connect(Location().add(TradeSequenceItem(0x087, TRADING_ITEM_HONEYCOMB)), TRADING_ITEM_STICK)
        self._addEntrance("prairie_left_phone", ukuku_prairie, None, None)
        self._addEntrance("prairie_right_phone", ukuku_prairie, None, None)
        self._addEntrance("prairie_left_cave1", ukuku_prairie, Location().add(Chest(0x2CD)), None) # cave next to town
        self._addEntrance("prairie_left_fairy", ukuku_prairie, None, BOMB)
        self._addEntranceRequirementExit("prairie_left_fairy", None) # if exiting, you do not need bombs

        prairie_left_cave2 = Location()  # Bomb cave
        Location().add(Chest(0x2F4)).connect(prairie_left_cave2, PEGASUS_BOOTS)
        Location().add(HeartPiece(0x2E5)).connect(prairie_left_cave2, AND(BOMB, PEGASUS_BOOTS))
        self._addEntrance("prairie_left_cave2", ukuku_prairie, prairie_left_cave2, BOMB)
        self._addEntranceRequirementExit("prairie_left_cave2", None) # if exiting, you do not need bombs

        mamu = Location().connect(Location().add(Song(0x2FB)), AND(OCARINA, COUNT("RUPEES", 1480)))
        self._addEntrance("mamu", ukuku_prairie, mamu, AND(OR(AND(FEATHER, PEGASUS_BOOTS), ROOSTER), OR(HOOKSHOT, ROOSTER), POWER_BRACELET))

        dungeon3_entrance = Location().connect(ukuku_prairie, OR(FEATHER, ROOSTER, FLIPPERS))
        self._addEntrance("d3", dungeon3_entrance, None, SLIME_KEY)
        self._addEntranceRequirementExit("d3", None) # if exiting, you do not need to open the door
        Location().add(Seashell(0x0A5)).connect(dungeon3_entrance, SHOVEL)  # above lv3
        dungeon3_entrance.connect(ukuku_prairie, None, one_way=True) # jump down ledge back to ukuku_prairie

        prairie_island_seashell = Location().add(Seashell(0x0A6)).connect(ukuku_prairie, AND(FLIPPERS, r.bush))  # next to lv3
        Location().add(Seashell(0x08B)).connect(ukuku_prairie, r.bush)  # next to seashell house
        Location().add(Seashell(0x0A4)).connect(ukuku_prairie, PEGASUS_BOOTS)  # smash into tree next to phonehouse
        self._addEntrance("castle_jump_cave", ukuku_prairie, Location().add(Chest(0x1FD)), OR(AND(FEATHER, PEGASUS_BOOTS), ROOSTER)) # left of the castle, 5 holes turned into 3
        Location().add(Seashell(0x0B9)).connect(ukuku_prairie, POWER_BRACELET)  # under the rock

        left_bay_area = Location()
        left_bay_area.connect(ghost_hut_outside, OR(AND(FEATHER, PEGASUS_BOOTS), ROOSTER))
        self._addEntrance("prairie_low_phone", left_bay_area, None, None)

        Location().add(Seashell(0x0E9)).connect(left_bay_area, r.bush)  # same screen as mermaid statue
        tiny_island = Location().add(Seashell(0x0F8)).connect(left_bay_area, AND(OR(FLIPPERS, ROOSTER), r.bush))  # tiny island

        prairie_plateau = Location()  # prairie plateau at the owl statue
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            prairie_plateau.add(OwlStatue(0x0A8))
        Location().add(Seashell(0x0A8)).connect(prairie_plateau, SHOVEL)  # at the owl statue

        prairie_cave = Location()
        prairie_cave_secret_exit = Location().connect(prairie_cave, AND(BOMB, OR(FEATHER, ROOSTER)))
        self._addEntrance("prairie_right_cave_top", ukuku_prairie, prairie_cave, None)
        self._addEntrance("prairie_right_cave_bottom", left_bay_area, prairie_cave, None)
        self._addEntrance("prairie_right_cave_high", prairie_plateau, prairie_cave_secret_exit, None)

        bay_madbatter_connector_entrance = Location()
        bay_madbatter_connector_exit = Location().connect(bay_madbatter_connector_entrance, FLIPPERS)
        bay_madbatter_connector_outside = Location()
        bay_madbatter = Location().connect(Location().add(MadBatter(0x1E0)), MAGIC_POWDER)
        self._addEntrance("prairie_madbatter_connector_entrance", left_bay_area, bay_madbatter_connector_entrance, AND(OR(FEATHER, ROOSTER), OR(SWORD, MAGIC_ROD, BOOMERANG)))
        self._addEntranceRequirementExit("prairie_madbatter_connector_entrance", AND(OR(FEATHER, ROOSTER), r.bush)) # if exiting, you can pick up the bushes by normal means
        self._addEntrance("prairie_madbatter_connector_exit", bay_madbatter_connector_outside, bay_madbatter_connector_exit, None)
        self._addEntrance("prairie_madbatter", bay_madbatter_connector_outside, bay_madbatter, None)

        seashell_mansion = Location()
        if options.goal != "seashells":
            Location().add(SeashellMansion(0x2E9)).connect(seashell_mansion, COUNT(SEASHELL, 20))
        else:
            seashell_mansion.add(DroppedKey(0x2E9))
        self._addEntrance("seashell_mansion", ukuku_prairie, seashell_mansion, None)

        bay_water = Location()
        bay_water.connect(ukuku_prairie, FLIPPERS)
        bay_water.connect(left_bay_area, FLIPPERS)
        fisher_under_bridge = Location().add(TradeSequenceItem(0x2F5, TRADING_ITEM_NECKLACE))
        fisher_under_bridge.connect(bay_water, AND(TRADING_ITEM_FISHING_HOOK, FEATHER, FLIPPERS))
        bay_water.connect(Location().add(TradeSequenceItem(0x0C9, TRADING_ITEM_SCALE)), AND(TRADING_ITEM_NECKLACE, FLIPPERS))
        d5_entrance = Location().connect(bay_water, FLIPPERS)
        self._addEntrance("d5", d5_entrance, None, None)

        # Richard
        richard_house = Location()
        richard_cave = Location().connect(richard_house, COUNT(GOLD_LEAF, 5))
        richard_cave.connect(richard_house, None, one_way=True) # can exit richard's cave even without leaves
        richard_cave_chest = Location().add(Chest(0x2C8)).connect(richard_cave, OR(FEATHER, HOOKSHOT, ROOSTER))
        richard_maze = Location()
        self._addEntrance("richard_house", ukuku_prairie, richard_house, None)
        self._addEntrance("richard_maze", richard_maze, richard_cave, None)
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            Location().add(OwlStatue(0x0C6)).connect(richard_maze, r.bush)
        Location().add(SlimeKey()).connect(richard_maze, AND(r.bush, SHOVEL))

        next_to_castle = Location()
        if options.tradequest:
            ukuku_prairie.connect(next_to_castle, TRADING_ITEM_BANANAS, one_way=True) # can only give bananas from ukuku prairie side
        else:
            next_to_castle.connect(ukuku_prairie, None)
        next_to_castle.connect(ukuku_prairie, FLIPPERS)
        self._addEntrance("castle_phone", next_to_castle, None, None)
        castle_secret_entrance_left = Location()
        castle_secret_entrance_right = Location().connect(castle_secret_entrance_left, FEATHER)
        castle_courtyard = Location()
        castle_frontdoor = Location().connect(castle_courtyard, r.bush)
        castle_frontdoor.connect(ukuku_prairie, "CASTLE_BUTTON") # the button in the castle connector allows access to the castle grounds in ER
        self._addEntrance("castle_secret_entrance", next_to_castle, castle_secret_entrance_right, OR(BOMB, BOOMERANG, MAGIC_POWDER, MAGIC_ROD, SWORD))
        self._addEntrance("castle_secret_exit", castle_courtyard, castle_secret_entrance_left, None)

        Location().add(HeartPiece(0x078)).connect(bay_water, FLIPPERS)  # in the moat of the castle
        castle_inside = Location()
        Location().add(KeyLocation("CASTLE_BUTTON")).connect(castle_inside, None)
        castle_top_outside = Location()
        castle_top_inside = Location()
        self._addEntrance("castle_main_entrance", castle_frontdoor, castle_inside, r.bush)
        self._addEntrance("castle_upper_left", castle_top_outside, castle_inside, None)
        self._addEntrance("castle_upper_right", castle_top_outside, castle_top_inside, None)
        Location().add(GoldLeaf(0x05A)).connect(castle_courtyard, OR(SWORD, BOW, MAGIC_ROD))  # mad bomber, enemy hiding in the 6 holes
        crow_gold_leaf = Location().add(GoldLeaf(0x058)).connect(castle_courtyard, AND(POWER_BRACELET, r.attack_hookshot_no_bomb))  # bird on tree, can't kill with bomb cause it flies off. immune to magic_powder
        Location().add(GoldLeaf(0x2D2)).connect(castle_inside, r.attack_hookshot_powder)  # in the castle, kill enemies
        Location().add(GoldLeaf(0x2C5)).connect(castle_inside, AND(BOMB, r.attack_hookshot_powder))  # in the castle, bomb wall to show enemy
        kanalet_chain_trooper = Location().add(GoldLeaf(0x2C6))  # in the castle, spinning spikeball enemy
        castle_top_inside.connect(kanalet_chain_trooper, AND(POWER_BRACELET, r.attack_hookshot), one_way=True)

        animal_village = Location()
        animal_village.connect(Location().add(TradeSequenceItem(0x0CD, TRADING_ITEM_FISHING_HOOK)), TRADING_ITEM_BROOM)
        cookhouse = Location()
        cookhouse.connect(Location().add(TradeSequenceItem(0x2D7, TRADING_ITEM_PINEAPPLE)), TRADING_ITEM_HONEYCOMB)
        goathouse = Location()
        goathouse.connect(Location().add(TradeSequenceItem(0x2D9, TRADING_ITEM_LETTER)), TRADING_ITEM_HIBISCUS)
        mermaid_statue = Location()
        mermaid_statue.connect(animal_village, AND(TRADING_ITEM_SCALE, HOOKSHOT))
        mermaid_statue.add(TradeSequenceItem(0x297, TRADING_ITEM_MAGNIFYING_GLASS))
        self._addEntrance("animal_phone", animal_village, None, None)
        self._addEntrance("animal_house1", animal_village, None, None)
        self._addEntrance("animal_house2", animal_village, None, None)
        self._addEntrance("animal_house3", animal_village, goathouse, None)
        self._addEntrance("animal_house4", animal_village, None, None)
        self._addEntrance("animal_house5", animal_village, cookhouse, None)
        animal_village.connect(bay_water, FLIPPERS)
        animal_village.connect(ukuku_prairie, OR(HOOKSHOT, ROOSTER))
        animal_village_connector_left = Location()
        animal_village_connector_right = Location().connect(animal_village_connector_left, PEGASUS_BOOTS)
        self._addEntrance("prairie_to_animal_connector", ukuku_prairie, animal_village_connector_left, OR(BOMB, BOOMERANG, MAGIC_POWDER, MAGIC_ROD, SWORD)) # passage under river blocked by bush
        self._addEntrance("animal_to_prairie_connector", animal_village, animal_village_connector_right, None)
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            animal_village.add(OwlStatue(0x0DA))
        Location().add(Seashell(0x0DA)).connect(animal_village, SHOVEL)  # owl statue at the water
        desert = Location().connect(animal_village, r.bush)  # Note: We moved the walrus blocking the desert.
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            desert.add(OwlStatue(0x0CF))
        desert_lanmola = Location().add(AnglerKey()).connect(desert, OR(BOW, SWORD, HOOKSHOT, MAGIC_ROD, BOOMERANG))

        animal_village_bombcave = Location()
        self._addEntrance("animal_cave", desert, animal_village_bombcave, BOMB)
        self._addEntranceRequirementExit("animal_cave", None) # if exiting, you do not need bombs
        animal_village_bombcave_heartpiece = Location().add(HeartPiece(0x2E6)).connect(animal_village_bombcave, OR(AND(BOMB, FEATHER, HOOKSHOT), ROOSTER))  # cave in the upper right of animal town

        desert_cave = Location()
        self._addEntrance("desert_cave", desert, desert_cave, None)
        desert.connect(desert_cave, None, one_way=True) # Drop down the sinkhole

        Location().add(HeartPiece(0x1E8)).connect(desert_cave, BOMB)  # above the quicksand cave
        Location().add(Seashell(0x0FF)).connect(desert, POWER_BRACELET) # bottom right corner of the map

        armos_maze = Location().connect(animal_village, POWER_BRACELET)
        armos_temple = Location()
        Location().add(FaceKey()).connect(armos_temple, r.miniboss_requirements[world_setup.miniboss_mapping["armos_temple"]])
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            armos_maze.add(OwlStatue(0x08F))
        self._addEntrance("armos_maze_cave", armos_maze, Location().add(Chest(0x2FC)), None)
        self._addEntrance("armos_temple", armos_maze, armos_temple, None)

        armos_fairy_entrance = Location().connect(bay_water, FLIPPERS).connect(animal_village, POWER_BRACELET)
        self._addEntrance("armos_fairy", armos_fairy_entrance, None, BOMB)
        self._addEntranceRequirementExit("armos_fairy", None) # if exiting, you do not need bombs

        d6_connector_left = Location()
        d6_connector_right = Location().connect(d6_connector_left, OR(AND(HOOKSHOT, OR(FLIPPERS, AND(FEATHER, PEGASUS_BOOTS))), ROOSTER))
        d6_entrance = Location()
        d6_entrance.connect(bay_water, FLIPPERS, one_way=True)
        d6_armos_island = Location().connect(bay_water, FLIPPERS)
        self._addEntrance("d6_connector_entrance", d6_armos_island, d6_connector_right, None)
        self._addEntrance("d6_connector_exit", d6_entrance, d6_connector_left, None)
        self._addEntrance("d6", d6_entrance, None, FACE_KEY)
        self._addEntranceRequirementExit("d6", None) # if exiting, you do not need to open the dungeon

        windfish_egg = Location().connect(swamp, POWER_BRACELET).connect(graveyard, POWER_BRACELET)
        windfish_egg.connect(graveyard, None, one_way=True) # Ledge jump

        obstacle_cave_entrance = Location()
        obstacle_cave_inside = Location().connect(obstacle_cave_entrance, SWORD)
        obstacle_cave_inside.connect(obstacle_cave_entrance, FEATHER, one_way=True) # can get past the rock room from right to left pushing blocks and jumping over the pit
        obstacle_cave_inside_chest = Location().add(Chest(0x2BB)).connect(obstacle_cave_inside, OR(HOOKSHOT, ROOSTER))  # chest at obstacles
        obstacle_cave_exit = Location().connect(obstacle_cave_inside, OR(PEGASUS_BOOTS, ROOSTER))

        lower_right_taltal = Location()
        self._addEntrance("obstacle_cave_entrance", windfish_egg, obstacle_cave_entrance, POWER_BRACELET)
        self._addEntrance("obstacle_cave_outside_chest", Location().add(Chest(0x018)), obstacle_cave_inside, None)
        self._addEntrance("obstacle_cave_exit", lower_right_taltal, obstacle_cave_exit, None)

        papahl_cave = Location().add(Chest(0x28A))
        papahl = Location().connect(lower_right_taltal, None, one_way=True)
        hibiscus_item = Location().add(TradeSequenceItem(0x019, TRADING_ITEM_HIBISCUS))
        papahl.connect(hibiscus_item, TRADING_ITEM_PINEAPPLE, one_way=True)
        self._addEntrance("papahl_entrance", lower_right_taltal, papahl_cave, None)
        self._addEntrance("papahl_exit", papahl, papahl_cave, None)

        # D4 entrance and related things
        below_right_taltal = Location().connect(windfish_egg, POWER_BRACELET)
        below_right_taltal.add(KeyLocation("ANGLER_KEYHOLE"))
        below_right_taltal.connect(bay_water, FLIPPERS)
        below_right_taltal.connect(next_to_castle, ROOSTER) # fly from staircase to staircase on the north side of the moat
        lower_right_taltal.connect(below_right_taltal, FLIPPERS, one_way=True)

        heartpiece_swim_cave = Location().connect(Location().add(HeartPiece(0x1F2)), FLIPPERS)
        self._addEntrance("heartpiece_swim_cave", below_right_taltal, heartpiece_swim_cave, FLIPPERS)  # cave next to level 4
        d4_entrance = Location().connect(below_right_taltal, FLIPPERS)
        lower_right_taltal.connect(d4_entrance, AND(ANGLER_KEY, "ANGLER_KEYHOLE"), one_way=True)
        self._addEntrance("d4", d4_entrance, None, ANGLER_KEY)
        self._addEntranceRequirementExit("d4", FLIPPERS) # if exiting, you can leave with flippers without opening the dungeon
        mambo = Location().connect(Location().add(Song(0x2FD)), AND(OCARINA, FLIPPERS))  # Manbo's Mambo
        self._addEntrance("mambo", d4_entrance, mambo, FLIPPERS) 

        # Raft game.
        raft_house = Location("Raft House")
        Location().add(KeyLocation("RAFT")).connect(raft_house, COUNT("RUPEES", 100))
        raft_return_upper = Location()
        raft_return_lower = Location().connect(raft_return_upper, None, one_way=True)
        outside_raft_house = Location().connect(below_right_taltal, HOOKSHOT).connect(below_right_taltal, FLIPPERS, one_way=True)
        raft_game = Location()
        raft_game.connect(outside_raft_house, "RAFT")
        raft_game.add(Chest(0x05C), Chest(0x05D)) # Chests in the rafting game
        raft_exit = Location()
        if options.logic != "casual":  # use raft to reach north armos maze entrances without flippers
            raft_game.connect(raft_exit, None, one_way=True)
            raft_game.connect(armos_fairy_entrance, None, one_way=True)
        self._addEntrance("raft_return_exit", outside_raft_house, raft_return_upper, None)
        self._addEntrance("raft_return_enter", raft_exit, raft_return_lower, None)
        raft_exit.connect(armos_fairy_entrance, FLIPPERS)
        self._addEntrance("raft_house", outside_raft_house, raft_house, None)
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            raft_game.add(OwlStatue(0x5D))

        outside_rooster_house = Location().connect(lower_right_taltal, OR(FLIPPERS, ROOSTER))
        self._addEntrance("rooster_house", outside_rooster_house, None, None)
        bird_cave = Location()
        bird_key = Location().add(BirdKey())
        bird_cave.connect(bird_key, OR(AND(FEATHER, COUNT(POWER_BRACELET, 2)), ROOSTER))
        if options.logic != "casual":
            bird_cave.connect(lower_right_taltal, None, one_way=True)  # Drop in a hole at bird cave
        self._addEntrance("bird_cave", outside_rooster_house, bird_cave, None)
        bridge_seashell = Location().add(Seashell(0x00C)).connect(outside_rooster_house, AND(OR(FEATHER, ROOSTER), POWER_BRACELET))  # seashell right of rooster house, there is a hole in the bridge

        multichest_cave = Location()
        multichest_cave_secret = Location().connect(multichest_cave, BOMB)
        water_cave_hole = Location()  # Location with the hole that drops you onto the hearth piece under water
        if options.logic != "casual":
            water_cave_hole.connect(heartpiece_swim_cave, FLIPPERS, one_way=True)
        multichest_outside = Location().add(Chest(0x01D))  # chest after multichest puzzle outside
        self._addEntrance("multichest_left", lower_right_taltal, multichest_cave, OR(FLIPPERS, ROOSTER))
        self._addEntrance("multichest_right", water_cave_hole, multichest_cave, None)
        self._addEntrance("multichest_top", multichest_outside, multichest_cave_secret, None)
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            water_cave_hole.add(OwlStatue(0x1E)) # owl statue below d7

        right_taltal_connector1 = Location()
        right_taltal_connector_outside1 = Location()
        right_taltal_connector2 = Location()
        right_taltal_connector3 = Location()
        right_taltal_connector2.connect(right_taltal_connector3, AND(OR(FEATHER, ROOSTER), HOOKSHOT), one_way=True)
        right_taltal_connector_outside2 = Location()
        right_taltal_connector4 = Location()
        d7_platau = Location()
        d7_tower = Location()
        d7_platau.connect(d7_tower, AND(POWER_BRACELET, BIRD_KEY), one_way=True)
        self._addEntrance("right_taltal_connector1", water_cave_hole, right_taltal_connector1, None)
        self._addEntrance("right_taltal_connector2", right_taltal_connector_outside1, right_taltal_connector1, None)
        self._addEntrance("right_taltal_connector3", right_taltal_connector_outside1, right_taltal_connector2, None)
        self._addEntrance("right_taltal_connector4", right_taltal_connector_outside2, right_taltal_connector3, None)
        self._addEntrance("right_taltal_connector5", right_taltal_connector_outside2, right_taltal_connector4, None)
        self._addEntrance("right_taltal_connector6", d7_platau, right_taltal_connector4, None)
        self._addEntrance("right_fairy", right_taltal_connector_outside2, None, BOMB)
        self._addEntranceRequirementExit("right_fairy", None) # if exiting, you do not need bombs
        self._addEntrance("d7", d7_tower, None, None)
        if options.logic != "casual": # D7 area ledge drops
            d7_platau.connect(heartpiece_swim_cave, FLIPPERS, one_way=True)
            d7_platau.connect(right_taltal_connector_outside1, None, one_way=True)

        mountain_bridge_staircase = Location().connect(outside_rooster_house, OR(HOOKSHOT, ROOSTER)) # cross bridges to staircase
        if options.logic != "casual":  # ledge drop
            mountain_bridge_staircase.connect(windfish_egg, None, one_way=True)

        left_right_connector_cave_entrance = Location()
        left_right_connector_cave_exit = Location()
        left_right_connector_cave_entrance.connect(left_right_connector_cave_exit, OR(HOOKSHOT, ROOSTER), one_way=True)  # pass through the underground passage to left side
        taltal_boulder_zone = Location()
        self._addEntrance("left_to_right_taltalentrance", mountain_bridge_staircase, left_right_connector_cave_entrance, OR(BOMB, BOOMERANG, MAGIC_POWDER, MAGIC_ROD, SWORD))
        self._addEntrance("left_taltal_entrance", taltal_boulder_zone, left_right_connector_cave_exit, None)
        mountain_heartpiece = Location().add(HeartPiece(0x2BA)) # heartpiece in connecting cave
        left_right_connector_cave_entrance.connect(mountain_heartpiece, BOMB, one_way=True)  # in the connecting cave from right to left. one_way to prevent access to left_side_mountain via glitched logic

        taltal_boulder_zone.add(Chest(0x004)) # top of falling rocks hill
        taltal_madbatter = Location().connect(Location().add(MadBatter(0x1E2)), MAGIC_POWDER)
        self._addEntrance("madbatter_taltal", taltal_boulder_zone, taltal_madbatter, POWER_BRACELET)
        self._addEntranceRequirementExit("madbatter_taltal", None) # if exiting, you do not need bracelet

        outside_fire_cave = Location()
        if options.logic != "casual":
            outside_fire_cave.connect(writes_hut_outside, None, one_way=True)  # Jump down the ledge
        taltal_boulder_zone.connect(outside_fire_cave, None, one_way=True)
        fire_cave_bottom = Location()
        fire_cave_top = Location().connect(fire_cave_bottom, COUNT(SHIELD, 2))
        self._addEntrance("fire_cave_entrance", outside_fire_cave, fire_cave_bottom, BOMB)
        self._addEntranceRequirementExit("fire_cave_entrance", None) # if exiting, you do not need bombs

        d8_entrance = Location()
        if options.logic != "casual":
            d8_entrance.connect(writes_hut_outside, None, one_way=True) # Jump down the ledge
            d8_entrance.connect(outside_fire_cave, None, one_way=True) # Jump down the other ledge
        self._addEntrance("fire_cave_exit", d8_entrance, fire_cave_top, None)
        self._addEntrance("phone_d8", d8_entrance, None, None)
        self._addEntrance("d8", d8_entrance, None, AND(OCARINA, SONG3, SWORD))
        self._addEntranceRequirementExit("d8", None) # if exiting, you do not need to wake the turtle

        nightmare = Location("Nightmare")
        windfish = Location("Windfish").connect(nightmare, AND(MAGIC_POWDER, SWORD, OR(BOOMERANG, BOW)))

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            hookshot_cave.connect(hookshot_cave_chest, AND(FEATHER, PEGASUS_BOOTS)) # boots jump the gap to the chest
            graveyard_cave_left.connect(graveyard_cave_right, HOOKSHOT, one_way=True) # hookshot the block behind the stairs while over the pit
            swamp_chest.connect(swamp, None)  # Clip past the flower
            self._addEntranceRequirement("d2", POWER_BRACELET) # clip the top wall to walk between the goponga flower and the wall
            self._addEntranceRequirement("d2", COUNT(SWORD, 2)) # use l2 sword spin to kill goponga flowers
            swamp.connect(writes_hut_outside, HOOKSHOT, one_way=True) # hookshot the sign in front of writes hut
            graveyard_heartpiece.connect(graveyard_cave_right, FEATHER) # jump to the bottom right tile around the blocks
            graveyard_heartpiece.connect(graveyard_cave_right, OR(HOOKSHOT, BOOMERANG)) # push bottom block, wall clip and hookshot/boomerang corner to grab item
            
            self._addEntranceRequirement("mamu", AND(FEATHER, POWER_BRACELET)) # can clear the gaps at the start with just feather, can reach bottom left sign with a well timed jump while wall clipped
            self._addEntranceRequirement("prairie_madbatter_connector_entrance", AND(OR(FEATHER, ROOSTER), OR(MAGIC_POWDER, BOMB))) # use bombs or powder to get rid of a bush on the other side by jumping across and placing the bomb/powder before you fall into the pit
            fisher_under_bridge.connect(bay_water, AND(TRADING_ITEM_FISHING_HOOK, FLIPPERS)) # can talk to the fisherman from the water when the boat is low (requires swimming up out of the water a bit)
            crow_gold_leaf.connect(castle_courtyard, POWER_BRACELET) # bird on tree at left side kanalet, can use both rocks to kill the crow removing the kill requirement
            castle_inside.connect(kanalet_chain_trooper, BOOMERANG, one_way=True) # kill the ball and chain trooper from the left side, then use boomerang to grab the dropped item
            animal_village_bombcave_heartpiece.connect(animal_village_bombcave, AND(PEGASUS_BOOTS, FEATHER)) # jump across horizontal 4 gap to heart piece
            desert_lanmola.connect(desert, BOMB) # use bombs to kill lanmola
            
            d6_connector_left.connect(d6_connector_right, AND(OR(FLIPPERS, PEGASUS_BOOTS), FEATHER))  # jump the gap in underground passage to d6 left side to skip hookshot
            bird_key.connect(bird_cave, COUNT(POWER_BRACELET, 2))  # corner walk past the one pit on the left side to get to the elephant statue
            fire_cave_bottom.connect(fire_cave_top, PEGASUS_BOOTS, one_way=True) # flame skip

        if options.logic == 'glitched' or options.logic == 'hell':
            #self._addEntranceRequirement("dream_hut", FEATHER) # text clip TODO: require nag messages
            self._addEntranceRequirementEnter("dream_hut", HOOKSHOT) # clip past the rocks in front of dream hut
            dream_hut_right.connect(dream_hut_left, FEATHER) # super jump
            forest.connect(swamp, BOMB)  # bomb trigger tarin
            forest.connect(forest_heartpiece, BOMB, one_way=True) # bomb trigger heartpiece
            self._addEntranceRequirementEnter("hookshot_cave", HOOKSHOT) # clip past the rocks in front of hookshot cave
            swamp.connect(forest_toadstool, None, one_way=True) # villa buffer from top (swamp phonebooth area) to bottom (toadstool area)
            writes_hut_outside.connect(swamp, None, one_way=True) # villa buffer from top (writes hut) to bottom (swamp phonebooth area) or damage boost
            graveyard.connect(forest_heartpiece, None, one_way=True) # villa buffer from top.
            log_cave_heartpiece.connect(forest_cave, FEATHER) # super jump
            log_cave_heartpiece.connect(forest_cave, BOMB) # bomb trigger
            graveyard_cave_left.connect(graveyard_heartpiece, BOMB, one_way=True) # bomb trigger the heartpiece from the left side
            graveyard_heartpiece.connect(graveyard_cave_right, None) # sideways block push from the right staircase.

            prairie_island_seashell.connect(ukuku_prairie, AND(FEATHER, r.bush)) # jesus jump from right side, screen transition on top of the water to reach the island
            self._addEntranceRequirement("castle_jump_cave", FEATHER) # 1 pit buffer to clip bottom wall and jump across.
            left_bay_area.connect(ghost_hut_outside, FEATHER) # 1 pit buffer to get across
            tiny_island.connect(left_bay_area, AND(FEATHER, r.bush)) # jesus jump around
            bay_madbatter_connector_exit.connect(bay_madbatter_connector_entrance, FEATHER, one_way=True) # jesus jump (3 screen) through the underground passage leading to martha's bay mad batter
            self._addEntranceRequirement("prairie_madbatter_connector_entrance", AND(FEATHER, POWER_BRACELET)) # villa buffer into the top side of the bush, then pick it up
            
            ukuku_prairie.connect(richard_maze, OR(BOMB, BOOMERANG, MAGIC_POWDER, MAGIC_ROD, SWORD), one_way=True) # break bushes on north side of the maze, and 1 pit buffer into the maze
            fisher_under_bridge.connect(bay_water, AND(BOMB, FLIPPERS)) # can bomb trigger the item without having the hook 
            animal_village.connect(ukuku_prairie, FEATHER) # jesus jump
            below_right_taltal.connect(next_to_castle, FEATHER) # jesus jump (north of kanalet castle phonebooth)
            animal_village_connector_right.connect(animal_village_connector_left, FEATHER) # text clip past the obstacles (can go both ways), feather to wall clip the obstacle without triggering text or shaq jump in bottom right corner if text is off
            animal_village_bombcave_heartpiece.connect(animal_village_bombcave, AND(BOMB, OR(HOOKSHOT, FEATHER, PEGASUS_BOOTS))) # bomb trigger from right side, corner walking top right pit is stupid so hookshot or boots added
            animal_village_bombcave_heartpiece.connect(animal_village_bombcave,  FEATHER) # villa buffer across the pits

            d6_entrance.connect(ukuku_prairie, FEATHER, one_way=True) # jesus jump (2 screen) from d6 entrance bottom ledge to ukuku prairie
            d6_entrance.connect(armos_fairy_entrance, FEATHER, one_way=True) # jesus jump (2 screen) from d6 entrance top ledge to armos fairy entrance
            armos_fairy_entrance.connect(d6_armos_island, FEATHER, one_way=True) # jesus jump from top (fairy bomb cave) to armos island
            armos_fairy_entrance.connect(raft_exit, FEATHER) # jesus jump (2-ish screen) from fairy cave to lower raft connector
            self._addEntranceRequirementEnter("obstacle_cave_entrance", HOOKSHOT) # clip past the rocks in front of obstacle cave entrance
            obstacle_cave_inside_chest.connect(obstacle_cave_inside, FEATHER) # jump to the rightmost pits + 1 pit buffer to jump across
            obstacle_cave_exit.connect(obstacle_cave_inside, FEATHER) #  1 pit buffer above boots crystals to get past
            lower_right_taltal.connect(hibiscus_item, AND(TRADING_ITEM_PINEAPPLE, BOMB), one_way=True) # bomb trigger papahl from below ledge, requires pineapple
            
            self._addEntranceRequirement("heartpiece_swim_cave", FEATHER)  # jesus jump into the cave entrance after jumping down the ledge, can jesus jump back to the ladder 1 screen below
            self._addEntranceRequirement("mambo", FEATHER)  # jesus jump from (unlocked) d4 entrance to mambo's cave entrance
            outside_raft_house.connect(below_right_taltal, FEATHER, one_way=True) # jesus jump from the ledge at raft to the staircase 1 screen south

            self._addEntranceRequirement("multichest_left", FEATHER) # jesus jump past staircase leading up the mountain 
            outside_rooster_house.connect(lower_right_taltal, FEATHER) # jesus jump (1 or 2 screen depending if angler key is used) to staircase leading up the mountain
            d7_platau.connect(water_cave_hole, None, one_way=True) # use save and quit menu to gain control while falling to dodge the water cave hole
            mountain_bridge_staircase.connect(outside_rooster_house, AND(PEGASUS_BOOTS, FEATHER)) # cross bridge to staircase with pit buffer to clip bottom wall and jump across
            bird_key.connect(bird_cave, AND(FEATHER, HOOKSHOT))  # hookshot jump across the big pits room
            right_taltal_connector2.connect(right_taltal_connector3, None, one_way=True) # 2 seperate pit buffers so not obnoxious to get past the two pit rooms before d7 area. 2nd pits can pit buffer on top right screen, bottom wall to scroll on top of the wall on bottom screen
            left_right_connector_cave_exit.connect(left_right_connector_cave_entrance, AND(HOOKSHOT, FEATHER), one_way=True)  # pass through the passage in reverse using a superjump to get out of the dead end
            obstacle_cave_inside.connect(mountain_heartpiece, BOMB, one_way=True) # bomb trigger from boots crystal cave
            self._addEntranceRequirement("d8", OR(BOMB, AND(OCARINA, SONG3))) # bomb trigger the head and walk trough, or play the ocarina song 3 and walk through

        if options.logic == 'hell':
            dream_hut_right.connect(dream_hut, None) # alternate diagonal movement with orthogonal movement to control the mimics. Get them clipped into the walls to walk past
            swamp.connect(forest_toadstool, None) # damage boost from toadstool area across the pit
            swamp.connect(forest, AND(r.bush, OR(PEGASUS_BOOTS, HOOKSHOT))) # boots bonk / hookshot spam over the pits right of forest_rear_chest
            forest.connect(forest_heartpiece, PEGASUS_BOOTS, one_way=True) # boots bonk across the pits
            log_cave_heartpiece.connect(forest_cave, BOOMERANG) # clip the boomerang through the corner gaps on top right to grab the item
            log_cave_heartpiece.connect(forest_cave, AND(ROOSTER, OR(PEGASUS_BOOTS, SWORD, BOW, MAGIC_ROD))) # boots rooster hop in bottom left corner to "superjump" into the area. use buffers after picking up rooster to gain height / time to throw rooster again facing up
            writes_hut_outside.connect(swamp, None) # damage boost with moblin arrow next to telephone booth
            writes_cave_left_chest.connect(writes_cave, None) # damage boost off the zol to get across the pit.
            graveyard.connect(crazy_tracy_hut, HOOKSHOT, one_way=True) # use hookshot spam to clip the rock on the right with the crow
            graveyard.connect(forest, OR(PEGASUS_BOOTS, HOOKSHOT)) # boots bonk witches hut, or hookshot spam across the pit
            graveyard_cave_left.connect(graveyard_cave_right, HOOKSHOT) # hookshot spam over the pit
            graveyard_cave_right.connect(graveyard_cave_left, PEGASUS_BOOTS, one_way=True) # boots bonk off the cracked block
            
            self._addEntranceRequirementEnter("mamu", AND(PEGASUS_BOOTS, POWER_BRACELET)) # can clear the gaps at the start with multiple pit buffers, can reach bottom left sign with bonking along the bottom wall
            self._addEntranceRequirement("castle_jump_cave", PEGASUS_BOOTS) # pit buffer to clip bottom wall and boots bonk across
            prairie_cave_secret_exit.connect(prairie_cave, AND(BOMB, OR(PEGASUS_BOOTS, HOOKSHOT))) # hookshot spam or boots bonk across pits can go from left to right by pit buffering on top of the bottom wall then boots bonk across
            richard_cave_chest.connect(richard_cave, None) # use the zol on the other side of the pit to damage boost across (requires damage from pit + zol)
            castle_secret_entrance_right.connect(castle_secret_entrance_left, AND(PEGASUS_BOOTS, "MEDICINE2")) # medicine iframe abuse to get across spikes with a boots bonk
            left_bay_area.connect(ghost_hut_outside, PEGASUS_BOOTS) # multiple pit buffers to bonk across the bottom wall
            tiny_island.connect(left_bay_area, AND(PEGASUS_BOOTS, r.bush)) # jesus jump around with boots bonks, then one final bonk off the bottom wall to get on the staircase (needs to be centered correctly)
            self._addEntranceRequirement("prairie_madbatter_connector_entrance", AND(PEGASUS_BOOTS, OR(MAGIC_POWDER, BOMB, SWORD, MAGIC_ROD, BOOMERANG))) # Boots bonk across the bottom wall, then remove one of the bushes to get on land
            self._addEntranceRequirementExit("prairie_madbatter_connector_entrance", AND(PEGASUS_BOOTS, r.bush)) # if exiting, you can pick up the bushes by normal means and boots bonk across the bottom wall

            # bay_water connectors, only left_bay_area, ukuku_prairie and animal_village have to be connected with jesus jumps. below_right_taltal, d6_armos_island and armos_fairy_entrance are accounted for via ukuku prairie in glitch logic
            left_bay_area.connect(bay_water, FEATHER) # jesus jump (can always reach bay_water with jesus jumping from every way to enter bay_water, so no one_way)
            animal_village.connect(bay_water, FEATHER) # jesus jump (can always reach bay_water with jesus jumping from every way to enter bay_water, so no one_way)
            ukuku_prairie.connect(bay_water, FEATHER, one_way=True) # jesus jump
            bay_water.connect(d5_entrance, FEATHER) # jesus jump into d5 entrance (wall clip), wall clip + jesus jump to get out
            
            crow_gold_leaf.connect(castle_courtyard, BOMB) # bird on tree at left side kanalet, place a bomb against the tree and the crow flies off. With well placed second bomb the crow can be killed
            mermaid_statue.connect(animal_village, AND(TRADING_ITEM_SCALE, FEATHER)) # early mermaid statue by buffering on top of the right ledge, then superjumping to the left (horizontal pixel perfect)
            animal_village_bombcave_heartpiece.connect(animal_village_bombcave, PEGASUS_BOOTS) # boots bonk across bottom wall (both at entrance and in item room)

            d6_armos_island.connect(ukuku_prairie, FEATHER) # jesus jump (3 screen) from seashell mansion to armos island
            armos_fairy_entrance.connect(d6_armos_island, PEGASUS_BOOTS, one_way=True) # jesus jump from top (fairy bomb cave) to armos island with fast falling 
            d6_connector_right.connect(d6_connector_left, PEGASUS_BOOTS) # boots bonk across bottom wall at water and pits (can do both ways)
            
            obstacle_cave_entrance.connect(obstacle_cave_inside, OR(HOOKSHOT, AND(FEATHER, PEGASUS_BOOTS, OR(SWORD, MAGIC_ROD, BOW)))) # get past crystal rocks by hookshotting into top pushable block, or boots dashing into top wall where the pushable block is to superjump down
            obstacle_cave_entrance.connect(obstacle_cave_inside, AND(PEGASUS_BOOTS, ROOSTER)) # get past crystal rocks pushing the top pushable block, then boots dashing up picking up the rooster before bonking. Pause buffer until rooster is fully picked up then throw it down before bonking into wall
            d4_entrance.connect(below_right_taltal, FEATHER) # jesus jump a long way
            if options.entranceshuffle in ("default", "simple"): # connector cave from armos d6 area to raft shop may not be randomized to add a flippers path since flippers stop you from jesus jumping
                below_right_taltal.connect(raft_game, AND(FEATHER, r.attack_hookshot_powder), one_way=True) # jesus jump from heartpiece water cave, around the island and clip past the diagonal gap in the rock, then jesus jump all the way down the waterfall to the chests (attack req for hardlock flippers+feather scenario)
            outside_raft_house.connect(below_right_taltal, AND(FEATHER, PEGASUS_BOOTS)) #superjump from ledge left to right, can buffer to land on ledge instead of water, then superjump right which is pixel perfect
            bridge_seashell.connect(outside_rooster_house, AND(PEGASUS_BOOTS, POWER_BRACELET)) # boots bonk
            bird_key.connect(bird_cave, AND(FEATHER, PEGASUS_BOOTS)) # boots jump above wall, use multiple pit buffers to get across
            mountain_bridge_staircase.connect(outside_rooster_house, OR(PEGASUS_BOOTS, FEATHER)) # cross bridge to staircase with pit buffer to clip bottom wall and jump or boots bonk across
            left_right_connector_cave_entrance.connect(left_right_connector_cave_exit, AND(PEGASUS_BOOTS, FEATHER), one_way=True) # boots jump to bottom left corner of pits, pit buffer and jump to left
            left_right_connector_cave_exit.connect(left_right_connector_cave_entrance, AND(ROOSTER, OR(PEGASUS_BOOTS, SWORD, BOW, MAGIC_ROD)), one_way=True)  # pass through the passage in reverse using a boots rooster hop or rooster superjump in the one way passage area
            
        self.start = start_house
        self.egg = windfish_egg
        self.nightmare = nightmare
        self.windfish = windfish

    def _addEntrance(self, name, outside, inside, requirement):
        assert name not in self.overworld_entrance, "Duplicate entrance: %s" % name
        assert name in ENTRANCE_INFO
        self.overworld_entrance[name] = EntranceExterior(outside, requirement)
        self.indoor_location[name] = inside

    def _addEntranceRequirement(self, name, requirement):
        assert name in self.overworld_entrance
        self.overworld_entrance[name].addRequirement(requirement)

    def _addEntranceRequirementEnter(self, name, requirement):
        assert name in self.overworld_entrance
        self.overworld_entrance[name].addEnterRequirement(requirement)

    def _addEntranceRequirementExit(self, name, requirement):
        assert name in self.overworld_entrance
        self.overworld_entrance[name].addExitRequirement(requirement)

    def updateIndoorLocation(self, name, location):
        assert name in self.indoor_location
        assert self.indoor_location[name] is None
        self.indoor_location[name] = location


class DungeonDiveOverworld:
    def __init__(self, options, r):
        self.overworld_entrance = {}
        self.indoor_location = {}

        start_house = Location("Start House").add(StartItem())
        Location().add(ShopItem(0)).connect(start_house, OR(COUNT("RUPEES", 200), SWORD))
        Location().add(ShopItem(1)).connect(start_house, OR(COUNT("RUPEES", 980), SWORD))
        Location().add(Song(0x0B1)).connect(start_house, OCARINA)  # Marins song
        start_house.add(DroppedKey(0xB2))  # Sword on the beach
        egg = Location().connect(start_house, AND(r.bush, BOMB))
        Location().add(MadBatter(0x1E1)).connect(start_house, MAGIC_POWDER)
        if options.boomerang == 'trade':
            Location().add(BoomerangGuy()).connect(start_house, AND(BOMB, OR(BOOMERANG, HOOKSHOT, MAGIC_ROD, PEGASUS_BOOTS, FEATHER, SHOVEL)))
        elif options.boomerang == 'gift':
            Location().add(BoomerangGuy()).connect(start_house, BOMB)

        nightmare = Location("Nightmare")
        windfish = Location("Windfish").connect(nightmare, AND(MAGIC_POWDER, SWORD, OR(BOOMERANG, BOW)))

        self.start = start_house
        self.overworld_entrance = {
            "d1": EntranceExterior(start_house, None),
            "d2": EntranceExterior(start_house, None),
            "d3": EntranceExterior(start_house, None),
            "d4": EntranceExterior(start_house, None),
            "d5": EntranceExterior(start_house, FLIPPERS),
            "d6": EntranceExterior(start_house, None),
            "d7": EntranceExterior(start_house, None),
            "d8": EntranceExterior(start_house, None),
            "d0": EntranceExterior(start_house, None),
        }
        self.egg = egg
        self.nightmare = nightmare
        self.windfish = windfish

    def updateIndoorLocation(self, name, location):
        self.indoor_location[name] = location


class EntranceExterior:
    def __init__(self, outside, requirement, one_way_enter_requirement="UNSET", one_way_exit_requirement="UNSET"):
        self.location = outside
        self.requirement = requirement
        self.one_way_enter_requirement = one_way_enter_requirement
        self.one_way_exit_requirement = one_way_exit_requirement
    
    def addRequirement(self, new_requirement):
        self.requirement = OR(self.requirement, new_requirement)

    def addExitRequirement(self, new_requirement):
        if self.one_way_exit_requirement == "UNSET":
            self.one_way_exit_requirement = new_requirement
        else:
            self.one_way_exit_requirement = OR(self.one_way_exit_requirement, new_requirement)

    def addEnterRequirement(self, new_requirement):
        if self.one_way_enter_requirement == "UNSET":
            self.one_way_enter_requirement = new_requirement
        else:
            self.one_way_enter_requirement = OR(self.one_way_enter_requirement, new_requirement)
    
    def enterIsSet(self):
        return self.one_way_enter_requirement != "UNSET"
    
    def exitIsSet(self):
        return self.one_way_exit_requirement != "UNSET"
