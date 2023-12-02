from .Names import ItemName, RegionName, LocationName

# this file contains the dicts,lists and sets used for making rules in rules.py
base_tools = [
    ItemName.FinishingPlus,
    ItemName.Guard,
    ItemName.AerialRecovery
]
gap_closer = [
    ItemName.SlideDash,
    ItemName.FlashStep
]
defensive_tool = [
    ItemName.ReflectElement,
    ItemName.Guard
]
form_list = [
    ItemName.ValorForm,
    ItemName.WisdomForm,
    ItemName.LimitForm,
    ItemName.MasterForm,
    ItemName.FinalForm
]
form_list_without_final = [
    ItemName.ValorForm,
    ItemName.WisdomForm,
    ItemName.LimitForm,
    ItemName.MasterForm
]
ground_finisher = [
    ItemName.GuardBreak,
    ItemName.Explosion,
    ItemName.FinishingLeap
]
party_limit = [
    ItemName.Fantasia,
    ItemName.FlareForce,
    ItemName.Teamwork,
    ItemName.TornadoFusion
]
donald_limit = [
    ItemName.Fantasia,
    ItemName.FlareForce
]
aerial_move = [
    ItemName.AerialDive,
    ItemName.AerialSpiral,
    ItemName.HorizontalSlash,
    ItemName.AerialSweep,
    ItemName.AerialFinish
]
level_3_form_loc = [
    LocationName.Valorlvl3,
    LocationName.Wisdomlvl3,
    LocationName.Limitlvl3,
    LocationName.Masterlvl3,
    LocationName.Finallvl3
]
black_magic = [
    ItemName.FireElement,
    ItemName.BlizzardElement,
    ItemName.ThunderElement
]
magic = [
    ItemName.FireElement,
    ItemName.BlizzardElement,
    ItemName.ThunderElement,
    ItemName.ReflectElement,
    ItemName.CureElement,
    ItemName.MagnetElement
]
summons = [
    ItemName.ChickenLittle,
    ItemName.Stitch,
    ItemName.Genie,
    ItemName.PeterPan
]
three_proofs = [
    ItemName.ProofofConnection,
    ItemName.ProofofPeace,
    ItemName.ProofofNonexistence
]

auto_form_dict = {
    ItemName.FinalForm:  ItemName.AutoFinal,
    ItemName.MasterForm: ItemName.AutoMaster,
    ItemName.LimitForm:  ItemName.AutoLimit,
    ItemName.WisdomForm: ItemName.AutoWisdom,
    ItemName.ValorForm:  ItemName.AutoValor,
}

# could use comprehension for getting a list of the region objects but eh I like this more
drive_form_list = [RegionName.Valor, RegionName.Wisdom, RegionName.Limit, RegionName.Master, RegionName.Final, RegionName.Summon]

easy_data_xigbar_tools = {
    ItemName.FinishingPlus:   1,
    ItemName.Guard:           1,
    ItemName.AerialDive:      1,
    ItemName.HorizontalSlash: 1,
    ItemName.AirComboPlus:    2,
    ItemName.FireElement:     3,
    ItemName.ReflectElement:  3,
}
normal_data_xigbar_tools = {
    ItemName.FinishingPlus:   1,
    ItemName.Guard:           1,
    ItemName.HorizontalSlash: 1,
    ItemName.FireElement:     3,
    ItemName.ReflectElement:  3,
}

easy_data_lex_tools = {
    ItemName.Guard:          1,
    ItemName.FireElement:    3,
    ItemName.ReflectElement: 2,
    ItemName.SlideDash:      1,
    ItemName.FlashStep:      1
}
normal_data_lex_tools = {
    ItemName.Guard:          1,
    ItemName.FireElement:    3,
    ItemName.ReflectElement: 1,
}

easy_data_marluxia_tools = {
    ItemName.Guard:          1,
    ItemName.FireElement:    3,
    ItemName.ReflectElement: 2,
    ItemName.SlideDash:      1,
    ItemName.FlashStep:      1,
    ItemName.AerialRecovery: 1,
}
normal_data_marluxia_tools = {
    ItemName.Guard:          1,
    ItemName.FireElement:    3,
    ItemName.ReflectElement: 1,
    ItemName.AerialRecovery: 1,
}
easy_terra_tools = {
    ItemName.SecondChance:   1,
    ItemName.OnceMore:       1,
    ItemName.SlideDash:      1,
    ItemName.FlashStep:      1,
    ItemName.Explosion:      1,
    ItemName.ComboPlus:      2,
    ItemName.FireElement:    3,
    ItemName.Fantasia:       1,
    ItemName.FlareForce:     1,
    ItemName.ReflectElement: 1,
    ItemName.Guard:          1,
    ItemName.DodgeRoll:      3,
    ItemName.AerialDodge:    3,
    ItemName.Glide:          3
}
normal_terra_tools = {
    ItemName.SlideDash:   1,
    ItemName.FlashStep:   1,
    ItemName.Explosion:   1,
    ItemName.ComboPlus:   2,
    ItemName.Guard:       1,
    ItemName.DodgeRoll:   2,
    ItemName.AerialDodge: 2,
    ItemName.Glide:       2
}
hard_terra_tools = {
    ItemName.Explosion:   1,
    ItemName.ComboPlus:   2,
    ItemName.DodgeRoll:   2,
    ItemName.AerialDodge: 2,
    ItemName.Glide:       2,
    ItemName.Guard:       1
}
easy_data_luxord_tools = {
    ItemName.SlideDash:      1,
    ItemName.FlashStep:      1,
    ItemName.AerialDodge:    2,
    ItemName.Glide:          2,
    ItemName.ReflectElement: 3,
    ItemName.Guard:          1,
}
easy_data_zexion = {
    ItemName.FireElement:    3,
    ItemName.SecondChance:   1,
    ItemName.OnceMore:       1,
    ItemName.Fantasia:       1,
    ItemName.FlareForce:     1,
    ItemName.ReflectElement: 3,
    ItemName.Guard:          1,
    ItemName.SlideDash:      1,
    ItemName.FlashStep:      1,
    ItemName.QuickRun:       3,
}
normal_data_zexion = {
    ItemName.FireElement:    3,
    ItemName.ReflectElement: 3,
    ItemName.Guard:          1,
    ItemName.QuickRun:       3
}
hard_data_zexion = {
    ItemName.FireElement:    2,
    ItemName.ReflectElement: 1,
    ItemName.QuickRun:       2,
}
easy_data_xaldin = {
    ItemName.FireElement:     3,
    ItemName.AirComboPlus:    2,
    ItemName.FinishingPlus:   1,
    ItemName.Guard:           1,
    ItemName.ReflectElement:  3,
    ItemName.FlareForce:      1,
    ItemName.Fantasia:        1,
    ItemName.HighJump:        3,
    ItemName.AerialDodge:     3,
    ItemName.Glide:           3,
    ItemName.MagnetElement:   1,
    ItemName.HorizontalSlash: 1,
    ItemName.AerialDive:      1,
    ItemName.AerialSpiral:    1,
    ItemName.BerserkCharge:   1
}
normal_data_xaldin = {
    ItemName.FireElement:     3,
    ItemName.FinishingPlus:   1,
    ItemName.Guard:           1,
    ItemName.ReflectElement:  3,
    ItemName.FlareForce:      1,
    ItemName.Fantasia:        1,
    ItemName.HighJump:        3,
    ItemName.AerialDodge:     3,
    ItemName.Glide:           3,
    ItemName.MagnetElement:   1,
    ItemName.HorizontalSlash: 1,
    ItemName.AerialDive:      1,
    ItemName.AerialSpiral:    1,
}
hard_data_xaldin = {
    ItemName.FireElement:   2,
    ItemName.FinishingPlus: 1,
    ItemName.Guard:         1,
    ItemName.HighJump:      2,
    ItemName.AerialDodge:   2,
    ItemName.Glide:         2,
    ItemName.MagnetElement: 1,
    ItemName.AerialDive:    1
}
easy_data_larxene = {
    ItemName.FireElement:    3,
    ItemName.SecondChance:   1,
    ItemName.OnceMore:       1,
    ItemName.Fantasia:       1,
    ItemName.FlareForce:     1,
    ItemName.ReflectElement: 3,
    ItemName.Guard:          1,
    ItemName.SlideDash:      1,
    ItemName.FlashStep:      1,
    ItemName.AerialDodge:    3,
    ItemName.Glide:          3,
    ItemName.GuardBreak:     1,
    ItemName.Explosion:      1
}
normal_data_larxene = {
    ItemName.FireElement:    3,
    ItemName.ReflectElement: 3,
    ItemName.Guard:          1,
    ItemName.AerialDodge:    3,
    ItemName.Glide:          3,
}
hard_data_larxene = {
    ItemName.FireElement:    2,
    ItemName.ReflectElement: 1,
    ItemName.Guard:          1,
    ItemName.AerialDodge:    2,
    ItemName.Glide:          2,
}
easy_data_vexen = {
    ItemName.FireElement:    3,
    ItemName.SecondChance:   1,
    ItemName.OnceMore:       1,
    ItemName.Fantasia:       1,
    ItemName.FlareForce:     1,
    ItemName.ReflectElement: 3,
    ItemName.Guard:          1,
    ItemName.SlideDash:      1,
    ItemName.FlashStep:      1,
    ItemName.AerialDodge:    3,
    ItemName.Glide:          3,
    ItemName.GuardBreak:     1,
    ItemName.Explosion:      1,
    ItemName.DodgeRoll:      3,
    ItemName.QuickRun:       3,
}
normal_data_vexen = {
    ItemName.FireElement:    3,
    ItemName.ReflectElement: 3,
    ItemName.Guard:          1,
    ItemName.AerialDodge:    3,
    ItemName.Glide:          3,
    ItemName.DodgeRoll:      3,
    ItemName.QuickRun:       3,
}
hard_data_vexen = {
    ItemName.FireElement:    2,
    ItemName.ReflectElement: 1,
    ItemName.Guard:          1,
    ItemName.AerialDodge:    2,
    ItemName.Glide:          2,
    ItemName.DodgeRoll:      3,
    ItemName.QuickRun:       3,
}
easy_thousand_heartless_rules = {
    ItemName.SecondChance:  1,
    ItemName.OnceMore:      1,
    ItemName.Guard:         1,
    ItemName.MagnetElement: 2,
}
normal_thousand_heartless_rules = {
    ItemName.LimitForm: 1,
    ItemName.Guard:     1,
}
easy_data_demyx = {
    ItemName.FormBoost:      1,
    ItemName.ReflectElement: 2,
    ItemName.FireElement:    3,
    ItemName.FlareForce:     1,
    ItemName.Guard:          1,
    ItemName.SecondChance:   1,
    ItemName.OnceMore:       1,
    ItemName.FinishingPlus:  1,
}
normal_data_demyx = {
    ItemName.ReflectElement: 2,
    ItemName.FireElement:    3,
    ItemName.FlareForce:     1,
    ItemName.Guard:          1,
    ItemName.FinishingPlus:  1,
}
hard_data_demyx = {
    ItemName.ReflectElement: 1,
    ItemName.FireElement:    2,
    ItemName.FlareForce:     1,
    ItemName.Guard:          1,
    ItemName.FinishingPlus:  1,
}
easy_sephiroth_tools = {
    ItemName.Guard:          1,
    ItemName.ReflectElement: 3,
    ItemName.SlideDash:      1,
    ItemName.FlashStep:      1,
    ItemName.GuardBreak:     1,
    ItemName.Explosion:      1,
    ItemName.DodgeRoll:      3,
    ItemName.FinishingPlus:  1,
    ItemName.SecondChance:   1,
    ItemName.OnceMore:       1,
}
normal_sephiroth_tools = {
    ItemName.Guard:          1,
    ItemName.ReflectElement: 2,
    ItemName.SlideDash:      1,
    ItemName.FlashStep:      1,
    ItemName.GuardBreak:     1,
    ItemName.Explosion:      1,
    ItemName.DodgeRoll:      3,
    ItemName.FinishingPlus:  1,
}
hard_sephiroth_tools = {
    ItemName.Guard:          1,
    ItemName.ReflectElement: 1,
    ItemName.DodgeRoll:      2,
    ItemName.FinishingPlus:  1,
}

not_hard_cor_tools_dict = {
    ItemName.ReflectElement: 3,
    ItemName.Stitch:         1,
    ItemName.ChickenLittle:  1,
    ItemName.MagnetElement:  2,
    ItemName.Explosion:      1,
    ItemName.FinishingLeap:  1,
    ItemName.ThunderElement: 2,
}
transport_tools_dict = {
    ItemName.ReflectElement: 3,
    ItemName.Stitch:         1,
    ItemName.ChickenLittle:  1,
    ItemName.MagnetElement:  2,
    ItemName.Explosion:      1,
    ItemName.FinishingLeap:  1,
    ItemName.ThunderElement: 3,
    ItemName.Fantasia:       1,
    ItemName.FlareForce:     1,
    ItemName.Genie:          1,
}
easy_data_saix = {
    ItemName.Guard:           1,
    ItemName.SlideDash:       1,
    ItemName.FlashStep:       1,
    ItemName.ThunderElement:  1,
    ItemName.BlizzardElement: 1,
    ItemName.FlareForce:      1,
    ItemName.Fantasia:        1,
    ItemName.FireElement:     3,
    ItemName.ReflectElement:  3,
    ItemName.GuardBreak:      1,
    ItemName.Explosion:       1,
    ItemName.AerialDodge:     3,
    ItemName.Glide:           3,
    ItemName.SecondChance:    1,
    ItemName.OnceMore:        1
}
normal_data_saix = {
    ItemName.Guard:           1,
    ItemName.ThunderElement:  1,
    ItemName.BlizzardElement: 1,
    ItemName.FireElement:     3,
    ItemName.ReflectElement:  3,
    ItemName.AerialDodge:     3,
    ItemName.Glide:           3,
}
hard_data_saix = {
    ItemName.Guard:           1,
    ItemName.BlizzardElement: 1,
    ItemName.ReflectElement:  1,
    ItemName.AerialDodge:     3,
    ItemName.Glide:           3,
}
easy_data_roxas_tools = {
    ItemName.Guard:          1,
    ItemName.ReflectElement: 3,
    ItemName.SlideDash:      1,
    ItemName.FlashStep:      1,
    ItemName.GuardBreak:     1,
    ItemName.Explosion:      1,
    ItemName.DodgeRoll:      3,
    ItemName.FinishingPlus:  1,
    ItemName.SecondChance:   1,
    ItemName.OnceMore:       1,
}
normal_data_roxas_tools = {
    ItemName.Guard:          1,
    ItemName.ReflectElement: 2,
    ItemName.SlideDash:      1,
    ItemName.FlashStep:      1,
    ItemName.GuardBreak:     1,
    ItemName.Explosion:      1,
    ItemName.DodgeRoll:      3,
    ItemName.FinishingPlus:  1,
}
hard_data_roxas_tools = {
    ItemName.Guard:          1,
    ItemName.ReflectElement: 1,
    ItemName.DodgeRoll:      2,
    ItemName.FinishingPlus:  1,
}
easy_data_axel_tools = {
    ItemName.Guard:           1,
    ItemName.ReflectElement:  3,
    ItemName.SlideDash:       1,
    ItemName.FlashStep:       1,
    ItemName.GuardBreak:      1,
    ItemName.Explosion:       1,
    ItemName.DodgeRoll:       3,
    ItemName.FinishingPlus:   1,
    ItemName.SecondChance:    1,
    ItemName.OnceMore:        1,
    ItemName.BlizzardElement: 3,
}
normal_data_axel_tools = {
    ItemName.Guard:           1,
    ItemName.ReflectElement:  2,
    ItemName.SlideDash:       1,
    ItemName.FlashStep:       1,
    ItemName.GuardBreak:      1,
    ItemName.Explosion:       1,
    ItemName.DodgeRoll:       3,
    ItemName.FinishingPlus:   1,
    ItemName.BlizzardElement: 3,
}
hard_data_axel_tools = {
    ItemName.Guard:           1,
    ItemName.ReflectElement:  1,
    ItemName.DodgeRoll:       2,
    ItemName.FinishingPlus:   1,
    ItemName.BlizzardElement: 2,
}
easy_roxas_tools = {
    ItemName.AerialDodge:     1,
    ItemName.Glide:           1,
    ItemName.LimitForm:       1,
    ItemName.ThunderElement:  1,
    ItemName.ReflectElement:  2,
    ItemName.GuardBreak:      1,
    ItemName.SlideDash:       1,
    ItemName.FlashStep:       1,
    ItemName.FinishingPlus:   1,
    ItemName.BlizzardElement: 1
}
normal_roxas_tools = {
    ItemName.ThunderElement:  1,
    ItemName.ReflectElement:  2,
    ItemName.GuardBreak:      1,
    ItemName.SlideDash:       1,
    ItemName.FlashStep:       1,
    ItemName.FinishingPlus:   1,
    ItemName.BlizzardElement: 1
}
easy_xigbar_tools = {
    ItemName.HorizontalSlash: 1,
    ItemName.FireElement:     2,
    ItemName.FinishingPlus:   1,
    ItemName.Glide:           2,
    ItemName.AerialDodge:     2,
    ItemName.QuickRun:        2,
    ItemName.ReflectElement:  1,
    ItemName.Guard:           1,
}
normal_xigbar_tools = {
    ItemName.FireElement:    2,
    ItemName.FinishingPlus:  1,
    ItemName.Glide:          2,
    ItemName.AerialDodge:    2,
    ItemName.QuickRun:       2,
    ItemName.ReflectElement: 1,
    ItemName.Guard:          1
}
easy_luxord_tools = {
    ItemName.AerialDodge:    1,
    ItemName.Glide:          1,
    ItemName.QuickRun:       2,
    ItemName.Guard:          1,
    ItemName.ReflectElement: 2,
    ItemName.SlideDash:      1,
    ItemName.FlashStep:      1,
    ItemName.LimitForm:      1,
}
normal_luxord_tools = {
    ItemName.AerialDodge:    1,
    ItemName.Glide:          1,
    ItemName.QuickRun:       2,
    ItemName.Guard:          1,
    ItemName.ReflectElement: 2,
}
easy_saix_tools = {
    ItemName.AerialDodge:    1,
    ItemName.Glide:          1,
    ItemName.QuickRun:       2,
    ItemName.Guard:          1,
    ItemName.ReflectElement: 2,
    ItemName.SlideDash:      1,
    ItemName.FlashStep:      1,
    ItemName.LimitForm:      1,
}
normal_saix_tools = {
    ItemName.AerialDodge:    1,
    ItemName.Glide:          1,
    ItemName.QuickRun:       2,
    ItemName.Guard:          1,
    ItemName.ReflectElement: 2,
}
easy_xemnas_tools = {
    ItemName.AerialDodge:    1,
    ItemName.Glide:          1,
    ItemName.QuickRun:       2,
    ItemName.Guard:          1,
    ItemName.ReflectElement: 2,
    ItemName.SlideDash:      1,
    ItemName.FlashStep:      1,
    ItemName.LimitForm:      1,
}
normal_xemnas_tools = {
    ItemName.AerialDodge:    1,
    ItemName.Glide:          1,
    ItemName.QuickRun:       2,
    ItemName.Guard:          1,
    ItemName.ReflectElement: 2,
}
easy_data_xemnas = {
    ItemName.ComboMaster:    1,
    ItemName.Slapshot:       1,
    ItemName.ReflectElement: 3,
    ItemName.SlideDash:      1,
    ItemName.FlashStep:      1,
    ItemName.FinishingPlus:  1,
    ItemName.Guard:          1,
    ItemName.TrinityLimit:   1,
    ItemName.SecondChance:   1,
    ItemName.OnceMore:       1,
    ItemName.LimitForm:      1,
}
normal_data_xemnas = {
    ItemName.ComboMaster:    1,
    ItemName.Slapshot:       1,
    ItemName.ReflectElement: 3,
    ItemName.SlideDash:      1,
    ItemName.FlashStep:      1,
    ItemName.FinishingPlus:  1,
    ItemName.Guard:          1,
    ItemName.LimitForm:      1,
}
hard_data_xemnas = {
    ItemName.ComboMaster:    1,
    ItemName.Slapshot:       1,
    ItemName.ReflectElement: 2,
    ItemName.FinishingPlus:  1,
    ItemName.Guard:          1,
    ItemName.LimitForm:      1,
}
final_leveling_access = {
    LocationName.MemorysSkyscaperMythrilCrystal,
    LocationName.GrimReaper2,
    LocationName.Xaldin,
    LocationName.StormRider,
    LocationName.SunsetTerraceAbilityRing
}

multi_form_region_access = {
    ItemName.CastleKey,
    ItemName.BattlefieldsofWar,
    ItemName.SwordoftheAncestor,
    ItemName.BeastsClaw,
    ItemName.BoneFist,
    ItemName.SkillandCrossbones,
    ItemName.Scimitar,
    ItemName.MembershipCard,
    ItemName.IceCream,
    ItemName.WaytotheDawn,
    ItemName.IdentityDisk,
}
limit_form_region_access = {
    ItemName.CastleKey,
    ItemName.BattlefieldsofWar,
    ItemName.SwordoftheAncestor,
    ItemName.BeastsClaw,
    ItemName.BoneFist,
    ItemName.SkillandCrossbones,
    ItemName.Scimitar,
    ItemName.MembershipCard,
    ItemName.IceCream,
    ItemName.WaytotheDawn,
    ItemName.IdentityDisk,
    ItemName.NamineSketches
}
