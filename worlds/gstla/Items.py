from typing import List, NamedTuple, Dict, Optional
from enum import Enum, IntEnum
from BaseClasses import Item, ItemClassification
from .Names.ItemName import ItemName

class ElementType(IntEnum):
   Earth = 0
   Water = 1
   Fire = 2
   Air = 3

class ItemType(str, Enum):
   KeyItem = "key"
   Class = "class"
   Consumable = "consumables"
   Trade = "trade"
   Forgeable = "forgeable"
   Weapon = "weapon"
   Armor = "armor"
   Helm = "helm"
   Shield = "shield"
   Psyenergy = "psyenergy"
   PsyenergyItem = "psyenergy_item"
   Shirt = "shirt"
   Boots = "boots"
   Ring = "ring"
   Djinn = "djinn"
   Event = "event"



class ItemData(NamedTuple):
   ap_id: Optional[int]
   itemName: str
   progression: ItemClassification
   addr: int
   type: ItemType
   gstla_id: int
   event_type: int = 131

class DjinItemData(ItemData):
    element: int
    stats_addr: int
    stats: List[int]

    def __new__(cls, ap_id, itemName, progression, addr, gstla_id, element, stats_addr, stats):
        self = super(ItemData, cls).__new__(cls, (ap_id, itemName, progression, addr, ItemType.Djinn, gstla_id, 1))
        self.element = element
        self.stats_addr = stats_addr
        self.stats = stats
        return self

class GSTLAItem(Item):
    game: str = "Golden Sun The Lost Age"

# key_item_list: List[ItemData] = [
#    # Golden Sun 1 Items
#    # ItemData(6, ItemName.Hermes_Water, ItemClassification.filler, 738052, 0),
#    # ItemData(7, ItemName.Empty_Bottle, ItemClassification.filler, 738096, 0),
#    # ItemData(19, ItemName.Small_Jewel, ItemClassification.filler, 739856, 0),
#    # ItemData(24, ItemName.Dragons_Eye, ItemClassification.filler, 740076, 0),
#    # ItemData(25, ItemName.Bone, ItemClassification.filler, 740120, 1),
#    # ItemData(26, ItemName.Anchor_Charm, ItemClassification.filler, 740164, 0),
#    # ItemData(28, ItemName.Cell_Key, ItemClassification.filler, 740252, 0),
#    # ItemData(29, ItemName.Boat_Ticket, ItemClassification.filler, 740296, 0),
#    # ItemData(31, ItemName.Mystic_Draught, ItemClassification.filler, 740384, 0),
#
#    # Briggs item
#    # ItemData(53, ItemName.Signal_Whistle, ItemClassification.filler, 749756, 0),
#
#    ItemData(23, ItemName.Lucky_Medal, ItemClassification.filler, 740032, ItemType.KeyItem, 19),
#
#    ItemData(36, ItemName.Black_Crystal, ItemClassification.filler, 740604, ItemType.KeyItem, 1),
#    ItemData(37, ItemName.Red_Key, ItemClassification.filler, 740648, ItemType.KeyItem, 1),
#    ItemData(38, ItemName.Blue_Key, ItemClassification.filler, 740692, ItemType.KeyItem, 1),
#    ItemData(48, ItemName.Right_Prong, ItemClassification.filler, 749272, ItemType.KeyItem, 1),
#    ItemData(49, ItemName.Left_Prong, ItemClassification.filler, 749316, ItemType.KeyItem, 1),
#    ItemData(50, ItemName.Center_Prong, ItemClassification.filler, 749360, ItemType.KeyItem, 1),
#    ItemData(51, ItemName.Healing_Fungus, ItemClassification.filler, 749668, ItemType.KeyItem, 1),
#    ItemData(52, ItemName.Laughing_Fungus, ItemClassification.filler, 749712, ItemType.KeyItem, 1),
#    ItemData(54, ItemName.Dancing_Idol, ItemClassification.filler, 749800, ItemType.KeyItem, 1),
#    ItemData(59, ItemName.Aquarius_Stone, ItemClassification.filler, 750020, ItemType.KeyItem, 1),
#    ItemData(60, ItemName.Large_Bread, ItemClassification.filler, 750064, ItemType.KeyItem, 1),
#    ItemData(61, ItemName.Sea_Gods_Tear, ItemClassification.filler, 750108, ItemType.KeyItem, 1),
#    ItemData(62, ItemName.Ruin_Key, ItemClassification.filler, 750152, ItemType.KeyItem, 1),
#    ItemData(63, ItemName.Magma_Ball, ItemClassification.filler, 750196, ItemType.KeyItem, 1)
# ]
#
# consumables_list: List[ItemData] = [
#    ItemData(1, ItemName.Empty, ItemClassification.filler, 729956, ItemType.Consumable, 17),
#    ItemData(2, ItemName.Herb, ItemClassification.filler, 737876, ItemType.Consumable, 3),
#    ItemData(3, ItemName.Nut, ItemClassification.filler, 737920, ItemType.Consumable, 8),
#    ItemData(4, ItemName.Vial, ItemClassification.filler, 737964, ItemType.Consumable, 8),
#    ItemData(5, ItemName.Potion, ItemClassification.filler, 738008, ItemType.Consumable, 5),
#    ItemData(8, ItemName.Psy_Crystal, ItemClassification.filler, 738140, ItemType.Consumable, 7),
#    ItemData(9, ItemName.Antidote, ItemClassification.filler, 738184, ItemType.Consumable, 6),
#    ItemData(10, ItemName.Elixir, ItemClassification.filler, 738228, ItemType.Consumable, 15),
#    ItemData(11, ItemName.Water_of_Life, ItemClassification.filler, 738272, ItemType.Consumable, 4),
#    ItemData(12, ItemName.Mist_Potion, ItemClassification.filler, 738316, ItemType.Consumable, 4),
#    ItemData(13, ItemName.Power_Bread, ItemClassification.filler, 738360, ItemType.Consumable, 4),
#    ItemData(14, ItemName.Cookie, ItemClassification.filler, 738404, ItemType.Consumable, 4),
#    ItemData(15, ItemName.Apple, ItemClassification.filler, 738448, ItemType.Consumable, 4),
#    ItemData(16, ItemName.Hard_Nut, ItemClassification.filler, 738492, ItemType.Consumable, 4),
#    ItemData(17, ItemName.Mint, ItemClassification.filler, 738536, ItemType.Consumable, 5),
#    ItemData(18, ItemName.Lucky_Pepper, ItemClassification.filler, 738580, ItemType.Consumable, 4),
#    ItemData(20, ItemName.Smoke_Bomb, ItemClassification.filler, 739900, ItemType.Consumable, 8),
#    ItemData(21, ItemName.Sleep_Bomb, ItemClassification.filler, 739944, ItemType.Consumable, 8),
#    ItemData(22, ItemName.Game_Ticket, ItemClassification.filler, 739988, ItemType.Consumable, 0),
#    ItemData(27, ItemName.Corn, ItemClassification.filler, 740208, ItemType.Consumable, 1),
#    ItemData(30, ItemName.Sacred_Feather, ItemClassification.filler, 740340, ItemType.Consumable, 1),
#    ItemData(32, ItemName.Oil_Drop, ItemClassification.filler, 740428, ItemType.Consumable, 4),
#    ItemData(33, ItemName.Weasels_Claw, ItemClassification.filler, 740472, ItemType.Consumable, 1),
#    ItemData(34, ItemName.Bramble_Seed, ItemClassification.filler, 740516, ItemType.Consumable, 3),
#    ItemData(35, ItemName.Crystal_Powder, ItemClassification.filler, 740560, ItemType.Consumable, 4)
# ]
#
# trading_items: List[ItemData] = [
#    ItemData(55, ItemName.Pretty_Stone, ItemClassification.filler, 749844, ItemType.Trade, 1),
#    ItemData(56, ItemName.Red_Cloth, ItemClassification.filler, 749888, ItemType.Trade, 1),
#    ItemData(57, ItemName.Milk, ItemClassification.filler, 749932, ItemType.Trade, 1),
#    ItemData(58, ItemName.Lil_Turtle, ItemClassification.filler, 749976, ItemType.Trade, 1)
# ]
#
# forgeables: List[ItemData] = [
#    ItemData(39, ItemName.Tear_Stone, ItemClassification.filler, 748832, ItemType.Forgeable, 4),
#    ItemData(40, ItemName.Star_Dust, ItemClassification.filler, 748876, ItemType.Forgeable, 4),
#    ItemData(41, ItemName.Sylph_Feather, ItemClassification.filler, 748920, ItemType.Forgeable, 3),
#    ItemData(42, ItemName.Dragon_Skin, ItemClassification.filler, 748964, ItemType.Forgeable, 2),
#    ItemData(43, ItemName.Salamander_Tail, ItemClassification.filler, 749008, ItemType.Forgeable, 2),
#    ItemData(44, ItemName.Golem_Core, ItemClassification.filler, 749052, ItemType.Forgeable, 3),
#    ItemData(45, ItemName.Mythril_Silver, ItemClassification.filler, 749096, ItemType.Forgeable, 2),
#    ItemData(46, ItemName.Dark_Matter, ItemClassification.filler, 749140, ItemType.Forgeable, 3),
#    ItemData(47, ItemName.Orihalcon, ItemClassification.filler, 749184, ItemType.Forgeable, 3),
#    ItemData(164, ItemName.Rusty_Sword, ItemClassification.filler, 748304, ItemType.Forgeable, 1),
#    ItemData(165, ItemName.Rusty_Sword, ItemClassification.filler, 748348, ItemType.Forgeable, 1),
#    ItemData(166, ItemName.Rusty_Sword, ItemClassification.filler, 748392, ItemType.Forgeable, 1),
#    ItemData(167, ItemName.Rusty_Sword, ItemClassification.filler, 748436, ItemType.Forgeable, 1),
#    ItemData(168, ItemName.Rusty_Axe, ItemClassification.filler, 748480, ItemType.Forgeable, 1),
#    ItemData(169, ItemName.Rusty_Axe, ItemClassification.filler, 748524, ItemType.Forgeable, 1),
#    ItemData(170, ItemName.Rusty_Mace, ItemClassification.filler, 748568, ItemType.Forgeable, 1),
#    ItemData(171, ItemName.Rusty_Mace, ItemClassification.filler, 748612, ItemType.Forgeable, 1),
#    ItemData(172, ItemName.Rusty_Staff, ItemClassification.filler, 748656, ItemType.Forgeable, 1),
#    ItemData(173, ItemName.Rusty_Staff, ItemClassification.filler, 748700, ItemType.Forgeable, 1),
#    ItemData(174, ItemName.Rusty_Staff, ItemClassification.filler, 748744, ItemType.Forgeable, 1)
# ]
#
# weapon_list: List[ItemData] = [
#    ItemData(64, ItemName.Long_Sword, ItemClassification.filler, 730000, ItemType.Weapon, 1),
#    ItemData(65, ItemName.Broad_Sword, ItemClassification.filler, 730044, ItemType.Weapon, 1),
#    ItemData(66, ItemName.Claymore, ItemClassification.filler, 730088, ItemType.Weapon, 1),
#    ItemData(67, ItemName.Great_Sword, ItemClassification.filler, 730132, ItemType.Weapon, 1),
#    ItemData(68, ItemName.Shamshir, ItemClassification.filler, 730176, ItemType.Weapon, 1),
#    ItemData(69, ItemName.Silver_Blade, ItemClassification.filler, 730220, ItemType.Weapon, 1),
#    ItemData(70, ItemName.Fire_Brand, ItemClassification.filler, 730264, ItemType.Weapon, 2),
#    ItemData(71, ItemName.Arctic_Blade, ItemClassification.filler, 730308, ItemType.Weapon, 1),
#    ItemData(72, ItemName.Gaia_Blade, ItemClassification.filler, 730352, ItemType.Weapon, 0),
#    ItemData(73, ItemName.Sol_Blade, ItemClassification.filler, 730396, ItemType.Weapon, 1),
#    ItemData(74, ItemName.Muramasa, ItemClassification.filler, 730440, ItemType.Weapon, 0),
#    ItemData(75, ItemName.Machete, ItemClassification.filler, 730616, ItemType.Weapon, 0),
#    ItemData(76, ItemName.Short_Sword, ItemClassification.filler, 730660, ItemType.Weapon, 0),
#    ItemData(77, ItemName.Hunters_Sword, ItemClassification.filler, 730704, ItemType.Weapon, 0),
#    ItemData(78, ItemName.Battle_Rapier, ItemClassification.filler, 730748, ItemType.Weapon, 0),
#    ItemData(79, ItemName.Master_Rapier, ItemClassification.filler, 730792, ItemType.Weapon, 0),
#    ItemData(80, ItemName.Ninja_Blade, ItemClassification.filler, 730836, ItemType.Weapon, 0),
#    ItemData(81, ItemName.Swift_Sword, ItemClassification.filler, 730880, ItemType.Weapon, 0),
#    ItemData(82, ItemName.Elven_Rapier, ItemClassification.filler, 730924, ItemType.Weapon, 0),
#    ItemData(83, ItemName.Assassin_Blade, ItemClassification.filler, 730968, ItemType.Weapon, 0),
#    ItemData(84, ItemName.Mystery_Blade, ItemClassification.filler, 731012, ItemType.Weapon, 0),
#    ItemData(85, ItemName.Kikuichimonji, ItemClassification.filler, 731056, ItemType.Weapon, 0),
#    ItemData(86, ItemName.Masamune, ItemClassification.filler, 731100, ItemType.Weapon, 1),
#    ItemData(87, ItemName.Bandits_Sword, ItemClassification.filler, 731144, ItemType.Weapon, 0),
#    ItemData(88, ItemName.Battle_Axe, ItemClassification.filler, 731320, ItemType.Weapon, 0),
#    ItemData(89, ItemName.Broad_Axe, ItemClassification.filler, 731364, ItemType.Weapon, 0),
#    ItemData(90, ItemName.Great_Axe, ItemClassification.filler, 731408, ItemType.Weapon, 0),
#    ItemData(91, ItemName.Dragon_Axe, ItemClassification.filler, 731452, ItemType.Weapon, 0),
#    ItemData(92, ItemName.Giant_Axe, ItemClassification.filler, 731496, ItemType.Weapon, 0),
#    ItemData(93, ItemName.Vulcan_Axe, ItemClassification.filler, 731540, ItemType.Weapon, 0),
#    ItemData(94, ItemName.Burning_Axe, ItemClassification.filler, 731584, ItemType.Weapon, 0),
#    ItemData(95, ItemName.Demon_Axe, ItemClassification.filler, 731628, ItemType.Weapon, 0),
#    ItemData(96, ItemName.Mace, ItemClassification.filler, 731848, ItemType.Weapon, 0),
#    ItemData(97, ItemName.Heavy_Mace, ItemClassification.filler, 731892, ItemType.Weapon, 0),
#    ItemData(98, ItemName.Battle_Mace, ItemClassification.filler, 731936, ItemType.Weapon, 0),
#    ItemData(99, ItemName.War_Mace, ItemClassification.filler, 731980, ItemType.Weapon, 0),
#    ItemData(100, ItemName.Righteous_Mace, ItemClassification.filler, 732024, ItemType.Weapon, 0),
#    ItemData(101, ItemName.Grievous_Mace, ItemClassification.filler, 732068, ItemType.Weapon, 0),
#    ItemData(102, ItemName.Blessed_Mace, ItemClassification.filler, 732112, ItemType.Weapon, 0),
#    ItemData(103, ItemName.Wicked_Mace, ItemClassification.filler, 732156, ItemType.Weapon, 0),
#    ItemData(104, ItemName.Wooden_Stick, ItemClassification.filler, 732376, ItemType.Weapon, 0),
#    ItemData(105, ItemName.Magic_Rod, ItemClassification.filler, 732420, ItemType.Weapon, 0),
#    ItemData(106, ItemName.Witchs_Wand, ItemClassification.filler, 732464, ItemType.Weapon, 0),
#    ItemData(107, ItemName.Blessed_Ankh, ItemClassification.filler, 732508, ItemType.Weapon, 0),
#    ItemData(108, ItemName.Psynergy_Rod, ItemClassification.filler, 732552, ItemType.Weapon, 0),
#    ItemData(109, ItemName.Frost_Wand, ItemClassification.filler, 732596, ItemType.Weapon, 0),
#    ItemData(110, ItemName.Angelic_Ankh, ItemClassification.filler, 732640, ItemType.Weapon, 0),
#    ItemData(111, ItemName.Demonic_Staff, ItemClassification.filler, 732684, ItemType.Weapon, 0),
#    ItemData(112, ItemName.Crystal_Rod, ItemClassification.filler, 732728, ItemType.Weapon, 0),
#    ItemData(113, ItemName.Zodiac_Wand, ItemClassification.filler, 732772, ItemType.Weapon, 0),
#    ItemData(114, ItemName.Shamans_Rod, ItemClassification.filler, 732816, ItemType.Weapon, 1),
#    ItemData(115, ItemName.Huge_Sword, ItemClassification.filler, 741924, ItemType.Weapon, 0),
#    ItemData(116, ItemName.Mythril_Blade, ItemClassification.filler, 741968, ItemType.Weapon, 0),
#    ItemData(117, ItemName.Levatine, ItemClassification.filler, 742012, ItemType.Weapon, 0),
#    ItemData(118, ItemName.Darksword, ItemClassification.filler, 742056, ItemType.Weapon, 0),
#    ItemData(119, ItemName.Excalibur, ItemClassification.filler, 742100, ItemType.Weapon, 0),
#    ItemData(120, ItemName.Robbers_Blade, ItemClassification.filler, 742144, ItemType.Weapon, 0),
#    ItemData(121, ItemName.Soul_Brand, ItemClassification.filler, 742188, ItemType.Weapon, 0),
#    ItemData(122, ItemName.Storm_Brand, ItemClassification.filler, 742232, ItemType.Weapon, 1),
#    ItemData(123, ItemName.Hestia_Blade, ItemClassification.filler, 742276, ItemType.Weapon, 0),
#    ItemData(124, ItemName.Lightning_Sword, ItemClassification.filler, 742320, ItemType.Weapon, 1),
#    ItemData(125, ItemName.Rune_Blade, ItemClassification.filler, 742364, ItemType.Weapon, 0),
#    ItemData(126, ItemName.Cloud_Brand, ItemClassification.filler, 742408, ItemType.Weapon, 1),
#    ItemData(127, ItemName.Sylph_Rapier, ItemClassification.filler, 742496, ItemType.Weapon, 0),
#    ItemData(128, ItemName.Burning_Sword, ItemClassification.filler, 742540, ItemType.Weapon, 0),
#    ItemData(129, ItemName.Pirates_Sword, ItemClassification.filler, 742584, ItemType.Weapon, 1),
#    ItemData(130, ItemName.Corsairs_Edge, ItemClassification.filler, 742628, ItemType.Weapon, 0),
#    ItemData(131, ItemName.Pirates_Sabre, ItemClassification.filler, 742672, ItemType.Weapon, 0),
#    ItemData(132, ItemName.Hypnos_Sword, ItemClassification.filler, 742716, ItemType.Weapon, 1),
#    ItemData(133, ItemName.Mist_Sabre, ItemClassification.filler, 742760, ItemType.Weapon, 1),
#    ItemData(134, ItemName.Phaetons_Blade, ItemClassification.filler, 742804, ItemType.Weapon, 1),
#    ItemData(135, ItemName.Tisiphone_Edge, ItemClassification.filler, 742848, ItemType.Weapon, 0),
#    ItemData(136, ItemName.Apollos_Axe, ItemClassification.filler, 742936, ItemType.Weapon, 0),
#    ItemData(137, ItemName.Gaias_Axe, ItemClassification.filler, 742980, ItemType.Weapon, 0),
#    ItemData(138, ItemName.Stellar_Axe, ItemClassification.filler, 743024, ItemType.Weapon, 0),
#    ItemData(139, ItemName.Captains_Axe, ItemClassification.filler, 743068, ItemType.Weapon, 0),
#    ItemData(140, ItemName.Viking_Axe, ItemClassification.filler, 743112, ItemType.Weapon, 0),
#    ItemData(141, ItemName.Disk_Axe, ItemClassification.filler, 743156, ItemType.Weapon, 1),
#    ItemData(142, ItemName.Themis_Axe, ItemClassification.filler, 743200, ItemType.Weapon, 1),
#    ItemData(143, ItemName.Mighty_Axe, ItemClassification.filler, 743244, ItemType.Weapon, 0),
#    ItemData(144, ItemName.Tartarus_Axe, ItemClassification.filler, 743288, ItemType.Weapon, 0),
#    ItemData(145, ItemName.Comet_Mace, ItemClassification.filler, 743376, ItemType.Weapon, 0),
#    ItemData(146, ItemName.Tungsten_Mace, ItemClassification.filler, 743420, ItemType.Weapon, 0),
#    ItemData(147, ItemName.Demon_Mace, ItemClassification.filler, 743464, ItemType.Weapon, 0),
#    ItemData(148, ItemName.Hagbone_Mace, ItemClassification.filler, 743508, ItemType.Weapon, 0),
#    ItemData(149, ItemName.Blow_Mace, ItemClassification.filler, 743552, ItemType.Weapon, 1),
#    ItemData(150, ItemName.Rising_Mace, ItemClassification.filler, 743596, ItemType.Weapon, 0),
#    ItemData(151, ItemName.Thanatos_Mace, ItemClassification.filler, 743640, ItemType.Weapon, 1),
#    ItemData(152, ItemName.Cloud_Wand, ItemClassification.filler, 743728, ItemType.Weapon, 0),
#    ItemData(153, ItemName.Salamander_Rod, ItemClassification.filler, 743772, ItemType.Weapon, 0),
#    ItemData(154, ItemName.Nebula_Wand, ItemClassification.filler, 743816, ItemType.Weapon, 0),
#    ItemData(155, ItemName.Dracomace, ItemClassification.filler, 743860, ItemType.Weapon, 0),
#    ItemData(156, ItemName.Glower_Staff, ItemClassification.filler, 743904, ItemType.Weapon, 0),
#    ItemData(157, ItemName.Goblins_Rod, ItemClassification.filler, 743948, ItemType.Weapon, 0),
#    ItemData(158, ItemName.Meditation_Rod, ItemClassification.filler, 743992, ItemType.Weapon, 1),
#    ItemData(159, ItemName.Firemans_Pole, ItemClassification.filler, 744036, ItemType.Weapon, 0),
#    ItemData(160, ItemName.Atropos_Rod, ItemClassification.filler, 744080, ItemType.Weapon, 0),
#    ItemData(161, ItemName.Lachesis_Rule, ItemClassification.filler, 744124, ItemType.Weapon, 0),
#    ItemData(162, ItemName.Clothos_Distaff, ItemClassification.filler, 744168, ItemType.Weapon, 0),
#    ItemData(163, ItemName.Staff_of_Anubis, ItemClassification.filler, 744212, ItemType.Weapon, 0)
# ]
#
# armor_list: List[ItemData] = [
#    ItemData(175, ItemName.Leather_Armor, ItemClassification.filler, 733256, ItemType.Armor, 0),
#    ItemData(176, ItemName.Psynergy_Armor, ItemClassification.filler, 733300, ItemType.Armor, 0),
#    ItemData(177, ItemName.Chain_Mail, ItemClassification.filler, 733344, ItemType.Armor, 0),
#    ItemData(178, ItemName.Armored_Shell, ItemClassification.filler, 733388, ItemType.Armor, 0),
#    ItemData(179, ItemName.Plate_Mail, ItemClassification.filler, 733432, ItemType.Armor, 0),
#    ItemData(180, ItemName.Steel_Armor, ItemClassification.filler, 733476, ItemType.Armor, 0),
#    ItemData(181, ItemName.Spirit_Armor, ItemClassification.filler, 733520, ItemType.Armor, 0),
#    ItemData(182, ItemName.Dragon_Scales, ItemClassification.filler, 733564, ItemType.Armor, 0),
#    ItemData(183, ItemName.Demon_Mail, ItemClassification.filler, 733608, ItemType.Armor, 0),
#    ItemData(184, ItemName.Asuras_Armor, ItemClassification.filler, 733652, ItemType.Armor, 0),
#    ItemData(185, ItemName.Spiked_Armor, ItemClassification.filler, 733696, ItemType.Armor, 0),
#    ItemData(186, ItemName.Cotton_Shirt, ItemClassification.filler, 733872, ItemType.Armor, 0),
#    ItemData(187, ItemName.Travel_Vest, ItemClassification.filler, 733916, ItemType.Armor, 0),
#    ItemData(188, ItemName.Fur_Coat, ItemClassification.filler, 733960, ItemType.Armor, 0),
#    ItemData(189, ItemName.Adepts_Clothes, ItemClassification.filler, 734004, ItemType.Armor, 0),
#    ItemData(190, ItemName.Elven_Shirt, ItemClassification.filler, 734048, ItemType.Armor, 0),
#    ItemData(191, ItemName.Silver_Vest, ItemClassification.filler, 734092, ItemType.Armor, 0),
#    ItemData(192, ItemName.Water_Jacket, ItemClassification.filler, 734136, ItemType.Armor, 0),
#    ItemData(193, ItemName.Storm_Gear, ItemClassification.filler, 734180, ItemType.Armor, 0),
#    ItemData(194, ItemName.Kimono, ItemClassification.filler, 734224, ItemType.Armor, 0),
#    ItemData(195, ItemName.Ninja_Garb, ItemClassification.filler, 734268, ItemType.Armor, 0),
#    ItemData(196, ItemName.OnePiece_Dress, ItemClassification.filler, 734488, ItemType.Armor, 0),
#    ItemData(197, ItemName.Travel_Robe, ItemClassification.filler, 734532, ItemType.Armor, 0),
#    ItemData(198, ItemName.Silk_Robe, ItemClassification.filler, 734576, ItemType.Armor, 0),
#    ItemData(199, ItemName.China_Dress, ItemClassification.filler, 734620, ItemType.Armor, 0),
#    ItemData(200, ItemName.Jerkin, ItemClassification.filler, 734664, ItemType.Armor, 0),
#    ItemData(201, ItemName.Cocktail_Dress, ItemClassification.filler, 734708, ItemType.Armor, 0),
#    ItemData(202, ItemName.Blessed_Robe, ItemClassification.filler, 734752, ItemType.Armor, 0),
#    ItemData(203, ItemName.Magical_Cassock, ItemClassification.filler, 734796, ItemType.Armor, 0),
#    ItemData(204, ItemName.Mysterious_Robe, ItemClassification.filler, 734840, ItemType.Armor, 0),
#    ItemData(205, ItemName.Feathered_Robe, ItemClassification.filler, 734884, ItemType.Armor, 0),
#    ItemData(206, ItemName.Oracles_Robe, ItemClassification.filler, 734928, ItemType.Armor, 0),
#    ItemData(207, ItemName.Planet_Armor, ItemClassification.filler, 744388, ItemType.Armor, 0),
#    ItemData(208, ItemName.Dragon_Mail, ItemClassification.filler, 744432, ItemType.Armor, 0),
#    ItemData(209, ItemName.Chronos_Mail, ItemClassification.filler, 744476, ItemType.Armor, 0),
#    ItemData(210, ItemName.Stealth_Armor, ItemClassification.filler, 744520, ItemType.Armor, 0),
#    ItemData(211, ItemName.Xylion_Armor, ItemClassification.filler, 744564, ItemType.Armor, 0),
#    ItemData(212, ItemName.Ixion_Mail, ItemClassification.filler, 744608, ItemType.Armor, 1),
#    ItemData(213, ItemName.Phantasmal_Mail, ItemClassification.filler, 744652, ItemType.Armor, 1),
#    ItemData(214, ItemName.Erebus_Armor, ItemClassification.filler, 744696, ItemType.Armor, 0),
#    ItemData(215, ItemName.Valkyrie_Mail, ItemClassification.filler, 744740, ItemType.Armor, 1),
#    ItemData(216, ItemName.Faery_Vest, ItemClassification.filler, 744828, ItemType.Armor, 0),
#    ItemData(217, ItemName.Mythril_Clothes, ItemClassification.filler, 744872, ItemType.Armor, 0),
#    ItemData(218, ItemName.Full_Metal_Vest, ItemClassification.filler, 744916, ItemType.Armor, 1),
#    ItemData(219, ItemName.Wild_Coat, ItemClassification.filler, 744960, ItemType.Armor, 0),
#    ItemData(220, ItemName.Floral_Dress, ItemClassification.filler, 745004, ItemType.Armor, 0),
#    ItemData(221, ItemName.Festival_Coat, ItemClassification.filler, 745048, ItemType.Armor, 1),
#    ItemData(222, ItemName.Erinyes_Tunic, ItemClassification.filler, 745092, ItemType.Armor, 1),
#    ItemData(223, ItemName.Tritons_Ward, ItemClassification.filler, 745136, ItemType.Armor, 0),
#    ItemData(224, ItemName.Dragon_Robe, ItemClassification.filler, 745224, ItemType.Armor, 0),
#    ItemData(225, ItemName.Ardagh_Robe, ItemClassification.filler, 745268, ItemType.Armor, 0),
#    ItemData(226, ItemName.Muni_Robe, ItemClassification.filler, 745312, ItemType.Armor, 1),
#    ItemData(227, ItemName.Aeolian_Cassock, ItemClassification.filler, 745356, ItemType.Armor, 0),
#    ItemData(228, ItemName.Iris_Robe, ItemClassification.filler, 745400, ItemType.Armor, 1)
# ]
#
# shield_list: List[ItemData] = [
#    ItemData(229, ItemName.Wooden_Shield, ItemClassification.filler, 735148, ItemType.Shield, 0),
#    ItemData(230, ItemName.Bronze_Shield, ItemClassification.filler, 735192, ItemType.Shield, 0),
#    ItemData(231, ItemName.Iron_Shield, ItemClassification.filler, 735236, ItemType.Shield, 0),
#    ItemData(232, ItemName.Knights_Shield, ItemClassification.filler, 735280, ItemType.Shield, 0),
#    ItemData(233, ItemName.Mirrored_Shield, ItemClassification.filler, 735324, ItemType.Shield, 0),
#    ItemData(234, ItemName.Dragon_Shield, ItemClassification.filler, 735368, ItemType.Shield, 0),
#    ItemData(235, ItemName.Earth_Shield, ItemClassification.filler, 735412, ItemType.Shield, 0),
#    ItemData(236, ItemName.Padded_Gloves, ItemClassification.filler, 735544, ItemType.Shield, 0),
#    ItemData(237, ItemName.Leather_Gloves, ItemClassification.filler, 735588, ItemType.Shield, 0),
#    ItemData(238, ItemName.Gauntlets, ItemClassification.filler, 735632, ItemType.Shield, 0),
#    ItemData(239, ItemName.Vambrace, ItemClassification.filler, 735676, ItemType.Shield, 0),
#    ItemData(240, ItemName.War_Gloves, ItemClassification.filler, 735720, ItemType.Shield, 0),
#    ItemData(241, ItemName.Spirit_Gloves, ItemClassification.filler, 735764, ItemType.Shield, 0),
#    ItemData(242, ItemName.Battle_Gloves, ItemClassification.filler, 735808, ItemType.Shield, 0),
#    ItemData(243, ItemName.Aura_Gloves, ItemClassification.filler, 735852, ItemType.Shield, 0),
#    ItemData(244, ItemName.Leather_Armlet, ItemClassification.filler, 735940, ItemType.Shield, 0),
#    ItemData(245, ItemName.Armlet, ItemClassification.filler, 735984, ItemType.Shield, 0),
#    ItemData(246, ItemName.Heavy_Armlet, ItemClassification.filler, 736028, ItemType.Shield, 0),
#    ItemData(247, ItemName.Silver_Armlet, ItemClassification.filler, 736072, ItemType.Shield, 0),
#    ItemData(248, ItemName.Spirit_Armlet, ItemClassification.filler, 736116, ItemType.Shield, 0),
#    ItemData(249, ItemName.Virtuous_Armlet, ItemClassification.filler, 736160, ItemType.Shield, 0),
#    ItemData(250, ItemName.Guardian_Armlet, ItemClassification.filler, 736204, ItemType.Shield, 0),
#    ItemData(251, ItemName.Luna_Shield, ItemClassification.filler, 745488, ItemType.Shield, 0),
#    ItemData(252, ItemName.Dragon_Shield, ItemClassification.filler, 745532, ItemType.Shield, 0),
#    ItemData(253, ItemName.Flame_Shield, ItemClassification.filler, 745576, ItemType.Shield, 0),
#    ItemData(254, ItemName.Terra_Shield, ItemClassification.filler, 745620, ItemType.Shield, 0),
#    ItemData(255, ItemName.Cosmos_Shield, ItemClassification.filler, 745664, ItemType.Shield, 0),
#    ItemData(256, ItemName.Fujin_Shield, ItemClassification.filler, 745708, ItemType.Shield, 1),
#    ItemData(257, ItemName.Aegis_Shield, ItemClassification.filler, 745752, ItemType.Shield, 0),
#    ItemData(258, ItemName.Aerial_Gloves, ItemClassification.filler, 745840, ItemType.Shield, 0),
#    ItemData(259, ItemName.Titan_Gloves, ItemClassification.filler, 745884, ItemType.Shield, 0),
#    ItemData(260, ItemName.Big_Bang_Gloves, ItemClassification.filler, 745928, ItemType.Shield, 0),
#    ItemData(261, ItemName.Crafted_Gloves, ItemClassification.filler, 745972, ItemType.Shield, 0),
#    ItemData(262, ItemName.Riot_Gloves, ItemClassification.filler, 746016, ItemType.Shield, 0),
#    ItemData(263, ItemName.Spirit_Gloves, ItemClassification.filler, 746060, ItemType.Shield, 1),
#    ItemData(264, ItemName.Clear_Bracelet, ItemClassification.filler, 746148, ItemType.Shield, 0),
#    ItemData(265, ItemName.Mythril_Armlet, ItemClassification.filler, 746192, ItemType.Shield, 0),
#    ItemData(266, ItemName.Bone_Armlet, ItemClassification.filler, 746236, ItemType.Shield, 1),
#    ItemData(267, ItemName.Jesters_Armlet, ItemClassification.filler, 746280, ItemType.Shield, 1),
#    ItemData(268, ItemName.Ledas_Bracelet, ItemClassification.filler, 746324, ItemType.Shield, 0)
# ]
#
# helm_list: List[ItemData] = [
#    ItemData(269, ItemName.Open_Helm, ItemClassification.filler, 736336, ItemType.Helm, 0),
#    ItemData(270, ItemName.Bronze_Helm, ItemClassification.filler, 736380, ItemType.Helm, 0),
#    ItemData(271, ItemName.Iron_Helm, ItemClassification.filler, 736424, ItemType.Helm, 0),
#    ItemData(272, ItemName.Steel_Helm, ItemClassification.filler, 736468, ItemType.Helm, 0),
#    ItemData(273, ItemName.Silver_Helm, ItemClassification.filler, 736512, ItemType.Helm, 0),
#    ItemData(274, ItemName.Knights_Helm, ItemClassification.filler, 736556, ItemType.Helm, 0),
#    ItemData(275, ItemName.Warriors_Helm, ItemClassification.filler, 736600, ItemType.Helm, 0),
#    ItemData(276, ItemName.Adepts_Helm, ItemClassification.filler, 736644, ItemType.Helm, 0),
#    ItemData(277, ItemName.Leather_Cap, ItemClassification.filler, 736820, ItemType.Helm, 0),
#    ItemData(278, ItemName.Wooden_Cap, ItemClassification.filler, 736864, ItemType.Helm, 0),
#    ItemData(279, ItemName.Mail_Cap, ItemClassification.filler, 736908, ItemType.Helm, 0),
#    ItemData(280, ItemName.Jeweled_Crown, ItemClassification.filler, 736952, ItemType.Helm, 0),
#    ItemData(281, ItemName.Ninja_Hood, ItemClassification.filler, 736996, ItemType.Helm, 0),
#    ItemData(282, ItemName.Lucky_Cap, ItemClassification.filler, 737040, ItemType.Helm, 0),
#    ItemData(283, ItemName.Thunder_Crown, ItemClassification.filler, 737084, ItemType.Helm, 0),
#    ItemData(284, ItemName.Prophets_Hat, ItemClassification.filler, 737128, ItemType.Helm, 0),
#    ItemData(285, ItemName.Lure_Cap, ItemClassification.filler, 737172, ItemType.Helm, 0),
#    ItemData(286, ItemName.Circlet, ItemClassification.filler, 737260, ItemType.Helm, 0),
#    ItemData(287, ItemName.Silver_Circlet, ItemClassification.filler, 737304, ItemType.Helm, 0),
#    ItemData(288, ItemName.Guardian_Circlet, ItemClassification.filler, 737348, ItemType.Helm, 0),
#    ItemData(289, ItemName.Platinum_Circlet, ItemClassification.filler, 737392, ItemType.Helm, 0),
#    ItemData(290, ItemName.Mythril_Circlet, ItemClassification.filler, 737436, ItemType.Helm, 0),
#    ItemData(291, ItemName.Glittering_Tiara, ItemClassification.filler, 737480, ItemType.Helm, 0),
#    ItemData(292, ItemName.Dragon_Helm, ItemClassification.filler, 746412, ItemType.Helm, 0),
#    ItemData(293, ItemName.Mythril_Helm, ItemClassification.filler, 746456, ItemType.Helm, 0),
#    ItemData(294, ItemName.Fear_Helm, ItemClassification.filler, 746500, ItemType.Helm, 0),
#    ItemData(295, ItemName.Millenium_Helm, ItemClassification.filler, 746544, ItemType.Helm, 0),
#    ItemData(296, ItemName.Viking_Helm, ItemClassification.filler, 746588, ItemType.Helm, 1),
#    ItemData(297, ItemName.Gloria_Helm, ItemClassification.filler, 746632, ItemType.Helm, 0),
#    ItemData(298, ItemName.Minerva_Helm, ItemClassification.filler, 746676, ItemType.Helm, 0),
#    ItemData(299, ItemName.Floating_Hat, ItemClassification.filler, 746764, ItemType.Helm, 0),
#    ItemData(300, ItemName.Nurses_Cap, ItemClassification.filler, 746808, ItemType.Helm, 1),
#    ItemData(301, ItemName.Thorn_Crown, ItemClassification.filler, 746852, ItemType.Helm, 1),
#    ItemData(302, ItemName.Otafuku_Mask, ItemClassification.filler, 746896, ItemType.Helm, 0),
#    ItemData(303, ItemName.Hiotoko_Mask, ItemClassification.filler, 746940, ItemType.Helm, 0),
#    ItemData(304, ItemName.Crown_of_Glory, ItemClassification.filler, 746984, ItemType.Helm, 0),
#    ItemData(305, ItemName.Alastors_Hood, ItemClassification.filler, 747028, ItemType.Helm, 1),
#    ItemData(306, ItemName.Pure_Circlet, ItemClassification.filler, 747116, ItemType.Helm, 0),
#    ItemData(307, ItemName.Astral_Circlet, ItemClassification.filler, 747160, ItemType.Helm, 0),
#    ItemData(308, ItemName.Psychic_Circlet, ItemClassification.filler, 747204, ItemType.Helm, 0),
#    ItemData(309, ItemName.Demon_Circlet, ItemClassification.filler, 747248, ItemType.Helm, 0),
#    ItemData(310, ItemName.Clarity_Circlet, ItemClassification.filler, 747292, ItemType.Helm, 1),
#    ItemData(311, ItemName.Brilliant_Circlet, ItemClassification.filler, 747336, ItemType.Helm, 0),
#    ItemData(312, ItemName.Berserker_Band, ItemClassification.filler, 747380, ItemType.Helm, 0)
# ]
#
# elemental_star_list: List[ItemData] = [
#    #ItemData(330, ItemName.Venus_Star, ItemClassification.filler, 739636, ItemType.KeyItem, 0),
#    #ItemData(331, ItemName.Mercury_Star, ItemClassification.filler, 739680, ItemType.KeyItem, 0),
#    #ItemData(332, ItemName.Mythril_Bag, ItemClassification.filler, 739724, ItemType.KeyItem, 1),
#    #ItemData(333, ItemName.Mythril_Bag, ItemClassification.filler, 739768, ItemType.KeyItem, 0),
#    ItemData(334, ItemName.Mythril_Bag, ItemClassification.filler, 739812, ItemType.KeyItem, 0),
#    ItemData(335, ItemName.Mythril_Bag, ItemClassification.filler, 740736, ItemType.KeyItem, 0),
#    ItemData(336, ItemName.Jupiter_Star, ItemClassification.filler, 740780, ItemType.KeyItem, 0),
#    ItemData(337, ItemName.Mars_Star, ItemClassification.filler, 740824, ItemType.KeyItem, 0)
# ]
#
# shirt_list: List[ItemData] = [
#    ItemData(338, ItemName.Mythril_Shirt, ItemClassification.filler, 740956, ItemType.Shirt, 0),
#    ItemData(339, ItemName.Silk_Shirt, ItemClassification.filler, 741000, ItemType.Shirt, 0),
#    ItemData(340, ItemName.Running_Shirt, ItemClassification.filler, 741044, ItemType.Shirt, 0),
#    ItemData(341, ItemName.Divine_Camisole, ItemClassification.filler, 747468, ItemType.Shirt, 0),
#    ItemData(342, ItemName.Herbed_Shirt, ItemClassification.filler, 747512, ItemType.Shirt, 0),
#    ItemData(343, ItemName.Golden_Shirt, ItemClassification.filler, 747556, ItemType.Shirt, 0),
#    ItemData(344, ItemName.Casual_Shirt, ItemClassification.filler, 747600, ItemType.Shirt, 0)
# ]
#
# boots_list: List[ItemData] = [
#    ItemData(345, ItemName.Hyper_Boots, ItemClassification.filler, 741220, ItemType.Boots, 0),
#    ItemData(346, ItemName.Quick_Boots, ItemClassification.filler, 741264, ItemType.Boots, 0),
#    ItemData(347, ItemName.Fur_Boots, ItemClassification.filler, 741308, ItemType.Boots, 0),
#    ItemData(348, ItemName.Turtle_Boots, ItemClassification.filler, 741352, ItemType.Boots, 1),
#    ItemData(349, ItemName.Leather_Boots, ItemClassification.filler, 747644, ItemType.Boots, 0),
#    ItemData(350, ItemName.Dragon_Boots, ItemClassification.filler, 747688, ItemType.Boots, 0),
#    ItemData(351, ItemName.Safety_Boots, ItemClassification.filler, 747732, ItemType.Boots, 0),
#    ItemData(352, ItemName.Knights_Greave, ItemClassification.filler, 747776, ItemType.Boots, 0),
#    ItemData(353, ItemName.Silver_Greave, ItemClassification.filler, 747820, ItemType.Boots, 0),
#    ItemData(354, ItemName.Ninja_Sandals, ItemClassification.filler, 747864, ItemType.Boots, 0),
#    ItemData(355, ItemName.Golden_Boots, ItemClassification.filler, 747908, ItemType.Boots, 0)
# ]
#
# ring_list: List[ItemData] = [
#    ItemData(356, ItemName.Adept_Ring, ItemClassification.filler, 741484, ItemType.Ring, 0),
#    ItemData(357, ItemName.War_Ring, ItemClassification.filler, 741528, ItemType.Ring, 0),
#    ItemData(358, ItemName.Sleep_Ring, ItemClassification.filler, 741572, ItemType.Ring, 0),
#    ItemData(359, ItemName.Healing_Ring, ItemClassification.filler, 741616, ItemType.Ring, 0),
#    ItemData(360, ItemName.Unicorn_Ring, ItemClassification.filler, 741660, ItemType.Ring, 1),
#    ItemData(361, ItemName.Fairy_Ring, ItemClassification.filler, 741704, ItemType.Ring, 0),
#    ItemData(362, ItemName.Clerics_Ring, ItemClassification.filler, 741748, ItemType.Ring, 0),
#    ItemData(363, ItemName.Spirit_Ring, ItemClassification.filler, 747952, ItemType.Ring, 0),
#    ItemData(364, ItemName.Stardust_Ring, ItemClassification.filler, 747996, ItemType.Ring, 0),
#    ItemData(365, ItemName.Aroma_Ring, ItemClassification.filler, 748040, ItemType.Ring, 0),
#    ItemData(366, ItemName.Rainbow_Ring, ItemClassification.filler, 748084, ItemType.Ring, 0),
#    ItemData(367, ItemName.Soul_Ring, ItemClassification.filler, 748128, ItemType.Ring, 0),
#    ItemData(368, ItemName.Guardian_Ring, ItemClassification.filler, 748172, ItemType.Ring, 1),
#    ItemData(369, ItemName.Golden_Ring, ItemClassification.filler, 748216, ItemType.Ring, 0)
# ]
#
# class_item_list: List[ItemData] = [
#    ItemData(371, ItemName.Mysterious_Card, ItemClassification.filler, 749448, ItemType.Class, 1),
#    ItemData(372, ItemName.Trainers_Whip, ItemClassification.filler, 749492, ItemType.Class, 1),
#    ItemData(373, ItemName.Tomegathericon, ItemClassification.filler, 749536, ItemType.Class, 1)
# ]

summon_list: List[ItemData] = [
   ItemData(400, ItemName.Moloch, ItemClassification.useful, 3859, ItemType.Psyenergy, 3859, 132),
   ItemData(401, ItemName.Daedalus, ItemClassification.useful, 3864, ItemType.Psyenergy, 3864, 132),
   ItemData(401, ItemName.Flora, ItemClassification.useful, 3858, ItemType.Psyenergy, 3858, 132),
   ItemData(401, ItemName.Ulysses, ItemClassification.useful, 3860, ItemType.Psyenergy, 3860, 132),
   ItemData(401, ItemName.Azul, ItemClassification.useful, 3865, ItemType.Psyenergy, 3865, 132),
   ItemData(401, ItemName.Zagan, ItemClassification.useful, 3856, ItemType.Psyenergy, 3856, 132),
   ItemData(401, ItemName.Megaera, ItemClassification.useful, 3857, ItemType.Psyenergy, 3857, 132),
   ItemData(401, ItemName.Haures, ItemClassification.useful, 3861, ItemType.Psyenergy, 3861, 132),
   ItemData(401, ItemName.Coatlicue, ItemClassification.useful, 3863, ItemType.Psyenergy, 3863, 132),
   ItemData(401, ItemName.Catastrophe, ItemClassification.useful, 3866, ItemType.Psyenergy, 3866, 132),
   ItemData(401, ItemName.Charon, ItemClassification.useful, 3867, ItemType.Psyenergy, 3867, 132),
   ItemData(401, ItemName.Iris, ItemClassification.useful, 3868, ItemType.Psyenergy, 3868, 132),
   ItemData(401, ItemName.Eclipse, ItemClassification.useful, 3862, ItemType.Psyenergy, 3862, 132)
]

psynergy_list: List[ItemData] = [
   ItemData(374, ItemName.Growth, ItemClassification.progression, 3596, ItemType.Psyenergy, 3596, 132),
   ItemData(375, ItemName.Whirlwind, ItemClassification.progression, 3662, ItemType.Psyenergy, 3662, 132),
   ItemData(376, ItemName.Parch, ItemClassification.progression, 3722, ItemType.Psyenergy, 3722, 132),
   ItemData(377, ItemName.Sand, ItemClassification.progression, 3723, ItemType.Psyenergy, 3723, 132),
   ItemData(378, ItemName.Mind_Read, ItemClassification.progression, 3725, ItemType.Psyenergy, 3725, 132),
   ItemData(379, ItemName.Reveal, ItemClassification.progression, 3728, ItemType.Psyenergy, 3728, 132),
   ItemData(380, ItemName.Blaze, ItemClassification.progression, 3738, ItemType.Psyenergy, 3738, 132)
]

psyenergy_as_item_list: List[ItemData] = [
   # ItemData(313, ItemName.Lash_Pebble, ItemClassification.progression, 738668, ItemType.PsyenergyItem, 738668, 1, 128),
   # ItemData(314, ItemName.Pound_Cube, ItemClassification.progression, 738712, ItemType.PsyenergyItem, 738712, 1, 128),
   # ItemData(315, ItemName.Orb_of_Force, ItemClassification.progression, 738756, ItemType.PsyenergyItem, 738756, 1, 128),
   # ItemData(316, ItemName.Douse_Drop, ItemClassification.progression, 738800, ItemType.PsyenergyItem, 738800, 1, 128),
   # ItemData(317, ItemName.Frost_Jewel, ItemClassification.progression, 738844, ItemType.PsyenergyItem, 738844, 1, 128),
   # ItemData(318, ItemName.Lifting_Gem, ItemClassification.progression, 738888, ItemType.PsyenergyItem, 738888, 1, 128),
   # ItemData(321, ItemName.Carry_Stone, ItemClassification.progression, 739020, ItemType.PsyenergyItem, 739020, 1, 128),
   # ItemData(322, ItemName.Catch_Beads, ItemClassification.progression, 739064, ItemType.PsyenergyItem, 739064, 1, 128),
   # ItemData(323, ItemName.Tremor_Bit, ItemClassification.progression, 739108, ItemType.PsyenergyItem, 739108, 1, 128),
   # ItemData(324, ItemName.Scoop_Gem, ItemClassification.progression, 739152, ItemType.PsyenergyItem, 739152, 1, 128),
   # ItemData(325, ItemName.Cyclone_Chip, ItemClassification.progression, 739196, ItemType.PsyenergyItem, 739196, 1, 128),
   # ItemData(326, ItemName.Burst_Brooch, ItemClassification.progression, 739328, ItemType.PsyenergyItem, 739328, 1, 128),
   # ItemData(327, ItemName.Grindstone, ItemClassification.progression, 739372, ItemType.PsyenergyItem, 739372, 1, 128),
   # ItemData(328, ItemName.Hover_Jade, ItemClassification.progression, 739416, ItemType.PsyenergyItem, 739416, 1, 128),
   # ItemData(329, ItemName.Teleport_Lapis, ItemClassification.progression, 739504, ItemType.PsyenergyItem, 739504, 1, 128)

   ItemData(313, ItemName.Lash_Pebble, ItemClassification.progression, 3717, ItemType.PsyenergyItem, 3717, 128),
   ItemData(314, ItemName.Pound_Cube, ItemClassification.progression, 3718, ItemType.PsyenergyItem, 3718, 128),
   ItemData(315, ItemName.Orb_of_Force, ItemClassification.progression, 3726, ItemType.PsyenergyItem, 3726, 128),
   ItemData(316, ItemName.Douse_Drop, ItemClassification.progression, 3617, ItemType.PsyenergyItem, 3617, 128),
   ItemData(317, ItemName.Frost_Jewel, ItemClassification.progression, 3608, ItemType.PsyenergyItem, 3608, 128),
   ItemData(318, ItemName.Lifting_Gem, ItemClassification.progression, 3727, ItemType.PsyenergyItem, 3727, 128),
   ItemData(321, ItemName.Carry_Stone, ItemClassification.progression, 3731, ItemType.PsyenergyItem, 3731, 128),
   ItemData(322, ItemName.Catch_Beads, ItemClassification.progression, 3732, ItemType.PsyenergyItem, 3732, 128),
   ItemData(323, ItemName.Tremor_Bit, ItemClassification.progression, 3719, ItemType.PsyenergyItem, 3719, 128),
   ItemData(324, ItemName.Scoop_Gem, ItemClassification.progression, 3720, ItemType.PsyenergyItem, 3720, 128),
   ItemData(325, ItemName.Cyclone_Chip, ItemClassification.progression, 3721, ItemType.PsyenergyItem, 3721, 128),
   ItemData(326, ItemName.Burst_Brooch, ItemClassification.progression, 3735, ItemType.PsyenergyItem, 3735, 131),
   ItemData(327, ItemName.Grindstone, ItemClassification.progression, 3736, ItemType.PsyenergyItem, 3736, 128),
   ItemData(328, ItemName.Hover_Jade, ItemClassification.progression, 3737, ItemType.PsyenergyItem, 3737, 128),
   ItemData(329, ItemName.Teleport_Lapis, ItemClassification.progression, 3740, ItemType.PsyenergyItem, 3740, 128)
]

base_djinn_index = 400

djinn_items: List[ItemData] =[
   DjinItemData(base_djinn_index, ItemName.Flint, ItemClassification.progression, 16384000, 0, ElementType.Earth,
                814004, [8, 4, 3, 0, 0, 0]),
   DjinItemData(base_djinn_index + 1, ItemName.Granite, ItemClassification.progression, 16384002, 1, ElementType.Earth,
                814016, [9, 0, 0, 2, 2, 1]),
   DjinItemData(base_djinn_index + 2, ItemName.Quartz, ItemClassification.progression, 16384004, 2, ElementType.Earth,
                814028, [10, 3, 0, 0, 3, 0]),
   DjinItemData(base_djinn_index + 3, ItemName.Vine, ItemClassification.progression, 16384006, 3, ElementType.Earth,
                814040, [12, 4, 0, 3, 0, 1]),
   DjinItemData(base_djinn_index + 4, ItemName.Sap, ItemClassification.progression, 16384008, 4, ElementType.Earth,
                814052, [10, 0, 3, 0, 0, 1]),
   DjinItemData(base_djinn_index + 5, ItemName.Ground, ItemClassification.progression, 16384010, 5, ElementType.Earth,
                814064, [9, 3, 0, 0, 3, 0]),
   DjinItemData(base_djinn_index + 6, ItemName.Bane, ItemClassification.progression, 16384012, 6, ElementType.Earth,
                814076, [12, 0, 4, 0, 0, 0]),
   DjinItemData(base_djinn_index + 7, ItemName.Echo, ItemClassification.progression, 16384014, 7, ElementType.Earth,
                814088, [9, 4, 3, 0, 0, 0]),
   DjinItemData(base_djinn_index + 8, ItemName.Iron, ItemClassification.progression, 16384016, 8, ElementType.Earth,
                814100, [11, 0, 0, 2, 3, 0]),
   DjinItemData(base_djinn_index + 9, ItemName.Steel, ItemClassification.progression, 16384018, 9, ElementType.Earth,
                814112, [9, 0, 4, 2, 0, 1]),
   DjinItemData(base_djinn_index + 10, ItemName.Mud, ItemClassification.progression, 16384020, 10, ElementType.Earth,
                814124, [10, 4, 0, 0, 3, 0]),
   DjinItemData(base_djinn_index + 11, ItemName.Flower, ItemClassification.progression, 16384022, 11, ElementType.Earth,
                814136, [12, 4, 0, 0, 0, 0]),
   DjinItemData(base_djinn_index + 12, ItemName.Meld, ItemClassification.progression, 16384024, 12, ElementType.Earth,
                814148, [9, 0, 0, 0, 4, 1]),
   DjinItemData(base_djinn_index + 13, ItemName.Petra, ItemClassification.progression, 16384026, 13, ElementType.Earth,
                814160, [11, 0, 0, 3, 0, 0]),
   DjinItemData(base_djinn_index + 14, ItemName.Salt, ItemClassification.progression, 16384028, 14, ElementType.Earth,
                814172, [9, 5, 0, 0, 0, 1]),
   DjinItemData(base_djinn_index + 15, ItemName.Geode, ItemClassification.progression, 16384030, 15, ElementType.Earth,
                814184, [12, 0, 6, 0, 0, 0]),
   DjinItemData(base_djinn_index + 16, ItemName.Mold, ItemClassification.progression, 16384032, 16, ElementType.Earth,
                814196, [8, 0, 4, 0, 2, 1]),
   DjinItemData(base_djinn_index + 17, ItemName.Crystal, ItemClassification.progression, 16384034, 16,
                ElementType.Earth, 814208, [10, 5, 0, 2, 0, 0]),

   DjinItemData(base_djinn_index + 18, ItemName.Fizz, ItemClassification.progression, 16384036, 0, ElementType.Water,
                814328, [9, 4, 0, 3, 0, 0]),
   DjinItemData(base_djinn_index + 19, ItemName.Sleet, ItemClassification.progression, 16384038, 1, ElementType.Water,
                814256, [12, 0, 3, 0, 0, 1]),
   DjinItemData(base_djinn_index + 20, ItemName.Mist, ItemClassification.progression, 16384040, 2, ElementType.Water,
                814268, [11, 0, 4, 0, 0, 0]),
   DjinItemData(base_djinn_index + 21, ItemName.Spritz, ItemClassification.progression, 16384042, 3, ElementType.Water,
                814280, [8, 4, 0, 0, 3, 0]),
   DjinItemData(base_djinn_index + 22, ItemName.Hail, ItemClassification.progression, 16384044, 4, ElementType.Water,
                814292, [9, 0, 4, 0, 0, 1]),
   DjinItemData(base_djinn_index + 23, ItemName.Tonic, ItemClassification.progression, 16384046, 5, ElementType.Water,
                814304, [8, 3, 0, 2, 0, 2]),
   DjinItemData(base_djinn_index + 24, ItemName.Dew, ItemClassification.progression, 16384048, 6, ElementType.Water,
                814316, [13, 4, 0, 0, 4, 0]),
   DjinItemData(base_djinn_index + 25, ItemName.Fog, ItemClassification.progression, 16384050, 7, ElementType.Water,
                814328, [9, 0, 0, 2, 2, 1]),
   DjinItemData(base_djinn_index + 26, ItemName.Sour, ItemClassification.progression, 16384052, 8, ElementType.Water,
                814340, [8, 4, 3, 0, 0, 0]),
   DjinItemData(base_djinn_index + 27, ItemName.Spring, ItemClassification.progression, 16384054, 9, ElementType.Water,
                814352, [11, 5, 0, 0, 0, 0]),
   DjinItemData(base_djinn_index + 28, ItemName.Shade, ItemClassification.progression, 16384056, 10, ElementType.Water,
                814364, [9, 0, 0, 3, 0, 2]),
   DjinItemData(base_djinn_index + 29, ItemName.Chill, ItemClassification.progression, 16384058, 11, ElementType.Water,
                814376, [10, 3, 0, 2, 0, 0]),
   DjinItemData(base_djinn_index + 30, ItemName.Steam, ItemClassification.progression, 16384060, 12, ElementType.Water,
                814388, [10, 0, 5, 0, 0, 0]),
   DjinItemData(base_djinn_index + 31, ItemName.Rime, ItemClassification.progression, 16384062, 13, ElementType.Water,
                814400, [10, 6, 0, 0, 0, 0]),
   DjinItemData(base_djinn_index + 32, ItemName.Gel, ItemClassification.progression, 16384064, 14, ElementType.Water,
                814412, [9, 0, 5, 0, 2, 0]),
   DjinItemData(base_djinn_index + 33, ItemName.Eddy, ItemClassification.progression, 16384066, 15, ElementType.Water,
                814424, [9, 0, 0, 0, 3, 2]),
   DjinItemData(base_djinn_index + 34, ItemName.Balm, ItemClassification.progression, 16384068, 16, ElementType.Water,
                814436, [13, 4, 0, 0, 0, 2]),
   DjinItemData(base_djinn_index + 35, ItemName.Serac, ItemClassification.progression, 16384070, 17, ElementType.Water,
                814448, [12, 0, 3, 0, 0, 0]),

   DjinItemData(base_djinn_index + 36, ItemName.Forge, ItemClassification.progression, 16384072, 0, ElementType.Fire,
                814484, [10, 0, 2, 0, 2, 2]),
   DjinItemData(base_djinn_index + 37, ItemName.Fever, ItemClassification.progression, 16384074, 1, ElementType.Fire,
                814496, [8, 0, 3, 0, 2, 0]),
   DjinItemData(base_djinn_index + 38, ItemName.Corona, ItemClassification.progression, 16384076, 2, ElementType.Fire,
                814508, [12, 3, 0, 3, 0, 1]),
   DjinItemData(base_djinn_index + 39, ItemName.Scorch, ItemClassification.progression, 16384078, 3, ElementType.Fire,
                814520, [8, 0, 3, 0, 0, 0]),
   DjinItemData(base_djinn_index + 40, ItemName.Ember, ItemClassification.progression, 16384080, 4, ElementType.Fire,
                814532, [9, 4, 0, 2, 2, 0]),
   DjinItemData(base_djinn_index + 41, ItemName.Flash, ItemClassification.progression, 16384082, 5, ElementType.Fire,
                814544, [14, 3, 0, 2, 0, 0]),
   DjinItemData(base_djinn_index + 42, ItemName.Torch, ItemClassification.progression, 16384084, 6, ElementType.Fire,
                814556, [9, 0, 3, 0, 0, 1]),
   DjinItemData(base_djinn_index + 43, ItemName.Cannon, ItemClassification.progression, 16384086, 7, ElementType.Fire,
                814568, [10, 0, 3, 0, 0, 0]),
   DjinItemData(base_djinn_index + 44, ItemName.Spark, ItemClassification.progression, 16384088, 8, ElementType.Fire,
                814580, [11, 6, 0, 0, 0, 0]),
   DjinItemData(base_djinn_index + 45, ItemName.Kindle, ItemClassification.progression, 16384090, 9, ElementType.Fire,
                814592, [8, 0, 5, 0, 0, 1]),
   DjinItemData(base_djinn_index + 46, ItemName.Char, ItemClassification.progression, 16384092, 10, ElementType.Fire,
                814604, [9, 0, 2, 0, 2, 1]),
   DjinItemData(base_djinn_index + 47, ItemName.Coal, ItemClassification.progression, 16384094, 11, ElementType.Fire,
                814616, [11, 3, 0, 0, 3, 0]),
   DjinItemData(base_djinn_index + 48, ItemName.Reflux, ItemClassification.progression, 16384096, 12, ElementType.Fire,
                814628, [9, 0, 0, 3, 0, 2]),
   DjinItemData(base_djinn_index + 49, ItemName.Core, ItemClassification.progression, 16384098, 13, ElementType.Fire,
                814640, [8, 0, 4, 2, 0, 0]),
   DjinItemData(base_djinn_index + 50, ItemName.Tinder, ItemClassification.progression, 16384100, 14, ElementType.Fire,
                814652, [12, 5, 0, 0, 0, 0]),
   DjinItemData(base_djinn_index + 51, ItemName.Shine, ItemClassification.progression, 16384102, 15, ElementType.Fire,
                814664, [9, 0, 3, 3, 2, 0]),
   DjinItemData(base_djinn_index + 52, ItemName.Fury, ItemClassification.progression, 16384104, 16, ElementType.Fire,
                814676, [12, 4, 0, 0, 0, 0]),
   DjinItemData(base_djinn_index + 53, ItemName.Fugue, ItemClassification.progression, 16384106, 17, ElementType.Fire,
                814688, [11, 4, 0, 2, 0, 0]),

   DjinItemData(base_djinn_index + 54, ItemName.Gust, ItemClassification.progression, 16384108, 0, ElementType.Air,
                814724, [9, 0, 2, 0, 2, 0]),
   DjinItemData(base_djinn_index + 55, ItemName.Breeze, ItemClassification.progression, 16384110, 1, ElementType.Air,
                814736, [12, 5, 0, 2, 0, 1]),
   DjinItemData(base_djinn_index + 56, ItemName.Zephyr, ItemClassification.progression, 16384112, 2, ElementType.Air,
                814748, [11, 3, 0, 0, 2, 1]),
   DjinItemData(base_djinn_index + 57, ItemName.Smog, ItemClassification.progression, 16384114, 3, ElementType.Air,
                814760, [9, 0, 3, 0, 0, 0]),
   DjinItemData(base_djinn_index + 58, ItemName.Kite, ItemClassification.progression, 16384116, 4, ElementType.Air,
                814772, [8, 4, 0, 0, 3, 0]),
   DjinItemData(base_djinn_index + 59, ItemName.Squall, ItemClassification.progression, 16384118, 5, ElementType.Air,
                814784, [10, 0, 5, 0, 0, 0]),
   DjinItemData(base_djinn_index + 60, ItemName.Luff, ItemClassification.progression, 16384120, 6, ElementType.Air,
                814796, [11, 5, 0, 2, 0, 1]),
   DjinItemData(base_djinn_index + 61, ItemName.Breath, ItemClassification.progression, 16384122, 7, ElementType.Air,
                814808, [9, 0, 0, 3, 4, 0]),
   DjinItemData(base_djinn_index + 62, ItemName.Blitz, ItemClassification.progression, 16384124, 8, ElementType.Air,
                814820, [10, 4, 3, 0, 0, 0]),
   DjinItemData(base_djinn_index + 63, ItemName.Ether, ItemClassification.progression, 16384126, 9, ElementType.Air,
                814832, [8, 4, 0, 0, 3, 2]),
   DjinItemData(base_djinn_index + 64, ItemName.Waft, ItemClassification.progression, 16384128, 10, ElementType.Air,
                814844, [11, 0, 4, 0, 0, 0]),
   DjinItemData(base_djinn_index + 65, ItemName.Haze, ItemClassification.progression, 16384130, 11, ElementType.Air,
                814856, [10, 0, 0, 2, 3, 2]),
   DjinItemData(base_djinn_index + 66, ItemName.Wheeze, ItemClassification.progression, 16384132, 12, ElementType.Air,
                814868, [9, 3, 5, 0, 0, 0]),
   DjinItemData(base_djinn_index + 67, ItemName.Aroma, ItemClassification.progression, 16384134, 13, ElementType.Air,
                814880, [11, 0, 0, 0, 3, 2]),
   DjinItemData(base_djinn_index + 68, ItemName.Whorl, ItemClassification.progression, 16384136, 14, ElementType.Air,
                814892, [9, 0, 4, 2, 0, 0]),
   DjinItemData(base_djinn_index + 69, ItemName.Gasp, ItemClassification.progression, 16384138, 15, ElementType.Air,
                814904, [12, 5, 0, 0, 0, 0]),
   DjinItemData(base_djinn_index + 70, ItemName.Lull, ItemClassification.progression, 16384140, 16, ElementType.Air,
                814916, [11, 6, 0, 0, 0, 0]),
   DjinItemData(base_djinn_index + 71, ItemName.Gale, ItemClassification.progression, 16384142, 17, ElementType.Air,
                814928, [10, 0, 0, 0, 5, 3])
]

test_items: List[ItemData] = [
   ItemData(2, ItemName.Herb, ItemClassification.filler, 737876, ItemType.Consumable, 180, 2),
   ItemData(20, ItemName.Smoke_Bomb, ItemClassification.filler, 739900, ItemType.Consumable, 226, 3),
   ItemData(21, ItemName.Sleep_Bomb, ItemClassification.filler, 739944, ItemType.Consumable, 227, 3),
   ItemData(8, ItemName.Psy_Crystal, ItemClassification.filler, 738140, ItemType.Consumable, 186, 131),
   ItemData(61, ItemName.Sea_Gods_Tear, ItemClassification.progression, 750108, ItemType.KeyItem, 458, 128),
   ItemData(371, ItemName.Mysterious_Card, ItemClassification.filler, 749448, ItemType.Class, 443, 128),
   ItemData(3, ItemName.Nut, ItemClassification.filler, 737920, ItemType.Consumable, 181, 128),
   ItemData(10, ItemName.Elixir, ItemClassification.filler, 738228, ItemType.Consumable, 188, 128),
   ItemData(17, ItemName.Mint, ItemClassification.filler, 738536, ItemType.Consumable, 195, 128),
   ItemData(142, ItemName.Themis_Axe, ItemClassification.filler, 743200, ItemType.Weapon, 301, 128),
   ItemData(218, ItemName.Full_Metal_Vest, ItemClassification.filler, 744916, ItemType.Armor, 340, 128),
   ItemData(9, ItemName.Antidote, ItemClassification.filler, 738184, ItemType.Consumable, 187, 128),
   ItemData(300, ItemName.Nurses_Cap, ItemClassification.filler, 746808, ItemType.Helm, 383, 128),

   ItemData(62, ItemName.Ruin_Key, ItemClassification.filler, 750152, ItemType.KeyItem, 459, 128),
   ItemData(15, ItemName.Apple, ItemClassification.filler, 738448, ItemType.Consumable, 193, 128),
   ItemData(23, ItemName.Lucky_Medal, ItemClassification.filler, 740032, ItemType.Consumable, 229, 128),
   ItemData(12, ItemName.Mist_Potion, ItemClassification.filler, 738316, ItemType.Consumable, 190, 128),

    ItemData(50, ItemName.Right_Prong, ItemClassification.progression, 749272, ItemType.KeyItem, 439, 131),
    ItemData(51, ItemName.Rusty_Staff, ItemClassification.filler, 748700, ItemType.Forgeable, 426, 128),
    ItemData(52, ItemName.Pirates_Sword, ItemClassification.filler, 742584, ItemType.Weapon, 287, 128),


    ItemData(53, ItemName.Guardian_Ring, ItemClassification.useful, 748172, ItemType.Ring, 414, 128),
    ItemData(54, ItemName.Trainers_Whip, ItemClassification.useful, 749492, ItemType.Weapon, 444, 128),
    ItemData(55, ItemName.Blow_Mace, ItemClassification.useful, 743552, ItemType.Weapon, 309, 128),
    ItemData(56, ItemName.Hard_Nut, ItemClassification.useful, 738492, ItemType.Consumable, 194, 128),


    ItemData(57, ItemName.Apple, ItemClassification.useful, 738448, ItemType.Consumable, 193, 2),
    ItemData(58, ItemName.Ixion_Mail, ItemClassification.useful, 744608, ItemType.Armor, 333, 128),
    ItemData(58, ItemName.Power_Bread, ItemClassification.useful, 738360, ItemType.Consumable, 191, 128),
    ItemData(58, ItemName.Potion, ItemClassification.filler, 742496, ItemType.Consumable, 183, 128)
]

events = [
   ItemData(None, ItemName.Ship, ItemClassification.progression, 0, ItemType.Event, 0),
   ItemData(None, ItemName.Victory, ItemClassification.progression, 0, ItemType.Event, 0),
   ItemData(None, ItemName.Chestbeaters_defeated, ItemClassification.progression, 0, ItemType.Event, 0),
   ItemData(None, ItemName.King_Scorpion_defeated, ItemClassification.progression, 0, ItemType.Event, 0),
   ItemData(None, ItemName.Gabombo_Statue_Completed, ItemClassification.progression, 0, ItemType.Event, 0)
]

all_items: List[ItemData] = test_items + djinn_items + psyenergy_as_item_list + psynergy_list + summon_list + events
item_table: Dict[str, ItemData] = {item.itemName: item for item in all_items}