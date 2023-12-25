from dataclasses import dataclass
from Options import Toggle, DeathLink, Range, PerGameCommonOptions

class RequiredArtifacts(Range):
    """How many Artifacts are required to finish"""
    display_name = "Required Artifacts"
    range_start = 0
    range_end = 45
    default = 25

class ComputerChecks(Toggle):
    """If enabled, places checks on the Computer data locations"""
    display_name = "Computer Checks"

class CityShuffle(Toggle):
    """Shuffles which doors lead to which cities"""
    display_name = "City Shuffle"

@dataclass
class MarioisMissingOptions(PerGameCommonOptions):
    required_artifacts: RequiredArtifacts
    computer_sanity: ComputerChecks
    city_shuffle: CityShuffle
    death_link: DeathLink
