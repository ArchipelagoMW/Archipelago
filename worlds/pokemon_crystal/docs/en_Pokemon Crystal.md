# Pokémon Crystal

## Where is the options page?

You can read through all the options and generate a YAML [here](../player-options).

## What does randomization do to this game?

Some changes have been made to the logic for this randomizer:

- The cut tree in Ilex Forest has been removed
- The director is always in the underground warehouse, even when Radio Tower isn't occupied
- The card key door in Goldenrod Department Store B1F unlocks with the Card Key in your Pack
- Time based checks such as the Day of the Week siblings and the Celadon Mansion roof guy are always available
    - The hidden items under Freida and Wesley have been moved a tile across to remain accessible
- Clair gives the Rising Badge and TM24 after defeat, you don't need to go to Dragon's Den for these checks
- The Ship between Olivine and Vermilion is always present, even before entering Hall of Fame, and available to
  ride with the S.S. Ticket
- Magnet train between Goldenrod and Saffron is availble to ride with the Pass before power is restored to Kanto
- Misty is always in Cerulean Gym
- There is a ledge above the Route 2 entry to Digglet Cave, allowing you to reach the rest of West Kanto without Cut
- If the HM Badges Requirement option is set to `add_kanto`, HMs can be used with the following badges in addition to
  their vanilla badges:
    - HM01 Cut - Cascade Badge
    - HM02 Fly - Thunder Badge
    - HM03 Surf - Soul Badge
    - HM04 Strength - Rainbow Badge
    - HM05 Flash - Boulder Badge
    - HM06 Whirlpool - Volcano Badge
    - HM07 Waterfall - Earth Badge

## What items and locations get randomized?

By default, items from item balls, items given by NPCs, and gym badges are randomized.
If Johto Only mode is enabled, items in Kanto will not be randomized.

There are options to include more items in the pool:

- Randomize Hidden Items: Adds hidden items to the pool
- Randomize Pokegear: Adds the Pokegear and cards to the pool
- Randomize Berry Trees: Adds berry tree items to the pool
- Trainersanity: Adds a reward for beating trainers to the pool

## What other changes are made to the game?

Many additional quality of life changes have been implemented:

- A new text speed option, Instant, is added to the options menu in game. This speeds up text and allows holding A to
  quickly speed through dialog
- You can hold B to run
- Reduced long dialog in various places
- The Bicycle can be used indoors
- If a repel runs out and you have more in your Pack, it will prompt to use another
- You may advance to Violet City after speaking to Mr. Pokémon, without returning to New Bark Town first
- Pokémon growth rates are normalized (Medium-Fast for non-Legendary Pokémon, Slow for Legendary Pokémon)
- The clock reset password system has been removed, you can reset the clock with Down + Select + B on the title screen
- Trade evolutions have been changed to make them possible in a solo run of the game:
    - Regular trade evolutions now evolve at level 40
    - Held item trade evolutions evolve when their evolution item is used on them, as you would an evolution stone

## What does another world's item look like in Pokémon Crystal?

Items from other worlds will print the item name and the name of the receiving player when collected. Due to
limitations with the game's text, these names are truncated at 16 characters, and special characters not found in the
font are replaced with question marks.

## When the player receives an item, what happens?

A sound effect will play when an item is received if the Item Receive Sound option is enabled. Different sounds will
play to distinguish progression items and traps.

## Can I play offline?

Yes, the game does not need to be connected to the client for solo seeds. Connection is only required for sending and
receiving items.
