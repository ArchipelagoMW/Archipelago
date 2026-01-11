
# Options checklist:

# version:
#   always random
# goal:
#   default ghetsis
#   each other has its own test
# randomize_wild_pokemon:
#   default []
#   one test for all modifiers
#   11 tests for "Randomize" + random selection of other modifiers
# randomize_trainer_pokemon:
#   default []
#   one test for just "Randomize"
#   one test for both
# pokemon_randomization_adjustments:
#   default {"Stats leniency": 10}
#   other values irrelevant
#   no other parameters so far
# encounter_plando:
#   default []
#   one test for multiple plandos with all different parameter variations
#   one test for two plandos + randomize_wild_pokemon = ["Randomize"]
#   one test for two plandos + randomize_wild_pokemon = ["Randomize", "Ensure all obtainable"]
# shuffle_badges:
#   default shuffle
#   each other has its own test
# shuffle_tm_hm:
#   default shuffle
#   each other has its own test
# dexsanity:
#   default 0
#   one test for 100
#   one test for 649 + randomize_wild_pokemon = ["Randomize", "Ensure all obtainable"]
# season_control:
#   default vanilla
#   each other has its own test
# modify_encounter_rates:
#   default vanilla
#   one test for each other choice each
#   one test for custom rates
# modify_item_pool:
#   default []
#   one test for all modifiers combined
# modify_logic:
#   default ["Require Dowsing Machine", "Prioritize key item locations"]
#   one test for []
# reusable_tms:
#   too complex to test
