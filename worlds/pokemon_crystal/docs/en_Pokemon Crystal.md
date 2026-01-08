# Pokémon Crystal

## What does randomization do to this game?

Some changes have been made to the base game for this randomizer:

- The trainer battle on Route 30 is resolved as soon as you talk to Mr. Pokémon, skipping a visit to Professor Elm
- The director is always in the underground warehouse, even when Radio Tower isn't occupied
- The card key door in Goldenrod Department Store B1F unlocks with the Card Key in your Pack
- Time based checks such as the Day of the Week siblings and the Celadon Mansion roof guy are always available
    - The hidden items under Freida and Wesley have been moved a tile across to remain accessible
- The Ship between Olivine and Vermilion is always present in non-Johto-Only-games, even before entering Hall of Fame,
  and available to ride with the S.S. Ticket
- Misty is always in Cerulean Gym
- A ledge on Route 45 has been moved so all items and trainers can be accessed in 2 passthroughs
- For options which enable it, the Kanto badges map to the following HMs:
    - HM01 Cut - Cascade Badge
    - HM02 Fly - Thunder Badge
    - HM03 Surf - Soul Badge
    - HM04 Strength - Rainbow Badge
    - HM05 Flash - Boulder Badge
    - HM06 Whirlpool - Volcano Badge
    - HM07 Waterfall - Earth Badge
- TM02 and TM08 will always be Headbutt and Rock Smash respectively, and are always reusable
- Trade evolutions have been changed to make them possible in a solo run of the game:
    - Regular trade evolutions now evolve at level 37
    - Held item trade evolutions evolve when their evolution item is used on them, as you would an evolution stone
- Eevee evolves into Espeon and Umbreon with the Sun Stone and Moon Stone respectively
- Happiness evolutions are logically tied to access to the Goldenrod Underground or Pallet Town. The younger haircut
  brother and Daisy will max out a Pokémon's happiness and are always available
- Unown will only appear in the wild after solving one puzzle in the Ruins of Alph. Prior to that, any encounter that
  would have been Unown will instead play its cry
- Tin Tower 1F is accessible once you obtain the Clear Bell.
- Tin Tower 2F+ is accessible once the aforementioned condition is met, and you have the Rainbow Wing. Both are items in
  the multiworld
- Eusine will give you an Eon Mail if you talk to him in Tin Tower 1F after seeing Suicune in the overworld at all
  possible locations, which you can visit in any order
- The Celebi Event can be activated by giving the multiworld item GS-Ball to Kurt after clearing Slowpoke Well and
  defeating the rival in Azalea
- The event which usually grants the GS Ball in Goldenrod Pokécenter 1F activates after becoming champion
- The man who gives a reward for having all badges in Vermilion City only checks for the 8 Kanto badges
- The Ruins of Alph Ho-Oh item chamber is accessible by owning the Rainbow Wing
- A shop has been added to 2F of all Pokémon Centers, you can customise what this shop sells using the `build_a_mart`
  option, the shop will always sell Poké Balls and Escape Ropes
- An NPC which allows you to fight a random wild Pokémon has been added to 2F of all Pokémon Centers, this fight awards
  money and exp, but does not grant Pokédex entries and is not catchable

## What items and locations get randomized?

By default, items from item balls and items given by NPCs are randomized.
Badges can be either vanilla, shuffled or randomized. Pokégear and its card modules can be vanilla or randomized.
If Johto Only mode is enabled, items in Kanto will not be randomized and Kanto will be inaccessible.
The S.S. Ticket given by Elm after beating the Elite 4 will also be replaced by the Silver Wing.

There are options to include more items in the pool:

- Randomize Hidden Items: Adds hidden items to the pool
- Randomize Berry Trees: Adds berry tree items to the pool
- Trainersanity: Adds a reward for beating trainers to the pool
- Dexsanity: A Pokémon's Dex entry can hold a check. This is tied to specific Pokémon
- Dexcountsanity: A certain amount of Dex entries hold checks. This is not tied to specific Pokémon but a total
- Shopsanity: Includes shop items in the pool
- Grasssanity: Cutting every grass tile is a location
- Bug Catching Contest: Shuffles prizes for the bug catching contest, from participating to winning
- Randomize Pokémon Requests: Adds Bill's Grandpa's rewards and the Lake of Rage Magikarp prize to the pool
- Randomize Phone Calls: Adds items from trainer phone calls to the pool

## What other changes are made to the game?

Many additional quality of life changes have been implemented:

- A new text speed option, Instant, is added to the options menu in game.
- The A and/or B buttons can be used as turbo buttons to speed through dialogues
- When battle scenes are turned off, HP reduction and XP gain animations are skipped
- The Battle Scene option is more granular, with the fastest choice, Speedy, cutting nearly every animation
- You can hold B to run. An Auto-run option also exists, and if enabled, B prevents you from running
- Many other options were added to drastically speed up gameplay, including: Rods can always work, Uncaught Pokémon can
  be more likely to appear, Trainers can be blind, etc.
- Lag in menus has been removed
- The Bicycle can be used indoors
- The Escape Rope can be used in more interiors, such as Gyms
- If a repel runs out and you have more in your Pack, you will be prompted to use another
- Pokémon growth rates are normalized (Medium-Fast for non-Legendary Pokémon, Slow for Legendary Pokémon)
- The clock reset password system has been removed, you can reset the clock with Down + Select + B on the title screen
- An in-game option for not requiring Field Moves to be taught was added. To keep Fly, Flash, and other Field Moves
  accessible, an additional menu is made available by pressing Select on the Start Menu
- You can respawn all static events by talking to the Time Capsule person in the second floor of any PokéCenter
- You can teleport back to your starting town by selecting "Go Home" in the main menu before you load into the
  overworld

## What does another world's item look like in Pokémon Crystal?

Items from other worlds will print the item name and the name of the receiving player when collected. Due to
limitations with the game's text, these names are truncated at 16 characters, and special characters not found in the
font are replaced with question marks.

## When the player receives an item, what happens?

A sound effect will play when an item is received if the Item Receive Sound option is enabled. Different sounds will
play to distinguish progression items and traps.

## Can I play offline?

Yes, the game does not need to be connected to the client for solo seeds. Connection is only required for sending and
receiving items. This does not apply when `remote_items` is enabled.
