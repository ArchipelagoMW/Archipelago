from Options import Range

class ResearchCostMultiplier(Range):
    """The amount of each research item required in the Research Table
	   to research a given technology"""
    displayname = "Research Cost Multiplier"
    range_start = 1
    range_end = 10
    default = 1


options = {
    "research_cost_multiplier": ResearchCostMultiplier
}
