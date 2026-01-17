from typing import Mapping, TYPE_CHECKING
from BaseClasses import Item
if TYPE_CHECKING:
    from . import SMMapRandoWorld

# For Metroid Item Matching, force major unique upgrades that don't quite match Map Rando items to be full dots
# (ie AP useful prog items)
DEFAULT_MAJOR = "ArchipelagoUsefulProgItem"
DEFAULT_AMMO = "ArchipelagoUsefulItem"

metroid_item_matching: Mapping[str, Mapping[str, str]] = {
    "Super Metroid": {
        "Energy Tank": "ETank",
        "Missile": "Missile",
        "SuperMissile": "Super",
        "Power Bomb": "PowerBomb",
        "Grappling Beam": "Grapple",
        "X-Ray Scope": "XRayScope",
        "Reserve Tank": "ReserveTank",
        "Charge Beam": "Charge",
        "Ice Beam": "Ice",
        "Wave Beam": "Wave",
        "Spazer": "Spazer",
        "Plasma Beam": "Plasma",
        "Varia Suit": "Varia",
        "Gravity Suit": "Gravity",
        "Morph Ball": "Morph",
        "Bomb": "Bombs",
        "Spring Ball": "SpringBall",
        "Screw Attack": "ScrewAttack",
        "Hi-Jump Boots": "HiJump",
        "Space Jump": "SpaceJump",
        "Speed Booster": "SpeedBooster"
    },
    "SMZ3": {
        "ETank": "ETank",
        "Missile": "Missile",
        "Super": "Super",
        "PowerBomb": "PowerBomb",
        "Grapple": "Grapple",
        "XRay": "XrayScope",
        "ReserveTank": "ReserveTank",
        "Charge": "Charge",
        "Ice": "Ice",
        "Wave": "Wave",
        "Spazer": "Spazer",
        "Plasma": "Plasma",
        "Varia": "Varia",
        "Gravity": "Gravity",
        "Morph": "Morph",
        "Bombs": "Bombs",
        "SpringBall": "SpringBall",
        "ScrewAttack": "ScrewAttack",
        "HiJump": "HiJump",
        "SpaceJump": "SpaceJump",
        "SpeedBooster": "SpeedBooster"
    },
    "Metroid Fusion": {
        "Missile Data": DEFAULT_MAJOR,
        "Missile Tank": "Missile",
        "Super Missile": DEFAULT_MAJOR,
        "Ice Missile": DEFAULT_MAJOR,
        "Diffusion Missile": DEFAULT_MAJOR,
        "Power Bomb Data": DEFAULT_MAJOR,
        "Power Bomb Tank": "PowerBomb",
        "Energy Tank": "ETank",
        "Charge Beam": "Charge",
        "Wide Beam": "Spazer",
        "Plasma Beam": "Plasma",
        "Wave Beam": "Wave",
        "Ice Beam": "Ice",
        "Morph Ball": "Morph",
        "Bomb Data": "Bombs",
        "Hi-Jump": "HiJump",
        "Space Jump": "SpaceJump",
        "Speed Booster": "SpeedBooster",
        "Screw Attack": "ScrewAttack",
        "Varia Suit": "Varia",
        "Gravity Suit": "Gravity",
        "Nothing": "Nothing"
    },
    "Metroid Zero Mission": {
        "Energy Tank": "ETank",
        "Missile Tank": "Missile",
        "Super Missile Tank": "Super",
        "Power Bomb Tank": "PowerBomb",
        "Long Beam": DEFAULT_MAJOR,
        "Charge Beam": "Charge",
        "Ice Beam": "Ice",
        "Wave Beam": "Wave",
        "Plasma Beam": "Plasma",
        "Bomb": "Bombs",
        "Varia Suit": "Varia",
        "Gravity Suit": "Gravity",
        "Morph Ball": "Morph",
        "Speed Booster": "SpeedBooster",
        "Hi-Jump": "HiJump",
        "Screw Attack": "ScrewAttack",
        "Space Jump": "SpaceJump",
        "Power Grip": DEFAULT_MAJOR,
        "Fully Powered Suit": DEFAULT_MAJOR,
        "Wall Jump": "WallJump",
        "Spring Ball": "SpringBall"
    },
    "Metroid Prime": {
        "Charge Beam": "Charge",
        "Power Beam": DEFAULT_MAJOR,
        "Progressive Power Beam": DEFAULT_MAJOR,
        "Super Missile": DEFAULT_MAJOR,
        "Ice Beam": "Ice",
        "Progressive Ice Beam": "Ice",
        "Ice Spreader": DEFAULT_MAJOR,
        "Wave Beam": "Wave",
        "Progressive Wave Beam": "Wave",
        "Wavebuster": DEFAULT_MAJOR,
        "Plasma Beam": "Plasma",
        "Progressive Plasma Beam": "Plasma",
        "Flamethrower": DEFAULT_MAJOR,
        "Missile Launcher": DEFAULT_MAJOR,
        "Missile Expansion": "Missile",
        "Power Bomb (Main)": DEFAULT_MAJOR,
        "Power Bomb Expansion": "PowerBomb",
        "Energy Tank": "ETank",
        "Morph Ball": "Morph",
        "Morph Ball Bomb": "Bombs",
        "Boost Ball": DEFAULT_MAJOR,
        "Spider Ball": DEFAULT_MAJOR,
        "Varia Suit": "Varia",
        "Gravity Suit": "Gravity",
        "Phazon Suit": DEFAULT_MAJOR,
        "Space Jump Boots": "SpaceJump",
        "Grapple Beam": "Grapple",
        "Scan Visor": DEFAULT_MAJOR,
        "Thermal Visor": DEFAULT_MAJOR,
        "X-Ray Visor": "XRayScope"
    },
    "Metroid Prime 2 Echoes": {
        "Power Beam": DEFAULT_MAJOR,
        "Dark Beam": DEFAULT_MAJOR,
        "Light Beam": DEFAULT_MAJOR,
        "Annihilator Beam": DEFAULT_MAJOR,
        "Super Missile": DEFAULT_MAJOR,
        "Darkburst": DEFAULT_MAJOR,
        "Sunburst": DEFAULT_MAJOR,
        "Sonic Boom": DEFAULT_MAJOR,
        "Combat Visor": DEFAULT_MAJOR,
        "Scan Visor": DEFAULT_MAJOR,
        "Dark Visor": DEFAULT_MAJOR,
        "Echo Visor": DEFAULT_MAJOR,
        "Dark Suit": DEFAULT_MAJOR,
        "Light Suit": DEFAULT_MAJOR,
        "Morph Ball": "Morph",
        "Boost Ball": DEFAULT_MAJOR,
        "Spider Ball": DEFAULT_MAJOR,
        "Morph Ball Bomb": "Bombs",
        "Charge Beam": "Charge",
        "Grapple Beam": "Grapple",
        "Space Jump Boots": "SpaceJump",
        "Gravity Boost": DEFAULT_MAJOR,
        "Seeker Launcher": DEFAULT_MAJOR,
        "Screw Attack": "Screwttack",
        "Energy Tank": "ETank",
        "Power Bomb Expansion": "PowerBomb",
        "Missile Expansion": "Missile",
        "Dark Ammo Expansion": DEFAULT_AMMO,
        "Light Ammo Expansion": DEFAULT_AMMO,
        "Beam Ammo Expansion": DEFAULT_AMMO,
        "Missile Launcher": DEFAULT_MAJOR,
        "Power Bomb Launcher": DEFAULT_MAJOR,
        "Unlimited Missiles": DEFAULT_AMMO,
        "Unlimited Beam Ammo": DEFAULT_AMMO,
        "Energy Transfer Module": DEFAULT_MAJOR
    }
}

def match_item_metroid(world: "SMMapRandoWorld", item: Item) -> str:
    if item.game in metroid_item_matching and item.name in metroid_item_matching[item.game]:
        return world.item_name_to_id[metroid_item_matching[item.game][item.name]]
    if item.game == world.game:
        if item.name.startswith("Prog"):
            return world.item_name_to_id[item.name[4:]]
        return item.code
    return match_item_generic(world, item)

def match_item_generic(world: "SMMapRandoWorld", item: Item) -> str:
    classification = ""
    if item.useful: classification += "Useful"
    if item.advancement: classification += "Prog"
    return world.item_name_to_id[f"Archipelago{classification}Item"]
