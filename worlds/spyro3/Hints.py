from BaseClasses import ItemClassification

hint_location_names = [
    "Icy Peak: Protect Nancy the skater. (Cerny)",
    "Enchanted Towers: Collect the bones. (Ralph)",
    "Enchanted Towers: All Gems",
    "Spooky Swamp: Escort the twins II. (Michele)",
    "Country Speedway: Race the pigs. (Shemp)",
    "Country Speedway: Hunter's rescue mission. (Roberto)",
    "Sgt. Byrd's Base: All Gems",
    "Lost Fleet: Skate race Hunter. (Aiden)",
    "Lost Fleet: Sink the subs II. (Dolores)",
    "Frozen Altars: Box the yeti again! (Ricco)",
    "Frozen Altars: Catch the ice cats. (Ba'ah)",
    "Fireworks Factory: You're still doomed! (Donovan)",
    "Fireworks Factory: Bad dragon! (Evan)",
    "Charmed Ridge: Cat witch chaos. (Abby)",
    "Charmed Ridge: Jack and the beanstalk II. (Chuck)",
    "Honey Speedway: Race the bees (Henri)",
    "Crystal Islands: Whack a mole. (Hank)",
    "Crystal Islands: All Gems",
    "Haunted Tomb: Tank blast II. (TJ)",
    "Haunted Tomb: Clear the caves. (Roxy)",
    "Dino Mines: Hit all the seahorses (Skill Point)",
    "Harbor Speedway: Race the blue footed boobies. (Jessie)"
]


def generateHints(player_slot, number_of_hints, s3_world):
    hints = {}
    location_hints = []
    progression_hints = []

    # fuzz.py fails when this is declared in a higher scope, since it is not reloaded before each run
    # and items are removed from it when generating seeds.
    joke_hints = [
        "Zoe says that, when you see a ladder, or walls that look climbable, jump onto it, and you'll grab it with your claws!",
        "Zoe says that you should just come back if you want some boarding tips from the master.",
        "Zoe says that she just bought some insta-sprout-ultra-super-grow seeds from a bear with a bag of gems.",
        "Zoe says that flaming metal enemies is probably a mistake.",
        "Zoe says that this game would be easier if you could double jump like in Spyro 2.",
        "Zoe says that there's an egg at the bottom of the lake in Sunrise Spring Home, unless you've already found it.",
        "Zoe says that the seal outside Seashell Shore has one of the cutest voice lines in the game. Yay!",
        "Zoe says that 6 people on the leaderboards have completed the Mushroom Speedway butterfly race in under 90 seconds. Can you?",
        "Zoe says that if you're charging nearby as a gem spawns, it will generally auto-collect as if you charged a basket or enemy.",
        "Zoe says that the True Sparxless option is probably not a good idea with gem checks.",
        "Zoe says that if you headbash the exact center of a headbash crate, you may bounce off instead of breaking it.",
        "Zoe says that it is possible to die during each skateboarding challenge, but you probably don't want to.",
        "Zoe says that holding both strafe buttons makes Sgt. Byrd move more quickly.",
        "Zoe says that by holding/mashing the correct buttons in Agent 9's Lab, you can fly from the end of the level to the start.",
        "Zoe says that in Fireworks Factory, it's possible to play the Agent 9 challenges as Spyro.",
        "Zoe says that there are ways to swim in the air in each of the first 3 homeworlds.",
        "Zoe says that you missed a gem earlier.",
        "Zoe says that the denizens of Crystal Islands are merely conjurers of cheap tricks.",
        "Zoe says that Sgt. Byrd's tactical instincts are to drop ammo where Spike can pick it up.",
        "Zoe says that red rockets are better for beating Scorch than green ones.",
        "Zoe says that you can jump twice to glide.",
        "Zoe says that Hunter can be found in Sunrise Spring home, even while he has been captured by the Sorceress.",
        "Zoe says that doing a full backflip, then a twisted lemon or lime, is a good trick for skateboarding.",
        "Zoe says that it is possible to rescue Farley in Enchanted Towers without ever using his rubber ball.",
        "Zoe says that it is possible to skip paying Moneybags entirely.",
        "Zoe says that it is possible to skip talking to her in this location.",
        "Zoe says that the maximum flying speed is different in each speedway."
    ]

    for location in s3_world.multiworld.get_filled_locations():
        if location.player == player_slot:
            # we are the sender of the location check
            if location.name in hint_location_names:
                location_hints.append((f"Zoe says that '{location.name}' contains a {location.item.name} for player {location.item.player}", location.address))
            # Remove progression events and fixed goal items, since "Sunny Villa Complete: Sunny Villa Complete"
            # is not a helpful (or valid) hint.
            elif location.item.classification == ItemClassification.progression and \
                    'Complete' not in location.item.name and \
                    'Defeated' not in location.item.name and \
                    location.item.name != 'Skill Point':
                progression_hints.append((f"Zoe says that '{location.name}' contains a {location.item.name} for player {location.item.player}", location.address))

    # Generate 3 types of hints - hints around difficult/slow/annoying checks, hints around progression items, and joke hints.
    # These are equally balanced as much as possible, prioritizing location hints over progression and progression over joke.
    # If number_of_hints is 11, the distribution is always 4-4-3.
    # In the future, we may consider rebalancing or allowing players to change the distribution, as in Ocarina of Time.
    for i in range(int(number_of_hints / 3)):
        location_hint = s3_world.random.choice(location_hints)
        location_hints.remove(location_hint)
        progression_hint = s3_world.random.choice(progression_hints)
        progression_hints.remove(progression_hint)
        joke_hint = s3_world.random.choice(joke_hints)
        joke_hints.remove(joke_hint)
        # The client expects each hint to have 2 parts - text to display, plus the ID of the location to
        # generate a free hint for (or -1 if no hint is needed)
        hints[f"Hint {3 * i + 1} Text"] = location_hint[0]
        hints[f"Hint {3 * i + 1} ID"] = f"{location_hint[1]}"
        hints[f"Hint {3 * i + 2} Text"] = progression_hint[0]
        hints[f"Hint {3 * i + 2} ID"] = f"{progression_hint[1]}"
        hints[f"Hint {3 * i + 3} Text"] = joke_hint
        hints[f"Hint {3 * i + 3} ID"] = "-1"

    if number_of_hints % 3 != 0:
        location_hint = s3_world.random.choice(location_hints)
        location_hints.remove(location_hint)
        hints[f"Hint {int(number_of_hints / 3) * 3 + 1} Text"] = location_hint[0]
        hints[f"Hint {int(number_of_hints / 3) * 3 + 1} ID"] = f"{location_hint[1]}"
    if number_of_hints % 3 == 2:
        progression_hint = s3_world.random.choice(progression_hints)
        progression_hints.remove(progression_hint)
        hints[f"Hint {int(number_of_hints / 3) * 3 + 2} Text"] = progression_hint[0]
        hints[f"Hint {int(number_of_hints / 3) * 3 + 2} ID"] = f"{progression_hint[1]}"

    return hints
