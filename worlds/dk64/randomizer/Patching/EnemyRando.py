"""Apply Boss Locations."""

from randomizer.Enums.EnemySubtypes import EnemySubtype
from randomizer.Enums.Settings import CrownEnemyDifficulty, DamageAmount, WinConditionComplex
from randomizer.Lists.EnemyTypes import EnemyMetaData
from randomizer.Enums.Enemies import Enemies
from randomizer.Enums.Items import Items
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Maps import Maps
from randomizer.Patching.Patcher import LocalROM
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames


class PkmnSnapEnemy:
    """Class which determines if an enemy is available for the pkmn snap goal."""

    def __init__(self, enemy):
        """Initialize with given parameters."""
        self.enemy = enemy
        if enemy in (
            Enemies.KasplatDK,
            Enemies.KasplatDiddy,
            Enemies.KasplatLanky,
            Enemies.KasplatTiny,
            Enemies.KasplatChunky,
            Enemies.Book,
            Enemies.EvilTomato,
            Enemies.FairyQueen,
            Enemies.IceTomato,
            Enemies.Llama,
            Enemies.Mermaid,
            Enemies.Seal1,
            Enemies.MechFish,
        ):
            # Always spawned, not in pool
            self.spawned = True
        else:
            self.spawned = False
        self.default = self.spawned

    def addEnemy(self):
        """Add enemy as spawned."""
        self.spawned = True

    def reset(self):
        """Reset enemy to default state."""
        self.spawned = self.default


class Spawner:
    """Class which stores information pertaining to a spawner."""

    def __init__(self, enemy_id: int, offset: int, index: int):
        """Initialize with given parameters."""
        self.enemy_id = enemy_id
        self.offset = offset
        self.index = index


pkmn_snap_enemies = [
    PkmnSnapEnemy(Enemies.Kaboom),
    PkmnSnapEnemy(Enemies.BeaverBlue),
    PkmnSnapEnemy(Enemies.Book),
    PkmnSnapEnemy(Enemies.Klobber),
    PkmnSnapEnemy(Enemies.ZingerCharger),
    PkmnSnapEnemy(Enemies.Klump),
    PkmnSnapEnemy(Enemies.KlaptrapGreen),
    PkmnSnapEnemy(Enemies.ZingerLime),
    PkmnSnapEnemy(Enemies.KlaptrapPurple),
    PkmnSnapEnemy(Enemies.KlaptrapRed),
    PkmnSnapEnemy(Enemies.BeaverGold),
    PkmnSnapEnemy(Enemies.MushroomMan),
    PkmnSnapEnemy(Enemies.Ruler),
    PkmnSnapEnemy(Enemies.RoboKremling),
    PkmnSnapEnemy(Enemies.Kremling),
    PkmnSnapEnemy(Enemies.KasplatDK),
    PkmnSnapEnemy(Enemies.KasplatDiddy),
    PkmnSnapEnemy(Enemies.KasplatLanky),
    PkmnSnapEnemy(Enemies.KasplatTiny),
    PkmnSnapEnemy(Enemies.KasplatChunky),
    PkmnSnapEnemy(Enemies.Guard),
    PkmnSnapEnemy(Enemies.ZingerRobo),
    PkmnSnapEnemy(Enemies.Krossbones),
    PkmnSnapEnemy(Enemies.Shuri),
    PkmnSnapEnemy(Enemies.Gimpfish),
    PkmnSnapEnemy(Enemies.MrDice0),
    PkmnSnapEnemy(Enemies.SirDomino),
    PkmnSnapEnemy(Enemies.MrDice1),
    PkmnSnapEnemy(Enemies.FireballGlasses),
    PkmnSnapEnemy(Enemies.SpiderSmall),
    PkmnSnapEnemy(Enemies.Bat),
    PkmnSnapEnemy(Enemies.EvilTomato),
    PkmnSnapEnemy(Enemies.Ghost),
    PkmnSnapEnemy(Enemies.Pufftup),
    PkmnSnapEnemy(Enemies.Kosha),
    PkmnSnapEnemy(Enemies.Bug),
    PkmnSnapEnemy(Enemies.ZingerFlamethrower),
    PkmnSnapEnemy(Enemies.Scarab),
    PkmnSnapEnemy(Enemies.FairyQueen),
    PkmnSnapEnemy(Enemies.IceTomato),
    PkmnSnapEnemy(Enemies.Mermaid),
    PkmnSnapEnemy(Enemies.Llama),
    PkmnSnapEnemy(Enemies.MechFish),
    PkmnSnapEnemy(Enemies.Seal1),
]

valid_maps = [
    Maps.JapesMountain,
    Maps.JungleJapes,
    Maps.JapesTinyHive,
    Maps.JapesLankyCave,
    Maps.AztecTinyTemple,
    Maps.HideoutHelm,
    Maps.AztecDonkey5DTemple,
    Maps.AztecDiddy5DTemple,
    Maps.AztecLanky5DTemple,
    Maps.AztecTiny5DTemple,
    Maps.AztecChunky5DTemple,
    Maps.AztecLlamaTemple,
    Maps.FranticFactory,
    Maps.FactoryPowerHut,
    Maps.GloomyGalleon,
    Maps.GalleonSickBay,
    Maps.JapesUnderGround,
    Maps.Isles,
    Maps.FactoryCrusher,
    Maps.AngryAztec,
    Maps.GalleonSealRace,
    Maps.JapesBaboonBlast,
    Maps.AztecBaboonBlast,
    Maps.Galleon2DShip,
    Maps.Galleon5DShipDiddyLankyChunky,
    Maps.Galleon5DShipDKTiny,
    Maps.GalleonTreasureChest,
    Maps.GalleonMermaidRoom,
    Maps.FungiForest,
    Maps.GalleonLighthouse,
    Maps.GalleonMechafish,
    Maps.ForestAnthill,
    Maps.GalleonBaboonBlast,
    Maps.ForestMinecarts,
    Maps.ForestMillAttic,
    Maps.ForestRafters,
    Maps.ForestMillAttic,
    Maps.ForestThornvineBarn,
    # Maps.ForestSpider, # Causes a lot of enemies to fall into the pit of their own volition
    Maps.ForestMillFront,
    Maps.ForestMillBack,
    Maps.ForestLankyMushroomsRoom,
    Maps.CrystalCaves,
    Maps.CavesDonkeyIgloo,
    Maps.CavesDiddyIgloo,
    Maps.CavesLankyIgloo,
    Maps.CavesTinyIgloo,
    # Maps.CavesChunkyIgloo, # Fireball with glasses is here
    Maps.CavesDonkeyCabin,
    Maps.CavesDiddyLowerCabin,
    Maps.CavesDiddyUpperCabin,
    Maps.CavesLankyCabin,
    Maps.CavesTinyCabin,
    Maps.CavesChunkyCabin,
    Maps.CreepyCastle,
    Maps.CastleBallroom,
    Maps.CavesRotatingCabin,
    Maps.CavesFrozenCastle,
    Maps.CastleCrypt,
    Maps.CastleMausoleum,
    Maps.CastleUpperCave,
    Maps.CastleLowerCave,
    Maps.CastleTower,
    Maps.CastleMinecarts,
    Maps.FactoryBaboonBlast,
    Maps.CastleMuseum,
    Maps.CastleLibrary,
    Maps.CastleDungeon,
    Maps.CastleTree,
    Maps.CastleShed,
    Maps.CastleTrashCan,
    Maps.JungleJapesLobby,
    Maps.AngryAztecLobby,
    Maps.FranticFactoryLobby,
    Maps.GloomyGalleonLobby,
    Maps.FungiForestLobby,
    Maps.CrystalCavesLobby,
    Maps.CreepyCastleLobby,
    Maps.HideoutHelmLobby,
    Maps.GalleonSubmarine,
    Maps.CavesBaboonBlast,
    Maps.CastleBaboonBlast,
    Maps.ForestBaboonBlast,
    Maps.IslesSnideRoom,
    Maps.ForestGiantMushroom,
    Maps.ForestLankyZingersRoom,
    Maps.CastleBoss,
]
crown_maps = [
    Maps.JapesCrown,
    Maps.AztecCrown,
    Maps.FactoryCrown,
    Maps.GalleonCrown,
    Maps.ForestCrown,
    Maps.CavesCrown,
    Maps.CastleCrown,
    Maps.HelmCrown,
    Maps.SnidesCrown,
    Maps.LobbyCrown,
]
minigame_maps_easy = [
    # Maps.BusyBarrelBarrageEasy,
    # Maps.BusyBarrelBarrageHard,
    # Maps.BusyBarrelBarrageNormal,
    # Maps.HelmBarrelDiddyKremling, # Only kremlings activate the switch
    Maps.HelmBarrelChunkyHidden,
    Maps.HelmBarrelChunkyShooting,
]
minigame_maps_beatable = [Maps.MadMazeMaulEasy, Maps.MadMazeMaulNormal, Maps.MadMazeMaulHard, Maps.MadMazeMaulInsane]
minigame_maps_nolimit = [
    Maps.HelmBarrelLankyMaze,
    Maps.StashSnatchEasy,
    Maps.StashSnatchNormal,
    Maps.StashSnatchHard,
    Maps.StashSnatchInsane,
]
minigame_maps_beavers = [Maps.BeaverBotherEasy, Maps.BeaverBotherNormal, Maps.BeaverBotherHard]
minigame_maps_total = minigame_maps_easy.copy()
minigame_maps_total.extend(minigame_maps_beatable)
minigame_maps_total.extend(minigame_maps_nolimit)
minigame_maps_total.extend(minigame_maps_beavers)
bbbarrage_maps = (Maps.BusyBarrelBarrageEasy, Maps.BusyBarrelBarrageNormal, Maps.BusyBarrelBarrageHard)
banned_speed_maps = list(bbbarrage_maps).copy() + minigame_maps_beavers.copy()
banned_size_maps = list(bbbarrage_maps).copy() + minigame_maps_beavers.copy() + [Maps.ForestAnthill, Maps.CavesDiddyLowerCabin, Maps.CavesTinyCabin, Maps.HelmBarrelChunkyShooting]
replacement_priority = {
    EnemySubtype.GroundSimple: [EnemySubtype.GroundBeefy, EnemySubtype.Water, EnemySubtype.Air],
    EnemySubtype.GroundBeefy: [EnemySubtype.GroundSimple, EnemySubtype.Water, EnemySubtype.Air],
    EnemySubtype.Water: [EnemySubtype.Air, EnemySubtype.GroundSimple, EnemySubtype.GroundBeefy],
    EnemySubtype.Air: [EnemySubtype.GroundSimple, EnemySubtype.GroundBeefy, EnemySubtype.Water],
}
banned_enemy_maps = {
    Enemies.Book: [Maps.CavesDonkeyCabin, Maps.JapesLankyCave, Maps.AngryAztecLobby],
    Enemies.Kosha: [Maps.CavesDiddyLowerCabin, Maps.CavesTinyCabin],
    Enemies.Guard: [Maps.CavesDiddyLowerCabin, Maps.CavesTinyIgloo, Maps.CavesTinyCabin],
}
ENABLE_BBBARRAGE_ENEMY_RANDO = False


def resetPkmnSnap():
    """Reset Pokemon Snap Listing."""
    for enemy in pkmn_snap_enemies:
        enemy.reset()


def setPkmnSnapEnemy(focused_enemy):
    """Set enemy to being spawned."""
    for enemy in pkmn_snap_enemies:
        ref_enemies = [enemy.enemy]
        if enemy.enemy == Enemies.Guard:
            ref_enemies = [Enemies.Guard, Enemies.GuardDisableA, Enemies.GuardDisableZ, Enemies.GuardTag, Enemies.GuardGetOut]
        if focused_enemy in ref_enemies:
            enemy.addEnemy()


MAP_DIFFICULTY_ORDER = (
    Maps.JapesCrown,
    Maps.AztecCrown,
    Maps.FactoryCrown,
    Maps.GalleonCrown,
    Maps.ForestCrown,
    Maps.CavesCrown,
    Maps.CastleCrown,
    Maps.HelmCrown,
    Maps.SnidesCrown,
    Maps.LobbyCrown,
)


def getCrownEnemyDifficultyFromMap(settings, map_id: Maps) -> CrownEnemyDifficulty:
    """Get the crown enemy difficulty for a map."""
    if map_id not in MAP_DIFFICULTY_ORDER:
        raise Exception("Suggested map is not in the difficulty mapping.")
    placement_index = MAP_DIFFICULTY_ORDER.index(map_id)
    return settings.crown_difficulties[placement_index]


def getCrownEnemyCount(map_id: Maps) -> int:
    """Get the amount of enemies in a crown map."""
    if map_id in (Maps.GalleonCrown, Maps.LobbyCrown, Maps.HelmCrown):
        return 4
    return 3


ANNOYING_ENEMIES = (Enemies.Klump, Enemies.Kosha, Enemies.Klobber)


def getBalancedCrownEnemyRando(spoiler, crown_setting: CrownEnemyDifficulty, damage_ohko_setting):
    """Get array of weighted enemies."""
    # this library will contain a list for every enemy it needs to generate
    enemy_swaps_library = {}

    if crown_setting == CrownEnemyDifficulty.vanilla:
        return {}
    # library of every crown map. will have a list of all enemies to put in those maps.
    enemy_swaps_library = {
        Maps.JapesCrown: [],
        Maps.AztecCrown: [],
        Maps.FactoryCrown: [],
        Maps.GalleonCrown: [],
        Maps.ForestCrown: [],
        Maps.CavesCrown: [],
        Maps.CastleCrown: [],
        Maps.HelmCrown: [],
        Maps.SnidesCrown: [],
        Maps.LobbyCrown: [],
    }
    # make 5 lists of enemies, per category.
    every_enemy = []  # every enemy (that can appear in crown battles)
    disruptive_max_1 = []  # anything that isn't... "2" disruptive (because disruptive is 1, at most)
    disruptive_at_most_kasplat = []  # anything that isn't marked as "disruptive"
    disruptive_0 = []  # the easiest enemies
    legacy_hard_mode = []  # legacy map with the exact same balance as the old "Hard" mode

    # Determine whether any crown-enabled enemies have been selected
    crown_enemy_found = False
    for enemy in EnemyMetaData:
        if enemy in spoiler.settings.enemies_selected:
            if EnemyMetaData[enemy].crown_enabled:
                if enemy is not Enemies.GetOut:
                    crown_enemy_found = True
                    break
    # Determine whether only GetOut is the only selected enemy that can appear in crown battles
    # If True, guarantees that there is 1 GetOut in every crown battle
    oops_all_get_out = False
    if crown_enemy_found is False:
        if Enemies.GetOut in spoiler.settings.enemies_selected:
            if damage_ohko_setting is False:
                oops_all_get_out = True
    # fill in the lists with the possibilities that belong in them.
    for enemy in EnemyMetaData:
        if EnemyMetaData[enemy].crown_enabled and enemy != Enemies.GetOut:
            if enemy in spoiler.settings.enemies_selected or (not crown_enemy_found):
                every_enemy.append(enemy)
                if EnemyMetaData[enemy].disruptive <= 1:
                    disruptive_max_1.append(enemy)
                if EnemyMetaData[enemy].kasplat is True:
                    disruptive_at_most_kasplat.append(enemy)
                elif EnemyMetaData[enemy].disruptive == 0:
                    disruptive_at_most_kasplat.append(enemy)
                    disruptive_0.append(enemy)
    # Make sure every list is populated, even if too few crown-enabled enemies have been selected
    # This breaks the crown balancing, but what the player wants, the player gets
    if len(disruptive_max_1) == 0:
        disruptive_max_1.extend(every_enemy.copy())
        for enemy in EnemyMetaData:
            if EnemyMetaData[enemy].disruptive > 1:
                EnemyMetaData[enemy].disruptive = 1
    if len(disruptive_at_most_kasplat) == 0:
        disruptive_at_most_kasplat.extend(disruptive_max_1.copy())
    if len(disruptive_0) == 0:
        disruptive_0.extend(disruptive_at_most_kasplat)
        for enemy in EnemyMetaData:
            if EnemyMetaData[enemy].disruptive > 0:
                EnemyMetaData[enemy].disruptive = 0
    # the legacy_hard_mode list is trickier to fill, but here goes:
    bias = 2
    for enemy in EnemyMetaData.keys():
        if EnemyMetaData[enemy].crown_enabled:
            if enemy in spoiler.settings.enemies_selected or crown_enemy_found is False:
                base_weight = EnemyMetaData[enemy].crown_weight
                weight_diff = abs(base_weight - bias)
                new_weight = abs(10 - weight_diff)
                if enemy == Enemies.GetOut:
                    new_weight = 1
                if damage_ohko_setting is False or enemy is not Enemies.GetOut:
                    for count in range(new_weight):
                        legacy_hard_mode.append(enemy)
    # picking enemies to put in the crown battles
    for map_id in enemy_swaps_library:
        difficulty = getCrownEnemyDifficultyFromMap(spoiler.settings, map_id)
        if difficulty == CrownEnemyDifficulty.easy:
            enemy_swaps_library[map_id].append(spoiler.settings.random.choice(disruptive_max_1))
            if oops_all_get_out is True:
                enemy_swaps_library[map_id].append(Enemies.GetOut)
            else:
                enemy_swaps_library[map_id].append(spoiler.settings.random.choice(disruptive_0))
            enemy_swaps_library[map_id].append(spoiler.settings.random.choice(disruptive_0))
            if map_id == Maps.GalleonCrown or map_id == Maps.LobbyCrown or map_id == Maps.HelmCrown:
                enemy_swaps_library[map_id].append(spoiler.settings.random.choice(disruptive_0))
        elif difficulty == CrownEnemyDifficulty.medium:
            new_enemy = 0
            count_disruptive = 0
            count_kasplats = 0
            number_of_enemies = 3
            if map_id == Maps.GalleonCrown or map_id == Maps.LobbyCrown or map_id == Maps.HelmCrown:
                number_of_enemies = 4
            for count in range(number_of_enemies):
                if count == 0 and oops_all_get_out is True:
                    new_enemy = Enemies.GetOut
                elif count_disruptive == 0:
                    if count_kasplats < 2:
                        new_enemy = spoiler.settings.random.choice(every_enemy)
                    elif count_kasplats == 2:
                        new_enemy = spoiler.settings.random.choice(disruptive_max_1)
                    elif count_kasplats == 3:
                        new_enemy = spoiler.settings.random.choice(disruptive_0)
                elif count_disruptive == 1:
                    if count_kasplats < 2:
                        new_enemy = spoiler.settings.random.choice(disruptive_max_1)
                    elif count_kasplats == 2:
                        new_enemy = spoiler.settings.random.choice(disruptive_0)
                elif count_disruptive == 2:
                    if count_kasplats == 0:
                        new_enemy = spoiler.settings.random.choice(disruptive_at_most_kasplat)
                    elif count_kasplats == 1:
                        new_enemy = spoiler.settings.random.choice(disruptive_0)
                if count_kasplats > 3 or (count_kasplats > 2 and count_disruptive > 1) or (count_kasplats == 2 and count_disruptive == 2):
                    print("This is a mistake in the crown enemy algorithm. Report this to the devs.")
                    new_enemy = Enemies.BeaverGold
                # We picked a new enemy, let's update our information and add it to the list
                if EnemyMetaData[new_enemy].kasplat is True:
                    count_kasplats = count_kasplats + 1
                count_disruptive = EnemyMetaData[new_enemy].disruptive + count_disruptive
                enemy_swaps_library[map_id].append(new_enemy)
        elif difficulty == CrownEnemyDifficulty.hard:
            number_of_enemies = getCrownEnemyCount(map_id)
            get_out_spawned_this_hard_map = False
            legacy_hard_mode_copy = legacy_hard_mode.copy()
            for count in range(number_of_enemies):
                if (not oops_all_get_out) and crown_setting == CrownEnemyDifficulty.progressive:
                    legacy_hard_mode_copy = [possible_enemy for possible_enemy in legacy_hard_mode_copy if possible_enemy != Enemies.GetOut]
                if count == 0 and oops_all_get_out:
                    enemy_to_place = Enemies.GetOut
                    get_out_spawned_this_hard_map = True
                else:
                    if get_out_spawned_this_hard_map:
                        legacy_hard_mode_copy = [possible_enemy for possible_enemy in legacy_hard_mode_copy if possible_enemy != Enemies.GetOut]
                    enemy_to_place = spoiler.settings.random.choice(legacy_hard_mode_copy)
                    if enemy_to_place in ANNOYING_ENEMIES:
                        no_annoying_enemies = [e for e in legacy_hard_mode_copy if e not in ANNOYING_ENEMIES]
                        if len(no_annoying_enemies) > 0:  # Make sure we're not going to be picking from an empty list
                            legacy_hard_mode_copy = no_annoying_enemies.copy()
                    if enemy_to_place == Enemies.GetOut:
                        get_out_spawned_this_hard_map = True
                enemy_swaps_library[map_id].append(enemy_to_place)
    # one last shuffle, to make sure any enemy can spawn in any spot
    for map_id in enemy_swaps_library:
        if len(enemy_swaps_library[map_id]) > 0:
            spoiler.settings.random.shuffle(enemy_swaps_library[map_id])
    return enemy_swaps_library


def writeEnemy(spoiler, ROM_COPY: LocalROM, cont_map_spawner_address: int, new_enemy_id: int, spawner: Spawner, cont_map_id: Maps, crown_timer: int = 0):
    """Write enemy to ROM."""
    ROM_COPY.seek(cont_map_spawner_address + spawner.offset)
    ROM_COPY.writeMultipleBytes(new_enemy_id, 1)
    # Enemy fixes
    if new_enemy_id in EnemyMetaData.keys():
        ROM_COPY.seek(cont_map_spawner_address + spawner.offset + 0x10)
        ROM_COPY.writeMultipleBytes(EnemyMetaData[new_enemy_id].aggro, 1)
        if new_enemy_id == Enemies.RoboKremling:
            ROM_COPY.seek(cont_map_spawner_address + spawner.offset + 0xB)
            ROM_COPY.writeMultipleBytes(0xC8, 1)
        elif new_enemy_id == Enemies.SpiderSmall:
            ROM_COPY.seek(cont_map_spawner_address + spawner.offset + 0x1)
            ROM_COPY.writeMultipleBytes(0, 1)
            ROM_COPY.seek(cont_map_spawner_address + spawner.offset + 0xB)
            ROM_COPY.writeMultipleBytes(0, 1)
            # Spawning fixes
            # Prevent respawn anim if that's how they initially appear
            ROM_COPY.seek(cont_map_spawner_address + spawner.offset + 0x12)
            init_respawn_state = int.from_bytes(ROM_COPY.readBytes(1), "big")
            if init_respawn_state == 3:
                ROM_COPY.seek(cont_map_spawner_address + spawner.offset + 0x12)
                ROM_COPY.writeMultipleBytes(0, 1)
            # Prevent them respawning
            ROM_COPY.seek(cont_map_spawner_address + spawner.offset + 0x14)
            ROM_COPY.writeMultipleBytes(0, 1)
        elif new_enemy_id == Enemies.Kaboom:
            # Fix their time to uh-oh timer
            ROM_COPY.seek(cont_map_spawner_address + spawner.offset + 0xA)
            ROM_COPY.writeMultipleBytes(140, 2)

        if (cont_map_id in crown_maps or cont_map_id in minigame_maps_total) and EnemyMetaData[new_enemy_id].air:
            height = 300
            if cont_map_id in crown_maps:
                height = int(spoiler.settings.random.uniform(250, 300))
            ROM_COPY.seek(cont_map_spawner_address + spawner.offset + 0x6)
            ROM_COPY.writeMultipleBytes(height, 2)
        if cont_map_id in crown_maps and new_enemy_id == Enemies.GetOut:
            ROM_COPY.seek(cont_map_spawner_address + spawner.offset + 0xA)
            get_out_timer = 20
            if crown_timer > 20:
                damage_mult = 1
                damage_amts = {DamageAmount.double: 2, DamageAmount.quad: 4, DamageAmount.ohko: 12}
                if spoiler.settings.damage_amount in damage_amts:
                    damage_mult = damage_amts[spoiler.settings.damage_amount]
                get_out_timer = spoiler.settings.random.randint(int(crown_timer / (12 / damage_mult)) + 1, crown_timer - 1)
            if get_out_timer == 0:
                get_out_timer = 1
            ROM_COPY.writeMultipleBytes(get_out_timer, 1)
            ROM_COPY.writeMultipleBytes(get_out_timer, 1)
        # Scale Adjustment
        if (EnemyMetaData[new_enemy_id].default_size is not None) and (cont_map_id not in banned_size_maps):
            scale = EnemyMetaData[new_enemy_id].default_size
            ROM_COPY.seek(cont_map_spawner_address + spawner.offset + 0xF)
            if cont_map_id == Maps.JapesTinyHive:
                # Is a mini monkey map, where we'd expect to see enemy sizes to be bigger to fit thematically
                scale = min(255, int(2.5 * scale))
            if new_enemy_id not in (Enemies.Gimpfish, Enemies.Shuri):  # Game is dumb
                if cont_map_id not in MAP_DIFFICULTY_ORDER:
                    if spoiler.settings.randomize_enemy_sizes:
                        lower_b = int(scale * 0.3)
                        if cont_map_id == Maps.CavesDiddyUpperCabin:
                            upper_b = scale
                        else:
                            upper_b = min(255, int(1.5 * scale))
                        chosen_scale = spoiler.settings.random.randint(lower_b, upper_b)
                        ROM_COPY.writeMultipleBytes(chosen_scale, 1)
                    elif spoiler.settings.normalize_enemy_sizes:
                        ROM_COPY.writeMultipleBytes(scale, 1)
        ROM_COPY.seek(cont_map_spawner_address + spawner.offset + 0xF)
        default_scale = int.from_bytes(ROM_COPY.readBytes(1), "big")
        if EnemyMetaData[new_enemy_id].size_cap > 0:
            if default_scale > EnemyMetaData[new_enemy_id].size_cap:
                ROM_COPY.seek(cont_map_spawner_address + spawner.offset + 0xF)
                ROM_COPY.writeMultipleBytes(EnemyMetaData[new_enemy_id].size_cap, 1)
        ROM_COPY.seek(cont_map_spawner_address + spawner.offset + 0xF)
        pre_size = int.from_bytes(ROM_COPY.readBytes(1), "big")
        if pre_size < EnemyMetaData[new_enemy_id].bbbarrage_min_scale and cont_map_id in bbbarrage_maps and ENABLE_BBBARRAGE_ENEMY_RANDO:
            ROM_COPY.seek(cont_map_spawner_address + spawner.offset + 0xF)
            ROM_COPY.writeMultipleBytes(EnemyMetaData[new_enemy_id].bbbarrage_min_scale, 1)
        if new_enemy_id in (Enemies.KlaptrapPurple, Enemies.KlaptrapRed) and cont_map_id == Maps.CavesDiddyLowerCabin:
            ROM_COPY.seek(cont_map_spawner_address + spawner.offset + 0xF)
            ROM_COPY.write(75)
        # Speed Adjustment
        if spoiler.settings.enemy_speed_rando:
            if cont_map_id not in banned_speed_maps:
                min_speed = EnemyMetaData[new_enemy_id].min_speed
                max_speed = EnemyMetaData[new_enemy_id].max_speed
                if min_speed > 0 and max_speed > 0:
                    ROM_COPY.seek(cont_map_spawner_address + spawner.offset + 0xD)
                    agg_speed = spoiler.settings.random.randint(min_speed, max_speed)
                    ROM_COPY.writeMultipleBytes(agg_speed, 1)
                    ROM_COPY.seek(cont_map_spawner_address + spawner.offset + 0xC)
                    ROM_COPY.writeMultipleBytes(spoiler.settings.random.randint(min_speed, agg_speed), 1)
        if cont_map_id in bbbarrage_maps and ENABLE_BBBARRAGE_ENEMY_RANDO:
            # Reduce Speeds
            ROM_COPY.seek(cont_map_spawner_address + spawner.offset + 0xC)
            speeds = []
            for x in range(2):
                speeds.append(int.from_bytes(ROM_COPY.readBytes(1), "big"))
            ROM_COPY.seek(cont_map_spawner_address + spawner.offset + 0xC)
            for x in speeds:
                ROM_COPY.writeMultipleBytes(int(x * 0.75), 1)
        elif cont_map_id in minigame_maps_beavers and new_enemy_id == Enemies.BeaverGold:
            for speed_offset in [0xC, 0xD]:
                ROM_COPY.seek(cont_map_spawner_address + spawner.offset + speed_offset)
                default_speed = int.from_bytes(ROM_COPY.readBytes(1), "big")
                new_speed = int(default_speed * 1.1)
                if new_speed > 255:
                    new_speed = 255
                ROM_COPY.seek(cont_map_spawner_address + spawner.offset + speed_offset)
                ROM_COPY.writeMultipleBytes(new_speed, 1)
        # Cap Klobber Speed
        if new_enemy_id in (Enemies.Klobber, Enemies.Kaboom):
            for speed_offset in [0xC, 0xD]:
                ROM_COPY.seek(cont_map_spawner_address + spawner.offset + speed_offset)
                current_speed = int.from_bytes(ROM_COPY.readBytes(1), "big")
                new_speed = max(1, int(current_speed * 0.6))
                ROM_COPY.seek(cont_map_spawner_address + spawner.offset + speed_offset)
                ROM_COPY.writeMultipleBytes(new_speed, 1)
    # Fix Tiny 5DI enemy to not respawn
    ROM_COPY.seek(cont_map_spawner_address + spawner.offset + 0x13)
    id = int.from_bytes(ROM_COPY.readBytes(1), "big")
    if cont_map_id == Maps.CavesTinyIgloo and id == 2:
        ROM_COPY.seek(cont_map_spawner_address + spawner.offset + 0x14)
        ROM_COPY.writeMultipleBytes(0, 1)  # Disable respawning


krem_kap_mapping = {
    Enemies.BeaverBlue: Items.PhotoBeaverBlue,
    Enemies.Book: Items.PhotoBook,
    Enemies.ZingerCharger: Items.PhotoZingerCharger,
    Enemies.Klobber: Items.PhotoKlobber,
    Enemies.Klump: Items.PhotoKlump,
    Enemies.Kaboom: Items.PhotoKaboom,
    Enemies.KlaptrapGreen: Items.PhotoKlaptrapGreen,
    Enemies.ZingerLime: Items.PhotoZingerLime,
    Enemies.KlaptrapPurple: Items.PhotoKlaptrapPurple,
    Enemies.KlaptrapRed: Items.PhotoKlaptrapRed,
    Enemies.BeaverGold: Items.PhotoBeaverGold,
    Enemies.Fireball: Items.PhotoFireball,
    Enemies.MushroomMan: Items.PhotoMushroomMan,
    Enemies.Ruler: Items.PhotoRuler,
    Enemies.RoboKremling: Items.PhotoRoboKremling,
    Enemies.Kremling: Items.PhotoKremling,
    Enemies.KasplatDK: Items.PhotoKasplatDK,
    Enemies.KasplatDiddy: Items.PhotoKasplatDiddy,
    Enemies.KasplatLanky: Items.PhotoKasplatLanky,
    Enemies.KasplatTiny: Items.PhotoKasplatTiny,
    Enemies.KasplatChunky: Items.PhotoKasplatChunky,
    Enemies.ZingerRobo: Items.PhotoZingerRobo,
    Enemies.Krossbones: Items.PhotoKrossbones,
    Enemies.Shuri: Items.PhotoShuri,
    Enemies.Gimpfish: Items.PhotoGimpfish,
    Enemies.MrDice0: Items.PhotoMrDice0,
    Enemies.SirDomino: Items.PhotoSirDomino,
    Enemies.MrDice1: Items.PhotoMrDice1,
    Enemies.Bat: Items.PhotoBat,
    Enemies.Ghost: Items.PhotoGhost,
    Enemies.Pufftup: Items.PhotoPufftup,
    Enemies.Kosha: Items.PhotoKosha,
    Enemies.SpiderSmall: Items.PhotoSpider,
    Enemies.FireballGlasses: Items.PhotoFireball,
    Enemies.Bug: Items.PhotoBug,
    Enemies.Guard: Items.PhotoKop,
    Enemies.GuardDisableA: Items.PhotoKop,
    Enemies.GuardDisableZ: Items.PhotoKop,
    Enemies.GuardGetOut: Items.PhotoKop,
    Enemies.GuardTag: Items.PhotoKop,
    Enemies.FairyQueen: Items.PhotoBFI,
    Enemies.IceTomato: Items.PhotoIceTomato,
    Enemies.Mermaid: Items.PhotoMermaid,
    Enemies.Llama: Items.PhotoLlama,
    Enemies.MechFish: Items.PhotoMechfish,
    Enemies.Seal1: Items.PhotoSeal,
}


def randomize_enemies_0(spoiler):
    """Determine randomized enemies."""
    data = {}
    pkmn = []
    resetPkmnSnap()
    spoiler.valid_photo_items = [
        Items.PhotoBook,  # Not randomized (yet), but permanently existing no matter what
        Items.PhotoTomato,  # Not randomized (yet), but permanently existing no matter what
        # Kasplats are always present outside enemy rando
        Items.PhotoKasplatDK,
        Items.PhotoKasplatDiddy,
        Items.PhotoKasplatLanky,
        Items.PhotoKasplatTiny,
        Items.PhotoKasplatChunky,
        Items.PhotoBFI,  # Not Randomized
        Items.PhotoIceTomato,  # Not Randomized
        Items.PhotoMermaid,  # Not Randomized
        Items.PhotoLlama,  # Not Randomized
        Items.PhotoMechfish,  # Not Randomized
        Items.PhotoSeal,  # Not Randomized
    ]
    for loc in spoiler.enemy_location_list:
        if spoiler.enemy_location_list[loc].enable_randomization:
            map = spoiler.enemy_location_list[loc].map
            if map not in data:
                data[map] = []
            new_enemy = spoiler.enemy_location_list[loc].placeNewEnemy(spoiler.settings.random, spoiler.settings.enemies_selected, True)
            krem_kap_location = (loc - Locations.JapesMainEnemy_Start) + Locations.KremKap_JapesMainEnemy_Start
            if krem_kap_location in spoiler.LocationList:
                item = krem_kap_mapping[new_enemy]
                spoiler.LocationList[krem_kap_location].default = item  # I hate hate hate this
                spoiler.LocationList[krem_kap_location].item = item
                if item not in spoiler.valid_photo_items:
                    spoiler.valid_photo_items.append(item)
                setPkmnSnapEnemy(new_enemy)
                if not spoiler.enemy_location_list[loc].respawns:
                    print(f"ALERT: INCORRECT ENEMY {loc.name}")
            elif spoiler.enemy_location_list[loc].respawns:
                print(f"ALERT: MISSING ENEMY {loc.name}")
            data[map].append(
                {
                    "enemy": new_enemy,
                    "speeds": [spoiler.enemy_location_list[loc].idle_speed, spoiler.enemy_location_list[loc].aggro_speed],
                    "id": spoiler.enemy_location_list[loc].id,
                    "location": Locations(loc).name,
                }
            )
    spoiler.enemy_rando_data = data
    for enemy in pkmn_snap_enemies:
        pkmn.append(enemy.spawned)
    spoiler.pkmn_snap_data = pkmn


def randomize_enemies(spoiler, ROM_COPY: LocalROM):
    """Write replaced enemies to ROM."""
    # Define Enemy Classes, Used for detection of if an enemy will be replaced
    enemy_classes = {}
    for enemy in EnemyMetaData:
        data = EnemyMetaData[enemy]
        if data.e_type != EnemySubtype.NoType and data.placeable:
            if data.e_type not in enemy_classes:
                enemy_classes[data.e_type] = []
            enemy_classes[data.e_type].append(enemy)

    # Define Enemies that can be placed in those classes
    enemy_placement_classes = {}
    banned_classes = []
    for enemy_class in enemy_classes:
        class_list = []
        for enemy in enemy_classes[enemy_class]:
            if enemy in spoiler.settings.enemies_selected:
                class_list.append(enemy)
        if len(class_list) == 0:
            # Nothing present, use backup
            for repl_type in replacement_priority[enemy_class]:
                if len(class_list) == 0:
                    for enemy in enemy_classes[repl_type]:
                        if enemy in spoiler.settings.enemies_selected:
                            class_list.append(enemy)
        if len(class_list) > 0:
            enemy_placement_classes[enemy_class] = class_list.copy()
        else:
            # Replace Nothing
            banned_classes.append(enemy_class)
    for enemy_class in banned_classes:
        del enemy_classes[enemy_class]
    # Crown Enemy Stuff
    crown_enemies_library = {}
    crown_enemies = []
    for enemy in EnemyMetaData:
        if EnemyMetaData[enemy].crown_enabled is True:
            crown_enemies.append(enemy)
    if len(spoiler.settings.enemies_selected) > 0 or spoiler.settings.crown_enemy_difficulty != CrownEnemyDifficulty.vanilla:
        boolean_damage_is_ohko = spoiler.settings.damage_amount == DamageAmount.ohko
        crown_enemies_library = getBalancedCrownEnemyRando(spoiler, spoiler.settings.crown_enemy_difficulty, boolean_damage_is_ohko)
        minigame_enemies_simple = []
        minigame_enemies_beatable = []
        minigame_enemies_nolimit = []
        minigame_enemies_beavers = []
        for enemy in EnemyMetaData:
            if EnemyMetaData[enemy].minigame_enabled:
                minigame_enemies_nolimit.append(enemy)
                if EnemyMetaData[enemy].beaver:
                    minigame_enemies_beavers.append(enemy)
                if EnemyMetaData[enemy].killable:
                    minigame_enemies_beatable.append(enemy)
                    if EnemyMetaData[enemy].simple:
                        minigame_enemies_simple.append(enemy)
        for cont_map_id in range(216):
            cont_map_spawner_address = getPointerLocation(TableNames.Spawners, cont_map_id)
            vanilla_spawners = []
            ROM_COPY.seek(cont_map_spawner_address)
            fence_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            offset = 2
            if fence_count > 0:
                for x in range(fence_count):
                    ROM_COPY.seek(cont_map_spawner_address + offset)
                    point_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
                    offset += (point_count * 6) + 2
                    ROM_COPY.seek(cont_map_spawner_address + offset)
                    point0_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
                    offset += (point0_count * 10) + 6
            ROM_COPY.seek(cont_map_spawner_address + offset)
            spawner_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            # Generate Enemy Swaps lists
            enemy_swaps = {}
            for enemy_class in enemy_classes:
                arr = []
                for x in range(spawner_count):
                    arr.append(spoiler.settings.random.choice(enemy_placement_classes[enemy_class]))
                enemy_swaps[enemy_class] = arr
            offset += 2
            for _ in range(spawner_count):
                ROM_COPY.seek(cont_map_spawner_address + offset)
                enemy_id = int.from_bytes(ROM_COPY.readBytes(1), "big")
                ROM_COPY.seek(cont_map_spawner_address + offset + 0x13)
                enemy_index = int.from_bytes(ROM_COPY.readBytes(1), "big")
                init_offset = offset
                ROM_COPY.seek(cont_map_spawner_address + offset + 0x11)
                extra_count = int.from_bytes(ROM_COPY.readBytes(1), "big")
                offset += 0x16 + (extra_count * 2)
                vanilla_spawners.append(Spawner(enemy_id, init_offset, enemy_index))
            if len(spoiler.settings.enemies_selected) > 0 and cont_map_id in spoiler.enemy_rando_data:
                referenced_spawner = None
                for enemy in spoiler.enemy_rando_data[cont_map_id]:
                    for spawner in vanilla_spawners:
                        if spawner.index == enemy["id"]:
                            referenced_spawner = spawner
                            break
                    if referenced_spawner is not None:
                        writeEnemy(spoiler, ROM_COPY, cont_map_spawner_address, enemy["enemy"], referenced_spawner, cont_map_id, 0)
            if len(spoiler.settings.enemies_selected) > 0 and cont_map_id in minigame_maps_total:
                tied_enemy_list = []
                if cont_map_id in minigame_maps_easy:
                    tied_enemy_list = minigame_enemies_simple.copy()
                    if cont_map_id in bbbarrage_maps and ENABLE_BBBARRAGE_ENEMY_RANDO:
                        if Enemies.KlaptrapGreen in tied_enemy_list:
                            tied_enemy_list.remove(Enemies.KlaptrapGreen)  # Remove Green Klaptrap out of BBBarrage pool
                elif cont_map_id in minigame_maps_beatable:
                    tied_enemy_list = minigame_enemies_beatable.copy()
                elif cont_map_id in minigame_maps_nolimit:
                    tied_enemy_list = minigame_enemies_nolimit.copy()
                elif cont_map_id in minigame_maps_beavers:
                    tied_enemy_list = minigame_enemies_beavers.copy()
                for spawner in vanilla_spawners:
                    if spawner.enemy_id in tied_enemy_list:
                        new_enemy_id = spoiler.settings.random.choice(tied_enemy_list)
                        # Balance beaver bother so it's a 4:1 ratio of blue to gold beavers, guarantee 1 gold
                        if cont_map_id in minigame_maps_beavers:
                            if spawner.index == 1:
                                new_enemy_id = Enemies.BeaverGold
                            else:
                                selection = spoiler.settings.random.uniform(0, 1)
                                new_enemy_id = Enemies.BeaverBlue
                                if selection < 0.2:
                                    new_enemy_id = Enemies.BeaverGold
                        writeEnemy(spoiler, ROM_COPY, cont_map_spawner_address, new_enemy_id, spawner, cont_map_id, 0)
            if spoiler.settings.crown_enemy_difficulty != CrownEnemyDifficulty.vanilla and cont_map_id in crown_maps:
                # Determine Crown Timer
                limits = {
                    CrownEnemyDifficulty.easy: 5,
                    CrownEnemyDifficulty.medium: 15,
                    CrownEnemyDifficulty.hard: 30,
                }
                difficulty = getCrownEnemyDifficultyFromMap(spoiler.settings, cont_map_id)
                low_limit = limits.get(difficulty, 5)
                crown_timer = spoiler.settings.random.randint(low_limit, low_limit + 30)
                # Place Enemies
                for spawner in vanilla_spawners:
                    if spawner.enemy_id in crown_enemies:
                        new_enemy_id = crown_enemies_library[cont_map_id].pop()
                        writeEnemy(spoiler, ROM_COPY, cont_map_spawner_address, new_enemy_id, spawner, cont_map_id, crown_timer)
                    elif spawner.enemy_id == Enemies.BattleCrownController:
                        ROM_COPY.seek(cont_map_spawner_address + spawner.offset + 0xB)
                        ROM_COPY.writeMultipleBytes(crown_timer, 1)  # Determine Crown length. DK64 caps at 255 seconds
        if spoiler.settings.win_condition_item == WinConditionComplex.krem_kapture:
            # Pkmn snap handler
            values = [0, 0, 0, 0, 0, 0]
            # In some cases, the Pkmn Snap data hasn't yet been initialized (enemy rando disabled)
            # so we use the default values
            if len(spoiler.pkmn_snap_data) == 0:
                # Pkmn Snap Default Enemies
                spoiler.pkmn_snap_data = [
                    True,  # Kaboom
                    True,  # Blue Beaver
                    True,  # Book
                    True,  # Klobber
                    True,  # Zinger (Charger)
                    True,  # Klump
                    True,  # Klaptrap (Green)
                    True,  # Zinger (Bomber)
                    True,  # Klaptrap (Purple)
                    False,  # Klaptrap (Red)
                    False,  # Gold Beaver
                    True,  # Mushroom Man
                    True,  # Ruler
                    True,  # Robo-Kremling
                    True,  # Kremling
                    True,  # Kasplat (DK)
                    True,  # Kasplat (Diddy)
                    True,  # Kasplat (Lanky)
                    True,  # Kasplat (Tiny)
                    True,  # Kasplat (Chunky)
                    False,  # Kop
                    True,  # Robo-Zinger
                    True,  # Krossbones
                    True,  # Shuri
                    True,  # Gimpfish
                    True,  # Mr. Dice (Green)
                    True,  # Sir Domino
                    True,  # Mr. Dice (Red)
                    True,  # Fireball w/ Glasses
                    True,  # Small Spider
                    True,  # Bat
                    True,  # Tomato
                    True,  # Ghost
                    True,  # Pufftup
                    True,  # Kosha
                    True,  # Fairy Queen
                    True,  # Ice Tomato
                    True,  # Mermaid
                    True,  # Llama
                    True,  # Mechfish
                    True,  # Seal
                ]
            for enemy_index, spawned in enumerate(spoiler.pkmn_snap_data):
                if spawned:
                    offset = enemy_index >> 3
                    shift = enemy_index & 7
                    values[offset] |= 1 << shift
            ROM_COPY.seek(spoiler.settings.rom_data + 0x196)
            for value in values:
                ROM_COPY.writeMultipleBytes(value, 1)
