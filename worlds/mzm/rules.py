"""
Logic rule definitions for Metroid: Zero Mission.

Logic based on MZM Randomizer, by Biospark and dragonfangs.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from .logic import *
from .tricks import Trick
from worlds.generic.Rules import add_rule

if TYPE_CHECKING:
    from . import MZMWorld


def set_location_rules(world: MZMWorld, locations):
    brinstar_start = {
            "Brinstar Morph Ball": None,
            "Brinstar Morph Ball Cannon": CanBallCannon,
            "Brinstar Ceiling E-Tank": any(
                all(
                    IceBeam,
                    any(
                        RidleyBoss,
                        HardMode
                    )
                ),
                CanFly,
                Trick("Brinstar Ceiling E-Tank Tricky Spark")
            ),
        }

    brinstar_main = {
            "Brinstar Long Beam": all(
                MorphBall,
                any(
                    CanLongBeam(2),
                    LayoutPatches("brinstar_long_beam_hall"),
                )
            ),
            "Brinstar Main Shaft Left Alcove": all(
                CanSingleBombBlock,
                any(
                    CanFlyWall,
                    IceBeam,
                    CanHiGrip
                )
            ),
            "Brinstar Ballspark": all(
                CanBallspark,
                CanBombTunnelBlock
            ),
            "Brinstar Ripper Climb": any(
                all(
                    PowerGrip,
                    any(
                        all(
                            IceBeam,
                            NormalMode  # On Hard, one Ripper is missing
                        ),
                        CanFlyWall
                    ),
                    any(
                        CanBallJump,
                        CanSingleBombBlock,
                        LayoutPatches("brinstar_top")
                    )
                ),
                CanIBJ,
                Trick("Brinstar Ripper Climb Zoomer Freeze"),
                Trick("Brinstar Ripper Climb Tricky Spark")
            ),
            "Brinstar Speed Booster Shortcut": all(
                any(
                    CanBallspark,
                    all(  # Reverse way
                        NormalLogic,
                        CanBallJump
                    ),
                ),
                CanBombTunnelBlock,
                CanVerticalWall,
            ),
            "Brinstar Worm Drop": all(
                MorphBall,
                Missiles
            ),
            "Brinstar First Missile": MorphBall,
            "Brinstar Behind Hive": all(
                MorphBall,
                Missiles
            ),
            "Brinstar Under Bridge": all(
                Missiles,
                CanSingleBombBlock
            ),
        }

    brinstar_top = {
            "Brinstar Upper Pillar": None
        }

    brinstar_varia_area = {
            "Brinstar Varia Suit": all(
                any(
                    CanHorizontalIBJ,
                    PowerGrip,
                    all(
                        GravitySuit,
                        CanVerticalWall
                    ),
                    all(
                        any(
                            HazardRuns,  # only 99 energy required as you can refill at the Chozo statue
                            VariaSuit
                        ),
                        CanHiWallJump,
                        any(  # The walljump up out of the acid is a little tight but doesn't feel worthy of a trick
                            SpaceJump,
                            NormalLogic
                        )
                    ),
                ),
                any(
                    Bomb,
                    Trick("Brinstar Varia Suit Power Bomb")
                ),
                CanEnterMediumMorphTunnel,
                Missiles
            ),
            "Brinstar Acid Near Varia": all(
                any(
                    CanLongBeam(5),
                    WaveBeam
                ),
                any(
                    VariaSuit,
                    GravitySuit,
                    Trick("Brinstar Acid Near Varia Acid Dive - Normal"),
                    Trick("Brinstar Acid Near Varia Acid Dive - Minimal")
                )
            ),
    }

    brinstar_pasthives = {
            "Brinstar Post-Hive in Wall": None,
            "Brinstar Behind Bombs": all(
                Missiles,
                CanBombTunnelBlock,
                CanBallJump
            ),
            "Brinstar Bomb": Missiles,
            "Brinstar Post-Hive Pillar": None
        }


    kraid_main = {
            "Kraid Save Room Tunnel": CanBombTunnelBlock,
            "Kraid Zipline Morph Jump": any(
                all(
                    Ziplines,
                    CanBallJump
                ),
                Trick("Kraid Zipline Morph Jump Without Ziplines")
            ),
            "Kraid Acid Ballspark": all(
                any(
                    CanIBJ,  # Gravity is required for this item so regular IBJ works, unlike regional access
                    PowerGrip,
                    all(  # A bit of a tight jump and kind of unintuitive
                        CanHiSpringBall,
                        NormalLogic
                    )
                ),
                CanBombTunnelBlock,
                GravitySuit,
                CanBallspark
            ),
            "Kraid Right Hall Pillar": Missiles,
            "Kraid Speed Jump": all(
                Missiles,
                SpeedBooster
            ),
            "Kraid Upper Right Morph Ball Cannon": all(
                Missiles,
                CanBallCannon
            )
        }

    kraid_acidworm_area = {
            "Kraid Under Acid Worm": all(
                Missiles,
                any(
                    NormalCombat,
                    all(
                        MissileTanks(5),
                        EnergyTanks(1)
                    )
                ),
                CanSingleBombBlock,
                CanVerticalWall
            ),
            "Kraid Zipline Activator Room": None,
            "Kraid Zipline Activator": None
        }

    # past the long acid pool
    kraid_left_shaft = {
            "Kraid Behind Giant Hoppers": CanEnterHighMorphTunnel,
            "Kraid Quad Ball Cannon Room": any(
                all(
                    CanBombTunnelBlock,
                    Ziplines,
                    Missiles
                ),
                Trick("Kraid Quad Ball Cannon No Bombs"),
                Trick("Kraid Quad Ball Cannon Crumble Grip"),
            ),
            "Kraid Unknown Item Statue": all(
                any(
                    Bomb,
                    PowerBombCount(4),  # nowhere good to refill PBs between elevator shaft and here
                    ScrewAttack,
                    Trick("Kraid Unknown Item Spaceboost"),  # 3 PBs
                    Trick("Kraid Unknown Item With 2 PBs"),  # 2 PBs
                ),
                any(  # To enter the morph tunnel to leave after getting the item on the statue
                    PowerGrip,
                    CanHiSpringBall,
                    CanIBJ,
                    all(
                        IceBeam,
                        CanBallJump
                    )
                )
            )
        }

    kraid_bottom = {
            "Kraid Speed Booster": any(
                KraidBoss,
                all(
                    NormalLogic,
                    SpeedBooster
                )
            ),
            "Kraid Acid Fall": None,
            "Kraid": all(
                any(
                    UnknownItem2,
                    all(
                        NormalLogic,
                        SpeedBooster
                    )
                ),
                Missiles,
                KraidCombat,
                any(  # to escape, or to get to the upper door if you take the speed booster exit into the room
                    SpeedBooster,
                    CanHiGrip,
                    CanFlyWall
                ),
                any(  # to escape via the bottom right shaft
                    LayoutPatches("kraid_right_shaft"),
                    SpeedBooster,
                    CanFly,
                    Trick("Kraid Bottom Escape Enemy Freeze"),
                    Trick("Kraid Bottom Escape Get-Around Walljump")
                )
            )
        }

    norfair_main = {
            "Norfair Hallway to Crateria": any(
                PowerGrip,
                CanIBJ,
                all(
                    IceBeam,
                    CanEnterMediumMorphTunnel
                )
            ),
            "Norfair Under Crateria Elevator": all(
                any(
                    CanLongBeam(1),
                    CanBallspark
                ),
                any(
                    CanEnterHighMorphTunnel,
                    Trick("Norfair Under Crateria Elevator Enemy Freeze")
                )
            )
        }

    norfair_right_shaft = {
            "Norfair Big Room": any(
                SpeedBooster,
                CanFly,
                all(
                    IceBeam,
                    CanVerticalWall
                ),
                Trick("Norfair Big Room Walljump")
            )
        }

    norfair_upper_right = {
            "Norfair Ice Beam": all(
                any(
                    CanFly,
                    PowerGrip,
                    all(
                        HazardRuns,
                        CanWallJump
                    ),
                    all(
                        IceBeam,
                        HardMode
                    ),
                    Trick("Norfair Ice Beam Hi-Jump Only")
                ),
                any(  # Escape
                    SuperMissiles,
                    all(
                        any(
                            CanLongBeam(2),
                            WaveBeam
                        ),
                        any(
                            IceBeam,
                            CanFlyWall,
                            CanHiGrip
                        )
                    )
                )
            ),
            "Norfair Heated Room Above Ice Beam": any(
                VariaSuit,
                Trick("Norfair Above Ice Hellrun - Normal"),
                Trick("Norfair Above Ice Hellrun - Minimal"),
            )
        }

    norfair_behind_ice = {
            "Norfair Behind Top Chozo Statue": None,  # TODO Hard has extra considerations
        }

    norfair_under_brinstar_elevator = {
            "Norfair Bomb Trap": all(
                CanReachLocation("Norfair Heated Room Under Brinstar Elevator"),
                any(
                    Bomb,
                    Trick("Norfair Bomb Trap PB Only"),
                    all(
                        PowerBombs,
                        SpaceJump
                    )
                )
            ),
            "Norfair Heated Room Under Brinstar Elevator": all(
                SuperMissiles,
                any(
                    VariaSuit,
                    Trick("Norfair Under Elevator Hellrun - Normal"),
                    Trick("Norfair Under Elevator Hellrun - Minimal")
                )
            ),
    }

    norfair_lowerrightshaft = {
            "Norfair Hi-Jump": Missiles,
        }

    norfair_lowerrightshaft_by_hijump = {
        "Norfair Right Shaft Near Hi-Jump": None
    }

    lower_norfair = {
            "Norfair Lava Dive Left": all(
                MissileCount(7),
                GravitySuit,
                CanFly
            ),
            "Norfair Lava Dive Right": all(
                MissileCount(5),
                any(
                    GravitySuit,
                    Trick("Lower Norfair Lava Dive - Normal"),
                    Trick("Lower Norfair Lava Dive - Minimal")
                ),
                any(
                    CanBombTunnelBlock,
                    WaveBeam
                ),
                any(
                    all(
                        GravitySuit,
                        CanVerticalWall
                    ),
                    PowerGrip,
                    CanHiWallJump
                )
            ),
            "Norfair Wave Beam": MissileCount(4),
            "Norfair Heated Room Below Wave - Left": all(
                CanVerticalWall,
                any(
                    VariaSuit,
                    Trick("Norfair Under Wave Hellrun Left - Normal"),
                    Trick("Norfair Under Wave Hellrun Left - Minimal")
                ),
                any(
                    CanIBJ,
                    CanHiSpringBall,
                    PowerGrip,
                    all(
                        IceBeam,
                        CanBallJump
                    )
                )
            ),
            "Norfair Heated Room Below Wave - Right": all(
                CanVerticalWall,
                any(
                    VariaSuit,
                    Trick("Norfair Under Wave Hellrun Right - Normal"),
                    Trick("Norfair Under Wave Hellrun Right - Minimal")
                )
            ),
        }

    norfair_screwattack = {
            "Norfair Screw Attack": None,
            "Norfair Next to Screw Attack": ScrewAttack,
        }

    norfair_behind_superdoor = {
            "Norfair Behind Lower Super Missile Door - Left": all(
                any(
                    all(
                        CanIBJ,
                        GravitySuit,
                    ),
                    all(
                        SpaceJump,
                        PowerGrip
                    ),
                    all(  # This is a kinda tight and unintuitive walljump but doesn't feel trick-worthy
                        NormalLogic,
                        GravitySuit,
                        CanHiGrip,
                        CanWallJump
                    ),
                    Trick("Norfair Behind Super Door Left Enemy Freeze"),
                    all(
                        HazardRuns,
                        Trick("Balljump to IBJ From Acid"),
                    )
                ),
                any(  # To get out
                    LayoutPatches("norfair_behind_superdoor"),
                    SpeedBooster,
                    CanBallJump
                )
            ),
            "Norfair Behind Lower Super Missile Door - Right": any(
                SpaceJump,
                CanHorizontalIBJ,
                all(
                    CanIBJ,
                    GravitySuit
                ),
                all(
                    IceBeam,
                    CanWallJump
                ),
                all(
                    HiJump,
                    IceBeam,
                ),
                all(
                    GravitySuit,
                    CanHiWallJump
                ),
                all(
                    HazardRuns,
                    Trick("Balljump to IBJ From Acid")
                )
            )
        }

    norfair_bottom = {
            "Norfair Larva Ceiling": CanReachEntrance("Lower Norfair -> Bottom"),
            "Norfair Right Shaft Bottom": any(
                # going from the right "stairs"
                all(
                    any(
                        CanVerticalWall,
                        IceBeam
                    ),
                    CanBallJump
                ),
                # using the shot blocks to the left
                all(
                    NormalLogic,
                    Missiles,
                    PowerGrip,
                    any(
                        CanFlyWall,
                        IceBeam
                    )
                )
            )
        }

    ridley_main = {
            "Ridley Imago Super Missile": all(
                CanVerticalWall,
                any(
                    all(
                        MissileTanks(7),
                        EnergyTanks(1)
                    ),
                    all(
                        NormalCombat,
                        MissileTanks(4),
                    ),
                    all(
                        MinimalCombat,
                        any(
                            MissileTanks(1),
                            SuperMissileCount(8)
                        )
                    ),
                    ChargeBeam
                )
            )
        }

    ridley_left_shaft = {
            "Ridley West Pillar": None,
            "Ridley Fake Floor": any(
                CanBombTunnelBlock,  # the long way
                CanFly,  # the short way
                Trick("Ridley Fake Floor Skip")  # the short way but spicy
            ),
        }

    ridley_sw_puzzle = {
            "Ridley Southwest Puzzle Top": all(
                CanReachLocation("Ridley Southwest Puzzle Bottom"),
                MissileCount(5),
                any(
                    CanWallJump,
                    PowerGrip,
                    SpaceJump
                )
            ),
            "Ridley Southwest Puzzle Bottom": all(
                SpeedBooster,
                MorphBall,
                any(
                    CanIBJ,
                    all(
                        PowerGrip,
                        any(
                            HiJump,
                            SpaceJump,
                            CanWallJump
                        )
                    )
                ),
                Missiles,
                any(
                    PowerGrip,
                    Trick("Ridley Southwest Puzzle Crumble Jump")
                ),
                any(
                    PowerGrip,
                    PowerBombs,
                    all(
                        LongBeam,
                        WaveBeam
                    )
                )
            )
        }

    ridley_right_shaft = {
            "Ridley Long Hall": None,
            "Ridley Northeast Corner": any(
                CanFly,
                all(
                    IceBeam,
                    any(
                        CanWallJump,
                        CanHiGrip
                    )
                ),
                Trick("Ridley Northeast Corner Get-Around Walljump"),
            )
        }

    ridley_right_speed_puzzles = {
            "Ridley Bomb Puzzle": all(
                any(
                    PowerGrip,
                    Trick("Ridley Bomb Puzzle No Grip")
                ),
                any(
                    all(
                        Bomb,
                        any(
                            CanWallJump,
                            SpaceJump
                        )
                    ),
                    Trick("Ridley Bomb Puzzle Power Bombs")
                )
            ),
            "Ridley Speed Jump": all(
                Missiles,
                any(
                    WaveBeam,
                    Trick("Ridley Speed Jump No Wave")
                )
            )
        }

    ridley_central = {
            "Ridley Upper Ball Cannon Puzzle": all(
                any(
                    CanHiSpringBall,
                    CanIBJ,
                    all(
                        PowerGrip,
                        any(
                            CanWallJump,
                            SpaceJump,
                            all(  # A well-placed balljump and well-timed unmorph will grab the ledge
                                NormalLogic,
                                CanBallJump
                            )
                        )
                    )
                ),
                any(
                    CanBallCannon,
                    LayoutPatches("ridley_ballcannon")
                )
            ),
            "Ridley Lower Ball Cannon Puzzle": all(
                any(
                    PowerBombs,
                    PowerGrip,
                    all(
                        WaveBeam,
                        any(
                            CanWallJump,
                            SpaceJump
                        )
                    )
                ),
                any(
                    CanBallCannon,
                    all(
                        LayoutPatches("ridley_ballcannon"),
                        any(
                            HiJump,
                            SpaceJump,
                            CanWallJump
                        )
                    )
                )
            ),
            "Ridley After Sidehopper Hall Upper": None,
            "Ridley After Sidehopper Hall Lower": None,
            "Ridley Center Pillar": any(
                CanWallJump,
                PowerGrip,
                IceBeam,
                SpaceJump,
                CanHorizontalIBJ,
                all(
                    NormalLogic,
                    HiJump
                )
            ),
            "Ridley Ball Room Lower": None,
            "Ridley Ball Room Upper": all(
                SuperMissiles,
                any(
                    CanFlyWall,
                    CanHiGrip
                ),
                any(
                    Bomb,
                    PowerBombCount(3)
                )
            ),
            "Ridley Fake Lava Under Floor": all(
                any(
                    WaveBeam,
                    CanBombTunnelBlock
                ),
                CanEnterHighMorphTunnel
            ),
            "Ridley Under Owls": None,
        }

    ridley_room = {
            "Ridley Behind Unknown Statue": UnknownItem3,
            "Ridley Unknown Item Statue": None,
            "Ridley": UnknownItem3,
        }

    tourian = {
            "Tourian Left of Mother Brain": all(
                ChozoGhostBoss,
                MotherBrainBoss,
                SpeedBooster,
                any(
                    SpaceJump,
                    NormalLogic
                )
            ),
            "Tourian Under Mother Brain": all(
                ChozoGhostBoss,
                MotherBrainBoss,
                SuperMissiles,
                CanEnterMediumMorphTunnel  # to escape
            ),
            "Mother Brain": all(
                IceBeam,
                any(
                    Bomb,  # only bomb can unlatch metroids
                    NormalCombat  # or just don't get hit!
                ),
                MotherBrainCombat,
                any(  # to get through the tunnel right before Mother Brain
                    CanEnterHighMorphTunnel,
                    Trick("Mother Brain Access Wall Jump"),
                    Trick("Mother Brain Access Ice Only")
                ),
                any(  # to get through escape shaft
                    all(
                        NormalMode,
                        CanVertical,
                    ),
                    any(  # Hard mode escape; much tighter time so rules are different
                        SpaceJump,
                        HiJump,
                        all(
                            PowerGrip,
                            CanWallJump
                        ),
                        Trick("Tourian Escape Hard Mode IBJ")
                    ),
                    Trick("Tourian Escape Shinespark")
                ),
                any(  # to get to ship
                    SpeedBooster,
                    CanFly,
                    all(
                        NormalLogic,
                        CanHiWallJump
                    )
                )
            )
        }

    crateria_main = {
            "Crateria Landing Site Ballspark": all(
                CanBallspark,
                PowerBombs,
                any(
                    GravitySuit,
                    CanReachEntrance("Brinstar -> Crateria Ballcannon")  # Room load weirdness
                )
            ),
            "Crateria Moat": None,
            "Crateria Statue Water": UnknownItem1,
            "Crateria Unknown Item Statue": all(
                any(
                    CanVertical,
                    CanBombTunnelBlock
                ),
                CanBallJump
            ),
        }

    crateria_upper_right = {
            "Crateria East Ballspark": all(
                CanBallspark,
                any(
                    CanReachEntrance("Crateria -> Chozodia Upper Door"),
                    CanReachLocation("Crateria Northeast Corner")
                )
            ),
            "Crateria Northeast Corner": all(
                SpeedBooster,
                any(
                    SpaceJump,
                    CanWallJump,
                    Trick("Crateria Northeast Corner Tricky Spark")
                )
            )
        }

    crateria_powergrip = {
        "Crateria Power Grip": None
    }

    chozodia_ruins_crateria_entrance = {
            "Chozodia Upper Crateria Door":
                CanReachEntrance("Crateria -> Chozodia Upper Door"),  # Specifically need to access this entrance, not just the region as it's one-way
            "Chozodia Ruins East of Upper Crateria Door": Missiles,
            "Chozodia Triple Crawling Pirates": all(
                Missiles,
                PowerBombCount(2),  # 2 PBs ALWAYS required at minimum, but you may need many more
                any(
                    all(
                        Bomb,
                        any(
                            NormalMode,
                            PowerBombCount(3)  # on Hard a save room is disabled, so you cannot refill PBs, requiring more
                        )
                    ),
                    PowerBombCount(7),  # Hard, no refills, only PBs, no ability to skip any bomb chains
                    all(
                        NormalMode,
                        PowerBombCount(5),  # no skipping bomb reqs, but with refills
                    ),
                    all(  # Skips one PB on either the slow-crumble morph tunnel or the bomb chain after
                        any(
                            PowerBombCount(6),
                            all(
                                NormalMode,
                                PowerBombCount(4)
                            )
                        ),
                        any(
                            ScrewAttack,
                            WaveBeam,
                            CanFlyWall
                        ),
                        NormalLogic
                    ),
                    all(  # Skips both but still only PBs
                        Trick("Chozo Ghost Access Reverse"),
                        any(
                            ScrewAttack,
                            WaveBeam
                        ),
                        any(
                            PowerBombCount(5),
                            all(
                                NormalMode,
                                PowerBombCount(3)
                            )
                        )
                    ),
                ),
                any(
                    CanHiGrip,
                    CanFlyWall,
                    Trick("Chozodia Pirates Enemy Freezes"),
                ),
                ChozodiaCombat
            )
        }

    chozodia_ruins_test = {
            "Chozodia Chozo Ghost Area Morph Tunnel Above Water": all(
                MissileCount(3),
                CanBallJump,
                any(
                    all(  # Going up through the water
                        any(
                            CanWallJump,
                            all(
                                GravitySuit,
                                CanFly
                            ),
                        ),
                        any(
                            ScrewAttack,
                            NormalLogic  # Skipping the screw attack wall with the missile tunnel
                        )
                    ),
                    Trick("Chozo Ghost Access Reverse"),
                )
            ),
            "Chozodia Chozo Ghost Area Underwater": all(
                Missiles,
                SpeedBooster,
                GravitySuit
            ),
            "Chozodia Chozo Ghost Area Long Shinespark": all(
                Missiles,
                SpeedBooster,
                GravitySuit,
                any(  # IBJ is too slow to keep charge
                    SpaceJump,
                    CanWallJump
                ),
                any(
                    ScrewAttack,
                    Trick("Chozo Ghost Shinespark No Screw")
                )
            ),
            "Chozodia Lava Dive": all(
                any(
                    ScrewAttack,
                    all(
                        Missiles,
                        any(
                            Bomb,
                            PowerBombCount(2)
                        )
                    )
                ),
                any(
                    all(
                        GravitySuit,
                        CanEnterHighMorphTunnel,
                        CanBallJump
                    ),
                    Trick("Chozodia Lava Dive Item - Normal"),
                    Trick("Chozodia Lava Dive Item - Minimal"),
                ),
                any(
                    CanWallJump,
                    all(
                        GravitySuit,
                        CanFly
                    )
                )
            ),
            "Chozodia Ruins Test Reward": CanReachLocation("Chozo Ghost"),
            "Chozo Ghost": all(
                MotherBrainBoss,
                RuinsTestEscape
            ),
        }

    chozodia_under_tube = {
            "Chozodia Bomb Maze": all(
                MorphBall,
                CanBallJump,
                any(
                    CanIBJ,
                    all(
                        PowerGrip,
                        any(
                            HiJump,
                            CanWallJump,
                            SpaceJump
                        )
                    ),
                    all(
                        Trick("Chozodia Under Tube Items Ballspark"),
                        CanHiSpringBall
                    )
                ),
                any(
                    Bomb,
                    PowerBombCount(3)
                )
            ),
            "Chozodia Zoomer Maze": any(
                CanIBJ,
                all(
                    PowerGrip,
                    CanBallJump
                ),
                Trick("Chozodia Under Tube Items Ballspark"),
            ),
            "Chozodia Left of Glass Tube": all(
                SpeedBooster,
                CanReachEntrance("Chozodia Glass Tube -> Chozo Ruins")  # Required to access a save station after collecting to warp if necessary
            ),
            "Chozodia Right of Glass Tube": all(
                PowerBombs,
                any(
                    CanFly,
                    all(
                        NormalLogic,
                        SpeedBooster,
                        CanVerticalWall
                    )
                )
            )
        }

    chozodia_upper_mothership = {
            "Chozodia Pirate Pitfall Trap": all(
                Missiles,
                any(
                    SuperMissiles,
                    all(
                        CanReachEntrance("Chozodia Upper Mothership -> Deep Mothership"),
                        PowerBombs
                    )
                ),
                any(
                    all(
                        CanBombTunnelBlock,
                        CanFlyWall
                    ),
                    all(
                        NormalLogic,  # doable without falling down using screw or by leaving the room then returning
                        CanSingleBombBlock
                    )
                )
            ),
            "Chozodia Behind Workbot": all(
                Missiles,
                any(
                    CanFly,
                    CanHiGrip,
                    CanHiWallJump
                )
            )
        }

    chozodia_lower_mothership = {
            "Chozodia Ceiling Near Map Station": Missiles,
            "Chozodia Southeast Corner in Hull": all(
                any(
                    SuperMissiles,
                    any(
                        Bomb,
                        PowerBombCount(2)
                    ),
                ),
                CanVerticalWall,
                PowerBombs
            )
    }

    chozodia_pb_area = {
            "Chozodia Original Power Bomb": None,
            "Chozodia Next to Original Power Bomb": all(
                any(
                    Bomb,
                    PowerBombCount(3)
                ),
                CanFly
            )
        }

    chozodia_mecha_ridley_hall = {
            "Chozodia Under Mecha Ridley Hallway": SpeedBooster,
            "Mecha Ridley": all(
                MechaRidleyCombat,
                CanEnterHighMorphTunnel,
                CanBallJump,
                PlasmaBeam,  # To defeat black pirates
                ReachedGoal
            ),
            "Chozodia Space Pirate's Ship": MechaRidleyBoss
    }

    access_rules = {
            **brinstar_start,
            **brinstar_main,
            **brinstar_top,
            **brinstar_varia_area,
            **brinstar_pasthives,
            **kraid_main,
            **kraid_acidworm_area,
            **kraid_left_shaft,
            **kraid_bottom,
            **norfair_main,
            **norfair_right_shaft,
            **norfair_upper_right,
            **norfair_behind_ice,
            **norfair_under_brinstar_elevator,
            **norfair_lowerrightshaft,
            **norfair_lowerrightshaft_by_hijump,
            **lower_norfair,
            **norfair_screwattack,
            **norfair_behind_superdoor,
            **norfair_bottom,
            **ridley_main,
            **ridley_left_shaft,
            **ridley_sw_puzzle,
            **ridley_right_shaft,
            **ridley_right_speed_puzzles,
            **ridley_central,
            **ridley_room,
            **tourian,
            **crateria_main,
            **crateria_upper_right,
            **crateria_powergrip,
            **chozodia_ruins_crateria_entrance,
            **chozodia_ruins_test,
            **chozodia_under_tube,
            **chozodia_upper_mothership,
            **chozodia_lower_mothership,
            **chozodia_pb_area,
            **chozodia_mecha_ridley_hall
        }

    for i in locations:
        location = world.multiworld.get_location(i, world.player)

        try:
            if access_rules[i]:
                add_rule(location, access_rules[i].create_rule(world))
        except KeyError:
            continue


# Regional connection requirements

# brinstar main to past-hives, top to past-hives is different
def brinstar_past_hives():
    return all(
        MorphBall,
        Missiles,
        any(
            NormalCombat,
            MissileCount(10),
            SuperMissiles,
            LongBeam,
            ChargeBeam,
            IceBeam,
            WaveBeam,
            PlasmaBeam,
            ScrewAttack
        )
    )


def brinstar_main_to_brinstar_top():
    return any(
        all(
            CanSingleBombBlock,
            CanBallJump
        ),
        Trick("Brinstar Top Access Damage Boost")
    )


def brinstar_pasthives_to_brinstar_top():
    return all(
        any(
            CanFly,
            all(
                IceBeam,
                CanHiWallJump
            )
        ),
        CanBallJump
    )


def brinstar_top_to_varia():
    return all(
        any(
            SpaceJump,
            CanHorizontalIBJ,
            CanHiGrip,
            Trick("Varia Area Access Enemy Freeze"),
            Trick("Varia Area Access Get-Around Walljump"),
            Trick("Varia Area Access Tricky Spark")
        ),
        CanBallJump
    )


# this works for now. it's kind of tricky, cause all you need just to get there is PBs and bombs,
# but to actually do anything (including get to ship) you need IBJ/speed/sj. it only checks for speed
# for now since the only thing you'd potentially need this entrance for is Landing Site Ballspark
# (this assumption changes if/when entrance/elevator rando happens)
def brinstar_crateria_ballcannon():
    return all(
         PowerBombs,
         CanBallCannon,
         CanVerticalWall,
         SpeedBooster
     )


# used for the items in this area as well as determining whether the ziplines can be activated
def kraid_upper_right():
    return all(
        Missiles,
        CanBallCannon,
        any(  # Getting to the top of the right shaft
            CanFlyWall,
            PowerGrip,
            Trick("Kraid Right Shaft Balljump Climb")
        ),
        any(  # Getting up to the top door of the right shaft
            CanVertical,
            Trick("Kraid Right Shaft Enemy Freeze")
        ),
        any(  # Getting through the hole in the next room
            CanHorizontalIBJ,
            PowerGrip,
            all(
                IceBeam,
                CanBallJump
            ),
            all(
                GravitySuit,
                CanIBJ
            ),
            all(
                any(
                    HazardRuns,
                    VariaSuit
                ),
                Trick("Balljump to IBJ From Acid"),
            )
        )
    )


# access to lower kraid
def kraid_left_shaft_access():
    return all(
        any(
            CanHorizontalIBJ,
            PowerGrip,
            all(
                GravitySuit,
                CanIBJ
            ),
            all(
                NormalLogic,
                CanHiSpringBall
            ),
            Trick("Kraid Left Shaft Access Space Jump Only")
        ),
        CanBallJump,
        CanBombTunnelBlock,
        any(
            Ziplines,
            SpaceJump,
            all(
                GravitySuit,
                any(
                    CanIBJ,
                    Trick("Acid Worm Skip Tricky Spark")
                )
            ),
            Trick("Acid Worm Skip Grip Only"),
            Trick("Acid Worm Skip Grip And Bombs"),
            Trick("Acid Worm Skip Bomb Only")
        )
    )


def kraid_left_shaft_to_bottom():
    return UnknownItem2


def kraid_bottom_to_lower_norfair():
    return Trick("Kraid-Norfair Shortcut")


def norfair_main_to_crateria():
    return all(
        MorphBall,
        any(
            CanLongBeam(1),
            CanBallspark
        ),
        any(
            LayoutPatches("crateria_water_speedway"),
            CanEnterMediumMorphTunnel
        )
    )


def norfair_right_shaft_access():
    return any(
        CanVertical,
        SpeedBooster,
        Trick("Norfair Big Room Entrance Enemy Freeze")
    )


def norfair_upper_right_shaft():
    return any(
        CanVerticalWall,
        IceBeam
    )


def norfair_behind_ice_beam():
    return all(
        CanReachLocation("Norfair Ice Beam"),
        any(
            CanLongBeam(2),
            WaveBeam
        ),
        MorphBall,
        any(
            all(
                PowerGrip,
                any(
                    CanWallJump,
                    SpaceJump,
                    IceBeam
                )
            ),
            CanIBJ,
            all(
                IceBeam,
                CanHiSpringBall,
                any(
                    NormalMode,
                    CanWallJump,
                    Trick("Behind Ice Beam Shaft Hard Mode Enemy Freeze")
                )
            )
        )
    )


def norfair_behind_ice_to_bottom():
    return Trick("Norfair-Ridley Shortcut")


def norfair_shaft_to_under_elevator():
    return any(
        SpeedBooster,
        all(
            ScrewAttack,
            any(
                CanFlyWall,
                CanHiGrip
            )
        )
    )


# under elevator to lower right shaft
def norfair_lower_right_shaft():
    LRSByHiJumpRule = norfair_lower_right_shaft_to_lrs_by_hijump()
    LowerNorfairAccess = norfair_lower_right_shaft_to_lower_norfair()
    return any(
        all(
            ScrewAttack,
            any(
                CanFlyWall,
                CanHiGrip
            )
        ),
        all(
            SpeedBooster,
            any(  # escape via ballcannon
                all(
                    LRSByHiJumpRule,
                    any(
                        Missiles,
                        CanVertical
                    ),
                    CanBallCannon,
                ),
                # to reach a save station and warp out
                LowerNorfairAccess
            )
        )
    )


# This region only contains the Lower Right Shaft By Hi-Jump item, and serves a pathfinding purpose
def norfair_lower_right_shaft_to_lrs_by_hijump():
    return all(
        any(
            CanIBJ,
            CanHiGrip,
            all(
                SpaceJump,
                PowerGrip
            ),
            Trick("Norfair Right Shaft Get-Around Walljump")
        ),
        any(  # escape
            CanIBJ,
            all(
                PowerGrip,
                any(
                    SpaceJump,
                    CanWallJump
                )
            ),
            all(
                CanBallCannon,
                any(
                    Missiles,
                    CanVertical
                )
            )
        )
    )


def by_hijump_to_lower_right_shaft():
    return any(
        CanIBJ,
        all(
            MorphBall,
            PowerGrip,
            CanFlyWall
        )
    )


def norfair_lower_shaft_to_under_elevator():
    return all(
        ScrewAttack,
        any(
            CanFlyWall,
            CanHiGrip
        )
    )


def norfair_lower_right_shaft_to_lower_norfair():
    return all(
        Missiles,
        CanBombTunnelBlock,
        any(
            VariaSuit,
            Trick("Norfair Right Shaft to Lower Hellrun - Normal"),
            Trick("Norfair Right Shaft to Lower Hellrun - Minimal")
        ),
        any(  # First heated room
            SpaceJump,
            CanWallJump,
            CanHorizontalIBJ,
            all(
                GravitySuit,
                any(
                    CanHiGrip,
                    CanIBJ
                )
            ),
            all(
                HazardRuns,
                Trick("Balljump to IBJ From Acid"),
            ),
            all(
                CanEnterMediumMorphTunnel,
                CanBallJump,
                any(
                    PowerGrip,
                    all(
                        CanBallJump,
                        NormalLogic  # Slightly tight bomb jump, but you can do it with just one bomb
                    )
                )
            )
        ),
        any(  # Second heated room
            SpaceJump,
            any(
                CanHorizontalIBJ,
                all(
                    GravitySuit,
                    CanIBJ
                )
            ),
            all(
                CanSingleBombBlock,
                SpeedBooster
            )
        )
    )


def lower_norfair_to_screwattack():
    return any(
        all(
            ScrewAttack,
            any(
                CanWallJump,
                SpaceJump
            )
        ),
        all(
            NormalLogic,
            MissileCount(5),
            any(
                CanFlyWall,
                Trick("Screw Attack Access Enemy Freeze")
            )
        ),
        Trick("Screw Attack Access Shinespark")
    )


# This is necessary if your only way to the Screw Attack region is the ballcannon near the Ridley elevator
# e.g. you don't have Varia/hellruns but can take the Ridley shortcut
def screw_to_lower_norfair():
    return any(
        MissileCount(4),
        ScrewAttack
    )


def lower_norfair_to_kraid():
    return all(
        Trick("Kraid-Norfair Shortcut"),
        any(
            CanIBJ,
            PowerGrip,
            CanBallspark,
            all(
                CanSpringBall,
                IceBeam
            )
        )
    )


# The two items in Lower Norfair behind the Super Missile door right under the Screw Attack area
def lower_norfair_to_spaceboost_room():
    return all(
        SuperMissiles,
        any(
            SpeedBooster,
            Bomb,
            PowerBombCount(2),
            all(
                WaveBeam,
                LongBeam,
                any(
                    PowerGrip,
                    all(
                        GravitySuit,
                        CanEnterMediumMorphTunnel
                    )
                )
            )
        ),
        CanVertical
    )


def lower_norfair_to_bottom_norfair():
    return all(
        MissileCount(2),
        SpeedBooster,
        any(
            VariaSuit,
            HazardRuns
        ),
        any(
            WaveBeam,
            Trick("Lower Norfair Wave Beam Skip Tricky Spark"),
            Trick("Lower Norfair Wave Beam Skip With Bombs")
        ),
        any(  # Escape from under the first larva
            CanBallJump,
            LayoutPatches("norfair_larvae_room")
        ),
        CanEnterMediumMorphTunnel,
        any(  # First larva
            WaveBeam,
            PowerBombCount(2),
            all(
                PowerBombs,
                any(
                    PlasmaBeam,
                    Bomb
                )
            ),
            Trick("Norfair Larvae Room Missiles")
        ),
        any(  # Second larva
            PlasmaBeam,
            CanBombTunnelBlock
        )
    )


# Needed for Kraid -> Norfair shortcut, so this rule is for getting to Hi-Jump location from that entrance
def lower_norfair_to_lower_right_shaft():
    return all(
        any(
            PowerGrip,
            HiJump,
            SpaceJump,
            CanWallJump,
            CanHorizontalIBJ,
            all(
                CanIBJ,
                any(
                    IceBeam,
                    GravitySuit
                )
            )
        ),
        CanBombTunnelBlock,
        any(
            VariaSuit,
            Trick("Lower Norfair to Right Shaft Hellrun - Normal"),
            Trick("Lower Norfair to Right Shaft Hellrun - Minimal")
        )
    )


def bottom_norfair_to_lower_shaft_by_hijump():
    return any(
        all(
            Missiles,
            CanReachLocation("Norfair Right Shaft Bottom"),
            any(
                CanBombTunnelBlock,
                WaveBeam
            ),
            CanFlyWall,
        ),
        all(
            NormalLogic,
            SpeedBooster,
            CanFlyWall
        ),
    )


def bottom_norfair_to_right_shaft():
    return SpeedBooster


def bottom_norfair_to_ridley():
    return any(
        PowerBombs,
        all(
            any(
                MissileCount(20),
                SuperMissileCount(8),
                all(
                    NormalCombat,
                    any(
                        MissileTanks(1),
                        SuperMissileCount(6),
                    )
                )
            ),
            any(
                IceBeam,
                SpaceJump,
                NormalLogic  # You can hit the vines without any items, it's just a little tricky
            )
        )
    )


def bottom_norfair_to_screw():
    return all(
        RidleyBoss,
        SpeedBooster,
        any(
            CanBallCannon,
            NormalLogic
        ),
        any(
            IceBeam,
            CanVerticalWall
        )
    )


def ridley_main_to_left_shaft():
    return all(
        SuperMissiles,
        any(
            CanVerticalWall,
            IceBeam
        ),
        any(
            VariaSuit,
            Trick("Ridley Hellrun - Normal"),
            Trick("Ridley Hellrun - Minimal"),
            all(
                CanBombTunnelBlock,
                any(
                    CanFly,
                    Trick("Ridley Fake Floor Skip"),
                )
            )
        ),
        MorphBall,
        any(
            NormalCombat,
            EnergyTanks(2),
            VariaSuit,
            GravitySuit
        )
    )


# shortcut to the right of elevator
def ridley_main_to_right_shaft():
    return all(
        Trick("Ridley Right Shaft Shortcut"),
        any(
            NormalCombat,
            EnergyTanks(2),
            VariaSuit,
            GravitySuit
        )
    )


def ridley_left_shaft_to_sw_puzzle():
    return all(
        SpeedBooster,
        any(
            CanVerticalWall,
            IceBeam
        )
    )


# The alcove to the right of the right shaft
def ridley_speed_puzzles_access():
    return all(
        SpeedBooster,
        CanVerticalWall
    )


# getting into the gap at the start of "ball room" and subsequently into the general area of ridley himself
def ridley_right_shaft_to_central():
    return CanEnterMediumMorphTunnel


def ridley_right_shaft_to_left_shaft():
    return any(
        CanIBJ,
        all(
            SpaceJump,
            any(
                PowerGrip,
                all(
                    NormalLogic,
                    CanBallspark
                )
            ),
        ),
        Trick("Ridley Left Shaft Climb Tricky Spark")
    )


# Ridley, Unknown 3, and the item behind Unknown 3
def ridley_central_to_ridley_room():
    return all(
        any(
            Missiles,
            ChargeBeam  # Fun fact! you can kill the eye door with charge beam
        ),
        RidleyCombat,
        any(
            CanFly,
            all(
                IceBeam,
                CanVerticalWall
            )
        )
    )


# TODO: Disabled for now since this warp is one-time. Later it may be repeatable, and then it might matter rarely
def tourian_to_chozodia():
    return all(
        MotherBrainBoss,
        RuinsTestEscape
    )


# From elevator to above the Unknown Item block by the Chozo statue
def crateria_lower_to_crateria_upper_right():
    return any(
        all(
            any(
                CanVerticalWall,
                CanBombTunnelBlock
            ),
            CanBallJump,
        ),
        all(
            NormalLogic,
            ScrewAttack,
            any(
                SpaceJump,
                CanHiWallJump,
                Trick("Crateria Upper Access Tricky Spark")
            ),
            CanFlyWall  # Getting up the pillars after the screw blocks
        )
    )


# From elevator to the left door of the Power Grip tower room
def crateria_lower_to_crateria_upper_left():
    return any(
        all(
            CanFly,
            any(
                all(
                    PowerBombs,
                    SpeedBooster,
                    GravitySuit
                ),
                all(
                    NormalLogic,  # not in Simple level logic because this requires meta knowledge of the rando
                    LayoutPatches("crateria_water_speedway")
                )
            ),
            any(
                LayoutPatches("crateria_left_of_grip"),
                CanEnterHighMorphTunnel
            )
        ),
        all(  # Shinespark up landing site
            any(
                PowerBombs,
                LayoutPatches("crateria_water_speedway")
            ),
            SpeedBooster,
            GravitySuit,
            any(
                all(
                    LayoutPatches("crateria_left_of_grip"),
                    CanVertical
                ),
                CanEnterHighMorphTunnel
            )
        )
    )


# This rule is mostly escape logic, so it's the same for both upper left and upper right
def crateria_upper_to_powergrip():
    return all(
        CanBallJump,
        any(
            all(
                CanVertical,
                LayoutPatches("crateria_left_of_grip")
            ),
            CanEnterHighMorphTunnel,
            CanFly
        )
    )


# Getting across the Power Grip tower room
def crateria_upper_leftright_connection():
    return any(
        CanFly,
        all(
            NormalLogic,  # Tight jump
            CanHiGrip
        )
    )


# Upper Crateria door to Ruins, the two items right by it, and the Triple Crawling Pirates
def crateria_upper_to_chozo_ruins():
    return all(
        PowerBombs,
        MorphBall,
        Missiles,
        any(
            CanFly,
            CanReachLocation("Crateria Northeast Corner"),
            Trick("Crateria-Chozodia Door Get-Around Walljump")
        ),
        any(
            MotherBrainBoss,
            Requirement.setting_is("chozodia_access", 0)
        )
    )


# Ruins to Chozo Ghost, the three items in that general area, and the lava dive item
def chozo_ruins_to_ruins_test():
    return all(
        MorphBall,
        PowerBombCount(2),  # 2 PBs ALWAYS required at minimum, but you may need many more
        any(
            all(
                Bomb,
                any(
                    NormalMode,
                    PowerBombCount(4)  # on Hard a save room is disabled, so you cannot refill PBs, requiring more
                )
            ),
            PowerBombCount(8),
            all(
                NormalMode,
                PowerBombCount(5),
            ),
            all(  # Skips one PB on the slow-crumble morph tunnel
                any(
                    PowerBombCount(7),
                    all(
                        NormalMode,
                        PowerBombCount(4)
                    )
                ),
                any(
                    ScrewAttack,
                    WaveBeam
                ),
                NormalLogic
            ),
            all(  # Skips the Triple Crawling Pirates room and a bomb chain but doesn't skip the crumble tunnel
                any(
                    PowerBombCount(5),  # Saves 2 on Hard
                    all(
                        NormalMode,
                        PowerBombCount(4),  # Only saves 1 on Normal because you can refill
                    )
                ),
                CanFlyWall,
                MissileCount(3),
                Missiles,
                Trick("Chozo Ghost Access Reverse")
            ),
            all(  # Skips everything possible, but still only PBs
                CanFlyWall,
                any(
                    ScrewAttack,
                    WaveBeam
                ),
                Missiles,
                PowerBombCount(4),  # technically should be 3 on Normal, but Normal can't have 3 max without having 4
                NormalLogic,
                Trick("Chozo Ghost Access Reverse")
            )
        ),
        CanVerticalWall,
        ChozodiaCombat,
    )


# Potentially useful for closed Chozodia post-MB warp, if that ever becomes a valid path
def ruins_test_to_ruins():
    return all(
        ChozoGhostBoss,
        RuinsTestEscape,
        any(
            all(  # Through the lava
                any(
                    CanWallJump,
                    all(
                        GravitySuit,
                        CanFly
                    )
                ),
                any(
                    ScrewAttack,
                    all(
                        NormalLogic,
                        Missiles,
                        any(
                            Bomb,
                            PowerBombCount(2)
                        )
                    )
                ),
                any(
                    GravitySuit,
                    Trick("Chozodia Lava Dive Escape - Normal"),
                    Trick("Chozodia Lava Dive Escape - Minimal")
                )
            ),
            all(  # Or going all the way back through the ruins
                NormalLogic,
                any(
                    PowerBombCount(4),
                    all(
                        Bomb,
                        PowerBombCount(2)
                    )
                ),
                CanFlyWall,
                ScrewAttack
            )
        )
    )


def chozo_ruins_to_chozodia_tube():
    return any(
        all(
            NormalLogic,  # It's a kinda tricky walljump but not really trick worthy
            CanWallJump
        ),
        CanFly
    )


# Specifically getting to the room with Crateria Upper Door location. Might need another empty region for region rando
def chozodia_tube_to_chozo_ruins():
    return all(
        any(
            CanFlyWall,
            CanHiGrip
        ),
        CanBombTunnelBlock
    )


def crateria_to_under_tube():
    return all(
        PowerBombs,
        MorphBall,
        any(
            SpeedBooster,
            CanFlyWall,
            CanHiGrip
        ),
        any(
            MotherBrainBoss,
            Requirement.setting_is("chozodia_access", 0)
        )
    )


def under_tube_to_tube():
    return any(
        SpeedBooster,
        all(
            CanFly,
            PowerBombs
        )
    )


def under_tube_to_crateria():
    return any(
        CanIBJ,
        all(
            PowerGrip,
            CanFlyWall
        ),
        Trick("Chozodia Under Tube Items Ballspark")  # Not an item but same idea so might as well reuse it
    )


def tube_to_under_tube():
    return any(
        PowerBombCount(3),  # most paths here require breaking a bomb chain on the way here and back
        all(
            Bomb,
            PowerBombs
        )
    )


def chozodia_tube_to_mothership_central():
    return all(
        ChozodiaCombat,
        any(
            CanFly,
            CanHiWallJump,
            Trick("Chozodia Pirates Enemy Freezes")
        )
    )


# access to the map station
def mothership_central_to_lower():
    return all(
        any(
            PowerBombCount(2),
            all(
                Bomb,
                PowerBombs
            )
        ),
        any(  # Getting to the save room
            Missiles,
            CanHiGrip,
            CanHiWallJump,
            CanFly,
            all(
                Trick("Chozodia Pirates Enemy Freezes"),
                any(
                    HiJump,
                    PowerGrip,
                    CanWallJump
                )
            )
        )
    )


# accessing the missile door just under the Behind Workbot item
def mothership_central_to_upper():
    return all(
        Missiles,
        any(
            Bomb,
            PowerBombCount(2)
        ),
        any(
            all(
                ScrewAttack,
                any(
                    CanWallJump,
                    SpaceJump,
                    all(
                        HiJump,
                        any(
                            PowerGrip,
                            CanIBJ
                        )
                    )
                )
            ),
            all(
                MissileCount(5),
                any(
                    CanFly,
                    CanHiGrip,
                    CanHiWallJump,
                    all(
                        Trick("Chozodia Pirates Enemy Freezes"),
                        CanVerticalWall
                    )
                )
            ),
            # the low% way
            all(
                any(
                    MissileCount(4),
                    ScrewAttack
                ),
                any(
                    CanFly,
                    CanHiGrip,
                    CanHiWallJump
                ),
                any(
                    Bomb,
                    PowerBombCount(3)
                ),
                any(
                    ScrewAttack,
                    MissileCount(5),
                    Bomb,
                    PowerBombCount(4)
                )
            )
        )
    )


def mothership_lower_to_upper():
    return all(
        CanBombTunnelBlock,
        any(
            CanFly,
            CanHiGrip,
            CanHiWallJump  # HJWJ required to get from the blue ship to the room under workbot; just WJ doesn't work
        )
    )


# the long way around - in case you don't have enough PBs
def mothership_upper_to_lower():
    return all(
        any(
            CanFlyWall,
            CanHiGrip
        ),
        any(
            all(
                NormalMode,
                MissileCount(2),
                CanBombTunnelBlock
            ),
            all(
                MissileCount(4),
                Bomb  # On Hard, you'd need 2 PBs to go this way, so the more direct central -> lower route is better
            )
        )
    )


# to the room right past Pirate Pitfall Trap
def mothership_upper_to_deep_mothership():
    return any(
        all(
            Missiles,
            any(
                CanFly,
                Trick("Mothership Upper Access Walljump")
            )
        ),
        # shortcut, going through Pirate Pitfall Trap
        all(
            SuperMissiles,
            PowerBombs,
            any(
                CanFlyWall,
                NormalLogic  # Leave and return to the room after PBing, the bomb blocks never reform
            )
        )
    )


def deep_mothership_to_cockpit():
    return all(
        CanFlyWall,
        any(
            Bomb,
            PowerBombCount(4)
        ),
        ChozodiaCombat
    )


def cockpit_to_original_pb():
    return all(
        any(  # cannot IBJ to escape to cockpit
            CanWallJump,
            HiJump,
            PowerGrip,
            SpaceJump
        ),
        any(
            Bomb,
            PowerBombCount(2)
        ),
        any(
            CanIBJ,
            all(
                PowerGrip,
                any(
                    CanFlyWall,
                    HiJump
                )
            ),
            Trick("Alpha PB Area Ice Escape")
        )
    )


def cockpit_to_mecha_ridley():
    return all(
        CanBombTunnelBlock,
        any(
            all(
                PowerBombs,
                CanVertical
            ),
            CanIBJ,
            PowerGrip,
            Trick("Chozodia Pirates Enemy Freezes")
        ),
        any(
            CanBallJump,
            PowerGrip
        ),
        any(
            all(
                PowerBombs,
                any(
                    Bomb,
                    PowerBombCount(2),
                    all(
                        NormalLogic,
                        MissileCount(4)
                    )
                ),
            ),
            Trick("Mecha Ridley Hall PB Skip")
        )
    )
