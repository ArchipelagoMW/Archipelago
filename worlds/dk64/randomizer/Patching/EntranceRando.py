"""Randomize Entrances passed from Misc options."""

from randomizer.Enums.Settings import ShuffleLoadingZones, HelmSetting
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Maps import Maps
from randomizer.Lists.MapsAndExits import GetExitId, GetMapId
from randomizer.Patching.Patcher import LocalROM
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames

valid_lz_types = [9, 12, 13, 16]


def getFilteredExit(settings, mapId, exit):
    """Filter the output of GetExitID."""
    if mapId == Maps.HideoutHelm:
        entry_mapping = {
            HelmSetting.default: 0,
            HelmSetting.skip_start: 3,
            HelmSetting.skip_all: 4,
        }
        return entry_mapping.get(settings.helm_setting, 0)
    return exit


def getOneByteExit(back):
    """Convert 'getExitId' output to something acceptable to write to a 1-byte value."""
    value = GetExitId(back)
    if value < 0:
        return value + 0x100
    return value


def getEntranceDict(spoiler, transition: Transitions, vanilla_map: Maps, vanilla_exit: int) -> dict:
    """Create the LZR Entrance dict for a locally stored entrance."""
    if transition in spoiler.shuffled_exit_data:
        shuffledBack = spoiler.shuffled_exit_data[transition]
        map_id = GetMapId(spoiler.settings, shuffledBack.regionId)
        return {
            "map": map_id,
            "exit": getFilteredExit(spoiler.settings, map_id, GetExitId(shuffledBack)),
        }
    return {
        "map": vanilla_map,
        "exit": getFilteredExit(spoiler.settings, vanilla_map, vanilla_exit),
    }


def writeEntrance(ROM_COPY: LocalROM, spoiler, transition: Transitions, offset: int, vanilla_map: Maps, vanilla_exit: int):
    """Write LZREntrance struct to ROM."""
    ROM_COPY.seek(spoiler.settings.rom_data + offset)
    data = getEntranceDict(spoiler, transition, vanilla_map, vanilla_exit)
    exit_id = data["exit"]
    if exit_id < 0:
        exit_id += 0x100
    ROM_COPY.write(data["map"])
    ROM_COPY.write(exit_id & 0xFF)


def randomize_entrances(spoiler, ROM_COPY: LocalROM):
    """Randomize Entrances based on shuffled_exit_instructions."""
    if spoiler.settings.shuffle_loading_zones == ShuffleLoadingZones.all and spoiler.shuffled_exit_instructions is not None:
        for cont_map in spoiler.shuffled_exit_instructions:
            # Pointer table 18, use the map index detailed in cont_map["container_map"] to get the starting address of the map lz file
            cont_map_id = int(cont_map["container_map"])
            cont_map_lzs_address = getPointerLocation(TableNames.Triggers, cont_map_id)
            ROM_COPY.seek(cont_map_lzs_address)
            lz_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            for lz_id in range(lz_count):
                start = (lz_id * 0x38) + 2
                ROM_COPY.seek(cont_map_lzs_address + start + 0x10)
                lz_type = int.from_bytes(ROM_COPY.readBytes(2), "big")
                # print(lz_type)
                if lz_type in valid_lz_types:
                    ROM_COPY.seek(cont_map_lzs_address + start + 0x12)
                    lz_map = int.from_bytes(ROM_COPY.readBytes(2), "big")
                    ROM_COPY.seek(cont_map_lzs_address + start + 0x14)
                    lz_exit = int.from_bytes(ROM_COPY.readBytes(2), "big")
                    for zone in cont_map["zones"]:
                        if lz_map == zone["vanilla_map"]:
                            if lz_exit == zone["vanilla_exit"] or (lz_map == Maps.FactoryCrusher):
                                ROM_COPY.seek(cont_map_lzs_address + start + 0x12)
                                ROM_COPY.writeMultipleBytes(zone["new_map"], 2)
                                ROM_COPY.seek(cont_map_lzs_address + start + 0x14)
                                ROM_COPY.writeMultipleBytes(getFilteredExit(spoiler.settings, zone["new_map"], zone["new_exit"]), 2)
                                if zone["new_map"] == Maps.HideoutHelm:
                                    # Set to LZ Type 9, which does the Helm filtering
                                    ROM_COPY.seek(cont_map_lzs_address + start + 0x10)
                                    ROM_COPY.writeMultipleBytes(9, 2)
        varspaceOffset = spoiler.settings.rom_data
        # Force call parent filter
        ROM_COPY.seek(varspaceOffset + 0x47)
        ROM_COPY.write(1)
        # /* 0x05D */ char randomize_more_loading_zones; // 0 = Not randomizing loading zones inside levels. 1 = On
        moreLoadingZonesOffset = 0x05D
        ROM_COPY.seek(varspaceOffset + moreLoadingZonesOffset)
        ROM_COPY.write(1)
        writeEntrance(ROM_COPY, spoiler, Transitions.AztecMainToRace, 0x5E, Maps.AztecTinyRace, 0)
        writeEntrance(ROM_COPY, spoiler, Transitions.GalleonLighthouseAreaToSickBay, 0x6A, Maps.GalleonSickBay, 0)
        writeEntrance(ROM_COPY, spoiler, Transitions.ForestMainToCarts, 0x6C, Maps.ForestMinecarts, 0)
        writeEntrance(ROM_COPY, spoiler, Transitions.IslesMainToCastleLobby, 0x74, Maps.CreepyCastleLobby, 0)
        # /* 0x078 */ unsigned short exit_levels[8]; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        enter_transitions = [
            Transitions.IslesToJapes,
            Transitions.IslesToAztec,
            Transitions.IslesToFactory,
            Transitions.IslesToGalleon,
            Transitions.IslesToForest,
            Transitions.IslesToCaves,
            Transitions.IslesToCastle,
        ]
        exit_transitions = [
            Transitions.JapesToIsles,
            Transitions.AztecToIsles,
            Transitions.FactoryToIsles,
            Transitions.GalleonToIsles,
            Transitions.ForestToIsles,
            Transitions.CavesToIsles,
            Transitions.CastleToIsles,
            Transitions.HelmToIsles,
        ]
        ROM_COPY.seek(varspaceOffset + 0x78)
        for transition in exit_transitions:
            if transition == Transitions.HelmToIsles and not spoiler.settings.shuffle_helm_location:
                # Helm exit won't be in the shuffled_exit_data dict, so just write the vanilla value without reference
                ROM_COPY.write(Maps.HideoutHelmLobby)
                ROM_COPY.write(1)
            else:
                shuffledBack = spoiler.shuffled_exit_data[transition]
                map_id = GetMapId(spoiler.settings, shuffledBack.regionId)
                ROM_COPY.write(map_id)
                ROM_COPY.write(getFilteredExit(spoiler.settings, map_id, getOneByteExit(shuffledBack)))
        # /* 0x088 */ unsigned short enter_levels[7]; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
        for world_index, transition in enumerate(enter_transitions):
            shuffledBack = spoiler.shuffled_exit_data[transition]
            map_id = GetMapId(spoiler.settings, shuffledBack.regionId)
            exit_id = GetExitId(shuffledBack)
            spoiler.settings.level_portal_destinations[world_index] = {
                "map": map_id,
                "exit": exit_id,
            }
        writeEntrance(ROM_COPY, spoiler, Transitions.CastleBallroomToMuseum, 0x130, Maps.CastleMuseum, 2)
        writeEntrance(ROM_COPY, spoiler, Transitions.CastleMuseumToBallroom, 0x132, Maps.CastleBallroom, 1)
        # Mech Fish Entrance
        spoiler.settings.mech_fish_entrance = getEntranceDict(spoiler, Transitions.GalleonShipyardToMechFish, Maps.GalleonMechafish, 0)
        # Mech Fish Exit
        writeEntrance(ROM_COPY, spoiler, Transitions.GalleonMechFishToShipyard, 0x32, Maps.GloomyGalleon, 34)


banned_filtration = (Maps.Cranky, Maps.Candy, Maps.Funky, Maps.Snide, Maps.HideoutHelm)
museum_exit_type = 13  # Maybe 9?


def filterEntranceType(ROM_COPY: LocalROM):
    """Change LZ Type for some entrances so that warps from crown pads work correctly."""
    for cont_map_id in range(216):
        cont_map_lzs_address = getPointerLocation(TableNames.Triggers, cont_map_id)
        ROM_COPY.seek(cont_map_lzs_address)
        lz_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
        for lz_id in range(lz_count):
            start = (lz_id * 0x38) + 2
            ROM_COPY.seek(cont_map_lzs_address + start + 0x10)
            lz_type = int.from_bytes(ROM_COPY.readBytes(2), "big")
            lz_map = int.from_bytes(ROM_COPY.readBytes(2), "big")
            if lz_type == 0x10 and lz_map not in banned_filtration:
                # Change type to 0xC
                ROM_COPY.seek(cont_map_lzs_address + start + 0x10)
                ROM_COPY.writeMultipleBytes(0xC, 2)
                # Change fade type to spin
                ROM_COPY.seek(cont_map_lzs_address + start + 0x16)
                ROM_COPY.writeMultipleBytes(0, 2)
            if cont_map_id == Maps.CastleMuseum and lz_id == 0 and lz_map not in banned_filtration:
                # Disable objects through museum exit
                ROM_COPY.seek(cont_map_lzs_address + start + 0x10)
                ROM_COPY.writeMultipleBytes(museum_exit_type, 2)


class ItemPreviewCutscene:
    """Class to store information regarding an item preview cutscene."""

    def __init__(self, map: Maps, old_cutscene: int, new_cutscene: int):
        """Initialize with given parameters."""
        self.map = map
        self.old_cutscene = old_cutscene
        self.new_cutscene = new_cutscene


ITEM_PREVIEW_CUTSCENES = [
    ItemPreviewCutscene(Maps.ForestSpider, 3, 9),
    # ItemPreviewCutscene(Maps.CavesChunkyIgloo, 0, 5),
]


def enableTriggerText(spoiler, ROM_COPY: LocalROM):
    """Change the cutscene trigger in Spider Boss and Chunky Igloo to the specific item reward cutscene."""
    if spoiler.settings.item_reward_previews:
        for cs in ITEM_PREVIEW_CUTSCENES:
            cont_map_lzs_address = getPointerLocation(TableNames.Triggers, cs.map)
            ROM_COPY.seek(cont_map_lzs_address)
            lz_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            for lz_id in range(lz_count):
                start = (lz_id * 0x38) + 2
                ROM_COPY.seek(cont_map_lzs_address + start + 0x10)
                lz_type = int.from_bytes(ROM_COPY.readBytes(2), "big")
                lz_cutscene = int.from_bytes(ROM_COPY.readBytes(2), "big")
                if lz_type == 10 and lz_cutscene == cs.old_cutscene:
                    # Change cutscene
                    ROM_COPY.seek(cont_map_lzs_address + start + 0x12)
                    ROM_COPY.writeMultipleBytes(cs.new_cutscene, 2)


def placeLevelOrder(spoiler, order: list, ROM_COPY: LocalROM):
    """Write level order to ROM."""
    varspaceOffset = spoiler.settings.rom_data
    lobbies = [
        Maps.JungleJapesLobby,
        Maps.AngryAztecLobby,
        Maps.FranticFactoryLobby,
        Maps.GloomyGalleonLobby,
        Maps.FungiForestLobby,
        Maps.CrystalCavesLobby,
        Maps.CreepyCastleLobby,
        Maps.HideoutHelmLobby,
    ]
    lobby_exits = [2, 3, 4, 5, 6, 10, 11, 7]
    altered_maps = {
        Maps.Isles: [],
        Maps.JungleJapesLobby: [],
        Maps.AngryAztecLobby: [],
        Maps.FranticFactoryLobby: [],
        Maps.GloomyGalleonLobby: [],
        Maps.FungiForestLobby: [],
        Maps.CrystalCavesLobby: [],
        Maps.CreepyCastleLobby: [],
        Maps.HideoutHelmLobby: [],
    }
    for index, item in enumerate(order):
        altered_maps[Maps.Isles].append({"original_map": lobbies[index], "original_exit": 0, "new_map": lobbies[item], "new_exit": 0})
        exit = None
        for index2, item2 in enumerate(order):
            if index == item2:
                exit = lobby_exits[index2]
        altered_maps[lobbies[index]].append({"original_map": Maps.Isles, "original_exit": lobby_exits[index], "new_map": Maps.Isles, "new_exit": exit})

    for cont_map_id in altered_maps:
        cont_map_lzs_address = getPointerLocation(TableNames.Triggers, cont_map_id)
        ROM_COPY.seek(cont_map_lzs_address)
        lz_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
        for lz_id in range(lz_count):
            start = (lz_id * 0x38) + 2
            ROM_COPY.seek(cont_map_lzs_address + start + 0x10)
            lz_type = int.from_bytes(ROM_COPY.readBytes(2), "big")
            if lz_type in valid_lz_types:
                ROM_COPY.seek(cont_map_lzs_address + start + 0x12)
                lz_map = int.from_bytes(ROM_COPY.readBytes(2), "big")
                ROM_COPY.seek(cont_map_lzs_address + start + 0x14)
                lz_exit = int.from_bytes(ROM_COPY.readBytes(2), "big")
                for zone in altered_maps[cont_map_id]:
                    if lz_map == zone["original_map"]:
                        if lz_exit == zone["original_exit"]:
                            ROM_COPY.seek(cont_map_lzs_address + start + 0x12)
                            ROM_COPY.writeMultipleBytes(zone["new_map"], 2)
                            ROM_COPY.seek(cont_map_lzs_address + start + 0x14)
                            ROM_COPY.writeMultipleBytes(zone["new_exit"], 2)
                            if zone["new_map"] == Maps.HideoutHelm:
                                # Set to LZ Type 9, which does the Helm filtering
                                ROM_COPY.seek(cont_map_lzs_address + start + 0x10)
                                ROM_COPY.writeMultipleBytes(9, 2)
                            elif cont_map_id == Maps.CastleMuseum and lz_id == 0:
                                # Disable objects through museum exit
                                ROM_COPY.seek(cont_map_lzs_address + start + 0x10)
                                ROM_COPY.writeMultipleBytes(museum_exit_type, 2)
    level_7_lobby = lobbies[order[6]]
    ROM_COPY.seek(varspaceOffset + 0x5D)
    ROM_COPY.write(2)
    ROM_COPY.seek(varspaceOffset + 0x74)
    ROM_COPY.write(level_7_lobby)
    ROM_COPY.write(0)
