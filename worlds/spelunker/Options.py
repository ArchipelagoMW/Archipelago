from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, PerGameCommonOptions


class HiddenLocs(Toggle):
    """Places items on the secret invisible item locations."""
    display_name = "Hidden Item Checks"

class CaveLevel(Choice):
    """This will determine the color palette of the cave you venture though."""
    display_name = "Cave Palette"
    option_cave_1 = 0
    option_cave_2 = 1
    option_cave_3 = 2
    option_cave_4 = 3
    default = 0
#NOT IMPLEMENTED
#class EnergyLink(Toggle):
  #  """Enables Energy Link. If enabled, you can hold the Select button to refill your energy from the pool.
   #    A specified percent of energy received from refills will be put into the pool."""
    #display_name = "Energy Link"

#class EnergyLinkPercent(Range):
 #   """Specifies how much energy from """
  #  display_name = "Energy Link Percent"
   # range_start = 1
    #range_end = 100
    #default = 50

@dataclass
class SpelunkerOptions(PerGameCommonOptions):
    hidden_items: HiddenLocs
    cave_color: CaveLevel
    #energy_link: EnergyLink
    #energy_link_percent: EnergyLinkPercent
    death_link: DeathLink
