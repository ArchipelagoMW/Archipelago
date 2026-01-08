from .item_data import Items
from .logicCommon import ammo_req, crystal_flash, energy_req, varia_or_hell_run
from .logic_shortcut import LogicShortcut
from .logic_shortcut_data import missileDamage
from .trick_data import Tricks


class BossKill:
    kraid = LogicShortcut(lambda loadout: (
        (Items.GravityBoots in loadout) and
        (missileDamage in loadout) and
        ((Items.Aqua in loadout) or (
            (Tricks.sbj_underwater_w_hjb in loadout) and
            ((Tricks.movement_zoast in loadout) or (
                (Tricks.movement_moderate in loadout) and
                (Items.SpaceJump in loadout)
            ))
        ) or (
            # cheesy did it first try without speedball or aqua or space jump
            (Tricks.movement_zoast in loadout) and
            (Items.HiJump in loadout) and
            (energy_req(459) in loadout)
        ))
    ))

    spore_spawn = LogicShortcut(lambda loadout: (
        (loadout.has_any(Tricks.movement_moderate, Items.HiJump, Items.SpaceJump)) and
        (loadout.has_any(
            Tricks.movement_moderate, energy_req(130), Items.Varia, Items.MetroidSuit, Items.Aqua
        )) and
        (loadout.has_any(missileDamage, Items.Charge))
    ))

    bomb_torizo = LogicShortcut(lambda loadout: (
        True  # if you can get there, you can kill
    ))

    draygon = LogicShortcut(lambda loadout: (
        ((Items.Aqua in loadout) or (
            (Tricks.movement_moderate in loadout) and (energy_req(850) in loadout)
        ) or (
            (Tricks.movement_zoast in loadout) and (energy_req(161) in loadout)
        ) or (
            # hypercharge makes up for not having aqua
            (Items.Charge in loadout) and
            (Items.Hypercharge in loadout)
        )) and
        ((energy_req(850) in loadout) or (
            (Tricks.movement_moderate in loadout) and
            (energy_req(450) in loadout)
        ) or (
            (Tricks.movement_zoast in loadout)
        )) and
        ((
            (Items.Varia in loadout)
        ) or (
            (Items.Charge in loadout) and
            (Items.Hypercharge in loadout)
        ) or (
            (ammo_req(350) in loadout) and
            (Tricks.movement_zoast in loadout) and
            (Items.Screw in loadout) and
            (Items.Aqua in loadout)
        ))
        # TODO: improve this logic

        # joonie did:
        # varia and aqua, no metroid suit
        # 1351 energy, 235 ammo (required luck, 250 probably better - need drops for a 3rd crystal flash from draygon)
        # hypercharge, 6 accel charges
        # screw, speedball, space jump with a few boosts, speed
        # no hi jump, no dark visor, no metroid suit
        #
        # do 1st crystal flash in draygon's room soon after you enter while waiting for fight to start
        # (on left side, turrets often have bad aim)
        # 2nd crystal flash after draygon's dead, waiting for death animation
        # pull in drops with charge for ammo for 3rd crystal flash on the way out
    ))

    dust_torizo = LogicShortcut(lambda loadout: (
        True  # if you're good, you might be able to kill
    ))

    gold_torizo = LogicShortcut(lambda loadout: (
        (varia_or_hell_run(1733, heat_and_metroid_suit_not_required=True) in loadout) and

        # in case CF is needed, need to be able to get up to the item platform
        (loadout.has_any(Items.Varia, Tricks.wall_jump_precise, Items.SpaceJump)) and

        (
            loadout.has_all(Items.Varia, Items.Charge) or
            loadout.has_all(Items.Charge, Items.Hypercharge) or
            (
                loadout.has_all(Items.Charge, Items.Ice, Items.Wave, Items.DamageAmp, Items.AccelCharge) and
                ((Items.Spazer in loadout) or (Items.Plasma in loadout))
            ) or
            loadout.has_all(Items.Super, ammo_req(230), varia_or_hell_run(2460)) or
            loadout.has_all(Items.Super, ammo_req(150), Items.Varia, energy_req(1210)) or
            loadout.has_all(Tricks.patience, Items.Varia, Items.Missile)
        )
    ))

    crocomire = LogicShortcut(lambda loadout: (
        True  # if you can get there (logically), you can kill
    ))

    ridley = LogicShortcut(lambda loadout: (
        # These numbers are all guesses, they might need to be tuned.
        # TODO: Should these numbers depend on accel charge?
        (
            (Items.MetroidSuit in loadout) and
            ((varia_or_hell_run(2001) in loadout) or (
                (Items.Hypercharge in loadout) and  # increases damage of the hyper beam you get from Metroid Suit
                (varia_or_hell_run(1520) in loadout)
            )) and
            ((energy_req(850) in loadout) or (
                (Tricks.movement_moderate in loadout) and
                ((energy_req(650) in loadout) or (
                    (crystal_flash in loadout) and
                    (energy_req(450) in loadout)
                ))
            ) or (
                (Tricks.movement_zoast in loadout) and
                ((energy_req(450) in loadout) or (
                    (crystal_flash in loadout) and
                    (energy_req(350) in loadout)
                ))
            ))
        ) or (
            (Items.Charge in loadout) and
            (Items.Hypercharge in loadout) and
            ((
                (energy_req(480) in loadout) and
                (varia_or_hell_run(680) in loadout)
            ) or (
                (Tricks.movement_moderate in loadout) and
                (energy_req(280) in loadout) and
                (varia_or_hell_run(480) in loadout)
            ) or (
                (Tricks.movement_zoast in loadout) and
                (energy_req(80) in loadout) and
                (varia_or_hell_run(280) in loadout)
                # TODO: test - I did this (no suits), but I had a few accel charges and damage amps.
                # Can it be done with no damage amp or accel charge?
            ))
        )
    ))

    phantoon = LogicShortcut(lambda loadout: (
        (Items.DarkVisor in loadout) and
        (
            (Items.Charge in loadout) or
            (Items.Missile in loadout) or
            ((Items.Super in loadout) and (
                (energy_req(550) in loadout) or
                (Items.Screw in loadout)
            ))
        ) and
        ((Tricks.movement_zoast in loadout) or (
            (Tricks.movement_moderate in loadout) and
            (energy_req(250) in loadout)
        ) or (
            (energy_req(450) in loadout)
        ))
    ))

    hyper_torizo = LogicShortcut(lambda loadout: (

        # doesn't matter because of exit logic
        # ((
        #     (Items.Hypercharge in loadout) and
        #     (Items.Charge in loadout)
        # ) or (
        #     (Items.Charge in loadout) and
        #     (energy_req(
        #         750
        #         if (Tricks.movement_zoast in loadout)
        #         else (
        #             1050
        #             if (Tricks.movement_moderate in loadout)
        #             else 1350
        #         )
        #     ) in loadout)
        # )) and

        # exit
        (Items.Hypercharge in loadout) and
        (Items.Charge in loadout)
    ))

    botwoon = LogicShortcut(lambda loadout: (
        ((
            (missileDamage in loadout) and
            (ammo_req(110) in loadout)  # This is just a guess
        ) or (
            (Items.Charge in loadout)
        )) and
        (loadout.has_any(Tricks.movement_zoast, energy_req(250)))  # don't know how much energy is good
    ))
