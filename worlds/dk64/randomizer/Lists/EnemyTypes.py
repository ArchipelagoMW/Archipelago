"""List of enemies with in-game index."""

from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING, Any, List, Union

from randomizer.Enums.Locations import Locations
from randomizer.Enums.EnemySubtypes import EnemySubtype
from randomizer.Enums.Enemies import Enemies
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Regions import Regions

ENEMY_REPLACEMENT_PRIORITY = {
    EnemySubtype.GroundSimple: [EnemySubtype.GroundBeefy, EnemySubtype.Water, EnemySubtype.Air],
    EnemySubtype.GroundBeefy: [EnemySubtype.GroundSimple, EnemySubtype.Water, EnemySubtype.Air],
    EnemySubtype.Water: [EnemySubtype.Air, EnemySubtype.GroundSimple, EnemySubtype.GroundBeefy],
    EnemySubtype.Air: [EnemySubtype.GroundSimple, EnemySubtype.GroundBeefy, EnemySubtype.Water],
}

INSTRUMENT_RESTRICTED_REGIONS = {
    Regions.MillAttic,
    Regions.SpiderRoom,
    Regions.DonkeyCabin,
    Regions.DiddyLowerCabin,
    Regions.LankyCabin,
    Regions.TinyCabin,
    Regions.ChunkyCabin,
    Regions.ChunkyIgloo,
    Regions.AngryAztecLobby,
}


class InteractionMethods:
    """Information about interactions with enemies."""

    def __init__(
        self,
        *,
        kill_melee=True,  # Killing can be done with regular attacks
        kill_orange=True,  # Killing can be done with oranges
        kill_gun=True,  # Killing can be done with a gun
        kill_shockwave=True,  # Killing can be done with a shockwave attack
        kill_instrument=True,  # Killing can be done with an instrument play
        kill_punch=False,  # Killing can be done by primate punching the enemy (when melee attacks don't work)
        kill_hunky=False,  # Killing can be done by squishing them with hunky
        can_kill=True,  # Master control of all kill variables
        can_bypass=True,  # Enemy can be bypassed without any additional tricks
    ) -> None:
        """Initialize with given data."""
        self.kill_melee = kill_melee and can_kill
        self.kill_orange = kill_orange and can_kill
        self.kill_gun = kill_gun and can_kill
        self.kill_shockwave = kill_shockwave and can_kill
        self.kill_instrument = kill_instrument and can_kill
        self.kill_punch = kill_punch and can_kill
        self.kill_hunky = kill_hunky and can_kill
        self.can_bypass = can_bypass


class EnemyData:
    """Information about the enemy."""

    def __init__(
        self,
        *,
        name="",
        e_type=EnemySubtype.NoType,
        aggro=1,
        min_speed=15,
        max_speed=150,
        crown_enabled=True,
        air=False,
        size_cap=0,
        crown_weight=0,
        simple=False,
        minigame_enabled=True,
        killable=True,
        beaver=False,
        kasplat=False,
        disruptive=0,
        bbbarrage_min_scale=50,
        selector_enabled=True,
        interaction: InteractionMethods = None,
        placeable=True,
        default_size=None,
    ) -> None:
        """Initialize with given parameters."""
        self.name = name
        self.e_type = e_type
        self.aggro = aggro
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.crown_enabled = crown_enabled
        self.air = air
        self.size_cap = size_cap
        self.crown_weight = crown_weight
        self.simple = simple
        self.minigame_enabled = minigame_enabled
        self.killable = killable
        self.beaver = beaver
        self.kasplat = kasplat
        self.disruptive = disruptive
        self.bbbarrage_min_scale = bbbarrage_min_scale
        self.selector_enabled = selector_enabled
        self.interaction = interaction
        self.placeable = placeable
        self.default_size = default_size
        if air:
            self.minigame_enabled = False


def getEnemyPermitted(enemy_type: EnemySubtype, banned_enemies: list):
    """Get list of permitted enemies for a group."""
    return [enemy for enemy in EnemyMetaData if EnemyMetaData[enemy].e_type == enemy_type and enemy not in banned_enemies and EnemyMetaData[enemy].placeable]


class EnemyLoc:
    """Information about an enemy."""

    def __init__(
        self,
        map: Maps,
        default_enemy: Enemies,
        id: int,
        banned_enemies: List[Union[Any, Enemies]],
        enable_randomization: bool,
        respawns: bool = True,
    ) -> None:
        """Initialize with given parameters."""
        self.map = map
        self.default_enemy = default_enemy
        self.enemy = default_enemy
        self.id = id
        self.banned_enemies = banned_enemies.copy()
        self.enable_randomization = enable_randomization
        self.default_type = EnemySubtype.GroundSimple
        self.allowed_enemies = [[], [], [], []]
        self.idle_speed: int = None
        self.aggro_speed: int = None
        self.respawns = respawns
        if enable_randomization:
            if default_enemy in EnemyMetaData:
                self.default_type = EnemyMetaData[default_enemy].e_type
            self.allowed_enemies[0] = getEnemyPermitted(self.default_type, banned_enemies)
            if self.default_type in list(ENEMY_REPLACEMENT_PRIORITY.keys()):
                for xi, x in enumerate(ENEMY_REPLACEMENT_PRIORITY[self.default_type]):
                    self.allowed_enemies[xi + 1] = getEnemyPermitted(x, banned_enemies)

    def placeNewEnemy(self, random, enabled_enemies: List[Any], enable_speed: bool) -> Enemies:
        """Place new enemy in slot."""
        if self.enable_randomization:
            permitted = []
            for x in range(4):
                if len(permitted) == 0:
                    permitted = [enemy for enemy in self.allowed_enemies[x] if enemy in enabled_enemies and EnemyMetaData[enemy].selector_enabled]
                    guard_count = len([e for e in permitted if e in kops])
                    if guard_count > 1:
                        new_permitted = []
                        for enemy in permitted:
                            if enemy in kops:
                                new_permitted.append(enemy)
                            else:
                                for _ in range(guard_count):
                                    new_permitted.append(enemy)
                        permitted = new_permitted.copy()
            if len(permitted) > 0:
                self.enemy = random.choice(permitted)
            if enable_speed and self.enemy in EnemyMetaData:
                enemy_data = EnemyMetaData[self.enemy]
                self.aggro_speed = random.randint(enemy_data.min_speed, enemy_data.max_speed)
        return self.enemy

    def canKill(self, logic_variable, instrument_restricted=None) -> bool:
        """Determine if the enemy can be killed."""
        if self.enemy in EnemyMetaData:
            interaction: InteractionMethods = EnemyMetaData[self.enemy].interaction
            if interaction is not None:
                if interaction.kill_melee:
                    return True
                if interaction.kill_orange and logic_variable.oranges:
                    return True
                if interaction.kill_gun and logic_variable.HasGun(Kongs.any):
                    return True
                if interaction.kill_shockwave and logic_variable.shockwave:
                    return True
                if interaction.kill_instrument and logic_variable.HasInstrument(Kongs.any):
                    if instrument_restricted is not None:
                        return not instrument_restricted
                    return True
                if interaction.kill_punch and logic_variable.punch and logic_variable.ischunky:
                    return True
                if interaction.kill_hunky and logic_variable.hunkyChunky and logic_variable.ischunky:
                    return True
        return False

    def canDropItem(self, logic_variable, instrument_restricted=None):
        """Determine if the enemy can drop an item."""
        return self.canKill(logic_variable, instrument_restricted) and self.enemy not in [Enemies.Book]  # Checking evil tomato

    def canBypass(self) -> bool:
        """Determine if the enemy can be bypassed."""
        if self.enemy in EnemyMetaData:
            interaction: InteractionMethods = EnemyMetaData[self.enemy].interaction
            if interaction is not None:
                return interaction.can_bypass
        return False


BEAVER_DEFAULT_SIZE = 80
KLAPTRAP_DEFAULT_SIZE = 65
ZINGER_DEFAULT_SIZE = 70
BARREL_ENEMY_DEFAULT_SIZE = 50

EnemyMetaData = {
    Enemies.BeaverBlue: EnemyData(
        name="Beaver (Blue)",
        e_type=EnemySubtype.GroundSimple,
        crown_weight=10,
        simple=True,
        bbbarrage_min_scale=70,
        beaver=True,
        interaction=InteractionMethods(),
        default_size=BEAVER_DEFAULT_SIZE,
    ),  #
    Enemies.Book: EnemyData(
        name="Book",
        aggro=6,
        crown_enabled=False,
        air=True,
        minigame_enabled=False,
        selector_enabled=False,
        interaction=InteractionMethods(can_kill=False),
        placeable=False,
        default_size=50,
    ),
    Enemies.ZingerCharger: EnemyData(
        name="Zinger (Charger)",
        e_type=EnemySubtype.Air,
        air=True,
        crown_weight=7,
        disruptive=1,
        interaction=InteractionMethods(kill_melee=False, kill_orange=False, kill_shockwave=False),
        default_size=ZINGER_DEFAULT_SIZE,
    ),  #
    Enemies.Klobber: EnemyData(
        name="Klobber",
        e_type=EnemySubtype.GroundBeefy,
        aggro=4,
        crown_weight=2,
        killable=False,
        disruptive=2,
        interaction=InteractionMethods(kill_gun=False, kill_melee=False),
        default_size=BARREL_ENEMY_DEFAULT_SIZE,
    ),
    Enemies.Klump: EnemyData(
        name="Klump",
        e_type=EnemySubtype.GroundBeefy,
        crown_weight=1,
        killable=False,
        disruptive=1,
        interaction=InteractionMethods(kill_gun=False, kill_melee=False),
        default_size=50,
    ),  #
    Enemies.Kaboom: EnemyData(
        name="Kaboom",
        e_type=EnemySubtype.GroundBeefy,
        aggro=4,
        crown_weight=2,
        killable=False,
        disruptive=2,
        interaction=InteractionMethods(kill_gun=False, kill_melee=False),
        default_size=BARREL_ENEMY_DEFAULT_SIZE,
    ),
    Enemies.KlaptrapGreen: EnemyData(
        name="Klaptrap (Green)",
        e_type=EnemySubtype.GroundSimple,
        crown_weight=8,
        simple=True,
        bbbarrage_min_scale=100,
        interaction=InteractionMethods(),
        default_size=KLAPTRAP_DEFAULT_SIZE,
    ),  #
    Enemies.ZingerLime: EnemyData(
        name="Zinger (Lime Thrower)",
        e_type=EnemySubtype.Air,
        air=True,
        crown_weight=5,
        disruptive=1,
        interaction=InteractionMethods(kill_orange=False, kill_melee=False, kill_shockwave=False),
        default_size=ZINGER_DEFAULT_SIZE,
    ),  #
    Enemies.KlaptrapPurple: EnemyData(
        name="Klaptrap (Purple)",
        e_type=EnemySubtype.GroundBeefy,
        crown_weight=2,
        killable=False,
        disruptive=1,
        interaction=InteractionMethods(kill_gun=False, kill_melee=False, kill_shockwave=False),
        default_size=KLAPTRAP_DEFAULT_SIZE,
    ),  #
    Enemies.KlaptrapRed: EnemyData(
        name="Klaptrap (Red)",
        e_type=EnemySubtype.GroundBeefy,
        crown_weight=2,
        killable=False,
        disruptive=1,
        interaction=InteractionMethods(kill_melee=False, kill_shockwave=False),
        default_size=KLAPTRAP_DEFAULT_SIZE,
    ),  #
    Enemies.BeaverGold: EnemyData(
        name="Beaver (Gold)",
        e_type=EnemySubtype.GroundSimple,
        crown_weight=10,
        simple=True,
        bbbarrage_min_scale=70,
        beaver=True,
        interaction=InteractionMethods(),
        default_size=BEAVER_DEFAULT_SIZE,
    ),  #
    Enemies.MushroomMan: EnemyData(
        name="Mushroom Man",
        e_type=EnemySubtype.GroundSimple,
        aggro=4,
        size_cap=60,
        crown_weight=10,
        simple=True,
        bbbarrage_min_scale=50,
        interaction=InteractionMethods(),
        default_size=45,
    ),
    Enemies.Ruler: EnemyData(
        name="Ruler",
        e_type=EnemySubtype.GroundSimple,
        crown_weight=10,
        simple=True,
        bbbarrage_min_scale=50,
        interaction=InteractionMethods(),
        default_size=50,
    ),  #
    Enemies.RoboKremling: EnemyData(
        name="Robo-Kremling",
        e_type=EnemySubtype.GroundBeefy,
        crown_weight=2,
        killable=False,
        disruptive=1,
        interaction=InteractionMethods(kill_melee=False, kill_gun=False, kill_punch=True),
        default_size=50,
    ),  #
    Enemies.Kremling: EnemyData(
        name="Kremling",
        e_type=EnemySubtype.GroundSimple,
        crown_weight=10,
        simple=True,
        bbbarrage_min_scale=50,
        interaction=InteractionMethods(),
        default_size=64,
    ),  #
    Enemies.KasplatDK: EnemyData(
        name="Kasplat (DK)",
        crown_weight=6,
        kasplat=True,
        interaction=InteractionMethods(),
        placeable=False,
    ),  #
    Enemies.KasplatDiddy: EnemyData(
        name="Kasplat (Diddy)",
        crown_weight=6,
        kasplat=True,
        interaction=InteractionMethods(),
        placeable=False,
    ),  #
    Enemies.KasplatLanky: EnemyData(
        name="Kasplat (Lanky)",
        crown_weight=6,
        kasplat=True,
        interaction=InteractionMethods(),
        placeable=False,
    ),  #
    Enemies.KasplatTiny: EnemyData(
        name="Kasplat (Tiny)",
        crown_weight=6,
        kasplat=True,
        interaction=InteractionMethods(),
        placeable=False,
    ),  #
    Enemies.KasplatChunky: EnemyData(
        name="Kasplat (Chunky)",
        crown_weight=6,
        kasplat=True,
        interaction=InteractionMethods(),
        placeable=False,
    ),  #
    Enemies.ZingerRobo: EnemyData(
        name="Robo-Zingers",
        e_type=EnemySubtype.Air,
        air=True,
        crown_weight=5,
        disruptive=1,
        interaction=InteractionMethods(kill_melee=False, kill_orange=False, kill_shockwave=False),
        default_size=50,
    ),  #
    Enemies.Krossbones: EnemyData(
        name="Krossbones",
        e_type=EnemySubtype.GroundSimple,
        crown_weight=10,
        simple=True,
        bbbarrage_min_scale=50,
        interaction=InteractionMethods(),
        default_size=60,
    ),  #
    Enemies.Shuri: EnemyData(
        name="Shuri",
        e_type=EnemySubtype.Water,
        crown_enabled=False,
        minigame_enabled=False,
        interaction=InteractionMethods(kill_melee=False, kill_gun=False, kill_shockwave=False),
        default_size=100,
        size_cap=100,  # Too big causes the game to crash, so just gonna limit it to size 100. Size 127 seems to be fine
    ),  #
    Enemies.Gimpfish: EnemyData(
        name="Gimpfish",
        e_type=EnemySubtype.Water,
        aggro=1,
        crown_enabled=False,
        minigame_enabled=False,
        interaction=InteractionMethods(kill_melee=False, kill_gun=False, kill_shockwave=False),
        default_size=110,
        size_cap=110,  # Runs the same code as the shuri, lets not tempt fate
    ),
    Enemies.MrDice0: EnemyData(
        name="Mr Dice (Green)",
        e_type=EnemySubtype.GroundSimple,
        crown_weight=10,
        simple=True,
        bbbarrage_min_scale=80,
        interaction=InteractionMethods(),
        default_size=160,
    ),  # Should be aggro 4, but I think this is because it normally spawns in the BHDM fight
    Enemies.SirDomino: EnemyData(
        name="Sir Domino",
        e_type=EnemySubtype.GroundSimple,
        crown_weight=10,
        simple=True,
        bbbarrage_min_scale=60,
        interaction=InteractionMethods(),
        default_size=70,
    ),  #
    Enemies.MrDice1: EnemyData(
        name="Mr Dice (Red)",
        e_type=EnemySubtype.GroundSimple,
        crown_weight=10,
        simple=True,
        bbbarrage_min_scale=100,
        interaction=InteractionMethods(),
        default_size=80,
    ),  #
    Enemies.FireballGlasses: EnemyData(
        name="Fireball with Glasses",
        e_type=EnemySubtype.GroundSimple,
        aggro=35,
        min_speed=100,
        max_speed=255,
        crown_weight=10,
        killable=False,
        interaction=InteractionMethods(kill_gun=False, kill_orange=False),
        default_size=50,
    ),  # 29 for if you want them to respond to the rabbit
    Enemies.SpiderSmall: EnemyData(
        name="Spider",
        e_type=EnemySubtype.GroundSimple,
        crown_weight=7,
        disruptive=1,
        crown_enabled=False,
        interaction=InteractionMethods(),
        default_size=55,
    ),  # with projectiles, disruptive will need to be set to 2
    Enemies.Bat: EnemyData(
        name="Bat",
        e_type=EnemySubtype.Air,
        air=True,
        crown_weight=5,
        minigame_enabled=False,
        disruptive=1,
        interaction=InteractionMethods(kill_melee=False, kill_orange=False, kill_shockwave=False),
        default_size=70,
    ),  #
    Enemies.EvilTomato: EnemyData(
        name="Evil Tomato",
        aggro=4,
        crown_enabled=False,
        minigame_enabled=False,
        selector_enabled=False,
        interaction=InteractionMethods(kill_hunky=True, kill_melee=False, kill_orange=False, kill_gun=False, kill_shockwave=False, kill_instrument=False),  # Can be killed with Hunky
        placeable=False,
        default_size=140,
    ),
    Enemies.Ghost: EnemyData(
        name="Ghost",
        e_type=EnemySubtype.GroundSimple,
        crown_weight=10,
        simple=True,
        bbbarrage_min_scale=70,
        interaction=InteractionMethods(),
        default_size=50,
    ),  #
    Enemies.Pufftup: EnemyData(
        name="Pufftup",
        e_type=EnemySubtype.Water,
        crown_enabled=False,
        size_cap=40,
        minigame_enabled=False,
        interaction=InteractionMethods(kill_gun=False, kill_orange=False, kill_shockwave=False),
        default_size=50,
    ),  #
    Enemies.Kosha: EnemyData(
        name="Kosha",
        e_type=EnemySubtype.GroundBeefy,
        crown_weight=1,
        killable=False,
        disruptive=2,
        interaction=InteractionMethods(kill_gun=False, kill_melee=False),
        default_size=50,
    ),  #
    Enemies.GetOut: EnemyData(
        name="Get Out Guy",
        aggro=6,
        crown_weight=1,
        minigame_enabled=False,
        disruptive=1,
        interaction=InteractionMethods(can_kill=False),
        placeable=False,
    ),
    Enemies.Guard: EnemyData(
        name="Kop (Warp Out)",
        e_type=EnemySubtype.GroundBeefy,
        aggro=1,
        crown_enabled=False,
        minigame_enabled=False,
        interaction=InteractionMethods(kill_melee=False, can_bypass=False, kill_shockwave=False),  # Can be meleed with distraction mechanic, but we'll ignore that for now
        default_size=50,
        max_speed=100,
    ),
    Enemies.GuardDisableA: EnemyData(
        name="Kop (Disable A)",
        e_type=EnemySubtype.GroundBeefy,
        aggro=1,
        crown_enabled=False,
        minigame_enabled=False,
        interaction=InteractionMethods(kill_melee=False, can_bypass=False, kill_shockwave=False),  # Can be meleed with distraction mechanic, but we'll ignore that for now
        default_size=50,
        max_speed=100,
    ),
    Enemies.GuardDisableZ: EnemyData(
        name="Kop (Disable Z)",
        e_type=EnemySubtype.GroundBeefy,
        aggro=1,
        crown_enabled=False,
        minigame_enabled=False,
        interaction=InteractionMethods(kill_melee=False, can_bypass=False, kill_shockwave=False),  # Can be meleed with distraction mechanic, but we'll ignore that for now
        default_size=50,
        max_speed=100,
    ),
    Enemies.GuardTag: EnemyData(
        name="Kop (Disable Tag Anywhere)",
        e_type=EnemySubtype.GroundBeefy,
        aggro=1,
        crown_enabled=False,
        minigame_enabled=False,
        interaction=InteractionMethods(kill_melee=False, can_bypass=False, kill_shockwave=False),  # Can be meleed with distraction mechanic, but we'll ignore that for now
        default_size=50,
        max_speed=100,
    ),
    Enemies.GuardGetOut: EnemyData(
        name="Kop (Get Out)",
        e_type=EnemySubtype.GroundBeefy,
        aggro=1,
        crown_enabled=False,
        minigame_enabled=False,
        interaction=InteractionMethods(kill_melee=False, can_bypass=False, kill_shockwave=False),  # Can be meleed with distraction mechanic, but we'll ignore that for now
        default_size=50,
        max_speed=100,
    ),
    Enemies.Bug: EnemyData(
        name="Bug",
        e_type=EnemySubtype.Air,
        air=True,
        crown_weight=7,
        disruptive=1,
        interaction=InteractionMethods(kill_melee=False, kill_orange=False, kill_shockwave=False),
        default_size=75,
    ),
    Enemies.ZingerFlamethrower: EnemyData(
        name="Zinger (Flamethrower)",
        e_type=EnemySubtype.Air,
        air=True,
        crown_weight=7,
        disruptive=1,
        interaction=InteractionMethods(kill_melee=False, kill_orange=False, kill_shockwave=False),
        selector_enabled=False,
        default_size=ZINGER_DEFAULT_SIZE,
    ),
    Enemies.Scarab: EnemyData(
        name="Scarab",
        e_type=EnemySubtype.GroundSimple,
        air=True,
        crown_enabled=False,
        interaction=InteractionMethods(),
        size_cap=50,
        selector_enabled=False,
        default_size=50,
    ),
}

kops = [Enemies.Guard, Enemies.GuardDisableA, Enemies.GuardDisableZ, Enemies.GuardTag, Enemies.GuardGetOut]
enemies_nokill_gun = [enemy for enemy in EnemyMetaData if ((not EnemyMetaData[enemy].interaction.kill_gun) and (not EnemyMetaData[enemy].interaction.kill_melee)) or enemy in kops]
enemies_shockwave_immune = [
    Enemies.Bat,
    Enemies.KlaptrapPurple,
    Enemies.KlaptrapRed,
    Enemies.ZingerCharger,
    Enemies.ZingerLime,
    Enemies.ZingerRobo,
]
enemies_not_ground_simple = [enemy for enemy in EnemyMetaData if EnemyMetaData[enemy].e_type != EnemySubtype.GroundSimple]
enemy_5dc_ban = [Enemies.Kosha] + kops

enemy_location_list = {
    # Japes
    # Main
    Locations.JapesMainEnemy_Start: EnemyLoc(Maps.JungleJapes, Enemies.BeaverBlue, 2, [], True),
    Locations.JapesMainEnemy_DiddyCavern: EnemyLoc(Maps.JungleJapes, Enemies.BeaverBlue, 4, [], True),
    Locations.JapesMainEnemy_Tunnel0: EnemyLoc(Maps.JungleJapes, Enemies.BeaverBlue, 5, [], True),
    Locations.JapesMainEnemy_Tunnel1: EnemyLoc(Maps.JungleJapes, Enemies.BeaverBlue, 6, [], True),
    Locations.JapesMainEnemy_Storm0: EnemyLoc(Maps.JungleJapes, Enemies.BeaverBlue, 15, [], True),
    Locations.JapesMainEnemy_Storm1: EnemyLoc(Maps.JungleJapes, Enemies.BeaverBlue, 18, [], True),
    Locations.JapesMainEnemy_Storm2: EnemyLoc(Maps.JungleJapes, Enemies.BeaverBlue, 20, [], True),
    Locations.JapesMainEnemy_Hive0: EnemyLoc(Maps.JungleJapes, Enemies.ZingerLime, 28, [], True),
    Locations.JapesMainEnemy_Hive1: EnemyLoc(Maps.JungleJapes, Enemies.ZingerLime, 29, [], True),
    Locations.JapesMainEnemy_Hive2: EnemyLoc(Maps.JungleJapes, Enemies.ZingerLime, 30, [], True),
    Locations.JapesMainEnemy_Hive3: EnemyLoc(Maps.JungleJapes, Enemies.Kremling, 36, [], True),
    Locations.JapesMainEnemy_Hive4: EnemyLoc(Maps.JungleJapes, Enemies.Kremling, 37, [], True),
    Locations.JapesMainEnemy_KilledInDemo: EnemyLoc(Maps.JungleJapes, Enemies.BeaverBlue, 33, [], True),
    Locations.JapesMainEnemy_NearUnderground: EnemyLoc(Maps.JungleJapes, Enemies.ZingerCharger, 49, [], True),
    Locations.JapesMainEnemy_NearPainting0: EnemyLoc(Maps.JungleJapes, Enemies.BeaverBlue, 34, [], True),
    Locations.JapesMainEnemy_NearPainting1: EnemyLoc(Maps.JungleJapes, Enemies.BeaverBlue, 35, [], True),
    Locations.JapesMainEnemy_NearPainting2: EnemyLoc(Maps.JungleJapes, Enemies.ZingerCharger, 48, [], True),
    Locations.JapesMainEnemy_Mountain: EnemyLoc(Maps.JungleJapes, Enemies.ZingerCharger, 50, [], True),
    Locations.JapesMainEnemy_FeatherTunnel: EnemyLoc(Maps.JungleJapes, Enemies.ZingerLime, 52, [], True),
    Locations.JapesMainEnemy_MiddleTunnel: EnemyLoc(Maps.JungleJapes, Enemies.BeaverBlue, 54, [], True),
    # Lobby
    Locations.JapesLobbyEnemy_Enemy0: EnemyLoc(Maps.JungleJapesLobby, Enemies.BeaverBlue, 1, [], True),
    Locations.JapesLobbyEnemy_Enemy1: EnemyLoc(Maps.JungleJapesLobby, Enemies.BeaverBlue, 2, [], True),
    # Painting
    Locations.JapesPaintingEnemy_Gauntlet0: EnemyLoc(Maps.JapesLankyCave, Enemies.ZingerCharger, 2, enemies_nokill_gun, True, False),
    Locations.JapesPaintingEnemy_Gauntlet1: EnemyLoc(Maps.JapesLankyCave, Enemies.ZingerCharger, 3, enemies_nokill_gun, True, False),
    Locations.JapesPaintingEnemy_Gauntlet2: EnemyLoc(Maps.JapesLankyCave, Enemies.ZingerCharger, 4, enemies_nokill_gun, True, False),
    Locations.JapesPaintingEnemy_Gauntlet3: EnemyLoc(Maps.JapesLankyCave, Enemies.ZingerCharger, 5, enemies_nokill_gun, True, False),
    Locations.JapesPaintingEnemy_Gauntlet4: EnemyLoc(Maps.JapesLankyCave, Enemies.ZingerCharger, 6, enemies_nokill_gun, True, False),
    # Mountain
    Locations.JapesMountainEnemy_Start0: EnemyLoc(Maps.JapesMountain, Enemies.BeaverBlue, 1, [], True),
    Locations.JapesMountainEnemy_Start1: EnemyLoc(Maps.JapesMountain, Enemies.BeaverBlue, 2, [], True),
    Locations.JapesMountainEnemy_Start2: EnemyLoc(Maps.JapesMountain, Enemies.BeaverBlue, 6, [], True),
    Locations.JapesMountainEnemy_Start3: EnemyLoc(Maps.JapesMountain, Enemies.ZingerCharger, 8, [], True),
    Locations.JapesMountainEnemy_Start4: EnemyLoc(Maps.JapesMountain, Enemies.ZingerCharger, 9, [], True),
    Locations.JapesMountainEnemy_NearGateSwitch0: EnemyLoc(Maps.JapesMountain, Enemies.ZingerLime, 13, [], True),
    Locations.JapesMountainEnemy_NearGateSwitch1: EnemyLoc(Maps.JapesMountain, Enemies.ZingerLime, 14, [], True),
    Locations.JapesMountainEnemy_HiLo: EnemyLoc(Maps.JapesMountain, Enemies.Klump, 15, kops, True),
    Locations.JapesMountainEnemy_Conveyor0: EnemyLoc(Maps.JapesMountain, Enemies.Klump, 16, [], True),
    Locations.JapesMountainEnemy_Conveyor1: EnemyLoc(Maps.JapesMountain, Enemies.Klump, 17, [], True),
    # Shellhive
    Locations.JapesShellhiveEnemy_FirstRoom: EnemyLoc(Maps.JapesTinyHive, Enemies.KlaptrapPurple, 7, [], True),
    Locations.JapesShellhiveEnemy_SecondRoom0: EnemyLoc(Maps.JapesTinyHive, Enemies.KlaptrapPurple, 8, [], True),
    Locations.JapesShellhiveEnemy_SecondRoom1: EnemyLoc(Maps.JapesTinyHive, Enemies.KlaptrapPurple, 9, [], True),
    Locations.JapesShellhiveEnemy_ThirdRoom0: EnemyLoc(Maps.JapesTinyHive, Enemies.KlaptrapPurple, 10, [], True),
    Locations.JapesShellhiveEnemy_ThirdRoom1: EnemyLoc(Maps.JapesTinyHive, Enemies.KlaptrapPurple, 11, [], True),
    Locations.JapesShellhiveEnemy_ThirdRoom2: EnemyLoc(Maps.JapesTinyHive, Enemies.ZingerCharger, 12, [], True),
    Locations.JapesShellhiveEnemy_ThirdRoom3: EnemyLoc(Maps.JapesTinyHive, Enemies.ZingerCharger, 13, [], True),
    Locations.JapesShellhiveEnemy_MainRoom: EnemyLoc(Maps.JapesTinyHive, Enemies.ZingerCharger, 14, [], True),
    # Angry Aztec
    # Main
    Locations.AztecMainEnemy_VaseRoom0: EnemyLoc(Maps.AngryAztec, Enemies.ZingerLime, 2, [], True),
    Locations.AztecMainEnemy_VaseRoom1: EnemyLoc(Maps.AngryAztec, Enemies.ZingerLime, 4, [], True),
    Locations.AztecMainEnemy_VaseRoom2: EnemyLoc(Maps.AngryAztec, Enemies.ZingerLime, 1, [], True),
    Locations.AztecMainEnemy_TunnelPad0: EnemyLoc(Maps.AngryAztec, Enemies.ZingerLime, 10, [], True),
    Locations.AztecMainEnemy_TunnelCage0: EnemyLoc(Maps.AngryAztec, Enemies.KlaptrapGreen, 13, [], True),
    Locations.AztecMainEnemy_TunnelCage1: EnemyLoc(Maps.AngryAztec, Enemies.KlaptrapGreen, 14, [], True),
    Locations.AztecMainEnemy_TunnelCage2: EnemyLoc(Maps.AngryAztec, Enemies.KlaptrapGreen, 15, [], True),
    Locations.AztecMainEnemy_StartingTunnel0: EnemyLoc(Maps.AngryAztec, Enemies.Kremling, 20, [], True),
    Locations.AztecMainEnemy_StartingTunnel1: EnemyLoc(Maps.AngryAztec, Enemies.Kremling, 21, [], True),
    Locations.AztecMainEnemy_OasisDoor: EnemyLoc(Maps.AngryAztec, Enemies.Kremling, 23, [], True),
    Locations.AztecMainEnemy_TunnelCage3: EnemyLoc(Maps.AngryAztec, Enemies.Kremling, 26, [], True),
    Locations.AztecMainEnemy_OutsideLlama: EnemyLoc(Maps.AngryAztec, Enemies.Kremling, 27, [], True),
    Locations.AztecMainEnemy_OutsideTower: EnemyLoc(Maps.AngryAztec, Enemies.Kremling, 28, [], True),
    Locations.AztecMainEnemy_TunnelPad1: EnemyLoc(Maps.AngryAztec, Enemies.ZingerLime, 31, [], True),
    Locations.AztecMainEnemy_NearCandy: EnemyLoc(Maps.AngryAztec, Enemies.ZingerLime, 32, [], True),
    Locations.AztecMainEnemy_AroundTotem: EnemyLoc(Maps.AngryAztec, Enemies.KlaptrapGreen, 33, [], True),
    Locations.AztecMainEnemy_StartingTunnel2: EnemyLoc(Maps.AngryAztec, Enemies.ZingerCharger, 38, [], True),
    Locations.AztecMainEnemy_StartingTunnel3: EnemyLoc(Maps.AngryAztec, Enemies.ZingerCharger, 39, [], True),
    Locations.AztecMainEnemy_OutsideSnide: EnemyLoc(Maps.AngryAztec, Enemies.KlaptrapGreen, 40, [], True),
    Locations.AztecMainEnemy_Outside5DT: EnemyLoc(Maps.AngryAztec, Enemies.ZingerLime, 41, [], True),
    Locations.AztecMainEnemy_NearSnoopTunnel: EnemyLoc(Maps.AngryAztec, Enemies.Kremling, 42, [], True),
    # Lobby
    Locations.AztecLobbyEnemy_Pad0: EnemyLoc(Maps.AngryAztecLobby, Enemies.ZingerCharger, 2, [], True, False),
    Locations.AztecLobbyEnemy_Pad1: EnemyLoc(Maps.AngryAztecLobby, Enemies.ZingerCharger, 3, [], True, False),
    # DK 5DT
    Locations.AztecDK5DTEnemy_StartTrap0: EnemyLoc(Maps.AztecDonkey5DTemple, Enemies.Kaboom, 5, [], True),
    Locations.AztecDK5DTEnemy_StartTrap1: EnemyLoc(Maps.AztecDonkey5DTemple, Enemies.Kaboom, 6, [], True),
    Locations.AztecDK5DTEnemy_StartTrap2: EnemyLoc(Maps.AztecDonkey5DTemple, Enemies.Kaboom, 7, [], True),
    Locations.AztecDK5DTEnemy_EndTrap0: EnemyLoc(Maps.AztecDonkey5DTemple, Enemies.Kaboom, 10, [], True),
    Locations.AztecDK5DTEnemy_EndTrap1: EnemyLoc(Maps.AztecDonkey5DTemple, Enemies.Kaboom, 11, [], True),
    Locations.AztecDK5DTEnemy_EndTrap2: EnemyLoc(Maps.AztecDonkey5DTemple, Enemies.Kaboom, 12, [], True),
    Locations.AztecDK5DTEnemy_EndPath0: EnemyLoc(Maps.AztecDonkey5DTemple, Enemies.KlaptrapPurple, 13, kops, True),
    Locations.AztecDK5DTEnemy_EndPath1: EnemyLoc(Maps.AztecDonkey5DTemple, Enemies.KlaptrapPurple, 14, kops, True),
    Locations.AztecDK5DTEnemy_StartPath: EnemyLoc(Maps.AztecDonkey5DTemple, Enemies.KlaptrapPurple, 15, [], True),
    # Diddy 5DT
    Locations.AztecDiddy5DTEnemy_EndTrap0: EnemyLoc(Maps.AztecDiddy5DTemple, Enemies.Klobber, 4, [], True),
    Locations.AztecDiddy5DTEnemy_EndTrap1: EnemyLoc(Maps.AztecDiddy5DTemple, Enemies.Klobber, 5, [], True),
    Locations.AztecDiddy5DTEnemy_EndTrap2: EnemyLoc(Maps.AztecDiddy5DTemple, Enemies.Klobber, 6, [], True),
    Locations.AztecDiddy5DTEnemy_StartLeft0: EnemyLoc(Maps.AztecDiddy5DTemple, Enemies.Kremling, 9, [], True),
    Locations.AztecDiddy5DTEnemy_StartLeft1: EnemyLoc(Maps.AztecDiddy5DTemple, Enemies.Kremling, 10, [], True),
    Locations.AztecDiddy5DTEnemy_Reward: EnemyLoc(Maps.AztecDiddy5DTemple, Enemies.Klump, 11, [], True),
    Locations.AztecDiddy5DTEnemy_SecondSwitch: EnemyLoc(Maps.AztecDiddy5DTemple, Enemies.Kremling, 12, [], True),
    # Lanky 5DT
    Locations.AztecLanky5DTEnemy_JoiningPaths: EnemyLoc(Maps.AztecLanky5DTemple, Enemies.Klump, 2, [], True),
    Locations.AztecLanky5DTEnemy_EndTrap: EnemyLoc(Maps.AztecLanky5DTemple, Enemies.Klump, 3, [], True),
    Locations.AztecLanky5DTEnemy_Reward: EnemyLoc(Maps.AztecLanky5DTemple, Enemies.Klump, 4, [], True),
    # Tiny 5DT
    Locations.AztecTiny5DTEnemy_StartRightFront: EnemyLoc(Maps.AztecTiny5DTemple, Enemies.ZingerLime, 2, [], True),
    Locations.AztecTiny5DTEnemy_StartLeftBack: EnemyLoc(Maps.AztecTiny5DTemple, Enemies.ZingerLime, 4, [], True),
    Locations.AztecTiny5DTEnemy_StartRightBack: EnemyLoc(Maps.AztecTiny5DTemple, Enemies.ZingerLime, 5, [], True),
    Locations.AztecTiny5DTEnemy_StartLeftFront: EnemyLoc(Maps.AztecTiny5DTemple, Enemies.ZingerLime, 6, [], True),
    Locations.AztecTiny5DTEnemy_Reward0: EnemyLoc(Maps.AztecTiny5DTemple, Enemies.ZingerLime, 7, [], True),
    Locations.AztecTiny5DTEnemy_Reward1: EnemyLoc(Maps.AztecTiny5DTemple, Enemies.ZingerLime, 8, [], True),
    Locations.AztecTiny5DTEnemy_DeadEnd0: EnemyLoc(Maps.AztecTiny5DTemple, Enemies.ZingerLime, 9, [], True),
    Locations.AztecTiny5DTEnemy_DeadEnd1: EnemyLoc(Maps.AztecTiny5DTemple, Enemies.ZingerLime, 10, [], True),
    # Chunky 5DT
    Locations.AztecChunky5DTEnemy_StartRight: EnemyLoc(Maps.AztecChunky5DTemple, Enemies.Klobber, 2, [], True),
    Locations.AztecChunky5DTEnemy_StartLeft: EnemyLoc(Maps.AztecChunky5DTemple, Enemies.Klobber, 3, [], True),
    Locations.AztecChunky5DTEnemy_SecondRight: EnemyLoc(Maps.AztecChunky5DTemple, Enemies.Klobber, 5, [], True),
    Locations.AztecChunky5DTEnemy_SecondLeft: EnemyLoc(Maps.AztecChunky5DTemple, Enemies.Klobber, 6, [], True),
    Locations.AztecChunky5DTEnemy_Reward: EnemyLoc(Maps.AztecChunky5DTemple, Enemies.ZingerLime, 7, [], True),
    # Llama Temple
    Locations.AztecLlamaEnemy_KongFreeInstrument: EnemyLoc(Maps.AztecLlamaTemple, Enemies.KlaptrapPurple, 5, [], True),
    Locations.AztecLlamaEnemy_DinoInstrument: EnemyLoc(Maps.AztecLlamaTemple, Enemies.KlaptrapPurple, 6, [], True),
    Locations.AztecLlamaEnemy_Matching0: EnemyLoc(Maps.AztecLlamaTemple, Enemies.Kremling, 10, [enemies_not_ground_simple], True),
    Locations.AztecLlamaEnemy_Matching1: EnemyLoc(Maps.AztecLlamaTemple, Enemies.Kremling, 11, [enemies_not_ground_simple], True),
    Locations.AztecLlamaEnemy_Right: EnemyLoc(Maps.AztecLlamaTemple, Enemies.Kremling, 14, [], True),
    Locations.AztecLlamaEnemy_Left: EnemyLoc(Maps.AztecLlamaTemple, Enemies.Kremling, 15, [], True),
    Locations.AztecLlamaEnemy_MelonCrate: EnemyLoc(Maps.AztecLlamaTemple, Enemies.KlaptrapPurple, 16, [], True),
    Locations.AztecLlamaEnemy_SlamSwitch: EnemyLoc(Maps.AztecLlamaTemple, Enemies.KlaptrapPurple, 17, [], True),
    # Tiny Temple
    Locations.AztecTempleEnemy_Rotating00: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 1, enemies_nokill_gun, True, False),
    Locations.AztecTempleEnemy_Rotating01: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 2, enemies_nokill_gun, True, False),
    Locations.AztecTempleEnemy_Rotating02: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 3, enemies_nokill_gun, True, False),
    Locations.AztecTempleEnemy_Rotating03: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 4, enemies_nokill_gun, True, False),
    Locations.AztecTempleEnemy_Rotating04: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 5, enemies_nokill_gun, True, False),
    Locations.AztecTempleEnemy_Rotating05: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 6, enemies_nokill_gun, True, False),
    Locations.AztecTempleEnemy_Rotating06: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 7, enemies_nokill_gun, True, False),
    Locations.AztecTempleEnemy_Rotating07: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 8, enemies_nokill_gun, True, False),
    Locations.AztecTempleEnemy_Rotating08: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 9, enemies_nokill_gun, True, False),
    Locations.AztecTempleEnemy_Rotating09: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 10, enemies_nokill_gun, True, False),
    Locations.AztecTempleEnemy_Rotating10: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 11, enemies_nokill_gun, True, False),
    Locations.AztecTempleEnemy_Rotating11: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 12, enemies_nokill_gun, True, False),
    Locations.AztecTempleEnemy_Rotating12: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 13, enemies_nokill_gun, True, False),
    Locations.AztecTempleEnemy_Rotating13: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 14, enemies_nokill_gun, True, False),
    Locations.AztecTempleEnemy_Rotating14: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 15, enemies_nokill_gun, True, False),
    Locations.AztecTempleEnemy_Rotating15: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 16, enemies_nokill_gun, True, False),
    Locations.AztecTempleEnemy_MiniRoom00: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 20, enemies_not_ground_simple, True, False),
    Locations.AztecTempleEnemy_MiniRoom01: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 21, enemies_not_ground_simple, True, False),
    Locations.AztecTempleEnemy_MiniRoom02: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 22, enemies_not_ground_simple, True, False),
    Locations.AztecTempleEnemy_MiniRoom03: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 23, enemies_not_ground_simple, True, False),
    Locations.AztecTempleEnemy_GuardRotating0: EnemyLoc(Maps.AztecTinyTemple, Enemies.Klobber, 24, [], True),
    Locations.AztecTempleEnemy_GuardRotating1: EnemyLoc(Maps.AztecTinyTemple, Enemies.Klobber, 36, [], True),
    Locations.AztecTempleEnemy_MainRoom0: EnemyLoc(Maps.AztecTinyTemple, Enemies.Kremling, 26, [], True),
    Locations.AztecTempleEnemy_MainRoom1: EnemyLoc(Maps.AztecTinyTemple, Enemies.Kremling, 28, [], True),
    Locations.AztecTempleEnemy_MainRoom2: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 35, [], True),
    Locations.AztecTempleEnemy_KongRoom0: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 29, [], True),
    Locations.AztecTempleEnemy_KongRoom1: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 30, [], True),
    Locations.AztecTempleEnemy_KongRoom2: EnemyLoc(Maps.AztecTinyTemple, Enemies.Kremling, 32, [], True),
    Locations.AztecTempleEnemy_KongRoom3: EnemyLoc(Maps.AztecTinyTemple, Enemies.Kremling, 33, [], True),
    Locations.AztecTempleEnemy_KongRoom4: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 34, [], True),
    Locations.AztecTempleEnemy_Underwater: EnemyLoc(Maps.AztecTinyTemple, Enemies.Shuri, 37, [], True),
    # Factory
    # Main
    Locations.FactoryMainEnemy_CandyCranky0: EnemyLoc(Maps.FranticFactory, Enemies.Kremling, 33, [], True),
    Locations.FactoryMainEnemy_CandyCranky1: EnemyLoc(Maps.FranticFactory, Enemies.Kremling, 72, [], True),
    Locations.FactoryMainEnemy_LobbyLeft: EnemyLoc(Maps.FranticFactory, Enemies.RoboKremling, 74, [], True),
    Locations.FactoryMainEnemy_LobbyRight: EnemyLoc(Maps.FranticFactory, Enemies.RoboKremling, 58, [], True),
    Locations.FactoryMainEnemy_StorageRoom: EnemyLoc(Maps.FranticFactory, Enemies.ZingerRobo, 91, [], True),
    Locations.FactoryMainEnemy_BlockTower0: EnemyLoc(Maps.FranticFactory, Enemies.MrDice1, 78, [], True),
    Locations.FactoryMainEnemy_BlockTower1: EnemyLoc(Maps.FranticFactory, Enemies.SirDomino, 79, [], True),
    Locations.FactoryMainEnemy_BlockTower2: EnemyLoc(Maps.FranticFactory, Enemies.MrDice1, 80, [], True),
    Locations.FactoryMainEnemy_TunnelToHatch: EnemyLoc(Maps.FranticFactory, Enemies.RoboKremling, 59, kops, True),
    Locations.FactoryMainEnemy_TunnelToProd0: EnemyLoc(Maps.FranticFactory, Enemies.Kremling, 63, kops, True),
    Locations.FactoryMainEnemy_TunnelToProd1: EnemyLoc(Maps.FranticFactory, Enemies.RoboKremling, 73, kops, True),
    Locations.FactoryMainEnemy_TunnelToBlockTower: EnemyLoc(Maps.FranticFactory, Enemies.RoboKremling, 84, kops, True),
    Locations.FactoryMainEnemy_TunnelToRace0: EnemyLoc(Maps.FranticFactory, Enemies.RoboKremling, 87, kops, True),
    Locations.FactoryMainEnemy_TunnelToRace1: EnemyLoc(Maps.FranticFactory, Enemies.ZingerRobo, 88, kops, True),
    Locations.FactoryMainEnemy_LowWarp4: EnemyLoc(Maps.FranticFactory, Enemies.RoboKremling, 66, [], True),
    Locations.FactoryMainEnemy_DiddySwitch: EnemyLoc(Maps.FranticFactory, Enemies.ZingerRobo, 67, [], True),
    Locations.FactoryMainEnemy_ToBlockTowerTunnel: EnemyLoc(Maps.FranticFactory, Enemies.ZingerRobo, 62, [Enemies.Bug] + kops, True),
    Locations.FactoryMainEnemy_DarkRoom0: EnemyLoc(Maps.FranticFactory, Enemies.ZingerRobo, 70, [], True),
    Locations.FactoryMainEnemy_DarkRoom1: EnemyLoc(Maps.FranticFactory, Enemies.ZingerRobo, 71, [], True),
    Locations.FactoryMainEnemy_BHDM0: EnemyLoc(Maps.FranticFactory, Enemies.MrDice0, 35, [], False, False),
    Locations.FactoryMainEnemy_BHDM1: EnemyLoc(Maps.FranticFactory, Enemies.SirDomino, 36, [], False, False),
    Locations.FactoryMainEnemy_BHDM2: EnemyLoc(Maps.FranticFactory, Enemies.SirDomino, 37, [], False, False),
    Locations.FactoryMainEnemy_BHDM3: EnemyLoc(Maps.FranticFactory, Enemies.MrDice0, 38, [], False, False),
    Locations.FactoryMainEnemy_BHDM4: EnemyLoc(Maps.FranticFactory, Enemies.MrDice0, 39, [], False, False),
    Locations.FactoryMainEnemy_BHDM5: EnemyLoc(Maps.FranticFactory, Enemies.Ruler, 40, [], False, False),
    Locations.FactoryMainEnemy_BHDM6: EnemyLoc(Maps.FranticFactory, Enemies.Ruler, 41, [], False, False),
    Locations.FactoryMainEnemy_BHDM7: EnemyLoc(Maps.FranticFactory, Enemies.MrDice1, 42, [], False, False),
    Locations.FactoryMainEnemy_BHDM8: EnemyLoc(Maps.FranticFactory, Enemies.SirDomino, 43, [], False, False),
    Locations.FactoryMainEnemy_BHDM9: EnemyLoc(Maps.FranticFactory, Enemies.SirDomino, 44, [], False, False),
    Locations.FactoryMainEnemy_1342Gauntlet0: EnemyLoc(Maps.FranticFactory, Enemies.ZingerRobo, 49, [], True, False),
    Locations.FactoryMainEnemy_1342Gauntlet1: EnemyLoc(Maps.FranticFactory, Enemies.RoboKremling, 50, [], True, False),
    Locations.FactoryMainEnemy_1342Gauntlet2: EnemyLoc(Maps.FranticFactory, Enemies.RoboKremling, 51, [], True, False),
    Locations.FactoryMainEnemy_3124Gauntlet0: EnemyLoc(Maps.FranticFactory, Enemies.MrDice1, 52, [], True, False),
    Locations.FactoryMainEnemy_3124Gauntlet1: EnemyLoc(Maps.FranticFactory, Enemies.SirDomino, 53, [], True, False),
    Locations.FactoryMainEnemy_3124Gauntlet2: EnemyLoc(Maps.FranticFactory, Enemies.MrDice1, 54, [], True, False),
    Locations.FactoryMainEnemy_4231Gauntlet0: EnemyLoc(Maps.FranticFactory, Enemies.RoboKremling, 55, [], True, False),
    Locations.FactoryMainEnemy_4231Gauntlet1: EnemyLoc(Maps.FranticFactory, Enemies.RoboKremling, 56, [], True, False),
    # Lobby
    Locations.FactoryLobbyEnemy_Enemy0: EnemyLoc(Maps.FranticFactoryLobby, Enemies.ZingerRobo, 1, [], True),
    # Galleon
    # Main
    Locations.GalleonMainEnemy_ChestRoom0: EnemyLoc(Maps.GloomyGalleon, Enemies.Klobber, 12, [], True),
    Locations.GalleonMainEnemy_ChestRoom1: EnemyLoc(Maps.GloomyGalleon, Enemies.Kaboom, 18, [], True),
    Locations.GalleonMainEnemy_NearVineCannon: EnemyLoc(Maps.GloomyGalleon, Enemies.Kaboom, 16, [], True),
    Locations.GalleonMainEnemy_CrankyCannon: EnemyLoc(Maps.GloomyGalleon, Enemies.Kaboom, 17, [], True),
    Locations.GalleonMainEnemy_Submarine: EnemyLoc(Maps.GloomyGalleon, Enemies.Pufftup, 14, [], True),
    Locations.GalleonMainEnemy_5DS0: EnemyLoc(Maps.GloomyGalleon, Enemies.Shuri, 19, [], True),
    Locations.GalleonMainEnemy_5DS1: EnemyLoc(Maps.GloomyGalleon, Enemies.Shuri, 20, [], True),
    Locations.GalleonMainEnemy_PeanutTunnel: EnemyLoc(Maps.GloomyGalleon, Enemies.Kosha, 26, [], True),
    Locations.GalleonMainEnemy_CoconutTunnel: EnemyLoc(Maps.GloomyGalleon, Enemies.Kremling, 27, [], True),
    # Lighthouse
    Locations.GalleonLighthouseEnemy_Enemy0: EnemyLoc(Maps.GalleonLighthouse, Enemies.Klump, 1, enemies_shockwave_immune + kops, True),
    Locations.GalleonLighthouseEnemy_Enemy1: EnemyLoc(Maps.GalleonLighthouse, Enemies.Klump, 2, enemies_shockwave_immune + kops, True),
    # 5DS Diddy, Lanky, Chunky
    Locations.Galleon5DSDLCEnemy_Diddy: EnemyLoc(Maps.Galleon5DShipDiddyLankyChunky, Enemies.Pufftup, 4, [], True),
    Locations.Galleon5DSDLCEnemy_Chunky: EnemyLoc(Maps.Galleon5DShipDiddyLankyChunky, Enemies.Pufftup, 5, [], True),
    Locations.Galleon5DSDLCEnemy_Lanky: EnemyLoc(Maps.Galleon5DShipDiddyLankyChunky, Enemies.Pufftup, 6, [], True),
    # 5DS DK, Tiny
    Locations.Galleon5DSDTEnemy_DK0: EnemyLoc(Maps.Galleon5DShipDKTiny, Enemies.Shuri, 4, [], True),
    Locations.Galleon5DSDTEnemy_DK1: EnemyLoc(Maps.Galleon5DShipDKTiny, Enemies.Shuri, 5, [], True),
    Locations.Galleon5DSDTEnemy_DK2: EnemyLoc(Maps.Galleon5DShipDKTiny, Enemies.Shuri, 6, [], True),
    Locations.Galleon5DSDTEnemy_TinyCage: EnemyLoc(Maps.Galleon5DShipDKTiny, Enemies.Shuri, 9, [], True),
    Locations.Galleon5DSDTEnemy_TinyBed: EnemyLoc(Maps.Galleon5DShipDKTiny, Enemies.Shuri, 10, [], True),
    # 2DS
    Locations.Galleon2DSEnemy_Tiny0: EnemyLoc(Maps.Galleon2DShip, Enemies.Gimpfish, 3, [], True),
    Locations.Galleon2DSEnemy_Tiny1: EnemyLoc(Maps.Galleon2DShip, Enemies.Gimpfish, 4, [], True),
    # Submarine
    Locations.GalleonSubEnemy_Enemy0: EnemyLoc(Maps.GalleonSubmarine, Enemies.Pufftup, 1, [], True),
    Locations.GalleonSubEnemy_Enemy1: EnemyLoc(Maps.GalleonSubmarine, Enemies.Pufftup, 3, [], True),
    Locations.GalleonSubEnemy_Enemy2: EnemyLoc(Maps.GalleonSubmarine, Enemies.Pufftup, 4, [], True),
    Locations.GalleonSubEnemy_Enemy3: EnemyLoc(Maps.GalleonSubmarine, Enemies.Pufftup, 6, [], True),
    # Fungi
    # Main
    Locations.ForestMainEnemy_HollowTree0: EnemyLoc(Maps.FungiForest, Enemies.Klump, 5, [], True),
    Locations.ForestMainEnemy_HollowTree1: EnemyLoc(Maps.FungiForest, Enemies.Klump, 30, [], True),
    Locations.ForestMainEnemy_HollowTreeEntrance: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 34, [], True),
    Locations.ForestMainEnemy_TreeMelonCrate0: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 31, [], True),
    Locations.ForestMainEnemy_TreeMelonCrate1: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 32, [], True),
    Locations.ForestMainEnemy_TreeMelonCrate2: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 33, [], True),
    Locations.ForestMainEnemy_AppleGauntlet0: EnemyLoc(Maps.FungiForest, Enemies.EvilTomato, 9, [], False),
    Locations.ForestMainEnemy_AppleGauntlet1: EnemyLoc(Maps.FungiForest, Enemies.EvilTomato, 10, [], False),
    Locations.ForestMainEnemy_AppleGauntlet2: EnemyLoc(Maps.FungiForest, Enemies.EvilTomato, 11, [], False),
    Locations.ForestMainEnemy_AppleGauntlet3: EnemyLoc(Maps.FungiForest, Enemies.EvilTomato, 12, [], False),
    Locations.ForestMainEnemy_NearBeanstalk0: EnemyLoc(Maps.FungiForest, Enemies.Klump, 55, [], True),
    Locations.ForestMainEnemy_NearBeanstalk1: EnemyLoc(Maps.FungiForest, Enemies.Klump, 56, [], True),
    Locations.ForestMainEnemy_GreenTunnel: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 57, [], True),
    Locations.ForestMainEnemy_NearLowWarp5: EnemyLoc(Maps.FungiForest, Enemies.MushroomMan, 23, [], True),
    Locations.ForestMainEnemy_NearPinkTunnelBounceTag: EnemyLoc(Maps.FungiForest, Enemies.MushroomMan, 24, [], True),
    Locations.ForestMainEnemy_NearGMRocketbarrel: EnemyLoc(Maps.FungiForest, Enemies.MushroomMan, 25, [], True),
    Locations.ForestMainEnemy_BetweenYellowTunnelAndRB: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 26, [], True),
    Locations.ForestMainEnemy_NearCranky: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 27, [], True),
    Locations.ForestMainEnemy_NearPinkTunnelGM: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 28, [], True),
    Locations.ForestMainEnemy_GMRearTag: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 29, [Enemies.Bug], True),
    Locations.ForestMainEnemy_NearFacePuzzle: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 51, [], True),
    Locations.ForestMainEnemy_NearCrown: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 52, [], True),
    Locations.ForestMainEnemy_NearHighWarp5: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 53, [], True),
    Locations.ForestMainEnemy_TopOfMushroom: EnemyLoc(Maps.FungiForest, Enemies.Klump, 54, enemies_shockwave_immune + kops, True),
    Locations.ForestMainEnemy_NearAppleDropoff: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 48, [], True),
    Locations.ForestMainEnemy_NearDKPortal: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 49, [], True),
    Locations.ForestMainEnemy_NearWellTag: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 50, [], True),
    Locations.ForestMainEnemy_YellowTunnel0: EnemyLoc(Maps.FungiForest, Enemies.MushroomMan, 22, [], True),
    Locations.ForestMainEnemy_YellowTunnel1: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 41, [], True),
    Locations.ForestMainEnemy_YellowTunnel2: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 42, [], True),
    Locations.ForestMainEnemy_YellowTunnel3: EnemyLoc(Maps.FungiForest, Enemies.Klump, 43, [], True),
    Locations.ForestMainEnemy_NearSnide: EnemyLoc(Maps.FungiForest, Enemies.MushroomMan, 35, [], True),
    Locations.ForestMainEnemy_NearIsoCoin: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 38, [], True),
    Locations.ForestMainEnemy_NearBBlast: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 39, [], True),
    Locations.ForestMainEnemy_NearDarkAttic: EnemyLoc(Maps.FungiForest, Enemies.Klump, 44, [], True),
    Locations.ForestMainEnemy_NearWellExit: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 47, [], True),
    Locations.ForestMainEnemy_NearBlueTunnel: EnemyLoc(Maps.FungiForest, Enemies.Klump, 59, [], True),
    Locations.ForestMainEnemy_Thornvine0: EnemyLoc(Maps.FungiForest, Enemies.Klump, 45, [], True),
    Locations.ForestMainEnemy_Thornvine1: EnemyLoc(Maps.FungiForest, Enemies.Klump, 46, [], True),
    Locations.ForestMainEnemy_Thornvine2: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 60, [], True),
    Locations.ForestMainEnemy_ThornvineEntrance: EnemyLoc(Maps.FungiForest, Enemies.Klump, 58, [], True),
    # Anthill
    Locations.ForestAnthillEnemy_Gauntlet0: EnemyLoc(Maps.ForestAnthill, Enemies.KlaptrapPurple, 1, [], True),
    Locations.ForestAnthillEnemy_Gauntlet1: EnemyLoc(Maps.ForestAnthill, Enemies.KlaptrapPurple, 2, [], True),
    Locations.ForestAnthillEnemy_Gauntlet2: EnemyLoc(Maps.ForestAnthill, Enemies.KlaptrapPurple, 3, [], True),
    Locations.ForestAnthillEnemy_Gauntlet3: EnemyLoc(Maps.ForestAnthill, Enemies.KlaptrapPurple, 4, [], True),
    # Winch Room
    Locations.ForestWinchEnemy_Enemy: EnemyLoc(Maps.ForestWinchRoom, Enemies.Bat, 1, [], True),
    # Thornvine Barn
    Locations.ForestThornBarnEnemy_Enemy: EnemyLoc(Maps.ForestThornvineBarn, Enemies.Kosha, 1, [], True),
    # Mill Front
    Locations.ForestMillFrontEnemy_Enemy: EnemyLoc(Maps.ForestMillFront, Enemies.ZingerLime, 1, [], True),
    # Mill Rear
    Locations.ForestMillRearEnemy_Enemy: EnemyLoc(Maps.ForestMillBack, Enemies.ZingerLime, 1, [], True),
    # Giant Mushroom
    Locations.ForestGMEnemy_AboveNightDoor: EnemyLoc(Maps.ForestGiantMushroom, Enemies.Klump, 2, [], True),
    Locations.ForestGMEnemy_Path0: EnemyLoc(Maps.ForestGiantMushroom, Enemies.ZingerLime, 3, [], False),
    Locations.ForestGMEnemy_Path1: EnemyLoc(Maps.ForestGiantMushroom, Enemies.ZingerLime, 4, [], False),
    # Lanky Attic
    Locations.ForestLankyAtticEnemy_Gauntlet0: EnemyLoc(Maps.ForestMillAttic, Enemies.Bat, 1, enemies_nokill_gun, True, False),
    Locations.ForestLankyAtticEnemy_Gauntlet1: EnemyLoc(Maps.ForestMillAttic, Enemies.Bat, 2, enemies_nokill_gun, True, False),
    Locations.ForestLankyAtticEnemy_Gauntlet2: EnemyLoc(Maps.ForestMillAttic, Enemies.Bat, 3, enemies_nokill_gun, True, False),
    # Mush Leap
    Locations.ForestLeapEnemy_Enemy0: EnemyLoc(Maps.ForestLankyZingersRoom, Enemies.ZingerLime, 1, [], True),
    Locations.ForestLeapEnemy_Enemy1: EnemyLoc(Maps.ForestLankyZingersRoom, Enemies.ZingerLime, 2, [], True),
    # Face Puzzle
    Locations.ForestFacePuzzleEnemy_Enemy: EnemyLoc(Maps.ForestChunkyFaceRoom, Enemies.ZingerLime, 1, [], True),
    # Spider Boss
    Locations.ForestSpiderEnemy_Gauntlet0: EnemyLoc(Maps.ForestSpider, Enemies.SpiderSmall, 2, [Enemies.Klobber, Enemies.Kaboom, Enemies.MushroomMan], False, False),
    Locations.ForestSpiderEnemy_Gauntlet1: EnemyLoc(Maps.ForestSpider, Enemies.SpiderSmall, 3, [Enemies.Klobber, Enemies.Kaboom, Enemies.MushroomMan], False, False),
    Locations.ForestSpiderEnemy_Gauntlet2: EnemyLoc(Maps.ForestSpider, Enemies.SpiderSmall, 4, [Enemies.Klobber, Enemies.Kaboom, Enemies.MushroomMan], False, False),
    # Caves
    # Main
    Locations.CavesMainEnemy_Start: EnemyLoc(Maps.CrystalCaves, Enemies.Kremling, 10, [], True),
    Locations.CavesMainEnemy_NearIceCastle: EnemyLoc(Maps.CrystalCaves, Enemies.BeaverBlue, 15, [], True),
    Locations.CavesMainEnemy_Outside5DC: EnemyLoc(Maps.CrystalCaves, Enemies.ZingerLime, 17, [], True),
    Locations.CavesMainEnemy_1DCWaterfall: EnemyLoc(Maps.CrystalCaves, Enemies.ZingerLime, 18, [], True),
    Locations.CavesMainEnemy_NearFunky: EnemyLoc(Maps.CrystalCaves, Enemies.ZingerCharger, 19, [], True),
    Locations.CavesMainEnemy_NearSnide: EnemyLoc(Maps.CrystalCaves, Enemies.Kosha, 27, [], True),
    Locations.CavesMainEnemy_NearBonusRoom: EnemyLoc(Maps.CrystalCaves, Enemies.Kosha, 28, [], True),
    Locations.CavesMainEnemy_1DCHeadphones: EnemyLoc(Maps.CrystalCaves, Enemies.Kosha, 29, enemies_shockwave_immune + kops, True),
    Locations.CavesMainEnemy_GiantKosha: EnemyLoc(Maps.CrystalCaves, Enemies.Kosha, 31, [], True, False),
    # DK 5DI
    Locations.Caves5DIDKEnemy_Right: EnemyLoc(Maps.CavesDonkeyIgloo, Enemies.Kosha, 1, [], True),
    Locations.Caves5DIDKEnemy_Left: EnemyLoc(Maps.CavesDonkeyIgloo, Enemies.Kosha, 3, [], True),
    # Lanky 5DI
    Locations.Caves5DILankyEnemy_First0: EnemyLoc(Maps.CavesLankyIgloo, Enemies.BeaverBlue, 1, [], False, False),
    Locations.Caves5DILankyEnemy_First1: EnemyLoc(Maps.CavesLankyIgloo, Enemies.BeaverBlue, 2, [], False, False),
    Locations.Caves5DILankyEnemy_Second0: EnemyLoc(Maps.CavesLankyIgloo, Enemies.Kremling, 3, [], False, False),
    Locations.Caves5DILankyEnemy_Second1: EnemyLoc(Maps.CavesLankyIgloo, Enemies.Kremling, 4, [], False, False),
    Locations.Caves5DILankyEnemy_Second2: EnemyLoc(Maps.CavesLankyIgloo, Enemies.Kremling, 5, [], False, False),
    # Tiny 5DI
    Locations.Caves5DITinyEnemy_BigEnemy: EnemyLoc(Maps.CavesTinyIgloo, Enemies.Kosha, 2, kops, True),
    # Chunky 5DI
    Locations.Caves5DIChunkyEnemy_Gauntlet00: EnemyLoc(Maps.CavesChunkyIgloo, Enemies.FireballGlasses, 2, [], False, False),
    Locations.Caves5DIChunkyEnemy_Gauntlet01: EnemyLoc(Maps.CavesChunkyIgloo, Enemies.FireballGlasses, 3, [], False, False),
    Locations.Caves5DIChunkyEnemy_Gauntlet02: EnemyLoc(Maps.CavesChunkyIgloo, Enemies.FireballGlasses, 4, [], False, False),
    Locations.Caves5DIChunkyEnemy_Gauntlet03: EnemyLoc(Maps.CavesChunkyIgloo, Enemies.FireballGlasses, 5, [], False, False),
    Locations.Caves5DIChunkyEnemy_Gauntlet04: EnemyLoc(Maps.CavesChunkyIgloo, Enemies.FireballGlasses, 6, [], False, False),
    # Lanky 1DC
    Locations.Caves1DCEnemy_Near: EnemyLoc(Maps.CavesLankyCabin, Enemies.Kosha, 2, [Enemies.KlaptrapRed, Enemies.KlaptrapPurple, Enemies.Klobber], True),
    Locations.Caves1DCEnemy_Far: EnemyLoc(Maps.CavesLankyCabin, Enemies.Kosha, 1, [], True, False),
    # DK 5DC
    Locations.Caves5DCDKEnemy_Gauntlet0: EnemyLoc(Maps.CavesDonkeyCabin, Enemies.ZingerLime, 1, enemies_nokill_gun + [Enemies.Bat], True, False),
    Locations.Caves5DCDKEnemy_Gauntlet1: EnemyLoc(Maps.CavesDonkeyCabin, Enemies.ZingerLime, 2, enemies_nokill_gun + [Enemies.Bat], True, False),
    Locations.Caves5DCDKEnemy_Gauntlet2: EnemyLoc(Maps.CavesDonkeyCabin, Enemies.ZingerLime, 3, enemies_nokill_gun + [Enemies.Bat], True, False),
    Locations.Caves5DCDKEnemy_Gauntlet3: EnemyLoc(Maps.CavesDonkeyCabin, Enemies.ZingerLime, 4, enemies_nokill_gun + [Enemies.Bat], True, False),
    Locations.Caves5DCDKEnemy_Gauntlet4: EnemyLoc(Maps.CavesDonkeyCabin, Enemies.ZingerLime, 5, enemies_nokill_gun + [Enemies.Bat], True, False),
    Locations.Caves5DCDKEnemy_Gauntlet5: EnemyLoc(Maps.CavesDonkeyCabin, Enemies.ZingerLime, 6, enemies_nokill_gun + [Enemies.Bat], True, False),
    # Diddy Enemies 5DC
    Locations.Caves5DCDiddyLowEnemy_CloseRight: EnemyLoc(Maps.CavesDiddyLowerCabin, Enemies.Klump, 1, enemy_5dc_ban, True, False),
    Locations.Caves5DCDiddyLowEnemy_FarRight: EnemyLoc(Maps.CavesDiddyLowerCabin, Enemies.Kremling, 2, enemy_5dc_ban, True, False),
    Locations.Caves5DCDiddyLowEnemy_CloseLeft: EnemyLoc(Maps.CavesDiddyLowerCabin, Enemies.Klump, 3, enemy_5dc_ban, True, False),
    Locations.Caves5DCDiddyLowEnemy_FarLeft: EnemyLoc(Maps.CavesDiddyLowerCabin, Enemies.Kremling, 4, enemy_5dc_ban, True, False),
    Locations.Caves5DCDiddyLowEnemy_Center0: EnemyLoc(Maps.CavesDiddyLowerCabin, Enemies.Klobber, 5, enemy_5dc_ban, True, False),
    Locations.Caves5DCDiddyLowEnemy_Center1: EnemyLoc(Maps.CavesDiddyLowerCabin, Enemies.Klobber, 6, enemy_5dc_ban, True, False),
    Locations.Caves5DCDiddyLowEnemy_Center2: EnemyLoc(Maps.CavesDiddyLowerCabin, Enemies.Klobber, 7, enemy_5dc_ban, True, False),
    Locations.Caves5DCDiddyLowEnemy_Center3: EnemyLoc(Maps.CavesDiddyLowerCabin, Enemies.Klobber, 8, enemy_5dc_ban, True, False),
    # Diddy Candle 5DC
    Locations.Caves5DCDiddyUpperEnemy_Enemy0: EnemyLoc(Maps.CavesDiddyUpperCabin, Enemies.Kosha, 1, [], True, False),
    Locations.Caves5DCDiddyUpperEnemy_Enemy1: EnemyLoc(Maps.CavesDiddyUpperCabin, Enemies.Kosha, 2, [], True, False),
    # Tiny 5DC
    Locations.Caves5DCTinyEnemy_Gauntlet0: EnemyLoc(Maps.CavesTinyCabin, Enemies.KlaptrapPurple, 1, [Enemies.Kosha] + kops, True, False),
    Locations.Caves5DCTinyEnemy_Gauntlet1: EnemyLoc(Maps.CavesTinyCabin, Enemies.KlaptrapPurple, 2, [Enemies.Kosha] + kops, True, False),
    Locations.Caves5DCTinyEnemy_Gauntlet2: EnemyLoc(Maps.CavesTinyCabin, Enemies.KlaptrapPurple, 3, [Enemies.Kosha] + kops, True, False),
    Locations.Caves5DCTinyEnemy_Gauntlet3: EnemyLoc(Maps.CavesTinyCabin, Enemies.KlaptrapPurple, 4, [Enemies.Kosha] + kops, True, False),
    Locations.Caves5DCTinyEnemy_Gauntlet4: EnemyLoc(Maps.CavesTinyCabin, Enemies.KlaptrapPurple, 5, [Enemies.Kosha] + kops, True, False),
    # Castle
    # Main
    Locations.CastleMainEnemy_NearBridge0: EnemyLoc(Maps.CreepyCastle, Enemies.Krossbones, 4, [], True),
    Locations.CastleMainEnemy_NearBridge1: EnemyLoc(Maps.CreepyCastle, Enemies.Krossbones, 5, [], True),
    Locations.CastleMainEnemy_WoodenExtrusion0: EnemyLoc(Maps.CreepyCastle, Enemies.Kosha, 6, kops, True),
    Locations.CastleMainEnemy_WoodenExtrusion1: EnemyLoc(Maps.CreepyCastle, Enemies.Kosha, 7, kops, True),
    Locations.CastleMainEnemy_NearShed: EnemyLoc(Maps.CreepyCastle, Enemies.Krossbones, 8, [], True),
    Locations.CastleMainEnemy_NearLibrary: EnemyLoc(Maps.CreepyCastle, Enemies.Krossbones, 9, [], True),
    Locations.CastleMainEnemy_NearTower: EnemyLoc(Maps.CreepyCastle, Enemies.Kosha, 10, [], True),
    Locations.CastleMainEnemy_MuseumSteps: EnemyLoc(Maps.CreepyCastle, Enemies.Ghost, 11, [], True),
    Locations.CastleMainEnemy_NearLowCave: EnemyLoc(Maps.CreepyCastle, Enemies.Krossbones, 12, [], True),
    Locations.CastleMainEnemy_PathToLowKasplat: EnemyLoc(Maps.CreepyCastle, Enemies.Krossbones, 13, [], True),
    Locations.CastleMainEnemy_LowTnS: EnemyLoc(Maps.CreepyCastle, Enemies.Krossbones, 14, [], True),
    Locations.CastleMainEnemy_PathToDungeon: EnemyLoc(Maps.CreepyCastle, Enemies.Krossbones, 15, [], True),
    Locations.CastleMainEnemy_NearHeadphones: EnemyLoc(Maps.CreepyCastle, Enemies.Krossbones, 16, [], True),
    # Lobby
    Locations.CastleLobbyEnemy_Left: EnemyLoc(Maps.CreepyCastleLobby, Enemies.Kosha, 2, [], True),
    Locations.CastleLobbyEnemy_FarRight: EnemyLoc(Maps.CreepyCastleLobby, Enemies.Kosha, 3, [], True),
    Locations.CastleLobbyEnemy_NearRight: EnemyLoc(Maps.CreepyCastleLobby, Enemies.Kosha, 4, [], True),
    # Ballroom
    Locations.CastleBallroomEnemy_Board00: EnemyLoc(Maps.CastleBallroom, Enemies.Krossbones, 1, [], True, False),
    Locations.CastleBallroomEnemy_Board01: EnemyLoc(Maps.CastleBallroom, Enemies.Ghost, 2, [], True, False),
    Locations.CastleBallroomEnemy_Board02: EnemyLoc(Maps.CastleBallroom, Enemies.Ghost, 3, [], True, False),
    Locations.CastleBallroomEnemy_Board03: EnemyLoc(Maps.CastleBallroom, Enemies.Ghost, 4, [], True, False),
    Locations.CastleBallroomEnemy_Board04: EnemyLoc(Maps.CastleBallroom, Enemies.Krossbones, 5, [], True, False),
    Locations.CastleBallroomEnemy_Start: EnemyLoc(Maps.CastleBallroom, Enemies.Kosha, 6, [], True),
    # Dungeon
    Locations.CastleDungeonEnemy_FaceRoom: EnemyLoc(Maps.CastleDungeon, Enemies.Krossbones, 1, [], True),
    Locations.CastleDungeonEnemy_ChairRoom: EnemyLoc(Maps.CastleDungeon, Enemies.Kosha, 2, [], True),
    Locations.CastleDungeonEnemy_OutsideLankyRoom: EnemyLoc(Maps.CastleDungeon, Enemies.Kosha, 3, [], True),
    # Shed
    Locations.CastleShedEnemy_Gauntlet00: EnemyLoc(Maps.CastleShed, Enemies.Bat, 1, enemies_nokill_gun, True, False),
    Locations.CastleShedEnemy_Gauntlet01: EnemyLoc(Maps.CastleShed, Enemies.Bat, 2, enemies_nokill_gun, True, False),
    Locations.CastleShedEnemy_Gauntlet02: EnemyLoc(Maps.CastleShed, Enemies.Bat, 3, enemies_nokill_gun, True, False),
    Locations.CastleShedEnemy_Gauntlet03: EnemyLoc(Maps.CastleShed, Enemies.Bat, 4, enemies_nokill_gun, True, False),
    Locations.CastleShedEnemy_Gauntlet04: EnemyLoc(Maps.CastleShed, Enemies.Bat, 5, enemies_nokill_gun, True, False),
    # Lower Cave
    Locations.CastleLowCaveEnemy_NearCrypt: EnemyLoc(Maps.CastleLowerCave, Enemies.Kosha, 3, [], True),
    Locations.CastleLowCaveEnemy_StairRight: EnemyLoc(Maps.CastleLowerCave, Enemies.Kosha, 4, [], True),
    Locations.CastleLowCaveEnemy_StairLeft: EnemyLoc(Maps.CastleLowerCave, Enemies.Krossbones, 5, [], True),
    Locations.CastleLowCaveEnemy_NearMausoleum: EnemyLoc(Maps.CastleLowerCave, Enemies.Bat, 6, [], True),
    Locations.CastleLowCaveEnemy_NearFunky: EnemyLoc(Maps.CastleLowerCave, Enemies.Bat, 7, [], True),
    Locations.CastleLowCaveEnemy_NearTag: EnemyLoc(Maps.CastleLowerCave, Enemies.Bat, 8, [], True),
    # Crypt
    Locations.CastleCryptEnemy_DiddyCoffin0: EnemyLoc(Maps.CastleCrypt, Enemies.Ghost, 1, [], True),
    Locations.CastleCryptEnemy_DiddyCoffin1: EnemyLoc(Maps.CastleCrypt, Enemies.Ghost, 2, [], True),
    Locations.CastleCryptEnemy_DiddyCoffin2: EnemyLoc(Maps.CastleCrypt, Enemies.Krossbones, 3, [], True),
    Locations.CastleCryptEnemy_DiddyCoffin3: EnemyLoc(Maps.CastleCrypt, Enemies.Ghost, 4, [], True),
    Locations.CastleCryptEnemy_ChunkyCoffin0: EnemyLoc(Maps.CastleCrypt, Enemies.Krossbones, 5, [], True),
    Locations.CastleCryptEnemy_ChunkyCoffin1: EnemyLoc(Maps.CastleCrypt, Enemies.Krossbones, 6, [], True),
    Locations.CastleCryptEnemy_ChunkyCoffin2: EnemyLoc(Maps.CastleCrypt, Enemies.Ghost, 7, [], True),
    Locations.CastleCryptEnemy_ChunkyCoffin3: EnemyLoc(Maps.CastleCrypt, Enemies.Krossbones, 8, [], True),
    Locations.CastleCryptEnemy_MinecartEntry: EnemyLoc(Maps.CastleCrypt, Enemies.Krossbones, 9, [], True),
    Locations.CastleCryptEnemy_Fork: EnemyLoc(Maps.CastleCrypt, Enemies.Krossbones, 10, [], True),
    Locations.CastleCryptEnemy_NearDiddy: EnemyLoc(Maps.CastleCrypt, Enemies.Krossbones, 11, [], True),
    Locations.CastleCryptEnemy_NearChunky: EnemyLoc(Maps.CastleCrypt, Enemies.Krossbones, 12, [], True),
    # Mausoleum
    Locations.CastleMausoleumEnemy_TinyPath: EnemyLoc(Maps.CastleMausoleum, Enemies.Krossbones, 1, [], True),
    Locations.CastleMausoleumEnemy_LankyPath0: EnemyLoc(Maps.CastleMausoleum, Enemies.Krossbones, 2, [], True),
    Locations.CastleMausoleumEnemy_LankyPath1: EnemyLoc(Maps.CastleMausoleum, Enemies.Krossbones, 3, [], True),
    # Upper Cave
    Locations.CastleUpperCaveEnemy_NearDungeon: EnemyLoc(Maps.CastleUpperCave, Enemies.Bat, 3, [], True),
    Locations.CastleUpperCaveEnemy_Pit: EnemyLoc(Maps.CastleUpperCave, Enemies.Bat, 4, [], True),
    Locations.CastleUpperCaveEnemy_NearPit: EnemyLoc(Maps.CastleUpperCave, Enemies.Bat, 5, [], True),
    Locations.CastleUpperCaveEnemy_NearEntrance: EnemyLoc(Maps.CastleUpperCave, Enemies.Krossbones, 6, [], True),
    # Kut Out
    Locations.CastleKKOEnemy_CenterEnemy: EnemyLoc(Maps.CastleBoss, Enemies.Ghost, 7, [enemies_not_ground_simple], True, False),
    Locations.CastleKKOEnemy_WaterEnemy00: EnemyLoc(Maps.CastleBoss, Enemies.Pufftup, 8, [], True, False),
    Locations.CastleKKOEnemy_WaterEnemy01: EnemyLoc(Maps.CastleBoss, Enemies.Pufftup, 9, [], True, False),
    Locations.CastleKKOEnemy_WaterEnemy02: EnemyLoc(Maps.CastleBoss, Enemies.Pufftup, 10, [], True, False),
    Locations.CastleKKOEnemy_WaterEnemy03: EnemyLoc(Maps.CastleBoss, Enemies.Pufftup, 11, [], True, False),
    # Library
    Locations.CastleLibraryEnemy_Gauntlet00: EnemyLoc(Maps.CastleLibrary, Enemies.Krossbones, 1, [], True, False),
    Locations.CastleLibraryEnemy_Gauntlet01: EnemyLoc(Maps.CastleLibrary, Enemies.Ghost, 2, [], True, False),
    Locations.CastleLibraryEnemy_Gauntlet02: EnemyLoc(Maps.CastleLibrary, Enemies.Ghost, 3, [], True, False),
    Locations.CastleLibraryEnemy_Gauntlet03: EnemyLoc(Maps.CastleLibrary, Enemies.Krossbones, 4, [], True, False),
    Locations.CastleLibraryEnemy_Corridor00: EnemyLoc(Maps.CastleLibrary, Enemies.Book, 5, [], True),
    Locations.CastleLibraryEnemy_Corridor01: EnemyLoc(Maps.CastleLibrary, Enemies.Book, 7, [], True),
    Locations.CastleLibraryEnemy_Corridor02: EnemyLoc(Maps.CastleLibrary, Enemies.Book, 8, [], True),
    Locations.CastleLibraryEnemy_Corridor03: EnemyLoc(Maps.CastleLibrary, Enemies.Book, 9, [], True),
    Locations.CastleLibraryEnemy_Corridor04: EnemyLoc(Maps.CastleLibrary, Enemies.Book, 10, [], True),
    Locations.CastleLibraryEnemy_Corridor05: EnemyLoc(Maps.CastleLibrary, Enemies.Book, 11, [], True),
    Locations.CastleLibraryEnemy_ForkLeft0: EnemyLoc(Maps.CastleLibrary, Enemies.Bat, 12, [], True),
    Locations.CastleLibraryEnemy_ForkLeft1: EnemyLoc(Maps.CastleLibrary, Enemies.Bat, 15, [], True),
    Locations.CastleLibraryEnemy_ForkCenter: EnemyLoc(Maps.CastleLibrary, Enemies.Bat, 13, [], True),
    Locations.CastleLibraryEnemy_ForkRight: EnemyLoc(Maps.CastleLibrary, Enemies.Bat, 14, [], True),
    # Museum
    Locations.CastleMuseumEnemy_MainFloor0: EnemyLoc(Maps.CastleMuseum, Enemies.Ghost, 1, [], True),
    Locations.CastleMuseumEnemy_MainFloor1: EnemyLoc(Maps.CastleMuseum, Enemies.Ghost, 2, [], True),
    Locations.CastleMuseumEnemy_MainFloor2: EnemyLoc(Maps.CastleMuseum, Enemies.Ghost, 3, [], True),
    Locations.CastleMuseumEnemy_MainFloor3: EnemyLoc(Maps.CastleMuseum, Enemies.Ghost, 4, [], True),
    Locations.CastleMuseumEnemy_Start: EnemyLoc(Maps.CastleMuseum, Enemies.Kosha, 6, [], True),
    # Tower
    Locations.CastleTowerEnemy_Gauntlet0: EnemyLoc(Maps.CastleTower, Enemies.Ghost, 1, [], True, False),
    Locations.CastleTowerEnemy_Gauntlet1: EnemyLoc(Maps.CastleTower, Enemies.Ghost, 2, [], True, False),
    Locations.CastleTowerEnemy_Gauntlet2: EnemyLoc(Maps.CastleTower, Enemies.Ghost, 3, [], True, False),
    Locations.CastleTowerEnemy_Gauntlet3: EnemyLoc(Maps.CastleTower, Enemies.Ghost, 4, [], True, False),
    Locations.CastleTowerEnemy_Gauntlet4: EnemyLoc(Maps.CastleTower, Enemies.Ghost, 5, [], True, False),
    # Trash Can
    Locations.CastleTrashEnemy_Gauntlet0: EnemyLoc(Maps.CastleTrashCan, Enemies.Bug, 1, [], False, False),
    Locations.CastleTrashEnemy_Gauntlet1: EnemyLoc(Maps.CastleTrashCan, Enemies.Bug, 2, [], False, False),
    Locations.CastleTrashEnemy_Gauntlet2: EnemyLoc(Maps.CastleTrashCan, Enemies.Bug, 3, [], False, False),
    Locations.CastleTrashEnemy_Gauntlet3: EnemyLoc(Maps.CastleTrashCan, Enemies.Bug, 4, [], False, False),
    Locations.CastleTrashEnemy_Gauntlet4: EnemyLoc(Maps.CastleTrashCan, Enemies.Bug, 5, [], False, False),
    # Tree
    Locations.CastleTreeEnemy_StartRoom0: EnemyLoc(Maps.CastleTree, Enemies.Bat, 3, [], True),
    Locations.CastleTreeEnemy_StartRoom1: EnemyLoc(Maps.CastleTree, Enemies.Bat, 5, [], True),
    # Helm
    # Main
    Locations.HelmMainEnemy_Start0: EnemyLoc(Maps.HideoutHelm, Enemies.KlaptrapGreen, 2, [], True),
    Locations.HelmMainEnemy_Start1: EnemyLoc(Maps.HideoutHelm, Enemies.Kremling, 3, [], True),
    Locations.HelmMainEnemy_Hill: EnemyLoc(Maps.HideoutHelm, Enemies.Klump, 4, [], True),
    Locations.HelmMainEnemy_SwitchRoom0: EnemyLoc(Maps.HideoutHelm, Enemies.Klump, 5, [], True),
    Locations.HelmMainEnemy_SwitchRoom1: EnemyLoc(Maps.HideoutHelm, Enemies.KlaptrapGreen, 16, [], True),
    Locations.HelmMainEnemy_MiniRoom0: EnemyLoc(Maps.HideoutHelm, Enemies.Kremling, 7, [], True),
    Locations.HelmMainEnemy_MiniRoom1: EnemyLoc(Maps.HideoutHelm, Enemies.Kremling, 8, [], True),
    Locations.HelmMainEnemy_MiniRoom2: EnemyLoc(Maps.HideoutHelm, Enemies.KlaptrapGreen, 17, [], True),
    Locations.HelmMainEnemy_MiniRoom3: EnemyLoc(Maps.HideoutHelm, Enemies.KlaptrapGreen, 18, [], True),
    Locations.HelmMainEnemy_DKRoom: EnemyLoc(Maps.HideoutHelm, Enemies.Kremling, 10, [], True),
    Locations.HelmMainEnemy_ChunkyRoom0: EnemyLoc(Maps.HideoutHelm, Enemies.Kremling, 11, [], True),
    Locations.HelmMainEnemy_ChunkyRoom1: EnemyLoc(Maps.HideoutHelm, Enemies.KlaptrapGreen, 19, [], True),
    Locations.HelmMainEnemy_TinyRoom: EnemyLoc(Maps.HideoutHelm, Enemies.Klump, 12, [], True),
    Locations.HelmMainEnemy_LankyRoom0: EnemyLoc(Maps.HideoutHelm, Enemies.Klump, 13, [], True),
    Locations.HelmMainEnemy_LankyRoom1: EnemyLoc(Maps.HideoutHelm, Enemies.KlaptrapGreen, 20, [], True),
    Locations.HelmMainEnemy_DiddyRoom0: EnemyLoc(Maps.HideoutHelm, Enemies.KlaptrapGreen, 21, [], True),
    Locations.HelmMainEnemy_DiddyRoom1: EnemyLoc(Maps.HideoutHelm, Enemies.KlaptrapGreen, 22, [], True),
    Locations.HelmMainEnemy_NavRight: EnemyLoc(Maps.HideoutHelm, Enemies.Kremling, 23, [], True),
    Locations.HelmMainEnemy_NavLeft: EnemyLoc(Maps.HideoutHelm, Enemies.KlaptrapGreen, 24, [], True),
    # Isles
    # Main
    Locations.IslesMainEnemy_PineappleCage0: EnemyLoc(Maps.Isles, Enemies.BeaverBlue, 1, [], True),
    Locations.IslesMainEnemy_FungiCannon0: EnemyLoc(Maps.Isles, Enemies.BeaverBlue, 2, [], True),
    Locations.IslesMainEnemy_JapesEntrance: EnemyLoc(Maps.Isles, Enemies.BeaverBlue, 3, [], True),
    Locations.IslesMainEnemy_MonkeyportPad: EnemyLoc(Maps.Isles, Enemies.Kremling, 4, [], True),
    Locations.IslesMainEnemy_UpperFactoryPath: EnemyLoc(Maps.Isles, Enemies.Kremling, 5, [], True),
    Locations.IslesMainEnemy_NearAztec: EnemyLoc(Maps.Isles, Enemies.ZingerCharger, 8, [], True),
    Locations.IslesMainEnemy_FungiCannon1: EnemyLoc(Maps.Isles, Enemies.ZingerCharger, 9, [], True),
    Locations.IslesMainEnemy_PineappleCage1: EnemyLoc(Maps.Isles, Enemies.ZingerCharger, 10, [], True),
    Locations.IslesMainEnemy_LowerFactoryPath0: EnemyLoc(Maps.Isles, Enemies.ZingerLime, 11, [], True),
    Locations.IslesMainEnemy_LowerFactoryPath1: EnemyLoc(Maps.Isles, Enemies.ZingerLime, 12, [], True),
}

EnemySelector = []
for enemyEnum, enemy in EnemyMetaData.items():
    if enemy.selector_enabled:
        EnemySelector.append({"name": enemy.name, "value": enemyEnum.name, "tooltip": ""})
EnemySelector = sorted(EnemySelector.copy(), key=lambda d: d["name"])
