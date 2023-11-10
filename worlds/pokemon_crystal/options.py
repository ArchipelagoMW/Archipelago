from Options import Toggle, Choice


class RandomizeHiddenItems(Toggle):
    """Shuffles hidden items into the pool"""
    display_name = "Randomize Hidden Items"
    default = 0


class RandomizeStarters(Toggle):
    """Randomizes species of starter Pokemon"""
    display_name = "Randomize Starters"
    default = 1


class RandomizeWilds(Toggle):
    """Randomizes species of wild Pokemon"""
    display_name = "Randomize Wilds"
    default = 1


class RandomizeLearnsets(Choice):
    """start_with_four_moves: Random movesets with 4 starting moves
    randomize: Random movesets
    vanilla: Vanilla movesets"""
    display_name = "Randomize Learnsets"
    default = 0
    option_start_with_four_moves = 2
    option_randomize = 1
    option_vanilla = 0


class FullTmHmCompatibility(Toggle):
    """All Pokemon can learn any TM/HM"""
    display_name = "Full TM/HM Compatibility"
    default = 0


class BlindTrainers(Toggle):
    """Trainers have no vision and will not start battles unless interacted with"""
    display_name = "Blind Trainers"
    default = 0


class BetterMarts(Toggle):
    """Improves the selection of items at Pokemarts"""
    display_name = "Better Marts"
    default = 0


class Goal(Choice):
    """Elite Four: collect 8 badges and enter the Hall of Fame
        Red: collect 16 badges and defeat Red at Mt. Silver"""
    display_name = "Goal"
    default = 0
    option_elite_four = 0
    option_red = 1


pokemon_crystal_options = {
    "randomize_hidden_items": RandomizeHiddenItems,
    "randomize_starters": RandomizeStarters,
    "randomize_wilds": RandomizeWilds,
    "randomize_learnsets": RandomizeLearnsets,
    "full_tmhm_compatibility": FullTmHmCompatibility,
    "blind_trainers": BlindTrainers,
    "better_marts": BetterMarts,
    "goal": Goal
}
