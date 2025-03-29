from dataclasses import dataclass
from Options import DeathLinkMixin, PerGameCommonOptions

@dataclass
class ChecksFinderOptions(PerGameCommonOptions, DeathLinkMixin):
    pass
