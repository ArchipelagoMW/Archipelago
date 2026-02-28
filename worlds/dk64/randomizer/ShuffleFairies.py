"""File that shuffles fairies locations."""

from randomizer.Lists import Exceptions

from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Lists.FairyLocations import fairy_locations
from randomizer.LogicClasses import LocationLogic


class FairyPlacementInfo:
    """Stores information regarding the internal memory table of fairies."""

    def __init__(self, location: Locations, level: Levels, internal_level_index: int, id: int, shift: int = -1):
        """Initialize with given data."""
        self.location = location
        self.level = level
        self.internal_level_index = internal_level_index
        self.id = id
        self.shift = shift


all_fairy_locations = [
    Locations.JapesBananaFairyRambiCave,
    Locations.JapesBananaFairyLankyCave,
    Locations.AztecBananaFairyLlamaTemple,
    Locations.AztecBananaFairyTinyTemple,
    Locations.FactoryBananaFairybyFunky,
    Locations.FactoryBananaFairybyCounting,
    Locations.GalleonBananaFairybyCranky,
    Locations.GalleonBananaFairy5DoorShip,
    Locations.CavesBananaFairyIgloo,
    Locations.CavesBananaFairyCabin,
    Locations.ForestBananaFairyRafters,
    Locations.ForestBananaFairyThornvines,
    Locations.CastleBananaFairyBallroom,
    Locations.CastleBananaFairyTree,
    Locations.IslesBananaFairyFactoryLobby,
    Locations.IslesBananaFairyForestLobby,
    Locations.IslesBananaFairyIsland,
    Locations.IslesBananaFairyCrocodisleIsle,
    Locations.HelmBananaFairy1,
    Locations.HelmBananaFairy2,
]


def ShuffleFairyLocations(spoiler):
    """Pick 20 locations from various levels and place them into the correct logic areas and dictionaries."""
    spoiler.fairy_locations = {}
    spoiler.fairy_locations_human = {}
    spoiler.fairy_data_table = [None] * 20
    level_to_name = {
        Levels.DKIsles: "Isles",
        Levels.JungleJapes: "Japes",
        Levels.AngryAztec: "Aztec",
        Levels.FranticFactory: "Factory",
        Levels.GloomyGalleon: "Galleon",
        Levels.FungiForest: "Forest",
        Levels.CrystalCaves: "Caves",
        Levels.CreepyCastle: "Castle",
        Levels.HideoutHelm: "Helm",
    }
    if spoiler.settings.random_fairies:
        ClearFairyLogic(spoiler)
        fairy_data_table = [
            # HAS to remain in this order. DO NOT REORDER
            FairyPlacementInfo(Locations.JapesBananaFairyRambiCave, Levels.JungleJapes, 0, 51),
            FairyPlacementInfo(Locations.JapesBananaFairyLankyCave, Levels.JungleJapes, 1, 7, 0),
            FairyPlacementInfo(Locations.AztecBananaFairyLlamaTemple, Levels.AngryAztec, 0, 12),
            FairyPlacementInfo(Locations.AztecBananaFairyTinyTemple, Levels.AngryAztec, 1, 11),
            FairyPlacementInfo(Locations.FactoryBananaFairybyFunky, Levels.FranticFactory, 0, 92, 1),
            FairyPlacementInfo(Locations.FactoryBananaFairybyCounting, Levels.FranticFactory, 1, 85),
            FairyPlacementInfo(Locations.GalleonBananaFairybyCranky, Levels.GloomyGalleon, 0, 21, 2),
            FairyPlacementInfo(Locations.GalleonBananaFairy5DoorShip, Levels.GloomyGalleon, 1, 8),
            FairyPlacementInfo(Locations.CavesBananaFairyIgloo, Levels.CrystalCaves, 0, 3, 5),
            FairyPlacementInfo(Locations.CavesBananaFairyCabin, Levels.CrystalCaves, 1, 3, 6),
            FairyPlacementInfo(Locations.ForestBananaFairyRafters, Levels.FungiForest, 0, 2, 3),
            FairyPlacementInfo(Locations.ForestBananaFairyThornvines, Levels.FungiForest, 1, 2, 4),
            FairyPlacementInfo(Locations.CastleBananaFairyBallroom, Levels.CreepyCastle, 0, 5),
            FairyPlacementInfo(Locations.CastleBananaFairyTree, Levels.CreepyCastle, 1, 4),
            FairyPlacementInfo(Locations.IslesBananaFairyFactoryLobby, Levels.DKIsles, 0, 2, 7),
            FairyPlacementInfo(Locations.IslesBananaFairyForestLobby, Levels.DKIsles, 1, 1, 8),
            FairyPlacementInfo(Locations.IslesBananaFairyIsland, Levels.DKIsles, 2, 6),
            FairyPlacementInfo(Locations.IslesBananaFairyCrocodisleIsle, Levels.DKIsles, 3, 7),
            FairyPlacementInfo(Locations.HelmBananaFairy1, Levels.HideoutHelm, 0, 25),
            FairyPlacementInfo(Locations.HelmBananaFairy2, Levels.HideoutHelm, 1, 26),
        ]
        plando_dict = {
            Levels.JungleJapes: [],
            Levels.AngryAztec: [],
            Levels.FranticFactory: [],
            Levels.GloomyGalleon: [],
            Levels.FungiForest: [],
            Levels.CrystalCaves: [],
            Levels.CreepyCastle: [],
            Levels.DKIsles: [],
            Levels.HideoutHelm: [],
        }
        if spoiler.settings.enable_plandomizer and spoiler.settings.plandomizer_dict["plando_fairies"] != []:
            fillPlandoDict(plando_dict, spoiler.settings.plandomizer_dict["plando_fairies"])

        for level in fairy_locations:
            pick_size = 2
            if level == Levels.DKIsles:
                pick_size = 4
            usable_fairy_indexes = list(range(len(fairy_locations[level])))
            # Prevent double occurrences
            if len(plando_dict[level]) > 0:
                bad_location_names = [plando_dict[level]]
                usable_fairy_indexes = [x for x in usable_fairy_indexes if fairy_locations[level][x].name not in bad_location_names]

            selection = spoiler.settings.random.sample(usable_fairy_indexes, pick_size)
            # Give plandomizer an opportunity to have the final say
            for plando_fairy_selection in range(len(plando_dict[level])):
                if plando_dict[level][plando_fairy_selection] != -1:
                    selection_name = plando_dict[level][plando_fairy_selection]
                    selection_index_list = [fairy_locations[level].index(x) for x in fairy_locations[level] if x.name == selection_name]
                    if len(selection_index_list) == 0:
                        raise Exceptions.PlandoIncompatibleException(f'Fairy "{selection_name}" not found in {level}.')
                    else:
                        selection_index = selection_index_list[0]
                        selection[plando_fairy_selection] = selection_index
            human_selection = [fairy_locations[level][x].name for x in selection]
            spoiler.fairy_locations[level] = selection.copy()
            spoiler.fairy_locations_human[level.name] = human_selection
            # Placement into the table format, placement into logic
            vacant_slots = list(range(pick_size))
            for x in selection:
                slot = fairy_locations[level][x].natural_index
                if slot >= 0:
                    vacant_slots = [y for y in vacant_slots if y != slot]
            for x in selection:
                slot = fairy_locations[level][x].natural_index
                is_vanilla = True
                if slot < 0:
                    slot = vacant_slots.pop()
                    is_vanilla = False
                for index, data in enumerate(fairy_data_table):
                    if data.level == level and data.internal_level_index == slot:
                        # Data array in ROM
                        spoiler.fairy_data_table[index] = {
                            "fairy_index": x,
                            "level": level,
                            "flag": spoiler.LocationList[data.location].default_mapid_data[0].flag,
                            "id": -1 if not is_vanilla else data.id,
                            "shift": -1 if not is_vanilla else data.shift,
                        }
                        # Insert into logic
                        new_region = fairy_locations[level][x].region
                        spoiler.RegionList[new_region].locations.append(LocationLogic(data.location, fairy_locations[level][x].logic))
                        spoiler.LocationList[data.location].name = f"{level_to_name[level]} Fairy ({fairy_locations[level][x].name})"
                        # Resolve location-item combinations for plando
                        if len(plando_dict[level]) > 0:
                            for fairy in spoiler.settings.plandomizer_dict["plando_fairies"]:
                                if fairy["location"] == fairy_locations[level][x].name and fairy["reward"] != -1:
                                    spoiler.settings.plandomizer_dict["locations"][data.location] = fairy["reward"]


def ClearFairyLogic(spoiler):
    """Clear out any fairy locations in preparation for filling custom ones."""
    for id, region in spoiler.RegionList.items():
        region.locations = [loc for loc in region.locations if loc.id not in all_fairy_locations]


def fillPlandoDict(plando_dict: dict, plando_input):
    """Fill the plando_dict variable, using input from the plandomizer_dict."""
    for fairy in plando_input:
        if fairy["level"] != -1:
            plando_dict[fairy["level"]].append(fairy["location"])
