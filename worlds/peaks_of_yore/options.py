from Options import Toggle, DefaultOnToggle, DeathLink, Choice, PerGameCommonOptions
from dataclasses import dataclass


class EnableFundamental(DefaultOnToggle):
    """Enables Fundamentals book, items and collectibles"""
    display_name = "Fundamental Peaks"


class EnableIntermediate(DefaultOnToggle):
    """Enables Intermediate book, items and collectibles"""
    display_name = "Intermediate Peaks"


class EnableAdvanced(DefaultOnToggle):
    """Enables Advanced book, items and collectibles"""
    display_name = "Advanced Peaks"


class EnableExpert(DefaultOnToggle):
    """Enables Expert book, items and collectibles"""
    display_name = "Expert Peaks"


class DisableSolemnTempest(DefaultOnToggle):
    """Removes Solemn Tempest from the locations pool, has no effect if \"Enable Expert Peaks\" is disabled"""
    display_name = "Disable Solemn Tempest"

@dataclass
class PeaksOfYoreOptions(PerGameCommonOptions):
    deathlink: DeathLink
    enable_fundamental: EnableFundamental
    enable_intermediate: EnableIntermediate
    enable_advanced: EnableAdvanced
    enable_expert: EnableExpert
    disable_solemn_tempest: DisableSolemnTempest
