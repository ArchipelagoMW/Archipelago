from .connection_data import area_doors
from .item_data import Items, items_unpackable
from .logic_shortcut import LogicShortcut
from .logicCommon import ammo_req, can_bomb, can_use_pbs
from .trick_data import Tricks

(
    Missile, Super, PowerBomb, Morph, GravityBoots, Speedball, Bombs, HiJump,
    Aqua, DarkVisor, Wave, SpeedBooster, Spazer, Varia, Ice, Grapple,
    MetroidSuit, Plasma, Screw, Hypercharge, Charge, Xray, SpaceJump, Energy,
    Refuel, SmallAmmo, LargeAmmo, DamageAmp, AccelCharge, SpaceJumpBoost,
    spaceDrop
) = items_unpackable

canFly = LogicShortcut(lambda loadout: (
    (GravityBoots in loadout) and (
        (SpaceJump in loadout) or (Tricks.infinite_bomb_jump in loadout)
    )
))
shootThroughWalls = LogicShortcut(lambda loadout: (
    (Wave in loadout) or ((Charge in loadout) and (Hypercharge in loadout))
))
breakIce = LogicShortcut(lambda loadout: (
    (Plasma in loadout) or ((Charge in loadout) and (Hypercharge in loadout))
))
missileDamage = LogicShortcut(lambda loadout: (
    loadout.has_any(Missile, Super)
))
pinkDoor = LogicShortcut(lambda loadout: (
    missileDamage in loadout
))
pinkSwitch = LogicShortcut(lambda loadout: (
    missileDamage in loadout
))
missileBarrier = LogicShortcut(lambda loadout: (
    (missileDamage in loadout) or loadout.has_all(Charge, Hypercharge)
))
icePod = LogicShortcut(lambda loadout: (
    ((Ice in loadout) and (missileDamage in loadout)) or ((Charge in loadout) and (Hypercharge in loadout))
))

electricHyper = LogicShortcut(lambda loadout: (
    (MetroidSuit in loadout) or (
        (Charge in loadout) and
        (Hypercharge in loadout)
    )
))
""" hyper beam when electricity is available """

plasmaWaveGate = LogicShortcut(lambda loadout: (
    ((Plasma in loadout) and (Wave in loadout)) or
    ((Hypercharge in loadout) and (Charge in loadout))
))
""" the switches that are blocked by plasma+wave barriers """

iceSBA = LogicShortcut(lambda loadout: (
    loadout.has_all(Ice, Charge, PowerBomb)
))

plasmaSBA = LogicShortcut(lambda loadout: (
    loadout.has_all(Plasma, Charge, PowerBomb)
))

spazerSBA = LogicShortcut(lambda loadout: (
    loadout.has_all(Spazer, Charge, PowerBomb)
))

hiJumpSuperSink = LogicShortcut(lambda loadout: (
    (Tricks.super_sink_hard in loadout) and
    (HiJump in loadout) and
    (
        (Tricks.patience in loadout) or
        (Xray in loadout) or
        (Tricks.movement_zoast in loadout)
    )
))
""" hi jump and not bonking ceiling """

bonkCeilingSuperSink = LogicShortcut(lambda loadout: (
    (Tricks.super_sink_hard in loadout) and
    ((Speedball in loadout) or (Tricks.movement_zoast in loadout)) and
    (
        (Tricks.patience in loadout) or
        (Xray in loadout) or
        (Tricks.movement_zoast in loadout)
    )
))
""" bonk ceiling above 4- or 5-tile space """

bonk7SuperSink = LogicShortcut(lambda loadout: (
    (Tricks.super_sink_hard in loadout) and
    (
        (Tricks.patience in loadout) or
        (Xray in loadout) or
        (Tricks.movement_zoast in loadout)
    )
))
""" bonk ceiling above 7-tile space """

underwaterSuperSink = LogicShortcut(lambda loadout: (
    (Tricks.super_sink_hard in loadout) and
    (
        (Tricks.patience in loadout) or
        (Xray in loadout) or
        (Tricks.movement_zoast in loadout)
    ) and False  # TODO: see if this is not that hard and I didn't just happen to fail it 50 times in a row
))
""" no bonk, no Aqua Suit, no hi jump """

killRippers = LogicShortcut(lambda loadout: (
    (Super in loadout) or
    (can_use_pbs(1) in loadout) or
    (Screw in loadout) or
    loadout.has_all(Charge, Hypercharge)
))
""" GET OUT OF MY WAY!! """


def killGreenOrRedPirates(super_count: int) -> LogicShortcut:
    return LogicShortcut(lambda loadout: (
        (Missile in loadout) or
        ((Super in loadout) and (ammo_req(super_count * 5) in loadout)) or
        (Charge in loadout) or
        (Ice in loadout) or
        (Wave in loadout) or
        (Plasma in loadout) or
        (can_bomb(1) in loadout) or
        (Spazer in loadout) or
        (Screw in loadout)
    ))


killYellowPirates = LogicShortcut(lambda loadout: (
    (Charge in loadout) or
    (Missile in loadout) or
    ((Super in loadout) and (ammo_req(15) in loadout)) or
    (can_use_pbs(3) in loadout) or
    (Screw in loadout) or
    ((Morph in loadout) and (Bombs in loadout) and (Tricks.patience in loadout))
))

# game objectives

can_fall_from_spaceport = LogicShortcut(lambda loadout: (
    loadout.has_any(Items.Morph, Items.Missile, shootThroughWalls, Items.Super, Tricks.wave_gate_glitch)
))

can_crash_spaceport = LogicShortcut(lambda loadout: (
    (
        (Items.spaceDrop not in loadout) and
        (Items.MetroidSuit in loadout) and
        (Items.Super in loadout)
        # This is dangerous because it messes up ocean logic.
    ) or (
        (Items.spaceDrop in loadout) and
        (Items.MetroidSuit in loadout) and
        (Items.Super in loadout) and
        (
            (Items.Grapple in loadout) or
            ((Items.Xray in loadout) and (Tricks.xray_climb in loadout)) or
            ((Items.Ice in loadout) and (Tricks.freeze_hard in loadout) and (Tricks.ice_clip in loadout))  # and super
        ) and
        (area_doors["LoadingDockSecurityAreaL"] in loadout) and
        (Items.GravityBoots in loadout)
    )
))
