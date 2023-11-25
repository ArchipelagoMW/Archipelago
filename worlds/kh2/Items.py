import typing

from BaseClasses import Item
from .Names import ItemName


class KH2Item(Item):
    game: str = "Kingdom Hearts 2"


class ItemData(typing.NamedTuple):
    quantity: int = 0
    kh2id: int = 0
    # Save+ mem addr
    memaddr: int = 0
    # some items have bitmasks. if bitmask>0 bitor to give item else
    bitmask: int = 0
    # if ability then
    ability: bool = False


# 0x130000
Reports_Table = {
    ItemName.SecretAnsemsReport1:  ItemData(1, 226, 0x36C4, 6),
    ItemName.SecretAnsemsReport2:  ItemData(1, 227, 0x36C4, 7),
    ItemName.SecretAnsemsReport3:  ItemData(1, 228, 0x36C5, 0),
    ItemName.SecretAnsemsReport4:  ItemData(1, 229, 0x36C5, 1),
    ItemName.SecretAnsemsReport5:  ItemData(1, 230, 0x36C5, 2),
    ItemName.SecretAnsemsReport6:  ItemData(1, 231, 0x36C5, 3),
    ItemName.SecretAnsemsReport7:  ItemData(1, 232, 0x36C5, 4),
    ItemName.SecretAnsemsReport8:  ItemData(1, 233, 0x36C5, 5),
    ItemName.SecretAnsemsReport9:  ItemData(1, 234, 0x36C5, 6),
    ItemName.SecretAnsemsReport10: ItemData(1, 235, 0x36C5, 7),
    ItemName.SecretAnsemsReport11: ItemData(1, 236, 0x36C6, 0),
    ItemName.SecretAnsemsReport12: ItemData(1, 237, 0x36C6, 1),
    ItemName.SecretAnsemsReport13: ItemData(1, 238, 0x36C6, 2),
}

Progression_Table = {
    ItemName.ProofofConnection:   ItemData(1, 593, 0x36B2),
    ItemName.ProofofNonexistence: ItemData(1, 594, 0x36B3),
    ItemName.ProofofPeace:        ItemData(1, 595, 0x36B4),
    ItemName.PromiseCharm:        ItemData(1, 524, 0x3694),
    ItemName.NamineSketches:      ItemData(1, 368, 0x3642),
    ItemName.CastleKey:           ItemData(2, 460, 0x365D),  # dummy 13
    ItemName.BattlefieldsofWar:   ItemData(2, 54, 0x35AE),
    ItemName.SwordoftheAncestor:  ItemData(2, 55, 0x35AF),
    ItemName.BeastsClaw:          ItemData(2, 59, 0x35B3),
    ItemName.BoneFist:            ItemData(2, 60, 0x35B4),
    ItemName.ProudFang:           ItemData(2, 61, 0x35B5),
    ItemName.SkillandCrossbones:  ItemData(2, 62, 0x35B6),
    ItemName.Scimitar:            ItemData(2, 72, 0x35C0),
    ItemName.MembershipCard:      ItemData(2, 369, 0x3643),
    ItemName.IceCream:            ItemData(3, 375, 0x3649),
    # Changed to 3 instead of one poster, picture and ice cream respectively
    ItemName.WaytotheDawn:        ItemData(2, 73, 0x35C1),
    # currently first visit locking doesn't work for twtnw.When goa is updated should be 2
    ItemName.IdentityDisk:        ItemData(2, 74, 0x35C2),
    ItemName.TornPages:           ItemData(5, 32, 0x3598),

}
Forms_Table = {
    ItemName.ValorForm:  ItemData(1, 26, 0x36C0, 1),
    ItemName.WisdomForm: ItemData(1, 27, 0x36C0, 2),
    ItemName.LimitForm:  ItemData(1, 563, 0x36CA, 3),
    ItemName.MasterForm: ItemData(1, 31, 0x36C0, 6),
    ItemName.FinalForm:  ItemData(1, 29, 0x36C0, 4),
    ItemName.AntiForm:   ItemData(1, 30, 0x36C0, 5)
}
Magic_Table = {
    ItemName.FireElement:     ItemData(3, 21, 0x3594),
    ItemName.BlizzardElement: ItemData(3, 22, 0x3595),
    ItemName.ThunderElement:  ItemData(3, 23, 0x3596),
    ItemName.CureElement:     ItemData(3, 24, 0x3597),
    ItemName.MagnetElement:   ItemData(3, 87, 0x35CF),
    ItemName.ReflectElement:  ItemData(3, 88, 0x35D0),
}
Summon_Table = {
    ItemName.Genie:         ItemData(1, 159, 0x36C4, 4),
    ItemName.PeterPan:      ItemData(1, 160, 0x36C4, 5),
    ItemName.Stitch:        ItemData(1, 25, 0x36C0, 0),
    ItemName.ChickenLittle: ItemData(1, 383, 0x36C0, 3),
}
Movement_Table = {
    ItemName.HighJump:    ItemData(4, 94, 0x05E, ability=True),
    ItemName.QuickRun:    ItemData(4, 98, 0x062, ability=True),
    ItemName.DodgeRoll:   ItemData(4, 564, 0x234, ability=True),
    ItemName.AerialDodge: ItemData(4, 102, 0x066, ability=True),
    ItemName.Glide:       ItemData(4, 106, 0x06A, ability=True),
}

Keyblade_Table = {
    ItemName.Oathkeeper:      ItemData(1, 42, 0x35A2),
    ItemName.Oblivion:        ItemData(1, 43, 0x35A3),
    ItemName.StarSeeker:      ItemData(1, 480, 0x367B),
    ItemName.HiddenDragon:    ItemData(1, 481, 0x367C),
    ItemName.HerosCrest:      ItemData(1, 484, 0x367F),
    ItemName.Monochrome:      ItemData(1, 485, 0x3680),
    ItemName.FollowtheWind:   ItemData(1, 486, 0x3681),
    ItemName.CircleofLife:    ItemData(1, 487, 0x3682),
    ItemName.PhotonDebugger:  ItemData(1, 488, 0x3683),
    ItemName.GullWing:        ItemData(1, 489, 0x3684),
    ItemName.RumblingRose:    ItemData(1, 490, 0x3685),
    ItemName.GuardianSoul:    ItemData(1, 491, 0x3686),
    ItemName.WishingLamp:     ItemData(1, 492, 0x3687),
    ItemName.DecisivePumpkin: ItemData(1, 493, 0x3688),
    ItemName.SleepingLion:    ItemData(1, 494, 0x3689),
    ItemName.SweetMemories:   ItemData(1, 495, 0x368A),
    ItemName.MysteriousAbyss: ItemData(1, 496, 0x368B),
    ItemName.TwoBecomeOne:    ItemData(1, 543, 0x3698),
    ItemName.FatalCrest:      ItemData(1, 497, 0x368C),
    ItemName.BondofFlame:     ItemData(1, 498, 0x368D),
    ItemName.Fenrir:          ItemData(1, 499, 0x368E),
    ItemName.UltimaWeapon:    ItemData(1, 500, 0x368F),
    ItemName.WinnersProof:    ItemData(1, 544, 0x3699),
    ItemName.Pureblood:       ItemData(1, 71, 0x35BF),
}
Staffs_Table = {
    ItemName.Centurion2:        ItemData(1, 546, 0x369B),
    ItemName.MeteorStaff:       ItemData(1, 150, 0x35F1),
    ItemName.NobodyLance:       ItemData(1, 155, 0x35F6),
    ItemName.PreciousMushroom:  ItemData(1, 549, 0x369E),
    ItemName.PreciousMushroom2: ItemData(1, 550, 0x369F),
    ItemName.PremiumMushroom:   ItemData(1, 551, 0x36A0),
    ItemName.RisingDragon:      ItemData(1, 154, 0x35F5),
    ItemName.SaveTheQueen2:     ItemData(1, 503, 0x3692),
    ItemName.ShamansRelic:      ItemData(1, 156, 0x35F7),
}
Shields_Table = {
    ItemName.AkashicRecord:     ItemData(1, 146, 0x35ED),
    ItemName.FrozenPride2:      ItemData(1, 553, 0x36A2),
    ItemName.GenjiShield:       ItemData(1, 145, 0x35EC),
    ItemName.MajesticMushroom:  ItemData(1, 556, 0x36A5),
    ItemName.MajesticMushroom2: ItemData(1, 557, 0x36A6),
    ItemName.NobodyGuard:       ItemData(1, 147, 0x35EE),
    ItemName.OgreShield:        ItemData(1, 141, 0x35E8),
    ItemName.SaveTheKing2:      ItemData(1, 504, 0x3693),
    ItemName.UltimateMushroom:  ItemData(1, 558, 0x36A7),
}
Accessory_Table = {
    ItemName.AbilityRing:     ItemData(1, 8, 0x3587),
    ItemName.EngineersRing:   ItemData(1, 9, 0x3588),
    ItemName.TechniciansRing: ItemData(1, 10, 0x3589),
    ItemName.SkillRing:       ItemData(1, 38, 0x359F),
    ItemName.SkillfulRing:    ItemData(1, 39, 0x35A0),
    ItemName.ExpertsRing:     ItemData(1, 11, 0x358A),
    ItemName.MastersRing:     ItemData(1, 34, 0x359B),
    ItemName.CosmicRing:      ItemData(1, 52, 0x35AD),
    ItemName.ExecutivesRing:  ItemData(1, 599, 0x36B5),
    ItemName.SardonyxRing:    ItemData(1, 12, 0x358B),
    ItemName.TourmalineRing:  ItemData(1, 13, 0x358C),
    ItemName.AquamarineRing:  ItemData(1, 14, 0x358D),
    ItemName.GarnetRing:      ItemData(1, 15, 0x358E),
    ItemName.DiamondRing:     ItemData(1, 16, 0x358F),
    ItemName.SilverRing:      ItemData(1, 17, 0x3590),
    ItemName.GoldRing:        ItemData(1, 18, 0x3591),
    ItemName.PlatinumRing:    ItemData(1, 19, 0x3592),
    ItemName.MythrilRing:     ItemData(1, 20, 0x3593),
    ItemName.OrichalcumRing:  ItemData(1, 28, 0x359A),
    ItemName.SoldierEarring:  ItemData(1, 40, 0x35A6),
    ItemName.FencerEarring:   ItemData(1, 46, 0x35A7),
    ItemName.MageEarring:     ItemData(1, 47, 0x35A8),
    ItemName.SlayerEarring:   ItemData(1, 48, 0x35AC),
    ItemName.Medal:           ItemData(1, 53, 0x35B0),
    ItemName.MoonAmulet:      ItemData(1, 35, 0x359C),
    ItemName.StarCharm:       ItemData(1, 36, 0x359E),
    ItemName.CosmicArts:      ItemData(1, 56, 0x35B1),
    ItemName.ShadowArchive:   ItemData(1, 57, 0x35B2),
    ItemName.ShadowArchive2:  ItemData(1, 58, 0x35B7),
    ItemName.FullBloom:       ItemData(1, 64, 0x35B9),
    ItemName.FullBloom2:      ItemData(1, 66, 0x35BB),
    ItemName.DrawRing:        ItemData(1, 65, 0x35BA),
    ItemName.LuckyRing:       ItemData(1, 63, 0x35B8),
}
Armor_Table = {
    ItemName.ElvenBandana:     ItemData(1, 67, 0x35BC),
    ItemName.DivineBandana:    ItemData(1, 68, 0x35BD),
    ItemName.ProtectBelt:      ItemData(1, 78, 0x35C7),
    ItemName.GaiaBelt:         ItemData(1, 79, 0x35CA),
    ItemName.PowerBand:        ItemData(1, 69, 0x35BE),
    ItemName.BusterBand:       ItemData(1, 70, 0x35C6),
    ItemName.CosmicBelt:       ItemData(1, 111, 0x35D1),
    ItemName.FireBangle:       ItemData(1, 173, 0x35D7),
    ItemName.FiraBangle:       ItemData(1, 174, 0x35D8),
    ItemName.FiragaBangle:     ItemData(1, 197, 0x35D9),
    ItemName.FiragunBangle:    ItemData(1, 284, 0x35DA),
    ItemName.BlizzardArmlet:   ItemData(1, 286, 0x35DC),
    ItemName.BlizzaraArmlet:   ItemData(1, 287, 0x35DD),
    ItemName.BlizzagaArmlet:   ItemData(1, 288, 0x35DE),
    ItemName.BlizzagunArmlet:  ItemData(1, 289, 0x35DF),
    ItemName.ThunderTrinket:   ItemData(1, 291, 0x35E2),
    ItemName.ThundaraTrinket:  ItemData(1, 292, 0x35E3),
    ItemName.ThundagaTrinket:  ItemData(1, 293, 0x35E4),
    ItemName.ThundagunTrinket: ItemData(1, 294, 0x35E5),
    ItemName.ShockCharm:       ItemData(1, 132, 0x35D2),
    ItemName.ShockCharm2:      ItemData(1, 133, 0x35D3),
    ItemName.ShadowAnklet:     ItemData(1, 296, 0x35F9),
    ItemName.DarkAnklet:       ItemData(1, 297, 0x35FB),
    ItemName.MidnightAnklet:   ItemData(1, 298, 0x35FC),
    ItemName.ChaosAnklet:      ItemData(1, 299, 0x35FD),
    ItemName.ChampionBelt:     ItemData(1, 305, 0x3603),
    ItemName.AbasChain:        ItemData(1, 301, 0x35FF),
    ItemName.AegisChain:       ItemData(1, 302, 0x3600),
    ItemName.Acrisius:         ItemData(1, 303, 0x3601),
    ItemName.Acrisius2:        ItemData(1, 307, 0x3605),
    ItemName.CosmicChain:      ItemData(1, 308, 0x3606),
    ItemName.PetiteRibbon:     ItemData(1, 306, 0x3604),
    ItemName.Ribbon:           ItemData(1, 304, 0x3602),
    ItemName.GrandRibbon:      ItemData(1, 157, 0x35D4),
}
Usefull_Table = {
    ItemName.MickeyMunnyPouch:  ItemData(1, 535, 0x3695),  # 5000 munny per
    ItemName.OletteMunnyPouch: ItemData(2, 362, 0x363C),  # 2500 munny per
    ItemName.HadesCupTrophy:   ItemData(1, 537, 0x3696),
    ItemName.UnknownDisk:      ItemData(1, 462, 0x365F),
    ItemName.OlympusStone:     ItemData(1, 370, 0x3644),
    ItemName.MaxHPUp:          ItemData(20, 112, 0x3671),  # 470 is DUMMY 23, 112 is Encampment Area Map
    ItemName.MaxMPUp:          ItemData(4, 113, 0x3672),  # 471 is DUMMY 24, 113 is Village Area Map
    ItemName.DriveGaugeUp:     ItemData(6, 114, 0x3673),  # 472 is DUMMY 25, 114 is Cornerstone Hill Map
    ItemName.ArmorSlotUp:      ItemData(3, 116, 0x3674),  # 473 is DUMMY 26, 116 is Lilliput Map
    ItemName.AccessorySlotUp:  ItemData(3, 117, 0x3675),  # 474 is DUMMY 27, 117 is Building Site Map
    ItemName.ItemSlotUp:       ItemData(5, 118, 0x3660),  # 463 is DUMMY 16, 118 is Mickey’s House Map
}
SupportAbility_Table = {
    ItemName.Scan:             ItemData(2, 138, 0x08A, ability=True),
    ItemName.AerialRecovery:   ItemData(1, 158, 0x09E, ability=True),
    ItemName.ComboMaster:      ItemData(1, 539, 0x21B, ability=True),
    ItemName.ComboPlus:        ItemData(3, 162, 0x0A2, ability=True),
    ItemName.AirComboPlus:     ItemData(3, 163, 0x0A3, ability=True),
    ItemName.ComboBoost:       ItemData(2, 390, 0x186, ability=True),
    ItemName.AirComboBoost:    ItemData(2, 391, 0x187, ability=True),
    ItemName.ReactionBoost:    ItemData(3, 392, 0x188, ability=True),
    ItemName.FinishingPlus:    ItemData(3, 393, 0x189, ability=True),
    ItemName.NegativeCombo:    ItemData(2, 394, 0x18A, ability=True),
    ItemName.BerserkCharge:    ItemData(2, 395, 0x18B, ability=True),
    ItemName.DamageDrive:      ItemData(2, 396, 0x18C, ability=True),
    ItemName.DriveBoost:       ItemData(2, 397, 0x18D, ability=True),
    ItemName.FormBoost:        ItemData(3, 398, 0x18E, ability=True),
    ItemName.SummonBoost:      ItemData(1, 399, 0x18F, ability=True),
    ItemName.ExperienceBoost:  ItemData(2, 401, 0x191, ability=True),
    ItemName.Draw:             ItemData(4, 405, 0x195, ability=True),
    ItemName.Jackpot:          ItemData(2, 406, 0x196, ability=True),
    ItemName.LuckyLucky:       ItemData(3, 407, 0x197, ability=True),
    ItemName.DriveConverter:   ItemData(2, 540, 0x21C, ability=True),
    ItemName.FireBoost:        ItemData(2, 408, 0x198, ability=True),
    ItemName.BlizzardBoost:    ItemData(2, 409, 0x199, ability=True),
    ItemName.ThunderBoost:     ItemData(2, 410, 0x19A, ability=True),
    ItemName.ItemBoost:        ItemData(2, 411, 0x19B, ability=True),
    ItemName.MPRage:           ItemData(2, 412, 0x19C, ability=True),
    ItemName.MPHaste:          ItemData(2, 413, 0x19D, ability=True),
    ItemName.MPHastera:        ItemData(2, 421, 0x1A5, ability=True),
    ItemName.MPHastega:        ItemData(1, 422, 0x1A6, ability=True),
    ItemName.Defender:         ItemData(2, 414, 0x19E, ability=True),
    ItemName.DamageControl:    ItemData(2, 542, 0x21E, ability=True),
    ItemName.NoExperience:     ItemData(0, 404, 0x194, ability=True),  # quantity changed to 0 because the player starts with one always.
    ItemName.LightDarkness:    ItemData(1, 541, 0x21D, ability=True),
    ItemName.MagicLock:        ItemData(1, 403, 0x193, ability=True),
    ItemName.LeafBracer:       ItemData(1, 402, 0x192, ability=True),
    ItemName.CombinationBoost: ItemData(1, 400, 0x190, ability=True),
    ItemName.OnceMore:         ItemData(1, 416, 0x1A0, ability=True),
    ItemName.SecondChance:     ItemData(1, 415, 0x19F, ability=True),
}
ActionAbility_Table = {
    ItemName.Guard:            ItemData(1, 82, 0x052, ability=True),
    ItemName.UpperSlash:       ItemData(1, 137, 0x089, ability=True),
    ItemName.HorizontalSlash:  ItemData(1, 271, 0x10F, ability=True),
    ItemName.FinishingLeap:    ItemData(1, 267, 0x10B, ability=True),
    ItemName.RetaliatingSlash: ItemData(1, 273, 0x111, ability=True),
    ItemName.Slapshot:         ItemData(1, 262, 0x106, ability=True),
    ItemName.DodgeSlash:       ItemData(1, 263, 0x107, ability=True),
    ItemName.FlashStep:        ItemData(1, 559, 0x22F, ability=True),
    ItemName.SlideDash:        ItemData(1, 264, 0x108, ability=True),
    ItemName.VicinityBreak:    ItemData(1, 562, 0x232, ability=True),
    ItemName.GuardBreak:       ItemData(1, 265, 0x109, ability=True),
    ItemName.Explosion:        ItemData(1, 266, 0x10A, ability=True),
    ItemName.AerialSweep:      ItemData(1, 269, 0x10D, ability=True),
    ItemName.AerialDive:       ItemData(1, 560, 0x230, ability=True),
    ItemName.AerialSpiral:     ItemData(1, 270, 0x10E, ability=True),
    ItemName.AerialFinish:     ItemData(1, 272, 0x110, ability=True),
    ItemName.MagnetBurst:      ItemData(1, 561, 0x231, ability=True),
    ItemName.Counterguard:     ItemData(1, 268, 0x10C, ability=True),
    ItemName.AutoValor:        ItemData(1, 385, 0x181, ability=True),
    ItemName.AutoWisdom:       ItemData(1, 386, 0x182, ability=True),
    ItemName.AutoLimit:        ItemData(1, 568, 0x238, ability=True),
    ItemName.AutoMaster:       ItemData(1, 387, 0x183, ability=True),
    ItemName.AutoFinal:        ItemData(1, 388, 0x184, ability=True),
    ItemName.AutoSummon:       ItemData(1, 389, 0x185, ability=True),
    ItemName.TrinityLimit:     ItemData(1, 198, 0x0C6, ability=True),
}
Boosts_Table = {
    ItemName.PowerBoost:   ItemData(1, 253, 0x359D),  # 276, 0x3666, market place map
    ItemName.MagicBoost:   ItemData(1, 586, 0x35E0),  # 277, 0x3667, dark rememberance map
    ItemName.DefenseBoost: ItemData(1, 590, 0x35F8),  # 278, 0x3668, depths of remembrance map
    ItemName.APBoost:      ItemData(1, 532, 0x35FE),  # 279, 0x3669, mansion map
}

# These items cannot be in other games so these are done locally in kh2
DonaldAbility_Table = {
    ItemName.DonaldFire:          ItemData(1, 165, 0xA5, ability=True),
    ItemName.DonaldBlizzard:      ItemData(1, 166, 0xA6, ability=True),
    ItemName.DonaldThunder:       ItemData(1, 167, 0xA7, ability=True),
    ItemName.DonaldCure:          ItemData(1, 168, 0xA8, ability=True),
    ItemName.Fantasia:            ItemData(1, 199, 0xC7, ability=True),
    ItemName.FlareForce:          ItemData(1, 200, 0xC8, ability=True),
    ItemName.DonaldMPRage:        ItemData(1, 412, 0x19C, ability=True),  # originally 3 but swapped to 1 because crit checks
    ItemName.DonaldJackpot:       ItemData(1, 406, 0x196, ability=True),
    ItemName.DonaldLuckyLucky:    ItemData(3, 407, 0x197, ability=True),
    ItemName.DonaldFireBoost:     ItemData(2, 408, 0x198, ability=True),
    ItemName.DonaldBlizzardBoost: ItemData(2, 409, 0x199, ability=True),
    ItemName.DonaldThunderBoost:  ItemData(2, 410, 0x19A, ability=True),
    ItemName.DonaldMPHaste:       ItemData(1, 413, 0x19D, ability=True),
    ItemName.DonaldMPHastera:     ItemData(2, 421, 0x1A5, ability=True),
    ItemName.DonaldMPHastega:     ItemData(2, 422, 0x1A6, ability=True),
    ItemName.DonaldAutoLimit:     ItemData(1, 417, 0x1A1, ability=True),
    ItemName.DonaldHyperHealing:  ItemData(2, 419, 0x1A3, ability=True),
    ItemName.DonaldAutoHealing:   ItemData(1, 420, 0x1A4, ability=True),
    ItemName.DonaldItemBoost:     ItemData(1, 411, 0x19B, ability=True),
    ItemName.DonaldDamageControl: ItemData(2, 542, 0x21E, ability=True),
    ItemName.DonaldDraw:          ItemData(1, 405, 0x195, ability=True),
}

GoofyAbility_Table = {
    ItemName.GoofyTornado:       ItemData(1, 423, 0x1A7, ability=True),
    ItemName.GoofyTurbo:         ItemData(1, 425, 0x1A9, ability=True),
    ItemName.GoofyBash:          ItemData(1, 429, 0x1AD, ability=True),
    ItemName.TornadoFusion:      ItemData(1, 201, 0xC9, ability=True),
    ItemName.Teamwork:           ItemData(1, 202, 0xCA, ability=True),
    ItemName.GoofyDraw:          ItemData(1, 405, 0x195, ability=True),
    ItemName.GoofyJackpot:       ItemData(1, 406, 0x196, ability=True),
    ItemName.GoofyLuckyLucky:    ItemData(1, 407, 0x197, ability=True),
    ItemName.GoofyItemBoost:     ItemData(2, 411, 0x19B, ability=True),
    ItemName.GoofyMPRage:        ItemData(2, 412, 0x19C, ability=True),
    ItemName.GoofyDefender:      ItemData(2, 414, 0x19E, ability=True),
    ItemName.GoofyDamageControl: ItemData(1, 542, 0x21E, ability=True),  # originally 3 but swapped to 1 because crit checks
    ItemName.GoofyAutoLimit:     ItemData(1, 417, 0x1A1, ability=True),
    ItemName.GoofySecondChance:  ItemData(1, 415, 0x19F, ability=True),
    ItemName.GoofyOnceMore:      ItemData(1, 416, 0x1A0, ability=True),
    ItemName.GoofyAutoChange:    ItemData(1, 418, 0x1A2, ability=True),
    ItemName.GoofyHyperHealing:  ItemData(2, 419, 0x1A3, ability=True),
    ItemName.GoofyAutoHealing:   ItemData(1, 420, 0x1A4, ability=True),
    ItemName.GoofyMPHaste:       ItemData(1, 413, 0x19D, ability=True),
    ItemName.GoofyMPHastera:     ItemData(1, 421, 0x1A5, ability=True),
    ItemName.GoofyMPHastega:     ItemData(1, 422, 0x1A6, ability=True),
    ItemName.GoofyProtect:       ItemData(2, 596, 0x254, ability=True),
    ItemName.GoofyProtera:       ItemData(2, 597, 0x255, ability=True),
    ItemName.GoofyProtega:       ItemData(2, 598, 0x256, ability=True),

}

Wincon_Table = {
    ItemName.LuckyEmblem: ItemData(kh2id=367, memaddr=0x3641),  # letter item
    ItemName.Victory:     ItemData(kh2id=263, memaddr=0x111),
    ItemName.Bounty:      ItemData(kh2id=461, memaddr=0x365E),  # Dummy 14
    # ItemName.UniversalKey:ItemData(,365,0x363F,0)#Tournament Poster
}

Consumable_Table = {
    ItemName.Potion:            ItemData(1, 127, 0x36B8),  # 1, 0x3580, piglets house map
    ItemName.HiPotion:          ItemData(1, 126, 0x36B9),  # 2, 0x03581, rabbits house map
    ItemName.Ether:             ItemData(1, 128, 0x36BA),  # 3, 0x3582, kangas house map
    ItemName.Elixir:            ItemData(1, 129, 0x36BB),  # 4, 0x3583, spooky cave map
    ItemName.Megalixir:         ItemData(1, 124, 0x36BC),  # 7, 0x3586, starry hill map
    ItemName.Tent:              ItemData(1, 512, 0x36BD),  # 131,0x35E1, savannah map
    ItemName.DriveRecovery:     ItemData(1, 252, 0x36BE),  # 274,0x3664, pride rock map
    ItemName.HighDriveRecovery: ItemData(1, 511, 0x36BF),  # 275,0x3665, oasis map
}

Events_Table = {
    ItemName.HostileProgramEvent,
    ItemName.McpEvent,
    ItemName.ASLarxeneEvent,
    ItemName.DataLarxeneEvent,
    ItemName.BarbosaEvent,
    ItemName.GrimReaper1Event,
    ItemName.GrimReaper2Event,
    ItemName.DataLuxordEvent,
    ItemName.DataAxelEvent,
    ItemName.CerberusEvent,
    ItemName.OlympusPeteEvent,
    ItemName.HydraEvent,
    ItemName.OcPainAndPanicCupEvent,
    ItemName.OcCerberusCupEvent,
    ItemName.HadesEvent,
    ItemName.ASZexionEvent,
    ItemName.DataZexionEvent,
    ItemName.Oc2TitanCupEvent,
    ItemName.Oc2GofCupEvent,
    ItemName.Oc2CupsEvent,
    ItemName.HadesCupEvents,
    ItemName.PrisonKeeperEvent,
    ItemName.OogieBoogieEvent,
    ItemName.ExperimentEvent,
    ItemName.ASVexenEvent,
    ItemName.DataVexenEvent,
    ItemName.ShanYuEvent,
    ItemName.AnsemRikuEvent,
    ItemName.StormRiderEvent,
    ItemName.DataXigbarEvent,
    ItemName.RoxasEvent,
    ItemName.XigbarEvent,
    ItemName.LuxordEvent,
    ItemName.SaixEvent,
    ItemName.XemnasEvent,
    ItemName.ArmoredXemnasEvent,
    ItemName.ArmoredXemnas2Event,
    ItemName.FinalXemnasEvent,
    ItemName.DataXemnasEvent,
    ItemName.ThresholderEvent,
    ItemName.BeastEvent,
    ItemName.DarkThornEvent,
    ItemName.XaldinEvent,
    ItemName.DataXaldinEvent,
    ItemName.TwinLordsEvent,
    ItemName.GenieJafarEvent,
    ItemName.ASLexaeusEvent,
    ItemName.DataLexaeusEvent,
    ItemName.ScarEvent,
    ItemName.GroundShakerEvent,
    ItemName.DataSaixEvent,
    ItemName.HBDemyxEvent,
    ItemName.ThousandHeartlessEvent,
    ItemName.Mushroom13Event,
    ItemName.SephiEvent,
    ItemName.DataDemyxEvent,
    ItemName.CorFirstFightEvent,
    ItemName.CorSecondFightEvent,
    ItemName.TransportEvent,
    ItemName.OldPeteEvent,
    ItemName.FuturePeteEvent,
    ItemName.ASMarluxiaEvent,
    ItemName.DataMarluxiaEvent,
    ItemName.TerraEvent,
    ItemName.TwilightThornEvent,
    ItemName.Axel1Event,
    ItemName.Axel2Event,
    ItemName.DataRoxasEvent,
}
# Items that are prone to duping.
# anchors for checking form keyblade
# Save+32F4 Valor Form Save+339C Master Form Save+33D4 Final Form
# Have to use the kh2id for checking stuff that sora has equipped
# Equipped abilities have an offset of 0x8000 so check for if whatever || whatever+0x8000
CheckDupingItems = {
    "Items":          {
        item_name for keys in [Progression_Table.keys(), Wincon_Table.keys(), Consumable_Table, [ItemName.MickeyMunnyPouch,
                                                                                                 ItemName.OletteMunnyPouch,
                                                                                                 ItemName.HadesCupTrophy,
                                                                                                 ItemName.UnknownDisk,
                                                                                                 ItemName.OlympusStone, ], Boosts_Table.keys()]
        for item_name in keys

    },
    "Magic":          {
        magic for magic in Magic_Table.keys()
    },
    "Bitmask":        {
        item_name for keys in [Forms_Table.keys(), Summon_Table.keys(), Reports_Table.keys()] for item_name in keys
    },
    "Weapons":        {
        "Keyblades": {
            keyblade for keyblade in Keyblade_Table.keys()
        },
        "Staffs":    {
            staff for staff in Staffs_Table.keys()
        },
        "Shields":   {
            shield for shield in Shields_Table.keys()
        }
    },
    "Equipment":      {
        "Accessories": {
            accessory for accessory in Accessory_Table.keys()
        },
        "Armor":       {
            armor for armor in Armor_Table.keys()
        }
    },
    "Stat Increases": {
        ItemName.MaxHPUp,
        ItemName.MaxMPUp,
        ItemName.DriveGaugeUp,
        ItemName.ArmorSlotUp,
        ItemName.AccessorySlotUp,
        ItemName.ItemSlotUp,
    },
    "Abilities":      {
        "Sora":   {
            item_name for keys in [SupportAbility_Table.keys(), ActionAbility_Table.keys(), Movement_Table.keys()] for item_name in keys
        },
        "Donald": {
            donald_ability for donald_ability in DonaldAbility_Table.keys()
        },
        "Goofy":  {
            goofy_ability for goofy_ability in GoofyAbility_Table.keys()
        }
    },
}
progression_set = {
    # abilities
    item_name for keys in [
        Wincon_Table.keys(),
        Progression_Table.keys(),
        Forms_Table.keys(),
        Magic_Table.keys(),
        Summon_Table.keys(),
        Movement_Table.keys(),
        Keyblade_Table.keys(),
        Staffs_Table.keys(),
        Shields_Table.keys(),
        [
            ItemName.AerialRecovery,
            ItemName.ComboMaster,
            ItemName.ComboPlus,
            ItemName.AirComboPlus,
            ItemName.FinishingPlus,
            ItemName.NegativeCombo,
            ItemName.BerserkCharge,
            ItemName.FormBoost,
            ItemName.LightDarkness,
            ItemName.OnceMore,
            ItemName.SecondChance,
            ItemName.Guard,
            ItemName.HorizontalSlash,
            ItemName.FinishingLeap,
            ItemName.Slapshot,
            ItemName.FlashStep,
            ItemName.SlideDash,
            ItemName.GuardBreak,
            ItemName.Explosion,
            ItemName.AerialSweep,
            ItemName.AerialDive,
            ItemName.AerialSpiral,
            ItemName.AerialFinish,
            ItemName.AutoValor,
            ItemName.AutoWisdom,
            ItemName.AutoLimit,
            ItemName.AutoMaster,
            ItemName.AutoFinal,
            ItemName.TrinityLimit,
            ItemName.DriveConverter,
            # Party Limits
            ItemName.FlareForce,
            ItemName.Fantasia,
            ItemName.Teamwork,
            ItemName.TornadoFusion,
            ItemName.HadesCupTrophy],
        Events_Table]
    for item_name in keys
}
party_filler_set = {
    ItemName.GoofyAutoHealing,
    ItemName.GoofyMPHaste,
    ItemName.GoofyMPHastera,
    ItemName.GoofyMPHastega,
    ItemName.GoofyProtect,
    ItemName.GoofyProtera,
    ItemName.GoofyProtega,
    ItemName.GoofyMPRage,
    ItemName.GoofyDefender,
    ItemName.GoofyDamageControl,

    ItemName.DonaldFireBoost,
    ItemName.DonaldBlizzardBoost,
    ItemName.DonaldThunderBoost,
    ItemName.DonaldMPHaste,
    ItemName.DonaldMPHastera,
    ItemName.DonaldMPHastega,
    ItemName.DonaldAutoHealing,
    ItemName.DonaldDamageControl,
    ItemName.DonaldDraw,
    ItemName.DonaldMPRage,
}
useful_set = {item_name for keys in [
    SupportAbility_Table.keys(),
    ActionAbility_Table.keys(),
    DonaldAbility_Table.keys(),
    GoofyAbility_Table.keys(),
    Armor_Table.keys(),
    Usefull_Table.keys(),
    Accessory_Table.keys()]
              for item_name in keys if item_name not in progression_set and item_name not in party_filler_set}

visit_locking_dict = {
    "2VisitLocking":   [
        ItemName.CastleKey,
        ItemName.BattlefieldsofWar,
        ItemName.SwordoftheAncestor,
        ItemName.BeastsClaw,
        ItemName.BoneFist,
        ItemName.ProudFang,
        ItemName.SkillandCrossbones,
        ItemName.Scimitar,
        ItemName.MembershipCard,
        ItemName.IceCream,
        ItemName.WaytotheDawn,
        ItemName.IdentityDisk,
        ItemName.IceCream,
        ItemName.NamineSketches
    ],
    "AllVisitLocking": {
        ItemName.CastleKey:          2,
        ItemName.BattlefieldsofWar:  2,
        ItemName.SwordoftheAncestor: 2,
        ItemName.BeastsClaw:         2,
        ItemName.BoneFist:           2,
        ItemName.ProudFang:          2,
        ItemName.SkillandCrossbones: 2,
        ItemName.Scimitar:           2,
        ItemName.MembershipCard:     2,
        ItemName.WaytotheDawn:       2,
        ItemName.IdentityDisk:       2,
        ItemName.IceCream:           3,
        ItemName.NamineSketches:     1,
    }
}
exclusion_item_table = {
    "StatUps": {
        ItemName.MaxHPUp,
        ItemName.MaxMPUp,
        ItemName.DriveGaugeUp,
        ItemName.ArmorSlotUp,
        ItemName.AccessorySlotUp,
        ItemName.ItemSlotUp,
    },
    "Ability": {
        item_name for keys in [SupportAbility_Table.keys(), ActionAbility_Table.keys(), Movement_Table.keys()] for item_name in keys
    }
}

default_itempool_option = {
    item_name: ItemData.quantity for dic in [Magic_Table, Progression_Table, Summon_Table, Movement_Table, Forms_Table] for item_name, ItemData in dic.items()
}
item_dictionary_table = {
    **Reports_Table,
    **Progression_Table,
    **Forms_Table,
    **Magic_Table,
    **Summon_Table,
    **Armor_Table,
    **Movement_Table,
    **Staffs_Table,
    **Shields_Table,
    **Keyblade_Table,
    **Accessory_Table,
    **Usefull_Table,
    **SupportAbility_Table,
    **ActionAbility_Table,
    **Boosts_Table,
    **Wincon_Table,
    **Boosts_Table,
    **DonaldAbility_Table,
    **GoofyAbility_Table,
    **Consumable_Table
}
filler_items = [ItemName.PowerBoost, ItemName.MagicBoost, ItemName.DefenseBoost, ItemName.APBoost,
                ItemName.Potion, ItemName.HiPotion, ItemName.Ether, ItemName.Elixir, ItemName.Megalixir,
                ItemName.Tent, ItemName.DriveRecovery, ItemName.HighDriveRecovery,
                ]
item_groups: typing.Dict[str, list] = {
    "Drive Form":      [item_name for item_name in Forms_Table.keys()],
    "Growth":          [item_name for item_name in Movement_Table.keys()],
    "Donald Limit":    [ItemName.FlareForce, ItemName.Fantasia],
    "Goofy Limit":     [ItemName.Teamwork, ItemName.TornadoFusion],
    "Magic":           [ItemName.FireElement, ItemName.BlizzardElement,
                        ItemName.ThunderElement,
                        ItemName.CureElement, ItemName.MagnetElement,
                        ItemName.ReflectElement],
    "Summon":          [ItemName.ChickenLittle, ItemName.Genie, ItemName.Stitch,
                        ItemName.PeterPan],
    "Gap Closer":      [ItemName.SlideDash, ItemName.FlashStep],
    "Ground Finisher": [ItemName.GuardBreak, ItemName.Explosion,
                        ItemName.FinishingLeap],
    "Visit Lock":      [item_name for item_name in
                        visit_locking_dict["2VisitLocking"]],
    "Keyblade":        [item_name for item_name in Keyblade_Table.keys()],
    "Fire":            [ItemName.FireElement],
    "Blizzard":        [ItemName.BlizzardElement],
    "Thunder":         [ItemName.ThunderElement],
    "Cure":            [ItemName.CureElement],
    "Magnet":          [ItemName.MagnetElement],
    "Reflect":         [ItemName.ReflectElement],
    "Proof":           [ItemName.ProofofNonexistence, ItemName.ProofofPeace,
                        ItemName.ProofofConnection],
    "hitlist":         [ItemName.Bounty],
}
