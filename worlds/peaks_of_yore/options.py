from Options import Toggle, DefaultOnToggle, DeathLink, Choice, PerGameCommonOptions
from dataclasses import dataclass

class StartingBook(Choice):
    """Choose what book to start with. WARNING: Make sure your selected book is also enabled"""
    display_name = "Starting Book"
    option_fundamentals = 0
    option_intermediate = 1
    option_advanced = 2
    option_expert = 3
    default = 0

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
    starting_book: StartingBook
    enable_fundamental: EnableFundamental
    enable_intermediate: EnableIntermediate
    enable_advanced: EnableAdvanced
    enable_expert: EnableExpert
    disable_solemn_tempest: DisableSolemnTempest
