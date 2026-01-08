from dataclasses import dataclass
from typing import List, Dict

from BaseClasses import ItemClassification, Item
from .Enums import SADX_BASE_ID
from .Names import ItemName


@dataclass
class ItemInfo:
    itemId: int
    name: str
    classification: ItemClassification


story_progression_item_table: List[ItemInfo] = [
    ItemInfo(90, ItemName.Progression.Emblem, ItemClassification.progression_skip_balancing),
    ItemInfo(91, ItemName.Progression.ChaosPeace, ItemClassification.progression),
]

chaos_emerald_item_table: List[ItemInfo] = [
    ItemInfo(92, ItemName.Progression.WhiteEmerald, ItemClassification.progression),
    ItemInfo(93, ItemName.Progression.RedEmerald, ItemClassification.progression),
    ItemInfo(94, ItemName.Progression.CyanEmerald, ItemClassification.progression),
    ItemInfo(95, ItemName.Progression.PurpleEmerald, ItemClassification.progression),
    ItemInfo(96, ItemName.Progression.GreenEmerald, ItemClassification.progression),
    ItemInfo(97, ItemName.Progression.YellowEmerald, ItemClassification.progression),
    ItemInfo(98, ItemName.Progression.BlueEmerald, ItemClassification.progression),
]

playable_character_item_table: List[ItemInfo] = [
    ItemInfo(1, ItemName.Sonic.Playable, ItemClassification.progression),
    ItemInfo(2, ItemName.Tails.Playable, ItemClassification.progression),
    ItemInfo(3, ItemName.Knuckles.Playable, ItemClassification.progression),
    ItemInfo(4, ItemName.Amy.Playable, ItemClassification.progression),
    ItemInfo(5, ItemName.Gamma.Playable, ItemClassification.progression),
    ItemInfo(6, ItemName.Big.Playable, ItemClassification.progression),

]

character_upgrade_item_table: List[ItemInfo] = [
    ItemInfo(10, ItemName.Sonic.LightShoes, ItemClassification.progression),
    ItemInfo(11, ItemName.Sonic.CrystalRing, ItemClassification.useful),
    ItemInfo(12, ItemName.Sonic.AncientLight, ItemClassification.progression),
    ItemInfo(20, ItemName.Tails.JetAnklet, ItemClassification.progression),
    ItemInfo(21, ItemName.Tails.RhythmBadge, ItemClassification.useful),
    ItemInfo(30, ItemName.Knuckles.ShovelClaw, ItemClassification.progression),
    ItemInfo(31, ItemName.Knuckles.FightingGloves, ItemClassification.useful),
    ItemInfo(40, ItemName.Amy.WarriorFeather, ItemClassification.useful),
    ItemInfo(41, ItemName.Amy.LongHammer, ItemClassification.useful),
    ItemInfo(50, ItemName.Gamma.JetBooster, ItemClassification.progression),
    ItemInfo(51, ItemName.Gamma.LaserBlaster, ItemClassification.useful),
    ItemInfo(60, ItemName.Big.LifeBelt, ItemClassification.progression),
    ItemInfo(61, ItemName.Big.PowerRod, ItemClassification.progression),
    ItemInfo(62, ItemName.Big.Lure1, ItemClassification.progression),
    ItemInfo(63, ItemName.Big.Lure2, ItemClassification.progression),
    ItemInfo(64, ItemName.Big.Lure3, ItemClassification.progression),
    ItemInfo(65, ItemName.Big.Lure4, ItemClassification.progression),

]

key_item_table: List[ItemInfo] = [
    ItemInfo(80, ItemName.KeyItem.Train, ItemClassification.progression),
    ItemInfo(81, ItemName.KeyItem.Boat, ItemClassification.progression),
    ItemInfo(82, ItemName.KeyItem.Raft, ItemClassification.progression),
    ItemInfo(83, ItemName.KeyItem.HotelFrontKey, ItemClassification.progression),
    ItemInfo(84, ItemName.KeyItem.HotelBackKey, ItemClassification.progression),
    ItemInfo(85, ItemName.KeyItem.TwinkleParkTicket, ItemClassification.progression),
    ItemInfo(86, ItemName.KeyItem.EmployeeCard, ItemClassification.progression),
    ItemInfo(87, ItemName.KeyItem.IceStone, ItemClassification.progression),
    ItemInfo(88, ItemName.KeyItem.Dynamite, ItemClassification.progression),
    ItemInfo(89, ItemName.KeyItem.JungleCart, ItemClassification.progression),
    ItemInfo(120, ItemName.KeyItem.WindStone, ItemClassification.progression),
    ItemInfo(121, ItemName.KeyItem.StationFrontKey, ItemClassification.progression),
    ItemInfo(122, ItemName.KeyItem.StationBackKey, ItemClassification.progression),
    ItemInfo(123, ItemName.KeyItem.Egglift, ItemClassification.progression),
    ItemInfo(124, ItemName.KeyItem.Monorail, ItemClassification.progression),

]

filler_item_table: List[ItemInfo] = [
    ItemInfo(71, ItemName.Filler.Invincibility, ItemClassification.filler),
    ItemInfo(72, ItemName.Filler.Rings5, ItemClassification.filler),
    ItemInfo(73, ItemName.Filler.Rings10, ItemClassification.filler),
    ItemInfo(74, ItemName.Filler.Shield, ItemClassification.filler),
    ItemInfo(75, ItemName.Filler.MagneticShield, ItemClassification.filler),
    ItemInfo(76, ItemName.Filler.ExtraLife, ItemClassification.filler),
]

trap_item_table: List[ItemInfo] = [
    ItemInfo(100, ItemName.Traps.IceTrap, ItemClassification.trap),
    ItemInfo(101, ItemName.Traps.SpringTrap, ItemClassification.trap),
    ItemInfo(102, ItemName.Traps.PoliceTrap, ItemClassification.trap),
    ItemInfo(103, ItemName.Traps.BuyonTrap, ItemClassification.trap),
    ItemInfo(104, ItemName.Traps.ReverseTrap, ItemClassification.trap),
    ItemInfo(105, ItemName.Traps.GravityTrap, ItemClassification.trap),
]

item_name_to_info: Dict[str, ItemInfo] = {
    item.name: item for item in (
            story_progression_item_table + chaos_emerald_item_table + playable_character_item_table
            + character_upgrade_item_table + key_item_table + filler_item_table + trap_item_table
    )
}

group_item_table: Dict[str, List[str]] = {
    ItemName.Groups.ChaosEmeralds: [item.name for item in chaos_emerald_item_table],
    ItemName.Groups.PlayableCharacters: [item.name for item in playable_character_item_table],
    ItemName.Groups.Upgrades: [item.name for item in character_upgrade_item_table],
    ItemName.Groups.KeyItems: [item.name for item in key_item_table],
    ItemName.Groups.Fillers: [item.name for item in filler_item_table],
    ItemName.Groups.Traps: [item.name for item in trap_item_table]
}


class SonicAdventureDXItem(Item):
    game: str = "Sonic Adventure DX"

    def __init__(self, name: str, player):
        item = item_name_to_info[name]
        super().__init__(item.name, item.classification, item.itemId + SADX_BASE_ID, player)
