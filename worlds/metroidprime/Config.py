import os
from typing import TYPE_CHECKING, Dict, Any, List

from .Items import ProgressiveUpgrade, SuitUpgrade


from .PrimeOptions import HudColor, MetroidPrimeOptions
from .data.RoomData import MetroidPrimeArea
from .data.Transports import get_transport_data

MAX_32_BIT_INT = 0x7FFFFFFF

if TYPE_CHECKING:
    from . import MetroidPrimeWorld


def starting_inventory(world: "MetroidPrimeWorld", item: str) -> bool:
    items = [item.name for item in world.multiworld.precollected_items[world.player]]
    return item in items


def skip_ridley(boss: int) -> bool:
    return boss not in [0, 1]


def get_starting_beam(world: "MetroidPrimeWorld") -> str:
    starting_items = [
        item.name for item in world.multiworld.precollected_items[world.player]
    ]
    starting_beam = "Power"
    for item in starting_items:
        if item in [
            SuitUpgrade.Wave_Beam.value,
            SuitUpgrade.Ice_Beam.value,
            SuitUpgrade.Plasma_Beam.value,
        ]:
            starting_beam = item.split(" ")[0]
            break
        if item in [
            ProgressiveUpgrade.Progressive_Wave_Beam.value,
            ProgressiveUpgrade.Progressive_Ice_Beam.value,
            ProgressiveUpgrade.Progressive_Plasma_Beam.value,
            ProgressiveUpgrade.Progressive_Power_Beam.value,
        ]:
            starting_beam = item.split(" ")[1]
            break
    return starting_beam


def color_options_to_value(world: "MetroidPrimeWorld") -> List[float]:
    options = world.options
    # If any overrides are set, use that instead
    if (
        options.hud_color_red.value
        or options.hud_color_green.value
        or options.hud_color_blue.value
    ):
        return [
            options.hud_color_red.value / 255,
            options.hud_color_green.value / 255,
            options.hud_color_blue.value / 255,
        ]

    # get the key in hudcolor enum that matches all caps color
    color: str = world.options.hud_color.current_key
    color = color.upper()
    for key in HudColor.__members__.keys():
        if key == color:
            return HudColor[key].value
    return HudColor.DEFAULT.value


def make_artifact_hints(world: "MetroidPrimeWorld") -> Dict[str, str]:
    def make_artifact_hint(item: str) -> str:
        try:
            if world.options.artifact_hints:
                location = world.multiworld.find_item(item, world.player)
                player_string = (
                    f"{world.multiworld.player_name[location.player]}'s"
                    if location.player != world.player
                    else "your"
                )
                return f"The &push;&main-color=#c300ff;{item} &pop; can be found in &push;&main-color=#d4cc33;{player_string} &pop; &push;&main-color=#89a1ff;{location.name} &pop;."
            else:
                return (
                    f"The &push;&main-color=#c300ff;{item}&pop; has not been collected."
                )
            # This will error when trying to find an artifact that does not have a location since was pre collected
        except:
            return f"The &push;&main-color=#c300ff;{item}&pop; does not need to be collected."

    return {
        "Artifact of Chozo": make_artifact_hint("Artifact of Chozo"),
        "Artifact of Nature": make_artifact_hint("Artifact of Nature"),
        "Artifact of Sun": make_artifact_hint("Artifact of Sun"),
        "Artifact of World": make_artifact_hint("Artifact of World"),
        "Artifact of Spirit": make_artifact_hint("Artifact of Spirit"),
        "Artifact of Newborn": make_artifact_hint("Artifact of Newborn"),
        "Artifact of Truth": make_artifact_hint("Artifact of Truth"),
        "Artifact of Strength": make_artifact_hint("Artifact of Strength"),
        "Artifact of Elder": make_artifact_hint("Artifact of Elder"),
        "Artifact of Wild": make_artifact_hint("Artifact of Wild"),
        "Artifact of Lifegiver": make_artifact_hint("Artifact of Lifegiver"),
        "Artifact of Warrior": make_artifact_hint("Artifact of Warrior"),
    }


def get_tweaks(world: "MetroidPrimeWorld") -> Dict[str, List[float]]:
    color = color_options_to_value(world)
    if color != HudColor.DEFAULT.value:
        return {"hudColor": color}
    else:
        return {}


def get_strg(world: "MetroidPrimeWorld") -> Dict[str, List[str]]:
    strg = {**OBJECTIVE_STRG}
    # Set objective text in temple security station
    objective_text = f"Current Mission: Retrieve {world.options.required_artifacts}  Chozo Artifact{'s' if world.options.required_artifacts != 1 else ''}"
    if world.options.final_bosses == 0:
        objective_text += "\nDefeat Meta Ridley\nDefeat Metroid Prime"
    elif world.options.final_bosses == 1:
        objective_text += "\nDefeat Meta Ridley"
    elif world.options.final_bosses == 2:
        objective_text += "\nDefeat Metroid Prime"

    strg[DEFAULT_OBJECTIVE_STRG_KEY][2] = objective_text

    return strg


def make_version_specific_changes(
    config_json: Dict[str, Any], version: str
) -> Dict[str, Any]:
    if DEFAULT_OBJECTIVE_STRG_KEY in config_json["strg"] and version not in [
        "0-00",
        "0-01",
        "0-02",
        "kor",
    ]:
        value = config_json["strg"][DEFAULT_OBJECTIVE_STRG_KEY]
        del config_json["strg"][DEFAULT_OBJECTIVE_STRG_KEY]
        config_json["strg"][get_objective_strg_key(version)] = value

    return config_json


def make_config(world: "MetroidPrimeWorld") -> Dict[str, Any]:
    options: MetroidPrimeOptions = world.options
    config: Dict[str, Any] = {
        "$schema": "https://randovania.org/randomprime/randomprime.schema.json",
        "inputIso": "prime.iso",
        "outputIso": "prime_out.iso",
        "forceVanillaLayout": False,
        "strg": get_strg(world),
        "preferences": {
            "forceFusion": bool(options.fusion_suit.value),
            "cacheDir": "cache",
            "qolGeneral": True,
            "qolGameBreaking": True,
            "qolCosmetic": True,
            "qolCutscenes": "Skippable",
            "qolPickupScans": True,
            "mapDefaultState": "Always",
            "artifactHintBehavior": "All",
            "skipSplashScreens": bool(os.environ.get("DEBUG", False)),
            "quickplay": bool(os.environ.get("DEBUG", False)),
            "quickpatch": bool(os.environ.get("DEBUG", False)),
            "quiet": bool(os.environ.get("DEBUG", False)),
            "suitColors": {
                "gravityDeg": world.options.gravity_suit_color.value or 0,
                "phazonDeg": world.options.phazon_suit_color.value or 0,
                "powerDeg": world.options.power_suit_color.value or 0,
                "variaDeg": world.options.varia_suit_color.value or 0,
            },
        },
        "tweaks": get_tweaks(world),
        "gameConfig": {
            "mainMenuMessage": "Archipelago Metroid Prime",
            "startingRoom": f"{world.starting_room_data.area.value}:{world.starting_room_data.name}",
            "springBall": bool(options.spring_ball.value),
            "warpToStart": True,
            "multiworldDolPatches": True,
            "nonvariaHeatDamage": bool(options.non_varia_heat_damage.value),
            "staggeredSuitDamage": options.staggered_suit_damage.current_option_name,
            "heatDamagePerSec": 10.0,
            "poisonDamagePerSec": 0.11,
            "phazonDamagePerSec": 0.964,
            "phazonDamageModifier": "Default",
            "autoEnabledElevators": bool(options.pre_scan_elevators.value),
            "skipRidley": skip_ridley(options.final_bosses.value),
            "removeHiveMecha": bool(options.remove_hive_mecha.value),
            "startingItems": {
                "combatVisor": True,
                "powerSuit": True,
                "powerBeam": starting_inventory(world, SuitUpgrade.Power_Beam.value)
                or starting_inventory(
                    world, ProgressiveUpgrade.Progressive_Power_Beam.value
                ),
                "scanVisor": starting_inventory(world, SuitUpgrade.Scan_Visor.value),
                # These are handled by the client
                "missiles": (
                    5
                    if starting_inventory(world, SuitUpgrade.Missile_Launcher.value)
                    or starting_inventory(world, SuitUpgrade.Missile_Expansion.value)
                    else 0
                ),
                "energyTanks": 0,
                "powerBombs": 0,
                "wave": starting_inventory(world, SuitUpgrade.Wave_Beam.value)
                or starting_inventory(
                    world, ProgressiveUpgrade.Progressive_Wave_Beam.value
                ),
                "ice": starting_inventory(world, SuitUpgrade.Ice_Beam.value)
                or starting_inventory(
                    world, ProgressiveUpgrade.Progressive_Ice_Beam.value
                ),
                "plasma": starting_inventory(world, SuitUpgrade.Plasma_Beam.value)
                or starting_inventory(
                    world, ProgressiveUpgrade.Progressive_Plasma_Beam.value
                ),
                "charge": starting_inventory(world, SuitUpgrade.Charge_Beam.value),
                "morphBall": starting_inventory(world, SuitUpgrade.Morph_Ball.value),
                "bombs": starting_inventory(world, SuitUpgrade.Morph_Ball_Bomb.value),
                "spiderBall": starting_inventory(world, SuitUpgrade.Spider_Ball.value),
                "boostBall": starting_inventory(world, SuitUpgrade.Boost_Ball.value),
                "variaSuit": starting_inventory(world, SuitUpgrade.Varia_Suit.value),
                "gravitySuit": starting_inventory(
                    world, SuitUpgrade.Gravity_Suit.value
                ),
                "phazonSuit": starting_inventory(world, SuitUpgrade.Phazon_Suit.value),
                "thermalVisor": starting_inventory(
                    world, SuitUpgrade.Thermal_Visor.value
                ),
                "xray": starting_inventory(world, SuitUpgrade.X_Ray_Visor.value),
                "spaceJump": starting_inventory(
                    world, SuitUpgrade.Space_Jump_Boots.value
                ),
                "grapple": starting_inventory(world, SuitUpgrade.Grapple_Beam.value),
                "superMissile": starting_inventory(
                    world, SuitUpgrade.Super_Missile.value
                ),
                "wavebuster": starting_inventory(world, SuitUpgrade.Wavebuster.value),
                "iceSpreader": starting_inventory(
                    world, SuitUpgrade.Ice_Spreader.value
                ),
                "flamethrower": starting_inventory(
                    world, SuitUpgrade.Flamethrower.value
                ),
            },
            "disableItemLoss": True,
            "startingVisor": "Combat",
            "startingBeam": get_starting_beam(world),
            "enableIceTraps": False,
            "missileStationPbRefill": True,
            "doorOpenMode": "Original",
            "etankCapacity": 100,
            "itemMaxCapacity": {
                "Power Beam": (
                    2 if bool(world.options.progressive_beam_upgrades.value) else 1
                ),
                "Ice Beam": (
                    2 if bool(world.options.progressive_beam_upgrades.value) else 1
                ),
                "Wave Beam": (
                    2 if bool(world.options.progressive_beam_upgrades.value) else 1
                ),
                "Plasma Beam": (
                    2 if bool(world.options.progressive_beam_upgrades.value) else 1
                ),
                "Missile": 999,
                "Scan Visor": 1,
                "Morph Ball Bomb": 1,
                "Power Bomb": 99,
                "Flamethrower": 1,
                "Thermal Visor": 1,
                "Charge Beam": 1,
                "Super Missile": 1,
                "Grapple Beam": 1,
                "X-Ray Visor": 1,
                "Ice Spreader": 1,
                "Space Jump Boots": 1,
                "Morph Ball": 1,
                "Combat Visor": 1,
                "Boost Ball": 1,
                "Spider Ball": 1,
                "Power Suit": 1,
                "Gravity Suit": 1,
                "Varia Suit": 1,
                "Phazon Suit": 1,
                "Energy Tank": 99,
                "Unknown Item 1": MAX_32_BIT_INT,
                "Health Refill": MAX_32_BIT_INT,
                "Unknown Item 2": MAX_32_BIT_INT,
                "Wavebuster": 1,
                "Artifact Of Truth": 1,
                "Artifact Of Strength": 1,
                "Artifact Of Elder": 1,
                "Artifact Of Wild": 1,
                "Artifact Of Lifegiver": 1,
                "Artifact Of Warrior": 1,
                "Artifact Of Chozo": 1,
                "Artifact Of Nature": 1,
                "Artifact Of Sun": 1,
                "Artifact Of World": 1,
                "Artifact Of Spirit": 1,
                "Artifact Of Newborn": 1,
            },
            "phazonEliteWithoutDynamo": True,
            "mainPlazaDoor": True,
            "backwardsLabs": True,
            "backwardsFrigate": True,
            "backwardsUpperMines": True,
            "backwardsLowerMines": bool(world.options.backwards_lower_mines),
            "patchPowerConduits": False,
            "removeMineSecurityStationLocks": False,
            "powerBombArboretumSandstone": bool(world.options.flaahgra_power_bombs),
            "artifactHints": make_artifact_hints(world),
            "requiredArtifactCount": world.options.required_artifacts.value,
        },
        "levelData": make_level_data(world),
    }

    return config


def make_level_data(world: "MetroidPrimeWorld") -> Dict[str, Any]:
    transport_data = get_transport_data(world)
    level_data: Dict[str, Any] = {
        MetroidPrimeArea.Tallon_Overworld.value: {
            "transports": transport_data[MetroidPrimeArea.Tallon_Overworld.value],
            "rooms": world.game_region_data[MetroidPrimeArea.Tallon_Overworld].get_config_data(world),
        },
        MetroidPrimeArea.Chozo_Ruins.value: {
            "transports": transport_data[MetroidPrimeArea.Chozo_Ruins.value],
            "rooms": world.game_region_data[MetroidPrimeArea.Chozo_Ruins].get_config_data(world),
        },
        MetroidPrimeArea.Magmoor_Caverns.value: {
            "transports": transport_data[MetroidPrimeArea.Magmoor_Caverns.value],
            "rooms": world.game_region_data[MetroidPrimeArea.Magmoor_Caverns].get_config_data(world),
        },
        MetroidPrimeArea.Phendrana_Drifts.value: {
            "transports": transport_data[MetroidPrimeArea.Phendrana_Drifts.value],
            "rooms": world.game_region_data[MetroidPrimeArea.Phendrana_Drifts].get_config_data(world),
        },
        MetroidPrimeArea.Phazon_Mines.value: {
            "transports": transport_data[MetroidPrimeArea.Phazon_Mines.value],
            "rooms": world.game_region_data[MetroidPrimeArea.Phazon_Mines].get_config_data(world),
        },
    }

    return level_data


def get_objective_strg_key(version: str) -> str:
    if version == "pal":
        return "3172743300"
    else:
        return "3012146902"


DEFAULT_OBJECTIVE_STRG_KEY = "3012146902"
OBJECTIVE_STRG = {
    DEFAULT_OBJECTIVE_STRG_KEY: ["Objective data decoded\n", "Mission Objectives", ""]
}
