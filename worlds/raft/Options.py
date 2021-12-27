from Options import Range

class ResearchCostMultiplier(Range):
    """The amount of each research item required in the Research Table
	   to research a given technology"""
    displayname = "Research Cost Multiplier"
    range_start = 1
    range_end = 10
    default = 1

class ResourcePackMultiplier(Range):
    """This will multiply the amount of resources obtained from random
       resource drops"""
    displayname = "Resource Pack Multipler"
    range_start = 1
    range_end = 5
    default = 1


options = {
    "research_cost_multiplier": ResearchCostMultiplier,
    "resource_pack_multiplier": ResourcePackMultiplier
}
