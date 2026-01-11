from typing import NamedTuple, Optional
from BaseClasses import Location
from .enums import MAIN_MENU_STRING, WORLD_2_STRING, Spelunky2Goal, JournalName, WorldName, LocationName

#####
# HUGE thanks to Cloiss for a lot of the logic changes in here to make more sense
#####


class Spelunky2Location(Location):
    game = "Spelunky 2"


class Spelunky2LocationData(NamedTuple):
    address: int
    region: str
    goal: Optional[int] = Spelunky2Goal.EASY


place_entries = {
    JournalName.DWELLING.value:        Spelunky2LocationData(1,  WorldName.DWELLING),
    JournalName.JUNGLE.value:          Spelunky2LocationData(2,  WorldName.JUNGLE),
    JournalName.VOLCANA.value:         Spelunky2LocationData(3,  WorldName.VOLCANA),
    JournalName.OLMECS_LAIR.value:     Spelunky2LocationData(4,  WorldName.OLMECS_LAIR),
    JournalName.TIDE_POOL.value:       Spelunky2LocationData(5,  WorldName.TIDE_POOL),
    JournalName.ABZU.value:            Spelunky2LocationData(6,  LocationName.ABZU),
    JournalName.TEMPLE.value:          Spelunky2LocationData(7,  WorldName.TEMPLE),
    JournalName.CITY_OF_GOLD.value:    Spelunky2LocationData(8,  LocationName.CITY_OF_GOLD),
    JournalName.DUAT.value:            Spelunky2LocationData(9,  LocationName.DUAT),
    JournalName.ICE_CAVES.value:       Spelunky2LocationData(10, WorldName.ICE_CAVES),
    JournalName.NEO_BABYLON.value:     Spelunky2LocationData(11, WorldName.NEO_BABYLON),
    JournalName.TIAMAT_THRONE.value:   Spelunky2LocationData(12, WorldName.SUNKEN_CITY, Spelunky2Goal.HARD),
    JournalName.SUNKEN_CITY.value:     Spelunky2LocationData(13, WorldName.SUNKEN_CITY, Spelunky2Goal.HARD),
    JournalName.EGGPLANT_WORLD.value:  Spelunky2LocationData(14, WorldName.EGGPLANT, Spelunky2Goal.HARD),
    JournalName.HUNDUN_HIDEAWAY.value: Spelunky2LocationData(15, WorldName.SUNKEN_CITY, Spelunky2Goal.HARD),
    JournalName.COSMIC_OCEAN.value:    Spelunky2LocationData(16, WorldName.COSMIC_OCEAN, Spelunky2Goal.CO),
}

people_entries = {
    JournalName.ANA_SPELUNKY.value:      Spelunky2LocationData(17, LocationName.VLADS_CASTLE),
    JournalName.MARGARET_TUNNEL.value:   Spelunky2LocationData(18, LocationName.VLADS_CASTLE),
    JournalName.COLIN_NORTHWARD.value:   Spelunky2LocationData(19, LocationName.VLADS_CASTLE),
    JournalName.ROFFY_D_SLOTH.value:     Spelunky2LocationData(20, LocationName.VLADS_CASTLE),

    JournalName.ALTO_SINGH.value:         Spelunky2LocationData(21, WorldName.DWELLING),
    JournalName.LIZ_MUTTON.value:         Spelunky2LocationData(22, WorldName.JUNGLE),
    JournalName.NEKKA_THE_EAGLE.value:    Spelunky2LocationData(23, LocationName.BLACK_MARKET),
    JournalName.LISE_PROJECT.value:       Spelunky2LocationData(24, WorldName.VOLCANA),
    JournalName.COCO_VON_DIAMONDS.value:  Spelunky2LocationData(25, LocationName.VLADS_CASTLE),
    JournalName.MANFRED_TUNNEL.value:     Spelunky2LocationData(26, WorldName.OLMECS_LAIR),
    JournalName.LITTLE_JAY.value:         Spelunky2LocationData(27, WorldName.TIDE_POOL),
    JournalName.TINA_FLAN.value:          Spelunky2LocationData(28, LocationName.ABZU),
    JournalName.VALERIE_CRUMP.value:      Spelunky2LocationData(29, WorldName.TEMPLE),
    JournalName.AU.value:                 Spelunky2LocationData(30, LocationName.CITY_OF_GOLD),
    JournalName.DEMI_VON_DIAMONDS.value:  Spelunky2LocationData(31, WorldName.ICE_CAVES),
    JournalName.PILOT.value:              Spelunky2LocationData(32, LocationName.MOTHERSHIP),
    JournalName.PRINCESS_AIRYN.value:     Spelunky2LocationData(33, WorldName.NEO_BABYLON),
    JournalName.DIRK_YAMAOKA.value:       Spelunky2LocationData(34, WorldName.SUNKEN_CITY, Spelunky2Goal.HARD),
    JournalName.GUY_SPELUNKY.value:       Spelunky2LocationData(35, WorldName.NEO_BABYLON, Spelunky2Goal.HARD),
    JournalName.CLASSIC_GUY.value:        Spelunky2LocationData(36, WorldName.SUNKEN_CITY, Spelunky2Goal.CO),
    JournalName.TERRA_TUNNEL.value:       Spelunky2LocationData(37, WORLD_2_STRING),
    JournalName.HIRED_HAND.value:         Spelunky2LocationData(38, WorldName.DWELLING),
    JournalName.EGGPLANT_CHILD.value:     Spelunky2LocationData(39, WorldName.ICE_CAVES),
    JournalName.SHOPKEEPER.value:         Spelunky2LocationData(40, WorldName.DWELLING),
    JournalName.TUN.value:                Spelunky2LocationData(41, WORLD_2_STRING),
    JournalName.YANG.value:               Spelunky2LocationData(42, WorldName.DWELLING),
    JournalName.MADAME_TUSK.value:        Spelunky2LocationData(43, WorldName.TIDE_POOL),
    JournalName.TUSK_BODYGUARD.value:     Spelunky2LocationData(44, WorldName.TIDE_POOL),
    JournalName.WADDLER.value:            Spelunky2LocationData(45, WorldName.OLMECS_LAIR),
    JournalName.CAVEMAN_SHOPKEEPER.value: Spelunky2LocationData(46, WorldName.TIDE_POOL),
    JournalName.GHIST_SHOPKEEPER.value:   Spelunky2LocationData(47, WorldName.DWELLING),
    JournalName.VAN_HORSING.value:        Spelunky2LocationData(48, WorldName.VOLCANA),
    JournalName.PARSLEY.value:            Spelunky2LocationData(49, WorldName.JUNGLE),
    JournalName.PARSNIP.value:            Spelunky2LocationData(50, WorldName.JUNGLE),
    JournalName.PARMESAN.value:           Spelunky2LocationData(51, WorldName.JUNGLE),
    JournalName.SPARROW.value:            Spelunky2LocationData(52, WORLD_2_STRING),
    JournalName.BEG.value:                Spelunky2LocationData(53, WORLD_2_STRING),
    JournalName.EGGPLANT_KING.value:      Spelunky2LocationData(54, WorldName.EGGPLANT, Spelunky2Goal.HARD),
}

bestiary_entries = {
    # Dwelling
    JournalName.SNAKE.value:         Spelunky2LocationData(55, WorldName.DWELLING),
    JournalName.SPIDER.value:        Spelunky2LocationData(56, WorldName.DWELLING),
    JournalName.BAT.value:           Spelunky2LocationData(57, WorldName.DWELLING),
    JournalName.CAVEMAN.value:       Spelunky2LocationData(58, WorldName.DWELLING),
    JournalName.SKELETON.value:      Spelunky2LocationData(59, WorldName.DWELLING),
    JournalName.HORNED_LIZARD.value: Spelunky2LocationData(60, WorldName.DWELLING),
    JournalName.CAVE_MOLE.value:     Spelunky2LocationData(61, WorldName.DWELLING),
    JournalName.QUILLBACK.value:     Spelunky2LocationData(62, WorldName.DWELLING),

    # Jungle
    JournalName.MANTRAP.value:       Spelunky2LocationData(63, WorldName.JUNGLE),
    JournalName.TIKI_MAN.value:      Spelunky2LocationData(64, WorldName.JUNGLE),
    JournalName.WITCH_DOCTOR.value:  Spelunky2LocationData(65, WorldName.JUNGLE),
    JournalName.MOSQUITO.value:      Spelunky2LocationData(66, WorldName.JUNGLE),
    JournalName.MONKEY.value:        Spelunky2LocationData(67, WorldName.JUNGLE),
    JournalName.HANG_SPIDER.value:   Spelunky2LocationData(68, WorldName.JUNGLE),
    JournalName.GIANT_SPIDER.value:  Spelunky2LocationData(69, WorldName.JUNGLE),

    # Volcana
    JournalName.MAGMAR.value:        Spelunky2LocationData(70, WorldName.VOLCANA),
    JournalName.ROBOT.value:         Spelunky2LocationData(71, WorldName.VOLCANA),
    JournalName.FIRE_BUG.value:      Spelunky2LocationData(72, WorldName.VOLCANA),
    JournalName.IMP.value:           Spelunky2LocationData(73, WorldName.VOLCANA),
    JournalName.LAVAMANDER.value:    Spelunky2LocationData(74, WorldName.VOLCANA),
    JournalName.VAMPIRE.value:       Spelunky2LocationData(75, LocationName.VLADS_CASTLE),
    JournalName.VLAD.value:          Spelunky2LocationData(76, LocationName.VLADS_CASTLE),

    # Olmec's Lair
    JournalName.OLMEC.value:         Spelunky2LocationData(77, WorldName.OLMECS_LAIR),

    # Tide Pool
    JournalName.JIANGSHI.value:           Spelunky2LocationData(78, WorldName.TIDE_POOL),
    JournalName.JIANGSHI_ASSASSIN.value:  Spelunky2LocationData(79, WorldName.TIDE_POOL),
    JournalName.FLYING_FISH.value:        Spelunky2LocationData(80, WorldName.TIDE_POOL),
    JournalName.OCTOPY.value:             Spelunky2LocationData(81, WorldName.TIDE_POOL),
    JournalName.HERMIT_CRAB.value:        Spelunky2LocationData(82, WorldName.TIDE_POOL),
    JournalName.PANGXIE.value:            Spelunky2LocationData(83, WorldName.TIDE_POOL),
    JournalName.GREAT_HUMPHEAD.value:     Spelunky2LocationData(84, WorldName.TIDE_POOL),
    JournalName.KINGU.value:              Spelunky2LocationData(85, LocationName.ABZU),

    # Temple
    JournalName.CROCMAN.value:       Spelunky2LocationData(86, WorldName.TEMPLE),
    JournalName.COBRA.value:         Spelunky2LocationData(87, WorldName.TEMPLE),
    JournalName.MUMMY.value:         Spelunky2LocationData(88, WorldName.TEMPLE),
    JournalName.SORCERESS.value:     Spelunky2LocationData(89, WorldName.TEMPLE),
    JournalName.CAT_MUMMY.value:     Spelunky2LocationData(90, WorldName.TEMPLE),
    JournalName.NECROMANCER.value:   Spelunky2LocationData(91, WorldName.TEMPLE),
    JournalName.ANUBIS.value:        Spelunky2LocationData(92, WorldName.TEMPLE),
    JournalName.AMMIT.value:         Spelunky2LocationData(93, LocationName.DUAT),
    JournalName.APEP.value:          Spelunky2LocationData(94, LocationName.DUAT),
    JournalName.ANUBIS_II.value:     Spelunky2LocationData(95, LocationName.DUAT),
    JournalName.OSIRIS.value:        Spelunky2LocationData(96, LocationName.DUAT),

    # Ice Caves
    JournalName.UFO.value:           Spelunky2LocationData(97, WorldName.ICE_CAVES),
    JournalName.ALIEN.value:         Spelunky2LocationData(98, WorldName.ICE_CAVES),
    JournalName.YETI.value:          Spelunky2LocationData(99, WorldName.ICE_CAVES),
    JournalName.YETI_KING.value:     Spelunky2LocationData(100, WorldName.ICE_CAVES),
    JournalName.YETI_QUEEN.value:    Spelunky2LocationData(101, WorldName.ICE_CAVES),
    JournalName.ALIEN_QUEEN_LAMAHU.value: Spelunky2LocationData(102, LocationName.MOTHERSHIP),
    JournalName.PROTO_SHOPKEEPER.value:   Spelunky2LocationData(103, LocationName.MOTHERSHIP),

    # Neo Babylon
    JournalName.OLMITE.value:        Spelunky2LocationData(104, WorldName.NEO_BABYLON),
    JournalName.LAMASSU.value:       Spelunky2LocationData(105, WorldName.NEO_BABYLON),
    JournalName.TIAMAT.value:        Spelunky2LocationData(106, WorldName.NEO_BABYLON, Spelunky2Goal.HARD),

    # Sunken City
    JournalName.TADPOLE.value:       Spelunky2LocationData(107, WorldName.SUNKEN_CITY, Spelunky2Goal.HARD),
    JournalName.FROG.value:          Spelunky2LocationData(108, WorldName.SUNKEN_CITY, Spelunky2Goal.HARD),
    JournalName.FIRE_FROG.value:     Spelunky2LocationData(109, WorldName.SUNKEN_CITY, Spelunky2Goal.HARD),
    JournalName.GOLIATH_FROG.value:  Spelunky2LocationData(110, WorldName.SUNKEN_CITY, Spelunky2Goal.HARD),
    JournalName.GRUB.value:          Spelunky2LocationData(111, WorldName.SUNKEN_CITY, Spelunky2Goal.HARD),
    JournalName.GIANT_FLY.value:     Spelunky2LocationData(112, WorldName.SUNKEN_CITY, Spelunky2Goal.HARD),
    JournalName.HUNDUN.value:        Spelunky2LocationData(113, WorldName.SUNKEN_CITY, Spelunky2Goal.HARD),
    JournalName.EGGPLANT_MINISTER.value: Spelunky2LocationData(114, WorldName.EGGPLANT, Spelunky2Goal.HARD),
    JournalName.EGGPLUP.value:       Spelunky2LocationData(115, WorldName.EGGPLANT, Spelunky2Goal.HARD),

    # Cosmic Ocean
    JournalName.CELESTIAL_JELLY.value: Spelunky2LocationData(116, WorldName.COSMIC_OCEAN, Spelunky2Goal.CO),

    # Miscellaneous
    JournalName.SCORPION.value:      Spelunky2LocationData(117, WORLD_2_STRING),
    JournalName.BEE.value:           Spelunky2LocationData(118, WorldName.JUNGLE),
    JournalName.QUEEN_BEE.value:     Spelunky2LocationData(119, WorldName.JUNGLE),
    JournalName.SCARAB.value:        Spelunky2LocationData(120, WorldName.DWELLING),
    JournalName.GOLDEN_MONKEY.value: Spelunky2LocationData(121, WORLD_2_STRING),
    JournalName.LEPRECHAUN.value:    Spelunky2LocationData(122, WORLD_2_STRING),
    JournalName.MONTY.value:         Spelunky2LocationData(123, WorldName.DWELLING),
    JournalName.PERCY.value:         Spelunky2LocationData(124, WorldName.DWELLING),
    JournalName.POOCHI.value:        Spelunky2LocationData(125, WorldName.DWELLING),
    JournalName.GHIST.value:         Spelunky2LocationData(126, WorldName.TIDE_POOL),
    JournalName.GHOST.value:         Spelunky2LocationData(127, WorldName.DWELLING),
    JournalName.CAVE_TURKEY.value:   Spelunky2LocationData(128, WorldName.DWELLING),
    JournalName.ROCK_DOG.value:      Spelunky2LocationData(129, WorldName.VOLCANA),
    JournalName.AXOLOTL.value:       Spelunky2LocationData(130, WorldName.TIDE_POOL),
    JournalName.QILIN.value:         Spelunky2LocationData(131, WorldName.NEO_BABYLON),
    JournalName.MECH_RIDER.value:    Spelunky2LocationData(132, WorldName.ICE_CAVES),
}

item_entries = {
    JournalName.ROPE_PILE.value:         Spelunky2LocationData(133, WorldName.DWELLING),
    JournalName.BOMB_BAG.value:          Spelunky2LocationData(134, WorldName.DWELLING),
    JournalName.BOMB_BOX.value:          Spelunky2LocationData(135, WorldName.DWELLING),
    JournalName.PASTE.value:             Spelunky2LocationData(136, WorldName.JUNGLE),
    JournalName.SPECTACLES.value:        Spelunky2LocationData(137, LocationName.BLACK_MARKET),
    JournalName.CLIMBING_GLOVES.value:   Spelunky2LocationData(138, LocationName.BLACK_MARKET),
    JournalName.PITCHERS_MITT.value:     Spelunky2LocationData(139, LocationName.BLACK_MARKET),
    JournalName.SPRING_SHOES.value:      Spelunky2LocationData(140, LocationName.BLACK_MARKET),
    JournalName.SPIKE_SHOES.value:       Spelunky2LocationData(141, WorldName.ICE_CAVES),
    JournalName.COMPASS.value:           Spelunky2LocationData(142, WorldName.ICE_CAVES),
    JournalName.ALIEN_COMPASS.value:     Spelunky2LocationData(143, LocationName.VLADS_CASTLE),
    JournalName.PARACHUTE.value:         Spelunky2LocationData(144, WorldName.OLMECS_LAIR),
    JournalName.UDJAT_EYE.value:         Spelunky2LocationData(145, WorldName.DWELLING),
    JournalName.KAPALA.value:            Spelunky2LocationData(146, WorldName.NEO_BABYLON),
    JournalName.HEDJET.value:            Spelunky2LocationData(147, LocationName.BLACK_MARKET),
    JournalName.CROWN.value:             Spelunky2LocationData(148, LocationName.VLADS_CASTLE),
    JournalName.EGGPLANT_CROWN.value:    Spelunky2LocationData(149, WorldName.EGGPLANT, Spelunky2Goal.HARD),
    JournalName.TRUE_CROWN.value:        Spelunky2LocationData(150, WorldName.ICE_CAVES),
    JournalName.ANKH.value:              Spelunky2LocationData(151, WorldName.OLMECS_LAIR),
    JournalName.TABLET_OF_DESTINY.value: Spelunky2LocationData(152, MAIN_MENU_STRING),
    JournalName.SKELETON_KEY.value:      Spelunky2LocationData(153, WORLD_2_STRING),
    JournalName.ROYAL_JELLY.value:       Spelunky2LocationData(154, WorldName.JUNGLE),
    JournalName.CAPE.value:              Spelunky2LocationData(155, LocationName.VLADS_CASTLE),
    JournalName.VLADS_CAPE.value:        Spelunky2LocationData(156, LocationName.VLADS_CASTLE),
    JournalName.JETPACK.value:           Spelunky2LocationData(157, LocationName.DUAT),
    JournalName.TELEPACK.value:          Spelunky2LocationData(158, LocationName.BLACK_MARKET),
    JournalName.HOVERPACK.value:         Spelunky2LocationData(159, LocationName.BLACK_MARKET),
    JournalName.POWERPACK.value:         Spelunky2LocationData(160, LocationName.BLACK_MARKET),
    JournalName.WEBGUN.value:            Spelunky2LocationData(161, LocationName.BLACK_MARKET),

    JournalName.SHOTGUN.value:           Spelunky2LocationData(162, WorldName.DWELLING),

    JournalName.FREEZE_RAY.value:        Spelunky2LocationData(163, LocationName.BLACK_MARKET),
    JournalName.CLONE_GUN.value:         Spelunky2LocationData(164, WorldName.TIDE_POOL),
    JournalName.CROSSBOW.value:          Spelunky2LocationData(165, WorldName.DWELLING),
    JournalName.CAMERA.value:            Spelunky2LocationData(166, WorldName.TIDE_POOL),
    JournalName.TELEPORTER.value:        Spelunky2LocationData(167, LocationName.BLACK_MARKET),
    JournalName.MATTOCK.value:           Spelunky2LocationData(168, WORLD_2_STRING),
    JournalName.BOOMERANG.value:         Spelunky2LocationData(169, WorldName.JUNGLE),
    JournalName.MACHETE.value:           Spelunky2LocationData(170, LocationName.BLACK_MARKET),
    JournalName.EXCALIBUR.value:         Spelunky2LocationData(171, WorldName.TIDE_POOL),
    JournalName.BROKEN_SWORD.value:      Spelunky2LocationData(172, WorldName.TIDE_POOL),
    JournalName.PLASMA_CANNON.value:     Spelunky2LocationData(173, LocationName.MOTHERSHIP),
    JournalName.SCEPTER.value:           Spelunky2LocationData(174, WorldName.TEMPLE),
    JournalName.HOU_YI_BOW.value:        Spelunky2LocationData(175, WORLD_2_STRING),
    JournalName.ARROW_OF_LIGHT.value:    Spelunky2LocationData(176, WorldName.SUNKEN_CITY, Spelunky2Goal.HARD),
    JournalName.WOODEN_SHIELD.value:     Spelunky2LocationData(177, WorldName.JUNGLE),
    JournalName.METAL_SHIELD.value:      Spelunky2LocationData(178, WorldName.TIDE_POOL),
    JournalName.IDOL.value:              Spelunky2LocationData(179, WorldName.DWELLING),
    JournalName.THE_TUSK_IDOL.value:     Spelunky2LocationData(180, WorldName.TIDE_POOL),
    JournalName.CURSE_POT.value:         Spelunky2LocationData(181, WorldName.DWELLING),
    JournalName.USHABTI.value:           Spelunky2LocationData(182, WorldName.NEO_BABYLON),
    JournalName.EGGPLANT.value:          Spelunky2LocationData(183, WorldName.TIDE_POOL),
    JournalName.COOKED_TURKEY.value:     Spelunky2LocationData(184, WorldName.DWELLING),
    JournalName.ELIXIR.value:            Spelunky2LocationData(185, WorldName.TEMPLE),
    JournalName.FOUR_LEAF_CLOVER.value:  Spelunky2LocationData(186, WORLD_2_STRING),
}

trap_entries = {
    JournalName.SPIKES.value:            Spelunky2LocationData(187, WorldName.DWELLING),
    JournalName.ARROW_TRAP.value:        Spelunky2LocationData(188, WorldName.DWELLING),
    JournalName.TOTEM_TRAP.value:        Spelunky2LocationData(189, WorldName.DWELLING),
    JournalName.LOG_TRAP.value:          Spelunky2LocationData(190, WorldName.DWELLING),
    JournalName.SPEAR_TRAP.value:        Spelunky2LocationData(191, WorldName.JUNGLE),
    JournalName.THORNY_VINE.value:       Spelunky2LocationData(192, WorldName.JUNGLE),
    JournalName.BEAR_TRAP.value:         Spelunky2LocationData(193, WorldName.JUNGLE),
    JournalName.POWDER_BOX.value:        Spelunky2LocationData(194, WorldName.VOLCANA),
    JournalName.FALLING_PLATFORM.value:  Spelunky2LocationData(195, WorldName.VOLCANA),
    JournalName.SPIKEBALL.value:         Spelunky2LocationData(196, WorldName.VOLCANA),
    JournalName.LION_TRAP.value:         Spelunky2LocationData(197, WorldName.TIDE_POOL),
    JournalName.GIANT_CLAM.value:        Spelunky2LocationData(198, WorldName.TIDE_POOL),
    JournalName.SLIDING_WALL.value:      Spelunky2LocationData(199, WorldName.TIDE_POOL),
    JournalName.CRUSH_TRAP.value:        Spelunky2LocationData(200, WorldName.TEMPLE),
    JournalName.GIANT_CRUSH_TRAP.value:  Spelunky2LocationData(201, WorldName.TEMPLE),
    JournalName.BOULDER.value:           Spelunky2LocationData(202, WorldName.ICE_CAVES),
    JournalName.SPRING_TRAP.value:       Spelunky2LocationData(203, WorldName.ICE_CAVES),
    JournalName.LANDMINE.value:          Spelunky2LocationData(204, WorldName.ICE_CAVES),
    JournalName.LASER_TRAP.value:        Spelunky2LocationData(205, WorldName.NEO_BABYLON),
    JournalName.SPARK_TRAP.value:        Spelunky2LocationData(206, WorldName.NEO_BABYLON),
    JournalName.FROG_TRAP.value:         Spelunky2LocationData(207, WorldName.SUNKEN_CITY, Spelunky2Goal.HARD),
    JournalName.STICKY_TRAP.value:       Spelunky2LocationData(208, WorldName.SUNKEN_CITY, Spelunky2Goal.HARD),
    JournalName.BONE_DROP.value:         Spelunky2LocationData(209, WorldName.SUNKEN_CITY, Spelunky2Goal.HARD),
    JournalName.EGG_SAC.value:           Spelunky2LocationData(210, WorldName.SUNKEN_CITY, Spelunky2Goal.HARD),
}

location_data_table = {

    **place_entries,
    **people_entries,
    **bestiary_entries,
    **item_entries,
    **trap_entries,
}
