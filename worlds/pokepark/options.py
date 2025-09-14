from dataclasses import dataclass
from typing import Any

from Options import PerGameCommonOptions, Choice, OptionGroup, Range, Toggle


class Powers(Choice):
    """
    Determines how Power Items are shuffled into the pool.
    Full: Start with all Power Items
    Thunderbolt: Start with one Thunderbolt Power
    Dash: Start with one Dash Power
    ThunderboltDash: Start with one Thunderbolt and Dash Power (Default)
    None: Start with no Powers (Thunderbolt and Dash unusable)
    """
    display_name = "Powers"
    option_full = 0
    option_thunderbolt = 1
    option_dash = 2
    option_thunderbolt_dash = 3
    option_none = 4
    default = 3


class RandomStartingZones(Choice):
    """
    Determines Starting Zone
    None: Start with only Meadow Zone (Default)
    One: Start with one random Fast Travel
    All: Start with Fast Travel to all Zones
    """
    display = "Starting Zone"
    option_none = 0
    option_one = 1
    option_all = 2
    default = 0


class Goal(Choice):
    """
    Determines World completion condition
    Mew: Beat Mew (Default)
    postgame: Complete the postgame Prisma check (needs all friends)
    """
    display = "Goal Condition"
    option_mew = 0
    option_postgame = 1


class NumRequiredBattleCount(Range):
    """
    Select the number of required consecutive Wins to challenge Battle count Pokemon
    """
    display = "Number of Battle Count"
    range_start = 0
    range_end = 10
    default = 5


class NumRequiredPrismaCountSkygarden(Range):
    """
    Select the number of required Prisma Shards to enter Skygarden
    """
    display = "Number of Battle Count"
    range_start = 1
    range_end = 14
    default = 14


class RemoveBattlePowerCompLocations(Toggle):
    """
    Removing Battle Power Competition Locations. These are not sending items anymore, but can still be used for
    gaining berries.
    """
    default = False


class RemoveChasePowerCompLocations(Toggle):
    """
    Removing Chase Power Competition Locations. These are not sending items anymore, but can still be used for
    gaining berries.
    """
    default = False


class RemoveQuizPowerCompLocations(Toggle):
    """
    Removing Quiz Power Competition Locations. These are not sending items anymore, but can still be used for
    gaining berries.
    """
    default = True


class RemoveHideAndSeekPowerCompLocations(Toggle):
    """
    Removing Hide and Seek Power Competition Locations. These are not sending items anymore, but can still be used for
    gaining berries.
    """
    default = False


class RemoveErrandPowerCompLocations(Toggle):
    """
    Removing Errand Power Competition Locations. These are not sending items anymore, but can still be used for
    gaining berries.
    """
    default = False


class RemoveMiscPowerCompLocations(Toggle):
    """
    Removing Miscellaneous Power Competition Locations. These are not sending items anymore, but can still be used for
    gaining berries.
    """
    default = False


class RemovePowerUpLocations(Toggle):
    """
    Removing Power Training Locations. e.g. Thunderbolt Upgrade Training at Electabuzz
    """
    default = False


class RemoveQuestLocations(Toggle):
    """
    Removing Quest Locations e.g. Bidoof Housing.
    """
    default = False


class RemoveAttractionLocations(Toggle):
    """
    Removes non prisma clear Attraction Locations.
    """
    default = True


class RemoveAttractionPrismaLocations(Toggle):
    """
    Removes Attraction Prisma clear location
    """
    default = False


class RemovePokemonUnlockLocations(Toggle):
    """
    Removes Pokemon Unlock Locations
    """
    default = False


class RandomizeAttractionEntrances(Toggle):
    """
    Randomizes Attraction Entrances
    """
    default = False

class EachZone(Toggle):
    """
    Pokemon that are in multiple Zones become additional Locations. e.g. Bonsly (Meadow, Cavern, Magma Zone)
    (not implemented, still generating)
    """
    default = False


class InZoneRoadBlocks(Toggle):
    """
    Additional Road Blocks inside the Zones e.g. Beach Zone Bridges as items
    """
    default = True

@dataclass
class PokeparkOptions(PerGameCommonOptions):
    power_randomizer: Powers
    starting_zone: RandomStartingZones
    goal: Goal
    num_required_battle_count: NumRequiredBattleCount
    each_zone: EachZone
    remove_battle_power_comp_locations: RemoveBattlePowerCompLocations
    remove_chase_power_comp_locations: RemoveChasePowerCompLocations
    remove_quiz_power_comp_locations: RemoveQuizPowerCompLocations
    remove_hide_and_seek_power_comp_locations: RemoveHideAndSeekPowerCompLocations
    remove_errand_power_comp_locations: RemoveErrandPowerCompLocations
    remove_misc_power_comp_locations: RemoveMiscPowerCompLocations
    remove_power_training_locations: RemovePowerUpLocations
    remove_quest_locations: RemoveQuestLocations
    remove_attraction_locations: RemoveAttractionLocations
    remove_attraction_prisma_locations: RemoveAttractionPrismaLocations
    remove_pokemon_unlock_locations: RemovePokemonUnlockLocations
    num_required_prisma_count_skygarden: NumRequiredPrismaCountSkygarden
    in_zone_road_blocks: InZoneRoadBlocks
    randomize_attraction_entrances: RandomizeAttractionEntrances

    def get_output_dict(self) -> dict[str, Any]:
        """
        Returns a dictionary of option name to value to be placed in
        the output pprk file.

        :return: Dictionary of option name to value for the output file.
        """

        # Note: these options' values must be able to be passed through
        # `yaml.safe_dump`.
        return self.as_dict(
            "num_required_battle_count",
            "num_required_prisma_count_skygarden"
        )


pokepark_option_groups = [
    OptionGroup("Goal", [
        Goal
    ]),
    OptionGroup("Misc", [
        Powers,
        RandomStartingZones,
        NumRequiredBattleCount
    ])
]
