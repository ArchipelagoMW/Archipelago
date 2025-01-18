import typing
from dataclasses import dataclass
from Options import DeathLink, PerGameCommonOptions

# Python hates it when you try to make an empty ChecksFinderOptions.
# Whether you are inheriting from PerGameCommonOptions or PerGameCommonOptions + DeathLinkMixin.
# Until ChecksFinder has a unique additional option, DeathLink has to be added as like this instead of DeathLinkMixin.
class ChecksFinderDeathLink(DeathLink):
    __doc__ = DeathLink.__doc__ + "\n\n    Good Luck!"

@dataclass
class ChecksFinderOptions(PerGameCommonOptions):
    death_link: ChecksFinderDeathLink
