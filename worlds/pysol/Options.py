from Options import Choice, OptionDict, Option, DefaultOnToggle, Range

class NumGames(Range):
    range_end = 1100
options = {"initial_games": NumGames,"victory_number": NumGames}