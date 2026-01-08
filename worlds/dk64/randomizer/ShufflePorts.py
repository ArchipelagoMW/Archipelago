"""Shuffle Bananaport Locations."""

from randomizer.Lists.MapsAndExits import RegionMapList
import randomizer.LogicFiles.AngryAztec
import randomizer.LogicFiles.CreepyCastle
import randomizer.LogicFiles.CrystalCaves
import randomizer.LogicFiles.DKIsles
import randomizer.LogicFiles.FranticFactory
import randomizer.LogicFiles.FungiForest
import randomizer.LogicFiles.GloomyGalleon
import randomizer.LogicFiles.JungleJapes
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Events import Events
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Settings import ActivateAllBananaports, ShufflePortLocations
from randomizer.Lists.CustomLocations import CustomLocation, CustomLocations, LocationTypes, getBannedWarps
from randomizer.Lists.Warps import BananaportVanilla
from randomizer.LogicClasses import Event

PortShufflerData = {
    Maps.JungleJapes: {
        "level": Levels.JungleJapes,
        "starting_warp": Events.JapesW1aTagged,
        "global_warp_count": 10,
    },
    Maps.AngryAztec: {
        "level": Levels.AngryAztec,
        "starting_warp": Events.AztecW1aTagged,
        "global_warp_count": 10,
    },
    Maps.FranticFactory: {
        "level": Levels.FranticFactory,
        "starting_warp": Events.FactoryW1aTagged,
        "global_warp_count": 10,
    },
    Maps.GloomyGalleon: {
        "level": Levels.GloomyGalleon,
        "starting_warp": Events.GalleonW1aTagged,
        "global_warp_count": 10,
    },
    Maps.FungiForest: {
        "level": Levels.FungiForest,
        "starting_warp": Events.ForestW1aTagged,
        "global_warp_count": 10,
    },
    Maps.CrystalCaves: {
        "level": Levels.CrystalCaves,
        "starting_warp": Events.CavesW1aTagged,
        "global_warp_count": 10,
    },
    Maps.CreepyCastle: {
        "level": Levels.CreepyCastle,
        "starting_warp": Events.CastleW1aTagged,
        "global_warp_count": 10,
    },
    Maps.Isles: {
        "level": Levels.DKIsles,
        "starting_warp": Events.IslesW1aTagged,
        "global_warp_count": 10,
    },
    Maps.AztecLlamaTemple: {
        "level": Levels.AngryAztec,
        "starting_warp": Events.LlamaW1aTagged,
        "global_warp_count": 4,
    },
    Maps.CastleCrypt: {
        "level": Levels.CreepyCastle,
        "starting_warp": Events.CryptW1aTagged,
        "global_warp_count": 6,
    },
}


def addPort(spoiler, warp: CustomLocation, event_enum: Events):
    """Add bananaport to relevant Logic Region."""
    spoiler.RegionList[warp.logic_region].events.append(Event(event_enum, warp.logic))
    for k in BananaportVanilla:
        if BananaportVanilla[k].event == event_enum:
            BananaportVanilla[k].region_id = warp.logic_region


def removePorts(spoiler, permitted_maps: list[Maps]):
    """Remove all bananaports from Logic regions."""
    level_logic_regions = {
        Levels.DKIsles: randomizer.LogicFiles.DKIsles.LogicRegions,
        Levels.JungleJapes: randomizer.LogicFiles.JungleJapes.LogicRegions,
        Levels.AngryAztec: randomizer.LogicFiles.AngryAztec.LogicRegions,
        Levels.FranticFactory: randomizer.LogicFiles.FranticFactory.LogicRegions,
        Levels.GloomyGalleon: randomizer.LogicFiles.GloomyGalleon.LogicRegions,
        Levels.FungiForest: randomizer.LogicFiles.FungiForest.LogicRegions,
        Levels.CrystalCaves: randomizer.LogicFiles.CrystalCaves.LogicRegions,
        Levels.CreepyCastle: randomizer.LogicFiles.CreepyCastle.LogicRegions,
    }
    BANNED_PORT_SHUFFLE_EVENTS = getBannedWarps(spoiler)
    persisted_events = []
    for map_id in PortShufflerData:
        if map_id not in permitted_maps:
            start_event = PortShufflerData[map_id]["starting_warp"]
            total_count = PortShufflerData[map_id]["global_warp_count"]
            persisted_events.extend([start_event + i for i in range(total_count)])
    for level_id in level_logic_regions:
        level = level_logic_regions[level_id]
        for region in level:
            region_data = spoiler.RegionList[region]
            region_data.events = [
                x for x in region_data.events if x.name < Events.JapesW1aTagged or x.name > Events.IslesW5bTagged or x.name in BANNED_PORT_SHUFFLE_EVENTS or x.name in persisted_events
            ]


def ResetPorts():
    """Reset all bananaports to their vanilla state."""
    for k in BananaportVanilla:
        BananaportVanilla[k].reset()


def isCustomLocationValid(spoiler, location: CustomLocation, map_id: Maps, level: Levels) -> bool:
    """Determine whether a custom location is valid for a warp pad."""
    if location.map != map_id:
        # Has to be in the right map
        return False
    if location.has_access_logic:
        # Locations that have logic to access them are banned from being warp locations when those warps are pre-activated
        if spoiler.settings.activate_all_bananaports == ActivateAllBananaports.all:
            return False
        elif spoiler.settings.activate_all_bananaports != ActivateAllBananaports.off and map_id == Maps.Isles:
            return False
    BANNED_PORT_SHUFFLE_EVENTS = getBannedWarps(spoiler)
    if location.tied_warp_event is not None:
        if location.tied_warp_event in BANNED_PORT_SHUFFLE_EVENTS:
            # Disable all locked warp locations
            return False
    if spoiler.settings.enable_plandomizer:
        if location.name in spoiler.settings.plandomizer_dict["reserved_custom_locations"][level]:
            return False
    if location.is_galleon_floating_crate:
        return False
    if location.map in [Maps.FungiForestLobby, Maps.CavesRotatingCabin]:
        if location.vanilla_crown:
            return False
    if spoiler.settings.bananaport_placement_rando == ShufflePortLocations.vanilla_only:
        if not location.vanilla_port:
            return False
        else:
            return True
    if spoiler.settings.bananaport_placement_rando == ShufflePortLocations.half_vanilla or (
        spoiler.settings.bananaport_placement_rando == ShufflePortLocations.on and not spoiler.settings.useful_bananaport_placement
    ):
        if location.logic_region in ONE_KONG_REGIONS:
            return False
    return location.isValidLocation(LocationTypes.Bananaport)


REGION_KLUMPS = {
    # A way to bias against zones of a map with a lot of logic regions
    # Any entries in the list will sort regarding region dict based on the key rather than the normal value
    Regions.IslesMainUpper: [Regions.IslesEar, Regions.IslesHill],
    Regions.KremIsleBeyondLift: [Regions.KremIsleMouth, Regions.KremIsleTopLevel],
    Regions.CabinIsle: [Regions.IslesAboveWaterfall],
    Regions.JungleJapesStart: [Regions.JapesBlastPadPlatform],
    Regions.JungleJapesMain: [Regions.JapesTnSAlcove, Regions.JapesPaintingRoomHill],
    Regions.JapesHill: [Regions.JapesHillTop, Regions.JapesCannonPlatform, Regions.JapesTopOfMountain],
    Regions.JapesBeyondCoconutGate2: [Regions.JapesLankyCave, Regions.JapesUselessSlope],
    Regions.AztecTunnelBeforeOasis: [Regions.AngryAztecStart, Regions.BetweenVinesByPortal],
    Regions.TempleStart: [Regions.TempleGuitarPad],
    Regions.LlamaTemple: [Regions.LlamaTempleBack, Regions.LlamaTempleMatching],
    Regions.DonkeyTemple: [Regions.DonkeyTempleDeadEndRight],
    Regions.DiddyTemple: [Regions.DiddyTempleDeadEndRight],
    Regions.LankyTemple: [Regions.LankyTempleEntrance],
    Regions.TinyTemple: [Regions.TinyTempleEntrance],
    Regions.ChunkyTemple: [Regions.ChunkyTempleEntrance],
    Regions.BeyondHatch: [Regions.FactoryStoragePipe],
    Regions.RandD: [Regions.RandDUpper],
    Regions.MiddleCore: [Regions.SpinningCore, Regions.UpperCore],
    Regions.Lighthouse: [Regions.LighthouseAboveLadder],
    Regions.MushroomUpperExterior: [Regions.MushroomNightExterior],
    Regions.MushroomLowerExterior: [Regions.MushroomUpperMidExterior, Regions.MushroomBlastLevelExterior, Regions.GiantMushroomArea],
    Regions.MillArea: [Regions.ForestTopOfMill, Regions.ForestVeryTopOfMill, Regions.ForestMillTopOfNightCage],
    Regions.CrystalCavesMain: [Regions.CavesBlueprintPillar, Regions.CavesBananaportSpire, Regions.CavesBonusCave],
    Regions.CabinArea: [Regions.CavesGGRoom, Regions.CavesRotatingCabinRoof, Regions.CavesSprintCabinRoof],
    Regions.CastleTree: [Regions.CastleTreePastPunch],
    Regions.Crypt: [Regions.CryptChunkyRoom, Regions.CryptDiddyRoom, Regions.CryptDonkeyRoom],
}

ONE_KONG_REGIONS = [
    # These regions are not accessible by every kong.
    Regions.JapesTopOfMountain,
    Regions.AztecDonkeyQuicksandCave,
    Regions.LlamaTempleBack,
    Regions.FactoryTinyRaceLobby,
    Regions.TreasureRoomDiddyGoldTower,
    Regions.CavesBonusCave,
    Regions.CavesBlueprintCave,
    Regions.CavesBlueprintPillar,
    Regions.CavesBananaportSpire,
]

warp_event_pairs = {}


def populate_warp_event_pairs():
    """Populate the dict of warp_event_pairs."""
    for k in BananaportVanilla:
        warp = BananaportVanilla[k].event
        if warp not in warp_event_pairs.keys():
            other_warp = [
                x.event for x in BananaportVanilla.values() if x.map_id == BananaportVanilla[k].map_id and x.vanilla_warp == BananaportVanilla[k].vanilla_warp and x.event != BananaportVanilla[k].event
            ][0]
            warp_event_pairs[warp] = other_warp
            warp_event_pairs[other_warp] = warp


def selectUsefulWarpFullShuffle(random, list_of_custom_locations, list_of_warps, warp: CustomLocation = None):
    """Find a useful warp to link to given warp."""
    region = warp.logic_region
    klumped_regions = []
    if region in REGION_KLUMPS.keys():
        klumped_regions = REGION_KLUMPS[region]
    klumped_regions.append(Regions.CreepyCastleMain)
    x = warp.coords[0]
    y = warp.coords[1]
    z = warp.coords[2]
    big_logic_regions = [Regions.CrystalCavesMain, Regions.CreepyCastleMain]
    possible_warps = [x for x in list_of_warps if list_of_custom_locations[x].logic_region != region or list_of_custom_locations[x].logic_region in big_logic_regions]
    if warp.logic_region in ONE_KONG_REGIONS:
        possible_warps = [x for x in possible_warps if list_of_custom_locations[x].logic_region not in ONE_KONG_REGIONS]
    for range in [1400, 1000, 800]:
        narrow_down = []
        for loc in possible_warps:
            warp_pad = list_of_custom_locations[loc]
            if (
                abs(abs(x - warp_pad.coords[0]) - abs(z - warp_pad.coords[2])) > range
                or abs(y - warp_pad.coords[1]) > 200
                or warp_pad.logic_region != region
                or warp_pad.logic_region not in klumped_regions
            ):
                narrow_down.append(loc)
        if len(narrow_down) > 8:
            possible_warps = narrow_down
            break
    return random.choice(possible_warps)


def EventToMap(event_id: Events) -> str:
    """Convert a warp event enum to a map name string."""
    if event_id < Events.JapesW1aTagged or event_id > Events.IslesW5bTagged:
        return None
    init_name = event_id.name
    for x in range(5):
        search_str = f"W{x + 1}"
        if search_str in init_name:
            return init_name.split(search_str)[0]
    return None


def EventToName(spoiler, event_id: Events) -> str:
    """Convert a warp event enum to a string."""
    if event_id < Events.JapesW1aTagged or event_id > Events.IslesW5bTagged:
        return None
    init_name = event_id.name
    for x in range(5):
        search_str = f"W{x + 1}"
        end_str = f"Warp {x + 1}"
        if search_str in init_name:
            if spoiler.settings.bananaport_placement_rando == ShufflePortLocations.half_vanilla:
                return end_str
            return f"{end_str} ({init_name.split(search_str)[1][0]})"
    return None


def ShufflePorts(spoiler, port_selection, human_ports):
    """Shuffle the location of bananaports."""
    port_list = spoiler.settings.warp_level_list_selected
    maps_to_check = [
        Maps.Isles,
        Maps.JungleJapes,
        Maps.AngryAztec,
        Maps.AztecLlamaTemple,
        Maps.FranticFactory,
        Maps.GloomyGalleon,
        Maps.FungiForest,
        Maps.CrystalCaves,
        Maps.CreepyCastle,
        Maps.CastleCrypt,
    ]
    if len(port_list) > 0:
        maps_to_check = port_list.copy()
    removePorts(spoiler, maps_to_check)
    BANNED_PORT_SHUFFLE_EVENTS = getBannedWarps(spoiler)
    for level in CustomLocations:
        level_lst = CustomLocations[level]
        for map in PortShufflerData:
            if PortShufflerData[map]["level"] == level and map in maps_to_check:
                index_lst = list(range(len(level_lst)))
                index_lst = [x for x in index_lst if isCustomLocationValid(spoiler, level_lst[x], map, level)]
                global_count = PortShufflerData[map]["global_warp_count"]
                start_event = PortShufflerData[map]["starting_warp"]
                end_event = start_event + PortShufflerData[map]["global_warp_count"]
                pick_count = global_count - len([x for x in BANNED_PORT_SHUFFLE_EVENTS if x >= start_event and x < end_event])
                if len(index_lst) < pick_count:
                    raise Exception(f"Insufficient custom location count for {map.name}. Expected: {pick_count}. Actual: {len(index_lst)}")
                pick_count = min(pick_count, len(index_lst))
                warps = []
                if spoiler.settings.useful_bananaport_placement and spoiler.settings.bananaport_placement_rando != ShufflePortLocations.vanilla_only:
                    spoiler.settings.random.shuffle(index_lst)
                    # Populate the region dict with custom locations in each region
                    region_dict = {}
                    for x in index_lst:
                        # Populate dict
                        if map == Maps.CreepyCastle:
                            # Castle is all 1 logic region, and it's usefulness is solely based on height
                            # As such, set the region as it's height component
                            y_val = level_lst[x].coords[1]
                            # Castle bottom = 400 (roughly), top is 2000 (roughly)
                            # 320 is deduced by (2000 - 400) / 5, splitting castle into 5 sections
                            region = int(y_val / 320)
                        else:
                            region = level_lst[x].logic_region
                            # Calculate the region based on klumping
                            for prop_region in REGION_KLUMPS:
                                if region in REGION_KLUMPS[prop_region]:
                                    region = prop_region
                                    break
                        if region not in region_dict:
                            region_dict[region] = []
                        region_dict[region].append(x)
                    # For all regions, push the first location in each region. Loop through regions repeatedly until warp list is filled
                    counter = pick_count
                    while counter > 0:
                        region_lst = [x for xi, x in enumerate(list(region_dict.keys())) if xi < counter]
                        for region in region_lst:
                            selected_warp = region_dict[region].pop(0)
                            warps.append(selected_warp)
                            counter -= 1
                        del_lst = []
                        for region in region_dict:
                            if len(region_dict[region]) == 0:  # delete any empty region
                                del_lst.append(region)
                        for region in del_lst:
                            del region_dict[region]
                else:
                    if spoiler.settings.bananaport_placement_rando == ShufflePortLocations.vanilla_only:
                        # Useful warps don't impact vanilla shuffle (yet). It's simpler and faster to just shuffle them
                        warps = index_lst.copy()
                        spoiler.settings.random.shuffle(warps)
                    else:
                        warps = spoiler.settings.random.sample(index_lst, pick_count)
                if pick_count > 0:
                    for k in BananaportVanilla:
                        event_id = BananaportVanilla[k].event
                        if event_id >= start_event and event_id < end_event and event_id not in BANNED_PORT_SHUFFLE_EVENTS:
                            if not (spoiler.settings.bananaport_placement_rando == ShufflePortLocations.on and spoiler.settings.useful_bananaport_placement):
                                selected_port = warps.pop(0)
                                port_selection[k] = selected_port
                            else:
                                populate_warp_event_pairs()
                                if warp_event_pairs[event_id] in BANNED_PORT_SHUFFLE_EVENTS or warp_event_pairs[event_id] in port_selection.keys():
                                    if warp_event_pairs[event_id] in port_selection.keys():
                                        warp = level_lst[port_selection[warp_event_pairs[event_id]]]
                                    else:
                                        warp = [x for x in level_lst if x.tied_warp_event == warp_event_pairs[event_id]][0]
                                    selected_port = selectUsefulWarpFullShuffle(spoiler.settings.random, level_lst, index_lst, warp)
                                    warps = [x for x in warps if x != selected_port]
                                    index_lst = [x for x in warps if x != selected_port]
                                    port_selection[k] = selected_port
                                else:
                                    selected_port = warps.pop(0)
                                    index_lst.remove(selected_port)
                                    port_selection[k] = selected_port
                            addPort(spoiler, level_lst[selected_port], event_id)
                            CustomLocations[level][selected_port].setCustomLocation(True)
                            map_name_spoiler = EventToMap(event_id)
                            if map_name_spoiler not in human_ports:
                                human_ports[map_name_spoiler] = {}
                            human_ports[map_name_spoiler][EventToName(spoiler, event_id)] = level_lst[selected_port].name
                            if len(warps) == 0:
                                break
