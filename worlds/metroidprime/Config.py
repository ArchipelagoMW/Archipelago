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
                return f"The &push;&main-color=#c300ff;{item}&pop; can be found in &push;&main-color=#d4cc33;{player_string}&pop; &push;&main-color=#89a1ff;{location.name}&pop;."
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
    objective_text = f"Current Mission: Retrieve {world.options.required_artifacts} Chozo Artifact{'s' if world.options.required_artifacts != 1 else ''}"
    if world.options.final_bosses == 0:
        objective_text += "\nDefeat Meta Ridley\nDefeat Metroid Prime"
    elif world.options.final_bosses == 1:
        objective_text += "\nDefeat Meta Ridley"
    elif world.options.final_bosses == 2:
        objective_text += "\nDefeat Metroid Prime"

    strg[DEFAULT_OBJECTIVE_STRG_KEY][2] = objective_text

    # Show suit colors in pause menu
    strg = {**strg, **PAUSE_STRG}
    pause_menu_overrides = {
        "Power Suit": world.options.power_suit_color.value,
        "Varia Suit": world.options.varia_suit_color.value,
        "Gravity Suit": world.options.gravity_suit_color.value,
        "Phazon Suit": world.options.phazon_suit_color.value,
    }
    # Update the name to include the color index if it is set
    for item in strg[PAUSE_MENU_STRG_KEY]:
        if item in pause_menu_overrides and pause_menu_overrides[item] != 0:
            index = strg[PAUSE_MENU_STRG_KEY].index(item)
            strg[PAUSE_MENU_STRG_KEY][
                index
            ] = f"{item} (Color: {pause_menu_overrides[item]})"
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

    # Pause Menu does not have correct id for non US versions right now
    if PAUSE_MENU_STRG_KEY in config_json["strg"] and version not in [
        "0-00",
        "0-01",
        "0-02",
    ]:
        del config_json["strg"][PAUSE_MENU_STRG_KEY]
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
            "multiworldDolPatches": False,
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
            "rooms": world.game_region_data[
                MetroidPrimeArea.Tallon_Overworld
            ].get_config_data(world),
        },
        MetroidPrimeArea.Chozo_Ruins.value: {
            "transports": transport_data[MetroidPrimeArea.Chozo_Ruins.value],
            "rooms": world.game_region_data[
                MetroidPrimeArea.Chozo_Ruins
            ].get_config_data(world),
        },
        MetroidPrimeArea.Magmoor_Caverns.value: {
            "transports": transport_data[MetroidPrimeArea.Magmoor_Caverns.value],
            "rooms": world.game_region_data[
                MetroidPrimeArea.Magmoor_Caverns
            ].get_config_data(world),
        },
        MetroidPrimeArea.Phendrana_Drifts.value: {
            "transports": transport_data[MetroidPrimeArea.Phendrana_Drifts.value],
            "rooms": world.game_region_data[
                MetroidPrimeArea.Phendrana_Drifts
            ].get_config_data(world),
        },
        MetroidPrimeArea.Phazon_Mines.value: {
            "transports": transport_data[MetroidPrimeArea.Phazon_Mines.value],
            "rooms": world.game_region_data[
                MetroidPrimeArea.Phazon_Mines
            ].get_config_data(world),
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
PAUSE_MENU_STRG_KEY = "1343145632"
PAUSE_STRG = {
    PAUSE_MENU_STRG_KEY: [
        "[ Log Book ]",
        "Pirate Data",
        "Chozo Lore",
        "Creatures",
        "Research",
        "Artifacts",
        "LOG BOOK",
        "OPTIONS",
        "INVENTORY",
        "[ Inventory ]",
        "Arm Cannon",
        "Morph Ball",
        "Suits",
        "Visors",
        "Secondary Items",
        "[ Options ]",
        "Visor",
        "Display",
        "Sound",
        "Controller",
        "Quit Game",
        "Visor Opacity",
        "Helmet Opacity",
        "HUD Lag",
        "Hint System",
        "Screen Brightness",
        "Screen Offset X",
        "Screen Offset Y",
        "Screen Stretch",
        "SFX Volume",
        "Music Volume",
        "Sound Mode",
        "Reverse Y-Axis",
        "Rumble",
        "Swap Beam Controls",
        "Restore Defaults",
        "Power Beam",
        "Ice Beam",
        "Wave Beam",
        "Plasma Beam",
        "Phazon Beam",
        "Super Missile",
        "Ice Spreader",
        "Wavebuster",
        "Flamethrower",
        "Phazon Combo",
        "Morph Ball",
        "Boost Ball",
        "Spider Ball",
        "Morph Ball Bomb",
        "Power Bomb",
        "Power Suit",
        "Varia Suit",
        "Gravity Suit",
        "Phazon Suit",
        "Energy Tank",
        "Combat Visor",
        "Scan Visor",
        "X-Ray Visor",
        "Thermal Visor",
        "Space Jump Boots",
        "Grapple Beam",
        "Missile Launcher",
        "Charge Beam",
        "Beam Combo",
        "[??????]\n\n",
        "The &main-color=#89D6FF;Combat Visor&main-color=#FF6705B3; is your default Visor. It provides you with a Heads-Up Display (HUD) containing radar, mini-map, lock-on reticules, threat assessment, energy gauge, and Missile count.\n\nPress &image=SA,3.0,0.6,0.85,F13452F8,C042EC91; to select the Combat Visor.\n\n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nIcons for the Arm Cannons you possess are shown in the lower-right corner of the Combat Visor.\n\nIcons for the Visors you possess are shown in the lower-left corner of the Combat Visor.\n\n",
        "The &main-color=#89D6FF;Scan Visor&main-color=#FF6705B3; is used to collect data. Some devices will activate when scanned.\n\nPress &image=SA,3.0,0.6,0.85,F13452F8,B306E26F; to select the Scan Visor. Move the Visor over targets with this symbol &image=SI,0.70,0.68,FD41E145;, then press and hold &image=SA,3.0,1.0,1.0,46434ED3,34E79314; to scan. \n\nUse &image=SI,0.6,0.85,F13452F8; to select another available Visor or press &image=SI,0.70,0.68,05AF9CAA; to turn the Visor off.\n\n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nMission-critical scan targets &image=SI,0.70,0.68,BCE843F2; will be red in color. \n\nScanning enemies with this Visor can reveal their vulnerabilities.\n\nYou will be unable to fire any weapons while the Scan Visor is active.\n\nScanned data vital to the success of the mission is downloaded and stored in the &main-color=#89D6FF;Log Book&main-color=#FF6705B3; section of the Pause Screen. \n\nPress &image=A,3.0,08A2E4B9,F2425B21; on this screen to access the Log Book.\n",
        "The &main-color=#89D6FF;X-Ray Visor&main-color=#FF6705B3; can see through certain types of materials. \n\nPress &image=SA,3.0,0.6,0.85,F13452F8,8ADA8184; to select the X-Ray Visor.\n\n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nThe X-Ray Visor can reveal invisible items, areas, and enemies.\n\nRobotic enemies jam the X-Ray Visor's frequency. Eliminate them to restore function to the Visor.\n",
        "The &main-color=#89D6FF;Thermal Visor&main-color=#FF6705B3; allows you to see in the infrared spectrum. Hot objects are bright in the Visor, while colder ones are dim.\n\nPress &image=SA,3.0,0.6,0.85,F13452F8,5F556002; to select the Thermal Visor.\n\n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nThe Thermal Visor will show the weak points of certain foes.\n\nUse the Thermal Visor to see in total darkness and poor weather conditions. \n\nBrightly lit areas, explosions, and intense heat can impair the Thermal Visor.\n\nEnemies with temperatures close to their surroundings will be tough to spot with this Visor.\n",
        "The &main-color=#89D6FF;Power Beam&main-color=#FF6705B3; is the default Arm Cannon. It has the best rate of fire.\n\nPress &image=SA,3.0,0.6,0.85,2A13C23E,A91A7703; to select the Power Beam as your active weapon.\n\n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nThe Power Beam can be used to open Blue Doors.\n\nIf you see your shots ricochet, cease fire. The Power Beam is not working against that target.\n\nYou can use the Power Beam to quickly clear an area of weak foes.\n",
        "\nThe &main-color=#89D6FF;Super Missile&main-color=#FF6705B3; is the &main-color=#89D6FF;Power&main-color=#FF6705B3; Charge Combo.\n\n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nSuper Missile is a Single Shot Charge Combo. Each shot costs 5 Missiles.\n\nSuper Missiles can destroy objects made of &main-color=#89D6FF;Cordite&main-color=#FF6705B3;.\n",
        "The &main-color=#89D6FF;Ice Beam&main-color=#FF6705B3; can freeze enemies solid. Hits from the Ice Beam may also slow foes down.  \n\nPress &image=SA,3.0,0.6,0.85,2A13C23E,12A12131; to select the Ice Beam as your active weapon.\n\n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nUse the Ice Beam to open White Doors.\n\nThe Ice Beam is quite effective against fire-based creatures.\n\nCharge the Ice Beam to increase the time an enemy will stay frozen when hit.\n\nSome frozen enemies can be shattered by Missile hits.\n",
        "\nThe &main-color=#89D6FF;Ice Spreader&main-color=#FF6705B3; is the &main-color=#89D6FF;Ice&main-color=#FF6705B3; Charge Combo. It can freeze targets in a wide area.\n\n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nIce Spreader is a Single Shot Charge Combo. Each shot costs 10 Missiles.\n\nIce Spreader is limited against aerial targets.\n",
        "The&main-color=#89D6FF; Wave Beam&main-color=#FF6705B3; fires powerful electric bolts. This weapon has a limited homing capability as well.\n\nPress &image=SA,3.0,0.6,0.85,2A13C23E,CD7B1ACA; to select the Wave Beam as your active weapon.\n  \n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nFire the Wave Beam to open Purple Doors.\n\nThe Wave Beam won't home in on targets without a lock-on. Press and hold &image=SA,3.0,1.0,1.0,46434ED3,34E79314; to lock on.\n\nCharge the Wave Beam to fire a fierce electric blast. Enemies struck by this blast will be enveloped in electrical energy for a few moments.\n",
        "\nThe &main-color=#89D6FF;Wavebuster&main-color=#FF6705B3; is the &main-color=#89D6FF;Wave&main-color=#FF6705B3; Charge Combo. This potent blast auto-seeks targets in the area.\n\n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nThe Wavebuster is a Sustained Fire Charge Combo. It costs 10 Missiles to activate, then 5 Missiles per second afterward.\n\nThe Wavebuster will seek enemies without a lock-on.\n\n\n\n\n\n\n\n\n\n\n",
        "The&main-color=#89D6FF; Plasma Beam&main-color=#FF6705B3; fires streams of molten energy. This Beam can ignite flammable objects and enemies.\n\nPress &image=SA,3.0,0.6,0.85,A9798329,2A13C23E; to select the Plasma Beam as your active weapon.\n  \n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nFire the Plasma Beam to open Red Doors.\n\nThe Plasma Beam is very effective against cold-based enemies.\n\nCharge the Plasma Beam to fire a sphere of plasma. Enemies struck by this blast will be engulfed in flames for a few moments.\n",
        "\nThe &main-color=#89D6FF;Flamethrower&main-color=#FF6705B3; is the &main-color=#89D6FF;Plasma&main-color=#FF6705B3; Charge Combo. You can sweep its stream of flame across multiple targets.\n\n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nFlamethrower is a Sustained Fire Charge Combo. It costs 10 Missiles to activate, then 5 Missiles per second afterward.\n\nThe Flamethrower is most effective against multiple targets in an area.\n",
        "The viral corruption of the Power Suit has altered the Arm Cannon as well. It is now capable of firing the powerful&main-color=#89D6FF; Phazon Beam&main-color=#FF6705B3;.\n \n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nThe Phazon Beam appears to trigger in the presence of high concentrations of Phazon.\n\nRegular Arm Cannon functions return when Phazon is not present.\n\nThe Charge Beam does not function when the Phazon Beam is active.\n",
        "The &main-color=#89D6FF;Space Jump Boots&main-color=#FF6705B3; increase the leaping capability of the Power Suit through the use of boot-mounted thrusters.  \n\nPress &image=SI,0.70,0.68,833BEE04; to jump, then press &image=SI,0.70,0.68,833BEE04; again during the jump to use the Space Jump Boots.\n\n\n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nTiming is important when using the Space Jump Boots. \n\nExperiment to discover ways to increase the height and length of your jumps.\n",
        "The &main-color=#89D6FF;Grapple Beam&main-color=#FF6705B3; allows you to swing back and forth from special points in the environment.  \n\nGrapple Points appear in your Visor as a &image=SI,0.70,0.68,2702E5E0; icon. \n\nPress and hold &image=SA,3.0,1.0,1.0,46434ED3,34E79314; to fire the Grapple Beam. \n\nHold &image=SA,3.0,1.0,1.0,46434ED3,34E79314; down to stay connected; let go to release.\n\n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nThe Grapple Beam can be used to cross large gaps.\n\nUse the &image=SA,7.0,0.6,1.0,C6C483AC,4050F102,8B0C22A7,4050F102,3A446C61,BCD01ECF,778CCD6A,BCD01ECF; while grappling to swing in different directions.\n",
        "The &main-color=#89D6FF;Missile Launcher&main-color=#FF6705B3; adds ballistic weapon capability to the Arm Cannon.\n\nPress &image=SI,1.0,0.68,EA2A1C5C; to fire the Missile Launcher. Press &image=SI,0.70,0.68,05AF9CAA; to return to Beam mode.\n\n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nMissiles fired with a lock-on will seek their targets.\n\nMissiles can destroy objects made from &main-color=#89D6FF;Radion&main-color=#FF6705B3; or &main-color=#89D6FF;Brinstone&main-color=#FF6705B3;.\n\nThere are Charge Combo enhancements scattered throughout the environment. They use the Missile Launcher and the Charge Beam in tandem to fire more effective blasts.\n\nEach Missile Expansion you find will increase the number of Missiles you can carry by 5.\n",
        "The &main-color=#89D6FF;Power Suit&main-color=#FF6705B3; is an advanced Chozo exoskeleton modified for use by Samus Aran.  \n\n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nThe Power Suit provides life-support functions and is well shielded from attack.  \n  \nThe modular nature of the Power Suit allows for the addition of weapons, Visors, and other gear as needed.\n\nThe Power Suit's shielding loses energy with each hit; collect energy when possible to keep the shielding charged.\n",
        "The &main-color=#89D6FF;Varia Suit&main-color=#FF6705B3; adds increased heat resistance to the Power Suit.\n\n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nThis modification increases your defensive shielding.\n\nWhile the Varia Suit can handle higher temperatures than normal, extreme heat sources and heat-based attacks will still cause damage.",
        "The &main-color=#89D6FF;Gravity Suit&main-color=#FF6705B3; eliminates the effects of liquid on movement.\n\n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nThis modification improves your defensive shielding.\n\nThe Gravity Suit allows for improved movement in liquid environments, but does not reduce damage delivered when exposed to hazardous fluids.\n\nVisor modifications in the Gravity Suit make it easier to see underwater.",
        "The Power Suit has been corrupted by viral exposure, turning it into the &main-color=#89D6FF;Phazon Suit&main-color=#FF6705B3;. \n\n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nThe viral corruption of the Power Suit has some beneficial side effects. \n\nThe suit is now resistant to the effects of Blue Phazon. The suit is not invulnerable to the effects of all Phazon, however.\n\nIn addition to Phazon resistance, the corruption has dramatically increased defensive shielding levels.",
        "The &main-color=#89D6FF;Energy Tanks&main-color=#FF6705B3; increase the power level available to your Suit's defense screens.\n\n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nEach Energy Tank increases your Suit's energy by 100 units. The more energy your Suit has, the longer you can stay alive.\n\nYou can fully recharge your Energy Tanks at Save Stations. Your gunship has this capability as well.",
        "The &main-color=#89D6FF;Morph Ball&main-color=#FF6705B3; changes your Suit into a compact, mobile sphere.  \n\nPress &image=SI,0.70,1.0,2176CFF9; to enter Morph Ball mode.\n\nPress &image=SI,0.70,1.0,2176CFF9; again to leave Morph Ball mode.\n\n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nLike the Power Suit, the Morph Ball is modular. There are several modifications that can be added to improve performance.",
        "The &main-color=#89D6FF;Boost Ball&main-color=#FF6705B3; can be used to increase the Morph Ball's speed for short periods.\n\nPress and hold &image=SI,0.70,0.68,833BEE04; to charge, then release &image=SI,0.70,0.68,833BEE04; to trigger a quick boost of speed.\n \n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nWhen charging, the longer you hold &image=SI,0.70,0.68,833BEE04;, the longer (and faster) the Boost Charge will be.\n\nThroughout the environment you will encounter U-shaped channels known as half-pipes. Using the Boost Ball in these areas will let you reach higher places. \n\nBuild a charge as you descend in the half-pipe, then trigger the Boost as you ascend the other side. This will give you the speed and momentum you need to reach new heights.\n",
        "The &main-color=#89D6FF;Spider Ball&main-color=#FF6705B3; allows you to move the Morph Ball along magnetic rails.\n\nPress and hold &image=A,3.0,08A2E4B9,F2425B21; to activate the Spider Ball ability.\n \n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nFollow the magnetic rails to explore new areas.\n\nThe Morph Ball Bomb can be used to trigger a Bomb Jump while attached to a rail.\n\n\n",
        "The &main-color=#89D6FF;Morph Ball Bomb&main-color=#FF6705B3; is the default weapon for the Morph Ball.\n\nPress &image=SI,0.70,0.68,05AF9CAA; when in Morph Ball mode to drop a Morph Ball Bomb. \n\n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nThe Morph Ball Bomb can be used to break cracked walls and activate certain devices.\n\nIf the Morph Ball is near a Morph Ball Bomb when it explodes, it will be popped a short distance into the air. This is called a&main-color=#89D6FF; Bomb Jump&main-color=#FF6705B3;. \n\nWhen a Morph Ball Bomb explodes, it must be close to the enemy to be effective.\n\nThe Morph Ball Bomb can easily break items made of&main-color=#89D6FF; Sandstone&main-color=#FF6705B3; or&main-color=#89D6FF; Talloric Alloy&main-color=#FF6705B3;.\n",
        "The &main-color=#89D6FF;Power Bomb&main-color=#FF6705B3; is the strongest Morph Ball weapon.\n\nPress &image=SI,1.0,0.68,EA2A1C5C; when in Morph Ball mode to drop a Power Bomb.  \n\n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nPower Bombs do not have unlimited ammo. Use them wisely.\n\nThe Power Bomb can destroy many materials, including &main-color=#89D6FF;Bendezium&main-color=#FF6705B3;.\n\nEach Power Bomb Expansion you find will increase the number of Power Bombs you can carry by 1.\n",
        "The &main-color=#89D6FF;Charge Beam&main-color=#FF6705B3; allows you to increase the damage and effectiveness of the Arm Cannon.\n\nPress and hold &image=SI,0.70,0.68,05AF9CAA; to charge the Arm Cannon, then release &image=SI,0.70,0.68,05AF9CAA; to fire.\n\n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nThe Charge Beam has a limited 'tractor beam' capacity.  Use it to pull small objects to you.\n\nThere are Charge Combo enhancements scattered through the environment.  They use the Charge Beam and the Missile Launcher in tandem to fire more effective blasts.\n\nThe Charge Beam increases the performance of each Arm Cannon mode.\n",
        "The &main-color=#89D6FF;Charge Combos&main-color=#FF6705B3; allow you to fire the Missile Launcher and Arm Cannon together. The combined attacks are stronger than normal blasts.\n\nThe Arm Cannon must be charged to use a Charge Combo.\n\nWhen your Arm Cannon is charged, press &image=SI,1.0,0.68,EA2A1C5C; to fire the Charge Combo.\n\n&main-color=#89D6FF;Samus's Notes:&main-color=#FF6705B3;\nThe &main-color=#89D6FF;Single Shot&main-color=#FF6705B3; Charge Combos fire one blast at a time. Each shot uses a number of Missiles.\n\n&main-color=#89D6FF;Sustained Fire&main-color=#FF6705B3; Charge Combos will fire as long as you have Missiles. Hold &image=SI,0.70,0.68,05AF9CAA; down after you fire. It takes ten Missiles to trigger these Charge Combos, then five Missiles per second afterward.\n\nPage down for information on the individual Charge Combos. \n\nThis data will download to the Log Book after each Charge Combo is acquired. \n\n\n\n\n\n\n\n\n\n",
        "On",
        "Off",
        "Mono",
        "Stereo",
        "Dolby",
        "Zoom",
    ]
}
