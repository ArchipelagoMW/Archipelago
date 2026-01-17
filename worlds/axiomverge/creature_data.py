import typing as t
from dataclasses import dataclass

from . import conditions
from .constants import AP_ID_BASE, AVRegion, AVGlitchRegion
from .types import AccessRule

@dataclass
class AVGlitchLocationData:
    id: int
    enemy: str
    glitch_level: AccessRule
    parent_region: str | None
    entrances: tuple[tuple[AVRegion, AccessRule]] | None

    def __post_init__(self):
        self.id += AP_ID_BASE

        if self.enemy.startswith(("A", "E", "I", "O", "U")):
            self.name = f'Glitch an {self.enemy}'
        else:
            self.name = f'Glitch a {self.enemy}'


creature_data: tuple[AVGlitchLocationData] = (
    AVGlitchLocationData(
        125,
        "Red Snailborg",
        conditions.any_glitch,
        None,
        (
            (AVRegion.UPPER_ERIBU, conditions.always_accessible),
            (AVRegion.LOWER_ERIBU, conditions.always_accessible),
            (AVRegion.WEST_ABSU, conditions.always_accessible),
            (AVRegion.EAST_ABSU, conditions.always_accessible),
        ),
    ),
    AVGlitchLocationData(
        126,
        "Blue Snailborg",
        conditions.any_glitch,
        None,
        (
            (AVRegion.LOWER_ERIBU, conditions.always_accessible),
            (AVRegion.WEST_ABSU, conditions.always_accessible),
            (AVRegion.ATTIC_JUNCTION, conditions.always_accessible),
            (AVRegion.EAST_ABSU, conditions.always_accessible),
            (AVRegion.LOWER_ABSU, conditions.always_accessible),
        ),
    ),
    AVGlitchLocationData(
        127,
        "Purple Trap Claw",
        conditions.any_glitch,
        None,
        (
            (AVRegion.XEDUR, conditions.always_accessible),
            (AVRegion.LOWER_ERIBU, conditions.always_accessible),
        ),
    ),
    AVGlitchLocationData(
        128,
        "Red Trap Claw",
        conditions.any_glitch,
        None,
        (
            (AVRegion.LOWER_ERIBU, conditions.always_accessible),
            (AVRegion.EAST_ABSU, conditions.any_coat),
        ),
    ),
    AVGlitchLocationData(
        129,
        "Cyan Trap Claw",
        conditions.has_glitch_2,
        None,
        (
            (AVRegion.GRAPPLE_CLIFFS, conditions.always_accessible),
            (AVRegion.MOUNTAIN_TOP, conditions.always_accessible),
            (AVRegion.LABORATORY, conditions.always_accessible),
        ),
    ),
    AVGlitchLocationData(
        130,
        "Yorchug",
        conditions.has_glitch_2,
        None,
        (
            (AVRegion.UPPER_ERIBU, conditions.always_accessible),
            (AVRegion.LOWER_ERIBU, conditions.always_accessible),
        ),
    ),
    AVGlitchLocationData(131, "Spiru", conditions.any_glitch, AVRegion.LOWER_ERIBU, None),
    AVGlitchLocationData(132, "Swarmily (Child)", conditions.any_glitch, AVGlitchRegion.SWARMILY, None),
    AVGlitchLocationData(133, "Swarmily (Parent)", conditions.any_glitch, AVGlitchRegion.SWARMILY, None),
    AVGlitchLocationData(
        134,
        "Pink Loop Diatom",
        conditions.any_glitch,
        None,
        (
            (AVRegion.WEST_ABSU, conditions.always_accessible),
            (AVRegion.ATTIC_JUNCTION, conditions.always_accessible),
            (AVRegion.EAST_ABSU, conditions.always_accessible),
        ),
    ),
    AVGlitchLocationData(
        135,
        "Violet Loop Diatom",
        conditions.any_glitch,
        None,
        (
            (AVRegion.WEST_ABSU, conditions.always_accessible),
            (AVRegion.LOWER_CORRIDOR, conditions.always_accessible),
        ),
    ),
    AVGlitchLocationData(
        136,
        "Quadropus",
        conditions.has_glitch_2,
        None,
        (
            (AVRegion.UPPER_ERIBU, conditions.upper_eribu_bomb_access),
            (AVRegion.WEST_ABSU, conditions.always_accessible),
            (AVRegion.LOWER_ABSU, conditions.any_coat),
            (AVRegion.INDI_TUNNEL, conditions.always_accessible),
        ),
    ),
    AVGlitchLocationData(
        137,
        "Arachnoptopus",
        conditions.has_glitch_2,
        None,
        (
            (AVRegion.LOWER_ABSU, conditions.any_coat),
            (AVRegion.EAST_ABSU, conditions.always_accessible),
            (AVRegion.INDI_TUNNEL, conditions.always_accessible),
            (AVRegion.ZI_CORRIDOR, conditions.always_accessible),
            (AVRegion.UPPER_ZI, conditions.always_accessible),
        ),
    ),
    AVGlitchLocationData(
        138,
        "Buoyg",
        conditions.any_glitch,
        None,
        (
            (AVRegion.UPPER_ERIBU, conditions.outside_lab_access),
            (AVRegion.EAST_ABSU, conditions.always_accessible),
        ),
    ),
    AVGlitchLocationData(139, "Fungine", conditions.any_glitch, AVRegion.EAST_ABSU, None),
    AVGlitchLocationData(140, "Green Rugg", conditions.any_glitch, AVRegion.LOWER_ZI, None),
    AVGlitchLocationData(141, "Magenta Rugg", conditions.any_glitch, AVRegion.UPPER_ZI, None),
    AVGlitchLocationData(142, "Scorpiant", conditions.any_glitch, AVRegion.LOWER_ZI, None),
    AVGlitchLocationData(
        143,
        "Prongfish",
        conditions.has_glitch_2,
        None,
        (
            (AVRegion.ZI_CORRIDOR, conditions.always_accessible),
            (AVRegion.UPPER_ZI, conditions.always_accessible),
        ),
    ),
    AVGlitchLocationData(144, "Hookfish", conditions.has_glitch_2, AVRegion.LOWER_E_KUR_MAH, None),
    AVGlitchLocationData(
        145,
        "Gill",
        conditions.any_glitch,
        None,
        (
            (AVRegion.LOWER_CAVES, conditions.always_accessible),
            (AVRegion.LOWER_ERIBU, conditions.has_passcode),
        ),
    ),
    AVGlitchLocationData(146, "Pliaa", conditions.any_glitch, AVRegion.LOWER_CAVES, None),
    AVGlitchLocationData(
        147,
        "Seamk",
        conditions.any_glitch,
        None,
        (
            (AVRegion.GAUNTLET_ENTRANCE, conditions.any_coat),
            (AVRegion.GIR_TAB_LOWER_ENTRANCE, conditions.always_accessible),
            (AVRegion.GIR_TAB_UPPER_ENTRANCE, conditions.always_accessible),
        ),
    ),
    AVGlitchLocationData(148, "Spidler", conditions.any_glitch, AVRegion.UPPER_CAVES, None),
    AVGlitchLocationData(149, "Volg", conditions.any_glitch, AVRegion.CLONE, None),
    AVGlitchLocationData(150, "Drometon", conditions.has_glitch_2, AVRegion.MOUNTAIN_BASE, None),
    AVGlitchLocationData(151, "Flynn Stone", conditions.any_glitch, AVRegion.MOUNTAIN_BASE, None),
    AVGlitchLocationData(
        152,
        "Brown Mutant",
        conditions.has_glitch_2,
        None,
        (
            (AVRegion.ELSENOVA, conditions.always_accessible),
            (AVRegion.LOWER_ABSU, conditions.always_accessible),
            (AVRegion.LOWER_ZI, conditions.non_grapple_height),
            (AVRegion.EAST_ZI, conditions.always_accessible),
            (AVRegion.UPPER_ZI, conditions.always_accessible),
        ),
    ),
    AVGlitchLocationData(
        153,
        "Blue Mutant",
        conditions.has_glitch_2,
        None,
        (
            (AVRegion.LABORATORY, conditions.always_accessible),
            (AVRegion.EAST_ABSU, conditions.zombie_tunnel_access),
            (AVRegion.ABOVE_GIR_TAB, conditions.always_accessible),
            (AVRegion.LOWER_EDIN_RIGHT, conditions.always_accessible),
            (AVRegion.EAST_EDIN, conditions.edin_double_check_tunnel_access),
        ),
    ),
    AVGlitchLocationData(154, "Small Mogra", conditions.any_glitch, AVGlitchRegion.MOGRA, None),
    AVGlitchLocationData(155, "Mogra", conditions.any_glitch, AVGlitchRegion.MOGRA, None),
    AVGlitchLocationData(156, "Pillbug", conditions.any_glitch, AVRegion.UKKIN_NA_BASE, None),
    AVGlitchLocationData(
        157,
        "Glugg",
        conditions.has_glitch_2,
        None,
        (
            (AVRegion.INDI, conditions.always_accessible),
            (AVRegion.OPHELIA, conditions.always_accessible),
        ),
    ),
    AVGlitchLocationData(158, "Blurst", conditions.any_glitch, AVRegion.BLURST, None),
    AVGlitchLocationData(159, "Blurst Swarm", conditions.any_glitch, AVRegion.BLURST, None),
    AVGlitchLocationData(160, "Jorm", conditions.has_glitch_2, AVRegion.LOWER_EDIN_RIGHT, None),
    AVGlitchLocationData(161, "Space Bat", conditions.has_glitch_2, AVRegion.CLONE, None),
    AVGlitchLocationData(
        162,
        "Eyecopter",
        conditions.any_glitch,
        None,
        (
            (AVRegion.GAUNTLET_ROOF, conditions.always_accessible),
            (AVRegion.LOWER_EDIN_LEFT, conditions.always_accessible),
            (AVRegion.LOWER_EDIN_RIGHT, conditions.always_accessible),
            (AVRegion.EAST_EDIN, conditions.always_accessible),
        ),
    ),
    AVGlitchLocationData(163, "Blite", conditions.any_glitch, AVRegion.LOWER_CAVES, None),
    AVGlitchLocationData(164, "Artichoker", conditions.any_glitch, AVRegion.LOWER_E_KUR_MAH, None),
    AVGlitchLocationData(
        165,
        "Furglot",
        conditions.any_glitch,
        None,
        (
            (AVRegion.LOWER_ZI, conditions.furglot_tunnel_access),
            (AVRegion.LOWER_E_KUR_MAH, conditions.always_accessible),
        ),
    ),
    AVGlitchLocationData(
        166,
        "Mushroom Poof",
        conditions.any_glitch,
        None,
        (
            (AVRegion.WEST_ABSU, conditions.always_accessible),
            (AVRegion.EAST_ABSU, conditions.always_accessible),
        ),
    ),
    AVGlitchLocationData(167, "Spungus Spore", conditions.any_glitch, AVRegion.EAST_ABSU, None),
    AVGlitchLocationData(
        168,
        "Goolumn",
        conditions.has_glitch_2,
        None,
        (
            (AVRegion.LOWER_ZI, conditions.always_accessible),
            (AVRegion.EAST_ZI, conditions.always_accessible),
        ),
    ),
    AVGlitchLocationData(
        169,
        "Hoverling",
        conditions.has_glitch_2,
        None,
        (
            (AVRegion.LOWER_EDIN_LEFT, conditions.always_accessible),
            (AVRegion.LOWER_EDIN_RIGHT, conditions.always_accessible),
            (AVRegion.EAST_EDIN, conditions.always_accessible),
        ),
    ),
    AVGlitchLocationData(170, "Annihiwaiter", conditions.has_glitch_2, AVRegion.UKKIN_NA_BASE, None),
    AVGlitchLocationData(171, "Silver Sentry Bot", conditions.has_glitch_2, AVRegion.OPHELIA, None),
    AVGlitchLocationData(
        172,
        "Ancient Sentry Bot",
        conditions.has_glitch_bomb,
        None,
        (
            (AVRegion.DINGER_GISBAR, conditions.always_accessible),
            (AVRegion.UPPER_E_KUR_MAH, conditions.always_accessible),
            (AVRegion.LOWER_E_KUR_MAH, conditions.always_accessible),
        ),
    ),
    AVGlitchLocationData(
        173,
        "Purple Sentry Bot",
        conditions.has_glitch_2,
        None,
        (
            (AVRegion.DINGER_GISBAR, conditions.always_accessible),
            (AVRegion.LOWER_ERIBU, conditions.eribu_sentry_bot_tunnel_trace_access),
            (AVRegion.MAR_URU_ENTRANCE, conditions.always_accessible),
        ),
    ),
    AVGlitchLocationData(174, "Tie-Flighter", conditions.has_glitch_2, AVRegion.MAR_URU_ENTRANCE, None),
    AVGlitchLocationData(175, "Diskko", conditions.has_glitch_2, AVRegion.ATHETOS, None),
    AVGlitchLocationData(176, "Donaught", conditions.has_glitch_bomb, AVRegion.ATHETOS, None),
    AVGlitchLocationData(177, "Spitbug", conditions.any_glitch, AVGlitchRegion.SPITBUG, None),
    AVGlitchLocationData(178, "Spitbug Nest", conditions.any_glitch, AVGlitchRegion.SPITBUG, None),
    AVGlitchLocationData(179, "Yellow Tube Worm", conditions.has_glitch_2, AVRegion.EAST_ZI, None),
    AVGlitchLocationData(
        180,
        "Green Tube Worm",
        conditions.has_glitch_2,
        None,
        (
            (AVRegion.WEST_ERIBU, conditions.west_caves_pool_access),
            (AVRegion.INDI, conditions.always_accessible),
            (AVRegion.OPHELIA, conditions.always_accessible),
        ),
    ),
    AVGlitchLocationData(
        181,
        "Will-o-Wisp",
        conditions.any_glitch,
        None,
        (
            (AVRegion.WEST_ERIBU, lambda s, c: conditions.can_displacement_warp(s, c) or conditions.non_jump_height(s, c) and conditions.can_drill(s, c)),
            (AVRegion.UKHU_TOWER, conditions.always_accessible),
            (AVRegion.EAST_EDIN, conditions.edin_double_check_tunnel_access),
        ),
    ),
    AVGlitchLocationData(182, "Boulder", conditions.any_glitch, AVRegion.MOUNTAIN_BASE, None),
    AVGlitchLocationData(183, "Ukhu Spawn", conditions.any_glitch, AVRegion.UKHU, None),
)
